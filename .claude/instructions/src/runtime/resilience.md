---
type: standard
description: Устойчивость сервисов — таймауты, повторы, circuit breaker, fallbacks
related:
  - src/runtime/health.md
  - src/runtime/database.md
  - src/api/rest.md
---

# Resilience

Стандарт обеспечения устойчивости сервисов к сбоям.

## Обзор паттернов

```
┌─────────────────────────────────────────────────────────────────┐
│                      Request Flow                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Client    Timeout    Retry     Circuit      Service           │
│     │         │          │       Breaker        │                │
│     │         │          │          │           │                │
│     ├────────►├─────────►├─────────►├──────────►│                │
│     │         │          │          │           │                │
│     │    10s  │   3x     │  50%     │           │                │
│     │   max   │  exp.    │ threshold│           │                │
│     │         │  backoff │          │           │                │
│                                                                  │
│   Fallback ◄────────────────────────┘                           │
│   (при всех неудачах)                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Таймауты

### Конфигурация таймаутов

```python
from dataclasses import dataclass
from typing import Optional
import httpx


@dataclass
class TimeoutConfig:
    """Конфигурация таймаутов для HTTP клиента."""
    connect: float = 5.0      # Подключение к серверу
    read: float = 10.0        # Чтение ответа
    write: float = 10.0       # Отправка запроса
    pool: float = 5.0         # Получение соединения из пула

    def to_httpx(self) -> httpx.Timeout:
        return httpx.Timeout(
            connect=self.connect,
            read=self.read,
            write=self.write,
            pool=self.pool,
        )


# Типовые конфигурации
TIMEOUTS = {
    "fast": TimeoutConfig(connect=2.0, read=5.0),      # Внутренние сервисы
    "normal": TimeoutConfig(connect=5.0, read=10.0),   # По умолчанию
    "slow": TimeoutConfig(connect=10.0, read=30.0),    # Тяжёлые операции
    "external": TimeoutConfig(connect=10.0, read=60.0), # Внешние API
}
```

### Использование

```python
async def call_service(url: str, timeout_type: str = "normal"):
    """Вызов сервиса с таймаутом."""
    timeout = TIMEOUTS[timeout_type].to_httpx()

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url)
            return response.json()
        except httpx.TimeoutException as e:
            logger.warning(f"Timeout calling {url}: {e}")
            raise ServiceTimeoutError(url)
```

### Таймауты для БД

```python
from sqlalchemy import event
from sqlalchemy.exc import OperationalError

# Таймаут выполнения запроса
@event.listens_for(engine.sync_engine, "before_cursor_execute")
def set_query_timeout(conn, cursor, statement, parameters, context, executemany):
    cursor.execute("SET statement_timeout = '30s'")


# Обёртка с таймаутом
async def execute_with_timeout(
    db: AsyncSession,
    query,
    timeout_seconds: int = 30
):
    """Выполнение запроса с таймаутом."""
    try:
        await db.execute(text(f"SET statement_timeout = '{timeout_seconds}s'"))
        result = await db.execute(query)
        return result
    except OperationalError as e:
        if "statement timeout" in str(e):
            raise QueryTimeoutError(f"Query exceeded {timeout_seconds}s")
        raise
```

## Повторы (Retry)

### Базовая реализация

```python
import asyncio
from functools import wraps
from typing import Tuple, Type


def retry(
    max_attempts: int = 3,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
):
    """Декоратор retry с exponential backoff."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts"
                        )
                        raise

                    # Exponential backoff
                    if jitter:
                        actual_delay = delay * (0.5 + random.random())
                    else:
                        actual_delay = delay

                    logger.warning(
                        f"{func.__name__} attempt {attempt} failed: {e}. "
                        f"Retrying in {actual_delay:.2f}s"
                    )

                    await asyncio.sleep(actual_delay)
                    delay = min(delay * exponential_base, max_delay)

        return wrapper
    return decorator
```

### Использование

```python
@retry(
    max_attempts=3,
    exceptions=(httpx.TransportError, httpx.TimeoutException),
    initial_delay=1.0,
)
async def fetch_user_data(user_id: int) -> dict:
    """Получение данных пользователя с повторами."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE}/users/{user_id}")
        response.raise_for_status()
        return response.json()
```

### Retry с tenacity

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def call_payment_service(payment_data: dict):
    """Вызов платёжного сервиса."""
    async with httpx.AsyncClient() as client:
        response = await client.post(PAYMENT_URL, json=payment_data)
        response.raise_for_status()
        return response.json()
```

## Circuit Breaker

### Состояния

```
┌──────────────┐                    ┌──────────────┐
│    CLOSED    │  failure_count     │     OPEN     │
│              │  >= threshold      │              │
│  Нормальная  ├───────────────────►│   Запросы    │
│   работа    │                    │  отклоняются │
│              │                    │              │
└──────┬───────┘                    └──────┬───────┘
       │                                   │
       │                                   │ timeout
       │                                   │ истёк
       │                                   ▼
       │                            ┌──────────────┐
       │         success            │  HALF_OPEN   │
       └────────────────────────────┤              │
                                    │  Пробный     │
              failure               │  запрос      │
        ┌───────────────────────────┤              │
        │                           └──────────────┘
        │
        ▼
┌──────────────┐
│     OPEN     │
└──────────────┘
```

### Реализация

```python
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5       # Порог ошибок
    success_threshold: int = 2       # Успехов для восстановления
    timeout: float = 30.0            # Время в OPEN состоянии
    half_open_max_calls: int = 3     # Лимит вызовов в HALF_OPEN


class CircuitBreaker:
    """Circuit Breaker для защиты от каскадных сбоев."""

    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: datetime = None
        self.half_open_calls = 0
        self._lock = asyncio.Lock()

    async def call(self, func, *args, **kwargs):
        """Выполнение функции через circuit breaker."""
        async with self._lock:
            await self._check_state()

            if self.state == CircuitState.OPEN:
                raise CircuitBreakerOpenError(self.name)

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure()
            raise

    async def _check_state(self):
        """Проверка и обновление состояния."""
        if self.state == CircuitState.OPEN:
            if self._timeout_expired():
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                logger.info(f"Circuit {self.name}: OPEN -> HALF_OPEN")

    def _timeout_expired(self) -> bool:
        if self.last_failure_time is None:
            return True
        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.config.timeout

    async def _on_success(self):
        async with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
                    logger.info(f"Circuit {self.name}: HALF_OPEN -> CLOSED")
            else:
                self.failure_count = 0

    async def _on_failure(self):
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()

            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit {self.name}: HALF_OPEN -> OPEN")
            elif self.failure_count >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit {self.name}: CLOSED -> OPEN")


class CircuitBreakerOpenError(Exception):
    """Circuit breaker открыт, запросы не выполняются."""
    pass
```

### Использование

```python
# Глобальные circuit breakers
circuit_breakers = {
    "payment": CircuitBreaker("payment", CircuitBreakerConfig(
        failure_threshold=5,
        timeout=60.0,
    )),
    "notification": CircuitBreaker("notification", CircuitBreakerConfig(
        failure_threshold=10,
        timeout=30.0,
    )),
}


async def charge_payment(amount: float) -> dict:
    """Списание оплаты через circuit breaker."""
    cb = circuit_breakers["payment"]

    async def _call():
        async with httpx.AsyncClient() as client:
            response = await client.post(PAYMENT_URL, json={"amount": amount})
            response.raise_for_status()
            return response.json()

    return await cb.call(_call)
```

## Fallbacks

### Стратегии fallback

```python
from typing import Callable, TypeVar, Optional
from functools import wraps

T = TypeVar("T")


def with_fallback(
    fallback_func: Callable[..., T],
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """Декоратор для fallback при ошибках."""

    def decorator(func: Callable[..., T]):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except exceptions as e:
                logger.warning(
                    f"{func.__name__} failed, using fallback: {e}"
                )
                return await fallback_func(*args, **kwargs)
        return wrapper
    return decorator
```

### Типы fallbacks

```python
# 1. Кэш как fallback
@with_fallback(get_cached_user, exceptions=(httpx.HTTPError,))
async def get_user(user_id: int) -> User:
    """Получение пользователя с fallback на кэш."""
    response = await user_service.get(user_id)
    await cache.set(f"user:{user_id}", response)
    return response


async def get_cached_user(user_id: int) -> User:
    """Fallback: данные из кэша."""
    cached = await cache.get(f"user:{user_id}")
    if cached:
        return User(**cached)
    raise UserNotFoundError(user_id)


# 2. Значение по умолчанию
@with_fallback(lambda: {"features": []}, exceptions=(ServiceUnavailableError,))
async def get_feature_flags() -> dict:
    """Feature flags с fallback на пустой список."""
    return await feature_service.get_all()


# 3. Деградация функциональности
async def process_order(order: Order):
    """Обработка заказа с деградацией."""
    try:
        await send_confirmation_email(order)
    except EmailServiceError:
        # Деградация: откладываем отправку
        await queue.push("delayed_emails", order.id)
        logger.warning(f"Email delayed for order {order.id}")

    try:
        await update_analytics(order)
    except AnalyticsError:
        # Деградация: пропускаем аналитику
        logger.warning(f"Analytics skipped for order {order.id}")
```

### Комбинированный паттерн

```python
async def resilient_call(
    func: Callable,
    circuit_breaker: CircuitBreaker,
    fallback: Callable,
    *args,
    **kwargs,
):
    """Вызов с retry + circuit breaker + fallback."""
    @retry(max_attempts=3, exceptions=(httpx.TransportError,))
    async def _with_retry():
        return await circuit_breaker.call(func, *args, **kwargs)

    try:
        return await _with_retry()
    except (CircuitBreakerOpenError, Exception) as e:
        logger.warning(f"All attempts failed, using fallback: {e}")
        return await fallback(*args, **kwargs)
```

## Рекомендуемые значения

| Компонент | Параметр | Значение | Комментарий |
|-----------|----------|----------|-------------|
| Timeout | connect | 5s | Подключение |
| Timeout | read | 10-30s | В зависимости от операции |
| Retry | attempts | 3 | Для idempotent операций |
| Retry | initial_delay | 1s | Начальная задержка |
| Retry | max_delay | 60s | Максимальная задержка |
| Circuit | failure_threshold | 5 | Ошибок до открытия |
| Circuit | timeout | 30s | Время в OPEN |

## Чек-лист

- [ ] Таймауты настроены для всех внешних вызовов
- [ ] Retry только для idempotent операций
- [ ] Exponential backoff с jitter
- [ ] Circuit breaker для критичных зависимостей
- [ ] Fallback стратегия определена
- [ ] Мониторинг состояния circuit breakers
- [ ] Логирование всех retry и fallback

## Связанные инструкции

- [health.md](health.md) — проверка состояния сервисов
- [database.md](database.md) — retry для БД операций
- [src/api/rest.md](../api/rest.md) — таймауты для API
