---
name: links-validate
description: Валидация ссылок между markdown-документами — проверка frontmatter-полей, якорных ссылок и путей. Используй после рефакторинга, переименования файлов или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--path <файл/папка>] [--json]"
---

# Валидация ссылок

**SSOT:** [validation-links.md](/.structure/.instructions/validation-links.md)

## Формат вызова

```
/links-validate [--path <файл/папка>] [--json]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--path` | Файл или папка для проверки | Весь проект |
| `--json` | JSON-вывод | false |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать:
> - [validation-links.md](/.structure/.instructions/validation-links.md)
> - [standard-links.md](/.structure/.instructions/standard-links.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-links.md#чек-лист](/.structure/.instructions/validation-links.md#чек-лист)

## Примеры

```
/links-validate
/links-validate --path specs/docs/README.md
/links-validate --path .structure/ --json
```
