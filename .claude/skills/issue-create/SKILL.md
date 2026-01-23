---
name: issue-create
description: Создание GitHub Issue с правильным форматом
allowed-tools: Read, Bash, Glob
category: git
triggers:
  commands:
    - /issue-create
  phrases:
    ru:
      - создай задачу
      - создай issue
      - новая задача
    en:
      - create issue
      - new issue
      - create task
---

# Создание Issue

Команда для создания GitHub Issue с правильным форматом: префикс, метки, шаблон описания.

## SSOT-инструкции

> **Вся информация по правилам, workflow и примерам находится в SSOT:**

| Аспект | Инструкция |
|--------|------------|
| Формат заголовка, префиксы | [issues/format.md](/.claude/.instructions/workflow/.github/issues/format.md) |
| Система меток | [issues/labels.md](/.claude/.instructions/workflow/.github/issues/labels.md) |
| Детальный workflow | [issues/workflow.md#issue-create](/.claude/.instructions/workflow/.github/issues/workflow.md#issue-create) |
| Команды gh CLI | [issues/commands.md](/.claude/.instructions/workflow/.github/issues/commands.md) |
| Обработка ошибок | [issues/errors.md](/.claude/.instructions/workflow/.github/issues/errors.md) |
| Примеры использования | [issues/examples.md](/.claude/.instructions/workflow/.github/issues/examples.md) |

---

## Формат вызова

```
/issue-create [--service <сервис>] [--type <тип>] [--priority <приоритет>] [--dry-run] [--auto] "<заголовок>"
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--service` | Сервис (auth, notify, pay, users, gw, infra, docs) | Из контекста |
| `--type` | Тип (feature, bug, enhancement) | feature |
| `--priority` | Приоритет (high, medium, low) | — |
| `--dry-run` | Показать план без создания | false |
| `--auto` | Без подтверждения | false |
| `заголовок` | Описание задачи | — (обязательный) |

**Примеры:**
```
/issue-create --service auth "Добавить OAuth авторизацию"
/issue-create --service notify --type bug "Email не отправляется"
/issue-create --service pay --dry-run "Добавить Stripe"
```

---

## Воркфлоу (краткий)

> **Детали:** [issues/workflow.md#issue-create](/.claude/.instructions/workflow/.github/issues/workflow.md#issue-create)

```
Шаг 0: /environment-check github --fix
    ↓
Шаг 1: Определить сервис
    ↓
Шаг 2: Сформировать заголовок [PREFIX]
    ↓
Шаг 3: Определить метки
    ↓
Шаг 4: Сформировать тело Issue
    ↓
Шаг 5: Показать предпросмотр
    ↓
Шаг 6: Создать Issue (gh issue create)
    ↓
Шаг 7: Результат
```

---

## Чек-лист

- [ ] Окружение проверено (`gh` установлен, авторизован)
- [ ] Сервис определён (из параметра или контекста)
- [ ] Заголовок сформирован с правильным префиксом
- [ ] Метки определены (сервис + тип + приоритет)
- [ ] Тело Issue сформировано по шаблону
- [ ] Предпросмотр показан (или `--auto`)
- [ ] Issue создан через `gh issue create`
- [ ] Результат выведен с URL

---

## Связанные скиллы

| Скилл | Назначение |
|-------|------------|
| [/issue-execute](/.claude/skills/issue-execute/SKILL.md) | Взять Issue в работу |
| [/issue-update](/.claude/skills/issue-update/SKILL.md) | Обновить Issue |
| [/issue-review](/.claude/skills/issue-review/SKILL.md) | Ревью перед закрытием |
| [/issue-complete](/.claude/skills/issue-complete/SKILL.md) | Закрыть как выполненный |
| [/issue-delete](/.claude/skills/issue-delete/SKILL.md) | Закрыть как неактуальный |

---

## Utility-скиллы

| Скилл | Когда вызывать |
|-------|----------------|
| [/environment-check](/.claude/skills/environment-check/SKILL.md) | Шаг 0: проверка gh/git |
