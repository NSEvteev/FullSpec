---
name: labels-modify
description: Изменение меток GitHub (добавление, удаление, переименование)
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash, Glob, Grep, Edit
triggers:
  commands:
    - /labels-modify
  phrases:
    ru:
      - изменить метку
      - добавить метку
      - удалить метку
      - переименовать метку
    en:
      - modify label
      - add label
      - delete label
      - rename label
---

# Изменение меток

**SSOT:** [modify-labels.md](/.github/.instructions/labels/modify-labels.md)

## Формат вызова

```
/labels-modify <действие> [аргументы]
```

| Действие | Формат | Описание |
|----------|--------|----------|
| `add-category` | `add-category <prefix> --color <HEX>` | Добавить категорию |
| `add-label` | `add-label <category>:<value> --desc "<описание>" --color <HEX>` | Добавить метку |
| `update` | `update <name> [--desc "<описание>"] [--color <HEX>]` | Обновить метку |
| `rename` | `rename <old-name> <new-name>` | Переименовать метку |
| `rename-category` | `rename-category <old-cat> <new-cat>` | Переименовать категорию |
| `delete` | `delete <name>` | Удалить метку |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-labels.md](/.github/.instructions/labels/modify-labels.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции для выбранного действия:
- [Добавление категории](/.github/.instructions/labels/modify-labels.md#добавление-категории)
- [Добавление метки](/.github/.instructions/labels/modify-labels.md#добавление-метки)
- [Обновление метки](/.github/.instructions/labels/modify-labels.md#обновление-метки)
- [Переименование метки](/.github/.instructions/labels/modify-labels.md#переименование-метки)
- [Переименование категории](/.github/.instructions/labels/modify-labels.md#переименование-категории)
- [Удаление метки](/.github/.instructions/labels/modify-labels.md#удаление-метки)

## Чек-лист

→ См. [modify-labels.md#чек-лист](/.github/.instructions/labels/modify-labels.md#чек-лист)

## Примеры

```
/labels-modify add-label area:mobile --desc "📱 Мобильное приложение" --color "10B981"
/labels-modify rename area:infra area:platform
/labels-modify delete area:legacy
/labels-modify update area:api --desc "🔌 REST API и GraphQL"
/labels-modify rename-category area scope
```
