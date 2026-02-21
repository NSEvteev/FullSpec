---
name: review
description: Ревью кода — локальное ревью ветки или ревью PR на GitHub. Объединяет оба этапа code review. Используй перед git push или при получении PR на ревью.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[<pr-number>] [--base <branch>]"
---

# Ревью кода

**SSOT:** [validation-review.md](/.github/.instructions/review/validation-review.md)

**Агент:** [code-reviewer](/.claude/agents/code-reviewer/AGENT.md)

## Формат вызова

```
/review [<pr-number>] [--base <branch>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `pr-number` | Номер PR на GitHub (включает Этап 2) | Нет |
| `--base` | Базовая ветка для сравнения (по умолчанию `main`) | Нет |

**Режимы:**
- Без аргументов или с `--base` → локальное ревью ветки (Этап 1)
- С `<pr-number>` → ревью PR на GitHub (Этап 2)

## Воркфлоу

> Прочитать [validation-review.md](/.github/.instructions/review/validation-review.md)

> Запустить агента `code-reviewer` через Task tool с параметрами вызова.

**Этап 1 (ветка):** Выполнить Шаги 1-3 из SSOT-инструкции.

**Этап 2 (PR):** Выполнить Шаги 4-8 из SSOT-инструкции.

## Чек-лист

→ См. [validation-review.md#чек-лист](/.github/.instructions/review/validation-review.md#чек-лист)

## Примеры

```
/review
/review --base develop
/review 42
/review 123
```
