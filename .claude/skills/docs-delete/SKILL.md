---
name: docs-delete
description: Обработка удаления исходного файла — пометка документации
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
category: documentation
triggers:
  commands:
    - /docs-delete
  phrases:
    ru:
      - файл удалён
      - удалена документация
      - пометь документацию
    en:
      - file deleted
      - documentation deleted
      - mark documentation
---

# Удаление документации

Команда для обработки удаления исходного файла — помечает документацию для ревью и создаёт Issue.

**Связанные скиллы:**
- [/docs-create](/.claude/skills/docs-create/SKILL.md) — создание документации
- [/docs-update](/.claude/skills/docs-update/SKILL.md) — обновление документации
- [/issue-create](/.claude/skills/issue-create/SKILL.md) — создание Issue для ревью
- [/links-delete](/.claude/skills/links-delete/SKILL.md) — очистка ссылок

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/docs-delete <путь-к-файлу> [--no-issue] [--remove]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь-к-файлу` | Путь к удалённому файлу | — (обязательный) |
| `--no-issue` | Не создавать GitHub Issue | false |
| `--remove` | Удалить документацию сразу | false |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать SSOT-инструкции:
> 1. [rules.md](/.claude/.instructions/workflow/docs/rules.md) — маппинг путей, формат пометки
> 2. [workflow.md#docs-delete](/.claude/.instructions/workflow/docs/workflow.md#docs-delete) — детальный воркфлоу
> 3. [errors.md](/.claude/.instructions/workflow/docs/errors.md) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Найти документацию для удалённого файла

> **SSOT:** [rules.md#маппинг-путей](/.claude/.instructions/workflow/docs/rules.md#маппинг-путей)

### Шаг 2: Добавить пометку о требовании ревью

> **SSOT:** [rules.md#формат-пометки-doc-delete](/.claude/.instructions/workflow/docs/rules.md#формат-пометки-doc-delete)

### Шаг 3: Создать GitHub Issue → /issue-create

> **SSOT:** [SKILL.md](/.claude/skills/issue-create/SKILL.md)

### Шаг 4: Очистка ссылок → /links-delete

> **SSOT:** [SKILL.md](/.claude/skills/links-delete/SKILL.md)

### Шаг 5: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 6: Результат

```
✅ Документация помечена для ревью

Файл: /doc/src/{service}/{path}.md
Issue: #{number}
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Документация для файла найдена
- [ ] Пометка добавлена (или файл удалён с `--remove`)
- [ ] Issue создан (или пропущен с `--no-issue`)
- [ ] `/links-delete` вызван
- [ ] Результат выведен

---

## Примеры

> **SSOT:** [examples.md#удаление-документации](/.claude/.instructions/workflow/docs/examples.md#удаление-документации)
