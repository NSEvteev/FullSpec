---
name: rollback-chain
description: Откат analysis chain (ROLLING_BACK → REJECTED) — 5 фаз оркестрации, валидация артефактов, отчёт, подтверждение пользователя. Используй при откате цепочки из RUNNING/WAITING в REJECTED.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.3
argument-hint: "<NNNN>"
---

# Откат analysis chain

**SSOT:** [create-rollback.md](/specs/.instructions/create-rollback.md)

## Формат вызова

```
/rollback-chain <NNNN>
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `NNNN` | Номер analysis chain (4 цифры) | Да |

## Воркфлоу

> **Перед выполнением** прочитать [create-rollback.md](/specs/.instructions/create-rollback.md)

> **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

-> Выполнить шаги из SSOT-инструкции (5 фаз: основной LLM → rollback-agent → валидация → AskUserQuestion → REJECTED + README).

## Чек-лист

-> См. [create-rollback.md#чек-лист](/specs/.instructions/create-rollback.md#чек-лист)

## Примеры

```
/rollback-chain 0001
/rollback-chain 0042
```
