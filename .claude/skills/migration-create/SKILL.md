---
name: migration-create
description: Выполнение миграции зависимых файлов после обновления стандарта — Workflows, экземпляры, скрипты. Используй после изменения любого standard-*.md файла для синхронизации всех зависимостей.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Edit, Write
argument-hint: "[стандарт]"
---

# Воркфлоу миграции

**SSOT:** [create-migration.md](/.instructions/migration/create-migration.md)

## Формат вызова

```
/migration-create [стандарт]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `стандарт` | Путь к изменённому стандарту | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-migration.md](/.instructions/migration/create-migration.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-migration.md#чек-лист](/.instructions/migration/create-migration.md#чек-лист)

## Примеры

```
/migration-create .instructions/standard-instruction.md
/migration-create .claude/.instructions/skills/standard-skill.md
```
