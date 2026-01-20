---
type: standard
description: OpenAPI спецификация, Swagger UI на /docs, автогенерация
related:
  - src/api/design.md
  - src/api/versioning.md
  - src/api/deprecation.md
  - shared/contracts.md
---

# API Documentation (Swagger/OpenAPI)

Правила документирования API: OpenAPI спецификация, Swagger UI, автогенерация.

## Оглавление

- [Правила](#правила)
  - [OpenAPI спецификация](#openapi-спецификация)
  - [Swagger UI](#swagger-ui)
  - [Автогенерация](#автогенерация)
  - [Документирование](#документирование)
- [Примеры](#примеры)
- [Чек-лист документации](#чек-лист-документации)
- [FAQ](#faq)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### OpenAPI спецификация

**Правило:** Использовать OpenAPI 3.0+ для описания REST API.

```yaml
openapi: 3.0.3
info:
  title: User Service API
  version: 1.0.0
  description: API для управления пользователями
```

**Правило:** Один файл спецификации на версию API.

```
/docs/
  /api/
    openapi-v1.yaml
    openapi-v2.yaml
```

**Правило:** Спецификация — source of truth для API.

| Подход | Когда использовать |
|--------|-------------------|
| Spec-first | Новый API, публичный API |
| Code-first | Быстрое прототипирование, внутренний API |

**Правило:** Хранить спецификацию в репозитории.

```
/shared/contracts/
  /openapi/
    user-service-v1.yaml
    notification-service-v1.yaml
```

### Swagger UI

**Правило:** Swagger UI доступен на `/docs` или `/api/docs`.

```
https://api.example.com/docs           # Основная документация
https://api.example.com/api/v1/docs    # Документация версии
```

**Правило:** В production — только для авторизованных (если не публичный API).

```python
# FastAPI пример
if settings.ENVIRONMENT == "production":
    app = FastAPI(docs_url=None)  # Отключено
else:
    app = FastAPI(docs_url="/docs")  # Доступно
```

**Правило:** Отдельный URL для JSON/YAML спецификации.

```
/docs              # Swagger UI (интерактивный)
/docs/openapi.json # JSON спецификация
/docs/openapi.yaml # YAML спецификация
```

**Правило:** Настроить информацию о сервере.

```yaml
servers:
  - url: https://api.example.com/api/v1
    description: Production
  - url: https://staging-api.example.com/api/v1
    description: Staging
  - url: http://localhost:8000/api/v1
    description: Local development
```

### Автогенерация

**Правило:** Код и спецификация должны быть синхронизированы.

**Подходы к синхронизации:**

| Подход | Инструмент | Когда |
|--------|------------|-------|
| Code-first | FastAPI, NestJS | Спека генерится из кода |
| Spec-first | OpenAPI Generator | Код генерится из спеки |
| Validation | Spectral, Dredd | Проверка соответствия |

**Правило:** Автогенерация клиентов из спецификации.

```bash
# Генерация TypeScript клиента
openapi-generator generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./generated/client
```

**Правило:** Валидация спецификации в CI.

```yaml
# .github/workflows/api-lint.yml
- name: Lint OpenAPI
  run: npx @stoplight/spectral-cli lint openapi.yaml
```

**Правило:** Автоматическая публикация документации при деплое.

```yaml
# CI pipeline
- name: Deploy API docs
  run: |
    aws s3 cp docs/openapi.yaml s3://docs-bucket/api/
    # или обновить Swagger Hub / Postman
```

### Документирование

**Правило:** Каждый endpoint должен иметь описание.

```yaml
paths:
  /users:
    get:
      summary: Получить список пользователей
      description: |
        Возвращает пагинированный список пользователей.
        Поддерживает фильтрацию по статусу и роли.
      operationId: getUsers
```

**Правило:** Все параметры документированы.

```yaml
parameters:
  - name: status
    in: query
    description: Фильтр по статусу пользователя
    required: false
    schema:
      type: string
      enum: [active, inactive, blocked]
      default: active
    example: active
```

**Правило:** Все ответы документированы с примерами.

```yaml
responses:
  '200':
    description: Список пользователей
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/UserListResponse'
        example:
          data:
            - id: "123"
              name: "John Doe"
              email: "john@example.com"
          pagination:
            page: 1
            limit: 20
            total: 100
  '400':
    $ref: '#/components/responses/BadRequest'
  '401':
    $ref: '#/components/responses/Unauthorized'
```

**Правило:** Использовать компоненты для переиспользования.

```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          description: Уникальный идентификатор
        name:
          type: string
          description: Полное имя пользователя
      required:
        - id
        - name

  responses:
    NotFound:
      description: Ресурс не найден
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1
```

**Правило:** Документировать аутентификацию.

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT токен. Получить через POST /auth/login.
        Формат: Bearer {token}

security:
  - bearerAuth: []
```

**Правило:** Помечать deprecated endpoints.

```yaml
paths:
  /users:
    get:
      deprecated: true
      x-sunset: "2024-12-01"
      summary: "[DEPRECATED] Получить список пользователей"
      description: |
        **Deprecated:** Используйте /api/v2/users вместо этого.
        Будет отключено: 2024-12-01
```

---

## Примеры

### Пример 1: Базовая спецификация

```yaml
openapi: 3.0.3
info:
  title: User Service API
  version: 1.0.0
  description: API для управления пользователями
  contact:
    name: API Team
    email: api@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/api/v1
    description: Production

tags:
  - name: Users
    description: Операции с пользователями
  - name: Auth
    description: Аутентификация

paths:
  /users:
    get:
      tags:
        - Users
      summary: Получить список пользователей
      operationId: listUsers
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Список пользователей
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
      security:
        - bearerAuth: []

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        email:
          type: string
          format: email
      required:
        - id
        - name
        - email

    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        total_pages:
          type: integer

    Error:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: object

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1

    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  responses:
    Unauthorized:
      description: Требуется аутентификация
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: UNAUTHORIZED
              message: Authentication required

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Пример 2: FastAPI автогенерация

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="User Service API",
    version="1.0.0",
    description="API для управления пользователями",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

class User(BaseModel):
    """Модель пользователя."""
    id: str = Field(..., description="Уникальный идентификатор")
    name: str = Field(..., description="Полное имя")
    email: str = Field(..., description="Email адрес")

    class Config:
        schema_extra = {
            "example": {
                "id": "123",
                "name": "John Doe",
                "email": "john@example.com"
            }
        }

class UserListResponse(BaseModel):
    """Ответ со списком пользователей."""
    data: List[User]
    pagination: dict

@app.get(
    "/users",
    response_model=UserListResponse,
    summary="Получить список пользователей",
    description="Возвращает пагинированный список пользователей.",
    tags=["Users"]
)
async def list_users(
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Элементов на странице")
):
    """
    Получить список пользователей с пагинацией.

    - **page**: номер страницы (начиная с 1)
    - **limit**: количество элементов на странице (1-100)
    """
    return {"data": [], "pagination": {"page": page, "limit": limit}}
```

### Пример 3: NestJS автогенерация

```typescript
// user.dto.ts
import { ApiProperty } from '@nestjs/swagger';

export class UserDto {
  @ApiProperty({ description: 'Уникальный идентификатор' })
  id: string;

  @ApiProperty({ description: 'Полное имя' })
  name: string;

  @ApiProperty({ description: 'Email адрес' })
  email: string;
}

// user.controller.ts
import { Controller, Get, Query } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiQuery } from '@nestjs/swagger';

@ApiTags('Users')
@Controller('users')
export class UserController {
  @Get()
  @ApiOperation({ summary: 'Получить список пользователей' })
  @ApiQuery({ name: 'page', required: false, type: Number })
  @ApiQuery({ name: 'limit', required: false, type: Number })
  @ApiResponse({ status: 200, description: 'Список пользователей', type: [UserDto] })
  @ApiResponse({ status: 401, description: 'Требуется аутентификация' })
  async listUsers(
    @Query('page') page: number = 1,
    @Query('limit') limit: number = 20
  ) {
    return { data: [], pagination: { page, limit } };
  }
}
```

### Пример 4: Spectral правила линтинга

```yaml
# .spectral.yaml
extends: ["spectral:oas"]

rules:
  operation-description:
    severity: warn
    message: "Операция должна иметь описание"

  operation-operationId:
    severity: error
    message: "Операция должна иметь operationId"

  oas3-valid-schema-example:
    severity: error
    message: "Пример должен соответствовать схеме"

  info-contact:
    severity: warn
    message: "Спецификация должна содержать контактную информацию"

  # Кастомное правило: требовать примеры
  require-examples:
    severity: warn
    given: "$.paths.*.*.responses.*.content.application/json"
    then:
      field: example
      function: truthy
```

---

## Чек-лист документации

### Обязательно

- [ ] OpenAPI версия 3.0+
- [ ] `info.title` и `info.version` заполнены
- [ ] Все endpoints имеют `summary`
- [ ] Все параметры имеют `description`
- [ ] Все ответы задокументированы
- [ ] Схемы ошибок определены
- [ ] Аутентификация описана в `securitySchemes`

### Рекомендуется

- [ ] Примеры для всех схем
- [ ] `operationId` для всех операций
- [ ] Теги для группировки endpoints
- [ ] Описания серверов (dev/staging/prod)
- [ ] Контактная информация
- [ ] Deprecated endpoints помечены

### CI/CD

- [ ] Линтинг спецификации (Spectral)
- [ ] Проверка breaking changes
- [ ] Автопубликация документации
- [ ] Генерация клиентов

---

## FAQ

### Spec-first или Code-first?

**Ответ:**
- **Spec-first** для публичных API, контрактов между командами
- **Code-first** для внутренних API, быстрого прототипирования

Можно комбинировать: начать code-first, затем зафиксировать spec-first.

### Как версионировать спецификацию?

**Ответ:** Отдельный файл на мажорную версию:
```
openapi-v1.yaml
openapi-v2.yaml
```

### Как документировать WebSocket/gRPC?

**Ответ:**
- **WebSocket:** AsyncAPI спецификация
- **gRPC:** Protobuf файлы + grpc-gateway для REST документации

### Где хранить спецификацию?

**Ответ:**
```
/shared/contracts/openapi/      # Общий репозиторий
/docs/api/openapi.yaml          # В сервисе (code-first)
```

---

## Связанные инструкции

- [src/api/design.md](design.md) — правила дизайна API
- [src/api/versioning.md](versioning.md) — версионирование
- [src/api/deprecation.md](deprecation.md) — deprecation
- [shared/contracts.md](../../shared/contracts.md) — API контракты
