---
description: Индекс инструкций для работы с инструкциями проекта
standard: .structure/.instructions/standard-readme.md
index: .instructions/README.md
---

# Инструкции /instructions/

Индекс инструкций для работы с инструкциями проекта.

**Содержание:** структура папок, типы инструкций, валидация, статусы, жизненный цикл, паттерны поиска.

**Полезные ссылки:**
- [Структура проекта](/.structure/README.md)

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Расположение](#1-расположение) | [structure.md](./structure.md) | Где хранить инструкции |
| [2. Типы](#2-типы) | [types.md](./types.md) | standard vs project |
| [3. Валидация](#3-валидация) | [validation.md](./validation.md) | Формат файлов и frontmatter |
| [4. Статусы](#4-статусы) | [statuses.md](./statuses.md) | Система статусов в README.md |
| [5. Жизненный цикл](#5-жизненный-цикл) | [workflow.md](./workflow.md) | CREATE, UPDATE, DEACTIVATE |
| — | [workflow-create.md](./workflow-create.md) | Детальный воркфлоу CREATE |
| — | [workflow-update.md](./workflow-update.md) | Детальный воркфлоу UPDATE |
| — | [workflow-deactivate.md](./workflow-deactivate.md) | Детальный воркфлоу DEACTIVATE |
| [6. Паттерны](#6-паттерны) | [patterns.md](./patterns.md) | Поиск ссылок на инструкции |
| [7. Примеры](#7-примеры) | [examples.md](./examples.md) | Правила создания examples.md |
| [8. Ответственность](#8-ответственность) | — | IN и границы папок |
| [9. Шаблоны](#9-шаблоны) | — | Шаблоны для инструкций |
| [10. Скиллы](#10-скиллы) | — | Скиллы для инструкций |
| [11. Скрипты](#11-скрипты) | — | Скрипты автоматизации |

```
/.instructions/
├── README.md               # Этот файл (индекс)
├── structure.md            # Расположение инструкций
├── types.md                # Типы (standard/project)
├── validation.md           # Валидация файлов
├── statuses.md             # Статусы в README.md
├── workflow.md             # Жизненный цикл (обзор)
├── workflow-create.md      # Детальный воркфлоу CREATE
├── workflow-update.md      # Детальный воркфлоу UPDATE
├── workflow-deactivate.md  # Детальный воркфлоу DEACTIVATE
├── patterns.md             # Паттерны поиска
├── examples.md             # Правила создания примеров
└── standard-instruction.md # Стандарт формата инструкций
```

---

# 1. Расположение

Расположение и структура папок инструкций.

**Оглавление:**
- [Базовая папка](./structure.md#базовая-папка)
- [Зеркалирование структуры](./structure.md#зеркалирование-структуры)
- [Допустимые папки](./structure.md#допустимые-папки)
- [Примеры](./structure.md#примеры)
- [Скиллы](./structure.md#скиллы)

**Инструкция:** [structure.md](./structure.md)

---

# 2. Типы

Типы инструкций (standard/project).

**Оглавление:**
- [Обзор типов](./types.md#обзор-типов)
- [standard — стандарты](./types.md#standard--стандарты)
- [project — специфика проекта](./types.md#project--специфика-проекта)
- [Как определить тип](./types.md#как-определить-тип)
- [Примеры](./types.md#примеры)
- [Скиллы](./types.md#скиллы)

**Инструкция:** [types.md](./types.md)

---

# 3. Валидация

Валидация путей и формата файлов инструкций.

**Оглавление:**
- [Формат названия](./validation.md#формат-названия)
- [Обязательные секции](./validation.md#обязательные-секции)
- [Навигационные ссылки](./validation.md#навигационные-ссылки)
- [Frontmatter](./validation.md#frontmatter)
- [standard](./validation.md#standard)
- [Скрипт валидации](./validation.md#скрипт-валидации)
- [Ошибки валидации](./validation.md#ошибки-валидации)
- [Скиллы](./validation.md#скиллы)
- [Связанные инструкции](./validation.md#связанные-инструкции)

**Инструкция:** [validation.md](./validation.md)

---

# 4. Статусы

Система статусов инструкций в README.md.

**Оглавление:**
- [Столбцы таблицы](./statuses.md#столбцы-таблицы)
- [Значения статусов](./statuses.md#значения-статусов)
- [Жизненный цикл статусов](./statuses.md#жизненный-цикл-статусов)
- [Примеры](./statuses.md#примеры)
- [Скиллы](./statuses.md#скиллы)

**Инструкция:** [statuses.md](./statuses.md)

---

# 5. Жизненный цикл

Жизненный цикл инструкций: CREATE, UPDATE, DEACTIVATE, MIGRATE.

**Оглавление:**
- [Диаграмма](./workflow.md#диаграмма)
- [Синхронизация README](./workflow.md#синхронизация-readme)
- [Фаза CREATE](./workflow.md#фаза-create)
- [Фаза UPDATE](./workflow.md#фаза-update)
- [Фаза DEACTIVATE](./workflow.md#фаза-deactivate)
- [Фаза MIGRATE](./workflow.md#фаза-migrate)
- [Граф зависимостей](./workflow.md#граф-зависимостей)
- [Скиллы](./workflow.md#скиллы)

**Инструкция:** [workflow.md](./workflow.md)

**Детальные воркфлоу:**
- [workflow-create.md](./workflow-create.md) — 15 шагов создания
- [workflow-update.md](./workflow-update.md) — 12 шагов обновления
- [workflow-deactivate.md](./workflow-deactivate.md) — 10 шагов деактивации

---

# 6. Паттерны

Паттерны поиска ссылок на инструкции.

**Оглавление:**
- [Где искать](./patterns.md#где-искать)
- [Типы ссылок](./patterns.md#типы-ссылок)
- [Действия при обнаружении](./patterns.md#действия-при-обнаружении)
- [Примеры](./patterns.md#примеры)
- [Скиллы](./patterns.md#скиллы)

**Инструкция:** [patterns.md](./patterns.md)

---

# 7. Примеры

Правила создания файлов examples.md в папках инструкций.

**Оглавление:**
- [Назначение](./examples.md#назначение)
- [Правила создания](./examples.md#правила-создания)
- [Структура файла](./examples.md#структура-файла)
- [Папки без скиллов](./examples.md#папки-без-скиллов)

**Инструкция:** [examples.md](./examples.md)

---

# 8. Ответственность

IN и границы для всех папок проекта.

**SSOT:** [/.structure/README.md](/.structure/README.md) — описание всех папок и их зон ответственности.

---

# 9. Шаблоны

Шаблоны для создания инструкций.

| Шаблон | Назначение |
|--------|------------|
| [instruction.md](/.claude/templates/instructions/instruction.md) | Шаблон инструкции |
| [readme.md](/.claude/templates/instructions/readme.md) | Шаблон README для папки инструкций |

---

# 10. Скиллы

Скиллы для работы с инструкциями.

| Скилл | Назначение |
|-------|------------|
| [/instruction-create](/.claude/skills/instruction-create/SKILL.md) | Создание инструкции |
| [/instruction-update](/.claude/skills/instruction-update/SKILL.md) | Проверка соответствия проекта |
| [/instruction-deactivate](/.claude/skills/instruction-deactivate/SKILL.md) | Деактивация неиспользуемой |

---

# 11. Скрипты

Скрипты автоматизации для инструкций.

| Скрипт | Назначение |
|--------|------------|
| instruction-validate.py | Валидация пути и формата |
| instruction-readme-update.py | Обновление README.md |
