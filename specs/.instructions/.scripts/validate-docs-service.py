#!/usr/bin/env python3
"""
validate-docs-service.py — Валидация формата specs/docs/{svc}.md.

Проверяет каждый .md файл (кроме README.md) в specs/docs/ на соответствие
standard-service.md: frontmatter, 10 обязательных секций в правильном порядке,
таблицы, подсекции API и Data Model, границы автономии, Changelog, stub-текст.

Использование:
    python validate-docs-service.py [--json] [--repo <dir>]

Примеры:
    python validate-docs-service.py
    python validate-docs-service.py --json
    python validate-docs-service.py --repo /path/to/repo

Возвращает:
    0 — валидация пройдена (все файлы корректны)
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

DOCS_DIR = "specs/docs"

# Папки, которые не содержат {svc}.md (пропускаются)
SKIP_DIRS = {".system", ".technologies", "analysis"}

REQUIRED_SECTIONS = [
    "Назначение",
    "API контракты",
    "Data Model",
    "Потоки",
    "Code Map",
    "Зависимости",
    "Доменная модель",
    "Границы автономии LLM",
    "Planned Changes",
    "Changelog",
]

# Таблицы с обязательными колонками (секция → подсекция h3 → колонки)
TABLE_COLUMNS_CODE_MAP = {
    "Tech Stack": ["Технология", "Версия", "Назначение", "Стандарт"],
    "Пакеты": ["Пакет", "Назначение", "Ключевые модули"],
    "Makefile таргеты": ["Таргет", "Команда", "Описание"],
}

TABLE_COLUMNS_DOMAIN = {
    "Агрегаты": ["Агрегат", "Описание"],
    "Доменные события": ["Событие", "Описание"],
}

# Data Model — проверяется по типу хранилища в заголовке h3
DATA_MODEL_COLUMNS = {
    "PostgreSQL": ["Колонка", "Тип", "Constraints", "Описание"],
    "Redis": ["Ключ", "Тип", "TTL", "Описание"],
    "MongoDB": ["Поле", "Тип", "Required", "Описание"],
}

VALID_CRITICALITY_VALUES = {"critical-high", "critical-medium", "critical-low"}

ERROR_CODES = {
    "SVC001": "Отсутствует или некорректный frontmatter",
    "SVC002": "Отсутствует обязательная секция",
    "SVC003": "Секции в неправильном порядке",
    "SVC004": "Таблица не содержит обязательных колонок",
    "SVC005": "Отсутствует обязательная подсекция API контрактов",
    "SVC006": "Отсутствует обязательная подсекция Data Model",
    "SVC007": "Границы автономии LLM неполны",
    "SVC008": "Changelog не содержит ни одной записи",
    "SVC009": "Пустая обязательная секция без stub-текста",
    "SVC010": "Поле criticality отсутствует или имеет недопустимое значение",
    "SVC011": "Per-service Makefile таргеты отсутствуют в Code Map",
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


def get_h3_sections(content: str) -> list[str]:
    """Извлечь все h3-секции из markdown."""
    return re.findall(r"^### (.+)$", content, re.MULTILINE)


def get_section_content(content: str, section_name: str) -> str:
    """Извлечь содержимое h2-секции (от ## до следующего ## или конца)."""
    pattern = rf"^## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    if not match:
        return ""
    return match.group(1)


def get_h3_section_content(content: str, section_name: str) -> str:
    """Извлечь содержимое h3-подсекции (от ### до следующего ###/## или конца)."""
    pattern = rf"^### {re.escape(section_name)}\s*\n(.*?)(?=\n### |\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    if not match:
        return ""
    return match.group(1)


def extract_table_header(section_text: str) -> list[str]:
    """Извлечь заголовки колонок из первой таблицы в тексте."""
    for line in section_text.strip().split("\n"):
        stripped = line.strip()
        if stripped.startswith("|") and "---" not in stripped:
            cols = [c.strip() for c in stripped.strip().strip("|").split("|")]
            return cols
    return []


def is_stub(section_text: str) -> bool:
    """Проверить, является ли секция stub-текстом (курсив)."""
    stripped = section_text.strip()
    if not stripped:
        return False
    # Stub: одна строка в курсиве *...*
    lines = [line.strip() for line in stripped.split("\n") if line.strip()]
    if len(lines) == 1 and lines[0].startswith("*") and lines[0].endswith("*"):
        return True
    return False


def has_content(section_text: str) -> bool:
    """Проверить, содержит ли секция таблицы, code-блоки, h3 или bold."""
    stripped = section_text.strip()
    has_table = "|" in stripped and "---" in stripped
    has_h3 = "### " in stripped
    has_code = "```" in stripped
    has_bold = "**" in stripped
    return has_table or has_h3 or has_code or has_bold


# =============================================================================
# Валидация
# =============================================================================

def validate_frontmatter(content: str) -> list[tuple[str, str]]:
    """SVC001, SVC010: Проверка frontmatter."""
    errors = []
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(("SVC001", "Frontmatter отсутствует"))
        return errors
    if not fm.get("description"):
        errors.append(("SVC001", "Frontmatter: отсутствует поле description"))
    if not fm.get("standard"):
        errors.append(("SVC001", "Frontmatter: отсутствует поле standard"))

    # SVC010: criticality
    criticality = fm.get("criticality")
    if not criticality:
        errors.append(("SVC010", "Frontmatter: отсутствует поле criticality"))
    elif criticality not in VALID_CRITICALITY_VALUES:
        errors.append(("SVC010", f"Frontmatter: недопустимое значение criticality «{criticality}» (допустимые: {', '.join(sorted(VALID_CRITICALITY_VALUES))})"))

    return errors


def validate_sections(content: str) -> list[tuple[str, str]]:
    """SVC002, SVC003: Проверка обязательных секций и порядка."""
    errors = []
    sections = get_h2_sections(content)

    # SVC002: Check presence
    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(("SVC002", f"Отсутствует секция: ## {required}"))

    # Check h1
    h1_match = re.search(r"^# .+$", content, re.MULTILINE)
    if not h1_match:
        errors.append(("SVC002", "Отсутствует заголовок h1"))

    # SVC003: Check order of required sections
    found_order = [s for s in sections if s in REQUIRED_SECTIONS]
    expected_order = [s for s in REQUIRED_SECTIONS if s in found_order]
    if found_order != expected_order:
        errors.append(("SVC003", f"Секции в неправильном порядке. Ожидается: {', '.join(REQUIRED_SECTIONS)}"))

    # SVC003: No extra h2 sections allowed
    extra = [s for s in sections if s not in REQUIRED_SECTIONS]
    if extra:
        errors.append(("SVC003", f"Дополнительные секции не допускаются: {', '.join(extra)}"))

    return errors


def validate_tables(content: str) -> list[tuple[str, str]]:
    """SVC004: Проверка таблиц с обязательными колонками в Code Map и Доменная модель."""
    errors = []

    # Code Map subsections
    code_map_text = get_section_content(content, "Code Map")
    if code_map_text and not is_stub(code_map_text):
        for subsection_name, expected_cols in TABLE_COLUMNS_CODE_MAP.items():
            # SVC011: Makefile таргеты — подсекция обязательна (предупреждение)
            error_code = "SVC011" if subsection_name == "Makefile таргеты" else "SVC004"
            sub_text = get_h3_section_content(code_map_text, subsection_name)
            if not sub_text:
                if subsection_name == "Makefile таргеты":
                    errors.append(("SVC011", "Code Map: отсутствует подсекция «Makefile таргеты»"))
                continue
            if is_stub(sub_text):
                continue
            header = extract_table_header(sub_text)
            if not header:
                errors.append((error_code, f"Code Map → {subsection_name}: таблица не найдена"))
                continue
            for col in expected_cols:
                if col not in header:
                    errors.append((error_code, f"Code Map → {subsection_name}: отсутствует колонка «{col}»"))

    # Доменная модель subsections
    domain_text = get_section_content(content, "Доменная модель")
    if domain_text and not is_stub(domain_text):
        for subsection_name, expected_cols in TABLE_COLUMNS_DOMAIN.items():
            sub_text = get_h3_section_content(domain_text, subsection_name)
            if not sub_text:
                continue
            if is_stub(sub_text):
                continue
            header = extract_table_header(sub_text)
            if not header:
                errors.append(("SVC004", f"Доменная модель → {subsection_name}: таблица не найдена"))
                continue
            for col in expected_cols:
                if col not in header:
                    errors.append(("SVC004", f"Доменная модель → {subsection_name}: отсутствует колонка «{col}»"))

    return errors


def validate_api_subsections(content: str) -> list[tuple[str, str]]:
    """SVC005: Проверка подсекций API контрактов."""
    errors = []
    api_text = get_section_content(content, "API контракты")
    if not api_text or is_stub(api_text):
        return errors

    # Must have at least one h3 subsection
    h3_sections = re.findall(r"^### .+$", api_text, re.MULTILINE)
    if not h3_sections:
        errors.append(("SVC005", "API контракты: нет ни одной h3-подсекции (endpoint/WebSocket/Event)"))
        return errors

    # Check each REST endpoint (starts with METHOD)
    rest_pattern = r"^### (GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS) .+$"
    rest_endpoints = re.findall(rest_pattern, api_text, re.MULTILINE)

    # Get full h3 headers for REST endpoints
    rest_headers = re.findall(r"^### (?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS) .+$", api_text, re.MULTILINE)

    for header in rest_headers:
        # Extract content between this header and next ### or ## or end
        header_escaped = re.escape(header)
        ep_match = re.search(
            rf"{header_escaped}\s*\n(.*?)(?=\n### |\n## |\Z)",
            api_text, re.DOTALL
        )
        if not ep_match:
            continue
        ep_content = ep_match.group(1)

        # Check required elements
        if "**Auth:**" not in ep_content:
            errors.append(("SVC005", f"{header}: отсутствует **Auth:**"))
        if "**Паттерн:**" not in ep_content:
            errors.append(("SVC005", f"{header}: отсутствует **Паттерн:**"))
        if "**Errors:**" not in ep_content:
            errors.append(("SVC005", f"{header}: отсутствует **Errors:**"))
        if "**Response" not in ep_content:
            # Check for reference pattern "аналогично"
            if "аналогично" not in ep_content.lower():
                errors.append(("SVC005", f"{header}: отсутствует **Response**"))

    return errors


def validate_data_model_subsections(content: str) -> list[tuple[str, str]]:
    """SVC006: Проверка подсекций Data Model."""
    errors = []
    dm_text = get_section_content(content, "Data Model")
    if not dm_text or is_stub(dm_text):
        return errors

    # Must have at least one h3 subsection
    h3_sections = re.findall(r"^### .+$", dm_text, re.MULTILINE)
    if not h3_sections:
        errors.append(("SVC006", "Data Model: нет ни одной h3-подсекции (таблица/коллекция/ключ)"))
        return errors

    # Check each h3 subsection by storage type
    for h3_header in h3_sections:
        h3_name = h3_header.replace("### ", "")

        # Determine storage type from header
        storage_type = None
        for st in DATA_MODEL_COLUMNS:
            if st.lower() in h3_name.lower():
                storage_type = st
                break

        if not storage_type:
            # Unknown storage type — skip column check
            continue

        # Get subsection content
        sub_text = get_h3_section_content(dm_text, h3_name)
        if not sub_text or is_stub(sub_text):
            continue

        expected_cols = DATA_MODEL_COLUMNS[storage_type]
        header = extract_table_header(sub_text)
        if not header:
            errors.append(("SVC006", f"Data Model → {h3_name}: таблица не найдена"))
            continue

        for col in expected_cols:
            if col not in header:
                errors.append(("SVC006", f"Data Model → {h3_name}: отсутствует колонка «{col}»"))

    return errors


def validate_autonomy(content: str) -> list[tuple[str, str]]:
    """SVC007: Проверка границ автономии LLM."""
    errors = []
    section_text = get_section_content(content, "Границы автономии LLM")
    if not section_text or is_stub(section_text):
        return errors

    required_levels = ["**Свободно:**", "**Флаг:**", "**CONFLICT:**"]
    for level in required_levels:
        if level not in section_text:
            errors.append(("SVC007", f"Границы автономии: не найден уровень {level}"))

    return errors


def validate_changelog(content: str) -> list[tuple[str, str]]:
    """SVC008: Проверка Changelog."""
    errors = []
    section_text = get_section_content(content, "Changelog")
    if not section_text:
        return errors

    if is_stub(section_text):
        errors.append(("SVC008", "Changelog не может быть stub — должна быть минимум одна запись"))
        return errors

    # Check for at least one list item or bold entry
    has_entry = bool(re.search(r"^[-*]\s+\*\*", section_text, re.MULTILINE))
    if not has_entry:
        errors.append(("SVC008", "Changelog: не найдено ни одной записи (формат: - **...**)"))

    return errors


def validate_empty_sections(content: str) -> list[tuple[str, str]]:
    """SVC009: Проверка пустых секций."""
    errors = []

    for section_name in REQUIRED_SECTIONS:
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue

        stripped = section_text.strip()
        if not stripped:
            errors.append(("SVC009", f"Секция «{section_name}» пуста: нужно содержание или stub-текст"))
            continue

        # Skip if has real content or is a valid stub
        if has_content(stripped) or is_stub(stripped):
            continue

        # Short text without formatting — likely empty or insufficient
        if len(stripped) < 20:
            errors.append(("SVC009", f"Секция «{section_name}» содержит слишком мало контента"))

    return errors


# =============================================================================
# Поиск файлов
# =============================================================================

def find_service_files(repo_root: Path) -> list[Path]:
    """Найти все {svc}.md файлы в specs/docs/ (кроме README.md и подпапок)."""
    docs_dir = repo_root / DOCS_DIR
    if not docs_dir.is_dir():
        return []

    files = []
    for item in sorted(docs_dir.iterdir()):
        if item.is_file() and item.suffix == ".md" and item.name != "README.md":
            files.append(item)
    return files


# =============================================================================
# Main
# =============================================================================

def validate_file(file_path: Path) -> list[tuple[str, str]]:
    """Валидировать один {svc}.md файл. Возвращает список ошибок."""
    content = file_path.read_text(encoding="utf-8")

    all_errors = []
    all_errors.extend(validate_frontmatter(content))
    all_errors.extend(validate_sections(content))
    all_errors.extend(validate_tables(content))
    all_errors.extend(validate_api_subsections(content))
    all_errors.extend(validate_data_model_subsections(content))
    all_errors.extend(validate_autonomy(content))
    all_errors.extend(validate_changelog(content))
    all_errors.extend(validate_empty_sections(content))

    return all_errors


def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация specs/docs/{svc}.md (SVC001-SVC011)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Пути к файлам (если указаны — проверяются только они, иначе все specs/docs/*.md)"
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

    # Determine files to validate
    if args.path:
        # Filter: only .md files in specs/docs/ (not README, not subdirs)
        files = []
        for p in args.path:
            fp = Path(p)
            if not fp.is_absolute():
                fp = repo_root / fp
            if fp.is_file() and fp.suffix == ".md":
                # Check it's in specs/docs/ and not in a subdirectory
                try:
                    rel = fp.relative_to(repo_root / DOCS_DIR)
                    if "/" not in str(rel).replace("\\", "/") and rel.name != "README.md":
                        files.append(fp)
                except ValueError:
                    pass
        if not files:
            # No relevant files in the changed set
            if args.json:
                print(json.dumps({"files": [], "errors": [], "valid": True}, ensure_ascii=False, indent=2))
            else:
                print("✅ service — нет файлов для проверки")
            sys.exit(0)
    else:
        files = find_service_files(repo_root)
        if not files:
            if args.json:
                print(json.dumps({"files": [], "errors": [], "valid": True}, ensure_ascii=False, indent=2))
            else:
                print("✅ service — нет файлов specs/docs/*.md для проверки")
            sys.exit(0)

    # Validate all files
    all_results = []
    total_errors = 0

    for file_path in files:
        rel_path = file_path.relative_to(repo_root)
        errors = validate_file(file_path)
        total_errors += len(errors)
        all_results.append({
            "file": str(rel_path).replace("\\", "/"),
            "errors": [{"code": code, "message": msg} for code, msg in errors],
            "valid": len(errors) == 0,
        })

    has_errors = total_errors > 0

    # Output
    if args.json:
        result = {
            "files": all_results,
            "total_errors": total_errors,
            "valid": not has_errors,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for r in all_results:
            if r["valid"]:
                print(f"✅ {r['file']} — валидация пройдена")
            else:
                print(f"❌ {r['file']} — {len(r['errors'])} ошибок:")
                for err in r["errors"]:
                    print(f"   {err['code']}: {err['message']}")

        if has_errors:
            print(f"\nИтого: {total_errors} ошибок в {sum(1 for r in all_results if not r['valid'])} файлах")
        else:
            print(f"\n✅ Все {len(all_results)} файлов прошли валидацию")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
