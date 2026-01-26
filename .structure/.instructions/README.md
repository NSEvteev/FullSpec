---
description: Индекс инструкций для SSOT структуры проекта
standard: .structure/.instructions/standard-readme.md
index: .structure/.instructions/README.md
---

# Инструкции /.structure/

Индекс инструкций для SSOT структуры проекта.

**Полезные ссылки:**
- [SSOT структуры проекта](../README.md)

**Содержание:** формат описания папок, воркфлоу создания/удаления/обновления, валидация, ссылки.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарт README](#1-стандарт-readme) | [standard-readme.md](./standard-readme.md) | Формат и шаблон README |
| [2. Создание папки](#2-создание-папки) | [workflow-create.md](./workflow-create.md) | Воркфлоу создания новой папки |
| [3. Удаление папки](#3-удаление-папки) | [workflow-delete.md](./workflow-delete.md) | Воркфлоу удаления папки |
| [4. Обновление папки](#4-обновление-папки) | [workflow-update.md](./workflow-update.md) | Переименование и перемещение |
| [5. Валидация](#5-валидация) | [validation-structure.md](./validation-structure.md) | Проверка согласованности структуры |
| [6. Ссылки](#6-ссылки) | [links/](./links/) | Типы, форматы, валидация ссылок |
| [7. Обязательные обновления](#7-обязательные-обновления) | — | Что обновлять при изменении структуры |
| [8. Шаблоны](#8-шаблоны) | — | Шаблоны для создания README |
| [9. Скиллы](#9-скиллы) | — | Скиллы для этой области |

```
/.structure/.instructions/
├── README.md              # Этот файл (индекс)
├── standard-readme.md     # Стандарт README (формат + шаблон)
├── workflow-create.md     # Воркфлоу создания папки
├── workflow-delete.md     # Воркфлоу удаления папки
├── workflow-update.md     # Воркфлоу обновления папки
├── validation-structure.md # Валидация согласованности
└── links/                 # Работа со ссылками
    ├── README.md          #   Индекс
    ├── types.md           #   Типы ссылок
    ├── format.md          #   Форматы ссылок
    ├── validation.md      #   Валидация ссылок
    └── workflow-update.md #   Обновление ссылок
```

---

# 1. Стандарт README

Формат и шаблон оформления README для папок проекта и папок инструкций.

**Оглавление:**
- [Два типа README](./standard-readme.md#1-два-типа-readme)
- [README папок проекта](./standard-readme.md#2-readme-папок-проекта)
- [README папок инструкций](./standard-readme.md#3-readme-папок-инструкций)
- [Правила контекстных ссылок](./standard-readme.md#4-правила-работы-с-контекстными-ссылками)

**Инструкция:** [standard-readme.md](./standard-readme.md)

---

# 2. Создание папки

Воркфлоу создания новой папки в структуре проекта.

**Оглавление:**
- [Шаги воркфлоу](./workflow-create.md#шаги)
- [Чек-лист](./workflow-create.md#чек-лист)

**Инструкция:** [workflow-create.md](./workflow-create.md)

---

# 3. Удаление папки

Воркфлоу удаления папки из структуры проекта.

**Оглавление:**
- [Шаги воркфлоу](./workflow-delete.md#шаги)
- [Чек-лист](./workflow-delete.md#чек-лист)

**Инструкция:** [workflow-delete.md](./workflow-delete.md)

---

# 4. Обновление папки

Воркфлоу переименования и перемещения папки.

**Оглавление:**
- [Переименование](./workflow-update.md#переименование)
- [Перемещение](./workflow-update.md#перемещение)
- [Чек-лист](./workflow-update.md#чек-лист)

**Инструкция:** [workflow-update.md](./workflow-update.md)

---

# 5. Валидация

Проверка согласованности структуры проекта.

**Оглавление:**
- [Когда валидировать](./validation-structure.md#когда-валидировать)
- [Шаги проверки](./validation-structure.md#шаги)
- [Чек-лист](./validation-structure.md#чек-лист)
- [Типичные ошибки](./validation-structure.md#типичные-ошибки)

**Инструкция:** [validation-structure.md](./validation-structure.md)

---

# 6. Ссылки

Правила работы со ссылками в документах проекта.

**Оглавление:**
- [Типы ссылок](./links/types.md)
- [Форматы](./links/format.md)
- [Валидация](./links/validation.md)
- [Обновление](./links/workflow-update.md)

**Индекс:** [links/README.md](./links/README.md)

---

# 7. Обязательные обновления

> **ПРАВИЛО:** При любом изменении структуры проекта — обновить связанные документы.

| Действие | Что обновить |
|----------|--------------|
| Создание папки | `/.instructions/coverage.md` — добавить в таблицу покрытия |
| Удаление папки | `/.instructions/coverage.md` — удалить из таблицы |
| Добавление `.instructions/` | `/.instructions/structure.md` — добавить в список локальных |

**Связанные документы:**
- [/.instructions/coverage.md](/.instructions/coverage.md) — таблица покрытия инструкциями
- [/.instructions/structure.md](/.instructions/structure.md) — допустимые папки для инструкций

---

# 8. Шаблоны

Шаблоны включены в [standard-readme.md](./standard-readme.md) — формат и шаблон объединены в один файл.

> **Принцип SSOT:** README.md создаётся ВМЕСТЕ с папкой. Папка без README не существует.

---

# 9. Скиллы

**Планируемые скиллы:**

| Скилл | Назначение | Статус |
|-------|------------|--------|
| `/structure-create` | Автоматизация создания папки в SSOT | TODO |
| `/structure-validate` | Проверка согласованности структуры | TODO |
