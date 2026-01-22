---
name: links-update
description: Обновление ссылок на файлы и папки в связанных документах
allowed-tools: Read, Edit, Glob, Grep, Bash
category: documentation
triggers:
  commands:
    - /links-update
  phrases:
    ru:
      - обнови ссылки
      - синхронизируй ссылки
    en:
      - update links
      - sync links
---

# Обновление ссылок

Обновление ссылок в связанных документах при создании или переименовании файла/папки.

**Связанные скиллы:**
- [links-create](/.claude/skills/links-create/SKILL.md) — создание ссылок
- [links-delete](/.claude/skills/links-delete/SKILL.md) — пометка битых ссылок
- [context-update](/.claude/skills/context-update/SKILL.md) — обновление семантики

**Скрипты:**
- [update_links.py](/.claude/scripts/update_links.py) — массовая замена

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/links-update [путь] [--old-name старое-имя]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь` | Файл или папка-источник | Последний созданный |
| `--old-name` | Старое имя (при переименовании) | — |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [format.md](/.claude/instructions/links/format.md) — форматы ссылок (включая помеченные)
> 2. [patterns.md](/.claude/instructions/links/patterns.md) — паттерны поиска
> 3. [workflow.md](/.claude/instructions/links/workflow.md#фаза-update) — фаза UPDATE
> 4. [edge-cases.md](/.claude/instructions/links/edge-cases.md) — граничные случаи
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все четыре файла.

### Шаг 1: Определить источник и тип

> **SSOT:** [workflow.md](/.claude/instructions/links/workflow.md#фаза-update)

### Шаг 2: Найти связанные документы

> **SSOT:** [patterns.md](/.claude/instructions/links/patterns.md#поиск-ссылок)

### Шаг 3: Определить тип обновления (add/update/none)

> **SSOT:** [edge-cases.md](/.claude/instructions/links/edge-cases.md#оба-файла-существуют)

### Шаг 4: Обновить документы

> **SSOT:** [format.md](/.claude/instructions/links/format.md#стандартная-ссылка)

### Шаг 5: Восстановить помеченные (если --old-name)

> **SSOT:** [format.md](/.claude/instructions/links/format.md#помеченная-ссылка)

### Шаг 6: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 7: Результат

```
✅ Ссылки обновлены для {источник}

Обновлено: {N}
Без изменений: {M}
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции
- [ ] Определил источник
- [ ] Нашёл связанные документы
- [ ] Определил тип обновления
- [ ] Обновил документы
- [ ] Вывел отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/instructions/links/examples.md#links-update)
