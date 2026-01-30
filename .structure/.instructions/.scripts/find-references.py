#!/usr/bin/env python3
"""
find-references.py — Поиск ссылок на папку или файл в проекте.

Использование:
    python find-references.py <паттерн>

Примеры:
    python find-references.py docs/
    python find-references.py old-api.md
    python find-references.py "shared/utils"

Возвращает:
    0 — найдены ссылки
    1 — ссылки не найдены
"""

import argparse
import re
import sys
from pathlib import Path


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def should_skip(path: Path, repo_root: Path) -> bool:
    """Проверить, нужно ли пропустить файл/папку."""
    rel_path = str(path.relative_to(repo_root))

    skip_patterns = [
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        ".env",
        "dist",
        "build",
        ".pytest_cache",
        ".mypy_cache",
    ]

    for pattern in skip_patterns:
        if pattern in rel_path.split("/") or pattern in rel_path.split("\\"):
            return True

    return False


def is_tree_line(line: str) -> bool:
    """Проверить, является ли строка частью дерева структуры."""
    tree_chars = ["│", "├", "└", "─"]
    return any(char in line for char in tree_chars)


def find_references(repo_root: Path, pattern: str, file_types: list[str]) -> list[dict]:
    """Найти все ссылки на паттерн в файлах проекта."""
    results = []

    # Экранируем спецсимволы regex, но оставляем возможность поиска
    search_pattern = re.escape(pattern)

    # Для путей типа ".claude/scripts/" также ищем последний компонент в деревьях
    # Извлекаем имя папки: ".claude/scripts/" -> "scripts/"
    folder_name = None
    if "/" in pattern or "\\" in pattern:
        # Нормализуем путь и берём последний компонент
        normalized = pattern.replace("\\", "/").rstrip("/")
        if "/" in normalized:
            folder_name = normalized.split("/")[-1] + "/"

    for file_type in file_types:
        for file_path in repo_root.rglob(f"*.{file_type}"):
            if should_skip(file_path, repo_root):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                lines = content.split("\n")

                for line_num, line in enumerate(lines, 1):
                    matched = False

                    # Основной поиск по полному паттерну
                    if re.search(search_pattern, line):
                        matched = True
                    # Дополнительный поиск в строках дерева по имени папки
                    elif folder_name and is_tree_line(line):
                        folder_pattern = re.escape(folder_name)
                        if re.search(folder_pattern, line):
                            matched = True

                    if matched:
                        rel_path = file_path.relative_to(repo_root)
                        results.append({
                            "file": str(rel_path),
                            "line": line_num,
                            "content": line.strip(),
                            "full_path": file_path,
                        })
            except (UnicodeDecodeError, PermissionError):
                continue

    return results


def format_results(results: list[dict], pattern: str, use_color: bool = True) -> str:
    """Форматировать результаты поиска."""
    if not results:
        return f"Ссылки на '{pattern}' не найдены."

    # Группируем по файлам
    by_file = {}
    for r in results:
        if r["file"] not in by_file:
            by_file[r["file"]] = []
        by_file[r["file"]].append(r)

    lines = []
    lines.append(f"Найдено {len(results)} ссылок на '{pattern}' в {len(by_file)} файлах:")
    lines.append("")

    for file_path, refs in sorted(by_file.items()):
        lines.append(f"📄 {file_path}")
        for ref in refs:
            content = ref["content"]
            # Подсветка паттерна
            if use_color:
                content = content.replace(pattern, f"\033[1;33m{pattern}\033[0m")
            lines.append(f"   {ref['line']:4d}: {content}")
        lines.append("")

    return "\n".join(lines)


def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Поиск ссылок на папку или файл в проекте",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python find-references.py docs/
  python find-references.py old-api.md
  python find-references.py "shared/utils"
  python find-references.py config --types md,yaml
"""
    )

    parser.add_argument(
        "pattern",
        help="Паттерн для поиска (папка/, файл.md, путь)"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )
    parser.add_argument(
        "--types",
        default="md",
        help="Типы файлов через запятую (по умолчанию: md)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Отключить подсветку"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    file_types = [t.strip() for t in args.types.split(",")]

    results = find_references(repo_root, args.pattern, file_types)

    if args.json:
        import json
        output = {
            "pattern": args.pattern,
            "total": len(results),
            "results": [
                {"file": r["file"], "line": r["line"], "content": r["content"]}
                for r in results
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(format_results(results, args.pattern, use_color=not args.no_color))

    sys.exit(0 if results else 1)


if __name__ == "__main__":
    main()
