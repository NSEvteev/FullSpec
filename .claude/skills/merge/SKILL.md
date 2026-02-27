---
name: merge
description: Merge PR с pre/post проверками, sync main и cleanup. Используй при merge PR вместо ручного gh pr merge.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "<PR-number>"
---

# Merge Pull Request

**SSOT:** [create-merge.md](/.github/.instructions/review/create-merge.md)

## Формат вызова

```
/merge <PR-number>
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<PR-number>` | Номер PR для merge | Да |

## Воркфлоу

> **Перед выполнением** прочитать [create-merge.md](/.github/.instructions/review/create-merge.md)

> **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

-> Выполнить шаги из SSOT-инструкции.

## Чек-лист

-> См. [create-merge.md#чек-лист](/.github/.instructions/review/create-merge.md#чек-лист)

## Примеры

```
/merge 42
/merge 7
```
