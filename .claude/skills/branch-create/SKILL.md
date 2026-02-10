---
name: branch-create
description: Создание git-ветки по стандарту именования с привязкой к Issue. Используй при начале работы над задачей, багфиксом или фичей — автоматически формирует имя ветки из номера Issue.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--issues <numbers>] [--description <name>]"
---

# Создание ветки

**SSOT:** [create-branch.md](/.github/.instructions/branches/create-branch.md)

## Формат вызова

```
/branch-create [--issues <numbers>] [--description <name>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--issues` | Номера Issues через запятую (42,43,44) | Нет (спросит) |
| `--description` | Описание для имени ветки (kebab-case) | Нет (определит по Issues) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-branch.md](/.github/.instructions/branches/create-branch.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-branch.md#чек-лист](/.github/.instructions/branches/create-branch.md#чек-лист)

## Примеры

```
/branch-create --issues 42,43,44
/branch-create --issues 50 --description upload-errors
/branch-create
```
