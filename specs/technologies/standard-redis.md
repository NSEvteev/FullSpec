---
description: Стандарт кодирования Redis — конвенции именования, структура, паттерны.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/technologies/README.md
technology: redis
---

# Стандарт Redis

Версия стандарта: 1.0

Правила и конвенции кодирования на Redis в проекте.

**Полезные ссылки:**
- [Технологический реестр](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-redis.md](./validation-redis.md) |

## Оглавление

- [1. Версия и источники](#1-версия-и-источники)
- [2. Конвенции именования](#2-конвенции-именования)
- [3. Структура кода](#3-структура-кода)
- [4. Паттерны использования](#4-паттерны-использования)
- [5. Типичные ошибки](#5-типичные-ошибки)
- [6. Ссылки](#6-ссылки)

---

## 1. Версия и источники

| Параметр | Значение |
|----------|----------|
| Версия | 7 |
| Документация | https://redis.io/docs/ |
| Style guide | https://redis.io/docs/latest/develop/use/keyspace/ |

---

## 2. Конвенции именования

| Элемент | Правило | Пример |
|---------|---------|--------|
| Ключи | `{service}:{entity}:{id}` — двоеточие как разделитель | `notification:ws:conn:user123` |
| Сервис-префикс | Имя сервиса первым сегментом | `notification:`, `auth:` |
| Сущность | Тип данных вторым сегментом | `:ws:`, `:cache:`, `:session:` |
| Идентификатор | ID или составной ключ последним | `:user123`, `:user:42:unread` |
| TTL-ключи | Суффикс не нужен — TTL задаётся при SET | — |
| Паттерны поиска | `{service}:{entity}:*` для SCAN | `notification:ws:conn:*` |
| Хэш-поля | snake_case | `session_id`, `connected_at` |
| Каналы Pub/Sub | `{service}:{event}` | `notification:new`, `system:event` |

---

## 3. Структура кода

**Организация Redis-кода в сервисе:**
```
src/{service}/
├── redis/
│   ├── client.{ext}        # Подключение, конфигурация
│   ├── keys.{ext}          # Константы ключей (шаблоны)
│   └── operations.{ext}    # Операции (get/set/delete)
```

**Ключи как константы:**
- Все шаблоны ключей — в одном файле `keys`
- Шаблон: функция/метод, принимающий параметры → возвращающий строку ключа
- Запрещено конструировать ключи inline (строковая конкатенация в бизнес-логике)

---

## 4. Паттерны использования

**Кэширование:**
- Всегда устанавливать TTL (по умолчанию — от конфигурации)
- Cache-aside: проверить Redis → если нет, прочитать из БД → записать в Redis
- Инвалидация: удалить ключ при изменении данных

**Сессии WebSocket:**
- Ключ: `{service}:ws:conn:{user_id}`
- Значение: SET (множество session ID)
- TTL: время жизни соединения + буфер (heartbeat обновляет TTL)

**Rate limiting:**
- Sliding window: ZADD с timestamp
- Fixed window: INCR + EXPIRE

**Pub/Sub:**
- Канал = `{service}:{event_type}`
- Payload = JSON
- Не использовать для гарантированной доставки (→ message broker)

**Максимальный размер значения:**
- Строки: до 512 MB (практический лимит — до 1 MB)
- Списки/множества: до 100K элементов (дальше — оптимизировать)

---

## 5. Типичные ошибки

**Ключи без TTL:**
```
-- Плохо: ключ живёт вечно → утечка памяти
SET notification:cache:user:42 "{data}"

-- Хорошо: с TTL
SET notification:cache:user:42 "{data}" EX 3600
```

**KEYS вместо SCAN:**
```
-- Плохо: блокирует Redis (O(N) по всем ключам)
KEYS notification:ws:conn:*

-- Хорошо: итеративный обход
SCAN 0 MATCH notification:ws:conn:* COUNT 100
```

**Большие значения в одном ключе:**
```
-- Плохо: весь список уведомлений в одном JSON
SET notification:all:user:42 "[{...}, {...}, ...]"

-- Хорошо: список ID + отдельные ключи
LPUSH notification:list:user:42 "notif-id-1" "notif-id-2"
SET notification:data:notif-id-1 "{...}" EX 86400
```

**Inline-конструирование ключей:**
```
-- Плохо: ключ собирается строкой в бизнес-логике
redis.get(f"notification:ws:conn:{user_id}")

-- Хорошо: через функцию из keys-модуля
redis.get(ws_connection_key(user_id))
```

---

## 6. Ссылки

- [Redis 7 Documentation](https://redis.io/docs/)
- [Redis Key Naming Conventions](https://redis.io/docs/latest/develop/use/keyspace/)
- [Redis Best Practices](https://redis.io/docs/latest/develop/use/patterns/)
