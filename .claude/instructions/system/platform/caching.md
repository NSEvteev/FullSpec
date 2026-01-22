---
type: standard
description: Redis кэширование, cache-aside, TTL, key naming conventions
related:
  - platform/docker.md
  - platform/observability/metrics.md
  - src/runtime/resilience.md
---

# Кэширование

Правила кэширования с Redis: паттерны, TTL, именование ключей, инвалидация.

## Оглавление

- [Правила](#правила)
  - [Паттерн Cache-Aside](#паттерн-cache-aside)
  - [Именование ключей](#именование-ключей)
  - [TTL стратегии](#ttl-стратегии)
  - [Инвалидация кэша](#инвалидация-кэша)
  - [Сериализация](#сериализация)
  - [Мониторинг](#мониторинг)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Паттерн Cache-Aside

**Правило:** Использовать cache-aside (lazy loading) как основной паттерн.

```
Чтение:
1. Проверить кэш
2. Если hit → вернуть из кэша
3. Если miss → загрузить из БД → записать в кэш → вернуть

Запись:
1. Обновить БД
2. Инвалидировать кэш (delete, не update)
```

```python
# Пример cache-aside
async def get_user(user_id: str) -> User:
    # 1. Проверить кэш
    cache_key = f"user:{user_id}"
    cached = await redis.get(cache_key)

    if cached:
        return User.model_validate_json(cached)

    # 2. Загрузить из БД
    user = await db.users.find_one({"_id": user_id})

    if user:
        # 3. Записать в кэш
        await redis.setex(
            cache_key,
            ttl=3600,  # 1 час
            value=user.model_dump_json()
        )

    return user
```

**Правило:** При обновлении данных — инвалидировать, не обновлять кэш.

```python
async def update_user(user_id: str, data: dict) -> User:
    # 1. Обновить БД
    user = await db.users.update_one(
        {"_id": user_id},
        {"$set": data}
    )

    # 2. Инвалидировать кэш
    await redis.delete(f"user:{user_id}")

    return user
```

### Именование ключей

**Правило:** Формат ключа: `{service}:{entity}:{id}[:{suffix}]`

| Компонент | Описание | Пример |
|-----------|----------|--------|
| `service` | Имя сервиса | `auth`, `catalog`, `orders` |
| `entity` | Тип сущности | `user`, `product`, `session` |
| `id` | Идентификатор | UUID, slug, email hash |
| `suffix` | Опционально: вариант | `full`, `short`, `v2` |

**Примеры:**

```
auth:user:550e8400-e29b-41d4-a716-446655440000
auth:session:abc123def456
catalog:product:macbook-pro-16
catalog:product:macbook-pro-16:prices
orders:cart:user-123
notify:preferences:user-456
```

**Правило:** Разделитель — двоеточие (`:`).

**Правило:** Использовать lowercase и kebab-case для составных частей.

```
# Правильно
catalog:product-category:electronics

# Неправильно
Catalog:ProductCategory:ELECTRONICS
catalog_product_category_electronics
```

### TTL стратегии

**Правило:** Всегда устанавливать TTL для каждого ключа.

| Тип данных | TTL | Обоснование |
|------------|-----|-------------|
| Сессии | 24h | Безопасность |
| Профили пользователей | 1h | Баланс свежести/нагрузки |
| Каталог товаров | 15min | Частые обновления |
| Справочники | 24h | Редко меняются |
| Rate limit counters | 1min | Скользящее окно |
| Временные токены | 5min | Безопасность |

**Правило:** Добавлять jitter (случайное смещение) для предотвращения stampede.

```python
import random

def get_ttl_with_jitter(base_ttl: int, jitter_percent: int = 10) -> int:
    """Добавляет случайное смещение к TTL."""
    jitter = int(base_ttl * jitter_percent / 100)
    return base_ttl + random.randint(-jitter, jitter)

# Использование
ttl = get_ttl_with_jitter(3600)  # 3600 +/- 360 секунд
await redis.setex(key, ttl, value)
```

### Инвалидация кэша

**Правило:** Предпочитать точечную инвалидацию паттерн-инвалидации.

| Метод | Когда использовать | Пример |
|-------|-------------------|--------|
| DELETE по ключу | Изменение одной сущности | `redis.delete("user:123")` |
| DELETE по паттерну | Массовое обновление | `redis.delete("catalog:product:*")` (осторожно!) |
| Версионирование | Полная инвалидация категории | `catalog:v2:product:123` |

**Правило:** Избегать `KEYS *` в production — использовать `SCAN`.

```python
# Неправильно — блокирует Redis
keys = redis.keys("catalog:product:*")

# Правильно — неблокирующий итератор
async def delete_by_pattern(pattern: str):
    cursor = 0
    while True:
        cursor, keys = await redis.scan(cursor, match=pattern, count=100)
        if keys:
            await redis.delete(*keys)
        if cursor == 0:
            break
```

**Правило:** Для связанных сущностей использовать транзакции или pipeline.

```python
async def update_product_with_category(product_id: str, category_id: str):
    # Атомарная инвалидация связанных ключей
    async with redis.pipeline() as pipe:
        pipe.delete(f"catalog:product:{product_id}")
        pipe.delete(f"catalog:category:{category_id}:products")
        pipe.delete(f"catalog:category:{category_id}:count")
        await pipe.execute()
```

### Сериализация

**Правило:** Использовать JSON для структурированных данных.

```python
# Сериализация
data = {"id": "123", "name": "Product", "price": 99.99}
await redis.set(key, json.dumps(data))

# Десериализация
raw = await redis.get(key)
data = json.loads(raw) if raw else None
```

**Правило:** Для больших объектов использовать сжатие.

```python
import gzip
import json

def compress(data: dict) -> bytes:
    return gzip.compress(json.dumps(data).encode())

def decompress(data: bytes) -> dict:
    return json.loads(gzip.decompress(data))

# Порог сжатия: > 1KB
if len(json_data) > 1024:
    await redis.set(key, compress(data))
else:
    await redis.set(key, json_data)
```

**Правило:** Версионировать формат данных в кэше.

```python
CACHE_VERSION = "v2"

def cache_key(entity: str, id: str) -> str:
    return f"{CACHE_VERSION}:{entity}:{id}"

# При изменении формата — увеличить версию
# Старые ключи автоматически станут недоступны
```

### Мониторинг

**Правило:** Отслеживать метрики кэша.

| Метрика | Описание | Alert threshold |
|---------|----------|-----------------|
| `cache_hit_ratio` | Процент попаданий | < 80% |
| `cache_latency_p99` | Задержка 99 перцентиль | > 10ms |
| `cache_memory_used` | Использование памяти | > 80% |
| `cache_evictions` | Количество вытеснений | > 1000/min |
| `cache_connections` | Активные соединения | > 80% от max |

```python
# Инструментирование
from prometheus_client import Counter, Histogram

cache_requests = Counter(
    'cache_requests_total',
    'Total cache requests',
    ['service', 'operation', 'status']
)

cache_latency = Histogram(
    'cache_latency_seconds',
    'Cache operation latency',
    ['service', 'operation']
)

async def get_cached(key: str):
    with cache_latency.labels(service='auth', operation='get').time():
        result = await redis.get(key)

    status = 'hit' if result else 'miss'
    cache_requests.labels(service='auth', operation='get', status=status).inc()

    return result
```

---

## Примеры

### Пример 1: Кэширование профиля пользователя

```python
from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class UserCache:
    redis: Redis
    ttl: int = 3600  # 1 час

    def _key(self, user_id: str) -> str:
        return f"auth:user:{user_id}"

    async def get(self, user_id: str) -> Optional[dict]:
        data = await self.redis.get(self._key(user_id))
        if data:
            return json.loads(data)
        return None

    async def set(self, user_id: str, user: dict) -> None:
        await self.redis.setex(
            self._key(user_id),
            self.ttl + random.randint(-360, 360),  # jitter
            json.dumps(user)
        )

    async def delete(self, user_id: str) -> None:
        await self.redis.delete(self._key(user_id))

    async def get_or_load(
        self,
        user_id: str,
        loader: Callable
    ) -> Optional[dict]:
        """Cache-aside паттерн."""
        user = await self.get(user_id)
        if user:
            return user

        user = await loader(user_id)
        if user:
            await self.set(user_id, user)

        return user
```

### Пример 2: Rate limiting

```python
class RateLimiter:
    def __init__(self, redis: Redis, limit: int, window: int):
        self.redis = redis
        self.limit = limit
        self.window = window  # секунды

    def _key(self, identifier: str) -> str:
        return f"ratelimit:{identifier}"

    async def is_allowed(self, identifier: str) -> tuple[bool, int]:
        """Проверить, разрешён ли запрос.

        Returns:
            (allowed, remaining)
        """
        key = self._key(identifier)

        async with self.redis.pipeline() as pipe:
            pipe.incr(key)
            pipe.ttl(key)
            count, ttl = await pipe.execute()

        # Установить TTL если ключ новый
        if ttl == -1:
            await self.redis.expire(key, self.window)

        remaining = max(0, self.limit - count)
        allowed = count <= self.limit

        return allowed, remaining

# Использование
limiter = RateLimiter(redis, limit=100, window=60)

async def handle_request(user_id: str):
    allowed, remaining = await limiter.is_allowed(user_id)

    if not allowed:
        raise HTTPException(
            status_code=429,
            headers={"X-RateLimit-Remaining": str(remaining)}
        )
```

### Пример 3: Кэширование списков с пагинацией

```python
class ProductListCache:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.ttl = 900  # 15 минут

    def _key(self, category_id: str, page: int, limit: int) -> str:
        return f"catalog:category:{category_id}:products:p{page}:l{limit}"

    def _count_key(self, category_id: str) -> str:
        return f"catalog:category:{category_id}:count"

    async def get_page(
        self,
        category_id: str,
        page: int,
        limit: int
    ) -> Optional[dict]:
        async with self.redis.pipeline() as pipe:
            pipe.get(self._key(category_id, page, limit))
            pipe.get(self._count_key(category_id))
            products_raw, count_raw = await pipe.execute()

        if products_raw and count_raw:
            return {
                "items": json.loads(products_raw),
                "total": int(count_raw)
            }
        return None

    async def set_page(
        self,
        category_id: str,
        page: int,
        limit: int,
        products: list,
        total: int
    ) -> None:
        ttl = self.ttl + random.randint(-90, 90)

        async with self.redis.pipeline() as pipe:
            pipe.setex(
                self._key(category_id, page, limit),
                ttl,
                json.dumps(products)
            )
            pipe.setex(self._count_key(category_id), ttl, str(total))
            await pipe.execute()

    async def invalidate_category(self, category_id: str) -> None:
        """Инвалидировать все страницы категории."""
        pattern = f"catalog:category:{category_id}:*"
        cursor = 0
        while True:
            cursor, keys = await self.redis.scan(
                cursor, match=pattern, count=100
            )
            if keys:
                await self.redis.delete(*keys)
            if cursor == 0:
                break
```

### Пример 4: Распределённая блокировка

```python
import uuid
from contextlib import asynccontextmanager

class DistributedLock:
    def __init__(self, redis: Redis):
        self.redis = redis

    def _key(self, name: str) -> str:
        return f"lock:{name}"

    @asynccontextmanager
    async def acquire(
        self,
        name: str,
        ttl: int = 30,
        retry_times: int = 3,
        retry_delay: float = 0.1
    ):
        """Захватить распределённую блокировку."""
        key = self._key(name)
        token = str(uuid.uuid4())

        for _ in range(retry_times):
            acquired = await self.redis.set(
                key, token, nx=True, ex=ttl
            )

            if acquired:
                try:
                    yield
                finally:
                    # Атомарное освобождение
                    await self._release(key, token)
                return

            await asyncio.sleep(retry_delay)

        raise LockError(f"Could not acquire lock: {name}")

    async def _release(self, key: str, token: str) -> None:
        """Освободить блокировку только если token совпадает."""
        script = """
        if redis.call('get', KEYS[1]) == ARGV[1] then
            return redis.call('del', KEYS[1])
        else
            return 0
        end
        """
        await self.redis.eval(script, 1, key, token)

# Использование
lock = DistributedLock(redis)

async def process_payment(order_id: str):
    async with lock.acquire(f"order:{order_id}"):
        # Критическая секция
        await do_payment()
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Cache stampede — что делать?

**Проблема:** Много запросов одновременно обращаются к протухшему ключу.

**Решения:**

1. **Jitter на TTL:**
   ```python
   ttl = base_ttl + random.randint(-jitter, jitter)
   ```

2. **Probabilistic early expiration:**
   ```python
   def should_refresh(ttl_remaining: int, delta: int = 60) -> bool:
       if ttl_remaining > delta:
           return False
       # Вероятность обновления растёт к концу TTL
       probability = 1 - (ttl_remaining / delta)
       return random.random() < probability
   ```

3. **Distributed lock:**
   ```python
   async def get_with_lock(key: str, loader):
       value = await redis.get(key)
       if value:
           return value

       lock_key = f"lock:{key}"
       if await redis.set(lock_key, "1", nx=True, ex=5):
           try:
               value = await loader()
               await redis.setex(key, ttl, value)
           finally:
               await redis.delete(lock_key)
       else:
           await asyncio.sleep(0.1)
           return await get_with_lock(key, loader)
   ```

### Как выбрать между кэшированием и без него?

| Сценарий | Кэшировать? | Причина |
|----------|-------------|---------|
| Данные меняются редко | Да | Высокий hit ratio |
| Запрос тяжёлый (> 100ms) | Да | Снижение latency |
| Данные персональные | Осторожно | Безопасность |
| Real-time данные | Нет | Stale data неприемлем |
| Данные < 10ms из БД | Нет | Overhead кэширования |

### Redis недоступен — что делать?

**Правило:** Кэш не должен быть единой точкой отказа.

```python
async def get_user_resilient(user_id: str) -> User:
    try:
        cached = await redis.get(f"user:{user_id}")
        if cached:
            return User.model_validate_json(cached)
    except RedisError as e:
        logger.warning(f"Redis error: {e}")
        # Продолжаем без кэша

    # Fallback к БД
    return await db.get_user(user_id)
```

### Как мигрировать формат кэша?

1. **Версионирование ключей:**
   ```python
   # Старый формат
   key_v1 = f"user:{id}"

   # Новый формат
   key_v2 = f"v2:user:{id}"
   ```

2. **Dual-read период:**
   ```python
   async def get_user(id: str):
       # Сначала новый формат
       data = await redis.get(f"v2:user:{id}")
       if data:
           return parse_v2(data)

       # Fallback на старый
       data = await redis.get(f"user:{id}")
       if data:
           # Мигрировать при чтении
           parsed = parse_v1(data)
           await redis.setex(f"v2:user:{id}", ttl, serialize_v2(parsed))
           return parsed
   ```

3. **Дождаться истечения старых ключей.**

### Память Redis заканчивается — что делать?

1. **Проверить политику eviction:**
   ```bash
   redis-cli CONFIG GET maxmemory-policy
   # Рекомендуется: allkeys-lru или volatile-lru
   ```

2. **Проанализировать ключи:**
   ```bash
   redis-cli --bigkeys
   redis-cli MEMORY USAGE key_name
   ```

3. **Установить TTL на все ключи:**
   ```bash
   # Найти ключи без TTL
   redis-cli --scan | while read key; do
       ttl=$(redis-cli TTL "$key")
       if [ "$ttl" = "-1" ]; then
           echo "$key has no TTL"
       fi
   done
   ```

4. **Включить сжатие** для больших значений.

---

## Связанные инструкции

- [docker.md](docker.md) — Docker для Redis
- [observability/metrics.md](observability/metrics.md) — Метрики кэша
- [resilience.md](../src/runtime/resilience.md) — Устойчивость при отказе кэша
