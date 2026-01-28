---
description: Индекс инструкций для Claude Code окружения
standard: .structure/.instructions/standard-readme.md
index: .claude/.instructions/README.md
---

# Инструкции /.claude/

Индекс инструкций для работы с Claude Code окружением.

**Полезные ссылки:**
- [Claude Code окружение](/.claude/README.md)
- [CLAUDE.md](/CLAUDE.md) — точка входа

**Содержание:** стандарты скиллов, воркфлоу создания и изменения, валидация.

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
/.claude/.instructions/
├── README.md              # Этот файл (индекс)
└── skills/                # Инструкции для скиллов
    ├── README.md          #   Индекс инструкций скиллов
    ├── standard-skill.md  #   Стандарт скиллов
    ├── create-skill.md    #   Создание скилла
    ├── modify-skill.md    #   Изменение скилла
    └── validation-skill.md #  Валидация скиллов
```

---

# 1. Стандарты

## 1.1. Стандарт скиллов

Формат и структура файлов SKILL.md в сокращённом формате.

**Оглавление:**
- [Назначение](./skills/standard-skill.md#1-назначение)
- [Формат файла](./skills/standard-skill.md#3-формат-файла)
- [Frontmatter](./skills/standard-skill.md#4-frontmatter)

**Инструкция:** [skills/standard-skill.md](./skills/standard-skill.md)

---

# 2. Воркфлоу

## 2.1. Создание скилла

Воркфлоу создания нового скилла.

**Инструкция:** [skills/create-skill.md](./skills/create-skill.md)

## 2.2. Изменение скилла

Воркфлоу обновления, удаления и миграции скиллов.

**Инструкция:** [skills/modify-skill.md](./skills/modify-skill.md)

---

# 3. Валидация

## 3.1. Валидация скиллов

Проверка соответствия скиллов сокращённому формату.

**Инструкция:** [skills/validation-skill.md](./skills/validation-skill.md)

---

# 4. Скрипты

*Нет скриптов.*

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/skill-create](/.claude/skills/skill-create/SKILL.md) | Создание скилла | [create-skill.md](./skills/create-skill.md) |
| [/skill-update](/.claude/skills/skill-update/SKILL.md) | Обновление скиллов | [modify-skill.md](./skills/modify-skill.md) |
| [/skill-delete](/.claude/skills/skill-delete/SKILL.md) | Удаление скилла | [modify-skill.md](./skills/modify-skill.md) |
| [/skill-migrate](/.claude/skills/skill-migrate/SKILL.md) | Переименование скилла | [modify-skill.md](./skills/modify-skill.md) |
