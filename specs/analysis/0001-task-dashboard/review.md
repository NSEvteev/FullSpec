---
description: Ревью кода для 0001-task-dashboard.
standard: specs/.instructions/analysis/review/standard-review.md
standard-version: v1.2
parent: specs/analysis/0001-task-dashboard/plan-dev.md
index: specs/analysis/README.md
milestone: v0.1.0
status: OPEN
---

# review: 0001 Task dashboard

**Ветка:** 0001-task-dashboard
**Base:** main

## Контекст ревью

> Секция заполняется при /review-create (до начала разработки).
> Содержит все ссылки, необходимые code-reviewer при запуске /review.

### Постановка

| Документ | Путь |
|----------|------|
| Discussion | `specs/analysis/0001-task-dashboard/discussion.md` |
| Design | `specs/analysis/0001-task-dashboard/design.md` |
| Plan Tests | `specs/analysis/0001-task-dashboard/plan-test.md` |
| Plan Dev | `specs/analysis/0001-task-dashboard/plan-dev.md` |

### task (critical-high)

| Секция | Путь | Что проверяем |
|--------|------|----------------|
| § 1 Назначение | `specs/docs/task.md#назначение` | ADDED: CRUD задач, история, фильтрация |
| § 2 API контракты | `specs/docs/task.md#api-контракты` | ADDED: 5 endpoints (POST/GET/GET/:id/PUT/DELETE /api/v1/tasks) |
| § 3 Data Model | `specs/docs/task.md#data-model` | ADDED: таблицы tasks, task_history; GIN-индекс |
| § 4 Потоки | `specs/docs/task.md#потоки` | ADDED: создание, смена статуса, фильтрация, детальный просмотр |
| § 5 Code Map | `specs/docs/task.md#code-map` | ADDED: структура src/task/ |
| § 6 Зависимости | `specs/docs/task.md#зависимости` | ADDED: потребляет INT-3, предоставляет INT-1 |
| § 7 Доменная модель | `specs/docs/task.md#доменная-модель` | ADDED: Task агрегат, TaskHistory VO, TaskStatusChanged событие |
| § 8 Автономия | `specs/docs/task.md#границы-автономии-llm` | Что можно без флага, что требует CONFLICT |
| § 9 Planned Changes | `specs/docs/task.md#planned-changes` | **Эталон для P1-сверки** |

### auth (critical-high)

| Секция | Путь | Что проверяем |
|--------|------|----------------|
| § 1 Назначение | `specs/docs/auth.md#назначение` | ADDED: аутентификация, JWT, список пользователей |
| § 2 API контракты | `specs/docs/auth.md#api-контракты` | ADDED: 3 endpoints (login, validate, users) |
| § 3 Data Model | `specs/docs/auth.md#data-model` | ADDED: таблица users |
| § 4 Потоки | `specs/docs/auth.md#потоки` | ADDED: логин, валидация JWT, список пользователей |
| § 5 Code Map | `specs/docs/auth.md#code-map` | ADDED: структура src/auth/ |
| § 6 Зависимости | `specs/docs/auth.md#зависимости` | ADDED: предоставляет INT-2, INT-3 |
| § 7 Доменная модель | `specs/docs/auth.md#доменная-модель` | ADDED: User агрегат, JwtToken VO |
| § 8 Автономия | `specs/docs/auth.md#границы-автономии-llm` | Что можно без флага, что требует CONFLICT |
| § 9 Planned Changes | `specs/docs/auth.md#planned-changes` | **Эталон для P1-сверки** |

### frontend (critical-high)

| Секция | Путь | Что проверяем |
|--------|------|----------------|
| § 1 Назначение | `specs/docs/frontend.md#назначение` | ADDED: канбан-доска, drag-and-drop, формы |
| § 4 Потоки | `specs/docs/frontend.md#потоки` | ADDED: инициализация, логин, создание, d&d, просмотр, удаление, фильтрация |
| § 5 Code Map | `specs/docs/frontend.md#code-map` | ADDED: структура src/frontend/ |
| § 6 Зависимости | `specs/docs/frontend.md#зависимости` | ADDED: потребляет INT-1, INT-2 |
| § 7 Доменная модель | `specs/docs/frontend.md#доменная-модель` | ADDED: Task/User DTO, FilterState, AuthState |
| § 8 Автономия | `specs/docs/frontend.md#границы-автономии-llm` | Что можно без флага, что требует CONFLICT |
| § 9 Planned Changes | `specs/docs/frontend.md#planned-changes` | **Эталон для P1-сверки** |

### Системная документация

- `specs/docs/.system/overview.md`
- `specs/docs/.system/conventions.md`
- `specs/docs/.system/testing.md`
- `specs/docs/.system/infrastructure.md`

### Tech-стандарты

| Технология | Стандарт |
|------------|----------|
| TypeScript | `specs/docs/.technologies/standard-typescript.md` |
| React | `specs/docs/.technologies/standard-react.md` |
| Express | `specs/docs/.technologies/standard-express.md` |
| PostgreSQL | `specs/docs/.technologies/standard-postgresql.md` |
| Prisma | `specs/docs/.technologies/standard-prisma.md` |
| jose | `specs/docs/.technologies/standard-jose.md` |

### Процесс разработки

- [validation-development.md](/.github/.instructions/development/validation-development.md)
