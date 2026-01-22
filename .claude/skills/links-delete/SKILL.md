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
> 1. [format.md](/.claude/instructions/meta/links/format.md) — форматы ссылок (секция "Помеченная ссылка")
> 2. [patterns.md](/.claude/instructions/meta/links/patterns.md) — паттерны поиска
> 3. [workflow.md](/.claude/instructions/meta/links/workflow.md#фаза-delete) — фаза DELETE
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все три файла.

### Шаг 1: Получить путь, проверить несуществование

> **SSOT:** [workflow.md](/.claude/instructions/meta/links/workflow.md#фаза-delete)

### Шаг 2: Найти все ссылки на путь

> **SSOT:** [patterns.md](/.claude/instructions/meta/links/patterns.md#поиск-ссылок)

### Шаг 3: Показать diff для подтверждения

> **SSOT:** [edge-cases.md](/.claude/instructions/meta/links/edge-cases.md#массовые-изменения)

### Шаг 4: Применить пометки (согласно format.md)

> **SSOT:** [format.md](/.claude/instructions/meta/links/format.md#помеченная-ссылка)

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

> **SSOT:** [examples.md](/.claude/instructions/meta/links/examples.md#links-delete)
