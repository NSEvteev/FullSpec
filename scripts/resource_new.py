#!/usr/bin/env python3
"""
Скрипт создания нового ресурса с автоинкрементом ID.

Использование:
    python scripts/resource_new.py "Название ресурса" -t backend
    python scripts/resource_new.py -n "Users API" -t backend -a "DEC-001"
    python scripts/resource_new.py -i  # интерактивный режим
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent
RESOURCES_DIR = PROJECT_ROOT / 'general_docs' / '05_resources'
COUNTER_FILE = PROJECT_ROOT / 'general_docs' / '.doc_counter'

# Допустимые типы ресурсов
VALID_TYPES = ['database', 'backend', 'frontend', 'infra']

# Соответствие типа и области
TYPE_TO_DOMAIN = {
    'database': 'Database',
    'backend': 'Backend/API',
    'frontend': 'UI/Frontend',
    'infra': 'Infrastructure'
}


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
    """Получить следующий ID для ресурса."""
    counters = load_counters()
    counters["resources"] += 1
    save_counters(counters)
    return f"{counters['resources']:03d}"


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


def update_index(res_id, title, filename, res_type, description='', adr_id=''):
    """Обновить индекс ресурсов в подпапке."""
    index_file = RESOURCES_DIR / res_type / f'000_{res_type}.md'

    if not index_file.exists():
        print(f"[WARN] Index file not found: {index_file}")
        return

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Формируем ссылки
    adr_link = f'[{adr_id}](../../04_decisions/{adr_id}_*.md)' if adr_id else '—'
    desc = description[:30] if description else title[:30]

    # Проверяем, есть ли заглушка
    if '| - | - | - | - |' in content:
        # Заменяем заглушку на реальную строку
        new_row = f'| [{title}]({filename}) | {desc} | {res_type} | {adr_link} |'
        content = content.replace('| - | - | - | - |', new_row)
    else:
        # Добавить строку в существующую таблицу
        new_row = f'| [{title}]({filename}) | {desc} | {res_type} | {adr_link} |'

        table_pattern = r'(\| Название \| Описание \| Тип \| Связанная архитектура \|\n\|[-|]+\|)'
        if re.search(table_pattern, content):
            content = re.sub(
                table_pattern,
                f'\\1\n{new_row}',
                content
            )

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)


def get_type_specific_content(res_type):
    """Получить контент, специфичный для типа ресурса."""
    if res_type == 'database':
        return """
## Схема данных

| Таблица | Описание | Связи |
|---------|----------|-------|
| [Название] | [Описание] | [FK → таблица] |

## Индексы

| Таблица | Индекс | Поля | Тип |
|---------|--------|------|-----|
| [Таблица] | [idx_name] | [field1, field2] | BTREE |

## Миграции

[Стратегия управления изменениями схемы]
"""
    elif res_type == 'backend':
        return """
## API Endpoints

| Endpoint | Метод | Описание | Авторизация |
|----------|-------|----------|-------------|
| /api/v1/... | GET | [Описание] | required/optional |

## Бизнес-логика

[Описание ключевых алгоритмов]

## Конфигурация

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| [VAR_NAME] | [Описание] | [default] |
"""
    elif res_type == 'frontend':
        return """
## Компоненты

| Компонент | Props | Описание |
|-----------|-------|----------|
| [Название] | [props] | [Описание] |

## Состояние

[Описание управления состоянием]

## Маршруты

| Путь | Компонент | Описание |
|------|-----------|----------|
| /path | [Component] | [Описание] |
"""
    elif res_type == 'infra':
        return """
## Сервисы

| Сервис | Образ | Порты | Зависимости |
|--------|-------|-------|-------------|
| [Название] | [image:tag] | [ports] | [deps] |

## Мониторинг

[Метрики, логи, алерты]

## Масштабирование

[Auto-scaling правила]
"""
    return ""


def create_resource(title, res_type, adr_id=None, description=None):
    """Создать новый ресурс."""
    if res_type not in VALID_TYPES:
        print(f"[ERROR] Nevernyi tip resursa: {res_type}")
        print(f"Dopustimye tipy: {', '.join(VALID_TYPES)}")
        return None, None

    res_id = get_next_id()
    slug = slugify(title)
    filename = f"{res_id}_{slug}.md"
    type_dir = RESOURCES_DIR / res_type
    filepath = type_dir / filename

    # Убедимся, что директория существует
    type_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime('%Y-%m-%d')
    desc = description or title[:50]
    domain = TYPE_TO_DOMAIN.get(res_type, res_type)

    # Связь с ADR
    adr_link = f'[{adr_id}](../../04_decisions/{adr_id}_*.md)' if adr_id else '[Нет связанного ADR]'

    # Получаем контент, специфичный для типа
    type_specific = get_type_specific_content(res_type)

    content = f"""# {title}

<!-- [📖 Ресурс](../../glossary.md#ресурс) -->

**Тип:** {res_type}
**Область:** {domain}
**Дата обновления:** {today}

## Назначение

{desc}

## Связанные документы

- **ADR:** {adr_link} (источник ресурса)
- **План реализации:** [ссылки на 06_imp_plans/]

## Компоненты

| Компонент | Назначение | Расположение |
|-----------|------------|--------------|
| [Название] | [Описание] | [Путь в коде] |

---
{type_specific}
---

**ID:** {res_id}
**Шаблон:** [resource.md](../../../llm_instructions/templates/resource.md)
**Индекс:** [000_{res_type}.md](000_{res_type}.md)
"""

    # Сохраняем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Обновляем индекс
    update_index(res_id, title, filename, res_type, desc, adr_id)

    print(f"[OK] Resurs sozdan: {res_id}")
    print(f"  Fayl: general_docs/05_resources/{res_type}/{filename}")
    print(f"  Nazvanie: {title}")
    print(f"  Tip: {res_type}")
    print(f"  Oblast: {domain}")
    print(f"  ADR: {adr_id or 'ne ukazan'}")
    print()
    print("Next steps:")
    print(f"  1. Fill resource sections")
    print(f"  2. Link to implementation plan")

    return res_id, filename


def interactive_mode():
    """Интерактивный режим создания ресурса."""
    print("=== Создание ресурса ===\n")

    title = input("Название ресурса: ").strip()
    if not title:
        print("Ошибка: название обязательно")
        return

    description = input("Краткое описание (Enter - использовать название): ").strip()
    if not description:
        description = title[:50]

    print("\nДоступные типы ресурсов:")
    for i, t in enumerate(VALID_TYPES, 1):
        print(f"  {i}. {t}")
    type_choice = input("Выберите тип (1-4): ").strip()

    if not type_choice.isdigit() or not (1 <= int(type_choice) <= len(VALID_TYPES)):
        print("Ошибка: неверный тип")
        return

    res_type = VALID_TYPES[int(type_choice) - 1]

    adr_id = input("ID связанного ADR (Enter - пропустить, формат: DEC-001): ").strip()
    if not adr_id:
        adr_id = None

    print()
    create_resource(title, res_type, adr_id, description)


def main():
    parser = argparse.ArgumentParser(description='Создать ресурс')
    parser.add_argument('title', nargs='?', help='Название ресурса')
    parser.add_argument('-n', '--name', dest='name_opt', help='Название (альтернатива positional)')
    parser.add_argument('-t', '--type', required=False, choices=VALID_TYPES,
                        help='Тип ресурса (database/backend/frontend/infra)')
    parser.add_argument('-a', '--adr', help='ID связанного ADR (например: DEC-001)')
    parser.add_argument('--desc', '--description', dest='description', help='Краткое описание')
    parser.add_argument('-i', '--interactive', action='store_true', help='Интерактивный режим')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif (args.title or args.name_opt) and args.type:
        title = args.title or args.name_opt
        create_resource(title, args.type, args.adr, args.description)
    else:
        parser.print_help()
        print("\nПримеры:")
        print('  python scripts/resource_new.py "Users API" -t backend')
        print('  python scripts/resource_new.py -n "Auth DB" -t database -a "DEC-001"')
        print('  python scripts/resource_new.py -i  # интерактивный режим')


if __name__ == '__main__':
    main()
