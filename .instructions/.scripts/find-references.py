#!/usr/bin/env python3
"""
find-references.py — Поиск всех ссылок на файл в проекте.

Находит все markdown-файлы, которые ссылаются на указанный файл.
Используется при деактивации, миграции и удалении.

Использование:
    python find-references.py <path> [--json] [--repo <dir>]
    python find-references.py --pattern <pattern> [--json]

Примеры:
    python find-references.py .instructions/old-instruction.md
    python find-references.py --pattern "standard-api.md"
    python find-references.py .scripts/old-script.py --json

Возвращает:
    0 — ссылки найдены
    1 — ссылки не найдены
    2 — ошибка аргументов
"""

import argparse
import json
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

def find_references(target: str, repo_root: Path) -> list[dict]:
    """
    Найти все ссылки на файл в markdown-файлах.

    Args:
        target: Имя файла или путь для поиска
        repo_root: Корень репозитория

    Returns:
        Список найденных ссылок с информацией о файле и строке
    """
    references = []

    # Паттерн для markdown-ссылок: [text](path) или [text]: path
    link_pattern = re.compile(
        r'\[([^\]]*)\]\(([^)]*' + re.escape(target) + r'[^)]*)\)|'
        r'\[([^\]]+)\]:\s*(\S*' + re.escape(target) + r'\S*)'
    )

    for md_file in repo_root.rglob("*.md"):
        # Пропустить node_modules, .git и т.д.
        if any(part.startswith('.') and part not in ('.instructions', '.structure', '.claude')
               for part in md_file.parts):
            continue
        if 'node_modules' in md_file.parts:
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception:
            continue

        for i, line in enumerate(content.split('\n'), 1):
            matches = link_pattern.findall(line)
            for match in matches:
                # match — кортеж из 4 элементов (text1, href1, text2, href2)
                text = match[0] or match[2]
                href = match[1] or match[3]

                if target in href:
                    rel_path = md_file.relative_to(repo_root)
                    references.append({
                        "file": str(rel_path).replace("\\", "/"),
                        "line": i,
                        "text": text,
                        "href": href,
                        "content": line.strip()
                    })

    return references


def format_text_output(references: list[dict], target: str) -> str:
    """Форматировать вывод для терминала."""
    if not references:
        return f"Ссылки на '{target}' не найдены"

    lines = [f"Найдено ссылок: {len(references)}", ""]

    current_file = None
    for ref in references:
        if ref["file"] != current_file:
            current_file = ref["file"]
            lines.append(f"📄 {current_file}")

        lines.append(f"   {ref['line']}: {ref['content'][:80]}{'...' if len(ref['content']) > 80 else ''}")

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
        description="Поиск всех ссылок на файл в проекте"
    )
    parser.add_argument("path", nargs="?", help="Путь к файлу для поиска")
    parser.add_argument("--pattern", help="Паттерн для поиска (имя файла)")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    if not args.path and not args.pattern:
        parser.print_help()
        sys.exit(2)

    repo_root = find_repo_root(Path(args.repo))

    # Определить цель поиска
    if args.pattern:
        target = args.pattern
    else:
        # Использовать имя файла из пути
        target = Path(args.path).name

    references = find_references(target, repo_root)

    # Сортировка по файлу и строке
    references.sort(key=lambda x: (x["file"], x["line"]))

    if args.json:
        print(json.dumps({
            "target": target,
            "count": len(references),
            "references": references
        }, ensure_ascii=False, indent=2))
    else:
        print(format_text_output(references, target))

    sys.exit(0 if references else 1)


if __name__ == "__main__":
    main()
