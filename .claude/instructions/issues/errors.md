---
type: instruction
status: active
priority: required
description: Обработка ошибок при работе с GitHub Issues
related:
  - issues/commands.md
  - skills/errors.md
---

# Обработка ошибок

Типичные ошибки при работе с GitHub Issues и способы их решения.

## Оглавление

- [Ошибки окружения](#ошибки-окружения)
- [Ошибки доступа](#ошибки-доступа)
- [Ошибки валидации](#ошибки-валидации)
- [Ошибки состояния](#ошибки-состояния)
- [Сетевые ошибки](#сетевые-ошибки)
- [Решения](#решения)
- [Связанные инструкции](#связанные-инструкции)

---

## Ошибки окружения

### gh не установлен

**Симптом:**
```
command not found: gh
```

**Решение:**
```bash
# macOS
brew install gh

# Windows
winget install GitHub.cli

# Linux
sudo apt install gh
```

**Документация:** https://cli.github.com/manual/installation

---

### gh не авторизован

**Симптом:**
```
gh: not logged in
```

**Решение:**
```bash
gh auth login
```

Выбрать:
1. GitHub.com
2. HTTPS
3. Authenticate with browser

**Проверка:**
```bash
gh auth status
```

---

### Неправильный репозиторий

**Симптом:**
```
no git remotes found
```

**Решение:**
```bash
# Проверить remotes
git remote -v

# Добавить origin
git remote add origin https://github.com/user/repo.git
```

---

## Ошибки доступа

### Нет прав на репозиторий

**Симптом:**
```
Resource not accessible by integration (FORBIDDEN)
```

**Причины:**
1. Нет доступа к приватному репозиторию
2. Токен не имеет нужных scope
3. Репозиторий архивирован

**Решение:**
```bash
# Проверить доступ
gh repo view

# Переавторизоваться с нужными scope
gh auth login --scopes "repo,read:org"
```

---

### Issue не найден

**Симптом:**
```
Could not resolve to an Issue with the number of 999
```

**Причины:**
1. Issue не существует
2. Неправильный репозиторий
3. Issue в другом репозитории

**Решение:**
```bash
# Проверить существующие Issue
gh issue list --state all

# Проверить текущий репозиторий
gh repo view --json nameWithOwner -q '.nameWithOwner'
```

---

### Метка не существует

**Симптом:**
```
label 'xxx' not found
```

**Решение:**
```bash
# Посмотреть существующие метки
gh label list

# Создать метку
gh label create "xxx" --color "0E8A16" --description "Описание"
```

---

## Ошибки валидации

### Заголовок без префикса

**Симптом (в скилле):**
```
❌ Заголовок должен начинаться с [PREFIX]
```

**Решение:**
```
# Неправильно
/issue-create "Добавить OAuth"

# Правильно
/issue-create --service auth "Добавить OAuth"
# или
/issue-create "[AUTH] Добавить OAuth"
```

---

### Неизвестный сервис

**Симптом:**
```
❌ Неизвестный сервис: ABC
```

**Решение:**
1. Использовать существующий сервис из списка
2. Или добавить новый сервис в [format.md](./format.md)

**Доступные сервисы:**
- auth, notify, payment, users, gateway
- infra, docs

---

### Пустое тело Issue

**Симптом:**
```
⚠️ Тело Issue не заполнено
```

**Решение:**
```bash
gh issue edit 123 --body "## Описание
...

## Критерии готовности
- [ ] ..."
```

---

## Ошибки состояния

### Issue уже закрыт

**Симптом:**
```
ℹ️ Issue #123 уже закрыт
```

**Решение (если нужно переоткрыть):**
```
/issue-reopen #123
```

---

### Issue уже открыт

**Симптом:**
```
ℹ️ Issue #123 уже открыт
```

**Решение:**
```
# Взять в работу
/issue-execute #123

# Или обновить
/issue-update #123
```

---

### Issue в работе — нельзя удалить

**Симптом:**
```
⚠️ Issue #123 в работе (in-progress)
```

**Решение:**
1. Снять метку `in-progress`
2. Затем закрыть

```
/issue-update #123 --remove-label "in-progress"
/issue-delete #123
```

---

### Не все критерии выполнены

**Симптом:**
```
⚠️ Не все критерии готовности выполнены
```

**Варианты:**
1. Выполнить недостающие критерии
2. Закрыть всё равно (если критерий неактуален)
3. Создать отдельный Issue для невыполненного

---

## Сетевые ошибки

### Timeout

**Симптом:**
```
context deadline exceeded
```

**Решение:**
```bash
# Повторить команду
gh issue view 123

# Или увеличить timeout
GH_HTTP_TIMEOUT=60 gh issue view 123
```

---

### Rate limit

**Симптом:**
```
API rate limit exceeded
```

**Решение:**
1. Подождать (обычно 1 час)
2. Или использовать Personal Access Token с большим лимитом

```bash
gh auth status  # Покажет оставшийся лимит
```

---

## Решения

### Универсальные шаги диагностики

```bash
# 1. Проверить авторизацию
gh auth status

# 2. Проверить репозиторий
gh repo view

# 3. Проверить Issue
gh issue view 123

# 4. Проверить права
gh api repos/{owner}/{repo}/collaborators/{username}/permission
```

### Сброс авторизации

```bash
gh auth logout
gh auth login
```

### Подробный вывод ошибок

```bash
GH_DEBUG=1 gh issue create --title "Test"
```

---

## Формат сообщений об ошибках

### В скиллах

```
❌ Ошибка: {краткое описание}

Причина: {детали}

Решение:
{конкретные шаги}

Документация: {ссылка}
```

### Пример

```
❌ Ошибка: Issue #123 не найден

Причина: Issue с таким номером не существует в репозитории user/repo

Решение:
1. Проверьте номер Issue: gh issue list
2. Убедитесь, что вы в правильном репозитории: gh repo view
3. Issue может быть в другом репозитории

Документация: https://cli.github.com/manual/gh_issue_view
```

---

## Связанные инструкции

- [commands.md](./commands.md) — команды gh CLI
- [workflow.md](./workflow.md) — жизненный цикл Issue
- [../skills/errors.md](../skills/errors.md) — общая обработка ошибок

---

> **Путь:** `/.claude/instructions/issues/errors.md`
