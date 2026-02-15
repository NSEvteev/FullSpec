#!/usr/bin/env python3
"""
validate-impact.py — Валидация документов импакт-анализа SDD.

Проверяет соответствие документа импакт-анализа стандарту standard-impact.md.

Использование:
    python validate-impact.py <path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-impact.py specs/impact/impact-0001-oauth2-authorization.md
    python validate-impact.py --all
    python validate-impact.py --json specs/impact/impact-0001-oauth2-authorization.md

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

FILENAME_REGEX = re.compile(r'^impact-(\d{4})-(.+)\.md$')
HEADING_REGEX = re.compile(r'^# impact-(\d{4}):\s+(.+)$', re.MULTILINE)

VALID_STATUSES = {
    "DRAFT", "WAITING", "RUNNING", "DONE",
    "CONFLICT", "ROLLING_BACK", "REJECTED",
}

REQUIRED_STANDARD = "specs/.instructions/impact/standard-impact.md"
REQUIRED_INDEX = "specs/impact/README.md"
STANDARD_VERSION_REGEX = re.compile(r'^v\d+\.\d+$')

PARENT_PATH_REGEX = re.compile(r'^discussion/disc-\d{4}-.+\.md$')

SECTION_HEADING_PREFIX = r'^##\s+(?:\S+\s+)?'  # Опциональный emoji перед именем

# Обязательные разделы (с emoji)
REQUIRED_SECTIONS = {
    "Резюме": ("I007", "📋"),
    "Затронутые сервисы": ("I008", "🏗️"),
    "Компоненты": ("I009", "📦"),
    "Данные и хранение": ("I010", "💾"),
    "API": ("I011", "🔌"),
    "Зависимости": ("I012", "🔗"),
    "Риски": ("I013", "⚠️"),
}

# Элементы с нумерацией
ELEMENT_PATTERNS = {
    "SVC": (re.compile(r'^\|\s*SVC-(\d+)\s*\|', re.MULTILINE), "I014"),
    "CMP": (re.compile(r'^\|\s*CMP-(\d+)\s*\|', re.MULTILINE), "I015"),
    "DATA": (re.compile(r'^\|\s*DATA-(\d+)\s*\|', re.MULTILINE), "I016"),
    "API": (re.compile(r'^\|\s*API-(\d+)\s*\|', re.MULTILINE), "I017"),
    "DEP": (re.compile(r'^\|\s*DEP-(\d+)\s*\|', re.MULTILINE), "I018"),
    "RISK": (re.compile(r'^\|\s*RISK-(\d+)\s*\|', re.MULTILINE), "I019"),
}

# Заглушки для необязательных разделов
SECTION_STUBS = {
    "Компоненты": re.compile(r'_Компоненты не идентифицированы\._'),
    "Данные и хранение": re.compile(r'_Изменений в данных нет\._'),
    "API": re.compile(r'_Изменений в API нет\._'),
    "Зависимости": re.compile(r'_Зависимостей нет\._'),
}

ERROR_CODES = {
    "I001": "Неверный формат имени файла",
    "I002": "Отсутствует description",
    "I003": "Неверный standard",
    "I004": "Невалидный status",
    "I005": "Отсутствует parent",
    "I006": "Parent не существует",
    "I007": "Отсутствует раздел 'Резюме'",
    "I008": "Отсутствует раздел 'Затронутые сервисы'",
    "I009": "Отсутствует раздел 'Компоненты'",
    "I010": "Отсутствует раздел 'Данные и хранение'",
    "I011": "Отсутствует раздел 'API'",
    "I012": "Отсутствует раздел 'Зависимости'",
    "I013": "Отсутствует раздел 'Риски'",
    "I014": "Дублирование SVC-N",
    "I015": "Дублирование CMP-N",
    "I016": "Дублирование DATA-N",
    "I017": "Дублирование API-N",
    "I018": "Дублирование DEP-N",
    "I019": "Дублирование RISK-N",
    "I020": "Маркер [ТРЕБУЕТ УТОЧНЕНИЯ] при статусе > DRAFT",
    "I021": "Dependency Barrier при статусе > DRAFT",
    "I022": "Распределение ответственностей (→ Design)",
    "I023": "Нет записи в README",
    "I024": "Рассинхрон статуса (README ≠ frontmatter)",
    "I025": "NNNN в имени файла ≠ NNNN в заголовке",
    "I026": "Отсутствует milestone",
    "I027": "Отсутствует или неверный standard-version",
    "I028": "Неверный index",
    "I029": "Description слишком длинное (> 1024 символов)",
    "I030": "Секция без контента и без заглушки",
    "I031": "'Затронутые сервисы' — нет элементов SVC-N",
    "I032": "'Риски' — нет элементов RISK-N",
    "I033": "Резюме пустое или содержит только placeholder",
    "I034": "Milestone Impact ≠ milestone parent Discussion",
    "I035": "Колонка 'Тип' в зависимости DEP-N пустая",
    "I036": "NNNN Impact ≠ NNNN parent Discussion",
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
        # Элемент списка
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


def get_section_text(body_no_code: str, section_name: str) -> str | None:
    """Извлечь текст секции по имени (с опциональным emoji)."""
    pattern = SECTION_HEADING_PREFIX + re.escape(section_name) + r'\s*\n(.*?)(?=^##\s|\Z)'
    match = re.search(pattern, body_no_code, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


# =============================================================================
# Проверки
# =============================================================================

def check_filename(path: Path) -> list[tuple[str, str]]:
    """I001: Проверить формат имени файла."""
    errors = []
    if not FILENAME_REGEX.match(path.name):
        errors.append(("I001", f"Имя '{path.name}' не соответствует impact-NNNN-topic.md"))
    return errors


def check_frontmatter(content: str, repo_root: Path) -> list[tuple[str, str]]:
    """I002-I006, I026-I029: Проверить frontmatter."""
    errors = []

    if not content.startswith("---\n"):
        errors.append(("I002", "Отсутствует frontmatter"))
        return errors

    fm = parse_frontmatter(content)

    # I002: description
    desc = fm.get("description", "")
    if not desc:
        errors.append(("I002", "Отсутствует поле description"))
    elif len(desc) > 1024:
        errors.append(("I029", f"Description {len(desc)} символов (макс. 1024)"))

    # I003: standard
    standard = fm.get("standard", "")
    if standard != REQUIRED_STANDARD:
        errors.append(("I003", f"standard = '{standard}', ожидается '{REQUIRED_STANDARD}'"))

    # I027: standard-version
    sv = fm.get("standard-version", "")
    if not sv:
        errors.append(("I027", "Отсутствует поле standard-version"))
    elif not STANDARD_VERSION_REGEX.match(sv):
        errors.append(("I027", f"standard-version = '{sv}', ожидается формат vX.Y"))

    # I004: status
    status = fm.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(("I004", f"status = '{status}', допустимые: {', '.join(sorted(VALID_STATUSES))}"))

    # I005: parent обязателен
    parent = fm.get("parent", "")
    if not parent:
        errors.append(("I005", "Отсутствует поле parent (обязательно для Impact)"))
    else:
        # I005: parent path format
        if not PARENT_PATH_REGEX.match(parent):
            errors.append(("I005", f"Неверный формат parent: ожидается discussion/disc-NNNN-topic.md"))
        # I006: parent существует
        parent_path = repo_root / "specs" / parent
        if not parent_path.exists():
            errors.append(("I006", f"Parent не найден: specs/{parent}"))

    # I026: milestone
    if not fm.get("milestone"):
        errors.append(("I026", "Отсутствует поле milestone"))

    # I028: index
    index = fm.get("index", "")
    if index != REQUIRED_INDEX:
        errors.append(("I028", f"index = '{index}', ожидается '{REQUIRED_INDEX}'"))

    return errors


def check_heading(content: str, path: Path) -> list[tuple[str, str]]:
    """I025: Проверить совпадение NNNN в имени файла и заголовке."""
    errors = []

    file_match = FILENAME_REGEX.match(path.name)
    if not file_match:
        return errors  # I001 уже покрыто

    file_nnnn = file_match.group(1)
    body = get_body(content)
    heading_match = HEADING_REGEX.search(body)

    if not heading_match:
        errors.append(("I025", "Заголовок '# impact-NNNN: Тема' не найден"))
        return errors

    heading_nnnn = heading_match.group(1)
    if file_nnnn != heading_nnnn:
        errors.append(("I025", f"NNNN в файле ({file_nnnn}) ≠ NNNN в заголовке ({heading_nnnn})"))

    return errors


def check_required_sections(content: str) -> list[tuple[str, str]]:
    """I007-I013: Проверить обязательные разделы (все 7)."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    for section_name, (error_code, emoji) in REQUIRED_SECTIONS.items():
        # Ищем с emoji и без
        found = (
            re.search(SECTION_HEADING_PREFIX + re.escape(section_name), body_no_code, re.MULTILINE)
            or re.search(SECTION_HEADING_PREFIX + re.escape(emoji) + r'\s+' + re.escape(section_name), body_no_code, re.MULTILINE)
        )
        if not found:
            errors.append((error_code, f"Отсутствует раздел '## {emoji} {section_name}'"))

    return errors


def check_section_content(content: str) -> list[tuple[str, str]]:
    """I030-I032: Проверить что секции содержат элементы или заглушку."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # I033: Резюме — не пустое и не placeholder
    resume_section = get_section_text(body_no_code, "Резюме")
    if resume_section is not None:
        resume_stripped = resume_section.strip()
        if not resume_stripped or '{Краткое описание' in resume_section:
            errors.append(("I033", "Резюме пустое или содержит только placeholder"))

    # I031: Затронутые сервисы — минимум 1 SVC-N
    svc_section = get_section_text(body_no_code, "Затронутые сервисы")
    if svc_section is not None:
        svc_pattern = ELEMENT_PATTERNS["SVC"][0]
        if not svc_pattern.search(svc_section):
            errors.append(("I031", "'Затронутые сервисы' — нет элементов SVC-N (минимум 1)"))

    # I032: Риски — минимум 1 RISK-N
    risk_section = get_section_text(body_no_code, "Риски")
    if risk_section is not None:
        risk_pattern = ELEMENT_PATTERNS["RISK"][0]
        if not risk_pattern.search(risk_section):
            errors.append(("I032", "'Риски' — нет элементов RISK-N (минимум 1)"))

    # I030: Остальные секции — контент или заглушка
    for section_name, stub_pattern in SECTION_STUBS.items():
        section_text = get_section_text(body_no_code, section_name)
        if section_text is not None:
            # Проверить наличие элементов
            element_prefix_map = {
                "Компоненты": "CMP",
                "Данные и хранение": "DATA",
                "API": "API",
                "Зависимости": "DEP",
            }
            prefix = element_prefix_map.get(section_name)
            has_elements = False
            if prefix and prefix in ELEMENT_PATTERNS:
                has_elements = bool(ELEMENT_PATTERNS[prefix][0].search(section_text))
            has_stub = bool(stub_pattern.search(section_text))
            if not has_elements and not has_stub:
                errors.append(("I030", f"Секция '{section_name}' без контента и без заглушки"))

    return errors


def check_numbering(content: str) -> list[tuple[str, str]]:
    """I014-I019: Проверить уникальность нумерации элементов."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    for prefix, (pattern, error_code) in ELEMENT_PATTERNS.items():
        numbers = pattern.findall(body_no_code)
        seen = set()
        for num in numbers:
            if num in seen:
                errors.append((error_code, f"Дубликат {prefix}-{num}"))
            seen.add(num)

    return errors


def check_markers_and_status(content: str) -> list[tuple[str, str]]:
    """I020-I021: Проверить маркеры при статусе > DRAFT."""
    errors = []

    fm = parse_frontmatter(content)
    status = fm.get("status", "DRAFT")

    if status in ("DRAFT", ""):
        return errors

    body = get_body(content)

    # I020: маркеры [ТРЕБУЕТ УТОЧНЕНИЯ]
    markers = re.findall(r'\[ТРЕБУЕТ УТОЧНЕНИЯ[^\]]*\]', body)
    if markers:
        errors.append(("I020", f"Найдено {len(markers)} маркеров при статусе {status}"))

    # I021: Dependency Barrier
    if '⛔ DEPENDENCY BARRIER' in body or 'DEPENDENCY BARRIER' in body:
        errors.append(("I021", f"Dependency Barrier при статусе {status}"))

    return errors


def check_zone_responsibility(content: str) -> list[tuple[str, str]]:
    """I022: Проверить зону ответственности (распределение → Design)."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # Паттерны окончательного распределения ответственностей
    responsibility_patterns = [
        (r'(\S+-сервис|сервис\s+\S+)\s+отвечает\s+за', "окончательное распределение ответственностей"),
        (r'(\S+)\s+будет\s+отвечать\s+за', "окончательное распределение ответственностей"),
        (r'\w+[-\w]*\s+отвечает\s+за', "окончательное распределение ответственностей"),
        (r'is\s+responsible\s+for', "окончательное распределение ответственностей (EN)"),
        (r'will\s+handle\b', "окончательное распределение ответственностей (EN)"),
        (r'\b\w+[-\w]*\s+owns\s+', "окончательное распределение ответственностей (EN)"),
    ]

    for pattern, desc in responsibility_patterns:
        matches = re.findall(pattern, body_no_code, re.IGNORECASE)
        if matches:
            errors.append(("I022", f"Обнаружено {desc}: {matches[0]}"))
            break

    return errors


def check_readme_registration(path: Path, content: str, repo_root: Path) -> list[tuple[str, str]]:
    """I023-I024: Проверить регистрацию в README."""
    errors = []

    readme_path = repo_root / "specs" / "impact" / "README.md"
    if not readme_path.exists():
        errors.append(("I023", f"README не найден: {readme_path}"))
        return errors

    try:
        readme_content = readme_path.read_text(encoding='utf-8')
    except Exception:
        errors.append(("I023", "Ошибка чтения README"))
        return errors

    # I023: проверить наличие записи
    file_stem = path.stem
    if file_stem not in readme_content and path.name not in readme_content:
        errors.append(("I023", f"Запись '{path.name}' не найдена в README"))
        return errors

    # I024: проверить синхронность статуса
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
                errors.append(("I024", f"Статус в README ({readme_status}) ≠ frontmatter ({fm_status})"))

    return errors


def check_milestone_match(content: str, repo_root: Path) -> list[tuple[str, str]]:
    """I034: Проверить совпадение milestone Impact с milestone parent Discussion."""
    errors = []

    fm = parse_frontmatter(content)
    parent = fm.get("parent", "")
    if not parent:
        return errors

    parent_path = repo_root / "specs" / parent
    if not parent_path.exists():
        return errors  # I006 уже покрыто

    try:
        parent_content = parent_path.read_text(encoding='utf-8')
    except Exception:
        return errors

    parent_fm = parse_frontmatter(parent_content)
    impact_milestone = fm.get("milestone", "")
    parent_milestone = parent_fm.get("milestone", "")

    if impact_milestone and parent_milestone and impact_milestone != parent_milestone:
        errors.append(("I034", f"Milestone Impact ({impact_milestone}) ≠ milestone parent ({parent_milestone})"))

    return errors


def check_number_matches_parent(path: Path, content: str) -> list[tuple[str, str]]:
    """I036: Проверить совпадение NNNN Impact с NNNN parent Discussion."""
    errors = []

    file_match = FILENAME_REGEX.match(path.name)
    if not file_match:
        return errors

    file_nnnn = file_match.group(1)

    fm = parse_frontmatter(content)
    parent = fm.get("parent", "")
    if not parent:
        return errors

    parent_match = re.search(r'disc-(\d{4})', parent)
    if not parent_match:
        return errors

    parent_nnnn = parent_match.group(1)

    if file_nnnn != parent_nnnn:
        errors.append(("I036", f"NNNN Impact ({file_nnnn}) ≠ NNNN parent Discussion ({parent_nnnn})"))

    return errors


def check_dependency_type(content: str) -> list[tuple[str, str]]:
    """I035: Проверить что колонка 'Тип' в зависимостях DEP-N не пустая."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    dep_section = get_section_text(body_no_code, "Зависимости")
    if dep_section is None:
        return errors

    # Пропустить если секция содержит заглушку
    if re.search(r'_Зависимостей нет\._', dep_section):
        return errors

    # Найти строки с DEP-N
    dep_lines = re.findall(r'^\|[^|]*DEP-\d+[^|]*\|.*$', dep_section, re.MULTILINE)
    for line in dep_lines:
        columns = [col.strip() for col in line.split('|')]
        # columns[0] пустая (до первого |), columns[1] = ID, ...
        # Типичный формат: | DEP-N | Описание | Источник | Тип | Статус |
        # Колонка 'Тип' — 4-я (индекс 4 в split)
        if len(columns) >= 5:
            dep_type = columns[4]
            if not dep_type:
                dep_id_match = re.search(r'DEP-\d+', line)
                dep_id = dep_id_match.group(0) if dep_id_match else "DEP-?"
                errors.append(("I035", f"Колонка 'Тип' пустая для {dep_id}"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_impact(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать один документ импакт-анализа."""
    errors = []

    if not path.exists():
        return [("I001", f"Файл не найден: {path}")]

    # I001: формат имени
    errors.extend(check_filename(path))

    # Читаем содержимое
    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [("I001", f"Ошибка чтения файла: {e}")]

    # I002-I006, I026-I029: frontmatter
    errors.extend(check_frontmatter(content, repo_root))

    # I025: NNNN совпадение
    errors.extend(check_heading(content, path))

    # I007-I013: обязательные разделы
    errors.extend(check_required_sections(content))

    # I030-I032: контент секций
    errors.extend(check_section_content(content))

    # I014-I019: нумерация
    errors.extend(check_numbering(content))

    # I020-I021: маркеры и статус
    errors.extend(check_markers_and_status(content))

    # I022: зона ответственности
    errors.extend(check_zone_responsibility(content))

    # I023-I024: README
    errors.extend(check_readme_registration(path, content, repo_root))

    # I034: milestone cross-check
    errors.extend(check_milestone_match(content, repo_root))

    # I036: NNNN Impact = NNNN parent
    errors.extend(check_number_matches_parent(path, content))

    # I035: dependency type non-empty
    errors.extend(check_dependency_type(content))

    return errors


def find_all_impacts(repo_root: Path) -> list[Path]:
    """Найти все документы импакт-анализа."""
    impact_dir = repo_root / "specs" / "impact"
    if not impact_dir.exists():
        return []

    return sorted(impact_dir.glob("impact-*.md"))


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
        description="Валидация документов импакт-анализа SDD"
    )
    parser.add_argument("path", nargs="?", help="Путь к документу импакт-анализа")
    parser.add_argument("--all", action="store_true", help="Проверить все импакт-анализы")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if args.all:
        impacts = find_all_impacts(repo_root)
        if not impacts:
            print("Импакт-анализы не найдены")
            sys.exit(0)
    elif args.path:
        impacts = [Path(args.path)]
    else:
        parser.print_help()
        sys.exit(2)

    all_valid = True
    results = []

    for path in impacts:
        errors = validate_impact(path, repo_root)
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
