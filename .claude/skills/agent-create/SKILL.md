---
name: agent-create
description: Создание нового агента (AGENT.md) с промптом, конфигурацией и регистрацией в README. Используй при добавлении нового AI-агента для автоматизации задач проекта.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Write, Bash, Glob, Grep, Edit
argument-hint: "[имя] [--type <тип>]"
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
