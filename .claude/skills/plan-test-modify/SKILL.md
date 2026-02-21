---
name: plan-test-modify
description: Изменение документа плана тестов SDD — обновление TC-N, разрешение маркеров, перевод DRAFT в WAITING, обработка CONFLICT. Используй при изменении существующего плана тестов.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<путь> [--status WAITING]"
---

# Изменение плана тестов

**SSOT:** [modify-plan-test.md](/specs/.instructions/analysis/plan-test/modify-plan-test.md)

## Формат вызова

```
/plan-test-modify <путь> [--status WAITING]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу плана тестов | Да |
| `--status` | Перевести в указанный статус (только WAITING) | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-plan-test.md](/specs/.instructions/analysis/plan-test/modify-plan-test.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-plan-test.md#чек-лист](/specs/.instructions/analysis/plan-test/modify-plan-test.md#чек-лист)

## Примеры

```
/plan-test-modify specs/analysis/0001-oauth2-authorization/plan-test.md
/plan-test-modify specs/analysis/0001-oauth2-authorization/plan-test.md --status WAITING
/plan-test-modify specs/analysis/0005-cache-optimization/plan-test.md
```
