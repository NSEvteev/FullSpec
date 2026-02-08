---
name: instruction-validate
description: Валидация формата и структуры инструкций
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[путь] [--all] [--json]"
---

# Валидация инструкции

**SSOT:** [validation-instruction.md](/.instructions/validation-instruction.md)

## Формат вызова

```
/instruction-validate [путь] [--all] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к инструкции | Нет (если --all) |
| `--all` | Проверить все инструкции | Нет |
| `--json` | JSON вывод | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-instruction.md](/.instructions/validation-instruction.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-instruction.md#чек-лист](/.instructions/validation-instruction.md#чек-лист)

## Примеры

```
/instruction-validate .instructions/standard-api.md
/instruction-validate --all
/instruction-validate .claude/.instructions/skills/create-skill.md --json
```
