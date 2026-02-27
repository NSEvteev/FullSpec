---
name: commit
description: Создание коммита по Conventional Commits — анализ diff, формирование message, staging, обработка hooks, push. Используй при создании коммита вместо ручного git commit.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--no-push] [--amend]"
---

# Создание коммита

**SSOT:** [create-commit.md](/.github/.instructions/commits/create-commit.md)

## Формат вызова

```
/commit [--no-push] [--amend]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--no-push` | Не делать push после коммита | Нет |
| `--amend` | Дополнить предыдущий коммит (проверяется push-статус) | Нет |

## Воркфлоу

> **Перед выполнением** прочитать [create-commit.md](/.github/.instructions/commits/create-commit.md)

> **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

-> Выполнить шаги из SSOT-инструкции.

**После успешного коммита:** выполнить `git push` (если не указан `--no-push`).

## Чек-лист

-> См. [create-commit.md#чек-лист](/.github/.instructions/commits/create-commit.md#чек-лист)

## Примеры

```
/commit
/commit --no-push
/commit --amend
```
