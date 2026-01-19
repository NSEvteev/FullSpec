---
type: standard
description: GitHub Issues: префиксы, метки, команды gh
related:
  - git/workflow.md
  - git/commits.md
---

# GitHub Issues

Правила работы с задачами через GitHub Issues. Локальные задачи не используем.

## Оглавление

- [Формат задачи](#формат-задачи)
- [Префиксы сервисов](#префиксы-сервисов)
- [Метки (Labels)](#метки-labels)
- [Workflow](#workflow)
- [Скиллы](#скиллы)
- [Команды gh](#команды-gh)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Формат задачи

**Заголовок:** `[PREFIX] Краткое описание`

```
[AUTH] Добавить OAuth авторизацию
[NOTIFY] Исправить отправку email
[INFRA] Настроить CI pipeline
```

**Тело задачи:**
```markdown
## Описание

{Что нужно сделать}

## Критерии готовности

- [ ] {Чек-лист выполнения}

## Связанные файлы

- {Ссылки на код/документацию}
```

---

## Префиксы сервисов

| Сервис | Префикс | Label | Пример |
|--------|---------|-------|--------|
| auth | AUTH | service:auth | [AUTH] Добавить OAuth |
| notification | NOTIFY | service:notify | [NOTIFY] Email templates |
| payment | PAY | service:payment | [PAY] Stripe интеграция |
| users | USERS | service:users | [USERS] Профили |
| gateway | GW | service:gateway | [GW] Rate limiting |
| общие/инфра | INFRA | infra | [INFRA] CI pipeline |
| документация | DOCS | docs | [DOCS] Обновить README |

**Правило:** При создании нового сервиса — добавить префикс в эту таблицу.

---

## Метки (Labels)

### По сервису

- `service:auth` — сервис аутентификации
- `service:notify` — сервис уведомлений
- `service:payment` — сервис платежей
- `service:users` — сервис пользователей
- `service:gateway` — API gateway

### По типу

- `bug` — ошибка
- `feature` — новая функциональность
- `enhancement` — улучшение
- `docs` — документация
- `infra` — инфраструктура

### По приоритету

- `priority:high` — высокий приоритет
- `priority:medium` — средний приоритет
- `priority:low` — низкий приоритет

---

## Workflow

| Событие | Действие | Скилл |
|---------|----------|-------|
| Новая задача | Создать Issue с префиксом и меткой | `/issue-create` |
| Изменение требований | Обновить описание Issue | `/issue-update` |
| Задача неактуальна | Закрыть Issue с комментарием | `/issue-delete` |
| Начало работы | Назначить себя, добавить метку `in-progress` | `/issue-execute` |

---

## Скиллы

Скиллы для автоматизации работы с Issues:

| Скилл | Назначение |
|-------|------------|
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Создание Issue с правильным форматом |
| [/issue-update](/.claude/skills/issue-update/SKILL.md) | Обновление описания Issue |
| [/issue-delete](/.claude/skills/issue-delete/SKILL.md) | Закрытие Issue с комментарием |
| [/issue-execute](/.claude/skills/issue-execute/SKILL.md) | Взятие Issue в работу |

### /issue-create

Создаёт Issue с:
1. Правильным префиксом `[PREFIX]`
2. Соответствующей меткой `service:*`
3. Шаблоном описания

### /issue-update

Обновляет Issue:
- Изменение описания
- Добавление/удаление меток
- Обновление чек-листа

### /issue-delete

Закрывает Issue:
1. Добавляет комментарий с причиной
2. Закрывает как `not planned` или `completed`

### /issue-execute

Берёт Issue в работу:
1. Назначает исполнителя
2. Добавляет метку `in-progress`
3. Создаёт ветку `feature/{issue-number}-{short-name}`

---

## Команды gh

### Создание

```bash
gh issue create \
  --label "service:auth" \
  --title "[AUTH] Добавить OAuth авторизацию"
```

### Просмотр

```bash
# Все открытые
gh issue list --state open

# По сервису
gh issue list --label "service:auth"

# По приоритету
gh issue list --label "priority:high"

# Детали задачи
gh issue view 123
```

### Управление

```bash
# Назначить себя
gh issue edit 123 --add-assignee @me

# Добавить метку
gh issue edit 123 --add-label "in-progress"

# Закрыть
gh issue close 123 --comment "Выполнено в PR #456"

# Закрыть как неактуальное
gh issue close 123 --reason "not planned" --comment "Неактуально"
```

---

## Примеры

### Пример 1: Создание задачи на фичу

```bash
gh issue create \
  --label "service:auth,feature" \
  --title "[AUTH] Добавить двухфакторную аутентификацию" \
  --body "## Описание

Реализовать 2FA через TOTP.

## Критерии готовности

- [ ] Генерация QR-кода
- [ ] Валидация TOTP
- [ ] Backup codes
- [ ] Тесты

## Связанные файлы

- /src/auth/backend/2fa/"
```

### Пример 2: Создание задачи на баг

```bash
gh issue create \
  --label "service:notify,bug,priority:high" \
  --title "[NOTIFY] Email не отправляется при регистрации"
```

### Пример 3: Задача на документацию (из doc-delete)

```bash
gh issue create \
  --label "docs" \
  --title "[DOCS] Обновить документацию после удаления handlers.ts" \
  --body "## Описание

Файл /src/auth/backend/handlers.ts был удалён.
Документация /doc/src/auth/backend/handlers.md требует ревью.

## Действия

- [ ] Удалить или обновить документацию
- [ ] Обновить ссылки в связанных документах"
```

---

## Связанные инструкции

- [git/workflow.md](workflow.md) — Git workflow, ветки, PR
- [git/commits.md](commits.md) — Conventional commits
