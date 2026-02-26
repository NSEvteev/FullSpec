#!/usr/bin/env python3
"""
validate-docs-readme-services.py — Валидация синхронизации specs/docs/README.md с реальным деревом.

Проверяет, что таблица «Сервисы» в specs/docs/README.md перечисляет все {svc}.md файлы
из specs/docs/ и не содержит лишних ссылок. Также проверяет, что дерево в секции «Дерево»
содержит все реальные файлы.

Использование:
    python validate-docs-readme-services.py [--json] [--repo <dir>]

Примеры:
    python validate-docs-readme-services.py
    python validate-docs-readme-services.py --json
    python validate-docs-readme-services.py --repo /path/to/repo

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
DOCS_DIR = "specs/docs"

# Подпапки, которые НЕ содержат {svc}.md
SKIP_DIRS = {".system", ".technologies", "analysis"}

ERROR_CODES = {
    "RMS001": "Файл {svc}.md не указан в таблице «Сервисы»",
    "RMS002": "В таблице «Сервисы» есть ссылка на несуществующий файл",
    "RMS003": "Файл {svc}.md не указан в секции «Дерево»",
    "RMS004": "README.md не найден",
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


def get_section_content(content: str, section_name: str) -> str:
    """Извлечь содержимое h2-секции (от ## до следующего ## или конца)."""
    pattern = rf"^## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    if not match:
        return ""
    return match.group(1)


# =============================================================================
# Поиск файлов
# =============================================================================

def find_service_files(repo_root: Path) -> set[str]:
    """Найти все {svc}.md файлы в specs/docs/ (кроме README.md и подпапок)."""
    docs_dir = repo_root / DOCS_DIR
    if not docs_dir.is_dir():
        return set()

    files = set()
    for item in docs_dir.iterdir():
        if item.is_file() and item.suffix == ".md" and item.name != "README.md":
            files.add(item.name)
    return files


def extract_services_from_table(content: str) -> set[str]:
    """Извлечь имена файлов {svc}.md из таблицы «Сервисы» в README."""
    section_text = get_section_content(content, "Сервисы")
    if not section_text:
        return set()

    # Find all markdown links to .md files (not in subdirs)
    # Pattern: [text](filename.md) or [text](./filename.md)
    links = re.findall(r"\[.*?\]\(\.?/?([^/)]+\.md)\)", section_text)

    # Filter: only direct .md files, not subdirectories
    return {link for link in links if "/" not in link and link != "README.md"}


def extract_files_from_tree(content: str) -> set[str]:
    """Извлечь имена {svc}.md файлов из секции «Дерево»."""
    section_text = get_section_content(content, "Дерево")
    if not section_text:
        return set()

    # Find all .md files in the tree that are at root level of docs/
    # Lines like: ├── notification.md  or └── example.md
    # These are NOT inside subdirectories (.system/, .technologies/)
    files = set()
    in_subdir = False
    for line in section_text.split("\n"):
        stripped = line.strip()

        # Track subdirectory context
        # Subdirectory starts: ├── .system/ or ├── .technologies/ or ├── analysis/
        if re.search(r"[├└]── \.\w+/|[├└]── \w+/", stripped):
            dirname = re.search(r"[├└]── (\.?\w+)/", stripped)
            if dirname:
                in_subdir = dirname.group(1) in SKIP_DIRS or dirname.group(1).startswith(".")

        # Root-level .md files: lines with ├── or └── and .md, not deeply indented
        # Count tree-drawing chars to determine depth
        if ".md" in stripped and ("├──" in stripped or "└──" in stripped):
            # Check indentation level — root files have minimal indentation
            md_match = re.search(r"[├└]── (.+\.md)", stripped)
            if md_match:
                filename = md_match.group(1).split("#")[0].strip()
                # Root level = indentation of 0 (just ├── or └──)
                prefix = line.split("├──")[0] if "├──" in line else line.split("└──")[0]
                # Root-level items have no │ prefix (or just spaces)
                depth = prefix.count("│")
                if depth == 0 and filename != "README.md":
                    files.add(filename)

    return files


# =============================================================================
# Валидация
# =============================================================================

def validate(repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать README.md. Возвращает список ошибок."""
    errors = []

    readme_path = repo_root / README_PATH
    if not readme_path.is_file():
        errors.append(("RMS004", f"Файл не найден: {README_PATH}"))
        return errors

    content = readme_path.read_text(encoding="utf-8")

    # Actual files on disk
    actual_files = find_service_files(repo_root)

    # Files referenced in table
    table_files = extract_services_from_table(content)

    # Files referenced in tree
    tree_files = extract_files_from_tree(content)

    # RMS001: Files on disk but not in table
    for f in sorted(actual_files - table_files):
        errors.append(("RMS001", f"Файл {f} не указан в таблице «Сервисы»"))

    # RMS002: Files in table but not on disk
    for f in sorted(table_files - actual_files):
        errors.append(("RMS002", f"В таблице «Сервисы» ссылка на несуществующий файл: {f}"))

    # RMS003: Files on disk but not in tree
    for f in sorted(actual_files - tree_files):
        errors.append(("RMS003", f"Файл {f} не указан в секции «Дерево»"))

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
        description="Валидация синхронизации specs/docs/README.md с реальным деревом (RMS001-RMS004)"
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

    all_errors = validate(repo_root)
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
            print("✅ specs/docs/README.md — синхронизация с деревом пройдена")
        else:
            print(f"❌ specs/docs/README.md — {len(all_errors)} ошибок:")
            for code, msg in all_errors:
                print(f"   {code}: {msg}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
