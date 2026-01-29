#!/usr/bin/env python3
"""
mark-deleted.py — Пометка инструкций и скиллов как удалённых.

При удалении папки инструкции НЕ удаляются, а помечаются префиксом DELETE_.
Это сохраняет знания, которые могут понадобиться позже.

Использование:
    python mark-deleted.py <папка>

Примеры:
    python mark-deleted.py docs/api

Что делает:
    1. Переименовывает папку: {корень}/.instructions/{папка}/ -> DELETE_{папка}/
    2. Переименовывает файлы внутри: *.md -> DELETE_*.md
    3. Находит связанные скиллы и переименовывает: skill/ -> DELETE_skill/

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
import re
import sys
from pathlib import Path


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
        (full_path, root_folder, subpath, folder_name, depth)
    """
    parts = folder_path.strip("/").split("/")
    full_path = "/".join(parts)
    root_folder = parts[0]
    subpath = "/".join(parts[1:]) if len(parts) > 1 else None
    folder_name = parts[-1]
    depth = len(parts) - 1
    return full_path, root_folder, subpath, folder_name, depth


def get_instructions_path(repo_root: Path, folder_path: str) -> Path:
    """Получить путь к зеркалу .instructions для папки."""
    full_path, root_folder, subpath, folder_name, depth = parse_folder_path(folder_path)

    if depth == 0:
        return repo_root / root_folder / ".instructions"
    else:
        return repo_root / root_folder / ".instructions" / subpath


# =============================================================================
# Поиск связанных скиллов
# =============================================================================

def find_related_skills(repo_root: Path, folder_path: str) -> list[Path]:
    """
    Найти скиллы, связанные с папкой инструкций.

    Ищет скиллы, которые:
    1. Имеют ссылку SSOT: на инструкцию из этой папки
    2. Имеют имя, содержащее путь папки (например, docs-api-*)
    """
    skills_dir = repo_root / ".claude" / "skills"
    if not skills_dir.exists():
        return []

    related = []
    full_path, root_folder, subpath, folder_name, depth = parse_folder_path(folder_path)

    # Паттерн имени скилла на основе пути (docs/api -> docs-api)
    skill_prefix = full_path.replace("/", "-")

    for skill_folder in skills_dir.iterdir():
        if not skill_folder.is_dir():
            continue

        # Пропускаем уже удалённые
        if skill_folder.name.startswith("DELETE_"):
            continue

        # Проверка 1: имя скилла содержит путь
        if skill_folder.name.startswith(skill_prefix):
            related.append(skill_folder)
            continue

        # Проверка 2: SSOT ссылается на инструкцию
        skill_md = skill_folder / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding="utf-8")
            # Ищем SSOT: ссылки на эту папку инструкций
            instructions_pattern = f"{root_folder}/.instructions"
            if subpath:
                instructions_pattern += f"/{subpath}"
            if instructions_pattern in content:
                related.append(skill_folder)

    return related


# =============================================================================
# Пометка DELETE_
# =============================================================================

def mark_folder_deleted(folder_path: Path, dry_run: bool = False) -> Path | None:
    """
    Пометить папку как удалённую (добавить префикс DELETE_).

    Returns:
        Новый путь папки или None при ошибке
    """
    if not folder_path.exists():
        return None

    parent = folder_path.parent
    old_name = folder_path.name
    new_name = f"DELETE_{old_name}"
    new_path = parent / new_name

    if new_path.exists():
        print(f"⚠️  Папка уже помечена: {new_path}", file=sys.stderr)
        return new_path

    if dry_run:
        print(f"   [DRY] {folder_path.name}/ -> {new_name}/")
        return new_path

    folder_path.rename(new_path)
    return new_path


def mark_files_deleted(folder_path: Path, dry_run: bool = False) -> int:
    """
    Пометить все .md файлы в папке как удалённые.

    Returns:
        Количество помеченных файлов
    """
    if not folder_path.exists():
        return 0

    count = 0
    for md_file in folder_path.rglob("*.md"):
        if md_file.name.startswith("DELETE_"):
            continue

        new_name = f"DELETE_{md_file.name}"
        new_path = md_file.parent / new_name

        if dry_run:
            print(f"   [DRY] {md_file.name} -> {new_name}")
        else:
            md_file.rename(new_path)

        count += 1

    return count


def mark_skill_deleted(skill_folder: Path, dry_run: bool = False) -> bool:
    """Пометить скилл как удалённый."""
    if not skill_folder.exists():
        return False

    parent = skill_folder.parent
    old_name = skill_folder.name
    new_name = f"DELETE_{old_name}"
    new_path = parent / new_name

    if new_path.exists():
        print(f"⚠️  Скилл уже помечен: {new_path}", file=sys.stderr)
        return True

    if dry_run:
        print(f"   [DRY] {old_name}/ -> {new_name}/")
        return True

    skill_folder.rename(new_path)
    return True


# =============================================================================
# Основная команда
# =============================================================================

def cmd_mark_deleted(repo_root: Path, folder_path: str, dry_run: bool = False) -> bool:
    """Пометить инструкции и связанные скиллы как удалённые."""
    full_path, root_folder, subpath, folder_name, depth = parse_folder_path(folder_path)

    print(f"🗑️  Пометка DELETE_ для: {full_path}/")
    print()

    # 1. Находим зеркало .instructions
    instructions_path = get_instructions_path(repo_root, folder_path)

    if not instructions_path.exists():
        print(f"⚠️  Зеркало не существует: {instructions_path}", file=sys.stderr)
    else:
        print(f"📁 Зеркало .instructions:")

        # 2. Помечаем файлы внутри
        files_count = mark_files_deleted(instructions_path, dry_run)
        if files_count > 0:
            print(f"   Файлов помечено: {files_count}")

        # 3. Помечаем папку
        new_path = mark_folder_deleted(instructions_path, dry_run)
        if new_path:
            rel_old = instructions_path.relative_to(repo_root)
            rel_new = new_path.relative_to(repo_root)
            if not dry_run:
                print(f"   ✅ {rel_old} -> {rel_new}")

    print()

    # 4. Находим связанные скиллы
    related_skills = find_related_skills(repo_root, folder_path)

    if related_skills:
        print(f"🔧 Связанные скиллы ({len(related_skills)}):")
        for skill_folder in related_skills:
            mark_skill_deleted(skill_folder, dry_run)
            if not dry_run:
                print(f"   ✅ {skill_folder.name}/ -> DELETE_{skill_folder.name}/")
    else:
        print("🔧 Связанных скиллов не найдено")

    print()

    if dry_run:
        print("=== DRY RUN — изменения не применены ===")
    else:
        print("✅ Готово. Теперь можно удалить папку из SSOT и файловой системы.")

    return True


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Пометка инструкций и скиллов как удалённых (DELETE_)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python mark-deleted.py docs/api
  python mark-deleted.py legacy --dry-run

При удалении папки:
  1. Запустить этот скрипт для пометки инструкций
  2. Удалить из SSOT: python ssot.py delete docs/api
  3. Удалить папку: rm -rf docs/api/
"""
    )

    parser.add_argument("folder", help="Путь к удаляемой папке")
    parser.add_argument("--repo", default=".", help="Корень репозитория")
    parser.add_argument("--dry-run", action="store_true", help="Показать без изменения")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    success = cmd_mark_deleted(repo_root, args.folder.strip("/"), args.dry_run)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
