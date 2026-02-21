---
name: plan-dev-validate
description: Проверка документа плана разработки на соответствие стандарту SDD — frontmatter, именование, TASK-N (5 полей), подзадачи, зависимости (циклы, порядок), TC трассируемость, INFRA лимит, маркеры, зона ответственности. Используй после создания или изменения плана разработки, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[путь] [--all] [--json]"
---

# Валидация плана разработки

**SSOT:** [validation-plan-dev.md](/specs/.instructions/analysis/plan-dev/validation-plan-dev.md)

## Формат вызова

```
/plan-dev-validate [путь] [--all] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу плана разработки | Нет (если --all) |
| `--all` | Проверить все документы плана разработки | Нет |
| `--json` | JSON вывод | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-plan-dev.md](/specs/.instructions/analysis/plan-dev/validation-plan-dev.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-plan-dev.md#чек-лист](/specs/.instructions/analysis/plan-dev/validation-plan-dev.md#чек-лист)

## Примеры

```
/plan-dev-validate specs/analysis/0001-oauth2-authorization/plan-dev.md
/plan-dev-validate --all
/plan-dev-validate specs/analysis/0005-cache-optimization/plan-dev.md --json
```
