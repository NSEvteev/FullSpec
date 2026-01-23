#!/usr/bin/env python3
"""
update_links.py — Массовое обновление ссылок в markdown файлах.

Использование:
    python update_links.py <старый_путь> <новый_путь> [--dry-run] [--repo <корень>]

Примеры:
    # Предпросмотр изменений
    python update_links.py tools/documentation.md doc/structure.md --dry-run

    # Применить изменения
    python update_links.py tools/documentation.md doc/structure.md

    # Обновить ссылки на папку
    python update_links.py /.claude/.instructions/tools/ /.claude/skills/ --dry-run

Функции:
    - Обновляет markdown ссылки: [text](old_path) → [text](new_path)
    - Обновляет относительные и абсолютные пути
    - Обновляет текст ссылки если он совпадал с путём
    - Поддерживает --dry-run для предпросмотра
    - Выводит статистику изменений
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple


class Change(NamedTuple):
    """Одно изменение в файле."""
    file: str
    line: int
    old_text: str
    new_text: str


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def is_inside_code_block(lines: list[str], line_idx: int) -> bool:
    """Проверить, находится ли строка внутри блока кода."""
    fence_count = 0
    for i in range(line_idx):
        line = lines[i].strip()
        if line.startswith("```") or line.startswith("~~~"):
            fence_count += 1
    return fence_count % 2 == 1


def update_link_text(text: str, old_path: str, new_path: str) -> str:
    """Обновить текст ссылки если он совпадает с путём."""
    # Если текст ссылки — это имя файла или путь, обновляем его тоже
    old_name = Path(old_path.rstrip("/")).name
    new_name = Path(new_path.rstrip("/")).name

    # Если текст совпадает с именем файла
    if text == old_name or text == old_path or text == old_path.lstrip("/"):
        return new_name

    # Если текст содержит путь как часть (например tools/skills.md)
    if old_path.lstrip("/") in text:
        return text.replace(old_path.lstrip("/"), new_path.lstrip("/"))

    return text


def update_links_in_line(
    line: str,
    old_path: str,
    new_path: str
) -> tuple[str, bool]:
    """Обновить ссылки в строке, вернуть (новая_строка, изменено)."""
    # Нормализуем пути
    old_path_norm = old_path.replace("\\", "/")
    new_path_norm = new_path.replace("\\", "/")

    # Варианты старого пути для поиска
    old_variants = [
        old_path_norm,                    # как есть
        old_path_norm.lstrip("/"),        # без начального /
        "/" + old_path_norm.lstrip("/"),  # с начальным /
    ]

    changed = False
    result = line

    # Паттерн для markdown ссылок: [text](path)
    link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

    def replace_link(match):
        nonlocal changed
        text = match.group(1)
        path = match.group(2)

        # Проверяем, содержит ли путь старый путь
        for old_var in old_variants:
            if old_var in path:
                new_link_path = path.replace(old_var, new_path_norm.lstrip("/") if not path.startswith("/") else new_path_norm)
                # Пробуем обновить текст ссылки
                new_text = update_link_text(text, old_path_norm, new_path_norm)
                changed = True
                return f"[{new_text}]({new_link_path})"

        return match.group(0)

    result = link_pattern.sub(replace_link, result)

    # Также ищем упоминания пути без ссылок (но не внутри [...](...)
    # Это для таких случаев как: related: tools/documentation.md
    if not changed:
        for old_var in old_variants:
            if old_var in result:
                # Проверяем что это не часть markdown ссылки
                # Простая эвристика: если нет ] или ( рядом
                idx = result.find(old_var)
                if idx > 0 and result[idx-1] == "(":
                    continue  # Это часть ссылки

                # Проверяем что это не bash команда
                bash_commands = ["mkdir", "rm ", "rm -", "cd ", "cp ", "mv ", "touch "]
                if any(cmd in result.lower() for cmd in bash_commands):
                    continue

                result = result.replace(old_var, new_path_norm.lstrip("/") if not old_var.startswith("/") else new_path_norm)
                changed = True
                break

    return result, changed


def process_file(
    file_path: Path,
    old_path: str,
    new_path: str,
    dry_run: bool
) -> list[Change]:
    """Обработать один файл, вернуть список изменений."""
    changes = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return changes

    lines = content.split("\n")
    new_lines = []
    modified = False

    for line_idx, line in enumerate(lines):
        # Пропустить строки внутри блоков кода
        if is_inside_code_block(lines, line_idx):
            new_lines.append(line)
            continue

        # Пропустить строки-ограничители блоков кода
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            new_lines.append(line)
            continue

        new_line, changed = update_links_in_line(line, old_path, new_path)

        if changed:
            changes.append(Change(
                file=str(file_path),
                line=line_idx + 1,
                old_text=line,
                new_text=new_line
            ))
            modified = True

        new_lines.append(new_line)

    # Записываем изменения если не dry-run
    if modified and not dry_run:
        file_path.write_text("\n".join(new_lines), encoding="utf-8")

    return changes


def find_all_md_files(repo_root: Path) -> list[Path]:
    """Найти все .md файлы в репозитории."""
    md_files = []

    for md_file in repo_root.rglob("*.md"):
        # Пропускаем файлы в .git, node_modules и т.д.
        parts = md_file.parts
        if any(p.startswith(".git") or p == "node_modules" for p in parts):
            continue
        md_files.append(md_file)

    return md_files


def main():
    # Устанавливаем UTF-8 для вывода на Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Массовое обновление ссылок в markdown файлах."
    )
    parser.add_argument(
        "old_path",
        help="Старый путь для замены"
    )
    parser.add_argument(
        "new_path",
        help="Новый путь"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать изменения без применения"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    md_files = find_all_md_files(repo_root)

    all_changes = []
    files_modified = set()

    for md_file in md_files:
        changes = process_file(md_file, args.old_path, args.new_path, args.dry_run)
        if changes:
            all_changes.extend(changes)
            files_modified.add(str(md_file))

    # Вывод результатов
    if args.dry_run:
        print(f"📋 Предпросмотр изменений (--dry-run)")
        print(f"   Замена: {args.old_path} → {args.new_path}")
        print()
    else:
        print(f"✅ Изменения применены")
        print(f"   Замена: {args.old_path} → {args.new_path}")
        print()

    if not all_changes:
        print("Ссылок для замены не найдено.")
        sys.exit(1)

    print(f"Изменено файлов: {len(files_modified)}")
    print(f"Всего замен: {len(all_changes)}")
    print()

    # Группируем по файлам
    current_file = None
    for change in sorted(all_changes, key=lambda c: (c.file, c.line)):
        rel_path = os.path.relpath(change.file, repo_root)

        if change.file != current_file:
            current_file = change.file
            print(f"📄 {rel_path}")

        print(f"   Строка {change.line}:")
        # Показываем краткую версию изменения
        old_short = change.old_text.strip()[:80]
        new_short = change.new_text.strip()[:80]
        if len(change.old_text.strip()) > 80:
            old_short += "..."
        if len(change.new_text.strip()) > 80:
            new_short += "..."
        print(f"   - {old_short}")
        print(f"   + {new_short}")
        print()

    if args.dry_run:
        print("ℹ️  Изменения НЕ применены (--dry-run)")
        print(f"   Для применения запустите без флага --dry-run")

    sys.exit(0)


if __name__ == "__main__":
    main()
