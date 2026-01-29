---
name: skill-modify
description: Обновление, деактивация и миграция существующих скиллов
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
triggers:
  commands:
    - /skill-modify
  phrases:
    ru:
      - измени скилл
      - обнови скилл
      - деактивируй скилл
      - мигрируй скилл
    en:
      - modify skill
      - update skill
---

# Изменение скилла

**SSOT:** [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

## Формат вызова

```
/skill-modify <название> [--action <тип>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `название` | Имя скилла | Да |
| `--action` | Тип: update, deactivate, migrate | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-skill.md#чек-лист](/.claude/.instructions/skills/modify-skill.md#чек-лист)

## Примеры

```
/skill-modify links-validate --action update
/skill-modify old-skill --action deactivate
/skill-modify old-name --action migrate
```
