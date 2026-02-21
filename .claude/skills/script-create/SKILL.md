---
name: script-create
description: Создание нового Python-скрипта автоматизации с docstring, argparse и регистрацией в README. Используй при добавлении скрипта валидации, синхронизации или другой автоматизации проекта.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: "[название] [--area <область>]"
---

# Создание скрипта

**SSOT:** [create-script.md](/.instructions/create-script.md)

## Формат вызова

```
/script-create [название] [--area <область>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `название` | Имя скрипта (kebab-case) | Нет (спросит) |
| `--area` | Область: `/.instructions/`, `/src/.instructions/` и т.д. | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-script.md](/.instructions/create-script.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-script.md#чек-лист](/.instructions/create-script.md#чек-лист)

## Примеры

```
/script-create validate-api
/script-create find-references --area .structure/.instructions
```
