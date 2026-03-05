---
name: docker-up
description: Поднятие Docker dev-окружения — docker compose up -d --build, healthcheck всех сервисов, troubleshooting. Используй перед /test и /test-ui (шаг 5.1).
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
---

# Поднятие Docker dev-окружения

**SSOT:** [create-docker-env.md](/specs/.instructions/create-docker-env.md)

## Формат вызова

```
/docker-up
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------
| — | Без параметров | — |

## Воркфлоу

> **Перед выполнением** прочитать [create-docker-env.md](/specs/.instructions/create-docker-env.md)

> **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

-> Выполнить шаги из SSOT-инструкции.

## Чек-лист

-> См. [create-docker-env.md#чек-лист](/specs/.instructions/create-docker-env.md#чек-лист)

## Примеры

```
/docker-up
```
