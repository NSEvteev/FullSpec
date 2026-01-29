---
name: structure-modify
description: Изменение папки — переименование, перемещение, удаление
standard: .claude/.instructions/skills/standard-skill.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
triggers:
  commands:
    - /structure-modify
  phrases:
    ru:
      - переименуй папку
      - перемести папку
      - удали папку
    en:
      - rename folder
      - move folder
      - delete folder
---

# Изменение папки

**SSOT:** [modify-structure.md](/.structure/.instructions/modify-structure.md)

## Формат вызова

```
/structure-modify <операция> <аргументы>
```

| Операция | Формат | Описание |
|----------|--------|----------|
| `rename` | `rename <старое> <новое>` | Переименовать |
| `move` | `move <путь> <новый_родитель>` | Переместить |
| `delete` | `delete <путь>` | Удалить |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-structure.md](/.structure/.instructions/modify-structure.md)

→ Выполнить шаги из SSOT-инструкции для выбранной операции:
- [Переименование](/.structure/.instructions/modify-structure.md#переименование)
- [Перемещение](/.structure/.instructions/modify-structure.md#перемещение)
- [Удаление](/.structure/.instructions/modify-structure.md#удаление)

## Чек-лист

→ См. [modify-structure.md#чек-лист](/.structure/.instructions/modify-structure.md#чек-лист)

## Примеры

```
/structure-modify rename utils helpers
/structure-modify move src/common shared/libs
/structure-modify delete legacy
```
