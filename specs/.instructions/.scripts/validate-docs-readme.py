#!/usr/bin/env python3
"""
validate-docs-readme.py — Валидация формата specs/docs/README.md.

Проверяет frontmatter, обязательные секции, соответствие дерева
файловой системе, синхронизацию таблиц сервисов и технологий.

Использование:
    python validate-docs-readme.py [--json] [--repo <dir>]

Примеры:
    python validate-docs-readme.py
    python validate-docs-readme.py --json
    python validate-docs-readme.py --repo /path/to/repo

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

README_PATH = "specs/docs/README.md"
DOCS_ROOT = "specs/docs"

REQUIRED_SECTIONS = ["Сервисы", "Системные документы", "Стандарты технологий", "Дерево"]

# Files to exclude from tree/table/FS checks
EXCLUDED_FILES = {"example.md", "standard-example.md", "README.md", ".gitkeep"}

ERROR_CODES = {
    "RDM001": "Отсутствует или некорректный frontmatter",
    "RDM002": "Отсутствует обязательная секция",
    "RDM003": "Дерево не соответствует файловой системе",
    "RDM004": "Таблица сервисов рассинхронизирована",
    "RDM005": "Таблица технологий рассинхронизирована",
    "RDM006": "Нарушен алфавитный порядок",
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


def extract_tree_block(content: str) -> str | None:
    """Извлечь содержимое code-блока из секции Дерево."""
    # Find the ## Дерево section
    match = re.search(r"## Дерево\s*\n+```\s*\n(.*?)```", content, re.DOTALL)
    if not match:
        return None
    return match.group(1).strip()


def parse_tree_entries(tree_text: str) -> set[str]:
    """Извлечь пути файлов/папок из ASCII-дерева."""
    entries = set()
    for line in tree_text.split("\n"):
        # Remove tree drawing characters and comments
        cleaned = re.sub(r"^[│├└─\s]+", "", line).strip()
        if not cleaned:
            continue
        # Remove inline comments (# ...)
        cleaned = re.sub(r"\s+#.*$", "", cleaned).strip()
        # Remove trailing /
        cleaned = cleaned.rstrip("/")
        if cleaned:
            entries.add(cleaned)
    return entries


def get_fs_entries(docs_root: Path) -> set[str]:
    """Получить файлы/папки в docs/ из файловой системы."""
    entries = set()
    if not docs_root.is_dir():
        return entries

    for item in sorted(docs_root.iterdir()):
        name = item.name
        if name in EXCLUDED_FILES:
            continue
        if name == "README.md":
            continue
        if item.is_dir():
            entries.add(name)
            # Add children
            for child in sorted(item.iterdir()):
                child_name = child.name
                if child_name in EXCLUDED_FILES:
                    continue
                entries.add(child_name)
        else:
            entries.add(name)
    return entries


def extract_table_links(content: str, section_name: str) -> list[str]:
    """Извлечь ссылки из таблицы в указанной секции."""
    # Find section content (until next h2 or end)
    pattern = rf"## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return []

    section_text = match.group(1)
    # Extract markdown links [text](path)
    links = re.findall(r"\[.*?\]\((.*?)\)", section_text)
    return links


# =============================================================================
# Валидация
# =============================================================================

def validate_frontmatter(content: str) -> list[tuple[str, str]]:
    """RDM001: Проверка frontmatter."""
    errors = []
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(("RDM001", "Frontmatter отсутствует"))
        return errors
    if not fm.get("description"):
        errors.append(("RDM001", "Frontmatter: отсутствует поле description"))
    if not fm.get("standard"):
        errors.append(("RDM001", "Frontmatter: отсутствует поле standard"))
    return errors


def validate_sections(content: str) -> list[tuple[str, str]]:
    """RDM002: Проверка обязательных секций."""
    errors = []
    sections = get_h2_sections(content)

    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(("RDM002", f"Отсутствует секция: ## {required}"))

    # Check h1 header
    h1_match = re.search(r"^# .+$", content, re.MULTILINE)
    if not h1_match:
        errors.append(("RDM002", "Отсутствует заголовок h1"))

    # Check architecture link
    if "**Архитектура:**" not in content:
        errors.append(("RDM002", "Отсутствует строка **Архитектура:** с ссылкой на overview.md"))

    return errors


def validate_tree(content: str, docs_root: Path) -> list[tuple[str, str]]:
    """RDM003: Проверка соответствия дерева файловой системе."""
    errors = []
    tree_text = extract_tree_block(content)
    if tree_text is None:
        errors.append(("RDM003", "Не найден code-блок в секции Дерево"))
        return errors

    tree_entries = parse_tree_entries(tree_text) - EXCLUDED_FILES
    fs_entries = get_fs_entries(docs_root)

    # Files in FS but not in tree
    missing_in_tree = fs_entries - tree_entries
    for entry in sorted(missing_in_tree):
        errors.append(("RDM003", f"В файловой системе есть, в дереве нет: {entry}"))

    # Files in tree but not in FS
    missing_in_fs = tree_entries - fs_entries
    for entry in sorted(missing_in_fs):
        # Skip directory names that are actually parents of known entries
        if any(e.startswith(entry + "/") or entry in {"specs/docs"} for e in tree_entries):
            continue
        errors.append(("RDM003", f"В дереве есть, в файловой системе нет: {entry}"))

    return errors


def validate_services_table(content: str, docs_root: Path) -> list[tuple[str, str]]:
    """RDM004: Проверка таблицы сервисов."""
    errors = []
    if not docs_root.is_dir():
        return errors

    # Get actual service files
    service_files = set()
    for item in sorted(docs_root.iterdir()):
        if item.is_file() and item.suffix == ".md" and item.name not in EXCLUDED_FILES:
            service_files.add(item.name)

    # Get links from Сервисы table
    links = extract_table_links(content, "Сервисы")
    table_files = {Path(link).name for link in links if not link.startswith(".") and link.endswith(".md")} - EXCLUDED_FILES

    # Service files not in table
    for f in sorted(service_files - table_files):
        errors.append(("RDM004", f"Сервис {f} есть в docs/, но нет в таблице"))

    # Table entries not in FS
    for f in sorted(table_files - service_files):
        errors.append(("RDM004", f"Сервис {f} в таблице, но нет в docs/"))

    return errors


def validate_tech_table(content: str, docs_root: Path) -> list[tuple[str, str]]:
    """RDM005: Проверка таблицы технологий."""
    errors = []
    tech_dir = docs_root / ".technologies"
    if not tech_dir.is_dir():
        return errors

    # Get actual tech files
    tech_files = set()
    for item in sorted(tech_dir.iterdir()):
        if item.is_file() and item.name.endswith(".md") and item.name not in EXCLUDED_FILES:
            tech_files.add(item.name)

    # Get links from Стандарты технологий table
    links = extract_table_links(content, "Стандарты технологий")
    table_files = {Path(link).name for link in links if link.endswith(".md")}

    # Tech files not in table
    for f in sorted(tech_files - table_files):
        errors.append(("RDM005", f"Технология {f} есть в .technologies/, но нет в таблице"))

    # Table entries not in FS
    for f in sorted(table_files - tech_files):
        errors.append(("RDM005", f"Технология {f} в таблице, но нет в .technologies/"))

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
        description="Валидация specs/docs/README.md (RDM001-RDM006)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Пути к файлам (игнорируются, проверяется specs/docs/README.md)"
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

    readme_path = repo_root / README_PATH
    docs_root = repo_root / DOCS_ROOT

    # Check README exists
    if not readme_path.is_file():
        if args.json:
            result = {"file": README_PATH, "errors": [{"code": "RDM001", "message": "Файл не найден"}], "valid": False}
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ specs/docs/README.md — файл не найден: {README_PATH}")
        sys.exit(1)

    content = readme_path.read_text(encoding="utf-8")

    # Run all validations
    all_errors = []
    all_errors.extend(validate_frontmatter(content))
    all_errors.extend(validate_sections(content))
    all_errors.extend(validate_tree(content, docs_root))
    all_errors.extend(validate_services_table(content, docs_root))
    all_errors.extend(validate_tech_table(content, docs_root))

    has_errors = len(all_errors) > 0

    # Output
    if args.json:
        result = {
            "file": README_PATH,
            "errors": [{"code": code, "message": msg} for code, msg in all_errors],
            "valid": not has_errors,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not has_errors:
            print(f"✅ specs/docs/README.md — валидация пройдена")
        else:
            print(f"❌ specs/docs/README.md — {len(all_errors)} ошибок:")
            for code, msg in all_errors:
                print(f"   {code}: {msg}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
