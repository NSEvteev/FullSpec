---
name: issue-modify
description: Обновление, закрытие или переоткрытие GitHub Issue с соблюдением стандарта проекта. Используй при изменении описания, меток, milestone или статуса существующего Issue.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "<number> [--close] [--reopen]"
---

# Изменение Issue

**SSOT:** [modify-issue.md](/.github/.instructions/issues/modify-issue.md)

## Формат вызова

```
/issue-modify <number> [--close] [--reopen] [--title <title>] [--milestone <title>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `number` | Номер Issue | Да |
| `--close` | Закрыть Issue (not planned) | Нет |
| `--reopen` | Переоткрыть Issue | Нет |
| `--title` | Новый заголовок | Нет |
| `--milestone` | Новый Milestone | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-issue.md](/.github/.instructions/issues/modify-issue.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-issue.md#чек-лист](/.github/.instructions/issues/modify-issue.md#чек-лист)

## Примеры

```
/issue-modify 42 --title "Исправить ошибку загрузки файлов более 10 МБ"
/issue-modify 55 --close
/issue-modify 42 --reopen
/issue-modify 42 --milestone "v1.1.0"
```
