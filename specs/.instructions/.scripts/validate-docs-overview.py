#!/usr/bin/env python3
"""
validate-docs-overview.py — Валидация формата docs/.system/overview.md.

Проверяет frontmatter, обязательные секции, таблицы, mermaid-схему,
сквозные потоки и консистентность сервисов между секциями.

Использование:
    python validate-docs-overview.py [--json] [--repo <dir>]

Примеры:
    python validate-docs-overview.py
    python validate-docs-overview.py --json
    python validate-docs-overview.py --repo /path/to/repo

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

OVERVIEW_PATH = "specs/docs/.system/overview.md"

REQUIRED_SECTIONS = [
    "Назначение системы",
    "Карта сервисов",
    "Связи между сервисами",
    "Сквозные потоки",
    "Контекстная карта доменов",
    "Shared-код",
]

TABLE_COLUMNS = {
    "Карта сервисов": ["Сервис", "Зона ответственности", "Владеет данными", "Ключевые API"],
    "Связи между сервисами": ["Источник", "Приёмник", "Протокол", "Назначение", "Паттерн"],
    "Контекстная карта доменов": ["Домен", "Реализует сервис", "Агрегаты", "Связь с другими доменами"],
    "Shared-код": ["Пакет", "Назначение", "Владелец", "Потребители"],
}

# Actors and external systems to exclude from consistency checks
KNOWN_NON_SERVICES = {"frontend", "admin frontend", "backend", "gateway", "broker", "client"}

ERROR_CODES = {
    "OVW001": "Отсутствует или некорректный frontmatter",
    "OVW002": "Отсутствует обязательная секция",
    "OVW003": "Секции в неправильном порядке",
    "OVW004": "Таблица не содержит обязательных колонок",
    "OVW005": "Отсутствует mermaid-схема",
    "OVW006": "Сквозной поток некорректен",
    "OVW007": "Консистентность сервисов нарушена",
    "OVW008": "Нарушен алфавитный порядок",
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


def extract_table_column(section_text: str, col_index: int) -> list[str]:
    """Извлечь значения колонки из markdown-таблицы."""
    values = []
    lines = section_text.strip().split("\n")
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and not in_table:
            in_table = True
            continue  # Skip header
        if in_table and stripped.startswith("|---"):
            continue  # Skip separator
        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")]
            # Remove empty first/last from split
            cells = [c for c in cells if c or cells.index(c) not in (0, len(cells) - 1)]
            cells = [c for i, c in enumerate(stripped.strip("|").split("|")) if True]
            cells = [c.strip() for c in stripped.strip().strip("|").split("|")]
            if col_index < len(cells):
                val = cells[col_index].strip()
                if val and val != "—":
                    values.append(val)
        elif in_table and not stripped.startswith("|"):
            in_table = False
    return values


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
    """OVW001: Проверка frontmatter."""
    errors = []
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(("OVW001", "Frontmatter отсутствует"))
        return errors
    if not fm.get("description"):
        errors.append(("OVW001", "Frontmatter: отсутствует поле description"))
    if not fm.get("standard"):
        errors.append(("OVW001", "Frontmatter: отсутствует поле standard"))
    return errors


def validate_sections(content: str) -> list[tuple[str, str]]:
    """OVW002, OVW003: Проверка обязательных секций и порядка."""
    errors = []
    sections = get_h2_sections(content)

    # Check presence
    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(("OVW002", f"Отсутствует секция: ## {required}"))

    # Check h1
    h1_match = re.search(r"^# .+$", content, re.MULTILINE)
    if not h1_match:
        errors.append(("OVW002", "Отсутствует заголовок h1"))

    # Check order
    found_order = [s for s in sections if s in REQUIRED_SECTIONS]
    expected_order = [s for s in REQUIRED_SECTIONS if s in found_order]
    if found_order != expected_order:
        errors.append(("OVW003", f"Секции в неправильном порядке. Ожидается: {', '.join(REQUIRED_SECTIONS)}"))

    return errors


def validate_tables(content: str) -> list[tuple[str, str]]:
    """OVW004: Проверка таблиц с обязательными колонками."""
    errors = []
    for section_name, expected_cols in TABLE_COLUMNS.items():
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue  # Section missing is caught by validate_sections

        header = extract_table_header(section_text)
        if not header:
            # Check for stub text (allowed for Shared-код)
            if section_name == "Shared-код" and "*" in section_text:
                continue
            errors.append(("OVW004", f"Секция «{section_name}»: таблица не найдена"))
            continue

        for col in expected_cols:
            if col not in header:
                errors.append(("OVW004", f"Секция «{section_name}»: отсутствует колонка «{col}»"))

    return errors


def validate_mermaid(content: str) -> list[tuple[str, str]]:
    """OVW005: Проверка наличия mermaid-схемы."""
    errors = []
    section_text = get_section_content(content, "Карта сервисов")
    if section_text and "```mermaid" not in section_text:
        errors.append(("OVW005", "Секция «Карта сервисов»: отсутствует mermaid-схема"))
    return errors


def validate_flows(content: str) -> list[tuple[str, str]]:
    """OVW006: Проверка сквозных потоков."""
    errors = []
    section_text = get_section_content(content, "Сквозные потоки")
    if not section_text:
        return errors

    # Find h3 subsections
    flows = re.findall(r"^### (.+)$", section_text, re.MULTILINE)
    if not flows:
        errors.append(("OVW006", "Секция «Сквозные потоки»: нет ни одного потока (h3-подсекции)"))
        return errors

    # Check each flow
    for flow_name in flows:
        flow_pattern = rf"### {re.escape(flow_name)}\s*\n(.*?)(?=\n### |\Z)"
        flow_match = re.search(flow_pattern, section_text, re.DOTALL)
        if not flow_match:
            continue
        flow_text = flow_match.group(1)

        if "**Участники:**" not in flow_text:
            errors.append(("OVW006", f"Поток «{flow_name}»: отсутствует строка **Участники:**"))
        if "```" not in flow_text:
            errors.append(("OVW006", f"Поток «{flow_name}»: отсутствует code-блок с шагами"))
        if "**Ключевые контракты:**" not in flow_text:
            errors.append(("OVW006", f"Поток «{flow_name}»: отсутствует раздел **Ключевые контракты:**"))

    return errors


def validate_consistency(content: str) -> list[tuple[str, str]]:
    """OVW007: Проверка консистентности сервисов между секциями."""
    errors = []

    # Set A: services from Карта сервисов (column 0)
    section_a = get_section_content(content, "Карта сервисов")
    services_a = set(extract_table_column(section_a, 0)) if section_a else set()

    # Set B: services from Связи (columns 0 and 1, excluding known non-services)
    section_b = get_section_content(content, "Связи между сервисами")
    if section_b:
        sources = extract_table_column(section_b, 0)
        targets = extract_table_column(section_b, 1)
        services_b = set(sources + targets) - KNOWN_NON_SERVICES
    else:
        services_b = set()

    # Set C: services from Контекстная карта (column 1)
    section_c = get_section_content(content, "Контекстная карта доменов")
    services_c = set(extract_table_column(section_c, 1)) if section_c else set()

    # Skip checks if stub file (no real data)
    if not services_a:
        return errors

    # Compare A vs B
    only_in_a_not_b = services_a - services_b
    only_in_b_not_a = services_b - services_a
    for svc in sorted(only_in_a_not_b):
        errors.append(("OVW007", f"Сервис «{svc}» есть в Карте сервисов, но отсутствует в Связях"))
    for svc in sorted(only_in_b_not_a):
        errors.append(("OVW007", f"Сервис «{svc}» есть в Связях, но отсутствует в Карте сервисов"))

    # Compare A vs C
    only_in_a_not_c = services_a - services_c
    only_in_c_not_a = services_c - services_a
    for svc in sorted(only_in_a_not_c):
        errors.append(("OVW007", f"Сервис «{svc}» есть в Карте сервисов, но отсутствует в Контекстной карте"))
    for svc in sorted(only_in_c_not_a):
        errors.append(("OVW007", f"Сервис «{svc}» есть в Контекстной карте, но отсутствует в Карте сервисов"))

    return errors


def validate_alphabetical(content: str) -> list[tuple[str, str]]:
    """OVW008: Проверка алфавитного порядка в таблицах."""
    errors = []

    checks = [
        ("Карта сервисов", 0, "Сервис"),
        ("Связи между сервисами", 0, "Источник"),
        ("Контекстная карта доменов", 0, "Домен"),
    ]

    for section_name, col_idx, col_name in checks:
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue
        values = extract_table_column(section_text, col_idx)
        if values and values != sorted(values, key=str.lower):
            errors.append(("OVW008", f"Секция «{section_name}»: строки не в алфавитном порядке по «{col_name}»"))

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
        description="Валидация docs/.system/overview.md (OVW001-OVW008)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Пути к файлам (игнорируются, проверяется specs/docs/.system/overview.md)"
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

    overview_path = repo_root / OVERVIEW_PATH

    # Check file exists
    if not overview_path.is_file():
        if args.json:
            result = {"file": OVERVIEW_PATH, "errors": [{"code": "OVW001", "message": "Файл не найден"}], "valid": False}
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ overview.md — файл не найден: {OVERVIEW_PATH}")
        sys.exit(1)

    content = overview_path.read_text(encoding="utf-8")

    # Run all validations
    all_errors = []
    all_errors.extend(validate_frontmatter(content))
    all_errors.extend(validate_sections(content))
    all_errors.extend(validate_tables(content))
    all_errors.extend(validate_mermaid(content))
    all_errors.extend(validate_flows(content))
    all_errors.extend(validate_consistency(content))
    all_errors.extend(validate_alphabetical(content))

    has_errors = len(all_errors) > 0

    # Output
    if args.json:
        result = {
            "file": OVERVIEW_PATH,
            "errors": [{"code": code, "message": msg} for code, msg in all_errors],
            "valid": not has_errors,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not has_errors:
            print(f"✅ overview.md — валидация пройдена")
        else:
            print(f"❌ overview.md — {len(all_errors)} ошибок:")
            for code, msg in all_errors:
                print(f"   {code}: {msg}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
