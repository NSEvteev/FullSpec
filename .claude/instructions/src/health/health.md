---
type: standard
description: Health checks — эндпоинты /health, /ready и graceful shutdown
related:
  - src/runtime/resilience.md
  - src/runtime/database.md
  - src/api/rest.md
---

# Health Checks

Стандарт проверки состояния сервисов и корректного завершения работы.

## Оглавление

- [Эндпоинты здоровья](#эндпоинты-здоровья)
- [Graceful Shutdown](#graceful-shutdown)
- [Kubernetes конфигурация](#kubernetes-конфигурация)
- [Диаграмма состояний](#диаграмма-состояний)
- [Чек-лист](#чек-лист)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Эндпоинты здоровья

### /health — Liveness Probe

Проверяет, что процесс жив и отвечает.

```python
@app.get("/health")
async def health():
    """
    Liveness probe — процесс работает.
    Не проверяет зависимости!
    """
    return {"status": "ok"}
```

**Когда использовать:** Kubernetes liveness probe для перезапуска зависших процессов.

**Что НЕ проверять:** БД, Redis, внешние сервисы — это задача /ready.

### /ready — Readiness Probe

Проверяет готовность принимать трафик.

```python
@app.get("/ready")
async def ready():
    """
    Readiness probe — сервис готов к работе.
    Проверяет критические зависимости.
    """
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "migrations": check_migrations_applied(),
    }

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if all_healthy else "not_ready",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
```

**Когда использовать:** Kubernetes readiness probe для исключения из балансировки.

### Проверки зависимостей

```python
async def check_database() -> bool:
    """Проверка подключения к БД."""
    try:
        async with db.acquire() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False


async def check_redis() -> bool:
    """Проверка подключения к Redis."""
    try:
        await redis.ping()
        return True
    except Exception:
        return False


def check_migrations_applied() -> bool:
    """Проверка применения миграций."""
    try:
        current = get_current_revision()
        head = get_head_revision()
        return current == head
    except Exception:
        return False
```

## Graceful Shutdown

### Принцип работы

```
SIGTERM получен
    ↓
Прекращаем принимать новые запросы
    ↓
Ждём завершения текущих (до 30s)
    ↓
Закрываем подключения
    ↓
Выход
```

### Реализация

```python
import asyncio
import signal
from contextlib import asynccontextmanager

# Глобальное состояние завершения
shutdown_event = asyncio.Event()
SHUTDOWN_TIMEOUT = 30  # секунд


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle приложения."""
    # Startup
    await setup_connections()

    # Регистрируем обработчик сигналов
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(shutdown(s))
        )

    yield

    # Shutdown
    await cleanup_connections()


async def shutdown(sig: signal.Signals):
    """Обработчик graceful shutdown."""
    logger.info(f"Получен сигнал {sig.name}, начинаем завершение...")

    # Сигнализируем о завершении
    shutdown_event.set()

    # Ждём завершения активных задач
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    if tasks:
        logger.info(f"Ожидаем завершения {len(tasks)} задач...")
        done, pending = await asyncio.wait(
            tasks,
            timeout=SHUTDOWN_TIMEOUT
        )

        # Отменяем незавершённые
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
```

### Middleware для graceful shutdown

```python
@app.middleware("http")
async def shutdown_middleware(request: Request, call_next):
    """Отклоняем запросы во время завершения."""
    if shutdown_event.is_set():
        return JSONResponse(
            status_code=503,
            content={"detail": "Сервис завершает работу"},
            headers={"Retry-After": "30"}
        )
    return await call_next(request)
```

## Kubernetes конфигурация

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      livenessProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 10
        failureThreshold: 3

      readinessProbe:
        httpGet:
          path: /ready
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 5
        failureThreshold: 3

      # Важно: terminationGracePeriodSeconds >= SHUTDOWN_TIMEOUT
      terminationGracePeriodSeconds: 35
```

## Диаграмма состояний

```
┌─────────────┐     SIGTERM      ┌──────────────┐
│   RUNNING   │ ───────────────► │  DRAINING    │
│             │                  │  (30s max)   │
│ /health: ok │                  │ /ready: 503  │
│ /ready: ok  │                  │ /health: ok  │
└─────────────┘                  └──────┬───────┘
                                        │
                                        ▼
                                 ┌──────────────┐
                                 │  TERMINATED  │
                                 └──────────────┘
```

## Чек-лист

- [ ] `/health` отвечает без проверки зависимостей
- [ ] `/ready` проверяет БД, Redis, миграции
- [ ] Graceful shutdown обрабатывает SIGTERM
- [ ] Таймаут завершения = 30 секунд
- [ ] `terminationGracePeriodSeconds` > таймаута
- [ ] Новые запросы отклоняются во время shutdown

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование health endpoints |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при изменении проверок |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |
| [/health-check](/.claude/skills/health-check/SKILL.md) | Проверка целостности проекта |

---

## Связанные инструкции

- [resilience.md](resilience.md) — таймауты и повторы
- [database.md](database.md) — проверка подключения к БД
- [src/api/rest.md](../api/rest.md) — REST эндпоинты
