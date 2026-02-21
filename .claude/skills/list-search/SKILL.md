---
name: list-search
description: Поиск по всей документации проекта — инструкции, скиллы, агенты, правила, README и скрипты. Используй при поиске документов по ключевым словам, для навигации по проекту или перед созданием нового объекта (проверка дубликатов).
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep
argument-hint: "[--type <type>] [--search <query>] [--json]"
---

# Поиск по документации

**SSOT:** [standard-search.md](/.structure/.instructions/standard-search.md)

## Формат вызова

```
/list-search [--type <type>] [--search <query>] [--json]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--type` | Тип: instruction, skill, agent, rule, readme, script, all | all |
| `--search` | Поисковый запрос (case-insensitive) | — |
| `--json` | JSON вывод | false |

## Воркфлоу

> **Перед выполнением** прочитать: [standard-search.md](/.structure/.instructions/standard-search.md)

Запустить единый поиск:

```bash
python .instructions/.scripts/search-docs.py [--type <type>] [--search <query>] [--json]
```

Вывести результаты пользователю.

## Чек-лист

> См. [standard-search.md#4-скрипты-поиска](/.structure/.instructions/standard-search.md#4-скрипты-поиска)

## Примеры

```
/list-search --search "валидация"
/list-search --type skill --search "создание"
/list-search --type readme --json
/list-search --type all --json
```
