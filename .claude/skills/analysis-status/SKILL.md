---
name: analysis-status
description: Отображение статусов analysis chain цепочек (одна/все/dashboard). Используй для мониторинга прогресса analysis chain или обновления dashboard в README.
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
ssot-version: v1.0
argument-hint: "[NNNN] [--all] [--update]"
---

# Статус analysis chain

**SSOT:** [analysis-status.py](/specs/.instructions/.scripts/analysis-status.py)

## Формат вызова

```
/analysis-status <NNNN>       # Статус одной цепочки
/analysis-status --all         # Статус всех цепочек
/analysis-status --update      # Обновить dashboard в README
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<NNNN>` | Номер analysis chain | Нет (если --all/--update) |
| `--all` | Показать все цепочки | Нет |
| `--update` | Обновить dashboard в README | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [analysis-status.py](/specs/.instructions/.scripts/analysis-status.py)

1. Выполнить скрипт analysis-status.py с переданными параметрами.
2. **Авто-предложение (только при `<NNNN>`):** после вывода статуса одной цепочки — предложить продолжить через AskUserQuestion: «Продолжить цепочку NNNN? → /chain --resume».

## Чек-лист

- [ ] Указан хотя бы один параметр (NNNN, --all или --update)
- [ ] Скрипт выполнен без ошибок
- [ ] При `--update` — README обновлён корректно

## Примеры

```
/analysis-status 0001
/analysis-status --all
/analysis-status --update
```
