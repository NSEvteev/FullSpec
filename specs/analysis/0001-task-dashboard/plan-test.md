---
description: Task Dashboard — встроенный дашборд управления задачами для создания, редактирования, удаления, фильтрации и отслеживания статусов задач. — проектирование распределения ответственностей между сервисами. — план тестов.
standard: specs/.instructions/analysis/plan-test/standard-plan-test.md
standard-version: v1.3
index: specs/analysis/README.md
parent: design.md
children:
  - plan-dev.md
status: WAITING
milestone: v0.1.0
---

# 0001: Task dashboard — Plan Tests

## Резюме

Plan Tests для Task Dashboard (0001). 3 сервиса: **task** (основной CRUD), **auth** (аутентификация, JWT), **frontend** (React-канбан, E2E через Playwright). Всего 47 acceptance-сценариев: 17 per-service для task (TC-1..TC-17), 10 для auth (TC-18..TC-27), 8 для frontend (TC-28..TC-35), 12 системных (TC-36..TC-47). Покрытие: REQ-1..REQ-10 (100%, 10 из 10), STS-1..STS-10 (100%, 10 из 10).

Ключевые тестовые решения (отличия от `specs/docs/.system/testing.md`):
- **Frontend: E2E через Playwright** — вместо unit-тестов компонентов; полные сценарии логин → создание задачи → drag-and-drop → фильтрация (ответ Clarify).
- **INT-3: изолированные integration-тесты** — task-middleware тестируется отдельно с валидным/невалидным/истёкшим JWT, auth-сервис мокируется (ответ Clarify).
- **Load-тесты (STS-10)** — нагрузочный сценарий с 100+ задачами, метрика p95 < 500ms (ответ Clarify).
- Стратегия мокирования для unit/integration соответствует `specs/docs/.system/testing.md`: unit мокает всё за пределами модуля, integration поднимает реальный PostgreSQL в Docker, e2e — все сервисы запущены реально через docker-compose.

## SVC-1: task

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-1 | POST /api/v1/tasks с валидным телом и Bearer JWT создаёт задачу — ответ 201 с id, title, status="todo", createdAt | integration | REQ-1, SVC-1 § 2 | valid_task_payload, valid_jwt |
| TC-2 | POST /api/v1/tasks с пустым title — ответ 400 с ошибкой "title is required" | unit | REQ-6, SVC-1 § 2 | task_empty_title |
| TC-3 | POST /api/v1/tasks без заголовка Authorization — ответ 401 Unauthorized | unit | SVC-1 § 2, INT-3 | no_auth_header |
| TC-4 | POST /api/v1/tasks с невалидным priority="urgent" — ответ 400 с ошибкой валидации | unit | SVC-1 § 2, SVC-1 § 7 | task_invalid_priority |
| TC-5 | GET /api/v1/tasks с валидным JWT возвращает список задач с полями items и total | integration | REQ-1, SVC-1 § 2 | valid_jwt, seeded_tasks |
| TC-6 | GET /api/v1/tasks?priority=high&status=todo фильтрует и возвращает только задачи с priority=high и status=todo | integration | REQ-3, SVC-1 § 4 | seeded_tasks_mixed, valid_jwt |
| TC-7 | GET /api/v1/tasks?search=логин применяет полнотекстовый поиск по GIN-индексу и возвращает только совпадения | integration | REQ-3, SVC-1 § 3 | seeded_tasks_search, valid_jwt |
| TC-8 | GET /api/v1/tasks/:id для существующей задачи возвращает задачу с полем history (массив записей изменений) | integration | REQ-4, SVC-1 § 4 | task_with_history, valid_jwt |
| TC-9 | GET /api/v1/tasks/:id для несуществующего id — ответ 404 Not Found | unit | SVC-1 § 2 | nonexistent_task_id, valid_jwt |
| TC-10 | PUT /api/v1/tasks/:id с { status: "in_progress" } обновляет статус задачи и создаёт запись в task_history (field="status", changedBy из JWT sub) | integration | REQ-2, SVC-1 § 4, SVC-1 § 7 | task_todo, valid_jwt |
| TC-11 | PUT /api/v1/tasks/:id с несколькими полями (title, priority, assigneeId) обновляет все переданные поля и фиксирует каждое изменение отдельной записью в task_history | integration | REQ-7, SVC-1 § 9 | task_todo, task_update_payload, valid_jwt |
| TC-12 | PUT /api/v1/tasks/:id для несуществующего id — ответ 404 Not Found | unit | SVC-1 § 2 | nonexistent_task_id, valid_jwt |
| TC-13 | DELETE /api/v1/tasks/:id удаляет задачу — ответ 204, повторный GET возвращает 404 | integration | REQ-8, SVC-1 § 2 | existing_task, valid_jwt |
| TC-14 | DELETE /api/v1/tasks/:id для несуществующего id — ответ 404 Not Found | unit | SVC-1 § 2 | nonexistent_task_id, valid_jwt |
| TC-15 | Zod-схема валидирует query params GET /api/v1/tasks — невалидный assigneeId (не UUID) отклоняется с 400 | unit | SVC-1 § 4, SVC-1 § 5 | invalid_assignee_query |
| TC-16 | JWT-middleware task-сервиса при валидном токене прокидывает req.user (sub, email, name) в контроллер для записи changedBy | integration | INT-3, SVC-1 § 9 | valid_jwt |
| TC-17 | JWT-middleware task-сервиса при истёкшем JWT возвращает 401 клиенту без выполнения бизнес-логики | integration | INT-3, SVC-1 § 9 | expired_jwt |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| valid_task_payload | Валидное тело для создания задачи | title: "Разработать login-форму", description: "Форма с email и password", priority: "high", assigneeId: "550e8400-e29b-41d4-a716-446655440001" |
| task_empty_title | Тело запроса с пустым заголовком | title: "", priority: "medium" |
| task_invalid_priority | Тело с невалидным приоритетом | title: "Задача", priority: "urgent" |
| seeded_tasks | 5 задач для листинга | [{ id: "uuid-t1", title: "Задача 1", status: "todo", priority: "high" }, { id: "uuid-t2", title: "Задача 2", status: "in_progress", priority: "low" }, ...] |
| seeded_tasks_mixed | 6 задач с разными priority и status | 2 high+todo, 2 medium+in_progress, 2 low+done |
| seeded_tasks_search | 3 задачи для поиска | [{ title: "Разработать login-форму" }, { title: "Настроить базу данных" }, { title: "Написать документацию" }] |
| task_with_history | Задача с 2 записями task_history | task: { id: "uuid-t3", title: "Задача с историей", status: "done" }, history: [{ field: "status", oldValue: "todo", newValue: "in_progress" }, { field: "status", oldValue: "in_progress", newValue: "done" }] |
| task_todo | Существующая задача со статусом todo | id: "uuid-t4", title: "Задача для обновления", status: "todo", priority: "medium" |
| task_update_payload | Тело для обновления нескольких полей | title: "Обновлённый заголовок", priority: "high", assigneeId: "550e8400-e29b-41d4-a716-446655440002" |
| existing_task | Существующая задача для удаления | id: "uuid-t5", title: "Задача для удаления", status: "todo" |
| nonexistent_task_id | Несуществующий UUID задачи | id: "00000000-0000-0000-0000-000000000000" |
| invalid_assignee_query | Невалидный assigneeId в query | assigneeId: "not-a-uuid" |
| no_auth_header | Запрос без заголовка Authorization | headers: {} |
| valid_jwt | Валидный JWT HS256 (sub=uuid-u1) | token: "eyJ...", sub: "550e8400-e29b-41d4-a716-446655440010", email: "ivan@example.com", name: "Иван Иванов", exp: now+3600 |
| expired_jwt | Истёкший JWT | token: "eyJ...", sub: "550e8400-e29b-41d4-a716-446655440010", exp: now-3600 |

## SVC-2: auth

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-18 | POST /api/v1/auth/login с валидными email и password возвращает 200 с token (JWT HS256), expiresIn=3600 и объектом user (id, email, name) | integration | REQ-9, SVC-2 § 4, INT-2 | auth_valid_credentials |
| TC-19 | POST /api/v1/auth/login с неверным паролем возвращает 401 с ошибкой "invalid credentials" | unit | REQ-9, SVC-2 § 2 | auth_wrong_password |
| TC-20 | POST /api/v1/auth/login с несуществующим email возвращает 401 с ошибкой "invalid credentials" | unit | REQ-9, SVC-2 § 2 | auth_nonexistent_email |
| TC-21 | POST /api/v1/auth/login без поля email — ответ 400 с ошибкой валидации Zod | unit | SVC-2 § 2 | auth_missing_email |
| TC-22 | POST /api/v1/auth/login без поля password — ответ 400 с ошибкой валидации Zod | unit | SVC-2 § 2 | auth_missing_password |
| TC-23 | GET /api/v1/auth/validate с валидным Bearer JWT возвращает 200 с { valid: true, sub, email, name } | unit | INT-3, SVC-2 § 4 | valid_jwt |
| TC-24 | GET /api/v1/auth/validate с истёкшим JWT (exp в прошлом) возвращает 401 с { valid: false, error: "token expired" } | unit | INT-3, SVC-2 § 4 | expired_jwt |
| TC-25 | GET /api/v1/auth/validate с JWT, подписанным неверным секретом, возвращает 401 с { valid: false, error: "invalid token" } | unit | INT-3, SVC-2 § 9 | jwt_wrong_secret |
| TC-26 | GET /api/v1/auth/users с валидным Bearer JWT возвращает 200 с массивом users (id, email, name — без passwordHash) | integration | REQ-9, SVC-2 § 4, INT-2 | valid_jwt, seeded_users |
| TC-27 | GET /api/v1/auth/users без Bearer JWT возвращает 401 Unauthorized | unit | SVC-2 § 2, INT-2 | no_auth_header |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| auth_valid_credentials | Пользователь с корректными данными (из seed) | email: "ivan@example.com", password: "TestPass123!", user_id: "550e8400-e29b-41d4-a716-446655440010" |
| auth_wrong_password | Пользователь с неверным паролем | email: "ivan@example.com", password: "wrongpassword" |
| auth_nonexistent_email | Несуществующий email | email: "ghost@example.com", password: "anypassword" |
| auth_missing_email | Тело без поля email | password: "TestPass123!" |
| auth_missing_password | Тело без поля password | email: "ivan@example.com" |
| seeded_users | 2 пользователя из seed-данных | [{ id: "550e8400-e29b-41d4-a716-446655440010", email: "ivan@example.com", name: "Иван Иванов" }, { id: "550e8400-e29b-41d4-a716-446655440011", email: "maria@example.com", name: "Мария Петрова" }] |
| jwt_wrong_secret | JWT с неверной подписью | token: "eyJ..." (подписан секретом "wrong-secret"), sub: "550e8400-e29b-41d4-a716-446655440010" |

## SVC-3: frontend

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-28 | Пользователь открывает приложение без JWT в localStorage — страница перенаправляет на /login | e2e | REQ-10, SVC-3 § 4 | browser_no_jwt |
| TC-29 | Пользователь заполняет форму логина с валидными email/password и нажимает "Войти" — токен сохраняется в localStorage, происходит редирект на канбан-доску | e2e | REQ-9, SVC-3 § 4, INT-2 | playwright_valid_login |
| TC-30 | Пользователь заполняет форму логина с неверным паролем — отображается сообщение об ошибке, редиректа нет | e2e | REQ-9, SVC-3 § 4, INT-2 | playwright_wrong_password |
| TC-31 | Пользователь заполняет форму создания задачи (заголовок, описание, приоритет, исполнитель) и нажимает "Создать" — новая карточка появляется в колонке "To Do" канбан-доски | e2e | REQ-1, REQ-6, SVC-3 § 4, INT-1 | playwright_create_task |
| TC-32 | Пользователь пытается создать задачу с пустым заголовком — форма не отправляется, отображается ошибка валидации рядом с полем заголовка | e2e | REQ-6, SVC-3 § 4 | playwright_empty_title |
| TC-33 | Пользователь перетаскивает карточку задачи из колонки "To Do" в "In Progress" (dnd-kit) — карточка немедленно отображается в новой колонке (оптимистичное обновление), статус персистируется после перезагрузки | e2e | REQ-2, SVC-3 § 4, SVC-3 § 9, INT-1 | playwright_drag_task |
| TC-34 | Пользователь выбирает фильтр "High" в панели фильтрации — канбан-доска отображает только задачи с priority=high, остальные скрыты | e2e | REQ-3, SVC-3 § 4, INT-1 | playwright_filter_priority |
| TC-35 | Пользователь нажимает кнопку удаления задачи, подтверждает в диалоге — карточка исчезает с доски; при отмене диалога — карточка остаётся | e2e | REQ-8, SVC-3 § 4, INT-1 | playwright_delete_task |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| browser_no_jwt | Состояние браузера без JWT | localStorage: {} (jwt отсутствует) |
| playwright_valid_login | Данные для логина через форму | email: "ivan@example.com", password: "TestPass123!" |
| playwright_wrong_password | Данные логина с неверным паролем | email: "ivan@example.com", password: "wrongpassword" |
| playwright_create_task | Данные для формы создания задачи | title: "Тестовая задача E2E", description: "Описание", priority: "high", assignee: "Иван Иванов" |
| playwright_empty_title | Попытка создания задачи с пустым заголовком | title: "", description: "Описание", priority: "medium" |
| playwright_drag_task | Задача в колонке To Do для перетаскивания | task: { title: "Перетащить меня", status: "todo" }, target_column: "In Progress" |
| playwright_filter_priority | Задачи на доске для проверки фильтрации | seeded: 2 high + 2 medium + 2 low, filter: "High" |
| playwright_delete_task | Задача для удаления | task: { title: "Удалить меня", status: "todo" } |

## Системные тест-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-36 | Пользователь логинится через POST /api/v1/auth/login с валидными credentials — получает JWT, токен используется в последующих запросах | e2e | STS-1, INT-2 | sys_valid_credentials |
| TC-37 | Frontend отправляет POST /api/v1/tasks → task вызывает GET /api/v1/auth/validate → auth возвращает 200 → task создаёт запись в БД → frontend получает 201 с созданной задачей | e2e | STS-2, INT-1, INT-3 | sys_valid_credentials, sys_create_task_payload |
| TC-38 | Пользователь перетаскивает карточку задачи в новую колонку → frontend отправляет PUT /api/v1/tasks/:id → задача остаётся в новой колонке после перезагрузки страницы | e2e | STS-3, INT-1, INT-3 | sys_task_for_drag, sys_valid_jwt |
| TC-39 | Frontend отправляет GET /api/v1/tasks?priority=high → task возвращает только задачи с priority=high → канбан-доска отображает только отфильтрованные карточки | e2e | STS-4, INT-1 | sys_tasks_mixed_priority, sys_valid_jwt |
| TC-40 | Пользователь отправляет форму создания задачи с пустым заголовком → frontend показывает ошибку валидации на клиенте, POST /api/v1/tasks не отправляется | e2e | STS-5, INT-1, REQ-6 | sys_valid_jwt |
| TC-41 | Пользователь подтверждает удаление задачи → DELETE /api/v1/tasks/:id → карточка исчезает с канбан-доски, повторный GET возвращает 404 | e2e | STS-6, INT-1, INT-3 | sys_task_for_delete, sys_valid_jwt |
| TC-42 | GET /api/v1/tasks без JWT-заголовка (или с истёкшим токеном) — task-middleware возвращает 401, frontend получает 401 | integration | STS-7, INT-3 | expired_jwt |
| TC-43 | Frontend загружает форму создания задачи → GET /api/v1/auth/users возвращает список пользователей → пользователь выбирает исполнителя → задача создаётся с заполненным assigneeId | e2e | STS-8, INT-1, INT-2, REQ-9 | sys_valid_credentials, sys_create_task_with_assignee |
| TC-44 | JWT истекает в процессе сессии → frontend получает 401 на следующем запросе к task → происходит редирект на /login | e2e | STS-9, INT-1, INT-3, REQ-10 | sys_expired_jwt_mid_session |
| TC-45 | 50 параллельных GET /api/v1/tasks к task-сервису при наличии 100+ задач в БД — p95 время ответа не превышает 500ms | load | STS-10, INT-1, REQ-5 | sys_100_tasks_seed |
| TC-46 | 50 параллельных POST /api/v1/tasks к task-сервису с валидными JWT — p95 время ответа создания не превышает 500ms | load | STS-10, INT-1, INT-3, REQ-5 | sys_valid_jwt, sys_create_task_payload |
| TC-47 | task-middleware делает изолированный вызов GET /api/v1/auth/validate с валидным JWT — auth возвращает 200 с данными пользователя; с истёкшим JWT — auth возвращает 401 | integration | STS-7, INT-3 | valid_jwt, expired_jwt |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| sys_valid_credentials | Системные credentials для e2e (из seed) | email: "ivan@example.com", password: "TestPass123!" |
| sys_valid_jwt | Системный валидный JWT для e2e | token: "eyJ...", sub: "550e8400-e29b-41d4-a716-446655440010", exp: now+3600 |
| sys_create_task_payload | Тело для создания задачи в e2e | title: "Системная тестовая задача", priority: "medium", assigneeId: null |
| sys_task_for_drag | Задача для e2e drag-and-drop теста | id: "uuid-sys-t1", title: "Перетащить в In Progress", status: "todo" |
| sys_task_for_delete | Задача для e2e теста удаления | id: "uuid-sys-t2", title: "Задача для удаления e2e", status: "todo" |
| sys_tasks_mixed_priority | 6 задач с разными приоритетами для теста фильтрации | 2×high, 2×medium, 2×low (все в status: todo) |
| sys_create_task_with_assignee | Тело создания задачи с исполнителем | title: "Задача с исполнителем", assigneeId: "550e8400-e29b-41d4-a716-446655440011" |
| sys_expired_jwt_mid_session | Истёкший JWT для теста mid-session | token: "eyJ...", exp: now-60 (истёк 1 минуту назад) |
| sys_100_tasks_seed | 100+ задач в БД для нагрузочного теста | count: 120, statuses: [todo, in_progress, done], priorities: [low, medium, high] |

## Матрица покрытия

| Источник | TC |
|----------|----|
| REQ-1 | TC-1, TC-5, TC-31, TC-37 |
| REQ-2 | TC-10, TC-33, TC-38 |
| REQ-3 | TC-6, TC-7, TC-34, TC-39 |
| REQ-4 | TC-8 |
| REQ-5 | TC-45, TC-46 |
| REQ-6 | TC-2, TC-32, TC-40 |
| REQ-7 | TC-11 |
| REQ-8 | TC-13, TC-35, TC-41 |
| REQ-9 | TC-18, TC-26, TC-29, TC-36, TC-43 |
| REQ-10 | TC-28, TC-44 |
| STS-1 | TC-36 |
| STS-2 | TC-37 |
| STS-3 | TC-38 |
| STS-4 | TC-39 |
| STS-5 | TC-40 |
| STS-6 | TC-41 |
| STS-7 | TC-42, TC-47 |
| STS-8 | TC-43 |
| STS-9 | TC-44 |
| STS-10 | TC-45, TC-46 |

## Блоки тестирования

| BLOCK | TC | Сервисы | Dev BLOCK |
|-------|----|---------|-----------|
| BLOCK-1 | TC-1..TC-17 | SVC-1: task | BLOCK-1 |
| BLOCK-2 | TC-18..TC-27 | SVC-2: auth | BLOCK-2 |
| BLOCK-3 | TC-28..TC-35 | SVC-3: frontend | BLOCK-3 |
| BLOCK-4 | TC-36..TC-47 | e2e, integration, load (system) | BLOCK-4 |
