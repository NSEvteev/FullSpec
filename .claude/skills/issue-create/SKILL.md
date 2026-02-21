---
name: issue-create
description: Создание GitHub Issue с метками, milestone и описанием по стандарту проекта. Используй при постановке задачи, регистрации бага или запросе на улучшение.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[описание]"
---

# Создание Issue

**SSOT:** [create-issue.md](/.github/.instructions/issues/create-issue.md)

## Формат вызова

```
/issue-create [описание задачи или контекст]
/issue-create --template <name> --title <title> --milestone <title>
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `описание` | Свободное описание задачи/задач | Нет |
| `--template` | Имя шаблона (bug-report, task, docs, refactor) | Нет (определяется из контекста) |
| `--title` | Заголовок Issue | Нет (определяется из контекста) |
| `--milestone` | Milestone для привязки | Нет (определяется из контекста) |

## Принцип автономности

> **LLM определяет всё самостоятельно.** Шаблон, title, labels, milestone, body — всё выводится из контекста разговора. НЕ спрашивать пользователя, если контекст достаточен.

> **Batch-режим.** Если из контекста следует несколько задач — создать все Issues за один вызов. LLM сам определяет количество, типы и приоритеты.

> **Спрашивать ТОЛЬКО** когда контекст объективно недостаточен (нет информации для определения типа задачи или milestone не существует).

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-issue.md](/.github/.instructions/issues/create-issue.md)

→ Выполнить шаги из SSOT-инструкции (автономно, без подтверждений).

## Чек-лист

→ См. [create-issue.md#чек-лист](/.github/.instructions/issues/create-issue.md#чек-лист)

## Примеры

```
/issue-create Надо добавить авторизацию и настроить CI/CD
/issue-create --template bug-report --title "Ошибка загрузки файлов" --milestone "v1.0.0"
/issue-create Создать задачи для milestone v0.2.0: валидация PR, автотесты, деплой
```
