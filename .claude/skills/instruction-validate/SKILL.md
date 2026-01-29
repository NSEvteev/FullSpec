---
name: instruction-validate
description: Валидация формата и структуры инструкций
allowed-tools: Read, Bash, Glob, Grep
triggers:
  commands:
    - /instruction-validate
  phrases:
    ru:
      - проверь инструкцию
      - валидируй инструкцию
    en:
      - validate instruction
---

# Валидация инструкции

**SSOT:** [validation-instruction.md](/.instructions/validation-instruction.md)

## Формат вызова

```
/instruction-validate [путь] [--all] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к инструкции | Нет (если --all) |
| `--all` | Проверить все инструкции | Нет |
| `--json` | JSON вывод | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-instruction.md](/.instructions/validation-instruction.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-instruction.md#чек-лист](/.instructions/validation-instruction.md#чек-лист)

## Примеры

```
/instruction-validate .instructions/standard-api.md
/instruction-validate --all
/instruction-validate .claude/.instructions/skills/create-skill.md --json
```
