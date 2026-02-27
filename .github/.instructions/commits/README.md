---
description: Инструкции для коммитов — Conventional Commits стандарт, типы, scope, breaking changes. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/commits/README.md
---

# Инструкции /.github/.instructions/commits/

Стандарт оформления коммитов (Conventional Commits).

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [SSOT .github](../../README.md)

**Содержание:** Формат коммитов, типы, правила, pre-commit hooks.

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
/.github/.instructions/commits/
├── .scripts/
│   └── validate-commit-msg.py  # Валидация формата commit message
├── README.md                   # Этот файл (индекс)
├── standard-commit.md          # Стандарт коммитов
└── create-commit.md            # Воркфлоу создания коммита
```

---

# 1. Стандарты

## 1.1. Стандарт коммитов

Формат Conventional Commits, типы коммитов, правила оформления.

**Оглавление:**
- [Формат сообщения](./standard-commit.md#1-формат-сообщения)
- [Типы коммитов](./standard-commit.md#2-типы-коммитов)
- [Scope](./standard-commit.md#3-scope)
- [Body и Footer](./standard-commit.md#4-body-и-footer)
- [Правила оформления](./standard-commit.md#5-правила-оформления)
- [Процесс коммита](./standard-commit.md#6-процесс-коммита)
- [Исправление коммитов](./standard-commit.md#7-исправление-коммитов)
- [Язык сообщений](./standard-commit.md#8-язык-сообщений)
- [Влияние коммита на релиз](./standard-commit.md#9-влияние-коммита-на-релиз)

**Инструкция:** [standard-commit.md](./standard-commit.md)

---

# 2. Воркфлоу

## 2.1. Создание коммита

Процесс создания коммита: анализ diff, определение type/scope, формирование message, staging, hooks, amend, signing.

**Инструкция:** [create-commit.md](./create-commit.md)

---

# 3. Валидация

*Нет валидаций.*

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-commit-msg.py](./.scripts/validate-commit-msg.py) | Валидация формата commit message (commit-msg hook) | [standard-commit.md](./standard-commit.md) |

---

# 5. Скиллы

*Нет скиллов.*

---

# 6. Скиллы

| Скилл | Назначение |
|-------|------------|
| [/commit](/.claude/skills/commit/SKILL.md) | Создание коммита по Conventional Commits |
