---
name: test-delete
description: Удаление теста
allowed-tools: Read, Edit, Bash
category: testing
triggers:
  commands:
    - /test-delete
  phrases:
    ru:
      - удали тест
    en:
      - delete test
      - remove test
---

# Удаление теста

Команда для удаления теста.

**Связанные скиллы:**
- [test-create](/.claude/skills/test-create/SKILL.md) — создание теста
- [test-update](/.claude/skills/test-update/SKILL.md) — изменение теста
- [test-execute](/.claude/skills/test-execute/SKILL.md) — выполнение тестов
- [test-review](/.claude/skills/test-review/SKILL.md) — проверка полноты теста
- [test-complete](/.claude/skills/test-complete/SKILL.md) — отметка о прохождении

**Связанные инструкции:**
- [tools/claude-testing.md](/.claude/instructions/tools/claude-testing.md) — тестирование Claude Code
- [tools/project-testing.md](/.claude/instructions/tools/project-testing.md) — тестирование проекта

## Формат вызова

```
/test-delete [путь-к-тесту] [--force]
```

## Воркфлоу

### Шаг 1: Определить тест

1. Из аргумента или спросить путь
2. Проверить существование теста

### Шаг 2: Подтверждение

```
⚠️ Удаление теста

Тест: {путь}
Тип: {smoke|functional|integration}
Последний результат: ✅ Passed

Удалить? [y/N]
```

### Шаг 3: Удаление

**Scope claude:**
- Удалить раздел "Тестирование" из SKILL.md
- Или удалить файл tests.md

**Scope project:**
- Удалить файл теста
- Обновить индексы (если есть)

### Шаг 4: Результат

```
✅ Тест удалён

Путь: {путь}
Тип: {scope}

Откатить: git checkout -- {путь}
```

## Примеры

### Пример 1: Удаление теста скилла

```
/test-delete .claude/skills/old-skill/SKILL.md

⚠️ Удаление теста

Тест: раздел "Тестирование" в old-skill/SKILL.md
Тип: smoke
Последний результат: ⬜ Не выполнен

Удалить? [y/N]
> y

Удалён раздел "Тестирование" из SKILL.md

✅ Тест удалён
```
