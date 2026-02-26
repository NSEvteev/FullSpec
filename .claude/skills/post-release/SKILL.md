---
name: post-release
description: Post-release валидация — проверка Release, Notes, CHANGELOG, деплой. Используй после создания GitHub Release для проверки корректности публикации.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "--version <vX.Y.Z> [--skip-deploy]"
---

# Post-release валидация

**SSOT:** [validation-release.md](/.github/.instructions/releases/validation-release.md)

## Формат вызова

```
/post-release --version <vX.Y.Z> [--skip-deploy] [--json]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--version` | Версия релиза (формат vX.Y.Z) | Да |
| `--skip-deploy` | Пропустить проверку деплоя | Нет |
| `--json` | Вывод в формате JSON | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [validation-release.md](/.github/.instructions/releases/validation-release.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-release.md#чек-лист](/.github/.instructions/releases/validation-release.md#чек-лист)

## Примеры

```
/post-release --version v1.0.0
/post-release --version v1.0.0 --skip-deploy
/post-release --version v1.0.0 --json
```
