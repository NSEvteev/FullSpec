---
name: rule-create
description: Создание нового rule-файла в .claude/rules/ с frontmatter и регистрацией. Используй при добавлении нового автоматического правила для Claude Code — контекстного или глобального.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Write
argument-hint: "[имя] [--global] [--paths <паттерны>]"
---

# Создание rule

**SSOT:** [create-rule.md](/.claude/.instructions/rules/create-rule.md)

## Формат вызова

```
/rule-create [имя] [--global] [--paths <паттерны>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `имя` | Имя rule без расширения (kebab-case) | Нет (спросит) |
| `--global` | Создать глобальный rule (без paths) | Нет |
| `--paths` | Glob-паттерны для условного rule | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-rule.md](/.claude/.instructions/rules/create-rule.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-rule.md#чек-лист](/.claude/.instructions/rules/create-rule.md#чек-лист)

## Примеры

```
/rule-create core --global
/rule-create instructions --paths "**/.instructions/**"
/rule-create skills --paths ".claude/skills/**"
```
