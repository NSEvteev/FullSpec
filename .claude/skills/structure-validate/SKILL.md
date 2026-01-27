---
name: structure-validate
description: Валидация согласованности SSOT структуры проекта
allowed-tools: Read, Bash, Glob, Grep
category: documentation
triggers:
  commands:
    - /structure-validate
  phrases:
    ru:
      - проверь структуру
      - валидация структуры
    en:
      - validate structure
      - check structure
---

# Валидация структуры

**SSOT:** [validation-structure.md](/.structure/.instructions/validation-structure.md)

## Формат вызова

```
/structure-validate [--json]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--json` | JSON-вывод | false |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-structure.md](/.structure/.instructions/validation-structure.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-structure.md#чек-лист](/.structure/.instructions/validation-structure.md#чек-лист)

## Примеры

```
/structure-validate
/structure-validate --json
```
