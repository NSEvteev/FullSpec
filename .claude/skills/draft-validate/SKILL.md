---
name: draft-validate
description: Валидация черновика по стандарту
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.0
allowed-tools: Read, Bash
triggers:
  commands:
    - /draft-validate
  phrases:
    ru:
      - проверь черновик
      - валидируй драфт
    en:
      - validate draft
---

# Валидация черновика

**SSOT:** [validation-draft.md](/.claude/.instructions/drafts/validation-draft.md)

## Формат вызова

```
/draft-validate [путь] [--all]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `путь` | Путь к черновику для проверки | Нет (если --all) |
| `--all` | Проверить все черновики в `/.claude/drafts/` | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-draft.md](/.claude/.instructions/drafts/validation-draft.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-draft.md#чек-лист](/.claude/.instructions/drafts/validation-draft.md#чек-лист)

## Примеры

```
/draft-validate .claude/drafts/2024-01-23-auth.md
/draft-validate --all
```
