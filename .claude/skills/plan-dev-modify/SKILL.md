---
name: plan-dev-modify
description: Изменение документа плана разработки SDD — обновление TASK-N, разрешение маркеров, перевод DRAFT в WAITING, рабочие правки при RUNNING, обработка CONFLICT с синхронизацией Issues. Используй при изменении существующего плана разработки.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<путь> [--status WAITING]"
---

# Изменение плана разработки

**SSOT:** [modify-plan-dev.md](/specs/.instructions/analysis/plan-dev/modify-plan-dev.md)

## Формат вызова

```
/plan-dev-modify <путь> [--status WAITING]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу плана разработки | Да |
| `--status` | Перевести в указанный статус (только WAITING) | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-plan-dev.md](/specs/.instructions/analysis/plan-dev/modify-plan-dev.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-plan-dev.md#чек-лист](/specs/.instructions/analysis/plan-dev/modify-plan-dev.md#чек-лист)

## Примеры

```
/plan-dev-modify specs/analysis/0001-oauth2-authorization/plan-dev.md
/plan-dev-modify specs/analysis/0001-oauth2-authorization/plan-dev.md --status WAITING
/plan-dev-modify specs/analysis/0005-cache-optimization/plan-dev.md
```
