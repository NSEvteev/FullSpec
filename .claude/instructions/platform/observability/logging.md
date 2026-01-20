---
type: standard
description: Централизованные логи — Loki, structured logging, корреляция с trace_id
related:
  - platform/observability/overview.md
  - platform/observability/tracing.md
  - platform/operations.md
  - src/data/logging.md
---

# Логирование (Loki)

Правила централизованного логирования: структурированные логи, Loki, корреляция.

## Оглавление

- [Правила](#правила)
  - [Structured Logging](#structured-logging)
  - [Log Levels](#log-levels)
  - [Обязательные поля](#обязательные-поля)
  - [Корреляция с трейсами](#корреляция-с-трейсами)
  - [Loki конфигурация](#loki-конфигурация)
  - [LogQL запросы](#logql-запросы)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Structured Logging

**Правило:** Все логи в формате JSON.

```json
{
  "timestamp": "2024-01-15T14:30:00.000Z",
  "level": "info",
  "message": "User logged in",
  "service": "auth-server",
  "trace_id": "abc123def456",
  "span_id": "789xyz",
  "request_id": "req-001",
  "user_id": "user-123",
  "duration_ms": 45
}
```

**Правило:** Не использовать string interpolation для структурированных данных.

```python
# Неправильно
logger.info(f"User {user_id} logged in after {duration}ms")

# Правильно
logger.info("User logged in", extra={
    "user_id": user_id,
    "duration_ms": duration
})
```

**Правило:** Консистентные имена полей.

| Поле | Формат | Пример |
|------|--------|--------|
| Timestamp | ISO 8601 | `2024-01-15T14:30:00.000Z` |
| Duration | `_ms` или `_seconds` | `duration_ms`, `latency_seconds` |
| Count | `_count` | `retry_count` |
| Size | `_bytes` | `request_size_bytes` |
| ID | `_id` | `user_id`, `order_id` |

### Log Levels

**Правило:** Использовать правильный уровень логирования.

| Level | Когда использовать | Примеры |
|-------|-------------------|---------|
| `error` | Ошибка, требующая внимания | Exception, failed request |
| `warn` | Потенциальная проблема | Retry, deprecation |
| `info` | Значимое событие | Request completed, user action |
| `debug` | Детали для отладки | Variable values, flow |
| `trace` | Очень детальная информация | Function entry/exit |

**Правило:** Production уровень — `info` и выше.

```python
import os
import logging

level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, level))
```

**Правило:** Не логировать sensitive data.

```python
# Неправильно
logger.info("Login attempt", extra={
    "email": user.email,
    "password": password,  # НИКОГДА!
    "credit_card": card_number  # НИКОГДА!
})

# Правильно
logger.info("Login attempt", extra={
    "user_id": user.id,
    "email_domain": user.email.split("@")[1]  # Только домен
})
```

### Обязательные поля

**Правило:** Каждый лог содержит обязательные поля.

| Поле | Источник | Описание |
|------|----------|----------|
| `timestamp` | Автоматически | ISO 8601 с timezone |
| `level` | Logger | info, warn, error, debug |
| `message` | Разработчик | Человекочитаемое описание |
| `service` | Конфигурация | Имя сервиса |
| `environment` | Конфигурация | production, staging, dev |
| `version` | Конфигурация | Версия приложения |

**Правило:** Request-scoped поля для HTTP.

| Поле | Описание |
|------|----------|
| `request_id` | Уникальный ID запроса |
| `trace_id` | OpenTelemetry trace ID |
| `span_id` | OpenTelemetry span ID |
| `method` | HTTP method |
| `path` | Request path |
| `status` | Response status |
| `duration_ms` | Request duration |
| `user_id` | Authenticated user (если есть) |

### Корреляция с трейсами

**Правило:** Добавлять trace_id и span_id в каждый лог.

```python
import logging
from opentelemetry import trace

class TraceContextFilter(logging.Filter):
    """Добавляет trace context в логи."""

    def filter(self, record):
        span = trace.get_current_span()
        if span.is_recording():
            ctx = span.get_span_context()
            record.trace_id = format(ctx.trace_id, '032x')
            record.span_id = format(ctx.span_id, '016x')
        else:
            record.trace_id = "0" * 32
            record.span_id = "0" * 16
        return True

# Добавить filter
logger = logging.getLogger()
logger.addFilter(TraceContextFilter())
```

**Правило:** Настроить Grafana для перехода от логов к трейсам.

```yaml
# grafana/provisioning/datasources.yml
datasources:
  - name: Loki
    type: loki
    url: http://loki:3100
    jsonData:
      derivedFields:
        - name: trace_id
          matcherRegex: '"trace_id":"(\w+)"'
          url: '$${__value.raw}'
          datasourceUid: tempo
          urlDisplayLabel: 'View Trace'
```

### Loki конфигурация

**Правило:** Labels для эффективной индексации.

```yaml
# promtail-config.yml
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      # Парсить JSON
      - json:
          expressions:
            level: level
            service: service
            trace_id: trace_id

      # Создать labels (только low-cardinality!)
      - labels:
          level:
          service:

      # Timestamp из JSON
      - timestamp:
          source: timestamp
          format: RFC3339Nano

      # НЕ добавлять high-cardinality как labels
      # trace_id, user_id, request_id -> только в log line
```

**Правило:** Labels должны быть low-cardinality.

| Хороший label | Плохой label |
|---------------|--------------|
| `service` | `user_id` |
| `environment` | `request_id` |
| `level` | `trace_id` |
| `namespace` | `timestamp` |

**Правило:** Loki retention policy.

```yaml
# loki-config.yml
schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

compactor:
  working_directory: /loki/compactor
  shared_store: filesystem
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150

limits_config:
  retention_period: 720h  # 30 дней
```

### LogQL запросы

**Правило:** Использовать LogQL для поиска и агрегации.

```logql
# Все ошибки сервиса
{service="api-server"} |= "error"

# JSON parsing + фильтр
{service="api-server"} | json | level="error"

# Фильтр по полю
{service="api-server"} | json | status >= 500

# Regex поиск
{service="api-server"} |~ "user.*failed"

# Исключить паттерн
{service="api-server"} != "health check"

# По trace_id
{service=~".+"} | json | trace_id="abc123def456"

# Агрегация: rate ошибок
sum(rate({service="api-server"} | json | level="error" [5m]))

# Топ ошибок по message
topk(10,
  sum by (message) (
    count_over_time({service="api-server"} | json | level="error" [1h])
  )
)
```

**Правило:** Оптимизация запросов.

```logql
# Медленно — сканирует все логи
{job="app"} | json | user_id="123"

# Быстро — использует label
{service="api-server", level="error"}

# Ещё быстрее — сначала label, потом фильтр
{service="api-server", level="error"} | json | status=500
```

---

## Примеры

### Пример 1: Python structured logging

```python
import logging
import json
import sys
from datetime import datetime
from opentelemetry import trace

class JSONFormatter(logging.Formatter):
    """Форматтер для JSON логов."""

    def __init__(self, service: str, version: str, environment: str):
        super().__init__()
        self.service = service
        self.version = version
        self.environment = environment

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname.lower(),
            "message": record.getMessage(),
            "service": self.service,
            "version": self.version,
            "environment": self.environment,
            "logger": record.name,
        }

        # Trace context
        if hasattr(record, 'trace_id'):
            log_entry["trace_id"] = record.trace_id
            log_entry["span_id"] = record.span_id

        # Extra fields
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)

        # Exception info
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str)


def setup_logging(service: str, version: str, environment: str):
    """Настройка structured logging."""

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter(service, version, environment))

    # Trace context filter
    class TraceFilter(logging.Filter):
        def filter(self, record):
            span = trace.get_current_span()
            if span.is_recording():
                ctx = span.get_span_context()
                record.trace_id = format(ctx.trace_id, '032x')
                record.span_id = format(ctx.span_id, '016x')
            else:
                record.trace_id = None
                record.span_id = None
            return True

    handler.addFilter(TraceFilter())

    logging.root.handlers = [handler]
    logging.root.setLevel(logging.INFO)


# Logger adapter с extra fields
class ContextLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = kwargs.get('extra', {})
        extra['extra_fields'] = {**self.extra, **extra.pop('extra_fields', {})}
        kwargs['extra'] = extra
        return msg, kwargs


# Использование
setup_logging("api-server", "1.2.3", "production")

logger = ContextLogger(
    logging.getLogger(__name__),
    {"request_id": "req-123"}
)

logger.info("User logged in", extra={"extra_fields": {"user_id": "user-456"}})
```

### Пример 2: Go structured logging

```go
package main

import (
    "context"
    "os"

    "go.opentelemetry.io/otel/trace"
    "go.uber.org/zap"
    "go.uber.org/zap/zapcore"
)

var logger *zap.Logger

func initLogger(service, version, environment string) {
    config := zap.NewProductionEncoderConfig()
    config.TimeKey = "timestamp"
    config.EncodeTime = zapcore.ISO8601TimeEncoder
    config.MessageKey = "message"
    config.LevelKey = "level"

    core := zapcore.NewCore(
        zapcore.NewJSONEncoder(config),
        zapcore.AddSync(os.Stdout),
        zapcore.InfoLevel,
    )

    logger = zap.New(core).With(
        zap.String("service", service),
        zap.String("version", version),
        zap.String("environment", environment),
    )
}

// WithTraceContext добавляет trace context к logger
func WithTraceContext(ctx context.Context) *zap.Logger {
    span := trace.SpanFromContext(ctx)
    if span.SpanContext().IsValid() {
        return logger.With(
            zap.String("trace_id", span.SpanContext().TraceID().String()),
            zap.String("span_id", span.SpanContext().SpanID().String()),
        )
    }
    return logger
}

// Использование
func handleRequest(ctx context.Context, userID string) {
    log := WithTraceContext(ctx)

    log.Info("Processing request",
        zap.String("user_id", userID),
        zap.String("action", "login"),
    )
}
```

### Пример 3: Request logging middleware

```python
import time
import uuid
from flask import Flask, request, g
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    g.start_time = time.time()

    logger.info("Request started", extra={"extra_fields": {
        "request_id": g.request_id,
        "method": request.method,
        "path": request.path,
        "remote_addr": request.remote_addr,
        "user_agent": request.user_agent.string,
    }})

@app.after_request
def after_request(response):
    duration_ms = (time.time() - g.start_time) * 1000

    logger.info("Request completed", extra={"extra_fields": {
        "request_id": g.request_id,
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "duration_ms": round(duration_ms, 2),
        "response_size_bytes": response.content_length,
    }})

    response.headers['X-Request-ID'] = g.request_id
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error("Request failed", extra={"extra_fields": {
        "request_id": g.request_id,
        "error": str(e),
        "error_type": type(e).__name__,
    }}, exc_info=True)

    return {"error": "Internal server error"}, 500
```

### Пример 4: Promtail конфигурация для Kubernetes

```yaml
# promtail-config.yml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push
    tenant_id: default

scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod

    relabel_configs:
      # Keep only pods with annotation
      - source_labels: [__meta_kubernetes_pod_annotation_promtail_io_scrape]
        action: keep
        regex: true

      # Namespace label
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace

      # Pod name label
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod

      # Container name label
      - source_labels: [__meta_kubernetes_pod_container_name]
        target_label: container

      # App label from pod
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app

    pipeline_stages:
      # Detect JSON logs
      - match:
          selector: '{app=~".+"}'
          stages:
            - json:
                expressions:
                  level: level
                  service: service
                  timestamp: timestamp

            - labels:
                level:
                service:

            - timestamp:
                source: timestamp
                format: RFC3339Nano

      # Multiline for stack traces (non-JSON)
      - multiline:
          firstline: '^\d{4}-\d{2}-\d{2}'
          max_wait_time: 3s
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Логи не появляются в Loki — что делать?

1. **Проверить Promtail:**
   ```bash
   # Targets
   curl http://promtail:9080/targets

   # Ready
   curl http://promtail:9080/ready
   ```

2. **Проверить labels:**
   ```bash
   # Должны быть low-cardinality labels
   curl http://loki:3100/loki/api/v1/labels
   ```

3. **Проверить формат логов:**
   ```bash
   # Должен быть валидный JSON (если ожидается JSON)
   kubectl logs pod-name | jq .
   ```

4. **Проверить Loki:**
   ```bash
   curl http://loki:3100/ready
   curl http://loki:3100/metrics | grep loki_ingester
   ```

### Запросы LogQL медленные — как оптимизировать?

1. **Использовать labels:**
   ```logql
   # Медленно
   {job="app"} | json | service="api"

   # Быстро
   {service="api"}
   ```

2. **Сузить time range:**
   ```logql
   # Быстрее
   {service="api"} [1h]
   ```

3. **Фильтровать раньше:**
   ```logql
   # Медленно
   {service="api"} | json | line_format "{{.message}}" | level="error"

   # Быстро
   {service="api", level="error"}
   ```

### Как найти все логи одного запроса?

```logql
# По request_id
{service=~".+"} | json | request_id="req-123"

# По trace_id (все сервисы)
{service=~".+"} | json | trace_id="abc123def456"

# Комбинация
{service=~".+"} | json | trace_id="abc123def456" | level="error"
```

### Как агрегировать ошибки по типу?

```logql
# Топ ошибок за час
topk(10,
  sum by (error_type, service) (
    count_over_time(
      {level="error"} | json [1h]
    )
  )
)

# Rate ошибок по сервису
sum by (service) (
  rate({level="error"} [5m])
)
```

### Retention: как долго хранить логи?

| Окружение | Retention | Причина |
|-----------|-----------|---------|
| Production | 30 дней | Расследования, compliance |
| Staging | 7 дней | Достаточно для тестирования |
| Development | 1 день | Минимум для отладки |

```yaml
# loki-config.yml
limits_config:
  retention_period: 720h  # 30 дней
```

---

## Связанные инструкции

- [overview.md](overview.md) — Обзор observability
- [tracing.md](tracing.md) — Корреляция с трейсами
- [operations.md](../operations.md) — Runbooks с логами
- [logging.md](../../src/data/logging.md) — Формат логов в коде
