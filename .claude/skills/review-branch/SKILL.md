---
name: review-branch
description: Локальное ревью текущей ветки — проверка коммитов, файлов, тестов и стандартов перед созданием PR. Используй перед git push для предварительной проверки качества изменений.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--base <branch>]"
---

# Локальное ревью ветки

**SSOT:** [validation-review.md](/.github/.instructions/review/validation-review.md)

## Формат вызова

```
/review-branch [--base <branch>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--base` | Базовая ветка для сравнения (по умолчанию `main`) | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-review.md](/.github/.instructions/review/validation-review.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить Шаги 1-3 из SSOT-инструкции (Этап 1: Review ветки).

## Чек-лист

→ См. [validation-review.md#этап-1-review-ветки](/.github/.instructions/review/validation-review.md#этап-1-review-ветки)

## Примеры

```
/review-branch
/review-branch --base develop
```
