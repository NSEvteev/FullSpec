#!/usr/bin/env python3
"""
validate-docs-overview.py — Валидация формата specs/docs/.system/overview.md.

Проверяет frontmatter, обязательные секции, таблицы, mermaid-схему,
сквозные потоки, консистентность сервисов, DDD-паттерны и вводные абзацы.

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
    "Карта сервисов": ["Сервис", "Зона ответственности", "Критичность", "Владеет данными", "Ключевые API"],
    "Связи между сервисами": ["Источник", "Приёмник", "Протокол", "Назначение", "Паттерн"],
    "Контекстная карта доменов": ["Домен", "Реализует сервис", "Агрегаты", "Связь с другими доменами"],
    "Shared-код": ["Пакет", "Назначение", "Владелец", "Потребители"],
}

# Секции, требующие вводный абзац перед таблицей/содержимым
SECTIONS_REQUIRING_INTRO = [
    "Карта сервисов",
    "Связи между сервисами",
    "Сквозные потоки",
    "Контекстная карта доменов",
    "Shared-код",
]

# Actors and external systems to exclude from consistency checks
KNOWN_NON_SERVICES = {"admin frontend", "backend", "gateway", "broker", "client"}

ERROR_CODES = {
    "OVW001": "Отсутствует или некорректный frontmatter",
    "OVW002": "Отсутствует обязательная секция",
    "OVW003": "Секции в неправильном порядке",
    "OVW004": "Таблица не содержит обязательных колонок",
    "OVW005": "Mermaid-схема отсутствует или некорректна",
    "OVW006": "Сквозной поток некорректен",
    "OVW007": "Консистентность сервисов нарушена",
    "OVW008": "Нарушен алфавитный порядок",
    "OVW009": "Отсутствует подраздел DDD-паттернов",
    "OVW010": "Отсутствует вводный абзац",
    "OVW011": "Некорректное значение критичности",
}

VALID_CRITICALITY_VALUES = {"critical-high", "critical-medium", "critical-low"}


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


def extract_table_rows(section_text: str) -> list[list[str]]:
    """Извлечь все строки таблицы как списки ячеек."""
    rows = []
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
            cells = [c.strip() for c in stripped.strip().strip("|").split("|")]
            rows.append(cells)
        elif in_table and not stripped.startswith("|"):
            break
    return rows


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
    """OVW005: Проверка mermaid-схемы — наличие, subgraph, узлы, связи."""
    errors = []
    section_text = get_section_content(content, "Карта сервисов")
    if not section_text:
        return errors

    if "```mermaid" not in section_text:
        errors.append(("OVW005", "Секция «Карта сервисов»: отсутствует mermaid-схема"))
        return errors

    # Extract mermaid content
    mermaid_match = re.search(r"```mermaid\s*\n(.*?)```", section_text, re.DOTALL)
    if not mermaid_match:
        errors.append(("OVW005", "Mermaid-блок не удалось распарсить"))
        return errors

    mermaid_content = mermaid_match.group(1)

    # Check for subgraph (grouping required by standard)
    if "subgraph" not in mermaid_content:
        errors.append(("OVW005", "Mermaid-схема: отсутствует subgraph (группировка по ролям обязательна)"))

    # Check for at least one node definition (NAME["label"] or NAME[label])
    if not re.search(r'\w+\[', mermaid_content):
        errors.append(("OVW005", "Mermaid-схема: не содержит узлов"))

    # Check for edges (connections between nodes)
    if "-->" not in mermaid_content and "---" not in mermaid_content:
        errors.append(("OVW005", "Mermaid-схема: не содержит связей между узлами"))

    return errors


def validate_flows(content: str) -> list[tuple[str, str]]:
    """OVW006: Проверка сквозных потоков — структура, количество, контракты."""
    errors = []
    section_text = get_section_content(content, "Сквозные потоки")
    if not section_text:
        return errors

    # Find h3 subsections
    flows = re.findall(r"^### (.+)$", section_text, re.MULTILINE)
    if not flows:
        errors.append(("OVW006", "Секция «Сквозные потоки»: нет ни одного потока (h3-подсекции)"))
        return errors

    # Check flow count (standard: 2-5)
    if len(flows) < 2:
        errors.append(("OVW006", f"Секция «Сквозные потоки»: {len(flows)} поток, требуется 2-5"))
    elif len(flows) > 5:
        errors.append(("OVW006", f"Секция «Сквозные потоки»: {len(flows)} потоков, максимум 5"))

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
        else:
            # Check that contracts section has at least one link/reference
            contracts_match = re.search(
                r"\*\*Ключевые контракты:\*\*\s*\n(.*?)(?=\n### |\n## |\Z)",
                flow_text, re.DOTALL,
            )
            if contracts_match:
                contracts_text = contracts_match.group(1).strip()
                has_link = bool(re.search(r"\[.+\]\(.+\)", contracts_text))
                has_ref = "см." in contracts_text.lower()
                if not has_link and not has_ref:
                    errors.append(("OVW006", f"Поток «{flow_name}»: раздел «Ключевые контракты» не содержит ни одной ссылки"))

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
    # Сервисы из Карты должны упоминаться в Связях
    only_in_a_not_b = services_a - services_b
    for svc in sorted(only_in_a_not_b):
        errors.append(("OVW007", f"Сервис «{svc}» есть в Карте сервисов, но отсутствует в Связях"))
    # Сервисы из Связей, отсутствующие в Карте — внешние системы (допустимо)

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

    # Single-column sort checks
    simple_checks = [
        ("Карта сервисов", 0, "Сервис"),
        ("Контекстная карта доменов", 0, "Домен"),
    ]

    for section_name, col_idx, col_name in simple_checks:
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue
        values = extract_table_column(section_text, col_idx)
        if values and values != sorted(values, key=str.lower):
            errors.append(("OVW008", f"Секция «{section_name}»: строки не в алфавитном порядке по «{col_name}»"))

    # Two-column sort for Связи: Источник (col 0), then Приёмник (col 1)
    section_text = get_section_content(content, "Связи между сервисами")
    if section_text:
        rows = extract_table_rows(section_text)
        if len(rows) >= 2:
            pairs = [(r[0].lower(), r[1].lower()) for r in rows if len(r) >= 2]
            if pairs != sorted(pairs):
                errors.append(("OVW008", "Секция «Связи между сервисами»: строки не в алфавитном порядке по «Источник» → «Приёмник»"))

    return errors


def validate_ddd(content: str) -> list[tuple[str, str]]:
    """OVW009: Проверка DDD-паттернов в Контекстной карте доменов."""
    errors = []
    section_text = get_section_content(content, "Контекстная карта доменов")
    if not section_text:
        return errors

    # Stub check — if section is just italic stub text, skip
    stripped = section_text.strip()
    if stripped.startswith("*") and stripped.endswith("*") and len(stripped) < 200:
        return errors

    # Standard requires either "DDD-паттерны связей" or "Связи между доменами" (non-DDD alternative)
    has_ddd = bool(re.search(r"DDD-паттерны связей", section_text))
    has_alt = bool(re.search(r"Связи между доменами", section_text))

    if not has_ddd and not has_alt:
        errors.append(("OVW009", "Секция «Контекстная карта доменов»: отсутствует подраздел «DDD-паттерны связей» или «Связи между доменами»"))

    return errors


def validate_intro_paragraphs(content: str) -> list[tuple[str, str]]:
    """OVW010: Проверка вводных абзацев перед таблицами/содержимым."""
    errors = []

    for section_name in SECTIONS_REQUIRING_INTRO:
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue

        # Stub check — skip if section is just italic stub text
        stripped = section_text.strip()
        if stripped.startswith("*") and stripped.endswith("*") and len(stripped) < 200:
            continue

        # First non-empty line must be regular text (not table, not mermaid, not h3)
        for line in stripped.split("\n"):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            # Structural elements that should NOT be first
            if (line_stripped.startswith("|")
                    or line_stripped.startswith("```")
                    or line_stripped.startswith("### ")):
                errors.append(("OVW010", f"Секция «{section_name}»: отсутствует вводный абзац перед таблицей/содержимым"))
            break  # Only check the first non-empty line

    return errors


def validate_criticality(content: str) -> list[tuple[str, str]]:
    """OVW011: Проверка допустимых значений колонки «Критичность» в Карте сервисов."""
    errors = []
    section_text = get_section_content(content, "Карта сервисов")
    if not section_text:
        return errors

    header = extract_table_header(section_text)
    if not header or "Критичность" not in header:
        # Missing column is caught by OVW004
        return errors

    crit_index = header.index("Критичность")
    rows = extract_table_rows(section_text)
    for row in rows:
        if crit_index < len(row):
            value = row[crit_index].strip()
            if value and value not in VALID_CRITICALITY_VALUES:
                errors.append(("OVW011", f"Некорректное значение критичности «{value}». Допустимые: critical-high, critical-medium, critical-low"))

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
        description="Валидация specs/docs/.system/overview.md (OVW001-OVW011)"
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
    all_errors.extend(validate_ddd(content))
    all_errors.extend(validate_intro_paragraphs(content))
    all_errors.extend(validate_criticality(content))

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
