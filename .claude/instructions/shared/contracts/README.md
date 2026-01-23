---
type: standard
description: API контракты: OpenAPI, Protobuf, JSON Schema
related:
  - shared/events.md
  - shared/libs.md
  - src/api/design.md
  - src/api/swagger.md
---

# API контракты

Правила создания и поддержки контрактов между сервисами. Контракты — единственный источник правды для межсервисного взаимодействия.

## Оглавление

- [Структура](#структура)
- [Правила](#правила)
- [OpenAPI (REST)](#openapi-rest)
- [Protobuf (gRPC)](#protobuf-grpc)
- [JSON Schema (Events)](#json-schema-events)
- [Версионирование](#версионирование)
- [Contract Testing](#contract-testing)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Структура

```
/shared/
  /contracts/
    /rest/                  # OpenAPI спецификации
      auth.yaml
      users.yaml
      orders.yaml
    /grpc/                  # Protocol Buffers
      auth.proto
      users.proto
    /events/                # JSON Schema для событий
      user-created.json
      order-completed.json
    /realtime/              # Схемы real-time сообщений
      notifications.json
      chat-messages.json
    /pacts/                 # Contract testing (генерируются)
      auth-users.json
```

---

## Правила

### Контракт первый (Contract-First)

**Правило:** Сначала контракт, потом код.

1. Создать/обновить контракт в `/shared/contracts/`
2. Провести ревью контракта
3. Сгенерировать код из контракта
4. Реализовать логику

**Почему:** Контракт — соглашение между командами. Изменение контракта без обсуждения ломает потребителей.

### Обратная совместимость

**Правило:** Изменения контракта должны быть обратно совместимыми.

| Действие | Разрешено | Запрещено |
|----------|-----------|-----------|
| Добавить поле | Да (optional) | Нет (required) |
| Удалить поле | Нет | — |
| Переименовать поле | Нет | — |
| Изменить тип поля | Нет | — |
| Добавить endpoint | Да | — |
| Удалить endpoint | Нет (deprecate) | — |

**Breaking change:** Создавать новую версию контракта (v2).

### Единый источник правды

**Правило:** Код генерируется из контракта, а не наоборот.

```
/shared/contracts/rest/users.yaml  →  генерация  →  /src/users/api/types.ts
/shared/contracts/grpc/auth.proto  →  protoc     →  /src/auth/proto/auth_pb2.py
```

---

## OpenAPI (REST)

### Формат файла

```yaml
# /shared/contracts/rest/users.yaml
openapi: 3.0.3
info:
  title: Users Service API
  version: 1.0.0
  description: Управление пользователями

servers:
  - url: /api/v1

paths:
  /users:
    get:
      summary: Список пользователей
      operationId: listUsers
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Успешный ответ
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        created_at:
          type: string
          format: date-time
```

### Правила именования

| Элемент | Формат | Пример |
|---------|--------|--------|
| Файл | kebab-case | `user-profiles.yaml` |
| operationId | camelCase | `getUserById` |
| Схемы | PascalCase | `UserResponse` |
| Параметры пути | snake_case | `user_id` |
| Поля JSON | snake_case | `created_at` |

### Обязательные элементы

- `info.title` — название сервиса
- `info.version` — версия API
- `operationId` — уникальный идентификатор операции
- `responses.default` — обработка ошибок
- `components.schemas` — все типы данных

---

## Protobuf (gRPC)

### Формат файла

```protobuf
// /shared/contracts/grpc/auth.proto
syntax = "proto3";

package auth.v1;

option go_package = "github.com/company/project/shared/proto/auth/v1";

// Сервис аутентификации
service AuthService {
  // Аутентификация пользователя
  rpc Login(LoginRequest) returns (LoginResponse);

  // Проверка токена
  rpc ValidateToken(ValidateTokenRequest) returns (ValidateTokenResponse);
}

message LoginRequest {
  string email = 1;
  string password = 2;
}

message LoginResponse {
  string access_token = 1;
  string refresh_token = 2;
  int64 expires_in = 3;
}
```

### Правила именования

| Элемент | Формат | Пример |
|---------|--------|--------|
| Файл | kebab-case | `user-service.proto` |
| Package | snake_case.version | `auth.v1` |
| Service | PascalCase | `AuthService` |
| RPC | PascalCase | `ValidateToken` |
| Message | PascalCase | `LoginRequest` |
| Поля | snake_case | `access_token` |

### Версионирование

```protobuf
package auth.v1;  // Первая версия
package auth.v2;  // Вторая версия (breaking changes)
```

---

## JSON Schema (Events)

### Формат файла

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://company.com/events/user-created.json",
  "title": "UserCreated",
  "description": "Событие создания пользователя",
  "type": "object",
  "required": ["event_id", "event_type", "timestamp", "data"],
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid",
      "description": "Уникальный идентификатор события"
    },
    "event_type": {
      "type": "string",
      "const": "users.user.created"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "data": {
      "type": "object",
      "required": ["user_id", "email"],
      "properties": {
        "user_id": {
          "type": "string",
          "format": "uuid"
        },
        "email": {
          "type": "string",
          "format": "email"
        }
      }
    }
  }
}
```

### Обязательные поля события

| Поле | Тип | Описание |
|------|-----|----------|
| `event_id` | uuid | Идентификатор для идемпотентности |
| `event_type` | string | Тип события (`{service}.{entity}.{action}`) |
| `timestamp` | datetime | Время создания события |
| `data` | object | Полезная нагрузка |

---

## Версионирование

### REST API

URL-версионирование:
```
/api/v1/users
/api/v2/users  # Новая версия с breaking changes
```

### gRPC

Package-версионирование:
```protobuf
package auth.v1;
package auth.v2;
```

### События

Поле версии в схеме:
```json
{
  "event_type": "users.user.created",
  "version": "1.0.0"
}
```

---

## Contract Testing

### Pact (Consumer-Driven)

```
/shared/contracts/pacts/
  auth-users.json       # Контракт между auth и users
```

**Процесс:**
1. Consumer (потребитель) создаёт Pact-контракт
2. Provider (поставщик) верифицирует контракт
3. При изменении — обновить Pact

### Валидация в CI

```yaml
# .github/workflows/contracts.yml
jobs:
  validate:
    steps:
      - name: Validate OpenAPI
        run: npx @redocly/cli lint shared/contracts/rest/*.yaml

      - name: Validate Protobuf
        run: buf lint shared/contracts/grpc/

      - name: Validate JSON Schema
        run: npx ajv validate -s meta-schema.json -d shared/contracts/events/*.json
```

---

## Примеры

### Пример 1: Добавление нового endpoint

1. Обновить контракт:
```yaml
# /shared/contracts/rest/users.yaml
paths:
  /users/{user_id}/avatar:
    put:
      summary: Загрузка аватара
      operationId: uploadUserAvatar
      # ...
```

2. Сгенерировать типы:
```bash
make generate-types
```

3. Реализовать endpoint в сервисе

### Пример 2: Создание нового события

1. Создать JSON Schema:
```bash
# /shared/contracts/events/order-shipped.json
```

2. Добавить в документацию событий
3. Реализовать публикацию в сервисе

### Пример 3: Breaking change

1. Создать новую версию:
```yaml
# /shared/contracts/rest/users-v2.yaml
openapi: 3.0.3
info:
  title: Users Service API
  version: 2.0.0
```

2. Поддерживать обе версии параллельно
3. Deprecate старую версию (минимум 3 месяца)

---

## Скиллы

Скиллы для автоматизации работы с контрактами:

| Скилл | Назначение |
|-------|------------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Создание документации для нового контракта |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации при изменении контракта |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации контрактов |

---

## Связанные инструкции

- [events.md](events.md) — правила работы с событиями
- [libs.md](libs.md) — общие библиотеки (валидация контрактов)
- [src/api/design.md](../src/api/design.md) — проектирование REST API
- [src/api/swagger.md](../src/api/swagger.md) — документация OpenAPI
- [src/api/versioning.md](../src/api/versioning.md) — версионирование API
