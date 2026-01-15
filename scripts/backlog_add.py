#!/usr/bin/env python3
"""
Скрипт для добавления задачи в бэклог (future_tasks.md)

Использование:
    python scripts/backlog_add.py --title "Название задачи" --priority P1 --category feat
    python scripts/backlog_add.py -t "Название" -p P2 -c docs -d "Описание..."

    # Интерактивный режим
    python scripts/backlog_add.py -i
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime


def get_next_id(tasks_file: Path) -> int:
    """Получить следующий свободный ID задачи"""
    if not tasks_file.exists():
        return 100  # Бэклог начинается с ID-100

    content = tasks_file.read_text(encoding='utf-8')

    # Ищем все ID в формате [ID-XXX]
    import re
    ids = re.findall(r'\[ID-(\d+)\]', content)

    if not ids:
        return 100

    max_id = max(int(id_num) for id_num in ids)
    return max_id + 1


def format_task(task_id: int, title: str, priority: str, category: str,
                description: str = "", context: str = "", dependencies: list = None,
                complexity: str = "средняя", time: str = "средняя") -> str:
    """Форматировать задачу для бэклога"""

    task_md = f"""#### [ID-{task_id:03d}] {title}
**Категория:** {category}
**Статус:** pending
**Создано:** {datetime.now().strftime('%Y-%m-%d')}

"""

    if description:
        task_md += f"**Описание:**\n{description}\n\n"

    if context:
        task_md += f"**Контекст:**\n{context}\n\n"

    if dependencies:
        task_md += "**Зависимости:**\n"
        for dep in dependencies:
            task_md += f"- {dep}\n"
        task_md += "\n"

    task_md += f"""**Оценка:**
- Сложность: {complexity}
- Время: {time}

---

"""

    return task_md


def add_task_to_file(tasks_file: Path, task_md: str, priority: str):
    """Добавить задачу в файл future_tasks.md"""

    if not tasks_file.exists():
        print(f"❌ Файл не найден: {tasks_file}")
        return False

    content = tasks_file.read_text(encoding='utf-8')

    # Определить раздел по приоритету
    priority_map = {
        'P0': '### Приоритет P0: Критичный',
        'P1': '### Приоритет P1: Высокий',
        'P2': '### Приоритет P2: Средний',
        'P3': '### Приоритет P3: Низкий'
    }

    marker = priority_map.get(priority)
    if not marker:
        print(f"❌ Неверный приоритет: {priority}")
        return False

    # Если раздел не существует, создать его
    if marker not in content:
        # Найти место для вставки
        if priority == 'P0':
            # P0 - вставить в начало после "## Бэклог задач"
            insert_marker = "## Бэклог задач"
            parts = content.split(insert_marker, 1)

            # Найти конец секции (следующая строка с датой обновления)
            after_marker = parts[1]
            next_line = after_marker.find("\n\n")

            new_section = f"\n\n{marker}\n\n{task_md}"
            new_content = parts[0] + insert_marker + after_marker[:next_line] + new_section + after_marker[next_line:]
        else:
            # Найти предыдущий приоритет
            prev_priority = f"P{int(priority[1]) - 1}"
            prev_marker = priority_map.get(prev_priority)

            if prev_marker in content:
                # Вставить после предыдущего приоритета
                parts = content.split(prev_marker, 1)
                after_marker = parts[1]
                next_section = after_marker.find("\n### Приоритет")

                if next_section == -1:
                    next_section = after_marker.find("\n## ")

                new_section = f"\n\n{marker}\n\n{task_md}"
                new_content = parts[0] + prev_marker + after_marker[:next_section] + new_section + after_marker[next_section:]
            else:
                print(f"❌ Не найден раздел для приоритета {priority}")
                return False
    else:
        # Раздел существует, вставить задачу
        parts = content.split(marker, 1)
        after_marker = parts[1]

        # Найти конец секции (следующий заголовок ###)
        next_section = after_marker.find("\n### Приоритет")
        if next_section == -1:
            next_section = after_marker.find("\n## ")

        if next_section == -1:
            # Нет следующей секции, добавить в конец
            new_content = parts[0] + marker + "\n\n" + task_md + after_marker
        else:
            # Вставить перед следующей секцией
            new_content = parts[0] + marker + "\n\n" + task_md + after_marker[next_section:]

    tasks_file.write_text(new_content, encoding='utf-8')
    return True


def interactive_mode():
    """Интерактивный режим создания задачи для бэклога"""
    print("\n📋 Добавление задачи в бэклог")
    print("=" * 50)

    title = input("\n1. Название задачи: ").strip()
    if not title:
        print("❌ Название обязательно!")
        return None

    print("\n2. Приоритет:")
    print("   0 - P0 (критично - блокирует работу)")
    print("   1 - P1 (высокий - важно для проекта)")
    print("   2 - P2 (средний - улучшение) [по умолчанию]")
    print("   3 - P3 (низкий - nice to have)")
    priority_choice = input("Выберите (0-3): ").strip() or "2"

    priority_map = {"0": "P0", "1": "P1", "2": "P2", "3": "P3"}
    priority = priority_map.get(priority_choice, "P2")

    print("\n3. Категория:")
    print("   1 - arch (архитектура)")
    print("   2 - feat (новая функциональность)")
    print("   3 - fix (исправление)")
    print("   4 - docs (документация)")
    print("   5 - infra (инфраструктура)")
    category_choice = input("Выберите (1-5): ").strip()

    category_map = {
        "1": "arch", "2": "feat", "3": "fix",
        "4": "docs", "5": "infra"
    }
    category = category_map.get(category_choice, "feat")

    print("\n4. Описание:")
    description = input("   ").strip()

    print("\n5. Контекст (необязательно, Enter для пропуска):")
    context = input("   ").strip()

    print("\n6. Зависимости (по одной на строку, пустая строка для завершения):")
    dependencies = []
    while True:
        dep = input("   - ").strip()
        if not dep:
            break
        dependencies.append(dep)

    print("\n7. Сложность:")
    print("   1 - простая")
    print("   2 - средняя [по умолчанию]")
    print("   3 - сложная")
    complexity_choice = input("Выберите (1-3): ").strip() or "2"

    complexity_map = {"1": "простая", "2": "средняя", "3": "сложная"}
    complexity = complexity_map.get(complexity_choice, "средняя")

    print("\n8. Время:")
    print("   1 - короткая")
    print("   2 - средняя [по умолчанию]")
    print("   3 - длительная")
    time_choice = input("Выберите (1-3): ").strip() or "2"

    time_map = {"1": "короткая", "2": "средняя", "3": "длительная"}
    time_estimate = time_map.get(time_choice, "средняя")

    return {
        'title': title,
        'priority': priority,
        'category': category,
        'description': description,
        'context': context,
        'dependencies': dependencies if dependencies else None,
        'complexity': complexity,
        'time': time_estimate
    }


def main():
    parser = argparse.ArgumentParser(
        description='Добавить задачу в бэклог (future_tasks.md)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Категории:
  arch  - Архитектура
  feat  - Новая функциональность
  fix   - Исправление
  docs  - Документация
  infra - Инфраструктура

Приоритеты:
  P0 - Критично (блокирует работу)
  P1 - Высокий (важно для проекта)
  P2 - Средний (улучшение)
  P3 - Низкий (nice to have)

Примеры:
  # Простая задача
  python scripts/backlog_add.py -t "Добавить тесты" -p P2 -c feat

  # С описанием
  python scripts/backlog_add.py -t "Задача" -p P1 -c docs -d "Описание задачи"

  # Интерактивный режим
  python scripts/backlog_add.py -i
        """
    )

    parser.add_argument('-t', '--title', help='Название задачи')
    parser.add_argument('-p', '--priority',
                       choices=['P0', 'P1', 'P2', 'P3'],
                       default='P2',
                       help='Приоритет (по умолчанию: P2)')
    parser.add_argument('-c', '--category',
                       choices=['arch', 'feat', 'fix', 'docs', 'infra'],
                       default='feat',
                       help='Категория (по умолчанию: feat)')
    parser.add_argument('-d', '--description', help='Описание задачи')
    parser.add_argument('--context', help='Контекст задачи')
    parser.add_argument('--complexity',
                       choices=['простая', 'средняя', 'сложная'],
                       default='средняя',
                       help='Сложность (по умолчанию: средняя)')
    parser.add_argument('--time',
                       choices=['короткая', 'средняя', 'длительная'],
                       default='средняя',
                       help='Оценка времени (по умолчанию: средняя)')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Интерактивный режим')

    args = parser.parse_args()

    # Путь к future_tasks.md
    root_dir = Path(__file__).parent.parent
    tasks_file = root_dir / 'llm_tasks' / 'future_tasks.md'

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
            'category': args.category,
            'description': args.description or "",
            'context': args.context or "",
            'dependencies': None,
            'complexity': args.complexity,
            'time': args.time
        }

    # Получить следующий ID
    task_id = get_next_id(tasks_file)

    # Сформировать задачу
    task_md = format_task(
        task_id=task_id,
        title=task_data['title'],
        priority=task_data['priority'],
        category=task_data['category'],
        description=task_data['description'],
        context=task_data['context'],
        dependencies=task_data['dependencies'],
        complexity=task_data['complexity'],
        time=task_data['time']
    )

    # Добавить в файл
    if add_task_to_file(tasks_file, task_md, task_data['priority']):
        print(f"\n✅ Задача [ID-{task_id:03d}] добавлена в бэклог")
        print(f"   Название: {task_data['title']}")
        print(f"   Приоритет: {task_data['priority']}")
        print(f"   Категория: {task_data['category']}")
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
