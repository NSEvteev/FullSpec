---
name: service-create
description: Создание сервисного документа services/{svc}.md (заглушка) при Design → WAITING. Используй при первом появлении нового сервиса в Design для создания заглушки с Резюме и Planned Changes.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "[service-name]"
---

# Создание сервисной документации

**SSOT:** [create-service.md](/specs/.instructions/living-docs/service/create-service.md)

## Формат вызова

```
/service-create [service-name] [--design <path>] [--impact <path>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `service-name` | Имя сервиса (kebab-case, совпадает с `src/{service}/`) | Нет (спросит) |
| `--design` | Путь к Design-документу (источник Dependencies, INT-N) | Нет (извлекается из контекста) |
| `--impact` | Путь к parent Impact-документу (источник API-N, DATA-N) | Нет (извлекается из контекста) |

При наличии `--design` и `--impact` — секции 2 (API контракты), 3 (Data Model), 5 (Внешние зависимости) заполняются предварительными данными из Impact/Design с маркером `*Предварительно (Design → WAITING). Финализируется при ADR → DONE.*`.

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-service.md](/specs/.instructions/living-docs/service/create-service.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-service.md#чек-лист](/specs/.instructions/living-docs/service/create-service.md#чек-лист)

## Примеры

```
/service-create auth
/service-create auth --design specs/design/design-0001-oauth2.md --impact specs/impact/impact-0001-oauth2.md
/service-create billing
/service-create notification-gateway
```
