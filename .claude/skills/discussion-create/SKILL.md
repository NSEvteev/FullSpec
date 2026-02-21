---
name: discussion-create
description: Создание документа дискуссии SDD с Clarify, генерацией разделов и валидацией. Используй при вызове пользователем "новой дискуссии", запуске нового "воркфлоу" и т.д. — в общем при разговоре с пользователем о проблеме, требованиях и критериях успеха проекта.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "[тема] [--auto-clarify]"
---

# Создание дискуссии

**SSOT:** [create-discussion.md](/specs/.instructions/analysis/discussion/create-discussion.md)

## Формат вызова

```
/discussion-create [тема] [--auto-clarify]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `тема` | Тема дискуссии (описание проблемы) | Нет (спросит) |
| `--auto-clarify` | Пропустить Clarify, маркеры на неясности | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-discussion.md](/specs/.instructions/analysis/discussion/create-discussion.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-discussion.md#чек-лист](/specs/.instructions/analysis/discussion/create-discussion.md#чек-лист)

## Примеры

```
/discussion-create OAuth2 авторизация вместо session-based
/discussion-create Снижение latency API --auto-clarify
/discussion-create Исправление race conditions в кэше
```
