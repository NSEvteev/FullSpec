---
name: chain-done
description: Завершение analysis chain — pre-flight проверки, T7 DONE каскад, перенос Planned Changes в AS IS, system-agent mode=done, cross-chain, отчёт. Используй при переводе цепочки из REVIEW в DONE.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.3
argument-hint: "<NNNN>"
---

# Завершение analysis chain

**SSOT:** [create-chain-done.md](/specs/.instructions/create-chain-done.md)

## Формат вызова

```
/chain-done <NNNN>
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `NNNN` | Номер analysis chain (4 цифры) | Да |

## Воркфлоу

> **Перед выполнением** прочитать [create-chain-done.md](/specs/.instructions/create-chain-done.md)

> **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

-> Выполнить шаги из SSOT-инструкции.

## Чек-лист

-> См. [create-chain-done.md#чек-лист](/specs/.instructions/create-chain-done.md#чек-лист)

## Примеры

```
/chain-done 0001
/chain-done 0042
```
