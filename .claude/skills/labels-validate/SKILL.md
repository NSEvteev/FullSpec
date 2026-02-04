---
name: labels-validate
description: Валидация labels.yml и меток на Issues/PR
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash, Glob, Grep
triggers:
  commands:
    - /labels-validate
  phrases:
    ru:
      - валидация меток
      - проверить метки
      - валидация labels
    en:
      - validate labels
      - check labels
---

# Валидация меток

**SSOT:** [validation-labels.md](/.github/.instructions/labels/validation-labels.md)

## Формат вызова

```
/labels-validate [--file] [--sync] [--issue <number>] [--pr <number>] [--all]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--file` | Валидация структуры labels.yml | Нет (по умолчанию) |
| `--sync` | Проверка синхронизации с GitHub | Нет |
| `--issue` | Валидация меток на конкретном Issue | Нет |
| `--pr` | Валидация меток на конкретном PR | Нет |
| `--all` | Валидация всех открытых Issues/PR | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-labels.md](/.github/.instructions/labels/validation-labels.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-labels.md#чек-лист](/.github/.instructions/labels/validation-labels.md#чек-лист)

## Примеры

```
/labels-validate --file
/labels-validate --sync
/labels-validate --issue 123
/labels-validate --all
/labels-validate --file --sync
```
