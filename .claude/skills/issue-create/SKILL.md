---
name: issue-create
description: Создание GitHub Issue по стандарту
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.1
allowed-tools: Read, Bash, Glob, Grep
triggers:
  commands:
    - /issue-create
  phrases:
    ru:
      - создать issue
      - создать задачу
      - новый issue
    en:
      - create issue
      - new issue
---

# Создание Issue

**SSOT:** [create-issue.md](/.github/.instructions/issues/create-issue.md)

## Формат вызова

```
/issue-create [--template <name>] [--title <title>] [--milestone <title>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--template` | Имя шаблона (bug-report, feature-request, task, docs, refactor, question) | Нет (спросит) |
| `--title` | Заголовок Issue | Нет (спросит) |
| `--milestone` | Milestone для привязки | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-issue.md](/.github/.instructions/issues/create-issue.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-issue.md#чек-лист](/.github/.instructions/issues/create-issue.md#чек-лист)

## Примеры

```
/issue-create --template bug-report
/issue-create --title "Добавить авторизацию" --milestone "v1.0.0"
/issue-create --template task
```
