---
name: service-modify
description: Изменение сервисного документа services/{svc}.md по событию SDD-lifecycle — заполнение при ADR DONE, перемещение в Changelog при Design DONE, деактивация и миграция.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<service-name> [--scenario <A|B|C|D|E|F>]"
---

# Изменение сервисной документации

**SSOT:** [modify-service.md](/specs/.instructions/living-docs/service/modify-service.md)

## Формат вызова

```
/service-modify <service-name> [--scenario <A|B|C|D|E|F>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `service-name` | Имя сервиса (kebab-case) | Да |
| `--scenario` | Сценарий: A (Design WAITING), B (ADR WAITING), C (ADR DONE заглушка→полный), D (ADR DONE последующий), E (Design DONE), F (REJECTED) | Нет (определит автоматически) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-service.md](/specs/.instructions/living-docs/service/modify-service.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-service.md#чек-лист](/specs/.instructions/living-docs/service/modify-service.md#чек-лист)

## Примеры

```
/service-modify auth --scenario C
/service-modify billing --scenario E
/service-modify auth --scenario F
```
