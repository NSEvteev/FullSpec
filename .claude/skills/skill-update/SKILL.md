---
name: skill-update
description: Обновление существующих скиллов при добавлении нового
allowed-tools: Read, Edit, Glob, Grep
category: skill-management
triggers:
  commands:
    - /skill-update
  phrases:
    ru:
      - обнови скиллы
      - интегрируй скилл
    en:
      - update skills
      - integrate skill
---

# Обновление скиллов

Интеграция нового скилла в существующие. Анализирует применимость и предлагает добавить вызовы.

**Связанные скиллы:**
- [skill-create](/.claude/skills/skill-create/SKILL.md) — создание скилла (вызывает этот скилл)
- [skill-delete](/.claude/skills/skill-delete/SKILL.md) — удаление скилла

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/skill-update <новый-скилл>
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `новый-скилл` | Имя скилла или путь к SKILL.md | Последний созданный |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать SSOT-инструкции:
> 1. [integration.md](/.claude/instructions/meta/skills/integration.md) — матрица применимости, критерии, форматы
> 2. [workflow.md](/.claude/instructions/meta/skills/workflow.md) — структура воркфлоу
> 3. [errors.md](/.claude/instructions/meta/skills/errors.md) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

<!--
ПРАВИЛО: Шаги содержат ТОЛЬКО название и ссылку на SSOT.
Детали, алгоритмы, примеры — в SSOT-инструкциях.
LLM ОБЯЗАН прочитать SSOT перед выполнением шага.
-->

### Шаг 1: Получить новый скилл

> **SSOT:** [workflow.md](/.claude/instructions/meta/skills/workflow.md#получение-скилла)

### Шаг 2: Загрузить существующие скиллы

> **SSOT:** [integration.md](/.claude/instructions/meta/skills/integration.md#загрузка-скиллов)

### Шаг 3: Анализ применимости

> **SSOT:** [integration.md](/.claude/instructions/meta/skills/integration.md#критерии-применимости)

### Шаг 4: Сформировать предложения

> **SSOT:** [integration.md](/.claude/instructions/meta/skills/integration.md#формат-интеграции-в-воркфлоу)

### Шаг 5: Применить изменения

> **SSOT:** [integration.md](/.claude/instructions/meta/skills/integration.md#применение-интеграции)

### Шаг 6: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 7: Результат

> **SSOT:** [workflow.md](/.claude/instructions/meta/skills/workflow.md#формат-результата)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Получил новый скилл
- [ ] Загрузил существующие скиллы
- [ ] Проанализировал применимость
- [ ] Сформировал предложения
- [ ] Применил изменения
- [ ] Вывел итоговый отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/instructions/meta/skills/examples.md#skill-update)
