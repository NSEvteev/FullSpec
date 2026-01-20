---
name: test-update
description: Изменение существующего теста
allowed-tools: Read, Edit, Glob, Grep
category: testing
triggers:
  commands:
    - /test-update
  phrases:
    ru:
      - обнови тест
      - измени тест
    en:
      - update test
      - modify test
---

# Изменение теста

Команда для обновления существующего теста.

**Связанные скиллы:**
- [test-create](/.claude/skills/test-create/SKILL.md) — создание теста
- [test-execute](/.claude/skills/test-execute/SKILL.md) — выполнение тестов
- [test-review](/.claude/skills/test-review/SKILL.md) — проверка полноты теста
- [test-complete](/.claude/skills/test-complete/SKILL.md) — отметка о прохождении
- [test-delete](/.claude/skills/test-delete/SKILL.md) — удаление теста

**Связанные инструкции:**
- [tools/claude-testing.md](/.claude/instructions/tools/claude-testing.md) — тестирование Claude Code
- [tools/project-testing.md](/.claude/instructions/tools/project-testing.md) — тестирование проекта

## Формат вызова

```
/test-update [путь-к-тесту]
```

## Воркфлоу

### Шаг 1: Определить тест

1. Из аргумента или спросить путь
2. Прочитать текущий тест

### Шаг 2: Определить изменения

1. Спросить что изменить:
   - Добавить сценарии
   - Исправить ожидания
   - Обновить под изменённый код

### Шаг 3: Применить изменения

1. Редактировать файл теста
2. Показать diff
3. Запросить подтверждение

### Шаг 4: Результат

```
✅ Тест обновлён

Файл: {путь}
Изменения:
- Добавлено: {N} сценариев
- Изменено: {M} ожиданий

Запустить тест? [Y/n]
```

## Примеры

### Пример 1: Добавить сценарий

```
/test-update .claude/skills/issue-create/SKILL.md

> Что изменить?
Добавить тест на невалидный ввод

Добавлен сценарий:
- Тест: невалидный заголовок Issue
- Ожидание: сообщение об ошибке

✅ Тест обновлён
```
