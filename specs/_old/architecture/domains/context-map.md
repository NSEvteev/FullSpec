---
description: Карта взаимодействия между bounded contexts — домены, ответственности, паттерны связей.
---

# Context Map

## Домены

### {Domain Name} — {краткое описание}

**Ответственность:** {что делает домен}

**Сервисы:** `{service1}`, `{service2}`

**Ключевые инварианты:**
- {инвариант 1}

## Связи между контекстами

| Upstream | Downstream | Паттерн | Описание |
|----------|-----------|---------|----------|
| {Domain1} | {Domain2} | {паттерн} | {описание} |

## Planned Changes

- **[design-0001: realtime notifications](../../design/design-0001-realtime-notifications.md)**
  Статус: WAITING | Затрагивает: домен Notifications (notification, frontend), домен Identity (auth, gateway)

## Changelog

*Нет записей.*
