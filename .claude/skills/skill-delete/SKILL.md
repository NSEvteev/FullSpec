---
name: skill-delete
description: Обновление существующих скиллов при удалении скилла
allowed-tools: Read, Edit, Glob, Grep, Bash
category: skill-management
triggers:
  commands:
    - /skill-delete
  phrases:
    ru:
      - удали скилл
      - очисти ссылки на скилл
    en:
      - delete skill
---

# Удаление скилла

**SSOT:** [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

## Формат вызова

```
/skill-delete <имя-скилла>
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `имя-скилла` | Имя удаляемого скилла | Да |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

→ Выполнить шаги из SSOT-инструкции (секция "Удаление скилла").

## Чек-лист

→ См. [modify-skill.md#5-чек-лист](/.claude/.instructions/skills/modify-skill.md#5-чек-лист)

## Примеры

```
/skill-delete old-skill
/skill-delete deprecated-feature
```

