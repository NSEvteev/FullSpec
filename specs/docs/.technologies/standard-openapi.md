---
description: Стандарт кодирования OpenAPI — конвенции именования, структура спецификаций, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: openapi
---

# Стандарт OpenAPI v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | OpenAPI Specification 3.1.0 |
| Ключевые библиотеки | Spectral 6.x (Stoplight) |
| Линтер | Spectral (`spectral lint`) |
| Конфигурация | `.spectral.yaml` в корне проекта |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| Файл | `{svc}.yaml` — совпадает с `docs/{svc}.md` | `auth.yaml`, `gateway.yaml` |
| Расположение | `shared/contracts/openapi/` | `shared/contracts/openapi/auth.yaml` |
| Версионирование | Поле `info.version` в файле. Единый файл, без v1/ v2/ поддиректорий. Версия API — в `servers[].url` (`/api/v1/`) | `info.version: 1.2.0` |
| operationId | `{verb}{Resource}` (camelCase) | `createUser`, `getTokenInfo` |
| Path parameters | camelCase в `{}` | `{userId}`, `{orderId}` |
| Схемы (components) | PascalCase | `UserProfile`, `TokenRequest` |
| Теги | kebab-case, по доменным группам | `auth`, `user-management` |

## Паттерны кода

### Структура файла

Полная структура OpenAPI 3.1 файла. Один файл на сервис — совпадает с именем `docs/{svc}.md`.

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

# Глобальная авторизация — все endpoints требуют Bearer JWT.
# Публичные endpoints переопределяют: security: []
security:
  - bearerAuth: []

paths:
  /auth/token:
    post:
      operationId: createToken
      tags: [auth]
      summary: "Получение JWT-токена"
      security: []  # Публичный endpoint — без авторизации
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TokenRequest'
      responses:
        '200':
          description: Токен создан
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenResponse'
        '401':
          description: Неверные credentials
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '422':
          description: Ошибка валидации
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

components:
  schemas:
    TokenRequest:
      type: object
      required: [grant_type]
      additionalProperties: false
      properties:
        grant_type:
          type: string
          enum: [password, refresh_token, device_code]
          description: "Тип авторизации"
          example: "password"
    TokenResponse:
      type: object
      required: [access_token, expires_in]
      additionalProperties: false
      properties:
        access_token:
          type: string
          description: "JWT access-токен"
          example: "eyJhbGciOiJSUzI1NiIs..."
        refresh_token:
          type: string
          description: "Refresh-токен для обновления"
        expires_in:
          type: integer
          description: "Время жизни access-токена в секундах"
          example: 3600
    ErrorResponse:
      type: object
      required: [code, message]
      additionalProperties: false
      properties:
        code:
          type: string
          description: "Машинно-читаемый код ошибки"
          example: "INVALID_CREDENTIALS"
        message:
          type: string
          description: "Описание ошибки для разработчика"
        details:
          type: object
          description: "Дополнительный контекст (опционально)"

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Ссылки на schemas

Все schemas в `paths` используют `$ref` на `components/schemas/`. Inline schemas запрещены — это дублирование.

```yaml
# Правильно: $ref на schemas из components
requestBody:
  required: true
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/TokenRequest'

responses:
  '200':
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/TokenResponse'

# Неправильно: inline schema (дублирование, нарушает SSOT)
requestBody:
  content:
    application/json:
      schema:
        type: object
        properties:
          grant_type:
            type: string
```

### Error responses

Стандартный формат ошибок — единая schema `ErrorResponse` для всех 4xx/5xx ответов. Определяется в `components/schemas` (см. основной пример) и ссылается через `$ref`.

```yaml
# Использование ErrorResponse в paths (GET + PUT + DELETE — типовой CRUD):
paths:
  /users/{userId}:
    get:
      operationId: getUser
      tags: [user-management]
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Пользователь найден
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserProfile'
        '404':
          description: Пользователь не найден
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
    put:
      operationId: updateUser
      tags: [user-management]
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: Пользователь обновлён
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserProfile'
        '404':
          description: Пользователь не найден
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '422':
          description: Ошибка валидации
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
    delete:
      operationId: deleteUser
      tags: [user-management]
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Пользователь удалён
        '404':
          description: Пользователь не найден
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

# Схемы для CRUD (добавить в components/schemas основного файла):
#   UserProfile:
#     type: object
#     required: [id, email]
#     additionalProperties: false
#     properties:
#       id: { type: string, format: uuid }
#       email: { type: string, format: email }
#       name: { type: string }
#   UpdateUserRequest:
#     type: object
#     additionalProperties: false
#     properties:
#       email: { type: string, format: email }
#       name: { type: string }
```

### Пагинация

Паттерн для list-endpoints с пагинацией. Query-параметры `limit`, `offset`, `sort`.

```yaml
# Endpoint с пагинацией (в paths):
paths:
  /users:
    get:
      operationId: listUsers
      tags: [user-management]
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
        - name: sort
          in: query
          schema:
            type: string
            enum: [created_at, -created_at, name, -name]
      responses:
        '200':
          description: Список пользователей
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedUsersResponse'
```

```yaml
# Schema для пагинированного ответа (в components/schemas):
components:
  schemas:
    PaginatedUsersResponse:
      type: object
      required: [items, total]
      additionalProperties: false
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/UserProfile'
        total:
          type: integer
          description: "Общее количество записей"
        limit:
          type: integer
        offset:
          type: integer
```

### Связь с SDD процессом

| Момент SDD | Действие с OpenAPI |
|------------|-------------------|
| Design (INT-N sync REST) | Определяет содержание контракта в markdown |
| INFRA-блок (wave 0) | Dev-agent создаёт/обновляет `{svc}.yaml` по INT-N |
| Per-service блок | Dev-agent реализует handlers, валидирует против spec |
| Design → DONE | `{svc}.yaml` — финальная версия, `info.version` обновлён |
| CONFLICT (shared/) | Изменение `{svc}.yaml` = CONFLICT уровня Design |

```yaml
# Пример: обновление info.version при Design → DONE
info:
  title: "Auth API"
  version: "1.2.0"  # Обновить при завершении цепочки NNNN
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|----------|-----------|
| `$ref` на файл другого сервиса | Дублирование ownership, нарушает "провайдер владеет" | Каждый файл самодостаточный |
| Версии в имени файла (`auth-v1.yaml`, `auth-v2.yaml`) | Дублирование — версия уже в `info.version` и `servers[].url` | Единый `auth.yaml` |
| JSON формат | Плохой diff, нет комментариев | YAML |
| `additionalProperties: true` по умолчанию | Слабая валидация — принимает любые поля | Явно `additionalProperties: false` |
| Inline schemas вместо $ref | Дублирование schemas внутри файла | `$ref: '#/components/schemas/...'` |

## Структура файлов

```
shared/contracts/openapi/
├── auth.yaml          # OpenAPI spec для auth-сервиса
├── gateway.yaml       # OpenAPI spec для gateway-сервиса
├── users.yaml         # OpenAPI spec для users-сервиса
└── README.md          # Конвенции и навигация
```

Правила размещения:
- Один файл на сервис (совпадает с `docs/{svc}.md`)
- Секция `paths` — endpoints из `docs/{svc}.md` § 2
- Секция `components/schemas` — Data Model из `docs/{svc}.md` § 3
- Кросс-сервисные ссылки: НЕ использовать `$ref` между файлами — каждый файл самодостаточный

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется линтером: `spectral lint shared/contracts/openapi/{svc}.yaml`. Pre-commit hook `openapi-lint` запускает spectral для изменённых .yaml в `shared/contracts/openapi/`.*

## Тестирование

*Тестирование не применимо — OpenAPI-спецификации являются декларативными контрактами, не исполняемым кодом. Валидация спецификаций выполняется линтером (Spectral). Contract testing (Schemathesis) опционален и настраивается per-service.*

## Логирование

*Логирование не применимо — технология не генерирует событий, требующих логирования.*
