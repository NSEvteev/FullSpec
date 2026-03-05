---
name: test-ui
description: Playwright UI smoke-тесты — делегирует test-ui-agent (playwright-cli), скриншоты, отчёт PASS/FAIL. Используй после /test (шаг 5.3).
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Agent
argument-hint: ""
---

# Playwright UI smoke-тесты

**SSOT:** [create-test-ui.md](/specs/.instructions/create-test-ui.md)

## Формат вызова

```
/test-ui
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------
| — | Без параметров | — |

## Воркфлоу

> **Перед выполнением** прочитать [create-test-ui.md](/specs/.instructions/create-test-ui.md)

> **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

-> Выполнить шаги из SSOT-инструкции.

## Чек-лист

-> См. [create-test-ui.md#чек-лист](/specs/.instructions/create-test-ui.md#чек-лист)

## Примеры

```
/test-ui
```
