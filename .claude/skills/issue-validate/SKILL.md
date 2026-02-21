---
name: issue-validate
description: Проверка GitHub Issue на соответствие стандарту — заголовок, метки, milestone, описание. Используй для аудита Issue, проверки перед закрытием или валидации всех Issue в milestone.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[number] [--all] [--milestone <title>]"
---

# Валидация Issue

**SSOT:** [validation-issue.md](/.github/.instructions/issues/validation-issue.md)

## Формат вызова

```
/issue-validate [number] [--all] [--milestone <title>] [--state <state>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `number` | Номер Issue для валидации | Нет |
| `--all` | Валидация всех Issues | Нет |
| `--milestone` | Валидация Issues конкретного milestone | Нет |
| `--state` | Состояние: open/closed/all (по умолчанию: open) | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-issue.md](/.github/.instructions/issues/validation-issue.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-issue.md#чек-лист](/.github/.instructions/issues/validation-issue.md#чек-лист)

## Примеры

```
/issue-validate 42
/issue-validate --all
/issue-validate --milestone "v1.0.0"
/issue-validate --all --state closed
```
