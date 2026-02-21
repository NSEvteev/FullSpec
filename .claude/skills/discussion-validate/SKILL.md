---
name: discussion-validate
description: Проверка документа дискуссии на соответствие стандарту SDD — frontmatter, именование, секции, нумерация, маркеры, зона ответственности. Используй после создания или изменения дискуссии, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[путь] [--all] [--json]"
---

# Валидация дискуссии

**SSOT:** [validation-discussion.md](/specs/.instructions/analysis/discussion/validation-discussion.md)

## Формат вызова

```
/discussion-validate [путь] [--all] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу дискуссии | Нет (если --all) |
| `--all` | Проверить все дискуссии | Нет |
| `--json` | JSON вывод | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-discussion.md](/specs/.instructions/analysis/discussion/validation-discussion.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-discussion.md#чек-лист](/specs/.instructions/analysis/discussion/validation-discussion.md#чек-лист)

## Примеры

```
/discussion-validate specs/analysis/0001-oauth2-authorization/discussion.md
/discussion-validate --all
/discussion-validate specs/analysis/0005-cache-race-conditions/discussion.md --json
```
