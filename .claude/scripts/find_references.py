#!/usr/bin/env python3
"""
find_references.py — Поиск ссылок на файл/папку в документах репозитория.

Использование:
    python find_references.py <путь> [--repo <корень>] [--format json|text]

Примеры:
    python find_references.py /.claude/scripts/
    python find_references.py skills.md
    python find_references.py /config/settings.json --format json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple


class Reference(NamedTuple):
    """Найденная ссылка."""
    file: str       # Файл, где найдена ссылка
    line: int       # Номер строки
    text: str       # Текст строки
    is_link: bool   # True если [text](path), False если просто path


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


def find_references_in_file(
    file_path: Path,
    search_path: str,
    search_name: str
) -> list[Reference]:
    """Найти ссылки на путь в файле."""
    references = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return references

    lines = content.split("\n")

    # Паттерны для поиска
    # 1. Markdown ссылка: [text](path)
    link_pattern = re.compile(
        r'\[([^\]]*)\]\(([^)]+)\)',
        re.IGNORECASE
    )

    for line_idx, line in enumerate(lines):
        # Пропустить строки внутри блоков кода
        if is_inside_code_block(lines, line_idx):
            continue

        # Пропустить строки, которые являются началом блока кода
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            continue

        line_num = line_idx + 1

        # Поиск markdown ссылок
        for match in link_pattern.finditer(line):
            link_path = match.group(2)
            if search_path in link_path or search_name in link_path:
                references.append(Reference(
                    file=str(file_path),
                    line=line_num,
                    text=line.strip(),
                    is_link=True
                ))
                break  # Одна ссылка на строку достаточно

        # Поиск упоминаний пути без ссылки (не внутри [...](...)
        # Удаляем markdown ссылки из строки для поиска plain text
        line_without_links = link_pattern.sub("", line)

        # Ищем путь или имя файла
        if search_path in line_without_links or search_name in line_without_links:
            # Проверяем, что это не часть bash команды
            bash_commands = ["mkdir", "rm ", "rm -", "cd ", "cp ", "mv ", "touch "]
            is_bash = any(cmd in line.lower() for cmd in bash_commands)

            if not is_bash:
                # Проверяем, не добавили ли мы уже эту строку как ссылку
                already_added = any(
                    r.file == str(file_path) and r.line == line_num
                    for r in references
                )
                if not already_added:
                    references.append(Reference(
                        file=str(file_path),
                        line=line_num,
                        text=line.strip(),
                        is_link=False
                    ))

    return references


def find_all_references(
    search_path: str,
    repo_root: Path
) -> list[Reference]:
    """Найти все ссылки на путь в репозитории."""
    all_references = []

    # Нормализуем путь для поиска
    search_path = search_path.replace("\\", "/")

    # Извлекаем имя файла/папки для поиска по имени
    search_name = Path(search_path).name
    if search_path.endswith("/"):
        search_name = search_name + "/"

    # Находим все .md файлы
    for md_file in repo_root.rglob("*.md"):
        # Пропускаем файлы в .git, node_modules и т.д.
        parts = md_file.parts
        if any(p.startswith(".git") or p == "node_modules" for p in parts):
            continue

        refs = find_references_in_file(md_file, search_path, search_name)
        all_references.extend(refs)

    return all_references


def format_output(references: list[Reference], fmt: str, repo_root: Path) -> str:
    """Форматировать вывод."""
    if fmt == "json":
        data = [
            {
                "file": os.path.relpath(r.file, repo_root),
                "line": r.line,
                "text": r.text,
                "is_link": r.is_link
            }
            for r in references
        ]
        return json.dumps(data, ensure_ascii=False, indent=2)

    # Текстовый формат
    if not references:
        return "Ссылки не найдены."

    lines = [f"Найдено ссылок: {len(references)}", ""]

    for ref in references:
        rel_path = os.path.relpath(ref.file, repo_root)
        link_marker = "[ссылка]" if ref.is_link else "[текст]"
        lines.append(f"{rel_path}:{ref.line} {link_marker}")
        lines.append(f"  {ref.text[:100]}{'...' if len(ref.text) > 100 else ''}")
        lines.append("")

    return "\n".join(lines)


def main():
    # Устанавливаем UTF-8 для вывода на Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Поиск ссылок на файл/папку в документах репозитория."
    )
    parser.add_argument(
        "path",
        help="Путь к файлу или папке для поиска"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Формат вывода (по умолчанию: text)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    references = find_all_references(args.path, repo_root)

    # Сортируем по файлу и строке
    references.sort(key=lambda r: (r.file, r.line))

    output = format_output(references, args.format, repo_root)
    print(output)

    # Возвращаем код 0 если найдены ссылки, 1 если нет
    sys.exit(0 if references else 1)


if __name__ == "__main__":
    main()
