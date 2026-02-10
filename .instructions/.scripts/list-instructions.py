#!/usr/bin/env python3
"""
list-instructions.py — Список всех инструкций проекта с описаниями.

Парсит все .md файлы в папках .instructions/ (включая вложенные),
извлекает frontmatter и возвращает структурированный список.

Использование:
    python list-instructions.py [--search <текст>] [--json] [--repo <dir>]

Примеры:
    python list-instructions.py
    python list-instructions.py --search "валидация"
    python list-instructions.py --json
    python list-instructions.py --repo /path/to/project

Возвращает:
    0 — успех
    1 — инструкции не найдены
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


def parse_frontmatter(content: str) -> dict:
    """Извлечь frontmatter из markdown."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    result = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    return result


def get_first_heading(content: str) -> str:
    """Извлечь первый заголовок H1."""
    match = re.search(r'^# (.+)$', content, re.MULTILINE)
    return match.group(1) if match else ""


def detect_instruction_type(filename: str) -> str:
    """Определить тип инструкции по имени файла."""
    if filename.startswith("standard-"):
        return "standard"
    elif filename.startswith("create-"):
        return "create"
    elif filename.startswith("modify-"):
        return "modify"
    elif filename.startswith("validation-"):
        return "validation"
    return "unknown"


# =============================================================================
# Основные функции
# =============================================================================

def find_all_instructions(repo_root: Path) -> list[dict]:
    """Найти все инструкции в репозитории."""
    instructions = []

    for instructions_dir in repo_root.rglob(".instructions"):
        if not instructions_dir.is_dir():
            continue

        # Пропустить .scripts папки
        if ".scripts" in str(instructions_dir):
            continue

        for md_file in instructions_dir.glob("*.md"):
            # Пропустить README
            if md_file.name == "README.md":
                continue

            try:
                content = md_file.read_text(encoding='utf-8')
            except Exception:
                continue

            fm = parse_frontmatter(content)
            heading = get_first_heading(content)

            # Относительный путь от корня
            rel_path = md_file.relative_to(repo_root)

            # Определить область (папка родительская для .instructions)
            parts = rel_path.parts
            instructions_idx = parts.index(".instructions")
            if instructions_idx > 0:
                area = "/".join(parts[:instructions_idx])
            else:
                area = "root"

            instructions.append({
                "path": str(rel_path).replace("\\", "/"),
                "name": md_file.stem,
                "type": detect_instruction_type(md_file.stem),
                "area": area,
                "title": heading,
                "description": fm.get("description", ""),
                "standard": fm.get("standard", ""),
            })

    return sorted(instructions, key=lambda x: (x["area"], x["type"], x["name"]))


def search_instructions(instructions: list[dict], query: str) -> list[dict]:
    """Фильтровать инструкции по поисковому запросу."""
    query_lower = query.lower()
    return [
        i for i in instructions
        if query_lower in i['name'].lower()
        or query_lower in i['description'].lower()
        or query_lower in i['title'].lower()
    ]


def format_text_output(instructions: list[dict]) -> str:
    """Форматировать вывод для LLM."""
    lines = [f"Найдено инструкций: {len(instructions)}", ""]

    current_area = None
    for inst in instructions:
        # Разделитель по области
        if inst["area"] != current_area:
            current_area = inst["area"]
            lines.append(f"## Область: {current_area}")
            lines.append("")

        # Информация об инструкции
        type_emoji = {
            "standard": "📘",
            "create": "➕",
            "modify": "✏️",
            "validation": "✅",
            "unknown": "📄"
        }.get(inst["type"], "📄")

        lines.append(f"{type_emoji} **{inst['name']}** ({inst['type']})")
        lines.append(f"   Путь: {inst['path']}")
        if inst["title"]:
            lines.append(f"   Заголовок: {inst['title']}")
        if inst["description"]:
            lines.append(f"   Описание: {inst['description']}")
        lines.append("")

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
        description="Список всех инструкций проекта"
    )
    parser.add_argument("--search", help="Поиск по имени/описанию/заголовку")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    instructions = find_all_instructions(repo_root)

    if args.search:
        instructions = search_instructions(instructions, args.search)

    if not instructions:
        print("Инструкции не найдены", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(instructions, ensure_ascii=False, indent=2))
    else:
        print(format_text_output(instructions))

    sys.exit(0)


if __name__ == "__main__":
    main()
