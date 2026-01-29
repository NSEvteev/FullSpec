---
name: instruction-modify
description: Обновление, деактивация и миграция инструкций
standard: .claude/.instructions/skills/standard-skill.md
allowed-tools: Read, Write, Edit, Glob, Grep
triggers:
  commands:
    - /instruction-modify
  phrases:
    ru:
      - измени инструкцию
      - обнови инструкцию
      - деактивируй инструкцию
      - мигрируй инструкцию
    en:
      - modify instruction
      - update instruction
      - deactivate instruction
---

# Изменение инструкции

**SSOT:** [modify-instruction.md](/.instructions/modify-instruction.md)

## Формат вызова

```
/instruction-modify <путь> [--deactivate] [--migrate <новый-путь>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к инструкции | Да |
| `--deactivate` | Деактивировать (не удалять) | Нет |
| `--migrate` | Переместить/переименовать | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-instruction.md](/.instructions/modify-instruction.md)

→ Выполнить шаги из SSOT-инструкции:
- Обновление → секция "1. Обновление инструкции"
- Деактивация → секция "2. Деактивация инструкции"
- Миграция → секция "3. Миграция инструкции"

## Чек-лист

→ См. [modify-instruction.md#5-чек-лист](/.instructions/modify-instruction.md#5-чек-лист)

## Примеры

```
/instruction-modify /.instructions/naming.md
/instruction-modify /src/.instructions/api.md --deactivate
/instruction-modify /old/path.md --migrate /new/path.md
```

