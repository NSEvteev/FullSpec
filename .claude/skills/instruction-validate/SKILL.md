---
name: instruction-validate
description: Проверка инструкции на соответствие стандарту — frontmatter, обязательные секции, ссылки, чек-лист. Используй после создания или изменения инструкции, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
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
