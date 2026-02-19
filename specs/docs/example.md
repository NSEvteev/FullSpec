# Example Service

Пример сервисного документа — демонстрирует все 10 секций.

## 1. Назначение

Example — демонстрационный сервис для иллюстрации формата документации. Зона ответственности: показать структуру `{svc}.md`.

## 2. API контракты

### GET /api/v1/examples

Получение списка примеров.

**Request:** `GET /api/v1/examples?limit=10&cursor=abc`

**Response (200):**
```json
{
  "data": [
    { "id": "ex-001", "title": "First example", "created_at": "2026-01-01T00:00:00Z" }
  ],
  "cursor": "next-abc"
}
```

### POST /api/v1/examples

Создание нового примера.

**Request:**
```json
{
  "title": "New example",
  "description": "Optional description"
}
```

**Response (201):**
```json
{
  "data": { "id": "ex-002", "title": "New example", "created_at": "2026-01-01T12:00:00Z" }
}
```

## 3. Data Model

### examples

| Колонка | Тип | Constraints | Описание |
|---------|-----|-------------|----------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Идентификатор |
| title | VARCHAR(255) | NOT NULL | Название |
| description | TEXT | NULL | Описание |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Дата создания |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Дата обновления |

**Индексы:**
- `idx_examples_created_at` — `created_at DESC`

## 4. Потоки

### Создание примера

1. Client → `POST /api/v1/examples` с JSON body
2. Example Service валидирует входные данные
3. Example Service записывает в PostgreSQL
4. Example Service публикует событие `example.created`
5. Client получает 201 с данными примера

## 5. Code Map

**Tech Stack:**
- Runtime: Node.js 20
- Framework: Express 4
- Database: PostgreSQL 16
- ORM: Prisma

**Структура:**
```
src/example/
├── backend/
│   ├── src/
│   │   ├── routes/       # Express routes
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Data access
│   │   └── index.ts      # Entry point
│   └── package.json
├── database/
│   └── migrations/
└── tests/
```

## 6. Зависимости

### auth — валидация JWT

Example использует auth-сервис для валидации JWT-токенов. См. auth.md (секция "API контракты").

## 7. Доменная модель

**Агрегат: Example**
- Инварианты: title не пустой, длина <= 255
- Доменные события: `example.created`, `example.updated`, `example.deleted`

## 8. Границы автономии LLM

| Уровень | Действие |
|---------|----------|
| Свободно | CRUD операции, валидация, тесты |
| Флаг | Изменение схемы БД, новые API endpoints |
| CONFLICT | Изменение контракта (breaking changes) |

## 9. Planned Changes

*Нет активных изменений.*

## 10. Changelog

| Дата | Изменение | Ссылка |
|------|----------|--------|
| 2026-02-19 | Создан пример сервисного документа | — |
