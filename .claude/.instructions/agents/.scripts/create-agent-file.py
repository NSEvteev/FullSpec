#!/usr/bin/env python3
"""
create-agent-file.py — Создание файла агента по шаблону.

Создаёт новый файл конфигурации агента в /.claude/agents/
с заполненной структурой YAML.

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
    0 — файл создан
    1 — ошибка (файл существует, неверные аргументы)
"""

import argparse
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

VALID_TYPES = ("explore", "bash", "plan", "general-purpose")

TEMPLATES = {
    "explore": '''name: {name}
description: {description}
type: explore

prompt: |
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

settings:
  model: haiku
  max_turns: 10
''',

    "bash": '''name: {name}
description: {description}
type: bash

prompt: |
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

settings:
  model: haiku
  max_turns: 5
''',

    "plan": '''name: {name}
description: {description}
type: plan

prompt: |
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

settings:
  model: sonnet
  max_turns: 15
''',

    "general-purpose": '''name: {name}
description: {description}
type: general-purpose

prompt: |
  ## Роль
  {role_description}

  ## Задача
  {task_description}

  ## Инструкции и SSOT
  Релевантные инструкции:
  - /.instructions/standard-principles.md — принципы кода

  ## Доступные скиллы
  При необходимости используй:
  - /principles-validate — проверка принципов

  ## Ограничения
  - Спрашивать подтверждение перед изменениями
  - Логировать все действия

  ## Формат вывода
  Markdown отчёт с результатами

settings:
  model: sonnet
  max_turns: 20
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

def create_agent_file(
    name: str,
    agent_type: str,
    repo_root: Path,
    description: str | None = None
) -> Path:
    """Создать файл агента."""
    # Путь к файлу
    agents_dir = repo_root / ".claude" / "agents"
    file_path = agents_dir / f"{name}.yaml"

    # Проверить существование
    if file_path.exists():
        raise FileExistsError(f"Файл уже существует: {file_path}")

    # Описание по умолчанию
    if not description:
        type_desc = {
            "explore": f"Агент для поиска и анализа",
            "bash": f"Агент для выполнения команд",
            "plan": f"Агент для планирования",
            "general-purpose": f"Универсальный агент",
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

    # Создать директорию если нужно
    agents_dir.mkdir(parents=True, exist_ok=True)

    # Записать файл
    file_path.write_text(content, encoding='utf-8')

    return file_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание файла агента по шаблону"
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
        file_path = create_agent_file(
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
