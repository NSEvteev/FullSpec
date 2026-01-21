# Database Template

> **Источник:** [/.claude/instructions/doc/structure.md](/.claude/instructions/doc/structure.md#шаблон-database-schema-migrations)

Шаблон документации для схем баз данных и миграций.

---

## Шаблон

```markdown
# {Название схемы/миграции}

> Исходный код: [{filename}](/{path-to-source})

{Описание изменений в БД}

## Таблицы

### {table_name}

{Описание таблицы}

| Колонка | Тип | Nullable | Описание |
|---------|-----|:--------:|----------|
| id | UUID | - | Первичный ключ |
| {column} | {type} | +/- | {description} |

**Индексы:**
- `idx_{name}` — {columns} ({description})

**Foreign keys:**
- `{column}` -> `{table}.{column}`

## Миграции

| Версия | Описание |
|--------|----------|
| 0001 | Создание таблицы |
| 0002 | Добавление колонки |
```

---

<!-- Пример заполнения

# Users Schema

> Исходный код: [schema.sql](/src/users/database/schema.sql)

Схема базы данных для хранения информации о пользователях системы.

## Таблицы

### users

Основная таблица пользователей.

| Колонка | Тип | Nullable | Описание |
|---------|-----|:--------:|----------|
| id | UUID | - | Первичный ключ |
| email | VARCHAR(255) | - | Email пользователя (уникальный) |
| password_hash | VARCHAR(255) | - | Хеш пароля (bcrypt) |
| name | VARCHAR(100) | + | Отображаемое имя |
| role | VARCHAR(50) | - | Роль: user, admin, moderator |
| created_at | TIMESTAMP | - | Дата создания |
| updated_at | TIMESTAMP | - | Дата последнего обновления |
| deleted_at | TIMESTAMP | + | Soft delete timestamp |

**Индексы:**
- `idx_users_email` — email (уникальный, для поиска при логине)
- `idx_users_role` — role (для фильтрации по ролям)
- `idx_users_created_at` — created_at (для сортировки)

**Foreign keys:**
- нет

### user_sessions

Таблица активных сессий пользователей.

| Колонка | Тип | Nullable | Описание |
|---------|-----|:--------:|----------|
| id | UUID | - | Первичный ключ |
| user_id | UUID | - | ID пользователя |
| refresh_token | VARCHAR(255) | - | Refresh токен |
| expires_at | TIMESTAMP | - | Время истечения |
| ip_address | INET | + | IP адрес клиента |
| user_agent | TEXT | + | User-Agent браузера |

**Индексы:**
- `idx_sessions_user_id` — user_id (для получения сессий пользователя)
- `idx_sessions_expires_at` — expires_at (для очистки устаревших)

**Foreign keys:**
- `user_id` -> `users.id` (ON DELETE CASCADE)

## Миграции

| Версия | Описание |
|--------|----------|
| 0001 | Создание таблицы users |
| 0002 | Добавление soft delete (deleted_at) |
| 0003 | Создание таблицы user_sessions |
| 0004 | Добавление индекса idx_users_role |

-->
