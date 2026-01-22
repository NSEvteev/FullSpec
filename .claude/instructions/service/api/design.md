---
type: standard
description: URL naming (kebab-case), HTTP методы, статус-коды, partial update, bulk operations
related:
  - src/api/versioning.md
  - src/api/deprecation.md
  - src/api/swagger.md
  - src/data/errors.md
  - src/data/pagination.md
---

# API Design

Правила проектирования REST API: URL naming, HTTP методы, статус-коды.

## Оглавление

- [Правила](#правила)
  - [URL Naming](#url-naming)
  - [HTTP методы](#http-методы)
  - [Статус-коды](#статус-коды)
  - [Partial Update](#partial-update)
  - [Bulk Operations](#bulk-operations)
- [Примеры](#примеры)
- [Анти-паттерны](#анти-паттерны)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### URL Naming

**Правило:** Используем kebab-case для URL.

```
/api/v1/user-profiles        # Правильно
/api/v1/userProfiles         # Неправильно (camelCase)
/api/v1/user_profiles        # Неправильно (snake_case)
```

**Правило:** Ресурсы во множественном числе.

```
/api/v1/users                # Правильно
/api/v1/user                 # Неправильно
```

**Правило:** Вложенные ресурсы через URL path.

```
/api/v1/users/{id}/orders              # Заказы пользователя
/api/v1/users/{id}/orders/{orderId}    # Конкретный заказ
```

**Правило:** Максимум 2 уровня вложенности. Дальше — query параметры.

```
# Правильно (2 уровня)
/api/v1/users/{id}/orders

# Неправильно (3+ уровня)
/api/v1/users/{id}/orders/{orderId}/items/{itemId}

# Правильно — вынести на отдельный endpoint
/api/v1/order-items/{itemId}
```

**Правило:** Действия (actions) — через отдельный endpoint с глаголом.

```
POST /api/v1/users/{id}/activate       # Активировать пользователя
POST /api/v1/orders/{id}/cancel        # Отменить заказ
POST /api/v1/payments/{id}/refund      # Вернуть платёж
```

### HTTP методы

**Правило:** Использовать методы по назначению.

| Метод | Назначение | Идемпотентность |
|-------|------------|-----------------|
| `GET` | Получение данных | Да |
| `POST` | Создание ресурса | Нет |
| `PUT` | Полная замена ресурса | Да |
| `PATCH` | Частичное обновление | Да |
| `DELETE` | Удаление ресурса | Да |

**Правило:** GET никогда не изменяет состояние.

```
# Неправильно
GET /api/v1/users/{id}/delete

# Правильно
DELETE /api/v1/users/{id}
```

**Правило:** POST для создания, PUT/PATCH для обновления.

```
POST /api/v1/users            # Создать пользователя (без id)
PUT /api/v1/users/{id}        # Заменить пользователя целиком
PATCH /api/v1/users/{id}      # Обновить часть полей
```

### Статус-коды

**Правило:** Использовать HTTP статус-коды семантически.

| Код | Когда использовать |
|-----|-------------------|
| `200 OK` | Успешный GET/PUT/PATCH |
| `201 Created` | Успешный POST (создание) |
| `204 No Content` | Успешный DELETE |
| `400 Bad Request` | Ошибка валидации |
| `401 Unauthorized` | Требуется аутентификация |
| `403 Forbidden` | Нет прав |
| `404 Not Found` | Ресурс не найден |
| `409 Conflict` | Конфликт (дублирование) |
| `422 Unprocessable Entity` | Бизнес-логика отклонила |
| `429 Too Many Requests` | Rate limit |
| `500 Internal Server Error` | Ошибка сервера |
| `503 Service Unavailable` | Сервис недоступен |

**Правило:** 2xx — успех, 4xx — ошибка клиента, 5xx — ошибка сервера.

**Правило:** Возвращать `201 Created` с заголовком `Location`.

```http
POST /api/v1/users
Content-Type: application/json

{"name": "John", "email": "john@example.com"}

HTTP/1.1 201 Created
Location: /api/v1/users/123
Content-Type: application/json

{"id": "123", "name": "John", "email": "john@example.com"}
```

### Partial Update

**Правило:** Используем PATCH для частичного обновления.

**Правило:** Передаём только изменяемые поля.

```http
PATCH /api/v1/users/123
Content-Type: application/json

{"name": "John Updated"}

HTTP/1.1 200 OK
{"id": "123", "name": "John Updated", "email": "john@example.com"}
```

**Правило:** Null vs отсутствие поля.

| Значение | Поведение |
|----------|-----------|
| Поле отсутствует | Не изменять |
| `"field": null` | Установить null/удалить |
| `"field": ""` | Установить пустую строку |

**Правило:** Для сложных обновлений — JSON Patch (RFC 6902).

```http
PATCH /api/v1/users/123
Content-Type: application/json-patch+json

[
  {"op": "replace", "path": "/name", "value": "New Name"},
  {"op": "remove", "path": "/middleName"},
  {"op": "add", "path": "/tags/-", "value": "premium"}
]
```

### Bulk Operations

**Правило:** Bulk-операции через отдельный endpoint.

```
POST /api/v1/users/bulk          # Массовое создание
PATCH /api/v1/users/bulk         # Массовое обновление
DELETE /api/v1/users/bulk        # Массовое удаление
```

**Правило:** Формат запроса — массив объектов.

```http
POST /api/v1/users/bulk
Content-Type: application/json

{
  "items": [
    {"name": "User 1", "email": "user1@example.com"},
    {"name": "User 2", "email": "user2@example.com"}
  ]
}
```

**Правило:** Формат ответа — результат для каждого элемента.

```json
{
  "results": [
    {"success": true, "id": "123", "data": {...}},
    {"success": false, "error": {"code": "DUPLICATE", "message": "Email exists"}}
  ],
  "summary": {
    "total": 2,
    "successful": 1,
    "failed": 1
  }
}
```

**Правило:** Лимит на количество элементов в bulk-запросе.

```
X-Bulk-Limit: 100
```

---

## Примеры

### Пример 1: CRUD для ресурса

```
# Список пользователей
GET /api/v1/users?page=1&limit=20

# Получить пользователя
GET /api/v1/users/123

# Создать пользователя
POST /api/v1/users
{"name": "John", "email": "john@example.com"}

# Обновить частично
PATCH /api/v1/users/123
{"name": "John Updated"}

# Удалить
DELETE /api/v1/users/123
```

### Пример 2: Вложенные ресурсы

```
# Заказы пользователя
GET /api/v1/users/123/orders

# Конкретный заказ
GET /api/v1/users/123/orders/456

# Создать заказ
POST /api/v1/users/123/orders
{"product_id": "789", "quantity": 2}
```

### Пример 3: Действия (Actions)

```
# Активировать пользователя
POST /api/v1/users/123/activate

# Заблокировать пользователя
POST /api/v1/users/123/block
{"reason": "Spam"}

# Отменить заказ
POST /api/v1/orders/456/cancel
{"reason": "Customer request"}
```

### Пример 4: Поиск и фильтрация

```
# Фильтрация через query params
GET /api/v1/users?status=active&role=admin

# Поиск
GET /api/v1/users?q=john

# Сортировка
GET /api/v1/users?sort=created_at&order=desc

# Комбинация
GET /api/v1/users?status=active&sort=name&page=2&limit=10
```

---

## Анти-паттерны

| Анти-паттерн | Проблема | Правильно |
|--------------|----------|-----------|
| `GET /getUsers` | Глагол в URL | `GET /users` |
| `POST /users/delete/123` | POST для удаления | `DELETE /users/123` |
| `GET /users/123/activate` | GET изменяет состояние | `POST /users/123/activate` |
| `/api/v1/UserProfiles` | CamelCase | `/api/v1/user-profiles` |
| `200 OK` с телом ошибки | Неверный статус | `4xx/5xx` с телом ошибки |

---

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Создание документации для API |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации при изменении API |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |

---

## Связанные инструкции

- [src/api/versioning.md](versioning.md) — версионирование API
- [src/api/deprecation.md](deprecation.md) — вывод API из эксплуатации
- [src/api/swagger.md](swagger.md) — OpenAPI документация
- [src/data/errors.md](../data/errors.md) — формат ошибок
- [src/data/pagination.md](../data/pagination.md) — формат пагинации
