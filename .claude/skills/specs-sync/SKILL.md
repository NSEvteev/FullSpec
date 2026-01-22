---
name: specs-sync
description: Синхронизация каскадных статусов документов /specs/
allowed-tools: Read, Write, Edit, Glob, Grep
category: specs
triggers:
  commands:
    - /specs-sync
  phrases:
    ru:
      - синхронизируй статусы
      - пересчитай статусы
      - обнови статусы specs
    en:
      - sync statuses
      - recalculate statuses
      - update specs statuses
---

# Синхронизация статусов /specs/

Пересчёт каскадных статусов для всех документов. Приводит статусы родительских документов в соответствие с дочерними.

**Связанные скиллы:**
- [spec-status](/.claude/skills/spec-status/SKILL.md) — изменение отдельного статуса
- [specs-health](/.claude/skills/specs-health/SKILL.md) — диагностика проблем

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/specs-sync [--dry-run]
```

| Параметр | Описание |
|----------|----------|
| `--dry-run` | Показать план без применения |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [specs/statuses.md](/.claude/instructions/workflow/specs/statuses.md) — правила статусов, финальные статусы
> 2. [specs/workflow.md](/.claude/instructions/workflow/specs/workflow.md) — каскадные переходы
> 3. [specs/relations.md](/.claude/instructions/workflow/specs/relations.md) — граф зависимостей
> 4. [specs/errors.md](/.claude/instructions/workflow/specs/errors.md#specs-sync) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Собрать все цепочки документов

> **SSOT:** [specs/relations.md](/.claude/instructions/workflow/specs/relations.md#граф-зависимостей)

### Шаг 2: Для каждой цепочки определить ожидаемые статусы

> **SSOT:** [specs/statuses.md](/.claude/instructions/workflow/specs/statuses.md#каскадные-проверки)

### Шаг 3: Найти расхождения

> **SSOT:** [specs/statuses.md](/.claude/instructions/workflow/specs/statuses.md#порядок-проверки-снизу-вверх)

### Шаг 4: Применить изменения

> **SSOT:** [specs/output.md](/.claude/instructions/workflow/specs/output.md#specs-sync)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Собраны все цепочки
- [ ] Определены ожидаемые статусы
- [ ] Найдены расхождения
- [ ] Применены изменения (или показан план)

---

## Примеры

> **SSOT:** [specs/examples.md](/.claude/instructions/workflow/specs/examples.md#specs-sync)
