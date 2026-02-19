---
description: Инфраструктура проекта — deployment, networking, мониторинг.
---

# Инфраструктура

## Deployment

| Окружение | Технология | Конфигурация |
|-----------|-----------|-------------|
| dev | {технология} | config/dev/ |
| staging | {технология} | config/staging/ |
| prod | {технология} | config/prod/ |

## Networking

{Путь запроса, DNS, Network Policies}

## Мониторинг

{Метрики, логи, трейсинг, алерты}

## Planned Changes

- **[design-0001: realtime notifications](../../design/design-0001-realtime-notifications.md)**
  Статус: WAITING | Затрагивает инфраструктуру:
  - **WebSocket:** gateway проксирует WS upgrade-запросы на notification (rate limiting: max 10 WS на пользователя)
  - **Redis:** хранение активных WebSocket-соединений пользователей (notification)
  - **PostgreSQL:** хранение уведомлений (notification), TTL cleanup 90 дней
  - **Message broker:** канал `system.events` для async event-driven коммуникации (INT-5)

## Changelog

*Нет записей.*
