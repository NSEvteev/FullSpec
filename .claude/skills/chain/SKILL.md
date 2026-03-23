---
name: chain
description: Оркестратор полного цикла — создаёт TaskList от идеи до релиза по standard-process.md. Используй при запросе на добавление функциональности, изменение поведения, исправление бага или любом изменении системы.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.3
argument-hint: "[--resume]"
---

# Оркестратор полного цикла

**SSOT:** [create-chain.md](/specs/.instructions/create-chain.md)

## Формат вызова

```
/chain              — Happy Path (полная цепочка, 15 задач)
/chain --resume     — Возобновить существующий TaskList
```

> Для багов и хотфиксов — `/hotfix`.

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--resume` | Продолжить после прерывания | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-chain.md](/specs/.instructions/create-chain.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-chain.md#чек-лист](/specs/.instructions/create-chain.md#чек-лист)

## Примеры

```
/chain
/chain --resume
```
