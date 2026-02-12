#!/usr/bin/env python3
"""
validate-instruction.py — Валидация формата инструкций.

Проверяет соответствие инструкции стандарту standard-instruction.md.

Использование:
    python validate-instruction.py <path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-instruction.py .instructions/create-script.md
    python validate-instruction.py --all
    python validate-instruction.py --json .instructions/standard-script.md

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

VALID_PREFIXES = ("standard-", "create-", "modify-", "validation-")

ERROR_CODES = {
    "I001": "Неверное расширение (не .md)",
    "I002": "Неверное имя файла (не kebab-case)",
    "I003": "Неверное расположение (не в .instructions/)",
    "I010": "Отсутствует frontmatter",
    "I011": "Отсутствует поле description",
    "I012": "Отсутствует поле standard",
    "I013": "Отсутствует поле index",
    "I014": "Description слишком длинное (> 1024 символов)",
    "I015": "Description слишком короткое (< 50 символов)",
    "I020": "Отсутствует заголовок H1",
    "I021": "Несколько заголовков H1",
    "I022": "Отсутствует секция Оглавление",
    "I023": "Отсутствует таблица Связанные документы",
    "I024": "Отсутствует блок Полезные ссылки",
    "I025": "Отсутствует описание после H1",
    "I026": "Секции standard-инструкции должны быть пронумерованы",
    "I027": "Отсутствуют нумерованные шаги (### Шаг N:)",
    "I030": "Битая ссылка",
    "I031": "Битый якорь",
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
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    return result


def slugify(text: str) -> str:
    """Преобразовать текст в якорь (как GitHub)."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = text.strip('-')
    return text


# =============================================================================
# Проверки
# =============================================================================

def check_file(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Проверить файл: расширение, имя, расположение."""
    errors = []

    # I001: расширение
    if path.suffix != ".md":
        errors.append(("I001", f"Расширение {path.suffix}, ожидается .md"))

    # I002: kebab-case
    name = path.stem
    if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name):
        errors.append(("I002", f"Имя '{name}' не в kebab-case"))

    # I003: расположение
    try:
        rel_path = path.resolve().relative_to(repo_root)
        parts = rel_path.parts
        if ".instructions" not in parts:
            errors.append(("I003", "Файл не в папке .instructions/"))
    except ValueError:
        errors.append(("I003", "Не удалось определить расположение"))

    return errors


def check_frontmatter(content: str) -> list[tuple[str, str]]:
    """Проверить frontmatter."""
    errors = []

    # I010: наличие frontmatter
    if not content.startswith("---\n"):
        errors.append(("I010", "Отсутствует frontmatter"))
        return errors

    fm = parse_frontmatter(content)

    # I011: description
    desc = fm.get("description", "")
    if not desc:
        errors.append(("I011", "Отсутствует поле description"))
    else:
        # I014: description слишком длинное
        if len(desc) > 1024:
            errors.append(("I014", f"Description {len(desc)} символов (макс. 1024)"))
        # I015: description слишком короткое
        if len(desc) < 50:
            errors.append(("I015", f"Description {len(desc)} символов (мин. 50)"))

    # I012: standard
    if not fm.get("standard"):
        errors.append(("I012", "Отсутствует поле standard"))

    # I013: index
    if not fm.get("index"):
        errors.append(("I013", "Отсутствует поле index"))

    return errors


def remove_code_blocks(content: str) -> str:
    """Убрать блоки кода из содержимого."""
    # Убрать блоки ```...```
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Убрать инлайн-код `...`
    content = re.sub(r'`[^`]+`', '', content)
    return content


def check_structure(content: str, file_name: str = "") -> list[tuple[str, str]]:
    """Проверить структуру документа."""
    errors = []

    # Убрать frontmatter для анализа
    body = re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)

    # Убрать блоки кода для поиска заголовков
    body_no_code = remove_code_blocks(body)

    # I020, I021: заголовок H1
    h1_matches = re.findall(r'^# .+$', body_no_code, re.MULTILINE)
    if len(h1_matches) == 0:
        errors.append(("I020", "Отсутствует заголовок H1"))
    elif len(h1_matches) > 1:
        errors.append(("I021", f"Найдено {len(h1_matches)} заголовков H1"))

    # I022: оглавление
    if "## Оглавление" not in body_no_code and "## оглавление" not in body_no_code.lower():
        errors.append(("I022", "Отсутствует секция Оглавление"))

    # I023: связанные документы
    if "Связанные документы" not in body_no_code:
        errors.append(("I023", "Отсутствует таблица Связанные документы"))

    # I024: полезные ссылки
    if "**Полезные ссылки:**" not in body:
        errors.append(("I024", "Отсутствует блок Полезные ссылки"))

    # I025: описание после H1
    h1_match = re.search(r'^# .+$', body_no_code, re.MULTILINE)
    if h1_match:
        # Найти текст между H1 и следующим заголовком или блоком
        after_h1 = body_no_code[h1_match.end():].strip()
        # Убрать пустые строки и найти первый контент
        first_content = after_h1.split('\n')[0].strip() if after_h1 else ""
        # Проверить что есть текст (не начинается с ** или ## или |)
        if not first_content or first_content.startswith(('**', '##', '|', '-', '```')):
            errors.append(("I025", "Отсутствует описание после H1"))

    # I026: нумерация секций для standard-инструкций
    if file_name.startswith("standard-"):
        # Найти все H2 заголовки (исключая Оглавление, Скрипты, Скиллы)
        h2_headers = re.findall(r'^## (.+)$', body_no_code, re.MULTILINE)
        excluded = {"Оглавление", "Скрипты", "Скиллы"}
        numbered_pattern = re.compile(r'^\d+\.\s+')

        unnumbered = []
        for header in h2_headers:
            if header in excluded:
                continue
            if not numbered_pattern.match(header):
                unnumbered.append(header)

        if unnumbered:
            errors.append(("I026", f"Ненумерованные секции: {', '.join(unnumbered[:3])}{'...' if len(unnumbered) > 3 else ''}"))

    # I027: нумерованные шаги для create/modify/validation инструкций
    if file_name.startswith(("create-", "modify-", "validation-")):
        # Проверить наличие ### Шаг N: заголовков
        step_pattern = re.compile(r'^### Шаг \d+:', re.MULTILINE)
        steps = step_pattern.findall(body_no_code)

        if not steps:
            errors.append(("I027", "Отсутствуют нумерованные шаги (### Шаг N:)"))

    return errors


def check_links(content: str, file_path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Проверить ссылки в документе."""
    errors = []

    # Убрать блоки кода перед поиском ссылок
    content_no_code = remove_code_blocks(content)

    # Найти все markdown-ссылки
    links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content_no_code)

    for text, href in links:
        # Пропустить внешние ссылки
        if href.startswith(('http://', 'https://', 'mailto:')):
            continue

        # Пропустить placeholder-якоря в шаблонах
        if '#секция-' in href or '#{' in href:
            continue

        # Разделить путь и якорь
        if '#' in href:
            path_part, anchor = href.split('#', 1)
        else:
            path_part, anchor = href, None

        # Проверить путь
        if path_part:
            if path_part.startswith('/'):
                # Абсолютный путь от корня репозитория
                target = repo_root / path_part.lstrip('/')
            else:
                # Относительный путь
                target = file_path.parent / path_part

            target = target.resolve()

            if not target.exists():
                errors.append(("I030", f"Битая ссылка: {href}"))
                continue

            # Проверить якорь
            if anchor and target.suffix == '.md':
                try:
                    target_content = target.read_text(encoding='utf-8')
                    # Собрать все заголовки
                    headings = re.findall(r'^#{1,6}\s+(.+)$', target_content, re.MULTILINE)
                    slugs = [slugify(h) for h in headings]

                    if anchor not in slugs and anchor.lower() not in [s.lower() for s in slugs]:
                        errors.append(("I031", f"Битый якорь: {href}"))
                except Exception:
                    pass
        elif anchor:
            # Только якорь — проверить в текущем файле
            headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
            slugs = [slugify(h) for h in headings]

            if anchor not in slugs and anchor.lower() not in [s.lower() for s in slugs]:
                errors.append(("I031", f"Битый якорь: #{anchor}"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_instruction(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать одну инструкцию."""
    errors = []

    if not path.exists():
        return [("I001", f"Файл не найден: {path}")]

    # Проверка файла
    errors.extend(check_file(path, repo_root))

    # Читаем содержимое
    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [("I001", f"Ошибка чтения файла: {e}")]

    # Проверки содержимого
    errors.extend(check_frontmatter(content))
    errors.extend(check_structure(content, path.name))
    errors.extend(check_links(content, path, repo_root))

    return errors


def find_all_instructions(repo_root: Path) -> list[Path]:
    """Найти все инструкции в репозитории."""
    instructions = []
    for instructions_dir in repo_root.rglob(".instructions"):
        if instructions_dir.is_dir():
            for md_file in instructions_dir.glob("*.md"):
                if md_file.name != "README.md":
                    instructions.append(md_file)
    return sorted(instructions)


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
        description="Валидация формата инструкций"
    )
    parser.add_argument("path", nargs="?", help="Путь к инструкции")
    parser.add_argument("--all", action="store_true", help="Проверить все инструкции")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if args.all:
        instructions = find_all_instructions(repo_root)
        if not instructions:
            print("Инструкции не найдены")
            sys.exit(1)
    elif args.path:
        instructions = [Path(args.path)]
    else:
        parser.print_help()
        sys.exit(2)

    all_valid = True
    results = []

    for path in instructions:
        errors = validate_instruction(path, repo_root)
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
