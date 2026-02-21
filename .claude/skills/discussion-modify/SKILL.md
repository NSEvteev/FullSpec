---
name: discussion-modify
description: Изменение документа дискуссии SDD — обновление контента, разрешение маркеров, принятие предложений, перевод DRAFT в WAITING. Используй при изменении существующей дискуссии.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<путь> [--status WAITING]"
---

# Изменение дискуссии

**SSOT:** [modify-discussion.md](/specs/.instructions/analysis/discussion/modify-discussion.md)

## Формат вызова

```
/discussion-modify <путь> [--status WAITING]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к документу дискуссии | Да |
| `--status` | Перевести в указанный статус (только WAITING) | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-discussion.md](/specs/.instructions/analysis/discussion/modify-discussion.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-discussion.md#чек-лист](/specs/.instructions/analysis/discussion/modify-discussion.md#чек-лист)

## Примеры

```
/discussion-modify specs/analysis/0001-oauth2-authorization/discussion.md
/discussion-modify specs/analysis/0001-oauth2-authorization/discussion.md --status WAITING
/discussion-modify specs/analysis/0005-cache-race-conditions/discussion.md
```
