---
name: agent-modify
description: Обновление конфигурации, деактивация или переименование агента. Используй при изменении промпта агента, смене модели, деактивации устаревшего агента или миграции на новое имя.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Write, Bash, Glob, Grep, Edit
argument-hint: "<имя> [--type <тип>]"
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
