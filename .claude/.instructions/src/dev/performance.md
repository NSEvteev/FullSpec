---
type: standard
description: Профилирование, бенчмарки, лимиты: p99 < 200ms, память < 512MB
related:
  - /.claude/.instructions/src/dev/local.md
  - /.claude/.instructions/tests/load.md
  - /.claude/.instructions/platform/observability/metrics.md
  - /.claude/.instructions/src/runtime/health.md
---

# Производительность

Правила профилирования, бенчмарки и лимиты производительности сервисов.

## Оглавление

- [Лимиты производительности](#лимиты-производительности)
- [Профилирование](#профилирование)
- [Бенчмарки](#бенчмарки)
- [Метрики производительности](#метрики-производительности)
- [Оптимизация](#оптимизация)
- [Performance budgets](#performance-budgets)
- [Инструменты](#инструменты)
- [Связанные инструкции](#связанные-инструкции)

---

## Лимиты производительности

### Обязательные пороги

| Метрика | Лимит | Описание |
|---------|-------|----------|
| p99 latency | < 200ms | 99% запросов быстрее 200ms |
| p95 latency | < 100ms | 95% запросов быстрее 100ms |
| p50 latency | < 50ms | Медиана времени ответа |
| Память | < 512MB | Максимум на контейнер сервиса |
| CPU | < 80% | Средняя загрузка при нормальной нагрузке |
| Startup time | < 30s | Время до ready state |

### Пороги по типам операций

| Операция | p99 лимит | Примечание |
|----------|-----------|------------|
| GET (простой) | < 50ms | Чтение одной записи |
| GET (список) | < 150ms | Пагинированный список |
| POST/PUT | < 200ms | Создание/обновление |
| DELETE | < 100ms | Удаление |
| Аутентификация | < 100ms | Проверка токена |
| Поиск | < 300ms | Полнотекстовый поиск |

### Нагрузочные пороги

| Сценарий | Требование |
|----------|------------|
| Обычная нагрузка | 100 RPS на сервис |
| Пиковая нагрузка | 500 RPS (кратковременно) |
| Error rate | < 0.1% при нормальной нагрузке |
| Error rate (пик) | < 1% при пиковой нагрузке |

---

## Профилирование

### CPU профилирование

**Node.js:**

```javascript
// Включить встроенный профайлер
node --prof src/index.js

// Обработать лог
node --prof-process isolate-*.log > profile.txt
```

**Python:**

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... код для профилирования ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # топ 20 функций
```

**Go:**

```go
import "runtime/pprof"

f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()

// ... код ...
```

### Memory профилирование

**Node.js:**

```javascript
// В Chrome DevTools
node --inspect src/index.js
// Открыть chrome://inspect → Memory → Take heap snapshot
```

**Python:**

```python
import tracemalloc

tracemalloc.start()

# ... код ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

**Go:**

```go
import "runtime/pprof"

f, _ := os.Create("mem.prof")
pprof.WriteHeapProfile(f)
f.Close()

// Анализ: go tool pprof mem.prof
```

### Профилирование в production

**Правила:**
- Использовать sampling (не continuous)
- Ограничивать время сбора (< 60 секунд)
- Профилировать на реплике, не на primary

```yaml
# Включение профилирования через переменную окружения
environment:
  - ENABLE_PROFILING=true
  - PROFILING_SAMPLE_RATE=0.01  # 1% запросов
```

---

## Бенчмарки

### Структура бенчмарков

```
/tests/load/
  /services/                  ← изолированные тесты сервисов
    auth.k6.js
    users.k6.js
  /scenarios/                 ← сценарные тесты
    user-registration.k6.js
    checkout-flow.k6.js
  /system/                    ← системные тесты
    peak-load.k6.js
    sustained-load.k6.js
```

### k6 бенчмарк пример

```javascript
// tests/load/services/auth.k6.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // ramp-up
    { duration: '3m', target: 50 },   // stable load
    { duration: '1m', target: 100 },  // peak
    { duration: '1m', target: 0 },    // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(99)<200'],  // p99 < 200ms
    http_req_failed: ['rate<0.01'],    // error rate < 1%
  },
};

export default function () {
  const res = http.post('http://localhost:8080/api/v1/auth/login', {
    email: 'test@example.com',
    password: 'password123',
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });

  sleep(1);
}
```

### Запуск бенчмарков

```bash
# Локальный запуск
k6 run tests/load/services/auth.k6.js

# С выводом метрик
k6 run --out influxdb=http://localhost:8086/k6 auth.k6.js

# CI интеграция
make test-load
```

### Регулярность бенчмарков

| Тип | Частота | Триггер |
|-----|---------|---------|
| Smoke (быстрый) | При каждом PR | CI pipeline |
| Load (полный) | Еженедельно | Scheduled CI |
| Stress | Перед релизом | Manual |
| Soak | Ежемесячно | Scheduled CI |

---

## Метрики производительности

### Обязательные метрики

```
# Latency (гистограмма)
http_request_duration_seconds_bucket{service="auth", endpoint="/login", le="0.05"}
http_request_duration_seconds_bucket{service="auth", endpoint="/login", le="0.1"}
http_request_duration_seconds_bucket{service="auth", endpoint="/login", le="0.2"}
http_request_duration_seconds_bucket{service="auth", endpoint="/login", le="0.5"}
http_request_duration_seconds_bucket{service="auth", endpoint="/login", le="1"}

# Throughput (counter)
http_requests_total{service="auth", status="200"}
http_requests_total{service="auth", status="500"}

# Errors (counter)
http_errors_total{service="auth", type="timeout"}
http_errors_total{service="auth", type="validation"}

# Memory (gauge)
process_resident_memory_bytes{service="auth"}

# CPU (gauge)
process_cpu_seconds_total{service="auth"}
```

### Алерты производительности

```yaml
# platform/monitoring/alerts/performance.yml
groups:
  - name: performance
    rules:
      - alert: HighLatency
        expr: histogram_quantile(0.99, http_request_duration_seconds_bucket) > 0.2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency > 200ms for {{ $labels.service }}"

      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes > 536870912  # 512MB
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Memory > 512MB for {{ $labels.service }}"

      - alert: HighErrorRate
        expr: rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate > 1% for {{ $labels.service }}"
```

---

## Оптимизация

### Чек-лист оптимизации

| Область | Проверка |
|---------|----------|
| **БД** | Индексы на часто используемых полях |
| **БД** | Избегать N+1 запросов (batch/join) |
| **БД** | Connection pooling настроен |
| **Кэш** | Hot data в Redis |
| **Кэш** | HTTP caching headers |
| **Код** | Async где возможно |
| **Код** | Избегать блокирующих операций |
| **Сеть** | Compression (gzip/brotli) |
| **Сеть** | Keep-alive соединения |

### Паттерны оптимизации

**Кэширование:**

```typescript
// Cache-aside pattern
async function getUser(id: string): Promise<User> {
  // 1. Проверить кэш
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  // 2. Получить из БД
  const user = await db.users.findById(id);

  // 3. Сохранить в кэш
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));

  return user;
}
```

**Batch запросы:**

```typescript
// Плохо: N+1 запросов
for (const orderId of orderIds) {
  const order = await db.orders.findById(orderId);  // N запросов
  orders.push(order);
}

// Хорошо: 1 запрос
const orders = await db.orders.findByIds(orderIds);
```

**Pagination:**

```typescript
// Использовать cursor-based для больших наборов
async function getUsers(cursor?: string, limit = 20) {
  const query = db.users.orderBy('id');

  if (cursor) {
    query.where('id', '>', cursor);
  }

  return query.limit(limit);
}
```

### Профилирование запросов БД

```sql
-- PostgreSQL: включить логирование медленных запросов
ALTER SYSTEM SET log_min_duration_statement = 100;  -- 100ms

-- Анализ плана запроса
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

---

## Performance budgets

### Бюджеты по ресурсам

| Ресурс | Бюджет | Действие при превышении |
|--------|--------|------------------------|
| Bundle size (frontend) | < 250KB gzip | Блокирует merge |
| API response size | < 100KB | Warning в CI |
| Docker image | < 500MB | Warning в CI |
| Dependencies | < 50 direct | Review required |

### Бюджеты по времени

| Операция | Бюджет | Измерение |
|----------|--------|-----------|
| Cold start | < 5s | Первый запрос после деплоя |
| Warm request | < 200ms | p99 в production |
| DB query | < 50ms | p99 в production |
| External API call | < 500ms | p99, с retry |

### Мониторинг бюджетов

```yaml
# CI check
- name: Check performance budgets
  run: |
    # Проверка размера bundle
    size=$(stat -f%z dist/main.js.gz)
    if [ $size -gt 262144 ]; then
      echo "Bundle size exceeds 256KB!"
      exit 1
    fi
```

---

## Инструменты

### Профилирование

| Язык | Инструмент | Назначение |
|------|------------|------------|
| Node.js | clinic.js | CPU, memory, I/O |
| Node.js | 0x | Flame graphs |
| Python | py-spy | Sampling profiler |
| Python | memory_profiler | Memory usage |
| Go | pprof | CPU, memory, goroutines |
| Go | trace | Execution tracer |

### Нагрузочное тестирование

| Инструмент | Назначение |
|------------|------------|
| k6 | Load testing (основной) |
| Apache Bench | Простые HTTP тесты |
| wrk | HTTP benchmarking |
| Locust | Python-based load testing |

### Мониторинг

| Инструмент | Назначение |
|------------|------------|
| Prometheus | Сбор метрик |
| Grafana | Визуализация |
| Jaeger/Tempo | Distributed tracing |

### Команды

```bash
# Профилирование
make profile-auth              # CPU profile сервиса auth
make profile-auth-memory       # Memory profile

# Бенчмарки
make bench-auth                # Бенчмарк auth сервиса
make bench-all                 # Все бенчмарки

# Анализ
make analyze-performance       # Сводный отчёт
```

---

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование метрик производительности |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при изменении лимитов |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |
| [/test-create](/.claude/skills/test-create/SKILL.md) | Создание бенчмарков |
| [/test-execute](/.claude/skills/test-execute/SKILL.md) | Запуск нагрузочных тестов |

---

## Связанные инструкции

- [local.md](./local.md) — локальная разработка
- [load.md](/.claude/.instructions/tests/load.md) — нагрузочные тесты
- [metrics.md](/.claude/.instructions/platform/observability/metrics.md) — метрики Prometheus
- [health.md](/.claude/.instructions/src/runtime/health.md) — health checks
