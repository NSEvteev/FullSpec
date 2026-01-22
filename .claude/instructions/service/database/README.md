# /src/runtime/ -- Runtime сервисов

Правила работы сервисов в runtime: база данных, health checks, устойчивость, real-time.

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Database](#1-database) | [database.md](./database.md) | Работа с базой данных -- connection pooling, миграции, транзакции, saga pattern |
| [2. Health](#2-health) | [health.md](./health.md) | Health checks -- эндпоинты /health, /ready и graceful shutdown |
| [3. Realtime](#3-realtime) | [realtime.md](./realtime.md) | Real-time коммуникация -- polling, SSE, WebSocket и выбор технологии |
| [4. Resilience](#4-resilience) | [resilience.md](./resilience.md) | Устойчивость сервисов -- таймауты, повторы, circuit breaker, fallbacks |

---

## 1. Database

**Файл:** [database.md](./database.md)

**Тип:** standard

**Описание:** Стандарт работы с базой данных: подключения, миграции, транзакции.

**Ключевые правила:**
- Connection pooling: pool_size=10, max_overflow=20, pool_recycle=1800
- pool_pre_ping=True для проверки соединения
- Миграции через Alembic (Python) или аналоги
- Saga pattern для распределённых транзакций

**Связанные инструкции:**
- [health.md](./health.md) -- проверка подключения к БД
- [resilience.md](./resilience.md) -- обработка сбоев БД

---

## 2. Health

**Файл:** [health.md](./health.md)

**Тип:** standard

**Описание:** Стандарт проверки состояния сервисов и корректного завершения работы.

**Ключевые правила:**
- `/health` (liveness) -- процесс жив, не проверяет зависимости
- `/ready` (readiness) -- готовность принимать трафик, проверяет БД, Redis
- Graceful shutdown: SIGTERM -> finish requests -> close connections
- Health check timeout < 5s

**Связанные инструкции:**
- [database.md](./database.md) -- проверка БД в /ready
- [resilience.md](./resilience.md) -- fallback при недоступности зависимостей

---

## 3. Realtime

**Файл:** [realtime.md](./realtime.md)

**Тип:** standard

**Описание:** Стандарт выбора и реализации real-time коммуникации.

**Ключевые правила:**
- Polling: данные обновляются редко (> 30 сек), максимальная совместимость
- SSE: односторонняя связь сервер -> клиент, автопереподключение
- WebSocket: двусторонняя связь, низкая латентность, чаты, игры
- Матрица выбора по критериям (направление, латентность, масштабирование)

**Связанные инструкции:**
- [health.md](./health.md) -- health checks для WebSocket серверов
- [resilience.md](./resilience.md) -- reconnection logic

---

## 4. Resilience

**Файл:** [resilience.md](./resilience.md)

**Тип:** standard

**Описание:** Стандарт обеспечения устойчивости сервисов к сбоям.

**Ключевые правила:**
- Таймауты: connect=5s, read=10s для внутренних сервисов
- Retry: exponential backoff, максимум 3 попытки
- Circuit breaker: 50% threshold, 30s timeout
- Fallback: дефолтное значение или cached response

**Связанные инструкции:**
- [health.md](./health.md) -- определение unhealthy состояния
- [database.md](./database.md) -- retry для БД операций
- [../security/auth.md](../security/auth.md) -- retry для auth сервиса

---

## Граф связей

```
                    ┌───────────────┐
                    │  health.md    │
                    │ (/health,     │
                    │  /ready)      │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
    ┌─────────────┐  ┌───────────┐  ┌──────────────┐
    │ database.md │  │realtime.md│  │resilience.md │
    │ (pool, saga)│  │(SSE, WS)  │  │(retry, CB)   │
    └──────┬──────┘  └───────────┘  └──────┬───────┘
           │                               │
           └───────────────┬───────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  ../security/   │
                  │  auth.md        │
                  └─────────────────┘
```

---

## Когда какую инструкцию читать

| Ситуация | Инструкция |
|----------|------------|
| Настраиваю подключение к БД | database.md |
| Создаю миграцию | database.md |
| Реализую распределённую транзакцию | database.md |
| Добавляю /health, /ready эндпоинты | health.md |
| Настраиваю graceful shutdown | health.md |
| Выбираю между polling/SSE/WebSocket | realtime.md |
| Реализую SSE или WebSocket | realtime.md |
| Настраиваю таймауты HTTP клиента | resilience.md |
| Добавляю retry с backoff | resilience.md |
| Реализую circuit breaker | resilience.md |

---

## Паттерны устойчивости

```
Request Flow:

Client → Timeout → Retry → Circuit Breaker → Service
                                │
                                ▼
                           Fallback
                      (при всех неудачах)
```

| Паттерн | Когда использовать | Пример |
|---------|-------------------|--------|
| Timeout | Всегда | 10s для внутренних, 60s для внешних API |
| Retry | Transient errors | 3 попытки с exponential backoff |
| Circuit Breaker | Защита от каскадных сбоев | 50% ошибок за 30s |
| Fallback | Graceful degradation | Cached response, default value |

---

## Связанные разделы

- [../api/](../api/) -- проектирование API endpoints
- [../data/](../data/) -- форматы ошибок, логирование
- [../security/](../security/) -- аутентификация между сервисами
- [../../platform/](../../platform/) -- инфраструктура (K8s probes)
