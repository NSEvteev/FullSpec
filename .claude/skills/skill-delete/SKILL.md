---
name: skill-delete
description: Обновление существующих скиллов при удалении скилла
allowed-tools: Read, Edit, Glob, Grep
category: skill-management
triggers:
  commands:
    - /skill-delete
  phrases:
    ru:
      - удали скилл
      - очисти ссылки на скилл
    en:
      - delete skill
      - clean skill references
---

# Удаление скилла

Очистка ссылок на удаляемый скилл из существующих скиллов, агентов и индексов.

**Связанные скиллы:**
- [skill-create](/.claude/skills/skill-create/SKILL.md) — создание скилла
- [skill-update](/.claude/skills/skill-update/SKILL.md) — интеграция скилла
- [context-update](/.claude/skills/context-update/SKILL.md) — обновление контекста после изменений

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/skill-delete <имя-скилла>
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `имя-скилла` | Имя удалённого скилла | — (обязательный) |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать SSOT-инструкции:
> 1. [integration.md](/.claude/instructions/skills/integration.md) — типы ссылок, паттерны удаления
> 2. [errors.md](/.claude/instructions/skills/errors.md) — обработка ошибок
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

<!--
ПРАВИЛО: Шаги содержат ТОЛЬКО название и ссылку на SSOT.
Детали, алгоритмы, примеры — в SSOT-инструкциях.
LLM ОБЯЗАН прочитать SSOT перед выполнением шага.
-->

### Шаг 1: Получить имя скилла

> **SSOT:** [workflow.md](/.claude/instructions/skills/workflow.md#получение-скилла)

### Шаг 2: Проверить факт удаления

> **SSOT:** [validation.md](/.claude/instructions/skills/validation.md#проверка-существования)

### Шаг 3: Найти ссылки

> **SSOT:** [integration.md](/.claude/instructions/skills/integration.md#типы-ссылок)

### Шаг 4: Сформировать предложения

> **SSOT:** [integration.md](/.claude/instructions/skills/integration.md#формат-удаления)

### Шаг 5: Применить изменения

> **SSOT:** [integration.md](/.claude/instructions/skills/integration.md#удаление-ссылок)

### Шаг 6: Обновить контекст

> **SSOT:** [workflow.md](/.claude/instructions/skills/workflow.md#обновление-контекста)

### Шаг 7: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 8: Результат

> **SSOT:** [workflow.md](/.claude/instructions/skills/workflow.md#формат-результата)

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Получил имя скилла
- [ ] Проверил факт удаления
- [ ] Нашёл ссылки
- [ ] Сформировал предложения
- [ ] Применил изменения
- [ ] Обновил контекст
- [ ] Вывел итоговый отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/instructions/skills/examples.md#skill-delete)
