---
description: Стандарт кодирования Protobuf — конвенции именования, структура .proto файлов, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: protobuf
---

# Стандарт Protobuf v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | Protocol Buffers v3 (proto3) |
| Ключевые библиотеки | buf 1.x (lint, breaking detection, codegen) |
| Линтер и валидация | buf (buf.build) |
| Конфигурация | `buf.yaml` в `shared/contracts/protobuf/` |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| Файл | `{svc}.proto` — совпадает с `docs/{svc}.md` | `auth.proto`, `users.proto` |
| Расположение | `shared/contracts/protobuf/` | `shared/contracts/protobuf/auth.proto` |
| Package | `{project}.{svc}.v{N}` | `myapp.auth.v1` |
| Service | PascalCase + `Service` суффикс | `AuthService` |
| RPC | PascalCase, verb + noun | `CreateToken`, `ValidateToken` |
| Message | PascalCase | `TokenRequest`, `TokenResponse` |
| Field | snake_case | `user_id`, `grant_type` |
| Enum | PascalCase, значения UPPER_SNAKE_CASE с префиксом | `GrantType`, `GRANT_TYPE_PASSWORD` |

## Паттерны кода

### Структура файла

Базовый шаблон .proto-файла для gRPC-сервиса. Один файл — один сервис.

```protobuf
syntax = "proto3";

package myapp.auth.v1;

// Language-specific options — раскомментировать нужные:
// option go_package = "myapp/gen/auth/v1;authv1";
// option java_package = "com.myapp.auth.v1";
// option csharp_namespace = "MyApp.Auth.V1";

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

message ValidateTokenRequest {
  string access_token = 1;
}

message ValidateTokenResponse {
  bool valid = 1;
  string user_id = 2;
  repeated string scopes = 3;
}
```

### Reserved fields

При удалении поля обязательно добавить `reserved`, чтобы исключить переиспользование номера и имени в будущем.

```protobuf
message CreateTokenRequest {
  string grant_type = 1;
  string username = 2;
  string password = 3;

  // Поля 4 и 5 удалены — зарезервированы во избежание wire format incompatibility.
  reserved 4, 5;
  reserved "client_id", "client_secret";
}
```

### Enum с префиксами

Значения enum должны иметь префикс — имя enum в UPPER_SNAKE_CASE. Нулевое значение — `UNSPECIFIED`.

```protobuf
enum GrantType {
  GRANT_TYPE_UNSPECIFIED = 0;
  GRANT_TYPE_PASSWORD = 1;
  GRANT_TYPE_REFRESH_TOKEN = 2;
  GRANT_TYPE_DEVICE_CODE = 3;
}

message CreateTokenRequest {
  GrantType grant_type = 1;
  string username = 2;
  string password = 3;
}
```

### CRUD операции

Типовой набор RPC для управления ресурсом. Каждый RPC имеет отдельную пару Request/Response.

```protobuf
import "google/protobuf/timestamp.proto";

service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
}

message CreateUserResponse {
  string user_id = 1;
}

message GetUserRequest {
  string user_id = 1;
}

message GetUserResponse {
  string user_id = 1;
  string email = 2;
  string name = 3;
  google.protobuf.Timestamp created_at = 4;
}

message ListUsersRequest {
  int32 page_size = 1;    // Максимум элементов (default: 20, max: 100)
  string page_token = 2;  // Токен следующей страницы
}

message ListUsersResponse {
  repeated GetUserResponse users = 1;
  string next_page_token = 2;  // Пусто = последняя страница
  int32 total_count = 3;
}

message UpdateUserRequest {
  string user_id = 1;
  string email = 2;
  string name = 3;
}

message UpdateUserResponse {
  string user_id = 1;
}

message DeleteUserRequest {
  string user_id = 1;
}

message DeleteUserResponse {}  // Пустой ответ — OK означает удалён
```

### Well-known types

Разрешённые `google.protobuf` типы и запрещённые:

```protobuf
import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";

message AuditLogEntry {
  string user_id = 1;
  string action = 2;
  google.protobuf.Timestamp created_at = 3;  // Правильно: Timestamp для дат
  google.protobuf.Duration ttl = 4;          // Правильно: Duration для интервалов
}

// РАЗРЕШЕНО: google.protobuf.Timestamp, Duration, Struct (для JSON-like данных)
// ЗАПРЕЩЕНО: google.protobuf.Any (потеря type safety — используйте oneof)
```

| Тип | Статус | Когда использовать |
|-----|--------|-------------------|
| `Timestamp` | Разрешён | Дата/время (вместо `int64` unix) |
| `Duration` | Разрешён | Интервалы (TTL, timeout) |
| `Struct` | Разрешён с осторожностью | JSON-like metadata (когда схема неизвестна заранее) |
| `Any` | Запрещён | Никогда — используйте `oneof` для полиморфизма |

### Обработка ошибок

gRPC использует стандартные status codes (`grpc/codes`). Custom error details — через `google.rpc.Status.details`. В proto-файле контракта описать error scenarios в doc-comments.

```protobuf
service AuthService {
  // CreateToken создаёт JWT-токен.
  // Errors:
  //   INVALID_ARGUMENT — неверный grant_type
  //   UNAUTHENTICATED — неверные credentials
  //   RESOURCE_EXHAUSTED — rate limit exceeded
  rpc CreateToken(CreateTokenRequest) returns (CreateTokenResponse);

  // ValidateToken проверяет JWT-токен.
  // Errors:
  //   INVALID_ARGUMENT — пустой access_token
  //   UNAUTHENTICATED — токен невалиден или истёк
  rpc ValidateToken(ValidateTokenRequest) returns (ValidateTokenResponse);
}
```

| gRPC Code | Когда использовать |
|-----------|-------------------|
| `INVALID_ARGUMENT` | Неверные параметры запроса |
| `NOT_FOUND` | Ресурс не найден |
| `ALREADY_EXISTS` | Дубликат при создании |
| `UNAUTHENTICATED` | Нет или невалидный токен |
| `PERMISSION_DENIED` | Нет прав на операцию |
| `RESOURCE_EXHAUSTED` | Rate limit, квоты |
| `INTERNAL` | Непредвиденная ошибка сервера |

### Streaming

Паттерны для server, client и bidirectional streaming:

```protobuf
import "google/protobuf/timestamp.proto";

service NotificationService {
  // Server streaming — клиент подписывается, сервер отправляет поток уведомлений.
  rpc StreamNotifications(StreamRequest) returns (stream Notification);

  // Client streaming — клиент отправляет batch событий, сервер отвечает итогом.
  rpc BatchAcknowledge(stream AcknowledgeRequest) returns (AcknowledgeResponse);

  // Bidirectional — двусторонний обмен (чат, real-time sync).
  rpc LiveSync(stream SyncMessage) returns (stream SyncMessage);
}

message StreamRequest {
  string user_id = 1;
  repeated string event_types = 2;  // Фильтр по типу событий
}

message Notification {
  string notification_id = 1;
  string event_type = 2;
  string payload = 3;            // JSON-encoded event data
  google.protobuf.Timestamp created_at = 4;
}

message AcknowledgeRequest {
  string notification_id = 1;
}

message AcknowledgeResponse {
  int32 acknowledged_count = 1;
}

message SyncMessage {
  string message_id = 1;
  string channel = 2;
  bytes data = 3;
}
```

### Конфигурация buf

```yaml
# shared/contracts/protobuf/buf.yaml
version: v2
lint:
  use:
    - STANDARD        # Базовые правила buf
    - COMMENTS        # Doc-comments обязательны
  except:
    - PACKAGE_VERSION_SUFFIX  # Не требуем суффикс v1 в package
breaking:
  use:
    - FILE            # Проверка обратной совместимости на уровне файлов
```

```yaml
# shared/contracts/protobuf/buf.gen.yaml
version: v2
plugins:
  # Раскомментировать для нужного языка:
  # - remote: buf.build/protocolbuffers/go
  #   out: gen/go
  # - remote: buf.build/grpc/go
  #   out: gen/go
```

### Связь с SDD процессом

| Момент SDD | Действие с Protobuf |
|------------|---------------------|
| Design (INT-N sync gRPC) | Определяет содержание контракта в markdown |
| INFRA-блок (wave 0) | Dev-agent создаёт/обновляет `{svc}.proto` по INT-N |
| Per-service блок | Dev-agent реализует service handlers, buf lint |
| Design → DONE | `{svc}.proto` — финальная версия, `buf breaking` пройден |
| CONFLICT (shared/) | Изменение `{svc}.proto` = CONFLICT уровня Design |

```protobuf
// При Design → DONE: проверить обратную совместимость
// buf breaking shared/contracts/protobuf/ --against .git#branch=main
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| `import` из другого сервиса | Нарушает "провайдер владеет" — изменения в чужом .proto ломают ваш | Каждый .proto самодостаточный, без cross-service импортов |
| Reuse Request/Response между RPC | Coupling: изменение для одного RPC ломает другой | Отдельная пара Request/Response на каждый RPC |
| Field number reuse после удаления | Wire format incompatibility при десериализации старых данных | `reserved 4, 5;` — зарезервировать удалённые номера |
| `google.protobuf.Any` | Потеря type safety, сложная десериализация | Явные типы или `oneof` для полиморфизма |
| Отсутствие doc-comments | Контракт непонятен без чтения реализации | `//`-комментарии перед каждым service, rpc, message |
| Enum без `UNSPECIFIED = 0` | Нулевое значение — по умолчанию, отсутствие UNSPECIFIED означает реальный кейс как default | Всегда добавлять `{NAME}_UNSPECIFIED = 0` |

## Структура файлов

```
shared/contracts/protobuf/
├── buf.yaml           # Конфигурация buf (lint, breaking rules)
├── buf.gen.yaml       # Генерация кода (go, java, python targets)
├── auth.proto         # gRPC контракт для auth-сервиса
├── users.proto        # gRPC контракт для users-сервиса
└── README.md          # Конвенции и навигация по контрактам
```

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется линтером: `buf lint shared/contracts/protobuf/`. Breaking change detection: `buf breaking shared/contracts/protobuf/ --against .git#branch=main`. Pre-commit hook `protobuf-lint` запускает buf lint для изменённых .proto.*

## Тестирование

*Тестирование не применимо — Protobuf-файлы являются декларативными контрактами, не исполняемым кодом. Обратная совместимость проверяется через `buf breaking`.*

## Логирование

*Логирование не применимо — технология не генерирует событий, требующих логирования.*
