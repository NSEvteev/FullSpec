---
name: review-create
description: Создание review.md с секцией Контекст ревью — читает цепочку документов, запускает extract-svc-context.py, заполняет сервисные блоки. Используй при переходе Plan Dev → WAITING, до начала разработки.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.0
argument-hint: "[ветка]"
---

# Создание review.md

**SSOT:** [create-review.md](/specs/.instructions/analysis/review/create-review.md)

## Формат вызова

```
/review-create [ветка]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `ветка` | Имя ветки / папки `NNNN-{topic}` | Нет (определяется автоматически через `git branch --show-current`) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-review.md](/specs/.instructions/analysis/review/create-review.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-review.md#чек-лист](/specs/.instructions/analysis/review/create-review.md#чек-лист)

## Примеры

```
/review-create
/review-create 0001-oauth2-authorization
```
