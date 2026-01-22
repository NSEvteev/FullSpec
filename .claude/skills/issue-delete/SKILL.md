---
name: issue-delete
description: Закрытие GitHub Issue как неактуального
allowed-tools: Read, Bash
category: git
triggers:
  commands:
    - /issue-delete
  phrases:
    ru:
      - закрой как неактуальный
      - задача неактуальна
      - удали задачу
    en:
      - close as not planned
      - delete issue
      - mark as not planned
---

# Закрытие Issue как неактуального

Команда для закрытия GitHub Issue как неактуального (not planned).

## SSOT-инструкции

> **Вся информация по правилам, workflow и примерам находится в SSOT:**

| Аспект | Инструкция |
|--------|------------|
| Жизненный цикл Issue | [issues/workflow.md#lifecycle](/.claude/instructions/issues/workflow.md#lifecycle) |
| Детальный workflow | [issues/workflow.md#issue-delete](/.claude/instructions/issues/workflow.md#issue-delete) |
| Команды gh CLI | [issues/commands.md](/.claude/instructions/issues/commands.md) |
| Обработка ошибок | [issues/errors.md](/.claude/instructions/issues/errors.md) |
| Примеры использования | [issues/examples.md](/.claude/instructions/issues/examples.md) |

---

## Формат вызова

```
/issue-delete <номер> [--reason <причина>] [--comment "<комментарий>"]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `номер` | Номер Issue | — (обязательный) |
| `--reason` | Причина: `not_planned`, `duplicate` | not_planned |
| `--comment` | Комментарий при закрытии | — |

**Примеры:**
```
/issue-delete 123 --comment "Неактуально"
/issue-delete 123 --reason duplicate --comment "Дубликат #100"
```

---

## Воркфлоу (краткий)

> **Детали:** [issues/workflow.md#issue-delete](/.claude/instructions/issues/workflow.md#issue-delete)

```
Шаг 0: /environment-check github --fix
    ↓
Шаг 1: Получить номер Issue
    ↓
Шаг 2: Показать текущее состояние
    ↓
Шаг 3: Определить причину закрытия
    ↓
Шаг 4: Добавить комментарий
    ↓
Шаг 5: Закрыть Issue (--reason "not planned")
    ↓
Шаг 6: Результат
```

### Причины закрытия

| Причина | Описание |
|---------|----------|
| `not_planned` | Неактуально / отменено |
| `duplicate` | Дубликат другого Issue |

---

## Чек-лист

- [ ] Окружение проверено
- [ ] Номер Issue получен
- [ ] Текущее состояние показано
- [ ] Причина закрытия определена
- [ ] Комментарий добавлен (если указан)
- [ ] Issue закрыт через `gh issue close`
- [ ] Результат выведен

---

## Связанные скиллы

| Скилл | Назначение |
|-------|------------|
| [/issue-complete](/.claude/skills/issue-complete/SKILL.md) | Закрыть как выполненный |
| [/issue-reopen](/.claude/skills/issue-reopen/SKILL.md) | Переоткрыть Issue |
| [/issue-update](/.claude/skills/issue-update/SKILL.md) | Обновить Issue |

---

## Utility-скиллы

| Скилл | Когда вызывать |
|-------|----------------|
| [/environment-check](/.claude/skills/environment-check/SKILL.md) | Шаг 0: проверка gh/git |
