#!/usr/bin/env python3
"""
instruction-stats.py — Статистика инструкций.

Использование:
    python instruction-stats.py [--json] [--repo <корень>]

Примеры:
    python instruction-stats.py
    python instruction-stats.py --json

Вывод:
    - Общее количество инструкций
    - Количество по папкам
    - Количество созданных/заполненных
    - Процент завершения

Возвращает:
    0 — всегда (информационный скрипт)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from collections import defaultdict


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def scan_instructions_dir(instructions_dir: Path) -> dict:
    """
    Сканировать папку инструкций и собрать статистику.

    Возвращает dict с файлами и их метаданными.
    """
    files = {}

    if not instructions_dir.exists():
        return files

    for md_file in instructions_dir.rglob("*.md"):
        rel_path = md_file.relative_to(instructions_dir)
        parts = rel_path.parts

        if len(parts) == 1:
            # Корневой файл (README.md)
            folder = ""
        else:
            folder = parts[0]

        # Читаем frontmatter для типа
        type_ = "unknown"
        try:
            content = md_file.read_text(encoding="utf-8")
            if content.startswith("---"):
                end_idx = content.find("---", 3)
                if end_idx > 0:
                    frontmatter = content[3:end_idx]
                    type_match = re.search(r'type:\s*(\w+)', frontmatter)
                    if type_match:
                        type_ = type_match.group(1)
        except (OSError, UnicodeDecodeError):
            pass

        files[str(rel_path)] = {
            "path": str(rel_path),
            "folder": folder,
            "name": md_file.name,
            "type": type_,
            "size": md_file.stat().st_size,
            "exists": True,
        }

    return files


def parse_readme_stats(readme_path: Path) -> dict:
    """
    Парсить README.md и извлечь статистику из таблиц.
    """
    stats = {
        "total": 0,
        "created": 0,
        "filled": 0,
        "by_folder": defaultdict(lambda: {"total": 0, "created": 0, "filled": 0}),
        "by_type": defaultdict(int),
    }

    if not readme_path.exists():
        return stats

    content = readme_path.read_text(encoding="utf-8")

    # Ищем строки таблиц с инструкциями
    # | [file.md](path) | description | type | ✅ | ✅ |
    row_pattern = re.compile(
        r'\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]*)\|\s*(\w+)\s*\|\s*([✅⬜])\s*\|\s*([✅⬜])\s*\|'
    )

    current_folder = ""

    for line in content.split("\n"):
        # Определяем текущую папку по заголовку секции
        folder_match = re.match(r'^##\s+/(\w+)/', line)
        if folder_match:
            current_folder = folder_match.group(1)
            continue

        # Парсим строку таблицы
        match = row_pattern.search(line)
        if match:
            file_name = match.group(1)
            path = match.group(2)
            description = match.group(3).strip()
            type_ = match.group(4)
            created = match.group(5) == "✅"
            filled = match.group(6) == "✅"

            # Определяем папку из пути если не определена
            folder = current_folder
            if not folder and "/" in path:
                folder = path.split("/")[1] if path.startswith("./") else path.split("/")[0]

            stats["total"] += 1
            if created:
                stats["created"] += 1
            if filled:
                stats["filled"] += 1

            stats["by_folder"][folder]["total"] += 1
            if created:
                stats["by_folder"][folder]["created"] += 1
            if filled:
                stats["by_folder"][folder]["filled"] += 1

            stats["by_type"][type_] += 1

    return stats


def format_progress_bar(current: int, total: int, width: int = 20) -> str:
    """Форматировать прогресс-бар."""
    if total == 0:
        return "[" + " " * width + "]"

    filled = int(width * current / total)
    empty = width - filled
    percent = 100 * current / total

    return f"[{'█' * filled}{'░' * empty}] {percent:.0f}%"


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Статистика инструкций."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в JSON формате"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    instructions_dir = repo_root / ".claude" / "instructions"
    readme_path = instructions_dir / "README.md"

    # Собираем статистику из двух источников
    files = scan_instructions_dir(instructions_dir)
    readme_stats = parse_readme_stats(readme_path)

    # Объединяем статистику
    stats = {
        "total_files": len(files),
        "total_in_readme": readme_stats["total"],
        "created": readme_stats["created"],
        "filled": readme_stats["filled"],
        "by_folder": dict(readme_stats["by_folder"]),
        "by_type": dict(readme_stats["by_type"]),
        "completion_percent": (
            100 * readme_stats["filled"] / readme_stats["total"]
            if readme_stats["total"] > 0 else 0
        ),
    }

    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        sys.exit(0)

    # Человекочитаемый вывод
    print("📊 Статистика инструкций")
    print()
    print(f"Всего инструкций: {stats['total_in_readme']}")
    print(f"Создано:          {stats['created']}")
    print(f"Заполнено:        {stats['filled']}")
    print()
    print(f"Прогресс: {format_progress_bar(stats['filled'], stats['total_in_readme'])}")
    print()

    if stats["by_folder"]:
        print("По папкам:")
        for folder, folder_stats in sorted(stats["by_folder"].items()):
            if folder:
                bar = format_progress_bar(folder_stats["filled"], folder_stats["total"], 10)
                print(f"  /{folder}/: {folder_stats['filled']}/{folder_stats['total']} {bar}")
        print()

    if stats["by_type"]:
        print("По типам:")
        for type_, count in sorted(stats["by_type"].items()):
            print(f"  {type_}: {count}")

    sys.exit(0)


if __name__ == "__main__":
    main()
