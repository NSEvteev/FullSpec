---
description: Потоки данных между сервисами — участники, контракты, паттерны взаимодействия.
---

# Потоки данных

## {от} → {к}: {назначение}

| Поле | Значение |
|------|----------|
| Участники | {от} ({роль}) → {к} ({роль}) |
| Контракт | {контракт} |
| Паттерн | {sync/gRPC | async/events} |
| Протокол | {протокол} |

## Planned Changes

- **[design-0001: realtime notifications](../../design/design-0001-realtime-notifications.md)**
  Статус: WAITING | 5 блоков взаимодействия:
  - **INT-1:** notification → frontend (через gateway) — WebSocket push notifications (async, WebSocket)
  - **INT-2:** notification → frontend — GET /api/v1/notifications (sync, REST)
  - **INT-3:** notification → frontend — PATCH /api/v1/notifications/{id} (sync, REST)
  - **INT-4:** auth → gateway, notification — POST /api/v1/auth/validate (sync, REST)
  - **INT-5:** * → notification — системные события через message broker (async, events)

## Changelog

*Нет записей.*
