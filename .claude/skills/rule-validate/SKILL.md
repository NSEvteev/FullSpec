---
name: rule-validate
description: Валидация формата и структуры rule
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash
argument-hint: "[имя] [--all]"
---

# Валидация rule

**SSOT:** [validation-rule.md](/.claude/.instructions/rules/validation-rule.md)

## Формат вызова

```
/rule-validate [имя] [--all]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `имя` | Имя rule без расширения (например: `core`) | Нет (спросит) |
| `--all` | Валидировать все rules в `/.claude/rules/` | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-rule.md](/.claude/.instructions/rules/validation-rule.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-rule.md#чек-лист](/.claude/.instructions/rules/validation-rule.md#чек-лист)

## Примеры

```
/rule-validate core
/rule-validate rules
/rule-validate --all
```
