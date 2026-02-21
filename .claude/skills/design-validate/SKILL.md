---
name: design-validate
description: Проверка документа проектирования на соответствие стандарту SDD — frontmatter, именование, секции SVC-N (9 подсекций, 8:8 маппинг), INT-N, STS-N, delta-формат, маркеры, зона ответственности. Используй после создания или изменения проектирования, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[путь] [--all] [--json]"
---

# Валидация проектирования

**SSOT:** [validation-design.md](/specs/.instructions/analysis/design/validation-design.md)

## Формат вызова

```
/design-validate [путь] [--all] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу проектирования | Нет (если --all) |
| `--all` | Проверить все документы проектирования | Нет |
| `--json` | JSON вывод | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-design.md](/specs/.instructions/analysis/design/validation-design.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-design.md#чек-лист](/specs/.instructions/analysis/design/validation-design.md#чек-лист)

## Примеры

```
/design-validate specs/analysis/0001-oauth2-authorization/design.md
/design-validate --all
/design-validate specs/analysis/0005-cache-optimization/design.md --json
```
