---
name: milestone-validate
description: Проверка GitHub Milestone на соответствие стандарту — формат версии, описание, привязка Issue. Используй для аудита milestones, проверки перед релизом или валидации всех milestones проекта.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--number <N>] [--all]"
---

# Валидация Milestone

**SSOT:** [validation-milestone.md](/.github/.instructions/milestones/validation-milestone.md)

## Формат вызова

```
/milestone-validate [--number <N>] [--title <title>] [--all] [--state <state>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--number` | Номер Milestone для валидации | Нет |
| `--title` | Title Milestone для валидации | Нет |
| `--all` | Валидация всех Milestones | Нет |
| `--state` | Состояние для --all: open/closed/all (по умолчанию: open) | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-milestone.md](/.github/.instructions/milestones/validation-milestone.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-milestone.md#чек-лист](/.github/.instructions/milestones/validation-milestone.md#чек-лист)

## Примеры

```
/milestone-validate --number 3
/milestone-validate --title "v1.0.0"
/milestone-validate --all
/milestone-validate --all --state closed
```
