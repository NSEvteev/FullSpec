---
type: standard
description: Prometheus метрики — naming conventions, labels, типы метрик
related:
  - platform/observability/overview.md
  - platform/observability/alerting.md
  - platform/caching.md
---

# Метрики (Prometheus)

Правила работы с Prometheus метриками: именование, labels, типы, best practices.

## Оглавление

- [Правила](#правила)
  - [Naming Conventions](#naming-conventions)
  - [Labels](#labels)
  - [Типы метрик](#типы-метрик)
  - [Стандартные метрики](#стандартные-метрики)
  - [Cardinality](#cardinality)
  - [Scraping](#scraping)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Naming Conventions

**Правило:** Формат имени метрики: `{namespace}_{subsystem}_{name}_{unit}`.

| Компонент | Описание | Примеры |
|-----------|----------|---------|
| `namespace` | Приложение/сервис | `api`, `auth`, `payments` |
| `subsystem` | Подсистема | `http`, `db`, `cache` |
| `name` | Что измеряется | `requests`, `connections`, `duration` |
| `unit` | Единица измерения | `total`, `seconds`, `bytes` |

**Примеры:**

```
api_http_requests_total
api_http_request_duration_seconds
auth_db_connections_active
payments_cache_hits_total
```

**Правило:** Использовать snake_case.

```
# Правильно
http_request_duration_seconds

# Неправильно
httpRequestDurationSeconds
http-request-duration-seconds
```

**Правило:** Суффиксы по типу данных.

| Суффикс | Тип | Пример |
|---------|-----|--------|
| `_total` | Counter | `http_requests_total` |
| `_seconds` | Duration | `http_request_duration_seconds` |
| `_bytes` | Size | `http_response_size_bytes` |
| `_ratio` | Ratio 0-1 | `cache_hit_ratio` |
| `_info` | Metadata | `build_info` |
| `_bucket` | Histogram bucket | `http_request_duration_seconds_bucket` |

### Labels

**Правило:** Labels для группировки, не для уникальности.

| Хороший label | Плохой label |
|---------------|--------------|
| `method="GET"` | `user_id="12345"` |
| `status="200"` | `request_id="abc"` |
| `service="api"` | `timestamp="..."` |
| `endpoint="/users"` | `session_id="..."` |

**Правило:** Стандартные labels для всех метрик.

| Label | Описание | Пример |
|-------|----------|--------|
| `service` | Имя сервиса | `api-server` |
| `environment` | Окружение | `production` |
| `version` | Версия приложения | `v1.2.3` |
| `instance` | Инстанс (автоматически) | `10.0.0.1:8080` |

**Правило:** HTTP метрики labels.

```prometheus
http_requests_total{
    service="api",
    method="POST",
    path="/api/v1/users",
    status="201"
}
```

| Label | Значения | Обязательный |
|-------|----------|--------------|
| `method` | GET, POST, PUT, DELETE, PATCH | Да |
| `path` | Нормализованный путь | Да |
| `status` | HTTP status code | Да |
| `handler` | Имя handler/controller | Опционально |

**Правило:** Нормализовать path — убирать ID.

```
# Правильно
path="/api/v1/users/{id}"
path="/api/v1/orders/{id}/items"

# Неправильно — создаст explosion labels
path="/api/v1/users/123"
path="/api/v1/users/456"
```

### Типы метрик

**Правило:** Выбирать тип метрики по характеру данных.

| Тип | Когда использовать | Пример |
|-----|-------------------|--------|
| Counter | Только растёт | Запросы, ошибки, bytes sent |
| Gauge | Растёт и падает | Температура, активные connections |
| Histogram | Распределение значений | Latency, response size |
| Summary | Квантили (редко) | Legacy, когда нужны точные квантили |

**Counter:**

```go
// Счётчик запросов
var httpRequests = prometheus.NewCounterVec(
    prometheus.CounterOpts{
        Name: "http_requests_total",
        Help: "Total number of HTTP requests",
    },
    []string{"method", "path", "status"},
)

// Использование
httpRequests.WithLabelValues("GET", "/api/users", "200").Inc()
httpRequests.WithLabelValues("POST", "/api/users", "201").Add(1)
```

**Gauge:**

```go
// Активные соединения
var activeConnections = prometheus.NewGauge(
    prometheus.GaugeOpts{
        Name: "db_connections_active",
        Help: "Number of active database connections",
    },
)

// Использование
activeConnections.Set(42)
activeConnections.Inc()
activeConnections.Dec()
```

**Histogram:**

```go
// Latency с buckets
var httpDuration = prometheus.NewHistogramVec(
    prometheus.HistogramOpts{
        Name:    "http_request_duration_seconds",
        Help:    "HTTP request duration in seconds",
        Buckets: []float64{.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10},
    },
    []string{"method", "path"},
)

// Использование
timer := prometheus.NewTimer(httpDuration.WithLabelValues("GET", "/api/users"))
defer timer.ObserveDuration()
```

**Правило:** Buckets для histogram выбирать по SLO.

| SLO | Рекомендуемые buckets |
|-----|----------------------|
| p99 < 100ms | `.005, .01, .025, .05, .075, .1, .25, .5` |
| p99 < 500ms | `.01, .025, .05, .1, .25, .5, 1, 2.5` |
| p99 < 2s | `.05, .1, .25, .5, 1, 2, 5, 10` |

### Стандартные метрики

**Правило:** Каждый сервис экспортирует RED метрики.

```go
// RED: Rate, Errors, Duration
var (
    // Rate
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "path", "status"},
    )

    // Errors (часть Rate с status 5xx)
    // Вычисляется через PromQL

    // Duration
    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "path"},
    )
)
```

**Правило:** USE метрики для ресурсов.

```go
// USE: Utilization, Saturation, Errors
var (
    // Utilization
    cpuUsage = prometheus.NewGauge(prometheus.GaugeOpts{
        Name: "process_cpu_usage_ratio",
        Help: "CPU usage ratio",
    })

    // Saturation
    goroutines = prometheus.NewGauge(prometheus.GaugeOpts{
        Name: "go_goroutines",
        Help: "Number of goroutines",
    })

    // Errors
    dbErrors = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "db_errors_total",
            Help: "Database errors",
        },
        []string{"operation", "error_type"},
    )
)
```

**Правило:** Build info метрика для версионирования.

```go
var buildInfo = prometheus.NewGaugeVec(
    prometheus.GaugeOpts{
        Name: "build_info",
        Help: "Build information",
    },
    []string{"version", "commit", "build_time"},
)

func init() {
    buildInfo.WithLabelValues(
        Version,
        GitCommit,
        BuildTime,
    ).Set(1)
}
```

### Cardinality

**Правило:** Контролировать cardinality — общее количество уникальных серий.

```
Cardinality = ∏(количество уникальных значений каждого label)

Пример:
- method: 5 значений
- path: 20 значений
- status: 10 значений

Cardinality = 5 × 20 × 10 = 1000 серий
```

**Правило:** Лимиты cardinality.

| Уровень | Cardinality | Рекомендация |
|---------|-------------|--------------|
| Метрика | < 1000 | OK |
| Метрика | 1000-10000 | Пересмотреть labels |
| Метрика | > 10000 | Требуется оптимизация |
| Сервис | < 10000 | OK |
| Сервис | > 100000 | Проблема |

**Правило:** Избегать unbounded labels.

```go
// Неправильно — user_id создаст миллионы серий
httpRequests.WithLabelValues(method, path, status, userID)

// Правильно — агрегировать
httpRequests.WithLabelValues(method, path, status, userTier)
// userTier: "free", "premium", "enterprise"
```

### Scraping

**Правило:** Экспортировать метрики на `/metrics`.

```go
import (
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
    http.Handle("/metrics", promhttp.Handler())
    http.ListenAndServe(":8080", nil)
}
```

**Правило:** Конфигурация Prometheus scraping.

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'api-server'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Фильтровать по annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      # Путь к метрикам
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      # Порт
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      # Labels из pod
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
```

**Правило:** Pod annotations для автоматического discovery.

```yaml
# Kubernetes Pod
apiVersion: v1
kind: Pod
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
```

---

## Примеры

### Пример 1: HTTP middleware для метрик

```go
package middleware

import (
    "net/http"
    "strconv"
    "time"

    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "path", "status"},
    )

    httpRequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration",
            Buckets: []float64{.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5},
        },
        []string{"method", "path"},
    )

    httpRequestSize = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_size_bytes",
            Help:    "HTTP request size",
            Buckets: prometheus.ExponentialBuckets(100, 10, 7),
        },
        []string{"method", "path"},
    )

    httpResponseSize = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_response_size_bytes",
            Help:    "HTTP response size",
            Buckets: prometheus.ExponentialBuckets(100, 10, 7),
        },
        []string{"method", "path"},
    )
)

func Metrics(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        // Wrap response writer
        wrapped := &responseWriter{ResponseWriter: w, statusCode: 200}

        // Нормализовать path
        path := normalizePath(r.URL.Path)

        // Record request size
        httpRequestSize.WithLabelValues(r.Method, path).Observe(float64(r.ContentLength))

        // Call next handler
        next.ServeHTTP(wrapped, r)

        // Record metrics
        duration := time.Since(start).Seconds()
        status := strconv.Itoa(wrapped.statusCode)

        httpRequestsTotal.WithLabelValues(r.Method, path, status).Inc()
        httpRequestDuration.WithLabelValues(r.Method, path).Observe(duration)
        httpResponseSize.WithLabelValues(r.Method, path).Observe(float64(wrapped.size))
    })
}

type responseWriter struct {
    http.ResponseWriter
    statusCode int
    size       int
}

func (w *responseWriter) WriteHeader(code int) {
    w.statusCode = code
    w.ResponseWriter.WriteHeader(code)
}

func (w *responseWriter) Write(b []byte) (int, error) {
    n, err := w.ResponseWriter.Write(b)
    w.size += n
    return n, err
}

func normalizePath(path string) string {
    // /api/v1/users/123 → /api/v1/users/{id}
    // Реализация зависит от routing library
    return path
}
```

### Пример 2: Database метрики

```go
package db

import (
    "database/sql"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    dbConnections = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "db_connections",
            Help: "Database connections",
        },
        []string{"state"}, // open, in_use, idle
    )

    dbQueryDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "db_query_duration_seconds",
            Help:    "Database query duration",
            Buckets: []float64{.001, .005, .01, .025, .05, .1, .25, .5, 1},
        },
        []string{"operation", "table"},
    )

    dbQueryErrors = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "db_query_errors_total",
            Help: "Database query errors",
        },
        []string{"operation", "error_type"},
    )
)

// Collector для sql.DBStats
type DBStatsCollector struct {
    db *sql.DB
}

func NewDBStatsCollector(db *sql.DB) *DBStatsCollector {
    return &DBStatsCollector{db: db}
}

func (c *DBStatsCollector) Describe(ch chan<- *prometheus.Desc) {
    prometheus.DescribeByCollect(c, ch)
}

func (c *DBStatsCollector) Collect(ch chan<- prometheus.Metric) {
    stats := c.db.Stats()

    ch <- prometheus.MustNewConstMetric(
        prometheus.NewDesc("db_connections_open", "Open connections", nil, nil),
        prometheus.GaugeValue,
        float64(stats.OpenConnections),
    )

    ch <- prometheus.MustNewConstMetric(
        prometheus.NewDesc("db_connections_in_use", "In-use connections", nil, nil),
        prometheus.GaugeValue,
        float64(stats.InUse),
    )

    ch <- prometheus.MustNewConstMetric(
        prometheus.NewDesc("db_connections_idle", "Idle connections", nil, nil),
        prometheus.GaugeValue,
        float64(stats.Idle),
    )

    ch <- prometheus.MustNewConstMetric(
        prometheus.NewDesc("db_wait_count_total", "Total wait count", nil, nil),
        prometheus.CounterValue,
        float64(stats.WaitCount),
    )

    ch <- prometheus.MustNewConstMetric(
        prometheus.NewDesc("db_wait_duration_seconds_total", "Total wait duration", nil, nil),
        prometheus.CounterValue,
        stats.WaitDuration.Seconds(),
    )
}
```

### Пример 3: PromQL запросы

```promql
# Request rate по сервису
sum(rate(http_requests_total{service="api"}[5m])) by (method)

# Error rate
sum(rate(http_requests_total{service="api",status=~"5.."}[5m]))
/
sum(rate(http_requests_total{service="api"}[5m]))

# Latency percentiles
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{service="api"}[5m])) by (le))
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service="api"}[5m])) by (le))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="api"}[5m])) by (le))

# Apdex score (threshold 0.5s)
(
  sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
  +
  sum(rate(http_request_duration_seconds_bucket{le="2.0"}[5m]))
) / 2
/
sum(rate(http_request_duration_seconds_count[5m]))

# Top 5 endpoints by request count
topk(5, sum(rate(http_requests_total[5m])) by (path))

# Saturation: goroutines growth
deriv(go_goroutines[5m])

# Utilization: CPU usage
rate(process_cpu_seconds_total[5m])
```

### Пример 4: Recording rules

```yaml
# prometheus-rules.yml
groups:
  - name: http_rules
    interval: 15s
    rules:
      # Request rate
      - record: service:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (service)

      # Error rate
      - record: service:http_errors:ratio5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)

      # Latency p99
      - record: service:http_latency_p99:5m
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
          )

      # Availability
      - record: service:availability:ratio5m
        expr: |
          1 - (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
            /
            sum(rate(http_requests_total[5m])) by (service)
          )
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Метрики не появляются в Prometheus — что делать?

1. **Проверить endpoint:**
   ```bash
   curl http://localhost:8080/metrics
   ```

2. **Проверить scrape config:**
   ```bash
   # Prometheus targets
   curl http://prometheus:9090/api/v1/targets
   ```

3. **Проверить labels и relabeling:**
   ```yaml
   # В prometheus.yml временно отключить relabeling
   ```

4. **Проверить network:**
   - Prometheus может достучаться до сервиса?
   - Firewall rules?

### High cardinality — как исправить?

1. **Найти проблемные метрики:**
   ```promql
   # Top метрики по cardinality
   topk(10, count by (__name__)({__name__=~".+"}))
   ```

2. **Найти проблемные labels:**
   ```promql
   # Количество уникальных значений label
   count(count by (path) (http_requests_total))
   ```

3. **Исправить:**
   - Нормализовать paths
   - Убрать user_id и подобные labels
   - Использовать relabeling для drop

### Как добавить метрики без изменения кода?

1. **Prometheus blackbox exporter:**
   ```yaml
   # Проверка HTTP endpoints
   - job_name: 'blackbox'
     metrics_path: /probe
     params:
       module: [http_2xx]
     static_configs:
       - targets:
         - https://api.example.com/health
     relabel_configs:
       - source_labels: [__address__]
         target_label: __param_target
       - source_labels: [__param_target]
         target_label: instance
       - target_label: __address__
         replacement: blackbox-exporter:9115
   ```

2. **Pushgateway** (для batch jobs):
   ```bash
   echo "job_duration_seconds 42" | curl --data-binary @- \
     http://pushgateway:9091/metrics/job/batch_job/instance/host1
   ```

### Histogram vs Summary — что выбрать?

| Критерий | Histogram | Summary |
|----------|-----------|---------|
| Агрегация | Да | Нет |
| Точность квантилей | Приблизительная | Точная |
| CPU на клиенте | Низкая | Высокая |
| CPU на сервере | Высокая | Низкая |
| Buckets | Фиксированные | — |

**Рекомендация:** Histogram в 95% случаев.

---

## Связанные инструкции

- [overview.md](overview.md) — Обзор observability
- [alerting.md](alerting.md) — Алертинг на основе метрик
- [caching.md](../caching.md) — Метрики кэша
