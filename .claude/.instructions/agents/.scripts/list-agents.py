#!/usr/bin/env python3
"""
list-agents.py — Вывод списка всех агентов с описаниями.

Сканирует папку /.claude/agents/ и выводит список агентов
с их описаниями и типами для анализа LLM.

Использование:
    python list-agents.py [--search <pattern>]

Примеры:
    python list-agents.py
    python list-agents.py --search "todo"
    python list-agents.py --search "explore"

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


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


def parse_yaml_simple(content: str) -> dict:
    """Простой парсер YAML без зависимостей."""
    result = {}
    current_key = None
    in_multiline = False

    for line in content.split('\n'):
        stripped = line.strip()

        # Пропуск пустых строк и комментариев
        if not stripped or stripped.startswith('#'):
            continue

        # Многострочное значение
        if in_multiline:
            if not line.startswith(' ') and not line.startswith('\t'):
                in_multiline = False
            else:
                continue

        # Парсинг ключ: значение
        if ':' in stripped and not stripped.startswith('-'):
            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()

            if value == '|' or value == '>':
                in_multiline = True
                current_key = key
            elif value:
                result[key] = value.strip('"\'')
            else:
                current_key = key

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

    for file_path in sorted(agents_dir.glob("*.yaml")):
        # Пропустить DELETE_ файлы
        if file_path.name.startswith("DELETE_"):
            continue

        try:
            content = file_path.read_text(encoding='utf-8')

            # Парсинг YAML
            if yaml:
                data = yaml.safe_load(content)
            else:
                data = parse_yaml_simple(content)

            if not data:
                continue

            agent_info = {
                "name": data.get("name", file_path.stem),
                "description": data.get("description", ""),
                "type": data.get("type", "unknown"),
                "path": str(file_path.relative_to(repo_root)),
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


def print_agents(agents: list[dict]) -> None:
    """Вывести список агентов."""
    if not agents:
        print("Агентов не найдено.")
        return

    print(f"Найдено агентов: {len(agents)}\n")

    # Группировка по типам
    by_type: dict[str, list] = {}
    for agent in agents:
        agent_type = agent["type"]
        if agent_type not in by_type:
            by_type[agent_type] = []
        by_type[agent_type].append(agent)

    # Вывод по типам
    for agent_type in sorted(by_type.keys()):
        print(f"## Тип: {agent_type}\n")
        for agent in by_type[agent_type]:
            print(f"• {agent['name']}")
            print(f"  {agent['description']}")
            print(f"  Путь: {agent['path']}")
            print()


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
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    try:
        agents = list_agents(repo_root, args.search)
        print_agents(agents)
        sys.exit(0)

    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
