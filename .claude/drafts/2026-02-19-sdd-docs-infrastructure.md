# docs/.system/infrastructure.md — платформа и окружения

Спецификация infrastructure.md: секции, шаблон, пример. Всё, что нужно LLM-разработчику для запуска, подключения и отладки: локальный запуск, порты, хранилища, окружения, секреты.

## Контекст

**Задача:** Определить формат docs/.system/infrastructure.md — платформенного документа для LLM-разработчика.

**Источник:** `.claude/drafts/2026-02-19-sdd-chain-rethink.md` (строки 1582-1832)

**Связанные файлы:**
- `2026-02-19-sdd-structure.md` — общая структура и решения
- `2026-02-19-sdd-docs-overview.md` — overview.md (архитектура системы vs платформа)

---

## Содержание

Всё, что LLM-разработчику нужно знать для запуска, подключения и отладки: как поднять систему, где что слушает, как сервисы находят друг друга, куда смотреть при ошибках.

### Секции docs/.system/infrastructure.md

| # | Секция | Содержание | Зачем LLM-разработчику |
|---|--------|-----------|----------------------|
| 1 | **Локальный запуск** | docker-compose, команды make, порядок запуска, .env.example | Поднять систему для разработки и тестирования |
| 2 | **Сервисы и порты** | Таблица: сервис, хост, порт, URL, healthcheck | Знать куда подключаться при написании кода и тестов |
| 3 | **Хранилища** | Для каждого хранилища: хост, порт, имя базы, пользователь, env-переменная | Писать connection strings, конфигурировать ORM |
| 4 | **Message Broker** | URL, exchange/queue/topic для каждого канала, формат сообщений | Настроить pub/sub, написать consumer/producer |
| 5 | **Service Discovery** | Как сервисы находят друг друга: DNS, env vars, hardcoded URLs | Знать откуда брать URL другого сервиса при вызове |
| 6 | **Окружения** | Таблица dev/staging/prod: отличия, ресурсы, ограничения | Не сломать prod-конфигурацию, писать env-aware код |
| 7 | **Мониторинг и логи** | Где логи, как искать, формат логирования, метрики | Добавить корректное логирование, найти ошибку |
| 8 | **Секреты** | Откуда берутся (env vars, Vault, .env), что никогда не коммитить | Не захардкодить секрет, правильно получить из env |

### Шаблон: docs/.system/infrastructure.md

`````markdown
# Инфраструктура

## Локальный запуск

Все команды определены в [Makefile](/Makefile) (SSOT). Полный список: `make help`.

**Порядок запуска:** {описание зависимостей при старте, если важен порядок}

**Переменные окружения:** скопировать `.env.example` → `.env`. Описание каждой переменной — в `.env.example`.

## Сервисы и порты

| Сервис | Хост (docker) | Хост (local) | Порт | URL | Healthcheck |
|--------|--------------|-------------|------|-----|-------------|
| {svc} | {svc} | localhost | {port} | http://localhost:{port} | GET /health |

## Хранилища

### {StorageType} ({назначение})

| Параметр | Значение (dev) | Env-переменная |
|----------|---------------|----------------|
| Хост | {host} | `{PREFIX}_HOST` |
| Порт | {port} | `{PREFIX}_PORT` |
| База/Namespace | {db_name} | `{PREFIX}_DB` |
| Пользователь | {user} | `{PREFIX}_USER` |
| Пароль | из .env | `{PREFIX}_PASSWORD` |

**Connection string:** `{protocol}://${PREFIX}_USER:${PREFIX}_PASSWORD@${PREFIX}_HOST:${PREFIX}_PORT/${PREFIX}_DB`

## Message Broker

### {BrokerType} ({назначение})

| Параметр | Значение (dev) | Env-переменная |
|----------|---------------|----------------|
| URL | {url} | `{PREFIX}_URL` |

**Каналы:**

| Канал | Тип | Издатели | Подписчики | Описание |
|-------|-----|---------|------------|----------|
| {channel} | {exchange/queue/topic} | {svc1} | {svc2} | {описание} |

## Service Discovery

{Как сервисы находят друг друга.}

| Сервис-источник | Сервис-цель | Механизм | Значение (dev) | Env-переменная |
|----------------|------------|----------|---------------|----------------|
| {svc1} | {svc2} | {env var / DNS} | http://{svc2}:{port} | `{SVC2}_URL` |

## Окружения

| Параметр | dev | staging | prod |
|----------|-----|---------|------|
| Реплики сервисов | 1 | 1 | {N} |
| БД | Docker container | {managed/shared} | {managed, HA} |
| Секреты | .env файл | {Vault / env vars} | {Vault} |
| Домен | localhost | {staging.domain} | {prod.domain} |
| Логирование | stdout | {централизованное} | {централизованное} |

## Мониторинг и логи

**Формат логов:** {JSON / structured / plain}

**Где смотреть:**

| Окружение | Логи | Метрики |
|-----------|------|---------|
| dev | `docker-compose logs {svc}` | — |
| staging | {инструмент, URL} | {инструмент, URL} |
| prod | {инструмент, URL} | {инструмент, URL} |

**Стандарт логирования:**
- Уровни: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- Обязательные поля: `timestamp`, `level`, `service`, `message`
- При ошибке: добавлять `error_type`, `stack_trace`, `request_id`

## Секреты

**Правило:** секреты НИКОГДА не коммитятся. Только `.env.example` с пустыми значениями.

| Секрет | Env-переменная | Источник (dev) | Источник (prod) |
|--------|---------------|----------------|-----------------|
| {описание} | `{VAR_NAME}` | .env | {Vault / env var} |
`````

### Пример: docs/.system/infrastructure.md

`````markdown
# Инфраструктура

## Локальный запуск

Все команды определены в [Makefile](/Makefile) (SSOT). Полный список: `make help`.

**Порядок запуска:** PostgreSQL и Redis стартуют первыми (healthcheck), затем сервисы. RabbitMQ стартует параллельно — сервисы с retry до подключения.

**Переменные окружения:** скопировать `.env.example` → `.env`. Описание каждой переменной — в `.env.example`. Для dev-окружения `.env.example` содержит рабочие значения.

## Сервисы и порты

| Сервис | Хост (docker) | Хост (local) | Порт | URL | Healthcheck |
|--------|--------------|-------------|------|-----|-------------|
| auth | auth | localhost | 8001 | http://localhost:8001 | GET /health |
| task | task | localhost | 8002 | http://localhost:8002 | GET /health |
| notification | notification | localhost | 8003 | http://localhost:8003 | GET /health |
| admin | admin | localhost | 8004 | http://localhost:8004 | GET /health |
| gateway | gateway | localhost | 8000 | http://localhost:8000 | GET /health |

**Gateway** проксирует все запросы: `/api/v1/auth/*` → auth:8001, `/api/v1/tasks/*` → task:8002, и т.д.

## Хранилища

### PostgreSQL (основное хранилище данных)

| Параметр | Значение (dev) | Env-переменная |
|----------|---------------|----------------|
| Хост | postgres | `POSTGRES_HOST` |
| Порт | 5432 | `POSTGRES_PORT` |
| База (auth) | myapp_auth | `AUTH_DB_NAME` |
| База (task) | myapp_task | `TASK_DB_NAME` |
| База (notification) | myapp_notification | `NOTIFICATION_DB_NAME` |
| База (admin) | myapp_admin | `ADMIN_DB_NAME` |
| Пользователь | myapp | `POSTGRES_USER` |
| Пароль | из .env | `POSTGRES_PASSWORD` |

**Connection string:** `postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${*_DB_NAME}`

Каждый сервис имеет свою базу данных. Кросс-сервисные запросы запрещены — только через API.

### Redis (кэш и WS-соединения)

| Параметр | Значение (dev) | Env-переменная |
|----------|---------------|----------------|
| Хост | redis | `REDIS_HOST` |
| Порт | 6379 | `REDIS_PORT` |
| База (notification) | 0 | `NOTIFICATION_REDIS_DB` |
| База (auth sessions) | 1 | `AUTH_REDIS_DB` |

**Connection string:** `redis://${REDIS_HOST}:${REDIS_PORT}/${*_REDIS_DB}`

## Message Broker

### RabbitMQ (асинхронное взаимодействие между сервисами)

| Параметр | Значение (dev) | Env-переменная |
|----------|---------------|----------------|
| URL | amqp://guest:guest@rabbitmq:5672 | `RABBITMQ_URL` |
| Management UI | http://localhost:15672 | — |

**Каналы:**

| Канал | Тип | Издатели | Подписчики | Описание |
|-------|-----|---------|------------|----------|
| system.events | fanout exchange | auth, task, admin | notification | Системные события для уведомлений |

**Формат сообщений:**
```json
{
  "event": "UserRegistered",
  "timestamp": "ISO8601",
  "source": "auth",
  "data": { "...": "event-specific payload" }
}
```

## Service Discovery

Сервисы находят друг друга через env-переменные с URL. В Docker — по имени контейнера, локально — localhost с портом.

| Сервис-источник | Сервис-цель | Механизм | Значение (dev) | Env-переменная |
|----------------|------------|----------|---------------|----------------|
| task | auth | env var | http://auth:8001 | `AUTH_SERVICE_URL` |
| notification | auth | env var | http://auth:8001 | `AUTH_SERVICE_URL` |
| admin | auth | env var | http://auth:8001 | `AUTH_SERVICE_URL` |
| gateway | auth | env var | http://auth:8001 | `AUTH_SERVICE_URL` |
| gateway | task | env var | http://task:8002 | `TASK_SERVICE_URL` |
| gateway | notification | env var | http://notification:8003 | `NOTIFICATION_SERVICE_URL` |
| gateway | admin | env var | http://admin:8004 | `ADMIN_SERVICE_URL` |

## Окружения

| Параметр | dev | staging | prod |
|----------|-----|---------|------|
| Реплики сервисов | 1 | 1 | 2-4 (auto-scale) |
| PostgreSQL | Docker container | AWS RDS (shared) | AWS RDS (HA, Multi-AZ) |
| Redis | Docker container | AWS ElastiCache | AWS ElastiCache (cluster) |
| RabbitMQ | Docker container | AWS MQ | AWS MQ (HA) |
| Секреты | .env файл | AWS Secrets Manager | AWS Secrets Manager |
| Домен | localhost:8000 | staging.myapp.com | myapp.com |
| TLS | нет | Let's Encrypt | ACM |
| Логирование | stdout (docker logs) | CloudWatch | CloudWatch + alerts |

## Мониторинг и логи

**Формат логов:** JSON structured

**Где смотреть:**

| Окружение | Логи | Метрики |
|-----------|------|---------|
| dev | `docker-compose logs -f {svc}` | — |
| staging | AWS CloudWatch → Log Group `/myapp/staging/{svc}` | CloudWatch Metrics |
| prod | AWS CloudWatch → Log Group `/myapp/prod/{svc}` | CloudWatch Metrics + Grafana |

**Стандарт логирования:**
- Уровни: `DEBUG` (dev only), `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- Обязательные поля: `timestamp`, `level`, `service`, `message`, `request_id`
- При ошибке: добавлять `error_type`, `stack_trace`
- При HTTP-запросе: `method`, `path`, `status_code`, `duration_ms`

**Alerting (prod):**
- ERROR rate > 1% за 5 минут → Slack #alerts
- Response time p99 > 2s → Slack #alerts
- Healthcheck fail → PagerDuty

## Секреты

**Правило:** секреты НИКОГДА не коммитятся. Только `.env.example` с пустыми значениями.

| Секрет | Env-переменная | Источник (dev) | Источник (prod) |
|--------|---------------|----------------|-----------------|
| Пароль PostgreSQL | `POSTGRES_PASSWORD` | .env | AWS Secrets Manager |
| JWT signing key | `JWT_SECRET_KEY` | .env | AWS Secrets Manager |
| RabbitMQ credentials | `RABBITMQ_URL` | .env (guest:guest) | AWS Secrets Manager |
| API keys внешних сервисов | `{SERVICE}_API_KEY` | .env | AWS Secrets Manager |
`````

---

## Аудит старых документов

| Старый документ | Что переиспользовать |
|-----------------|---------------------|
| `specs/architecture/system/infrastructure.md` | Текущий шаблон (для сравнения) |
| `specs/.instructions/living-docs/architecture/standard-architecture.md` | Planned Changes/Changelog паттерн |
