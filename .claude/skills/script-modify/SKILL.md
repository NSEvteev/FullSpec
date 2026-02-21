---
name: script-modify
description: Обновление логики, рефакторинг или удаление Python-скрипта автоматизации. Используй при изменении поведения скрипта, добавлении новых проверок, исправлении ошибок или удалении устаревшего скрипта.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: "<путь> [--action <тип>]"
---

# Изменение скрипта

**SSOT:** [modify-script.md](/.instructions/modify-script.md)

## Формат вызова

```
/script-modify <путь> [--action <тип>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к скрипту | Да |
| `--action` | Тип: update, refactor, delete | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-script.md](/.instructions/modify-script.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции:
- Обновление → секция "Обновление"
- Рефакторинг → секция "Рефакторинг"
- Удаление → секция "Удаление"

## Чек-лист

→ См. [modify-script.md#чек-лист](/.instructions/modify-script.md#чек-лист)

## Примеры

```
/script-modify .instructions/.scripts/validate-api.py --action update
/script-modify .instructions/.scripts/old-script.py --action delete
```
