#!/usr/bin/env python3
"""
validate-design.py — Валидация документов проектирования SDD.

Проверяет соответствие документа проектирования стандарту standard-design.md.
Документ содержит секции SVC-N (Ответственность, Компоненты, Зависимости),
блоки INT-N (Контракт, Sequence) и системные тест-сценарии STS-N.

Использование:
    python validate-design.py <path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-design.py specs/design/design-0001-oauth2-service-design.md
    python validate-design.py --all
    python validate-design.py --json specs/design/design-0001-oauth2-service-design.md

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

FILENAME_REGEX = re.compile(r'^design-(\d{4})-(.+)\.md$')
HEADING_REGEX = re.compile(r'^# design-(\d{4}):\s+(.+)$', re.MULTILINE)

VALID_STATUSES = {
    "DRAFT", "WAITING", "RUNNING", "DONE",
    "CONFLICT", "ROLLING_BACK", "REJECTED",
}

REQUIRED_STANDARD = "specs/.instructions/design/standard-design.md"
REQUIRED_INDEX = "specs/design/README.md"
STANDARD_VERSION_REGEX = re.compile(r'^v\d+\.\d+$')

PARENT_PATH_REGEX = re.compile(r'^impact/impact-\d{4}-.+\.md$')

# Паттерны секций
SVC_SECTION_PATTERN = re.compile(r'^##\s+SVC-(\d+):\s+(.+)$', re.MULTILINE)
INT_SECTION_PATTERN = re.compile(r'^##\s+INT-(\d+):\s+(.+)$', re.MULTILINE)

# Элементы с нумерацией
ELEMENT_PATTERNS = {
    "SVC": (re.compile(r'^##\s+SVC-(\d+):', re.MULTILINE), "D016"),
    "CMP": (re.compile(r'^\|\s*CMP-(\d+)\s*\|', re.MULTILINE), "D017"),
    "INT": (re.compile(r'^##\s+INT-(\d+):', re.MULTILINE), "D018"),
    "STS": (re.compile(r'^\|\s*STS-(\d+)\s*\|', re.MULTILINE), "D019"),
}

# Заглушки для подсекций SVC
SVC_SUBSECTION_STUBS = {
    "Компоненты": re.compile(r'_Компоненты наследуются из Impact без изменений\._'),
    "Зависимости": re.compile(r'_Внешних зависимостей нет\._'),
}

# Заглушка для тест-сценариев
STS_STUB = re.compile(r'_Системных тест-сценариев нет\._')

ERROR_CODES = {
    "D001": "Неверный формат имени файла",
    "D002": "Отсутствует description",
    "D003": "Неверный standard",
    "D004": "Невалидный status",
    "D005": "Отсутствует parent",
    "D006": "Parent не существует",
    "D007": "Отсутствует раздел 'Резюме'",
    "D008": "Нет секций SVC-N",
    "D009": "Подсекция 'Ответственность' отсутствует в SVC",
    "D010": "Подсекция 'Компоненты' отсутствует в SVC",
    "D011": "Подсекция 'Зависимости' отсутствует в SVC",
    "D012": "Нет блоков INT-N (при > 1 сервиса)",
    "D013": "Подсекция 'Контракт' отсутствует в INT",
    "D014": "Подсекция 'Sequence' отсутствует в INT",
    "D015": "Отсутствует 'Системные тест-сценарии'",
    "D016": "Дублирование SVC-N",
    "D017": "Дублирование CMP-N",
    "D018": "Дублирование INT-N",
    "D019": "Дублирование STS-N",
    "D020": "Маркер [ТРЕБУЕТ УТОЧНЕНИЯ] при статусе > DRAFT",
    "D021": "Dependency Barrier при статусе > DRAFT",
    "D022": "Детали реализации (→ ADR)",
    "D023": "Нет записи в README",
    "D024": "Рассинхрон статуса (README ≠ frontmatter)",
    "D025": "NNNN в имени файла ≠ NNNN в заголовке",
    "D026": "Отсутствуют метаданные SVC",
    "D027": "Нет описания ответственности",
    "D028": "Ответственность пуста",
    "D029": "Контракт пуст",
    "D030": "Sequence пуст",
    "D031": "Резюме пустое/placeholder",
    "D032": "Milestone не совпадает",
    "D033": "NNNN ≠ parent NNNN",
    "D034": "Нарушен порядок SVC",
    "D035": "SVC не ссылается на INT",
    "D036": "Косвенный сервис имеет SVC",
    "D037": "Отклонённый без обоснования",
    "D038": "Внутрисервисные детали в контракте",
    "D039": "Given/When/Then в STS",
    "D040": "Метаданные INT отсутствуют",
}


# =============================================================================
# Общие функции
# =============================================================================

def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def parse_frontmatter(content: str) -> dict:
    """Извлечь frontmatter из markdown."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    result = {}
    current_key = None
    list_values = []

    for line in match.group(1).split('\n'):
        if line.strip().startswith('- ') and current_key:
            list_values.append(line.strip()[2:])
            result[current_key] = list_values
            continue

        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if value == '[]':
                result[key] = []
                current_key = key
                list_values = []
            elif value == '' or value is None:
                current_key = key
                list_values = []
                result[key] = value
            else:
                result[key] = value
                current_key = key
                list_values = []

    return result


def remove_code_blocks(content: str) -> str:
    """Убрать блоки кода из содержимого."""
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', '', content)
    return content


def get_body(content: str) -> str:
    """Получить тело документа без frontmatter."""
    return re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)


def get_section_text(body: str, heading_pattern: str) -> str | None:
    """Извлечь текст h2 секции по паттерну заголовка."""
    pattern = r'^##\s+' + heading_pattern + r'\s*\n(.*?)(?=^##\s|\Z)'
    match = re.search(pattern, body, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


def get_svc_section_text(body: str, svc_num: str) -> str | None:
    """Извлечь текст секции SVC-N."""
    pattern = r'^##\s+SVC-' + re.escape(svc_num) + r':.*?\n(.*?)(?=^##\s|\Z)'
    match = re.search(pattern, body, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


def get_int_section_text(body: str, int_num: str) -> str | None:
    """Извлечь текст блока INT-N."""
    pattern = r'^##\s+INT-' + re.escape(int_num) + r':.*?\n(.*?)(?=^##\s|\Z)'
    match = re.search(pattern, body, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


def get_subsection_text(section_text: str, subsection_name: str) -> str | None:
    """Извлечь текст h3 подсекции."""
    pattern = r'^###\s+(?:\S+\s+)?' + re.escape(subsection_name) + r'\s*\n(.*?)(?=^###\s|\Z)'
    match = re.search(pattern, section_text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


# =============================================================================
# Проверки
# =============================================================================

def extract_file_nnnn(path: Path) -> str | None:
    """Извлечь NNNN из имени файла design-NNNN-topic.md."""
    m = FILENAME_REGEX.match(path.name)
    return m.group(1) if m else None


def check_filename(path: Path) -> list[tuple[str, str]]:
    """D001: Проверить формат имени файла."""
    errors = []
    if not FILENAME_REGEX.match(path.name):
        errors.append(("D001", f"Имя '{path.name}' не соответствует design-NNNN-topic.md"))
    return errors


def check_frontmatter(content: str, repo_root: Path) -> list[tuple[str, str]]:
    """D002-D006, D032: Проверить frontmatter."""
    errors = []

    if not content.startswith("---\n"):
        errors.append(("D002", "Отсутствует frontmatter"))
        return errors

    fm = parse_frontmatter(content)

    # D002: description
    desc = fm.get("description", "")
    if not desc:
        errors.append(("D002", "Отсутствует поле description"))
    elif len(desc) > 1024:
        errors.append(("D002", f"Description {len(desc)} символов (макс. 1024)"))

    # D003: standard
    standard = fm.get("standard", "")
    if standard != REQUIRED_STANDARD:
        errors.append(("D003", f"standard = '{standard}', ожидается '{REQUIRED_STANDARD}'"))

    # standard-version
    sv = fm.get("standard-version", "")
    if not sv:
        errors.append(("D003", "Отсутствует поле standard-version"))
    elif not STANDARD_VERSION_REGEX.match(sv):
        errors.append(("D003", f"standard-version = '{sv}', ожидается формат vX.Y"))

    # D004: status
    status = fm.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(("D004", f"status = '{status}', допустимые: {', '.join(sorted(VALID_STATUSES))}"))

    # D005: parent обязателен
    parent = fm.get("parent", "")
    if not parent:
        errors.append(("D005", "Отсутствует поле parent (обязательно для Design)"))
    else:
        if not PARENT_PATH_REGEX.match(parent):
            errors.append(("D005", "Неверный формат parent: ожидается impact/impact-NNNN-topic.md"))
        # D006: parent существует
        parent_path = repo_root / "specs" / parent
        if not parent_path.exists():
            errors.append(("D006", f"Parent не найден: specs/{parent}"))

    # index
    index = fm.get("index", "")
    if index != REQUIRED_INDEX:
        errors.append(("D003", f"index = '{index}', ожидается '{REQUIRED_INDEX}'"))

    # milestone
    if not fm.get("milestone"):
        errors.append(("D032", "Отсутствует поле milestone"))

    return errors


def check_heading(content: str, path: Path) -> list[tuple[str, str]]:
    """D025: Проверить совпадение NNNN в имени файла и заголовке."""
    errors = []

    file_nnnn = extract_file_nnnn(path)
    if not file_nnnn:
        return errors
    body = get_body(content)
    heading_match = HEADING_REGEX.search(body)

    if not heading_match:
        errors.append(("D025", "Заголовок '# design-NNNN: Тема' не найден"))
        return errors

    heading_nnnn = heading_match.group(1)
    if file_nnnn != heading_nnnn:
        errors.append(("D025", f"NNNN в файле ({file_nnnn}) ≠ NNNN в заголовке ({heading_nnnn})"))

    return errors


def check_required_sections(content: str) -> list[tuple[str, str]]:
    """D007-D015: Проверить обязательные разделы."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # D007: Резюме
    resume_pattern = r'^##\s+(?:📋\s+)?Резюме'
    if not re.search(resume_pattern, body_no_code, re.MULTILINE):
        errors.append(("D007", "Отсутствует раздел '## 📋 Резюме'"))

    # D008: Минимум 1 секция SVC-N
    svc_sections = SVC_SECTION_PATTERN.findall(body_no_code)
    if not svc_sections:
        errors.append(("D008", "Нет секций SVC-N (минимум 1 обязательна)"))
    else:
        # D009-D011: Проверить подсекции в каждой SVC
        for svc_num, svc_name in svc_sections:
            svc_text = get_svc_section_text(body_no_code, svc_num)
            if svc_text is None:
                continue

            # D009: Ответственность
            resp_pattern = r'###\s+(?:📋\s+)?Ответственность'
            if not re.search(resp_pattern, svc_text, re.MULTILINE):
                errors.append(("D009", f"SVC-{svc_num} ({svc_name.strip()}): отсутствует '📋 Ответственность'"))

            # D010: Компоненты
            comp_pattern = r'###\s+(?:📦\s+)?Компоненты'
            if not re.search(comp_pattern, svc_text, re.MULTILINE):
                errors.append(("D010", f"SVC-{svc_num} ({svc_name.strip()}): отсутствует '📦 Компоненты'"))

            # D011: Зависимости
            dep_pattern = r'###\s+(?:🔗\s+)?Зависимости'
            if not re.search(dep_pattern, svc_text, re.MULTILINE):
                errors.append(("D011", f"SVC-{svc_num} ({svc_name.strip()}): отсутствует '🔗 Зависимости'"))

    # D012: INT-N (если > 1 сервиса)
    int_sections = INT_SECTION_PATTERN.findall(body_no_code)
    if len(svc_sections) > 1 and not int_sections:
        errors.append(("D012", "Нет блоков INT-N (обязательно при > 1 сервиса)"))

    # D013-D014: Проверить подсекции в каждом INT
    for int_num, int_name in int_sections:
        int_text = get_int_section_text(body_no_code, int_num)
        if int_text is None:
            continue

        # D013: Контракт
        if not re.search(r'###\s+Контракт', int_text, re.MULTILINE):
            errors.append(("D013", f"INT-{int_num} ({int_name.strip()}): отсутствует 'Контракт'"))

        # D014: Sequence
        if not re.search(r'###\s+Sequence', int_text, re.MULTILINE):
            errors.append(("D014", f"INT-{int_num} ({int_name.strip()}): отсутствует 'Sequence'"))

    # D015: Системные тест-сценарии
    sts_pattern = r'^##\s+(?:🧪\s+)?Системные тест-сценарии'
    if not re.search(sts_pattern, body_no_code, re.MULTILINE):
        errors.append(("D015", "Отсутствует раздел '## 🧪 Системные тест-сценарии'"))

    return errors


def check_section_content(content: str) -> list[tuple[str, str]]:
    """D026-D031, D039-D040: Проверить содержание секций."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # D031: Резюме — не пустое и не placeholder
    resume_text = get_section_text(body_no_code, r'(?:📋\s+)?Резюме')
    if resume_text is not None:
        resume_stripped = resume_text.strip()
        if not resume_stripped or '{Краткое описание' in resume_text:
            errors.append(("D031", "Резюме пустое или содержит только placeholder"))

    # Проверить каждую SVC
    svc_sections = SVC_SECTION_PATTERN.findall(body_no_code)
    for svc_num, svc_name in svc_sections:
        svc_text = get_svc_section_text(body_no_code, svc_num)
        if svc_text is None:
            continue

        # D026: Метаданные SVC (Impact → Design решение)
        if not re.search(r'\*\*Impact:\*\*.*\|\s*\*\*Решение Design:\*\*', svc_text):
            errors.append(("D026", f"SVC-{svc_num}: отсутствуют метаданные '**Impact:** ... | **Решение Design:**'"))

        # D028: Ответственность заполнена
        resp_text = get_subsection_text(svc_text, "Ответственность")
        if resp_text is not None:
            has_bullets = bool(re.search(r'^-\s+\S', resp_text, re.MULTILINE))
            if not has_bullets:
                errors.append(("D028", f"SVC-{svc_num}: подсекция 'Ответственность' без bullet list"))

        # D010 content: Компоненты — контент или заглушка
        comp_text = get_subsection_text(svc_text, "Компоненты")
        if comp_text is not None:
            has_cmp = bool(re.search(r'CMP-\d+', comp_text))
            has_stub = bool(SVC_SUBSECTION_STUBS["Компоненты"].search(comp_text))
            if not has_cmp and not has_stub and '{Компонент}' not in comp_text:
                errors.append(("D010", f"SVC-{svc_num}: 'Компоненты' без контента и без заглушки"))

        # D011 content: Зависимости — контент или заглушка
        dep_text = get_subsection_text(svc_text, "Зависимости")
        if dep_text is not None:
            has_int_ref = bool(re.search(r'INT-\d+', dep_text))
            has_stub = bool(SVC_SUBSECTION_STUBS["Зависимости"].search(dep_text))
            if not has_int_ref and not has_stub and '{INT-N' not in dep_text:
                errors.append(("D035", f"SVC-{svc_num}: 'Зависимости' не ссылается на INT-N"))

    # Проверить каждый INT
    int_sections = INT_SECTION_PATTERN.findall(body_no_code)
    for int_num, int_name in int_sections:
        int_text_no_code = get_int_section_text(body_no_code, int_num)
        int_text_with_code = get_int_section_text(body, int_num)

        if int_text_no_code is None:
            continue

        # D040: Метаданные INT
        has_participants = bool(re.search(r'\*\*Участники:\*\*', int_text_no_code))
        has_pattern = bool(re.search(r'\*\*Паттерн:\*\*', int_text_no_code))
        if not has_participants or not has_pattern:
            errors.append(("D040", f"INT-{int_num}: отсутствуют метаданные (Участники/Паттерн)"))

        # D029: Контракт не пуст
        contract_text = get_subsection_text(int_text_no_code, "Контракт")
        if contract_text is not None:
            contract_stripped = contract_text.strip()
            if not contract_stripped or '{Спецификация' in contract_text:
                errors.append(("D029", f"INT-{int_num}: 'Контракт' пуст или placeholder"))

        # D030: Sequence не пуст (проверяем в int_text_with_code)
        if int_text_with_code is not None:
            seq_text = get_subsection_text(int_text_with_code, "Sequence")
            if seq_text is not None:
                if not re.search(r'sequenceDiagram', seq_text):
                    errors.append(("D030", f"INT-{int_num}: 'Sequence' без mermaid sequenceDiagram"))

    # D039: STS без Given/When/Then
    sts_text = get_section_text(body_no_code, r'(?:🧪\s+)?Системные тест-сценарии')
    if sts_text is not None:
        if re.search(r'\b(Given|When|Then)\b', sts_text):
            errors.append(("D039", "Тест-сценарии содержат Given/When/Then (→ Plan тестов)"))

    return errors


def check_numbering(content: str) -> list[tuple[str, str]]:
    """D016-D019: Проверить уникальность нумерации."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    for prefix, (pattern, error_code) in ELEMENT_PATTERNS.items():
        numbers = []
        for m in pattern.finditer(body_no_code):
            num = m.group(1)
            if num:
                numbers.append(num)

        seen = set()
        for num in numbers:
            if num in seen:
                errors.append((error_code, f"Дубликат {prefix}-{num}"))
            seen.add(num)

    return errors


def check_markers_and_status(content: str) -> list[tuple[str, str]]:
    """D020-D021: Проверить маркеры при статусе > DRAFT."""
    errors = []

    fm = parse_frontmatter(content)
    status = fm.get("status", "DRAFT")

    if status in ("DRAFT", ""):
        return errors

    body = get_body(content)

    # D020: маркеры
    markers = re.findall(r'\[ТРЕБУЕТ УТОЧНЕНИЯ[^\]]*\]', body)
    if markers:
        errors.append(("D020", f"Найдено {len(markers)} маркеров при статусе {status}"))

    # D021: Dependency Barrier
    if '⛔ DEPENDENCY BARRIER' in body or 'DEPENDENCY BARRIER' in body:
        errors.append(("D021", f"Dependency Barrier при статусе {status}"))

    return errors


def check_readme_registration(path: Path, content: str, repo_root: Path) -> list[tuple[str, str]]:
    """D023-D024: Проверить регистрацию в README."""
    errors = []

    readme_path = repo_root / "specs" / "design" / "README.md"
    if not readme_path.exists():
        errors.append(("D023", f"README не найден: {readme_path}"))
        return errors

    try:
        readme_content = readme_path.read_text(encoding='utf-8')
    except Exception:
        errors.append(("D023", "Ошибка чтения README"))
        return errors

    file_stem = path.stem
    if file_stem not in readme_content and path.name not in readme_content:
        errors.append(("D023", f"Запись '{path.name}' не найдена в README"))
        return errors

    # D024: синхронность статуса
    fm = parse_frontmatter(content)
    fm_status = fm.get("status", "")

    if fm_status:
        table_pattern = re.compile(
            rf'\|[^|]*\|[^|]*{re.escape(path.name)}[^|]*\|[^|]*({"|".join(VALID_STATUSES)})[^|]*\|',
            re.IGNORECASE
        )
        table_match = table_pattern.search(readme_content)
        if not table_match:
            table_pattern2 = re.compile(
                rf'\|[^|]*\|[^|]*{re.escape(file_stem)}[^|]*\|[^|]*({"|".join(VALID_STATUSES)})[^|]*\|',
                re.IGNORECASE
            )
            table_match = table_pattern2.search(readme_content)

        if table_match:
            readme_status = table_match.group(1).strip()
            if readme_status != fm_status:
                errors.append(("D024", f"Статус в README ({readme_status}) ≠ frontmatter ({fm_status})"))

    return errors


def check_number_matches_parent(path: Path, content: str) -> list[tuple[str, str]]:
    """D033: Проверить совпадение NNNN Design с NNNN parent Discussion (через Impact)."""
    errors = []

    file_nnnn = extract_file_nnnn(path)
    if not file_nnnn:
        return errors

    fm = parse_frontmatter(content)
    parent = fm.get("parent", "")
    if not parent:
        return errors

    parent_match = re.search(r'impact-(\d{4})', parent)
    if not parent_match:
        return errors

    parent_nnnn = parent_match.group(1)

    if file_nnnn != parent_nnnn:
        errors.append(("D033", f"NNNN Design ({file_nnnn}) ≠ NNNN parent Impact ({parent_nnnn})"))

    return errors


def check_milestone_match(content: str, repo_root: Path) -> list[tuple[str, str]]:
    """D032: Проверить совпадение milestone Design с milestone parent Impact."""
    errors = []

    fm = parse_frontmatter(content)
    parent = fm.get("parent", "")
    if not parent:
        return errors

    parent_path = repo_root / "specs" / parent
    if not parent_path.exists():
        return errors

    try:
        parent_content = parent_path.read_text(encoding='utf-8')
    except Exception:
        return errors

    parent_fm = parse_frontmatter(parent_content)
    design_milestone = fm.get("milestone", "")
    parent_milestone = parent_fm.get("milestone", "")

    if design_milestone and parent_milestone and design_milestone != parent_milestone:
        errors.append(("D032", f"Milestone Design ({design_milestone}) ≠ milestone parent ({parent_milestone})"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_design(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать один документ проектирования."""
    errors = []

    if not path.exists():
        return [("D001", f"Файл не найден: {path}")]

    errors.extend(check_filename(path))

    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [("D001", f"Ошибка чтения файла: {e}")]

    errors.extend(check_frontmatter(content, repo_root))
    errors.extend(check_heading(content, path))
    errors.extend(check_required_sections(content))
    errors.extend(check_section_content(content))
    errors.extend(check_numbering(content))
    errors.extend(check_markers_and_status(content))
    errors.extend(check_readme_registration(path, content, repo_root))
    errors.extend(check_milestone_match(content, repo_root))
    errors.extend(check_number_matches_parent(path, content))

    return errors


def find_all_designs(repo_root: Path) -> list[Path]:
    """Найти все документы проектирования."""
    design_dir = repo_root / "specs" / "design"
    if not design_dir.exists():
        return []

    return sorted(design_dir.glob("design-*.md"))


def format_output(path: Path, errors: list[tuple[str, str]], as_json: bool) -> str:
    """Форматировать вывод."""
    if as_json:
        return json.dumps({
            "file": str(path),
            "valid": len(errors) == 0,
            "errors": [{"code": code, "message": msg} for code, msg in errors]
        }, ensure_ascii=False, indent=2)

    if not errors:
        return f"✅ {path.name} — валидация пройдена"

    lines = [f"❌ {path.name} — {len(errors)} ошибок:"]
    for code, msg in errors:
        lines.append(f"   {code}: {msg}")
    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация документов проектирования SDD"
    )
    parser.add_argument("path", nargs="?", help="Путь к документу проектирования")
    parser.add_argument("--all", action="store_true", help="Проверить все документы проектирования")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if args.all:
        designs = find_all_designs(repo_root)
        if not designs:
            print("Документы проектирования не найдены")
            sys.exit(0)
    elif args.path:
        designs = [Path(args.path)]
    else:
        parser.print_help()
        sys.exit(2)

    all_valid = True
    results = []

    for path in designs:
        errors = validate_design(path, repo_root)
        if errors:
            all_valid = False

        output = format_output(path, errors, args.json)
        results.append(output)

    if args.json:
        print("[" + ",\n".join(results) + "]")
    else:
        print("\n".join(results))

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
