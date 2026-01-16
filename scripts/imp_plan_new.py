#!/usr/bin/env python3
"""
Скрипт создания нового плана реализации с автоинкрементом ID.

Использование:
    python scripts/imp_plan_new.py "Название плана"
    python scripts/imp_plan_new.py -t "Название" -a "DEC-001" --domain "Backend/API"
    python scripts/imp_plan_new.py -i  # интерактивный режим
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent
PLANS_DIR = PROJECT_ROOT / 'general_docs' / '06_imp_plans'
INDEX_FILE = PLANS_DIR / '000_imp_plans.md'
COUNTER_FILE = PROJECT_ROOT / 'general_docs' / '.doc_counter'

# Допустимые домены
VALID_DOMAINS = [
    'UI/Frontend',
    'Backend/API',
    'Auth/Security',
    'Database',
    'Infrastructure',
    'Architecture'
]


def load_counters():
    """Загрузить счётчики документов."""
    if not COUNTER_FILE.exists():
        default = {
            "discuss": 0,
            "architecture": 0,
            "diagrams": 0,
            "decisions": 0,
            "resources": 0,
            "imp_plans": 0,
            "description": "Счётчики ID для документов в general_docs/"
        }
        save_counters(default)
        return default

    with open(COUNTER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_counters(counters):
    """Сохранить счётчики документов."""
    with open(COUNTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(counters, f, indent=2, ensure_ascii=False)


def get_next_id():
    """Получить следующий ID для плана."""
    counters = load_counters()
    counters["imp_plans"] += 1
    save_counters(counters)
    return f"{counters['imp_plans']:03d}"


def slugify(text):
    """Преобразовать текст в slug для имени файла."""
    translit = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': '_', '-': '_'
    }

    result = []
    for char in text.lower():
        if char in translit:
            result.append(translit[char])
        elif char.isalnum():
            result.append(char)
        elif char in '_ ':
            result.append('_')

    slug = re.sub(r'_+', '_', ''.join(result)).strip('_')
    return slug[:50]


def update_index(plan_id, title, filename, description='', adr_id=''):
    """Обновить индекс планов."""
    today = datetime.now().strftime('%Y-%m-%d')

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Формируем ссылки
    adr_link = f'[{adr_id}](../04_decisions/{adr_id}_*.md)' if adr_id else '—'
    desc = description[:30] if description else title[:30]

    # Проверяем, есть ли уже таблица с данными или заглушка
    if 'В настоящее время планы реализации отсутствуют.' in content:
        # Заменяем заглушку на таблицу
        new_table = f"""| ID | Название | Описание | Статус | Прогресс | Связанная архитектура |
|----|----------|----------|--------|----------|----------------------|
| {plan_id} | [{title}]({filename}) | {desc} | 🟡 draft | 0% | {adr_link} |"""

        content = content.replace(
            'В настоящее время планы реализации отсутствуют.\n\n**Формат таблицы:**\n\n| ID | Название | Описание | Статус | Прогресс | Связанная архитектура |\n|----|----------|----------|--------|----------|----------------------|\n| - | - | - | - | - | - |',
            new_table
        )
    else:
        # Добавить строку в существующую таблицу
        new_row = f'| {plan_id} | [{title}]({filename}) | {desc} | 🟡 draft | 0% | {adr_link} |'

        table_pattern = r'(\| ID \| Название \| Описание \| Статус \| Прогресс \| Связанная архитектура \|\n\|[-|]+\|)'
        if re.search(table_pattern, content):
            content = re.sub(
                table_pattern,
                f'\\1\n{new_row}',
                content
            )

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


def create_imp_plan(title, adr_id=None, description=None, domain=None):
    """Создать новый план реализации."""
    plan_id = get_next_id()
    slug = slugify(title)
    filename = f"{plan_id}_plan_{slug}.md"
    filepath = PLANS_DIR / filename

    today = datetime.now().strftime('%Y-%m-%d')
    desc = description or title[:50]
    domain_str = domain or '[UI/Frontend | Backend/API | Auth/Security | Database | Infrastructure | Architecture]'

    # Связь с ADR
    adr_link = f'[{adr_id}](../04_decisions/{adr_id}_*.md)' if adr_id else '[Нет связанного ADR]'

    content = f"""# {plan_id}_plan_{slug}

<!-- [📖 План реализации](../glossary.md#план-реализации) -->

**Статус:** 🟡 draft
**Область:** {domain_str}
**Дата создания:** {today}
**Дата обновления:** {today}

<!--
WORKFLOW СТАТУСОВ ПЛАНА:

🟡 draft        — план создан, задачи не определены
🔵 in_progress  — работа по плану идёт
🟣 review       — план на проверке
🧪 test         — тестирование
🟢 approved     — одобрено
⚪ final        — план завершён, всё реализовано

Переходы:
draft → in_progress (после определения задач)
in_progress → review (основная работа завершена)
review → test (ревью пройдено)
test → approved (тесты пройдены)
approved → final (документация обновлена)
-->

## Связанные документы

- **ADR:** {adr_link} (источник плана)
- **Ресурсы:** [ссылки на 05_resources/]

## Обзор

{desc}

## Задачи

### Фаза 1: Подготовка

| # | Задача | Описание | Зависимости | Статус |
|---|--------|----------|-------------|--------|
| 1.1 | [Название] | [Что нужно сделать] | — | task_planned |
| 1.2 | [Название] | [Что нужно сделать] | 1.1 | task_planned |

### Фаза 2: Реализация

| # | Задача | Описание | Зависимости | Статус |
|---|--------|----------|-------------|--------|
| 2.1 | [Название] | [Что нужно сделать] | 1.2 | task_planned |
| 2.2 | [Название] | [Что нужно сделать] | 2.1 | task_planned |

### Фаза 3: Тестирование и документация

| # | Задача | Описание | Зависимости | Статус |
|---|--------|----------|-------------|--------|
| 3.1 | Написать тесты | [Описание тестов] | 2.2 | task_planned |
| 3.2 | Обновить документацию | [Что обновить] | 3.1 | task_planned |

## Статусы задач

- `task_planned` — задача запланирована
- `task_in_progress` — задача в работе
- `task_testing` — задача на тестировании
- `task_done` — задача завершена
- `task_blocked` — задача заблокирована

## Критерии готовности

- [ ] Все задачи выполнены
- [ ] Тесты написаны и проходят
- [ ] Документация обновлена
- [ ] Code review пройдено

## Заметки

[Дополнительная информация, если есть]

---

**ID:** {plan_id}
**Шаблон:** [imp_plan.md](../../llm_instructions/templates/imp_plan.md)
**Индекс:** [000_imp_plans.md](000_imp_plans.md)
"""

    # Сохраняем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Обновляем индекс
    update_index(plan_id, title, filename, desc, adr_id)

    print(f"[OK] Plan sozdan: {plan_id}")
    print(f"  Fayl: general_docs/06_imp_plans/{filename}")
    print(f"  Nazvanie: {title}")
    print(f"  Opisanie: {desc}")
    print(f"  ADR: {adr_id or 'ne ukazan'}")
    print(f"  Oblast: {domain_str}")
    print(f"  Status: draft")
    print()
    print("Next steps:")
    print(f"  1. Define tasks in phases")
    print(f"  2. Link to resources")
    print(f"  3. Start working -> change status to in_progress")

    return plan_id, filename


def interactive_mode():
    """Интерактивный режим создания плана."""
    print("=== Создание плана реализации ===\n")

    title = input("Название плана: ").strip()
    if not title:
        print("Ошибка: название обязательно")
        return

    description = input("Краткое описание (Enter - использовать название): ").strip()
    if not description:
        description = title[:50]

    adr_id = input("ID связанного ADR (Enter - пропустить, формат: DEC-001): ").strip()
    if not adr_id:
        adr_id = None

    print("\nДоступные домены:")
    for i, d in enumerate(VALID_DOMAINS, 1):
        print(f"  {i}. {d}")
    domain_choice = input("Выберите домен (1-6 или Enter для пропуска): ").strip()

    domain = None
    if domain_choice.isdigit() and 1 <= int(domain_choice) <= len(VALID_DOMAINS):
        domain = VALID_DOMAINS[int(domain_choice) - 1]

    print()
    create_imp_plan(title, adr_id, description, domain)


def main():
    parser = argparse.ArgumentParser(description='Создать план реализации')
    parser.add_argument('title', nargs='?', help='Название плана')
    parser.add_argument('-t', '--title', dest='title_opt', help='Название (альтернатива positional)')
    parser.add_argument('-a', '--adr', help='ID связанного ADR (например: DEC-001)')
    parser.add_argument('--desc', '--description', dest='description', help='Краткое описание')
    parser.add_argument('--domain', help='Область (UI/Frontend, Backend/API, etc.)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Интерактивный режим')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.title or args.title_opt:
        title = args.title or args.title_opt
        create_imp_plan(title, args.adr, args.description, args.domain)
    else:
        parser.print_help()
        print("\nПримеры:")
        print('  python scripts/imp_plan_new.py "Реализация аутентификации"')
        print('  python scripts/imp_plan_new.py -t "Auth System" -a "DEC-001" --domain "Auth/Security"')
        print('  python scripts/imp_plan_new.py -i  # интерактивный режим')


if __name__ == '__main__':
    main()
