---
name: review-pr
description: Ревью Pull Request на GitHub
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "<number>"
---

# Ревью Pull Request

**SSOT:** [validation-review.md](/.github/.instructions/review/validation-review.md)

## Формат вызова

```
/review-pr <number>
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `number` | Номер PR на GitHub | Да |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-review.md](/.github/.instructions/review/validation-review.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить Шаги 4-8 из SSOT-инструкции (Этап 2: Review PR).

## Чек-лист

→ См. [validation-review.md#этап-2-review-pr](/.github/.instructions/review/validation-review.md#этап-2-review-pr)

## Примеры

```
/review-pr 42
/review-pr 123
```
