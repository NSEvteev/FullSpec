#!/usr/bin/env python3
"""
validate-discussion.py — Валидация документов дискуссий SDD.

Проверяет соответствие документа дискуссии стандарту standard-discussion.md.

Использование:
    python validate-discussion.py <path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-discussion.py specs/discussion/disc-0001-oauth2-authorization.md
    python validate-discussion.py --all
    python validate-discussion.py --json specs/discussion/disc-0001-oauth2-authorization.md

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

FILENAME_REGEX = re.compile(r'^disc-(\d{4})-(.+)\.md$')
HEADING_REGEX = re.compile(r'^# disc-(\d{4}):\s+(.+)$', re.MULTILINE)

VALID_STATUSES = {
    "DRAFT", "WAITING", "RUNNING", "DONE",
    "CONFLICT", "ROLLING_BACK", "REJECTED",
}

REQUIRED_STANDARD = "specs/.instructions/discussion/standard-discussion.md"
REQUIRED_INDEX = "specs/discussion/README.md"
STANDARD_VERSION_REGEX = re.compile(r'^v\d+\.\d+$')

OPTIONAL_SECTION_ELEMENTS = {
    "Фичи": re.compile(r'^### F-\d+:', re.MULTILINE),
    "User Stories": re.compile(r'^### US-\d+:', re.MULTILINE),
    "Требования": re.compile(r'^### REQ-\d+:', re.MULTILINE),
    "Предложения": re.compile(r'^### PROP-\d+:', re.MULTILINE),
}

ELEMENT_PATTERNS = {
    "F": (re.compile(r'^### F-(\d+):', re.MULTILINE), "D008"),
    "US": (re.compile(r'^### US-(\d+):', re.MULTILINE), "D009"),
    "REQ": (re.compile(r'^### REQ-(\d+):', re.MULTILINE), "D010"),
    "PROP": (re.compile(r'^### PROP-(\d+):', re.MULTILINE), "D011"),
}

ERROR_CODES = {
    "D001": "Неверный формат имени файла",
    "D002": "Отсутствует description",
    "D003": "Неверный standard",
    "D004": "Невалидный status",
    "D005": "Присутствует parent (запрещено для Discussion)",
    "D006": "Отсутствует раздел 'Проблема / Контекст'",
    "D007": "Отсутствует раздел 'Критерии успеха'",
    "D008": "Дублирование номера F-N",
    "D009": "Дублирование номера US-N",
    "D010": "Дублирование номера REQ-N",
    "D011": "Дублирование номера PROP-N",
    "D012": "REQ без Given/When/Then",
    "D013": "Маркер [ТРЕБУЕТ УТОЧНЕНИЯ] при статусе > DRAFT",
    "D014": "Dependency Barrier при статусе > DRAFT",
    "D015": "Привязка к сервису (зона ответственности)",
    "D016": "Нет записи в README",
    "D017": "Рассинхрон статуса (README ≠ frontmatter)",
    "D018": "NNNN в имени файла ≠ NNNN в заголовке",
    "D019": "Отсутствует milestone",
    "D020": "Отсутствует или неверный standard-version",
    "D021": "Неверный index",
    "D022": "Опциональная секция без элементов",
    "D023": "Description слишком длинное (> 1024 символов)",
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
            # Сохранить предыдущий список
            if current_key and isinstance(result.get(current_key), list):
                pass  # уже сохранён

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

def check_filename(path: Path) -> list[tuple[str, str]]:
    """D001: Проверить формат имени файла."""
    errors = []
    if not FILENAME_REGEX.match(path.name):
        errors.append(("D001", f"Имя '{path.name}' не соответствует disc-NNNN-topic.md"))
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
    """D018: Проверить совпадение NNNN в имени файла и заголовке."""
    errors = []

    file_match = FILENAME_REGEX.match(path.name)
    if not file_match:
        return errors  # D001 уже покрыто

    file_nnnn = file_match.group(1)

    body = get_body(content)
    heading_match = HEADING_REGEX.search(body)

    if not heading_match:
        errors.append(("D018", f"Заголовок '# disc-NNNN: Тема' не найден"))
        return errors

    heading_nnnn = heading_match.group(1)

    if file_nnnn != heading_nnnn:
        errors.append(("D018", f"NNNN в файле ({file_nnnn}) ≠ NNNN в заголовке ({heading_nnnn})"))

    return errors


def check_required_sections(content: str) -> list[tuple[str, str]]:
    """D006-D007: Проверить обязательные разделы."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # D006: Проблема / Контекст
    if not re.search(r'^## Проблема\s*/\s*Контекст', body_no_code, re.MULTILINE):
        errors.append(("D006", "Отсутствует раздел '## Проблема / Контекст'"))

    # D007: Критерии успеха
    if not re.search(r'^## Критерии успеха', body_no_code, re.MULTILINE):
        errors.append(("D007", "Отсутствует раздел '## Критерии успеха'"))

    return errors


def check_optional_sections(content: str) -> list[tuple[str, str]]:
    """D022: Проверить что опциональные секции содержат элементы."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    for section_name, element_pattern in OPTIONAL_SECTION_ELEMENTS.items():
        # Найти секцию
        section_match = re.search(
            rf'^## {re.escape(section_name)}\s*\n(.*?)(?=^## |\Z)',
            body_no_code, re.MULTILINE | re.DOTALL
        )
        if section_match:
            section_text = section_match.group(1)
            if not element_pattern.search(section_text):
                errors.append(("D022", f"Секция '{section_name}' присутствует, но не содержит элементов"))

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


def check_requirements_format(content: str) -> list[tuple[str, str]]:
    """D012: Проверить формат требований (Given/When/Then)."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    # Найти секцию Требования
    req_section = re.search(r'^## Требования\s*\n(.*?)(?=^## |\Z)', body_no_code, re.MULTILINE | re.DOTALL)
    if not req_section:
        return errors  # секция опциональна

    section_text = req_section.group(1)

    # Найти все REQ-N в секции
    req_headers = re.finditer(r'^### REQ-(\d+):\s*(.+?)$', section_text, re.MULTILINE)
    for match in req_headers:
        req_num = match.group(1)
        # Найти текст от этого REQ до следующего ### или конца секции
        start = match.end()
        next_header = re.search(r'^### ', section_text[start:], re.MULTILINE)
        end = start + next_header.start() if next_header else len(section_text)
        req_body = section_text[start:end]

        has_given = bool(re.search(r'\*\*GIVEN\*\*', req_body, re.IGNORECASE))
        has_when = bool(re.search(r'\*\*WHEN\*\*', req_body, re.IGNORECASE))
        has_then = bool(re.search(r'\*\*THEN\*\*', req_body, re.IGNORECASE))

        if not (has_given and has_when and has_then):
            missing = []
            if not has_given:
                missing.append("GIVEN")
            if not has_when:
                missing.append("WHEN")
            if not has_then:
                missing.append("THEN")
            errors.append(("D012", f"REQ-{req_num}: отсутствует {', '.join(missing)}"))

    return errors


def check_markers_and_status(content: str) -> list[tuple[str, str]]:
    """D013-D014: Проверить маркеры при статусе > DRAFT."""
    errors = []

    fm = parse_frontmatter(content)
    status = fm.get("status", "DRAFT")

    # Проверяем только если статус > DRAFT
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

    # Паттерны привязки к сервисам
    service_patterns = [
        (r'реализовать\s+в\s+\S+-сервис', "привязка к сервису"),
        (r'(\S+-сервис|сервис\s+\S+)\s+отвечает\s+за', "распределение ответственностей"),
        (r'в\s+(auth|gateway|api|user|payment|notification|order|billing|catalog)-сервис[еау]?\b', "привязка к конкретному сервису"),
    ]

    for pattern, desc in service_patterns:
        matches = re.findall(pattern, body_no_code, re.IGNORECASE)
        if matches:
            errors.append(("D015", f"Обнаружена {desc}: {matches[0] if isinstance(matches[0], str) else matches[0]}"))
            break  # одного предупреждения достаточно

    return errors


def check_readme_registration(path: Path, content: str, repo_root: Path) -> list[tuple[str, str]]:
    """D016-D017: Проверить регистрацию в README."""
    errors = []

    readme_path = repo_root / "specs" / "discussion" / "README.md"
    if not readme_path.exists():
        errors.append(("D016", f"README не найден: {readme_path}"))
        return errors

    try:
        readme_content = readme_path.read_text(encoding='utf-8')
    except Exception:
        errors.append(("D016", "Ошибка чтения README"))
        return errors

    # D016: проверить наличие записи
    file_stem = path.stem  # disc-0001-topic
    if file_stem not in readme_content and path.name not in readme_content:
        errors.append(("D016", f"Запись '{path.name}' не найдена в README"))
        return errors

    # D017: проверить синхронность статуса
    fm = parse_frontmatter(content)
    fm_status = fm.get("status", "")

    if fm_status:
        # Найти строку таблицы с именем файла
        table_pattern = re.compile(
            rf'\|[^|]*\|[^|]*{re.escape(path.name)}[^|]*\|[^|]*({"|".join(VALID_STATUSES)})[^|]*\|',
            re.IGNORECASE
        )
        # Попробовать также по stem
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
                errors.append(("D017", f"Статус в README ({readme_status}) ≠ frontmatter ({fm_status})"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_discussion(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать один документ дискуссии."""
    errors = []

    if not path.exists():
        return [("D001", f"Файл не найден: {path}")]

    # D001: формат имени
    errors.extend(check_filename(path))

    # Читаем содержимое
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

    # D022: опциональные секции без элементов
    errors.extend(check_optional_sections(content))

    # D008-D011: нумерация
    errors.extend(check_numbering(content))

    # D012: формат требований
    errors.extend(check_requirements_format(content))

    # D013-D014: маркеры и статус
    errors.extend(check_markers_and_status(content))

    # D015: зона ответственности
    errors.extend(check_zone_responsibility(content))

    # D016-D017: README
    errors.extend(check_readme_registration(path, content, repo_root))

    return errors


def find_all_discussions(repo_root: Path) -> list[Path]:
    """Найти все документы дискуссий."""
    discussion_dir = repo_root / "specs" / "discussion"
    if not discussion_dir.exists():
        return []

    return sorted(discussion_dir.glob("disc-*.md"))


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
        description="Валидация документов дискуссий SDD"
    )
    parser.add_argument("path", nargs="?", help="Путь к документу дискуссии")
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
        discussions = [Path(args.path)]
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
