# Инструкции /git/

Индекс инструкций для работы с Git и GitHub.

**Содержание:** Git workflow, conventional commits, GitHub Issues, code review, CI/CD pipeline.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Commits](#1-commits) | [commits.md](./commits.md) | Conventional commits, автогенерация CHANGELOG |
| [2. Issues](#2-issues) | [issues.md](./issues.md) | GitHub Issues: префиксы, метки, команды gh |
| [3. Workflow](#3-workflow) | [workflow.md](./workflow.md) | GitHub Flow: ветки, PR, merge strategy |
| [4. Review](#4-review) | [review.md](./review.md) | Code review: чек-листы, CODEOWNERS |
| [5. CI](#5-ci) | [ci.md](./ci.md) | CI/CD pipeline, GitHub Actions, quality gates |

---

# 1. Commits

Правила оформления коммитов для автогенерации CHANGELOG и семантического версионирования.

**Содержание:** формат сообщения (`<type>(<scope>): <description>`), типы изменений (feat/fix/docs/refactor), scopes по сервисам, breaking changes, Co-Authored-By.

| Тип | Влияние на версию |
|-----|-------------------|
| `feat` | MINOR (1.X.0) |
| `fix` | PATCH (1.0.X) |
| Breaking changes | MAJOR (X.0.0) |

**Инструкция:** [commits.md](./commits.md)

---

# 2. Issues

Правила работы с задачами через GitHub Issues. Локальные задачи не используем.

**Содержание:** формат заголовка (`[PREFIX] Описание`), префиксы сервисов (AUTH, NOTIFY, PAY), метки (service:*, priority:*, type:*), workflow задач, скиллы /issue-*.

| Префикс | Сервис |
|---------|--------|
| `AUTH` | auth |
| `NOTIFY` | notification |
| `PAY` | payment |
| `INFRA` | инфраструктура |
| `DOCS` | документация |

**Инструкция:** [issues.md](./issues.md)

---

# 3. Workflow

Правила работы с Git: ветвление, pull requests, ревью.

**Содержание:** GitHub Flow (main + feature-ветки), формат названия веток (`{тип}/{номер-issue}-{описание}`), структура PR, squash merge strategy.

| Ветка | Назначение |
|-------|------------|
| `main` | Стабильная версия |
| `feature/*` | Новая функциональность |
| `fix/*` | Исправление багов |
| `docs/*` | Документация |

**Инструкция:** [workflow.md](./workflow.md)

---

# 4. Review

Правила проведения code review: чек-лист проверки, CODEOWNERS, процесс approve.

**Содержание:** процесс review (7 этапов), CODEOWNERS по сервисам, чек-листы reviewer и self-review, правила approve, формат комментариев (nit/suggestion/question/blocker).

| Тип изменений | Требуется approve |
|---------------|-------------------|
| Обычные | 1 |
| shared/ | 2 (CODEOWNERS) |
| Breaking changes | 2 (Tech lead + CODEOWNERS) |

**Инструкция:** [review.md](./review.md)

---

# 5. CI

Правила организации CI/CD: структура pipeline, GitHub Actions, quality gates.

**Содержание:** стадии pipeline (lint → test → build → security → deploy), quality gates (покрытие >= 80%, 0 critical уязвимостей), GitHub Actions workflows, секреты и переменные, rollback, alerting при failure.

| Стадия | Блокирует merge |
|--------|-----------------|
| `lint` | Да |
| `test` | Да |
| `build` | Да |
| `security` | Да (для main) |

**Инструкция:** [ci.md](./ci.md)

