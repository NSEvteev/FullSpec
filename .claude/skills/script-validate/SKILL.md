---
name: script-validate
description: Валидация формата и структуры скриптов
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[путь] [--all] [--json]"
---

# Валидация скрипта

**SSOT:** [validation-script.md](/.instructions/validation-script.md)

## Формат вызова

```
/script-validate [путь] [--all] [--principles] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к скрипту | Нет (если --all) |
| `--all` | Проверить все скрипты | Нет |
| `--principles` | Проверить принципы программирования | Нет |
| `--json` | JSON вывод | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-script.md](/.instructions/validation-script.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-script.md#чек-лист](/.instructions/validation-script.md#чек-лист)

## Примеры

```
/script-validate .instructions/.scripts/validate-api.py
/script-validate --all
/script-validate .instructions/.scripts/parse-docstrings.py --principles
```
