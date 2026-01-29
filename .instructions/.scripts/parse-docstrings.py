#!/usr/bin/env python3
"""
parse-docstrings.py — Поиск скриптов по описанию в docstring.

Парсит все скрипты в папках {любая папка}/.instructions/.scripts/
и выводит информацию о них. Позволяет искать по ключевым словам.

Использование:
    python parse-docstrings.py [--search <запрос>] [--path <папка>]
    python parse-docstrings.py --list
    python parse-docstrings.py --json

Примеры:
    python parse-docstrings.py --list
    python parse-docstrings.py --search "валидация"
    python parse-docstrings.py --search "frontmatter" --path .instructions/

Возвращает:
    0 — найдены скрипты
    1 — скрипты не найдены
"""

import argparse
import json
import re
import sys
from pathlib import Path


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


# =============================================================================
# Парсинг docstring
# =============================================================================

def extract_docstring(content: str) -> str | None:
    """Извлечь docstring из Python-файла."""
    # Ищем многострочный docstring после shebang
    pattern = r'^(?:#!.*\n)?(?:#.*\n)*\s*"""(.*?)"""'
    match = re.match(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Пробуем одинарные кавычки
    pattern = r"^(?:#!.*\n)?(?:#.*\n)*\s*'''(.*?)'''"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()

    return None


def parse_docstring(docstring: str) -> dict:
    """Парсит docstring в структурированный формат."""
    result = {
        "description": "",
        "usage": [],
        "examples": [],
        "returns": []
    }

    if not docstring:
        return result

    lines = docstring.split('\n')

    # Первая строка — описание
    if lines:
        result["description"] = lines[0].strip()

    # Парсим секции
    current_section = None
    section_content = []

    for line in lines[1:]:
        stripped = line.strip()

        # Проверяем начало секции
        if stripped.endswith(':') and stripped[:-1] in ('Использование', 'Примеры', 'Возвращает', 'Подкоманды', 'Проверки'):
            if current_section and section_content:
                result[current_section] = section_content
            current_section = {
                'Использование': 'usage',
                'Примеры': 'examples',
                'Возвращает': 'returns',
                'Подкоманды': 'subcommands',
                'Проверки': 'checks'
            }.get(stripped[:-1], None)
            section_content = []
        elif current_section and stripped:
            section_content.append(stripped)

    # Сохраняем последнюю секцию
    if current_section and section_content:
        result[current_section] = section_content

    return result


# =============================================================================
# Поиск скриптов
# =============================================================================

def find_all_scripts(root: Path) -> list[Path]:
    """Найти все скрипты в папках .instructions/.scripts/."""
    scripts = []

    # Паттерн: {любая папка}/.instructions/.scripts/*.py
    for scripts_dir in root.rglob('.instructions/.scripts'):
        if scripts_dir.is_dir():
            for py_file in scripts_dir.glob('*.py'):
                scripts.append(py_file)

    return sorted(scripts)


def get_script_info(script_path: Path, repo_root: Path) -> dict | None:
    """Получить информацию о скрипте."""
    try:
        content = script_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"⚠️ Ошибка чтения {script_path}: {e}", file=sys.stderr)
        return None

    docstring = extract_docstring(content)
    if not docstring:
        return None

    parsed = parse_docstring(docstring)

    return {
        "path": str(script_path.relative_to(repo_root)),
        "name": script_path.name,
        "description": parsed["description"],
        "usage": parsed.get("usage", []),
        "examples": parsed.get("examples", [])
    }


def search_scripts(scripts_info: list[dict], query: str) -> list[dict]:
    """Поиск скриптов по ключевым словам."""
    query_lower = query.lower()
    results = []

    for info in scripts_info:
        # Ищем в описании, имени, usage и examples
        searchable = ' '.join([
            info["description"],
            info["name"],
            ' '.join(info.get("usage", [])),
            ' '.join(info.get("examples", []))
        ]).lower()

        if query_lower in searchable:
            results.append(info)

    return results


# =============================================================================
# Вывод
# =============================================================================

def print_script_info(info: dict, verbose: bool = False) -> None:
    """Вывести информацию о скрипте."""
    print(f"📄 {info['name']}")
    print(f"   Путь: {info['path']}")
    print(f"   {info['description']}")

    if verbose and info.get('usage'):
        print("   Использование:")
        for line in info['usage'][:3]:
            print(f"      {line}")

    print()


def print_json(scripts_info: list[dict]) -> None:
    """Вывести в JSON формате."""
    print(json.dumps(scripts_info, ensure_ascii=False, indent=2))


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Поиск скриптов по описанию в docstring"
    )
    parser.add_argument(
        "--search", "-s",
        help="Поиск по ключевым словам"
    )
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Папка для поиска (по умолчанию: корень репозитория)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="Показать все скрипты"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Вывод в JSON формате"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Подробный вывод"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.path))

    # Находим все скрипты
    scripts = find_all_scripts(repo_root)

    if not scripts:
        print("Скрипты не найдены")
        sys.exit(1)

    # Собираем информацию
    scripts_info = []
    for script in scripts:
        info = get_script_info(script, repo_root)
        if info:
            scripts_info.append(info)

    if not scripts_info:
        print("Не удалось получить информацию о скриптах")
        sys.exit(1)

    # Поиск или список
    if args.search:
        results = search_scripts(scripts_info, args.search)
        if not results:
            print(f"Скрипты по запросу '{args.search}' не найдены")
            sys.exit(1)
        scripts_info = results

    # Вывод
    if args.json:
        print_json(scripts_info)
    else:
        print(f"Найдено скриптов: {len(scripts_info)}\n")
        for info in scripts_info:
            print_script_info(info, verbose=args.verbose)

    sys.exit(0)


if __name__ == "__main__":
    main()
