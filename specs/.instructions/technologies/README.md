---
description: Инструкции для технологического реестра — мета-стандарт технологий, per-tech стандарты кодирования, валидация.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: specs/.instructions/technologies/README.md
---

# Инструкции /specs/technologies/

Инструкции для технологического реестра `/specs/technologies/` и per-tech стандартов кодирования.

**Полезные ссылки:**
- [Инструкции specs/](../README.md)
- [Технологический реестр](/specs/technologies/README.md)

**Содержание:** мета-стандарт технологий, per-tech стандарты (standard-{tech}.md + validation-{tech}.md).

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
/specs/.instructions/technologies/
├── standard-technology.md       # Мета-стандарт технологий
├── validation-technology.md     # Валидация per-tech стандартов
├── create-technology.md         # Создание per-tech стандарта
├── modify-technology.md         # Изменение per-tech стандарта
└── README.md                    # Этот файл (индекс)
```

---

# 1. Стандарты

## 1.1. Мета-стандарт технологий

Как создавать per-tech стандарты кодирования (standard-{tech}.md + validation-{tech}.md). Двухфазная модель: заглушка при Design → WAITING, заполнение при ADR → DONE.

**Оглавление:**
- [Расположение и именование](./standard-technology.md#2-расположение-и-именование)
- [Триггер создания (двухфазная модель)](./standard-technology.md#4-триггер-создания)
- [Когда НЕ создавать](./standard-technology.md#41-когда-не-создавать-per-tech-стандарт)
- [Секции per-tech стандарта](./standard-technology.md#5-секции-per-tech-стандарта)
- [Автозагрузка через rules](./standard-technology.md#6-автозагрузка-через-rules)
- [Шаблоны (включая заглушки)](./standard-technology.md#7-шаблоны)

**Инструкция:** [standard-technology.md](./standard-technology.md)

---

# 2. Воркфлоу

## 2.1. Создание per-tech стандарта

Двухфазное создание: заглушка (Design → WAITING) + заполнение конвенциями (ADR → DONE).

**Оглавление:**
- [Фаза 1: Заглушка](./create-technology.md#фаза-1-заглушка-design--waiting)
- [Фаза 2: Заполнение](./create-technology.md#фаза-2-заполнение-adr--done)

**Инструкция:** [create-technology.md](./create-technology.md)

## 2.2. Изменение per-tech стандарта

Обновление сервисов, заполнение заглушки, обновление конвенций, откат, деактивация.

**Оглавление:**
- [Типы изменений](./modify-technology.md#типы-изменений)
- [Откат (ROLLING_BACK)](./modify-technology.md#сценарий-d-откат-rolling_back)

**Инструкция:** [modify-technology.md](./modify-technology.md)

---

# 3. Валидация

## 3.1. Валидация per-tech стандарта

Проверка frontmatter, секций, rule, реестра, режима заглушки.

**Оглавление:**
- [Коды ошибок TECH001-TECH011](./validation-technology.md#типичные-ошибки)
- [Режим заглушки](./validation-technology.md#режим-заглушки-если-секции-2-6-содержат-placeholder)

**Инструкция:** [validation-technology.md](./validation-technology.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-technology.py](../../.scripts/validate-technology.py) | Валидация per-tech стандартов | [validation-technology.md](./validation-technology.md) |

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/technology-create](/.claude/skills/technology-create/SKILL.md) | Создание per-tech стандарта | [create-technology.md](./create-technology.md) |
| [/technology-modify](/.claude/skills/technology-modify/SKILL.md) | Изменение per-tech стандарта | [modify-technology.md](./modify-technology.md) |
| [/technology-validate](/.claude/skills/technology-validate/SKILL.md) | Валидация per-tech стандарта | [validation-technology.md](./validation-technology.md) |
