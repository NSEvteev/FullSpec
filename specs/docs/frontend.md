---
description: frontend — React-приложение, канбан-доска задач с drag-and-drop, формы, фильтрация, аутентификация.
standard: specs/.instructions/docs/service/standard-service.md
criticality: critical-high
---

# frontend

## Назначение

Сервис frontend — единственный UI-слой системы. Реализует канбан-доску с тремя колонками статусов (To Do, In Progress, Done), drag-and-drop для смены статуса, CRUD-формы задач, фильтрацию/поиск и детальный просмотр с историей. Хранит JWT в localStorage, отображает страницу логина при его отсутствии/истечении. Является потребителем REST API обоих backend-сервисов.

**Обоснование критичности:** Уровень `critical-high` — frontend является единственным UI-слоем системы. При его недоступности пользователи полностью теряют доступ к системе управления задачами: невозможны создание, просмотр, редактирование и удаление задач. Обходных путей нет — нет альтернативного интерфейса.

## API контракты

*API контракты не применимо — сервис frontend является SPA и не предоставляет публичных API. Он выступает исключительно потребителем API сервисов task и auth.*

## Data Model

*Data Model не применимо — сервис frontend stateless со стороны хранилищ на сервере. Данные хранятся в client-state: JWT в localStorage, UI-состояние в Zustand stores (filterStore, authStore) в памяти браузера.*

## Потоки

Общий паттерн обработки в frontend: запросы к API проходят через TanStack Query хуки (useTasks, useUsers) → api-обёртки (tasks.api.ts, auth.api.ts) → backend REST API. UI-состояние (фильтры, auth) управляется через Zustand stores. Drag-and-drop реализован через dnd-kit с оптимистичным обновлением. Чтобы добавить новый функционал — создать хук в `hooks/`, api-функцию в `api/`, компонент в `components/`.

### Инициализация приложения

```
1. Браузер → App.tsx: загрузка приложения
2. App.tsx: проверка localStorage на наличие JWT
3. Если JWT отсутствует → редирект на /login
4. Если JWT присутствует → TanStack Query (useTasks): GET /api/v1/tasks
5. useTasks → tasks.api.ts → task-сервис: запрос списка задач
6. DashboardPage.tsx: задачи группируются по статусу → KanbanBoard отображает колонки
```

### Логин (REQ-9)

```
1. Пользователь → LoginPage.tsx: заполняет форму (email, password)
2. LoginPage.tsx → auth.api.ts: POST /api/v1/auth/login
3. auth-сервис → auth.api.ts: 200 { token, expiresIn, user }
4. auth.api.ts: сохраняет token в localStorage
5. authStore (Zustand): сохраняет user в памяти
6. App.tsx: редирект на / (DashboardPage)
```

### Создание задачи через форму (REQ-1, REQ-6)

```
1. Пользователь → TaskForm.tsx: открывает форму создания
2. TaskForm.tsx → useUsers (TanStack Query) → auth.api.ts: GET /api/v1/auth/users (список для assignee)
3. Пользователь заполняет форму; клиентская валидация title (обязателен) → ошибка при пустом
4. TaskForm.tsx → tasks.api.ts: POST /api/v1/tasks с Bearer JWT
5. TanStack Query: инвалидирует кэш tasks
6. KanbanBoard: перерисовывается, новая карточка появляется в колонке «To Do»
```

### Drag-and-drop смена статуса (REQ-2, US-2)

```
1. Пользователь → KanbanBoard.tsx (dnd-kit DndContext): захватывает карточку (DragStart)
2. Пользователь отпускает карточку в другую колонку (DragEnd)
3. filterStore / Zustand: оптимистично обновляет UI (карточка перемещается)
4. tasks.api.ts: PUT /api/v1/tasks/:id { status: newStatus } с Bearer JWT
5. При успехе: TanStack Query инвалидирует кэш, карточка остаётся в новой колонке
6. При ошибке: Zustand откатывает оптимистичное обновление, показывает уведомление
```

### Детальный просмотр задачи с историей (REQ-4, US-4)

```
1. Пользователь → TaskCard.tsx: клик по карточке
2. TaskDetail.tsx → useTasks (TanStack Query) → tasks.api.ts: GET /api/v1/tasks/:id
3. task-сервис: ответ 200 { ...Task, history: HistoryEntry[] }
4. TaskDetail.tsx: отображает поля задачи и историю изменений (кто, когда, что изменил)
```

### Удаление задачи с подтверждением (REQ-8)

```
1. Пользователь → TaskCard.tsx / TaskDetail.tsx: нажимает кнопку удаления
2. Frontend показывает диалог подтверждения
3. При подтверждении → tasks.api.ts: DELETE /api/v1/tasks/:id с Bearer JWT
4. TanStack Query: инвалидирует кэш tasks → карточка исчезает с доски
5. При отмене: диалог закрывается, никаких действий
```

### Фильтрация (REQ-3)

```
1. Пользователь → FilterPanel.tsx: выбирает фильтры (priority, assigneeId, search)
2. filterStore (Zustand): обновляет активные фильтры
3. useTasks (TanStack Query): пересылает GET /api/v1/tasks?... с новыми параметрами
4. KanbanBoard: перерисовывается с отфильтрованными задачами
```

## Code Map

### Tech Stack

| Технология | Версия | Назначение | Стандарт |
|-----------|--------|-----------|---------|
| React | 18 | UI-фреймворк | — |
| TypeScript | 5 | Типизация | — |
| TanStack Query | 5 | Server state (кэш задач, пользователей) | — |
| Zustand | 4 | Client/UI state (фильтры, drag-and-drop, auth) | — |
| dnd-kit | 6 | Drag-and-drop для канбан-доски | — |
| Vite | 5 | Сборщик/dev-server | — |

### Пакеты

Сервис организован по слоям: `pages/` — маршруты/страницы, `components/` — переиспользуемые UI-компоненты, `store/` — Zustand stores для client state, `api/` — функции-обёртки для REST API, `hooks/` — TanStack Query хуки для server state.

| Пакет | Назначение | Ключевые модули |
|-------|-----------|----------------|
| `frontend.pages` | Страницы приложения (маршруты) | `LoginPage.tsx`, `DashboardPage.tsx` |
| `frontend.components` | UI-компоненты: канбан, формы, детали | `KanbanBoard.tsx`, `KanbanColumn.tsx`, `TaskCard.tsx`, `TaskForm.tsx`, `TaskDetail.tsx`, `FilterPanel.tsx` |
| `frontend.store` | Zustand stores: auth, фильтры | `authStore.ts`, `filterStore.ts` |
| `frontend.api` | Обёртки REST API для task и auth | `tasks.api.ts`, `auth.api.ts` |
| `frontend.hooks` | TanStack Query хуки | `useTasks.ts`, `useUsers.ts` |

### Точки входа

- App: `src/frontend/src/main.tsx`
- Корневой компонент с роутингом: `src/frontend/src/App.tsx`

### Внутренние зависимости

frontend.pages → frontend.components + frontend.hooks + frontend.store
frontend.components → frontend.hooks + frontend.store + frontend.api
frontend.hooks → frontend.api
frontend.store (authStore, filterStore) — изолированы, без зависимостей от других пакетов

**Как добавить новый функционал:**
- Новый компонент → создать файл в `src/frontend/src/components/`, использовать хуки из `hooks/` и store из `store/`
- Новый API-вызов → добавить функцию в `api/tasks.api.ts` или `api/auth.api.ts`, создать хук в `hooks/`
- Новый UI-state → добавить поле в соответствующий Zustand store (`filterStore.ts` или `authStore.ts`)

### Makefile таргеты

| Таргет | Команда | Описание |
|--------|---------|----------|
| test | `make test-frontend` | Unit + integration тесты сервиса |
| lint | `make lint-frontend` | Линтинг кода сервиса |
| build | `make build-frontend` | Сборка Docker-образа |

## Зависимости

Frontend зависит от двух backend-сервисов: task (критическая — основной функционал канбан-доски) и auth (критическая — аутентификация и список пользователей). При недоступности любого из них деградирует соответствующая функциональность.

### task — CRUD задач

Frontend потребляет REST API task-сервиса для всех операций с задачами: создание, чтение списка, получение по ID с историей, обновление (включая смену статуса через drag-and-drop), удаление. При недоступности task-сервиса канбан-доска не загружается, все мутации возвращают ошибку. Запросы выполняются через TanStack Query хуки с Bearer JWT в заголовке Authorization.
Паттерн: **Conformist** (frontend конформен к API task-сервиса).
См. [INT-1: frontend → task CRUD API](../analysis/0001-task-dashboard/design.md#int-1-frontend--task-crud-api).

### auth — аутентификация и список пользователей

Frontend потребляет REST API auth-сервиса для логина (POST /api/v1/auth/login) и получения списка пользователей для назначения исполнителей (GET /api/v1/auth/users). При недоступности auth-сервиса логин невозможен; при уже существующем JWT список assignee не загружается (форма создания задачи деградирует).
Паттерн: **Conformist** (frontend конформен к API auth-сервиса).
См. [INT-2: frontend → auth (логин + список пользователей)](../analysis/0001-task-dashboard/design.md#int-2-frontend--auth-логин--список-пользователей).

## Доменная модель

Frontend не имеет собственных доменных агрегатов — оперирует DTO из backend API.

- DTO `Task` — клиентское представление задачи (mirrors SVC-1 API response)
- DTO `User` — клиентское представление пользователя (id, email, name)
- UI-состояние `FilterState` (Zustand filterStore): `{ status?: string, priority?: string, assigneeId?: string, search?: string }`
- UI-состояние `AuthState` (Zustand authStore): `{ token: string|null, user: User|null }`

## Границы автономии LLM

| Область | Уровень | Примечание |
|---------|---------|------------|
| React-компоненты (разметка, стили) | **Свободно:** | Реализация по требованиям Discussion |
| TanStack Query хуки (useQuery, useMutation) | **Свободно:** | Стандартный паттерн |
| Zustand stores (filterStore, authStore) | **Свободно:** | Структура определена в § 7 |
| dnd-kit DndContext/SortableContext | **Свободно:** | Паттерн из документации dnd-kit |
| Оптимистичное обновление drag-and-drop | **Флаг:** | Откат при ошибке API обязателен |
| Маршрутизация и защита маршрутов | **Флаг:** | Редирект на `/login` при отсутствии JWT |
| CSS-фреймворк/компонентная библиотека | **Флаг:** | Выбор на усмотрение LLM (Tailwind рекомендован) |
| Offline-режим / ServiceWorker | **CONFLICT:** | Вне scope v0.1.0; требует Discussion |
| Сохранение фильтров между сессиями | **CONFLICT:** | В v0.1.0 фильтры не персистируются; требует Discussion |

## Planned Changes

- **[analysis/0001-task-dashboard](../analysis/0001-task-dashboard/)** Создание task dashboard. Затрагивает: полный UI + backend.

<!-- chain: 0001-task-dashboard -->
Из Design 0001: создание нового сервиса frontend с нуля.
- ADDED: React 18 SPA, TypeScript, Vite (§ 5 Code Map / Tech Stack)
- ADDED: TanStack Query + Zustand — разделение server/client state (§ 5, § 7)
- ADDED: dnd-kit — drag-and-drop канбан-доска (§ 4, § 5)
- ADDED: страницы LoginPage, DashboardPage (§ 5 Code Map)
- ADDED: компоненты KanbanBoard, KanbanColumn, TaskCard, TaskForm, TaskDetail, FilterPanel (§ 5 Code Map)
- ADDED: stores authStore, filterStore (§ 7 Доменная модель)
- ADDED: api-обёртки tasks.api.ts, auth.api.ts (§ 5 Code Map)
- ADDED: хуки useTasks.ts, useUsers.ts (§ 5 Code Map)
- ADDED: потоки инициализации, логина, создания задачи, drag-and-drop, детального просмотра, удаления, фильтрации (§ 4)
- ADDED: зависимости INT-1 (frontend → task), INT-2 (frontend → auth) (§ 6)
<!-- /chain: 0001-task-dashboard -->

## Changelog

- **Создание сервиса** | DONE 2026-03-01 — первоначальная документация.
