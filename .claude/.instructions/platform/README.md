# Инструкции /platform/

Индекс инструкций для работы с инфраструктурой и платформенными компонентами.

**Содержание:** Docker, кэширование, деплой, операции, безопасность, observability (логи, метрики, трейсы, алертинг).

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Docker](#1-docker) | [docker.md](./docker.md) | Dockerfile best practices, docker-compose |
| [2. Caching](#2-caching) | [caching.md](./caching.md) | Redis кэширование, cache-aside, TTL |
| [3. Deployment](#3-deployment) | [deployment.md](./deployment.md) | Стратегии деплоя, health checks, откат |
| [4. Operations](#4-operations) | [operations.md](./operations.md) | Runbooks, инциденты, postmortems |
| [5. Security](#5-security) | [security.md](./security.md) | Dependabot, GitLeaks, Semgrep, scanning |
| [6. Observability](#6-observability) | [observability/overview.md](./observability/overview.md) | Три столпа: логи, метрики, трейсы |
| [6.1. Metrics](#61-metrics) | [observability/metrics.md](./observability/metrics.md) | Prometheus метрики, naming, labels |
| [6.2. Tracing](#62-tracing) | [observability/tracing.md](./observability/tracing.md) | OpenTelemetry, spans, context propagation |
| [6.3. Logging](#63-logging) | [observability/logging.md](./observability/logging.md) | Loki, structured logging, корреляция |
| [6.4. Alerting](#64-alerting) | [observability/alerting.md](./observability/alerting.md) | Severity levels, routing, runbooks |

---

# 1. Docker

Правила работы с Docker: написание Dockerfile, docker-compose, управление образами.

**Содержание:** best practices (один контейнер = один процесс, минимизация слоёв), multi-stage builds, базовые образы (-alpine, -slim), docker-compose, теги и версионирование, безопасность (non-root, no secrets).

| Базовый образ | Размер |
|---------------|--------|
| `node:20-alpine` | ~180MB |
| `python:3.12-slim` | ~150MB |
| `golang:1.22-alpine` + `scratch` | ~10MB |

**Инструкция:** [docker.md](./docker.md)

---

# 2. Caching

Правила кэширования с Redis: паттерны, TTL, именование ключей, инвалидация.

**Содержание:** паттерн cache-aside, именование ключей (`{service}:{entity}:{id}`), TTL стратегии с jitter, инвалидация (delete, не update), сериализация JSON, мониторинг (hit ratio, latency).

| Тип данных | TTL |
|------------|-----|
| Сессии | 24h |
| Профили | 1h |
| Каталог | 15min |
| Rate limit | 1min |

**Инструкция:** [caching.md](./caching.md)

---

# 3. Deployment

Правила деплоя: стратегии развёртывания, откат, health checks.

**Содержание:** стратегии (Rolling Update, Blue-Green, Canary), health checks (liveness, readiness, startup), автооткат при падении метрик, pre/post deploy hooks, graceful shutdown.

| Стратегия | Downtime | Rollback | Ресурсы |
|-----------|----------|----------|---------|
| Rolling Update | Нет | Медленный | 1.25x |
| Blue-Green | Нет | Мгновенный | 2x |
| Canary | Нет | Быстрый | 1.1x |

**Инструкция:** [deployment.md](./deployment.md)

---

# 4. Operations

Правила операционной работы: runbooks, управление инцидентами, postmortems.

**Содержание:** runbooks (структура, связь с алертами), severity levels (P1-P4), incident response (lifecycle, роли), postmortems (blameless, action items), on-call (ротация, SLA).

| Severity | Response SLA | Resolution SLA |
|----------|--------------|----------------|
| P1/Critical | 5 минут | 1 час |
| P2/High | 15 минут | 4 часа |
| P3/Medium | 1 час | 24 часа |
| P4/Low | 4 часа | 1 неделя |

**Инструкция:** [operations.md](./operations.md)

---

# 5. Security

Правила безопасности: сканирование уязвимостей, секреты, статический анализ.

**Содержание:** Dependabot (управление зависимостями), GitLeaks (сканирование секретов), Semgrep (SAST), Trivy (сканирование контейнеров), CI/CD security gates, управление секретами (Vault, GitHub Secrets).

| Инструмент | Назначение |
|------------|------------|
| Dependabot | Обновление зависимостей |
| GitLeaks | Поиск секретов в коде |
| Semgrep | Статический анализ |
| Trivy | Сканирование контейнеров |

**Инструкция:** [security.md](./security.md)

---

# 6. Observability

Три столпа наблюдаемости: логи, метрики, трейсы. Стек Grafana (Loki + Prometheus + Tempo).

**Содержание:** три столпа, стек технологий (OTel Collector, Grafana), корреляция данных (trace_id, span_id), иерархия dashboards (Overview → Service → Detail), best practices (labels, cardinality, retention).

| Столп | Вопрос | Инструмент |
|-------|--------|------------|
| Logs | Что произошло? | Loki |
| Metrics | Сколько? Как быстро? | Prometheus |
| Traces | Где задержка? | Tempo |

**Инструкция:** [observability/overview.md](./observability/overview.md)

---

## 6.1. Metrics

Правила работы с Prometheus метриками: именование, labels, типы, best practices.

**Содержание:** naming conventions (`{namespace}_{subsystem}_{name}_{unit}`), labels (low-cardinality), типы метрик (Counter, Gauge, Histogram), RED метрики (Rate, Errors, Duration), cardinality control, scraping.

| Тип | Когда использовать |
|-----|-------------------|
| Counter | Только растёт (запросы, ошибки) |
| Gauge | Растёт и падает (connections) |
| Histogram | Распределение (latency) |

**Инструкция:** [observability/metrics.md](./observability/metrics.md)

---

## 6.2. Tracing

Правила distributed tracing: OpenTelemetry, spans, context propagation, Tempo.

**Содержание:** концепции (trace → span → events), OpenTelemetry SDK, span атрибуты (семантические конвенции), W3C Trace Context propagation, sampling (head-based, tail-based), инструментирование (auto + manual).

| Понятие | Описание |
|---------|----------|
| Trace | Весь путь запроса |
| Span | Отдельная операция |
| Span Context | trace_id, span_id |
| Event | Log entry внутри span |

**Инструкция:** [observability/tracing.md](./observability/tracing.md)

---

## 6.3. Logging

Инфраструктура централизованного логирования: Loki, Promtail, корреляция с трейсами.

**Содержание:** формат логов (JSON), корреляция с трейсами (trace_id в логах), Loki конфигурация (labels, retention), LogQL запросы, Promtail для Kubernetes.

> Формат логов в коде: [src/data/logging.md](../src/data/logging.md)

| Label | Хороший | Плохой |
|-------|---------|--------|
| Low-cardinality | `service`, `level` | `user_id`, `trace_id` |

**Инструкция:** [observability/logging.md](./observability/logging.md)

---

## 6.4. Alerting

Правила алертинга: severity levels, маршрутизация, runbooks, noise reduction.

**Содержание:** severity levels (critical/high/warning/info), alert design (actionable alerts), routing и escalation, связь с runbooks, noise reduction (grouping, inhibition, silences), Alertmanager конфигурация.

| Severity | Response Time | Канал |
|----------|---------------|-------|
| critical | 5 минут | Phone + SMS |
| high | 15 минут | Slack + Push |
| warning | 1 час | Slack |

**Инструкция:** [observability/alerting.md](./observability/alerting.md)

