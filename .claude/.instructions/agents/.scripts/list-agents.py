#!/usr/bin/env python3
"""
list-agents.py — Вывод списка всех агентов с описаниями.

Сканирует папку /.claude/agents/ и выводит список агентов
с их описаниями и типами для анализа LLM.

Использование:
    python list-agents.py [--search <pattern>] [--json] [--repo <dir>]

Примеры:
    python list-agents.py
    python list-agents.py --search "todo"
    python list-agents.py --json
    python list-agents.py --search "explore" --json

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


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
    """Парсить YAML frontmatter из markdown."""
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}

    frontmatter_text = match.group(1)

    if yaml:
        try:
            return yaml.safe_load(frontmatter_text) or {}
        except Exception:
            return {}

    # Простой парсер без зависимостей
    result = {}
    for line in frontmatter_text.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if ':' in stripped and not stripped.startswith('-'):
            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()
            if value and not value.startswith('|'):
                result[key] = value.strip('"\'')

    return result


# =============================================================================
# Основные функции
# =============================================================================

def list_agents(repo_root: Path, search: str | None = None) -> list[dict]:
    """Получить список всех агентов."""
    agents_dir = repo_root / ".claude" / "agents"

    if not agents_dir.exists():
        return []

    agents = []

    for agent_dir in sorted(agents_dir.iterdir()):
        # Пропустить файлы и DELETE_ папки
        if not agent_dir.is_dir():
            continue
        if agent_dir.name.startswith("DELETE_"):
            continue
        if agent_dir.name.startswith("."):
            continue

        # Проверить AGENT.md
        agent_file = agent_dir / "AGENT.md"
        if not agent_file.exists():
            continue

        try:
            content = agent_file.read_text(encoding='utf-8')
            data = parse_frontmatter(content)

            if not data:
                continue

            agent_info = {
                "name": data.get("name", agent_dir.name),
                "description": data.get("description", ""),
                "type": data.get("type", "unknown"),
                "model": data.get("model", "inherit"),
                "path": str(agent_dir.relative_to(repo_root)),
            }

            # Фильтр по search
            if search:
                search_lower = search.lower()
                searchable = f"{agent_info['name']} {agent_info['description']} {agent_info['type']}".lower()
                if search_lower not in searchable:
                    continue

            agents.append(agent_info)

        except Exception:
            continue

    return agents


def format_output(agents: list[dict], search: str | None, as_json: bool) -> str:
    """Форматировать результат."""
    if as_json:
        return json.dumps({
            "query": search,
            "count": len(agents),
            "agents": agents,
        }, ensure_ascii=False, indent=2)

    if not agents:
        if search:
            return f"Агенты по запросу '{search}' не найдены"
        return "Агентов не найдено."

    lines = []
    if search:
        lines.append(f"Найдено {len(agents)} агентов по запросу '{search}':")
    else:
        lines.append(f"Найдено агентов: {len(agents)}")
    lines.append("")

    # Группировка по типам
    by_type: dict[str, list] = {}
    for agent in agents:
        agent_type = agent["type"]
        if agent_type not in by_type:
            by_type[agent_type] = []
        by_type[agent_type].append(agent)

    for agent_type in sorted(by_type.keys()):
        lines.append(f"## Тип: {agent_type}")
        lines.append("")
        for agent in by_type[agent_type]:
            lines.append(f"• {agent['name']}")
            lines.append(f"  {agent['description']}")
            lines.append(f"  Модель: {agent['model']}")
            lines.append(f"  Путь: {agent['path']}")
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
        description="Вывод списка всех агентов"
    )
    parser.add_argument(
        "--search",
        help="Фильтр по имени, описанию или типу"
    )
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    try:
        agents = list_agents(repo_root, args.search)
        print(format_output(agents, args.search, args.json))
        sys.exit(0 if agents else 1)

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
