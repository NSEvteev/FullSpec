---
name: rule-modify
description: Изменение, деактивация и миграция rule
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.0
allowed-tools: Read, Bash, Edit, Grep
triggers:
  commands:
    - /rule-modify
  phrases:
    ru:
      - измени rule
      - обнови rule
      - деактивируй rule
      - переименуй rule
      - измени правило
      - обнови правило
      - деактивируй правило
      - переименуй правило
    en:
      - modify rule
      - update rule
---

# Изменение rule

**SSOT:** [modify-rule.md](/.claude/.instructions/rules/modify-rule.md)

## Формат вызова

```
/rule-modify <имя> [--type <тип>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<имя>` | Имя rule без расширения | Да |
| `--type` | Тип изменения: update, deactivate, migrate | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-rule.md](/.claude/.instructions/rules/modify-rule.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-rule.md#чек-лист](/.claude/.instructions/rules/modify-rule.md#чек-лист)

## Примеры

```
/rule-modify ssot --type update
/rule-modify old-workflow --type deactivate
/rule-modify rules --type migrate
```
