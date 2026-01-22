---
name: docs-reindex
description: Полная переиндексация документации проекта
allowed-tools: Read, Write, Edit, Glob, Grep
category: documentation
triggers:
  commands:
    - /docs-reindex
  phrases:
    ru:
      - переиндексируй документацию
      - проверь документацию
      - синхронизируй всю документацию
    en:
      - reindex documentation
      - check documentation
      - sync all documentation
---

# Переиндексация документации

Команда для полной проверки и синхронизации документации с исходным кодом.

**Связанные скиллы:**
- [/docs-create](/.claude/skills/docs-create/SKILL.md) — для missing файлов
- [/docs-update](/.claude/skills/docs-update/SKILL.md) — для outdated файлов
- [/docs-delete](/.claude/skills/docs-delete/SKILL.md) — для orphan файлов
- [/links-validate](/.claude/skills/links-validate/SKILL.md) — проверка ссылок

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/docs-reindex [--check] [--json] [--verbose] [--fix]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--check` | Только проверка, без изменений | false |
| `--json` | JSON формат вывода | false |
| `--verbose` | Подробный вывод | false |
| `--fix` | Автоматическое исправление проблем | false |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать SSOT-инструкции:
> 1. [structure.md](/.claude/instructions/docs/structure.md) — структура /doc/
> 2. [workflow.md#docs-reindex](/.claude/instructions/docs/workflow.md#docs-reindex) — детальный воркфлоу
> 3. [errors.md](/.claude/instructions/docs/errors.md) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Сканировать /src/

> **SSOT:** [workflow.md#docs-reindex](/.claude/instructions/docs/workflow.md#docs-reindex)

### Шаг 2: Сканировать /doc/src/

> **SSOT:** [structure.md#дерево-doc](/.claude/instructions/docs/structure.md#дерево-doc)

### Шаг 3: Построить карту соответствий

> **SSOT:** [rules.md#маппинг-путей](/.claude/instructions/docs/rules.md#маппинг-путей)

### Шаг 4: Выявить проблемы

> **SSOT:** [workflow.md#типы-проблем](/.claude/instructions/docs/workflow.md#типы-проблем)

### Шаг 5: Вывести отчёт / исправить

> **SSOT:** [workflow.md#режим---fix](/.claude/instructions/docs/workflow.md#режим---fix)

### Шаг 6: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 7: Результат

```
✅ Переиндексация завершена

Синхронизировано: {N} файлов
Missing: {N} (создано)
Orphan: {N} (помечено)
Outdated: {N} (обновлено)
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] /src/ просканирован
- [ ] /doc/src/ просканирован
- [ ] Карта соответствий построена
- [ ] Проблемы выявлены
- [ ] Отчёт выведен (или `--fix` применён)
- [ ] Результат выведен

---

## Примеры

> **SSOT:** [examples.md#переиндексация](/.claude/instructions/docs/examples.md#переиндексация)
