---
name: skill-update
description: Обновление существующих скиллов при добавлении нового
allowed-tools: Read, Edit, Glob, Grep
category: skill-management
triggers:
  commands:
    - /skill-update
  phrases:
    ru:
      - обнови скиллы
      - интегрируй скилл
    en:
      - update skills
---

# Обновление скиллов

**SSOT:** [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

## Формат вызова

```
/skill-update <новый-скилл>
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `новый-скилл` | Имя скилла или путь к SKILL.md | Нет (последний созданный) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

→ Выполнить шаги из SSOT-инструкции (секция "Обновление скилла").

## Чек-лист

→ См. [modify-skill.md#5-чек-лист](/.claude/.instructions/skills/modify-skill.md#5-чек-лист)

## Примеры

```
/skill-update links-validate
/skill-update spec-archive
```

