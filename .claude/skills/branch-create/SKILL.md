---
name: branch-create
description: Создание git-ветки по стандарту именования с привязкой к analysis chain. Используй при начале работы над задачей — автоматически формирует имя ветки из номера анализа NNNN.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--analysis <NNNN>] [--description <name>]"
---

# Создание ветки

**SSOT:** [create-branch.md](/.github/.instructions/branches/create-branch.md)

## Формат вызова

```
/branch-create [--analysis <NNNN>] [--description <name>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--analysis` | 4-значный номер анализа (0001, 0042) | Нет (спросит) |
| `--description` | Описание для имени ветки (kebab-case) | Нет (определит по analysis topic) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-branch.md](/.github/.instructions/branches/create-branch.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-branch.md#чек-лист](/.github/.instructions/branches/create-branch.md#чек-лист)

## Примеры

```
/branch-create --analysis 0001
/branch-create --analysis 0001 --description oauth2-auth
/branch-create
```
