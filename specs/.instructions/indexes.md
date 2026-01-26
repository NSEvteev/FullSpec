---
description: Форматы индексов README.md в /specs/ и workflow обновления
standard: .instructions/standard-instruction.md
index: specs/.instructions/README.md
---

# Индексы README.md в /specs/

Форматы таблиц в README.md индексах для разных типов документов и алгоритм обновления.

**Полезные ссылки:**
- [Инструкции для /specs/](./README.md)

## Оглавление

- [Список индексов](#список-индексов)
- [Формат таблиц](#формат-таблиц)
- [Формат строки](#формат-строки)
- [Workflow обновления](#workflow-обновления)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Список индексов

| README | Тип документов | Формат таблицы |
|--------|----------------|----------------|
| `/specs/discussions/README.md` | Discussions | [Стандартный](#discussions--impact) |
| `/specs/impact/README.md` | Impacts | [Стандартный](#discussions--impact) |
| `/specs/services/{service}/README.md` | Описание сервиса | Произвольный |
| `/specs/services/{service}/adr/README.md` | ADR | [С Impact](#adr) |
| `/specs/services/{service}/plans/README.md` | Plans | [С ADR](#plans) |

---

## Формат таблиц

### Discussions / Impact

```markdown
| # | Тема | Статус | Дата |
|---|------|--------|------|
| [001](001-auth.md) | Auth Strategy | 🔍 REVIEW | 2025-01-21 |
| [002](002-caching.md) | Caching | 📝 DRAFT | 2025-01-20 |
```

| Колонка | Описание |
|---------|----------|
| `#` | Ссылка на документ с номером |
| `Тема` | Краткое название (из заголовка документа) |
| `Статус` | Emoji + статус (см. [statuses.md](./statuses.md)) |
| `Дата` | Дата последнего изменения |

### ADR

```markdown
| # | Тема | Impact | Статус | Дата |
|---|------|--------|--------|------|
| [001](001-jwt.md) | JWT Tokens | [001](/specs/impact/001.md) | 🆗 APPROVED | 2025-01-21 |
| [002](002-session.md) | Session Storage | [001](/specs/impact/001.md) | 📝 DRAFT | 2025-01-22 |
```

| Колонка | Описание |
|---------|----------|
| `Impact` | Ссылка на родительский Impact |

### Plans

```markdown
| План | ADR | Статус | Дата |
|------|-----|--------|------|
| [jwt-migration](jwt-migration-plan.md) | [002](../adr/002.md) | ⏳ RUNNING | 2025-01-21 |
| [redis-cache](redis-cache-plan.md) | [003](../adr/003.md) | 📝 DRAFT | 2025-01-22 |
```

| Колонка | Описание |
|---------|----------|
| `План` | Ссылка на план (без номера, по теме) |
| `ADR` | Ссылка на родительский ADR |

---

## Формат строки

### При создании документа

```markdown
| [{NNN}]({NNN}-{topic}.md) | {Тема} | 📝 DRAFT | {YYYY-MM-DD} |
```

**Пример:**
```markdown
| [003](003-payments.md) | Payments Integration | 📝 DRAFT | 2025-01-22 |
```

### При изменении статуса

Обновить только колонку "Статус":

```markdown
| [001](001-auth.md) | Auth Strategy | 🔍 REVIEW | 2025-01-21 |
```

### Emoji статусов

| Статус | Emoji |
|--------|-------|
| DRAFT | 📝 |
| REVIEW | 🔍 |
| APPROVED | 🆗 |
| RUNNING | ⏳ |
| DONE | ✅ |
| REJECTED | ❌ |
| SUPERSEDED | 🚫 |

---

## Workflow обновления

### Алгоритм /specs-index

```
/specs-index [path]
    │
    ├── path указан?
    │   ├── Да → обновить только этот README
    │   └── Нет → найти все README.md в /specs/
    │
    ├── Для каждого README:
    │   │
    │   ├── Определить тип (discussions, impact, adr, plans)
    │   │
    │   ├── Найти все документы в папке
    │   │   └── ls *.md | grep -v README.md
    │   │
    │   ├── Для каждого документа:
    │   │   ├── Прочитать заголовок (# ...)
    │   │   ├── Прочитать статус (из метаданных или frontmatter)
    │   │   ├── Прочитать дату (mtime или из документа)
    │   │   └── Для ADR/Plans: прочитать ссылку на родителя
    │   │
    │   ├── Сформировать таблицу по формату типа
    │   │
    │   └── Обновить README.md
    │
    └── Вывести результат
```

### Обновление при создании документа

При `/spec-create`:

1. Создать документ
2. Добавить строку в соответствующий README.md:
   - Найти таблицу (строка начинается с `| #` или `| План`)
   - Найти конец таблицы
   - Добавить новую строку перед концом

### Обновление при изменении статуса

При `/spec-status`:

1. Найти README.md документа
2. Найти строку с документом (по номеру или имени)
3. Заменить статус в строке

---

## Скиллы

| Скилл | Использует |
|-------|------------|
| [/spec-create](/.claude/skills/spec-create/SKILL.md) | Добавление строки в README |
| [/spec-status](/.claude/skills/spec-status/SKILL.md) | Обновление статуса в README |
| [/specs-index](/.claude/skills/specs-index/SKILL.md) | Полная переиндексация |

---

## Связанные инструкции

- [naming.md](./naming.md) — формат названия документов
- [statuses.md](./statuses.md) — система статусов и emoji
