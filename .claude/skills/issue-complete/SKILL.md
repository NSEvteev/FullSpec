---
name: issue-complete
description: Закрытие GitHub Issue как выполненного
allowed-tools: Read, Bash
category: git
triggers:
  commands:
    - /issue-complete
  phrases:
    ru:
      - заверши задачу
      - закрой как выполненный
      - задача выполнена
    en:
      - complete issue
      - finish issue
      - close as completed
---

# Завершение Issue

Команда для закрытия GitHub Issue как выполненного (completed).

## SSOT-инструкции

> **Вся информация по правилам, workflow и примерам находится в SSOT:**

| Аспект | Инструкция |
|--------|------------|
| Жизненный цикл Issue | [issues/workflow.md#lifecycle](/.claude/.instructions/workflow/.github/issues/workflow.md#lifecycle) |
| Детальный workflow | [issues/workflow.md#issue-complete](/.claude/.instructions/workflow/.github/issues/workflow.md#issue-complete) |
| Команды gh CLI | [issues/commands.md](/.claude/.instructions/workflow/.github/issues/commands.md) |
| CI pipeline | [git/ci.md](/.claude/.instructions/workflow/git/ci.md) |
| Обработка ошибок | [issues/errors.md](/.claude/.instructions/workflow/.github/issues/errors.md) |
| Примеры использования | [issues/examples.md](/.claude/.instructions/workflow/.github/issues/examples.md) |

---

## Формат вызова

```
/issue-complete [номер | --last] [--pr <номер-pr>] [--comment <текст>]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `номер` | Номер Issue | — |
| `--last` | Последний Issue из state | false |
| `--pr` | Номер связанного PR | Автоопределение |
| `--comment` | Дополнительный комментарий | — |

**Примеры:**
```
/issue-complete 123
/issue-complete --last
/issue-complete 123 --pr 456
/issue-complete 123 --comment "Реализовано в v1.2.0"
```

---

## Воркфлоу (краткий)

> **Детали:** [issues/workflow.md#issue-complete](/.claude/.instructions/workflow/.github/issues/workflow.md#issue-complete)

```
Шаг 1: Получить номер Issue
    ↓
Шаг 2: Проверить статус (open, in-progress)
    ↓
Шаг 3: Проверить критерии готовности
    ↓
Шаг 4: Проверить связанный PR + CI статус
    ↓
Шаг 5: Добавить комментарий
    ↓
Шаг 6: Закрыть Issue (--reason completed)
    ↓
Шаг 7: Вызвать /docs-update
    ↓
Шаг 8: Результат
```

---

## Чек-лист

- [ ] Номер Issue получен
- [ ] Статус проверен (открыт, в работе)
- [ ] Критерии готовности проверены
- [ ] Связанный PR найден (или подтверждено без PR)
- [ ] CI статус проверен (если есть PR)
- [ ] Комментарий добавлен
- [ ] Issue закрыт как completed
- [ ] `/docs-update` вызван
- [ ] Результат выведен

---

## Связанные скиллы

| Скилл | Назначение |
|-------|------------|
| [/issue-review](/.claude/skills/issue-review/SKILL.md) | Вызывает этот скилл |
| [/issue-reopen](/.claude/skills/issue-reopen/SKILL.md) | Переоткрыть Issue |
| [/docs-update](/.claude/skills/docs-update/SKILL.md) | Обновить документацию |

---

## Utility-скиллы

| Скилл | Когда вызывать |
|-------|----------------|
| [/environment-check](/.claude/skills/environment-check/SKILL.md) | Шаг 0: проверка gh/git |
