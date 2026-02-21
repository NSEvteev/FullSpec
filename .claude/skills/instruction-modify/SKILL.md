---
name: instruction-modify
description: Обновление содержания, деактивация или миграция инструкции. Используй при изменении процесса, переименовании файла, обновлении standard-version или выводе инструкции из эксплуатации.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: "<путь> [--deactivate] [--migrate <новый-путь>]"
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

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции:
- Обновление → секция "1. Обновление инструкции"
- Деактивация → секция "2. Деактивация инструкции"
- Миграция → секция "3. Миграция инструкции"

## Чек-лист

→ См. [modify-instruction.md#чек-лист](/.instructions/modify-instruction.md#чек-лист)

## Примеры

```
/instruction-modify /.instructions/naming.md
/instruction-modify /src/.instructions/api.md --deactivate
/instruction-modify /old/path.md --migrate /new/path.md
```

