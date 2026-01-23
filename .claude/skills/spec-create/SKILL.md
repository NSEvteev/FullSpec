---
name: spec-create
description: Создание документов /specs/ (Discussion, Impact, ADR, Plan)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
category: specs
triggers:
  commands:
    - /spec-create
  phrases:
    ru:
      - создай спецификацию
      - новая дискуссия
      - создай adr
      - создай план
      - создай импакт
    en:
      - create spec
      - new discussion
      - create adr
      - create plan
      - create impact
---

# Создание документов /specs/

Создание документов спецификаций: Discussion, Impact, ADR, Plan.

**Связанные скиллы:**
- [spec-status](/.claude/skills/spec-status/SKILL.md) — изменение статуса
- [spec-update](/.claude/skills/spec-update/SKILL.md) — работа с документом

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/spec-create <type> [parent] [service] [--dry-run] [--new]
```

| Параметр | Описание | Обязательный |
|----------|----------|:------------:|
| `type` | Тип документа: `discussion`, `impact`, `adr`, `plan` | Да |
| `parent` | ID или тема родительского документа | Для impact/adr/plan |
| `service` | Название сервиса (для adr) | Для adr |
| `--dry-run` | Показать план без создания | Нет |
| `--new` | Создать структуру нового сервиса | Нет |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [specs/README.md](/.claude/.instructions/workflow/specs/README.md) — индекс инструкций
> 2. [specs/naming.md](/.claude/.instructions/workflow/specs/naming.md) — формат имён, нумерация
> 3. [specs/relations.md](/.claude/.instructions/workflow/specs/relations.md) — связи, backlinks
> 4. [specs/errors.md](/.claude/.instructions/workflow/specs/errors.md) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Определить тип документа

> **SSOT:** [specs/rules.md](/.claude/.instructions/workflow/specs/rules.md#spec-create--создание-документов)

### Шаг 2: Получить и валидировать родителя

> **SSOT:** [specs/relations.md](/.claude/.instructions/workflow/specs/relations.md#обязательные-ссылки)

### Шаг 3: Получить тему и определить номер

> **SSOT:** [specs/naming.md](/.claude/.instructions/workflow/specs/naming.md)

### Шаг 4: Для ADR — определить сервис

> **SSOT:** [specs/impact.md](/.claude/.instructions/workflow/specs/impact.md#создание-нового-сервиса)

### Шаг 5: Прочитать шаблон и создать документ

> **SSOT:** Шаблоны в [specs/README.md](/.claude/.instructions/workflow/specs/README.md#17-шаблоны)

### Шаг 6: Обновить индекс README.md

> **SSOT:** [specs/indexes.md](/.claude/.instructions/workflow/specs/indexes.md)

### Шаг 7: Добавить backlink в родителя

> **SSOT:** [specs/relations.md](/.claude/.instructions/workflow/specs/relations.md#обратные-ссылки-backlinks)

### Шаг 8: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 9: Результат

> **SSOT:** [specs/output.md](/.claude/.instructions/workflow/specs/output.md#spec-create)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Определён тип документа
- [ ] Получен и валидирован родитель (если нужен)
- [ ] Получена тема, определён номер
- [ ] Для ADR: определён сервис
- [ ] Для нового сервиса: создана структура (если `--new`)
- [ ] Прочитан шаблон
- [ ] Создан файл документа
- [ ] Обновлён индекс README.md
- [ ] Добавлен backlink в родителя
- [ ] Выведен результат

---

## Примеры

> **SSOT:** [specs/examples.md](/.claude/.instructions/workflow/specs/examples.md#spec-create)
