---
type: standard
description: Версионирование API через URL (/v1/, /v2/), gRPC package versioning
related:
  - src/api/design.md
  - src/api/deprecation.md
  - src/api/swagger.md
---

# API Versioning

Правила версионирования API: URL versioning для REST, package versioning для gRPC.

## Оглавление

- [Правила](#правила)
  - [REST API Versioning](#rest-api-versioning)
  - [gRPC Versioning](#grpc-versioning)
  - [Когда создавать новую версию](#когда-создавать-новую-версию)
  - [Поддержка версий](#поддержка-версий)
- [Примеры](#примеры)
- [FAQ](#faq)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### REST API Versioning

**Правило:** Версия в URL path (не в header, не в query).

```
/api/v1/users              # Правильно
/api/users?version=1       # Неправильно
Accept: application/vnd.api.v1+json  # Неправильно (сложнее отлаживать)
```

**Почему URL versioning:**
- Простота понимания и использования
- Легко тестировать в браузере
- Кэширование работает из коробки
- Логирование понятное

**Правило:** Формат версии — `v{N}` (major version only).

```
/api/v1/users              # Правильно
/api/v1.2/users            # Неправильно (minor версия)
/api/1/users               # Неправильно (без v)
```

**Правило:** Префикс `/api/` обязателен.

```
/api/v1/users              # Правильно
/v1/users                  # Неправильно (без /api/)
```

**Структура URL:**
```
https://{host}/api/v{N}/{resource}
```

| Часть | Пример | Описание |
|-------|--------|----------|
| `{host}` | `api.example.com` | Хост (может быть поддоменом) |
| `/api/` | `/api/` | Фиксированный префикс |
| `v{N}` | `v1`, `v2` | Мажорная версия |
| `{resource}` | `users`, `orders` | Ресурс |

### gRPC Versioning

**Правило:** Версия в package name.

```protobuf
// v1
package myservice.v1;

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
}
```

```protobuf
// v2
package myservice.v2;

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc GetUserDetails(GetUserDetailsRequest) returns (UserDetails);
}
```

**Правило:** Один файл .proto на версию.

```
/proto/
  /user/
    /v1/
      user.proto
    /v2/
      user.proto
```

**Правило:** Import указывает полный путь с версией.

```protobuf
import "user/v1/user.proto";
import "common/v1/types.proto";
```

### Когда создавать новую версию

**Правило:** Новая мажорная версия (v1 -> v2) при breaking changes.

**Breaking changes (требуют новую версию):**

| Изменение | Пример | Почему breaking |
|-----------|--------|-----------------|
| Удаление поля | Удалить `user.middleName` | Клиенты ожидают поле |
| Переименование поля | `name` -> `fullName` | Клиенты используют старое имя |
| Изменение типа | `id: int` -> `id: string` | Несовместимость типов |
| Изменение URL | `/users` -> `/accounts` | Клиенты запрашивают старый URL |
| Удаление endpoint | Удалить `DELETE /users` | Клиенты используют endpoint |
| Изменение обязательности | `email` стал required | Клиенты не передают поле |

**Non-breaking changes (не требуют новую версию):**

| Изменение | Пример |
|-----------|--------|
| Добавление поля | Добавить `user.avatar` |
| Добавление endpoint | Добавить `GET /users/search` |
| Добавление query param | Добавить `?include=orders` |
| Расширение enum | Добавить новый статус |
| Улучшение описания | Уточнить документацию |

### Поддержка версий

**Правило:** Поддерживаем N-1 версий одновременно (текущая + предыдущая).

```
v1 — deprecated (поддержка 6 месяцев)
v2 — current (активная)
v3 — beta (опциональная)
```

**Правило:** Минимальный срок поддержки deprecated версии — 6 месяцев.

**Правило:** Уведомлять о deprecation через заголовки (см. [deprecation.md](deprecation.md)).

**Жизненный цикл версии:**

```
[alpha] -> [beta] -> [stable] -> [deprecated] -> [sunset]
   |         |          |            |              |
   |         |          |            |              +-- Версия отключена
   |         |          |            +-- Поддержка, но не развивается
   |         |          +-- Основная версия для продакшена
   |         +-- Для раннего тестирования
   +-- Внутренняя разработка
```

---

## Примеры

### Пример 1: Эволюция REST API

**v1 — начальная версия:**
```
GET /api/v1/users
Response: [{"id": 1, "name": "John"}]
```

**v2 — breaking change (структура изменилась):**
```
GET /api/v2/users
Response: {
  "data": [{"id": "1", "name": "John", "email": "john@example.com"}],
  "pagination": {"page": 1, "total": 100}
}
```

Изменения:
- `id` стал строкой
- Добавлена обёртка `data`
- Добавлена пагинация

### Пример 2: Параллельная поддержка версий

```python
# FastAPI пример
from fastapi import APIRouter

router_v1 = APIRouter(prefix="/api/v1")
router_v2 = APIRouter(prefix="/api/v2")

# v1 — старый формат
@router_v1.get("/users")
async def get_users_v1():
    return [{"id": 1, "name": "John"}]

# v2 — новый формат
@router_v2.get("/users")
async def get_users_v2():
    return {"data": [{"id": "1", "name": "John"}], "pagination": {...}}

# Регистрация обоих роутеров
app.include_router(router_v1)
app.include_router(router_v2)
```

### Пример 3: gRPC версионирование

**proto/user/v1/user.proto:**
```protobuf
syntax = "proto3";
package user.v1;

message User {
  int64 id = 1;
  string name = 2;
}

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
}
```

**proto/user/v2/user.proto:**
```protobuf
syntax = "proto3";
package user.v2;

message User {
  string id = 1;  // Изменён тип
  string name = 2;
  string email = 3;  // Добавлено поле
  Profile profile = 4;  // Добавлена вложенная структура
}

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);  // Новый метод
}
```

### Пример 4: Миграция между версиями

```
# Клиент запрашивает v1
GET /api/v1/users/123

# Внутренняя логика преобразует в v2 формат и обратно
v1_response = convert_v2_to_v1(get_user_v2(123))
return v1_response
```

**Adapter pattern для поддержки старых версий:**
```python
class UserAdapterV1:
    def to_v1(self, user_v2: UserV2) -> dict:
        return {
            "id": int(user_v2.id),  # v2 string -> v1 int
            "name": user_v2.name
            # email и profile не возвращаем в v1
        }
```

---

## FAQ

### Когда использовать header versioning?

**Ответ:** Не рекомендуется. URL versioning проще для отладки, документации и кэширования. Header versioning может быть оправдан только если URL версионирование невозможно по техническим причинам.

### Как версионировать WebSocket/SSE?

**Ответ:** Версия в URL path, как для REST:
```
wss://api.example.com/api/v1/ws/notifications
```

### Сколько версий поддерживать одновременно?

**Ответ:** Максимум 2 (current + deprecated). Больше — сложно поддерживать, растёт техдолг.

### Что делать если клиент не указал версию?

**Ответ:** Редирект на последнюю стабильную версию или 400 Bad Request с описанием.
```http
GET /api/users
HTTP/1.1 400 Bad Request
{"error": {"code": "VERSION_REQUIRED", "message": "Please specify API version: /api/v1/users or /api/v2/users"}}
```

---

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Создание документации для новой версии API |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации при изменении версии |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |

---

## Связанные инструкции

- [src/api/design.md](design.md) — общие правила дизайна API
- [src/api/deprecation.md](deprecation.md) — вывод версий из эксплуатации
- [src/api/swagger.md](swagger.md) — документация версий
