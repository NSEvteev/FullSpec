---
description: Архитектура сервиса frontend — клиентское приложение, UI компоненты уведомлений.
service: frontend
---

# frontend

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

**Резюме:** Клиентское приложение уведомлений. При загрузке устанавливает WebSocket-соединение с notification через gateway, отображает toast-нотификации и bell с badge-счётчиком непрочитанных. Подгружает историю уведомлений через REST API, обновляет статусы read/unread. Reconnect с exponential backoff при обрыве соединения.

**Внешние зависимости:**

| Тип | Путь/Сервис | Что используем | Роль |
|-----|------------|---------------|------|
| service | notification (через gateway) | INT-1: WebSocket Push Notifications | consumer |
| service | notification | INT-2: GET /api/v1/notifications | consumer |
| service | notification | INT-3: PATCH /api/v1/notifications/{id} | consumer |

#### MODIFIED

*Нет (новый сервис).*

#### REMOVED

*Нет.*

## Changelog

*Нет записей.*
