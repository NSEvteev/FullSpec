---
description: Индекс инструкций для создания и управления rules
standard: .structure/.instructions/standard-readme.md
standard-version: v1.0
index: .claude/.instructions/rules/README.md
---

# Инструкции /.claude/rules/

Индекс инструкций для создания и управления rules.

**Полезные ссылки:**
- [Инструкции .claude/](../README.md)
- [Rules](/.claude/rules/README.md)

**Содержание:** стандарт формата rule, воркфлоу создания и изменения, валидация.

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
/.claude/.instructions/rules/
├── README.md          # Этот файл (индекс)
├── standard-rule.md   # Стандарт формата rule
├── validation-rule.md # Валидация rules
├── create-rule.md     # Создание rule
├── modify-rule.md     # Изменение rule
└── .scripts/
    ├── validate-rule.py # Валидация формата rule
    └── list-rules.py    # Список всех rules
```

---

# 1. Стандарты

## 1.1. Стандарт rule

Формат и правила оформления rule-файлов для автоматической загрузки контекста.

**Оглавление:**
- [Назначение](./standard-rule.md#1-назначение)
- [Расположение](./standard-rule.md#2-расположение)
- [Frontmatter](./standard-rule.md#3-frontmatter)
- [Структура](./standard-rule.md#4-структура)
- [Типы применения](./standard-rule.md#5-типы-применения)
- [Содержимое rule](./standard-rule.md#6-содержимое-rule)
- [Конфликты paths](./standard-rule.md#7-конфликты-paths)
- [Примеры](./standard-rule.md#8-примеры)

**Инструкция:** [standard-rule.md](./standard-rule.md)

---

# 2. Воркфлоу

## 2.1. Создание rule

Воркфлоу создания нового rule-файла.

> **Принцип:** Rule = триггер контекста, не дублировать существующие.

**Оглавление:**
- [Принципы](./create-rule.md#принципы)
- [Шаги воркфлоу](./create-rule.md#шаги)
- [Чек-лист](./create-rule.md#чек-лист)
- [Примеры](./create-rule.md#примеры)

**Инструкция:** [create-rule.md](./create-rule.md)

## 2.2. Изменение rule

Воркфлоу изменения, деактивации и миграции rule-файлов.

**Оглавление:**
- [Типы изменений](./modify-rule.md#типы-изменений)
- [Обновление](./modify-rule.md#обновление)
- [Деактивация](./modify-rule.md#деактивация)
- [Миграция](./modify-rule.md#миграция)
- [Чек-лист](./modify-rule.md#чек-лист)

**Инструкция:** [modify-rule.md](./modify-rule.md)

---

# 3. Валидация

## 3.1. Валидация rule

Проверка формата и структуры rule-файлов.

**Оглавление:**
- [Когда валидировать](./validation-rule.md#когда-валидировать)
- [Шаги валидации](./validation-rule.md#шаги)
- [Чек-лист](./validation-rule.md#чек-лист)
- [Типичные ошибки](./validation-rule.md#типичные-ошибки)

**Инструкция:** [validation-rule.md](./validation-rule.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-rule.py](./.scripts/validate-rule.py) | Валидация формата rule | [validation-rule.md](./validation-rule.md) |
| [list-rules.py](./.scripts/list-rules.py) | Список всех rules с описаниями | [create-rule.md](./create-rule.md) |

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/rule-create](../../skills/rule-create/SKILL.md) | Создание нового rule-файла | [create-rule.md](./create-rule.md) |
| [/rule-modify](../../skills/rule-modify/SKILL.md) | Изменение, деактивация и миграция rule | [modify-rule.md](./modify-rule.md) |
| [/rule-validate](../../skills/rule-validate/SKILL.md) | Валидация формата и структуры rule | [validation-rule.md](./validation-rule.md) |
