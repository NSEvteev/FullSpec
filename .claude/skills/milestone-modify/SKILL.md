---
name: milestone-modify
description: Обновление описания, закрытие или удаление GitHub Milestone. Используй при изменении срока релиза, закрытии завершённого milestone или удалении ошибочно созданного.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--number <N>] [--close] [--delete]"
---

# Изменение Milestone

**SSOT:** [modify-milestone.md](/.github/.instructions/milestones/modify-milestone.md)

## Формат вызова

```
/milestone-modify [--number <N>] [--title <title>] [--close] [--delete]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--number` | Номер Milestone | Нет |
| `--title` | Title Milestone | Нет |
| `--close` | Закрыть Milestone | Нет |
| `--delete` | Удалить Milestone | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-milestone.md](/.github/.instructions/milestones/modify-milestone.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-milestone.md#чек-лист](/.github/.instructions/milestones/modify-milestone.md#чек-лист)

## Примеры

```
/milestone-modify --title "v1.0.0" --close
/milestone-modify --number 3
/milestone-modify --title "v0.1.0" --delete
```
