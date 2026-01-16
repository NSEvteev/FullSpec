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

    # 1. Добавить строку в таблицу индекса
    desc = description or title[:50]  # Описание или обрезанный title
    new_row = f'| {discuss_id} | [{title}]({filename}) | {desc} | 🟡 draft | {today} | — |'

    # Найти таблицу и добавить строку после заголовка
    table_pattern = r'(\| ID \| Название \| Описание \| Статус \| Обновлено \| Связанная архитектура \|\n\|[-|]+\|)'
    if re.search(table_pattern, content):
        content = re.sub(
            table_pattern,
            f'\\1\n{new_row}',
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

    # Создаём контент по новому шаблону
    content = f"""# {discuss_id}_{slug}

<!-- [📖 Дискуссия](../glossary.md#дискуссия) -->

**Статус:** 🟡 draft
**Дата:** {today}

<!--
WORKFLOW СТАТУСОВ ДИСКУССИИ:

🟡 draft        — файл создан, варианты не предложены
🔵 in_progress  — варианты предложены, идёт обсуждение с пользователем
🟣 review       — пользователь выбрал вариант, проводится ревью (/discussion-review)
🟢 approved     — решение принято после ревью
⚪ final        — созданы документы архитектуры

Переходы:
draft → in_progress (после заполнения вариантов)
in_progress → review (пользователь выбрал вариант, запускается /discussion-review)
review → approved (решение подтверждено после ревью, запускается /architect)
approved → final (/architect создаёт архитектуру и переводит в final)
-->

## Исходный запрос пользователя

> {user_request or title}

## Анализ цели и контекст

**Проблема:** [Какую проблему решаем?]

**Область обсуждения:**
- [Что входит в область обсуждения]
- [Что входит в область обсуждения]

**Вне области:** [Что НЕ обсуждаем в этой дискуссии]

## Предложения

| # | Вариант | Плюсы | Минусы | Статус |
|---|---------|-------|--------|--------|
| 1 | [Описание] | [+] | [-] | — |
| 2 | [Описание] | [+] | [-] | — |

## Критерии оценки

| Критерий | Вес | Описание |
|----------|-----|----------|
| [Критерий 1] | Высокий/Средний/Низкий | [Описание] |
| [Критерий 2] | Высокий/Средний/Низкий | [Описание] |

## Сравнение вариантов по критериям

**Шкала:** ⭐⭐⭐ отлично | ⭐⭐ хорошо | ⭐ удовлетворительно | — плохо

| Критерий | Вариант 1 | Вариант 2 | Вариант N |
|----------|-----------|-----------|-----------|
| [Критерий 1] | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| [Критерий 2] | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Итого** | **X/Y** | **X/Y** | **X/Y** |

**Результаты:** 🏆 **[Вариант 1]** | 🥈 **[Вариант 2]** | 🥉 **[Вариант 3]**

## Текстовое сравнение вариантов

**[Вариант 1] vs [Вариант 2]:**
- [В чём ключевое отличие]
- [Когда лучше первый, когда второй]

**[Вариант 2] vs [Вариант 3]:**
- [В чём ключевое отличие]
- [Компромиссы]

**Общие наблюдения:**
- [Что объединяет лидеров]
- [Какой критерий оказался решающим]

## Рекомендуемые варианты

На основе анализа предлагаются **3-4 лучших варианта**:

| # | Вариант | Баллы | Рекомендация |
|---|---------|-------|--------------|
| 1 | **[Лидер]** | X/Y | [Почему рекомендуется — 1 предложение] |
| 2 | **[2-е место]** | X/Y | [Почему рекомендуется — 1 предложение] |
| 3 | **[3-е место]** | X/Y | [Почему рекомендуется — 1 предложение] |

## Принятое решение

[Ожидает обсуждения]

<!-- После принятия решения заменить на:

**Выбран вариант:** [Название варианта]

**Обоснование:**
[Почему выбран этот вариант — 2-3 предложения]

**Аргументы за:**
- [Критерий 1]: [почему хорошо]
- [Критерий 2]: [почему хорошо]

**Почему не другие варианты:**
- [Вариант 2]: [причина отказа]
- [Вариант 3]: [причина отказа]
-->

## Ревью решения

<!-- Заполняется скиллом /discussion-review после выбора варианта -->

[Ожидает выбора варианта]

## Вопросы и допущения

**Вопросы для уточнения:**
- [Вопрос, на который нужен ответ]
  - **Ответ:** [Ответ пользователя — заполняется после обсуждения]

**Неявные допущения:**
- [Допущение, которое делается]

## История обсуждения

- [{today}]: Дискуссия создана

## Связанная архитектура

<!-- При переходе в статус final — заполнить ссылки на созданные документы -->

- [ ] Создать `02_architecture/[ID]_[название].md`

## Добавления к глоссарию

- **[Термин]:** [Определение]
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
