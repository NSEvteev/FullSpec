---
name: links-delete
description: Пометка битых ссылок при удалении файлов и папок
allowed-tools: Read, Edit, Glob, Grep
category: documentation
triggers:
  commands:
    - /links-delete
  phrases:
    ru:
      - удали ссылки
      - пометь битые ссылки
    en:
      - delete links
      - mark broken links
---

# Удаление ссылок

Пометка битых ссылок в документах при удалении файлов или папок. НЕ удаляет контент, а помечает для восстановления.

**Связанные скиллы:**
- [links-create](/.claude/skills/links-create/SKILL.md) — создание ссылок
- [links-update](/.claude/skills/links-update/SKILL.md) — восстановление ссылок
- [context-delete](/.claude/skills/context-delete/SKILL.md) — очистка контекста

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/links-delete <путь> [--dry-run] [--scan-all]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь` | Удалённый файл или папка | — (обязательный) |
| `--dry-run` | Показать без применения | false |
| `--scan-all` | Найти все битые ссылки | false |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [standard-links.md](/.structure/.instructions/standard-links.md) — типы и форматы ссылок
> 2. [workflow-modify.md](/.structure/.instructions/workflow-modify.md#удаление) — воркфлоу удаления
>
> **НЕ ПРОДОЛЖАТЬ** пока инструкции не прочитаны.

### Шаг 1: Получить путь, проверить несуществование

> **SSOT:** [workflow-modify.md](/.structure/.instructions/workflow-modify.md#удаление)

### Шаг 2: Найти все ссылки на путь

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md#1-типы-ссылок)

### Шаг 3: Показать diff для подтверждения

> **SSOT:** [workflow-modify.md](/.structure/.instructions/workflow-modify.md#чек-лист)

### Шаг 4: Применить пометки (согласно format.md)

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md#5-якорные-ссылки)

### Шаг 5: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 6: Результат

```
✅ Ссылки помечены как удалённые

Путь: {путь}
Помечено: {N} в {M} документах
```

---

## Режим --scan-all

Аудит всех битых ссылок в проекте (без указания конкретного пути).

---

## Чек-лист

- [ ] Прочитал SSOT инструкции
- [ ] Получил путь
- [ ] Нашёл ссылки
- [ ] Показал diff
- [ ] Применил пометки
- [ ] Вывел отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/.instructions/.structure/links/examples.md#links-delete)
