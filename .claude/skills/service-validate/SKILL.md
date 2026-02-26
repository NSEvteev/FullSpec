---
name: service-validate
description: Проверка specs/docs/{svc}.md на соответствие стандарту — frontmatter, 10 секций, таблицы, подсекции API/Data Model, автономия, Changelog. Используй после создания или изменения сервисного документа, при code review или перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[service-name | --all]"
---

# Валидация сервисной документации

**SSOT:** [validation-service.md](/specs/.instructions/docs/service/validation-service.md)

## Формат вызова

```
/service-validate [service-name | --all]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `service-name` | Имя сервиса (проверяет `specs/docs/{svc}.md`) | Нет |
| `--all` | Проверить все `{svc}.md` в `specs/docs/` | Нет |

Без параметров — проверяет все файлы.

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-service.md](/specs/.instructions/docs/service/validation-service.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-service.md#чек-лист](/specs/.instructions/docs/service/validation-service.md#чек-лист)

## Примеры

```
/service-validate notification
/service-validate auth
/service-validate --all
```
