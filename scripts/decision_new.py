#!/usr/bin/env python3
"""
Скрипт создания нового архитектурного решения (ADR) с автоинкрементом ID.

Использование:
    python scripts/decision_new.py "Название решения"
    python scripts/decision_new.py -t "Название" -a "ID архитектуры" --domain "Backend/API"
    python scripts/decision_new.py -i  # интерактивный режим
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent
DECISIONS_DIR = PROJECT_ROOT / 'general_docs' / '04_decisions'
INDEX_FILE = DECISIONS_DIR / '000_decisions.md'
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
    """Получить следующий ID для решения."""
    counters = load_counters()
    counters["decisions"] += 1
    save_counters(counters)
    return f"DEC-{counters['decisions']:03d}"


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


def update_index(dec_id, title, filename, description='', arch_id='', domain=''):
    """Обновить индекс решений."""
    today = datetime.now().strftime('%Y-%m-%d')

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Формируем ссылки
    arch_link = f'[{arch_id}](../02_architecture/{arch_id}_*.md)' if arch_id else '—'
    desc = description[:50] if description else title[:50]

    # Проверяем, есть ли уже таблица с данными или заглушка
    if 'В настоящее время архитектурные решения отсутствуют.' in content:
        # Заменяем заглушку на таблицу
        new_table = f"""| ID | Название | Описание | Статус | Обновлено | Связанные дискуссии | Архитектура |
|----|----------|----------|--------|-----------|---------------------|-------------|
| {dec_id} | [{title}]({filename}) | {desc} | 🟡 draft | {today} | — | {arch_link} |"""

        content = content.replace(
            'В настоящее время архитектурные решения отсутствуют.\n\n**Формат таблицы:**\n\n| ID | Название | Описание | Статус | Обновлено | Связанные дискуссии | Архитектура |\n|----|----------|----------|--------|-----------|---------------------|-------------|\n| - | - | - | - | - | - | - |',
            new_table
        )
    else:
        # Добавить строку в существующую таблицу
        new_row = f'| {dec_id} | [{title}]({filename}) | {desc} | 🟡 draft | {today} | — | {arch_link} |'

        table_pattern = r'(\| ID \| Название \| Описание \| Статус \| Обновлено \| Связанные дискуссии \| Архитектура \|\n\|[-|]+\|)'
        if re.search(table_pattern, content):
            content = re.sub(
                table_pattern,
                f'\\1\n{new_row}',
                content
            )

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


def create_decision(title, arch_id=None, description=None, domain=None):
    """Создать новое архитектурное решение (ADR)."""
    dec_id = get_next_id()
    slug = slugify(title)
    filename = f"{dec_id}_{slug}.md"
    filepath = DECISIONS_DIR / filename

    today = datetime.now().strftime('%Y-%m-%d')
    desc = description or title[:50]
    domain_str = domain or '[UI/Frontend | Backend/API | Auth/Security | Database | Infrastructure | Architecture]'

    # Связь с архитектурой
    arch_link = f'[{arch_id}_*](../02_architecture/{arch_id}_*.md)' if arch_id else '[Нет связанной архитектуры]'

    content = f"""# {dec_id}_{slug}

<!-- [📖 Decision (ADR)](../glossary.md#decision-adr) -->

**Статус:** 🟡 draft
**Область:** {domain_str}
**Дата:** {today}

<!--
WORKFLOW СТАТУСОВ ADR:

🟡 draft    — документ создан, решение формируется
🟣 review   — на ревью
🟢 approved — одобрено, можно создавать ресурсы и план

Переходы:
draft → review (решение готово к ревью)
review → approved (ревью пройдено)
approved → создаются ресурсы (05_resources/) и план (06_imp_plans/)
-->

**Связанные документы:**
- **Архитектура:** {arch_link}
- **Ресурсы:** [создаются из этого ADR → 05_resources/]
- **План реализации:** [создаётся из этого ADR → 06_imp_plans/]

---

## Решение

**Краткая суть решения (1-2 предложения):**

[Описать, что именно решили]

---

## Контекст

**Проблема, которую решаем:**

[Описать проблему или задачу, для которой принимается решение]

**Требования:**

- [Требование 1]
- [Требование 2]
- [Требование 3]

---

## Обоснование

**Почему выбрали это решение:**

1. [Аргумент 1]
2. [Аргумент 2]
3. [Аргумент 3]

**Преимущества:**

- ✅ [Преимущество 1]
- ✅ [Преимущество 2]
- ✅ [Преимущество 3]

**Недостатки (принимаем осознанно):**

- ⚠️ [Недостаток 1 и как с ним справляемся]
- ⚠️ [Недостаток 2 и как с ним справляемся]

---

## Рассмотренные альтернативы

### Альтернатива 1: [Название]

**Описание:**
[Краткое описание альтернативного подхода]

**Почему отклонено:**
[Причины отказа от этого варианта]

---

### Альтернатива 2: [Название]

**Описание:**
[Краткое описание альтернативного подхода]

**Почему отклонено:**
[Причины отказа от этого варианта]

---

## Последствия

**Что нужно реализовать:**

- [ ] [Задача 1]
- [ ] [Задача 2]
- [ ] [Задача 3]

**Изменения в архитектуре:**

- [Какие компоненты затрагивает]
- [Какие зависимости появляются]
- [Какие интерфейсы меняются]

**Влияние на другие решения:**

- [Связь с DEC-XXX]

**Риски и митигация:**

| Риск | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|
| [Риск 1] | Низкая/Средняя/Высокая | Низкое/Среднее/Высокое | [Как снижаем риск] |

---

## История изменений

| Дата | Версия | Изменения | Автор |
|------|--------|-----------|-------|
| {today} | 1.0 | Создание документа | [Автор] |

---

## Метаданные

**ID:** {dec_id}
**Категория:** {domain_str}
**Приоритет:** [Критичный / Высокий / Средний / Низкий]
**Теги:** #decision #adr

---

## Примечания

[Дополнительная информация, ссылки на источники, best practices]

---

**Шаблон:** [decision_adr.md](../../llm_instructions/templates/decision_adr.md)
**Индекс решений:** [000_decisions.md](000_decisions.md)
"""

    # Сохраняем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Обновляем индекс
    update_index(dec_id, title, filename, desc, arch_id, domain_str)

    print(f"[OK] ADR sozdan: {dec_id}")
    print(f"  Fayl: general_docs/04_decisions/{filename}")
    print(f"  Nazvanie: {title}")
    print(f"  Opisanie: {desc}")
    print(f"  Arhitektura: {arch_id or 'ne ukazana'}")
    print(f"  Oblast: {domain_str}")
    print(f"  Status: draft")
    print()
    print("Next steps:")
    print(f"  1. Fill ADR sections (decision, context, rationale)")
    print(f"  2. Change status to review")
    print(f"  3. After approval -> create resources and imp_plan")

    return dec_id, filename


def interactive_mode():
    """Интерактивный режим создания ADR."""
    print("=== Создание архитектурного решения (ADR) ===\n")

    title = input("Название решения: ").strip()
    if not title:
        print("Ошибка: название обязательно")
        return

    description = input("Краткое описание (Enter - использовать название): ").strip()
    if not description:
        description = title[:50]

    arch_id = input("ID связанной архитектуры (Enter - пропустить, формат: 001): ").strip()
    if not arch_id:
        arch_id = None

    print("\nДоступные домены:")
    for i, d in enumerate(VALID_DOMAINS, 1):
        print(f"  {i}. {d}")
    domain_choice = input("Выберите домен (1-6 или Enter для пропуска): ").strip()

    domain = None
    if domain_choice.isdigit() and 1 <= int(domain_choice) <= len(VALID_DOMAINS):
        domain = VALID_DOMAINS[int(domain_choice) - 1]

    print()
    create_decision(title, arch_id, description, domain)


def main():
    parser = argparse.ArgumentParser(description='Создать архитектурное решение (ADR)')
    parser.add_argument('title', nargs='?', help='Название решения')
    parser.add_argument('-t', '--title', dest='title_opt', help='Название (альтернатива positional)')
    parser.add_argument('-a', '--arch', help='ID связанной архитектуры (например: 001)')
    parser.add_argument('--desc', '--description', dest='description', help='Краткое описание')
    parser.add_argument('--domain', help='Область (UI/Frontend, Backend/API, etc.)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Интерактивный режим')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.title or args.title_opt:
        title = args.title or args.title_opt
        create_decision(title, args.arch, args.description, args.domain)
    else:
        parser.print_help()
        print("\nПримеры:")
        print('  python scripts/decision_new.py "JWT аутентификация"')
        print('  python scripts/decision_new.py -t "Выбор БД" -a "001" --domain "Database"')
        print('  python scripts/decision_new.py -i  # интерактивный режим')


if __name__ == '__main__':
    main()
