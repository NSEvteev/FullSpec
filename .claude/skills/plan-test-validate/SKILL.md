---
name: plan-test-validate
description: Проверка документа плана тестов на соответствие стандарту SDD — frontmatter, именование, TC-N формат (естественные предложения, не G/W/T), покрытие REQ-N/STS-N, матрица, маркеры, зона ответственности. Используй после создания или изменения плана тестов, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[путь] [--all] [--json]"
---

# Валидация плана тестов

**SSOT:** [validation-plan-test.md](/specs/.instructions/analysis/plan-test/validation-plan-test.md)

## Формат вызова

```
/plan-test-validate [путь] [--all] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу плана тестов | Нет (если --all) |
| `--all` | Проверить все документы плана тестов | Нет |
| `--json` | JSON вывод | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-plan-test.md](/specs/.instructions/analysis/plan-test/validation-plan-test.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-plan-test.md#чек-лист](/specs/.instructions/analysis/plan-test/validation-plan-test.md#чек-лист)

## Примеры

```
/plan-test-validate specs/analysis/0001-oauth2-authorization/plan-test.md
/plan-test-validate --all
/plan-test-validate specs/analysis/0005-cache-optimization/plan-test.md --json
```
