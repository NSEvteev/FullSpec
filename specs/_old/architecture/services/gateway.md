---
description: Архитектура сервиса gateway — API Gateway, WebSocket proxy и rate limiting.
service: gateway
---

# gateway

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

**Резюме:** API Gateway для WebSocket-соединений. Проксирует WebSocket upgrade-запросы на notification, выполняет JWT-валидацию при handshake через shared JWT Middleware из /shared/auth/, ограничивает количество одновременных WS-соединений (max 10 на пользователя).

**API контракты:**

| Тип | Endpoint/Event | Метод | Описание |
|-----|---------------|-------|----------|
| WebSocket | /ws/* | — | WebSocket proxy route на notification-сервис |

**Внешние зависимости:**

| Тип | Путь/Сервис | Что используем | Роль |
|-----|------------|---------------|------|
| shared | /shared/auth/ | JWT Middleware — валидация токенов при WS handshake | consumer |
| service | auth | INT-4: JWT Validation | consumer |
| service | notification | WebSocket proxy target | consumer |

#### MODIFIED

*Нет (новый сервис).*

#### REMOVED

*Нет.*

## Changelog

*Нет записей.*
