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
> 1. [validation.md](/.claude/instructions/links/validation.md) — правила валидации
> 2. [patterns.md](/.claude/instructions/links/patterns.md) — паттерны поиска
> 3. [workflow.md](/.claude/instructions/links/workflow.md#фаза-validate) — фаза VALIDATE
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все три файла.

### Шаг 1: Найти .md файлы в scope

### Шаг 2: Извлечь все ссылки (согласно patterns.md)

### Шаг 3: Валидировать каждую (согласно validation.md)

### Шаг 4: Сформировать отчёт

### Шаг 5: (--fix) Предложить исправления

### Шаг 6: Результат

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
