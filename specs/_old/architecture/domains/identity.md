---
description: Домен Identity — аутентификация, авторизация, JWT-валидация, проксирование запросов.
---

# Домен: Identity

## Агрегаты

| Агрегат | Описание | Сервис |
|---------|----------|--------|
| JWTToken | Токен аутентификации (генерация, валидация, подпись) | auth |
| WebSocketProxy | Проксирование WS upgrade-запросов с аутентификацией | gateway |

## Доменные события

| Событие | Издатель | Потребители |
|---------|----------|------------|
| UserRegistered | auth | notification (INT-5) |
| PasswordChanged | auth | notification (INT-5) |

## Инварианты

- JWT-токен подписан секретным ключом auth
- Валидация токена — синхронная (REST, INT-4)
- Gateway не хранит состояние пользователя — проксирует после валидации

## Planned Changes

- **[design-0001: realtime notifications](../../design/design-0001-realtime-notifications.md)**
  Статус: WAITING | Домен создан этим Design

## Changelog

*Нет записей.*
