---
description: example — демонстрационный сервис для иллюстрации формата документации {svc}.md.
standard: specs/.instructions/docs/service/standard-service.md
standard-version: v1.2
criticality: critical-low
---

# example

## Назначение

Example — демонстрационный сервис для иллюстрации формата документации. Показывает структуру всех 10 секций `{svc}.md`. Основные потребители: разработчики, изучающие формат. Взаимодействие: REST API.

**Обоснование критичности:** `critical-low` — демонстрационный сервис без бизнес-функций. Недоступность не влияет на пользователей и revenue.

## API контракты

Сервис предоставляет REST API для CRUD операций над примерами. Все endpoint-ы следуют конвенциям из [conventions.md](.system/conventions.md).

### GET /api/v1/examples

Получение списка примеров с пагинацией.

- **Auth:** Bearer JWT (обязательно)
- **Паттерн:** sync | **Протокол:** REST/JSON

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| limit | int | нет (default 10, max 100) | Количество |
| cursor | string | нет | Курсор пагинации |

**Response 200:**
```json
{
  "data": [
    { "id": "ex-001", "title": "First example", "created_at": "2026-01-01T00:00:00Z" }
  ],
  "cursor": "next-abc"
}
```

**Errors:** 401 Unauthorized, 422 Validation Error

---

### POST /api/v1/examples

Создание нового примера.

- **Auth:** Bearer JWT (обязательно)
- **Паттерн:** sync | **Протокол:** REST/JSON

**Request:**
```json
{
  "title": "New example",
  "description": "Optional description"
}
```

**Response 201:**
```json
{
  "data": { "id": "ex-002", "title": "New example", "created_at": "2026-01-01T12:00:00Z" }
}
```

**Errors:** 401 Unauthorized, 422 Validation Error

## Data Model

PostgreSQL — основное хранилище примеров (таблица `examples`).

### examples (PostgreSQL)

| Колонка | Тип | Constraints | Описание |
|---------|-----|------------|----------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Идентификатор |
| title | VARCHAR(255) | NOT NULL | Название |
| description | TEXT | NULL | Описание |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Дата создания |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Дата обновления |

**Индексы:**
- `idx_examples_created_at` — по created_at DESC (сортировка, пагинация)

## Потоки

Общий паттерн: запрос приходит через REST API, routes валидирует, services обрабатывает бизнес-логику, repositories сохраняет в PostgreSQL. Чтобы добавить новый endpoint — создать route, service-метод и repository-метод.

### Создание примера (основной)

```
1. Client → POST /api/v1/examples с JSON body
2. example.routes валидирует входные данные
3. example.services обрабатывает бизнес-логику
4. example.repositories записывает в PostgreSQL
5. Client получает 201 с данными примера
```

## Code Map

### Tech Stack

| Технология | Версия | Назначение | Стандарт |
|-----------|--------|-----------|---------|
| Node.js | 20 | Runtime | — |
| Express | 4 | API-фреймворк | — |
| PostgreSQL | 16 | Хранение данных | — |
| Prisma | — | ORM | — |

### Пакеты

Сервис разделён на 3 пакета: routes (точка входа), services (бизнес-логика), repositories (хранение).

| Пакет | Назначение | Ключевые модули |
|-------|-----------|----------------|
| `example.routes` | REST API — endpoints, валидация | `index.ts` |
| `example.services` | Бизнес-логика | `example.service.ts` |
| `example.repositories` | Data access — PostgreSQL queries | `example.repository.ts` |

### Точки входа

- API: `example/backend/src/routes/index.ts`

### Внутренние зависимости

example.routes → example.services → example.repositories

### Makefile таргеты

| Таргет | Команда | Описание |
|--------|---------|----------|
| test | `make test-example` | Unit + integration тесты сервиса |
| lint | `make lint-example` | Линтинг кода сервиса |

## Зависимости

Example зависит от auth (критическая — без JWT-валидации REST не работает). Прямых sync-вызовов к другим сервисам нет.

### auth — валидация JWT
Example использует auth-сервис для валидации JWT-токенов через shared/auth middleware. Если auth недоступен — все запросы возвращают 401.
Паттерн: **Conformist** (example конформен к API auth).
См. [auth.md](auth.md).

## Доменная модель

Example реализует домен Examples. Основная сущность — Example — проходит жизненный цикл: создание → обновление → удаление.

### Агрегаты

| Агрегат | Описание |
|---------|----------|
| Example | Пример (title, description). Жизненный цикл: created → updated → deleted |

### Инварианты

- Title не пустой, длина <= 255 символов

### Доменные события

| Событие | Описание |
|---------|----------|
| ExampleCreated | Новый пример создан |
| ExampleUpdated | Пример обновлён |
| ExampleDeleted | Пример удалён |

## Границы автономии LLM

- **Свободно:** CRUD операции, валидация, тесты, рефакторинг внутренней логики
- **Флаг:** изменение схемы БД, новые API endpoints (может затронуть тесты)
- **CONFLICT:** изменение контракта (breaking changes), изменение data model

## Planned Changes

*Planned Changes не применимо — демонстрационный сервис без активных analysis/.*

## Changelog

- **Создание сервиса** | DONE 2026-02-19
  Создан как пример формата документации {svc}.md.
