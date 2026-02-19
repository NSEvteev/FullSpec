---
description: Домен Notifications — управление уведомлениями в реальном времени, доставка через WebSocket и REST.
---

# Домен: Notifications

## Агрегаты

| Агрегат | Описание | Сервис |
|---------|----------|--------|
| Notification | Уведомление (тип, заголовок, тело, статус read/unread, TTL) | notification |
| WebSocketConnection | Активное WS-соединение пользователя | notification |
| NotificationUI | Компоненты отображения (bell, dropdown, toast) | frontend |

## Доменные события

| Событие | Издатель | Потребители |
|---------|----------|------------|
| NotificationCreated | notification (Event Consumer) | notification (WebSocket Hub → frontend) |
| NotificationRead | notification | frontend |

## Инварианты

- Одно уведомление принадлежит одному пользователю
- Уведомление не может быть помечено как read до доставки
- TTL уведомлений — 90 дней (cleanup)
- Max 10 одновременных WebSocket-соединений на пользователя (rate limit gateway)

## Planned Changes

- **[design-0001: realtime notifications](../../design/design-0001-realtime-notifications.md)**
  Статус: WAITING | Домен создан этим Design

## Changelog

*Нет записей.*
