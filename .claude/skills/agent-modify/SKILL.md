---
name: agent-modify
description: Изменение, деактивация и миграция агентов
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Write, Bash, Glob, Grep, Edit
triggers:
  commands:
    - /agent-modify
  phrases:
    ru:
      - измени агента
      - обнови агента
    en:
      - modify agent
---

# Изменение агента

**SSOT:** [modify-agent.md](/.claude/.instructions/agents/modify-agent.md)

## Формат вызова

```
/agent-modify <имя> [--type <тип>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<имя>` | Имя агента без расширения | Да |
| `--type` | Тип изменения: update, deactivate, migrate | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-agent.md](/.claude/.instructions/agents/modify-agent.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-agent.md#чек-лист](/.claude/.instructions/agents/modify-agent.md#чек-лист)

## Примеры

```
/agent-modify todo-finder --type update
/agent-modify old-checker --type deactivate
/agent-modify todo-finder --type migrate
```
