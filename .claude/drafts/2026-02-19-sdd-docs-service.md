# docs/{svc}.md — сервисный документ

Спецификация per-service документа: 10 секций, 3 уровня детализации, шаблон, пример notification.md. Один файл — всё, что LLM-разработчику нужно знать о сервисе для написания кода.

## Контекст

**Задача:** Определить формат docs/{svc}.md — per-service документа, являющегося основным рабочим контекстом LLM-разработчика при реализации задач.

**Источник:** `.claude/drafts/2026-02-19-sdd-chain-rethink.md` (строки 636-1148)

**Связанные файлы:**
- `2026-02-19-sdd-structure.md` — общая структура и решения
- `2026-02-19-sdd-docs-overview.md` — overview.md (системный взгляд, {svc}.md — per-service детали)
- `2026-02-19-sdd-docs-conventions.md` — conventions.md (shared-пакеты интерфейсы, на которые ссылается секция Зависимости)
- `2026-02-19-sdd-docs-technology.md` — standard-{tech}.md (на которые ссылается секция Code Map / Tech Stack)

---

## Содержание

### Полный перечень секций docs/{svc}.md

Составлен на основе анализа трёх текущих стандартов:
- `standard-service.md` — секции сервисного документа, Code Map, Planned Changes, Changelog
- `standard-architecture.md` — форматы data-flows (Участники, Контракт, Паттерн, Протокол), context-map (DDD-паттерны связей)
- `standard-technology.md` — per-tech стандарты, связь Tech Stack → standard-{tech}.md

#### Секции

| # | Секция | Содержание | Уровень детализации | Источник |
|---|--------|-----------|--------------------|---------|
| 1 | **Назначение** | Что делает сервис, зона ответственности. 1-3 предложения | Навигационный | standard-service.md § 5.1 |
| 2 | **API контракты** | Каждый endpoint подробно: path, method, auth, request schema, response schema, status codes, паттерн (sync/async), протокол. **Достаточно, чтобы написать новый endpoint по аналогии** | Имплементационный | standard-service.md § 5.2 + data-flows.md (расширено) |
| 3 | **Data Model** | Каждая таблица/коллекция подробно: колонки с типами, PK/FK, индексы, constraints, defaults. **Достаточно, чтобы добавить колонку по аналогии** | Имплементационный | standard-service.md § 5.3 (расширено) |
| 4 | **Потоки** | Ключевые runtime-сценарии: как данные проходят от входа до выхода. Текстовое описание "событие → обработка → результат" | Архитектурный | Новое (не было в текущей модели) |
| 5 | **Code Map** | Tech Stack (ссылки на standard-{tech}.md), пакеты/модули, точки входа, внутренние зависимости | Навигационный | standard-service.md § 5.4 + standard-technology.md § 4 |
| 6 | **Зависимости** | От кого зависит (абзац + ссылка на API провайдера). Что владеет в shared/. DDD-паттерн связи | Навигационный | standard-service.md § 5.5 + § 7 + context-map.md |
| 7 | **Доменная модель** | Агрегаты, доменные события, инварианты. Встроено в per-service | Архитектурный | standard-service.md § 6 (per-domain → встроено) |
| 8 | **Границы автономии LLM** | Три уровня: Свободно, Флаг, CONFLICT | Навигационный | standard-service.md § 5.6 |
| 9 | **Planned Changes** | Ссылки на активные analysis/ документы, затрагивающие сервис | Навигационный | standard-service.md § 5.7 (упрощён) |
| 10 | **Changelog** | История изменений сервиса. Ссылки на analysis/ | Навигационный | standard-service.md § 5.8 |

**Три уровня детализации:**

| Уровень | Что значит | Пример |
|---------|-----------|--------|
| **Имплементационный** | Достаточно для написания кода по аналогии без чтения исходников | API: полный request/response, Data Model: типы колонок |
| **Архитектурный** | Понимание "как работает" без деталей реализации | Потоки, доменная модель |
| **Навигационный** | Знать что есть и где искать | Назначение, Code Map, зависимости (со ссылками) |

#### Изменения относительно текущей модели

| Аспект | Текущая модель (standard-service.md) | Новая модель |
|--------|--------------------------------------|--------------|
| API контракты | Навигационная таблица (Тип, Endpoint, Метод, Описание). "Полный контракт описан в Design" | **Имплементационный** — request/response schema, status codes, auth, паттерн, протокол. Полный контракт в docs/, не в Design |
| Data Model | Навигационная таблица (Сущность, Хранилище, Назначение) | **Имплементационный** — колонки с типами, PK/FK, индексы, constraints |
| Потоки | Нет (разбросано по Code Map и data-flows.md) | **Новая секция** — ключевые runtime-сценарии |
| Зависимости | Таблица (Тип, Путь, Что используем, Роль) | **Абзац + ссылка** на API провайдера + DDD-паттерн связи |
| Shared-код | Отдельная § 7 в standard-service.md | Встроено в секцию "Зависимости" |
| Доменная модель | Отдельные файлы domains/{domain}.md | **Встроено** в per-service документ |
| Planned Changes | Полные дельты ADDED/MODIFIED/REMOVED | **Лёгкие указатели** — ссылки на analysis/ |
| Расположение | `specs/architecture/services/{svc}.md` | `specs/docs/{svc}.md` |

---

### Пример: docs/notification.md

`````markdown
# notification

## Назначение

Сервис push-уведомлений в реальном времени. Управляет WebSocket-соединениями,
подписывается на системные события через AMQP, доставляет уведомления через WS и REST API.
Основные потребители: frontend (REST для истории, WebSocket для push) и все сервисы системы
(публикуют события, которые notification преобразует в уведомления пользователям).

## API контракты

Сервис предоставляет 3 типа интерфейсов: REST API для получения/обновления уведомлений,
WebSocket для real-time push, и AMQP subscriber для приёма системных событий. Все REST
endpoint-ы требуют Bearer JWT и следуют конвенциям из [conventions.md](../.system/conventions.md).

### GET /api/v1/notifications

Список уведомлений текущего пользователя с пагинацией.

- **Auth:** Bearer JWT (обязательно)
- **Паттерн:** sync | **Протокол:** REST/JSON

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| limit | int | нет (default 20, max 100) | Количество |
| offset | int | нет (default 0) | Смещение |
| status | string | нет | Фильтр: `read`, `unread` |

**Response 200:**
```json
{
  "items": [
    {
      "id": "uuid",
      "type": "system|user|admin",
      "title": "string",
      "body": "string",
      "status": "read|unread",
      "created_at": "ISO8601"
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

**Errors:** 401 Unauthorized, 422 Validation Error

---

### PATCH /api/v1/notifications/{id}

Обновление статуса уведомления.

- **Auth:** Bearer JWT (обязательно, владелец уведомления)
- **Паттерн:** sync | **Протокол:** REST/JSON

**Request:**
```json
{ "status": "read" }
```

**Response 200:** Обновлённый объект notification (как в GET).

**Errors:** 401 Unauthorized, 403 Forbidden (не владелец), 404 Not Found

---

### WebSocket /ws/notifications

Push-уведомления в реальном времени.

- **Auth:** JWT передаётся как query param `?token=...` при подключении
- **Паттерн:** async | **Протокол:** WebSocket/JSON

**Подключение:** `ws://host/ws/notifications?token={jwt}`

**Server → Client messages:**
```json
{
  "event": "notification.created",
  "data": {
    "id": "uuid",
    "type": "system",
    "title": "string",
    "body": "string",
    "created_at": "ISO8601"
  }
}
```

**Rate limit:** max 10 одновременных соединений на пользователя.

---

### Event: system.events (subscriber)

Подписка на системные события через message broker.

- **Паттерн:** async | **Протокол:** AMQP/JSON
- **Канал:** `system.events`

**Обрабатываемые события:**
| Событие | Издатель | Действие |
|---------|----------|----------|
| UserRegistered | auth | Создать welcome-уведомление |
| PasswordChanged | auth | Создать security-уведомление |
| AdminAction | admin | Создать admin-уведомление |
| SystemError | * | Создать alert-уведомление |

## Data Model

PostgreSQL — основное хранилище уведомлений (таблица `notifications`). Redis — кэш активных
WebSocket-соединений для быстрого lookup при push. PostgreSQL-данные персистентны с TTL 90 дней,
Redis-данные эфемерны (удаляются при disconnect).

### notifications (PostgreSQL)

| Колонка | Тип | Constraints | Описание |
|---------|-----|------------|----------|
| id | UUID | PK, default gen_random_uuid() | Идентификатор |
| user_id | UUID | NOT NULL, INDEX | Владелец уведомления |
| type | VARCHAR(20) | NOT NULL, CHECK (system, user, admin) | Тип |
| title | VARCHAR(255) | NOT NULL | Заголовок |
| body | TEXT | NOT NULL | Тело |
| status | VARCHAR(10) | NOT NULL, DEFAULT 'unread', CHECK (read, unread) | Статус |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now(), INDEX | Дата создания |

**Индексы:**
- `idx_notifications_user_id` — по user_id (основной запрос)
- `idx_notifications_created_at` — по created_at (TTL cleanup, сортировка)

**TTL:** Cleanup уведомлений старше 90 дней (cron job).

### ws:connections:{user_id} (Redis)

| Ключ | Тип | TTL | Описание |
|------|-----|-----|----------|
| ws:connections:{user_id} | SET of session_id | При disconnect | Активные WebSocket session ID |

## Потоки

Общий паттерн обработки в notification: внешнее событие или запрос приходит через одну из трёх
точек входа (REST API, WebSocket, AMQP consumer). Бизнес-логика в `events.handlers` или
`api.routes` формирует данные, `storage.repository` сохраняет в PostgreSQL, `ws.hub` отправляет
push через WebSocket если пользователь онлайн. Чтобы добавить новый тип уведомления — достаточно
добавить обработчик в `events.handlers` и маппинг события на шаблон уведомления.

### Доставка уведомления (основной сценарий)

```
1. Другой сервис публикует событие в system.events (AMQP)
2. notification.events.handlers получает событие
3. handlers определяет тип → формирует Notification
4. notification.storage.repository сохраняет в PostgreSQL
5. notification.ws.hub находит активные WS по user_id (Redis lookup)
6. hub отправляет JSON-сообщение через WebSocket
```

### Получение истории (REST)

```
1. frontend → GET /api/v1/notifications?status=unread
2. JWT middleware валидирует токен (shared/auth → auth-сервис)
3. notification.api.routes извлекает user_id из токена
4. notification.storage.repository → SELECT с пагинацией
5. Response: JSON массив уведомлений
```

## Code Map

### Tech Stack

| Технология | Версия | Назначение | Стандарт |
|-----------|--------|-----------|---------|
| Python | 3.12 | Backend | [standard-python.md](.technologies/standard-python.md) |
| PostgreSQL | 16 | Хранение уведомлений | [standard-postgresql.md](.technologies/standard-postgresql.md) |
| Redis | 7 | WS connections | [standard-redis.md](.technologies/standard-redis.md) |
| FastAPI | — | API-фреймворк | — |

### Пакеты

Сервис разделён на 4 пакета по принципу "точка входа + хранение": три пакета принимают запросы
каждый по своему каналу (REST, WebSocket, AMQP), четвёртый — общее хранилище, которое используют все три.

| Пакет | Назначение | Ключевые модули |
|-------|-----------|----------------|
| `notification.ws` | WebSocket Hub — управление соединениями, отправка сообщений | `hub.py`, `connections.py` |
| `notification.events` | Event Consumer — подписка на system.events, маршрутизация | `handlers.py`, `router.py` |
| `notification.api` | REST API — endpoints, валидация, пагинация | `routes.py`, `schemas.py` |
| `notification.storage` | Persistence — PostgreSQL repository, Redis connections | `repository.py`, `models.py` |

### Точки входа

- API: `notification/api/routes.py`
- WebSocket: `notification/ws/hub.py`
- Events: `notification/events/handlers.py`

### Внутренние зависимости

notification.api → notification.storage
notification.ws → notification.storage
notification.events → notification.ws (push) + notification.storage (persist)

**Как добавить новый функционал:**
- Новый REST endpoint → создать route в `api/routes.py`, schema в `api/schemas.py`, query в `storage/repository.py`
- Новый тип уведомления из события → добавить case в `events/handlers.py`, маппинг события → шаблон уведомления
- Новый WS-функционал → расширить `ws/hub.py` (новый тип сообщения)

## Зависимости

Notification зависит от auth (критическая — без JWT-валидации REST и WS не работают) и от
всех сервисов-издателей через AMQP (некритическая — если издатель упал, notification продолжает
работать, просто новые события не приходят). Прямых sync-вызовов к другим сервисам кроме auth нет.

### auth — валидация JWT
Notification использует auth-сервис для валидации JWT-токенов при WebSocket-подключении
и REST-запросах. Для REST — автоматически через shared/auth middleware (разработчику достаточно
добавить `Depends(get_current_user)` в route). Для WebSocket — явный вызов при подключении.
Если auth недоступен — все запросы возвращают 401, WS-подключения отклоняются.
Паттерн: **Conformist** (notification конформен к API auth).
См. [POST /api/v1/auth/validate](auth.md#post-apiv1authvalidate).

### shared/auth/ — JWT Middleware
Notification использует shared JWT middleware для валидации токенов в HTTP-запросах.
Подключение: `from shared.auth import get_current_user` → `Depends(get_current_user)` в route.
Роль: consumer. Владелец: auth. Интерфейс: [conventions.md](../.system/conventions.md#sharedauth--jwt-middleware).

### * (любой сервис) — системные события
Notification подписывается на канал `system.events` через AMQP. Все сервисы, публикующие
события (auth, task, admin), являются неявными зависимостями. При добавлении нового сервиса,
который публикует события — достаточно добавить handler в `events/handlers.py`.
Паттерн: **Published Language** (стандартные события).
Роль: subscriber. Схемы событий: [conventions.md](../.system/conventions.md#sharedevents--схемы-событий-amqp).

## Доменная модель

Notification реализует домен Notifications. Основная сущность — Notification — проходит
жизненный цикл: создание (из события) → доставка (WS push) → чтение (пользователь пометил
read) → удаление (TTL 90 дней). WebSocketConnection — вспомогательная сущность, живёт
только пока пользователь подключён.

### Агрегаты

| Агрегат | Описание |
|---------|----------|
| Notification | Уведомление (тип, заголовок, тело, статус read/unread, TTL 90 дней). Жизненный цикл: created → delivered → read → expired |
| WebSocketConnection | Активное WS-соединение пользователя. Эфемерное — существует только при подключении |

### Инварианты

- Одно уведомление принадлежит одному пользователю
- Уведомление не может быть помечено read до сохранения в БД
- TTL уведомлений — 90 дней (cleanup удаляет старые)
- Max 10 одновременных WS-соединений на пользователя (при превышении — reject)

### Доменные события

| Событие | Описание |
|---------|----------|
| NotificationCreated | Новое уведомление сохранено → push через WebSocket |
| NotificationRead | Статус обновлён на read |

## Границы автономии LLM

- **Свободно:** реализация внутри пакета (алгоритмы, рефакторинг, оптимизация)
- **Флаг:** изменение контрактов между пакетами (может затронуть тесты)
- **CONFLICT:** изменение API (/notifications/*), data model (колонки, индексы), WebSocket-протокол

## Planned Changes

- **[analysis/0002-notification-groups](../analysis/0002-notification-groups/)**
  Группировка уведомлений по категориям. Затрагивает: API (новый query param), Data Model (новая колонка group_id).

## Changelog

- **[analysis/0001-realtime-notifications](../analysis/0001-realtime-notifications/)** | DONE 2026-03-01
  Создание сервиса. Затрагивало: всё.
`````

---

### Шаблон: docs/{svc}.md

`````markdown
# {svc}

## Назначение

{Что делает сервис, зона ответственности. 2-3 предложения. Указать ключевых потребителей (frontend, другие сервисы) и основной способ взаимодействия (REST, WS, события).}

## API контракты

{Абзац: обзор API сервиса — сколько endpoint-ов, какие группы, общий паттерн. Все endpoint-ы следуют конвенциям из [conventions.md](../.system/conventions.md) (формат ответов, ошибок, пагинация, auth).}

### {METHOD} {/api/v1/path}

{Что делает endpoint. Одно предложение.}

- **Auth:** {Bearer JWT / API Key / нет}
- **Паттерн:** {sync/async} | **Протокол:** {REST/JSON, gRPC, GraphQL}

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| {param} | {type} | {да/нет (default X)} | {описание} |

**Request:** *(если POST/PUT/PATCH)*
```json
{ "{field}": "{type}" }
```

**Response {code}:**
```json
{ "{field}": "{type | описание}" }
```

**Errors:** {code} {описание}, {code} {описание}

---

### WebSocket {/ws/path} *(если есть)*

{Описание.}

- **Auth:** {как передаётся}
- **Паттерн:** async | **Протокол:** WebSocket/JSON

**Подключение:** `ws://host{/ws/path}?{auth_param}={value}`

**Server → Client messages:**
```json
{ "event": "{event_name}", "data": { "{field}": "{type}" } }
```

---

### Event: {channel} ({publisher/subscriber})  *(если есть)*

{Описание — что публикует или обрабатывает.}

- **Паттерн:** async | **Протокол:** {AMQP/JSON, Kafka, Redis Pub/Sub}
- **Канал:** `{channel_name}`

**Обрабатываемые события:** *(для subscriber)*
| Событие | Издатель | Действие |
|---------|----------|----------|
| {EventName} | {svc} | {что делает при получении} |

**Публикуемые события:** *(для publisher)*
| Событие | Когда | Payload |
|---------|-------|---------|
| {EventName} | {триггер} | `{ "{field}": "{type}" }` |

## Data Model

{Абзац: какие хранилища использует сервис, как они разделяют ответственность. Например: "PostgreSQL — основное хранилище уведомлений, Redis — кэш активных WS-соединений."}

### {table_name} ({storage}: PostgreSQL/MongoDB/Redis)

| Колонка | Тип | Constraints | Описание |
|---------|-----|------------|----------|
| {col} | {TYPE} | {PK/FK/NOT NULL/DEFAULT/CHECK/INDEX} | {описание} |

**Индексы:**
- `idx_{table}_{col}` — по {col} ({зачем: основной запрос / сортировка / FK lookup})

**Особенности:** {TTL, партиционирование, репликация — если есть}

### {key_pattern} (Redis) *(если есть)*

| Ключ | Тип | TTL | Описание |
|------|-----|-----|----------|
| {pattern}:{id} | {SET/HASH/STRING/LIST} | {TTL или "при событии"} | {описание} |

## Потоки

{Абзац: как в целом устроена обработка внутри сервиса. Какой пакет принимает запросы, куда передаёт, где хранит результат. Это "жизненный цикл запроса" — общий паттерн, по которому разработчик добавляет новый функционал.}

### {Название сценария} ({основной / альтернативный / ошибка})

```
1. {Актор/сервис} → {модуль}: {действие}
2. {модуль}: {внутренняя обработка}
3. {модуль} → {хранилище}: {операция}
4. {модуль} → {Актор/сервис}: {результат}
```

## Code Map

### Tech Stack

| Технология | Версия | Назначение | Стандарт |
|-----------|--------|-----------|---------|
| {tech} | {ver} | {назначение} | [standard-{tech}.md](.technologies/standard-{tech}.md) |

### Пакеты

{Абзац: общий принцип организации кода — как пакеты разделяют ответственность. "Сервис разделён на N пакетов по принципу {какому}. {package1} — точка входа для {чего}, {package2} — бизнес-логика, {package3} — хранение."}

| Пакет | Назначение | Ключевые модули |
|-------|-----------|----------------|
| `{svc}.{package}` | {назначение} | `{module1}.py`, `{module2}.py` |

### Точки входа

- API: `{svc}/{package}/{module}.py`
- {другой тип}: `{path}`

### Внутренние зависимости

{package1} → {package2}
{package3} → {package2} + {package4}

{Абзац: как добавить новый функционал — рецепт. "Чтобы добавить новый endpoint: 1) создать route в {package}.{module}, 2) добавить schema в {package}.{module}, 3) добавить repository-метод в {package}.{module}. Чтобы обработать новое событие: 1) добавить handler в {package}.{module}, 2) ...".}

## Зависимости

{Абзац: общая картина зависимостей сервиса — от скольких сервисов зависит, каким способом (sync REST / async events / shared-код). Какие зависимости критические (если упадёт X — сервис не работает), какие некритические (если упадёт Y — деградация).}

### {other_svc} — {зачем}
{Описание: что конкретно использует, как именно подключается (middleware автоматически / явный вызов), что произойдёт если зависимость недоступна.}
Паттерн: **{Conformist/ACL/Published Language}** ({пояснение}).
См. [{METHOD} {path}]({other_svc}.md#{anchor}).

### shared/{package}/ — {зачем}
{Описание: что использует, как подключить (import, Depends), роль в обработке запроса.}
Роль: consumer. Владелец: {owner_svc}. Интерфейс: [conventions.md](../.system/conventions.md#shared{package}).

## Доменная модель

{Абзац: какой домен реализует сервис, основная бизнес-сущность, ключевой жизненный цикл (создание → состояния → завершение).}

### Агрегаты

| Агрегат | Описание |
|---------|----------|
| {Name} | {описание, ключевые атрибуты, жизненный цикл} |

### Инварианты

- {Бизнес-правило, которое всегда должно быть истинным}

### Доменные события

| Событие | Описание |
|---------|----------|
| {EventName} | {когда возникает → что запускает} |

## Границы автономии LLM

- **Свободно:** {что можно менять без согласования}
- **Флаг:** {что требует проверки — может затронуть другие пакеты/тесты}
- **CONFLICT:** {что нельзя менять без обсуждения — API, data model, протоколы}

## Planned Changes

- **[analysis/{NNNN}-{slug}](../analysis/{NNNN}-{slug}/)**
  {Краткое описание изменения. Затрагивает: {что именно}.}

## Changelog

- **[analysis/{NNNN}-{slug}](../analysis/{NNNN}-{slug}/)** | DONE {дата}
  {Краткое описание. Затрагивало: {что}.}
`````

---

## Аудит старых документов

| Старый документ | Что переиспользовать |
|-----------------|---------------------|
| `specs/.instructions/living-docs/service/standard-service.md` | Двухслойная модель AS IS/Planned Changes, триггеры (Design→WAITING, ADR→DONE), Code Map на уровне пакетов, Границы автономии LLM (3 уровня), шаблон заглушки, чек-лист |
| `specs/.instructions/living-docs/service/validation-service.md` | Коды ошибок SVC001-SVC016, детекция режима заглушка/полный, скрипт validate-service.py |
| `specs/.instructions/living-docs/service/create-service.md` | Воркфлоу создания (7 шагов: PREPARE→REPORT) |
| `specs/.instructions/living-docs/service/modify-service.md` | Воркфлоу обновления |
| `specs/architecture/services/notification.md` | Текущая заглушка (для сравнения с новым примером) |
