#!/usr/bin/env python3
"""
find-skill-references.py — Поиск всех ссылок на скилл в проекте.

Использование:
    python find-skill-references.py <skill-name>
    python find-skill-references.py <skill-name> --json

Примеры:
    python find-skill-references.py structure-create
    python find-skill-references.py skill-modify --json

Возвращает:
    0 — ссылки найдены
    1 — ссылки не найдены или ошибка
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

SEARCH_PATTERNS = [
    # Markdown-ссылка на SKILL.md
    r'\[.*?\]\(.*?skills/{skill}.*?\)',
    # Упоминание команды /skill-name
    r'/{skill}(?:\s|$|`|\)|\])',
    # Ссылка в таблице
    r'\|\s*\[?/?{skill}\]?.*?\|',
    # Просто имя скилла
    r'skills/{skill}',
]

SEARCH_LOCATIONS = [
    ("Скиллы", ".claude/skills/*/SKILL.md"),
    ("Инструкции", "**/.instructions/**/*.md"),
    ("README", "**/README.md"),
    ("CLAUDE.md", "CLAUDE.md"),
]


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
# Поиск ссылок
# =============================================================================

def find_references(repo_root: Path, skill_name: str) -> dict:
    """
    Найти все ссылки на скилл.

    Returns:
        dict с полями:
            skill: имя скилла
            total: общее количество ссылок
            locations: dict[категория -> list[{file, line, text}]]
    """
    result = {
        "skill": skill_name,
        "total": 0,
        "locations": {},
    }

    # Компилируем паттерны
    patterns = []
    for pattern_template in SEARCH_PATTERNS:
        pattern = pattern_template.format(skill=re.escape(skill_name))
        patterns.append(re.compile(pattern, re.IGNORECASE))

    # Ищем по каждой локации
    for category, glob_pattern in SEARCH_LOCATIONS:
        matches = []

        for file_path in repo_root.glob(glob_pattern):
            if not file_path.is_file():
                continue

            # Пропускаем сам скилл
            if f"skills/{skill_name}/" in str(file_path).replace("\\", "/"):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue

            for i, line in enumerate(content.split("\n"), 1):
                for pattern in patterns:
                    if pattern.search(line):
                        rel_path = file_path.relative_to(repo_root)
                        matches.append({
                            "file": str(rel_path).replace("\\", "/"),
                            "line": i,
                            "text": line.strip()[:100],
                        })
                        break  # Одна строка — один матч

        if matches:
            result["locations"][category] = matches
            result["total"] += len(matches)

    return result


# =============================================================================
# Форматирование
# =============================================================================

def format_output(result: dict, as_json: bool) -> str:
    """Форматировать результат."""
    if as_json:
        return json.dumps(result, ensure_ascii=False, indent=2)

    if result["total"] == 0:
        return f"Ссылок на скилл '{result['skill']}' не найдено"

    lines = [f"Найдено {result['total']} ссылок на скилл '{result['skill']}':", ""]

    for category, matches in result["locations"].items():
        lines.append(f"📁 {category} ({len(matches)}):")
        for match in matches:
            lines.append(f"   {match['file']}:{match['line']}")
            lines.append(f"      {match['text']}")
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
        description="Поиск всех ссылок на скилл в проекте"
    )
    parser.add_argument("skill", help="Имя скилла для поиска")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    result = find_references(repo_root, args.skill)

    print(format_output(result, args.json))

    sys.exit(0 if result["total"] > 0 else 1)


if __name__ == "__main__":
    main()
