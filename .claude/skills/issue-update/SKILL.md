---
name: issue-update
description: Обновление описания и меток GitHub Issue
allowed-tools: Read, Bash
category: git
triggers:
  commands:
    - /issue-update
  phrases:
    ru:
      - обнови задачу
      - обнови issue
      - измени задачу
    en:
      - update issue
      - edit issue
      - modify task
---

# Обновление Issue

Команда для обновления описания, меток и статуса GitHub Issue.

## SSOT-инструкции

> **Вся информация по правилам, workflow и примерам находится в SSOT:**

| Аспект | Инструкция |
|--------|------------|
| Система меток | [issues/labels.md](/.claude/instructions/issues/labels.md) |
| Детальный workflow | [issues/workflow.md#issue-update](/.claude/instructions/issues/workflow.md#issue-update) |
| Команды gh CLI | [issues/commands.md](/.claude/instructions/issues/commands.md) |
| Обработка ошибок | [issues/errors.md](/.claude/instructions/issues/errors.md) |
| Примеры использования | [issues/examples.md](/.claude/instructions/issues/examples.md) |

---

## Формат вызова

```
/issue-update <номер> [--title "<заголовок>"] [--add-label <метка>] [--remove-label <метка>] [--body] [--comment "<текст>"]
```

| Параметр | Описание |
|----------|----------|
| `номер` | Номер Issue (обязательный) |
| `--title` | Новый заголовок |
| `--add-label` | Добавить метку |
| `--remove-label` | Удалить метку |
| `--body` | Редактировать тело Issue |
| `--comment` | Добавить комментарий |

**Примеры:**
```
/issue-update 123 --add-label "in-progress"
/issue-update 123 --title "[AUTH] Новый заголовок"
/issue-update 123 --comment "Начал работу"
/issue-update 123 --remove-label "priority:low" --add-label "priority:high"
```

---

## Воркфлоу (краткий)

> **Детали:** [issues/workflow.md#issue-update](/.claude/instructions/issues/workflow.md#issue-update)

```
Шаг 0: /environment-check github --fix
    ↓
Шаг 1: Получить номер Issue
    ↓
Шаг 2: Показать текущее состояние
    ↓
Шаг 3: Определить изменения
    ↓
Шаг 4: Применить изменения (gh issue edit)
    ↓
Шаг 5: Результат
```

### Типы обновлений

| Тип | Команда gh |
|-----|------------|
| Заголовок | `gh issue edit {num} --title "..."` |
| Добавить метку | `gh issue edit {num} --add-label "..."` |
| Удалить метку | `gh issue edit {num} --remove-label "..."` |
| Тело | `gh issue edit {num} --body "..."` |
| Комментарий | `gh issue comment {num} --body "..."` |

---

## Чек-лист

- [ ] Окружение проверено
- [ ] Номер Issue получен
- [ ] Текущее состояние показано
- [ ] Изменения определены
- [ ] Изменения применены через `gh issue edit`
- [ ] Результат выведен

---

## Связанные скиллы

| Скилл | Назначение |
|-------|------------|
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Создать Issue |
| [/issue-execute](/.claude/skills/issue-execute/SKILL.md) | Взять в работу |
| [/issue-complete](/.claude/skills/issue-complete/SKILL.md) | Закрыть Issue |
| [/issue-reopen](/.claude/skills/issue-reopen/SKILL.md) | Переоткрыть Issue |

---

## Utility-скиллы

| Скилл | Когда вызывать |
|-------|----------------|
| [/environment-check](/.claude/skills/environment-check/SKILL.md) | Шаг 0: проверка gh/git |
