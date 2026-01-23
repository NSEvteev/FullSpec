---
name: specs-health
description: Проверка целостности /specs/ — статусы, ссылки, застрявшие документы
allowed-tools: Read, Glob, Grep, Bash
category: specs
triggers:
  commands:
    - /specs-health
  phrases:
    ru:
      - проверь спецификации
      - здоровье specs
      - найди проблемы в specs
    en:
      - check specs
      - specs health
      - find specs issues
---

# Проверка целостности /specs/

Диагностика проблем в документах спецификаций: статусы, ссылки, застрявшие документы.

**Связанные скиллы:**
- [spec-status](/.claude/skills/spec-status/SKILL.md) — исправление статусов
- [specs-sync](/.claude/skills/specs-sync/SKILL.md) — синхронизация статусов
- [specs-index](/.claude/skills/specs-index/SKILL.md) — обновление индексов

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/specs-health [--fix] [--verbose]
```

| Параметр | Описание |
|----------|----------|
| `--fix` | Предложить исправления для найденных проблем |
| `--verbose` | Подробный вывод всех проверок |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [specs/statuses.md](/.claude/.instructions/workflow/specs/statuses.md) — статусы, каскадные проверки
> 2. [specs/rules.md](/.claude/.instructions/workflow/specs/rules.md#проверки-specs-health) — типы проблем
> 3. [specs/relations.md](/.claude/.instructions/workflow/specs/relations.md) — связи документов
> 4. [specs/errors.md](/.claude/.instructions/workflow/specs/errors.md#specs-health) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Собрать все документы /specs/

> **SSOT:** [specs/README.md](/.claude/.instructions/workflow/specs/README.md#1-структура-specs)

### Шаг 2: Проверить каждый документ

> **SSOT:** [specs/rules.md](/.claude/.instructions/workflow/specs/rules.md#проверки-specs-health)

### Шаг 3: Проверить консистентность статусов

> **SSOT:** [specs/statuses.md](/.claude/.instructions/workflow/specs/statuses.md#каскадные-проверки)

### Шаг 4: Проверить сервисы

> **SSOT:** [specs/relations.md](/.claude/.instructions/workflow/specs/relations.md#связь-specs--doc)

### Шаг 5: Сформировать отчёт

> **SSOT:** [specs/output.md](/.claude/.instructions/workflow/specs/output.md#specs-health)

### Шаг 6: При `--fix` — предложить исправления

> **SSOT:** [specs/errors.md](/.claude/.instructions/workflow/specs/errors.md#specs-health)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Собраны все документы
- [ ] Проверен каждый документ
- [ ] Проверена консистентность статусов
- [ ] Проверены сервисы
- [ ] Сформирован отчёт
- [ ] При `--fix` — предложены исправления

---

## Примеры

> **SSOT:** [specs/examples.md](/.claude/.instructions/workflow/specs/examples.md#specs-health)
