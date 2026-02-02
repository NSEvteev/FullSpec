---
name: structure-validate
description: Валидация согласованности SSOT структуры проекта
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash, Glob, Grep
triggers:
  commands:
    - /structure-validate
  phrases:
    ru:
      - проверь структуру
      - валидация структуры
      - проверь редми
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

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-structure.md#чек-лист](/.structure/.instructions/validation-structure.md#чек-лист)

## Примеры

```
/structure-validate
/structure-validate --json
```
