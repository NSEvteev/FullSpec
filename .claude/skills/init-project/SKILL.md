---
name: init-project
description: Инициализация проекта — GitHub Labels, Security, docs/, pre-commit, customization. Используй при настройке нового проекта или для healthcheck существующего.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion
argument-hint: "[--check] [--skip-github] [--skip-docs] [--skip-setup]"
---

# Инициализация проекта

**SSOT:** [create-initialization.md](/.structure/.instructions/create-initialization.md)

## Формат вызова

```
/init-project [--check] [--skip-github] [--skip-docs] [--skip-setup]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--check` | Только проверка, без мутаций (healthcheck) | Нет |
| `--skip-github` | Пропустить GitHub-шаги (4–7) | Нет |
| `--skip-docs` | Пропустить проверку docs/ (шаг 8) | Нет |
| `--skip-setup` | Пропустить make setup (шаг 1) | Нет |

## Воркфлоу

> **Перед выполнением** прочитать [create-initialization.md](/.structure/.instructions/create-initialization.md)

> **Шаблон** — найти пример в SSOT (секция "Шаг 10"), скопировать структуру отчёта. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-initialization.md#чек-лист](/.structure/.instructions/create-initialization.md#чек-лист)

## Примеры

```
/init-project
/init-project --check
/init-project --skip-github
/init-project --check --skip-docs
```
