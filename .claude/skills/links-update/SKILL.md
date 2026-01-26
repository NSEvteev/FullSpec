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
> 1. [standard-links.md](/.structure/.instructions/standard-links.md) — типы и форматы ссылок
> 2. [workflow-modify.md](/.structure/.instructions/workflow-modify.md) — воркфлоу изменения папок
>
> **НЕ ПРОДОЛЖАТЬ** пока инструкции не прочитаны.

### Шаг 1: Определить источник и тип

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md)

### Шаг 2: Найти связанные документы

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md#1-типы-ссылок)

### Шаг 3: Определить тип обновления (add/update/none)

> **SSOT:** [workflow-modify.md](/.structure/.instructions/workflow-modify.md#переименование)

### Шаг 4: Обновить документы

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md#4-ссылки-на-файлы)

### Шаг 5: Восстановить помеченные (если --old-name)

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md#5-якорные-ссылки)

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

> **SSOT:** [examples.md](/.claude/.instructions/.structure/links/examples.md#links-update)
