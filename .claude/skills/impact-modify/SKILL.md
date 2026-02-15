---
name: impact-modify
description: Изменение документа импакт-анализа SDD — обновление контента, разрешение маркеров, перевод DRAFT в WAITING. Используй при изменении существующего импакт-анализа.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<путь> [--status WAITING]"
---

# Изменение импакт-анализа

**SSOT:** [modify-impact.md](/specs/.instructions/impact/modify-impact.md)

## Формат вызова

```
/impact-modify <путь> [--status WAITING]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу импакт-анализа | Да |
| `--status` | Перевести в указанный статус (только WAITING) | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-impact.md](/specs/.instructions/impact/modify-impact.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-impact.md#чек-лист](/specs/.instructions/impact/modify-impact.md#чек-лист)

## Примеры

```
/impact-modify specs/impact/impact-0001-oauth2-authorization.md
/impact-modify specs/impact/impact-0001-oauth2-authorization.md --status WAITING
/impact-modify specs/impact/impact-0005-cache-race-conditions.md
```
