---
name: design-create
description: Создание документа проектирования SDD с Unified Scan (5 источников), Clarify, генерацией секций SVC-N (9 подсекций, 8:8 маппинг), INT-N, STS-N, валидацией и артефактами. Используй после одобрения Discussion (WAITING) для распределения ответственностей между сервисами.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<parent-discussion> [--auto-clarify]"
---

# Создание проектирования

**SSOT:** [create-design.md](/specs/.instructions/analysis/design/create-design.md)

## Формат вызова

```
/design-create <parent-discussion> [--auto-clarify]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `parent-discussion` | Путь к parent Discussion (в WAITING) | Да |
| `--auto-clarify` | Пропустить Clarify, маркеры на неясности | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-design.md](/specs/.instructions/analysis/design/create-design.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-design.md#чек-лист](/specs/.instructions/analysis/design/create-design.md#чек-лист)

## Примеры

```
/design-create specs/analysis/0001-oauth2-authorization/discussion.md
/design-create specs/analysis/0005-cache-optimization/discussion.md --auto-clarify
/design-create specs/analysis/0010-payment-integration/discussion.md
```
