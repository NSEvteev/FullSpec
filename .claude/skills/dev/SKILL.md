---
name: dev
description: Запуск разработки по analysis chain — prerequisite check, создание Issues/Milestone/Branch, переход WAITING → RUNNING. Используй при переходе Plan Dev в WAITING для запуска кодирования.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.0
argument-hint: <NNNN> [--resume]
---

# Запуск разработки

**SSOT:** [create-dev.md](/.github/.instructions/development/create-dev.md)

## Формат вызова

```
/dev <NNNN> [--resume]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<NNNN>` | Номер analysis chain | Да |
| `--resume` | Продолжить прерванный запуск | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-dev.md](/.github/.instructions/development/create-dev.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-dev.md#чек-лист](/.github/.instructions/development/create-dev.md#чек-лист)

## Примеры

```
/dev 0001
/dev 0003 --resume
```
