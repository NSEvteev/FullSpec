---
name: dev-create
description: Запуск разработки по analysis chain — prerequisite check, создание Issues/Milestone/Branch, переход WAITING → RUNNING. Используй при переходе Plan Dev в WAITING для запуска кодирования.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.0
argument-hint: <NNNN> [--resume]
---

# Запуск разработки

**SSOT:** [create-development.md](/.github/.instructions/development/create-development.md)

## Формат вызова

```
/dev-create <NNNN> [--resume]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<NNNN>` | Номер analysis chain | Да |
| `--resume` | Продолжить прерванный запуск | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-development.md](/.github/.instructions/development/create-development.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-development.md#чек-лист](/.github/.instructions/development/create-development.md#чек-лист)

## Примеры

```
/dev-create 0001
/dev-create 0003 --resume
```
