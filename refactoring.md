# Рефакторинг структуры проекта

## Назначение документа

Определить целевую структуру проекта:
1. Структура папок
2. Перечень инструкций (`/.claude/instructions/`) для каждой области
3. Требования к каждой области (правила)

Структура, описанная в данном документе, **является памятью для LLM**.

**Требования к будущим инструкциям:**
- Каждая инструкция содержит детали реализации для своей зоны ответственности
- Инструкции связаны перелинковкой между собой

**Текущий статус:** 🔄 Проработка разделов

**TODO:** Пройтись по каждому разделу документа:
1. Определить его зоны ответственности
2. Доописать в формате "что за документ и что в нём должно быть описано"
3. Проверить, не дублирует ли раздел зоны ответственности других разделов и/или файлов — если да, устранить дублирование
4. Поискать информацию о нём во всех других разделах — если найдено соответствие, исправить и текущий раздел, и раздел с соответствием

**Инструкция:** После обсуждения раздела — отметить его как ✅ в таблице ниже.

### Таблица проработки разделов

| # | Раздел | Статус | Примечания |
|---|--------|--------|------------|
| **ЧАСТЬ 1: СТРУКТУРА** ||||
| 1.1 | Общая структура | ✅ | Добавлены: принцип разделения, диаграмма связей, чеклисты для папок и файлов |
| 1.2 | Дерево Claude (`/.claude/`) | ✅ | Сокращён, ссылка на [instructions/README.md](/.claude/instructions/README.md) |
| 1.3 | CLAUDE.md | ⬜ | |
| 1.4 | Паттерн инструкций | ✅ | Вынесен в [instructions/README.md](/.claude/instructions/README.md) |
| 1.5 | Задачи — GitHub Issues | ✅ | Вынесен в [git/issues.md](/.claude/instructions/git/issues.md) |
| 1.6 | Дерево сервисов (`/src/`) | ⬜ | |
| 1.7 | Дерево документации (`/doc/`) | ✅ | Вынесен в [doc/structure.md](/.claude/instructions/doc/structure.md) |
| 1.8 | Дерево общего кода (`/shared/`) | ⬜ | |
| 1.9 | Дерево конфигураций (`/config/`) | ⬜ | |
| 1.10 | Дерево инфраструктуры (`/platform/`) | ⬜ | |
| 1.11 | Дерево тестов (`/tests/`) | ⬜ | |
| 1.12 | Git workflow | ✅ | Вынесен в [workflow.md](/.claude/instructions/git/workflow.md), [commits.md](/.claude/instructions/git/commits.md) |
| 1.13 | Code style | ⬜ | |
| 1.14 | Security | ⬜ | |
| 1.15 | Observability | ⬜ | |
| 1.16 | Event-driven | ⬜ | |
| 1.17 | Real-time communication | ⬜ | |
| 1.18 | Caching | ⬜ | |
| 1.19 | Makefile | ⬜ | |
| 1.20 | Secrets | ⬜ | |
| 1.21 | Service creation workflow | ⬜ | |
| **ЧАСТЬ 2: РЕШЕНИЯ** ||||
| 2.1 | Таблица решений | ⬜ | Сверка с разделами |
| **ЧАСТЬ 3: ДЕТАЛИ ИНСТРУКЦИЙ** ||||
| 3.1 | Форматы данных | ⬜ | |
| 3.2 | Health checks / Graceful shutdown | ⬜ | |
| 3.3 | API design | ⬜ | |
| 3.4 | Local development | ⬜ | |
| 3.5 | Deployment strategies | ⬜ | |
| 3.6 | Database patterns | ⬜ | |
| 3.7 | API deprecation | ⬜ | |
| 3.8 | Performance | ⬜ | |
| 3.9 | Compliance/Audit | ⬜ | |

### MemoryBank

**MemoryBank** — структурированная память проекта для LLM. Набор концептов, описывающих что есть в проекте, как тут принято делать, почему так решили и над чем сейчас работаем.

**Patterns (Паттерны)** — `/.claude/instructions/` (весь раздел "Дерево Claude")

**Entities (Сущности)** —
- Сами сущности: `/src/`, `/shared/`, `/platform/`
- Описания сущностей: `/doc/src/`, `/doc/shared/`, `/doc/platform/`

**Tech Context (Технический контекст)** — `/doc/src/{service}/specs/architecture/`

**ADR (Архитектурные решения)** — `/doc/src/{service}/specs/adr/`

**Progress (Прогресс)** — `/doc/src/{service}/specs/plans/`

**Active Context (Активный контекст)** — GitHub Issues

**Glossary (Глоссарий)** — `/doc/glossary.md`

**Discussions (Дискуссии)** — `/.claude/discussions/`

---

# ЧАСТЬ 1: СТРУКТУРА (ЧТО)

---

## Общая структура

> **Назначение раздела:** Обзор верхнего уровня — какие папки и файлы есть в корне проекта. Детали каждой папки — в соответствующих разделах ниже.

### Корневые папки

```
/.claude/                   ← инструменты Claude (инструкции, агенты, скиллы, шаблоны)
/src/                       ← код сервисов
/doc/                       ← документация (зеркало src, shared, platform)
/shared/                    ← общий код (контракты, библиотеки, assets)
/config/                    ← конфигурации окружений
/platform/                  ← инфраструктура (Docker, Terraform, мониторинг)
/tests/                     ← системные тесты (e2e, нагрузочные)
/.github/                   ← CI/CD workflows
```

### Файлы в корне

```
/CLAUDE.md                  ← точка входа для LLM
/docker-compose.yml         ← конфигурация запуска сервисов
/docker-compose.dev.yml     ← конфигурация для разработки
/docker-compose.test.yml    ← конфигурация для тестов
/Makefile                   ← интерфейс команд проекта
/README.md                  ← руководство по началу работы
/CHANGELOG.md               ← история изменений
/LICENSE                    ← лицензия (проприетарная)
/.gitignore                 ← исключения git
/.dockerignore              ← исключения Docker
/.editorconfig              ← базовые правила редактора
/.prettierrc                ← конфигурация Prettier (JS/TS)
/.eslintrc.js               ← конфигурация ESLint (JS/TS)
/.pre-commit-config.yaml    ← конфигурация git hooks
```

### Какие файлы должны быть в корне

**Правило:** В корне только файлы, которые:
- Нужны инструментам, ожидающим их в корне (git, Docker, IDE)
- Являются точками входа для людей или LLM

| Категория | Файлы | Почему в корне |
|-----------|-------|----------------|
| Точки входа | README.md, CLAUDE.md | Первое, что видит человек/LLM |
| Запуск проекта | docker-compose.*, Makefile | Docker и make ищут в корне |
| Git | .gitignore, .pre-commit-config.yaml | Git ожидает в корне |
| Docker | .dockerignore | Docker ожидает в корне |
| IDE/редакторы | .editorconfig, .prettierrc, .eslintrc.js | IDE ищут конфиги в корне |
| Метаданные | LICENSE, CHANGELOG.md | Стандартное расположение |

**Чеклист перед добавлением файла в корень:**
1. ❓ Инструмент требует файл именно в корне?
2. ❓ Это точка входа (README, CLAUDE.md)?
3. ❓ Файл относится ко всему проекту, а не к конкретной папке?

**Если нет — файл должен быть в соответствующей папке:**
- Конфиги окружений → `/config/`
- Скрипты → `/platform/scripts/` или `/.claude/scripts/`
- Документация → `/doc/`

### Принцип разделения

**Ключевое:** Структура позволяет писать сервисы на разных языках и использовать разные БД для каждого сервиса.

| Папка | Отвечает за | Критерий попадания |
|-------|-------------|-------------------|
| `/src/` | Исполняемый код | Запускается как процесс |
| `/doc/` | Документация | Читается человеком/LLM, не исполняется |
| `/shared/` | Переиспользуемое | Используется 2+ сервисами |
| `/config/` | Настройки окружений | Меняется между dev/staging/prod |
| `/platform/` | Инфраструктура | Не бизнес-логика, а "как запускать" |
| `/tests/` | Системные тесты | Тестирует взаимодействие сервисов |
| `/.claude/` | Инструменты LLM | Используется только Claude |
| `/.github/` | CI/CD | GitHub-специфичное |

### Связи между папками

```mermaid
graph LR
    subgraph "Код"
        SRC["/src/"]
        SHARED["/shared/"]
    end

    subgraph "Запуск"
        PLATFORM["/platform/"]
        CONFIG["/config/"]
    end

    DOC["/doc/"]
    TESTS["/tests/"]
    CLAUDE["/.claude/"]

    SRC -->|использует| SHARED
    SRC -->|запускается| PLATFORM
    PLATFORM -->|читает| CONFIG
    TESTS -->|тестирует| SRC

    DOC -.->|зеркалирует| SRC
    DOC -.->|зеркалирует| SHARED
    DOC -.->|зеркалирует| PLATFORM

    CLAUDE -.->|правила для| SRC
    CLAUDE -.->|правила для| DOC
    CLAUDE -.->|правила для| SHARED
    CLAUDE -.->|правила для| CONFIG
    CLAUDE -.->|правила для| PLATFORM
    CLAUDE -.->|правила для| TESTS
```

### Связь папок и инструкций

**Правило:** Каждая корневая папка `/X/` имеет инструкцию `/.claude/instructions/X/README.md`.

```
/src/      → /.claude/instructions/src/README.md
/doc/      → /.claude/instructions/doc/README.md
/shared/   → /.claude/instructions/shared/README.md
/config/   → /.claude/instructions/config/README.md
/platform/ → /.claude/instructions/platform/README.md
/tests/    → /.claude/instructions/tests/README.md
```

**Исключения:**
- `/.github/` — самодокументируемый (YAML с комментариями)
- `/.claude/` — сам является инструкцией

### Добавление новой папки в корень

**Правило:** Новая корневая папка — исключение, не норма.

**Чеклист перед созданием:**
1. ❓ Можно ли поместить в существующую папку?
2. ❓ Будет ли использоваться регулярно (не одноразово)?
3. ❓ Есть ли чёткая зона ответственности, не пересекающаяся с другими?

**Если ответ "да" на все три:**
1. Добавить папку в этот раздел (Общая структура)
2. Создать раздел "Дерево {название}" в документе
3. Создать `/.claude/instructions/{название}/README.md`
4. Обновить MemoryBank (если папка содержит сущности или паттерны)

---

## Дерево Claude (`/.claude/`)

Всё для Claude Code в одном месте.

> 📋 **Полная документация:** [/.claude/instructions/README.md](/.claude/instructions/README.md)

### Статус реализации

| Компонент | Статус | Документация |
|-----------|:------:|--------------|
| Индекс инструкций | ✅ | [README.md](/.claude/instructions/README.md) |
| Инструменты | ✅ | [skills.md](/.claude/instructions/tools/skills.md), [agents.md](/.claude/instructions/tools/agents.md), [claude-testing.md](/.claude/instructions/tools/claude-testing.md) |
| Git | ✅ | [workflow.md](/.claude/instructions/git/workflow.md), [commits.md](/.claude/instructions/git/commits.md), [issues.md](/.claude/instructions/git/issues.md), [ci.md](/.claude/instructions/git/ci.md), [review.md](/.claude/instructions/git/review.md) |
| /src/ | ✅ | [documentation.md](/.claude/instructions/src/documentation.md) |
| /doc/ | ✅ | [structure.md](/.claude/instructions/doc/structure.md) |
| Скиллы | ✅ | [25 скиллов](/.claude/instructions/tools/skills.md) |
| Скрипты | ✅ | [find_references.py](/.claude/scripts/find_references.py) |
| /tests/ | ✅ | [README.md](/.claude/instructions/tests/README.md) |
| /shared/, /config/, /platform/ | ⬜ | Инструкции не созданы |
| agents/, templates/, discussions/ | ⬜ | Папки созданы, контент не заполнен |

---

## Дерево сервисов (`/src/`)

Сервис-ориентированный подход. Каждый сервис автономен.

### Архитектурный принцип: Database per Service

Каждый сервис владеет своей БД. Другие сервисы получают данные через API, не через SQL.

**Плюсы:**
- Независимость (деплой auth не ломает notification)
- Можно разные БД (auth → PostgreSQL, notification → MongoDB)
- Чёткие границы ответственности

### Обнаружение сервисов (Service discovery)

Docker DNS — имя сервиса из docker-compose равно хосту.
URL сервисов через переменные окружения для гибкости (`AUTH_SERVICE_URL=http://auth:8080`).

### Аутентификация между сервисами

JWT между сервисами:
1. Каждый сервис имеет свой service account
2. При запросе к другому сервису — подписывает JWT
3. Принимающий сервис проверяет подпись

### Структура сервиса

```
/src/
  /auth/
    README.md             ← ссылка на /doc/src/auth/
    Makefile              ← команды для этого сервиса (специфика языка)
    dependencies.yaml     ← зависимости сервиса
    .env.example          ← шаблон переменных окружения
    /backend/
      /v1/                ← версия API
      /v2/
      /shared/            ← общая логика между версиями
      /health/            ← health check endpoints
    /frontend/
    /database/
      schema.sql          ← текущая схема
      /migrations/
        0001_initial.sql
        0002_add_roles.sql
      /seeds/             ← тестовые данные для этого сервиса
    /tests/               ← unit/integration тесты

  /notification/
    README.md
    Makefile
    /backend/
    /frontend/
    /database/
    /tests/
```

### Swagger UI

Каждый сервис хостит документацию API:
```
GET /api/v1/auth/docs     ← Swagger UI для auth
GET /api/v1/users/docs    ← Swagger UI для users
```

### Версионирование сервисов

Git tags как источник правды:
```bash
git tag v1.2.3
git push --tags
```

Версия доступна в health check ответе.

### Связь src ↔ doc

> 📋 **Инструкция:** [/.claude/instructions/src/documentation.md](/.claude/instructions/src/documentation.md)

### Версионирование API

**REST:** URL-версионирование:
```
/api/v1/users
/api/v2/users
```

**gRPC:** Package-версионирование:
```protobuf
package auth.v1;
package auth.v2;
```

---

## Дерево документации (`/doc/`)

> 📋 **Инструкция:** [/.claude/instructions/doc/structure.md](/.claude/instructions/doc/structure.md)

---

## Дерево общего кода (`/shared/`)

Переиспользуемый код и контракты между сервисами:

```
/shared/
  /contracts/               ← API контракты (ключевое!)
    /rest/                  ← OpenAPI спецификации
      auth.yaml
      users.yaml
    /grpc/                  ← Protocol Buffers
      auth.proto
    /events/                ← схемы событий для очередей
      user-created.json
      order-completed.json
    /realtime/              ← схемы real-time сообщений
      notifications.json
      chat-messages.json
    /pacts/                 ← contract testing (генерируются)

  /libs/                    ← общие библиотеки
    /errors/                ← единый формат ошибок
    /logging/               ← единый формат логов
    /validation/            ← общие валидаторы
    /http-client/           ← HTTP клиент с timeouts, retries, circuit breaker
    /features/              ← проверка feature flags

  /packages/                ← npm/pip пакеты
  /types/                   ← общие типы/схемы

  /assets/                  ← статика
    /icons/
    /fonts/
    /brand/

  /i18n/                    ← локализация
    /ru/                    ← пока только русский
      common.json
      errors.json

  /seeds/                   ← общие справочники
    countries.sql
    currencies.sql
```

### Межсервисное взаимодействие

Три типа коммуникации — три папки контрактов:

| Тип | Папка | Формат |
|-----|-------|--------|
| REST | `/shared/contracts/rest/` | OpenAPI (YAML) |
| gRPC | `/shared/contracts/grpc/` | Protobuf (.proto) |
| Очереди | `/shared/contracts/events/` | JSON Schema |

---

## Дерево конфигураций (`/config/`)

Конфигурации окружений:

```
/config/
  /environments/
    development.yaml
    staging.yaml
    production.yaml
  /features/               ← feature flags (когда понадобится)
    features.yaml
```

**Пример `development.yaml`:**
```yaml
database:
  host: localhost
  pool_size: 5
redis:
  host: localhost
logging:
  level: debug
```

### Feature flags

Пока не реализованы. При необходимости:
- Простой вариант: `/config/features/features.yaml`
- Продвинутый: сервис Unleash в `/src/feature-flags/`

---

## Дерево инфраструктуры (`/platform/`)

Инфраструктура и деплой:

```
/platform/
  /gateway/                 ← Traefik конфигурация
    traefik.yml
    /dynamic/               ← динамические middlewares
      cors.yml              ← CORS настройки
      rate-limit.yml        ← rate limiting
  /docker/                  ← Dockerfile'ы
  /terraform/               ← IaC
  /monitoring/              ← Prometheus, Grafana, алерты
    prometheus.yml
    /dashboards/
    /alerts/
  /queues/                  ← очереди сообщений (RabbitMQ, Kafka)
    rabbitmq.conf
    docker-compose.queues.yml
  /cache/                   ← кэширование (Redis)
    redis.conf
  /security/                ← security scanning конфиги
    semgrep.yml
    .gitleaks.toml
  /secrets/                 ← документация по секретам
    README.md
  /scripts/                 ← деплой-скрипты (не LLM!)
```

### API Gateway — Traefik

Выбран Traefik:
- Бесплатный (open source)
- Автоматически обнаруживает сервисы в Docker
- Конфигурация через labels в docker-compose

**Load balancing (Балансировка нагрузки):** Traefik автоматически балансирует при нескольких репликах (round-robin).

**CORS (Кросс-доменные запросы):** Настраивается централизованно в Traefik (не в сервисах).

```yaml
# /platform/gateway/dynamic/cors.yml
http:
  middlewares:
    cors:
      headers:
        accessControlAllowOriginList:
          - "https://app.example.com"
        accessControlAllowMethods:
          - GET
          - POST
          - PUT
          - DELETE
        accessControlAllowHeaders:
          - Authorization
          - Content-Type
```

**Rate limiting (Ограничение частоты):** Централизованно в Traefik.

```yaml
# /platform/gateway/dynamic/rate-limit.yml
http:
  middlewares:
    rate-limit:
      rateLimit:
        average: 100    # запросов в секунду
        burst: 50       # пиковый burst
```

---

## Дерево тестов (`/tests/`)

Тесты системного уровня:

```
/tests/
  /unit/                    ← юнит-тесты сервисов
  /integration/             ← интеграционные тесты
  /e2e/                     ← функциональные сценарии
    auth-flow.spec.ts
    checkout.spec.ts
  /smoke/                   ← быстрая проверка работоспособности
  /load/                    ← нагрузочные тесты (k6)
    /services/              ← изолированные тесты сервисов
      auth.k6.js
    /scenarios/             ← сценарные тесты
      full-flow.k6.js
    /system/                ← системные тесты
      peak-load.k6.js
  /fixtures/                ← общие тестовые данные
```

**Unit/integration тесты** — внутри сервисов (`/src/auth/tests/`).

---

## Git workflow (Git-процессы)

> 📋 **Инструкции:**
> - [workflow.md](/.claude/instructions/git/workflow.md) — GitHub Flow, ветки, PR
> - [commits.md](/.claude/instructions/git/commits.md) — Conventional Commits, CHANGELOG
> - [issues.md](/.claude/instructions/git/issues.md) — GitHub Issues, метки, префиксы

---

## Code style (Стиль кода)

Конфиги в корне, сервис может переопределить:

```
/.editorconfig            ← базовые правила (отступы, encoding)
/.prettierrc              ← JS/TS форматирование
/.eslintrc.js             ← JS/TS линтинг
/ruff.toml                ← Python линтинг (если нужен)
/pyproject.toml           ← Python конфигурация (если нужен)

/src/auth/
  .eslintrc.js            ← переопределение для сервиса (опционально)
```

---

## Security (Безопасность)

### В CI (/.github/workflows/security.yml):
- **Dependabot** — уязвимые зависимости
- **GitLeaks** — секреты в коде
- **Semgrep** — SAST (опционально)

### Конфиги:
```
/platform/security/
  semgrep.yml
  .gitleaks.toml
```

---

## Observability (Наблюдаемость)

Три столпа наблюдаемости для микросервисов:

```
         ┌─────────────────────────────────────────┐
         │            Observability                │
         ├─────────────┬─────────────┬─────────────┤
         │    Logs     │   Metrics   │   Traces    │
         │   (Loki)    │(Prometheus) │  (Tempo)    │
         └──────┬──────┴──────┬──────┴──────┬──────┘
                │             │             │
                └─────────────┼─────────────┘
                              │
                      ┌───────┴───────┐
                      │  request_id   │  ← корреляция
                      │  trace_id     │
                      └───────────────┘
```

### Структура в `/platform/`

```
/platform/
  /monitoring/
    prometheus.yml            ← сбор метрик
    /dashboards/              ← Grafana dashboards
    /alerts/                  ← правила алертинга

  /tracing/
    tempo.yml                 ← конфиг Tempo

  /logging/
    loki.yml                  ← конфиг Loki
    promtail.yml              ← сборщик логов
```

### Корреляция: request_id и trace_id

Каждый запрос получает идентификаторы для связи логов, метрик и traces:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Gateway   │────▶│    Auth     │────▶│    Users    │
│             │     │             │     │             │
│ request_id  │     │ request_id  │     │ request_id  │
│ trace_id    │     │ trace_id    │     │ trace_id    │
│ span_id: A  │     │ span_id: B  │     │ span_id: C  │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
   [Logs]              [Logs]              [Logs]
   [Metrics]           [Metrics]           [Metrics]
   [Traces]            [Traces]            [Traces]
```

**Правила:**
- `request_id` — генерируется на Gateway, передаётся в заголовке `X-Request-ID`
- `trace_id` — генерируется OpenTelemetry, propagation через `traceparent` (W3C)
- Все логи содержат оба ID
- Метрики содержат label `service`

### Инструкции в `/.claude/instructions/`

```
/.claude/instructions/
  /platform/
    /observability/
      overview.md       ← общий обзор, ссылки на детали
      metrics.md        ← требования к метрикам
      tracing.md        ← требования к трейсам
      logging.md        ← требования к логам
      alerting.md       ← требования к алертам
```

---

## Event-driven (Событийная архитектура)

Асинхронное взаимодействие между сервисами через очереди.

### Структура

```
/shared/contracts/events/     ← JSON Schema для каждого события
  user-created.json
  order-completed.json

/platform/queues/             ← конфиги очередей
  rabbitmq.conf
  /dlq/                       ← dead letter queues
```

### Инструкции

```
/.claude/instructions/
  /shared/
    events.md                 ← naming, idempotency, retry, dead letter
```

### Правила

- **Naming (Именование):** `{service}.{entity}.{action}` (например `users.user.created`)
- **Idempotency (Идемпотентность):** обязателен `event_id` в каждом событии
- **Dead letter (Недоставленные):** необработанные события → `/platform/queues/dlq/`

---

## Real-time communication (Real-time коммуникация)

Варианты push-коммуникации от сервера к клиенту.

### Структура

```
/shared/contracts/realtime/     ← схемы сообщений
  notifications.json
  chat-messages.json
```

### Инструкции

```
/.claude/instructions/
  /src/
    /runtime/
      realtime.md               ← polling, SSE, WebSocket
```

### Правила

| Технология | Когда использовать |
|------------|-------------------|
| **Polling** | Редкие обновления, простота важнее |
| **SSE** | Односторонний push (нотификации, ленты) |
| **WebSocket** | Двусторонний (чат, collaborative editing) |

- **Выбор:** определяется в ADR сервиса
- **Схемы сообщений:** `/shared/contracts/realtime/`
- **Heartbeat (Пульс):** обязателен для WebSocket (keep-alive)

---

## Caching (Кэширование)

Кэширование для ускорения и снижения нагрузки на БД.

### Структура

```
/platform/cache/
  redis.conf
```

### Инструкции

```
/.claude/instructions/
  /platform/
    caching.md                ← паттерны, TTL, invalidation
```

### Правила

- **Паттерн:** cache-aside (приложение управляет кэшем)
- **Key naming (Именование ключей):** `{service}:{entity}:{id}` (например `users:user:123`)
- **TTL (Время жизни):** обязателен для всех ключей
- **Invalidation (Инвалидация):** при изменении данных — удалять ключ

---

## Makefile

Корневой Makefile — единый интерфейс, абстрагирует языки:

```makefile
# Запуск
dev:           docker-compose -f docker-compose.dev.yml up
stop:          docker-compose down

# Сборка
build:         docker-compose build

# Тесты
test:          запуск unit/integration тестов всех сервисов
test-e2e:      запуск e2e тестов
test-load:     запуск нагрузочных тестов
test-auth:     cd src/auth && make test

# База данных
db-migrate:    миграции всех сервисов

# Утилиты
lint:          линтеры
clean:         очистка

# Создание
new-service:   создание нового сервиса из шаблона
```

Каждый сервис имеет свой Makefile со спецификой языка.

---

## Secrets (Секреты и конфигурация)

```
/.env.example               ← шаблон для корня
/src/auth/.env.example      ← шаблон для сервиса

/platform/secrets/
  README.md                 ← как работать с секретами
  rotation.md               ← runbook ротации секретов
```

**Правило:** `.env` в `.gitignore`, `.env.example` в репо.

### Ротация секретов (Secrets rotation)

- **Runbook (Инструкция):** `/platform/secrets/rotation.md`
- **Паттерн dual keys:** для JWT — два signing key активны одновременно
- **Vault (Хранилище секретов):** при необходимости автоматической ротации

---

## Service creation workflow (Процесс создания сервиса)

```
Дискуссия (/.claude/discussions/)
    ↓ (решение принято)
Скилл /new-service
    ↓
Скрипт create-service.py + шаблоны из /.claude/templates/
    ↓
/src/payment/                   ← код сервиса
/doc/src/payment/               ← документация сервиса
/shared/contracts/rest/payment.yaml  ← контракт
```

---

# ЧАСТЬ 2: РЕШЕНИЯ

---

## Решения

| Вопрос | Решение |
|--------|---------|
| Тесты unit/integration | Внутри сервиса (`/src/auth/tests/`) |
| Тесты e2e | `/tests/e2e/` |
| Тесты нагрузочные | `/tests/load/` |
| Инфраструктура | `/platform/` |
| Миграции | Внутри сервиса (`/src/auth/database/migrations/`) |
| Seed данные | Сервис-специфичные в сервисе, общие в `/shared/seeds/` |
| CI/CD | `/.github/` |
| Зависимости | `dependencies.yaml` в корне сервиса |
| Версионирование API (REST) | URL (`/api/v1/`, `/api/v2/`) |
| Версионирование API (gRPC) | Package (`package auth.v1;`) |
| Версионирование сервисов | Git tags |
| Владение БД | Database per Service |
| Service discovery | Docker DNS (имя сервиса = хост) |
| Auth между сервисами | JWT |
| API Gateway | Traefik (`/platform/gateway/`) |
| Load balancing | Traefik (round-robin при нескольких репликах) |
| CORS | Централизованно в Traefik (`/platform/gateway/dynamic/cors.yml`) |
| Rate limiting | Централизованно в Traefik (`/platform/gateway/dynamic/rate-limit.yml`) |
| Контракты API | По типу: `/shared/contracts/{rest,grpc,events}/` |
| Contract testing | `/shared/contracts/pacts/` |
| Мониторинг | Правила в `/.claude/instructions/platform/`, конфиги в `/platform/monitoring/` |
| Logs (агрегация) | Loki (`/platform/logging/`) |
| Metrics | Prometheus (`/platform/monitoring/`) |
| Traces | Tempo (`/platform/tracing/`) |
| Корреляция | request_id + trace_id (передаются через заголовки) |
| Очереди | `/platform/queues/` |
| Events naming | `{service}.{entity}.{action}` |
| Events idempotency | `event_id` в каждом событии |
| Dead letter queues | `/platform/queues/dlq/` |
| Real-time | Polling/SSE/WebSocket — выбор в ADR сервиса |
| Real-time схемы | `/shared/contracts/realtime/` |
| Кэширование | `/platform/cache/`, паттерн cache-aside |
| Cache key naming | `{service}:{entity}:{id}` |
| Cache TTL | Обязателен для всех ключей |
| API URLs | kebab-case, множественное число |
| Partial update | PATCH + JSON Merge Patch |
| Bulk operations | POST `/{entity}/bulk` |
| Local dev | `make dev`, hot reload, debug порты |
| Deployment | Rolling update по умолчанию, blue-green/canary для критичных |
| Rollback | Автоматический при падении health checks |
| Connection pooling | Обязателен |
| DB migrations | Только forward, no rollback в prod |
| Cross-service transactions | Saga pattern |
| DB naming | snake_case |
| API deprecation | Sunset + Deprecation headers, минимум 3 месяца |
| Лимиты производительности | p99 < 200ms, память < 512MB |
| Аудит-логи | Отдельно от обычных логов, кто/что/когда |
| PII | Не логировать, маскировать |
| Окружения | `/config/environments/` |
| Feature flags | Инструкция, сервис Unleash при необходимости |
| docker-compose | В корне проекта |
| Makefile | В корне + в каждом сервисе |
| Статика/Assets | `/shared/assets/` |
| Локализация | `/shared/i18n/ru/`, другие языки позже |
| Связь src ↔ doc | Ссылки в файлах, зеркальная структура |
| Зеркалирование /doc/ | src, shared, platform (не config, tests, .github) |
| ADR | `/doc/src/{service}/specs/adr/` |
| Runbooks | `/doc/runbooks/` + `/doc/src/{service}/runbooks/` + `/doc/platform/runbooks/` |
| Backup/restore | Runbook `/doc/runbooks/backup-restore.md` |
| Шаблоны | `/.claude/templates/` + скрипт + скилл |
| CLAUDE.md | Entry point в корне, ссылки на `/.claude/` |
| Code style | В корне, сервис может переопределить |
| Git hooks | `.pre-commit-config.yaml` в корне |
| Branching | GitHub Flow |
| Changelog | `CHANGELOG.md` в корне + conventional commits |
| Error handling | Единый формат, `/shared/libs/errors/` |
| Validation | Единый формат, `/shared/libs/validation/` |
| Pagination | Единый формат offset-based |
| Logging | JSON structured, `/shared/libs/logging/` |
| Security scanning | Dependabot + GitLeaks в CI |
| Secrets rotation | Dual keys + runbook, Vault при необходимости |
| Health checks | `/health`, `/ready` в каждом сервисе |
| Graceful shutdown | В health-checks.md (связан с /ready) |
| Swagger UI | `/docs` в каждом сервисе |
| Глоссарий | `/doc/glossary.md` |
| Лицензия | Проприетарная |
| Задачи | GitHub Issues с префиксами [AUTH], [NOTIFY] |
| .gitignore | В корне |
| .dockerignore | В корне |
| Инструкции Claude | По зонам: `/.claude/instructions/{src,doc,shared,config,platform,tests,git,tools}/` |
| Инструкции тестов | src/testing.md (unit) ↔ tests/*.md (e2e, load) — перелинковка |
| README.md в инструкциях | Каждая папка имеет README.md — точка входа со ссылками |
| Resilience | Инструкция + `/shared/libs/http-client/` (timeouts, retries, circuit breaker) |
| Ссылки в agents/skills | Каждый файл начинается со ссылки на инструкцию |

---

# ЧАСТЬ 3: ДЕТАЛИ ИНСТРУКЦИЙ (КАК)

Заготовки для будущих файлов в `/.claude/instructions/`. После рефакторинга — вынести в соответствующие инструкции.

---

## Форматы данных

> **Инструкция:** `/.claude/instructions/src/data/errors.md`, `logging.md`, `pagination.md`

### Единый формат ошибок

```json
{
  "error": {
    "code": "AUTH_TOKEN_EXPIRED",
    "message": "Token has expired",
    "details": {
      "expired_at": "2024-01-15T10:00:00Z"
    },
    "request_id": "abc-123"
  }
}
```

### Ошибки валидации

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "fields": {
        "email": "Invalid email format",
        "age": "Must be at least 18"
      }
    }
  }
}
```

### Единый формат логов

Structured logging в JSON:
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "error",
  "service": "auth",
  "request_id": "abc-123",
  "message": "Failed to validate token",
  "context": {
    "user_id": "user-456"
  }
}
```

### Единый формат пагинации

```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 156,
    "total_pages": 8
  }
}
```

---

## Health checks / Graceful shutdown (Проверки работоспособности)

> **Инструкция:** `/.claude/instructions/src/runtime/health.md`

Каждый сервис реализует:
```
GET /health      ← liveness (жив ли сервис)
GET /ready       ← readiness (готов ли принимать трафик)
```

Формат ответа:
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "redis": "ok"
  },
  "version": "1.2.3"
}
```

**Graceful shutdown (Мягкое завершение):**
1. Сервис получает SIGTERM
2. `/ready` → false (перестаёт получать новый трафик)
3. Дожидается завершения текущих запросов (timeout: 30 сек)
4. Закрывает соединения (БД, Redis, очереди)
5. Завершается

---

## API design (Проектирование API)

> **Инструкция:** `/.claude/instructions/src/api/design.md`

- **URLs:** kebab-case, множественное число (`/users`, `/order-items`)
- **Методы:** GET=читать, POST=создать, PUT=заменить, PATCH=частично, DELETE=удалить
- **Статусы:** 200/201/204 успех, 400 валидация, 401 auth, 403 forbidden, 404 not found, 500 server
- **Partial update (Частичное обновление):** PATCH + JSON Merge Patch (RFC 7396)
- **Bulk operations (Массовые операции):** POST `/{entity}/bulk` с массивом

---

## Local development (Локальная разработка)

> **Инструкция:** `/.claude/instructions/src/dev/local.md`

- **Запуск:** `make dev` поднимает всё через docker-compose
- **Hot reload (Горячая перезагрузка):** код монтируется в контейнер, изменения применяются автоматически
- **Отладка:** debug порты открыты (9229 для Node.js, 5678 для Python)
- **IDE:** рекомендации по VS Code / JetBrains в инструкции

---

## Deployment strategies (Стратегии развёртывания)

> **Инструкция:** `/.claude/instructions/platform/deployment.md`

- **Rolling update (Постепенное обновление):** по умолчанию (постепенная замена подов)
- **Blue-green (Сине-зелёный деплой):** для критичных изменений (две среды, переключение)
- **Canary (Канареечный деплой):** для рискованных (1% → 10% → 100% трафика)
- **Rollback (Откат):** автоматический при падении health checks

---

## Database patterns (Паттерны работы с БД)

> **Инструкция:** `/.claude/instructions/src/runtime/database.md`

- **Connection pooling (Пул соединений):** обязателен
- **Migrations (Миграции):** только forward (no rollback в prod)
- **Transactions (Транзакции):** в пределах сервиса; между сервисами — saga
- **Naming (Именование):** snake_case для таблиц и колонок

---

## API deprecation (Вывод API из эксплуатации)

> **Инструкция:** `/.claude/instructions/src/api/deprecation.md`

- **Sunset header (Заголовок окончания):** дата отключения (`Sunset: Sat, 01 Jun 2025 00:00:00 GMT`)
- **Deprecation header (Заголовок устаревания):** `Deprecation: true`
- **Срок:** минимум 3 месяца между deprecation и удалением
- **Документация:** changelog с датами и migration guide

---

## Performance (Производительность)

> **Инструкция:** `/.claude/instructions/src/dev/performance.md`

- **Profiling (Профилирование):** встроено в dev-режим (CPU, память)
- **Benchmarks (Бенчмарки):** `/tests/load/` — k6 сценарии
- **Performance budgets (Лимиты):** p99 latency < 200ms, память < 512MB на сервис
- **Bottleneck detection (Поиск узких мест):** через трейсы + метрики

---

## Compliance/Audit (Соответствие и аудит)

> **Инструкция:** `/.claude/instructions/src/security/audit.md`

- **Audit logs (Аудит-логи):** кто, что, когда (отдельно от обычных логов)
- **Data retention (Хранение):** срок хранения данных (например 1 год)
- **Right to be forgotten (Удаление данных):** API для удаления по запросу
- **PII (Персональные данные):** не логировать, маскировать
