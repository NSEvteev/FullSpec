---
name: impact-validate
description: Проверка документа импакт-анализа на соответствие стандарту SDD — frontmatter, именование, секции, нумерация, маркеры, зона ответственности. Используй после создания или изменения импакт-анализа, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[путь] [--all] [--json]"
---

# Валидация импакт-анализа

**SSOT:** [validation-impact.md](/specs/.instructions/impact/validation-impact.md)

## Формат вызова

```
/impact-validate [путь] [--all] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу импакт-анализа | Нет (если --all) |
| `--all` | Проверить все импакт-анализы | Нет |
| `--json` | JSON вывод | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-impact.md](/specs/.instructions/impact/validation-impact.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-impact.md#чек-лист](/specs/.instructions/impact/validation-impact.md#чек-лист)

## Примеры

```
/impact-validate specs/impact/impact-0001-oauth2-authorization.md
/impact-validate --all
/impact-validate specs/impact/impact-0005-cache-race-conditions.md --json
```
