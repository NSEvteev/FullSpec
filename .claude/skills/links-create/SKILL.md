---
name: links-create
description: Создание ссылок на файлы и папки репозитория в документе
allowed-tools: Read, Edit, Glob, Grep
category: documentation
triggers:
  commands:
    - /links-create
  phrases:
    ru:
      - создай ссылки
      - добавь ссылки
      - оформи ссылки
    en:
      - create links
      - add links
---

# Создание ссылок

Оформление упоминаний файлов и папок как markdown-ссылки.

**Связанные скиллы:**
- [links-update](/.claude/skills/links-update/SKILL.md) — обновление ссылок
- [links-delete](/.claude/skills/links-delete/SKILL.md) — пометка битых ссылок

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/links-create [путь-к-файлу] [--dry-run]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь-к-файлу` | Файл для обработки | Последний редактируемый .md |
| `--dry-run` | Показать план без изменений | false |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [format.md](/.claude/instructions/links/format.md) — форматы ссылок
> 2. [patterns.md](/.claude/instructions/links/patterns.md) — паттерны поиска и исключения
> 3. [workflow.md](/.claude/instructions/links/workflow.md#фаза-create) — фаза CREATE
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все три файла.

### Шаг 1: Получить документ

> **SSOT:** [workflow.md](/.claude/instructions/links/workflow.md#фаза-create)

### Шаг 2: Найти упоминания (согласно patterns.md)

> **SSOT:** [patterns.md](/.claude/instructions/links/patterns.md#поиск-упоминаний)

### Шаг 3: Проверить существование файлов

> **SSOT:** [patterns.md](/.claude/instructions/links/patterns.md#исключения)

### Шаг 4: Создать ссылки (согласно format.md)

> **SSOT:** [format.md](/.claude/instructions/links/format.md#стандартная-ссылка)

### Шаг 5: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 6: Результат

```
✅ Ссылки созданы в {файл}

Оформлено: {N}
Не найдено: {M}
Пропущено (код): {K}
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции
- [ ] Получил документ
- [ ] Нашёл упоминания
- [ ] Проверил существование
- [ ] Создал ссылки
- [ ] Вывел отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/instructions/links/examples.md#links-create)
