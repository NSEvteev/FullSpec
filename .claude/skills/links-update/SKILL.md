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

### Шаг 2: Найти связанные документы

### Шаг 3: Определить тип обновления (add/update/none)

### Шаг 4: Обновить документы

### Шаг 5: Восстановить помеченные (если --old-name)

### Шаг 6: Результат

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
