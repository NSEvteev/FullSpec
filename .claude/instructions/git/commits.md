---
type: standard
description: Conventional commits: feat/fix/breaking, автогенерация CHANGELOG
related:
  - git/workflow.md
  - git/issues.md
---

# Conventional Commits

Правила оформления коммитов для автогенерации CHANGELOG и семантического версионирования.

## Оглавление

- [Правила](#правила)
  - [Формат сообщения](#формат-сообщения)
  - [Типы изменений](#типы-изменений)
  - [Scope (область)](#scope-область)
  - [Breaking changes](#breaking-changes)
  - [Co-Authored-By](#co-authored-by)
- [Примеры](#примеры)
- [Автогенерация CHANGELOG](#автогенерация-changelog)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Формат сообщения

**Правило:** Коммит имеет структуру:

```
<type>(<scope>): <description>

[body]

[footer]
```

**Обязательные части:**
- `type` — тип изменения
- `description` — краткое описание (императив, с маленькой буквы, на английском)

**Опциональные части:**
- `scope` — область изменения (сервис, модуль)
- `body` — развёрнутое описание
- `footer` — ссылки на issues, breaking changes

**Правило:** Первая строка не длиннее 72 символов.

**Правило:** Description пишется на английском языке (стандарт conventional commits).

### Типы изменений

| Тип | Описание | Влияние на версию |
|-----|----------|-------------------|
| `feat` | Новая функциональность | MINOR (1.X.0) |
| `fix` | Исправление бага | PATCH (1.0.X) |
| `docs` | Документация | — |
| `style` | Форматирование (без изменения логики) | — |
| `refactor` | Рефакторинг (без изменения поведения) | — |
| `perf` | Улучшение производительности | PATCH |
| `test` | Добавление/изменение тестов | — |
| `build` | Изменения в системе сборки | — |
| `ci` | CI/CD изменения | — |
| `chore` | Прочие изменения | — |

**Правило:** `feat` и `fix` — основные типы, влияющие на версионирование.

### Scope (область)

**Правило:** Scope соответствует сервису или модулю.

| Scope | Описание |
|-------|----------|
| `auth` | Сервис аутентификации |
| `notify` | Сервис уведомлений |
| `payment` | Сервис платежей |
| `users` | Сервис пользователей |
| `gateway` | API gateway |
| `shared` | Общий код |
| `infra` | Инфраструктура |
| `docs` | Документация |

**Примеры:**
```
feat(auth): add OAuth configuration
fix(notify): validate email format
refactor(shared): extract common utils
```

### Breaking changes

**Правило:** Breaking changes помечаются `!` после scope или в footer.

**Вариант 1: В заголовке**
```
feat(auth)!: change token format from JWT to opaque
```

**Вариант 2: В footer**
```
feat(auth): change authentication method

BREAKING CHANGE: Token format changed from JWT to opaque.
Migration: regenerate all active tokens.
```

**Правило:** Breaking changes увеличивают MAJOR версию (X.0.0).

### Co-Authored-By

**Правило:** Коммиты, созданные с помощью Claude, должны содержать Co-Authored-By в footer.

```
feat(auth): add OAuth configuration

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Примеры

### Пример 1: Новая функциональность

```
feat(auth): add two-factor authentication

- Add TOTP generation
- Add QR code for authenticator apps
- Add backup codes

Closes #123
```

### Пример 2: Исправление бага

```
fix(notify): handle empty email gracefully

Previously, empty email caused 500 error.
Now returns 400 with validation message.

Fixes #456
```

### Пример 3: Рефакторинг

```
refactor(shared): extract validation utils

Move email and phone validation to shared/validation.ts
No behavior changes.
```

### Пример 4: Breaking change

```
feat(auth)!: require email verification

BREAKING CHANGE: New users must verify email before login.
Migration: run scripts/migrate-unverified-users.ts

Closes #789
```

### Пример 5: Документация

```
docs: update API authentication guide

- Add OAuth2 examples
- Update token refresh flow
- Add troubleshooting section
```

### Пример 6: CI/CD

```
ci: add automated security scanning

- Add Snyk dependency check
- Add SAST with CodeQL
- Run on all PRs to main
```

---

## Автогенерация CHANGELOG

**Правило:** CHANGELOG генерируется автоматически из commit history.

**Что попадает в CHANGELOG:**
- `feat` → Features
- `fix` → Bug Fixes
- Breaking changes → Breaking Changes

**Пример сгенерированного CHANGELOG:**

```markdown
## [1.2.0] - 2024-01-15

### Features
- **auth:** add two-factor authentication (#123)
- **notify:** add SMS notifications (#124)

### Bug Fixes
- **auth:** fix token refresh race condition (#125)
- **gateway:** handle timeout errors (#126)

### Breaking Changes
- **auth:** require email verification (#127)
```

**Инструменты:**
- `standard-version` — Node.js
- `conventional-changelog` — генератор
- `semantic-release` — полная автоматизация

---

## Связанные инструкции

- [git/workflow.md](workflow.md) — Git workflow, ветки, PR
- [git/issues.md](issues.md) — GitHub Issues, префиксы, метки
