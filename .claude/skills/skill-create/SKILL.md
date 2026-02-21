---
name: skill-create
description: Создание нового скилла (SKILL.md) с frontmatter, SSOT-ссылкой и регистрацией в README. Используй при добавлении новой команды для Claude Code на базе существующей SSOT-инструкции.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "[название] [--dry-run]"
---

# Создание скилла

**SSOT:** [create-skill.md](/.claude/.instructions/skills/create-skill.md)

## Формат вызова

```
/skill-create [название] [--dry-run]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `название` | Имя в формате `{объект}-{действие}` | Нет (спросит) |
| `--dry-run` | Показать план без выполнения | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-skill.md](/.claude/.instructions/skills/create-skill.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-skill.md#чек-лист](/.claude/.instructions/skills/create-skill.md#чек-лист)

## Примеры

```
/skill-create links-validate
/skill-create spec-archive --dry-run
```

