---
name: instruction-create
description: Создание новой инструкции (standard/validation/create/modify) с frontmatter, секциями и регистрацией в README. Используй при добавлении нового процесса, стандарта или воркфлоу.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: "[имя] [--path <область>] [--dry-run]"
---

# Создание инструкции

**SSOT:** [create-instruction.md](/.instructions/create-instruction.md)

## Формат вызова

```
/instruction-create [имя] [--path <область>] [--dry-run]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `имя` | Имя инструкции (kebab-case) | Нет (спросит) |
| `--path` | Область: `/.instructions/`, `/src/.instructions/` и т.д. | Нет (спросит) |
| `--dry-run` | Показать план без выполнения | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-instruction.md](/.instructions/create-instruction.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-instruction.md#чек-лист](/.instructions/create-instruction.md#чек-лист)

## Примеры

```
/instruction-create error-handling
/instruction-create api-versioning --path /src/.instructions/
/instruction-create naming --dry-run
```

