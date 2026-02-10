---
description: Инструкции для веток Git — стандарт именования, создание, валидация. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/branches/README.md
---

# Инструкции /.github/.instructions/branches/

Стандарт именования и создания веток.

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [SSOT .github](../../README.md)

**Содержание:** Naming convention, создание веток, жизненный цикл, граничные случаи.

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
/.github/.instructions/branches/
├── README.md                 # Этот файл (индекс)
├── standard-branching.md     # Стандарт ветвления
├── validation-branch.md      # Валидация ветки
└── create-branch.md          # Создание ветки
```

---

# 1. Стандарты

## 1.1. Стандарт ветвления

Модель ветвления, naming convention, жизненный цикл, запреты, граничные случаи, валидация.

**Оглавление:**
- [Модель ветвления](./standard-branching.md#1-модель-ветвления)
- [Naming Convention](./standard-branching.md#2-naming-convention)
- [Жизненный цикл ветки](./standard-branching.md#3-жизненный-цикл-ветки)
- [Запреты и ограничения](./standard-branching.md#4-запреты-и-ограничения)
- [Граничные случаи](./standard-branching.md#5-граничные-случаи)
- [Валидация](./standard-branching.md#6-валидация)

**Инструкция:** [standard-branching.md](./standard-branching.md)

---

# 2. Воркфлоу

## 2.1. Создание ветки

Воркфлоу создания ветки: sync main, определение type по Issues, формирование имени.

**Инструкция:** [create-branch.md](./create-branch.md)

---

# 3. Валидация

## 3.1. Валидация ветки

Проверка формата имени, существования Issues, соответствия TYPE-меток.

**Инструкция:** [validation-branch.md](./validation-branch.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-branch-name.py](../.scripts/validate-branch-name.py) | Валидация имени ветки и Issues | [validation-branch.md](./validation-branch.md) |

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/branch-create](/.claude/skills/branch-create/SKILL.md) | Создание ветки по стандарту | [create-branch.md](./create-branch.md) |

> Валидация ветки выполняется автоматически через pre-commit hook (`branch-validate`).
