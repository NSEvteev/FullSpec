---
description: Инструкции для каскадных миграций при обновлении стандартов — создание, валидация. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: .instructions/migration/README.md
---

# Инструкции /.instructions/migration/

Инструкции для процесса миграции стандартов.

**Полезные ссылки:**
- [Инструкции .instructions](../README.md)
- [SSOT проекта](../../.structure/README.md)

**Содержание:** стандарт миграции, валидация, воркфлоу.

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
/.instructions/migration/
├── README.md                 # Этот файл (индекс)
├── create-migration.md       # Воркфлоу миграции
├── standard-migration.md     # Стандарт миграции
└── validation-migration.md   # Валидация миграции
```

---

# 1. Стандарты

## 1.1. Стандарт миграции

Процесс обновления зависимых файлов при изменении стандартов.

**Оглавление:**
- [Принципы](./standard-migration.md#принципы)
- [Что такое миграция](./standard-migration.md#1-что-такое-миграция)
- [Два уровня обновления](./standard-migration.md#2-два-уровня-обновления)
- [Порядок миграции](./standard-migration.md#3-порядок-миграции)
- [Формат отчёта](./standard-migration.md#4-формат-отчёта-о-миграции)

**Инструкция:** [standard-migration.md](./standard-migration.md)

---

# 2. Воркфлоу

## 2.1. Воркфлоу миграции

Процесс выполнения миграции при обновлении стандарта.

**Оглавление:**
- [Принципы](./create-migration.md#принципы)
- [Шаги](./create-migration.md#шаги)
- [Чек-лист](./create-migration.md#чек-лист)
- [Примеры](./create-migration.md#примеры)

**Инструкция:** [create-migration.md](./create-migration.md)

---

# 3. Валидация

## 3.1. Валидация миграции

Проверка корректности миграции после обновления стандарта.

**Оглавление:**
- [Когда валидировать](./validation-migration.md#когда-валидировать)
- [Шаги](./validation-migration.md#шаги)
- [Чек-лист](./validation-migration.md#чек-лист)
- [Типичные ошибки](./validation-migration.md#типичные-ошибки)

**Инструкция:** [validation-migration.md](./validation-migration.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [check-version-drift.py](../.scripts/check-version-drift.py) | Проверка расхождений версий | [validation-migration.md](./validation-migration.md) |
| [check-content-drift.py](../.scripts/check-content-drift.py) | Проверка контентного покрытия секций стандарта | [create-migration.md](./create-migration.md), [validation-migration.md](./validation-migration.md) |
| [bump-standard-version.py](../.scripts/bump-standard-version.py) | Увеличение версии стандарта | [create-migration.md](./create-migration.md) |

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/migration-create](/.claude/skills/migration-create/SKILL.md) | Выполнение миграции | [create-migration.md](./create-migration.md) |
| [/migration-validate](/.claude/skills/migration-validate/SKILL.md) | Валидация миграции | [validation-migration.md](./validation-migration.md) |
