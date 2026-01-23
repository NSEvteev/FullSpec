---
type: standard
description: Зеркалирование папок проекта и инструкций
governed-by: .structure/README.md
---

# Зеркалирование

Связь между папками проекта и папками инструкций.

---

## Принцип

```
Папка проекта /X/  →  Инструкции /.claude/.instructions/X/
```

Каждая значимая папка проекта имеет зеркальную папку в инструкциях.

---

## Что где

| Папка проекта | Содержит | Папка инструкций | Содержит |
|---------------|----------|------------------|----------|
| `/src/` | Код сервисов | `/.claude/.instructions/src/` | Правила разработки |
| `/src/README.md` | Зона ответственности | `/.claude/.instructions/src/README.md` | Индекс правил |

**Папка проекта:** ЧТО хранится (зона ответственности)
**Папка инструкций:** КАК работать (правила для LLM)

---

## Таблица соответствий

| Папка проекта | Папка инструкций |
|---------------|------------------|
| `/src/` | `/.claude/.instructions/src/` |
| `/platform/` | `/.claude/.instructions/platform/` |
| `/tests/` | `/.claude/.instructions/tests/` |
| `/shared/` | `/.claude/.instructions/shared/` |
| `/config/` | `/.claude/.instructions/config/` |
| `/specs/` | `/.claude/.instructions/specs/` |
| `/.github/` | `/.claude/.instructions/.github/` |
| `/.claude/` | `/.claude/.instructions/.claude/` |
| `/.structure/` | `/.claude/.instructions/.structure/` |

---

## Когда создавать зеркало

Зеркало нужно для папок:
- `/src/`, `/platform/`, `/shared/`, `/tests/`, `/specs/`, `/config/`, `/.github/`
- Вложенных папок, если для них нужны отдельные правила

Зеркало НЕ нужно для:
- Папок с кодом без специфических правил (`/src/{service}/backend/v1/handlers/`)
- Временных папок
- `node_modules/`, `__pycache__/`, etc.

---

## Флоу создания зеркала

```
1. Создать папку /.claude/.instructions/{path}/
2. Создать README.md с индексом правил
```

---

## См. также

- [workflows/create-folder.md](./workflows/create-folder.md) — полный флоу создания папки
