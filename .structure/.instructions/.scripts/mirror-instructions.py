#!/usr/bin/env python3
"""
mirror-instructions.py — Зеркалирование структуры в .instructions.

Подкоманды:
    create  Создать зеркало .instructions для папки
    rename  Переименовать зеркало при переименовании папки
    move    Переместить зеркало при перемещении папки

Использование:
    python mirror-instructions.py create <папка>
    python mirror-instructions.py rename <старый_путь> <новый_путь>
    python mirror-instructions.py move <старый_путь> <новый_путь>

Примеры:
    python mirror-instructions.py create docs
    python mirror-instructions.py create docs/api
    python mirror-instructions.py rename docs/api docs/endpoints
    python mirror-instructions.py move src/utils shared/utils
"""

import argparse
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

INSTRUCTIONS_DIR = ".instructions"

README_TEMPLATE = """---
description: Инструкции для {folder_name}/
index: {index_path}
---

# Инструкции для {folder_name}/

**Полезные ссылки:**
- [{folder_name}/]({folder_readme_path})
- [Структура проекта](/.structure/README.md)

## Документы

*Нет документов.*

## Скрипты

*Нет скриптов.*
"""


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


def parse_folder_path(folder_path: str) -> tuple:
    """
    Парсить путь папки.

    Returns:
        (full_path, root_folder, subpath, depth)

    Примеры:
        "docs" -> ("docs", "docs", None, 0)
        "docs/api" -> ("docs/api", "docs", "api", 1)
        "docs/api/v1" -> ("docs/api/v1", "docs", "api/v1", 2)
    """
    parts = folder_path.strip("/").split("/")
    full_path = "/".join(parts)
    root_folder = parts[0]
    subpath = "/".join(parts[1:]) if len(parts) > 1 else None
    depth = len(parts) - 1
    return full_path, root_folder, subpath, depth


def get_instructions_path(repo_root: Path, folder_path: str) -> Path:
    """
    Получить путь к зеркалу .instructions для папки.

    Примеры:
        "docs" -> repo_root/docs/.instructions/
        "docs/api" -> repo_root/docs/.instructions/api/
    """
    full_path, root_folder, subpath, depth = parse_folder_path(folder_path)

    if depth == 0:
        # Корневая папка: docs/.instructions/
        return repo_root / root_folder / INSTRUCTIONS_DIR
    else:
        # Подпапка: docs/.instructions/api/
        return repo_root / root_folder / INSTRUCTIONS_DIR / subpath


def generate_readme_content(folder_path: str, repo_root: Path) -> str:
    """Сгенерировать содержимое README.md для .instructions."""
    full_path, root_folder, subpath, depth = parse_folder_path(folder_path)

    folder_name = full_path.split("/")[-1]

    # Путь к README папки (относительно .instructions/README.md)
    if depth == 0:
        # docs/.instructions/README.md -> ../README.md
        folder_readme_path = "../README.md"
        index_path = f"{root_folder}/.instructions/README.md"
    else:
        # docs/.instructions/api/README.md -> ../../api/README.md
        ups = "../" * (depth + 1)
        folder_readme_path = f"{ups}{subpath}/README.md"
        index_path = f"{root_folder}/.instructions/README.md"

    return README_TEMPLATE.format(
        folder_name=folder_name,
        folder_readme_path=folder_readme_path,
        index_path=index_path,
    )


# =============================================================================
# CREATE — Создание зеркала
# =============================================================================

def cmd_create(repo_root: Path, folder_path: str, dry_run: bool = False) -> bool:
    """Создать зеркало .instructions для папки."""
    full_path, root_folder, subpath, depth = parse_folder_path(folder_path)

    # Проверяем существование папки
    target_folder = repo_root / full_path
    if not target_folder.exists():
        print(f"❌ Папка не существует: {target_folder}", file=sys.stderr)
        return False

    # Путь к зеркалу
    instructions_path = get_instructions_path(repo_root, folder_path)
    readme_path = instructions_path / "README.md"

    if readme_path.exists():
        print(f"⚠️  Зеркало уже существует: {readme_path}", file=sys.stderr)
        return True

    # Генерируем содержимое
    content = generate_readme_content(folder_path, repo_root)

    if dry_run:
        print(f"=== DRY RUN: {readme_path} ===")
        print(content)
        return True

    # Создаём папку и файл
    instructions_path.mkdir(parents=True, exist_ok=True)
    readme_path.write_text(content, encoding="utf-8")

    print(f"✅ Зеркало создано: {readme_path}")
    return True


# =============================================================================
# RENAME — Переименование зеркала
# =============================================================================

def cmd_rename(repo_root: Path, old_path: str, new_path: str, dry_run: bool = False) -> bool:
    """Переименовать зеркало .instructions."""
    old_full, old_root, old_subpath, old_depth = parse_folder_path(old_path)
    new_full, new_root, new_subpath, new_depth = parse_folder_path(new_path)

    # Проверяем, что корневая папка та же
    if old_root != new_root:
        print(f"❌ Переименование между разными корнями — используйте 'move'", file=sys.stderr)
        return False

    # Пути к зеркалам
    old_instructions = get_instructions_path(repo_root, old_path)
    new_instructions = get_instructions_path(repo_root, new_path)

    if not old_instructions.exists():
        print(f"⚠️  Старое зеркало не существует: {old_instructions}", file=sys.stderr)
        # Создаём новое
        return cmd_create(repo_root, new_path, dry_run)

    if new_instructions.exists():
        print(f"❌ Новое зеркало уже существует: {new_instructions}", file=sys.stderr)
        return False

    if dry_run:
        print(f"=== DRY RUN ===")
        print(f"Переименование: {old_instructions} -> {new_instructions}")
        return True

    # Переименовываем
    new_instructions.parent.mkdir(parents=True, exist_ok=True)
    old_instructions.rename(new_instructions)

    # Обновляем README внутри
    readme_path = new_instructions / "README.md"
    if readme_path.exists():
        content = generate_readme_content(new_path, repo_root)
        readme_path.write_text(content, encoding="utf-8")

    print(f"✅ Зеркало переименовано: {old_instructions.relative_to(repo_root)} -> {new_instructions.relative_to(repo_root)}")
    return True


# =============================================================================
# MOVE — Перемещение зеркала
# =============================================================================

def cmd_move(repo_root: Path, old_path: str, new_path: str, dry_run: bool = False) -> bool:
    """Переместить зеркало .instructions между корневыми папками."""
    old_full, old_root, old_subpath, old_depth = parse_folder_path(old_path)
    new_full, new_root, new_subpath, new_depth = parse_folder_path(new_path)

    # Пути к зеркалам
    old_instructions = get_instructions_path(repo_root, old_path)
    new_instructions = get_instructions_path(repo_root, new_path)

    if not old_instructions.exists():
        print(f"⚠️  Старое зеркало не существует: {old_instructions}", file=sys.stderr)
        # Создаём новое
        return cmd_create(repo_root, new_path, dry_run)

    if new_instructions.exists():
        print(f"❌ Новое зеркало уже существует: {new_instructions}", file=sys.stderr)
        return False

    if dry_run:
        print(f"=== DRY RUN ===")
        print(f"Перемещение: {old_instructions} -> {new_instructions}")
        return True

    # Перемещаем
    new_instructions.parent.mkdir(parents=True, exist_ok=True)

    # Используем shutil для перемещения между разными директориями
    import shutil
    shutil.move(str(old_instructions), str(new_instructions))

    # Обновляем README внутри
    readme_path = new_instructions / "README.md"
    if readme_path.exists():
        content = generate_readme_content(new_path, repo_root)
        readme_path.write_text(content, encoding="utf-8")

    print(f"✅ Зеркало перемещено: {old_instructions.relative_to(repo_root)} -> {new_instructions.relative_to(repo_root)}")
    return True


# =============================================================================
# Main
# =============================================================================

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Зеркалирование структуры в .instructions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python mirror-instructions.py create docs
  python mirror-instructions.py create docs/api
  python mirror-instructions.py rename docs/api docs/endpoints
  python mirror-instructions.py move src/utils shared/utils
"""
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # === CREATE ===
    create_parser = subparsers.add_parser("create", help="Создать зеркало .instructions")
    create_parser.add_argument("folder", help="Путь к папке")
    create_parser.add_argument("--repo", default=".", help="Корень репозитория")
    create_parser.add_argument("--dry-run", action="store_true", help="Показать без создания")

    # === RENAME ===
    rename_parser = subparsers.add_parser("rename", help="Переименовать зеркало")
    rename_parser.add_argument("old_path", help="Старый путь папки")
    rename_parser.add_argument("new_path", help="Новый путь папки")
    rename_parser.add_argument("--repo", default=".", help="Корень репозитория")
    rename_parser.add_argument("--dry-run", action="store_true", help="Показать без изменения")

    # === MOVE ===
    move_parser = subparsers.add_parser("move", help="Переместить зеркало")
    move_parser.add_argument("old_path", help="Старый путь папки")
    move_parser.add_argument("new_path", help="Новый путь папки")
    move_parser.add_argument("--repo", default=".", help="Корень репозитория")
    move_parser.add_argument("--dry-run", action="store_true", help="Показать без изменения")

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    if args.command == "create":
        success = cmd_create(repo_root, args.folder.strip("/"), args.dry_run)
    elif args.command == "rename":
        success = cmd_rename(repo_root, args.old_path.strip("/"), args.new_path.strip("/"), args.dry_run)
    elif args.command == "move":
        success = cmd_move(repo_root, args.old_path.strip("/"), args.new_path.strip("/"), args.dry_run)
    else:
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
