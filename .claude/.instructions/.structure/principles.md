---
type: standard
description: Принципы организации структуры проекта
governed-by: .structure/README.md
related:
  - .structure/lifecycle.md
  - .structure/responsibilities.md
  - .structure/readme-index.md
---

# Принципы организации структуры

**Индекс:** [README.md](./README.md)

## Оглавление

- [Зеркалирование](#зеркалирование)
- [Общие правила](#общие-правила)
- [Именование](#именование)
- [SSOT](#ssot)

---

## Зеркалирование

Папка проекта `/X/` → инструкции `/.claude/.instructions/X/`

```
Папка /X/  →  Инструкции /.claude/.instructions/X/
Правила    →  Инструкции /.claude/.instructions/.claude/
```

### Примеры

| Папка проекта | Папка инструкций |
|---------------|------------------|
| `/src/` | `/.claude/.instructions/src/` |
| `/platform/` | `/.claude/.instructions/platform/` |
| `/tests/` | `/.claude/.instructions/tests/` |
| `/.github/` | `/.claude/.instructions/.github/` |
| `/.claude/` | `/.claude/.instructions/.claude/` |
| `/.structure/` | `/.claude/.instructions/.structure/` |

---

## Общие правила

1. **README.md обязателен** — каждая папка ДОЛЖНА иметь README.md как индекс
2. **SSOT в drafts/** — документы-первоисточники в `/.claude/drafts/`
3. **settings.local.json не в git** — локальные настройки игнорируются
4. **state/ не в git** — состояния агентов игнорируются

---

## Именование

### Папки

- Папки с точкой в проекте → папки с точкой в инструкциях
- Пример: `/.github/` → `/.claude/.instructions/.github/`

### Файлы

- kebab-case для всех файлов
- Расширение `.md` для инструкций
- Примеры: `api-design.md`, `error-handling.md`

---

## SSOT

**Single Source of Truth** — каждый факт хранится в одном месте.

| Тип данных | SSOT |
|------------|------|
| Структура проекта | `/.structure/project.md` |
| Маппинг инструкций | `/.structure/mapping.md` |
| Индекс инструкций | `/.claude/.instructions/README.md` |
| Глоссарий | `/specs/glossary.md` |

**Правило:** Не дублировать информацию. Ссылаться на SSOT.
