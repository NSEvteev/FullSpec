---
name: technology-create
description: Создание per-tech стандарта кодирования (полностью при Design → WAITING). Используй при добавлении новой технологии в Tech Stack — запускает N technology-agent параллельно, по одному на технологию.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<technologies...>"
---

# Создание per-tech стандарта

**SSOT:** [create-technology.md](/specs/.instructions/docs/technology/create-technology.md)

## Формат вызова

```
/technology-create <technologies...> [--design <path>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `technologies` | Список технологий (например `python:3.12 fastapi:0.104`) | Да |
| `--design` | Путь к Design-документу (источник Tech Stack) | Нет (извлекается из контекста) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-technology.md](/specs/.instructions/docs/technology/create-technology.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

> ⚠️ **Параллельный запуск:** N технологий = N technology-agent параллельно, по одному на технологию.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-technology.md#чек-лист](/specs/.instructions/docs/technology/create-technology.md#чек-лист)

## Примеры

```
/technology-create python:3.12
/technology-create python:3.12 fastapi:0.104 postgresql:16 --design specs/design/design-0001-auth.md
/technology-create tailwind-css:3.4
```
