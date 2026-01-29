#!/usr/bin/env python3
"""
update-skill-refs.py — Обновление SSOT-ссылок в скиллах.

При переименовании/перемещении инструкций обновляет ссылки в SKILL.md файлах.

Использование:
    python update-skill-refs.py <старый_путь> <новый_путь>

Примеры:
    python update-skill-refs.py docs/api docs/endpoints
    python update-skill-refs.py src/utils shared/utils

Что делает:
    1. Находит все SKILL.md с ссылками на старый путь
    2. Заменяет старый путь на новый
    3. Выводит список обновлённых скиллов

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


def get_instructions_patterns(folder_path: str) -> list[str]:
    """
    Получить паттерны путей инструкций для поиска.

    Для docs/api возвращает:
    - docs/.instructions/api
    - docs/api/.instructions (альтернативный формат)
    """
    parts = folder_path.strip("/").split("/")
    root = parts[0]
    subpath = "/".join(parts[1:]) if len(parts) > 1 else ""

    patterns = []

    if subpath:
        # Подпапка: docs/.instructions/api
        patterns.append(f"{root}/.instructions/{subpath}")
    else:
        # Корневая: docs/.instructions
        patterns.append(f"{root}/.instructions")

    return patterns


# =============================================================================
# Обновление ссылок
# =============================================================================

def find_skills_with_refs(repo_root: Path, old_path: str) -> list[tuple[Path, list[str]]]:
    """
    Найти скиллы со ссылками на старый путь.

    Returns:
        Список кортежей (путь_к_SKILL.md, список_найденных_паттернов)
    """
    skills_dir = repo_root / ".claude" / "skills"
    if not skills_dir.exists():
        return []

    old_patterns = get_instructions_patterns(old_path)
    results = []

    for skill_folder in skills_dir.iterdir():
        if not skill_folder.is_dir():
            continue

        # Пропускаем удалённые
        if skill_folder.name.startswith("DELETE_"):
            continue

        skill_md = skill_folder / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")

        # Ищем любой из паттернов
        found_patterns = []
        for pattern in old_patterns:
            if pattern in content:
                found_patterns.append(pattern)

        if found_patterns:
            results.append((skill_md, found_patterns))

    return results


def update_skill_refs(
    skill_md: Path,
    old_patterns: list[str],
    new_patterns: list[str],
    dry_run: bool = False
) -> list[str]:
    """
    Обновить ссылки в SKILL.md.

    Returns:
        Список выполненных замен (old -> new)
    """
    content = skill_md.read_text(encoding="utf-8")
    original = content
    replacements = []

    for old_pattern, new_pattern in zip(old_patterns, new_patterns):
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            replacements.append(f"{old_pattern} -> {new_pattern}")

    if content != original and not dry_run:
        skill_md.write_text(content, encoding="utf-8")

    return replacements


# =============================================================================
# Основная команда
# =============================================================================

def cmd_update_refs(repo_root: Path, old_path: str, new_path: str, dry_run: bool = False) -> bool:
    """Обновить SSOT-ссылки в скиллах."""
    old_path = old_path.strip("/")
    new_path = new_path.strip("/")

    print(f"🔄 Обновление ссылок в скиллах: {old_path} -> {new_path}")
    print()

    # Паттерны для замены
    old_patterns = get_instructions_patterns(old_path)
    new_patterns = get_instructions_patterns(new_path)

    # Находим скиллы
    skills = find_skills_with_refs(repo_root, old_path)

    if not skills:
        print("📭 Скиллов со ссылками на этот путь не найдено")
        return True

    print(f"📝 Найдено скиллов: {len(skills)}")
    print()

    updated_count = 0

    for skill_md, found_patterns in skills:
        skill_name = skill_md.parent.name

        # Обновляем
        replacements = update_skill_refs(skill_md, old_patterns, new_patterns, dry_run)

        if replacements:
            prefix = "[DRY] " if dry_run else "✅ "
            print(f"{prefix}.claude/skills/{skill_name}/SKILL.md")
            for repl in replacements:
                print(f"   {repl}")
            updated_count += 1

    print()

    if dry_run:
        print(f"=== DRY RUN — {updated_count} скиллов будет обновлено ===")
    else:
        print(f"📊 Итого: {updated_count} скилл(ов) обновлено")

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
        description="Обновление SSOT-ссылок в скиллах при переименовании/перемещении инструкций",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python update-skill-refs.py docs/api docs/endpoints
  python update-skill-refs.py src/utils shared/utils --dry-run

Использовать после:
  - mirror-instructions.py rename
  - mirror-instructions.py move
"""
    )

    parser.add_argument("old_path", help="Старый путь папки")
    parser.add_argument("new_path", help="Новый путь папки")
    parser.add_argument("--repo", default=".", help="Корень репозитория")
    parser.add_argument("--dry-run", action="store_true", help="Показать без изменения")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    success = cmd_update_refs(repo_root, args.old_path, args.new_path, args.dry_run)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
