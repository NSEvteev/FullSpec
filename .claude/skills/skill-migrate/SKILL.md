---
name: skill-migrate
description: Переименование скилла с обновлением всех ссылок
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
category: skill-management
triggers:
  commands:
    - /skill-migrate
  phrases:
    ru:
      - мигрируй скилл
      - переименуй скилл
    en:
      - migrate skill
---

# Миграция скилла

**SSOT:** [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

## Формат вызова

```
/skill-migrate <old-name> <new-name> [--dry-run]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `old-name` | Текущее имя скилла | Да |
| `new-name` | Новое имя скилла | Да |
| `--dry-run` | Показать план без выполнения | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

→ Выполнить шаги из SSOT-инструкции (секция "Миграция скилла").

## Чек-лист

→ См. [modify-skill.md#5-чек-лист](/.claude/.instructions/skills/modify-skill.md#5-чек-лист)

## Примеры

```
/skill-migrate old-name new-name
/skill-migrate links-update links-sync --dry-run
```

