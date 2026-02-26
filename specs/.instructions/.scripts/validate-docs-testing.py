#!/usr/bin/env python3
"""
validate-docs-testing.py — Валидация формата specs/docs/.system/testing.md.

Проверяет frontmatter, обязательные секции, таблицы, дерево файлов,
принципы тестовых данных и пустые секции.

Использование:
    python validate-docs-testing.py [--json] [--repo <dir>]

Примеры:
    python validate-docs-testing.py
    python validate-docs-testing.py --json
    python validate-docs-testing.py --repo /path/to/repo

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

TESTING_PATH = "specs/docs/.system/testing.md"

REQUIRED_SECTIONS = [
    "Типы тестов",
    "Структура файлов",
    "Стратегия мокирования",
    "Межсервисные тесты",
    "Тестовые данные",
    "Команды запуска",
]

TABLE_COLUMNS = {
    "Типы тестов": ["Тип", "Что проверяет", "Scope", "Внешние зависимости", "Когда запускается"],
    "Стратегия мокирования": ["Уровень", "БД", "Message Broker", "Другие сервисы", "Shared-код", "Внешние API"],
}

PRINCIPLES_KEYWORDS = {
    "Независимость": ["независим", "порядок запуска", "межтестов"],
    "Минимальность": ["минимальн", "фабрик", "валидн"],
    "Изоляция": ["изоляци", "очища", "rollback", "truncate"],
}

ERROR_CODES = {
    "TST001": "Отсутствует или некорректный frontmatter",
    "TST002": "Отсутствует обязательная секция",
    "TST003": "Секции в неправильном порядке",
    "TST004": "Таблица не содержит обязательных колонок",
    "TST005": "Отсутствует обязательный элемент секции",
    "TST006": "Принципы тестовых данных неполны",
    "TST007": "Пустая обязательная секция без stub-текста",
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


def parse_frontmatter(content: str) -> dict | None:
    """Извлечь frontmatter из markdown."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    result = {}
    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def get_h2_sections(content: str) -> list[str]:
    """Извлечь все h2-секции из markdown."""
    return re.findall(r"^## (.+)$", content, re.MULTILINE)


def get_section_content(content: str, section_name: str) -> str:
    """Извлечь содержимое секции (от ## до следующего ## или конца)."""
    pattern = rf"## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return ""
    return match.group(1)


def extract_table_header(section_text: str) -> list[str]:
    """Извлечь заголовки колонок из первой таблицы в секции."""
    for line in section_text.strip().split("\n"):
        stripped = line.strip()
        if stripped.startswith("|") and "---" not in stripped:
            cols = [c.strip() for c in stripped.strip().strip("|").split("|")]
            return cols
    return []


# =============================================================================
# Валидация
# =============================================================================

def validate_frontmatter(content: str) -> list[tuple[str, str]]:
    """TST001: Проверка frontmatter."""
    errors = []
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(("TST001", "Frontmatter отсутствует"))
        return errors
    if not fm.get("description"):
        errors.append(("TST001", "Frontmatter: отсутствует поле description"))
    if not fm.get("standard"):
        errors.append(("TST001", "Frontmatter: отсутствует поле standard"))
    return errors


def validate_sections(content: str) -> list[tuple[str, str]]:
    """TST002, TST003: Проверка обязательных секций и порядка."""
    errors = []
    sections = get_h2_sections(content)

    # Check presence
    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(("TST002", f"Отсутствует секция: ## {required}"))

    # Check h1
    h1_match = re.search(r"^# .+$", content, re.MULTILINE)
    if not h1_match:
        errors.append(("TST002", "Отсутствует заголовок h1"))

    # Check order of required sections
    found_order = [s for s in sections if s in REQUIRED_SECTIONS]
    expected_order = [s for s in REQUIRED_SECTIONS if s in found_order]
    if found_order != expected_order:
        errors.append(("TST003", f"Секции в неправильном порядке. Ожидается: {', '.join(REQUIRED_SECTIONS)}"))

    return errors


def validate_tables(content: str) -> list[tuple[str, str]]:
    """TST004: Проверка таблиц с обязательными колонками."""
    errors = []

    for section_name, expected_cols in TABLE_COLUMNS.items():
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue

        header = extract_table_header(section_text)
        if not header:
            # Check for stub text
            if "*" in section_text:
                continue
            errors.append(("TST004", f"Секция «{section_name}»: таблица не найдена"))
            continue

        for col in expected_cols:
            if col not in header:
                errors.append(("TST004", f"Секция «{section_name}»: отсутствует колонка «{col}»"))

    return errors


def validate_file_tree(content: str) -> list[tuple[str, str]]:
    """TST005: Проверка дерева файлов в секции Структура файлов."""
    errors = []
    section_text = get_section_content(content, "Структура файлов")
    if not section_text:
        return errors

    # Check for code block
    if "```" not in section_text:
        errors.append(("TST005", "Секция «Структура файлов»: отсутствует code-блок с деревом"))
        return errors

    # Extract code block content
    code_match = re.search(r"```\w*\n(.*?)```", section_text, re.DOTALL)
    if not code_match:
        errors.append(("TST005", "Секция «Структура файлов»: code-блок пуст или некорректен"))
        return errors

    tree_content = code_match.group(1)

    # Check for src/ and tests/
    if "src/" not in tree_content:
        errors.append(("TST005", "Дерево файлов: отсутствует src/"))
    if "tests/" not in tree_content:
        errors.append(("TST005", "Дерево файлов: отсутствует tests/"))

    # Check for comments
    tree_lines = [line for line in tree_content.strip().split("\n") if line.strip()]
    lines_with_comments = sum(1 for line in tree_lines if "#" in line)
    if lines_with_comments == 0:
        errors.append(("TST005", "Дерево файлов: строки не содержат комментариев (#)"))

    return errors


def validate_principles(content: str) -> list[tuple[str, str]]:
    """TST006: Проверка принципов тестовых данных."""
    errors = []
    section_text = get_section_content(content, "Тестовые данные")
    if not section_text:
        return errors

    # Check for list items
    list_items = re.findall(r"^[-*]\s+.+$", section_text, re.MULTILINE)
    if len(list_items) < 3:
        errors.append(("TST006", f"Секция «Тестовые данные»: найдено {len(list_items)} принципов, минимум 3"))
        return errors

    # Check for required principle meanings
    all_principles_text = " ".join(list_items).lower()
    for display_name, keywords in PRINCIPLES_KEYWORDS.items():
        found = any(kw in all_principles_text for kw in keywords)
        if not found:
            errors.append(("TST006", f"Принципы тестовых данных: не найден принцип «{display_name}»"))

    return errors


def validate_empty_sections(content: str) -> list[tuple[str, str]]:
    """TST007: Проверка пустых секций."""
    errors = []

    for section_name in REQUIRED_SECTIONS:
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue

        stripped = section_text.strip()
        if not stripped:
            errors.append(("TST007", f"Секция «{section_name}» пуста: нужно содержание или stub-текст"))
            continue

        # Skip sections that have tables, h3, code blocks, or substantial content
        has_table = "|" in stripped and "---" in stripped
        has_h3 = "### " in stripped
        has_code = "```" in stripped
        has_bold = "**" in stripped
        has_stub = "*" in stripped and not has_bold

        if not has_table and not has_h3 and not has_code and not has_bold and not has_stub:
            if len(stripped) < 20:
                errors.append(("TST007", f"Секция «{section_name}» содержит слишком мало контента"))

    return errors


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация specs/docs/.system/testing.md (TST001-TST007)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Пути к файлам (игнорируются, проверяется specs/docs/.system/testing.md)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    testing_path = repo_root / TESTING_PATH

    # Check file exists
    if not testing_path.is_file():
        if args.json:
            result = {"file": TESTING_PATH, "errors": [{"code": "TST001", "message": "Файл не найден"}], "valid": False}
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ testing.md — файл не найден: {TESTING_PATH}")
        sys.exit(1)

    content = testing_path.read_text(encoding="utf-8")

    # Run all validations
    all_errors = []
    all_errors.extend(validate_frontmatter(content))
    all_errors.extend(validate_sections(content))
    all_errors.extend(validate_tables(content))
    all_errors.extend(validate_file_tree(content))
    all_errors.extend(validate_principles(content))
    all_errors.extend(validate_empty_sections(content))

    has_errors = len(all_errors) > 0

    # Output
    if args.json:
        result = {
            "file": TESTING_PATH,
            "errors": [{"code": code, "message": msg} for code, msg in all_errors],
            "valid": not has_errors,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not has_errors:
            print("✅ testing.md — валидация пройдена")
        else:
            print(f"❌ testing.md — {len(all_errors)} ошибок:")
            for code, msg in all_errors:
                print(f"   {code}: {msg}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
