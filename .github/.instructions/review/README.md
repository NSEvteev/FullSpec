---
description: Ревью и merge Pull Request
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/review/README.md
---

# Инструкции /.github/.instructions/review/

Ревью и merge Pull Request.

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [SSOT .github](../../README.md)

**Содержание:** Code Review, Merge, Branch Protection.

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
/.github/.instructions/review/
├── README.md              # Этот файл (индекс)
├── standard-review.md     # Стандарт ревью и merge
└── validation-review.md   # Валидация (review-branch + review-pr)
```

---

# 1. Стандарты

## 1.1. Стандарт ревью

Code Review процесс, merge стратегии и Branch Protection Rules.

**Оглавление:**
- [Code Review](./standard-review.md#2-code-review-процесс)
- [Merge](./standard-review.md#3-merge-стратегии)
- [Branch Protection](./standard-review.md#4-branch-protection-rules)

**Инструкция:** [standard-review.md](./standard-review.md)

---

# 2. Воркфлоу

*Нет воркфлоу.*

---

# 3. Валидация

## 3.1. Валидация Review

Два этапа: локальное ревью ветки (до PR) и ревью PR (после создания).

**Инструкция:** [validation-review.md](./validation-review.md)

---

# 4. Скрипты

*Нет скриптов.*

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/review-branch](/.claude/skills/review-branch/SKILL.md) | Локальное ревью ветки (Этап 1) | [validation-review.md](./validation-review.md) |
| [/review-pr](/.claude/skills/review-pr/SKILL.md) | Ревью PR на GitHub (Этап 2) | [validation-review.md](./validation-review.md) |
