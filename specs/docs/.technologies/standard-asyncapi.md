---
description: Стандарт кодирования AsyncAPI — конвенции именования, структура event-спецификаций, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: asyncapi
---

# Стандарт AsyncAPI v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | AsyncAPI Specification 3.0 |
| Ключевые библиотеки | AsyncAPI CLI 1.x |
| Линтер | AsyncAPI CLI (`asyncapi validate`) |
| Конфигурация | `.asyncapi-cli` (если нужна кастомизация правил) |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| Файл | `{domain-event-group}.yaml` — по доменной группе | `auth-events.yaml`, `order-events.yaml` |
| Расположение | `shared/events/` | `shared/events/auth-events.yaml` |
| Channel | `{domain}.{subdomain}.{event}` (dot-separated) | `auth.token.created`, `order.placed` |
| Message | PascalCase + `Event` суффикс | `TokenCreatedEvent`, `OrderPlacedEvent` |
| Schema | PascalCase + `Payload` суффикс | `TokenCreatedPayload`, `OrderPlacedPayload` |

## Паттерны кода

### Структура файла

Один файл содержит все события одной доменной группы. Каждый message ссылается на schema через `$ref`. Schemas объявляются в `components/schemas`.

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

  publishUserLoggedIn:
    action: send
    channel:
      $ref: '#/channels/auth.user.logged_in'

  onTokenCreated:
    action: receive
    channel:
      $ref: '#/channels/auth.token.created'

components:
  messages:
    TokenCreatedEvent:
      payload:
        $ref: '#/components/schemas/TokenCreatedPayload'

    UserLoggedInEvent:
      payload:
        $ref: '#/components/schemas/UserLoggedInPayload'

  schemas:
    TokenCreatedPayload:
      type: object
      required: [event_id, event_type, timestamp, source_service, user_id]
      additionalProperties: false
      properties:
        event_id:
          type: string
          format: uuid
          description: "Уникальный ID события (для идемпотентности)"
        event_type:
          type: string
          const: "auth.token.created"
        timestamp:
          type: string
          format: date-time
          description: "ISO 8601, UTC"
        source_service:
          type: string
          description: "Имя сервиса-publisher"
          example: "auth"
        correlation_id:
          type: string
          format: uuid
          description: "ID запроса, инициировавшего цепочку (distributed tracing)"
        causation_id:
          type: string
          format: uuid
          description: "event_id события-причины"
        user_id:
          type: string
          format: uuid
        metadata:
          type: object
          additionalProperties: false
          properties:
            ip_address:
              type: string
            user_agent:
              type: string

    UserLoggedInPayload:
      type: object
      required: [event_id, event_type, timestamp, source_service, user_id]
      additionalProperties: false
      properties:
        event_id:
          type: string
          format: uuid
          description: "Уникальный ID события (для идемпотентности)"
        event_type:
          type: string
          const: "auth.user.logged_in"
        timestamp:
          type: string
          format: date-time
          description: "ISO 8601, UTC"
        source_service:
          type: string
          description: "Имя сервиса-publisher"
          example: "auth"
        correlation_id:
          type: string
          format: uuid
        causation_id:
          type: string
          format: uuid
        user_id:
          type: string
          format: uuid
```

### Стандартные поля payload

Каждый payload ДОЛЖЕН содержать обязательные поля. Домен-специфичные поля добавляются в конкретный payload (не через `allOf`).

**Как расширять:** Скопировать стандартные поля в конкретный payload, добавить домен-специфичные, поставить `additionalProperties: false` на **конкретный** payload. `StandardEventPayload` ниже — **справочный шаблон**, не используется напрямую в `$ref`.

```yaml
# Справочный шаблон — НЕ используется через $ref.
# Копировать эти поля в каждый конкретный {Event}Payload.
# additionalProperties: false ставить на конкретный payload, не на шаблон.
StandardEventPayload:
  type: object
  required: [event_id, event_type, timestamp, source_service]
  properties:
    event_id:
      type: string
      format: uuid
      description: "Уникальный ID события (UUID v4, для идемпотентности)"
    event_type:
      type: string
      description: "Совпадает с адресом channel (SSOT)"
    timestamp:
      type: string
      format: date-time
      description: "ISO 8601, UTC"
    source_service:
      type: string
      description: "Имя сервиса-publisher"
    correlation_id:
      type: string
      format: uuid
      description: "ID запроса, инициировавшего цепочку (distributed tracing)"
    causation_id:
      type: string
      format: uuid
      description: "event_id события-причины (причинно-следственная цепочка)"
```

### Consumer (receive)

Помимо `send` (publisher), описать `receive` (consumer) для каждого события, на которое сервис подписывается. Consumer-операции определяют, кто слушает канал.

```yaml
operations:
  # Publisher: auth-сервис отправляет событие
  publishTokenCreated:
    action: send
    channel:
      $ref: '#/channels/auth.token.created'

  # Consumer: notification-сервис слушает событие
  onTokenCreated:
    action: receive
    channel:
      $ref: '#/channels/auth.token.created'
```

Consumer-операции размещаются в файле **домена-publisher** (auth-events.yaml), а не consumer'а. Это позволяет видеть всех подписчиков в одном месте.

### Группировка по домену

Один файл на доменную группу (не на событие). Все события домена `auth` — в `auth-events.yaml`, все события домена `order` — в `order-events.yaml`.

```yaml
# auth-events.yaml — содержит все события домена auth:
# - auth.token.created
# - auth.token.revoked
# - auth.user.logged_in
# - auth.user.logged_out
# НЕ создавать отдельный файл auth-token-created.yaml
```

### Версионирование

Backward compatibility: добавление новых опциональных полей НЕ ломает consumer'ов. Удаление или переименование полей — breaking change.

```yaml
# v1.0.0 — исходная версия
TokenCreatedPayload:
  required: [event_id, event_type, timestamp, source_service, user_id]
  properties:
    user_id:
      type: string
      format: uuid

# v1.1.0 — добавлено опциональное поле (backward compatible)
TokenCreatedPayload:
  required: [event_id, event_type, timestamp, source_service, user_id]
  properties:
    user_id:
      type: string
      format: uuid
    session_id:          # Новое опциональное поле — consumer'ы не ломаются
      type: string
      format: uuid

# BREAKING: удаление поля, переименование, изменение required
# → Новый channel: auth.token.created.v2 + deprecation старого
```

```yaml
# Пример: breaking change — v1 deprecated + v2 active
channels:
  auth.token.created:
    address: auth.token.created
    description: "DEPRECATED — use auth.token.created.v2. Удаление после 2026-06-01."
    messages:
      TokenCreatedEvent:
        $ref: '#/components/messages/TokenCreatedEvent'

  auth.token.created.v2:
    address: auth.token.created.v2
    messages:
      TokenCreatedV2Event:
        $ref: '#/components/messages/TokenCreatedV2Event'

# TokenCreatedV2Event и TokenCreatedV2Payload объявляются в components
# аналогично v1, с изменёнными/добавленными полями.
# Все стандартные поля (event_id, event_type, timestamp, source_service)
# копируются в v2 payload. event_type = "auth.token.created.v2".
#
# Оба канала работают параллельно до deprecation deadline.
# Publisher отправляет в ОБА канала (transition period).
# Consumer мигрирует на v2, затем v1 удаляется.
```

### Связь с SDD процессом

| Момент SDD | Действие с AsyncAPI |
|------------|---------------------|
| Design (INT-N async event) | Определяет содержание контракта в markdown |
| INFRA-блок (wave 0) | Dev-agent создаёт/обновляет `{domain}-events.yaml` по INT-N |
| Per-service блок | Dev-agent реализует publisher/consumer, валидирует payload |
| Design → DONE | `{domain}-events.yaml` — финальная версия |
| CONFLICT (shared/) | Изменение `{domain}-events.yaml` = CONFLICT уровня Design |

```yaml
# При Design → DONE: валидировать финальную версию
# asyncapi validate shared/events/{domain}-events.yaml
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|----------|-----------|
| TypedDict вместо JSON Schema | Не машинно-валидируемые, не читаются AsyncAPI CLI | JSON Schema в блоке `components/schemas` |
| Один файл на событие | Избыточная гранулярность, сложно навигировать | Группировка по доменной группе в один файл |
| Inline schemas в message | Дублирование при переиспользовании, сложно поддерживать | `$ref: '#/components/schemas/...'` |
| Отсутствие `event_type` в payload | Consumer не может маршрутизировать без заголовков брокера | Обязательное поле `event_type` = адрес channel |
| Отсутствие `timestamp` в payload | Невозможно восстановить порядок событий при replay | Обязательное поле `timestamp` в ISO 8601 UTC |
| Несовпадение `event_type` и адреса channel | Нарушает SSOT — два источника истины для одного значения | `event_type` объявлять как `const: "{channel.address}"` |
| Отсутствие `event_id` | Consumer не может определить дубликат, нет идемпотентности | Обязательное поле `event_id` (UUID v4) |
| `additionalProperties: true` | Слабая валидация — принимает любые поля | Явно `additionalProperties: false` |

## Структура файлов

```
shared/events/
├── auth-events.yaml          # AsyncAPI spec для событий домена auth
├── order-events.yaml         # AsyncAPI spec для событий домена order
├── notification-events.yaml  # AsyncAPI spec для событий домена notification
└── README.md                 # Конвенции именования и навигация по файлам
```

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется линтером: `asyncapi validate shared/events/{group}.yaml`. Pre-commit hook `asyncapi-lint` запускает валидацию для изменённых `.yaml` в `shared/events/`.*

## Тестирование

*Тестирование не применимо — AsyncAPI-спецификации являются декларативными контрактами, не исполняемым кодом. Schema validation при publish выполняется runtime-кодом сервиса.*

## Логирование

*Логирование не применимо — технология не генерирует событий, требующих логирования.*
