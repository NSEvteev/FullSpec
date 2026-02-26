#!/usr/bin/env python3
"""
validate-docs-conventions.py — Валидация формата specs/docs/.system/conventions.md.

Проверяет frontmatter, обязательные секции, таблицы, code-блоки
и структуру shared-пакетов.

Использование:
    python validate-docs-conventions.py [--json] [--repo <dir>]

Примеры:
    python validate-docs-conventions.py
    python validate-docs-conventions.py --json
    python validate-docs-conventions.py --repo /path/to/repo

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

CONVENTIONS_PATH = "specs/docs/.system/conventions.md"

REQUIRED_SECTIONS = [
    "Формат ответов",
    "Формат ошибок",
    "Пагинация",
    "Аутентификация",
    "Версионирование API",
    "Shared-пакеты",
    "Логирование",
    "Требования по уровням критичности",
]

TABLE_COLUMNS = {
    "Формат ошибок": ["HTTP Status", "Код", "Когда"],
    "Пагинация": ["Параметр", "Тип", "Default", "Max", "Описание"],
}

LOGGING_TABLE_COLUMNS = {
    "уровни": ["Уровень", "Когда использовать", "Пример"],
    "поля": ["Поле", "Источник", "Описание"],
}

SECTIONS_WITH_CODE = ["Формат ошибок", "Пагинация", "Логирование"]

ERROR_CODES = {
    "CNV001": "Отсутствует или некорректный frontmatter",
    "CNV002": "Отсутствует обязательная секция",
    "CNV003": "Секции в неправильном порядке",
    "CNV004": "Таблица не содержит обязательных колонок",
    "CNV005": "Отсутствует code-блок с реализацией",
    "CNV006": "Shared-пакет без обязательного элемента",
    "CNV007": "Пустая обязательная секция без stub-текста",
    "CNV008": "Секция «Требования по уровням критичности» отсутствует или неполная",
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


def find_all_tables(section_text: str) -> list[list[str]]:
    """Найти заголовки всех таблиц в секции."""
    tables = []
    lines = section_text.strip().split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|") and "---" not in stripped:
            # Check if next line is separator
            if i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|", lines[i + 1].strip()):
                cols = [c.strip() for c in stripped.strip().strip("|").split("|")]
                tables.append(cols)
    return tables


# =============================================================================
# Валидация
# =============================================================================

def validate_frontmatter(content: str) -> list[tuple[str, str]]:
    """CNV001: Проверка frontmatter."""
    errors = []
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(("CNV001", "Frontmatter отсутствует"))
        return errors
    if not fm.get("description"):
        errors.append(("CNV001", "Frontmatter: отсутствует поле description"))
    if not fm.get("standard"):
        errors.append(("CNV001", "Frontmatter: отсутствует поле standard"))
    return errors


def validate_sections(content: str) -> list[tuple[str, str]]:
    """CNV002, CNV003: Проверка обязательных секций и порядка."""
    errors = []
    sections = get_h2_sections(content)

    # Check presence
    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(("CNV002", f"Отсутствует секция: ## {required}"))

    # Check h1
    h1_match = re.search(r"^# .+$", content, re.MULTILINE)
    if not h1_match:
        errors.append(("CNV002", "Отсутствует заголовок h1"))

    # Check order of required sections
    found_order = [s for s in sections if s in REQUIRED_SECTIONS]
    expected_order = [s for s in REQUIRED_SECTIONS if s in found_order]
    if found_order != expected_order:
        errors.append(("CNV003", f"Секции в неправильном порядке. Ожидается: {', '.join(REQUIRED_SECTIONS)}"))

    return errors


def validate_tables(content: str) -> list[tuple[str, str]]:
    """CNV004: Проверка таблиц с обязательными колонками."""
    errors = []

    # Check main tables
    for section_name, expected_cols in TABLE_COLUMNS.items():
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue

        header = extract_table_header(section_text)
        if not header:
            errors.append(("CNV004", f"Секция «{section_name}»: таблица не найдена"))
            continue

        for col in expected_cols:
            if col not in header:
                errors.append(("CNV004", f"Секция «{section_name}»: отсутствует колонка «{col}»"))

    # Check logging tables
    section_text = get_section_content(content, "Логирование")
    if section_text:
        tables = find_all_tables(section_text)
        for table_type, expected_cols in LOGGING_TABLE_COLUMNS.items():
            found = False
            for header in tables:
                if all(col in header for col in expected_cols):
                    found = True
                    break
            if not found:
                errors.append(("CNV004", f"Секция «Логирование»: таблица {table_type} не найдена или неполна"))

    return errors


def validate_code_blocks(content: str) -> list[tuple[str, str]]:
    """CNV005: Проверка наличия code-блоков с реализацией."""
    errors = []
    for section_name in SECTIONS_WITH_CODE:
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue

        # Count code blocks (``` ... ```)
        code_blocks = re.findall(r"```\w+\n.*?```", section_text, re.DOTALL)
        if not code_blocks:
            errors.append(("CNV005", f"Секция «{section_name}»: отсутствует code-блок с реализацией"))

    return errors


def validate_shared_packages(content: str) -> list[tuple[str, str]]:
    """CNV006: Проверка структуры shared-пакетов."""
    errors = []
    section_text = get_section_content(content, "Shared-пакеты")
    if not section_text:
        return errors

    # Find h3 subsections
    packages = re.findall(r"^### (.+)$", section_text, re.MULTILINE)
    if not packages:
        # No packages — check for stub text
        return validate_empty_sections(content)

    for pkg_name in packages:
        pkg_pattern = rf"### {re.escape(pkg_name)}\s*\n(.*?)(?=\n### |\Z)"
        pkg_match = re.search(pkg_pattern, section_text, re.DOTALL)
        if not pkg_match:
            continue
        pkg_text = pkg_match.group(1)

        if "**Владелец:**" not in pkg_text:
            errors.append(("CNV006", f"Пакет «{pkg_name}»: отсутствует **Владелец:**"))

        # Check for interface code block
        code_blocks = re.findall(r"```\w+\n.*?```", pkg_text, re.DOTALL)
        if len(code_blocks) < 2:
            errors.append(("CNV006", f"Пакет «{pkg_name}»: нужно минимум 2 code-блока (интерфейс + пример)"))

        # Check for table
        if "|" not in pkg_text or "---" not in pkg_text:
            errors.append(("CNV006", f"Пакет «{pkg_name}»: отсутствует таблица параметров/полей"))

    return errors


def validate_empty_sections(content: str) -> list[tuple[str, str]]:
    """CNV007: Проверка пустых секций."""
    errors = []
    section_text = get_section_content(content, "Shared-пакеты")
    if not section_text:
        return errors

    packages = re.findall(r"^### (.+)$", section_text, re.MULTILINE)
    if not packages:
        # No h3 packages — must have stub text
        if "*" not in section_text:
            errors.append(("CNV007", "Секция «Shared-пакеты» пуста: нужен stub-текст в курсиве или h3-подсекции"))

    return errors


CRITICALITY_TABLE_COLUMNS = {
    "отказоустойчивость": ["Критерий", "critical-high", "critical-medium", "critical-low"],
    "логирование": ["Критерий", "critical-high", "critical-medium", "critical-low"],
}


def validate_criticality_section(content: str) -> list[tuple[str, str]]:
    """CNV008: Проверка секции «Требования по уровням критичности»."""
    errors = []
    section_text = get_section_content(content, "Требования по уровням критичности")
    if not section_text:
        return errors  # CNV002 already catches missing section

    # Check introductory paragraph (non-empty text before first table or bold)
    stripped = section_text.strip()
    if not stripped or stripped.startswith("|"):
        errors.append(("CNV008", "Секция «Требования по уровням критичности»: отсутствует вводный абзац"))

    # Check for two tables with correct columns
    tables = find_all_tables(section_text)
    if len(tables) < 2:
        errors.append(("CNV008", "Секция «Требования по уровням критичности»: нужно минимум 2 таблицы (отказоустойчивость + логирование)"))
        return errors

    expected_cols = ["Критерий", "critical-high", "critical-medium", "critical-low"]
    valid_tables = 0
    for header in tables:
        if all(col in header for col in expected_cols):
            valid_tables += 1
    if valid_tables < 2:
        errors.append(("CNV008", "Секция «Требования по уровням критичности»: таблицы должны содержать колонки: Критерий, critical-high, critical-medium, critical-low"))

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
        description="Валидация specs/docs/.system/conventions.md (CNV001-CNV008)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Пути к файлам (игнорируются, проверяется specs/docs/.system/conventions.md)"
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

    conventions_path = repo_root / CONVENTIONS_PATH

    # Check file exists
    if not conventions_path.is_file():
        if args.json:
            result = {"file": CONVENTIONS_PATH, "errors": [{"code": "CNV001", "message": "Файл не найден"}], "valid": False}
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ conventions.md — файл не найден: {CONVENTIONS_PATH}")
        sys.exit(1)

    content = conventions_path.read_text(encoding="utf-8")

    # Run all validations
    all_errors = []
    all_errors.extend(validate_frontmatter(content))
    all_errors.extend(validate_sections(content))
    all_errors.extend(validate_tables(content))
    all_errors.extend(validate_code_blocks(content))
    all_errors.extend(validate_shared_packages(content))
    all_errors.extend(validate_empty_sections(content))
    all_errors.extend(validate_criticality_section(content))

    has_errors = len(all_errors) > 0

    # Output
    if args.json:
        result = {
            "file": CONVENTIONS_PATH,
            "errors": [{"code": code, "message": msg} for code, msg in all_errors],
            "valid": not has_errors,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not has_errors:
            print(f"✅ conventions.md — валидация пройдена")
        else:
            print(f"❌ conventions.md — {len(all_errors)} ошибок:")
            for code, msg in all_errors:
                print(f"   {code}: {msg}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
