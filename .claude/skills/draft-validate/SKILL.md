---
name: draft-validate
description: Проверка черновика в .claude/drafts/ на соответствие стандарту — frontmatter, структура, именование файла. Используй после создания или изменения черновика, перед коммитом.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash
argument-hint: "[путь] [--all]"
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
