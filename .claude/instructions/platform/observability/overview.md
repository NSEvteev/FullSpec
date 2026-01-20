---
type: standard
description: Обзор наблюдаемости — три столпа (logs, metrics, traces), стек Grafana
related:
  - platform/observability/metrics.md
  - platform/observability/tracing.md
  - platform/observability/logging.md
  - platform/observability/alerting.md
  - platform/operations.md
---

# Observability: Обзор

Три столпа наблюдаемости: логи, метрики, трейсы. Стек и интеграция.

## Оглавление

- [Три столпа](#три-столпа)
- [Стек технологий](#стек-технологий)
- [Корреляция данных](#корреляция-данных)
- [Dashboards](#dashboards)
- [Best Practices](#best-practices)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Три столпа

**Правило:** Полная наблюдаемость требует всех трёх компонентов.

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌───────────┐     ┌───────────┐     ┌───────────┐        │
│   │   LOGS    │     │  METRICS  │     │  TRACES   │        │
│   │           │     │           │     │           │        │
│   │ Loki      │     │ Prometheus│     │   Tempo   │        │
│   │           │     │           │     │           │        │
│   │ "Что      │     │ "Сколько" │     │ "Где"     │        │
│   │ произошло"│     │           │     │           │        │
│   └─────┬─────┘     └─────┬─────┘     └─────┬─────┘        │
│         │                 │                 │               │
│         └────────────┬────┴────────────────┘               │
│                      │                                      │
│                      ▼                                      │
│              ┌───────────────┐                              │
│              │   GRAFANA     │                              │
│              │  Dashboards   │                              │
│              │  Alerting     │                              │
│              └───────────────┘                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

| Столп | Назначение | Вопрос | Инструмент |
|-------|------------|--------|------------|
| Logs | Детальные события | Что произошло? | Loki |
| Metrics | Агрегированные числа | Сколько? Как быстро? | Prometheus |
| Traces | Распределённые запросы | Где задержка? | Tempo |

**Правило:** Все три столпа связаны через общие идентификаторы.

| Идентификатор | Описание | Пример |
|---------------|----------|--------|
| `trace_id` | ID распределённого запроса | `abc123def456` |
| `span_id` | ID операции в трейсе | `789xyz` |
| `request_id` | Пользовательский ID запроса | `req-2024-01-15-001` |
| `service` | Имя сервиса | `api-server` |

---

## Стек технологий

**Правило:** Использовать Grafana Stack для единообразия.

```yaml
# docker-compose.observability.yml
version: '3.8'

services:
  # Метрики
  prometheus:
    image: prom/prometheus:v2.48.0
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=15d'
      - '--web.enable-remote-write-receiver'
    ports:
      - "9090:9090"

  # Логи
  loki:
    image: grafana/loki:2.9.0
    volumes:
      - ./loki-config.yml:/etc/loki/local-config.yaml
      - loki_data:/loki
    ports:
      - "3100:3100"

  # Трейсы
  tempo:
    image: grafana/tempo:2.3.0
    volumes:
      - ./tempo-config.yml:/etc/tempo/config.yaml
      - tempo_data:/tmp/tempo
    ports:
      - "3200:3200"   # Tempo API
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP

  # Визуализация
  grafana:
    image: grafana/grafana:10.2.0
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_FEATURE_TOGGLES_ENABLE=traceqlEditor
    ports:
      - "3000:3000"

  # Сбор метрик и трейсов
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.91.0
    volumes:
      - ./otel-config.yml:/etc/otel/config.yaml
    command: ["--config=/etc/otel/config.yaml"]
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "8889:8889"   # Prometheus metrics

volumes:
  prometheus_data:
  loki_data:
  tempo_data:
  grafana_data:
```

**Правило:** Конфигурация OpenTelemetry Collector.

```yaml
# otel-config.yml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

  # Добавить атрибуты
  attributes:
    actions:
      - key: environment
        value: ${ENVIRONMENT}
        action: upsert

exporters:
  # Метрики → Prometheus
  prometheus:
    endpoint: "0.0.0.0:8889"

  # Трейсы → Tempo
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true

  # Логи → Loki
  loki:
    endpoint: http://loki:3100/loki/api/v1/push

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, attributes]
      exporters: [otlp/tempo]

    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]

    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [loki]
```

---

## Корреляция данных

**Правило:** Связывать логи, метрики и трейсы через общие labels.

```
User Request
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  trace_id: abc123                                           │
│  request_id: req-001                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  API Gateway ──────► Auth Service ──────► User Service      │
│       │                    │                    │            │
│       ▼                    ▼                    ▼            │
│   ┌───────┐           ┌───────┐           ┌───────┐         │
│   │ Span  │           │ Span  │           │ Span  │         │
│   │ Logs  │           │ Logs  │           │ Logs  │         │
│   │Metrics│           │Metrics│           │Metrics│         │
│   └───────┘           └───────┘           └───────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Правило:** Передавать trace context между сервисами.

```python
# Python пример с OpenTelemetry
from opentelemetry import trace
from opentelemetry.propagate import inject, extract

tracer = trace.get_tracer(__name__)

# Исходящий запрос
def call_service(url: str):
    headers = {}
    inject(headers)  # Добавить trace context в headers

    with tracer.start_as_current_span("http_call") as span:
        span.set_attribute("http.url", url)
        response = requests.get(url, headers=headers)
        return response

# Входящий запрос
def handle_request(request):
    context = extract(request.headers)  # Извлечь trace context

    with tracer.start_as_current_span("handle_request", context=context):
        # Логирование с trace_id
        logger.info("Processing request", extra={
            "trace_id": trace.get_current_span().get_span_context().trace_id
        })
```

**Правило:** Grafana автоматически связывает данные.

```yaml
# grafana/provisioning/datasources/datasources.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    jsonData:
      exemplarTraceIdDestinations:
        - name: trace_id
          datasourceUid: tempo

  - name: Loki
    type: loki
    url: http://loki:3100
    jsonData:
      derivedFields:
        - name: trace_id
          matcherRegex: 'trace_id=(\w+)'
          url: '$${__value.raw}'
          datasourceUid: tempo

  - name: Tempo
    type: tempo
    url: http://tempo:3200
    jsonData:
      tracesToLogs:
        datasourceUid: loki
        tags: ['service']
        mappedTags: [{ key: 'service.name', value: 'service' }]
        mapTagNamesEnabled: true
        filterByTraceID: true
      tracesToMetrics:
        datasourceUid: prometheus
        tags: [{ key: 'service.name', value: 'service' }]
```

---

## Dashboards

**Правило:** Иерархия dashboards: Overview → Service → Detail.

```
┌─────────────────────────────────────────────────────────────┐
│                    Dashboard Hierarchy                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Level 1: Overview                                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ System Health │ All Services │ Key Metrics │ Alerts    ││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                   │
│                          ▼                                   │
│  Level 2: Service                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ API Server   │  │ Auth Service │  │ User Service │      │
│  │ • Requests   │  │ • Requests   │  │ • Requests   │      │
│  │ • Latency    │  │ • Latency    │  │ • Latency    │      │
│  │ • Errors     │  │ • Errors     │  │ • Errors     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                          │                                   │
│                          ▼                                   │
│  Level 3: Detail                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Endpoint /v1 │  │ Database     │  │ Cache        │      │
│  │ • Per path   │  │ • Queries    │  │ • Hit ratio  │      │
│  │ • Per method │  │ • Latency    │  │ • Memory     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Правило:** RED метрики для каждого сервиса.

| Метрика | Описание | Prometheus |
|---------|----------|------------|
| Rate | Запросов в секунду | `rate(http_requests_total[5m])` |
| Errors | Процент ошибок | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])` |
| Duration | Latency p50/p95/p99 | `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))` |

**Правило:** USE метрики для ресурсов.

| Метрика | Описание | Prometheus |
|---------|----------|------------|
| Utilization | Процент использования | `container_cpu_usage_seconds_total` |
| Saturation | Очереди, задержки | `container_network_receive_packets_dropped_total` |
| Errors | Ошибки ресурса | `node_disk_io_time_seconds_total` |

---

## Best Practices

**Правило:** Стандартизировать labels across всех источников.

| Label | Описание | Пример |
|-------|----------|--------|
| `service` | Имя сервиса | `api-server` |
| `environment` | Окружение | `production` |
| `version` | Версия приложения | `v1.2.3` |
| `instance` | Инстанс | `api-server-abc123` |

**Правило:** Cardinality control — избегать high cardinality labels.

```yaml
# Неправильно — user_id создаст миллионы серий
http_requests_total{user_id="123", ...}

# Правильно — агрегировать до разумного уровня
http_requests_total{user_tier="premium", ...}
```

**Правило:** Retention policy по типу данных.

| Данные | Retention | Причина |
|--------|-----------|---------|
| Метрики (raw) | 15 дней | Высокая детализация |
| Метрики (downsampled) | 1 год | Тренды |
| Логи | 30 дней | Расследования |
| Трейсы | 7 дней | Отладка |

---

## Примеры

### Пример 1: Инструментирование Python сервиса

```python
# instrumentation.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
import logging

def setup_observability(service_name: str, version: str):
    resource = Resource.create({
        "service.name": service_name,
        "service.version": version,
        "deployment.environment": os.environ.get("ENVIRONMENT", "development")
    })

    # Traces
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(
            endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317")
        ))
    )

    # Metrics
    metrics.set_meter_provider(MeterProvider(
        resource=resource,
        metric_readers=[PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint="localhost:4317"),
            export_interval_millis=10000
        )]
    ))

    # Auto-instrumentation
    FlaskInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument()

    # Logging с trace context
    class TraceContextFilter(logging.Filter):
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

    logging.getLogger().addFilter(TraceContextFilter())
```

### Пример 2: Grafana dashboard JSON

```json
{
  "title": "Service Overview",
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{service=\"$service\"}[5m])) by (method, path)",
          "legendFormat": "{{method}} {{path}}"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{service=\"$service\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{service=\"$service\"}[5m])) * 100",
          "legendFormat": "Error %"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              {"value": 0, "color": "green"},
              {"value": 1, "color": "yellow"},
              {"value": 5, "color": "red"}
            ]
          },
          "unit": "percent"
        }
      }
    },
    {
      "title": "Latency Distribution",
      "type": "heatmap",
      "targets": [
        {
          "expr": "sum(rate(http_request_duration_seconds_bucket{service=\"$service\"}[5m])) by (le)",
          "format": "heatmap"
        }
      ]
    },
    {
      "title": "Recent Traces",
      "type": "traces",
      "datasource": "Tempo",
      "targets": [
        {
          "query": "{service=\"$service\"} | status = error",
          "limit": 20
        }
      ]
    }
  ],
  "templating": {
    "list": [
      {
        "name": "service",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(http_requests_total, service)"
      }
    ]
  }
}
```

### Пример 3: Связь через exemplars

```go
// Go пример с exemplars
import (
    "github.com/prometheus/client_golang/prometheus"
    "go.opentelemetry.io/otel/trace"
)

var httpDuration = prometheus.NewHistogramVec(
    prometheus.HistogramOpts{
        Name:    "http_request_duration_seconds",
        Help:    "HTTP request duration",
        Buckets: prometheus.DefBuckets,
    },
    []string{"method", "path", "status"},
)

func recordMetricWithExemplar(method, path, status string, duration float64, ctx context.Context) {
    span := trace.SpanFromContext(ctx)
    traceID := span.SpanContext().TraceID().String()

    httpDuration.WithLabelValues(method, path, status).(prometheus.ExemplarObserver).ObserveWithExemplar(
        duration,
        prometheus.Labels{"trace_id": traceID},
    )
}
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Как выбрать между логами и метриками?

| Сценарий | Использовать |
|----------|--------------|
| "Сколько запросов в секунду?" | Метрики |
| "Почему запрос упал?" | Логи + Трейс |
| "Какой процент ошибок?" | Метрики |
| "Что содержал запрос?" | Логи |
| "Где была задержка?" | Трейс |
| "Тренд за неделю?" | Метрики |

### Grafana не показывает данные — что делать?

1. **Проверить datasource:**
   - Configuration → Data sources → Test

2. **Проверить query:**
   - Explore → выполнить query напрямую

3. **Проверить time range:**
   - Данные могут быть вне выбранного диапазона

4. **Проверить labels:**
   ```promql
   # Посмотреть доступные labels
   http_requests_total
   ```

### Как уменьшить стоимость хранения?

1. **Уменьшить cardinality:**
   - Удалить ненужные labels
   - Агрегировать high-cardinality данные

2. **Настроить retention:**
   ```yaml
   # prometheus.yml
   global:
     scrape_interval: 15s
   storage:
     tsdb:
       retention.time: 15d
       retention.size: 50GB
   ```

3. **Downsampling:**
   - Использовать Thanos/Cortex для long-term storage

4. **Sampling трейсов:**
   ```yaml
   # otel-config.yml
   processors:
     probabilistic_sampler:
       sampling_percentage: 10  # 10% трейсов
   ```

### Как отладить отсутствующие трейсы?

1. **Проверить propagation:**
   ```bash
   curl -v -H "traceparent: 00-abc123-def456-01" http://service/api
   ```

2. **Проверить exporter:**
   ```bash
   # Логи collector
   docker logs otel-collector
   ```

3. **Проверить sampling:**
   - По умолчанию может быть < 100%

4. **Проверить Tempo:**
   ```bash
   curl http://tempo:3200/api/traces/abc123
   ```

---

## Связанные инструкции

- [metrics.md](metrics.md) — Prometheus метрики
- [tracing.md](tracing.md) — Distributed tracing
- [logging.md](logging.md) — Централизованные логи
- [alerting.md](alerting.md) — Алертинг
- [operations.md](../operations.md) — Runbooks и инциденты
