---
description: Инструкции для SSOT структуры проекта — frontmatter, README, ссылки, создание и модификация папок. Индекс документов и скриптов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: .structure/.instructions/README.md
---

# Инструкции /.structure/

Индекс инструкций для SSOT структуры проекта.

**Полезные ссылки:**
- [SSOT структуры проекта](../README.md)

**Содержание:** стандарты README и frontmatter, воркфлоу создания и изменения, валидация.

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
/.structure/.instructions/
├── .scripts/
│   ├── find-references.py        # Поиск ссылок на папку/файл
│   ├── generate-readme.py        # Генерация шаблона README
│   ├── mark-deleted.py           # Пометка DELETE_ при удалении
│   ├── mirror-instructions.py    # Зеркалирование .instructions
│   ├── pre-commit-structure.py   # Pre-commit хук для структуры
│   ├── ssot.py                   # Управление SSOT (add/rename/delete)
│   ├── sync-readme.py            # Синхронизация README с файловой системой
│   ├── update-skill-refs.py      # Обновление ссылок в скиллах
│   ├── validate.py               # Единая валидация
│   ├── validate-links.py         # Валидация ссылок
│   └── validate-structure.py     # Валидация структуры
├── README.md                     # Этот файл (индекс)
├── create-initialization.md      # Инициализация проекта (Фаза 0)
├── create-structure.md           # Создание папки
├── modify-structure.md           # Изменение папки (rename/move/delete)
├── standard-frontmatter.md       # Стандарт frontmatter
├── standard-links.md             # Стандарт ссылок
├── standard-readme.md            # Стандарт README
├── standard-search.md            # Стандарт поиска по документации
├── validation-links.md           # Валидация ссылок
└── validation-structure.md       # Валидация структуры
```

---

# 1. Стандарты

## 1.1. Стандарт README

Формат и шаблон оформления README для папок проекта и папок инструкций.

**Оглавление:**
- [Определение типа README](./standard-readme.md#1-определение-типа-readme)
- [README папок проекта](./standard-readme.md#2-readme-папок-проекта)
- [README папок инструкций](./standard-readme.md#3-readme-папок-инструкций)
- [Правила контекстных ссылок](./standard-readme.md#4-правила-работы-с-контекстными-ссылками)

**Инструкция:** [standard-readme.md](./standard-readme.md)

## 1.2. Стандарт frontmatter

Формат и правила для frontmatter в Markdown-файлах.

**Оглавление:**
- [Обязательные поля](./standard-frontmatter.md#1-обязательные-поля)
- [Пример](./standard-frontmatter.md#2-пример)

**Инструкция:** [standard-frontmatter.md](./standard-frontmatter.md)

## 1.3. Стандарт ссылок

Типы и форматы ссылок в документах проекта.

**Оглавление:**
- [Типы ссылок](./standard-links.md#1-типы-ссылок)
- [Абсолютные vs относительные](./standard-links.md#2-абсолютные-vs-относительные)
- [Ссылки в SSOT](./standard-links.md#6-ссылки-в-ssot-структуры)

**Инструкция:** [standard-links.md](./standard-links.md)

## 1.4. Стандарт поиска по документации

Единая система поиска: API скриптов, типы сущностей, формат вывода.

**Оглавление:**
- [Типы сущностей](./standard-search.md#2-типы-сущностей)
- [API конвенция](./standard-search.md#3-api-конвенция)
- [Скрипты поиска](./standard-search.md#4-скрипты-поиска)

**Инструкция:** [standard-search.md](./standard-search.md)

---

# 2. Воркфлоу

## 2.1. Создание папки

Воркфлоу создания новой папки в структуре проекта.

> **Принцип:** README.md создаётся ВМЕСТЕ с папкой. Папка без README не существует.

**Оглавление:**
- [Шаги воркфлоу](./create-structure.md#шаги)
- [Чек-лист](./create-structure.md#чек-лист)
- [Скрипты](./create-structure.md#скрипты)

**Инструкция:** [create-structure.md](./create-structure.md)

## 2.2. Изменение папки

Воркфлоу переименования, перемещения и удаления папки.

**Оглавление:**
- [Переименование](./modify-structure.md#переименование)
- [Перемещение](./modify-structure.md#перемещение)
- [Деактивация](./modify-structure.md#деактивация)
- [Чек-лист](./modify-structure.md#чек-лист)

**Инструкция:** [modify-structure.md](./modify-structure.md)

## 2.3. Инициализация проекта

Оркестрация Фазы 0: GitHub Labels, Security, docs/, pre-commit, customization, отчёт. 10 шагов Check → Act → Status.

**Оглавление:**
- [Принципы](./create-initialization.md#принципы)
- [Шаги 1–10](./create-initialization.md#шаги)
- [Режимы запуска](./create-initialization.md#режимы-запуска)
- [Чек-лист](./create-initialization.md#чек-лист)

**Инструкция:** [create-initialization.md](./create-initialization.md)

---

# 3. Валидация

## 3.1. Валидация структуры

Проверка согласованности SSOT структуры проекта.

**Оглавление:**
- [Когда валидировать](./validation-structure.md#когда-валидировать)
- [Шаги проверки](./validation-structure.md#шаги)
- [Чек-лист](./validation-structure.md#чек-лист)
- [Типичные ошибки](./validation-structure.md#типичные-ошибки)

**Инструкция:** [validation-structure.md](./validation-structure.md)

## 3.2. Валидация ссылок

Проверка корректности ссылок в markdown-документах.

**Оглавление:**
- [Когда валидировать](./validation-links.md#когда-валидировать)
- [Что проверяется](./validation-links.md#что-проверяется)
- [Шаги валидации](./validation-links.md#шаги-валидации)
- [Типичные ошибки](./validation-links.md#типичные-ошибки)

**Инструкция:** [validation-links.md](./validation-links.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [find-references.py](./.scripts/find-references.py) | Поиск ссылок на папку/файл | [modify-structure.md](./modify-structure.md) |
| [generate-readme.py](./.scripts/generate-readme.py) | Генерация шаблона README | [create-structure.md](./create-structure.md) |
| [mark-deleted.py](./.scripts/mark-deleted.py) | Пометка DELETE_ при удалении | [modify-structure.md](./modify-structure.md) |
| [mirror-instructions.py](./.scripts/mirror-instructions.py) | Зеркалирование `.instructions` | [create-structure.md](./create-structure.md), [modify-structure.md](./modify-structure.md) |
| [ssot.py](./.scripts/ssot.py) | Управление SSOT (add/rename/delete) | [create-structure.md](./create-structure.md), [modify-structure.md](./modify-structure.md) |
| [update-skill-refs.py](./.scripts/update-skill-refs.py) | Обновление ссылок в скиллах | [modify-structure.md](./modify-structure.md), [validation-links.md](./validation-links.md) |
| [validate.py](./.scripts/validate.py) | Единая валидация | [validation-structure.md](./validation-structure.md), [validation-links.md](./validation-links.md) |
| [validate-links.py](./.scripts/validate-links.py) | Валидация ссылок | [validation-links.md](./validation-links.md) |
| [validate-structure.py](./.scripts/validate-structure.py) | Валидация структуры | [validation-structure.md](./validation-structure.md) |

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Валидация ссылок | [validation-links.md](./validation-links.md) |
| [/structure-create](/.claude/skills/structure-create/SKILL.md) | Создание папки | [create-structure.md](./create-structure.md) |
| [/structure-modify](/.claude/skills/structure-modify/SKILL.md) | Изменение папки | [modify-structure.md](./modify-structure.md) |
| [/structure-validate](/.claude/skills/structure-validate/SKILL.md) | Валидация структуры | [validation-structure.md](./validation-structure.md) |

