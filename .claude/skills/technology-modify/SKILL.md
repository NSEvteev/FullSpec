---
name: technology-modify
description: Изменение per-tech стандарта кодирования — добавление сервиса, обновление конвенций, откат, деактивация. Используй при изменении существующего per-tech стандарта.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<tech-name> [--scenario A|B|C|D]"
---

# Изменение per-tech стандарта

**SSOT:** [modify-technology.md](/specs/.instructions/docs/technology/modify-technology.md)

## Формат вызова

```
/technology-modify <tech-name> [--scenario A|B|C|D]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `tech-name` | Имя технологии (kebab-case, например `python`) | Да |
| `--scenario` | Сценарий: A (новый сервис), B (обновление конвенций), C (откат), D (деактивация) | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-technology.md](/specs/.instructions/docs/technology/modify-technology.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-technology.md#чек-лист](/specs/.instructions/docs/technology/modify-technology.md#чек-лист)

## Примеры

```
/technology-modify python --scenario A
/technology-modify tailwind-css --scenario B
/technology-modify postgresql --scenario C
```
