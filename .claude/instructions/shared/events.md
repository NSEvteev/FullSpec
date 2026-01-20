---
type: standard
description: События: naming ({service}.{entity}.{action}), идемпотентность, DLQ
related:
  - shared/contracts.md
  - shared/libs.md
  - platform/observability/logging.md
---

# События

Правила работы с событиями в событийно-ориентированной архитектуре (Event-Driven Architecture).

## Оглавление

- [Структура](#структура)
- [Правила](#правила)
- [Именование событий](#именование-событий)
- [Формат события](#формат-события)
- [Идемпотентность](#идемпотентность)
- [Dead Letter Queue (DLQ)](#dead-letter-queue-dlq)
- [Retry и обработка ошибок](#retry-и-обработка-ошибок)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Структура

```
/shared/
  /contracts/
    /events/                    # JSON Schema для событий
      user-created.json
      user-updated.json
      order-created.json
      order-completed.json
      payment-processed.json

/platform/
  /queues/
    rabbitmq.conf               # Конфигурация RabbitMQ
    /dlq/                       # Dead Letter Queues
      dlq-config.yaml
```

---

## Правила

### Асинхронность по умолчанию

**Правило:** Межсервисное взаимодействие — асинхронное через события.

| Когда | Подход |
|-------|--------|
| Запрос-ответ нужен немедленно | REST/gRPC |
| Можно подождать (секунды-минуты) | События |
| Fire-and-forget (уведомления) | События |
| Длинные операции | События + polling/callback |

### Один продюсер — много консьюмеров

**Правило:** Событие публикуется один раз, потребляется многими.

```
[Users Service] → user.created → [Exchange]
                                     ↓
                    ┌────────────────┼────────────────┐
                    ↓                ↓                ↓
              [Email Queue]   [Analytics Queue]  [Audit Queue]
                    ↓                ↓                ↓
              [Notifications]  [Analytics]       [Audit Log]
```

### Событие — факт, не команда

**Правило:** Событие описывает что произошло, а не что нужно сделать.

| Правильно | Неправильно |
|-----------|-------------|
| `users.user.created` | `users.create_user` |
| `orders.order.shipped` | `orders.ship_order` |
| `payments.payment.failed` | `payments.retry_payment` |

---

## Именование событий

### Формат

```
{service}.{entity}.{action}
```

| Компонент | Описание | Примеры |
|-----------|----------|---------|
| `service` | Сервис-источник | `users`, `orders`, `payments` |
| `entity` | Сущность | `user`, `order`, `payment` |
| `action` | Действие (прошедшее время) | `created`, `updated`, `deleted` |

### Примеры событий

| Событие | Описание |
|---------|----------|
| `users.user.created` | Пользователь создан |
| `users.user.updated` | Данные пользователя обновлены |
| `users.user.deleted` | Пользователь удалён |
| `orders.order.created` | Заказ создан |
| `orders.order.shipped` | Заказ отправлен |
| `orders.order.delivered` | Заказ доставлен |
| `orders.order.cancelled` | Заказ отменён |
| `payments.payment.processed` | Платёж обработан |
| `payments.payment.failed` | Платёж не прошёл |
| `payments.payment.refunded` | Возврат средств |

### Специальные действия

| Действие | Когда использовать |
|----------|-------------------|
| `activated` / `deactivated` | Изменение статуса активности |
| `verified` | Подтверждение (email, телефон) |
| `expired` | Истечение срока |
| `locked` / `unlocked` | Блокировка/разблокировка |

---

## Формат события

### Обязательные поля

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "users.user.created",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "source": "users-service",
  "correlation_id": "req-abc-123",
  "data": {
    "user_id": "user-456",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `event_id` | UUID | Уникальный идентификатор события |
| `event_type` | string | Тип события (см. именование) |
| `version` | semver | Версия схемы события |
| `timestamp` | ISO 8601 | Время создания события (UTC) |
| `source` | string | Сервис-источник |
| `correlation_id` | string | ID для трассировки цепочки |
| `data` | object | Полезная нагрузка события |

### Опциональные поля

| Поле | Тип | Описание |
|------|-----|----------|
| `metadata` | object | Дополнительные метаданные |
| `caused_by` | string | ID события-причины |
| `actor` | object | Кто инициировал действие |

### Пример с метаданными

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "users.user.updated",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "source": "users-service",
  "correlation_id": "req-abc-123",
  "data": {
    "user_id": "user-456",
    "changes": {
      "name": {"old": "John", "new": "John Doe"}
    }
  },
  "metadata": {
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0..."
  },
  "actor": {
    "type": "user",
    "id": "admin-789"
  }
}
```

---

## Идемпотентность

### Правило

**Обязательно:** Каждый консьюмер должен быть идемпотентным.

Одно и то же событие может быть доставлено несколько раз (at-least-once delivery). Повторная обработка не должна менять результат.

### Реализация

**Способ 1: Хранение обработанных event_id**

```python
def handle_event(event):
    event_id = event["event_id"]

    # Проверка: уже обработано?
    if is_event_processed(event_id):
        logger.info(f"Event {event_id} already processed, skipping")
        return

    # Обработка события
    process_event(event)

    # Отметка как обработанного
    mark_event_processed(event_id)
```

**Способ 2: Идемпотентные операции**

```python
def handle_user_created(event):
    user_id = event["data"]["user_id"]

    # INSERT ... ON CONFLICT DO NOTHING
    # Повторный INSERT просто ничего не сделает
    db.execute("""
        INSERT INTO users (id, email)
        VALUES (%s, %s)
        ON CONFLICT (id) DO NOTHING
    """, user_id, event["data"]["email"])
```

### Хранение event_id

```sql
CREATE TABLE processed_events (
    event_id UUID PRIMARY KEY,
    processed_at TIMESTAMP DEFAULT NOW(),
    consumer VARCHAR(100)
);

-- Индекс для очистки старых записей
CREATE INDEX idx_processed_events_date ON processed_events(processed_at);
```

**TTL:** Хранить event_id минимум 7 дней, затем очищать.

---

## Dead Letter Queue (DLQ)

### Назначение

DLQ — очередь для сообщений, которые не удалось обработать после всех попыток.

### Когда событие попадает в DLQ

1. Превышено количество retry (по умолчанию: 3)
2. Ошибка парсинга (malformed message)
3. Исключение без возможности retry (validation error)

### Структура DLQ

```
/platform/queues/dlq/
  dlq-config.yaml
```

```yaml
# dlq-config.yaml
dead_letter_queues:
  - name: users-dlq
    source_queue: users-events
    max_retries: 3
    retention_days: 30

  - name: orders-dlq
    source_queue: orders-events
    max_retries: 5
    retention_days: 30
```

### Формат сообщения в DLQ

```json
{
  "original_event": { /* исходное событие */ },
  "error": {
    "message": "Database connection failed",
    "type": "ConnectionError",
    "stack_trace": "..."
  },
  "metadata": {
    "retry_count": 3,
    "first_failure_at": "2024-01-15T10:00:00Z",
    "last_failure_at": "2024-01-15T10:05:00Z",
    "consumer": "notifications-service"
  }
}
```

### Мониторинг DLQ

**Алерт:** DLQ не пустая более 1 часа → уведомление в Slack.

```yaml
# /platform/monitoring/alerts/dlq.yml
groups:
  - name: dlq
    rules:
      - alert: DLQNotEmpty
        expr: rabbitmq_queue_messages{queue=~".*-dlq"} > 0
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "DLQ contains unprocessed messages"
```

---

## Retry и обработка ошибок

### Стратегия retry

**Exponential backoff с jitter:**

```python
def calculate_delay(attempt: int) -> float:
    """
    attempt 1: ~1 сек
    attempt 2: ~2 сек
    attempt 3: ~4 сек
    """
    base_delay = 1.0
    max_delay = 60.0
    jitter = random.uniform(0, 0.5)

    delay = min(base_delay * (2 ** attempt) + jitter, max_delay)
    return delay
```

### Классификация ошибок

| Тип ошибки | Retry | Пример |
|------------|-------|--------|
| Transient (временная) | Да | Таймаут БД, сеть недоступна |
| Permanent (постоянная) | Нет | Невалидные данные, 404 |
| Unknown (неизвестная) | Да (ограниченно) | Неожиданное исключение |

### Пример обработки

```python
def handle_event(event):
    try:
        process_event(event)
    except TransientError as e:
        # Retry
        raise RetryableError(e)
    except ValidationError as e:
        # В DLQ без retry
        logger.error(f"Validation failed: {e}")
        raise PermanentError(e)
    except Exception as e:
        # Неизвестная ошибка — retry с логированием
        logger.exception(f"Unexpected error: {e}")
        raise RetryableError(e)
```

---

## Примеры

### Пример 1: Публикация события

```python
# users-service
from events import publish_event

def create_user(email: str, name: str) -> User:
    user = User.create(email=email, name=name)

    # Публикация события после успешного создания
    publish_event(
        event_type="users.user.created",
        data={
            "user_id": str(user.id),
            "email": user.email,
            "name": user.name
        },
        correlation_id=get_current_correlation_id()
    )

    return user
```

### Пример 2: Обработка события

```python
# notifications-service
@event_handler("users.user.created")
def on_user_created(event: dict):
    user_id = event["data"]["user_id"]
    email = event["data"]["email"]

    # Идемпотентная отправка welcome email
    if not is_welcome_email_sent(user_id):
        send_welcome_email(email)
        mark_welcome_email_sent(user_id)
```

### Пример 3: Цепочка событий

```
[Orders] → orders.order.created
                    ↓
[Payments] обрабатывает → payments.payment.processed
                                    ↓
[Orders] обрабатывает → orders.order.paid
                                ↓
[Warehouse] обрабатывает → warehouse.item.reserved
                                    ↓
[Notifications] → отправка email клиенту
```

### Пример 4: JSON Schema события

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://company.com/events/orders.order.created.json",
  "title": "OrderCreated",
  "type": "object",
  "required": ["event_id", "event_type", "version", "timestamp", "source", "data"],
  "properties": {
    "event_id": { "type": "string", "format": "uuid" },
    "event_type": { "const": "orders.order.created" },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "timestamp": { "type": "string", "format": "date-time" },
    "source": { "type": "string" },
    "correlation_id": { "type": "string" },
    "data": {
      "type": "object",
      "required": ["order_id", "user_id", "items", "total"],
      "properties": {
        "order_id": { "type": "string", "format": "uuid" },
        "user_id": { "type": "string", "format": "uuid" },
        "items": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["product_id", "quantity", "price"],
            "properties": {
              "product_id": { "type": "string" },
              "quantity": { "type": "integer", "minimum": 1 },
              "price": { "type": "number", "minimum": 0 }
            }
          }
        },
        "total": { "type": "number", "minimum": 0 }
      }
    }
  }
}
```

---

## Скиллы

Скиллы для автоматизации работы с событиями:

| Скилл | Назначение |
|-------|------------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Создание документации для нового события |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации при изменении схемы события |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации событий |

---

## Связанные инструкции

- [contracts.md](contracts.md) — API контракты (JSON Schema для событий)
- [libs.md](libs.md) — общие библиотеки (event publisher/consumer)
- [platform/observability/logging.md](../platform/observability/logging.md) — логирование с correlation_id
- [platform/observability/tracing.md](../platform/observability/tracing.md) — трассировка событий
