---
name: service-create
description: Создание сервисного документа services/{svc}.md (stub) при Design → WAITING. Используй при первом появлении нового сервиса в Design для создания файла-заглушки с Резюме и Planned Changes.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "[service-name]"
---

# Создание сервисной документации

**SSOT:** [create-service.md](/specs/.instructions/living-docs/service/create-service.md)

## Формат вызова

```
/service-create [service-name]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `service-name` | Имя сервиса (kebab-case, совпадает с `src/{service}/`) | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-service.md](/specs/.instructions/living-docs/service/create-service.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-service.md#чек-лист](/specs/.instructions/living-docs/service/create-service.md#чек-лист)

## Примеры

```
/service-create auth
/service-create billing
/service-create notification-gateway
```
