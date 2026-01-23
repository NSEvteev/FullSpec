---
name: issue-execute
description: Взятие GitHub Issue в работу
allowed-tools: Read, Bash
category: git
triggers:
  commands:
    - /issue-execute
  phrases:
    ru:
      - возьми задачу
      - начни задачу
      - работаю над
      - выполни таски
      - выполни задачи
    en:
      - take issue
      - start issue
      - work on
      - execute tasks
---

# Взятие Issue в работу

Команда для полного цикла работы с GitHub Issue: подготовка, выполнение задачи, закрытие.

## SSOT-инструкции

> **Вся информация по правилам, workflow и примерам находится в SSOT:**

| Аспект | Инструкция |
|--------|------------|
| Жизненный цикл Issue | [issues/workflow.md#lifecycle](/.claude/.instructions/workflow/.github/issues/workflow.md#lifecycle) |
| Детальный workflow | [issues/workflow.md#issue-execute](/.claude/.instructions/workflow/.github/issues/workflow.md#issue-execute) |
| Формат ветки | [git/workflow.md](/.claude/.instructions/workflow/git/workflow.md) |
| Команды gh CLI | [issues/commands.md](/.claude/.instructions/workflow/.github/issues/commands.md) |
| Обработка ошибок | [issues/errors.md](/.claude/.instructions/workflow/.github/issues/errors.md) |
| Примеры использования | [issues/examples.md](/.claude/.instructions/workflow/.github/issues/examples.md) |

---

## Формат вызова

```
/issue-execute <номер> [--no-branch] [--branch-name <имя>] [--continue]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `номер` | Номер Issue | — (обязательный) |
| `--no-branch` | Не создавать ветку | false |
| `--branch-name` | Кастомное имя ветки | Автогенерация |
| `--continue` | Продолжить последний Issue | false |

**Примеры:**
```
/issue-execute 123
/issue-execute 123 --no-branch
/issue-execute 123 --branch-name feature/oauth-login
/issue-execute --continue
```

---

## Воркфлоу (краткий)

> **Детали:** [issues/workflow.md#issue-execute](/.claude/.instructions/workflow/.github/issues/workflow.md#issue-execute)

```
Шаг 0: /environment-check github --fix
    ↓
Шаг 1: Получить номер Issue
    ↓
Шаг 2: Показать Issue, получить подтверждение
    ↓
Шаг 3: Назначить исполнителя (@me)
    ↓
Шаг 4: Добавить метку in-progress
    ↓
Шаг 5: Создать ветку (feature/{num}-{slug})
    ↓
Шаг 6: Добавить комментарий
    ↓
Шаг 7: Выполнить задачу
    ↓
Шаг 8: Вызвать /issue-review
```

### Формат ветки

| Тип Issue | Префикс ветки | Пример |
|-----------|---------------|--------|
| feature | `feature/` | `feature/123-oauth-auth` |
| bug | `fix/` | `fix/124-email-bug` |
| enhancement | `feature/` | `feature/125-ci-pipeline` |

---

## Чек-лист

- [ ] Окружение проверено
- [ ] Номер Issue получен
- [ ] Issue показан, подтверждение получено
- [ ] Исполнитель назначен
- [ ] Метка `in-progress` добавлена
- [ ] Ветка создана (или `--no-branch`)
- [ ] Комментарий добавлен
- [ ] Задача выполнена
- [ ] `/issue-review` вызван

---

## Связанные скиллы

| Скилл | Назначение |
|-------|------------|
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Создать Issue |
| [/issue-review](/.claude/skills/issue-review/SKILL.md) | Ревью после выполнения |
| [/issue-complete](/.claude/skills/issue-complete/SKILL.md) | Закрыть как выполненный |
| [/issue-update](/.claude/skills/issue-update/SKILL.md) | Обновить Issue |

---

## Utility-скиллы

| Скилл | Когда вызывать |
|-------|----------------|
| [/environment-check](/.claude/skills/environment-check/SKILL.md) | Шаг 0: проверка gh/git |
