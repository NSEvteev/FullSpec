---
name: technology-validate
description: Проверка per-tech стандарта на соответствие стандарту — frontmatter, секции, rule, реестр. Используй после создания или изменения per-tech стандарта, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[tech-name | path]"
---

# Валидация per-tech стандарта

**SSOT:** [validation-technology.md](/specs/.instructions/technologies/validation-technology.md)

## Формат вызова

```
/technology-validate [tech-name | path]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `tech-name` | Имя технологии (например `python`) или путь к файлу/папке | Нет (валидирует все) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-technology.md](/specs/.instructions/technologies/validation-technology.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-technology.md#чек-лист](/specs/.instructions/technologies/validation-technology.md#чек-лист)

## Примеры

```
/technology-validate python
/technology-validate specs/technologies/standard-python.md
/technology-validate specs/technologies/
```
