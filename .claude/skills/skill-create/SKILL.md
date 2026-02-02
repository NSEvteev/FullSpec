---
name: skill-create
description: Создание нового скилла по шаблону
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
triggers:
  commands:
    - /skill-create
  phrases:
    ru:
      - создай скилл
      - новый скилл
    en:
      - create skill
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

