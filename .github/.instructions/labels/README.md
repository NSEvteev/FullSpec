---
description: Инструкции для GitHub Labels — стандарт, модификация, валидация labels.yml. Индекс документов и скриптов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/labels/README.md
---

# Инструкции Labels

Индекс инструкций для системы меток GitHub.

**Полезные ссылки:**
- [Инструкции .github/](../README.md)
- [.github/](../../README.md)

**Содержание:** Система меток GitHub для Issues и Pull Requests.

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
/.github/.instructions/labels/
├── README.md                # Этот файл (индекс)
├── standard-labels.md       # Стандарт системы меток
├── validation-labels.md     # Валидация labels.yml и меток
└── modify-labels.md         # Модификация меток
```

---

# 1. Стандарты

| Инструкция | Описание |
|------------|----------|
| [standard-labels.md](./standard-labels.md) | Стандарт управления метками (создание, применение, удаление) |

**Справочник меток:** [.github/labels.yml](../labels.yml) — SSOT категорий и меток

---

# 2. Воркфлоу

| Инструкция | Описание |
|------------|----------|
| [modify-labels.md](./modify-labels.md) | Модификация меток (добавление, удаление, переименование) |

---

# 3. Валидация

| Инструкция | Описание |
|------------|----------|
| [validation-labels.md](./validation-labels.md) | Валидация labels.yml и меток на Issues/PR |

---

# 4. Скрипты

*Нет скриптов.*

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/labels-validate](/.claude/skills/labels-validate/SKILL.md) | Валидация labels.yml и меток | [validation-labels.md](./validation-labels.md) |
| [/labels-modify](/.claude/skills/labels-modify/SKILL.md) | Изменение меток | [modify-labels.md](./modify-labels.md) |
