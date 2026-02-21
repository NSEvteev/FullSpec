---
name: agent-validate
description: Проверка AGENT.md на соответствие стандарту — frontmatter, промпт, секции, ссылки. Используй после создания или изменения агента, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[путь] [--all]"
---

# Валидация агента

**SSOT:** [validation-agent.md](/.claude/.instructions/agents/validation-agent.md)

## Формат вызова

```
/agent-validate [путь] [--all]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к .yaml файлу или директории | Нет (по умолчанию .claude/agents/) |
| `--all` | Проверить все агенты | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-agent.md](/.claude/.instructions/agents/validation-agent.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-agent.md#чек-лист](/.claude/.instructions/agents/validation-agent.md#чек-лист)

## Примеры

```
/agent-validate .claude/agents/todo-finder.yaml
/agent-validate --all
/agent-validate
```
