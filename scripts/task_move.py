#!/usr/bin/env python3
"""
Скрипт перемещения задачи между current и future.

Использование:
    python scripts/task_move.py FEAT-00001 current   # future → current
    python scripts/task_move.py FEAT-00002 future    # current → future
"""

import shutil
import argparse
from pathlib import Path


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent


def find_task(task_id):
    """Найти задачу в current или future."""
    # Проверяем current
    current_file = PROJECT_ROOT / 'llm_tasks' / 'current' / f"{task_id}.md"
    if current_file.exists():
        return current_file, 'current'

    # Проверяем future
    future_file = PROJECT_ROOT / 'llm_tasks' / 'future' / f"{task_id}.md"
    if future_file.exists():
        return future_file, 'future'

    return None, None


def move_task(task_id, target):
    """Переместить задачу."""
    task_file, current_location = find_task(task_id)

    if not task_file:
        print(f"✗ Ошибка: задача {task_id} не найдена")
        return False

    if current_location == target:
        print(f"✗ Задача {task_id} уже находится в {target}/")
        return False

    # Целевая папка
    target_folder = PROJECT_ROOT / 'llm_tasks' / target
    destination = target_folder / f"{task_id}.md"

    # Перемещаем
    shutil.move(str(task_file), str(destination))

    print(f"✓ Задача перемещена:")
    print(f"  Из: {task_file.relative_to(PROJECT_ROOT)}")
    print(f"  В: {destination.relative_to(PROJECT_ROOT)}")
    print()
    print("Следующие шаги:")
    print(f"  1. Обновить индекс: {current_location}/0_task_index.md")
    print(f"  2. Обновить индекс: {target}/0_task_index.md")

    return True


def main():
    parser = argparse.ArgumentParser(description='Переместить задачу между current и future')
    parser.add_argument('task_id', help='ID задачи (например, FEAT-00001)')
    parser.add_argument('target', choices=['current', 'future'],
                        help='Целевая папка (current или future)')

    args = parser.parse_args()

    move_task(args.task_id, args.target)


if __name__ == '__main__':
    main()
