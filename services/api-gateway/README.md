# API Gateway

Единая точка входа для всех клиентских запросов. Маршрутизирует запросы к соответствующим микросервисам.

## Функциональность

- ✅ Маршрутизация запросов к сервисам
- ✅ Валидация JWT токенов
- ✅ Rate limiting
- ✅ Request/Response logging
- ✅ CORS обработка
- ✅ Load balancing (при нескольких инстансах сервисов)
- ✅ Request/Response трансформация
- ✅ Кэширование ответов

## Структура

```
api-gateway/
├── src/                   # Исходный код gateway
├── tests/                 # Тесты
├── .env.example           # Пример переменных окружения
├── Dockerfile             # Docker конфигурация
├── package.json           # Зависимости
└── README.md              # Этот файл
```

## Технологический стек

**TODO:** Выбрать стек для API Gateway:
- Node.js + Express + http-proxy-middleware
- Kong API Gateway
- NGINX + Lua
- Traefik
- Envoy Proxy

## Переменные окружения

```env
# Порт API Gateway
PORT=8000

# Сервисы
AUTH_SERVICE_URL=http://auth:8001
USERS_SERVICE_URL=http://users:8002

# Rate limiting
RATE_LIMIT_WINDOW=15m
RATE_LIMIT_MAX=100
RATE_LIMIT_SKIP_SUCCESSFUL=false

# CORS
CORS_ORIGINS=http://localhost:3000,https://app.example.com
CORS_CREDENTIALS=true

# Кэширование
REDIS_URL=redis://redis:6379
CACHE_TTL=60  # секунды

# Логирование
LOG_LEVEL=info
LOG_REQUESTS=true
LOG_RESPONSES=false  # Не логировать тела ответов в production
```

## Маршрутизация

### Auth Service

```
/api/auth/*  →  http://auth:8001/api/auth/*
```

**Примеры:**
- `POST /api/auth/login` → `http://auth:8001/api/auth/login`
- `POST /api/auth/register` → `http://auth:8001/api/auth/register`
- `POST /api/auth/refresh` → `http://auth:8001/api/auth/refresh`

### Users Service

```
/api/users/*  →  http://users:8002/api/users/*
```

**Примеры:**
- `GET /api/users/me` → `http://users:8002/api/users/me`
- `PUT /api/users/me` → `http://users:8002/api/users/me`
- `POST /api/users/me/avatar` → `http://users:8002/api/users/me/avatar`

## Middleware Pipeline

```
Request
  ↓
1. CORS Handler
  ↓
2. Rate Limiter
  ↓
3. Request Logger
  ↓
4. JWT Validator (для защищенных роутов)
  ↓
5. Route Matcher
  ↓
6. Service Proxy
  ↓
7. Response Cache (для GET запросов)
  ↓
8. Response Logger
  ↓
Response
```

## Защищенные роуты

Роуты, требующие авторизации:

```typescript
const protectedRoutes = [
  '/api/users/me',
  '/api/users/me/*',
  // Все остальные /api/users/* требуют admin прав
];

const publicRoutes = [
  '/api/auth/login',
  '/api/auth/register',
  '/api/auth/forgot-password',
  '/health',
  '/metrics',
];
```

## Rate Limiting

### По IP адресу

```typescript
// Глобальный лимит
const globalLimit = {
  windowMs: 15 * 60 * 1000,  // 15 минут
  max: 100,                   // 100 запросов
};

// Для auth эндпоинтов (строже)
const authLimit = {
  windowMs: 15 * 60 * 1000,
  max: 5,  // Только 5 попыток логина
};
```

### По пользователю (после авторизации)

```typescript
const userLimit = {
  windowMs: 15 * 60 * 1000,
  max: 1000,  // Авторизованные пользователи
};
```

## Кэширование

GET запросы кэшируются в Redis:

```typescript
const cacheConfig = {
  '/api/users/:id': 60,        // 60 секунд
  '/api/users/:id/avatar': 300, // 5 минут
};
```

Инвалидация при:
- PUT/POST/DELETE запросах к тому же ресурсу
- Явном вызове `/api/cache/invalidate`

## Обработка ошибок

```typescript
// Сервис недоступен
503 Service Unavailable
{
  "error": "Service Temporarily Unavailable",
  "service": "auth",
  "message": "Auth service is down"
}

// Таймаут
504 Gateway Timeout
{
  "error": "Gateway Timeout",
  "service": "users",
  "timeout": "5000ms"
}

// Rate limit
429 Too Many Requests
{
  "error": "Too Many Requests",
  "retryAfter": 900  // секунды
}
```

## Мониторинг

### Health Check

```
GET /health

Response:
{
  "status": "healthy",
  "services": {
    "auth": "up",
    "users": "up"
  },
  "uptime": 3600
}
```

### Метрики

```
GET /metrics

# Prometheus формат
http_requests_total{service="auth",method="POST",status="200"} 150
http_requests_total{service="users",method="GET",status="200"} 450
http_request_duration_ms{service="auth"} 45
```

## Логирование

### Request Log

```json
{
  "timestamp": "2026-01-15T10:00:00Z",
  "method": "POST",
  "path": "/api/auth/login",
  "ip": "192.168.1.1",
  "userAgent": "Mozilla/5.0...",
  "requestId": "req-123-456"
}
```

### Response Log

```json
{
  "timestamp": "2026-01-15T10:00:01Z",
  "requestId": "req-123-456",
  "status": 200,
  "duration": 145,  // ms
  "service": "auth"
}
```

## Установка и запуск

```bash
# Установка зависимостей
npm install

# Запуск в dev режиме
npm run dev

# Запуск в production
npm start

# Docker
docker build -t api-gateway .
docker run -p 8000:8000 api-gateway
```

## Тестирование

```bash
# Unit тесты
npm test

# Integration тесты (с моками сервисов)
npm run test:integration

# Load testing
npm run test:load
```

## Безопасность

- ✅ CORS конфигурация
- ✅ Helmet.js для HTTP заголовков безопасности
- ✅ Rate limiting
- ✅ JWT валидация
- ✅ Request sanitization
- ✅ Защита от DDOS (через rate limiting)

## Масштабирование

Gateway поддерживает горизонтальное масштабирование:

```yaml
# docker-compose.yml
api-gateway:
  image: api-gateway
  deploy:
    replicas: 3  # 3 инстанса
  ports:
    - "8000:8000"
```

Load balancer (Nginx/HAProxy) распределяет трафик между инстансами.

## Дополнительная информация

- [Архитектура](../../general_docs/02_architecture/)
- [Мониторинг и логи](../../general_docs/05_resources/infra/)
