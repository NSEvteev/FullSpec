---
name: skill-modify
description: Обновление SSOT-ссылки, параметров или деактивация существующего скилла. Используй при изменении SSOT-инструкции, переименовании скилла или выводе из эксплуатации.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
argument-hint: "<название> [--action <тип>]"
---

# Изменение скилла

**SSOT:** [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

## Формат вызова

```
/skill-modify <название> [--action <тип>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `название` | Имя скилла | Да |
| `--action` | Тип: update, deactivate, migrate | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [modify-skill.md](/.claude/.instructions/skills/modify-skill.md)

> ⚠️ **Шаблон** — найти пример в SSOT (секция "Примеры"), скопировать структуру. Запрещено придумывать свой формат.

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [modify-skill.md#чек-лист](/.claude/.instructions/skills/modify-skill.md#чек-лист)

## Примеры

```
/skill-modify links-validate --action update
/skill-modify old-skill --action deactivate
/skill-modify old-name --action migrate
```
