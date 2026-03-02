#!/usr/bin/env python3
"""
validate-analysis-design.py — Валидация документов проектирования SDD.

Проверяет соответствие документа проектирования стандарту standard-design.md.

Использование:
    python validate-analysis-design.py <path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-analysis-design.py specs/analysis/0001-oauth2-authorization/design.md
    python validate-analysis-design.py --all
    python validate-analysis-design.py --json specs/analysis/0001-oauth2-authorization/design.md

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

FOLDER_REGEX = re.compile(r'^(\d{4})-.+$')
HEADING_REGEX = re.compile(r'^# (\d{4}):\s+(.+?)\s*—\s*Design\s*$', re.MULTILINE)

VALID_STATUSES = {
    "DRAFT", "WAITING", "RUNNING", "REVIEW", "DONE",
    "CONFLICT", "ROLLING_BACK", "REJECTED",
}

REQUIRED_STANDARD = "specs/.instructions/analysis/design/standard-design.md"
REQUIRED_INDEX = "specs/analysis/README.md"
STANDARD_VERSION_REGEX = re.compile(r'^v\d+\.\d+$')

SVC_HEADING_REGEX = re.compile(r'^## SVC-(\d+):\s+(.+)$', re.MULTILINE)
INT_HEADING_REGEX = re.compile(r'^## INT-(\d+):\s+(.+)$', re.MULTILINE)
STS_ROW_REGEX = re.compile(r'^\|\s*STS-(\d+)\s*\|', re.MULTILINE)

SVC_SUBSECTIONS = [
    "1. Назначение",
    "2. API контракты",
    "3. Data Model",
    "4. Потоки",
    "5. Code Map",
    "6. Зависимости",
    "7. Доменная модель",
    "8. Границы автономии LLM",
    "9. Решения по реализации",
]

SVC_STUBS = {
    "2. API контракты": re.compile(r'_Нет изменений в API\._'),
    "3. Data Model": re.compile(r'_Нет изменений в Data Model\._'),
    "4. Потоки": re.compile(r'_Нет изменений в потоках\._'),
    "5. Code Map": re.compile(r'_Нет изменений в Code Map\._'),
    "6. Зависимости": re.compile(r'_Нет изменений в зависимостях\._'),
    "7. Доменная модель": re.compile(r'_Нет изменений в доменной модели\._'),
    "8. Границы автономии LLM": re.compile(r'_Нет изменений в границах автономии\._'),
}

DELTA_MARKER_REGEX = re.compile(r'\*\*(ADDED|MODIFIED|REMOVED)[:\s]', re.MULTILINE)
DELTA_SUBSECTIONS = {"2. API контракты", "3. Data Model", "4. Потоки",
                     "5. Code Map", "6. Зависимости", "7. Доменная модель"}

ERROR_CODES = {
    "DES001": "Неверное расположение файла",
    "DES002": "Отсутствует description",
    "DES003": "Неверный standard",
    "DES004": "Невалидный status",
    "DES005": "Отсутствует parent",
    "DES006": "Parent Discussion не существует",
    "DES007": "Milestone не совпадает с parent",
    "DES008": "Отсутствует Резюме",
    "DES009": "Нет секции SVC-N",
    "DES010": "SVC-N: отсутствует подсекция",
    "DES011": "SVC-N: § 1 пуст",
    "DES012": "SVC-N: § 9 пуст",
    "DES013": "SVC-N: нет описания",
    "DES014": "SVC-N: нет Решение:",
    "DES015": "INT-N отсутствует при 2+ сервисах",
    "DES016": "INT-N: нет метаданных",
    "DES017": "INT-N: нет Контракта",
    "DES018": "INT-N: нет Sequence",
    "DES019": "Нет Системные тест-сценарии",
    "DES020": "Дублирование SVC-N",
    "DES021": "Дублирование INT-N",
    "DES022": "Дублирование STS-N",
    "DES023": "Delta-формат: нет маркеров",
    "DES024": "Маркер при статусе > DRAFT",
    "DES025": "Dependency Barrier при статусе > DRAFT",
    "DES026": "Зона: бизнес-обоснование",
    "DES027": "Зона: unit-тесты",
    "DES028": "Зона: задачи",
    "DES029": "NNNN не совпадает",
    "DES030": "Description слишком длинное",
    "DES031": "INT-N осиротевший",
    "DES032": "8:8 маппинг: названия не совпадают",
    "DES033": "Нет секции Выбор технологий",
    "DES034": "Выбор технологий без Выбрано",
    "DES035": "Нарушен порядок секций",
    "DES036": "Code Map: двойная вложенность src/",
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
                # Parse YAML scalar types
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
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


def get_section_text(body: str, heading_pattern: str, next_h2: bool = True) -> str:
    """Извлечь текст секции до следующего h2."""
    match = re.search(heading_pattern, body, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    if next_h2:
        next_match = re.search(r'^## ', body[start:], re.MULTILINE)
        if next_match:
            return body[start:start + next_match.start()]
    return body[start:]


# =============================================================================
# Проверки
# =============================================================================

def check_location(path: Path) -> list[tuple[str, str]]:
    """DES001: Проверить расположение файла."""
    errors = []

    if path.name != "design.md":
        errors.append(("DES001", f"Имя файла '{path.name}', ожидается 'design.md'"))
        return errors

    parent_name = path.parent.name
    if not FOLDER_REGEX.match(parent_name):
        errors.append(("DES001", f"Папка '{parent_name}' не соответствует формату NNNN-{{topic}}"))

    return errors


def check_frontmatter(content: str, path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """DES002-DES007, DES030: Проверить frontmatter."""
    errors = []

    if not content.startswith("---\n"):
        errors.append(("DES002", "Отсутствует frontmatter"))
        return errors

    fm = parse_frontmatter(content)

    # DES002: description
    desc = fm.get("description", "")
    if not desc:
        errors.append(("DES002", "Отсутствует поле description"))
    elif len(desc) > 1024:
        errors.append(("DES030", f"Description {len(desc)} символов (макс. 1024)"))

    # DES003: standard
    standard = fm.get("standard", "")
    if standard != REQUIRED_STANDARD:
        errors.append(("DES003", f"standard = '{standard}', ожидается '{REQUIRED_STANDARD}'"))

    # standard-version
    sv = fm.get("standard-version", "")
    if not sv:
        errors.append(("DES003", "Отсутствует поле standard-version"))
    elif not STANDARD_VERSION_REGEX.match(sv):
        errors.append(("DES003", f"standard-version = '{sv}', ожидается формат vX.Y"))

    # DES004: status
    status = fm.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(("DES004", f"status = '{status}', допустимые: {', '.join(sorted(VALID_STATUSES))}"))

    # DES005: parent обязателен
    parent = fm.get("parent", "")
    if not parent:
        errors.append(("DES005", "Отсутствует поле parent (обязательно для Design)"))
    else:
        # DES006: parent существует
        parent_path = path.parent / parent
        if not parent_path.exists():
            errors.append(("DES006", f"Parent Discussion не найден: {parent_path}"))
        else:
            # DES007: milestone совпадает
            try:
                parent_content = parent_path.read_text(encoding='utf-8')
                parent_fm = parse_frontmatter(parent_content)
                parent_milestone = parent_fm.get("milestone", "")
                design_milestone = fm.get("milestone", "")
                if parent_milestone and design_milestone and parent_milestone != design_milestone:
                    errors.append(("DES007",
                                   f"Milestone '{design_milestone}' ≠ parent '{parent_milestone}'"))
            except Exception:
                pass

    # index
    index = fm.get("index", "")
    if index != REQUIRED_INDEX:
        errors.append(("DES003", f"index = '{index}', ожидается '{REQUIRED_INDEX}'"))

    # milestone
    if not fm.get("milestone"):
        errors.append(("DES007", "Отсутствует поле milestone"))

    # docs-synced (опционально, если присутствует — boolean true)
    if "docs-synced" in fm:
        val = fm["docs-synced"]
        if not isinstance(val, bool):
            errors.append(("DES030", f"docs-synced должен быть boolean, получено: {type(val).__name__}"))

    return errors


def check_heading(content: str, path: Path) -> list[tuple[str, str]]:
    """DES029: Проверить совпадение NNNN и суффикс — Design."""
    errors = []

    folder_match = FOLDER_REGEX.match(path.parent.name)
    if not folder_match:
        return errors

    folder_nnnn = folder_match.group(1)
    body = get_body(content)
    heading_match = HEADING_REGEX.search(body)

    if not heading_match:
        errors.append(("DES029", "Заголовок '# NNNN: {Тема} — Design' не найден"))
        return errors

    heading_nnnn = heading_match.group(1)
    if folder_nnnn != heading_nnnn:
        errors.append(("DES029", f"NNNN в папке ({folder_nnnn}) ≠ NNNN в заголовке ({heading_nnnn})"))

    theme = heading_match.group(2).strip()
    if len(theme) > 80:
        errors.append(("DES029", f"Тема ({len(theme)} символов) превышает 80 символов"))

    return errors


def check_required_sections(content: str) -> list[tuple[str, str]]:
    """DES008-DES009, DES015, DES019, DES033-DES035: Проверить обязательные разделы."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # DES008: Резюме
    if not re.search(r'^## Резюме', body_no_code, re.MULTILINE):
        errors.append(("DES008", "Отсутствует раздел '## Резюме'"))

    # DES033: Выбор технологий
    has_tech_choice = bool(re.search(r'^## Выбор технологий', body_no_code, re.MULTILINE))
    if not has_tech_choice:
        errors.append(("DES033", "Отсутствует раздел '## Выбор технологий' (обязателен между Резюме и SVC-1)"))

    # DES034: минимум 1 "Выбрано" в секции Выбор технологий
    if has_tech_choice:
        tech_section = get_section_text(body_no_code, r'^## Выбор технологий')
        if tech_section:
            # Проверяем "Выбрано:" с непустым значением (не плейсхолдер)
            chosen = re.findall(r'\*\*Выбрано:\*\*\s*(.+)', tech_section)
            real_chosen = [c for c in chosen if c.strip() and '[ТРЕБУЕТ УТОЧНЕНИЯ]' not in c
                          and not c.strip().startswith('_') and not c.strip().startswith('{')]
            # Также проверяем однострочный формат подтверждения
            confirmed = re.findall(r'Технологический стек подтверждён', tech_section)
            if not real_chosen and not confirmed:
                errors.append(("DES034", "Секция 'Выбор технологий' не содержит ни одного заполненного 'Выбрано'"))

    # DES009: минимум 1 SVC-N
    svc_matches = SVC_HEADING_REGEX.findall(body_no_code)
    if not svc_matches:
        errors.append(("DES009", "Нет ни одной секции SVC-N"))

    # DES015: INT-N при 2+ сервисах
    int_matches = INT_HEADING_REGEX.findall(body_no_code)
    if len(svc_matches) > 1 and not int_matches:
        errors.append(("DES015", f"{len(svc_matches)} сервисов, но нет секции INT-N"))

    # DES019: Системные тест-сценарии
    if not re.search(r'^## Системные тест-сценарии', body_no_code, re.MULTILINE):
        errors.append(("DES019", "Отсутствует раздел '## Системные тест-сценарии'"))

    # DES035: проверить порядок секций
    errors.extend(_check_section_order(body_no_code, has_tech_choice))

    return errors


def _check_section_order(body_no_code: str, has_tech_choice: bool) -> list[tuple[str, str]]:
    """DES035: Проверить порядок секций."""
    errors = []

    # Собрать позиции ключевых секций
    sections_order = []
    for pattern, name in [
        (r'^## Резюме', 'Резюме'),
        (r'^## Выбор технологий', 'Выбор технологий'),
        (r'^## SVC-\d+:', 'SVC-N'),
        (r'^## INT-\d+:', 'INT-N'),
        (r'^## Системные тест-сценарии', 'STS'),
        (r'^## Предложения', 'Предложения'),
        (r'^## Отвергнутые предложения', 'Отвергнутые предложения'),
    ]:
        match = re.search(pattern, body_no_code, re.MULTILINE)
        if match:
            sections_order.append((match.start(), name))

    sections_order.sort(key=lambda x: x[0])
    ordered_names = [name for _, name in sections_order]

    # Ожидаемый порядок (только присутствующие)
    expected = ['Резюме', 'Выбор технологий', 'SVC-N', 'INT-N', 'STS',
                'Предложения', 'Отвергнутые предложения']
    expected_present = [s for s in expected if s in ordered_names]

    # Проверить что фактический порядок совпадает с ожидаемым
    actual_filtered = [s for s in ordered_names if s in expected_present]
    if actual_filtered != expected_present:
        errors.append(("DES035",
                       f"Порядок секций нарушен: {' → '.join(actual_filtered)}, "
                       f"ожидается: {' → '.join(expected_present)}"))

    return errors


def check_svc_sections(content: str) -> list[tuple[str, str]]:
    """DES010-DES014, DES023: Проверить подсекции SVC-N."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # Найти все SVC-N секции
    svc_starts = [(m.start(), m.group(1), m.group(2))
                  for m in SVC_HEADING_REGEX.finditer(body_no_code)]

    for i, (start, svc_num, svc_name) in enumerate(svc_starts):
        # Определить конец секции
        if i + 1 < len(svc_starts):
            end = svc_starts[i + 1][0]
        else:
            # Искать следующий ## (INT-N или Системные тест-сценарии)
            next_h2 = re.search(r'^## (?!SVC-)', body_no_code[start + 1:], re.MULTILINE)
            end = start + 1 + next_h2.start() if next_h2 else len(body_no_code)

        svc_text = body_no_code[start:end]
        prefix = f"SVC-{svc_num}"

        # DES013: описание (1-2 абзаца перед первой ###)
        first_h3 = re.search(r'^### ', svc_text, re.MULTILINE)
        if first_h3:
            desc_area = svc_text[len(f"## SVC-{svc_num}: {svc_name}"):first_h3.start()].strip()
            if len(desc_area) < 10:
                errors.append(("DES013", f"{prefix}: описание слишком короткое или отсутствует"))

            # DES014: содержит **Решение:**
            if '**Решение:**' not in desc_area and '**Решение: ' not in svc_text[:first_h3.start()]:
                errors.append(("DES014", f"{prefix}: нет '**Решение:**' в описании"))
        else:
            errors.append(("DES013", f"{prefix}: нет подсекций (### не найден)"))
            continue

        # DES010: все 9 подсекций
        for subsection in SVC_SUBSECTIONS:
            pattern = rf'^### {re.escape(subsection)}\s*$'
            if not re.search(pattern, svc_text, re.MULTILINE):
                errors.append(("DES010", f"{prefix}: отсутствует подсекция '### {subsection}'"))

        # DES011: § 1 Назначение — контент обязателен
        sec1_text = _get_subsection_text(svc_text, "1. Назначение", SVC_SUBSECTIONS)
        if sec1_text is not None and len(sec1_text.strip()) < 10:
            errors.append(("DES011", f"{prefix}: § 1 'Назначение' пуст или слишком короткий"))

        # DES012: § 9 Решения по реализации — контент обязателен
        sec9_text = _get_subsection_text(svc_text, "9. Решения по реализации", SVC_SUBSECTIONS)
        if sec9_text is not None and len(sec9_text.strip()) < 10:
            errors.append(("DES012", f"{prefix}: § 9 'Решения по реализации' пуст"))

        # DES023: Delta-формат в §§ 2-7
        for subsection in SVC_SUBSECTIONS[1:7]:  # §§ 2-7
            sub_text = _get_subsection_text(svc_text, subsection, SVC_SUBSECTIONS)
            if sub_text is None:
                continue
            sub_text_stripped = sub_text.strip()
            if not sub_text_stripped:
                continue
            # Проверить заглушку
            stub = SVC_STUBS.get(subsection)
            if stub and stub.search(sub_text_stripped):
                continue
            # Есть контент — должны быть маркеры
            if not DELTA_MARKER_REGEX.search(sub_text_stripped):
                errors.append(("DES023",
                               f"{prefix}: § '{subsection}' имеет контент без маркеров ADDED/MODIFIED/REMOVED"))

        # DES036: Code Map — двойная вложенность src/
        codemap_text = _get_subsection_text(svc_text, "5. Code Map", SVC_SUBSECTIONS)
        if codemap_text:
            codemap_stripped = codemap_text.strip()
            stub = SVC_STUBS.get("5. Code Map")
            if not (stub and stub.search(codemap_stripped)):
                # Ищем паттерн src/{svc}/src/ в путях
                double_src = re.findall(r'src/\w+/src/', codemap_stripped)
                if double_src:
                    errors.append(("DES036",
                                   f"{prefix}: § 5 Code Map содержит двойную вложенность "
                                   f"src/ ({double_src[0]}...) — конвенция монорепо: src/{{svc}}/ без вложенного src/"))

    return errors


def _get_subsection_text(svc_text: str, subsection: str,
                         all_subsections: list[str]) -> str | None:
    """Извлечь текст подсекции из SVC-N."""
    pattern = rf'^### {re.escape(subsection)}\s*$'
    match = re.search(pattern, svc_text, re.MULTILINE)
    if not match:
        return None

    start = match.end()

    # Найти следующую подсекцию или конец SVC
    idx = all_subsections.index(subsection) if subsection in all_subsections else -1
    if idx >= 0 and idx + 1 < len(all_subsections):
        next_sub = all_subsections[idx + 1]
        next_pattern = rf'^### {re.escape(next_sub)}\s*$'
        next_match = re.search(next_pattern, svc_text[start:], re.MULTILINE)
        if next_match:
            return svc_text[start:start + next_match.start()]

    # До конца секции или следующего ##
    next_h2 = re.search(r'^## ', svc_text[start:], re.MULTILINE)
    if next_h2:
        return svc_text[start:start + next_h2.start()]

    return svc_text[start:]


def check_int_sections(content: str) -> list[tuple[str, str]]:
    """DES016-DES018, DES031: Проверить INT-N секции."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    int_starts = [(m.start(), m.group(1), m.group(2))
                  for m in INT_HEADING_REGEX.finditer(body_no_code)]

    for i, (start, int_num, int_name) in enumerate(int_starts):
        if i + 1 < len(int_starts):
            end = int_starts[i + 1][0]
        else:
            next_h2 = re.search(r'^## (?!INT-)', body_no_code[start + 1:], re.MULTILINE)
            end = start + 1 + next_h2.start() if next_h2 else len(body_no_code)

        int_text = body_no_code[start:end]
        prefix = f"INT-{int_num}"

        # DES016: метаданные
        if '**Участники:**' not in int_text:
            errors.append(("DES016", f"{prefix}: отсутствует '**Участники:**'"))
        if '**Паттерн:**' not in int_text:
            errors.append(("DES016", f"{prefix}: отсутствует '**Паттерн:**'"))

        # DES017: Контракт
        if not re.search(r'^### Контракт', int_text, re.MULTILINE):
            errors.append(("DES017", f"{prefix}: отсутствует '### Контракт'"))

        # DES018: Sequence с mermaid
        if not re.search(r'^### Sequence', int_text, re.MULTILINE):
            errors.append(("DES018", f"{prefix}: отсутствует '### Sequence'"))

    # DES031: осиротевшие INT-N (проверка через § 6)
    body_full = get_body(content)
    for _, int_num, _ in int_starts:
        pattern = rf'INT-{int_num}\b'
        # Ищем в секциях SVC (§ 6 Зависимости)
        svc_refs = re.findall(pattern, body_full)
        # Минус собственное упоминание в заголовке INT-N
        if len(svc_refs) <= 1:
            errors.append(("DES031", f"INT-{int_num} не упомянут в § 6 ни одного SVC-N"))

    return errors


def check_numbering(content: str) -> list[tuple[str, str]]:
    """DES020-DES022: Проверить уникальность нумерации."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # SVC-N
    svc_nums = SVC_HEADING_REGEX.findall(body_no_code)
    seen_svc = set()
    for num, _ in svc_nums:
        if num in seen_svc:
            errors.append(("DES020", f"Дубликат SVC-{num}"))
        seen_svc.add(num)

    # INT-N
    int_nums = INT_HEADING_REGEX.findall(body_no_code)
    seen_int = set()
    for num, _ in int_nums:
        if num in seen_int:
            errors.append(("DES021", f"Дубликат INT-{num}"))
        seen_int.add(num)

    # STS-N
    sts_nums = STS_ROW_REGEX.findall(body_no_code)
    seen_sts = set()
    for num in sts_nums:
        if num in seen_sts:
            errors.append(("DES022", f"Дубликат STS-{num}"))
        seen_sts.add(num)

    return errors


def check_markers_and_status(content: str) -> list[tuple[str, str]]:
    """DES024-DES025: Проверить маркеры при статусе > DRAFT."""
    errors = []

    fm = parse_frontmatter(content)
    status = fm.get("status", "DRAFT")

    if status in ("DRAFT", ""):
        return errors

    body = get_body(content)

    markers = re.findall(r'\[ТРЕБУЕТ УТОЧНЕНИЯ[^\]]*\]', body)
    if markers:
        errors.append(("DES024", f"Найдено {len(markers)} маркеров при статусе {status}"))

    if '⛔ DEPENDENCY BARRIER' in body or 'DEPENDENCY BARRIER' in body:
        errors.append(("DES025", f"Dependency Barrier при статусе {status}"))

    return errors


def check_zone_responsibility(content: str) -> list[tuple[str, str]]:
    """DES026-DES028: Проверить зону ответственности."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # DES027: unit-тесты
    unit_patterns = [
        (r'unit[\s-]тест', "unit-тест"),
        (r'Given\s+.*\s+When\s+.*\s+Then', "Given/When/Then"),
    ]
    for pattern, desc in unit_patterns:
        if re.search(pattern, body_no_code, re.IGNORECASE):
            errors.append(("DES027", f"Обнаружен {desc} (→ Plan Tests)"))
            break

    # DES028: задачи
    task_patterns = [
        (r'Задача:\s+реализовать', "Задача на реализацию"),
        (r'TODO:\s+', "TODO-задача"),
    ]
    for pattern, desc in task_patterns:
        if re.search(pattern, body_no_code, re.IGNORECASE):
            errors.append(("DES028", f"Обнаружена {desc} (→ Plan Dev)"))
            break

    return errors


def check_readme_registration(path: Path, content: str, repo_root: Path) -> list[tuple[str, str]]:
    """Проверить регистрацию в README."""
    errors = []

    readme_path = repo_root / "specs" / "analysis" / "README.md"
    if not readme_path.exists():
        return errors

    try:
        readme_content = readme_path.read_text(encoding='utf-8')
    except Exception:
        return errors

    folder_name = path.parent.name
    folder_match = FOLDER_REGEX.match(folder_name)
    if not folder_match:
        return errors

    folder_nnnn = folder_match.group(1)

    if folder_nnnn not in readme_content and folder_name not in readme_content:
        errors.append(("DES029", f"Запись для '{folder_name}' не найдена в README"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_design(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать один документ проектирования."""
    errors = []

    if not path.exists():
        return [("DES001", f"Файл не найден: {path}")]

    errors.extend(check_location(path))

    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [("DES001", f"Ошибка чтения файла: {e}")]

    errors.extend(check_frontmatter(content, path, repo_root))
    errors.extend(check_heading(content, path))
    errors.extend(check_required_sections(content))
    errors.extend(check_svc_sections(content))
    errors.extend(check_int_sections(content))
    errors.extend(check_numbering(content))
    errors.extend(check_markers_and_status(content))
    errors.extend(check_zone_responsibility(content))
    errors.extend(check_readme_registration(path, content, repo_root))
    errors.extend(check_rejected_proposals(content))

    return errors


def check_rejected_proposals(content: str) -> list[tuple[str, str]]:
    """Проверить секцию 'Отвергнутые предложения' — колонка 'Причина отклонения'."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    if re.search(r'^## Отвергнутые предложения', body_no_code, re.MULTILINE):
        section = get_section_text(body_no_code, r'^## Отвергнутые предложения')
        if section and 'Причина отклонения' not in section:
            errors.append(("DES035",
                           "Секция 'Отвергнутые предложения' должна содержать колонку 'Причина отклонения'"))

    return errors


def find_all_designs(repo_root: Path) -> list[Path]:
    """Найти все документы проектирования."""
    analysis_dir = repo_root / "specs" / "analysis"
    if not analysis_dir.exists():
        return []

    results = []
    for folder in sorted(analysis_dir.iterdir()):
        if folder.is_dir() and FOLDER_REGEX.match(folder.name):
            design_file = folder / "design.md"
            if design_file.exists():
                results.append(design_file)
    return results


def format_output(path: Path, errors: list[tuple[str, str]], as_json: bool) -> str:
    """Форматировать вывод."""
    if as_json:
        return json.dumps({
            "file": str(path),
            "valid": len(errors) == 0,
            "errors": [{"code": code, "message": msg} for code, msg in errors]
        }, ensure_ascii=False, indent=2)

    display_name = f"{path.parent.name}/{path.name}"
    if not errors:
        return f"✅ {display_name} — валидация пройдена"

    lines = [f"❌ {display_name} — {len(errors)} ошибок:"]
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
    parser.add_argument("--all", action="store_true", help="Проверить все документы")
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
