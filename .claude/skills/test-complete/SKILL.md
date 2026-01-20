---
name: test-complete
description: Отметка теста как пройденного
allowed-tools: Read, Edit
category: testing
triggers:
  commands:
    - /test-complete
  phrases:
    ru:
      - тест пройден
      - отметь тест
    en:
      - test passed
      - mark test complete
---

# Отметка теста

Команда для отметки теста как пройденного.

**Связанные скиллы:**
- [test-create](/.claude/skills/test-create/SKILL.md) — создание теста
- [test-update](/.claude/skills/test-update/SKILL.md) — изменение теста
- [test-execute](/.claude/skills/test-execute/SKILL.md) — выполнение тестов
- [test-review](/.claude/skills/test-review/SKILL.md) — проверка полноты теста
- [test-delete](/.claude/skills/test-delete/SKILL.md) — удаление теста

**Связанные инструкции:**
- [tools/claude-testing.md](/.claude/instructions/tools/claude-testing.md) — тестирование Claude Code
- [tools/project-testing.md](/.claude/instructions/tools/project-testing.md) — тестирование проекта

## Формат вызова

```
/test-complete [путь-к-тесту] [--status passed|failed|skipped]
```

## Воркфлоу

### Шаг 1: Определить тест

1. Из аргумента или из последнего выполненного теста
2. Проверить существование теста

### Шаг 2: Обновить статус

1. Найти строку `Результат: ⬜ Не выполнен`
2. Заменить на `Результат: ✅ Passed` (или ❌ Failed)
3. Добавить дату и время

### Шаг 3: Результат

```
✅ Тест отмечен

Тест: {название}
Статус: ✅ Passed
Дата: 2026-01-20 15:30

История:
- 2026-01-20: ✅ Passed
- 2026-01-19: ❌ Failed
- 2026-01-18: ✅ Passed
```

## Примеры

### Пример 1: После успешного теста

```
/test-complete .claude/skills/issue-create/SKILL.md

Обновлён статус теста:
- Было: Результат: ⬜ Не выполнен
- Стало: Результат: ✅ Passed (2026-01-20)

✅ Тест отмечен как пройденный
```
