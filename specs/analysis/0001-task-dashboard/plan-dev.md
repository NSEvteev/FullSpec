---
description: Plan Dev Task Dashboard — задачи реализации для task, auth, frontend.
standard: specs/.instructions/analysis/plan-dev/standard-plan-dev.md
standard-version: v1.3
index: specs/analysis/README.md
parent: plan-test.md
status: DRAFT
milestone: v0.1.0
---

# 0001: Task dashboard — Plan Dev

## Резюме

Реализация Task Dashboard затрагивает 3 сервиса: **task**, **auth**, **frontend**. Всего 20 задач (средняя сложность: 4.8/10). Ключевая зависимость: INFRA-блок (TASK-1) блокирует scaffold всех сервисов; системные тесты (TASK-19, TASK-20) зависят от полной функциональности всех трёх сервисов. Порядок: INFRA (wave 0) → auth + task параллельно (wave 1) → frontend (wave 2) → системные тесты (wave 3).

## Инфраструктура

### Задачи

#### TASK-1: Инициализация монорепо и shared-инфраструктуры
- **Сложность:** 5/10
- **Приоритет:** high
- **Зависимости:** —
- **TC:** INFRA
- **Источник:** SVC-1 § 5, SVC-2 § 5, SVC-3 § 5

Подзадачи:
- [ ] 1.1. Инициализация корневого package.json с workspaces
- [ ] 1.2. Создание shared tsconfig.base.json и per-service extends (deps: 1.1)
- [ ] 1.3. Создание docker-compose.yml (PostgreSQL 16 + сервисы task, auth, frontend) (deps: 1.1)
- [ ] 1.4. Создание docker-compose.test.yml для тестового окружения (deps: 1.3)
- [ ] 1.5. Создание .env.example с переменными окружения (JWT_SECRET, DATABASE_URL, порты) (deps: 1.3)

## SVC-1: task

### Задачи

#### TASK-2: Scaffold task-сервиса и Prisma-схема
- **Сложность:** 5/10
- **Приоритет:** high
- **Зависимости:** TASK-1
- **TC:** TC-1
- **Источник:** SVC-1 § 3, SVC-1 § 5

Подзадачи:
- [ ] 2.1. Инициализация Express-приложения (src/task/index.ts, tsconfig.json)
- [ ] 2.2. Prisma-схема: таблица tasks с полями и constraints (deps: 2.1)
- [ ] 2.3. Prisma-схема: таблица task_history с FK → tasks.id ON DELETE CASCADE (deps: 2.2)
- [ ] 2.4. Миграции: создание таблиц + индексы idx_tasks_status, idx_tasks_priority, idx_tasks_assigneeId (deps: 2.2, 2.3)
- [ ] 2.5. GIN-индекс idx_tasks_fts для полнотекстового поиска (to_tsvector) (deps: 2.4)

#### TASK-3: Zod-схемы валидации запросов
- **Сложность:** 3/10
- **Приоритет:** high
- **Зависимости:** TASK-2
- **TC:** TC-2, TC-4, TC-15
- **Источник:** SVC-1 § 2, SVC-1 § 5

Подзадачи:
- [ ] 3.1. Zod-схема CreateTaskRequest (title required, description/priority/assigneeId optional)
- [ ] 3.2. Zod-схема UpdateTaskRequest (все поля optional) (deps: 3.1)
- [ ] 3.3. Zod-схема QueryTaskParams (status, priority, assigneeId UUID validation, search) (deps: 3.1)
- [ ] 3.4. Middleware обработки ошибок Zod → 400 с описанием ошибки (deps: 3.1, 3.2, 3.3)

#### TASK-4: JWT-middleware (auth.middleware.ts)
- **Сложность:** 4/10
- **Приоритет:** high
- **Зависимости:** TASK-2
- **TC:** TC-3, TC-16, TC-17
- **Источник:** SVC-1 § 5, SVC-1 § 9, INT-3

Подзадачи:
- [ ] 4.1. auth.middleware.ts: извлечение Bearer token из заголовка Authorization
- [ ] 4.2. HTTP-клиент для GET /api/v1/auth/validate (deps: 4.1)
- [ ] 4.3. Типизация req.user (sub, email, name) и прокидывание в контроллеры (deps: 4.2)
- [ ] 4.4. Обработка ошибок: 401 при невалидном/истёкшем/отсутствующем токене (deps: 4.2)
- [ ] 4.5. Unit-тесты middleware с моком auth-сервиса (deps: 4.4)

#### TASK-5: CRUD-эндпоинты задач
- **Сложность:** 6/10
- **Приоритет:** high
- **Зависимости:** TASK-3, TASK-4
- **TC:** TC-1, TC-5, TC-8, TC-9, TC-10, TC-12, TC-13, TC-14
- **Источник:** SVC-1 § 2, SVC-1 § 4

Подзадачи:
- [ ] 5.1. Маршруты tasks.ts: POST, GET (list), GET (by id), PUT, DELETE
- [ ] 5.2. Контроллер tasks.controller.ts: 5 обработчиков с Zod-валидацией (deps: 5.1)
- [ ] 5.3. Сервис tasks.service.ts: Prisma CRUD-операции (create, findMany, findById, update, delete) (deps: 5.2)
- [ ] 5.4. Обработка ошибок: 404 для несуществующих задач, 400 для валидации (deps: 5.3)
- [ ] 5.5. Integration-тесты: создание, получение, обновление, удаление с реальной БД (deps: 5.4)

#### TASK-6: Фильтрация и полнотекстовый поиск
- **Сложность:** 5/10
- **Приоритет:** medium
- **Зависимости:** TASK-5
- **TC:** TC-6, TC-7
- **Источник:** SVC-1 § 3, SVC-1 § 4, SVC-1 § 9

Подзадачи:
- [ ] 6.1. Расширение сервиса: обработка query params status, priority, assigneeId
- [ ] 6.2. Prisma where-builder: динамическое формирование условий фильтрации (deps: 6.1)
- [ ] 6.3. Полнотекстовый поиск: ts_query → Prisma raw query по GIN-индексу (deps: 6.2)
- [ ] 6.4. Integration-тесты: фильтрация по priority+status, полнотекстовый поиск (deps: 6.3)

#### TASK-7: История изменений (task_history)
- **Сложность:** 5/10
- **Приоритет:** medium
- **Зависимости:** TASK-5
- **TC:** TC-10, TC-11
- **Источник:** SVC-1 § 4, SVC-1 § 7, SVC-1 § 9

Подзадачи:
- [ ] 7.1. Утилита diff: сравнение старого и нового состояния задачи, определение изменённых полей
- [ ] 7.2. Интеграция в update-сервис: создание записей task_history при каждом PUT (changedBy из req.user.sub) (deps: 7.1)
- [ ] 7.3. Расширение GET /tasks/:id: include task_history ORDER BY changedAt DESC (deps: 7.2)
- [ ] 7.4. Unit-тесты diff-утилиты (deps: 7.1)
- [ ] 7.5. Integration-тесты: обновление полей → проверка записей task_history (deps: 7.3)

## SVC-2: auth

### Задачи

#### TASK-8: Scaffold auth-сервиса, Prisma-схема и seed
- **Сложность:** 5/10
- **Приоритет:** high
- **Зависимости:** TASK-1
- **TC:** TC-18
- **Источник:** SVC-2 § 3, SVC-2 § 5

Подзадачи:
- [ ] 8.1. Инициализация Express-приложения (src/auth/index.ts, tsconfig.json)
- [ ] 8.2. Prisma-схема: таблица users с полями и UNIQUE email (deps: 8.1)
- [ ] 8.3. Миграция: создание таблицы users + индекс idx_users_email (deps: 8.2)
- [ ] 8.4. seed.ts: создание 2 тестовых пользователей (bcrypt cost=12) (deps: 8.3)
- [ ] 8.5. Настройка prisma db seed в package.json (deps: 8.4)

#### TASK-9: JWT-сервис (jose sign/verify)
- **Сложность:** 4/10
- **Приоритет:** high
- **Зависимости:** TASK-8
- **TC:** TC-23, TC-24, TC-25
- **Источник:** SVC-2 § 5, SVC-2 § 9

Подзадачи:
- [ ] 9.1. jwt.service.ts: функция sign (jose, HS256, claims: sub, iat, exp=1h)
- [ ] 9.2. jwt.service.ts: функция verify (jose, обработка expired/invalid) (deps: 9.1)
- [ ] 9.3. Конфигурация: JWT_SECRET из env (deps: 9.1)
- [ ] 9.4. Unit-тесты: sign → verify roundtrip, expired token, wrong secret (deps: 9.2)

#### TASK-10: Login-эндпоинт и Zod-схемы auth
- **Сложность:** 5/10
- **Приоритет:** high
- **Зависимости:** TASK-9
- **TC:** TC-18, TC-19, TC-20, TC-21, TC-22
- **Источник:** SVC-2 § 2, SVC-2 § 4

Подзадачи:
- [ ] 10.1. Zod-схема LoginRequest (email required, password required)
- [ ] 10.2. Маршрут auth.ts: POST /api/v1/auth/login (deps: 10.1)
- [ ] 10.3. auth.service.ts: поиск пользователя по email, bcrypt.compare (deps: 10.2)
- [ ] 10.4. Контроллер: Zod-валидация → сервис → jwt.service.sign → ответ с token + user (deps: 10.1, 10.3)
- [ ] 10.5. Integration-тесты: valid login, wrong password, nonexistent email, missing fields (deps: 10.4)

#### TASK-11: Validate-эндпоинт (INT-3)
- **Сложность:** 3/10
- **Приоритет:** high
- **Зависимости:** TASK-9
- **TC:** TC-23, TC-24, TC-25, TC-47
- **Источник:** SVC-2 § 2, SVC-2 § 4, INT-3

Подзадачи:
- [ ] 11.1. Маршрут: GET /api/v1/auth/validate
- [ ] 11.2. Контроллер: извлечение Bearer token, jwt.service.verify (deps: 11.1)
- [ ] 11.3. Ответы: 200 { valid, sub, email, name } или 401 { valid: false, error } (deps: 11.2)
- [ ] 11.4. Unit-тесты: valid token, expired, wrong secret (deps: 11.3)

#### TASK-12: Users-эндпоинт
- **Сложность:** 2/10
- **Приоритет:** medium
- **Зависимости:** TASK-8
- **TC:** TC-26, TC-27
- **Источник:** SVC-2 § 2, SVC-2 § 4, INT-2

Подзадачи:
- [ ] 12.1. Маршрут: GET /api/v1/auth/users
- [ ] 12.2. Контроллер: JWT guard + Prisma findMany (select: id, email, name — без passwordHash) (deps: 12.1)
- [ ] 12.3. Unit-тесты: with valid JWT, without JWT (deps: 12.2)

## SVC-3: frontend

### Задачи

#### TASK-13: Scaffold React-приложения
- **Сложность:** 4/10
- **Приоритет:** high
- **Зависимости:** TASK-1
- **TC:** TC-28
- **Источник:** SVC-3 § 5

Подзадачи:
- [ ] 13.1. Vite + React 18 + TypeScript инициализация
- [ ] 13.2. Установка зависимостей: @tanstack/react-query, zustand, @dnd-kit/core, @dnd-kit/sortable, react-router-dom (deps: 13.1)
- [ ] 13.3. Структура каталогов: pages/, components/, store/, api/, hooks/ (deps: 13.1)
- [ ] 13.4. main.tsx: QueryClientProvider + BrowserRouter (deps: 13.2)
- [ ] 13.5. Конфигурация API base URL из env (VITE_API_URL) (deps: 13.1)

#### TASK-14: API-слой и TanStack Query хуки
- **Сложность:** 4/10
- **Приоритет:** high
- **Зависимости:** TASK-13
- **TC:** TC-29, TC-31
- **Источник:** SVC-3 § 5, INT-1, INT-2

Подзадачи:
- [ ] 14.1. auth.api.ts: функции login(email, password), getUsers()
- [ ] 14.2. tasks.api.ts: функции createTask, getTasks, getTask, updateTask, deleteTask (deps: 14.1)
- [ ] 14.3. useTasks.ts: TanStack Query хуки (useTasksList, useTask, useCreateTask, useUpdateTask, useDeleteTask) (deps: 14.2)
- [ ] 14.4. useUsers.ts: TanStack Query хук для списка пользователей (deps: 14.1)
- [ ] 14.5. HTTP interceptor: автоматическое добавление JWT из localStorage в Authorization header (deps: 14.1)

#### TASK-15: Аутентификация (LoginPage + authStore)
- **Сложность:** 5/10
- **Приоритет:** high
- **Зависимости:** TASK-14
- **TC:** TC-28, TC-29, TC-30
- **Источник:** SVC-3 § 4, SVC-3 § 5, INT-2

Подзадачи:
- [ ] 15.1. authStore.ts (Zustand): token, user, login(), logout()
- [ ] 15.2. LoginPage.tsx: форма с email/password, обработка ошибок (deps: 15.1)
- [ ] 15.3. Вызов auth.api.login → сохранение token в localStorage + authStore (deps: 15.1, 15.2)
- [ ] 15.4. ProtectedRoute: компонент-обёртка, редирект на /login при отсутствии JWT (deps: 15.1)
- [ ] 15.5. App.tsx: роутинг /login (публичный) + / (protected) (deps: 15.4)

#### TASK-16: Канбан-доска с drag-and-drop
- **Сложность:** 7/10
- **Приоритет:** high
- **Зависимости:** TASK-15
- **TC:** TC-31, TC-33, TC-34
- **Источник:** SVC-3 § 4, SVC-3 § 5, SVC-3 § 9

Подзадачи:
- [ ] 16.1. DashboardPage.tsx: layout страницы с KanbanBoard
- [ ] 16.2. KanbanBoard.tsx: DndContext (dnd-kit), 3 колонки (todo, in_progress, done) (deps: 16.1)
- [ ] 16.3. KanbanColumn.tsx: SortableContext, отрисовка карточек по статусу (deps: 16.2)
- [ ] 16.4. TaskCard.tsx: draggable карточка задачи (title, priority, assignee badge) (deps: 16.3)
- [ ] 16.5. onDragEnd handler: определение source/destination колонки (deps: 16.2, 16.4)
- [ ] 16.6. Оптимистичное обновление: Zustand немедленно перемещает карточку, PUT /tasks/:id в фоне (deps: 16.5)
- [ ] 16.7. Откат при ошибке API: Zustand возвращает карточку в исходную колонку, уведомление (deps: 16.6)

#### TASK-17: Формы задач (создание, редактирование, удаление)
- **Сложность:** 5/10
- **Приоритет:** high
- **Зависимости:** TASK-15
- **TC:** TC-31, TC-32, TC-35
- **Источник:** SVC-3 § 4, SVC-3 § 5

Подзадачи:
- [ ] 17.1. TaskForm.tsx: поля title, description, priority, assignee (select из useUsers)
- [ ] 17.2. Клиентская валидация: title обязателен, ошибка при пустом (deps: 17.1)
- [ ] 17.3. Мутация создания: useCreateTask → POST /tasks → invalidate кэш tasks (deps: 17.1)
- [ ] 17.4. Мутация редактирования: useUpdateTask → PUT /tasks/:id → invalidate кэш (deps: 17.1)
- [ ] 17.5. Диалог удаления: кнопка → подтверждение → useDeleteTask → invalidate кэш (deps: 17.1)

#### TASK-18: Детальный просмотр и фильтрация
- **Сложность:** 4/10
- **Приоритет:** medium
- **Зависимости:** TASK-16
- **TC:** TC-8, TC-34
- **Источник:** SVC-3 § 4, SVC-3 § 5

Подзадачи:
- [ ] 18.1. TaskDetail.tsx: отображение всех полей задачи (title, description, priority, status, assignee)
- [ ] 18.2. История изменений: timeline из массива history (кто, когда, что изменил) (deps: 18.1)
- [ ] 18.3. FilterPanel.tsx: выпадающие списки priority, assignee, поле поиска
- [ ] 18.4. filterStore.ts (Zustand): активные фильтры, сброс (deps: 18.3)
- [ ] 18.5. Интеграция: filterStore → TanStack Query query params → перерисовка доски (deps: 18.4)

## Системные тесты

### Задачи

#### TASK-19: E2E и integration тесты
- **Сложность:** 7/10
- **Приоритет:** medium
- **Зависимости:** TASK-7, TASK-11, TASK-18
- **TC:** TC-36, TC-37, TC-38, TC-39, TC-40, TC-41, TC-42, TC-43, TC-44, TC-47
- **Источник:** SVC-1 § 4, SVC-2 § 4, SVC-3 § 4

Подзадачи:
- [ ] 19.1. Конфигурация docker-compose.test.yml: все сервисы + PostgreSQL + seed
- [ ] 19.2. Конфигурация Playwright: baseURL, auth fixture (login → JWT) (deps: 19.1)
- [ ] 19.3. E2E тесты: логин (TC-36), создание задачи full-stack (TC-37), drag-and-drop (TC-38) (deps: 19.2)
- [ ] 19.4. E2E тесты: фильтрация (TC-39), валидация пустого title (TC-40), удаление (TC-41) (deps: 19.3)
- [ ] 19.5. E2E тесты: назначение исполнителя (TC-43), JWT expiry mid-session (TC-44) (deps: 19.3)
- [ ] 19.6. Integration тесты: JWT-валидация task→auth без JWT (TC-42), изолированный вызов validate (TC-47) (deps: 19.1)

#### TASK-20: Нагрузочные тесты
- **Сложность:** 4/10
- **Приоритет:** low
- **Зависимости:** TASK-19
- **TC:** TC-45, TC-46
- **Источник:** SVC-1 § 2

Подзадачи:
- [ ] 20.1. Seed 120 задач для нагрузочного тестирования (все статусы и приоритеты)
- [ ] 20.2. k6/Locust сценарий: 50 параллельных GET /api/v1/tasks (TC-45) (deps: 20.1)
- [ ] 20.3. k6/Locust сценарий: 50 параллельных POST /api/v1/tasks с JWT (TC-46) (deps: 20.1)
- [ ] 20.4. Проверка p95 < 500ms, генерация отчёта (deps: 20.2, 20.3)

## Кросс-сервисные зависимости

| Зависимость | Блокирует | Причина |
|-------------|-----------|---------|
| TASK-4 (task) | TASK-19 (system) | JWT-middleware task требует реальный auth validate для integration-тестов |
| TASK-11 (auth) | TASK-19 (system) | Системные тесты вызывают auth validate через task-middleware |
| TASK-7 (task) | TASK-19 (system) | E2E тесты проверяют полную функциональность task (включая task_history) |
| TASK-18 (frontend) | TASK-19 (system) | E2E тесты Playwright требуют работающий frontend |

## Блоки выполнения

| BLOCK | Задачи | Сервисы | Зависимости | Wave |
|-------|--------|---------|-------------|------|
| BLOCK-5 | TASK-1 | shared (INFRA) | — | 0 |
| BLOCK-1 | TASK-2, TASK-3, TASK-4, TASK-5, TASK-6, TASK-7 | task | BLOCK-5 | 1 |
| BLOCK-2 | TASK-8, TASK-9, TASK-10, TASK-11, TASK-12 | auth | BLOCK-5 | 1 |
| BLOCK-3 | TASK-13, TASK-14, TASK-15, TASK-16, TASK-17, TASK-18 | frontend | BLOCK-5, BLOCK-1, BLOCK-2 | 2 |
| BLOCK-4 | TASK-19, TASK-20 | system | BLOCK-1, BLOCK-2, BLOCK-3 | 3 |

## Маппинг GitHub Issues

Маппинг выполняется **по команде пользователя** после перехода всей цепочки в RUNNING ([Стандарт analysis/ § 4.1](../standard-analysis.md#41-прямой-поток)). LLM создаёт каждый TASK-N → Issue через `/issue-create`.

| Элемент Plan Dev | GitHub Issue |
|------------------|-------------|
| TASK-N | Отдельный Issue через `/issue-create` |
| Подзадачи N.M | Чек-лист в body Issue |
| Приоритет | Label приоритета ([standard-labels.md](/.github/.instructions/labels/standard-labels.md)) |
| Зависимости | `**Зависит от:** #N` в body |
| TC | Ссылка в секции "Связанная документация" |
| Milestone | Из frontmatter Discussion ([standard-milestone.md § 6](/.github/.instructions/milestones/standard-milestone.md#6)) |

## Предложения

_(Нет предложений)_

## Отвергнутые предложения

_(Нет отвергнутых предложений)_
