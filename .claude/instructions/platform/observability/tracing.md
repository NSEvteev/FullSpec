---
type: standard
description: Distributed tracing — OpenTelemetry, spans, W3C traceparent, Tempo
related:
  - platform/observability/overview.md
  - platform/observability/logging.md
  - platform/observability/metrics.md
---

# Distributed Tracing

Правила distributed tracing: OpenTelemetry, spans, context propagation, Tempo.

## Оглавление

- [Правила](#правила)
  - [Основные концепции](#основные-концепции)
  - [OpenTelemetry](#opentelemetry)
  - [Span атрибуты](#span-атрибуты)
  - [Context Propagation](#context-propagation)
  - [Sampling](#sampling)
  - [Инструментирование](#инструментирование)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Основные концепции

**Правило:** Понимать иерархию trace → span → events.

```
Trace (trace_id: abc123)
│
├── Span: HTTP GET /api/users (span_id: span1, parent: null)
│   │
│   ├── Span: auth.validate (span_id: span2, parent: span1)
│   │   └── Event: "token validated"
│   │
│   ├── Span: db.query (span_id: span3, parent: span1)
│   │   ├── Event: "query started"
│   │   └── Event: "query completed"
│   │
│   └── Span: cache.get (span_id: span4, parent: span1)
│
└── Total duration: 150ms
```

| Понятие | Описание | Пример |
|---------|----------|--------|
| Trace | Весь путь запроса | Запрос от клиента до ответа |
| Span | Отдельная операция | HTTP вызов, DB query |
| Span Context | Идентификаторы для связывания | trace_id, span_id |
| Event | Событие внутри span | Log entry, exception |
| Link | Связь между traces | Async processing |

**Правило:** Каждый span имеет обязательные поля.

| Поле | Описание |
|------|----------|
| `trace_id` | 128-bit ID всего trace |
| `span_id` | 64-bit ID этого span |
| `parent_span_id` | ID родительского span (null для root) |
| `name` | Имя операции |
| `start_time` | Время начала |
| `end_time` | Время окончания |
| `status` | OK, ERROR, UNSET |

### OpenTelemetry

**Правило:** Использовать OpenTelemetry как стандарт трейсинга.

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenTelemetry Architecture               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Application                                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ OTel SDK                                              │  │
│  │ ┌────────────┐ ┌────────────┐ ┌────────────┐        │  │
│  │ │   Tracer   │ │   Meter    │ │   Logger   │        │  │
│  │ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘        │  │
│  │       │              │              │                │  │
│  │       └──────────────┼──────────────┘                │  │
│  │                      ▼                               │  │
│  │              ┌───────────────┐                       │  │
│  │              │   Exporter    │                       │  │
│  │              └───────┬───────┘                       │  │
│  └──────────────────────┼───────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│              ┌───────────────────┐                         │
│              │  OTel Collector   │                         │
│              │ (process, batch)  │                         │
│              └─────────┬─────────┘                         │
│                        │                                    │
│           ┌────────────┼────────────┐                      │
│           ▼            ▼            ▼                      │
│      ┌────────┐   ┌────────┐   ┌────────┐                 │
│      │ Tempo  │   │Prometheus│  │  Loki  │                 │
│      │(traces)│   │(metrics) │  │ (logs) │                 │
│      └────────┘   └────────┘   └────────┘                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Правило:** Настройка SDK с resource attributes.

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Resource описывает сервис
resource = Resource.create({
    SERVICE_NAME: "api-server",
    SERVICE_VERSION: "1.2.3",
    "deployment.environment": "production",
    "service.namespace": "backend",
})

# Создать provider
provider = TracerProvider(resource=resource)

# Добавить exporter
exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",
    insecure=True
)
provider.add_span_processor(BatchSpanProcessor(exporter))

# Установить глобально
trace.set_tracer_provider(provider)

# Получить tracer
tracer = trace.get_tracer(__name__)
```

### Span атрибуты

**Правило:** Использовать семантические конвенции OpenTelemetry.

| Категория | Атрибут | Пример |
|-----------|---------|--------|
| HTTP | `http.method` | `GET` |
| HTTP | `http.url` | `https://api.example.com/users` |
| HTTP | `http.status_code` | `200` |
| HTTP | `http.route` | `/api/v1/users/{id}` |
| Database | `db.system` | `postgresql` |
| Database | `db.statement` | `SELECT * FROM users WHERE id = $1` |
| Database | `db.operation` | `SELECT` |
| RPC | `rpc.system` | `grpc` |
| RPC | `rpc.service` | `UserService` |
| RPC | `rpc.method` | `GetUser` |

**Правило:** Добавлять бизнес-атрибуты с префиксом `app.`.

```python
with tracer.start_as_current_span("process_order") as span:
    span.set_attribute("app.order.id", order_id)
    span.set_attribute("app.order.total", order.total)
    span.set_attribute("app.customer.tier", customer.tier)
    span.set_attribute("app.items.count", len(order.items))
```

**Правило:** Не добавлять PII (персональные данные) в атрибуты.

```python
# Неправильно — PII
span.set_attribute("user.email", "user@example.com")
span.set_attribute("user.phone", "+1234567890")

# Правильно — идентификаторы
span.set_attribute("user.id", "user-123")
span.set_attribute("user.tier", "premium")
```

### Context Propagation

**Правило:** Использовать W3C Trace Context для propagation.

```
HTTP Headers:
traceparent: 00-{trace_id}-{span_id}-{flags}
             │   │          │         │
             │   │          │         └── 01 = sampled
             │   │          └── 16 hex chars
             │   └── 32 hex chars
             └── version

Пример:
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
tracestate: vendor1=value1,vendor2=value2
```

**Правило:** Инжектировать и извлекать context.

```python
from opentelemetry.propagate import inject, extract
from opentelemetry import trace

# Исходящий HTTP запрос
def make_request(url: str):
    headers = {}
    inject(headers)  # Добавляет traceparent header

    with tracer.start_as_current_span("http_client") as span:
        span.set_attribute("http.url", url)
        response = requests.get(url, headers=headers)
        span.set_attribute("http.status_code", response.status_code)
        return response

# Входящий HTTP запрос
def handle_request(request):
    # Извлечь context из headers
    context = extract(request.headers)

    with tracer.start_as_current_span(
        "http_server",
        context=context,
        kind=SpanKind.SERVER
    ) as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.route", request.path)
        # Process request...
```

**Правило:** Для async messaging передавать context в message headers.

```python
# Producer
def publish_message(message: dict):
    headers = {}
    inject(headers)

    kafka_producer.send(
        topic="orders",
        value=message,
        headers=[(k, v.encode()) for k, v in headers.items()]
    )

# Consumer
def consume_message(message):
    headers = {k: v.decode() for k, v in message.headers}
    context = extract(headers)

    with tracer.start_as_current_span(
        "process_message",
        context=context,
        kind=SpanKind.CONSUMER
    ):
        # Process message...
```

### Sampling

**Правило:** Использовать sampling для контроля объёма данных.

| Стратегия | Описание | Когда использовать |
|-----------|----------|-------------------|
| AlwaysOn | 100% трейсов | Development |
| AlwaysOff | 0% трейсов | Disabled |
| TraceIdRatio | Процент по trace_id | Production |
| ParentBased | Наследовать от parent | Микросервисы |

```python
from opentelemetry.sdk.trace.sampling import (
    TraceIdRatioBased,
    ParentBasedTraceIdRatio,
)

# 10% трейсов
sampler = TraceIdRatioBased(0.1)

# Parent-based: если parent sampled, то и child sampled
sampler = ParentBasedTraceIdRatio(0.1)

provider = TracerProvider(
    resource=resource,
    sampler=sampler
)
```

**Правило:** Head-based vs Tail-based sampling.

| Тип | Когда решение | Плюсы | Минусы |
|-----|---------------|-------|--------|
| Head-based | В начале trace | Простота | Теряем интересные трейсы |
| Tail-based | В конце trace | Умный выбор | Сложность, буфер |

```yaml
# OTel Collector tail-based sampling
processors:
  tail_sampling:
    decision_wait: 10s
    num_traces: 100000
    policies:
      # Всегда сохранять ошибки
      - name: errors
        type: status_code
        status_code:
          status_codes: [ERROR]
      # Всегда сохранять медленные
      - name: slow
        type: latency
        latency:
          threshold_ms: 1000
      # 10% остальных
      - name: default
        type: probabilistic
        probabilistic:
          sampling_percentage: 10
```

### Инструментирование

**Правило:** Использовать автоматическое инструментирование где возможно.

```python
# Python auto-instrumentation
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

# Автоматически инструментирует все Flask routes
FlaskInstrumentor().instrument()

# Автоматически инструментирует все HTTP вызовы
RequestsInstrumentor().instrument()

# Автоматически инструментирует все DB queries
SQLAlchemyInstrumentor().instrument()

# Автоматически инструментирует Redis
RedisInstrumentor().instrument()
```

**Правило:** Добавлять ручное инструментирование для бизнес-логики.

```python
@tracer.start_as_current_span("process_payment")
def process_payment(order: Order):
    span = trace.get_current_span()
    span.set_attribute("app.order.id", order.id)
    span.set_attribute("app.payment.method", order.payment_method)

    try:
        with tracer.start_as_current_span("validate_card"):
            validate_card(order.card)

        with tracer.start_as_current_span("charge_amount"):
            result = charge(order.card, order.total)
            span.set_attribute("app.payment.transaction_id", result.tx_id)

        span.set_status(StatusCode.OK)
        return result

    except PaymentError as e:
        span.set_status(StatusCode.ERROR, str(e))
        span.record_exception(e)
        raise
```

---

## Примеры

### Пример 1: Полная настройка Python сервиса

```python
# tracing.py
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator

def setup_tracing(service_name: str, service_version: str):
    """Настройка OpenTelemetry tracing."""

    # Resource
    resource = Resource.create({
        "service.name": service_name,
        "service.version": service_version,
        "deployment.environment": os.environ.get("ENVIRONMENT", "development"),
        "host.name": os.environ.get("HOSTNAME", "unknown"),
    })

    # Provider
    provider = TracerProvider(resource=resource)

    # Exporter
    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317")
    exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)

    # Processor
    processor = BatchSpanProcessor(
        exporter,
        max_queue_size=2048,
        max_export_batch_size=512,
        export_timeout_millis=30000,
    )
    provider.add_span_processor(processor)

    # Set global
    trace.set_tracer_provider(provider)

    # Propagator (W3C Trace Context + Baggage)
    set_global_textmap(CompositePropagator([
        TraceContextTextMapPropagator(),
        W3CBaggagePropagator(),
    ]))

    return trace.get_tracer(service_name)


# app.py
from flask import Flask, request
from tracing import setup_tracing
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = Flask(__name__)
tracer = setup_tracing("api-server", "1.2.3")

# Auto-instrument
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route("/api/users/<user_id>")
def get_user(user_id: str):
    with tracer.start_as_current_span("get_user_handler") as span:
        span.set_attribute("app.user.id", user_id)

        user = fetch_user(user_id)

        if not user:
            span.set_status(StatusCode.ERROR, "User not found")
            return {"error": "Not found"}, 404

        return user
```

### Пример 2: Go сервис с трейсингом

```go
package main

import (
    "context"
    "net/http"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/propagation"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
    "go.opentelemetry.io/otel/trace"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

var tracer trace.Tracer

func initTracer() func() {
    ctx := context.Background()

    // Exporter
    exporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        panic(err)
    }

    // Resource
    res, err := resource.New(ctx,
        resource.WithAttributes(
            semconv.ServiceName("api-server"),
            semconv.ServiceVersion("1.2.3"),
            attribute.String("environment", "production"),
        ),
    )
    if err != nil {
        panic(err)
    }

    // Provider
    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(res),
        sdktrace.WithSampler(sdktrace.TraceIDRatioBased(0.1)),
    )

    otel.SetTracerProvider(tp)
    otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
        propagation.TraceContext{},
        propagation.Baggage{},
    ))

    tracer = tp.Tracer("api-server")

    return func() {
        tp.Shutdown(ctx)
    }
}

func main() {
    shutdown := initTracer()
    defer shutdown()

    // Wrap handler with tracing
    handler := otelhttp.NewHandler(
        http.HandlerFunc(handleRequest),
        "HTTP Server",
    )

    http.ListenAndServe(":8080", handler)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    ctx, span := tracer.Start(ctx, "handleRequest")
    defer span.End()

    span.SetAttributes(
        attribute.String("app.request.id", r.Header.Get("X-Request-ID")),
    )

    // Process request...
}
```

### Пример 3: Межсервисный трейсинг

```python
# Service A
from opentelemetry import trace
from opentelemetry.propagate import inject
import requests

tracer = trace.get_tracer(__name__)

def call_service_b(data: dict):
    with tracer.start_as_current_span(
        "call_service_b",
        kind=SpanKind.CLIENT
    ) as span:
        headers = {"Content-Type": "application/json"}
        inject(headers)  # Добавить trace context

        span.set_attribute("http.method", "POST")
        span.set_attribute("http.url", "http://service-b/api/process")
        span.set_attribute("peer.service", "service-b")

        response = requests.post(
            "http://service-b/api/process",
            json=data,
            headers=headers
        )

        span.set_attribute("http.status_code", response.status_code)
        return response.json()


# Service B
from flask import Flask, request
from opentelemetry import trace
from opentelemetry.propagate import extract

app = Flask(__name__)
tracer = trace.get_tracer(__name__)

@app.route("/api/process", methods=["POST"])
def process():
    # Извлечь trace context из headers
    context = extract(request.headers)

    with tracer.start_as_current_span(
        "process_request",
        context=context,
        kind=SpanKind.SERVER
    ) as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.route", "/api/process")

        data = request.json
        result = do_processing(data)

        return {"result": result}
```

### Пример 4: Трейсинг с async/await

```python
import asyncio
from opentelemetry import trace
from opentelemetry.trace import SpanKind

tracer = trace.get_tracer(__name__)

async def process_order(order_id: str):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("app.order.id", order_id)

        # Параллельные операции сохраняют parent span
        results = await asyncio.gather(
            validate_order(order_id),
            check_inventory(order_id),
            calculate_shipping(order_id),
        )

        with tracer.start_as_current_span("finalize_order"):
            return finalize(order_id, results)


async def validate_order(order_id: str):
    # Автоматически связан с parent span
    with tracer.start_as_current_span("validate_order") as span:
        span.set_attribute("app.order.id", order_id)
        await asyncio.sleep(0.1)  # Simulate work
        return True


async def check_inventory(order_id: str):
    with tracer.start_as_current_span("check_inventory") as span:
        span.set_attribute("app.order.id", order_id)
        await asyncio.sleep(0.05)
        return {"available": True}


async def calculate_shipping(order_id: str):
    with tracer.start_as_current_span("calculate_shipping") as span:
        span.set_attribute("app.order.id", order_id)
        await asyncio.sleep(0.02)
        return {"cost": 9.99}
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Трейсы не появляются в Tempo — что делать?

1. **Проверить exporter:**
   ```python
   # Добавить debug exporter
   from opentelemetry.sdk.trace.export import ConsoleSpanExporter
   provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
   ```

2. **Проверить endpoint:**
   ```bash
   # Проверить доступность collector
   curl -v http://otel-collector:4318/v1/traces
   ```

3. **Проверить sampling:**
   ```python
   # Временно включить 100%
   sampler = TraceIdRatioBased(1.0)
   ```

4. **Проверить collector logs:**
   ```bash
   docker logs otel-collector
   ```

### Как найти медленную операцию в trace?

1. **В Grafana Tempo:**
   - Открыть trace
   - Посмотреть waterfall view
   - Найти span с максимальной duration

2. **TraceQL запрос:**
   ```traceql
   { duration > 1s && status = error }
   ```

3. **Программно:**
   ```python
   # Добавить события для измерения
   with tracer.start_as_current_span("slow_operation") as span:
       span.add_event("started_step_1")
       step1()
       span.add_event("completed_step_1")

       span.add_event("started_step_2")
       step2()
       span.add_event("completed_step_2")
   ```

### Context теряется между async операциями — как исправить?

```python
import contextvars
from opentelemetry import context

# Вручную передавать context
async def process():
    ctx = context.get_current()

    async def subtask():
        # Восстановить context
        token = context.attach(ctx)
        try:
            with tracer.start_as_current_span("subtask"):
                await do_work()
        finally:
            context.detach(token)

    await asyncio.gather(subtask(), subtask())
```

### Как уменьшить объём трейсов без потери важных?

1. **Tail-based sampling с правилами:**
   ```yaml
   policies:
     - name: errors
       type: status_code
       status_codes: [ERROR]
     - name: slow
       type: latency
       threshold_ms: 1000
     - name: default
       type: probabilistic
       sampling_percentage: 5
   ```

2. **Фильтровать неинтересные spans:**
   ```yaml
   processors:
     filter:
       spans:
         exclude:
           match_type: regexp
           attributes:
             - key: http.route
               value: "^/health"
   ```

3. **Уменьшить количество атрибутов:**
   ```python
   # Только важные атрибуты
   span.set_attribute("app.order.id", order_id)
   # НЕ добавлять все поля объекта
   ```

---

## Связанные инструкции

- [overview.md](overview.md) — Обзор observability
- [logging.md](logging.md) — Корреляция с логами
- [metrics.md](metrics.md) — Exemplars для связи с метриками
