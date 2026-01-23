# Инструкции /docs/

Индекс инструкций для работы с документацией проекта.

**Содержание:** структура `/doc/`, документирование кода, шаблоны, workflow документации.

> **Область ответственности:** `/doc/` — зеркалирование документации кода из `/src/`, `/shared/`, `/platform/`.
> Спецификации (ADR, Plans, Architecture) хранятся в `/specs/` — см. [specs/README.md](../specs/README.md).

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Структура](#1-структура) | [structure.md](./structure.md) | Структура /doc/, документирование кода |
| [2. Правила](#2-правила) | [rules.md](./rules.md) | Маппинг путей, валидация, языки |
| [3. Шаблоны](#3-шаблоны) | [templates.md](./templates.md) | Шаблоны документации |
| [4. Workflow](#4-workflow) | [workflow.md](./workflow.md) | Детальный workflow скиллов docs-* |
| [5. Ошибки](#5-ошибки) | [errors.md](./errors.md) | Обработка ошибок |
| [6. Примеры](#6-примеры) | [examples.md](./examples.md) | Примеры использования |
| [7. Шаблоны файлов](#7-шаблоны-файлов) | — | Шаблоны для документации |
| [8. Скиллы](#8-скиллы) | — | Скиллы docs-* |

```
/.claude/instructions/docs/
├── README.md           # Этот файл (индекс)
├── structure.md        # Структура /doc/, документирование кода
├── rules.md            # Маппинг путей, валидация, языки
├── templates.md        # Шаблоны документации
├── workflow.md         # Детальный workflow скиллов docs-*
├── errors.md           # Обработка ошибок
└── examples.md         # Примеры использования
```

---

# 1. Структура

Структура /doc/, документирование кода, шаблоны, workflow.

**Оглавление:**
- [Принцип зеркалирования](./structure.md#принцип-зеркалирования)
- [Что зеркалируется](./structure.md#что-зеркалируется)
- [Типы документов](./structure.md#типы-документов)
- [Дерево /doc/](./structure.md#дерево-doc)
- [Структура сервиса /src/](./structure.md#2-где-структура-сервиса-src)
- [Документирование кода](./structure.md#3-как-документирование-кода)
- [Workflow документации](./structure.md#4-workflow-документации)

**Инструкция:** [structure.md](./structure.md)

---

# 2. Правила

Правила документации для docs-* скиллов — маппинг путей, валидация, языки.

**Оглавление:**
- [Маппинг путей](./rules.md#маппинг-путей)
- [Валидация путей](./rules.md#валидация-путей)
- [Поддерживаемые языки](./rules.md#поддерживаемые-языки)
- [Шаблон документации](./rules.md#шаблон-документации)
- [Формат пометки (docs-delete)](./rules.md#формат-пометки-doc-delete)

**Инструкция:** [rules.md](./rules.md)

---

# 3. Шаблоны

Шаблоны документации для различных типов файлов.

**Оглавление:**
- [Файлы шаблонов](./templates.md#файлы-шаблонов)
- [Выбор шаблона](./templates.md#выбор-шаблона)

**Инструкция:** [templates.md](./templates.md)

---

# 4. Workflow

Детальный workflow скиллов docs-* — режимы, шаги, цепочки вызовов.

**Оглавление:**
- [docs-create](./workflow.md#docs-create)
- [docs-update](./workflow.md#docs-update)
- [docs-delete](./workflow.md#docs-delete)
- [docs-reindex](./workflow.md#docs-reindex)
- [Цепочки вызовов](./workflow.md#цепочки-вызовов)

**Инструкция:** [workflow.md](./workflow.md)

---

# 5. Ошибки

Обработка ошибок при работе с документацией.

**Оглавление:**
- [Ошибки валидации](./errors.md#ошибки-валидации)
- [Ошибки файловой системы](./errors.md#ошибки-файловой-системы)
- [Ошибки шаблонов](./errors.md#ошибки-шаблонов)
- [Ошибки анализа кода](./errors.md#ошибки-анализа-кода)
- [Ошибки цепочек](./errors.md#ошибки-цепочек)
- [Откат изменений](./errors.md#откат-изменений)

**Инструкция:** [errors.md](./errors.md)

---

# 6. Примеры

Примеры работы с документацией — создание, обновление, удаление.

**Оглавление:**
- [Создание документации](./examples.md#создание-документации)
- [Обновление документации](./examples.md#обновление-документации)
- [Удаление документации](./examples.md#удаление-документации)
- [Переиндексация](./examples.md#переиндексация)
- [Сложные сценарии](./examples.md#сложные-сценарии)

**Инструкция:** [examples.md](./examples.md)

---

# 7. Шаблоны файлов

Шаблоны для создания документации.

| Шаблон | Назначение |
|--------|------------|
| [backend-template.md](/.claude/templates/docs/backend-template.md) | handlers, services, controllers |
| [database-template.md](/.claude/templates/docs/database-template.md) | schema, migrations |
| [frontend-template.md](/.claude/templates/docs/frontend-template.md) | components, pages |
| [minimal-template.md](/.claude/templates/docs/minimal-template.md) | утилиты, константы |

---

# 8. Скиллы

Скиллы для работы с документацией.

| Скилл | Назначение |
|-------|------------|
| [/docs-create](/.claude/skills/docs-create/SKILL.md) | Создание документации для нового файла |
| [/docs-update](/.claude/skills/docs-update/SKILL.md) | Обновление документации при изменении кода |
| [/docs-delete](/.claude/skills/docs-delete/SKILL.md) | Пометка документации при удалении файла |
| [/docs-reindex](/.claude/skills/docs-reindex/SKILL.md) | Полная переиндексация документации |

---

# 9. Скрипты

**Скрипты для этой области отсутствуют.**

---

## Связанные инструкции

- [specs/README.md](../specs/README.md) — спецификации (ADR, Plans, Architecture)
- [instructions/instructions/](../instructions/) — правила для инструкций
- [git/issues.md](../git/issues.md) — создание Issue при удалении документации
- [shared/scope.md](../shared/scope.md) — определение scope (claude/project)
