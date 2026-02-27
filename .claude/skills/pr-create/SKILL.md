---
name: pr-create
description: Создание Pull Request с автосбором Issues из chain, формированием title/body/labels, push и preview. Используй при создании PR вместо ручного gh pr create.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[<chain-id>] [--draft]"
---

# Создание Pull Request

**SSOT:** [create-pull-request.md](/.github/.instructions/pull-requests/create-pull-request.md)

## Формат вызова

```
/pr-create [<chain-id>] [--draft]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<chain-id>` | 4-значный номер chain (0001). Если не указан — определяется из ветки | Нет |
| `--draft` | Создать Draft PR | Нет |

## Воркфлоу

> **Перед выполнением** прочитать [create-pull-request.md](/.github/.instructions/pull-requests/create-pull-request.md)

> **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

-> Выполнить шаги из SSOT-инструкции.

## Чек-лист

-> См. [create-pull-request.md#чек-лист](/.github/.instructions/pull-requests/create-pull-request.md#чек-лист)

## Примеры

```
/pr-create
/pr-create 0001
/pr-create --draft
```
