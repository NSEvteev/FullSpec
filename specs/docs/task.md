---
description: task — основной сервис управления задачами: CRUD, статусы, история изменений, фильтрация.
standard: specs/.instructions/docs/service/standard-service.md
criticality: critical-high
---

# task

## Назначение

Сервис task — основной владелец доменной сущности «задача». Отвечает за CRUD-операции с задачами, переходы статусов (To Do → In Progress → Done), фиксацию истории изменений в отдельной таблице, фильтрацию и полнотекстовый поиск. Аутентификация делегирована сервису auth через JWT-middleware (task не хранит пользователей), но task хранит ссылку `assigneeId` на пользователя. Основной потребитель — frontend (REST API); внешняя зависимость — auth (JWT-валидация, INT-3).

**Обоснование критичности:** Уровень `critical-high` — task является основным сервисом платформы, реализующим все CRUD-операции с задачами. При недоступности сервиса пользователи полностью теряют возможность создавать, редактировать, просматривать и удалять задачи; канбан-доска перестаёт работать. Обходных путей нет — весь функционал управления задачами сосредоточен в этом сервисе.

## API контракты

Сервис предоставляет 5 REST endpoint-ов для управления задачами: создание, список с фильтрацией, детальный просмотр с историей, обновление и удаление. Все endpoint-ы требуют Bearer JWT и следуют конвенциям из [conventions.md](../.system/conventions.md).

### POST /api/v1/tasks

Создать задачу.

- **Auth:** Bearer JWT (обязателен)
- **Паттерн:** sync | **Протокол:** REST/JSON

**Request:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "priority": "low|medium|high (optional, default medium)",
  "assigneeId": "string (optional)"
}
```

**Response 201:**
```json
{
  "id": "string",
  "title": "string",
  "description": "string|null",
  "priority": "string",
  "status": "todo",
  "assigneeId": "string|null",
  "createdAt": "string",
  "updatedAt": "string"
}
```

**Errors:** 400 (валидация), 401 (нет/невалидный JWT)

---

### GET /api/v1/tasks

Список задач с фильтрацией.

- **Auth:** Bearer JWT (обязателен)
- **Паттерн:** sync | **Протокол:** REST/JSON

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| status | string | нет | Фильтр по статусу |
| priority | string | нет | Фильтр по приоритету |
| assigneeId | string | нет | Фильтр по исполнителю |
| search | string | нет | Полнотекстовый поиск |

**Response 200:**
```json
{
  "items": "Task[]",
  "total": "number"
}
```

**Errors:** 401

---

### GET /api/v1/tasks/:id

Получить задачу по ID.

- **Auth:** Bearer JWT (обязателен)
- **Паттерн:** sync | **Протокол:** REST/JSON

**Response 200:**
```json
{
  "id": "string",
  "title": "string",
  "description": "string|null",
  "priority": "string",
  "status": "string",
  "assigneeId": "string|null",
  "createdAt": "string",
  "updatedAt": "string",
  "history": "HistoryEntry[]"
}
```

**Errors:** 401, 404

---

### PUT /api/v1/tasks/:id

Обновить задачу.

- **Auth:** Bearer JWT (обязателен)
- **Паттерн:** sync | **Протокол:** REST/JSON

**Request:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "priority": "string (optional)",
  "status": "string (optional)",
  "assigneeId": "string|null (optional)"
}
```

**Response 200:**
```json
{
  "id": "string",
  "title": "string",
  "description": "string|null",
  "priority": "string",
  "status": "string",
  "assigneeId": "string|null",
  "createdAt": "string",
  "updatedAt": "string"
}
```

**Errors:** 400, 401, 404

---

### DELETE /api/v1/tasks/:id

Удалить задачу.

- **Auth:** Bearer JWT (обязателен)
- **Паттерн:** sync | **Протокол:** REST/JSON

**Response 204:** No Content

**Errors:** 401, 404

## Data Model

Сервис использует PostgreSQL 16 как основное хранилище. Две таблицы: `tasks` — основная сущность задачи, `task_history` — история изменений полей задачи для детального просмотра (REQ-4).

### tasks (PostgreSQL)

| Колонка | Тип | Constraints | Описание |
|---------|-----|------------|----------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Идентификатор |
| title | VARCHAR(255) | NOT NULL | Заголовок задачи |
| description | TEXT | NULL | Описание задачи |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'todo', CHECK (todo, in_progress, done) | Текущий статус |
| priority | VARCHAR(10) | NOT NULL, DEFAULT 'medium', CHECK (low, medium, high) | Приоритет |
| assigneeId | UUID | NULL | Внешний ID исполнителя (без FK — cross-DB) |
| createdAt | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Дата создания |
| updatedAt | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Дата последнего обновления |

**Индексы:**
- `idx_tasks_status` — по status (фильтрация по статусу)
- `idx_tasks_priority` — по priority (фильтрация по приоритету)
- `idx_tasks_assigneeId` — по assigneeId (фильтрация по исполнителю)
- `idx_tasks_fts` — GIN-индекс по `to_tsvector('russian', title || ' ' || coalesce(description, ''))` (полнотекстовый поиск)

### task_history (PostgreSQL)

| Колонка | Тип | Constraints | Описание |
|---------|-----|------------|----------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Идентификатор |
| taskId | UUID | NOT NULL, FK → tasks.id ON DELETE CASCADE | Задача |
| field | VARCHAR(50) | NOT NULL | Изменённое поле |
| oldValue | TEXT | NULL | Старое значение |
| newValue | TEXT | NULL | Новое значение |
| changedBy | UUID | NOT NULL | ID пользователя (JWT sub) |
| changedAt | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Дата изменения |

**Индексы:**
- `idx_task_history_taskId` — по taskId (выборка истории задачи)

## Потоки

Общий паттерн: HTTP-запрос поступает в `routes/tasks.ts` → `middleware/auth.middleware.ts` валидирует JWT через вызов auth-сервиса (INT-3) → `controllers/tasks.controller.ts` принимает запрос → `services/tasks.service.ts` выполняет бизнес-логику → Prisma работает с PostgreSQL. При PUT — сервис дополнительно пишет в `task_history`. Чтобы добавить новый endpoint — создать маршрут в `routes/tasks.ts`, обработчик в `controllers/tasks.controller.ts`, логику в `services/tasks.service.ts`, Zod-схему в `schemas/task.schema.ts`.

### Создание задачи (REQ-1)

```
1. Frontend → POST /api/v1/tasks (Bearer JWT)
2. middleware/auth.middleware.ts → GET /api/v1/auth/validate (INT-3)
3. auth-сервис → 200 { valid: true, sub, email }
4. schemas/task.schema.ts: Zod валидирует тело (title обязателен — REQ-6)
5. services/tasks.service.ts → Prisma: INSERT в tasks (status = 'todo')
6. → Frontend: 201 с созданной задачей
```

### Смена статуса (REQ-2, US-2)

```
1. Frontend → PUT /api/v1/tasks/:id { status: "in_progress" }
2. middleware/auth.middleware.ts → GET /api/v1/auth/validate (INT-3)
3. auth-сервис → 200 { valid: true, sub }
4. services/tasks.service.ts → Prisma: UPDATE tasks SET status = 'in_progress'
5. services/tasks.service.ts → Prisma: INSERT в task_history (field: "status", oldValue, newValue, changedBy из JWT sub)
6. → Frontend: 200 с обновлённой задачей
```

### Фильтрация (REQ-3)

```
1. Frontend → GET /api/v1/tasks?priority=high&assigneeId=...
2. middleware/auth.middleware.ts → GET /api/v1/auth/validate (INT-3)
3. schemas/task.schema.ts: Zod валидирует query params
4. services/tasks.service.ts → Prisma: SELECT с WHERE-условием по переданным фильтрам
5. При наличии search: полнотекстовый поиск через GIN-индекс
6. → Frontend: 200 { items: [...], total: N }
```

### Детальный просмотр с историей (REQ-4)

```
1. Frontend → GET /api/v1/tasks/:id
2. middleware/auth.middleware.ts → GET /api/v1/auth/validate (INT-3)
3. services/tasks.service.ts → Prisma: SELECT задача + task_history WHERE taskId = :id ORDER BY changedAt DESC
4. → Frontend: 200 { ...Task, history: HistoryEntry[] }
```

## Code Map

### Tech Stack

| Технология | Версия | Назначение | Стандарт |
|-----------|--------|-----------|---------|
| Node.js | 20 | Runtime | — |
| TypeScript | 5 | Типизация | — |
| Express | 4 | HTTP-фреймворк | — |
| Zod | 3 | Runtime-валидация схем | — |
| Prisma | 5 | ORM + миграции | — |
| PostgreSQL | 16 | Основная БД | — |

### Пакеты

Сервис организован по слоям: routes → controllers → services → prisma (ORM). Middleware отвечает за сквозную JWT-валидацию на всех маршрутах. Schemas содержат Zod-определения для request/response.

| Пакет | Назначение | Ключевые модули |
|-------|-----------|----------------|
| `task.routes` | HTTP-маршруты `/api/v1/tasks` | `tasks.ts` |
| `task.controllers` | Обработчики запросов | `tasks.controller.ts` |
| `task.services` | Бизнес-логика CRUD, history | `tasks.service.ts` |
| `task.middleware` | JWT-валидация (вызов auth-сервиса) | `auth.middleware.ts` |
| `task.schemas` | Zod-схемы для request/response | `task.schema.ts` |
| `task.prisma` | Prisma-схема и миграции | `schema.prisma`, `migrations/` |

### Точки входа

- API: `src/task/index.ts`

### Внутренние зависимости

task.routes → task.middleware → task.controllers → task.services → task.prisma

**Как добавить новый функционал:**
- Новый endpoint → создать маршрут в `routes/tasks.ts`, обработчик в `controllers/tasks.controller.ts`, логику в `services/tasks.service.ts`, Zod-схему в `schemas/task.schema.ts`
- Новое поле в задаче → добавить колонку в `prisma/schema.prisma`, создать миграцию в `prisma/migrations/`, обновить Zod-схемы и контракты API

### Makefile таргеты

| Таргет | Команда | Описание |
|--------|---------|----------|
| test | `make test-task` | Unit + integration тесты сервиса |
| lint | `make lint-task` | Линтинг кода сервиса |
| build | `make build-task` | Сборка Docker-образа |

## Зависимости

Сервис task зависит от auth (критическая — без JWT-валидации ни один endpoint не работает). Предоставляет REST API для frontend (INT-1). Прямых зависимостей от shared-пакетов нет.

### auth — JWT-валидация

Task использует auth-сервис для валидации JWT-токенов при каждом входящем HTTP-запросе. Middleware `auth.middleware.ts` делает HTTP-запрос `GET /api/v1/auth/validate` к auth-сервису и прокидывает результат (sub, email) в `req.user` для использования в контроллерах (например, `changedBy` при записи в `task_history`). Если auth недоступен — все запросы к task возвращают 401.
Паттерн: **Conformist** (task конформен к API auth).
См. [GET /api/v1/auth/validate](auth.md#get-apiv1authvalidate).

## Доменная модель

Сервис task реализует домен задач. Основная сущность — Task — проходит жизненный цикл: создание (todo) → выполнение (in_progress) → завершение (done). TaskHistory фиксирует каждое изменение полей задачи.

### Агрегаты

| Агрегат | Описание |
|---------|----------|
| Task | Корень агрегата. Поля: id, title, description, status, priority, assigneeId, createdAt, updatedAt. Жизненный цикл: todo → in_progress → done (и обратно — без ограничений в v0.1.0) |

### Value Objects

Value Object `TaskHistory` — запись об изменении. Поля: id, taskId, field, oldValue, newValue, changedBy, changedAt. Создаётся автоматически при каждом PUT-запросе.

### Инварианты

- title задачи не может быть пустым
- status ∈ {todo, in_progress, done}
- priority ∈ {low, medium, high}
- TaskHistory создаётся при каждом PUT, фиксирует какие поля изменились (diff)
- assigneeId хранится как внешний UUID без FK (cross-DB микросервисная архитектура)

### Доменные события

| Событие | Описание |
|---------|----------|
| TaskStatusChanged | Триггер записи в task_history при смене статуса (REQ-2) → порождает запись TaskHistory |

## Границы автономии LLM

- **Свободно:** реализация CRUD-эндпоинтов (Express routes, controllers); Zod-схемы валидации (соответствуют § 2 API контракты); Prisma-схема и миграции (соответствуют § 3 Data Model); логика записи в task_history (фиксировать все изменённые поля через diff)
- **Флаг:** JWT-middleware (вызов auth-сервиса) — протокол вызова строго по INT-3; полнотекстовый поиск (GIN-индекс) — проверить locale (russian/simple)
- **CONFLICT:** переходы статусов (ограничения FSM) — в v0.1.0 без ограничений; в v0.2+ возможна FSM — требует Discussion; удаление задачи (soft vs hard delete) — в v0.1.0 hard delete; soft delete — отдельный Discussion

## Planned Changes

<!-- chain: 0001-task-dashboard -->
Из Design 0001: ADDED таблица tasks (id, title, description, status, priority, assigneeId, createdAt, updatedAt); ADDED таблица task_history (id, taskId, field, oldValue, newValue, changedBy, changedAt); ADDED 5 REST endpoint-ов (POST/GET/GET:id/PUT/DELETE /api/v1/tasks); ADDED потоки создания, смены статуса, фильтрации, детального просмотра; ADDED Code Map (Node.js, TypeScript, Express, Zod, Prisma, PostgreSQL 16); ADDED зависимость INT-3 (task → auth JWT-валидация); ADDED зависимость INT-1 (frontend → task CRUD API); ADDED доменная модель (Task, TaskHistory, TaskStatusChanged).
<!-- /chain: 0001-task-dashboard -->

## Changelog

- **Создание сервиса** | DONE 2026-03-01 — первоначальная документация.
