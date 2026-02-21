---
name: principles-validate
description: Проверка Python-кода на соответствие принципам программирования проекта — SSOT, DRY, именование, структура. Используй при code review, после написания нового кода или рефакторинга.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[путь] [--all] [--json]"
---

# Валидация принципов

**SSOT:** [validation-principles.md](/.instructions/validation-principles.md)

## Формат вызова

```
/principles-validate [путь] [--all] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к файлу или директории | Нет (если --all) |
| `--all` | Проверить все .py файлы в репозитории | Нет |
| `--json` | JSON вывод | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-principles.md](/.instructions/validation-principles.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

**Скрипт:**
```bash
python .instructions/.scripts/validate-principles.py <путь> [--all] [--json]
```

## Чек-лист

→ См. [validation-principles.md#чек-лист](/.instructions/validation-principles.md#чек-лист)

## Примеры

```
/principles-validate src/api/handlers.py
/principles-validate src/
/principles-validate --all
/principles-validate src/ --json
```
