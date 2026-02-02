---
name: agent-create
description: Создание нового агента по стандарту
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.0
allowed-tools: Read, Write, Bash, Glob, Grep, Edit
triggers:
  commands:
    - /agent-create
  phrases:
    ru:
      - создай агента
      - новый агент
    en:
      - create agent
---

# Создание агента

**SSOT:** [create-agent.md](/.claude/.instructions/agents/create-agent.md)

## Формат вызова

```
/agent-create [имя] [--type <тип>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `имя` | Имя агента (kebab-case) | Нет (спросит) |
| `--type` | Тип агента: explore, bash, plan, general-purpose | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-agent.md](/.claude/.instructions/agents/create-agent.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-agent.md#чек-лист](/.claude/.instructions/agents/create-agent.md#чек-лист)

## Примеры

```
/agent-create todo-finder --type explore
/agent-create code-reviewer --type general-purpose
/agent-create test-runner --type bash
```
