---
name: dev
description: Процесс разработки в feature-ветке — взятие задачи, написание кода, тестирование, коммит. Используй когда ветка уже в RUNNING.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.0
argument-hint: "[--issue <N>] [--continue]"
---

# Процесс разработки

**SSOT:** [modify-development.md](/.github/.instructions/development/modify-development.md)

## Формат вызова

```
/dev [--issue <N>] [--continue]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--issue <N>` | Номер конкретного Issue для работы | Нет |
| `--continue` | Продолжить с текущего Issue | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-development.md](/.github/.instructions/development/modify-development.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-development.md#чек-лист](/.github/.instructions/development/modify-development.md#чек-лист)

## Примеры

```
/dev
/dev --issue 42
/dev --continue
```
