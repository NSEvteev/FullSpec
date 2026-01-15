#!/usr/bin/env python3
"""
Скрипт для добавления новой задачи в current_tasks.md

Использование:
    python scripts/task_add.py --title "Название задачи" --priority средний
    python scripts/task_add.py -t "Название" -p высокий --description "Описание..."

    # Интерактивный режим
    python scripts/task_add.py -i
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime


def get_next_id(tasks_file: Path) -> int:
    """Получить следующий свободный ID задачи"""
    if not tasks_file.exists():
        return 5  # Начинаем с ID-005 (001-004 уже заняты)

    content = tasks_file.read_text(encoding='utf-8')

    # Ищем все ID в формате [ID-XXX]
    import re
    ids = re.findall(r'\[ID-(\d+)\]', content)

    if not ids:
        return 5

    max_id = max(int(id_num) for id_num in ids)
    return max_id + 1


def format_task(task_id: int, title: str, priority: str, description: str = "",
                subtasks: list = None, files: list = None) -> str:
    """Форматировать задачу в Markdown"""

    task_md = f"""### [ID-{task_id:03d}] {title}

**Статус:** pending
**Приоритет:** {priority}
**Создано:** {datetime.now().strftime('%Y-%m-%d')}

"""

    if description:
        task_md += f"**Описание:**\n{description}\n\n"

    if subtasks:
        task_md += "**Подзадачи:**\n"
        for subtask in subtasks:
            task_md += f"- [ ] {subtask}\n"
        task_md += "\n"

    if files:
        task_md += "**Связанные файлы:**\n"
        for file_path in files:
            task_md += f"- `{file_path}`\n"
        task_md += "\n"

    return task_md


def add_task_to_file(tasks_file: Path, task_md: str):
    """Добавить задачу в файл current_tasks.md"""

    if not tasks_file.exists():
        print(f"❌ Файл не найден: {tasks_file}")
        return False

    content = tasks_file.read_text(encoding='utf-8')

    # Найти раздел "## Задачи в работе" или "## В процессе"
    if "## Задачи в работе" in content:
        marker = "## Задачи в работе"
    elif "## В процессе" in content:
        marker = "## В процессе"
    else:
        print("❌ Не найден раздел для добавления задачи")
        return False

    # Вставить задачу после маркера
    parts = content.split(marker, 1)

    # Найти конец текущих задач (следующий заголовок ##)
    after_marker = parts[1]
    next_section = after_marker.find("\n## ")

    if next_section == -1:
        # Нет следующей секции, добавить в конец
        new_content = parts[0] + marker + "\n\n" + task_md + after_marker
    else:
        # Вставить перед следующей секцией
        new_content = (parts[0] + marker + "\n\n" + task_md +
                      after_marker[next_section:])

    tasks_file.write_text(new_content, encoding='utf-8')
    return True


def interactive_mode():
    """Интерактивный режим создания задачи"""
    print("\n📝 Создание новой задачи")
    print("=" * 50)

    title = input("\n1. Название задачи: ").strip()
    if not title:
        print("❌ Название обязательно!")
        return None

    print("\n2. Приоритет:")
    print("   1 - высокий")
    print("   2 - средний (по умолчанию)")
    print("   3 - низкий")
    priority_choice = input("Выберите (1-3): ").strip() or "2"

    priority_map = {"1": "высокий", "2": "средний", "3": "низкий"}
    priority = priority_map.get(priority_choice, "средний")

    print("\n3. Описание (необязательно, Enter для пропуска):")
    description = input("   ").strip()

    print("\n4. Подзадачи (по одной на строку, пустая строка для завершения):")
    subtasks = []
    while True:
        subtask = input("   - ").strip()
        if not subtask:
            break
        subtasks.append(subtask)

    print("\n5. Связанные файлы (по одному на строку, пустая строка для завершения):")
    files = []
    while True:
        file_path = input("   ").strip()
        if not file_path:
            break
        files.append(file_path)

    return {
        'title': title,
        'priority': priority,
        'description': description,
        'subtasks': subtasks if subtasks else None,
        'files': files if files else None
    }


def main():
    parser = argparse.ArgumentParser(
        description='Добавить задачу в current_tasks.md',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  # Простая задача
  python scripts/task_add.py -t "Исправить баг в auth" -p высокий

  # С описанием
  python scripts/task_add.py -t "Задача" -p средний -d "Подробное описание задачи"

  # Интерактивный режим
  python scripts/task_add.py -i
        """
    )

    parser.add_argument('-t', '--title', help='Название задачи')
    parser.add_argument('-p', '--priority',
                       choices=['высокий', 'средний', 'низкий'],
                       default='средний',
                       help='Приоритет задачи (по умолчанию: средний)')
    parser.add_argument('-d', '--description', help='Описание задачи')
    parser.add_argument('-s', '--subtasks', nargs='*', help='Список подзадач')
    parser.add_argument('-f', '--files', nargs='*', help='Связанные файлы')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Интерактивный режим создания задачи')

    args = parser.parse_args()

    # Путь к current_tasks.md
    root_dir = Path(__file__).parent.parent
    tasks_file = root_dir / 'llm_tasks' / 'current_tasks.md'

    # Интерактивный режим
    if args.interactive:
        task_data = interactive_mode()
        if not task_data:
            return 1
    else:
        # CLI режим
        if not args.title:
            print("❌ Укажите название задачи через --title или используйте -i для интерактивного режима")
            return 1

        task_data = {
            'title': args.title,
            'priority': args.priority,
            'description': args.description or "",
            'subtasks': args.subtasks,
            'files': args.files
        }

    # Получить следующий ID
    task_id = get_next_id(tasks_file)

    # Сформировать задачу
    task_md = format_task(
        task_id=task_id,
        title=task_data['title'],
        priority=task_data['priority'],
        description=task_data['description'],
        subtasks=task_data['subtasks'],
        files=task_data['files']
    )

    # Добавить в файл
    if add_task_to_file(tasks_file, task_md):
        print(f"\n✅ Задача [ID-{task_id:03d}] добавлена в current_tasks.md")
        print(f"   Название: {task_data['title']}")
        print(f"   Приоритет: {task_data['priority']}")
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
