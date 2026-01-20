---
type: standard
description: Документирование кода: ссылки на /doc/, комментарии, README
related:
  - doc/structure.md      # структура документации, зеркалирование
  - git/issues.md         # создание Issue при удалении документации
---

# Документирование кода

Правила документирования исходного кода в `/src/`. Обеспечивает связь между кодом и документацией.

## Оглавление

- [Структура сервиса](#структура-сервиса)
- [Правила](#правила)
- [Workflow](#workflow)
- [Скиллы](#скиллы)
- [Шаблоны документации](#шаблоны-документации)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Структура сервиса

Каждый сервис в `/src/{service}/` имеет стандартную структуру.

### Дерево файлов

```
/src/{service}/
  README.md               ← точка входа, ссылка на документацию
  Makefile                ← команды сервиса (build, test, run)
  dependencies.yaml       ← зависимости от других сервисов
  .env.example            ← шаблон переменных окружения

  /backend/               ← серверный код
    /v1/                  ← версия API
    /v2/
    /shared/              ← общая логика между версиями
    /health/              ← health check endpoints

  /frontend/              ← клиентский код (если есть)

  /database/              ← работа с БД
    schema.sql            ← текущая схема
    /migrations/          ← миграции
    /seeds/               ← тестовые данные

  /tests/                 ← unit/integration тесты
```

### Обязательные файлы

| Файл | Назначение | Документировать |
|------|------------|:---------------:|
| `README.md` | Точка входа в сервис | ❌ (сам является документацией) |
| `Makefile` | Команды сервиса | ✅ в README |
| `dependencies.yaml` | Зависимости от других сервисов | ✅ в README |
| `.env.example` | Шаблон переменных окружения | ✅ в README |

### dependencies.yaml

Описывает зависимости сервиса от других сервисов:

```yaml
# /src/auth/dependencies.yaml
dependencies:
  services:
    - name: users
      required: true
      description: Получение данных пользователя
    - name: notification
      required: false
      description: Отправка email при регистрации

  external:
    - name: redis
      required: true
      description: Хранение сессий
```

---

## Правила

### Ссылка на инструкцию

**Правило:** При генерации любого файла в `/src/` добавлять ссылку на данную инструкцию:

```
Инструкция: /.claude/instructions/src/documentation.md
```

Это обеспечивает связь кода с правилами документирования.

### Связь src ↔ doc

**Правило:** При создании файла в `/src/{service}/{path}` — создать `/doc/src/{service}/{path}.md` и добавить ссылку в начало файла.

| Файл в /src/ | Документация в /doc/ |
|--------------|---------------------|
| `/src/auth/` | `/doc/src/auth/` |
| `/src/auth/backend/handlers.ts` | `/doc/src/auth/backend/handlers.md` |
| `/src/notification/database/schema.sql` | `/doc/src/notification/database/schema.md` |

### README.md сервиса

Каждый сервис содержит `README.md` — точку входа с полной информацией:

```markdown
# {Service} Service

{Краткое описание назначения сервиса — 1-2 предложения}

📖 **Документация:** [/doc/src/{service}/](/doc/src/{service}/)

## Быстрый старт

\`\`\`bash
# Запуск для разработки
make dev

# Запуск тестов
make test
\`\`\`

## Зависимости

| Сервис | Обязательный | Назначение |
|--------|:------------:|------------|
| users | ✅ | Получение данных пользователя |
| notification | ❌ | Отправка email |

**Внешние:**
- Redis — хранение сессий

## Переменные окружения

См. [.env.example](.env.example)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `PORT` | Порт сервиса | `8080` |
| `DATABASE_URL` | URL базы данных | — |
| `JWT_SECRET` | Секрет для JWT | — |

## Команды

| Команда | Описание |
|---------|----------|
| `make dev` | Запуск для разработки |
| `make test` | Запуск тестов |
| `make build` | Сборка |
| `make migrate` | Применить миграции |

## API

- Swagger UI: `GET /docs`
- Health check: `GET /health`
- Readiness: `GET /ready`
```

### Ссылки в коде

Файлы кода содержат ссылку на документацию в начале:

**Python:**
```python
"""
Auth handlers.

Документация: /doc/src/auth/backend/handlers.md
"""
```

**TypeScript/JavaScript:**
```typescript
/**
 * Auth handlers.
 *
 * Документация: /doc/src/auth/backend/handlers.md
 */
```

### Комментарии

- Комментировать **"почему"**, а не **"что"**
- Код должен быть самодокументируемым
- Сложная логика требует пояснения
- Использовать JSDoc/docstrings для публичных API

---

## Workflow

| Событие | Действие | Скилл |
|---------|----------|-------|
| Создан файл в `/src/` | Создать документацию в `/doc/src/` | `/doc-create` |
| Изменён файл в `/src/` | Обновить документацию | `/doc-update` |
| Удалён файл из `/src/` | Пометить документацию, создать Issue | `/doc-delete` |

### Автоматизация

При работе с файлами `/src/` скиллы вызываются вручную или интегрируются в процесс разработки:

```
/doc-create /src/auth/backend/handlers.ts
/doc-update /src/auth/backend/handlers.ts
/doc-delete /src/auth/backend/handlers.ts
```

---

## Скиллы

Скиллы для автоматизации работы с документацией:

| Скилл | Назначение |
|-------|------------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Создание документации для нового файла |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации при изменении кода |
| [/doc-delete](/.claude/skills/doc-delete/SKILL.md) | Пометка документации при удалении файла |

### /doc-create

Создаёт:
1. Файл `/doc/src/{service}/{path}.md` по шаблону
2. Ссылку на документацию в исходном файле

### /doc-update

Обновляет документацию при изменении:
- Сигнатур функций/методов
- Структуры модуля
- Зависимостей

### /doc-delete

При удалении файла из `/src/`:
1. Помечает документацию в `/doc/` как требующую ревью
2. Создаёт GitHub Issue для отслеживания

---

## Шаблоны документации

Шаблоны зависят от типа файла. Выбирайте подходящий.

### Шаблон: Backend (handlers, services, controllers)

```markdown
# {Название модуля}

> Исходный код: [{filename}](/{path-to-source})

{Краткое описание — 1-2 предложения}

## API

### {FunctionName}

{Описание функции}

**Сигнатура:**
\`\`\`{language}
{signature}
\`\`\`

**Параметры:**
| Параметр | Тип | Описание |
|----------|-----|----------|
| {name} | {type} | {description} |

**Возвращает:** {return type and description}

**Ошибки:**
| Код | Описание |
|-----|----------|
| 400 | Невалидные данные |
| 401 | Не авторизован |

## Примеры

\`\`\`{language}
// Пример вызова
{example}
\`\`\`

## Зависимости

- [{dependency}](/{path}) — {description}
```

### Шаблон: Database (schema, migrations)

```markdown
# {Название схемы/миграции}

> Исходный код: [{filename}](/{path-to-source})

{Описание изменений в БД}

## Таблицы

### {table_name}

{Описание таблицы}

| Колонка | Тип | Nullable | Описание |
|---------|-----|:--------:|----------|
| id | UUID | ❌ | Первичный ключ |
| {column} | {type} | ✅/❌ | {description} |

**Индексы:**
- `idx_{name}` — {columns} ({description})

**Foreign keys:**
- `{column}` → `{table}.{column}`

## Миграции

| Версия | Описание |
|--------|----------|
| 0001 | Создание таблицы |
| 0002 | Добавление колонки |
```

### Шаблон: Frontend (components, pages)

```markdown
# {Название компонента}

> Исходный код: [{filename}](/{path-to-source})

{Описание компонента}

## Props

| Prop | Тип | Обязательный | Описание |
|------|-----|:------------:|----------|
| {name} | {type} | ✅/❌ | {description} |

## События

| Событие | Payload | Описание |
|---------|---------|----------|
| onClick | `{type}` | {description} |

## Примеры

\`\`\`tsx
<{Component} prop={value} />
\`\`\`

## Зависимости

- [{component}](/{path}) — {description}
```

### Шаблон: Минимальный

Для простых файлов (утилиты, константы):

```markdown
# {Название}

> Исходный код: [{filename}](/{path})

{Описание}

## API

| Функция/Константа | Описание |
|-------------------|----------|
| `{name}` | {description} |
```

---

## Примеры

### Пример 1: README.md сервиса auth

**Файл:** `/src/auth/README.md`

```markdown
# Auth Service

Документация: [/doc/src/auth/](/doc/src/auth/)

## Быстрый старт

См. документацию для настройки и запуска.
```

### Пример 2: Файл с обработчиками

**Файл:** `/src/auth/backend/handlers.py`

```python
"""
Обработчики аутентификации.

Документация: /doc/src/auth/backend/handlers.md
"""

def login(request):
    """
    Аутентификация пользователя.

    Args:
        request: HTTP запрос с credentials

    Returns:
        JWT токен при успехе
    """
    # Проверяем rate limit перед валидацией
    # (защита от brute-force атак)
    check_rate_limit(request.ip)
    ...
```

### Пример 3: Комментарии — хорошо vs плохо

```python
# ❌ Плохо — описывает "что"
# Увеличиваем счётчик на 1
counter += 1

# ✅ Хорошо — объясняет "почему"
# Пропускаем первую строку CSV (заголовки)
counter += 1
```

---

## Связанные инструкции

- [doc/structure.md](../doc/structure.md) — структура документации, зеркалирование
- [git/issues.md](../git/issues.md) — создание Issue при удалении документации

---

> **Путь:** `/.claude/instructions/src/documentation.md`
