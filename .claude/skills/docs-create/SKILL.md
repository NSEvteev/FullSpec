---
name: docs-create
description: Создание документации для нового файла в /src/
allowed-tools: Read, Write, Edit, Glob, Grep
category: documentation
triggers:
  commands:
    - /docs-create
  phrases:
    ru:
      - создай документацию
      - добавь документацию
      - задокументируй
    en:
      - create documentation
      - add documentation
      - document this
---

# Создание документации

Команда для автоматического создания документации при добавлении нового файла в проект.

**Связанные скиллы:**
- [/docs-update](/.claude/skills/docs-update/SKILL.md) — обновление документации
- [/docs-delete](/.claude/skills/docs-delete/SKILL.md) — пометка при удалении файла
- [/links-update](/.claude/skills/links-update/SKILL.md) — синхронизация ссылок

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/docs-create <путь-к-файлу> [--dry-run] [--no-link]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь-к-файлу` | Любой файл проекта (кроме исключённых) | — (обязательный) |
| `--dry-run` | Показать план без создания | false |
| `--no-link` | Не добавлять ссылку в исходный файл | false |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать SSOT-инструкции:
> 1. [rules.md](/.claude/instructions/workflow/docs/rules.md) — маппинг путей, валидация
> 2. [workflow.md#docs-create](/.claude/instructions/workflow/docs/workflow.md#docs-create) — детальный воркфлоу
> 3. [templates.md](/.claude/instructions/workflow/docs/templates.md) — выбор шаблона
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Валидация пути

> **SSOT:** [rules.md#валидация-путей](/.claude/instructions/workflow/docs/rules.md#валидация-путей)

### Шаг 2: Определение типа файла

> **SSOT:** [rules.md#поддерживаемые-языки](/.claude/instructions/workflow/docs/rules.md#поддерживаемые-языки)

### Шаг 3: Выбор шаблона

> **SSOT:** [templates.md#выбор-шаблона](/.claude/instructions/workflow/docs/templates.md#выбор-шаблона)

### Шаг 4: Анализ исходного файла

> **SSOT:** [workflow.md#шаги-подробно](/.claude/instructions/workflow/docs/workflow.md#шаги-подробно)

### Шаг 5: Генерация документации

> **SSOT:** [rules.md#шаблон-документации](/.claude/instructions/workflow/docs/rules.md#шаблон-документации)

### Шаг 6: Создание директорий и файла

> **SSOT:** [workflow.md#docs-create](/.claude/instructions/workflow/docs/workflow.md#docs-create)

### Шаг 7: Добавление ссылки в исходный файл

> **SSOT:** [structure.md#ссылки-в-коде](/.claude/instructions/workflow/docs/structure.md#ссылки-в-коде)

### Шаг 8: Обновление ссылок → /links-update

> **SSOT:** [SKILL.md](/.claude/skills/links-update/SKILL.md)

### Шаг 9: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 10: Результат

```
✅ Документация создана

Файл: /doc/src/{service}/{path}.md
Шаблон: {template}
Ссылка в исходном файле: {да/нет}
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Путь к файлу валидирован (не в исключённых директориях)
- [ ] Путь документации определён по маппингу
- [ ] Документация не существует (или получено подтверждение)
- [ ] Исходный файл прочитан, API извлечён
- [ ] Документация создана по шаблону
- [ ] Ссылка добавлена в исходный файл (если не --no-link)
- [ ] `/links-update` вызван
- [ ] Результат выведен

---

## Примеры

> **SSOT:** [examples.md#создание-документации](/.claude/instructions/workflow/docs/examples.md#создание-документации)
