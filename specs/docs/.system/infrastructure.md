---
description: Инфраструктура MyApp — платформа, окружения, хранилища, сервисы.
standard: specs/.instructions/docs/infrastructure/standard-infrastructure.md
standard-version: v1.1
---

> **Это визуализация.** Содержание заполнено примером из стандарта (MyApp, 4 сервиса). При реальном использовании — заменить на данные проекта по [Сценарию 6](../../../specs/.instructions/docs/infrastructure/modify-infrastructure.md) (когда будет создан).

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
| Management UI | http://localhost:15672 (*недоступно в staging/prod*) | — |

**Каналы:**

| Канал | Тип | Издатели | Подписчики | Описание |
|-------|-----|---------|------------|----------|
| system.events | fanout exchange | auth, task, admin | notification | Системные события для уведомлений |

**Формат сообщений** (общий формат для всех каналов):

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

**Стандарт логирования:** см. [conventions.md](./conventions.md) секция Логирование.

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
