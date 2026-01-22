# Commit Message Template

> **Источник:** [/.claude/instructions/git/commits.md](/.claude/instructions/git/commits.md)

## Шаблон

```
<type>(<scope>): <description>

[body]

[footer]
```

### Типы изменений

| Тип | Описание | Влияние на версию |
|-----|----------|-------------------|
| `feat` | Новая функциональность | MINOR (1.X.0) |
| `fix` | Исправление бага | PATCH (1.0.X) |
| `docs` | Документация | - |
| `style` | Форматирование (без изменения логики) | - |
| `refactor` | Рефакторинг (без изменения поведения) | - |
| `perf` | Улучшение производительности | PATCH |
| `test` | Добавление/изменение тестов | - |
| `build` | Изменения в системе сборки | - |
| `ci` | CI/CD изменения | - |
| `chore` | Прочие изменения | - |

### Scopes (области)

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

### Breaking Changes

Помечаются `!` после scope или в footer:

```
feat(auth)!: change token format from JWT to opaque
```

или

```
feat(auth): change authentication method

BREAKING CHANGE: Token format changed from JWT to opaque.
Migration: regenerate all active tokens.
```

### Co-Authored-By

Коммиты с помощью Claude должны содержать:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Правила

- Первая строка не длиннее 72 символов
- Description пишется на английском языке (императив, с маленькой буквы)
- `feat` и `fix` - основные типы, влияющие на версионирование
- Breaking changes увеличивают MAJOR версию (X.0.0)

<!-- Пример заполнения

feat(auth): add two-factor authentication

- Add TOTP generation
- Add QR code for authenticator apps
- Add backup codes

Closes #123

Co-Authored-By: Claude <noreply@anthropic.com>

---

fix(notify): handle empty email gracefully

Previously, empty email caused 500 error.
Now returns 400 with validation message.

Fixes #456

---

refactor(shared): extract validation utils

Move email and phone validation to shared/validation.ts
No behavior changes.

---

feat(auth)!: require email verification

BREAKING CHANGE: New users must verify email before login.
Migration: run scripts/migrate-unverified-users.ts

Closes #789

---

docs: update API authentication guide

- Add OAuth2 examples
- Update token refresh flow
- Add troubleshooting section

---

ci: add automated security scanning

- Add Snyk dependency check
- Add SAST with CodeQL
- Run on all PRs to main
-->
