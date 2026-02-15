---
name: impact-create
description: Создание документа импакт-анализа SDD с Quick Scan, Clarify, генерацией разделов и валидацией. Используй после одобрения Discussion (WAITING) для анализа влияния изменений на сервисы.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<parent-discussion> [--auto-clarify]"
---

# Создание импакт-анализа

**SSOT:** [create-impact.md](/specs/.instructions/impact/create-impact.md)

## Формат вызова

```
/impact-create <parent-discussion> [--auto-clarify]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `parent-discussion` | Путь к parent Discussion (в WAITING) | Да |
| `--auto-clarify` | Пропустить Clarify, маркеры на неясности | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-impact.md](/specs/.instructions/impact/create-impact.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-impact.md#чек-лист](/specs/.instructions/impact/create-impact.md#чек-лист)

## Примеры

```
/impact-create specs/discussion/disc-0001-oauth2-authorization.md
/impact-create specs/discussion/disc-0005-cache-race-conditions.md --auto-clarify
/impact-create specs/discussion/disc-0008-api-latency-reduction.md
```
