---
name: skill-create
description: Создание нового скилла по шаблону
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
category: skill-management
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

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-skill.md#5-чек-лист](/.claude/.instructions/skills/create-skill.md#5-чек-лист)

## Примеры

```
/skill-create links-validate
/skill-create spec-archive --dry-run
```

