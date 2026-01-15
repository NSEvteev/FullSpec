#!/usr/bin/env python3
"""
Скрипт создания новой задачи с автоинкрементом ID.

Использование:
    python scripts/task_new.py --title "Название задачи" --priority high --category feat
    python scripts/task_new.py -t "Название" -p medium -c fix --assignee amy-santiago
    python scripts/task_new.py -i  # интерактивный режим
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent


def load_counter():
    """Загрузить счётчик задач."""
    counter_file = PROJECT_ROOT / 'llm_tasks' / '.task_counter'

    if not counter_file.exists():
        # Создать дефолтный счётчик
        default_counter = {
            "FEAT": 0,
            "FIX": 0,
            "REFACTOR": 0,
            "DOCS": 0,
            "TEST": 0,
            "INFRA": 0,
            "ID": 5,
            "AMY": 0,
            "description": "Счётчики для каждой категории задач."
        }
        with open(counter_file, 'w', encoding='utf-8') as f:
            json.dump(default_counter, f, indent=2, ensure_ascii=False)
        return default_counter

    with open(counter_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_counter(counter):
    """Сохранить счётчик задач."""
    counter_file = PROJECT_ROOT / 'llm_tasks' / '.task_counter'
    with open(counter_file, 'w', encoding='utf-8') as f:
        json.dump(counter, f, indent=2, ensure_ascii=False)


def get_next_id(category):
    """Получить следующий ID для категории."""
    counter = load_counter()

    if category.upper() not in counter:
        raise ValueError(f"Unknown category: {category}")

    # Инкрементируем счётчик
    counter[category.upper()] += 1
    next_num = counter[category.upper()]

    # Сохраняем
    save_counter(counter)

    # Формируем ID
    task_id = f"{category.upper()}-{next_num:05d}"
    return task_id


def get_task_folder(assignee):
    """Определить папку для задачи."""
    # Все задачи создаются в общей папке current/
    return PROJECT_ROOT / 'llm_tasks' / 'current'


def create_task(title, priority, category, assignee='llm-main', description='', context=''):
    """Создать новую задачу."""
    # Получаем ID
    task_id = get_next_id(category)

    # Папка задачи
    task_folder = get_task_folder(assignee)
    task_file = task_folder / f"{task_id}.md"

    # Текущая дата
    today = datetime.now().strftime('%Y-%m-%d')

    # Загружаем шаблон
    template_file = PROJECT_ROOT / 'templates' / 'task.md'
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()

    # Заполняем шаблон
    content = template.replace('{{ID}}', task_id)
    content = content.replace('{{TITLE}}', title)
    content = content.replace('{{STATUS}}', 'pending')
    content = content.replace('{{PRIORITY}}', priority)
    content = content.replace('{{CATEGORY}}', category.lower())
    content = content.replace('{{CREATED_DATE}}', today)
    content = content.replace('{{UPDATED_DATE}}', today)
    content = content.replace('{{ASSIGNEE}}', assignee)
    content = content.replace('{{DESCRIPTION}}', description or 'Описание задачи.')
    content = content.replace('{{CONTEXT}}', context or 'Контекст задачи.')

    # Сохраняем файл
    with open(task_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Задача создана: {task_id}")
    print(f"  Файл: {task_file.relative_to(PROJECT_ROOT)}")
    print(f"  Приоритет: {priority}")
    print(f"  Категория: {category}")
    print(f"  Исполнитель: {assignee}")
    print()
    print("Следующие шаги:")
    print(f"  1. Отредактировать файл: {task_file.relative_to(PROJECT_ROOT)}")
    print(f"  2. Обновить индекс: llm_tasks/current/000_current_index.md")

    return task_id


def interactive_mode():
    """Интерактивный режим создания задачи."""
    print("=== Создание новой задачи ===\n")

    title = input("Название задачи: ").strip()
    if not title:
        print("Ошибка: название обязательно")
        return

    print("\nПриоритет:")
    print("  1. high (высокий)")
    print("  2. medium (средний)")
    print("  3. low (низкий)")
    priority_choice = input("Выберите (1-3): ").strip()
    priority_map = {'1': 'high', '2': 'medium', '3': 'low'}
    priority = priority_map.get(priority_choice, 'medium')

    print("\nКатегория:")
    print("  1. FEAT (новая функциональность)")
    print("  2. FIX (исправление бага)")
    print("  3. REFACTOR (рефакторинг)")
    print("  4. DOCS (документация)")
    print("  5. TEST (тесты)")
    print("  6. INFRA (инфраструктура)")
    print("  7. ID (общая задача)")
    category_choice = input("Выберите (1-7): ").strip()
    category_map = {
        '1': 'FEAT',
        '2': 'FIX',
        '3': 'REFACTOR',
        '4': 'DOCS',
        '5': 'TEST',
        '6': 'INFRA',
        '7': 'ID'
    }
    category = category_map.get(category_choice, 'ID')

    print("\nИсполнитель:")
    print("  1. llm-main (основной LLM)")
    print("  2. amy-santiago (агент Amy)")
    assignee_choice = input("Выберите (1-2): ").strip()
    assignee = 'amy-santiago' if assignee_choice == '2' else 'llm-main'

    description = input("\nОписание (Enter - пропустить): ").strip()
    context = input("Контекст (Enter - пропустить): ").strip()

    print()
    create_task(title, priority, category, assignee, description, context)


def main():
    parser = argparse.ArgumentParser(description='Создать новую задачу')
    parser.add_argument('-t', '--title', help='Название задачи')
    parser.add_argument('-p', '--priority', choices=['high', 'medium', 'low'], default='medium',
                        help='Приоритет задачи (default: medium)')
    parser.add_argument('-c', '--category',
                        choices=['feat', 'fix', 'refactor', 'docs', 'test', 'infra', 'id'],
                        help='Категория задачи')
    parser.add_argument('-a', '--assignee', default='llm-main',
                        help='Исполнитель (llm-main, amy-santiago)')
    parser.add_argument('-d', '--description', default='', help='Описание задачи')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Интерактивный режим')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.title and args.category:
        create_task(
            args.title,
            args.priority,
            args.category,
            args.assignee,
            args.description
        )
    else:
        parser.print_help()
        print("\nПримеры:")
        print('  python scripts/task_new.py -t "Добавить тесты" -p high -c test')
        print('  python scripts/task_new.py -i  # интерактивный режим')


if __name__ == '__main__':
    main()
