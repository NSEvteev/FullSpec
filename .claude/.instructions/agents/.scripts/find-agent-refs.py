#!/usr/bin/env python3
"""
find-agent-refs.py — Поиск всех ссылок на агента.

Находит все упоминания агента в markdown и yaml файлах
для миграции или деактивации.

Использование:
    python find-agent-refs.py <agent-name>

Аргументы:
    agent-name    Имя агента (без расширения)

Примеры:
    python find-agent-refs.py todo-finder
    python find-agent-refs.py code-reviewer

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
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

def find_references(agent_name: str, repo_root: Path) -> list[dict]:
    """Найти все ссылки на агента."""
    references = []

    # Паттерны для поиска
    patterns = [
        f"{agent_name}.yaml",
        f"{agent_name}:",
        f"[{agent_name}]",
        f"/{agent_name}",
        f"- {agent_name}",
    ]

    # Где искать
    search_paths = [
        ("**/*.md", "Markdown"),
        ("**/*.yaml", "YAML"),
        (".claude/agents/README.md", "Agents README"),
        (".claude/drafts/*.md", "Drafts"),
    ]

    for glob_pattern, source_type in search_paths:
        for file_path in repo_root.glob(glob_pattern):
            # Пропустить сам файл агента
            if file_path.name == f"{agent_name}.yaml":
                continue

            # Пропустить .git и node_modules
            path_str = str(file_path)
            if ".git" in path_str or "node_modules" in path_str:
                continue

            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')

                for line_num, line in enumerate(lines, 1):
                    for pattern in patterns:
                        if pattern in line:
                            references.append({
                                "file": str(file_path.relative_to(repo_root)),
                                "line": line_num,
                                "content": line.strip()[:100],
                                "pattern": pattern,
                                "type": source_type,
                            })
                            break  # Одна ссылка на строку

            except Exception:
                continue

    return references


def print_references(references: list[dict], agent_name: str) -> None:
    """Вывести найденные ссылки."""
    if not references:
        print(f"Ссылки на агента '{agent_name}' не найдены.")
        return

    print(f"Найдено ссылок на '{agent_name}': {len(references)}\n")

    # Группировка по файлам
    by_file: dict[str, list] = {}
    for ref in references:
        file_path = ref["file"]
        if file_path not in by_file:
            by_file[file_path] = []
        by_file[file_path].append(ref)

    # Вывод
    for file_path in sorted(by_file.keys()):
        print(f"## {file_path}")
        for ref in by_file[file_path]:
            print(f"  Строка {ref['line']}: {ref['content']}")
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
        description="Поиск всех ссылок на агента"
    )
    parser.add_argument("agent_name", help="Имя агента (без расширения)")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    try:
        references = find_references(args.agent_name, repo_root)
        print_references(references, args.agent_name)
        sys.exit(0)

    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
