#!/usr/bin/env python3
"""
Скрипт создания нового архитектурного документа с автоинкрементом ID.

Использование:
    python scripts/architecture_new.py "Название компонента"
    python scripts/architecture_new.py -t "Название" -d "ID дискуссии" --desc "Описание"
    python scripts/architecture_new.py -i  # интерактивный режим
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent
ARCH_DIR = PROJECT_ROOT / 'general_docs' / '02_architecture'
INDEX_FILE = ARCH_DIR / '000_architecture.md'
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
    """Получить следующий ID для архитектуры."""
    counters = load_counters()
    counters["architecture"] += 1
    save_counters(counters)
    return f"{counters['architecture']:03d}"


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


def update_index(arch_id, title, filename, description='', discuss_id=''):
    """Обновить индекс архитектуры."""
    today = datetime.now().strftime('%Y-%m-%d')

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Заменить "В настоящее время архитектурные документы отсутствуют." на таблицу
    if 'В настоящее время архитектурные документы отсутствуют.' in content:
        discuss_link = f'[{discuss_id}](../01_discuss/{discuss_id}_*.md)' if discuss_id else '—'
        new_table = f"""| ID | Название | Описание | Статус | Обновлено | Связанные дискуссии | Ресурсы |
|----|----------|----------|--------|-----------|---------------------|---------|
| {arch_id} | [{title}]({filename}) | {description[:50]} | draft | {today} | {discuss_link} | — |"""

        content = content.replace(
            'В настоящее время архитектурные документы отсутствуют.\n\n**Формат таблицы:**\n\n| ID | Название | Описание | Статус | Обновлено | Связанные дискуссии | Ресурсы |\n|----|----------|----------|--------|-----------|---------------------|---------|',
            new_table
        )
        content = content.replace('| - | - | - | - | - | - | - |', '')
    else:
        # Добавить строку в существующую таблицу
        discuss_link = f'[{discuss_id}](../01_discuss/{discuss_id}_*.md)' if discuss_id else '—'
        new_row = f'| {arch_id} | [{title}]({filename}) | {description[:50]} | draft | {today} | {discuss_link} | — |'

        # Найти таблицу и добавить строку
        table_pattern = r'(\| ID \| Название \| Описание \| Статус \| Обновлено \| Связанные дискуссии \| Ресурсы \|\n\|[-|]+\|)'
        if re.search(table_pattern, content):
            content = re.sub(
                table_pattern,
                f'\\1\n{new_row}',
                content
            )

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


def create_architecture(title, discuss_id=None, description=None):
    """Создать новый архитектурный документ."""
    arch_id = get_next_id()
    slug = slugify(title)
    filename = f"{arch_id}_{slug}.md"
    filepath = ARCH_DIR / filename

    today = datetime.now().strftime('%Y-%m-%d')
    desc = description or title[:50]

    # Связь с дискуссией
    discuss_link = f'[{discuss_id}_*](../01_discuss/{discuss_id}_*.md)' if discuss_id else '[Нет связанной дискуссии]'

    content = f"""# {arch_id}_{slug}

<!-- [📖 Архитектура](../glossary.md#архитектура) -->

**Статус:** 🟡 draft
**Версия:** 1.0
**Дата:** {today}

<!--
WORKFLOW СТАТУСОВ АРХИТЕКТУРЫ:

🟡 draft        — документ создан, структура не заполнена
🔵 in_progress  — активная работа над архитектурой
🟠 feedback     — обратная связь от ресурсов/планов
🟣 review       — ревью архитектуры
🟢 approved     — одобрена, готова к реализации
⚪ final        — реализована, документация завершена

Переходы:
draft → in_progress (после заполнения основных секций)
in_progress → review (архитектура готова к ревью)
review → approved (ревью пройдено)
approved → final (созданы ресурсы и план реализации)
-->

## Оглавление

- [Цель и контекст](#цель-и-контекст)
- [Связанные документы](#связанные-документы)
- [Принципы и ограничения](#принципы-и-ограничения)
- [Компоненты](#компоненты)
- [Диаграммы](#диаграммы)
- [Интерфейсы и контракты](#интерфейсы-и-контракты)
- [Данные](#данные)
- [Внешние зависимости](#внешние-зависимости)
- [Требования к качеству](#требования-к-качеству)
- [Риски и компромиссы](#риски-и-компромиссы)
- [История изменений](#история-изменений)

## Цель и контекст

**Назначение:** {desc}

**Какую проблему решает:**
[Описание проблемы из связанной дискуссии]

## Связанные документы

- **Дискуссия:** {discuss_link}
- **Ресурсы:** [Будут созданы после approve]
- **План реализации:** [Будет создан после approve]

## Принципы и ограничения

**Принципы:**
- [Принцип 1]
- [Принцип 2]

**Ограничения:**
- [Ограничение 1]
- [Ограничение 2]

## Компоненты

| Компонент | Назначение | Технологии |
|-----------|------------|------------|
| [Компонент 1] | [Описание] | [Стек] |
| [Компонент 2] | [Описание] | [Стек] |

## Диаграммы

<!-- Mermaid или ссылка на 03_diagrams/{arch_id}_[название]/ -->

```mermaid
graph TD
    A[Компонент A] --> B[Компонент B]
    B --> C[Компонент C]
```

## Интерфейсы и контракты

### API

| Endpoint | Метод | Описание |
|----------|-------|----------|
| /api/v1/... | GET | [Описание] |

### Форматы данных

```json
{{
  "field": "type"
}}
```

## Данные

- **Модели:** [Описание основных сущностей]
- **Хранение:** [Где и как хранятся данные]
- **Миграции:** [Стратегия миграций]

## Внешние зависимости

| Зависимость | Версия | Назначение | Лицензия |
|-------------|--------|------------|----------|
| [Библиотека] | [x.y.z] | [Для чего] | [MIT/Apache/etc] |

## Требования к качеству

- **Доступность:** [SLA, uptime]
- **Производительность:** [Latency, throughput]
- **Безопасность:** [Требования]
- **Масштабируемость:** [Горизонтальная/вертикальная]

## Риски и компромиссы

| Риск | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|
| [Риск 1] | Высокая/Средняя/Низкая | [Описание] | [Действия] |

## История изменений

| Версия | Дата | Описание | Связанный документ |
|--------|------|----------|-------------------|
| 1.0 | {today} | Первоначальное создание | {discuss_link} |
"""

    # Сохраняем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Обновляем индекс
    update_index(arch_id, title, filename, desc, discuss_id)

    print(f"[OK] Arhitektura sozdana: {arch_id}")
    print(f"  Fayl: general_docs/02_architecture/{filename}")
    print(f"  Nazvanie: {title}")
    print(f"  Opisanie: {desc}")
    print(f"  Diskussiya: {discuss_id or 'ne ukazana'}")
    print(f"  Status: draft")
    print()
    print("Next steps:")
    print(f"  1. Fill architecture sections")
    print(f"  2. Change status to in_progress")
    print(f"  3. Run /doc-review for validation")

    return arch_id, filename


def interactive_mode():
    """Интерактивный режим создания архитектуры."""
    print("=== Создание архитектурного документа ===\n")

    title = input("Название компонента: ").strip()
    if not title:
        print("Ошибка: название обязательно")
        return

    description = input("Краткое описание (Enter - использовать название): ").strip()
    if not description:
        description = title[:50]

    discuss_id = input("ID связанной дискуссии (Enter - пропустить, формат: 001): ").strip()
    if not discuss_id:
        discuss_id = None

    print()
    create_architecture(title, discuss_id, description)


def main():
    parser = argparse.ArgumentParser(description='Создать архитектурный документ')
    parser.add_argument('title', nargs='?', help='Название компонента')
    parser.add_argument('-t', '--title', dest='title_opt', help='Название (альтернатива positional)')
    parser.add_argument('-d', '--discuss', help='ID связанной дискуссии (например: 001)')
    parser.add_argument('--desc', '--description', dest='description', help='Краткое описание')
    parser.add_argument('-i', '--interactive', action='store_true', help='Интерактивный режим')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.title or args.title_opt:
        title = args.title or args.title_opt
        create_architecture(title, args.discuss, args.description)
    else:
        parser.print_help()
        print("\nПримеры:")
        print('  python scripts/architecture_new.py "UI Styleguide"')
        print('  python scripts/architecture_new.py -t "Auth Service" -d "001" --desc "Сервис аутентификации"')
        print('  python scripts/architecture_new.py -i  # интерактивный режим')


if __name__ == '__main__':
    main()
