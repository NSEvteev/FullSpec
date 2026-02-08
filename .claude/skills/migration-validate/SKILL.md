---
name: migration-validate
description: Валидация миграции при обновлении стандартов
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[стандарт]"
---

# Валидация миграции

**SSOT:** [validation-migration.md](/.instructions/migration/validation-migration.md)

## Формат вызова

```
/migration-validate [стандарт]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `стандарт` | Путь к стандарту для проверки миграции | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-migration.md](/.instructions/migration/validation-migration.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-migration.md#чек-лист](/.instructions/migration/validation-migration.md#чек-лист)

## Примеры

```
/migration-validate .instructions/standard-instruction.md
/migration-validate .claude/.instructions/skills/standard-skill.md
```
