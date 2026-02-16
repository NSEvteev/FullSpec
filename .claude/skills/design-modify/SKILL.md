---
name: design-modify
description: Изменение документа проектирования SDD — обновление контента, разрешение маркеров, перевод DRAFT в WAITING, откат артефактов. Используй при изменении существующего проектирования.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<путь> [--status WAITING]"
---

# Изменение проектирования

**SSOT:** [modify-design.md](/specs/.instructions/design/modify-design.md)

## Формат вызова

```
/design-modify <путь> [--status WAITING]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу проектирования | Да |
| `--status` | Перевести в указанный статус (только WAITING) | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-design.md](/specs/.instructions/design/modify-design.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-design.md#чек-лист](/specs/.instructions/design/modify-design.md#чек-лист)

## Примеры

```
/design-modify specs/design/design-0001-oauth2-service-design.md
/design-modify specs/design/design-0001-oauth2-service-design.md --status WAITING
/design-modify specs/design/design-0005-cache-optimization.md
```
