---
name: structure-modify
description: Переименование, перемещение или удаление папки в структуре проекта с обновлением всех ссылок и SSOT. Используй при реорганизации структуры, переименовании модуля или удалении устаревшего раздела.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<операция> <аргументы>"
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

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

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
