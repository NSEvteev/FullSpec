---
name: issue-reopen
description: Переоткрытие закрытого GitHub Issue
allowed-tools: Read, Bash, Glob
category: git
critical: true
triggers:
  commands:
    - /issue-reopen
  phrases:
    ru:
      - переоткрой issue
      - верни issue
      - открой снова
      - issue не закрыт
      - issue не выполнен
    en:
      - reopen issue
      - restore issue
      - open again
      - issue not done
---

# Переоткрытие Issue

Команда для переоткрытия ранее закрытого GitHub Issue с добавлением комментария о причине.

## SSOT-инструкции

> **Вся информация по правилам, workflow и примерам находится в SSOT:**

| Аспект | Инструкция |
|--------|------------|
| Жизненный цикл Issue | [issues/workflow.md#lifecycle](/.claude/instructions/issues/workflow.md#lifecycle) |
| Детальный workflow | [issues/workflow.md#issue-reopen](/.claude/instructions/issues/workflow.md#issue-reopen) |
| Команды gh CLI | [issues/commands.md](/.claude/instructions/issues/commands.md) |
| Обработка ошибок | [issues/errors.md](/.claude/instructions/issues/errors.md) |
| Примеры использования | [issues/examples.md](/.claude/instructions/issues/examples.md) |

---

## Формат вызова

```
/issue-reopen <#номер> ["причина"] [--assign] [--dry-run] [--json] [--priority <уровень>]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `#номер` | Номер Issue | — (обязательный) |
| `"причина"` | Комментарий о причине | — |
| `--assign` | Назначить на себя | false |
| `--dry-run` | Показать план без изменений | false |
| `--json` | JSON формат вывода | false |
| `--priority` | Установить приоритет | — |

**Примеры:**
```
/issue-reopen #123
/issue-reopen #123 "Задача не была полностью выполнена"
/issue-reopen #123 --assign
/issue-reopen #123 --priority high "Баг вернулся"
```

---

## Воркфлоу (краткий)

> **Детали:** [issues/workflow.md#issue-reopen](/.claude/instructions/issues/workflow.md#issue-reopen)

```
Шаг 0: /environment-check github --fix
    ↓
Шаг 1: Получить информацию об Issue
    ↓
Шаг 2: Проверить статус (должен быть CLOSED)
    ↓
Шаг 3: Показать информацию, подтверждение
    ↓
Шаг 4: Переоткрыть Issue (gh issue reopen)
    ↓
Шаг 5: Добавить комментарий (если указана причина)
    ↓
Шаг 6: Назначить на себя (если --assign)
    ↓
Шаг 7: Результат
```

### Когда использовать

| Ситуация | Действие |
|----------|----------|
| Закрыто преждевременно | `/issue-reopen` |
| Новые требования | `/issue-reopen` с комментарием |
| Баг вернулся | `/issue-reopen --priority high` |
| Решение неполное | `/issue-reopen --assign` |

---

## Чек-лист

- [ ] Окружение проверено
- [ ] Информация об Issue получена
- [ ] Статус проверен (был CLOSED)
- [ ] Подтверждение получено
- [ ] Issue переоткрыт
- [ ] Комментарий добавлен (если указан)
- [ ] Назначение выполнено (если `--assign`)
- [ ] Результат выведен

---

## Связанные скиллы

| Скилл | Назначение |
|-------|------------|
| [/issue-execute](/.claude/skills/issue-execute/SKILL.md) | Взять в работу |
| [/issue-update](/.claude/skills/issue-update/SKILL.md) | Обновить Issue |
| [/issue-complete](/.claude/skills/issue-complete/SKILL.md) | Закрыть как выполненный |
| [/issue-delete](/.claude/skills/issue-delete/SKILL.md) | Закрыть как неактуальный |

---

## Utility-скиллы

| Скилл | Когда вызывать |
|-------|----------------|
| [/environment-check](/.claude/skills/environment-check/SKILL.md) | Шаг 0: проверка gh/git |
| [/input-validate](/.claude/skills/input-validate/SKILL.md) | Валидация номера Issue |
