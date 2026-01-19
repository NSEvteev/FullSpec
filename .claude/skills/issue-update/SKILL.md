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

**Связанная инструкция:** [/.claude/instructions/git/issues.md](/.claude/instructions/git/issues.md)

**Связанные скиллы:**
- [issue-create](/.claude/skills/issue-create/SKILL.md) — создание Issue
- [issue-delete](/.claude/skills/issue-delete/SKILL.md) — закрытие Issue
- [issue-execute](/.claude/skills/issue-execute/SKILL.md) — взятие Issue в работу

## Оглавление

- [Формат вызова](#формат-вызова)
- [Типы обновлений](#типы-обновлений)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/issue-update <номер> [--title "<заголовок>"] [--add-label <метка>] [--remove-label <метка>] [--body]
```

| Параметр | Описание |
|----------|----------|
| `номер` | Номер Issue (обязательный) |
| `--title` | Новый заголовок |
| `--add-label` | Добавить метку |
| `--remove-label` | Удалить метку |
| `--body` | Редактировать тело Issue |

**Примеры:**
- `/issue-update 123 --add-label "in-progress"`
- `/issue-update 123 --title "[AUTH] Новый заголовок"`
- `/issue-update 123 --body`

---

## Типы обновлений

| Тип | Команда gh |
|-----|-----------|
| Изменить заголовок | `gh issue edit {num} --title "..."` |
| Добавить метку | `gh issue edit {num} --add-label "..."` |
| Удалить метку | `gh issue edit {num} --remove-label "..."` |
| Изменить тело | `gh issue edit {num} --body "..."` |
| Добавить комментарий | `gh issue comment {num} --body "..."` |

---

## Воркфлоу

### Шаг 1: Получить номер Issue

1. Из аргумента: `/issue-update 123`
2. Проверить существование: `gh issue view 123`

### Шаг 2: Показать текущее состояние

```
📋 Issue #123

Заголовок: [AUTH] Добавить OAuth авторизацию
Статус: open
Метки: service:auth, feature
Назначен: —

Тело:
---
## Описание
...
---
```

### Шаг 3: Определить изменения

1. Из параметров командной строки
2. Или интерактивно:
   ```
   Что обновить?
   [1] Заголовок
   [2] Метки
   [3] Тело
   [4] Добавить комментарий
   ```

### Шаг 4: Применить изменения

```bash
gh issue edit 123 --add-label "in-progress"
```

### Шаг 5: Результат

```
✅ Issue #123 обновлён

Изменения:
- Добавлена метка: in-progress

Текущее состояние:
- Метки: service:auth, feature, in-progress
```

---

## Чек-лист

- [ ] **Шаг 1:** Получил номер Issue
- [ ] **Шаг 2:** Показал текущее состояние
- [ ] **Шаг 3:** Определил изменения
- [ ] **Шаг 4:** Применил изменения через `gh issue edit`
- [ ] **Шаг 5:** Вывел результат

---

## Примеры

### Пример 1: Добавить метку

**Вызов:**
```
/issue-update 123 --add-label "in-progress"
```

**Результат:**
```
✅ Issue #123 обновлён

Добавлена метка: in-progress
```

### Пример 2: Изменить заголовок

**Вызов:**
```
/issue-update 123 --title "[AUTH] Добавить OAuth 2.0 авторизацию"
```

**Результат:**
```
✅ Issue #123 обновлён

Заголовок изменён:
- Было: [AUTH] Добавить OAuth авторизацию
- Стало: [AUTH] Добавить OAuth 2.0 авторизацию
```

### Пример 3: Интерактивное редактирование

**Вызов:**
```
/issue-update 123
```

**Вывод:**
```
📋 Issue #123

Заголовок: [AUTH] Добавить OAuth авторизацию
Метки: service:auth, feature

Что обновить?
[1] Заголовок
[2] Добавить метку
[3] Удалить метку
[4] Редактировать тело
[5] Добавить комментарий
[6] Отмена

> 2

Доступные метки:
- in-progress
- blocked
- priority:high
- priority:medium
- priority:low

Введите метку: in-progress

✅ Issue #123 обновлён
Добавлена метка: in-progress
```

### Пример 4: Добавить комментарий

**Вызов:**
```
/issue-update 123 --comment "Начал работу над задачей"
```

**Результат:**
```
✅ Комментарий добавлен к Issue #123
```
