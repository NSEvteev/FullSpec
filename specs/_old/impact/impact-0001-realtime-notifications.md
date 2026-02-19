---
description: Импакт-анализ системы уведомлений в реальном времени — 4 новых сервиса (notification, frontend, gateway, auth), WebSocket hub, PostgreSQL + Redis, UI-компоненты, межсервисные зависимости и риски масштабирования.
standard: specs/.instructions/impact/standard-impact.md
standard-version: v1.0
index: specs/impact/README.md
parent: discussion/disc-0001-realtime-notifications.md
children:
  - design/design-0001-realtime-notifications.md
status: WAITING
milestone: v0.1.0
---

# impact-0001: Система уведомлений в реальном времени

## 📋 Резюме

Реализация системы уведомлений затрагивает 4 сервиса (2 основных + 2 вторичных), все — новые. Основной scope: создание notification-сервиса с WebSocket hub и PostgreSQL-хранилищем, UI-компонентов на фронтенде, WebSocket proxy в gateway и JWT-аутентификация через auth. Ключевые risk areas: надёжность WebSocket-соединений при масштабировании, потеря уведомлений при даунтайме notification-сервиса, утечка zombie-соединений.

## SVC-1: notification

**Тип влияния:** Новый (план создания) | **Уверенность:** Предположительно

Когда пользователь регистрируется, меняет пароль или администратор выполняет действие — исходный сервис публикует событие в message broker. Event Consumer подписан на эти события, формирует из них уведомление и сохраняет в PostgreSQL. Одновременно WebSocket Hub проверяет, есть ли у целевого пользователя активное WS-соединение (через Redis), и если есть — пушит уведомление в реальном времени. Для доступа к истории уведомлений предоставляется REST API с пагинацией и управлением статусами read/unread.

### 📦 Компоненты

| ID | Компонент | Scope | Изменение |
|----|-----------|-------|-----------|
| CMP-1 | WebSocket Hub | local | Новый — управление WebSocket-соединениями, broadcast уведомлений целевым пользователям |
| CMP-2 | Event Consumer | local | Новый — подписка на системные события от других сервисов, формирование уведомлений |
| CMP-3 | Notification Repository | local | Новый — CRUD-операции с уведомлениями в PostgreSQL, пагинация, TTL cleanup |
| CMP-10 | JWT Middleware | shared (auth) | Новый — валидация JWT при REST-запросах к API уведомлений (shared с gateway) |

### 💾 Данные и хранение

| ID | Хранилище | Изменение |
|----|-----------|-----------|
| DATA-1 | PostgreSQL | Новая таблица `notifications`: id (UUID PK), user_id (UUID FK, index), type (VARCHAR), title (VARCHAR), body (TEXT), status (VARCHAR, default 'unread'), created_at (TIMESTAMP, index) |
| DATA-2 | Redis | Новый key-space `ws:connections:{user_id}` — хранение активных WebSocket session ID для маршрутизации уведомлений |

### 🔌 API

| ID | Эндпоинт | Изменение | Совместимость |
|----|----------|-----------|---------------|
| API-1 | GET /api/v1/notifications | Новый — список уведомлений пользователя с пагинацией (limit, offset) | N/A |
| API-2 | PATCH /api/v1/notifications/{id} | Новый — обновление статуса уведомления (read/unread) | N/A |
| API-3 | WS /ws/notifications | Новый — WebSocket-эндпоинт для push-уведомлений в реальном времени | N/A |

## SVC-2: frontend

**Тип влияния:** Новый (план создания) | **Уверенность:** Предположительно

При загрузке приложения WebSocketClient устанавливает соединение с notification-сервисом через gateway. Когда приходит новое уведомление по WS — отображается toast в правом верхнем углу (auto-dismiss 5s), badge на bell-иконке увеличивается. Пользователь кликает на bell — открывается dropdown со списком уведомлений (подгружаются через REST API). При клике на уведомление — оно помечается прочитанным через PATCH, badge обновляется. При обрыве соединения WebSocketClient выполняет reconnect с exponential backoff.

### 📦 Компоненты

| ID | Компонент | Scope | Изменение |
|----|-----------|-------|-----------|
| CMP-4 | NotificationBell | local | Новый — bell-иконка с badge-счётчиком непрочитанных |
| CMP-5 | NotificationDropdown | local | Новый — dropdown-список уведомлений с пагинацией |
| CMP-6 | ToastNotification | local | Новый — toast-компонент для новых уведомлений (auto-dismiss 5s) |
| CMP-7 | WebSocketClient | shared (notification) | Новый — WebSocket-клиент с exponential backoff reconnect |

### 💾 Данные и хранение

_Изменений в данных нет._

### 🔌 API

_Изменений в API нет._

## SVC-3: gateway

**Тип влияния:** Новый (план создания) | **Уверенность:** Предположительно

Когда клиент инициирует WebSocket-соединение, запрос приходит в gateway. JWT Middleware извлекает токен из параметров handshake и валидирует его через auth-сервис. После успешной аутентификации WebSocket Proxy выполняет upgrade и проксирует соединение на notification-сервис. Rate limiting ограничивает количество одновременных WS-соединений (max 10 на пользователя).

### 📦 Компоненты

| ID | Компонент | Scope | Изменение |
|----|-----------|-------|-----------|
| CMP-8 | WebSocket Proxy | local | Новый — проксирование WebSocket upgrade-запросов на notification-сервис |
| CMP-9 | JWT Middleware | shared (auth) | Новый — валидация JWT при HTTP и WebSocket handshake |

### 💾 Данные и хранение

_Изменений в данных нет._

### 🔌 API

| ID | Эндпоинт | Изменение | Совместимость |
|----|----------|-----------|---------------|
| API-4 | WS /ws/* | Новый — WebSocket proxy route на notification-сервис | N/A |

## SVC-4: auth

**Тип влияния:** Новый (план создания) | **Уверенность:** Предположительно

При логине пользователя auth выпускает JWT-токен. Notification-сервис и gateway потребляют этот токен для аутентификации — gateway при WebSocket handshake, notification при валидации REST-запросов к API уведомлений. Auth не инициирует взаимодействие с notification напрямую, но является обязательной зависимостью для всей цепочки аутентификации.

### 📦 Компоненты

_Компоненты не идентифицированы._

### 💾 Данные и хранение

_Изменений в данных нет._

### 🔌 API

_Изменений в API нет._

## 🔗 Зависимости

| ID | От сервиса | К сервису | Тип | Описание | Версия контракта |
|----|-----------|----------|-----|----------|------------------|
| DEP-1 | gateway | notification | sync | WebSocket proxy: gateway проксирует WS upgrade-запросы на notification-сервис | /v1 |
| DEP-2 | notification | auth | sync | JWT-валидация: notification-сервис проверяет токен при WebSocket handshake через auth-сервис | /v1 |
| DEP-3 | * (любой сервис) | notification | async | Публикация событий: сервисы отправляют системные события (регистрация, смена пароля, действия админа, ошибки) в notification через message broker | |

## ⚠️ Риски

| ID | Риск | Вероятность | Влияние | Mitigation |
|----|------|-------------|---------|------------|
| RISK-1 | Потеря уведомлений при падении notification-сервиса — события, отправленные во время даунтайма, не будут доставлены | Средняя | Высокое | Использовать persistent message broker (RabbitMQ/Kafka) с гарантией at-least-once delivery |
| RISK-2 | Утечка WebSocket-соединений (zombie connections) при некорректном disconnect — рост потребления памяти | Средняя | Среднее | Таймаут неактивных соединений, периодическая очистка Redis от stale sessions |
| RISK-3 | Превышение лимита 1000 одновременных WebSocket-соединений на инстанс при росте пользователей | Низкая | Высокое | Горизонтальное масштабирование notification-сервиса + Redis pub/sub для синхронизации между инстансами |
