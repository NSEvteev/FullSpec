---
name: skill-migrate
description: Переименование скилла с обновлением всех ссылок
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
category: skill-management
critical: true
triggers:
  commands:
    - /skill-migrate
  phrases:
    ru:
      - мигрируй скилл
      - переименуй скилл
    en:
      - migrate skill
      - rename skill
---

# Миграция скилла

Переименование или перемещение скилла с автоматическим обновлением всех ссылок.

**Связанные скиллы:**
- [skill-create](/.claude/skills/skill-create/SKILL.md) — создание скилла
- [skill-delete](/.claude/skills/skill-delete/SKILL.md) — удаление скилла
- [links-update](/.claude/skills/links-update/SKILL.md) — обновление ссылок

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/skill-migrate <old-name> <new-name> [--category <category>] [--dry-run]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `old-name` | Текущее имя | — (обязательный) |
| `new-name` | Новое имя | — (обязательный) |
| `--category` | Новая категория | Без изменения |
| `--dry-run` | Показать план | false |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать SSOT-инструкции:
> 1. [rules.md](/.claude/.instructions/skills/rules.md) — правила именования
> 2. [integration.md](/.claude/.instructions/skills/integration.md) — типы ссылок
> 3. [errors.md](/.claude/.instructions/skills/errors.md) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

<!--
ПРАВИЛО: Шаги содержат ТОЛЬКО название и ссылку на SSOT.
Детали, алгоритмы, примеры — в SSOT-инструкциях.
LLM ОБЯЗАН прочитать SSOT перед выполнением шага.
-->

### Шаг 1: Проверки

> **SSOT:** [validation.md](/.claude/.instructions/skills/validation.md#проверка-имён)

### Шаг 2: Анализ зависимостей

> **SSOT:** [integration.md](/.claude/.instructions/skills/integration.md#типы-ссылок)

### Шаг 3: Подтверждение

> **SSOT:** [workflow.md](/.claude/.instructions/skills/workflow.md#подтверждение-пользователя)

### Шаг 4: Переименование папки

> **SSOT:** [workflow.md](/.claude/.instructions/skills/workflow.md#переименование-скилла)

### Шаг 5: Обновление ссылок

> **SSOT:** [integration.md](/.claude/.instructions/skills/integration.md#обновление-ссылок)

### Шаг 6: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 7: Результат

> **SSOT:** [workflow.md](/.claude/.instructions/skills/workflow.md#формат-результата)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Проверил имена (старое и новое)
- [ ] Проанализировал зависимости
- [ ] Получил подтверждение
- [ ] Переименовал папку
- [ ] Обновил ссылки
- [ ] Вывел итоговый отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/.instructions/skills/examples.md#skill-migrate)
