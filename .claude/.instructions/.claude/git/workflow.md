---
type: instruction
status: active
priority: required
description: Git workflow: GitHub Flow, ветки (main + feature/fix), PR
related:
  - git/issues.md
  - git/commits.md
  - git/review.md
  - git/ci.md
---

# Git Workflow

Правила работы с Git: ветвление, pull requests, ревью.

## Оглавление

- [Правила](#правила)
  - [Ветвление](#ветвление)
  - [Pull Requests](#pull-requests)
  - [Ревью](#ревью)
  - [Merge Strategy](#merge-strategy)
- [Примеры](#примеры)
- [Команды gh](#команды-gh)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Ветвление

**Правило:** Используем GitHub Flow — простую модель с main и feature-ветками.

**Основные ветки:**

| Ветка | Назначение |
|-------|------------|
| `main` | Стабильная версия, всегда готова к деплою |
| `feature/*` | Новая функциональность |
| `fix/*` | Исправление багов |
| `docs/*` | Изменения документации |
| `refactor/*` | Рефакторинг без изменения поведения |

**Правило:** Формат названия ветки: `{тип}/{номер-issue}-{краткое-описание}`.

```
feature/123-oauth-auth
fix/456-email-validation
docs/789-update-readme
```

**Правило:** Всегда создавать ветку от актуального `main`.

```bash
git checkout main
git pull origin main
git checkout -b feature/123-oauth-auth
```

**Автоматизация:** Используй скилл [/issue-execute](/.claude/skills/issue-execute/SKILL.md) для автоматического создания ветки от Issue.

### Pull Requests

**Правило:** Каждое изменение — через Pull Request.

**Структура PR:**

```markdown
## Summary
<1-3 буллет-поинта>

## Test plan
- [ ] {Как проверить изменения}
- [ ] {Что должно работать}
```

**Правило:** PR должен быть связан с Issue.

```bash
gh pr create --title "[AUTH] Добавить OAuth" --body "Closes #123"
```

**Правило:** Название PR начинается с префикса сервиса (как в Issues).

```
[AUTH] Добавить OAuth авторизацию
[NOTIFY] Исправить отправку email
[INFRA] Настроить CI pipeline
```

### Ревью

**Правило:** PR требует минимум 1 approve перед мержем.

**Правило:** Автор PR не может approve свой PR.

**Правило:** После ревью исправления — в новых коммитах, не amend.

### Merge Strategy

**Правило:** Используем squash merge для feature/fix веток.

```bash
gh pr merge 123 --squash
```

**Почему squash:**
- Чистая история в main
- Один коммит = один PR = одна фича/фикс
- Легче откатывать изменения

---

## Примеры

### Пример 1: Создание feature-ветки

```bash
# Обновить main
git checkout main
git pull origin main

# Создать ветку
git checkout -b feature/123-oauth-auth

# Работа над фичей
# ...

# Коммиты
git add .
git commit -m "feat(auth): add OAuth configuration"

# Запушить
git push -u origin feature/123-oauth-auth

# Создать PR
gh pr create --title "[AUTH] Добавить OAuth авторизацию" --body "Closes #123"
```

### Пример 2: Fix ветка

```bash
git checkout -b fix/456-email-validation

# Исправление
git add .
git commit -m "fix(notify): validate email format before sending"

git push -u origin fix/456-email-validation
gh pr create --title "[NOTIFY] Исправить валидацию email"
```

### Пример 3: Связать PR с Issue

```bash
# В теле PR
gh pr create --body "$(cat <<'EOF'
## Summary
- Добавлена OAuth авторизация через Google
- Настроены callback URLs
- Добавлены тесты

## Test plan
- [ ] Проверить авторизацию через Google
- [ ] Проверить обработку ошибок

Closes #123
EOF
)"
```

---

## Команды gh

### Работа с ветками

```bash
# Создать ветку от Issue
gh issue develop 123 --checkout

# Создать PR из текущей ветки
gh pr create

# Посмотреть статус PR
gh pr status

# Список открытых PR
gh pr list
```

### Работа с PR

```bash
# Создать PR
gh pr create --title "Название" --body "Описание"

# Посмотреть PR
gh pr view 123

# Одобрить PR
gh pr review 123 --approve

# Запросить изменения
gh pr review 123 --request-changes --body "Нужно исправить..."

# Смержить PR
gh pr merge 123 --squash
```

### Связь Issue и PR

```bash
# В теле PR добавить
Closes #123
Fixes #123
Resolves #123
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Создание Issue с правильным форматом |
| [/issue-update](/.claude/skills/issue-update/SKILL.md) | Обновление Issue (метки, описание) |
| [/issue-execute](/.claude/skills/issue-execute/SKILL.md) | Создание ветки от Issue, выполнение задачи |
| [/issue-review](/.claude/skills/issue-review/SKILL.md) | Ревью решения перед закрытием Issue |
| [/issue-complete](/.claude/skills/issue-complete/SKILL.md) | Закрытие Issue, создание PR |
| [/issue-delete](/.claude/skills/issue-delete/SKILL.md) | Закрытие Issue как неактуального |
| [/issue-reopen](/.claude/skills/issue-reopen/SKILL.md) | Переоткрытие закрытого Issue |

---

## Связанные инструкции

- [git/issues.md](issues.md) — GitHub Issues, префиксы, метки
- [git/commits.md](commits.md) — Conventional commits
- [git/review.md](review.md) — Code review, чек-листы
- [git/ci.md](ci.md) — CI/CD pipeline
