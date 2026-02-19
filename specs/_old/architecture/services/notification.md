---
description: Архитектура сервиса notification — уведомления в реальном времени через WebSocket и REST API.
service: notification
---

# notification

## Оглавление

- [Резюме](#резюме)
- [API контракты](#api-контракты)
- [Data Model](#data-model)
- [Code Map](#code-map)
- [Внешние зависимости](#внешние-зависимости)
- [Границы автономии LLM](#границы-автономии-llm)
- [Planned Changes](#planned-changes)
- [Changelog](#changelog)

---

## Резюме

*Сервис ещё не реализован.*

## API контракты

*Нет.*

## Data Model

*Нет.*

## Code Map

*Нет.*

## Внешние зависимости

*Нет.*

## Границы автономии LLM

*Нет.*

## Planned Changes

### design-0001: realtime notifications

> [Discussion 0001](../../discussion/disc-0001-realtime-notifications.md) →
> [Design 0001](../../design/design-0001-realtime-notifications.md) |
> Статус: WAITING

#### ADDED

**Резюме:** Основной сервис уведомлений. Управляет WebSocket-соединениями пользователей, подписывается на системные события от других сервисов через message broker, формирует уведомления и сохраняет в PostgreSQL. Доставляет уведомления в реальном времени через WebSocket, предоставляет REST API для истории и обновления статусов. TTL cleanup уведомлений старше 90 дней.

**API контракты:**

| Тип | Endpoint/Event | Метод | Описание |
|-----|---------------|-------|----------|
| REST | /api/v1/notifications | GET | Список уведомлений пользователя с пагинацией (limit, offset) |
| REST | /api/v1/notifications/{id} | PATCH | Обновление статуса уведомления (read/unread) |
| WebSocket | /ws/notifications | — | Push-уведомления в реальном времени |
| Event | system.events | subscribe | Подписка на системные события (UserRegistered, PasswordChanged, AdminAction, SystemError) |

**Data Model:**

| Сущность | Хранилище | Назначение |
|----------|-----------|-----------|
| Notification | PostgreSQL: notifications | id (UUID PK), user_id (UUID FK, index), type, title, body, status (default 'unread'), created_at (index) |
| WS Connection | Redis: ws:connections:{user_id} | Активные WebSocket session ID для маршрутизации уведомлений |

**Внешние зависимости:**

| Тип | Путь/Сервис | Что используем | Роль |
|-----|------------|---------------|------|
| shared | /shared/auth/ | JWT Middleware — валидация токенов | consumer |
| service | auth | INT-4: JWT Validation | consumer |
| service | frontend | INT-1: WebSocket Push Notifications | provider |
| service | frontend | INT-2: GET /api/v1/notifications | provider |
| service | frontend | INT-3: PATCH /api/v1/notifications/{id} | provider |
| service | * (любой) | INT-5: System Events через message broker | subscriber |

#### MODIFIED

*Нет (новый сервис).*

#### REMOVED

*Нет.*

## Changelog

*Нет записей.*
