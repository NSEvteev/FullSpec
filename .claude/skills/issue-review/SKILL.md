---
name: issue-review
description: Ревью решения перед закрытием Issue
allowed-tools: Read, Bash, Edit, Glob, Grep
category: git
triggers:
  commands:
    - /issue-review
  phrases:
    ru:
      - проверь решение
      - ревью задачи
      - оцени реализацию
    en:
      - review solution
      - review issue
      - check implementation
---

# Ревью решения

Команда для проверки качества решения перед закрытием Issue. Автоматически вызывается после `/issue-execute`.

## SSOT-инструкции

> **Вся информация по правилам, workflow и примерам находится в SSOT:**

| Аспект | Инструкция |
|--------|------------|
| Критерии ревью | [issues/workflow.md#issue-review](/.claude/instructions/workflow/github/issues/workflow.md#issue-review) |
| Чек-лист self-review | [git/review.md#чек-лист-self-review](/.claude/instructions/workflow/git/review.md#чек-лист-self-review) |
| Команды gh CLI | [issues/commands.md](/.claude/instructions/workflow/github/issues/commands.md) |
| Обработка ошибок | [issues/errors.md](/.claude/instructions/workflow/github/issues/errors.md) |
| Примеры использования | [issues/examples.md](/.claude/instructions/workflow/github/issues/examples.md) |

---

## Формат вызова

```
/issue-review [номер | --last] [--auto] [--strict]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `номер` | Номер Issue | — |
| `--last` | Последний Issue из state | false |
| `--auto` | Автоматический режим | false |
| `--strict` | Строгий режим | false |

**Примеры:**
```
/issue-review 123
/issue-review --last
/issue-review 123 --auto
/issue-review 123 --strict
```

---

## Воркфлоу (краткий)

> **Детали:** [issues/workflow.md#issue-review](/.claude/instructions/workflow/github/issues/workflow.md#issue-review)

```
Шаг 1: Получить контекст (Issue, файлы)
    ↓
Шаг 2: Проверить качество кода (lint, types)
    ↓
Шаг 3: Оценить реализацию, собрать предложения
    ↓
Шаг 4: Проверить тесты
    ↓
Шаг 5: Проверить критерии готовности
    ↓
Шаг 6: Сформировать отчёт
    ↓
Шаг 7: Применить исправления (если есть)
    ↓
Шаг 8: Принять решение (complete / reject)
```

### Критерии ревью

| Аспект | Что проверяется | Блокирует |
|--------|-----------------|:---------:|
| Качество кода | Линтинг, типизация | ✅ |
| Оптимальность | Можно ли лучше | ⚠️ |
| Тесты | Проходят, покрытие | ✅ |
| Критерии готовности | Все пункты из Issue | ✅ |

---

## Чек-лист

- [ ] Информация об Issue получена
- [ ] Изменённые файлы определены
- [ ] Линтер запущен (если есть)
- [ ] Типизация проверена (если есть)
- [ ] Код прочитан, предложения собраны
- [ ] Тесты запущены
- [ ] Критерии готовности проверены
- [ ] Отчёт сформирован
- [ ] Исправления применены (если есть)
- [ ] `/issue-complete` вызван (если пройдено)

---

## Связанные скиллы

| Скилл | Назначение |
|-------|------------|
| [/issue-execute](/.claude/skills/issue-execute/SKILL.md) | Вызывает этот скилл |
| [/issue-complete](/.claude/skills/issue-complete/SKILL.md) | Вызывается при успехе |
| [/issue-update](/.claude/skills/issue-update/SKILL.md) | Обновить Issue |

---

## Utility-скиллы

| Скилл | Когда вызывать |
|-------|----------------|
| [/environment-check](/.claude/skills/environment-check/SKILL.md) | Шаг 0: проверка gh/git |
