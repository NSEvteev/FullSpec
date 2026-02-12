#!/usr/bin/env python3
"""
search-docs.py — Единый поиск по всей документации проекта.

Ищет по инструкциям, скиллам, агентам, правилам, README, скриптам и сервисам.
Собственная реализация — без subprocess к отдельным list-скриптам.

Использование:
    python search-docs.py [--type <type>] [--search <query>] [--json] [--repo <dir>]

Примеры:
    python search-docs.py --search "валидация"
    python search-docs.py --type skill --search "создание"
    python search-docs.py --type service --search "auth"
    python search-docs.py --type readme --json
    python search-docs.py --type all --json

Возвращает:
    0 — найдены результаты
    1 — результаты не найдены
"""

import argparse
import json
import re
import sys
from pathlib import Path


VALID_TYPES = ["instruction", "skill", "agent", "rule", "readme", "script", "service", "all"]


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
        if ':' in line and not line.startswith(' ') and not line.startswith('-'):
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    return result


def get_first_heading(content: str) -> str:
    """Извлечь первый заголовок H1."""
    match = re.search(r'^# (.+)$', content, re.MULTILINE)
    return match.group(1) if match else ""


def extract_docstring(content: str) -> str:
    """Извлечь docstring из Python-файла."""
    pattern = r'^(?:#!.*\n)?(?:#.*\n)*\s*"""(.*?)"""'
    match = re.match(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()

    pattern = r"^(?:#!.*\n)?(?:#.*\n)*\s*'''(.*?)'''"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()

    return ""


# =============================================================================
# Коллекторы
# =============================================================================

def collect_instructions(repo_root: Path) -> list[dict]:
    """Собрать все инструкции из .instructions/ папок."""
    items = []

    for instructions_dir in repo_root.rglob(".instructions"):
        if not instructions_dir.is_dir():
            continue
        if ".scripts" in str(instructions_dir):
            continue

        for md_file in instructions_dir.glob("*.md"):
            if md_file.name == "README.md":
                continue

            try:
                content = md_file.read_text(encoding='utf-8')
            except Exception:
                continue

            fm = parse_frontmatter(content)
            rel_path = md_file.relative_to(repo_root)

            parts = rel_path.parts
            instructions_idx = parts.index(".instructions")
            area = "/".join(parts[:instructions_idx]) if instructions_idx > 0 else "root"

            items.append({
                "type": "instruction",
                "name": md_file.stem,
                "path": str(rel_path).replace("\\", "/"),
                "description": fm.get("description", ""),
                "area": area,
            })

    return sorted(items, key=lambda x: (x["area"], x["name"]))


def collect_skills(repo_root: Path) -> list[dict]:
    """Собрать все скиллы из .claude/skills/."""
    items = []
    skills_dir = repo_root / ".claude" / "skills"

    if not skills_dir.exists():
        return items

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.endswith('_old'):
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        try:
            content = skill_file.read_text(encoding='utf-8')
            fm = parse_frontmatter(content)

            items.append({
                "type": "skill",
                "name": fm.get("name", skill_dir.name),
                "path": f".claude/skills/{skill_dir.name}/SKILL.md",
                "description": fm.get("description", ""),
                "area": ".claude",
            })
        except Exception:
            continue

    return items


def collect_agents(repo_root: Path) -> list[dict]:
    """Собрать все агенты из .claude/agents/."""
    items = []
    agents_dir = repo_root / ".claude" / "agents"

    if not agents_dir.exists():
        return items

    for agent_dir in sorted(agents_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        if agent_dir.name.startswith("DELETE_") or agent_dir.name.startswith("."):
            continue

        agent_file = agent_dir / "AGENT.md"
        if not agent_file.exists():
            continue

        try:
            content = agent_file.read_text(encoding='utf-8')
            fm = parse_frontmatter(content)

            if not fm:
                continue

            items.append({
                "type": "agent",
                "name": fm.get("name", agent_dir.name),
                "path": f".claude/agents/{agent_dir.name}/AGENT.md",
                "description": fm.get("description", ""),
                "area": ".claude",
            })
        except Exception:
            continue

    return items


def collect_rules(repo_root: Path) -> list[dict]:
    """Собрать все rules из .claude/rules/."""
    items = []
    rules_dir = repo_root / ".claude" / "rules"

    if not rules_dir.exists():
        return items

    for rule_file in sorted(rules_dir.glob("*.md")):
        try:
            content = rule_file.read_text(encoding='utf-8')
            fm = parse_frontmatter(content)

            items.append({
                "type": "rule",
                "name": rule_file.stem,
                "path": f".claude/rules/{rule_file.name}",
                "description": fm.get("description", ""),
                "area": ".claude",
            })
        except Exception:
            continue

    return items


def collect_readmes(repo_root: Path) -> list[dict]:
    """Собрать все README.md с frontmatter."""
    items = []

    for readme_file in repo_root.rglob("README.md"):
        try:
            content = readme_file.read_text(encoding='utf-8')
        except Exception:
            continue

        fm = parse_frontmatter(content)
        if not fm:
            continue

        rel_path = readme_file.relative_to(repo_root)
        parent = rel_path.parent

        items.append({
            "type": "readme",
            "name": str(parent).replace("\\", "/") if str(parent) != "." else "root",
            "path": str(rel_path).replace("\\", "/"),
            "description": fm.get("description", ""),
            "area": str(parent).replace("\\", "/") if str(parent) != "." else "root",
        })

    return sorted(items, key=lambda x: x["path"])


def collect_scripts(repo_root: Path) -> list[dict]:
    """Собрать все скрипты из .instructions/.scripts/ папок."""
    items = []

    for scripts_dir in repo_root.rglob('.instructions/.scripts'):
        if not scripts_dir.is_dir():
            continue

        for py_file in sorted(scripts_dir.glob('*.py')):
            try:
                content = py_file.read_text(encoding='utf-8')
            except Exception:
                continue

            docstring = extract_docstring(content)
            if not docstring:
                continue

            # Первая строка docstring — описание
            description = docstring.split('\n')[0].strip()

            rel_path = py_file.relative_to(repo_root)
            parts = rel_path.parts
            instructions_idx = parts.index(".instructions")
            area = "/".join(parts[:instructions_idx]) if instructions_idx > 0 else "root"

            items.append({
                "type": "script",
                "name": py_file.stem,
                "path": str(rel_path).replace("\\", "/"),
                "description": description,
                "area": area,
            })

    return items


def collect_services(repo_root: Path) -> list[dict]:
    """Собрать все сервисные документы из specs/architecture/services/."""
    items = []
    services_dir = repo_root / "specs" / "architecture" / "services"

    if not services_dir.exists():
        return items

    for md_file in sorted(services_dir.glob("*.md")):
        if md_file.name == "README.md":
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        fm = parse_frontmatter(content)
        if not fm:
            continue

        service_name = fm.get("service", md_file.stem)
        created_by = fm.get("created-by", "")
        status = "full" if created_by else "stub"

        items.append({
            "type": "service",
            "name": service_name,
            "path": str(md_file.relative_to(repo_root)).replace("\\", "/"),
            "description": fm.get("description", ""),
            "area": "specs/architecture/services",
            "status": status,
        })

    return items


# =============================================================================
# Поиск и вывод
# =============================================================================

def search_items(items: list[dict], query: str) -> list[dict]:
    """Фильтровать элементы по поисковому запросу (case-insensitive substring)."""
    query_lower = query.lower()
    return [
        item for item in items
        if query_lower in item['name'].lower()
        or query_lower in item.get('description', '').lower()
        or query_lower in item.get('area', '').lower()
    ]


def format_text_output(items: list[dict], query: str | None, doc_type: str) -> str:
    """Форматировать результат в текст."""
    if not items:
        if query:
            return f"По запросу '{query}' (тип: {doc_type}) ничего не найдено"
        return f"Документы типа '{doc_type}' не найдены"

    lines = []
    if query:
        lines.append(f"Найдено {len(items)} по запросу '{query}' (тип: {doc_type}):")
    else:
        lines.append(f"Найдено: {len(items)} (тип: {doc_type})")
    lines.append("")

    current_type = None
    for item in items:
        if item["type"] != current_type:
            current_type = item["type"]
            lines.append(f"## {current_type}")
            lines.append("")

        lines.append(f"  {item['name']}")
        lines.append(f"    Путь: {item['path']}")
        if item.get("description"):
            lines.append(f"    Описание: {item['description']}")
        lines.append("")

    return "\n".join(lines)


def format_json_output(items: list[dict], query: str | None, doc_type: str) -> str:
    """Форматировать результат в JSON."""
    return json.dumps({
        "query": query,
        "type": doc_type,
        "count": len(items),
        "items": items,
    }, ensure_ascii=False, indent=2)


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Единый поиск по документации проекта"
    )
    parser.add_argument(
        "--type",
        default="all",
        choices=VALID_TYPES,
        help="Тип документа: instruction, skill, agent, rule, readme, script, service, all"
    )
    parser.add_argument("--search", help="Поисковый запрос (case-insensitive substring)")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Собрать элементы по типу
    collectors = {
        "instruction": collect_instructions,
        "skill": collect_skills,
        "agent": collect_agents,
        "rule": collect_rules,
        "readme": collect_readmes,
        "script": collect_scripts,
        "service": collect_services,
    }

    items = []
    if args.type == "all":
        for collector in collectors.values():
            items.extend(collector(repo_root))
    else:
        items = collectors[args.type](repo_root)

    # Поиск
    if args.search:
        items = search_items(items, args.search)

    # Вывод
    if args.json:
        print(format_json_output(items, args.search, args.type))
    else:
        print(format_text_output(items, args.search, args.type))

    sys.exit(0 if items else 1)


if __name__ == "__main__":
    main()
