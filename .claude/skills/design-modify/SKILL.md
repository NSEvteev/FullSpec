---
name: design-modify
description: Изменение документа проектирования SDD — обновление контента, разрешение маркеров, перевод DRAFT в WAITING, откат артефактов. Используй при изменении существующего проектирования.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<путь> [--status WAITING]"
---

# Изменение проектирования

**SSOT:** [modify-design.md](/specs/.instructions/analysis/design/modify-design.md)

## Формат вызова

```
/design-modify <путь> [--status WAITING]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу проектирования | Да |
| `--status` | Перевести в указанный статус (только WAITING) | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-design.md](/specs/.instructions/analysis/design/modify-design.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-design.md#чек-лист](/specs/.instructions/analysis/design/modify-design.md#чек-лист)

## Примеры

```
/design-modify specs/analysis/0001-oauth2-authorization/design.md
/design-modify specs/analysis/0001-oauth2-authorization/design.md --status WAITING
/design-modify specs/analysis/0005-cache-optimization/design.md
```
