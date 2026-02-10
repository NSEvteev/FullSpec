---
description: Инструкции для GitHub Milestones — стандарт, создание, изменение, валидация. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/milestones/README.md
---

# Инструкции /.github/milestones/

Индекс инструкций для папки milestones/.

**Полезные ссылки:**
- [Инструкции .github/](../README.md)
- [.github/](../../README.md)

**Содержание:** Milestones, SemVer, версионирование, жизненный цикл

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | [standard-milestone.md](./standard-milestone.md) | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | 2 воркфлоу | Создание и изменение |
| [3. Валидация](#3-валидация) | [validation-milestone.md](./validation-milestone.md) | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | 3 скрипта | Автоматизация |
| [5. Скиллы](#5-скиллы) | 3 скилла | Скиллы для этой области |

```
/.github/.instructions/milestones/
├── README.md                           # Этот файл (индекс)
├── standard-milestone.md               # Стандарт управления Milestones
├── validation-milestone.md             # Валидация Milestone по стандарту
├── create-milestone.md                # Воркфлоу создания Milestone
└── modify-milestone.md                # Воркфлоу изменения Milestone
```

---

# 1. Стандарты

| Документ | Описание |
|----------|----------|
| [standard-milestone.md](./standard-milestone.md) | Правила жизненного цикла, создания и управления Milestones |

---

# 2. Воркфлоу

| Документ | Описание |
|----------|----------|
| [create-milestone.md](./create-milestone.md) | Пошаговый процесс создания Milestone |
| [modify-milestone.md](./modify-milestone.md) | Обновление, закрытие и удаление Milestone |

---

# 3. Валидация

| Документ | Описание |
|----------|----------|
| [validation-milestone.md](./validation-milestone.md) | Проверка Milestone: title, description, due date, Issues, Release |

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-milestone.py](../.scripts/validate-milestone.py) | Валидация Milestone по стандарту | [validation-milestone.md](./validation-milestone.md) |
| [create-milestone.py](../.scripts/create-milestone.py) | Создание Milestone: версия, уникальность, API | [create-milestone.md](./create-milestone.md) |
| [close-milestone.py](../.scripts/close-milestone.py) | Закрытие Milestone: проверки, перенос Issues | [modify-milestone.md](./modify-milestone.md) |

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/milestone-create](/.claude/skills/milestone-create/SKILL.md) | Создание Milestone | [create-milestone.md](./create-milestone.md) |
| [/milestone-modify](/.claude/skills/milestone-modify/SKILL.md) | Изменение/закрытие/удаление Milestone | [modify-milestone.md](./modify-milestone.md) |
| [/milestone-validate](/.claude/skills/milestone-validate/SKILL.md) | Валидация Milestone | [validation-milestone.md](./validation-milestone.md) |
