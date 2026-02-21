---
name: milestone-create
description: Создание GitHub Milestone с версией, описанием и датой завершения по стандарту проекта. Используй при планировании нового релиза или группировки задач в итерацию.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[version] [--due <date>]"
---

# Создание Milestone

**SSOT:** [create-milestone.md](/.github/.instructions/milestones/create-milestone.md)

## Формат вызова

```
/milestone-create [version] [--due <date>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `version` | Версия SemVer (например, v0.1.0) | Нет (определит автоматически) |
| `--due` | Дедлайн (YYYY-MM-DD) | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-milestone.md](/.github/.instructions/milestones/create-milestone.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-milestone.md#чек-лист](/.github/.instructions/milestones/create-milestone.md#чек-лист)

## Примеры

```
/milestone-create v0.1.0
/milestone-create v1.0.0 --due 2026-03-15
/milestone-create
```
