---
name: discussion-create
description: Создание документа дискуссии SDD с Clarify, генерацией разделов и валидацией. Используй при запуске нового SDD-воркфлоу — описание проблемы, требований и критериев успеха.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "[тема] [--auto-clarify]"
---

# Создание дискуссии

**SSOT:** [create-discussion.md](/specs/.instructions/discussion/create-discussion.md)

## Формат вызова

```
/discussion-create [тема] [--auto-clarify]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `тема` | Тема дискуссии (описание проблемы) | Нет (спросит) |
| `--auto-clarify` | Пропустить Clarify, маркеры на неясности | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-discussion.md](/specs/.instructions/discussion/create-discussion.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-discussion.md#чек-лист](/specs/.instructions/discussion/create-discussion.md#чек-лист)

## Примеры

```
/discussion-create OAuth2 авторизация вместо session-based
/discussion-create Снижение latency API --auto-clarify
/discussion-create Исправление race conditions в кэше
```
