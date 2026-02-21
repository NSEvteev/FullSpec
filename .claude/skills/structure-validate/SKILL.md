---
name: structure-validate
description: Проверка согласованности SSOT структуры проекта — README, .instructions/, дерево папок, ссылки. Используй после изменения структуры, при аудите проекта или перед релизом для проверки целостности.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--json]"
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
