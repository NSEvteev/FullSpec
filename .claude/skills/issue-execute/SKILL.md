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
    en:
      - take issue
      - start issue
      - work on
---

# Взятие Issue в работу

Команда для взятия GitHub Issue в работу: назначение, метка, создание ветки.

**Связанная инструкция:** [/.claude/instructions/git/issues.md](/.claude/instructions/git/issues.md)

**Связанные скиллы:**
- [issue-create](/.claude/skills/issue-create/SKILL.md) — создание Issue
- [issue-update](/.claude/skills/issue-update/SKILL.md) — обновление Issue
- [issue-delete](/.claude/skills/issue-delete/SKILL.md) — закрытие Issue

## Оглавление

- [Формат вызова](#формат-вызова)
- [Что делает](#что-делает)
- [Воркфлоу](#воркфлоу)
- [Формат ветки](#формат-ветки)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/issue-execute <номер> [--no-branch] [--branch-name <имя>]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `номер` | Номер Issue (обязательный) | — |
| `--no-branch` | Не создавать ветку | false |
| `--branch-name` | Кастомное имя ветки | Автогенерация |

**Примеры:**
- `/issue-execute 123`
- `/issue-execute 123 --no-branch`
- `/issue-execute 123 --branch-name feature/oauth-login`

---

## Что делает

| Действие | Описание |
|----------|----------|
| Назначает исполнителя | `gh issue edit --add-assignee @me` |
| Добавляет метку | `gh issue edit --add-label "in-progress"` |
| Создаёт ветку | `git checkout -b feature/{num}-{short-name}` |
| Добавляет комментарий | `gh issue comment --body "Начал работу"` |

---

## Воркфлоу

### Шаг 1: Получить номер Issue

1. Из аргумента: `/issue-execute 123`
2. Проверить существование и статус

### Шаг 2: Показать Issue

```
📋 Issue #123

Заголовок: [AUTH] Добавить OAuth авторизацию
Статус: open
Метки: service:auth, feature
Назначен: —

Взять в работу? [Y/n]
```

### Шаг 3: Назначить исполнителя

```bash
gh issue edit 123 --add-assignee @me
```

### Шаг 4: Добавить метку in-progress

```bash
gh issue edit 123 --add-label "in-progress"
```

### Шаг 5: Создать ветку (если не --no-branch)

**Формат имени:**
```
feature/{номер}-{короткое-имя}
```

Пример: `feature/123-oauth-auth`

```bash
git checkout -b feature/123-oauth-auth
```

### Шаг 6: Добавить комментарий

```bash
gh issue comment 123 --body "🚀 Начал работу над задачей

Ветка: \`feature/123-oauth-auth\`"
```

### Шаг 7: Результат

```
✅ Issue #123 взят в работу

Выполнено:
- Назначен: @username
- Добавлена метка: in-progress
- Создана ветка: feature/123-oauth-auth
- Добавлен комментарий

Текущая ветка: feature/123-oauth-auth

Следующие шаги:
- Реализовать задачу
- Создать PR с привязкой к Issue: "Closes #123"
```

---

## Формат ветки

### Автогенерация

```
{тип}/{номер}-{slug}
```

| Тип Issue | Префикс ветки |
|-----------|---------------|
| feature | `feature/` |
| bug | `fix/` |
| enhancement | `feature/` |

**Slug** — первые 3-4 слова из заголовка в kebab-case:
- `[AUTH] Добавить OAuth авторизацию` → `oauth-auth`
- `[NOTIFY] Email не отправляется` → `email-not-sending`

### Примеры

| Issue | Ветка |
|-------|-------|
| #123 [AUTH] Добавить OAuth | `feature/123-oauth-auth` |
| #124 [NOTIFY] Баг с email | `fix/124-email-bug` |
| #125 [INFRA] CI pipeline | `feature/125-ci-pipeline` |

---

## Чек-лист

- [ ] **Шаг 1:** Получил номер Issue
- [ ] **Шаг 2:** Показал Issue и запросил подтверждение
- [ ] **Шаг 3:** Назначил исполнителя (`@me`)
- [ ] **Шаг 4:** Добавил метку `in-progress`
- [ ] **Шаг 5:** Создал ветку (если не `--no-branch`)
- [ ] **Шаг 6:** Добавил комментарий о начале работы
- [ ] **Шаг 7:** Вывел результат

---

## Примеры

### Пример 1: Стандартное выполнение

**Вызов:**
```
/issue-execute 123
```

**Результат:**
```
✅ Issue #123 взят в работу

- Назначен: @myusername
- Метка: in-progress
- Ветка: feature/123-oauth-auth

Текущая ветка: feature/123-oauth-auth
```

### Пример 2: Без создания ветки

**Вызов:**
```
/issue-execute 123 --no-branch
```

**Результат:**
```
✅ Issue #123 взят в работу

- Назначен: @myusername
- Метка: in-progress
- Ветка: не создана (--no-branch)
```

### Пример 3: Кастомное имя ветки

**Вызов:**
```
/issue-execute 123 --branch-name feature/new-auth-system
```

**Результат:**
```
✅ Issue #123 взят в работу

- Назначен: @myusername
- Метка: in-progress
- Ветка: feature/new-auth-system
```

### Пример 4: Issue уже в работе

**Вызов:**
```
/issue-execute 123
```

**Вывод:**
```
⚠️ Issue #123 уже в работе

Назначен: @otherusername
Метки: service:auth, feature, in-progress

Варианты:
[1] Переназначить на себя
[2] Отменить

> 1

✅ Issue #123 переназначен

- Назначен: @myusername (было: @otherusername)
- Ветка: feature/123-oauth-auth
```

### Пример 5: Issue закрыт

**Вызов:**
```
/issue-execute 123
```

**Вывод:**
```
⚠️ Issue #123 закрыт

Статус: closed
Закрыт: 2024-01-15

Переоткрыть и взять в работу? [y/N]
> y

✅ Issue #123 переоткрыт и взят в работу
```
