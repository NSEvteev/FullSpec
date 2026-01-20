---
name: test-review
description: Проверка полноты и качества теста
allowed-tools: Read, Glob, Grep
category: testing
triggers:
  commands:
    - /test-review
  phrases:
    ru:
      - проверь тест
      - ревью теста
    en:
      - review test
      - check test
---

# Проверка теста

Команда для проверки полноты и качества теста.

**Связанные скиллы:**
- [test-create](/.claude/skills/test-create/SKILL.md) — создание теста
- [test-update](/.claude/skills/test-update/SKILL.md) — изменение теста
- [test-execute](/.claude/skills/test-execute/SKILL.md) — выполнение тестов

**Связанные инструкции:**
- [tools/claude-testing.md](/.claude/instructions/tools/claude-testing.md) — тестирование Claude Code
- [tests/README.md](/.claude/instructions/tests/README.md) — тестирование проекта

## Формат вызова

```
/test-review [путь-к-тесту]
```

## Воркфлоу

### Шаг 1: Определить тест

1. Из аргумента или спросить путь
2. Прочитать тест и тестируемый объект

### Шаг 2: Анализ покрытия

**Scope claude:**
- Проверены ли все триггеры?
- Покрыты ли все шаги воркфлоу?
- Есть ли тесты на ошибки?

**Scope project:**
- Покрытие функций
- Покрытие edge cases
- Покрытие ошибок

### Шаг 3: Отчёт

```
📋 Ревью теста: {путь}

Покрытие:
- Основные сценарии: ✅ 100%
- Граничные случаи: ⚠️ 50%
- Обработка ошибок: ❌ 0%

💡 Рекомендации:
1. Добавить тест на пустой ввод
2. Добавить тест на невалидные данные
3. Добавить тест на timeout

Улучшить тест? [Y/n]
```

## Примеры

### Пример 1: Ревью скилла

```
/test-review .claude/skills/issue-create/SKILL.md

📋 Ревью теста: issue-create

Покрытие:
- Триггеры: ✅ 100% (команда + фраза)
- Воркфлоу: ⚠️ 60% (шаги 1-3 из 5)
- Ошибки: ❌ 0%

💡 Рекомендации:
1. Добавить тест шага 4 (создание Issue)
2. Добавить тест на ошибку GitHub API

Улучшить тест? [Y/n]
```
