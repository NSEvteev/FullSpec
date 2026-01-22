---
name: docs-update
description: Обновление документации при изменении кода в /src/
allowed-tools: Read, Write, Edit, Glob, Grep
category: documentation
triggers:
  commands:
    - /docs-update
  phrases:
    ru:
      - обнови документацию
      - синхронизируй документацию
      - документация устарела
    en:
      - update documentation
      - sync documentation
      - documentation outdated
---

# Обновление документации

Команда для синхронизации документации с изменениями в исходном файле.

**Связанные скиллы:**
- [/docs-create](/.claude/skills/docs-create/SKILL.md) — создание документации
- [/docs-delete](/.claude/skills/docs-delete/SKILL.md) — пометка при удалении
- [/links-update](/.claude/skills/links-update/SKILL.md) — синхронизация ссылок

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/docs-update [путь] [--diff] [--auto] [--force]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь` | Путь к файлу (или автоопределение) | Изменённые файлы |
| `--diff` | Показать изменения без применения | false |
| `--auto` | Применить без подтверждения | false |
| `--force` | Перезаписать даже без изменений | false |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать SSOT-инструкции:
> 1. [rules.md](/.claude/instructions/docs/rules.md) — маппинг путей, валидация
> 2. [workflow.md#docs-update](/.claude/instructions/docs/workflow.md#docs-update) — детальный воркфлоу
> 3. [errors.md](/.claude/instructions/docs/errors.md) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Определить изменённые файлы

> **SSOT:** [workflow.md#docs-update](/.claude/instructions/docs/workflow.md#docs-update)

### Шаг 2: Найти соответствующую документацию

> **SSOT:** [rules.md#маппинг-путей](/.claude/instructions/docs/rules.md#маппинг-путей)

### Шаг 3: Проанализировать изменения

> **SSOT:** [workflow.md#типы-изменений-api](/.claude/instructions/docs/workflow.md#типы-изменений-api)

### Шаг 4: Сгенерировать обновления

> **SSOT:** [workflow.md#docs-update](/.claude/instructions/docs/workflow.md#docs-update)

### Шаг 5: Показать diff / применить

> **SSOT:** [workflow.md#режим---diff](/.claude/instructions/docs/workflow.md#режим---diff)

### Шаг 6: Обновление ссылок → /links-update

> **SSOT:** [SKILL.md](/.claude/skills/links-update/SKILL.md)

### Шаг 7: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 8: Результат

```
✅ Документация обновлена

Файлов обновлено: {N}
Изменения: {список}
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Изменённые файлы определены
- [ ] Документация найдена для каждого файла
- [ ] Изменения проанализированы
- [ ] Diff показан (или применён с `--auto`)
- [ ] Пользователь подтвердил (или `--auto`)
- [ ] Изменения применены
- [ ] `/links-update` вызван
- [ ] Результат выведен

---

## Примеры

> **SSOT:** [examples.md#обновление-документации](/.claude/instructions/docs/examples.md#обновление-документации)
