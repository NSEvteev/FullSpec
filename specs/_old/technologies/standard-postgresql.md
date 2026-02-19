---
description: Стандарт кодирования PostgreSQL — конвенции именования, структура, паттерны.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/technologies/README.md
technology: postgresql
---

# Стандарт PostgreSQL

Версия стандарта: 1.0

Правила и конвенции кодирования на PostgreSQL в проекте.

**Полезные ссылки:**
- [Технологический реестр](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-postgresql.md](./validation-postgresql.md) |

## Оглавление

- [1. Версия и источники](#1-версия-и-источники)
- [2. Конвенции именования](#2-конвенции-именования)
- [3. Структура кода](#3-структура-кода)
- [4. Паттерны использования](#4-паттерны-использования)
- [5. Типичные ошибки](#5-типичные-ошибки)
- [6. Ссылки](#6-ссылки)

---

## 1. Версия и источники

| Параметр | Значение |
|----------|----------|
| Версия | 16 |
| Документация | https://www.postgresql.org/docs/16/ |
| Style guide | https://www.sqlstyle.guide/ |

---

## 2. Конвенции именования

| Элемент | Правило | Пример |
|---------|---------|--------|
| Таблицы | snake_case, множественное число | `notifications`, `user_preferences` |
| Колонки | snake_case, единственное число | `user_id`, `created_at`, `is_active` |
| Primary key | `id` (serial/UUID) | `id BIGSERIAL PRIMARY KEY` |
| Foreign key | `{referenced_table_singular}_id` | `user_id`, `notification_id` |
| Индексы | `idx_{table}_{columns}` | `idx_notifications_user_id` |
| Уникальные индексы | `uq_{table}_{columns}` | `uq_users_email` |
| Enum типы | snake_case, единственное число | `notification_status`, `event_type` |
| Функции | snake_case, глагол первым | `get_unread_count()`, `mark_as_read()` |
| Триггеры | `trg_{table}_{event}` | `trg_notifications_before_insert` |
| Миграции | `{NNN}_{description}.sql` | `001_create_notifications.sql` |

---

## 3. Структура кода

**Организация SQL-файлов:**
```
src/{service}/database/
├── migrations/          # Миграции (нумерованные)
│   ├── 001_create_tables.sql
│   └── 002_add_indexes.sql
├── seeds/               # Тестовые данные
│   └── seed_notifications.sql
└── queries/             # Именованные запросы (если используются)
    └── notifications.sql
```

**Порядок в миграции:**
1. CREATE TYPE (enums)
2. CREATE TABLE (в порядке зависимостей)
3. CREATE INDEX
4. CREATE FUNCTION / TRIGGER

**SQL-стиль:**
- Ключевые слова SQL — UPPER CASE: `SELECT`, `INSERT`, `WHERE`
- Идентификаторы — lower_snake_case
- Один statement на строку для читаемости
- Запятые в начале строки при перечислении колонок

---

## 4. Паттерны использования

**Timestamps:**
- Всегда `TIMESTAMPTZ` (с timezone), не `TIMESTAMP`
- `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()` + триггер на обновление

**Soft delete:**
- `deleted_at TIMESTAMPTZ` (nullable) вместо физического удаления
- Фильтр `WHERE deleted_at IS NULL` в запросах

**Пагинация:**
- Cursor-based: `WHERE id > :last_id ORDER BY id LIMIT :page_size`
- Offset-based только для UI с номерами страниц

**UUID vs Serial:**
- `BIGSERIAL` для внутренних ID
- `UUID` для публичных идентификаторов (API)

**Enum vs Reference table:**
- PostgreSQL ENUM для малых фиксированных наборов (< 10 значений)
- Reference table для изменяемых или расширяемых наборов

---

## 5. Типичные ошибки

**Без индекса на FK:**
```sql
-- Плохо: FK без индекса — медленные JOIN
ALTER TABLE notifications ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);

-- Хорошо: индекс на FK
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
ALTER TABLE notifications ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);
```

**TIMESTAMP вместо TIMESTAMPTZ:**
```sql
-- Плохо: без timezone
created_at TIMESTAMP NOT NULL DEFAULT NOW()

-- Хорошо: с timezone
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**SELECT * в production:**
```sql
-- Плохо: тянет все колонки
SELECT * FROM notifications WHERE user_id = :uid;

-- Хорошо: только нужные колонки
SELECT id, title, body, status, created_at
FROM notifications WHERE user_id = :uid;
```

**N+1 запросы:**
```sql
-- Плохо: цикл по users, затем SELECT для каждого
-- Хорошо: один JOIN или подзапрос
SELECT u.id, u.name, COUNT(n.id) AS unread
FROM users u
LEFT JOIN notifications n ON n.user_id = u.id AND n.status = 'unread'
GROUP BY u.id, u.name;
```

---

## 6. Ссылки

- [PostgreSQL 16 Documentation](https://www.postgresql.org/docs/16/)
- [SQL Style Guide](https://www.sqlstyle.guide/)
- [PostgreSQL Wiki: Don't Do This](https://wiki.postgresql.org/wiki/Don%27t_Do_This)
