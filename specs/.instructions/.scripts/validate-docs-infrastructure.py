#!/usr/bin/env python3
"""
validate-docs-infrastructure.py — Валидация формата specs/docs/.system/infrastructure.md.

Проверяет frontmatter, обязательные секции, таблицы, хранилища,
окружения и пустые секции.

Использование:
    python validate-docs-infrastructure.py [--json] [--repo <dir>]

Примеры:
    python validate-docs-infrastructure.py
    python validate-docs-infrastructure.py --json
    python validate-docs-infrastructure.py --repo /path/to/repo

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

INFRASTRUCTURE_PATH = "specs/docs/.system/infrastructure.md"

REQUIRED_SECTIONS = [
    "Локальный запуск",
    "Сервисы и порты",
    "Хранилища",
    "Message Broker",
    "Service Discovery",
    "Окружения",
    "Мониторинг и логи",
    "Секреты",
]

TABLE_COLUMNS = {
    "Сервисы и порты": ["Сервис", "Порт", "URL", "Healthcheck"],
    "Service Discovery": ["Сервис-источник", "Сервис-цель", "Механизм"],
    "Окружения": ["Параметр", "dev"],
    "Секреты": ["Секрет", "Env-переменная"],
}

STORAGE_TABLE_COLUMNS = ["Параметр", "Значение (dev)", "Env-переменная"]

ENVIRONMENT_REQUIRED_ROWS = {
    "Реплики": ["реплик"],
    "БД": ["бд", "database", "postgresql", "mysql", "mongo", "хранилищ"],
    "Секреты": ["секрет"],
    "Домен": ["домен", "domain"],
    "Логирование": ["логир", "logging"],
}

ERROR_CODES = {
    "INF001": "Отсутствует или некорректный frontmatter",
    "INF002": "Отсутствует обязательная секция",
    "INF003": "Секции в неправильном порядке",
    "INF004": "Таблица не содержит обязательных колонок",
    "INF005": "Хранилище без обязательного элемента",
    "INF006": "Таблица Окружений без обязательных строк",
    "INF007": "Пустая обязательная секция без stub-текста",
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


def get_table_rows(section_text: str) -> list[list[str]]:
    """Извлечь строки данных из первой таблицы в секции."""
    rows = []
    in_table = False
    past_separator = False
    for line in section_text.strip().split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table and past_separator:
                break
            continue
        in_table = True
        if re.match(r"^\|[\s\-:|]+\|", stripped):
            past_separator = True
            continue
        if past_separator:
            cols = [c.strip() for c in stripped.strip().strip("|").split("|")]
            rows.append(cols)
    return rows


# =============================================================================
# Валидация
# =============================================================================

def validate_frontmatter(content: str) -> list[tuple[str, str]]:
    """INF001: Проверка frontmatter."""
    errors = []
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(("INF001", "Frontmatter отсутствует"))
        return errors
    if not fm.get("description"):
        errors.append(("INF001", "Frontmatter: отсутствует поле description"))
    if not fm.get("standard"):
        errors.append(("INF001", "Frontmatter: отсутствует поле standard"))
    return errors


def validate_sections(content: str) -> list[tuple[str, str]]:
    """INF002, INF003: Проверка обязательных секций и порядка."""
    errors = []
    sections = get_h2_sections(content)

    # Check presence
    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(("INF002", f"Отсутствует секция: ## {required}"))

    # Check h1
    h1_match = re.search(r"^# .+$", content, re.MULTILINE)
    if not h1_match:
        errors.append(("INF002", "Отсутствует заголовок h1"))

    # Check order of required sections
    found_order = [s for s in sections if s in REQUIRED_SECTIONS]
    expected_order = [s for s in REQUIRED_SECTIONS if s in found_order]
    if found_order != expected_order:
        errors.append(("INF003", f"Секции в неправильном порядке. Ожидается: {', '.join(REQUIRED_SECTIONS)}"))

    return errors


def validate_tables(content: str) -> list[tuple[str, str]]:
    """INF004: Проверка таблиц с обязательными колонками."""
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
            errors.append(("INF004", f"Секция «{section_name}»: таблица не найдена"))
            continue

        for col in expected_cols:
            if col not in header:
                errors.append(("INF004", f"Секция «{section_name}»: отсутствует колонка «{col}»"))

    return errors


def validate_storages(content: str) -> list[tuple[str, str]]:
    """INF005: Проверка структуры хранилищ."""
    errors = []
    section_text = get_section_content(content, "Хранилища")
    if not section_text:
        return errors

    # Find h3 subsections
    storages = re.findall(r"^### (.+)$", section_text, re.MULTILINE)
    if not storages:
        # No storages — check for stub text
        if "*" not in section_text:
            errors.append(("INF007", "Секция «Хранилища» пуста: нужен stub-текст в курсиве или h3-подсекции"))
        return errors

    for storage_name in storages:
        pkg_pattern = rf"### {re.escape(storage_name)}\s*\n(.*?)(?=\n### |\Z)"
        pkg_match = re.search(pkg_pattern, section_text, re.DOTALL)
        if not pkg_match:
            continue
        storage_text = pkg_match.group(1)

        # Check for table
        header = extract_table_header(storage_text)
        if not header:
            errors.append(("INF005", f"Хранилище «{storage_name}»: отсутствует таблица параметров"))
        else:
            for col in STORAGE_TABLE_COLUMNS:
                if col not in header:
                    errors.append(("INF005", f"Хранилище «{storage_name}»: отсутствует колонка «{col}»"))

        # Check for connection string
        if "**Connection string:**" not in storage_text:
            errors.append(("INF005", f"Хранилище «{storage_name}»: отсутствует Connection string"))

    return errors


def validate_environments(content: str) -> list[tuple[str, str]]:
    """INF006: Проверка обязательных строк таблицы Окружений."""
    errors = []
    section_text = get_section_content(content, "Окружения")
    if not section_text:
        return errors

    rows = get_table_rows(section_text)
    if not rows:
        return errors

    # Get first column values (parameter names)
    param_names = [row[0].lower() if row else "" for row in rows]
    all_params = " ".join(param_names)

    for display_name, keywords in ENVIRONMENT_REQUIRED_ROWS.items():
        found = any(kw in all_params for kw in keywords)
        if not found:
            errors.append(("INF006", f"Таблица Окружений: отсутствует строка «{display_name}»"))

    return errors


def validate_empty_sections(content: str) -> list[tuple[str, str]]:
    """INF007: Проверка пустых секций."""
    errors = []

    for section_name in REQUIRED_SECTIONS:
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue

        stripped = section_text.strip()
        if not stripped:
            errors.append(("INF007", f"Секция «{section_name}» пуста: нужен содержание или stub-текст"))
            continue

        # Skip sections that have tables, h3, code blocks, or substantial content
        has_table = "|" in stripped and "---" in stripped
        has_h3 = "### " in stripped
        has_code = "```" in stripped
        has_bold = "**" in stripped
        has_stub = "*" in stripped and not has_bold

        if not has_table and not has_h3 and not has_code and not has_bold and not has_stub:
            # Check if it's just whitespace or very minimal
            if len(stripped) < 20:
                errors.append(("INF007", f"Секция «{section_name}» содержит слишком мало контента"))

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
        description="Валидация specs/docs/.system/infrastructure.md (INF001-INF007)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Пути к файлам (игнорируются, проверяется specs/docs/.system/infrastructure.md)"
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

    infrastructure_path = repo_root / INFRASTRUCTURE_PATH

    # Check file exists
    if not infrastructure_path.is_file():
        if args.json:
            result = {"file": INFRASTRUCTURE_PATH, "errors": [{"code": "INF001", "message": "Файл не найден"}], "valid": False}
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ infrastructure.md — файл не найден: {INFRASTRUCTURE_PATH}")
        sys.exit(1)

    content = infrastructure_path.read_text(encoding="utf-8")

    # Run all validations
    all_errors = []
    all_errors.extend(validate_frontmatter(content))
    all_errors.extend(validate_sections(content))
    all_errors.extend(validate_tables(content))
    all_errors.extend(validate_storages(content))
    all_errors.extend(validate_environments(content))
    all_errors.extend(validate_empty_sections(content))

    has_errors = len(all_errors) > 0

    # Output
    if args.json:
        result = {
            "file": INFRASTRUCTURE_PATH,
            "errors": [{"code": code, "message": msg} for code, msg in all_errors],
            "valid": not has_errors,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not has_errors:
            print(f"✅ infrastructure.md — валидация пройдена")
        else:
            print(f"❌ infrastructure.md — {len(all_errors)} ошибок:")
            for code, msg in all_errors:
                print(f"   {code}: {msg}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
