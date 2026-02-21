---
name: structure-create
description: Создание новой папки в структуре проекта с README, .instructions/ и синхронизацией SSOT. Используй при добавлении нового модуля, сервиса или раздела документации.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: '<путь> [--description "..."]'
---

# Создание папки

**SSOT:** [create-structure.md](/.structure/.instructions/create-structure.md)

## Формат вызова

```
/structure-create <путь> [--description "Описание"]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<путь>` | Путь к новой папке | Да |
| `--description` | Описание для SSOT | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-structure.md](/.structure/.instructions/create-structure.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-structure.md#чек-лист](/.structure/.instructions/create-structure.md#чек-лист)

## Примеры

```
/structure-create docs --description "Документация проекта"
/structure-create src/utils --description "Утилиты"
```
