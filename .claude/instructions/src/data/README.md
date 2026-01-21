# /src/data/ -- Форматы данных

Стандарты форматов данных: ошибки, логирование, валидация, пагинация.

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Errors](#1-errors) | [errors.md](./errors.md) | Единый формат ошибок API -- структура, коды, локализация |
| [2. Logging](#2-logging) | [logging.md](./logging.md) | Structured JSON logging -- формат, уровни, контекст, трейсинг |
| [3. Validation](#3-validation) | [validation.md](./validation.md) | Валидация входных данных -- правила, форматы ошибок, JSON Schema |
| [4. Pagination](#4-pagination) | [pagination.md](./pagination.md) | Формат пагинации -- структура ответа, параметры, курсорная пагинация |

---

## 1. Errors

**Файл:** [errors.md](./errors.md)

**Тип:** standard

**Описание:** Единый формат ответов об ошибках для всех API сервисов.

**Ключевые правила:**
- Структура: `{ "error": { "code", "message", "details", "request_id" } }`
- Код в UPPER_SNAKE_CASE: `VALIDATION_ERROR`, `NOT_FOUND`
- Обязательный `request_id` для трейсинга
- Клиентские ошибки (4xx) и серверные (5xx)

**Связанные инструкции:**
- [validation.md](./validation.md) -- детали ошибок валидации
- [logging.md](./logging.md) -- логирование ошибок
- [../api/design.md](../api/design.md) -- HTTP статус-коды

---

## 2. Logging

**Файл:** [logging.md](./logging.md)

**Тип:** standard

**Описание:** Стандарт структурированного логирования в формате JSON.

**Ключевые правила:**
- Формат: JSON с обязательными полями (timestamp, level, service, request_id, message)
- Уровни: FATAL, ERROR, WARN, INFO, DEBUG, TRACE
- Production: INFO и выше, Staging: DEBUG и выше
- Контекст события в поле `context`

**Связанные инструкции:**
- [errors.md](./errors.md) -- логирование ошибок
- [../../platform/observability/logging.md](../../platform/observability/logging.md) -- инфраструктура (Loki)

---

## 3. Validation

**Файл:** [validation.md](./validation.md)

**Тип:** standard

**Описание:** Стандарт валидации входных данных для API и внутренних сервисов.

**Ключевые правила:**
- Fail fast -- валидация на входе, до бизнес-логики
- Все ошибки за один запрос, не по одной
- Коды ошибок полей: `REQUIRED`, `INVALID_FORMAT`, `TOO_SHORT`, `OUT_OF_RANGE`
- JSON Schema для определения схем

**Связанные инструкции:**
- [errors.md](./errors.md) -- общий формат ошибок
- [pagination.md](./pagination.md) -- валидация параметров пагинации
- [../api/design.md](../api/design.md) -- проектирование API

---

## 4. Pagination

**Файл:** [pagination.md](./pagination.md)

**Тип:** standard

**Описание:** Стандарт пагинации для API, возвращающих списки данных.

**Ключевые правила:**
- Структура: `{ "data": [...], "pagination": { page, limit, total, total_pages } }`
- Параметры: `page` (от 1), `limit` (1-100, default 20), `sort`, `order`
- Курсорная пагинация для больших наборов данных
- Ограничение limit: максимум 100

**Связанные инструкции:**
- [validation.md](./validation.md) -- валидация параметров
- [errors.md](./errors.md) -- ошибки пагинации
- [../api/design.md](../api/design.md) -- URL для списков

---

## Граф связей

```
                    ┌───────────────┐
                    │  errors.md    │
                    │(формат ошибок)│
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
    ┌─────────────┐  ┌───────────┐  ┌──────────────┐
    │validation.md│  │logging.md │  │ ../api/      │
    │(field errors)│ │(log errors)│ │ design.md    │
    └──────┬──────┘  └─────┬─────┘  └──────────────┘
           │               │
           ▼               ▼
    ┌─────────────┐  ┌─────────────────────────┐
    │pagination.md│  │ platform/observability/ │
    │(param valid.)│ │ logging.md              │
    └─────────────┘  └─────────────────────────┘
```

---

## Когда какую инструкцию читать

| Ситуация | Инструкция |
|----------|------------|
| Формирую ответ об ошибке | errors.md |
| Выбираю HTTP статус-код ошибки | errors.md |
| Добавляю логирование в сервис | logging.md |
| Выбираю уровень логирования | logging.md |
| Валидирую входные данные | validation.md |
| Определяю JSON Schema | validation.md |
| Возвращаю список с пагинацией | pagination.md |
| Реализую курсорную пагинацию | pagination.md |

---

## Связанные разделы

- [../api/](../api/) -- проектирование API (статус-коды, URL)
- [../runtime/](../runtime/) -- runtime (health checks, resilience)
- [../../platform/observability/](../../platform/observability/) -- инфраструктура логирования
