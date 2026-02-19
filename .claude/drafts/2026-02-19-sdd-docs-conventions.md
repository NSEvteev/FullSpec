# docs/.system/conventions.md — конвенции API и shared-интерфейсы

Спецификация conventions.md: секции, шаблон, пример. Кросс-сервисные соглашения по формату ответов, ошибок, пагинации, авторизации + интерфейсы shared-пакетов.

## Контекст

**Задача:** Определить формат docs/.system/conventions.md — документа с кросс-сервисными конвенциями API и интерфейсами shared-пакетов.

**Источник:** `.claude/drafts/2026-02-19-sdd-chain-rethink.md` (строки 1150-~1580)

**Связанные файлы:**
- `2026-02-19-sdd-structure.md` — общая структура и решения
- `2026-02-19-sdd-docs-overview.md` — overview.md (архитектура vs конвенции: разделение ответственности)
- `2026-02-19-sdd-docs-technology.md` — standard-{tech}.md (per-tech конвенции, дополняют conventions.md)

---

## Содержание

Кросс-сервисные соглашения, которым следуют ВСЕ сервисы: формат ответов, ошибок, пагинации, авторизации. Плюс интерфейсы shared-пакетов — сигнатуры, параметры, примеры вызова.

Разделение: overview.md = архитектура (что система ДЕЛАЕТ), conventions.md = конвенции (как пишем код одинаково). Аналогично `.technologies/standard-{tech}.md` — конвенции конкретной технологии.

### Секции docs/.system/conventions.md

| # | Секция | Содержание | Зачем LLM-разработчику |
|---|--------|-----------|----------------------|
| 1 | **Формат ответов** | Стандартная обёртка response, формат успешных ответов | Возвращать ответы в едином формате во всех сервисах |
| 2 | **Формат ошибок** | Стандартная структура ошибки, коды, HTTP-статусы | Не изобретать свой формат ошибок в каждом endpoint |
| 3 | **Пагинация** | Формат request-параметров и response для списков | Одинаковая пагинация везде |
| 4 | **Аутентификация** | Формат Bearer-заголовка, структура JWT claims, middleware | Знать как авторизовать запрос в любом сервисе |
| 5 | **Версионирование API** | Схема версионирования, правила обратной совместимости | Знать в какой версии создавать новый endpoint |
| 6 | **Shared-пакеты** | Для каждого пакета: назначение, интерфейс (сигнатуры), примеры вызова | Использовать shared-код, а не дублировать |
| 7 | **Логирование** | Библиотека, уровни, обязательные поля, формат, что не логировать | Логировать единообразно во всех сервисах, не пропускать обязательные поля |

### Шаблон: docs/.system/conventions.md

`````markdown
# Конвенции API

## Формат ответов

Все API возвращают JSON. Успешные ответы:

**Единичный объект:**
```json
{ "{field}": "{value}", ... }
```

**Список с пагинацией:**
```json
{
  "items": [...],
  "total": "{int — общее количество}",
  "limit": "{int — запрошенный лимит}",
  "offset": "{int — смещение}"
}
```

## Формат ошибок

Все ошибки возвращаются в едином формате:

```json
{
  "error": {
    "code": "{SNAKE_UPPER — машинный код}",
    "message": "{человеко-читаемое описание}",
    "details": { "{доп. поля, зависят от ошибки}" }
  }
}
```

**Стандартные коды ошибок:**

| HTTP Status | Код | Когда |
|-------------|-----|-------|
| {status} | {CODE} | {описание} |

## Пагинация

Все списочные endpoint-ы принимают:

| Параметр | Тип | Default | Max | Описание |
|----------|-----|---------|-----|----------|
| limit | int | {N} | {M} | Количество записей |
| offset | int | 0 | — | Смещение |

Ответ всегда содержит `items`, `total`, `limit`, `offset`.

## Аутентификация

**Заголовок:** `Authorization: Bearer {JWT}`

**Структура JWT claims:**
```json
{
  "sub": "{user_id (UUID)}",
  "role": "{admin|manager|member}",
  "exp": "{Unix timestamp}",
  "iat": "{Unix timestamp}"
}
```

**Правило:** Все endpoint-ы требуют Bearer JWT, кроме: {список публичных endpoint-ов}.

## Версионирование API

{Схема: /api/v1/, /api/v2/...}

**Правила:**
- {правило обратной совместимости}
- {когда создавать новую версию}

## Shared-пакеты

### shared/{package} — {назначение}

**Владелец:** {svc}

**Интерфейс:**

```{lang}
{сигнатура функции / класса — что вызывать}
```

**Параметры:**

| Параметр | Тип | Описание |
|----------|-----|----------|
| {param} | {type} | {описание} |

**Возвращает:** {что возвращает, структура}

**Пример использования:**

```{lang}
{рабочий пример — готовый к копированию}
```

## Логирование

{Библиотека, базовая настройка. Все сервисы используют единый подход к логированию — структурированные JSON-логи с обязательными полями для трассировки.}

**Библиотека:** `{lib}` — {почему выбрана}

**Уровни:**

| Уровень | Когда использовать | Пример |
|---------|-------------------|--------|
| DEBUG | {описание} | {пример} |
| INFO | {описание} | {пример} |
| WARNING | {описание} | {пример} |
| ERROR | {описание} | {пример} |

**Обязательные поля:**

| Поле | Источник | Описание |
|------|---------|----------|
| {field} | {откуда берётся} | {зачем} |

**Запрещено логировать:** {PII, токены, пароли, ...}

**Базовый паттерн:**

```{lang}
{код — как создать логгер и использовать в handler/service}
```
`````

### Пример: docs/.system/conventions.md

`````markdown
# Конвенции API

## Формат ответов

Все API возвращают JSON. Content-Type: `application/json`.

**Единичный объект:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "system",
  "title": "Welcome",
  "status": "unread",
  "created_at": "2026-03-01T12:00:00Z"
}
```

**Список с пагинацией:**
```json
{
  "items": [ { "...": "..." } ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

**Даты:** ISO 8601 с timezone (`2026-03-01T12:00:00Z`). Хранение в TIMESTAMPTZ.

**UUID:** Строка в формате `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`. Генерация: `gen_random_uuid()` на стороне БД.

## Формат ошибок

Все ошибки возвращаются в едином формате:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Field 'email' is required",
    "details": {
      "field": "email",
      "constraint": "required"
    }
  }
}
```

**Стандартные коды ошибок:**

| HTTP Status | Код | Когда |
|-------------|-----|-------|
| 400 | `BAD_REQUEST` | Некорректный формат запроса |
| 401 | `UNAUTHORIZED` | Отсутствует или невалидный JWT |
| 403 | `FORBIDDEN` | Нет прав (роль не позволяет) |
| 404 | `NOT_FOUND` | Ресурс не найден |
| 409 | `CONFLICT` | Конфликт состояния (дубликат, race condition) |
| 422 | `VALIDATION_ERROR` | Валидация полей не прошла |
| 429 | `RATE_LIMITED` | Превышен лимит запросов |
| 500 | `INTERNAL_ERROR` | Необработанная ошибка сервера |

**Реализация в FastAPI:**
```python
from fastapi import HTTPException

class AppError(HTTPException):
    def __init__(self, status: int, code: str, message: str, details: dict = None):
        super().__init__(
            status_code=status,
            detail={"error": {"code": code, "message": message, "details": details or {}}}
        )

# Использование:
raise AppError(404, "NOT_FOUND", f"Notification {id} not found")
raise AppError(422, "VALIDATION_ERROR", "Invalid status", {"field": "status", "allowed": ["read", "unread"]})
```

## Пагинация

Все списочные endpoint-ы принимают:

| Параметр | Тип | Default | Max | Описание |
|----------|-----|---------|-----|----------|
| limit | int | 20 | 100 | Количество записей на страницу |
| offset | int | 0 | — | Смещение от начала |

Ответ всегда содержит `items`, `total`, `limit`, `offset`.

**Реализация:**
```python
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class PaginatedResponse(BaseModel):
    items: list
    total: int
    limit: int
    offset: int
```

## Аутентификация

**Заголовок:** `Authorization: Bearer {JWT}`

**Структура JWT claims:**
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "role": "member",
  "exp": 1740000000,
  "iat": 1739913600
}
```

- `sub` — user_id (UUID)
- `role` — одна из: `admin`, `manager`, `member`
- Время жизни: 24 часа (access token)

**Публичные endpoint-ы (без JWT):** `POST /auth/register`, `POST /auth/login`, `GET /health`.

Все остальные endpoint-ы требуют валидный JWT. Middleware shared/auth проверяет токен автоматически (см. Shared-пакеты).

## Версионирование API

Все endpoint-ы: `/api/v1/...`

**Правила:**
- Добавление нового поля в response — совместимо, не требует новой версии
- Удаление или переименование поля — несовместимо, требует v2
- Добавление опционального query-параметра — совместимо
- Изменение формата существующего поля — несовместимо

## Shared-пакеты

### shared/auth — JWT Middleware

**Владелец:** auth

**Интерфейс:**

```python
from shared.auth import require_auth, get_current_user, AuthUser

@app.get("/api/v1/notifications")
async def list_notifications(user: AuthUser = Depends(get_current_user)):
    # user.id — UUID пользователя
    # user.role — "admin" | "manager" | "member"
    ...
```

**AuthUser:**

| Поле | Тип | Описание |
|------|-----|----------|
| id | UUID | ID пользователя (из JWT sub) |
| role | str | Роль: `admin`, `manager`, `member` |

**Функции:**

| Функция | Назначение | Вызывает ошибку |
|---------|-----------|----------------|
| `get_current_user` | FastAPI Dependency — извлекает AuthUser из JWT | 401 если токен невалидный/отсутствует |
| `require_role(role)` | FastAPI Dependency — проверяет роль | 403 если роль не совпадает |

**Пример с проверкой роли:**
```python
from shared.auth import require_role

@app.delete("/api/v1/admin/users/{user_id}")
async def delete_user(user_id: UUID, admin: AuthUser = Depends(require_role("admin"))):
    ...
```

### shared/events — Схемы событий AMQP

**Владелец:** auth (Identity-события), task (Task-события)

**Интерфейс:**

```python
from shared.events import publish_event, UserRegistered, TaskCreated

# Публикация события:
await publish_event("system.events", UserRegistered(
    user_id="550e8400-...",
    email="user@example.com",
    name="John"
))
```

**Базовый класс:**

```python
class DomainEvent(TypedDict):
    event: str          # Имя события (auto из класса)
    timestamp: str      # ISO8601 (auto)
    source: str         # Имя сервиса (auto из config)
    data: dict          # Event-specific payload
```

**Доступные события:**

| Событие | Источник | Поля data |
|---------|---------|-----------|
| `UserRegistered` | auth | `user_id`, `email`, `name` |
| `PasswordChanged` | auth | `user_id` |
| `TaskCreated` | task | `task_id`, `creator_id`, `title` |
| `TaskAssigned` | task | `task_id`, `assignee_id`, `assigner_id` |
| `AdminAction` | admin | `action`, `target_user_id`, `admin_id` |

**Подписка на события:**
```python
from shared.events import subscribe, DomainEvent

@subscribe("system.events")
async def handle_event(event: DomainEvent):
    match event["event"]:
        case "UserRegistered":
            await create_welcome_notification(event["data"]["user_id"])
        case "TaskAssigned":
            await create_assignment_notification(event["data"])
```

## Логирование

Все сервисы используют structlog для структурированного логирования в JSON. Каждая log-запись автоматически обогащается контекстными полями (service, request_id), что позволяет трассировать запрос через цепочку сервисов в ELK.

**Библиотека:** `structlog 24.x` — структурированные логи в JSON, автоматический context binding, интеграция с stdlib logging.

**Уровни:**

| Уровень | Когда использовать | Пример |
|---------|-------------------|--------|
| DEBUG | Детали внутренней логики (не в production) | `Resolving notification template`, `Cache hit for user preferences` |
| INFO | Бизнес-события, успешные операции | `Notification sent`, `User registered`, `Task assigned` |
| WARNING | Восстановимые проблемы, degraded mode | `Redis unavailable, fallback to DB`, `Rate limit approaching` |
| ERROR | Сбои, требующие внимания | `Failed to send email`, `Database connection lost` |

**Обязательные поля:**

| Поле | Источник | Описание |
|------|---------|----------|
| `service` | Конфиг (auto) | Имя сервиса: `notification`, `auth`, `task` |
| `request_id` | Middleware (auto) | UUID запроса для трассировки через сервисы |
| `user_id` | Middleware (auto, если авторизован) | UUID пользователя из JWT |
| `timestamp` | structlog (auto) | ISO 8601 |
| `level` | structlog (auto) | DEBUG / INFO / WARNING / ERROR |

**Запрещено логировать:** пароли, JWT-токены (полные), email-адреса, номера телефонов, IP-адреса пользователей, любые PII-данные. Для отладки использовать ID (user_id, notification_id), не данные.

**Базовый паттерн:**

```python
import structlog

logger = structlog.get_logger()

# В handler / service:
async def send_notification(user_id: str, type: str):
    logger.info("notification.sending", user_id=user_id, type=type)
    try:
        result = await do_send(user_id, type)
        logger.info("notification.sent", user_id=user_id, notification_id=result.id)
    except DeliveryError as e:
        logger.error("notification.send_failed", user_id=user_id, type=type, error=str(e))
        raise
```

**Именование событий:** `{domain}.{action}` в snake_case — `notification.sent`, `user.registered`, `task.assigned`, `auth.login_failed`.
`````

---

## Аудит старых документов

| Старый документ | Что переиспользовать |
|-----------------|---------------------|
| `standard-specs.md` § 3.5 | Концепция shared-кода как не-сервиса (частично) |
