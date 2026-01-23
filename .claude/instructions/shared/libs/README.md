---
type: project
description: Общие библиотеки: errors, logging, validation
related:
  - shared/contracts.md
  - shared/events.md
  - src/data/errors.md
  - src/data/logging.md
  - src/data/validation.md
---

# Общие библиотеки

Описание переиспользуемых библиотек в `/shared/libs/`. Каждая библиотека решает одну задачу и используется всеми сервисами.

> **Тип инструкции:** `project` — описывает конкретные библиотеки проекта. При инициализации заполнить под специфику проекта.

## Оглавление

- [Структура](#структура)
- [Библиотеки](#библиотеки)
  - [errors](#errors)
  - [logging](#logging)
  - [validation](#validation)
  - [http-client](#http-client)
  - [features](#features)
- [Правила](#правила)
- [Примеры использования](#примеры-использования)
- [Связанные инструкции](#связанные-инструкции)

---

## Структура

```
/shared/
  /libs/
    /errors/                    # Единый формат ошибок
      README.md
      index.ts                  # или index.py
      types.ts
      codes.ts                  # Коды ошибок
      __tests__/

    /logging/                   # Единый формат логов
      README.md
      index.ts
      logger.ts
      formatters.ts
      __tests__/

    /validation/                # Общие валидаторы
      README.md
      index.ts
      validators/
        email.ts
        phone.ts
        uuid.ts
      __tests__/

    /http-client/               # HTTP клиент с resilience
      README.md
      index.ts
      client.ts
      retry.ts
      circuit-breaker.ts
      __tests__/

    /features/                  # Проверка feature flags
      README.md
      index.ts
      client.ts
      __tests__/
```

---

## Библиотеки

### errors

**Назначение:** Единый формат ошибок для всех сервисов.

**Структура ошибки:**

```typescript
interface AppError {
  code: string;           // AUTH_TOKEN_EXPIRED
  message: string;        // Human-readable сообщение
  details?: object;       // Дополнительные данные
  request_id?: string;    // ID запроса для трассировки
  http_status?: number;   // HTTP статус код
}
```

**Коды ошибок:**

| Префикс | Область | Примеры |
|---------|---------|---------|
| `AUTH_` | Аутентификация | `AUTH_TOKEN_EXPIRED`, `AUTH_INVALID_CREDENTIALS` |
| `AUTHZ_` | Авторизация | `AUTHZ_FORBIDDEN`, `AUTHZ_ROLE_REQUIRED` |
| `VAL_` | Валидация | `VAL_INVALID_EMAIL`, `VAL_REQUIRED_FIELD` |
| `DB_` | База данных | `DB_CONNECTION_FAILED`, `DB_UNIQUE_VIOLATION` |
| `EXT_` | Внешние сервисы | `EXT_TIMEOUT`, `EXT_UNAVAILABLE` |
| `SYS_` | Системные | `SYS_INTERNAL_ERROR`, `SYS_NOT_IMPLEMENTED` |

**API:**

```typescript
// Создание ошибки
import { AppError, ErrorCodes } from '@shared/errors';

throw new AppError({
  code: ErrorCodes.AUTH_TOKEN_EXPIRED,
  message: 'Token has expired',
  details: { expired_at: '2024-01-15T10:00:00Z' },
  http_status: 401
});

// Проверка типа ошибки
if (AppError.isAppError(error)) {
  response.status(error.http_status || 500).json({
    error: error.toJSON()
  });
}
```

---

### logging

**Назначение:** Структурированное логирование в JSON формате.

**Формат лога:**

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "info",
  "service": "users",
  "request_id": "req-abc-123",
  "trace_id": "trace-xyz-789",
  "message": "User created",
  "context": {
    "user_id": "user-456"
  }
}
```

**Уровни логирования:**

| Уровень | Когда использовать |
|---------|-------------------|
| `error` | Ошибки, требующие внимания |
| `warn` | Предупреждения, аномалии |
| `info` | Важные бизнес-события |
| `debug` | Отладочная информация |
| `trace` | Детальная трассировка |

**API:**

```typescript
import { logger } from '@shared/logging';

// Базовое использование
logger.info('User created', { user_id: '123' });
logger.error('Failed to create user', { error: err.message });

// С контекстом запроса
const requestLogger = logger.child({
  request_id: req.id,
  trace_id: req.headers['x-trace-id']
});

requestLogger.info('Processing request');
```

**Правила:**

- Не логировать PII (email, телефон) — маскировать
- Не логировать секреты (пароли, токены)
- Всегда включать `request_id` для корреляции

---

### validation

**Назначение:** Переиспользуемые валидаторы для типичных полей.

**Встроенные валидаторы:**

| Валидатор | Описание |
|-----------|----------|
| `isEmail` | Проверка email |
| `isPhone` | Проверка телефона (международный формат) |
| `isUUID` | Проверка UUID v4 |
| `isURL` | Проверка URL |
| `isDate` | Проверка даты (ISO 8601) |
| `isPassword` | Проверка сложности пароля |

**API:**

```typescript
import { validators, validate } from '@shared/validation';

// Отдельные валидаторы
if (!validators.isEmail(email)) {
  throw new ValidationError('Invalid email');
}

// Схема валидации
const userSchema = {
  email: { required: true, validator: validators.isEmail },
  phone: { required: false, validator: validators.isPhone },
  age: { required: true, validator: (v) => v >= 18 }
};

const errors = validate(data, userSchema);
// { email: 'Invalid format', age: 'Validation failed' }
```

**Формат ошибок валидации:**

```json
{
  "error": {
    "code": "VAL_VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "fields": {
        "email": "Invalid email format",
        "age": "Must be at least 18"
      }
    }
  }
}
```

---

### http-client

**Назначение:** HTTP клиент для межсервисного взаимодействия с retry, timeout и circuit breaker.

**Возможности:**

- Автоматический retry с exponential backoff
- Circuit breaker для защиты от каскадных сбоев
- Таймауты на соединение и чтение
- Автоматическая передача trace headers

**API:**

```typescript
import { HttpClient } from '@shared/http-client';

const client = new HttpClient({
  baseURL: process.env.USERS_SERVICE_URL,
  timeout: 5000,
  retry: {
    attempts: 3,
    delay: 1000,
    backoff: 2
  },
  circuitBreaker: {
    threshold: 5,      // 5 ошибок
    timeout: 30000     // 30 сек в открытом состоянии
  }
});

// Использование
const user = await client.get('/users/123');
await client.post('/users', { email, name });
```

**Передача контекста:**

```typescript
// Автоматически передаются заголовки:
// - X-Request-ID
// - X-Trace-ID
// - Authorization (если настроен)

const user = await client.get('/users/123', {
  headers: {
    'X-Custom-Header': 'value'
  }
});
```

---

### features

**Назначение:** Клиент для проверки feature flags.

**API:**

```typescript
import { features } from '@shared/features';

// Проверка флага
if (await features.isEnabled('new-checkout-flow')) {
  // Новый функционал
} else {
  // Старый функционал
}

// С контекстом пользователя
const enabled = await features.isEnabled('beta-feature', {
  userId: user.id,
  userGroup: user.group
});

// Получение значения флага
const limit = await features.getValue('rate-limit', 100);
```

**Конфигурация:**

```typescript
// Локальный fallback (для dev)
const localFlags = {
  'new-checkout-flow': true,
  'beta-feature': false
};

// Production: Unleash или аналог
features.configure({
  provider: 'unleash',
  url: process.env.UNLEASH_URL,
  fallback: localFlags
});
```

---

## Правила

### Версионирование библиотек

**Правило:** Библиотеки версионируются через package.json / pyproject.toml.

```json
{
  "name": "@shared/errors",
  "version": "1.2.0"
}
```

### Обратная совместимость

**Правило:** Breaking changes требуют major версию (semver).

| Изменение | Версия |
|-----------|--------|
| Новая функция | minor (1.1.0 → 1.2.0) |
| Баг фикс | patch (1.1.0 → 1.1.1) |
| Breaking change | major (1.1.0 → 2.0.0) |

### Документация

**Правило:** Каждая библиотека имеет README.md с:

1. Назначение
2. Установка / импорт
3. API reference
4. Примеры использования
5. Changelog

### Тесты

**Правило:** Покрытие тестами >= 80%.

```
/shared/libs/errors/__tests__/
  errors.test.ts
  codes.test.ts
```

---

## Примеры использования

### Пример 1: Обработка ошибок в контроллере

```typescript
import { AppError, ErrorCodes } from '@shared/errors';
import { logger } from '@shared/logging';
import { validate, validators } from '@shared/validation';

async function createUser(req, res) {
  try {
    // Валидация
    const errors = validate(req.body, {
      email: { required: true, validator: validators.isEmail },
      name: { required: true }
    });

    if (errors) {
      throw new AppError({
        code: ErrorCodes.VAL_VALIDATION_ERROR,
        message: 'Validation failed',
        details: { fields: errors },
        http_status: 400
      });
    }

    // Бизнес-логика
    const user = await userService.create(req.body);

    logger.info('User created', { user_id: user.id });
    res.status(201).json(user);

  } catch (error) {
    if (AppError.isAppError(error)) {
      logger.warn('Request failed', { code: error.code });
      res.status(error.http_status || 500).json({ error: error.toJSON() });
    } else {
      logger.error('Unexpected error', { error: error.message });
      res.status(500).json({
        error: {
          code: 'SYS_INTERNAL_ERROR',
          message: 'Internal server error'
        }
      });
    }
  }
}
```

### Пример 2: Межсервисный вызов

```typescript
import { HttpClient } from '@shared/http-client';
import { AppError, ErrorCodes } from '@shared/errors';
import { logger } from '@shared/logging';

const usersClient = new HttpClient({
  baseURL: process.env.USERS_SERVICE_URL
});

async function getUserProfile(userId: string) {
  try {
    const user = await usersClient.get(`/users/${userId}`);
    return user;

  } catch (error) {
    if (error.status === 404) {
      throw new AppError({
        code: ErrorCodes.NOT_FOUND,
        message: 'User not found',
        http_status: 404
      });
    }

    logger.error('Users service call failed', {
      user_id: userId,
      error: error.message
    });

    throw new AppError({
      code: ErrorCodes.EXT_UNAVAILABLE,
      message: 'Users service unavailable',
      http_status: 503
    });
  }
}
```

### Пример 3: Feature flag

```typescript
import { features } from '@shared/features';
import { logger } from '@shared/logging';

async function processCheckout(order, user) {
  const useNewFlow = await features.isEnabled('new-checkout-flow', {
    userId: user.id
  });

  logger.info('Processing checkout', {
    order_id: order.id,
    new_flow: useNewFlow
  });

  if (useNewFlow) {
    return processNewCheckout(order);
  } else {
    return processLegacyCheckout(order);
  }
}
```

---

## Скиллы

> Специфичные скиллы для этой области отсутствуют. Используйте общие скиллы проекта.

---

## Связанные инструкции

- [contracts.md](contracts.md) — контракты для межсервисного взаимодействия
- [events.md](events.md) — события (используют logging)
- [src/data/errors.md](../src/data/errors.md) — стандарт формата ошибок
- [src/data/logging.md](../src/data/logging.md) — стандарт логирования
- [src/data/validation.md](../src/data/validation.md) — стандарт валидации
- [src/runtime/resilience.md](../src/runtime/resilience.md) — паттерны устойчивости (http-client)
- [config/feature-flags.md](../config/feature-flags.md) — feature flags
