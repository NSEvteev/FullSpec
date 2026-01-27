---
description: Индекс инструкций для SSOT структуры проекта
standard: .structure/.instructions/standard-readme.md
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
├── README.md                # Этот файл (индекс)
├── standard-frontmatter.md  # Стандарт frontmatter
├── standard-links.md        # Стандарт ссылок
├── standard-readme.md       # Стандарт README
├── validation-links.md      # Валидация ссылок
├── validation-structure.md  # Валидация структуры
├── create-structure.md       # Создание папки
├── modify-structure.md       # Изменение папки (rename/move/delete)
└── .scripts/
    ├── generate-readme.py   # Генерация шаблона README
    └── validate-structure.py # Валидация структуры
```

---

# 1. Стандарты

## 1.1. Стандарт README

Формат и шаблон оформления README для папок проекта и папок инструкций.

**Оглавление:**
- [Два типа README](./standard-readme.md#1-два-типа-readme)
- [README папок проекта](./standard-readme.md#2-readme-папок-проекта)
- [README папок инструкций](./standard-readme.md#3-readme-папок-инструкций)
- [Правила контекстных ссылок](./standard-readme.md#4-правила-работы-с-контекстными-ссылками)

**Инструкция:** [standard-readme.md](./standard-readme.md)

## 1.2. Стандарт frontmatter

Формат и правила для frontmatter в Markdown-файлах.

**Оглавление:**
- [Обязательные поля](./standard-frontmatter.md#обязательные-поля)
- [Правила заполнения](./standard-frontmatter.md#правила-заполнения)

**Инструкция:** [standard-frontmatter.md](./standard-frontmatter.md)

## 1.3. Стандарт ссылок

Типы и форматы ссылок в документах проекта.

**Оглавление:**
- [Типы ссылок](./standard-links.md#1-типы-ссылок)
- [Абсолютные vs относительные](./standard-links.md#2-абсолютные-vs-относительные)
- [Ссылки в SSOT](./standard-links.md#6-ссылки-в-ssot-структуры)

**Инструкция:** [standard-links.md](./standard-links.md)

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
- [Удаление](./modify-structure.md#удаление)
- [Чек-лист](./modify-structure.md#чек-лист)

**Инструкция:** [modify-structure.md](./modify-structure.md)

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
- [Шаги проверки](./validation-links.md#шаги)
- [Типичные ошибки](./validation-links.md#типичные-ошибки)

**Инструкция:** [validation-links.md](./validation-links.md)

---

# 4. Скрипты

| Скрипт | Назначение | Использование |
|--------|------------|---------------|
| [generate-readme.py](./.scripts/generate-readme.py) | Генерация шаблона README | `python .structure/.instructions/.scripts/generate-readme.py <путь>` |
| [validate-structure.py](./.scripts/validate-structure.py) | Валидация структуры | `python .structure/.instructions/.scripts/validate-structure.py` |

**Воркфлоу LLM:**
1. `generate-readme.py <путь>` → получить шаблон с плейсхолдерами
2. Заполнить `{PLACEHOLDER}` реальными значениями
3. Записать через Write tool
4. `validate-structure.py` → проверить согласованность

---

# 5. Скиллы

**Скиллы для этой области отсутствуют.**

---

# 6. Обязательные обновления

> **ПРАВИЛО:** При любом изменении структуры проекта — обновить связанные документы.

| Действие | Что обновить |
|----------|--------------|
| Создание папки | `/.instructions/coverage.md` — добавить в таблицу покрытия |
| Удаление папки | `/.instructions/coverage.md` — удалить из таблицы |
| Добавление `.instructions/` | `/.instructions/structure.md` — добавить в список локальных |

**Связанные документы:**
- [/.instructions/coverage.md](/.instructions/coverage.md) — таблица покрытия инструкциями
- [/.instructions/structure.md](/.instructions/structure.md) — допустимые папки для инструкций
