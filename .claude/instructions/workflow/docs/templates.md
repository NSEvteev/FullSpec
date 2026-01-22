---
type: standard
description: Шаблоны документации для различных типов файлов
governed-by: docs/README.md
related:
  - docs/structure.md
  - docs/rules.md
---

# Шаблоны документации

Шаблоны для документирования различных типов файлов в `/doc/`.

## Оглавление

- [Файлы шаблонов](#файлы-шаблонов)
- [Выбор шаблона](#выбор-шаблона)
- [Связанные инструкции](#связанные-инструкции)

---

## Файлы шаблонов

> **SSOT:** Шаблоны находятся в [/.claude/templates/docs/](/.claude/templates/docs/)

| Шаблон | Файл | Назначение |
|--------|------|------------|
| Backend | [backend-template.md](/.claude/templates/docs/backend-template.md) | handlers, services, controllers |
| Database | [database-template.md](/.claude/templates/docs/database-template.md) | schema, migrations |
| Frontend | [frontend-template.md](/.claude/templates/docs/frontend-template.md) | components, pages |
| Minimal | [minimal-template.md](/.claude/templates/docs/minimal-template.md) | утилиты, константы |

---

## Выбор шаблона

| Тип файла | Шаблон |
|-----------|--------|
| `handlers.ts`, `services.py`, `controllers.go` | Backend |
| `schema.sql`, `migrations/*.sql` | Database |
| `*.tsx`, `*.vue`, `pages/*.ts` | Frontend |
| `utils.ts`, `constants.py`, `helpers.go` | Minimal |

**Правило:** Если файл не подходит ни под один шаблон — используйте Minimal.

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/docs-create](/.claude/skills/docs-create/SKILL.md) | Создание документации |
| [/docs-update](/.claude/skills/docs-update/SKILL.md) | Обновление документации |
| [/docs-delete](/.claude/skills/docs-delete/SKILL.md) | Удаление документации |

---

## Связанные инструкции

- [structure.md](./structure.md) — структура /doc/, workflow документации
- [/.claude/templates/README.md](/.claude/templates/README.md) — SSOT шаблоны

---

> **Путь:** `/.claude/instructions/docs/templates.md`
