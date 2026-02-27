---
description: Инструкции для Code Review — стандарт ревью, валидация, merge стратегия. Индекс документов.
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
├── validation-review.md   # Валидация (скилл /review)
└── create-merge.md        # Воркфлоу merge PR
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

## 2.1. Merge PR

Процесс merge PR: pre-checks, squash merge, post-merge sync, cleanup, verification.

**Инструкция:** [create-merge.md](./create-merge.md)

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
| [/review](/.claude/skills/review/SKILL.md) | Ревью кода (Этап 1 — ветка, Этап 2 — PR) | [validation-review.md](./validation-review.md) |
| [/review-create](/.claude/skills/review-create/SKILL.md) | Создание review.md с Контекст ревью | [create-review.md](/.specs/.instructions/analysis/review/create-review.md) |

**Агент / Скилл:**

| Имя | Назначение |
|-----|------------|
| [code-reviewer](/.claude/agents/code-reviewer/AGENT.md) | Глубокий анализ diff, сверка с постановкой из specs/analysis/ |
| [/merge](/.claude/skills/merge/SKILL.md) | Merge PR с pre/post проверками и sync |
