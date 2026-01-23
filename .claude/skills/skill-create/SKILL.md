---
name: skill-create
description: Создание нового скилла по шаблону
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
category: skill-management
triggers:
  commands:
    - /skill-create
  phrases:
    ru:
      - создай скилл
      - новый скилл
      - добавь скилл
    en:
      - create skill
      - new skill
---

# Создание скилла

Создание нового скилла по шаблону с валидацией и интеграцией.

**Связанные скиллы:**
- [skill-update](/.claude/skills/skill-update/SKILL.md) — интеграция в существующие скиллы
- [skill-delete](/.claude/skills/skill-delete/SKILL.md) — удаление скилла
- [links-update](/.claude/skills/links-update/SKILL.md) — синхронизация ссылок

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/skill-create [название] [--dry-run] [--auto]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `название` | Имя скилла в формате `{объект}-{действие}` | Спросить |
| `--dry-run` | Показать план без создания | false |
| `--auto` | Автоматический режим | false |

> **Параметры:** см. [parameters.md](/.claude/.instructions/.claude/skills/parameters.md)

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать SSOT-инструкции:
> 1. [rules.md](/.claude/.instructions/.claude/skills/rules.md) — правила именования, категории
> 2. [workflow.md](/.claude/.instructions/.claude/skills/workflow.md) — структура воркфлоу
> 3. [validation.md](/.claude/.instructions/.claude/skills/validation.md) — fail-fast, ревью, чек-листы
> 4. [parameters.md](/.claude/.instructions/.claude/skills/parameters.md) — стандартные флаги
> 5. [integration.md](/.claude/.instructions/.claude/skills/integration.md) — интеграция скиллов
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

<!--
ПРАВИЛО: Шаги содержат ТОЛЬКО название и ссылку на SSOT.
Детали, алгоритмы, примеры — в SSOT-инструкциях.
LLM ОБЯЗАН прочитать SSOT перед выполнением шага.
-->

### Шаг 1: Fail-fast проверки

> **SSOT:** [validation.md](/.claude/.instructions/.claude/skills/validation.md#fail-fast-проверки)

### Шаг 2: Проверка пересечений

> **SSOT:** [validation.md](/.claude/.instructions/.claude/skills/validation.md#проверка-пересечений)

### Шаг 3: Получить название

> **SSOT:** [rules.md](/.claude/.instructions/.claude/skills/rules.md#формат-названия)

### Шаг 4: Категория

> **SSOT:** [rules.md](/.claude/.instructions/.claude/skills/rules.md#категории-скиллов)

### Шаг 5: Метаданные

> **SSOT:** [workflow.md](/.claude/.instructions/.claude/skills/workflow.md#генерация-метаданных)

### Шаг 6: Создать файлы

> **SSOT:** [workflow.md](/.claude/.instructions/.claude/skills/workflow.md#создание-файлов)

### Шаг 7: Наполнение содержимым

> **SSOT:** [workflow.md](/.claude/.instructions/.claude/skills/workflow.md#наполнение-содержимым)

### Шаг 8: Ревью

> **SSOT:** [validation.md](/.claude/.instructions/.claude/skills/validation.md#ревью-скилла)

### Шаг 9: Валидация структуры

> **SSOT:** [validation.md](/.claude/.instructions/.claude/skills/validation.md#валидация-структуры-skillmd)

### Шаг 10: Связь с агентами

> **SSOT:** [integration.md](/.claude/.instructions/.claude/skills/integration.md#связь-с-агентами)

### Шаг 11: Синхронизация

> **SSOT:** [integration.md](/.claude/.instructions/.claude/skills/integration.md#синхронизация)

### Шаг 12: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 13: Результат

> **SSOT:** [workflow.md](/.claude/.instructions/.claude/skills/workflow.md#формат-результата)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Прошёл fail-fast проверки
- [ ] Проверил пересечения
- [ ] Получил название в формате `{объект}-{действие}`
- [ ] Определил категорию
- [ ] Заполнил метаданные
- [ ] Создал файлы
- [ ] Наполнил содержимым
- [ ] Провёл ревью
- [ ] Валидировал структуру
- [ ] Настроил связь с агентами
- [ ] Синхронизировал ссылки
- [ ] Вывел итоговый отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/.instructions/.claude/skills/examples.md#skill-create)
