---
name: structure-create
description: Создание новой папки в структуре проекта
standard: .claude/.instructions/skills/standard-skill.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
triggers:
  commands:
    - /structure-create
  phrases:
    ru:
      - создай папку
      - добавь папку
      - новая папка
    en:
      - create folder
      - add folder
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

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-structure.md#чек-лист](/.structure/.instructions/create-structure.md#чек-лист)

## Примеры

```
/structure-create docs --description "Документация проекта"
/structure-create src/utils --description "Утилиты"
```
