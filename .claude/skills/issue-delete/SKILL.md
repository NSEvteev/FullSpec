---
name: issue-delete
description: Закрытие GitHub Issue с комментарием
allowed-tools: Read, Bash
category: git
triggers:
  commands:
    - /issue-delete
  phrases:
    ru:
      - закрой задачу
      - закрой issue
      - удали задачу
    en:
      - close issue
      - delete issue
      - remove task
---

# Закрытие Issue

Команда для закрытия GitHub Issue с комментарием и указанием причины.

**Связанная инструкция:** [/.claude/instructions/git/issues.md](/.claude/instructions/git/issues.md)

**Связанные скиллы:**
- [issue-create](/.claude/skills/issue-create/SKILL.md) — создание Issue
- [issue-update](/.claude/skills/issue-update/SKILL.md) — обновление Issue
- [issue-execute](/.claude/skills/issue-execute/SKILL.md) — взятие Issue в работу

## Оглавление

- [Формат вызова](#формат-вызова)
- [Причины закрытия](#причины-закрытия)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/issue-delete <номер> [--reason <причина>] [--comment "<комментарий>"]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `номер` | Номер Issue (обязательный) | — |
| `--reason` | Причина: `completed`, `not_planned`, `duplicate` | completed |
| `--comment` | Комментарий при закрытии | — |

**Примеры:**
- `/issue-delete 123 --comment "Выполнено в PR #456"`
- `/issue-delete 123 --reason not_planned --comment "Неактуально"`
- `/issue-delete 123 --reason duplicate --comment "Дубликат #100"`

---

## Причины закрытия

| Причина | Описание | Команда gh |
|---------|----------|-----------|
| `completed` | Задача выполнена | `gh issue close {num}` |
| `not_planned` | Неактуально / отменено | `gh issue close {num} --reason "not planned"` |
| `duplicate` | Дубликат другого Issue | `gh issue close {num} --reason "not planned"` + комментарий |

---

## Воркфлоу

### Шаг 1: Получить номер Issue

1. Из аргумента: `/issue-delete 123`
2. Проверить существование и статус

### Шаг 2: Показать текущее состояние

```
📋 Issue #123

Заголовок: [AUTH] Добавить OAuth авторизацию
Статус: open
Метки: service:auth, feature, in-progress
```

### Шаг 3: Определить причину

1. Из параметра `--reason`
2. Или спросить:
   ```
   Причина закрытия?
   [1] Выполнено (completed)
   [2] Неактуально (not_planned)
   [3] Дубликат (duplicate)
   ```

### Шаг 4: Добавить комментарий (если есть)

```bash
gh issue comment 123 --body "Выполнено в PR #456"
```

### Шаг 5: Закрыть Issue

```bash
gh issue close 123 --reason "completed"
```

### Шаг 6: Результат

```
✅ Issue #123 закрыт

Причина: completed
Комментарий: Выполнено в PR #456

URL: https://github.com/user/repo/issues/123
```

---

## Чек-лист

- [ ] **Шаг 1:** Получил номер Issue
- [ ] **Шаг 2:** Показал текущее состояние
- [ ] **Шаг 3:** Определил причину закрытия
- [ ] **Шаг 4:** Добавил комментарий (если указан)
- [ ] **Шаг 5:** Закрыл Issue через `gh issue close`
- [ ] **Шаг 6:** Вывел результат

---

## Примеры

### Пример 1: Задача выполнена

**Вызов:**
```
/issue-delete 123 --comment "Выполнено в PR #456"
```

**Результат:**
```
✅ Issue #123 закрыт

Причина: completed
Комментарий: Выполнено в PR #456
```

### Пример 2: Задача неактуальна

**Вызов:**
```
/issue-delete 123 --reason not_planned --comment "Требования изменились, задача неактуальна"
```

**Результат:**
```
✅ Issue #123 закрыт

Причина: not_planned
Комментарий: Требования изменились, задача неактуальна
```

### Пример 3: Дубликат

**Вызов:**
```
/issue-delete 123 --reason duplicate --comment "Дубликат #100"
```

**Результат:**
```
✅ Issue #123 закрыт

Причина: duplicate
Комментарий: Дубликат #100
```

### Пример 4: Интерактивный режим

**Вызов:**
```
/issue-delete 123
```

**Вывод:**
```
📋 Issue #123

Заголовок: [AUTH] Добавить OAuth авторизацию
Статус: open

Причина закрытия?
[1] Выполнено
[2] Неактуально
[3] Дубликат

> 1

Добавить комментарий? (Enter для пропуска)
> Реализовано в PR #456

✅ Issue #123 закрыт
Причина: completed
Комментарий: Реализовано в PR #456
```

### Пример 5: Issue уже закрыт

**Вызов:**
```
/issue-delete 123
```

**Вывод:**
```
ℹ️ Issue #123 уже закрыт

Статус: closed
Закрыт: 2024-01-15
Причина: completed

Переоткрыть? [y/N]
> N

Операция отменена.
```
