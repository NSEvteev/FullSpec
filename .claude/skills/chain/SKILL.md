---
name: chain
description: Оркестратор полного цикла — создаёт TaskList от идеи до релиза по standard-process.md. Используй при запросе на добавление функциональности, изменение поведения, исправление бага или любом изменении системы.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.3
argument-hint: "[--hotfix] [--bug-bundle] [--doc-only] [--resume]"
---

# Оркестратор полного цикла

**SSOT:** [create-chain.md](/specs/.instructions/create-chain.md)

## Формат вызова

```
/chain              — Happy Path (Путь A)
/chain --hotfix     — Hotfix (Путь C.2)
/chain --bug-bundle — Bug-fix bundle (Путь C.3)
/chain --doc-only   — Doc-only (Путь C.4)
/chain --resume     — Возобновить существующий TaskList
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--hotfix` | Критический баг, метки bug/critical | Нет |
| `--bug-bundle` | Группировка мелких багов | Нет |
| `--doc-only` | Опечатки, форматирование (без chain) | Нет |
| `--resume` | Продолжить после прерывания | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-chain.md](/specs/.instructions/create-chain.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-chain.md#чек-лист](/specs/.instructions/create-chain.md#чек-лист)

## Примеры

```
/chain
/chain --hotfix
/chain --doc-only
/chain --resume
```
