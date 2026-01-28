---
description: Индекс инструкций для написания скиллов
standard: .structure/.instructions/standard-readme.md
index: .claude/.instructions/skills/README.md
---

# Инструкции /.claude/.instructions/skills/

Индекс инструкций для написания скиллов Claude Code.

**Полезные ссылки:**
- [Индекс скиллов](/.claude/skills/README.md)
- [CLAUDE.md](/CLAUDE.md) — точка входа

**Содержание:** стандарт скиллов, воркфлоу создания и изменения, валидация.

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
/.claude/.instructions/skills/
├── README.md              # Этот файл (индекс)
├── standard-skill.md      # Стандарт скиллов
├── create-skill.md        # Создание скилла
├── modify-skill.md        # Изменение скилла
└── validation-skill.md    # Валидация скиллов
```

---

# 1. Стандарты

## 1.1. Стандарт скиллов

Формат и структура файлов SKILL.md в сокращённом формате.

**Оглавление:**
- [Назначение](./standard-skill.md#1-назначение)
- [Формат файла](./standard-skill.md#3-формат-файла)
- [Frontmatter](./standard-skill.md#4-frontmatter)
- [Секции документа](./standard-skill.md#5-секции-документа)

**Инструкция:** [standard-skill.md](./standard-skill.md)

---

# 2. Воркфлоу

## 2.1. Создание скилла

Воркфлоу создания нового скилла в сокращённом формате.

**Оглавление:**
- [Когда создавать](./create-skill.md#1-когда-создавать)
- [Шаги создания](./create-skill.md#3-шаги-создания)
- [Чек-лист](./create-skill.md#5-чек-лист)

**Инструкция:** [create-skill.md](./create-skill.md)

## 2.2. Изменение скилла

Воркфлоу обновления, удаления и миграции скиллов.

**Оглавление:**
- [Обновление](./modify-skill.md#1-обновление-скилла)
- [Удаление](./modify-skill.md#2-удаление-скилла)
- [Миграция](./modify-skill.md#3-миграция-скилла)

**Инструкция:** [modify-skill.md](./modify-skill.md)

---

# 3. Валидация

## 3.1. Валидация скиллов

Проверка соответствия скиллов сокращённому формату (коды K001-K031).

**Оглавление:**
- [Когда валидировать](./validation-skill.md#1-когда-валидировать)
- [Коды ошибок](./validation-skill.md#3-коды-ошибок)
- [Чек-лист](./validation-skill.md#5-чек-лист)

**Инструкция:** [validation-skill.md](./validation-skill.md)

---

# 4. Скрипты

*Нет скриптов.*

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/skill-create](/.claude/skills/skill-create/SKILL.md) | Создание нового скилла | [create-skill.md](./create-skill.md) |
| [/skill-update](/.claude/skills/skill-update/SKILL.md) | Обновление связанных скиллов | [modify-skill.md](./modify-skill.md) |
| [/skill-delete](/.claude/skills/skill-delete/SKILL.md) | Удаление скилла | [modify-skill.md](./modify-skill.md) |
| [/skill-migrate](/.claude/skills/skill-migrate/SKILL.md) | Переименование скилла | [modify-skill.md](./modify-skill.md) |
