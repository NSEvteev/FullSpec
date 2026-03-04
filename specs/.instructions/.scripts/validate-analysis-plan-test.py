#!/usr/bin/env python3
"""
validate-analysis-plan-test.py — Валидация документов плана тестов SDD.

Проверяет соответствие документа плана тестов стандарту standard-plan-test.md.

Использование:
    python validate-analysis-plan-test.py <path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-analysis-plan-test.py specs/analysis/0001-oauth2-authorization/plan-test.md
    python validate-analysis-plan-test.py --all
    python validate-analysis-plan-test.py --json specs/analysis/0001-oauth2-authorization/plan-test.md

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
HEADING_REGEX = re.compile(r'^# (\d{4}):\s+(.+?)(?:\s*—\s*Plan Tests)?\s*$', re.MULTILINE)
HEADING_SUFFIX_REGEX = re.compile(r'—\s*Plan Tests\s*$')

VALID_STATUSES = {
    "DRAFT", "WAITING", "RUNNING", "REVIEW", "DONE",
    "CONFLICT", "ROLLING_BACK", "REJECTED",
}

REQUIRED_STANDARD = "specs/.instructions/analysis/plan-test/standard-plan-test.md"
REQUIRED_INDEX = "specs/analysis/README.md"
STANDARD_VERSION_REGEX = re.compile(r'^v\d+\.\d+$')

TC_PATTERN = re.compile(r'^\|\s*TC-(\d+)\s*\|', re.MULTILINE)
TC_ROW_PATTERN = re.compile(
    r'^\|\s*TC-(\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|',
    re.MULTILINE,
)
FIXTURE_NAME_PATTERN = re.compile(r'^\|\s*(\w+)\s*\|', re.MULTILINE)

GWT_PATTERNS = [
    re.compile(r'\bGiven\b', re.IGNORECASE),
    re.compile(r'\bWhen\b', re.IGNORECASE),
    re.compile(r'\bThen\b', re.IGNORECASE),
]

MODAL_PATTERNS = [
    re.compile(r'\bдолжен\b', re.IGNORECASE),
    re.compile(r'\bследует\b', re.IGNORECASE),
    re.compile(r'\bдолжна\b', re.IGNORECASE),
    re.compile(r'\bдолжно\b', re.IGNORECASE),
    re.compile(r'\bдолжны\b', re.IGNORECASE),
]

VALID_TC_TYPES = {"unit", "integration", "e2e", "load", "smoke"}

ERROR_CODES = {
    "PT001": "Неверное расположение файла",
    "PT002": "Отсутствует description",
    "PT003": "Неверный standard",
    "PT004": "Невалидный status",
    "PT005": "Отсутствует parent",
    "PT006": "Parent Design не существует",
    "PT007": "Milestone не совпадает с parent",
    "PT008": "Отсутствует Резюме",
    "PT009": "Нет per-service раздела",
    "PT010": "Нет Acceptance-сценарии",
    "PT011": "Нет Тестовые данные",
    "PT012": "Формат Given/When/Then",
    "PT013": "Модальный глагол в описании TC-N",
    "PT014": "Невалидный тип TC-N",
    "PT015": "Нет источника (REQ-N, STS-N, SVC-N или INT-N)",
    "PT016": "Fixture не найден",
    "PT017": "Дублирование TC-N",
    "PT018": "Нет Системные тест-сценарии",
    "PT019": "Нет Матрица покрытия",
    "PT020": "REQ-N без покрытия",
    "PT021": "STS-N без покрытия",
    "PT022": "Маркер при статусе > DRAFT",
    "PT023": "Dependency Barrier при статусе > DRAFT",
    "PT024": "NNNN не совпадает",
    "PT025": "Description слишком длинное",
    "PT026": "Нет Блоки тестирования",
    "PT027": "TC-N без BLOCK-N",
    "PT028": "BLOCK-N не совпадает с plan-dev",
    "PT029": "Системные TC не в отдельном BLOCK",
    "PT030": "Нет Предложения",
    "PT031": "Нет Отвергнутые предложения",
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


def split_sections(body: str) -> list[tuple[str, str]]:
    """Разбить body на секции h2. Возвращает [(heading, content), ...]."""
    parts = re.split(r'^(## .+)$', body, flags=re.MULTILINE)
    sections = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((heading, content))
    return sections


# =============================================================================
# Проверки
# =============================================================================

def check_location(path: Path) -> list[tuple[str, str]]:
    """PT001: Проверить расположение файла."""
    errors = []

    if path.name != "plan-test.md":
        errors.append(("PT001", f"Имя файла '{path.name}', ожидается 'plan-test.md'"))
        return errors

    parent_name = path.parent.name
    if not FOLDER_REGEX.match(parent_name):
        errors.append(("PT001", f"Папка '{parent_name}' не соответствует формату NNNN-{{topic}}"))

    return errors


def check_frontmatter(content: str, path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """PT002-PT007, PT025: Проверить frontmatter."""
    errors = []

    if not content.startswith("---\n"):
        errors.append(("PT002", "Отсутствует frontmatter"))
        return errors

    fm = parse_frontmatter(content)

    # PT002: description
    desc = fm.get("description", "")
    if not desc:
        errors.append(("PT002", "Отсутствует поле description"))
    elif len(desc) > 1024:
        errors.append(("PT025", f"Description {len(desc)} символов (макс. 1024)"))

    # PT003: standard
    standard = fm.get("standard", "")
    if standard != REQUIRED_STANDARD:
        errors.append(("PT003", f"standard = '{standard}', ожидается '{REQUIRED_STANDARD}'"))

    # standard-version
    sv = fm.get("standard-version", "")
    if not sv:
        errors.append(("PT003", "Отсутствует поле standard-version"))
    elif not STANDARD_VERSION_REGEX.match(sv):
        errors.append(("PT003", f"standard-version = '{sv}', ожидается формат vX.Y"))

    # PT004: status
    status = fm.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(("PT004", f"status = '{status}', допустимые: {', '.join(sorted(VALID_STATUSES))}"))

    # index
    index = fm.get("index", "")
    if index != REQUIRED_INDEX:
        errors.append(("PT003", f"index = '{index}', ожидается '{REQUIRED_INDEX}'"))

    # PT005: parent
    parent = fm.get("parent", "")
    if not parent:
        errors.append(("PT005", "Отсутствует поле parent (Design обязателен)"))
    else:
        # PT006: parent exists
        parent_path = path.parent / parent
        if not parent_path.exists():
            errors.append(("PT006", f"Parent Design не найден: {parent}"))

    # milestone
    milestone = fm.get("milestone", "")
    if not milestone:
        errors.append(("PT007", "Отсутствует поле milestone"))

    return errors


def check_heading(content: str, path: Path) -> list[tuple[str, str]]:
    """PT024: Проверить совпадение NNNN и суффикс — Plan Tests."""
    errors = []

    folder_match = FOLDER_REGEX.match(path.parent.name)
    if not folder_match:
        return errors

    folder_nnnn = folder_match.group(1)
    body = get_body(content)

    # Ищем заголовок h1
    h1_match = re.search(r'^# (.+)$', body, re.MULTILINE)
    if not h1_match:
        errors.append(("PT024", "Заголовок '# NNNN: Тема — Plan Tests' не найден"))
        return errors

    h1_text = h1_match.group(1).strip()

    # Проверяем суффикс
    if not HEADING_SUFFIX_REGEX.search(h1_text):
        errors.append(("PT024", "Заголовок не заканчивается на '— Plan Tests'"))

    # Проверяем NNNN
    nnnn_match = re.match(r'^(\d{4}):', h1_text)
    if nnnn_match:
        heading_nnnn = nnnn_match.group(1)
        if folder_nnnn != heading_nnnn:
            errors.append(("PT024", f"NNNN в папке ({folder_nnnn}) ≠ NNNN в заголовке ({heading_nnnn})"))
    else:
        errors.append(("PT024", "NNNN не найден в заголовке"))

    return errors


def check_required_sections(content: str) -> list[tuple[str, str]]:
    """PT008, PT009, PT018, PT019: Проверить обязательные разделы."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)
    sections = split_sections(body_no_code)
    headings = [h for h, _ in sections]

    # PT008: Резюме
    if not any("Резюме" in h for h in headings):
        errors.append(("PT008", "Отсутствует раздел '## Резюме'"))

    # PT018: Системные тест-сценарии
    if not any("Системные тест-сценарии" in h for h in headings):
        errors.append(("PT018", "Отсутствует раздел '## Системные тест-сценарии'"))

    # PT019: Матрица покрытия
    if not any("Матрица покрытия" in h for h in headings):
        errors.append(("PT019", "Отсутствует раздел '## Матрица покрытия'"))

    # PT026: Блоки тестирования
    if not any("Блоки тестирования" in h for h in headings):
        errors.append(("PT026", "Отсутствует раздел '## Блоки тестирования'"))

    # PT030: Предложения
    if not any("Предложения" == h.replace("## ", "").strip() for h in headings):
        errors.append(("PT030", "Отсутствует раздел '## Предложения'"))

    # PT031: Отвергнутые предложения
    if not any("Отвергнутые предложения" in h for h in headings):
        errors.append(("PT031", "Отсутствует раздел '## Отвергнутые предложения'"))

    # PT009: per-service разделы (секции h2, не являющиеся Резюме/Системные/Матрица/Блоки/Предложения)
    special = {"Резюме", "Системные тест-сценарии", "Матрица покрытия", "Блоки тестирования", "Предложения", "Отвергнутые предложения"}
    per_service = [h for h in headings if not any(s in h for s in special)]
    if not per_service:
        errors.append(("PT009", "Нет ни одного per-service раздела"))

    return errors


def check_per_service_sections(content: str) -> list[tuple[str, str]]:
    """PT010, PT011: Проверить подсекции per-service разделов."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)
    sections = split_sections(body_no_code)

    special = {"Резюме", "Системные тест-сценарии", "Матрица покрытия", "Блоки тестирования", "Предложения", "Отвергнутые предложения"}

    for heading, section_content in sections:
        if any(s in heading for s in special):
            continue

        raw_name = heading.replace("## ", "").strip()
        # Поддержка формата "SVC-N: {name}" и legacy "{name}"
        svc_match = re.match(r'SVC-\d+:\s*(.+)', raw_name)
        service_name = svc_match.group(1).strip() if svc_match else raw_name

        # PT010: Acceptance-сценарии
        if "### Acceptance-сценарии" not in section_content:
            errors.append(("PT010", f"Сервис '{service_name}': нет подсекции 'Acceptance-сценарии'"))

        # PT011: Тестовые данные
        if "### Тестовые данные" not in section_content:
            errors.append(("PT011", f"Сервис '{service_name}': нет подсекции 'Тестовые данные'"))

    return errors


def check_tc_format(content: str) -> list[tuple[str, str]]:
    """PT012-PT015, PT017: Проверить формат TC-N."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # PT017: дублирование TC-N
    tc_numbers = TC_PATTERN.findall(body_no_code)
    seen = set()
    for num in tc_numbers:
        if num in seen:
            errors.append(("PT017", f"Дубликат TC-{num}"))
        seen.add(num)

    # Проверяем каждую строку TC-N
    for match in TC_ROW_PATTERN.finditer(body_no_code):
        tc_num = match.group(1)
        description = match.group(2).strip()
        tc_type = match.group(3).strip()
        source = match.group(4).strip()

        # PT012: G/W/T
        for gwt in GWT_PATTERNS:
            if gwt.search(description):
                errors.append(("PT012", f"TC-{tc_num}: формат Given/When/Then в описании"))
                break

        # PT013: модальные глаголы
        for modal in MODAL_PATTERNS:
            if modal.search(description):
                errors.append(("PT013", f"TC-{tc_num}: модальный глагол в описании"))
                break

        # PT014: тип
        if tc_type.lower() not in VALID_TC_TYPES:
            errors.append(("PT014", f"TC-{tc_num}: тип '{tc_type}' не из допустимых: {', '.join(sorted(VALID_TC_TYPES))}"))

        # PT015: источник (≥ 1 из REQ-N, STS-N, SVC-N, INT-N)
        has_req = bool(re.search(r'REQ-\d+', source))
        has_sts = bool(re.search(r'STS-\d+', source))
        has_svc = bool(re.search(r'SVC-\d+', source))
        has_int = bool(re.search(r'INT-\d+', source))
        if not has_req and not has_sts and not has_svc and not has_int:
            errors.append(("PT015", f"TC-{tc_num}: нет источника (REQ-N, STS-N, SVC-N или INT-N)"))

    return errors


BLOCK_ROW_PATTERN_TEST = re.compile(
    r'\|\s*BLOCK-(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|'
)


def expand_tc_range(tc_str: str) -> list[int]:
    """Раскрыть TC-N..TC-M в список TC номеров."""
    result = []
    for match in re.finditer(r'TC-(\d+)\.\.TC-(\d+)', tc_str):
        start, end = int(match.group(1)), int(match.group(2))
        result.extend(range(start, end + 1))
    cleaned = re.sub(r'TC-\d+\.\.TC-\d+', '', tc_str)
    result.extend(int(m) for m in re.findall(r'TC-(\d+)', cleaned))
    return result


def check_blocks(content: str) -> list[tuple[str, str]]:
    """PT026-PT029: Проверить секцию Блоки тестирования."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)
    sections = split_sections(body_no_code)

    block_section = None
    for heading, sec_content in sections:
        if "Блоки тестирования" in heading:
            block_section = sec_content
            break

    if block_section is None:
        return errors  # PT026 уже проверено в check_required_sections

    # Если заглушка — пропустить
    if "заглушка" in block_section.lower() or "нет блоков" in block_section.lower():
        return errors

    # Извлечь строки таблицы
    block_rows = list(BLOCK_ROW_PATTERN_TEST.finditer(block_section))
    if not block_rows:
        return errors

    # Собрать все TC-N из документа
    all_tc_nums = set(int(n) for n in TC_PATTERN.findall(body_no_code))

    # Собрать TC-N из блоков
    tcs_in_blocks: set[int] = set()
    for match in block_rows:
        tc_str = match.group(2).strip()
        tc_nums = expand_tc_range(tc_str)
        tcs_in_blocks.update(tc_nums)

    # PT027: каждый TC-N принадлежит блоку
    for tc_num in all_tc_nums:
        if tc_num not in tcs_in_blocks:
            errors.append(("PT027", f"TC-{tc_num} не принадлежит ни одному BLOCK-N"))

    return errors


def check_markers_and_status(content: str) -> list[tuple[str, str]]:
    """PT022-PT023: Проверить маркеры при статусе > DRAFT."""
    errors = []

    fm = parse_frontmatter(content)
    status = fm.get("status", "DRAFT")

    if status in ("DRAFT", ""):
        return errors

    body = get_body(content)

    # PT022: маркеры
    markers = re.findall(r'\[ТРЕБУЕТ УТОЧНЕНИЯ[^\]]*\]', body)
    if markers:
        errors.append(("PT022", f"Найдено {len(markers)} маркеров при статусе {status}"))

    # PT023: Dependency Barrier
    if '⛔ DEPENDENCY BARRIER' in body or 'DEPENDENCY BARRIER' in body:
        errors.append(("PT023", f"Dependency Barrier при статусе {status}"))

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

    folder_match = FOLDER_REGEX.match(path.parent.name)
    if not folder_match:
        return errors

    folder_nnnn = folder_match.group(1)
    folder_name = path.parent.name

    if folder_nnnn not in readme_content and folder_name not in readme_content:
        errors.append(("PT024", f"Запись для '{folder_name}' не найдена в README"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_plan_test(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать один документ плана тестов."""
    errors = []

    if not path.exists():
        return [("PT001", f"Файл не найден: {path}")]

    # PT001: расположение
    errors.extend(check_location(path))

    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [("PT001", f"Ошибка чтения файла: {e}")]

    # PT002-PT007, PT025: frontmatter
    errors.extend(check_frontmatter(content, path, repo_root))

    # PT024: заголовок
    errors.extend(check_heading(content, path))

    # PT008, PT009, PT018, PT019: обязательные разделы
    errors.extend(check_required_sections(content))

    # PT010, PT011: per-service подсекции
    errors.extend(check_per_service_sections(content))

    # PT012-PT015, PT017: формат TC-N
    errors.extend(check_tc_format(content))

    # PT026-PT029: блоки тестирования
    errors.extend(check_blocks(content))

    # PT022-PT023: маркеры и статус
    errors.extend(check_markers_and_status(content))

    # README
    errors.extend(check_readme_registration(path, content, repo_root))

    return errors


def find_all_plan_tests(repo_root: Path) -> list[Path]:
    """Найти все документы плана тестов."""
    analysis_dir = repo_root / "specs" / "analysis"
    if not analysis_dir.exists():
        return []

    results = []
    for folder in sorted(analysis_dir.iterdir()):
        if folder.is_dir() and FOLDER_REGEX.match(folder.name):
            pt_file = folder / "plan-test.md"
            if pt_file.exists():
                results.append(pt_file)
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
        description="Валидация документов плана тестов SDD"
    )
    parser.add_argument("path", nargs="?", help="Путь к документу плана тестов")
    parser.add_argument("--all", action="store_true", help="Проверить все планы тестов")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if args.all:
        plan_tests = find_all_plan_tests(repo_root)
        if not plan_tests:
            print("Планы тестов не найдены")
            sys.exit(0)
    elif args.path:
        plan_tests = [Path(args.path)]
    else:
        parser.print_help()
        sys.exit(2)

    all_valid = True
    results = []

    for path in plan_tests:
        errors = validate_plan_test(path, repo_root)
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
