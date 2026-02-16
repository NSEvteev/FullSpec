---
name: design-create
description: Создание документа проектирования SDD с Deep Scan, Clarify, генерацией секций SVC/INT/STS, валидацией и артефактами. Используй после одобрения Impact (WAITING) для распределения ответственностей между сервисами.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<parent-impact> [--auto-clarify]"
---

# Создание проектирования

**SSOT:** [create-design.md](/specs/.instructions/design/create-design.md)

## Формат вызова

```
/design-create <parent-impact> [--auto-clarify]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `parent-impact` | Путь к parent Impact (в WAITING) | Да |
| `--auto-clarify` | Пропустить Clarify, маркеры на неясности | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-design.md](/specs/.instructions/design/create-design.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-design.md#чек-лист](/specs/.instructions/design/create-design.md#чек-лист)

## Примеры

```
/design-create specs/impact/impact-0001-oauth2-authorization.md
/design-create specs/impact/impact-0005-cache-optimization.md --auto-clarify
/design-create specs/impact/impact-0010-payment-integration.md
```
