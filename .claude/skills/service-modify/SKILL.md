---
name: service-modify
description: Изменение specs/docs/{svc}.md — обновление секций, деактивация при удалении сервиса, миграция при переименовании. Используй при изменении API, Data Model, зависимостей или Tech Stack сервиса.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<service-name> [--scenario <1-6>]"
---

# Изменение сервисной документации

**SSOT:** [modify-service.md](/specs/.instructions/docs/service/modify-service.md)

## Формат вызова

```
/service-modify <service-name> [--scenario <1-6>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `service-name` | Имя сервиса (kebab-case) | Да |
| `--scenario` | Сценарий: 1 (endpoint), 2 (Data Model), 3 (зависимости), 4 (Tech Stack), 5 (analysis/ DONE), 6 (новый analysis/) | Нет (определит по триггеру) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-service.md](/specs/.instructions/docs/service/modify-service.md)

> ⚠️ **Шаблон** — форматы секций в [standard-service.md § 3](/specs/.instructions/docs/service/standard-service.md#3-секции).

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-service.md#чек-лист](/specs/.instructions/docs/service/modify-service.md#чек-лист)

## Примеры

```
/service-modify auth --scenario 1
/service-modify notification --scenario 2
/service-modify billing
```
