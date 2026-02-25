---
description: Per-tech стандарты контрактных технологий (OpenAPI, Protobuf, AsyncAPI) + обновление shared/ README. Фаза 0 шаблона.
type: feature
status: draft
created: 2026-02-24
---

# Shared contracts — per-tech стандарты контрактных технологий

Per-tech стандарты кодирования для OpenAPI, Protobuf и AsyncAPI в `docs/.technologies/`. Часть шаблона проекта (Фаза 0), создаются при инициализации. Обновление README в `shared/` папках.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблема](#1-проблема)
  - [2. Решение — per-tech стандарты](#2-решение--per-tech-стандарты)
  - [3. standard-openapi.md](#3-standard-openapimd)
  - [4. standard-protobuf.md](#4-standard-protobufmd)
  - [5. standard-asyncapi.md](#5-standard-asyncapimd)
  - [6. Обновление shared/ README](#6-обновление-shared-readme)
  - [7. Интеграция в процесс](#7-интеграция-в-процесс)
  - [8. Изменения в стандартах](#8-изменения-в-стандартах)
- [Решения](#решения)
- [Закрытые вопросы](#закрытые-вопросы)
- [Задачи](#задачи)

---

## Контекст

**Задача:** Закрыть пробел "кодовый уровень" для shared/contracts/ и shared/events/
**Почему создан:** Исследование покрытия показало: аналитический (Design INT-N) и документационный (docs/) контуры покрывают контракты полностью. Но dev-agent, получив TASK-N "создать OpenAPI-контракт", не имеет стандарта: как назвать файл, какая структура спецификации, какие правила. Это тот же пробел, что "PostgreSQL без standard-postgresql.md" — технология используется, но конвенции не описаны.
**Связанные файлы:**
- `specs/.instructions/analysis/standard-analysis.md` § 3.4 — правила shared/
- `specs/.instructions/docs/standard-docs.md` § 4 — типы документов (per-tech стандарт)
- `specs/.instructions/docs/technology/standard-technology.md` — стандарт per-tech документа (8 секций)
- `specs/docs/.technologies/` — расположение per-tech стандартов
- `shared/contracts/openapi/` — REST контракты
- `shared/contracts/protobuf/` — gRPC контракты
- `shared/events/` — схемы событий
- `.claude/drafts/2026-02-24-conflict-detect.md` — dev-agent, INFRA-блок (wave 0)

**Предшественник:** Этот черновик заменяет исследование "shared-contracts — исследование покрытия". Исследование выполнено, выводы зафиксированы в секции "Закрытые вопросы".

---

## Содержание

### 1. Проблема

Путь dev-agent при задаче "Создать OpenAPI-контракт для auth":

| Шаг | Источник | Что узнаёт | Статус |
|-----|----------|-----------|--------|
| 1 | plan-dev.md TASK-N | **Что** сделать (создать файл в shared/contracts/) | Есть |
| 2 | design.md INT-N | **Содержание** контракта (endpoints, request/response) | Есть |
| 3 | design.md SVC-N § 2 | Дельта ADDED для shared/ | Есть |
| 4 | conventions.md § 5 | Версионирование API | Есть |
| 5 | conventions.md § 6 | Shared-интерфейсы (runtime) | Есть |
| 6 | ??? | **Формат файла** (структура OpenAPI yaml, naming, layout) | **НЕТ** |

Агент знает *что* положить в контракт, но не знает *как оформить файл*. Аналогичная ситуация для Protobuf и AsyncAPI (события).

**Текущее состояние shared/:**

| Файл | Содержание |
|------|-----------|
| `shared/.instructions/README.md` | Индекс — все секции пустые |
| `shared/contracts/README.md` | Одна строка: `openapi/*.yaml, protobuf/*.proto → Код handlers` |
| `shared/contracts/openapi/README.md` | Одна строка: `auth.yaml, users.yaml → gRPC` |
| `shared/contracts/protobuf/README.md` | Одна строка: `auth.proto, users.proto → REST` |
| `shared/events/README.md` | Одна строка: `user.created.json, order.placed.json → Код publishers` |

### 2. Решение — per-tech стандарты

Создать 3 per-tech стандарта в `docs/.technologies/`, по аналогии с `standard-postgresql.md` и `standard-redis.md`. Каждый следует формату из `standard-technology.md` (8 секций). Стандарты — часть шаблона проекта, создаются при init (Фаза 0), не при analysis chain.

**Что входит в шаблон (универсальное):**

| Стандарт | Файл | Что покрывает |
|----------|------|--------------|
| OpenAPI | `standard-openapi.md` | REST контракты: структура yaml, именование, версионирование файлов, валидация (spectral) |
| Protobuf | `standard-protobuf.md` | gRPC контракты: структура .proto, именование, package convention, валидация (buf) |
| AsyncAPI | `standard-asyncapi.md` | Event schemas: структура yaml, именование каналов, payload schema, валидация |

**Что НЕ входит (project-specific, определяется при Design):**

- Конкретные endpoints (→ INT-N)
- Конкретные events (→ INT-N async)
- Конкретные сервисы (→ SVC-N)
- Runtime-интерфейсы shared-пакетов (→ conventions.md § 6)

**Почему шаблон, а не analysis chain:**

Naming conventions для OpenAPI/Protobuf/AsyncAPI универсальны — они не зависят от конкретного проекта. Имя файла `{svc}.yaml`, layout `info → paths → components`, правила Protobuf `package {domain}.{svc}.v1` — одинаковы для любого микросервисного проекта. Создавать их через `/technology-create` при каждой первой цепочке — избыточно.

### 3. standard-openapi.md

Расположение: `docs/.technologies/standard-openapi.md`

**§ 1 Версия и настройка:**
- OpenAPI Specification 3.1.0
- YAML формат (не JSON — лучше diff, комментарии)
- Линтер: Spectral (Stoplight)
- Конфигурация: `.spectral.yaml` в корне проекта

**§ 2 Именование:**

| Элемент | Правило | Пример |
|---------|---------|--------|
| Файл | `{svc}.yaml` — совпадает с `docs/{svc}.md` | `auth.yaml`, `gateway.yaml` |
| Расположение | `shared/contracts/openapi/` | `shared/contracts/openapi/auth.yaml` |
| Версионирование | Поле `info.version` в файле. Единый файл, без v1/ v2/ поддиректорий. Версия API — в `servers[].url` (`/api/v1/`) | `info.version: 1.2.0` |
| operationId | `{verb}{Resource}` (camelCase) | `createUser`, `getTokenInfo` |
| Схемы (components) | PascalCase | `UserProfile`, `TokenRequest` |
| Теги | kebab-case, по доменным группам | `auth`, `user-management` |

**§ 3 Паттерны кода (структура файла):**

```yaml
openapi: "3.1.0"
info:
  title: "{Service} API"
  description: "REST API контракты для {service}-сервиса"
  version: "1.0.0"
  contact:
    name: "{service} team"

servers:
  - url: /api/v1
    description: Current version

paths:
  /auth/token:
    post:
      operationId: createToken
      tags: [auth]
      summary: "Получение JWT-токена"
      # ... request/response из Design INT-N

components:
  schemas:
    TokenRequest:
      type: object
      required: [grant_type]
      properties:
        grant_type:
          type: string
          enum: [password, refresh_token, device_code]
    # ... schemas из Design SVC-N § 3 Data Model

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

Правила:
- Один файл на сервис (совпадает с `docs/{svc}.md`)
- Секция `paths` — endpoints из `docs/{svc}.md` § 2
- Секция `components/schemas` — Data Model из `docs/{svc}.md` § 3
- `$ref` для переиспользования schemas внутри файла
- Кросс-сервисные ссылки: **не использовать** `$ref` между файлами — каждый файл самодостаточный (провайдер владеет контрактом)

**§ 4 Анти-паттерны:**

| Анти-паттерн | Почему | Правильно |
|-------------|--------|-----------|
| `$ref` на файл другого сервиса | Дублирование ownership, нарушает "провайдер владеет" | Каждый файл самодостаточный |
| Версии в имени файла (`auth-v1.yaml`, `auth-v2.yaml`) | Дублирование — версия уже в `info.version` и `servers[].url` | Единый `auth.yaml` |
| JSON формат | Плохой diff, нет комментариев | YAML |
| `additionalProperties: true` по умолчанию | Слабая валидация | Явно `additionalProperties: false` |
| Inline schemas вместо $ref | Дублирование schemas внутри файла | `$ref: '#/components/schemas/...'` |

**§ 5 Структура файлов:**

```
shared/contracts/openapi/
├── auth.yaml          # OpenAPI spec для auth-сервиса
├── gateway.yaml       # OpenAPI spec для gateway-сервиса
├── users.yaml         # OpenAPI spec для users-сервиса
└── README.md          # Конвенции и навигация
```

**§ 6 Валидация:**
- Линтер: `spectral lint shared/contracts/openapi/{svc}.yaml`
- Pre-commit hook: `openapi-lint` — запускает spectral для изменённых .yaml в `shared/contracts/openapi/`
- Конфигурация: `.spectral.yaml` — набор правил (oas3-valid-schema, operation-operationId, info-contact и т.д.)

**§ 7 Тестирование:**
- Contract testing (опционально): Schemathesis — автоматическая генерация тестов из OpenAPI spec
- Команда: `make test-contracts-openapi` (если включён)
- Валидация response schemas: middleware FastAPI проверяет, что response соответствует OpenAPI spec

**§ 8 Связь с SDD процессом:**

| Момент SDD | Действие с OpenAPI |
|------------|-------------------|
| Design (INT-N sync REST) | Определяет содержание контракта в markdown |
| INFRA-блок (wave 0) | Dev-agent создаёт/обновляет `{svc}.yaml` по INT-N |
| Per-service блок | Dev-agent реализует handlers, валидирует против spec |
| Design → DONE | `{svc}.yaml` — финальная версия, `info.version` обновлён |
| CONFLICT (shared/) | Изменение `{svc}.yaml` = CONFLICT уровня Design |

### 4. standard-protobuf.md

Расположение: `docs/.technologies/standard-protobuf.md`

**§ 1 Версия и настройка:**
- Protocol Buffers v3 (proto3)
- Линтер и валидация: buf (buf.build)
- Конфигурация: `buf.yaml` в `shared/contracts/protobuf/`

**§ 2 Именование:**

| Элемент | Правило | Пример |
|---------|---------|--------|
| Файл | `{svc}.proto` — совпадает с `docs/{svc}.md` | `auth.proto`, `users.proto` |
| Расположение | `shared/contracts/protobuf/` | `shared/contracts/protobuf/auth.proto` |
| Package | `{project}.{svc}.v{N}` | `myapp.auth.v1` |
| Service | PascalCase + `Service` суффикс | `AuthService` |
| RPC | PascalCase, verb + noun | `CreateToken`, `ValidateToken` |
| Message | PascalCase | `TokenRequest`, `TokenResponse` |
| Field | snake_case | `user_id`, `grant_type` |
| Enum | PascalCase, значения UPPER_SNAKE_CASE с префиксом | `GrantType`, `GRANT_TYPE_PASSWORD` |

**§ 3 Паттерны кода (структура файла):**

```protobuf
syntax = "proto3";

package myapp.auth.v1;

option go_package = "myapp/gen/auth/v1;authv1";
option java_package = "com.myapp.auth.v1";

// Сервис аутентификации — управление JWT-токенами.
service AuthService {
  // Создание JWT-токена по credentials.
  rpc CreateToken(CreateTokenRequest) returns (CreateTokenResponse);

  // Валидация существующего JWT-токена.
  rpc ValidateToken(ValidateTokenRequest) returns (ValidateTokenResponse);
}

message CreateTokenRequest {
  string grant_type = 1;  // password | refresh_token | device_code
  string username = 2;
  string password = 3;
}

message CreateTokenResponse {
  string access_token = 1;
  string refresh_token = 2;
  int32 expires_in = 3;
}
```

Правила:
- Один файл на сервис (совпадает с OpenAPI подходом)
- Package = версионированный namespace (`v1`)
- Каждый RPC — пара Request/Response messages (не reuse)
- Field numbers: не переиспользовать удалённые (reserved)
- Комментарии: doc-comments (`//`) перед service, rpc, message

**§ 4 Анти-паттерны:**

| Анти-паттерн | Почему | Правильно |
|-------------|--------|-----------|
| `import` из другого сервиса | Нарушает "провайдер владеет" | Каждый .proto самодостаточный |
| Reuse Request/Response между RPC | Coupling, breaking changes | Отдельная пара на каждый RPC |
| Field number reuse после удаления | Wire format incompatibility | `reserved 4, 5;` |
| `google.protobuf.Any` | Потеря type safety | Явные типы или `oneof` |

**§ 5 Структура файлов:**

```
shared/contracts/protobuf/
├── buf.yaml           # Конфигурация buf
├── buf.gen.yaml       # Генерация кода (если применимо)
├── auth.proto         # gRPC контракт для auth-сервиса
├── users.proto        # gRPC контракт для users-сервиса
└── README.md          # Конвенции и навигация
```

**§ 6 Валидация:**
- Линтер: `buf lint shared/contracts/protobuf/`
- Breaking change detection: `buf breaking shared/contracts/protobuf/ --against .git#branch=main`
- Pre-commit hook: `protobuf-lint` — запускает buf lint для изменённых .proto

**§ 7 Тестирование:**
- buf breaking — автоматическая проверка обратной совместимости
- Генерация кода: `buf generate` (если настроена кодогенерация)

**§ 8 Связь с SDD процессом:**

| Момент SDD | Действие с Protobuf |
|------------|-------------------|
| Design (INT-N sync gRPC) | Определяет RPC, messages в markdown |
| INFRA-блок (wave 0) | Dev-agent создаёт/обновляет `{svc}.proto` по INT-N |
| Per-service блок | Dev-agent реализует gRPC server/client |
| Design → DONE | `{svc}.proto` — финальная версия |
| CONFLICT (shared/) | Изменение `{svc}.proto` = CONFLICT уровня Design |

### 5. standard-asyncapi.md

Расположение: `docs/.technologies/standard-asyncapi.md`

**§ 1 Версия и настройка:**
- AsyncAPI Specification 3.0
- YAML формат
- Линтер: AsyncAPI CLI (`asyncapi validate`)
- Конфигурация: `.asyncapi-cli` (если нужна)

**§ 2 Именование:**

| Элемент | Правило | Пример |
|---------|---------|--------|
| Файл | `{domain-event-group}.yaml` — по доменной группе | `auth-events.yaml`, `order-events.yaml` |
| Расположение | `shared/events/` | `shared/events/auth-events.yaml` |
| Channel | `{domain}.{event}` (dot-separated) | `auth.token.created`, `order.placed` |
| Message | PascalCase + `Event` суффикс | `TokenCreatedEvent`, `OrderPlacedEvent` |
| Schema | PascalCase | `TokenCreatedPayload` |

**§ 3 Паттерны кода (структура файла):**

```yaml
asyncapi: "3.0.0"
info:
  title: "Auth Events"
  description: "Асинхронные события сервиса аутентификации"
  version: "1.0.0"

servers:
  rabbitmq:
    host: "rabbitmq:5672"
    protocol: amqp

channels:
  auth.token.created:
    address: auth.token.created
    messages:
      TokenCreatedEvent:
        $ref: '#/components/messages/TokenCreatedEvent'

  auth.user.logged_in:
    address: auth.user.logged_in
    messages:
      UserLoggedInEvent:
        $ref: '#/components/messages/UserLoggedInEvent'

operations:
  publishTokenCreated:
    action: send
    channel:
      $ref: '#/channels/auth.token.created'

components:
  messages:
    TokenCreatedEvent:
      payload:
        $ref: '#/components/schemas/TokenCreatedPayload'

  schemas:
    TokenCreatedPayload:
      type: object
      required: [event_type, user_id, timestamp]
      properties:
        event_type:
          type: string
          const: "auth.token.created"
        user_id:
          type: string
          format: uuid
        timestamp:
          type: string
          format: date-time
        metadata:
          type: object
          properties:
            ip_address:
              type: string
            user_agent:
              type: string
```

Правила:
- Один файл на доменную группу (не на event — группировка по домену)
- Каждый message — `$ref` на schema в `components/`
- Payload schemas — JSON Schema (машинно-валидируемые, не TypedDict)
- Обязательные поля payload: `event_type`, `timestamp` (+ domain-specific)
- `event_type` = channel address (SSOT)

**§ 4 Анти-паттерны:**

| Анти-паттерн | Почему | Правильно |
|-------------|--------|-----------|
| TypedDict вместо JSON Schema | Не машинно-валидируемые | JSON Schema в AsyncAPI |
| Один файл на event | Избыточная гранулярность | Группировка по домену |
| Inline schemas | Дублирование | `$ref: '#/components/schemas/...'` |
| Отсутствие `event_type` в payload | Consumer не может маршрутизировать | Обязательное поле |

**§ 5 Структура файлов:**

```
shared/events/
├── auth-events.yaml       # AsyncAPI spec для auth-событий
├── order-events.yaml      # AsyncAPI spec для order-событий
├── notification-events.yaml # AsyncAPI spec для notification-событий
└── README.md              # Конвенции и навигация
```

**§ 6 Валидация:**
- Линтер: `asyncapi validate shared/events/{group}.yaml`
- Pre-commit hook: `asyncapi-lint` — запускает валидацию для изменённых .yaml в `shared/events/`

**§ 7 Тестирование:**
- Schema validation при publish: runtime проверка payload против AsyncAPI schema
- Consumer compatibility: "старый" consumer обрабатывает "новое" событие (backward compatible)

**§ 8 Связь с SDD процессом:**

| Момент SDD | Действие с AsyncAPI |
|------------|-------------------|
| Design (INT-N async events) | Определяет events, payload в markdown |
| INFRA-блок (wave 0) | Dev-agent создаёт/обновляет `{group}.yaml` по INT-N |
| Per-service блок | Dev-agent реализует publisher/subscriber |
| Design → DONE | `{group}.yaml` — финальная версия |
| CONFLICT (shared/) | Изменение schema = CONFLICT уровня Design |

### 6. Обновление shared/ README

README в shared/ папках обновляются для ссылки на per-tech стандарты. README остаются краткими (навигация), детали — в стандартах.

**shared/contracts/README.md:**

```markdown
# shared/contracts/

Контракты API между сервисами. Файлы создаются dev-agent в INFRA-блоке (wave 0) по Design INT-N.

| Папка | Технология | Стандарт |
|-------|-----------|----------|
| `openapi/` | OpenAPI 3.1 (REST) | [standard-openapi.md](/specs/docs/.technologies/standard-openapi.md) |
| `protobuf/` | Protobuf v3 (gRPC) | [standard-protobuf.md](/specs/docs/.technologies/standard-protobuf.md) |

**Владение:** Провайдер сервиса владеет контрактом (standard-analysis.md § 3.4).
**Именование:** `{svc}.yaml` / `{svc}.proto` — совпадает с `docs/{svc}.md`.
```

**shared/contracts/openapi/README.md:**

```markdown
# shared/contracts/openapi/

REST контракты в формате OpenAPI 3.1. Один файл на сервис.

**Стандарт:** [standard-openapi.md](/specs/docs/.technologies/standard-openapi.md)
**Валидация:** `spectral lint {file}.yaml`
```

**shared/contracts/protobuf/README.md:**

```markdown
# shared/contracts/protobuf/

gRPC контракты в формате Protobuf v3. Один файл на сервис.

**Стандарт:** [standard-protobuf.md](/specs/docs/.technologies/standard-protobuf.md)
**Валидация:** `buf lint`
```

**shared/events/README.md:**

```markdown
# shared/events/

Схемы событий в формате AsyncAPI 3.0. Один файл на доменную группу.

**Стандарт:** [standard-asyncapi.md](/specs/docs/.technologies/standard-asyncapi.md)
**Валидация:** `asyncapi validate {file}.yaml`
```

### 7. Интеграция в процесс

**Где в SDD процессе dev-agent создаёт контрактные файлы:**

```
Design INT-N (markdown)
    ↓ содержание контракта
Plan Dev TASK-N (INFRA-блок, wave 0)
    ↓ задача "создать/обновить контракт"
Dev-agent читает:
    - INT-N → endpoints, messages, schemas
    - standard-openapi.md → формат файла, naming
    - standard-protobuf.md → формат файла, naming
    - standard-asyncapi.md → формат файла, naming
    ↓
Создаёт файлы в shared/contracts/ и shared/events/
    ↓
Per-service блоки (wave 1+)
    - Dev-agent реализует handlers/publishers
    - Валидирует код против spec (опционально)
```

**Что это меняет в процессе:** Ничего. Цепочка Design → TASK-N → код уже существует (standard-analysis.md § 3.4). Per-tech стандарты только отвечают на вопрос "в каком формате", который раньше был неявным.

**Как dev-agent узнаёт про per-tech стандарт:**

Через `docs/{svc}.md` § 5 Code Map → Tech Stack → ссылка на `standard-openapi.md`. Аналогично тому, как сейчас ссылается на `standard-postgresql.md`. Dev-agent при старте блока читает service doc → видит технологии → читает стандарты.

Дополнительно: INFRA-блок не привязан к конкретному сервису, но main LLM при запуске передаёт в контексте `conventions.md` (обязательный, добавлен в conflict-detect § 5.1) — оттуда агент берёт кросс-сервисные конвенции.

### 8. Изменения в стандартах

#### 8.1 standard-docs.md § 7 — стартовый набор

| Секция | Изменение |
|--------|-----------|
| § 7 "Минимальный стартовый набор" → "Примеры" | Добавить в таблицу примеров 3 строки: `standard-openapi.md`, `standard-protobuf.md`, `standard-asyncapi.md` — часть шаблона при init |

#### 8.2 docs/.technologies/README.md — реестр

| Секция | Изменение |
|--------|-----------|
| Таблица реестра | Добавить 3 строки: openapi, protobuf, asyncapi с пометкой "Шаблон (Фаза 0)" в колонке "Сервисы" |

#### 8.3 shared/ README файлы

| Файл | Изменение |
|------|-----------|
| `shared/contracts/README.md` | Заменить одну строку на навигационный README (§ 6) |
| `shared/contracts/openapi/README.md` | Заменить одну строку на ссылку на стандарт (§ 6) |
| `shared/contracts/protobuf/README.md` | Заменить одну строку на ссылку на стандарт (§ 6) |
| `shared/events/README.md` | Заменить одну строку на ссылку на стандарт (§ 6) |

#### 8.4 standard-process.md § 10 — закрытие

| Секция | Изменение |
|--------|-----------|
| § 10 | Нет отдельного пробела для shared-contracts (это не G-пробел). Если нужно — добавить запись "shared-contracts: Закрыт — per-tech стандарты standard-openapi/protobuf/asyncapi.md" |

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| R1 | Per-tech стандарты, не standard-shared.md | shared/ — не технология, это папка. OpenAPI, Protobuf, AsyncAPI — технологии. Стандарт описывает технологию, не папку |
| R2 | Часть шаблона (Фаза 0), не analysis chain | Naming conventions OpenAPI/Protobuf/AsyncAPI универсальны, не project-specific. Создавать через `/technology-create` при каждом первом Design — избыточно |
| R3 | Один файл на сервис (OpenAPI, Protobuf) | Совпадает с принципом "один сервис — один файл" (`docs/{svc}.md`). Провайдер владеет файлом |
| R4 | Один файл на доменную группу (AsyncAPI) | Events группируются по домену, не по сервису. `auth-events.yaml` содержит все события auth-домена |
| R5 | YAML, не JSON | Лучший diff, поддержка комментариев, единый формат для всех трёх технологий |
| R6 | Версия в `info.version`, не в имени файла | Одна точка правды. Нет дублирования `auth-v1.yaml` / `auth-v2.yaml`. Версия API — в URL path (`/api/v1/`), не в файле |
| R7 | Каждый файл самодостаточный (нет cross-file $ref) | Принцип "провайдер владеет контрактом". Потребитель ссылается, не импортирует |
| R8 | JSON Schema для events (не TypedDict) | Машинно-валидируемые, language-agnostic, совместимы с AsyncAPI. TypedDict — Python-specific runtime |
| R9 | Pre-commit hooks для линтинга | spectral (OpenAPI), buf lint (Protobuf), asyncapi validate (AsyncAPI). Валидация при каждом коммите |
| R10 | Не создаём скилл `/contract-create` | Dev-agent создаёт файлы по стандарту как часть TASK-N. Отдельный скилл — лишняя абстракция |

---

## Закрытые вопросы

### Q1. Нужен ли standard-shared.md?

**Ответ: нет.** `shared/` — папка в структуре проекта, не технология и не сервис. Конвенции файлов определяются per-tech стандартами (OpenAPI, Protobuf, AsyncAPI). Правила владения и зависимостей — в `standard-analysis.md` § 3.4. Описание shared-пакетов — в `conventions.md` § 6. Отдельный стандарт создал бы дублирование.

→ R1

### Q2. Code-first или spec-first?

**Ответ: spec-first внутри SDD.** В SDD подходе спецификация (Design INT-N) определяет контракт до кода. Dev-agent **сначала** создаёт файл в `shared/contracts/` (INFRA-блок, wave 0), **затем** реализует код в `src/{svc}/` (per-service блок, wave 1+). Это spec-first в рамках процесса, даже если FastAPI потом генерирует OpenAPI из декораторов — файл в shared/ первичен как контракт.

### Q3. Аналитический и документационный уровни — есть ли пробелы?

**Ответ: нет.** Исследование покрытия показало: Design INT-N полностью покрывает определение контрактов. docs/ ({svc}.md § 2, conventions.md § 6, overview.md § 6) покрывают документирование. design-reviewer проверяет качество. Пробел — только кодовый уровень (формат файлов).

### Q4. Events: JSON Schema или TypedDict?

**Ответ: JSON Schema в AsyncAPI-файлах.** TypedDict — Python-specific runtime-определение, описанное в conventions.md. JSON Schema в `shared/events/` — машинно-валидируемое, language-agnostic определение. Оба сосуществуют: AsyncAPI (schema) — контракт, TypedDict (Python) — реализация. Связь: TypedDict в коде ДОЛЖЕН соответствовать schema из AsyncAPI.

### Q5. Нужен ли скилл `/contract-create`?

**Ответ: нет.** Создание контрактных файлов — часть TASK-N в INFRA-блоке. Dev-agent читает INT-N (содержание) + standard-{tech}.md (формат) и создаёт файл. Отдельный скилл создал бы параллельный path мимо analysis chain.

→ R10

---

## Задачи

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Создать standard-openapi.md
  description: >
    Драфт: .claude/drafts/2026-02-24-shared-contracts.md (секция "§ 3")
    /technology-create для docs/.technologies/standard-openapi.md.
    8 секций по standard-technology.md: версия (OpenAPI 3.1, YAML, spectral),
    именование ({svc}.yaml, operationId camelCase, schemas PascalCase),
    паттерны (структура файла — info → paths → components),
    анти-паттерны (cross-file $ref, JSON формат, additionalProperties: true),
    структура файлов (shared/contracts/openapi/),
    валидация (spectral lint, pre-commit hook openapi-lint),
    тестирование (Schemathesis опционально),
    связь с SDD (Design INT-N → INFRA-блок → per-service).
  activeForm: Создаю standard-openapi.md

TASK 2: Создать standard-protobuf.md
  description: >
    Драфт: .claude/drafts/2026-02-24-shared-contracts.md (секция "§ 4")
    /technology-create для docs/.technologies/standard-protobuf.md.
    8 секций: версия (proto3, buf), именование ({svc}.proto, package {project}.{svc}.v{N},
    PascalCase services/messages, snake_case fields),
    паттерны (структура файла — syntax → package → service → messages),
    анти-паттерны (cross-file import, field number reuse, google.protobuf.Any),
    структура файлов (shared/contracts/protobuf/ + buf.yaml),
    валидация (buf lint, buf breaking, pre-commit hook protobuf-lint),
    тестирование (buf breaking against main),
    связь с SDD.
  activeForm: Создаю standard-protobuf.md

TASK 3: Создать standard-asyncapi.md
  description: >
    Драфт: .claude/drafts/2026-02-24-shared-contracts.md (секция "§ 5")
    /technology-create для docs/.technologies/standard-asyncapi.md.
    8 секций: версия (AsyncAPI 3.0, YAML, asyncapi CLI),
    именование ({domain-event-group}.yaml, channels dot-separated, messages PascalCase+Event),
    паттерны (структура файла — info → servers → channels → operations → components,
    payload JSON Schema, обязательные поля event_type/timestamp),
    анти-паттерны (TypedDict вместо JSON Schema, один файл на event, inline schemas),
    структура файлов (shared/events/),
    валидация (asyncapi validate, pre-commit hook asyncapi-lint),
    тестирование (schema validation при publish),
    связь с SDD.
  activeForm: Создаю standard-asyncapi.md

TASK 4: Обновить shared/ README файлы
  blockedBy: [1, 2, 3]
  description: >
    Драфт: .claude/drafts/2026-02-24-shared-contracts.md (секция "§ 6")
    Обновить 4 README файла:
    - shared/contracts/README.md — навигационный с таблицей (папка, технология, стандарт)
    - shared/contracts/openapi/README.md — ссылка на standard-openapi.md, валидация
    - shared/contracts/protobuf/README.md — ссылка на standard-protobuf.md, валидация
    - shared/events/README.md — ссылка на standard-asyncapi.md, валидация
    Использовать /structure-modify для каждого README (правило из core.md).
  activeForm: Обновляю shared/ README файлы

TASK 5: Обновить docs/.technologies/README.md — реестр
  blockedBy: [1, 2, 3]
  description: >
    Драфт: .claude/drafts/2026-02-24-shared-contracts.md (секция "§ 8.2")
    Добавить 3 строки в таблицу реестра docs/.technologies/README.md:
    - openapi | standard-openapi.md | Шаблон (Фаза 0)
    - protobuf | standard-protobuf.md | Шаблон (Фаза 0)
    - asyncapi | standard-asyncapi.md | Шаблон (Фаза 0)
  activeForm: Обновляю реестр технологий

TASK 6: Обновить standard-docs.md § 7 — стартовый набор
  blockedBy: [1, 2, 3]
  description: >
    Драфт: .claude/drafts/2026-02-24-shared-contracts.md (секция "§ 8.1")
    Обновить specs/.instructions/docs/standard-docs.md:
    - § 7 "Минимальный стартовый набор" → таблица "Примеры": добавить 3 строки
      standard-openapi.md, standard-protobuf.md, standard-asyncapi.md
      с пометкой "Часть шаблона, создаётся при init"
  activeForm: Обновляю standard-docs.md

TASK 7: Миграция standard-docs.md
  blockedBy: [6]
  description: >
    /migration-create для standard-docs.md.
    Синхронизировать зависимые файлы (validation-docs.md и др.).
  activeForm: Мигрирую зависимости standard-docs.md

TASK 8: Валидация миграции
  blockedBy: [7]
  description: >
    /migration-validate для standard-docs.md.
    Убедиться что все зависимые файлы синхронизированы.
  activeForm: Валидирую миграцию

TASK 9: Обновить CLAUDE.md
  blockedBy: [5]
  description: >
    В CLAUDE.md отметить shared-contracts как выполненный:
    - Изменить строку shared-contracts — статус "ГОТОВ К РЕАЛИЗАЦИИ" с описанием
      (3 per-tech стандарта + shared/ README, N задач)
  activeForm: Обновляю CLAUDE.md
```
