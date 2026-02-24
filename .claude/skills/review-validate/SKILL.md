---
name: review-validate
description: Проверка документа ревью кода на соответствие стандарту — frontmatter, именование, секции Контекст ревью и Итерации, вердикт, статус OPEN/RESOLVED. Используй после создания или изменения review.md, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
ssot-version: v1.0
argument-hint: "[путь] [--all]"
---

# Валидация ревью

**SSOT:** [validation-review.md](/specs/.instructions/analysis/review/validation-review.md)

## Формат вызова

```
/review-validate [путь] [--all]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу ревью | Нет (если --all) |
| `--all` | Проверить все review.md в specs/analysis/ | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-review.md](/specs/.instructions/analysis/review/validation-review.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-review.md#чек-лист](/specs/.instructions/analysis/review/validation-review.md#чек-лист)

## Примеры

```
/review-validate specs/analysis/0001-oauth2-authorization/review.md
/review-validate --all
```
