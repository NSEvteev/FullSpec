---
type: standard
description: Structured JSON logging — формат, уровни, контекст, трейсинг
related:
  - src/data/errors.md
  - src/runtime/observability.md
  - platform/observability/logging.md
---

# Structured Logging

> **Разделение ответственности:**
> - Этот файл: КАК логировать в коде сервиса (форматы, уровни, примеры)
> - [platform/observability/logging.md](/.claude/instructions/platform/observability/logging.md): ИНФРАСТРУКТУРА логирования (Loki, сбор, хранение)

Стандарт структурированного логирования в формате JSON для всех сервисов.

## Оглавление

- [Формат записи](#формат-записи)
- [Обязательные поля](#обязательные-поля)
- [Опциональные поля](#опциональные-поля)
- [Уровни логирования](#уровни-логирования)
- [Примеры](#примеры)
- [Контекст запроса](#контекст-запроса)
- [Трейсинг](#трейсинг)
- [Чувствительные данные](#чувствительные-данные)
- [Антипаттерны](#антипаттерны)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Формат записи

```json
{
  "timestamp": "2026-01-20T15:30:45.123Z",
  "level": "INFO",
  "service": "auth-service",
  "request_id": "req_abc123def456",
  "message": "Пользователь успешно аутентифицирован",
  "context": {
    "user_id": "usr_12345",
    "method": "POST",
    "path": "/api/v1/auth/login",
    "duration_ms": 145
  }
}
```

## Обязательные поля

| Поле | Тип | Формат | Описание |
|------|-----|--------|----------|
| `timestamp` | string | ISO 8601 | Время события в UTC |
| `level` | string | enum | Уровень логирования |
| `service` | string | kebab-case | Имя сервиса |
| `request_id` | string | req_xxx | ID запроса для трейсинга |
| `message` | string | — | Описание события |

## Опциональные поля

| Поле | Тип | Описание |
|------|-----|----------|
| `context` | object | Дополнительный контекст события |
| `error` | object | Информация об ошибке (для ERROR/FATAL) |
| `trace_id` | string | ID распределённого трейса |
| `span_id` | string | ID текущего спана |
| `user_id` | string | ID пользователя (если известен) |

## Уровни логирования

| Уровень | Когда использовать | Примеры |
|---------|-------------------|---------|
| `FATAL` | Критическая ошибка, сервис падает | Не удалось подключиться к БД при старте |
| `ERROR` | Ошибка, требуется внимание | Ошибка обработки запроса, сбой интеграции |
| `WARN` | Потенциальная проблема | Retry запроса, deprecation warning |
| `INFO` | Важные бизнес-события | Вход пользователя, создание заказа |
| `DEBUG` | Отладочная информация | Детали обработки, значения переменных |
| `TRACE` | Детальная трассировка | Вход/выход из функций, SQL-запросы |

### Правила по уровням

```
Продакшен: INFO и выше
Staging:   DEBUG и выше
Локально:  TRACE и выше
```

## Примеры

### INFO — Бизнес-событие

```json
{
  "timestamp": "2026-01-20T15:30:45.123Z",
  "level": "INFO",
  "service": "order-service",
  "request_id": "req_7f3a9b2c",
  "message": "Заказ успешно создан",
  "context": {
    "order_id": "ord_98765",
    "user_id": "usr_12345",
    "total_amount": 15000,
    "items_count": 3
  }
}
```

### ERROR — Ошибка обработки

```json
{
  "timestamp": "2026-01-20T15:30:45.123Z",
  "level": "ERROR",
  "service": "payment-service",
  "request_id": "req_8d4e1f6a",
  "message": "Ошибка обработки платежа",
  "error": {
    "code": "PAYMENT_DECLINED",
    "message": "Карта отклонена банком",
    "stack": "PaymentError: Card declined\n    at processPayment..."
  },
  "context": {
    "order_id": "ord_98765",
    "payment_method": "card",
    "attempt": 2
  }
}
```

### WARN — Retry операции

```json
{
  "timestamp": "2026-01-20T15:30:45.123Z",
  "level": "WARN",
  "service": "notification-service",
  "request_id": "req_2c5b8a3d",
  "message": "Повторная попытка отправки уведомления",
  "context": {
    "notification_id": "ntf_54321",
    "channel": "email",
    "attempt": 3,
    "max_attempts": 5,
    "reason": "SMTP timeout"
  }
}
```

### DEBUG — Детали обработки

```json
{
  "timestamp": "2026-01-20T15:30:45.123Z",
  "level": "DEBUG",
  "service": "auth-service",
  "request_id": "req_9e7f4c1b",
  "message": "Проверка JWT токена",
  "context": {
    "token_type": "access",
    "expires_in": 3600,
    "claims": ["user:read", "user:write"]
  }
}
```

## Контекст запроса

### HTTP-запросы

```json
{
  "context": {
    "http": {
      "method": "POST",
      "path": "/api/v1/users",
      "status": 201,
      "duration_ms": 145,
      "client_ip": "192.168.1.100",
      "user_agent": "Mozilla/5.0..."
    }
  }
}
```

### База данных

```json
{
  "context": {
    "db": {
      "operation": "SELECT",
      "table": "users",
      "duration_ms": 23,
      "rows_affected": 1
    }
  }
}
```

### Внешние сервисы

```json
{
  "context": {
    "external": {
      "service": "payment-gateway",
      "method": "POST",
      "endpoint": "/charges",
      "duration_ms": 890,
      "status": 200
    }
  }
}
```

## Трейсинг

### Распределённый трейсинг

```json
{
  "timestamp": "2026-01-20T15:30:45.123Z",
  "level": "INFO",
  "service": "order-service",
  "request_id": "req_abc123",
  "trace_id": "trace_def456789",
  "span_id": "span_ghi012",
  "parent_span_id": "span_jkl345",
  "message": "Обработка заказа"
}
```

### Корреляция логов

Все сервисы в цепочке используют одинаковый `request_id` и `trace_id`:

```
[gateway]  request_id=req_abc123 → "Входящий запрос"
[auth]     request_id=req_abc123 → "Проверка токена"
[order]    request_id=req_abc123 → "Создание заказа"
[payment]  request_id=req_abc123 → "Обработка платежа"
[gateway]  request_id=req_abc123 → "Ответ клиенту"
```

## Чувствительные данные

### Запрещено логировать

- Пароли и секреты
- Полные номера карт (только последние 4 цифры)
- Персональные данные (PII) без маскирования
- Токены доступа

### Маскирование

```json
{
  "context": {
    "card_number": "****1234",
    "email": "u***@example.com",
    "phone": "+7***567890"
  }
}
```

## Антипаттерны

```json
// ❌ Неправильно: неструктурированное сообщение
{
  "message": "User usr_12345 logged in from 192.168.1.1 at 2026-01-20"
}

// ✅ Правильно: данные в context
{
  "message": "Пользователь вошёл в систему",
  "context": {
    "user_id": "usr_12345",
    "client_ip": "192.168.1.1"
  }
}

// ❌ Неправильно: логирование чувствительных данных
{
  "context": {
    "password": "secret123",
    "card_number": "4111111111111111"
  }
}

// ❌ Неправильно: отсутствует request_id
{
  "timestamp": "2026-01-20T15:30:45.123Z",
  "level": "ERROR",
  "message": "Что-то пошло не так"
}
```

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование формата логов |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при изменении формата |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |

---

## Связанные инструкции

- [errors.md](errors.md) — Формат ошибок с request_id
- [src/runtime/observability.md](../runtime/observability.md) — Метрики и мониторинг
