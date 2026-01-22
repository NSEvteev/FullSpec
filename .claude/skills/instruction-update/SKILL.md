---
name: instruction-update
description: Проверка файлов проекта на соответствие изменённой инструкции
allowed-tools: Read, Edit, Glob, Grep
category: instruction-management
triggers:
  commands:
    - /instruction-update
  phrases:
    ru:
      - обнови инструкцию
      - проверь инструкцию
      - валидируй инструкцию
    en:
      - update instruction
      - validate instruction
      - check instruction
---

# Обновление инструкции

Проверка файлов проекта на соответствие правилам инструкции. Находит несоответствия и формирует список TODO.

**Связанные скиллы:**
- [instruction-create](/.claude/skills/instruction-create/SKILL.md) — создание инструкций
- [instruction-deactivate](/.claude/skills/instruction-deactivate/SKILL.md) — деактивация инструкций
- [context-update](/.claude/skills/context-update/SKILL.md) — распространение контекста
- [test-update](/.claude/skills/test-update/SKILL.md) — обновление связанных тестов

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/instruction-update <путь>
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь` | Путь к инструкции (относительно `/.claude/instructions/`) | — (обязательный) |

**Примеры:**
- `/instruction-update src/api/design.md`
- `/instruction-update git/commits.md`

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [workflow-update.md](/.claude/instructions/instructions/workflow-update.md) — **детальный воркфлоу UPDATE (12 шагов)**
> 2. [validation.md](/.claude/instructions/instructions/validation.md) — формат файлов
> 3. [patterns.md](/.claude/instructions/instructions/patterns.md) — паттерны поиска
> 4. [relations.md](/.claude/instructions/instructions/relations.md) — проверка связей (governed-by, related)
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Получить путь

> **SSOT:** [workflow-update.md](/.claude/instructions/instructions/workflow-update.md#шаг-1-получить-путь)

### Шаг 2: Определить зону ответственности (согласно workflow-update.md)

> **SSOT:** [workflow-update.md](/.claude/instructions/instructions/workflow-update.md#шаг-2-определить-зону-ответственности)

### Шаг 3: Найти файлы в зоне

> **SSOT:** [workflow-update.md](/.claude/instructions/instructions/workflow-update.md#шаг-3-найти-файлы-в-зоне)

### Шаг 4: Извлечь правила из инструкции

> **SSOT:** [workflow-update.md](/.claude/instructions/instructions/workflow-update.md#шаг-4-извлечь-правила)

### Шаг 5: Проверить файлы на соответствие

> **SSOT:** [workflow-update.md](/.claude/instructions/instructions/workflow-update.md#шаг-5-проверить-файлы)

### Шаг 6: Сформировать список несоответствий

> **SSOT:** [workflow-update.md](/.claude/instructions/instructions/workflow-update.md#шаг-6-сформировать-список-несоответствий)

### Шаг 7: Внести изменения в инструкцию (добавить TODO или изменить правила)

> **SSOT:** [workflow-update.md](/.claude/instructions/instructions/workflow-update.md#шаг-7-внести-изменения-в-инструкцию)

### Шаг 8: Обновить README папки

> **SSOT:** [workflow-update.md](/.claude/instructions/instructions/workflow-update.md#шаг-8-обновить-readme-папки)

### Шаг 9: Обновить контекст скиллов → /context-update

> **SSOT:** [SKILL.md](/.claude/skills/context-update/SKILL.md)

### Шаг 10: Проверить связанные тесты → /test-update

> **SSOT:** [SKILL.md](/.claude/skills/test-update/SKILL.md)

### Шаг 11: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 12: Результат

```
✅ Проверка инструкции завершена

Инструкция: /.claude/instructions/{путь}
Зона ответственности: {зона}

Статистика:
- Проверено файлов: {N}
- Найдено несоответствий: {M}
- Файлов без проблем: {K}

Связанные скиллы обновлены: {P}
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Получил путь к инструкции
- [ ] Определил зону ответственности
- [ ] Нашёл файлы в зоне
- [ ] Извлёк правила из инструкции
- [ ] Проверил файлы на соответствие
- [ ] Сформировал список несоответствий
- [ ] Внёс изменения в инструкцию (если требуется)
- [ ] Обновил README папки
- [ ] Вызвал /context-update
- [ ] Проверил связанные тесты
- [ ] Вывел итоговый отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/instructions/instructions/examples.md#instruction-update)
