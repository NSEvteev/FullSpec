---
name: service-create
description: Создание нового specs/docs/{svc}.md — per-service документа с 10 секциями по стандарту. Используй при появлении нового сервиса или перед началом работы с сервисом без документации.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "[service-name]"
---

# Создание сервисной документации

**SSOT:** [create-service.md](/specs/.instructions/docs/service/create-service.md)

## Формат вызова

```
/service-create [service-name]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `service-name` | Имя сервиса (kebab-case, совпадает с `src/{service}/`) | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-service.md](/specs/.instructions/docs/service/create-service.md)

> ⚠️ **Шаблон** — взять из [standard-service.md § 5](/specs/.instructions/docs/service/standard-service.md#5-шаблон). Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-service.md#чек-лист](/specs/.instructions/docs/service/create-service.md#чек-лист)

## Примеры

```
/service-create auth
/service-create notification
/service-create api-gateway
```
