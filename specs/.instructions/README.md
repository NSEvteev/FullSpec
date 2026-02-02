---
description: Индекс инструкций для работы с документами спецификаций
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: specs/.instructions/README.md
---

# Инструкции /specs/

Индекс инструкций для работы с документами спецификаций `/specs/`.

**Содержание:** структура /specs/, workflow, статусы, типы документов (Discussion, Impact, ADR, Plan, Architecture, Glossary), правила, именование, связи.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Структура /specs/](#1-структура-specs) | — | Назначение и структура папки |
| [2. Статусы](#2-статусы) | [statuses.md](./statuses.md) | Унифицированная система статусов |
| [3. Workflow](#3-workflow) | [workflow.md](./workflow.md) | Полный workflow от идеи до реализации |
| [4. Discussions](#4-discussions) | [discussions.md](./discussions.md) | Формат и чек-листы для дискуссий |
| [5. Impact](#5-impact) | [impact.md](./impact.md) | Импакт-анализ, связь с ADR |
| [6. ADR](#6-adr) | [adr.md](./adr.md) | Architecture Decision Records |
| [7. Plans](#7-plans) | [plans.md](./plans.md) | Планы реализации, GitHub Issues |
| [8. Architecture](#8-architecture) | [architecture.md](./architecture.md) | Архитектура сервиса (живой документ) |
| [9. Glossary](#9-glossary) | [glossary.md](./glossary.md) | Глоссарий терминов проекта |
| [10. Правила](#10-правила) | [rules.md](./rules.md) | Скиллы, шаблоны, запреты, принятые решения |
| [11. Именование](#11-именование) | [naming.md](./naming.md) | Нумерация, формат названия, сокращённые пути |
| [12. Индексы](#12-индексы) | [indexes.md](./indexes.md) | Форматы таблиц README, workflow обновления |
| [13. Ошибки](#13-ошибки) | [errors.md](./errors.md) | Обработка ошибок, откат |
| [14. Форматы вывода](#14-форматы-вывода) | [output.md](./output.md) | Форматы результатов, диалоги |
| [15. Примеры](#15-примеры) | [examples.md](./examples.md) | Примеры использования скиллов |
| [16. Связи](#16-связи) | [relations.md](./relations.md) | Граф зависимостей, связь /specs/ ↔ /doc/ |
| [17. Шаблоны](#17-шаблоны) | — | Шаблоны документов |
| [18. Скиллы](#18-скиллы) | — | Скиллы для работы с /specs/ |

```
/.claude/.instructions/specs/
├── README.md           # Этот файл (индекс)
├── statuses.md         # Система статусов
├── workflow.md         # Workflow от идеи до реализации
├── discussions.md      # Формат Discussion
├── impact.md           # Формат Impact
├── adr.md              # Формат ADR
├── plans.md            # Формат Plan
├── architecture.md     # Формат Architecture
├── glossary.md         # Формат Glossary
├── rules.md            # Правила, запреты, принятые решения
├── naming.md           # Именование и нумерация
├── indexes.md          # Форматы README-индексов
├── errors.md           # Обработка ошибок
├── output.md           # Форматы вывода
├── examples.md         # Примеры использования
└── relations.md        # Связи между документами
```

---

# 1. Структура /specs/

`/specs/` — единая папка для проектных спецификаций.

```
/specs/
├── discussions/                  # Дискуссии (идеи, исследования)
│   ├── README.md                 # Индекс дискуссий
│   └── 001-{topic}.md
├── impact/                       # Импакт-анализ (какие сервисы затронуты)
│   ├── README.md                 # Индекс импактов
│   └── 001-{topic}.md
├── services/                     # Сервисы
│   └── {service}/
│       ├── README.md             # Описание сервиса
│       ├── architecture.md       # Архитектура сервиса
│       ├── adr/                  # Архитектурные решения
│       │   ├── README.md         # Индекс ADR
│       │   └── 001-{topic}.md
│       └── plans/                # Планы реализации
│           ├── README.md         # Индекс планов
│           └── {topic}-plan.md
└── glossary.md                   # Глоссарий терминов
```

---

# 2. Статусы

Унифицированная система статусов для всех типов документов в `/specs/`.

**Оглавление:**
- [Все статусы](./statuses.md#все-статусы)
- [Схема переходов](./statuses.md#схема-переходов)
- [Статусы по типам документов](./statuses.md#статусы-по-типам-документов)
- [Каскадные проверки](./statuses.md#каскадные-проверки)

**Инструкция:** [statuses.md](./statuses.md)

---

# 3. Workflow

Полный workflow от идеи до реализации: Discussion → Impact → ADR → Plan → Implementation.

**Оглавление:**
- [Обзор workflow](./workflow.md#обзор-workflow)
- [Фазы workflow](./workflow.md#фазы-workflow)
- [Точка синхронизации](./workflow.md#точка-синхронизации)
- [Полная диаграмма](./workflow.md#полная-диаграмма-переходов)

**Инструкция:** [workflow.md](./workflow.md)

---

# 4. Discussions

Точка входа для новых идей и изменений.

**Оглавление:**
- [Расположение](./discussions.md#расположение)
- [Формат документа](./discussions.md#формат-документа)
- [Статусы Discussion](./discussions.md#статусы-discussion)
- [Чек-листы переходов](./discussions.md#чек-листы-переходов)

**Инструкция:** [discussions.md](./discussions.md)

---

# 5. Impact

Импакт-анализ определяет какие сервисы затронуты изменением.

**Оглавление:**
- [Расположение](./impact.md#расположение)
- [Формат документа](./impact.md#формат-документа)
- [Создание нового сервиса](./impact.md#создание-нового-сервиса)
- [Связь Impact и ADR](./impact.md#связь-impact-и-adr)
- [Чек-листы переходов](./impact.md#чек-листы-переходов)

**Инструкция:** [impact.md](./impact.md)

---

# 6. ADR

Architecture Decision Records — фиксация архитектурных решений для конкретного сервиса.

**Оглавление:**
- [Расположение](./adr.md#расположение)
- [Формат документа](./adr.md#формат-документа)
- [Проверка бизнес-логики](./adr.md#проверка-бизнес-логики)
- [Проверка конфликтующих ADR](./adr.md#проверка-конфликтующих-adr)
- [Breaking Changes](./adr.md#breaking-changes)
- [Чек-листы переходов](./adr.md#чек-листы-переходов)

**Инструкция:** [adr.md](./adr.md)

---

# 7. Plans

Декомпозиция ADR на конкретные задачи.

**Оглавление:**
- [Расположение](./plans.md#расположение)
- [Формат документа](./plans.md#формат-документа)
- [Согласование с пользователем](./plans.md#согласование-с-пользователем)
- [Автоматическое создание GitHub Issues](./plans.md#автоматическое-создание-github-issues)
- [Версионирование планов](./plans.md#версионирование-планов)
- [Чек-листы переходов](./plans.md#чек-листы-переходов)

**Инструкция:** [plans.md](./plans.md)

---

# 8. Architecture

Живой документ — описание текущего состояния сервиса.

**Оглавление:**
- [Расположение](./architecture.md#расположение)
- [Формат документа](./architecture.md#формат-документа)
- [Ссылки на ADR](./architecture.md#ссылки-на-adr)
- [Workflow обновления](./architecture.md#workflow-обновления)

**Особенность:** Без статусов. Обновляется автоматически при завершении ADR.

**Инструкция:** [architecture.md](./architecture.md)

---

# 9. Glossary

Единое место для терминов проекта.

**Оглавление:**
- [Расположение](./glossary.md#расположение)
- [Структура термина](./glossary.md#структура-термина)
- [Категории](./glossary.md#категории)
- [Скиллы глоссария](./glossary.md#скиллы)

**Особенность:** Без статусов. Управляется отдельными скиллами `/glossary-*`.

**Инструкция:** [glossary.md](./glossary.md)

---

# 10. Правила

Правила автоматизации и ограничения для работы с `/specs/`.

**Оглавление:**
- [Скиллы автоматизации](./rules.md#скиллы-автоматизации)
- [Шаблоны](./rules.md#шаблоны)
- [Запреты (миграция, удаление, архивирование)](./rules.md#запрет-миграции)
- [Принятые решения](./rules.md#принятые-решения)

**Инструкция:** [rules.md](./rules.md)

---

# 11. Именование

Правила именования файлов в `/specs/`.

**Оглавление:**
- [Формат названия](./naming.md#формат-названия)
- [Нумерация](./naming.md#нумерация)
- [Сокращённые пути](./naming.md#сокращённые-пути)
- [Валидация](./naming.md#валидация)

**Инструкция:** [naming.md](./naming.md)

---

# 12. Индексы

Форматы таблиц в README.md индексах и workflow их обновления.

**Оглавление:**
- [Список индексов](./indexes.md#список-индексов)
- [Формат таблиц](./indexes.md#формат-таблиц)
- [Формат строки](./indexes.md#формат-строки)
- [Workflow обновления](./indexes.md#workflow-обновления)

**Инструкция:** [indexes.md](./indexes.md)

---

# 13. Ошибки

Обработка ошибок и откат при сбоях в скиллах `/spec-*`.

**Оглавление:**
- [spec-create](./errors.md#spec-create)
- [spec-status](./errors.md#spec-status)
- [spec-update](./errors.md#spec-update)
- [specs-health](./errors.md#specs-health)
- [Откат при ошибке](./errors.md#откат-при-ошибке)

**Инструкция:** [errors.md](./errors.md)

---

# 14. Форматы вывода

Форматы результатов выполнения скиллов и диалоги подтверждения.

**Оглавление:**
- [spec-create](./output.md#spec-create)
- [spec-status](./output.md#spec-status)
- [spec-update](./output.md#spec-update)
- [specs-health](./output.md#specs-health)
- [specs-index](./output.md#specs-index)
- [specs-sync](./output.md#specs-sync)
- [Диалоги подтверждения](./output.md#диалоги-подтверждения)

**Инструкция:** [output.md](./output.md)

---

# 15. Примеры

Примеры использования скиллов `/spec-*` и `/specs-*`.

**Оглавление:**
- [spec-create](./examples.md#spec-create)
- [spec-status](./examples.md#spec-status)
- [spec-update](./examples.md#spec-update)
- [specs-health](./examples.md#specs-health)
- [specs-index](./examples.md#specs-index)
- [specs-sync](./examples.md#specs-sync)

**Инструкция:** [examples.md](./examples.md)

---

# 16. Связи

Граф зависимостей документов и разделение ответственности `/specs/` ↔ `/doc/`.

**Оглавление:**
- [Цепочка документов](./relations.md#цепочка-документов)
- [Граф зависимостей](./relations.md#граф-зависимостей)
- [Обязательные ссылки](./relations.md#обязательные-ссылки)
- [Обратные ссылки (Backlinks)](./relations.md#обратные-ссылки-backlinks)
- [Связь /specs/ ↔ /doc/](./relations.md#связь-specs--doc)

**Инструкция:** [relations.md](./relations.md)

---

# 17. Шаблоны

Шаблоны документов для `/specs/`.

| Шаблон | Назначение |
|--------|------------|
| [discussion.md](/.claude/templates/specs/discussion.md) | Дискуссия |
| [impact.md](/.claude/templates/specs/impact.md) | Импакт-анализ |
| [adr.md](/.claude/templates/specs/adr.md) | ADR |
| [plan.md](/.claude/templates/specs/plan.md) | План |
| [architecture.md](/.claude/templates/specs/architecture.md) | Архитектура |

---

# 18. Скиллы

Скиллы для работы с `/specs/`.

| Скилл | Назначение |
|-------|------------|
| [/spec-create](/.claude/skills/spec-create/SKILL.md) | Создание документов |
| [/spec-status](/.claude/skills/spec-status/SKILL.md) | Изменение статуса |
| [/spec-update](/.claude/skills/spec-update/SKILL.md) | Работа с документом |
| [/specs-health](/.claude/skills/specs-health/SKILL.md) | Проверка целостности |
| [/specs-sync](/.claude/skills/specs-sync/SKILL.md) | Синхронизация статусов |
| [/specs-index](/.claude/skills/specs-index/SKILL.md) | Обновление индексов |
