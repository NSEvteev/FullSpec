---
name: spec-update
description: Работа с документом /specs/ (редактирование, валидация, переход)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
category: specs
triggers:
  commands:
    - /spec-update
  phrases:
    ru:
      - обнови спецификацию
      - поработаем с дискуссией
      - открой adr
      - редактируй план
    en:
      - update spec
      - work on discussion
      - open adr
      - edit plan
---

# Работа с документом /specs/

Основной скилл для редактирования документов спецификаций. Вызывает `/spec-status` при переходе по workflow.

**Связанные скиллы:**
- [spec-create](/.claude/skills/spec-create/SKILL.md) — создание документов
- [spec-status](/.claude/skills/spec-status/SKILL.md) — изменение статуса

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/spec-update <path> [--validate]
```

| Параметр | Описание |
|----------|----------|
| `path` | Путь к документу (сокращённый или полный) |
| `--validate` | Только проверить документ без редактирования |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [specs/README.md](/.claude/instructions/specs/README.md) — индекс инструкций
> 2. [specs/workflow.md](/.claude/instructions/specs/workflow.md) — триггеры переходов
> 3. [specs/rules.md](/.claude/instructions/specs/rules.md) — правила работы
> 4. [specs/errors.md](/.claude/instructions/specs/errors.md) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Найти документ по пути

> **SSOT:** [specs/naming.md](/.claude/instructions/specs/naming.md#сокращённые-пути)

### Шаг 2: Прочитать документ и метаданные

> **SSOT:** Формат документа по типу:
> - [discussions.md](/.claude/instructions/specs/discussions.md#формат-документа)
> - [impact.md](/.claude/instructions/specs/impact.md#формат-документа)
> - [adr.md](/.claude/instructions/specs/adr.md#формат-документа)
> - [plans.md](/.claude/instructions/specs/plans.md#формат-документа)

### Шаг 3: Показать контекст документа

> **SSOT:** [specs/output.md](/.claude/instructions/specs/output.md#spec-update)

### Шаг 4: Интерактивная работа (редактирование)

> **SSOT:** [specs/rules.md](/.claude/instructions/specs/rules.md#режим-валидации---validate)

### Шаг 5: Обработка триггеров перехода

> **SSOT:** [specs/rules.md](/.claude/instructions/specs/rules.md#spec-update--работа-с-документом)

### Шаг 6: Сохранение изменений

> **SSOT:** [specs/errors.md](/.claude/instructions/specs/errors.md#spec-update)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Найден и прочитан документ
- [ ] Показан контекст пользователю
- [ ] Выполнены запрошенные изменения
- [ ] При триггере перехода — вызван `/spec-status`
- [ ] Изменения сохранены

---

## Примеры

> **SSOT:** [specs/examples.md](/.claude/instructions/specs/examples.md#spec-update)
