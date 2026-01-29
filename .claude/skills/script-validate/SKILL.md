---
name: script-validate
description: Валидация формата и структуры скриптов
allowed-tools: Read, Bash, Glob, Grep
triggers:
  commands:
    - /script-validate
  phrases:
    ru:
      - проверь скрипт
      - валидируй скрипт
    en:
      - validate script
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

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-script.md#чек-лист](/.instructions/validation-script.md#чек-лист)

## Примеры

```
/script-validate .instructions/.scripts/validate-api.py
/script-validate --all
/script-validate .instructions/.scripts/parse-docstrings.py --principles
```
