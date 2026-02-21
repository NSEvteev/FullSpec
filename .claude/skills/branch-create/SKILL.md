---
name: branch-create
description: Создание git-ветки по стандарту именования с привязкой к analysis chain. Используй при начале работы над задачей — автоматически формирует имя ветки из номера анализа NNNN.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--analysis <NNNN>]"
---

# Создание ветки

**SSOT:** [create-branch.md](/.github/.instructions/branches/create-branch.md)

## Формат вызова

```
/branch-create [--analysis <NNNN>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--analysis` | 4-значный номер анализа (0001, 0042). Имя ветки = имя папки analysis chain. | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-branch.md](/.github/.instructions/branches/create-branch.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-branch.md#чек-лист](/.github/.instructions/branches/create-branch.md#чек-лист)

## Примеры

```
/branch-create --analysis 0001
/branch-create
```
