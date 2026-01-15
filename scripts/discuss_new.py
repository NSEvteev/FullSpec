#!/usr/bin/env python3
"""
Скрипт создания новой дискуссии с автоинкрементом ID.

Использование:
    python scripts/discuss_new.py "Тема дискуссии"
    python scripts/discuss_new.py -t "Тема" -q "Исходный запрос пользователя"
    python scripts/discuss_new.py -i  # интерактивный режим
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent
DISCUSS_DIR = PROJECT_ROOT / 'general_docs' / '01_discuss'
INDEX_FILE = DISCUSS_DIR / '000_discuss.md'
TEMPLATE_FILE = PROJECT_ROOT / 'llm_instructions' / 'templates' / 'discuss.md'
COUNTER_FILE = PROJECT_ROOT / 'general_docs' / '.doc_counter'


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
    """Получить следующий ID для дискуссии."""
    counters = load_counters()
    counters["discuss"] += 1
    save_counters(counters)
    return f"{counters['discuss']:03d}"


def slugify(text):
    """Преобразовать текст в slug для имени файла."""
    # Транслитерация кириллицы
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

    # Убираем множественные подчёркивания и обрезаем
    slug = re.sub(r'_+', '_', ''.join(result)).strip('_')
    return slug[:50]  # Ограничиваем длину


def update_index(discuss_id, title, filename, description=''):
    """Обновить индекс дискуссий."""
    today = datetime.now().strftime('%Y-%m-%d')

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Обновить статистику draft
    content = re.sub(
        r'\| draft \| (\d+) \|',
        lambda m: f'| draft | {int(m.group(1)) + 1} |',
        content
    )

    # 2. Обновить всего
    content = re.sub(
        r'\| \*\*Всего\*\* \| \*\*(\d+)\*\* \|',
        lambda m: f'| **Всего** | **{int(m.group(1)) + 1}** |',
        content
    )

    # 3. Обновить дату
    content = re.sub(
        r'\*\*Последнее обновление:\*\* \d{4}-\d{2}-\d{2}',
        f'**Последнее обновление:** {today}',
        content
    )

    # 4. Добавить строку в таблицу индекса
    desc = description or title[:50]  # Описание или обрезанный title
    new_row = f'| {discuss_id} | [{title}]({filename}) | {desc} | draft | {today} | — |'

    # Найти таблицу и добавить строку после заголовка
    table_pattern = r'(\| ID \| Название \| Описание \| Статус \| Обновлено \| Связанная архитектура \|\n\|[-|]+\|)'
    if re.search(table_pattern, content):
        content = re.sub(
            table_pattern,
            f'\\1\n{new_row}',
            content
        )

    # 5. Обновить быстрый поиск по статусу draft
    content = re.sub(
        r'- \*\*draft\*\* \((\d+)\) — новые идеи и предложения:?[^\n]*',
        lambda m: f'- **draft** ({int(m.group(1)) + 1}) — новые идеи и предложения: [{discuss_id}_{slugify(title)}]({filename})',
        content
    )

    # Если draft был 0, добавить ссылку
    if '- **draft** (0)' in content:
        content = content.replace(
            '- **draft** (0) — новые идеи и предложения',
            f'- **draft** (1) — новые идеи и предложения: [{discuss_id}_{slugify(title)}]({filename})'
        )

    # 6. Обновить "По дате"
    content = re.sub(
        r'- \*\*Последние обновления:\*\* [^\n]+',
        f'- **Последние обновления:** [{discuss_id}_{slugify(title)}]({filename})',
        content
    )
    content = re.sub(
        r'- \*\*Недавно созданные:\*\* [^\n]+',
        f'- **Недавно созданные:** [{discuss_id}_{slugify(title)}]({filename})',
        content
    )

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


def create_discussion(title, user_request=None, description=None):
    """Создать новую дискуссию."""
    discuss_id = get_next_id()
    slug = slugify(title)
    filename = f"{discuss_id}_{slug}.md"
    filepath = DISCUSS_DIR / filename

    today = datetime.now().strftime('%Y-%m-%d')
    desc = description or title[:50]  # Короткое описание для индекса

    # Создаём контент
    content = f"""# {discuss_id}_{slug}

<!-- [📖 Дискуссия](../glossary.md#дискуссия) -->

**Статус:** draft

## Исходный запрос пользователя

> {user_request or title}

## Анализ цели и контекст

[Какую проблему/возможность обсуждаем?]

## Предложения

| # | Вариант | Плюсы | Минусы | Статус |
|---|---------|-------|--------|--------|
| 1 | [Описание] | [+] | [-] | — |
| 2 | [Описание] | [+] | [-] | — |

## Принятое решение

[Ожидает обсуждения]

## Аргументация

[После обсуждения]

## Дискуссия и анализ

[Критика, вопросы, уточнения — если есть]

## Принятые архитектурные решения

- [ ] [Действие] → создать `02_architecture/[ID]_[название].md`

## Добавления к глоссарию

- **[Термин]:** [Определение]

## Связанные документы

- Архитектура: [будет создана]
- Ресурсы: [будут добавлены]
"""

    # Сохраняем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Обновляем индекс
    update_index(discuss_id, title, filename, desc)

    print(f"[OK] Diskussiya sozdana: {discuss_id}")
    print(f"  Fayl: general_docs/01_discuss/{filename}")
    print(f"  Tema: {title}")
    print(f"  Opisanie: {desc}")
    print(f"  Status: draft")
    print()
    print("Next steps:")
    print(f"  1. Fill variants in discussion file")
    print(f"  2. Discuss with team")
    print(f"  3. Make decision -> change status")

    return discuss_id, filename


def interactive_mode():
    """Интерактивный режим создания дискуссии."""
    print("=== Создание новой дискуссии ===\n")

    title = input("Тема дискуссии: ").strip()
    if not title:
        print("Ошибка: тема обязательна")
        return

    description = input("Краткое описание (для индекса, Enter - использовать тему): ").strip()
    if not description:
        description = title[:50]

    user_request = input("Исходный запрос (Enter - использовать тему): ").strip()
    if not user_request:
        user_request = title

    print()
    create_discussion(title, user_request, description)


def main():
    parser = argparse.ArgumentParser(description='Создать новую дискуссию')
    parser.add_argument('topic', nargs='?', help='Тема дискуссии')
    parser.add_argument('-t', '--title', help='Тема дискуссии (альтернатива positional)')
    parser.add_argument('-d', '--description', help='Краткое описание для индекса')
    parser.add_argument('-q', '--request', help='Исходный запрос пользователя')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Интерактивный режим')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.topic or args.title:
        title = args.topic or args.title
        create_discussion(title, args.request, args.description)
    else:
        parser.print_help()
        print("\nПримеры:")
        print('  python scripts/discuss_new.py "UI стайлгайд"')
        print('  python scripts/discuss_new.py -t "Выбор БД" -d "Выбор базы данных"')
        print('  python scripts/discuss_new.py -i  # интерактивный режим')


if __name__ == '__main__':
    main()
