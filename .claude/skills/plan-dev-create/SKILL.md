---
name: plan-dev-create
description: Создание документа плана разработки SDD — чтение Plan Tests (TC-N), Design (SVC-N), Discussion (REQ-N), Clarify, генерация TASK-N с 5 полями, подзадачи, кросс-сервисные зависимости, маппинг Issues. Используй после одобрения Plan Tests (WAITING) для определения задач реализации.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<parent-plan-test> [--auto-clarify]"
---

# Создание плана разработки

**SSOT:** [create-plan-dev.md](/specs/.instructions/analysis/plan-dev/create-plan-dev.md)

## Формат вызова

```
/plan-dev-create <parent-plan-test> [--auto-clarify]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `parent-plan-test` | Путь к parent Plan Tests (в WAITING) | Да |
| `--auto-clarify` | Пропустить Clarify, маркеры на неясности | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-plan-dev.md](/specs/.instructions/analysis/plan-dev/create-plan-dev.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-plan-dev.md#чек-лист](/specs/.instructions/analysis/plan-dev/create-plan-dev.md#чек-лист)

## Примеры

```
/plan-dev-create specs/analysis/0001-oauth2-authorization/plan-test.md
/plan-dev-create specs/analysis/0005-cache-optimization/plan-test.md --auto-clarify
/plan-dev-create specs/analysis/0010-payment-integration/plan-test.md
```
