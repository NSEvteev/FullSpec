---
name: hotfix
description: Процесс хотфикса — диагностика бага/инцидента, impact analysis, параллельное исправление кода и документации. Используй при багах, production-инцидентах, bundle мелких фиксов.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.0
argument-hint: "[--resume]"
---

# Процесс хотфикса

**SSOT:** [create-hotfix.md](/specs/.instructions/hotfixes/create-hotfix.md)

## Формат вызова

```
/hotfix              — Новый хотфикс
/hotfix --resume     — Продолжить существующий хотфикс
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--resume` | Продолжить существующий хотфикс | Нет |

## Воркфлоу

> Перед выполнением прочитать [create-hotfix.md](/specs/.instructions/hotfixes/create-hotfix.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-hotfix.md#чек-лист](/specs/.instructions/hotfixes/create-hotfix.md#чек-лист)

## Примеры

```
/hotfix
/hotfix --resume
```
