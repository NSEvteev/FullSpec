---
name: instruction-create
description: Создание новой инструкции по стандарту
standard: .claude/.instructions/skills/standard-skill.md
allowed-tools: Read, Write, Edit, Glob, Grep
triggers:
  commands:
    - /instruction-create
  phrases:
    ru:
      - создай инструкцию
      - новая инструкция
    en:
      - create instruction
---

# Создание инструкции

**SSOT:** [create-instruction.md](/.instructions/create-instruction.md)

## Формат вызова

```
/instruction-create [имя] [--path <область>] [--dry-run]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `имя` | Имя инструкции (kebab-case) | Нет (спросит) |
| `--path` | Область: `/.instructions/`, `/src/.instructions/` и т.д. | Нет (спросит) |
| `--dry-run` | Показать план без выполнения | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-instruction.md](/.instructions/create-instruction.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-instruction.md#5-чек-лист](/.instructions/create-instruction.md#5-чек-лист)

## Примеры

```
/instruction-create error-handling
/instruction-create api-versioning --path /src/.instructions/
/instruction-create naming --dry-run
```

