---
name: skill-validate
description: Проверка SKILL.md на соответствие стандарту — frontmatter, секции, SSOT-ссылка, размер. Используй после создания или изменения скилла, при code review или массовой валидации всех скиллов.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[название] [--all] [--json]"
---

# Валидация скилла

**SSOT:** [validation-skill.md](/.claude/.instructions/skills/validation-skill.md)

## Формат вызова

```
/skill-validate [название] [--all] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `название` | Имя скилла для проверки | Нет (если --all) |
| `--all` | Проверить все скиллы | Нет |
| `--json` | Вывод в формате JSON | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-skill.md](/.claude/.instructions/skills/validation-skill.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-skill.md#чек-лист](/.claude/.instructions/skills/validation-skill.md#чек-лист)

## Примеры

```
/skill-validate structure-create
/skill-validate --all
/skill-validate links-validate --json
```
