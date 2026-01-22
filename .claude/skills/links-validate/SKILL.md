---
name: links-validate
category: documentation
trigger: /links-validate
description: Валидация всех ссылок в проекте
critical: false
---

# /links-validate

Проверка всех ссылок в markdown-файлах проекта на валидность.

**Связанные скиллы:**
- [links-update](/.claude/skills/links-update/SKILL.md) — обновление ссылок
- [links-delete](/.claude/skills/links-delete/SKILL.md) — пометка битых
- [health-check](/.claude/skills/health-check/SKILL.md) — использует этот скилл

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/links-validate [путь] [--fix] [--dry-run] [--json]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь` | Файл или папка | Весь проект |
| `--fix` | Предложить исправления | false |
| `--dry-run` | Показать без изменений | false |
| `--json` | JSON формат | false |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [validation.md](/.claude/instructions/meta/links/validation.md) — правила валидации
> 2. [patterns.md](/.claude/instructions/meta/links/patterns.md) — паттерны поиска
> 3. [workflow.md](/.claude/instructions/meta/links/workflow.md#фаза-validate) — фаза VALIDATE
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все три файла.

### Шаг 1: Найти .md файлы в scope

> **SSOT:** [workflow.md](/.claude/instructions/meta/links/workflow.md#фаза-validate)

### Шаг 2: Извлечь все ссылки (согласно patterns.md)

> **SSOT:** [patterns.md](/.claude/instructions/meta/links/patterns.md#поиск-ссылок)

### Шаг 3: Валидировать каждую (согласно validation.md)

> **SSOT:** [validation.md](/.claude/instructions/meta/links/validation.md#правила-проверки)

### Шаг 4: Сформировать отчёт

> **SSOT:** [validation.md](/.claude/instructions/meta/links/validation.md#типы-ссылок)

### Шаг 5: (--fix) Предложить исправления

> **SSOT:** [validation.md](/.claude/instructions/meta/links/validation.md#режим---fix)

### Шаг 6: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 7: Результат

```
📋 Валидация ссылок

Проверено: {N} файлов, {M} ссылок
✅ Валидных: {K}
❌ Битых: {L}
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции
- [ ] Нашёл файлы
- [ ] Извлёк ссылки
- [ ] Провалидировал
- [ ] Сформировал отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/instructions/meta/links/examples.md#links-validate)
