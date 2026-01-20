---
type: standard
description: Real-time коммуникация — polling, SSE, WebSocket и выбор технологии
related:
  - src/runtime/health.md
  - src/runtime/resilience.md
  - src/api/rest.md
---

# Real-time

Стандарт выбора и реализации real-time коммуникации.

## Сравнение технологий

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Real-time Technologies                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Polling          SSE                    WebSocket                          │
│   ────────         ───                    ─────────                          │
│                                                                              │
│   Client ──►       Client ──►             Client ◄──►                        │
│          ◄──              ◄──                    ◄──►  Server               │
│   Server           Server                                                    │
│                                                                              │
│   Простота         Односторонний          Двусторонний                       │
│   Много запросов   Легковесный            Низкая латентность                 │
│   HTTP             HTTP                   WS протокол                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Матрица выбора технологии

| Критерий | Polling | SSE | WebSocket |
|----------|---------|-----|-----------|
| Направление | Клиент → Сервер | Сервер → Клиент | Двустороннее |
| Латентность | Высокая (интервал) | Низкая | Очень низкая |
| Нагрузка на сервер | Высокая | Низкая | Низкая |
| Поддержка прокси | Отличная | Хорошая | Проблемная |
| Масштабирование | Простое | Среднее | Сложное |
| Автопереподключение | Ручное | Встроенное | Ручное |
| Бинарные данные | Да (base64) | Нет | Да |
| Сложность | Низкая | Низкая | Высокая |

## Когда что использовать

### Polling

**Выбирайте polling когда:**
- Данные обновляются редко (> 30 сек)
- Точное время обновления не критично
- Нужна максимальная совместимость
- Простота важнее эффективности

```python
# Клиент (JavaScript)
async function pollStatus() {
    while (true) {
        const response = await fetch('/api/status');
        const data = await response.json();
        updateUI(data);
        await sleep(10000);  // 10 секунд
    }
}


# Сервер (FastAPI)
@app.get("/api/status")
async def get_status():
    """Эндпоинт для polling."""
    return {
        "status": await get_current_status(),
        "timestamp": datetime.utcnow().isoformat(),
        "next_poll": 10,  # Подсказка клиенту
    }
```

**Примеры использования:**
- Статус заказа
- Проверка наличия обновлений
- Dashboard с низкой частотой обновления

### Server-Sent Events (SSE)

**Выбирайте SSE когда:**
- Обновления от сервера к клиенту
- Клиенту не нужно отправлять данные
- Нужно автопереподключение
- Текстовые данные (JSON)

```python
# Сервер (FastAPI)
from fastapi.responses import StreamingResponse
import asyncio


async def event_generator(user_id: int):
    """Генератор событий SSE."""
    while True:
        # Проверяем новые события
        events = await get_pending_events(user_id)

        for event in events:
            # Формат SSE: event, data, id
            yield f"event: {event.type}\n"
            yield f"data: {json.dumps(event.data)}\n"
            yield f"id: {event.id}\n\n"

        # Heartbeat каждые 15 секунд
        yield f": heartbeat\n\n"
        await asyncio.sleep(15)


@app.get("/events/{user_id}")
async def events(user_id: int):
    """SSE эндпоинт для событий пользователя."""
    return StreamingResponse(
        event_generator(user_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Nginx
        }
    )
```

```javascript
// Клиент (JavaScript)
const eventSource = new EventSource('/events/123');

eventSource.addEventListener('notification', (event) => {
    const data = JSON.parse(event.data);
    showNotification(data);
});

eventSource.addEventListener('status_update', (event) => {
    const data = JSON.parse(event.data);
    updateStatus(data);
});

eventSource.onerror = (error) => {
    console.error('SSE error:', error);
    // Автопереподключение встроено в браузер
};
```

**Примеры использования:**
- Уведомления
- Live-обновления статуса
- Логи в реальном времени
- Новостная лента

### WebSocket

**Выбирайте WebSocket когда:**
- Двусторонняя коммуникация
- Критична низкая латентность
- Высокая частота сообщений
- Бинарные данные

```python
# Сервер (FastAPI)
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set


class ConnectionManager:
    """Менеджер WebSocket подключений."""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = set()
        self.active_connections[room].add(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        self.active_connections[room].discard(websocket)

    async def broadcast(self, room: str, message: dict):
        """Отправка всем в комнате."""
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(connection, room)


manager = ConnectionManager()


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_json()

            # Обработка сообщения
            response = await process_message(data)

            # Broadcast всем в комнате
            await manager.broadcast(room_id, response)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast(room_id, {
            "type": "user_left",
            "user_id": data.get("user_id"),
        })
```

```javascript
// Клиент (JavaScript)
class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            console.log('Connected');
            this.reconnectAttempts = 0;
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.ws.onclose = () => {
            this.reconnect();
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
            setTimeout(() => this.connect(), delay);
        }
    }

    send(data) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }
}
```

**Примеры использования:**
- Чаты
- Игры
- Совместное редактирование
- Торговые платформы

## Архитектурные паттерны

### Масштабирование SSE/WebSocket

```
┌─────────────────────────────────────────────────────────────────┐
│                        Load Balancer                             │
│                   (sticky sessions / IP hash)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │ Server 1│        │ Server 2│        │ Server 3│
    │ WS/SSE  │        │ WS/SSE  │        │ WS/SSE  │
    └────┬────┘        └────┬────┘        └────┬────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                     ┌──────┴──────┐
                     │    Redis    │
                     │   Pub/Sub   │
                     └─────────────┘
```

### Реализация с Redis Pub/Sub

```python
import aioredis


class PubSubManager:
    """Pub/Sub для масштабирования WebSocket."""

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: aioredis.Redis = None
        self.pubsub: aioredis.PubSub = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)
        self.pubsub = self.redis.pubsub()

    async def subscribe(self, channel: str, callback):
        """Подписка на канал."""
        await self.pubsub.subscribe(channel)
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                await callback(json.loads(message["data"]))

    async def publish(self, channel: str, data: dict):
        """Публикация в канал."""
        await self.redis.publish(channel, json.dumps(data))


# Использование
pubsub = PubSubManager("redis://localhost:6379")


@app.on_event("startup")
async def startup():
    await pubsub.connect()


async def broadcast_to_all_servers(room: str, message: dict):
    """Broadcast через Redis на все серверы."""
    await pubsub.publish(f"room:{room}", message)
```

## Heartbeat и Keep-alive

### SSE Heartbeat

```python
async def sse_with_heartbeat(user_id: int):
    """SSE с heartbeat каждые 15 секунд."""
    last_event_time = time.time()
    heartbeat_interval = 15

    while True:
        events = await get_events_non_blocking(user_id)

        if events:
            for event in events:
                yield format_sse_event(event)
            last_event_time = time.time()
        elif time.time() - last_event_time > heartbeat_interval:
            # Heartbeat — комментарий в SSE
            yield ": heartbeat\n\n"
            last_event_time = time.time()

        await asyncio.sleep(1)
```

### WebSocket Ping/Pong

```python
import asyncio


async def websocket_with_ping(websocket: WebSocket):
    """WebSocket с ping/pong для обнаружения разрывов."""

    async def ping_loop():
        while True:
            try:
                await websocket.send_json({"type": "ping"})
                await asyncio.sleep(30)
            except Exception:
                break

    ping_task = asyncio.create_task(ping_loop())

    try:
        while True:
            data = await asyncio.wait_for(
                websocket.receive_json(),
                timeout=60  # Таймаут без активности
            )

            if data.get("type") == "pong":
                continue  # Игнорируем pong

            await process_message(data)

    except asyncio.TimeoutError:
        await websocket.close(code=1000, reason="Timeout")
    finally:
        ping_task.cancel()
```

## Обработка ошибок

```python
@app.websocket("/ws/{room}")
async def websocket_with_error_handling(websocket: WebSocket, room: str):
    try:
        await manager.connect(websocket, room)

        while True:
            try:
                data = await websocket.receive_json()
                result = await process_message(data)
                await websocket.send_json({"status": "ok", "data": result})

            except json.JSONDecodeError:
                await websocket.send_json({
                    "status": "error",
                    "error": "Invalid JSON",
                })

            except ValidationError as e:
                await websocket.send_json({
                    "status": "error",
                    "error": str(e),
                })

    except WebSocketDisconnect:
        logger.info(f"Client disconnected from {room}")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011, reason="Internal error")

    finally:
        manager.disconnect(websocket, room)
```

## Чек-лист выбора технологии

```
Нужна двусторонняя связь?
├── Да → WebSocket
└── Нет → Данные меняются часто (< 10 сек)?
          ├── Да → SSE
          └── Нет → Polling
```

## Чек-лист реализации

- [ ] Выбрана подходящая технология
- [ ] Реализован heartbeat/ping
- [ ] Настроено автопереподключение на клиенте
- [ ] Обработка ошибок и таймаутов
- [ ] Масштабирование через Redis Pub/Sub (для prod)
- [ ] Sticky sessions на балансировщике
- [ ] Логирование подключений/отключений
- [ ] Graceful shutdown для активных соединений

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование WebSocket/SSE протоколов |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при изменении событий |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |

---

## Связанные инструкции

- [health.md](health.md) — проверка WebSocket подключений
- [resilience.md](resilience.md) — таймауты и переподключения
- [src/api/rest.md](../api/rest.md) — REST endpoints
