---
description: Архитектура сервиса auth — аутентификация, генерация и валидация JWT.
service: auth
---

# auth

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

**Резюме:** Сервис аутентификации. Генерирует JWT-токены при логине пользователя, предоставляет endpoint для валидации токенов по запросу от gateway и notification. Хранит секретные ключи для подписи JWT.

**API контракты:**

| Тип | Endpoint/Event | Метод | Описание |
|-----|---------------|-------|----------|
| REST | /api/v1/auth/validate | POST | Валидация JWT-токена по запросу от других сервисов |

**Внешние зависимости:**

| Тип | Путь/Сервис | Что используем | Роль |
|-----|------------|---------------|------|
| service | gateway | INT-4: JWT Validation | provider |
| service | notification | INT-4: JWT Validation | provider |

#### MODIFIED

*Нет (новый сервис).*

#### REMOVED

*Нет.*

## Changelog

*Нет записей.*
