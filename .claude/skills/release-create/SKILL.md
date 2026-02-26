---
name: release-create
description: Создание GitHub Release — проверка chains, pre-release валидация, Release Notes, публикация, CHANGELOG. Используй при подготовке нового релиза или для hotfix.
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion
ssot-version: v1.0
argument-hint: "[--draft] [--skip-tests] [--skip-chains]"
---

# Создание Release

**SSOT:** [create-release.md](/.github/.instructions/releases/create-release.md)

## Формат вызова

```
/release-create [--draft] [--skip-tests] [--skip-chains]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--draft` | Draft Release (публикация позже) | Нет |
| `--skip-tests` | Hotfix: пропустить make test | Нет |
| `--skip-chains` | Hotfix: пропустить проверку analysis chains | Нет |

## Воркфлоу

> **Перед выполнением** прочитать [create-release.md](/.github/.instructions/releases/create-release.md)

> **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-release.md#чек-лист](/.github/.instructions/releases/create-release.md#чек-лист)

## Примеры

```
/release-create
/release-create --draft
/release-create --skip-tests --skip-chains
```
