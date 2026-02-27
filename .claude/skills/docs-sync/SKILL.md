---
name: docs-sync
description: Синхронизация specs/docs/ после аналитической цепочки — оркестрация service-agent, technology-agent, system-agent с ревью. Используй после Plan Dev (все 4 документа в WAITING) для создания per-service docs, per-tech стандартов и обновления overview.md.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.3
argument-hint: "<design-path>"
---

# Синхронизация docs/

**SSOT:** [create-docs-sync.md](/specs/.instructions/create-docs-sync.md)

## Формат вызова

```
/docs-sync <design-path>
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `design-path` | Путь к design.md в WAITING | Да |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-docs-sync.md](/specs/.instructions/create-docs-sync.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Шаги"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-docs-sync.md#чек-лист](/specs/.instructions/create-docs-sync.md#чек-лист)

## Примеры

```
/docs-sync specs/analysis/0001-task-dashboard/design.md
/docs-sync specs/analysis/0002-auth-flow/design.md
```
