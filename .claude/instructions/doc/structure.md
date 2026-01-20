---
type: project
description: Структура /doc/, документирование кода, шаблоны, workflow
related:
  - git/issues.md   # создание Issue при удалении документации
---

# Структура и документирование

Правила организации документации в `/doc/` и документирования кода в `/src/`.

## Оглавление

- [1. ЧТО: Структура /doc/](#1-что-структура-doc)
  - [Принцип зеркалирования](#принцип-зеркалирования)
  - [Что зеркалируется](#что-зеркалируется)
  - [Типы документов](#типы-документов)
  - [Дерево /doc/](#дерево-doc)
- [2. ГДЕ: Структура сервиса /src/](#2-где-структура-сервиса-src)
  - [Дерево файлов сервиса](#дерево-файлов-сервиса)
  - [Обязательные файлы](#обязательные-файлы)
  - [dependencies.yaml](#dependenciesyaml)
- [3. КАК: Документирование кода](#3-как-документирование-кода)
  - [README.md сервиса](#readmemd-сервиса)
  - [Ссылки в коде](#ссылки-в-коде)
  - [Комментарии](#комментарии)
- [4. Workflow документации](#4-workflow-документации)
- [5. Шаблоны документации](#5-шаблоны-документации)
- [6. Скиллы](#6-скиллы)
- [7. Примеры](#7-примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## 1. ЧТО: Структура /doc/

### Принцип зеркалирования

**Правило:** Документация располагается рядом с тем, что документирует (colocation principle).

| Код | Документация |
|-----|--------------|
| `/src/auth/backend/handlers.ts` | `/doc/src/auth/backend/handlers.md` |
| `/shared/libs/errors/` | `/doc/shared/libs/errors.md` |
| `/platform/gateway/` | `/doc/platform/gateway/README.md` |

### Что зеркалируется

**Правило:** Зеркалируются только папки, содержимое которых требует документации.

| Папка | Зеркалируется | Причина |
|-------|:-------------:|---------|
| `/src/` | ✅ | Сервисы требуют документации: API, архитектура, ADR, runbooks |
| `/shared/` | ✅ | Библиотеки и контракты нужно документировать для потребителей |
| `/platform/` | ✅ | Инфраструктура требует runbooks, инструкций по деплою |
| `/config/` | ❌ | Конфиги самодокументируемы (комментарии внутри YAML) |
| `/tests/` | ❌ | Тесты сами являются документацией (код = спецификация) |
| `/.github/` | ❌ | Workflows самодокументируемы (YAML с комментариями) |

### Типы документов

**Правило:** Каждый тип документа имеет своё место в структуре.

| Тип | Расположение | Назначение |
|-----|--------------|------------|
| README.md | Корень каждой папки | Точка входа: обзор, ссылки, быстрый старт |
| ADR | `/doc/src/{service}/specs/adr/` | Фиксация архитектурных решений |
| Runbooks | `/doc/runbooks/`, `/doc/src/{service}/runbooks/` | Инструкции по эксплуатации |
| Specs | `/doc/src/{service}/specs/` | Архитектура, планы реализации |

**Формат ADR:**
- Название: `NNNN-название.md`
- Содержит: контекст, решение, последствия

### Дерево /doc/

```
/doc/
  README.md                 # как работать с документацией
  glossary.md               # глоссарий терминов проекта
  /runbooks/                # общие runbooks (инфра, БД)
    database-full.md
    high-load.md
    backup-restore.md

  # Зеркало /src/ — документация сервисов
  /src/
    /auth/
      README.md             # обзор сервиса
      /specs/               # спецификации
        /architecture/      # архитектурные описания
        /adr/               # ADR этого сервиса
          0001-jwt-tokens.md
        /plans/             # планы реализации
      /backend/
        handlers.md
        api.md
      /database/
        schema.md
      /runbooks/            # runbooks этого сервиса
        token-issues.md

  # Зеркало /shared/ — документация библиотек и контрактов
  /shared/
    README.md
    /contracts/
      README.md
    /libs/
      errors.md
      logging.md

  # Зеркало /platform/ — документация инфраструктуры
  /platform/
    README.md
    /gateway/
      README.md
    /docker/
      README.md
    /monitoring/
      README.md
    /runbooks/
      deploy.md
      rollback.md
      incident-response.md
```

---

## 2. ГДЕ: Структура сервиса /src/

Каждый сервис в `/src/{service}/` имеет стандартную структуру.

### Дерево файлов сервиса

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

## 3. КАК: Документирование кода

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

```python
# ❌ Плохо — описывает "что"
# Увеличиваем счётчик на 1
counter += 1

# ✅ Хорошо — объясняет "почему"
# Пропускаем первую строку CSV (заголовки)
counter += 1
```

---

## 4. Workflow документации

### Этапы от идеи до документации

```
Дискуссия (/.claude/discussions/)
    ↓ (решение принято)
/doc/src/{service}/specs/adr/       # ADR
    ↓
/doc/src/{service}/specs/plans/     # план реализации
    ↓
/src/{service}/                     # код
    ↓
/doc/src/{service}/backend/         # документация кода
```

**Этапы:**

1. **Дискуссия** — обсуждение подхода в `/.claude/discussions/`
2. **ADR** — фиксация решения в `/doc/src/{service}/specs/adr/`
3. **План** — детальный план в `/doc/src/{service}/specs/plans/`
4. **Код** — реализация в `/src/{service}/`
5. **Документация** — описание API в `/doc/src/{service}/`

### Связь src ↔ doc

**Правило:** При создании файла в `/src/{service}/{path}` — создать `/doc/src/{service}/{path}.md` и добавить ссылку в начало файла.

| Файл в /src/ | Документация в /doc/ |
|--------------|---------------------|
| `/src/auth/` | `/doc/src/auth/` |
| `/src/auth/backend/handlers.ts` | `/doc/src/auth/backend/handlers.md` |
| `/src/notification/database/schema.sql` | `/doc/src/notification/database/schema.md` |

### Автоматизация

| Событие | Действие | Скилл |
|---------|----------|-------|
| Создан файл в `/src/` | Создать документацию в `/doc/src/` | `/doc-create` |
| Изменён файл в `/src/` | Обновить документацию | `/doc-update` |
| Удалён файл из `/src/` | Пометить документацию, создать Issue | `/doc-delete` |

---

## 5. Шаблоны документации

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

## 6. Скиллы

Скиллы для автоматизации работы с документацией:

| Скилл | Назначение |
|-------|------------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Создание документации для нового файла в /src/ |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации при изменении кода |
| [/doc-delete](/.claude/skills/doc-delete/SKILL.md) | Пометка документации при удалении файла |
| [/doc-reindex](/.claude/skills/doc-reindex/SKILL.md) | Полная переиндексация документации |

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

## 7. Примеры

### Пример 1: Документирование нового сервиса

**Задача:** Создать документацию для сервиса `auth`.

**Структура:**
```
/doc/src/auth/
  README.md                     # обзор сервиса
  /specs/
    /adr/
      0001-jwt-tokens.md        # решение по токенам
    /plans/
      oauth-implementation.md   # план реализации OAuth
  /backend/
    handlers.md                 # документация handlers.ts
    api.md                      # описание API
  /runbooks/
    token-issues.md             # что делать при проблемах с токенами
```

### Пример 2: ADR

**Файл:** `/doc/src/auth/specs/adr/0001-jwt-tokens.md`

```markdown
# 0001: Использование JWT токенов

## Статус

Принято

## Контекст

Нужен механизм аутентификации для микросервисной архитектуры.

## Решение

Использовать JWT токены с коротким временем жизни (15 мин) и refresh токены.

## Последствия

- (+) Stateless аутентификация
- (+) Легко масштабируется
- (-) Нельзя отозвать токен до истечения
```

### Пример 3: Runbook

**Файл:** `/doc/src/auth/runbooks/token-issues.md`

```markdown
# Token Issues Runbook

## Симптомы

- Пользователи получают 401 Unauthorized
- Логи: "Token validation failed"

## Диагностика

1. Проверить время на серверах: `date`
2. Проверить секрет JWT: `kubectl get secret jwt-secret`

## Решение

1. Если время разошлось — синхронизировать NTP
2. Если секрет изменился — перезапустить сервис
```

### Пример 4: README.md сервиса

**Файл:** `/src/auth/README.md`

```markdown
# Auth Service

Сервис аутентификации и авторизации.

📖 **Документация:** [/doc/src/auth/](/doc/src/auth/)

## Быстрый старт

\`\`\`bash
make dev
\`\`\`

## Зависимости

- users (обязательный)
- redis (внешний)
```

### Пример 5: Файл с обработчиками

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

---

## Связанные инструкции

- [git/issues.md](../git/issues.md) — создание Issue при удалении документации

---

> **Путь:** `/.claude/instructions/doc/structure.md`
