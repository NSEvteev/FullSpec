#!/usr/bin/env python3
"""
create-agent-file.py — Создание агента по шаблону.

Создаёт папку агента с файлом AGENT.md в /.claude/agents/

Использование:
    python create-agent-file.py <name> <type> [--description <text>]

Аргументы:
    name        Имя агента (kebab-case)
    type        Тип: explore, bash, plan, general-purpose

Примеры:
    python create-agent-file.py todo-finder explore
    python create-agent-file.py code-reviewer general-purpose --description "Код-ревью"
    python create-agent-file.py test-runner bash

Возвращает:
    0 — агент создан
    1 — ошибка (агент существует, неверные аргументы)
"""

import argparse
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

VALID_TYPES = ("explore", "bash", "plan", "general-purpose")

TEMPLATES = {
    "explore": '''---
name: {name}
description: {description}
type: explore
model: haiku
tools: Read, Grep, Glob
permissionMode: plan
max_turns: 10
---

## Роль
{role_description}

## Задача
{task_description}

## Область работы
- Путь: указывается в запросе
- Типы файлов: *
- Исключения: node_modules/, .git/, __pycache__/

## Ограничения
- НЕ модифицировать файлы
- НЕ создавать файлы
- Только поиск и анализ

## Формат вывода
Markdown таблица:
| Файл | Строка | Результат |
|------|--------|-----------|
''',

    "bash": '''---
name: {name}
description: {description}
type: bash
model: haiku
tools: Bash, Read
permissionMode: default
max_turns: 10
---

## Роль
{role_description}

## Задача
{task_description}

## Ограничения
- НЕ выполнять деструктивные команды (rm -rf, git reset --hard)
- Спрашивать подтверждение перед изменениями
- Логировать все команды

## Формат вывода
Результаты выполнения команд
''',

    "plan": '''---
name: {name}
description: {description}
type: plan
model: sonnet
tools: Read, Grep, Glob
permissionMode: plan
max_turns: 20
---

## Роль
{role_description}

## Задача
{task_description}

## Контекст для сбора
1. Структура папок и их назначение
2. Зависимости между модулями
3. Точки расширения

## Ограничения
- Только анализ, НЕ реализация
- НЕ создавать файлы
- НЕ модифицировать код

## Формат вывода
Markdown отчёт с секциями:
- Анализ
- Рекомендации
- План действий
''',

    "general-purpose": '''---
name: {name}
description: {description}
type: general-purpose
model: sonnet
tools: Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion
disallowedTools: WebSearch, WebFetch
permissionMode: default
max_turns: 30
skills:
  - principles-validate
---

## Роль
{role_description}

## Задача
{task_description}

## Инструкции и SSOT
Релевантные инструкции:
- /.instructions/standard-principles.md — принципы кода

## Скиллы
Используй скиллы из frontmatter вместо ручных операций.

## Ограничения
- Спрашивать подтверждение перед изменениями
- Логировать все действия

## Формат вывода
Markdown отчёт с результатами
''',
}


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

def create_agent(
    name: str,
    agent_type: str,
    repo_root: Path,
    description: str | None = None
) -> Path:
    """Создать папку агента с AGENT.md."""
    # Путь к папке агента
    agents_dir = repo_root / ".claude" / "agents"
    agent_dir = agents_dir / name
    agent_file = agent_dir / "AGENT.md"

    # Проверить существование
    if agent_dir.exists():
        raise FileExistsError(f"Агент уже существует: {agent_dir}")

    # Описание по умолчанию
    if not description:
        type_desc = {
            "explore": f"Агент для поиска и анализа. Используй для исследования кодовой базы.",
            "bash": f"Агент для выполнения команд. Используй для автоматизации.",
            "plan": f"Агент для планирования. Используй для анализа архитектуры.",
            "general-purpose": f"Универсальный агент. Используй для сложных задач.",
        }
        description = type_desc.get(agent_type, f"Агент {name}")

    # Заполнить шаблон
    template = TEMPLATES[agent_type]
    content = template.format(
        name=name,
        description=description,
        role_description=f"Агент {name}.",
        task_description="Описание задачи.",
    )

    # Создать директорию
    agent_dir.mkdir(parents=True, exist_ok=True)

    # Записать файл
    agent_file.write_text(content, encoding='utf-8')

    return agent_file


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание агента по шаблону"
    )
    parser.add_argument("name", help="Имя агента (kebab-case)")
    parser.add_argument("type", choices=VALID_TYPES, help="Тип агента")
    parser.add_argument(
        "--description",
        help="Описание агента"
    )
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    try:
        file_path = create_agent(
            name=args.name,
            agent_type=args.type,
            repo_root=repo_root,
            description=args.description,
        )
        rel_path = file_path.relative_to(repo_root)
        print(f"✅ Создан: {rel_path}")
        sys.exit(0)

    except FileExistsError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
