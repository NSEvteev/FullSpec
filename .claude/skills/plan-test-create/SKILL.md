---
name: plan-test-create
description: Создание документа плана тестов SDD — чтение Design (SVC-N, INT-N, STS-N) и Discussion (REQ-N), Clarify, генерация TC-N acceptance-сценариев, тестовых данных, системных сценариев и матрицы покрытия. Используй после одобрения Design (WAITING) для определения тестовых сценариев.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<parent-design> [--auto-clarify]"
---

# Создание плана тестов

**SSOT:** [create-plan-test.md](/specs/.instructions/analysis/plan-test/create-plan-test.md)

## Формат вызова

```
/plan-test-create <parent-design> [--auto-clarify]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `parent-design` | Путь к parent Design (в WAITING) | Да |
| `--auto-clarify` | Пропустить Clarify, маркеры на неясности | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-plan-test.md](/specs/.instructions/analysis/plan-test/create-plan-test.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-plan-test.md#чек-лист](/specs/.instructions/analysis/plan-test/create-plan-test.md#чек-лист)

## Примеры

```
/plan-test-create specs/analysis/0001-oauth2-authorization/design.md
/plan-test-create specs/analysis/0005-cache-optimization/design.md --auto-clarify
/plan-test-create specs/analysis/0010-payment-integration/design.md
```
