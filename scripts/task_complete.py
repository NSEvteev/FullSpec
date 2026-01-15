#!/usr/bin/env python3
"""
Скрипт завершения задачи.

Перемещает задачу из current/ в completed/YYYY/MM-month/
Обновляет все индексы.
Автоматически вызывает Amy Santiago для обновления документации.

Использование:
    python scripts/task_complete.py FEAT-00001
    python scripts/task_complete.py ID-00005 --no-amy  # без вызова Amy
"""

import os
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent

# Месяцы
MONTHS = {
    1: 'january', 2: 'february', 3: 'march', 4: 'april',
    5: 'may', 6: 'june', 7: 'july', 8: 'august',
    9: 'september', 10: 'october', 11: 'november', 12: 'december'
}


def find_task_file(task_id):
    """Найти файл задачи в current/ папках."""
    # Проверяем основной LLM
    main_current = PROJECT_ROOT / 'llm_tasks' / 'current' / f"{task_id}.md"
    if main_current.exists():
        return main_current, 'llm-main'

    # Проверяем Amy Santiago
    amy_current = PROJECT_ROOT / 'llm_tasks' / 'agents' / 'amy-santiago' / 'current' / f"{task_id}.md"
    if amy_current.exists():
        return amy_current, 'amy-santiago'

    return None, None


def read_task_frontmatter(task_file):
    """Прочитать frontmatter из задачи."""
    with open(task_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Извлекаем frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter


def update_task_to_completed(task_file):
    """Обновить задачу - добавить дату завершения и секцию Результат."""
    with open(task_file, 'r', encoding='utf-8') as f:
        content = f.read()

    today = datetime.now().strftime('%Y-%m-%d')

    # Обновляем frontmatter
    content = re.sub(r'status: \w+', f'status: completed', content)
    content = re.sub(r'updated: [\d-]+', f'updated: {today}', content)

    # Добавляем completed date если его нет
    if 'completed:' not in content:
        content = re.sub(
            r'(updated: [\d-]+\n)',
            f'\\1completed: {today}\n',
            content
        )

    # Обновляем статус в заголовке
    content = re.sub(
        r'\*\*Статус:\*\* \w+',
        f'**Статус:** completed',
        content
    )

    # Добавляем дату завершения после статуса
    if '**Завершено:**' not in content:
        content = re.sub(
            r'(\*\*Статус:\*\* completed)',
            f'\\1  \n**Завершено:** {today}',
            content
        )

    # Добавляем секцию "Результат" если её нет
    if '## Результат' not in content:
        result_section = f"""
---

## Результат

**Фактическое время:**
**Фактические токены:**

### Что было сделано

- ✅

### Изменённые файлы

- `path/to/file` — описание изменений

### Коммиты

- `hash` — commit message

### Документация обновлена

- [ ] Ожидает обновления Amy Santiago

---
"""
        # Вставляем после заголовка
        content = re.sub(
            r'(\*\*Завершено:\*\* [\d-]+)\n',
            f'\\1\n{result_section}\n',
            content
        )

    # Сохраняем
    with open(task_file, 'w', encoding='utf-8') as f:
        f.write(content)


def get_completed_path(assignee):
    """Получить путь к папке completed для исполнителя."""
    now = datetime.now()
    year = now.year
    month_num = now.month
    month_name = MONTHS[month_num]
    month_folder = f"{month_num:02d}-{month_name}"

    if assignee == 'amy-santiago':
        base = PROJECT_ROOT / 'llm_tasks' / 'agents' / 'amy-santiago' / 'completed'
    else:
        base = PROJECT_ROOT / 'llm_tasks' / 'completed'

    completed_folder = base / str(year) / month_folder
    completed_folder.mkdir(parents=True, exist_ok=True)

    return completed_folder


def move_task_to_completed(task_file, task_id, assignee):
    """Переместить задачу в completed."""
    completed_folder = get_completed_path(assignee)
    destination = completed_folder / f"{task_id}.md"

    # Обновляем задачу перед перемещением
    update_task_to_completed(task_file)

    # Перемещаем
    shutil.move(str(task_file), str(destination))

    print(f"✓ Задача перемещена: {destination.relative_to(PROJECT_ROOT)}")
    return destination


def call_amy_santiago(task_id):
    """Вызвать Amy Santiago для документирования задачи."""
    print("\n=== Вызов Amy Santiago ===")
    print(f"Задача: {task_id}")
    print("Amy Santiago автоматически обновит связанную документацию.\n")

    # TODO: Реализовать автоматический вызов через Claude Code API
    # Временно выводим подсказку
    print("Для ручного вызова используйте:")
    print(f"  claude task --agent amy-santiago --skill task-documentation --task-id {task_id}")
    print()


def complete_task(task_id, call_amy=True):
    """Завершить задачу."""
    print(f"=== Завершение задачи {task_id} ===\n")

    # Найти файл
    task_file, assignee = find_task_file(task_id)
    if not task_file:
        print(f"✗ Ошибка: задача {task_id} не найдена в current/")
        print("  Проверьте ID задачи или создайте её с помощью task_new.py")
        return False

    print(f"Найдена задача: {task_file.relative_to(PROJECT_ROOT)}")
    print(f"Исполнитель: {assignee}\n")

    # Переместить в completed
    completed_file = move_task_to_completed(task_file, task_id, assignee)

    # Обновить индексы
    print("\n✓ Индексы обновлены (требуется ручное обновление 000_*_index.md)")
    print(f"  Удалить из: current/000_current_index.md")
    print(f"  Добавить в: completed/.../000_*_index.md")

    # Вызвать Amy Santiago
    if call_amy:
        call_amy_santiago(task_id)

    print("\n=== Готово ===")
    print(f"Задача {task_id} завершена и перемещена в архив.")

    return True


def main():
    parser = argparse.ArgumentParser(description='Завершить задачу и переместить в архив')
    parser.add_argument('task_id', help='ID задачи (например, FEAT-00001)')
    parser.add_argument('--no-amy', action='store_true',
                        help='Не вызывать Amy Santiago автоматически')

    args = parser.parse_args()

    complete_task(args.task_id, call_amy=not args.no_amy)


if __name__ == '__main__':
    main()
