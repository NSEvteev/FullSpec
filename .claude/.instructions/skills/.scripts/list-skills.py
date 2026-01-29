#!/usr/bin/env python3
"""
list-skills.py — Список скиллов с описаниями.

Использование:
    python list-skills.py [--search <текст>] [--json]

Примеры:
    python list-skills.py
    python list-skills.py --search "валидация"
    python list-skills.py --json

Возвращает:
    0 — скиллы найдены
    1 — скиллы не найдены
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


# =============================================================================
# Константы
# =============================================================================

SKILLS_DIR = Path(__file__).parent.parent.parent.parent / "skills"


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
    if not content.startswith('---'):
        return {}

    end_idx = content.find('---', 3)
    if end_idx == -1:
        return {}

    yaml_content = content[3:end_idx].strip()
    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return {}


# =============================================================================
# Основные функции
# =============================================================================

def get_all_skills(skills_dir: Path) -> list[dict]:
    """
    Получить список всех скиллов.

    Returns:
        list[dict] с полями: name, description, path, triggers
    """
    skills = []

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        # Пропускаем деактивированные
        if skill_dir.name.endswith('_old'):
            continue

        skill_file = skill_dir / 'SKILL.md'
        if not skill_file.exists():
            continue

        try:
            content = skill_file.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)

            skill_info = {
                "name": frontmatter.get('name', skill_dir.name),
                "description": frontmatter.get('description', ''),
                "path": f".claude/skills/{skill_dir.name}/SKILL.md",
                "triggers": [],
            }

            # Извлекаем триггеры
            triggers = frontmatter.get('triggers', {})
            if triggers.get('commands'):
                skill_info["triggers"].extend(triggers['commands'])

            skills.append(skill_info)
        except Exception:
            continue

    return skills


def search_skills(skills: list[dict], query: str) -> list[dict]:
    """Фильтровать скиллы по поисковому запросу."""
    query_lower = query.lower()
    return [
        s for s in skills
        if query_lower in s['name'].lower()
        or query_lower in s['description'].lower()
    ]


# =============================================================================
# Форматирование
# =============================================================================

def format_output(skills: list[dict], query: str | None, as_json: bool) -> str:
    """Форматировать результат."""
    if as_json:
        return json.dumps({
            "query": query,
            "count": len(skills),
            "skills": skills,
        }, ensure_ascii=False, indent=2)

    if not skills:
        if query:
            return f"Скиллы по запросу '{query}' не найдены"
        return "Скиллы не найдены"

    lines = []
    if query:
        lines.append(f"Найдено {len(skills)} скиллов по запросу '{query}':")
    else:
        lines.append(f"Всего скиллов: {len(skills)}")
    lines.append("")

    for skill in skills:
        triggers = ", ".join(skill["triggers"]) if skill["triggers"] else "—"
        lines.append(f"• {skill['name']}")
        lines.append(f"  {skill['description']}")
        lines.append(f"  Триггеры: {triggers}")
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
        description="Список скиллов с описаниями"
    )
    parser.add_argument("--search", help="Поиск по имени/описанию")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    skills = get_all_skills(SKILLS_DIR)

    if args.search:
        skills = search_skills(skills, args.search)

    print(format_output(skills, args.search, args.json))

    sys.exit(0 if skills else 1)


if __name__ == "__main__":
    main()
