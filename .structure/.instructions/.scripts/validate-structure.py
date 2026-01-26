#!/usr/bin/env python3
"""
validate-structure.py — Валидация согласованности /.structure/README.md.

Использование:
    python validate-structure.py [--repo <корень>] [--json]

Примеры:
    python validate-structure.py
    python validate-structure.py --json
    python validate-structure.py --repo /path/to/project

Проверки:
    - Дерево папок соответствует файловой системе
    - Все папки из дерева существуют
    - Все папки из ФС (кроме исключений) есть в дереве
    - Комментарии в дереве соответствуют описаниям в секциях

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Папки, которые исключаются из проверки
EXCLUDED_FOLDERS = {
    "node_modules",
    ".git",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "venv",
    ".venv",
    "env",
}


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def get_filesystem_folders(repo_root: Path) -> set[str]:
    """Получить список корневых папок из файловой системы."""
    folders = set()
    for item in repo_root.iterdir():
        if item.is_dir() and item.name not in EXCLUDED_FOLDERS:
            folders.add(item.name)
    return folders


def parse_tree_from_readme(readme_path: Path) -> dict[str, str]:
    """
    Парсить дерево папок из README.md.

    Возвращает dict: имя_папки -> комментарий
    """
    if not readme_path.exists():
        return {}

    content = readme_path.read_text(encoding="utf-8")

    # Ищем секцию "Дерево" (может быть "Дерево", "Дерево папок", "3. Дерево")
    tree_match = re.search(
        r"##\s*\d*\.?\s*Дерево.*?```(.*?)```",
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not tree_match:
        return {}

    tree_content = tree_match.group(1)
    folders = {}

    # Паттерн для корневой папки в дереве:
    # ├── .claude/                             # Комментарий
    # Корневые папки — строки без │ в начале (не вложенные)
    pattern = r"^[├└]──\s+([^/\s]+)/\s+#\s*(.*)$"

    for line in tree_content.split("\n"):
        # Пропускаем вложенные папки (начинаются с │)
        stripped = line.lstrip()
        if stripped.startswith("│"):
            continue

        match = re.match(pattern, stripped)
        if match:
            folder_name = match.group(1)
            comment = match.group(2).strip()
            folders[folder_name] = comment

    return folders


def parse_sections_from_readme(readme_path: Path) -> dict[str, str]:
    """
    Парсить описания папок из секций README.md.

    Возвращает dict: имя_папки -> краткое описание
    """
    if not readme_path.exists():
        return {}

    content = readme_path.read_text(encoding="utf-8")
    sections = {}

    # Паттерн для секции папки: ### 🔗 [folder/](path) \n\n **Описание.**
    pattern = r"###\s*🔗\s*\[([^/]+)/\]\([^)]+\)\s*\n\n\*\*([^*]+)\.\*\*"

    for match in re.finditer(pattern, content):
        folder_name = match.group(1)
        description = match.group(2).strip()
        sections[folder_name] = description

    return sections


def validate_structure(repo_root: Path) -> dict:
    """
    Валидировать структуру проекта.

    Возвращает dict с полями:
        valid: bool
        fs_folders: list — папки в файловой системе
        tree_folders: list — папки в дереве
        missing_in_tree: list — папки есть в ФС, но нет в дереве
        missing_in_fs: list — папки есть в дереве, но нет в ФС
        comment_mismatches: list — несоответствия комментариев
        errors: list[str]
        warnings: list[str]
    """
    result = {
        "valid": True,
        "fs_folders": [],
        "tree_folders": [],
        "missing_in_tree": [],
        "missing_in_fs": [],
        "comment_mismatches": [],
        "errors": [],
        "warnings": [],
    }

    structure_readme = repo_root / ".structure" / "README.md"

    # Проверка: файл существует
    if not structure_readme.exists():
        result["errors"].append(
            f"Файл /.structure/README.md не найден в {repo_root}"
        )
        result["valid"] = False
        return result

    # Получаем данные
    fs_folders = get_filesystem_folders(repo_root)
    tree_folders = parse_tree_from_readme(structure_readme)
    section_descriptions = parse_sections_from_readme(structure_readme)

    result["fs_folders"] = sorted(fs_folders)
    result["tree_folders"] = sorted(tree_folders.keys())

    # Проверка 1: папки из ФС есть в дереве
    for folder in fs_folders:
        if folder not in tree_folders:
            result["missing_in_tree"].append(folder)
            result["errors"].append(
                f"Папка '{folder}/' существует в ФС, но отсутствует в дереве"
            )
            result["valid"] = False

    # Проверка 2: папки из дерева есть в ФС
    for folder in tree_folders:
        if folder not in fs_folders:
            result["missing_in_fs"].append(folder)
            result["errors"].append(
                f"Папка '{folder}/' в дереве, но не существует в ФС"
            )
            result["valid"] = False

    # Проверка 3: комментарии соответствуют секциям
    for folder, tree_comment in tree_folders.items():
        if folder in section_descriptions:
            section_desc = section_descriptions[folder]
            # Сравниваем начало (комментарий может быть сокращённым)
            if not tree_comment.lower().startswith(section_desc.lower()[:20]):
                # Нестрогая проверка — только предупреждение
                result["comment_mismatches"].append({
                    "folder": folder,
                    "tree_comment": tree_comment,
                    "section_description": section_desc,
                })
                result["warnings"].append(
                    f"Комментарий для '{folder}/' может не соответствовать описанию в секции"
                )

    return result


def main():
    # UTF-8 для Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация согласованности /.structure/README.md"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в JSON формате"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    result = validate_structure(repo_root)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["valid"] else 1)

    # Человекочитаемый вывод
    print(f"Проверка: {repo_root / '.structure' / 'README.md'}")
    print()

    if result["valid"] and not result["warnings"]:
        print("✅ Структура валидна")
        print()
        print(f"   Папок в ФС: {len(result['fs_folders'])}")
        print(f"   Папок в дереве: {len(result['tree_folders'])}")
        sys.exit(0)

    if result["errors"]:
        print("❌ Ошибки:")
        for error in result["errors"]:
            print(f"   • {error}")
        print()

    if result["warnings"]:
        print("⚠️  Предупреждения:")
        for warning in result["warnings"]:
            print(f"   • {warning}")
        print()

    if result["missing_in_tree"]:
        print("📁 Добавить в дерево:")
        for folder in sorted(result["missing_in_tree"]):
            print(f"   ├── {folder}/")
        print()

    if result["missing_in_fs"]:
        print("🗑️  Удалить из дерева (или создать папку):")
        for folder in sorted(result["missing_in_fs"]):
            print(f"   ├── {folder}/")
        print()

    sys.exit(1 if not result["valid"] else 0)


if __name__ == "__main__":
    main()
