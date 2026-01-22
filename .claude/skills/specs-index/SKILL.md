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

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

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

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [specs/indexes.md](/.claude/instructions/specs/indexes.md) — список индексов, форматы таблиц
> 2. [specs/statuses.md](/.claude/instructions/specs/statuses.md) — отображение статусов
> 3. [specs/errors.md](/.claude/instructions/specs/errors.md#specs-index) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Найти все README.md в /specs/

> **SSOT:** [specs/indexes.md](/.claude/instructions/specs/indexes.md#список-индексов)

### Шаг 2: Для каждого README

> **SSOT:** [specs/indexes.md](/.claude/instructions/specs/indexes.md#workflow-обновления)

### Шаг 3: Результат

> **SSOT:** [specs/output.md](/.claude/instructions/specs/output.md#specs-index)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Найдены все README.md
- [ ] Обработан каждый README
- [ ] Выведен результат

---

## Примеры

> **SSOT:** [specs/examples.md](/.claude/instructions/specs/examples.md#specs-index)
