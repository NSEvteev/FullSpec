---
type: standard
description: Формат пагинации — структура ответа, параметры, курсорная пагинация
related:
  - src/data/validation.md
  - src/data/errors.md
  - src/api/design.md
---

# Пагинация

Стандарт пагинации для API, возвращающих списки данных.

## Формат ответа

```json
{
  "data": [
    { "id": "usr_001", "name": "Иван" },
    { "id": "usr_002", "name": "Мария" },
    { "id": "usr_003", "name": "Пётр" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

## Поля pagination

| Поле | Тип | Описание |
|------|-----|----------|
| `page` | integer | Текущая страница (начиная с 1) |
| `limit` | integer | Количество элементов на странице |
| `total` | integer | Общее количество элементов |
| `total_pages` | integer | Общее количество страниц |

## Параметры запроса

### Стандартные параметры

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `page` | integer | 1 | Номер страницы |
| `limit` | integer | 20 | Элементов на странице |
| `sort` | string | — | Поле сортировки |
| `order` | string | asc | Направление: asc/desc |

### Примеры запросов

```
GET /api/v1/users?page=2&limit=10
GET /api/v1/orders?page=1&limit=50&sort=created_at&order=desc
GET /api/v1/products?page=3&limit=20&sort=price&order=asc
```

## Валидация параметров

### Ограничения

| Параметр | Мин. | Макс. | По умолчанию |
|----------|------|-------|--------------|
| `page` | 1 | — | 1 |
| `limit` | 1 | 100 | 20 |

### Ошибки валидации

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Ошибка валидации параметров пагинации",
    "details": {
      "fields": {
        "page": {
          "code": "OUT_OF_RANGE",
          "message": "Номер страницы должен быть положительным",
          "params": { "min": 1, "actual": 0 }
        },
        "limit": {
          "code": "OUT_OF_RANGE",
          "message": "Лимит должен быть от 1 до 100",
          "params": { "min": 1, "max": 100, "actual": 500 }
        }
      }
    },
    "request_id": "req_abc123"
  }
}
```

## Типы пагинации

### 1. Offset-based (стандартная)

**Использовать когда:**
- Нужен прямой доступ к странице
- Данные редко меняются
- Важна общая информация (total)

```
GET /api/v1/users?page=5&limit=20
```

```json
{
  "data": [...],
  "pagination": {
    "page": 5,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

### 2. Cursor-based (курсорная)

**Использовать когда:**
- Данные часто меняются
- Большие объёмы данных
- Real-time ленты

```
GET /api/v1/feed?limit=20&cursor=eyJpZCI6MTIzNH0=
```

```json
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "has_more": true,
    "next_cursor": "eyJpZCI6MTI1NH0=",
    "prev_cursor": "eyJpZCI6MTIxNH0="
  }
}
```

### 3. Keyset-based (по ключу)

**Использовать когда:**
- Сортировка по уникальному полю
- Нужна высокая производительность

```
GET /api/v1/logs?after_id=log_12345&limit=50
```

```json
{
  "data": [...],
  "pagination": {
    "limit": 50,
    "has_more": true,
    "last_id": "log_12395"
  }
}
```

## Примеры ответов

### Первая страница

```json
{
  "data": [
    { "id": "usr_001", "name": "Иван", "email": "ivan@example.com" },
    { "id": "usr_002", "name": "Мария", "email": "maria@example.com" }
  ],
  "pagination": {
    "page": 1,
    "limit": 2,
    "total": 150,
    "total_pages": 75
  }
}
```

### Последняя страница

```json
{
  "data": [
    { "id": "usr_149", "name": "Алексей", "email": "alexey@example.com" },
    { "id": "usr_150", "name": "Елена", "email": "elena@example.com" }
  ],
  "pagination": {
    "page": 75,
    "limit": 2,
    "total": 150,
    "total_pages": 75
  }
}
```

### Пустой результат

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 0,
    "total_pages": 0
  }
}
```

### Страница за пределами

```json
{
  "data": [],
  "pagination": {
    "page": 100,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

## Сортировка

### Формат параметров

```
GET /api/v1/products?sort=price&order=asc
GET /api/v1/products?sort=created_at&order=desc
```

### Множественная сортировка

```
GET /api/v1/products?sort=category,price&order=asc,desc
```

### Ответ с информацией о сортировке

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  },
  "sort": {
    "field": "created_at",
    "order": "desc"
  }
}
```

## Фильтрация

### Совместимость с пагинацией

```
GET /api/v1/orders?status=completed&page=1&limit=20
GET /api/v1/users?role=admin&created_after=2026-01-01&page=1
```

### Ответ с фильтрами

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "total_pages": 3
  },
  "filters": {
    "status": "completed"
  }
}
```

## Метаданные

### Расширенный формат

```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": true
  },
  "links": {
    "self": "/api/v1/users?page=2&limit=20",
    "first": "/api/v1/users?page=1&limit=20",
    "last": "/api/v1/users?page=8&limit=20",
    "next": "/api/v1/users?page=3&limit=20",
    "prev": "/api/v1/users?page=1&limit=20"
  }
}
```

## Производительность

### Рекомендации

| Ситуация | Решение |
|----------|---------|
| > 10K записей | Использовать курсорную пагинацию |
| Частые изменения | Использовать курсорную пагинацию |
| Нужен total | Кешировать count отдельно |
| Глубокая пагинация | Ограничить page * limit |

### Оптимизация count

```sql
-- ❌ Медленно на больших таблицах
SELECT COUNT(*) FROM users WHERE status = 'active';

-- ✅ Использовать приблизительный count
SELECT reltuples FROM pg_class WHERE relname = 'users';

-- ✅ Или кешировать результат
SELECT cached_count FROM counters WHERE table_name = 'users';
```

## Антипаттерны

```json
// ❌ Неправильно: page начинается с 0
{
  "pagination": {
    "page": 0,
    "limit": 20
  }
}

// ❌ Неправильно: нет total_pages
{
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}

// ❌ Неправильно: данные не в массиве data
{
  "users": [...],
  "pagination": {...}
}

// ❌ Неправильно: разные имена полей
{
  "items": [...],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total_count": 150
  }
}

// ✅ Правильно: единообразный формат
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование API с пагинацией |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при изменении формата |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |

---

## Связанные инструкции

- [validation.md](validation.md) — Валидация параметров пагинации
- [errors.md](errors.md) — Формат ошибок при неверных параметрах
- [src/api/design.md](../api/design.md) — Общие принципы дизайна API
