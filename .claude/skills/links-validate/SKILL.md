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
> 1. [standard-links.md](/.structure/.instructions/standard-links.md) — типы и форматы ссылок
> 2. [validation-structure.md](/.structure/.instructions/validation-structure.md) — валидация структуры
>
> **НЕ ПРОДОЛЖАТЬ** пока инструкции не прочитаны.

### Шаг 1: Найти .md файлы в scope

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md)

### Шаг 2: Извлечь все ссылки (согласно patterns.md)

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md#1-типы-ссылок)

### Шаг 3: Валидировать каждую (согласно validation.md)

> **SSOT:** [validation-structure.md](/.structure/.instructions/validation-structure.md#шаг-3-проверить-ссылки)

### Шаг 4: Сформировать отчёт

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md#1-типы-ссылок)

### Шаг 5: (--fix) Предложить исправления

> **SSOT:** [standard-links.md](/.structure/.instructions/standard-links.md#8-скиллы)

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

> **SSOT:** [examples.md](/.claude/.instructions/.structure/links/examples.md#links-validate)
