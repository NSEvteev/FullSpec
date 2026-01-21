---
name: specs-index
description: Обновление индексов README.md в /specs/
allowed-tools: Read, Write, Edit, Glob, Grep
category: specs
triggers:
  commands:
    - /specs-index
  phrases:
    ru:
      - обнови индексы specs
      - переиндексируй specs
      - обнови readme specs
    en:
      - update specs index
      - reindex specs
      - update specs readme
---

# Обновление индексов /specs/

Обновление всех README.md индексов в папке /specs/ на основе существующих документов.

**Связанные скиллы:**
- [spec-create](/.claude/skills/spec-create/SKILL.md) — создание документов
- [specs-health](/.claude/skills/specs-health/SKILL.md) — проверка целостности

**Связанные инструкции:**
- [specs/rules.md](/.claude/instructions/specs/rules.md) — правила работы

## Оглавление

- [Формат вызова](#формат-вызова)
- [Индексы](#индексы)
- [Воркфлоу](#воркфлоу)
- [Формат таблиц](#формат-таблиц)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/specs-index [path] [--dry-run]
```

| Параметр | Описание |
|----------|----------|
| `path` | Путь к конкретному README (опционально) |
| `--dry-run` | Показать изменения без применения |

---

## Индексы

| README | Содержимое |
|--------|------------|
| `/specs/discussions/README.md` | Список дискуссий |
| `/specs/impact/README.md` | Список импактов |
| `/specs/services/{service}/README.md` | Описание сервиса |
| `/specs/services/{service}/adr/README.md` | Список ADR сервиса |
| `/specs/services/{service}/plans/README.md` | Список планов сервиса |

---

## Воркфлоу

### Шаг 1: Найти все README.md

```bash
find /specs -name "README.md"
```

### Шаг 2: Для каждого README

1. Определить тип (discussions, impact, adr, plans)
2. Найти все документы в папке
3. Прочитать статус каждого документа
4. Сформировать таблицу
5. Обновить README

### Шаг 3: Результат

```
✅ Индексы обновлены

Обновлено README: 5
- /specs/discussions/README.md (3 документа)
- /specs/impact/README.md (2 документа)
- /specs/services/auth/adr/README.md (4 документа)
- /specs/services/auth/plans/README.md (2 документа)
- /specs/services/gateway/adr/README.md (1 документ)
```

---

## Формат таблиц

### Discussions / Impact

```markdown
| # | Тема | Статус | Дата |
|---|------|--------|------|
| [001](001-auth.md) | Auth Strategy | 🔍 REVIEW | 2025-01-21 |
| [002](002-caching.md) | Caching | 📝 DRAFT | 2025-01-20 |
```

### ADR

```markdown
| # | Тема | Impact | Статус | Дата |
|---|------|--------|--------|------|
| [001](001-jwt.md) | JWT Tokens | [001](/specs/impact/001.md) | 🆗 APPROVED | 2025-01-21 |
```

### Plans

```markdown
| План | ADR | Статус | Дата |
|------|-----|--------|------|
| [jwt-migration](jwt-migration-plan.md) | [002](../adr/002.md) | ⏳ RUNNING | 2025-01-21 |
```

---

## Примеры использования

### Пример 1: Обновить все индексы

```
/specs-index

📋 Обновление индексов /specs/

Сканирование...

Найдено README: 5
Найдено документов: 12

Обновляю...

✅ Индексы обновлены

- discussions/README.md: 3 документа
- impact/README.md: 2 документа
- services/auth/adr/README.md: 4 документа
- services/auth/plans/README.md: 2 документа
- services/gateway/adr/README.md: 1 документ
```

### Пример 2: Обновить конкретный индекс

```
/specs-index /specs/services/auth/adr/

✅ Индекс обновлён: /specs/services/auth/adr/README.md

Документов: 4
- 001-initial.md (DONE)
- 002-jwt-tokens.md (RUNNING)
- 003-session-storage.md (APPROVED)
- 004-rate-limiting.md (DRAFT)
```
