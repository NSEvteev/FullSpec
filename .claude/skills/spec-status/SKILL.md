---
name: spec-status
description: Изменение статуса документа /specs/ с каскадными проверками
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
category: specs
triggers:
  commands:
    - /spec-status
  phrases:
    ru:
      - статус спецификации
      - измени статус
      - переведи в review
      - одобри adr
    en:
      - spec status
      - change status
      - move to review
      - approve adr
---

# Изменение статуса документа /specs/

Изменение статуса документа спецификации с автоматическими каскадными проверками и переходами.

**Связанные скиллы:**
- [spec-create](/.claude/skills/spec-create/SKILL.md) — создание документов
- [spec-update](/.claude/skills/spec-update/SKILL.md) — работа с документом
- [specs-sync](/.claude/skills/specs-sync/SKILL.md) — синхронизация всех статусов

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/spec-status <path> <status> [--force]
```

| Параметр | Описание | Пример |
|----------|----------|--------|
| `path` | Путь к документу (сокращённый) | `discussions/001`, `auth/adr/002` |
| `status` | Целевой статус | `review`, `approved`, `done`, `rejected` |
| `--force` | Пропустить проверку чек-листа | — |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [specs/statuses.md](/.claude/instructions/workflow/specs/statuses.md) — статусы, допустимые переходы
> 2. [specs/workflow.md](/.claude/instructions/workflow/specs/workflow.md) — каскадные переходы
> 3. [specs/naming.md](/.claude/instructions/workflow/specs/naming.md) — сокращённые пути
> 4. [specs/errors.md](/.claude/instructions/workflow/specs/errors.md) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Найти документ по сокращённому пути

> **SSOT:** [specs/naming.md](/.claude/instructions/workflow/specs/naming.md#сокращённые-пути)

### Шаг 2: Прочитать текущий статус

> **SSOT:** [specs/statuses.md](/.claude/instructions/workflow/specs/statuses.md#специфика-по-типам)

### Шаг 3: Проверить допустимость перехода

> **SSOT:** [specs/statuses.md](/.claude/instructions/workflow/specs/statuses.md#схема-переходов)

### Шаг 4: Проверить чек-лист перехода

> **SSOT:** Чек-листы в инструкциях по типам:
> - [discussions.md](/.claude/instructions/workflow/specs/discussions.md#чек-листы-переходов)
> - [impact.md](/.claude/instructions/workflow/specs/impact.md#чек-листы-переходов)
> - [adr.md](/.claude/instructions/workflow/specs/adr.md#чек-листы-переходов)
> - [plans.md](/.claude/instructions/workflow/specs/plans.md#чек-листы-переходов)

### Шаг 5: Обновить статус в документе

> **SSOT:** [specs/statuses.md](/.claude/instructions/workflow/specs/statuses.md#отображение-в-readme)

### Шаг 6: Обновить README.md индекс

> **SSOT:** [specs/indexes.md](/.claude/instructions/workflow/specs/indexes.md)

### Шаг 7: Выполнить каскадные действия

> **SSOT:** [specs/statuses.md](/.claude/instructions/workflow/specs/statuses.md#каскадные-проверки)

### Шаг 8: Результат

> **SSOT:** [specs/output.md](/.claude/instructions/workflow/specs/output.md#spec-status)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Найден документ
- [ ] Проверена допустимость перехода
- [ ] Проверен чек-лист (или `--force`)
- [ ] Обновлён статус в документе
- [ ] Обновлён README.md индекс
- [ ] Выполнены каскадные действия
- [ ] Выведен результат

---

## Примеры

> **SSOT:** [specs/examples.md](/.claude/instructions/workflow/specs/examples.md#spec-status)
