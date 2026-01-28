#!/usr/bin/env python3
"""
update-references.py — Замена ссылок во всех файлах проекта.

Заменяет старый путь на новый во всех markdown-ссылках.
Используется при миграции (переименовании) файлов.

Использование:
    python update-references.py <old-path> <new-path> [--dry-run] [--repo <dir>]

Примеры:
    python update-references.py naming.md naming-conventions.md
    python update-references.py old/path.md new/path.md --dry-run
    python update-references.py ./old.md ./new.md

Возвращает:
    0 — ссылки обновлены (или --dry-run)
    1 — ссылки не найдены
    2 — ошибка
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


# =============================================================================
# Основные функции
# =============================================================================

def find_and_replace_references(
    old_path: str,
    new_path: str,
    repo_root: Path,
    dry_run: bool = False
) -> list[dict]:
    """
    Найти и заменить ссылки на файл.

    Args:
        old_path: Старый путь/имя файла
        new_path: Новый путь/имя файла
        repo_root: Корень репозитория
        dry_run: Только показать изменения, не применять

    Returns:
        Список изменённых файлов с информацией
    """
    changes = []

    for md_file in repo_root.rglob("*.md"):
        # Пропустить служебные папки
        if any(part.startswith('.') and part not in ('.instructions', '.structure', '.claude')
               for part in md_file.parts):
            continue
        if 'node_modules' in md_file.parts:
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception:
            continue

        # Проверить, есть ли ссылки на старый путь
        if old_path not in content:
            continue

        # Заменить ссылки
        new_content = content.replace(old_path, new_path)

        if new_content != content:
            rel_path = md_file.relative_to(repo_root)

            # Подсчитать количество замен
            count = content.count(old_path)

            changes.append({
                "file": str(rel_path).replace("\\", "/"),
                "count": count,
                "path": md_file
            })

            if not dry_run:
                md_file.write_text(new_content, encoding='utf-8')

    return changes


def format_output(changes: list[dict], old_path: str, new_path: str, dry_run: bool) -> str:
    """Форматировать вывод."""
    if not changes:
        return f"Ссылки на '{old_path}' не найдены"

    total = sum(c["count"] for c in changes)
    mode = "Будет заменено" if dry_run else "Заменено"

    lines = [
        f"{mode}: '{old_path}' → '{new_path}'",
        f"Файлов: {len(changes)}, ссылок: {total}",
        ""
    ]

    for change in changes:
        status = "📝" if dry_run else "✅"
        lines.append(f"{status} {change['file']} ({change['count']} ссылок)")

    if dry_run:
        lines.append("")
        lines.append("Для применения запустите без --dry-run")

    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Замена ссылок во всех файлах проекта"
    )
    parser.add_argument("old_path", help="Старый путь/имя файла")
    parser.add_argument("new_path", help="Новый путь/имя файла")
    parser.add_argument("--dry-run", action="store_true", help="Только показать изменения")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    changes = find_and_replace_references(
        args.old_path,
        args.new_path,
        repo_root,
        dry_run=args.dry_run
    )

    print(format_output(changes, args.old_path, args.new_path, args.dry_run))

    sys.exit(0 if changes else 1)


if __name__ == "__main__":
    main()
