---
description: Индекс инструкций для написания инструкций и скриптов
standard: .structure/.instructions/standard-readme.md
index: .instructions/README.md
---

# Инструкции /.instructions/

Индекс инструкций для написания инструкций и скриптов автоматизации.

**Полезные ссылки:**
- [CLAUDE.md](/CLAUDE.md) — точка входа

**Содержание:** стандарты инструкций и скриптов, воркфлоу создания и изменения, валидация.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/.instructions/
├── README.md                    # Этот файл (индекс)
├── standard-instruction.md      # Стандарт инструкций
├── standard-script.md           # Стандарт скриптов
├── standard-principles.md       # Стандарт принципов программирования
├── create-instruction.md        # Создание инструкции
├── create-script.md             # Создание скрипта
├── modify-instruction.md        # Изменение инструкции
├── modify-script.md             # Изменение скрипта
├── validation-instruction.md    # Валидация инструкций
├── validation-script.md         # Валидация скриптов
├── validation-principles.md     # Валидация принципов
└── .scripts/
    ├── list-instructions.py       # Список инструкций
    ├── create-instruction-file.py # Создание инструкции
    ├── create-script-file.py      # Создание скрипта
    ├── validate-instruction.py    # Валидация инструкций
    ├── validate-script.py         # Валидация скриптов
    ├── parse-docstrings.py        # Поиск скриптов по описанию
    ├── find-references.py         # Поиск ссылок на файл
    └── update-references.py       # Замена ссылок
```

---

# 1. Стандарты

## 1.1. Стандарт инструкций

Формат и правила оформления инструкций в папках `.instructions/`.

**Оглавление:**
- [Формат файла](./standard-instruction.md#4-формат-файла)
- [Frontmatter](./standard-instruction.md#5-frontmatter)
- [Правила именования](./standard-instruction.md#правила-именования-файлов)

**Инструкция:** [standard-instruction.md](./standard-instruction.md)

## 1.2. Стандарт скриптов

Формат и правила оформления Python-скриптов автоматизации.

**Оглавление:**
- [Формат файла](./standard-script.md#3-формат-файла)
- [Docstring](./standard-script.md#4-docstring)
- [Exit codes](./standard-script.md#exit-codes)

**Инструкция:** [standard-script.md](./standard-script.md)

## 1.3. Стандарт принципов программирования

Принципы KISS, DRY, YAGNI, SOLID и другие для скриптов автоматизации.

**Оглавление:**
- [KISS](./standard-principles.md#1-kiss)
- [DRY](./standard-principles.md#2-dry)
- [YAGNI](./standard-principles.md#3-yagni)
- [Обработка ошибок](./standard-principles.md#7-обработка-ошибок)

**Инструкция:** [standard-principles.md](./standard-principles.md)

---

# 2. Воркфлоу

## 2.1. Создание инструкции

Воркфлоу создания новой инструкции.

**Оглавление:**
- [Шаги создания](./create-instruction.md#3-шаги-создания)
- [Чек-лист](./create-instruction.md#5-чек-лист)

**Инструкция:** [create-instruction.md](./create-instruction.md)

## 2.2. Изменение инструкции

Воркфлоу обновления, деактивации и миграции инструкций.

**Оглавление:**
- [Обновление](./modify-instruction.md#1-обновление-инструкции)
- [Деактивация](./modify-instruction.md#2-деактивация-инструкции)
- [Миграция](./modify-instruction.md#3-миграция-инструкции)

**Инструкция:** [modify-instruction.md](./modify-instruction.md)

## 2.3. Создание скрипта

Воркфлоу создания нового скрипта автоматизации.

**Оглавление:**
- [Шаги создания](./create-script.md#3-шаги-создания)
- [Чек-лист](./create-script.md#5-чек-лист)

**Инструкция:** [create-script.md](./create-script.md)

## 2.4. Изменение скрипта

Воркфлоу обновления, рефакторинга и удаления скриптов.

**Оглавление:**
- [Обновление](./modify-script.md#1-обновление-скрипта)
- [Рефакторинг](./modify-script.md#2-рефакторинг-скрипта)
- [Удаление](./modify-script.md#3-удаление-скрипта)

**Инструкция:** [modify-script.md](./modify-script.md)

---

# 3. Валидация

## 3.1. Валидация инструкций

Проверка соответствия инструкций стандарту (коды I001-I031).

**Оглавление:**
- [Когда валидировать](./validation-instruction.md#1-когда-валидировать)
- [Коды ошибок](./validation-instruction.md#3-коды-ошибок)
- [Чек-лист](./validation-instruction.md#5-чек-лист)

**Инструкция:** [validation-instruction.md](./validation-instruction.md)

## 3.2. Валидация скриптов

Проверка соответствия скриптов стандарту (коды S001-S031).

**Оглавление:**
- [Когда валидировать](./validation-script.md#1-когда-валидировать)
- [Коды ошибок](./validation-script.md#3-коды-ошибок)
- [Чек-лист](./validation-script.md#5-чек-лист)

**Инструкция:** [validation-script.md](./validation-script.md)

## 3.3. Валидация принципов

Проверка соблюдения принципов программирования (коды P001-P008).

**Оглавление:**
- [Проверка KISS](./validation-principles.md#шаг-1-проверить-kiss)
- [Проверка DRY](./validation-principles.md#шаг-2-проверить-dry)
- [Проверка зависимостей](./validation-principles.md#шаг-4-проверить-зависимости)

**Инструкция:** [validation-principles.md](./validation-principles.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [list-instructions.py](./.scripts/list-instructions.py) | Список всех инструкций с описаниями | [create-instruction.md](./create-instruction.md) |
| [create-instruction-file.py](./.scripts/create-instruction-file.py) | Создание файла инструкции по шаблону | [create-instruction.md](./create-instruction.md) |
| [create-script-file.py](./.scripts/create-script-file.py) | Создание файла скрипта по шаблону | [create-script.md](./create-script.md) |
| [validate-instruction.py](./.scripts/validate-instruction.py) | Валидация формата инструкций | [validation-instruction.md](./validation-instruction.md) |
| [validate-script.py](./.scripts/validate-script.py) | Валидация формата скриптов | [validation-script.md](./validation-script.md) |
| [parse-docstrings.py](./.scripts/parse-docstrings.py) | Поиск скриптов по описанию | [create-script.md](./create-script.md) |
| [find-references.py](./.scripts/find-references.py) | Поиск всех ссылок на файл | [modify-instruction.md](./modify-instruction.md) |
| [update-references.py](./.scripts/update-references.py) | Замена ссылок (старый → новый путь) | [modify-instruction.md](./modify-instruction.md) |

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/instruction-create](/.claude/skills/instruction-create/SKILL.md) | Создание инструкции | [create-instruction.md](./create-instruction.md) |
| [/instruction-modify](/.claude/skills/instruction-modify/SKILL.md) | Изменение инструкции | [modify-instruction.md](./modify-instruction.md) |
