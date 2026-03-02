---
name: test
description: Финальная валидация — sync main, docker up, make test/lint/build/test-e2e, проверка полноты, отчёт READY/NOT READY. Используй после завершения разработки (все TASK-N done) перед ревью ветки.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: ""
---

# Финальная валидация

**SSOT:** [create-test.md](/specs/.instructions/create-test.md)

## Формат вызова

```
/test
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| — | Без параметров | — |

## Воркфлоу

> **Перед выполнением** прочитать [create-test.md](/specs/.instructions/create-test.md)

> **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

-> Выполнить шаги из SSOT-инструкции.

## Чек-лист

-> См. [create-test.md#чек-лист](/specs/.instructions/create-test.md#чек-лист)

## Примеры

```
/test
```
