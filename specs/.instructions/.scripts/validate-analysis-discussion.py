#!/usr/bin/env python3
"""
validate-analysis-discussion.py — Валидация документов дискуссий SDD.

Проверяет соответствие документа дискуссии стандарту standard-discussion.md.

Использование:
    python validate-analysis-discussion.py <path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-analysis-discussion.py specs/analysis/0001-oauth2-authorization/discussion.md
    python validate-analysis-discussion.py --all
    python validate-analysis-discussion.py --json specs/analysis/0001-oauth2-authorization/discussion.md

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
HEADING_REGEX = re.compile(r'^# (\d{4}):\s+(.+)$', re.MULTILINE)

VALID_STATUSES = {
    "DRAFT", "WAITING", "RUNNING", "REVIEW", "DONE",
    "CONFLICT", "ROLLING_BACK", "REJECTED",
}

REQUIRED_STANDARD = "specs/.instructions/analysis/discussion/standard-discussion.md"
REQUIRED_INDEX = "specs/analysis/README.md"
STANDARD_VERSION_REGEX = re.compile(r'^v\d+\.\d+$')

SECTION_HEADING_PREFIX = r'^##\s+(?:\S+\s+)?'  # Опциональный emoji перед именем

SECTION_ELEMENTS = {
    "Фичи": re.compile(r'^\|\s*F-\d+\s*\|', re.MULTILINE),
    "User Stories": re.compile(r'^\|\s*US-\d+\s*\|', re.MULTILINE),
    "Требования": re.compile(r'^\|\s*REQ-\d+\s*\|', re.MULTILINE),
    "Предложения": re.compile(r'^\|\s*PROP-\d+\s*\|', re.MULTILINE),
}

SECTION_STUBS = {
    "Фичи": re.compile(r'_Нет выделенных фич\._'),
    "User Stories": re.compile(r'_Нет User Stories\._'),
    "Требования": re.compile(r'_Нет формализованных требований\._'),
    "Предложения": re.compile(r'_(Предложений нет|Все предложения обработаны)\._'),
}

ELEMENT_PATTERNS = {
    "F": (re.compile(r'^\|\s*F-(\d+)\s*\|', re.MULTILINE), "D008"),
    "US": (re.compile(r'^\|\s*US-(\d+)\s*\|', re.MULTILINE), "D009"),
    "REQ": (re.compile(r'^\|\s*REQ-(\d+)\s*\|', re.MULTILINE), "D010"),
    "PROP": (re.compile(r'^\|\s*PROP-(\d+)\s*\|', re.MULTILINE), "D011"),
}

ERROR_CODES = {
    "D001": "Неверное расположение файла",
    "D002": "Отсутствует description",
    "D003": "Неверный standard",
    "D004": "Невалидный status",
    "D005": "Присутствует parent (запрещено для Discussion)",
    "D006": "Отсутствует обязательный раздел",
    "D007": "Отсутствует раздел 'Критерии успеха'",
    "D008": "Дублирование номера F-N",
    "D009": "Дублирование номера US-N",
    "D010": "Дублирование номера REQ-N",
    "D011": "Дублирование номера PROP-N",
    "D012": "(удалено) REQ без Given/When/Then — требования в формате естественных предложений",
    "D013": "Маркер [ТРЕБУЕТ УТОЧНЕНИЯ] при статусе > DRAFT",
    "D014": "Dependency Barrier при статусе > DRAFT",
    "D015": "Привязка к сервису (зона ответственности)",
    "D016": "Нет записи в README",
    "D017": "Рассинхрон статуса (README ≠ frontmatter)",
    "D018": "NNNN в папке ≠ NNNN в заголовке",
    "D019": "Отсутствует milestone",
    "D020": "Отсутствует или неверный standard-version",
    "D021": "Неверный index",
    "D022": "Секция без контента и без заглушки",
    "D023": "Description слишком длинное (> 1024 символов)",
    "D024": "Секция 'Отвергнутые предложения' без таблицы",
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


# =============================================================================
# Проверки
# =============================================================================

def check_location(path: Path) -> list[tuple[str, str]]:
    """D001: Проверить расположение файла."""
    errors = []

    # Файл должен называться discussion.md
    if path.name != "discussion.md":
        errors.append(("D001", f"Имя файла '{path.name}', ожидается 'discussion.md'"))
        return errors

    # Родительская папка должна соответствовать NNNN-{topic}
    parent_name = path.parent.name
    if not FOLDER_REGEX.match(parent_name):
        errors.append(("D001", f"Папка '{parent_name}' не соответствует формату NNNN-{{topic}}"))

    return errors


def check_frontmatter(content: str) -> list[tuple[str, str]]:
    """D002-D005, D019-D021, D023: Проверить frontmatter."""
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
        # D023: description слишком длинное
        errors.append(("D023", f"Description {len(desc)} символов (макс. 1024)"))

    # D003: standard
    standard = fm.get("standard", "")
    if standard != REQUIRED_STANDARD:
        errors.append(("D003", f"standard = '{standard}', ожидается '{REQUIRED_STANDARD}'"))

    # D020: standard-version
    sv = fm.get("standard-version", "")
    if not sv:
        errors.append(("D020", "Отсутствует поле standard-version"))
    elif not STANDARD_VERSION_REGEX.match(sv):
        errors.append(("D020", f"standard-version = '{sv}', ожидается формат vX.Y"))

    # D004: status
    status = fm.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(("D004", f"status = '{status}', допустимые: {', '.join(sorted(VALID_STATUSES))}"))

    # D005: parent запрещён
    if "parent" in fm:
        errors.append(("D005", "Поле parent присутствует (Discussion — корневой объект)"))

    # D019: milestone
    if not fm.get("milestone"):
        errors.append(("D019", "Отсутствует поле milestone"))

    # D021: index
    index = fm.get("index", "")
    if index != REQUIRED_INDEX:
        errors.append(("D021", f"index = '{index}', ожидается '{REQUIRED_INDEX}'"))

    return errors


def check_heading(content: str, path: Path) -> list[tuple[str, str]]:
    """D018: Проверить совпадение NNNN в папке и заголовке."""
    errors = []

    folder_match = FOLDER_REGEX.match(path.parent.name)
    if not folder_match:
        return errors  # D001 уже покрыто

    folder_nnnn = folder_match.group(1)

    body = get_body(content)
    heading_match = HEADING_REGEX.search(body)

    if not heading_match:
        errors.append(("D018", "Заголовок '# NNNN: Тема' не найден"))
        return errors

    heading_nnnn = heading_match.group(1)

    if folder_nnnn != heading_nnnn:
        errors.append(("D018", f"NNNN в папке ({folder_nnnn}) ≠ NNNN в заголовке ({heading_nnnn})"))

    # Проверка длины темы (до 80 символов)
    theme = heading_match.group(2).strip()
    if len(theme) > 80:
        errors.append(("D018", f"Тема в заголовке ({len(theme)} символов) превышает 80 символов"))

    return errors


def check_required_sections(content: str) -> list[tuple[str, str]]:
    """D006-D007: Проверить обязательные разделы (все 6)."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # D006: Проблема / Контекст
    if not re.search(SECTION_HEADING_PREFIX + r'Проблема\s*/\s*Контекст', body_no_code, re.MULTILINE):
        errors.append(("D006", "Отсутствует раздел '## Проблема / Контекст'"))

    # D007: Критерии успеха
    if not re.search(SECTION_HEADING_PREFIX + r'Критерии успеха', body_no_code, re.MULTILINE):
        errors.append(("D007", "Отсутствует раздел '## Критерии успеха'"))

    # Остальные 4 раздела
    for section_name in SECTION_ELEMENTS:
        if not re.search(SECTION_HEADING_PREFIX + re.escape(section_name), body_no_code, re.MULTILINE):
            errors.append(("D006", f"Отсутствует обязательный раздел '## {section_name}'"))

    return errors


def check_section_content(content: str) -> list[tuple[str, str]]:
    """D022: Проверить что секции содержат элементы или заглушку."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    for section_name, element_pattern in SECTION_ELEMENTS.items():
        section_match = re.search(
            SECTION_HEADING_PREFIX + re.escape(section_name) + r'\s*\n(.*?)(?=^##\s|\Z)',
            body_no_code, re.MULTILINE | re.DOTALL
        )
        if section_match:
            section_text = section_match.group(1)
            has_elements = element_pattern.search(section_text)
            stub_pattern = SECTION_STUBS.get(section_name)
            has_stub = stub_pattern and stub_pattern.search(section_text)
            if not has_elements and not has_stub:
                errors.append(("D022", f"Секция '{section_name}' без контента и без заглушки"))

    return errors


def check_numbering(content: str) -> list[tuple[str, str]]:
    """D008-D011: Проверить уникальность нумерации элементов."""
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
    """D013-D014: Проверить маркеры при статусе > DRAFT."""
    errors = []

    fm = parse_frontmatter(content)
    status = fm.get("status", "DRAFT")

    if status in ("DRAFT", ""):
        return errors

    body = get_body(content)

    # D013: маркеры [ТРЕБУЕТ УТОЧНЕНИЯ]
    markers = re.findall(r'\[ТРЕБУЕТ УТОЧНЕНИЯ[^\]]*\]', body)
    if markers:
        errors.append(("D013", f"Найдено {len(markers)} маркеров при статусе {status}"))

    # D014: Dependency Barrier
    if '⛔ DEPENDENCY BARRIER' in body or 'DEPENDENCY BARRIER' in body:
        errors.append(("D014", f"Dependency Barrier при статусе {status}"))

    return errors


def check_zone_responsibility(content: str) -> list[tuple[str, str]]:
    """D015: Проверить зону ответственности (привязка к сервисам)."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    service_patterns = [
        (r'реализовать\s+в\s+\S+-сервис', "привязка к сервису"),
        (r'(\S+-сервис|сервис\s+\S+)\s+отвечает\s+за', "распределение ответственностей"),
        (r'в\s+(auth|gateway|api|user|payment|notification|order|billing|catalog)-сервис[еау]?\b',
         "привязка к конкретному сервису"),
    ]

    for pattern, desc in service_patterns:
        matches = re.findall(pattern, body_no_code, re.IGNORECASE)
        if matches:
            match_text = matches[0] if isinstance(matches[0], str) else matches[0]
            errors.append(("D015", f"Обнаружена {desc}: {match_text}"))
            break

    return errors


def check_readme_registration(path: Path, content: str, repo_root: Path) -> list[tuple[str, str]]:
    """D016-D017: Проверить регистрацию в README."""
    errors = []

    readme_path = repo_root / "specs" / "analysis" / "README.md"
    if not readme_path.exists():
        errors.append(("D016", f"README не найден: {readme_path}"))
        return errors

    try:
        readme_content = readme_path.read_text(encoding='utf-8')
    except Exception:
        errors.append(("D016", "Ошибка чтения README"))
        return errors

    # D016: проверить наличие записи по имени папки
    folder_name = path.parent.name
    folder_match = FOLDER_REGEX.match(folder_name)
    if not folder_match:
        return errors

    folder_nnnn = folder_match.group(1)

    # Ищем NNNN или имя папки в README
    if folder_nnnn not in readme_content and folder_name not in readme_content:
        errors.append(("D016", f"Запись для '{folder_name}' не найдена в README"))
        return errors

    # D017: проверить синхронность статуса
    fm = parse_frontmatter(content)
    fm_status = fm.get("status", "")

    if fm_status:
        table_pattern = re.compile(
            rf'\|\s*{re.escape(folder_nnnn)}\s*\|.*?({"|".join(VALID_STATUSES)})',
            re.IGNORECASE
        )
        table_match = table_pattern.search(readme_content)

        if table_match:
            readme_status = table_match.group(1).strip()
            if readme_status != fm_status:
                errors.append(("D017", f"Статус в README ({readme_status}) ≠ frontmatter ({fm_status})"))

    return errors


def check_rejected_proposals(content: str) -> list[tuple[str, str]]:
    """D024: Если секция 'Отвергнутые предложения' есть — проверить таблицу."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    section_match = re.search(
        SECTION_HEADING_PREFIX + r'Отвергнутые предложения\s*\n(.*?)(?=^##\s|\Z)',
        body_no_code, re.MULTILINE | re.DOTALL
    )
    if section_match:
        section_text = section_match.group(1)
        has_table = re.search(r'^\|', section_text, re.MULTILINE)
        has_stub = re.search(r'_Отвергнутых предложений нет\._', section_text)
        if not has_table and not has_stub:
            errors.append(("D024", "Секция 'Отвергнутые предложения' без таблицы и без заглушки"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_discussion(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать один документ дискуссии."""
    errors = []

    if not path.exists():
        return [("D001", f"Файл не найден: {path}")]

    # D001: расположение
    errors.extend(check_location(path))

    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [("D001", f"Ошибка чтения файла: {e}")]

    # D002-D005, D019-D021, D023: frontmatter
    errors.extend(check_frontmatter(content))

    # D018: NNNN совпадение
    errors.extend(check_heading(content, path))

    # D006-D007: обязательные разделы
    errors.extend(check_required_sections(content))

    # D022: секции без контента и без заглушки
    errors.extend(check_section_content(content))

    # D008-D011: нумерация
    errors.extend(check_numbering(content))

    # D013-D014: маркеры и статус
    errors.extend(check_markers_and_status(content))

    # D024: "Отвергнутые предложения" — если секция есть, должна содержать таблицу
    errors.extend(check_rejected_proposals(content))

    # D015: зона ответственности
    errors.extend(check_zone_responsibility(content))

    # D016-D017: README
    errors.extend(check_readme_registration(path, content, repo_root))

    return errors


def find_all_discussions(repo_root: Path) -> list[Path]:
    """Найти все документы дискуссий."""
    analysis_dir = repo_root / "specs" / "analysis"
    if not analysis_dir.exists():
        return []

    results = []
    for folder in sorted(analysis_dir.iterdir()):
        if folder.is_dir() and FOLDER_REGEX.match(folder.name):
            disc_file = folder / "discussion.md"
            if disc_file.exists():
                results.append(disc_file)
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
        description="Валидация документов дискуссий SDD"
    )
    parser.add_argument("path", nargs="*", help="Путь к документу дискуссии")
    parser.add_argument("--all", action="store_true", help="Проверить все дискуссии")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if args.all:
        discussions = find_all_discussions(repo_root)
        if not discussions:
            print("Дискуссии не найдены")
            sys.exit(0)
    elif args.path:
        discussions = [Path(p) for p in args.path]
    else:
        parser.print_help()
        sys.exit(2)

    all_valid = True
    results = []

    for path in discussions:
        errors = validate_discussion(path, repo_root)
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
