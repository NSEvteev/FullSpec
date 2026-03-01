---
description: auth — аутентификация пользователей, выдача JWT, хранение учётных записей, список пользователей для назначения исполнителей.
standard: specs/.instructions/docs/service/standard-service.md
criticality: critical-high
---

# auth

## Назначение

Сервис auth — единственный источник истины об учётных записях пользователей и JWT-токенах. Отвечает за регистрацию (seed-данные в v0.1.0, без публичной регистрации), логин с выдачей JWT, валидацию токенов для сервисов-потребителей и предоставление списка пользователей для назначения исполнителей задач. Хранит хэшированные пароли, не передаёт их другим сервисам. Основные потребители: frontend (REST — логин, список пользователей) и task-сервис (REST — валидация JWT через middleware). Взаимодействие через REST API.

**Обоснование критичности:** Уровень `critical-high` — при недоступности auth-сервиса весь функционал системы перестаёт работать: frontend не может аутентифицировать пользователей, task-сервис не может валидировать JWT ни на одном входящем запросе и возвращает 401 на все операции. Бизнес-остановка полная — ни один аутентифицированный пользователь не может работать с задачами. Обходных путей нет.

## API контракты

Сервис предоставляет 3 REST endpoint-а: публичный логин (`POST /login`), защищённая валидация токена для внутреннего потребления task-сервисом (`GET /validate`) и защищённый список пользователей для назначения исполнителей (`GET /users`). Все endpoint-ы следуют конвенциям из [conventions.md](../.system/conventions.md).

### POST /api/v1/auth/login

Аутентификация пользователя по email/password, выдача JWT-токена.

- **Auth:** нет (публичный endpoint)
- **Паттерн:** sync | **Протокол:** REST/JSON

**Request:**
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response 200:**
```json
{
  "token": "string (JWT)",
  "expiresIn": "number (секунды)",
  "user": {
    "id": "string (UUID)",
    "email": "string",
    "name": "string"
  }
}
```

**Errors:** 400 валидация (email или password отсутствуют), 401 неверные credentials

---

### GET /api/v1/auth/validate

Валидация JWT-токена — вызывается task-middleware при каждом входящем запросе к task-сервису (INT-3).

- **Auth:** Bearer JWT (обязателен)
- **Паттерн:** sync | **Протокол:** REST/JSON

**Response 200:**
```json
{
  "valid": true,
  "sub": "string (UUID пользователя)",
  "email": "string",
  "name": "string"
}
```

**Errors:** 401 невалидный или истёкший токен (`{ "valid": false, "error": "token expired" }`)

---

### GET /api/v1/auth/users

Список пользователей для назначения исполнителей задач.

- **Auth:** Bearer JWT (обязателен)
- **Паттерн:** sync | **Протокол:** REST/JSON

**Response 200:**
```json
{
  "users": [
    {
      "id": "string (UUID)",
      "email": "string",
      "name": "string"
    }
  ]
}
```

**Errors:** 401 невалидный или истёкший токен

## Data Model

Сервис использует PostgreSQL 16 как единственное хранилище. Хранит учётные записи пользователей с хэшированными паролями. Выбор PostgreSQL обоснован в Design (лучшая реляционная БД для данного домена, полная экосистема).

### users (PostgreSQL)

| Колонка | Тип | Constraints | Описание |
|---------|-----|------------|----------|
| id | UUID | PK, NOT NULL, DEFAULT gen_random_uuid() | Идентификатор пользователя |
| email | VARCHAR(255) | NOT NULL, UNIQUE | Email — уникальный идентификатор для логина |
| name | VARCHAR(100) | NOT NULL | Отображаемое имя пользователя |
| passwordHash | VARCHAR(255) | NOT NULL | Хэш пароля (bcrypt, cost=12) |
| createdAt | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Дата создания |

**Индексы:**
- `idx_users_email` — UNIQUE по email (быстрый lookup при логине)

## Потоки

Общий паттерн обработки в auth: запрос приходит через Express routes → router передаёт в controller → controller делегирует бизнес-логику в service → service взаимодействует с Prisma (PostgreSQL). JWT-операции инкапсулированы в отдельном `jwt.service.ts`. Чтобы добавить новый endpoint — создать route в `auth/routes/auth.ts`, обработчик в `auth/controllers/auth.controller.ts`, бизнес-логику в `auth/services/auth.service.ts`.

### Логин (REQ-9)

```
1. frontend → POST /api/v1/auth/login { email, password }
2. auth.routes/auth.ts → auth.controllers/auth.controller.ts: передача запроса
3. auth.controller: Zod-схема валидирует тело запроса
4. auth.controller → auth.services/auth.service.ts: вызов loginUser(email, password)
5. auth.service → Prisma: SELECT * FROM users WHERE email = ?
6. auth.service: bcrypt.compare(password, user.passwordHash)
7. auth.service → auth.services/jwt.service.ts: sign({ sub: user.id, iat, exp=1h })
8. auth.controller → frontend: 200 { token, expiresIn: 3600, user: { id, email, name } }
```

### Валидация JWT (вызов от task-middleware, INT-3)

```
1. task-middleware → GET /api/v1/auth/validate (Bearer JWT)
2. auth.routes/auth.ts → auth.controllers/auth.controller.ts: передача запроса
3. auth.controller → auth.services/jwt.service.ts: verify(token)
4. При валидном токене: jose верифицирует подпись HS256
5. auth.controller → task-middleware: 200 { valid: true, sub, email, name }
6. При невалидном/истёкшем: auth.controller → task-middleware: 401 { valid: false, error: "token expired" }
```

### Список пользователей

```
1. frontend → GET /api/v1/auth/users (Bearer JWT)
2. auth.routes/auth.ts → auth.controllers/auth.controller.ts: передача запроса
3. auth.controller → auth.services/jwt.service.ts: verify(token) (локальная валидация)
4. auth.controller → auth.services/auth.service.ts: getUsers()
5. auth.service → Prisma: SELECT id, email, name FROM users (без passwordHash)
6. auth.controller → frontend: 200 { users: [{ id, email, name }, ...] }
```

## Code Map

### Tech Stack

| Технология | Версия | Назначение | Стандарт |
|-----------|--------|-----------|---------|
| Node.js | 20 | Runtime | — |
| TypeScript | 5 | Типизация | — |
| Express | 4 | HTTP-фреймворк | — |
| Zod | 3 | Runtime-валидация схем | — |
| jose | 5 | JWT генерация и верификация | — |
| Prisma | 5 | ORM + миграции | — |
| PostgreSQL | 16 | Основная БД | — |
| bcrypt | 5 | Хэширование паролей | — |

### Пакеты

Сервис организован по слоям: routes → controllers → services → prisma. Каждый слой имеет одну ответственность: маршрутизация, обработка HTTP-запроса, бизнес-логика, доступ к данным.

| Пакет | Назначение | Ключевые модули |
|-------|-----------|----------------|
| `auth.routes` | Маршрутизация HTTP-запросов | `auth.ts` |
| `auth.controllers` | Обработчики запросов, HTTP input/output | `auth.controller.ts` |
| `auth.services` | Бизнес-логика: credentials, JWT | `auth.service.ts`, `jwt.service.ts` |
| `auth.schemas` | Zod-схемы для валидации запросов | `auth.schema.ts` |
| `auth.prisma` | Prisma-схема, миграции, seed | `schema.prisma`, `seed.ts` |

### Точки входа

- API: `src/auth/index.ts`
- Routes: `src/auth/routes/auth.ts`

### Внутренние зависимости

```
auth.routes → auth.controllers
auth.controllers → auth.services (auth.service, jwt.service)
auth.controllers → auth.schemas (Zod-валидация)
auth.services → auth.prisma (Prisma Client)
```

**Как добавить новый функционал:**
- Новый endpoint → добавить route в `src/auth/routes/auth.ts`, обработчик в `src/auth/controllers/auth.controller.ts`, логику в `src/auth/services/auth.service.ts`, Zod-схему в `src/auth/schemas/auth.schema.ts`
- Новое поле пользователя → обновить `src/auth/prisma/schema.prisma`, создать миграцию, обновить Zod-схемы и response-типы в controllers

### Makefile таргеты

| Таргет | Команда | Описание |
|--------|---------|----------|
| test | `make test-auth` | Unit + integration тесты сервиса |
| lint | `make lint-auth` | Линтинг кода сервиса |
| build | `make build-auth` | Сборка Docker-образа |
| seed | `make seed-auth` | Запуск seed-скрипта (тестовые пользователи) |

## Зависимости

Auth-сервис не зависит от других сервисов системы — является провайдером для frontend (INT-2) и task (INT-3). Зависимости только от инфраструктуры: PostgreSQL (критическая — без БД сервис не работает). Является листовым узлом в графе зависимостей сервисов.

### frontend — потребитель логина и списка пользователей (INT-2)
Auth предоставляет frontend публичный endpoint логина (`POST /api/v1/auth/login`) и защищённый endpoint списка пользователей (`GET /api/v1/auth/users`). Auth является провайдером — управляет контрактом, frontend следует ему.
Паттерн: **Published Language** (auth публикует стабильный REST-контракт; frontend конформен к нему).
См. [POST /api/v1/auth/login](#post-apiv1authlogin), [GET /api/v1/auth/users](#get-apiv1authusers).

### task — потребитель JWT-валидации (INT-3)
Auth предоставляет task внутренний endpoint валидации токена (`GET /api/v1/auth/validate`), который task-middleware вызывает при каждом входящем запросе. При недоступности auth — task возвращает 401 на все запросы.
Паттерн: **Published Language** (auth публикует стабильный контракт validate; task конформен к нему).
См. [GET /api/v1/auth/validate](#get-apiv1authvalidate).

## Доменная модель

Auth реализует домен Authentication & Identity. Основная сущность — User — проходит жизненный цикл: создание через seed (в v0.1.0) → активный (может логиниться и получать JWT). JwtToken — Value Object, инкапсулирует логику генерации/верификации токена с помощью jose.

### Агрегаты

| Агрегат | Описание |
|---------|----------|
| User | Учётная запись пользователя (id, email, name, passwordHash). Жизненный цикл: created → active. В v0.1.0 создаётся только через seed |
| JwtToken | Value Object: инкапсулирует генерацию и верификацию JWT. Claims: sub (userId), iat, exp (1h). Алгоритм: HS256 |

### Инварианты

- email пользователя уникален в системе
- passwordHash хранится только в виде bcrypt-хэша (cost=12), открытый пароль не хранится и не передаётся
- В v0.1.0 создание пользователей возможно только через seed-скрипт (нет публичной регистрации)
- JWT имеет время жизни 1 час (exp=1h), алгоритм HS256, секрет из env JWT_SECRET

### Доменные события

*Доменных событий нет.*

## Границы автономии LLM

- **Свободно:** реализация login-эндпоинта (routes, controller, service); Zod-схемы валидации (соответствуют § 2 API контракты); Prisma-схема и миграции (соответствуют § 3 Data Model); seed-данные (тестовые пользователи, хэш через bcrypt cost=12)
- **Флаг:** JWT — алгоритм HS256 и время жизни exp=1h строго фиксированы, секрет только из env JWT_SECRET; хэширование паролей — только bcrypt, cost не ниже 10
- **CONFLICT:** публичная регистрация пользователей (в v0.1.0 только seed — требует отдельный Discussion для v0.2+); refresh-токены (вне scope v0.1.0, требует отдельный Discussion); изменение API контрактов (§ 2), Data Model (§ 3), алгоритма JWT

## Planned Changes

<!-- chain: 0001-task-dashboard -->
Из Design 0001: ADDED `POST /api/v1/auth/login` — аутентификация, выдача JWT; ADDED `GET /api/v1/auth/validate` — валидация JWT для task-middleware (INT-3); ADDED `GET /api/v1/auth/users` — список пользователей для назначения исполнителей (INT-2); ADDED таблица `users` (PostgreSQL); ADDED потоки «Логин», «Валидация JWT», «Список пользователей»; ADDED агрегаты `User`, `JwtToken`; ADDED структура `src/auth/`.
<!-- /chain: 0001-task-dashboard -->

## Changelog

- **Создание сервиса** | DONE 2026-03-01 — первоначальная документация на основе Design 0001-task-dashboard SVC-2.
