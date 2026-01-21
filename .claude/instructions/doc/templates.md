---
type: standard
description: Шаблоны документации для различных типов файлов
related:
  - doc/structure.md   # основная инструкция по документации
---

# Шаблоны документации

Шаблоны для документирования различных типов файлов в `/doc/`.

## Оглавление

- [Файлы шаблонов](#файлы-шаблонов)
- [Выбор шаблона](#выбор-шаблона)
- [Связанные инструкции](#связанные-инструкции)

---

## Файлы шаблонов

> **SSOT:** Шаблоны находятся в [/.claude/templates/doc/](/.claude/templates/doc/)

| Шаблон | Файл | Назначение |
|--------|------|------------|
| Backend | [backend-template.md](/.claude/templates/doc/backend-template.md) | handlers, services, controllers |
| Database | [database-template.md](/.claude/templates/doc/database-template.md) | schema, migrations |
| Frontend | [frontend-template.md](/.claude/templates/doc/frontend-template.md) | components, pages |
| Minimal | [minimal-template.md](/.claude/templates/doc/minimal-template.md) | утилиты, константы |

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
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Создание документации |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации |
| [/doc-delete](/.claude/skills/doc-delete/SKILL.md) | Удаление документации |

---

## Связанные инструкции

- [structure.md](./structure.md) — структура /doc/, workflow документации
- [/.claude/templates/README.md](/.claude/templates/README.md) — SSOT шаблоны

---

> **Путь:** `/.claude/instructions/doc/templates.md`
