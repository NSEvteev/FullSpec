#!/usr/bin/env python3
"""
sync-readme.py — Синхронизация дерева в README с файловой системой.

Использование:
    python sync-readme.py <путь_к_папке> [--check] [--fix]
    python sync-readme.py --all [--check] [--fix]

Проверки:
    R001 — Элемент в ФС, отсутствует в дереве README
    R002 — Элемент в дереве, отсутствует в ФС

Флаги:
    --check — Только проверка (exit 1 если расхождения)
    --fix   — Автоматическое обновление дерева в README
    --all   — Проверить все папки с README

Возвращает:
    0 — всё синхронизировано
    1 — есть расхождения
"""

import argparse
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

ERROR_CODES = {
    "R001": "Элемент в ФС, отсутствует в дереве README",
    "R002": "Элемент в дереве, отсутствует в ФС",
}

# Папки/файлы, исключённые из проверки
EXCLUDED_NAMES = {
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
    ".DS_Store",
    "Thumbs.db",
    "DELETE_*",
    ".gitkeep",  # Placeholder файлы
}

# Паттерны для исключения
EXCLUDED_PATTERNS = [
    r"^DELETE_",
    r"\.pyc$",
    r"\.pyo$",
]

# README файлы, которые проверяются другими скриптами или имеют особый формат
# README.md — корневой README проекта (описывает проект, не папку)
# .structure/README.md — SSOT всей структуры, проверяется validate-structure.py
EXCLUDED_READMES = {
    "README.md",  # Корневой README
    ".structure/README.md",
    ".structure\\README.md",  # Windows path
}


# =============================================================================
# Вспомогательные функции
# =============================================================================

def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def is_excluded(name: str) -> bool:
    """Проверить, исключён ли элемент из проверки."""
    if name in EXCLUDED_NAMES:
        return True
    for pattern in EXCLUDED_PATTERNS:
        if re.match(pattern, name):
            return True
    return False


def get_fs_items(folder_path: Path) -> dict:
    """
    Получить элементы из файловой системы.

    Возвращает dict: имя -> тип ('folder' или 'file')
    """
    items = {}
    if not folder_path.exists():
        return items

    for item in folder_path.iterdir():
        if is_excluded(item.name):
            continue
        item_type = "folder" if item.is_dir() else "file"
        items[item.name] = item_type

    return items


def parse_tree_from_readme(readme_path: Path) -> dict:
    """
    Парсить дерево из README.md.

    Поддерживает два формата:
    1. Секция "## Дерево" или "## 3. Дерево" с блоком ```
    2. Блок ``` сразу после "## Оглавление" (формат .instructions/)

    Возвращает dict: имя -> тип ('folder' или 'file')
    """
    items = {}
    if not readme_path.exists():
        return items

    content = readme_path.read_text(encoding="utf-8")

    # Формат 1: секция "## Дерево" или "## 3. Дерево"
    tree_match = re.search(
        r"##\s*\d*\.?\s*Дерево.*?```(.*?)```",
        content,
        re.DOTALL | re.IGNORECASE
    )

    # Формат 2: блок ``` после "## Оглавление" (таблица, затем ```)
    if not tree_match:
        tree_match = re.search(
            r"##\s*Оглавление.*?\|.*?\|.*?```(.*?)```",
            content,
            re.DOTALL | re.IGNORECASE
        )

    if not tree_match:
        return items

    tree_content = tree_match.group(1)

    # Паттерн для первого уровня вложенности:
    # ├── folder_name/       # comment
    # ├── file_name          # comment
    # └── file_name          # comment
    # Вложенные элементы имеют отступ (пробелы, │, или табы) перед ├── или └──
    pattern = r"^[├└]── ([^\s/]+)(/)?.*$"

    for line in tree_content.split("\n"):
        # Пропускаем строки с путём папки (например: "/.instructions/")
        if line.strip().startswith("/") or line.strip().endswith("/"):
            if "├" not in line and "└" not in line:
                continue

        # Пропускаем вложенные элементы:
        # - начинаются с пробелов/табов перед ├── или └──
        # - начинаются с │
        # Первый уровень начинается сразу с ├── или └──
        if not line.startswith("├") and not line.startswith("└"):
            continue

        match = re.match(pattern, line)
        if match:
            name = match.group(1)
            is_folder = match.group(2) == "/"
            if not is_excluded(name):
                items[name] = "folder" if is_folder else "file"

    return items


def is_excluded_readme(readme_path: Path, repo_root: Path) -> bool:
    """Проверить, исключён ли README из проверки sync-readme."""
    try:
        rel_path = readme_path.relative_to(repo_root)
        rel_str = str(rel_path).replace("\\", "/")
        return rel_str in EXCLUDED_READMES or str(rel_path) in EXCLUDED_READMES
    except ValueError:
        return False


def validate_readme_sync(folder_path: Path, repo_root: Path = None) -> dict:
    """
    Валидировать синхронизацию README с файловой системой.

    Возвращает dict с полями:
        valid: bool
        readme_path: str
        fs_items: dict
        tree_items: dict
        missing_in_tree: list — R001
        missing_in_fs: list — R002
        errors: list[str]
        skipped: bool — пропущен (исключённый README)
    """
    result = {
        "valid": True,
        "readme_path": None,
        "fs_items": {},
        "tree_items": {},
        "missing_in_tree": [],
        "missing_in_fs": [],
        "errors": [],
        "skipped": False,
    }

    readme_path = folder_path / "README.md"
    result["readme_path"] = str(readme_path)

    if not readme_path.exists():
        # Нет README — нечего проверять
        return result

    # Проверяем исключения
    if repo_root and is_excluded_readme(readme_path, repo_root):
        result["skipped"] = True
        return result

    # Получаем данные
    fs_items = get_fs_items(folder_path)
    tree_items = parse_tree_from_readme(readme_path)

    result["fs_items"] = fs_items
    result["tree_items"] = tree_items

    # Если README не содержит секции "Дерево" — пропускаем проверку
    if not tree_items:
        result["skipped"] = True
        return result

    # Проверка 1: элементы из ФС есть в дереве (R001)
    for name, item_type in fs_items.items():
        if name == "README.md":
            continue  # README не указывается сам в себе
        if name not in tree_items:
            result["missing_in_tree"].append({"name": name, "type": item_type})
            suffix = "/" if item_type == "folder" else ""
            result["errors"].append(f"R001: {ERROR_CODES['R001']}: {name}{suffix}")
            result["valid"] = False

    # Проверка 2: элементы из дерева есть в ФС (R002)
    for name, item_type in tree_items.items():
        if name not in fs_items:
            result["missing_in_fs"].append({"name": name, "type": item_type})
            suffix = "/" if item_type == "folder" else ""
            result["errors"].append(f"R002: {ERROR_CODES['R002']}: {name}{suffix}")
            result["valid"] = False

    return result


def fix_readme_tree(folder_path: Path, missing_in_tree: list, missing_in_fs: list) -> bool:
    """
    Исправить дерево в README.

    Returns:
        True если исправлено, False если ошибка
    """
    readme_path = folder_path / "README.md"
    if not readme_path.exists():
        return False

    content = readme_path.read_text(encoding="utf-8")

    # Ищем секцию "Дерево"
    tree_match = re.search(
        r"(##\s*\d*\.?\s*Дерево.*?```)(.*?)(```)",
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not tree_match:
        print(f"⚠️  Секция 'Дерево' не найдена в {readme_path}", file=sys.stderr)
        return False

    tree_content = tree_match.group(2)
    lines = tree_content.split("\n")

    # 1. Удаляем элементы R002 (есть в дереве, нет в ФС)
    names_to_remove = {item["name"] for item in missing_in_fs}
    new_lines = []
    for line in lines:
        should_keep = True
        for name in names_to_remove:
            if f"── {name}/" in line or f"── {name} " in line or line.rstrip().endswith(f"── {name}"):
                should_keep = False
                break
        if should_keep:
            new_lines.append(line)

    # 2. Добавляем элементы R001 (есть в ФС, нет в дереве)
    for item in missing_in_tree:
        name = item["name"]
        item_type = item["type"]
        suffix = "/" if item_type == "folder" else ""
        comment = "TODO: добавить описание"

        # Форматируем строку
        tree_line = f"├── {name}{suffix}"
        padding = max(1, 40 - len(tree_line))
        tree_line = f"{tree_line}{' ' * padding}# {comment}"

        # Вставляем перед последним элементом (└──)
        insert_idx = len(new_lines) - 1
        for i in range(len(new_lines) - 1, -1, -1):
            if "└── " in new_lines[i]:
                insert_idx = i
                break
            if "├── " in new_lines[i]:
                insert_idx = i + 1
                break

        new_lines.insert(insert_idx, tree_line)

    # 3. Исправляем последний коннектор (└── вместо ├──)
    last_item_idx = None
    for i in range(len(new_lines) - 1, -1, -1):
        if "├── " in new_lines[i] or "└── " in new_lines[i]:
            last_item_idx = i
            break

    if last_item_idx is not None:
        for i, line in enumerate(new_lines):
            if "├── " in line or "└── " in line:
                if i == last_item_idx:
                    new_lines[i] = line.replace("├── ", "└── ")
                else:
                    new_lines[i] = line.replace("└── ", "├── ")

    # Собираем результат
    new_tree = "\n".join(new_lines)
    new_content = content[:tree_match.start(2)] + new_tree + content[tree_match.end(2):]

    readme_path.write_text(new_content, encoding="utf-8")
    return True


def find_all_readmes(repo_root: Path) -> list:
    """
    Найти все папки с README.md для проверки.

    Исключает:
    - .git
    - node_modules
    - и другие из EXCLUDED_NAMES
    - README из EXCLUDED_READMES (проверяются другими скриптами)
    """
    readmes = []

    for readme_path in repo_root.rglob("README.md"):
        # Проверяем, не в исключённой ли папке
        parts = readme_path.relative_to(repo_root).parts
        if any(is_excluded(part) for part in parts[:-1]):
            continue

        # Проверяем, не исключённый ли README
        if is_excluded_readme(readme_path, repo_root):
            continue

        folder_path = readme_path.parent
        readmes.append(folder_path)

    return readmes


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Синхронизация дерева в README с файловой системой"
    )
    parser.add_argument(
        "folder",
        nargs="?",
        help="Путь к папке для проверки"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Проверить все папки с README"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Только проверка (exit 1 если расхождения)"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Автоматическое обновление дерева в README"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в JSON формате"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Определяем папки для проверки
    if args.all:
        folders = find_all_readmes(repo_root)
    elif args.folder:
        folder_path = Path(args.folder)
        if not folder_path.is_absolute():
            folder_path = repo_root / folder_path
        folders = [folder_path]
    else:
        print("Укажите папку или используйте --all", file=sys.stderr)
        sys.exit(1)

    # Проверяем каждую папку
    all_valid = True
    all_results = []

    for folder_path in folders:
        result = validate_readme_sync(folder_path, repo_root)
        all_results.append(result)

        # Пропускаем исключённые README
        if result.get("skipped"):
            continue

        if not result["valid"]:
            all_valid = False

            if not args.json:
                print(f"\n📁 {folder_path}")

                if result["errors"]:
                    print("   ❌ Ошибки:")
                    for error in result["errors"]:
                        print(f"      • {error}")

            # Исправляем если --fix
            if args.fix and (result["missing_in_tree"] or result["missing_in_fs"]):
                if fix_readme_tree(folder_path, result["missing_in_tree"], result["missing_in_fs"]):
                    if not args.json:
                        print("   🔧 Исправлено")
                else:
                    if not args.json:
                        print("   ⚠️  Не удалось исправить")

    # Вывод результата
    if args.json:
        import json
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    elif all_valid:
        if len(folders) == 1:
            print(f"✅ README синхронизирован: {folders[0]}")
        else:
            print(f"✅ Все README синхронизированы ({len(folders)} папок)")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
