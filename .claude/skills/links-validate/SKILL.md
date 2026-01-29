---
name: links-validate
description: Валидация ссылок в markdown-документах
allowed-tools: Read, Bash, Glob, Grep
triggers:
  commands:
    - /links-validate
  phrases:
    ru:
      - проверь ссылки
      - валидация ссылок
      - найди битые ссылки
    en:
      - validate links
      - check links
      - find broken links
---

# Валидация ссылок

**SSOT:** [validation-links.md](/.structure/.instructions/validation-links.md)

## Формат вызова

```
/links-validate [--path <файл/папка>] [--json]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--path` | Файл или папка для проверки | Весь проект |
| `--json` | JSON-вывод | false |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать:
> - [validation-links.md](/.structure/.instructions/validation-links.md)
> - [standard-links.md](/.structure/.instructions/standard-links.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [validation-links.md#чек-лист](/.structure/.instructions/validation-links.md#чек-лист)

## Примеры

```
/links-validate
/links-validate --path docs/README.md
/links-validate --path .structure/ --json
```
