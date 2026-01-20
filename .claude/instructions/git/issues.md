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

- [Правила](#правила)
  - [Формат задачи](#формат-задачи)
  - [Префиксы сервисов](#префиксы-сервисов)
  - [Метки (Labels)](#метки-labels)
  - [Workflow](#workflow)
- [Скиллы](#скиллы)
- [Команды gh](#команды-gh)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Формат задачи

**Правило:** Заголовок Issue имеет формат `[PREFIX] Краткое описание`.

```
[AUTH] Добавить OAuth авторизацию
[NOTIFY] Исправить отправку email
[INFRA] Настроить CI pipeline
```

**Правило:** Тело задачи содержит три обязательных раздела.

```markdown
## Описание

{Что нужно сделать}

## Критерии готовности

- [ ] {Чек-лист выполнения}

## Связанные файлы

- {Ссылки на код/документацию}
```

### Префиксы сервисов

**Правило:** Каждый сервис имеет уникальный префикс и метку.

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

### Метки (Labels)

**Правило:** Каждый Issue должен иметь метки по категориям.

**По сервису:**
- `service:auth` — сервис аутентификации
- `service:notify` — сервис уведомлений
- `service:payment` — сервис платежей
- `service:users` — сервис пользователей
- `service:gateway` — API gateway

**По типу:**
- `bug` — ошибка
- `feature` — новая функциональность
- `enhancement` — улучшение
- `docs` — документация
- `infra` — инфраструктура

**По приоритету:**
- `priority:high` — высокий приоритет
- `priority:medium` — средний приоритет
- `priority:low` — низкий приоритет

**По статусу:**
- `in-progress` — в работе
- `blocked` — заблокировано
- `needs-review` — требует ревью

### Workflow

**Правило:** Жизненный цикл Issue управляется через скиллы.

| Событие | Действие | Скилл |
|---------|----------|-------|
| Новая задача | Создать Issue с префиксом и меткой | [/issue-create](/.claude/skills/issue-create/SKILL.md) |
| Изменение требований | Обновить описание Issue | [/issue-update](/.claude/skills/issue-update/SKILL.md) |
| Начало работы | Взять в работу и выполнить задачу | [/issue-execute](/.claude/skills/issue-execute/SKILL.md) |
| После выполнения | Проверить качество решения | [/issue-review](/.claude/skills/issue-review/SKILL.md) |
| Ревью пройдено | Закрыть Issue как выполненный | [/issue-complete](/.claude/skills/issue-complete/SKILL.md) |
| Задача неактуальна | Закрыть Issue как not planned | [/issue-delete](/.claude/skills/issue-delete/SKILL.md) |
| Преждевременное закрытие | Переоткрыть закрытый Issue | [/issue-reopen](/.claude/skills/issue-reopen/SKILL.md) |

---

## Автоматизация

Скиллы для работы с этой инструкцией:

| Скилл | Назначение |
|-------|------------|
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Создание Issue с правильным форматом |
| [/issue-update](/.claude/skills/issue-update/SKILL.md) | Обновление описания Issue |
| [/issue-execute](/.claude/skills/issue-execute/SKILL.md) | Взятие Issue в работу и выполнение |
| [/issue-review](/.claude/skills/issue-review/SKILL.md) | Ревью решения перед закрытием |
| [/issue-complete](/.claude/skills/issue-complete/SKILL.md) | Закрытие Issue как выполненного |
| [/issue-delete](/.claude/skills/issue-delete/SKILL.md) | Закрытие Issue как неактуального |
| [/issue-reopen](/.claude/skills/issue-reopen/SKILL.md) | Переоткрытие закрытого Issue |

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

### /issue-execute

Берёт Issue в работу и выполняет:
1. Назначает исполнителя
2. Добавляет метку `in-progress`
3. Создаёт ветку `feature/{issue-number}-{short-name}`
4. Выполняет задачу (код, тесты, документация)
5. Вызывает `/issue-review` для проверки

### /issue-review

Проверяет качество решения перед закрытием:
1. Проверяет качество кода (линтинг, типы)
2. Оценивает реализацию (можно ли улучшить)
3. Проверяет тесты
4. Проверяет критерии готовности из Issue
5. При успехе — вызывает `/issue-complete`

### /issue-complete

Закрывает Issue как выполненный:
1. Проверяет критерии готовности
2. Находит связанный PR
3. Добавляет комментарий о выполнении
4. Закрывает как `completed`

### /issue-delete

Закрывает Issue как неактуальный:
1. Добавляет комментарий с причиной
2. Закрывает как `not planned`

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

### Пример 3: Задача на документацию

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

### Пример 4: Взятие задачи в работу

```bash
# Назначить себя
gh issue edit 123 --add-assignee @me

# Добавить метку in-progress
gh issue edit 123 --add-label "in-progress"

# Создать ветку
git checkout -b feature/123-oauth-auth

# Добавить комментарий
gh issue comment 123 --body "Начал работу над задачей. Ветка: feature/123-oauth-auth"
```

### Пример 5: Закрытие выполненной задачи

```bash
gh issue close 123 --comment "Выполнено в PR #456"
```

### Пример 6: Закрытие неактуальной задачи

```bash
gh issue close 123 --reason "not planned" --comment "Требования изменились, задача неактуальна"
```

---

## Связанные инструкции

- [git/workflow.md](workflow.md) — Git workflow, ветки, PR
- [git/commits.md](commits.md) — Conventional commits
