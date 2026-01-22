---
type: standard
description: Аутентификация между сервисами: JWT, service accounts
related:
  - /.claude/instructions/src/security/audit.md
  - /.claude/instructions/platform/security.md
  - /.claude/instructions/src/runtime/resilience.md
---

# Аутентификация между сервисами

Правила аутентификации и авторизации при межсервисном взаимодействии.

## Оглавление

- [Архитектура](#архитектура)
- [JWT токены](#jwt-токены)
- [Service accounts](#service-accounts)
- [Проверка токенов](#проверка-токенов)
- [Ротация ключей](#ротация-ключей)
- [Безопасность](#безопасность)
- [Примеры реализации](#примеры-реализации)
- [Связанные инструкции](#связанные-инструкции)

---

## Архитектура

### Схема аутентификации

```
┌─────────────┐      JWT        ┌─────────────┐
│   Service   │ ──────────────▶ │   Service   │
│     A       │                 │     B       │
│             │                 │             │
│ [SA: svc-a] │                 │ [Verifies]  │
└─────────────┘                 └─────────────┘
      │                               │
      │ signs JWT                     │ verifies signature
      │ with private key              │ with public key
      ▼                               ▼
┌─────────────────────────────────────────────┐
│              JWT Signing Keys               │
│  Private (svc-a) ←→ Public (shared)        │
└─────────────────────────────────────────────┘
```

### Принципы

| Принцип | Описание |
|---------|----------|
| **Zero Trust** | Каждый запрос проверяется, даже внутри периметра |
| **Least Privilege** | Service account имеет минимальные права |
| **Short-lived tokens** | JWT живёт максимум 15 минут |
| **Asymmetric keys** | RS256/ES256 для подписи |

---

## JWT токены

### Структура токена

```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "key-2024-01"
  },
  "payload": {
    "iss": "auth-service",
    "sub": "svc-payment",
    "aud": ["users-service", "orders-service"],
    "iat": 1705320000,
    "exp": 1705320900,
    "jti": "unique-token-id",
    "scope": ["read:users", "write:orders"],
    "request_id": "req-abc-123"
  }
}
```

### Обязательные claims

| Claim | Описание | Пример |
|-------|----------|--------|
| `iss` | Кто выпустил токен | `auth-service` |
| `sub` | Service account | `svc-payment` |
| `aud` | Для кого токен | `["users-service"]` |
| `iat` | Время создания | Unix timestamp |
| `exp` | Время истечения | iat + 900 (15 мин) |
| `jti` | Уникальный ID | UUID v4 |
| `scope` | Права доступа | `["read:users"]` |

### Опциональные claims

| Claim | Назначение |
|-------|------------|
| `request_id` | Корреляция с исходным запросом |
| `user_id` | ID пользователя (если действие от имени user) |
| `tenant_id` | Multi-tenant идентификатор |

### TTL токенов

| Тип | TTL | Использование |
|-----|-----|---------------|
| Service-to-service | 15 минут | Межсервисные запросы |
| Background job | 1 час | Фоновые задачи |
| User delegation | 5 минут | Действия от имени пользователя |

---

## Service accounts

### Соглашения об именовании

```
svc-{service-name}
```

| Service Account | Сервис |
|-----------------|--------|
| `svc-auth` | Auth service |
| `svc-users` | Users service |
| `svc-payment` | Payment service |
| `svc-notification` | Notification service |

### Регистрация service account

```yaml
# config/service-accounts/payment.yaml
service_account:
  name: svc-payment
  description: Payment service
  allowed_scopes:
    - read:users
    - write:orders
    - read:orders
  allowed_audiences:
    - users-service
    - orders-service
  rate_limit: 1000/min
```

### Матрица доступа

| Service | Может вызывать | Scopes |
|---------|----------------|--------|
| auth | users | read:users |
| users | notification | send:email |
| payment | users, orders | read:users, write:orders |
| orders | payment, notification | charge:payment, send:email |

### Права (Scopes)

```
{action}:{resource}

Примеры:
- read:users        # читать пользователей
- write:orders      # создавать/обновлять заказы
- delete:sessions   # удалять сессии
- send:email        # отправлять email
- charge:payment    # списывать платежи
```

---

## Проверка токенов

### Алгоритм проверки

```
1. Извлечь токен из заголовка Authorization: Bearer {token}
2. Проверить формат JWT (3 части, base64)
3. Декодировать header, извлечь kid (key ID)
4. Получить public key по kid
5. Проверить подпись токена
6. Проверить claims:
   a. exp > now (не истёк)
   b. iat < now (не из будущего)
   c. aud содержит текущий сервис
   d. scope содержит требуемое право
7. Проверить jti не в blacklist (отозванные токены)
8. Пропустить запрос или вернуть 401/403
```

### Middleware проверки

```typescript
// middleware/auth.ts
import { verify } from 'jsonwebtoken';
import { getPublicKey } from './keys';

export async function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: { code: 'MISSING_TOKEN' } });
  }

  const token = authHeader.substring(7);

  try {
    // Декодировать header для получения kid
    const decoded = decodeHeader(token);
    const publicKey = await getPublicKey(decoded.kid);

    // Верифицировать токен
    const payload = verify(token, publicKey, {
      algorithms: ['RS256'],
      audience: process.env.SERVICE_NAME,
    });

    // Проверить scope
    if (!payload.scope.includes(req.requiredScope)) {
      return res.status(403).json({ error: { code: 'INSUFFICIENT_SCOPE' } });
    }

    req.serviceAccount = payload.sub;
    req.requestId = payload.request_id;
    next();
  } catch (error) {
    return res.status(401).json({ error: { code: 'INVALID_TOKEN' } });
  }
}
```

### Кэширование public keys

```typescript
// keys.ts
const keyCache = new Map<string, { key: string; expires: number }>();
const KEY_CACHE_TTL = 3600 * 1000; // 1 час

export async function getPublicKey(kid: string): Promise<string> {
  const cached = keyCache.get(kid);

  if (cached && cached.expires > Date.now()) {
    return cached.key;
  }

  // Получить из auth service или secrets manager
  const key = await fetchPublicKey(kid);

  keyCache.set(kid, {
    key,
    expires: Date.now() + KEY_CACHE_TTL,
  });

  return key;
}
```

---

## Ротация ключей

### Dual Key паттерн

```
Время:  ────────────────────────────────────────────▶

Key 1:  ████████████████████████████████
                    │
Key 2:              ████████████████████████████████
                    │
                    └── Период перекрытия (обе активны)
```

### Процесс ротации

1. **Генерация нового ключа** (kid: key-2024-02)
2. **Публикация public key** во все сервисы
3. **Период перехода** (7 дней): оба ключа активны
4. **Переключение**: новые токены подписываются key-2024-02
5. **Deprecation**: старый ключ только для верификации (7 дней)
6. **Удаление**: старый ключ отзывается

### Конфигурация ключей

```yaml
# config/jwt-keys.yaml
keys:
  - kid: key-2024-01
    status: deprecated    # только для верификации
    public_key: |
      -----BEGIN PUBLIC KEY-----
      MIIBIjANBg...
      -----END PUBLIC KEY-----
    expires: 2024-02-01

  - kid: key-2024-02
    status: active        # для подписи и верификации
    public_key: |
      -----BEGIN PUBLIC KEY-----
      MIIBIjANBg...
      -----END PUBLIC KEY-----
    private_key_ref: vault:jwt/key-2024-02
```

### Runbook ротации

```markdown
## Runbook: JWT Key Rotation

### Предусловия
- [ ] Новый ключ сгенерирован и сохранён в Vault
- [ ] Public key добавлен в config/jwt-keys.yaml

### Шаги
1. Deploy config с новым ключом (все сервисы)
2. Подождать 15 минут (распространение конфига)
3. Переключить auth-service на новый ключ для подписи
4. Мониторить ошибки 401 (не должно быть всплеска)
5. Через 7 дней: удалить старый ключ из конфига
6. Удалить старый private key из Vault

### Откат
- Вернуть status: active для старого ключа
- Переключить auth-service обратно
```

---

## Безопасность

### Обязательные требования

| Требование | Описание |
|------------|----------|
| HTTPS only | Токены передаются только через TLS |
| Short TTL | Максимум 15 минут для service-to-service |
| Audience check | Токен принимается только целевым сервисом |
| Scope check | Проверка прав перед операцией |
| Key rotation | Ротация минимум раз в 90 дней |

### Что НЕ включать в токен

- Пароли и секреты
- Полные данные пользователя
- PII без необходимости
- Токены других систем

### Отзыв токенов

```typescript
// Token blacklist (Redis)
const BLACKLIST_PREFIX = 'token:revoked:';

async function revokeToken(jti: string, exp: number): Promise<void> {
  const ttl = exp - Math.floor(Date.now() / 1000);
  if (ttl > 0) {
    await redis.setex(`${BLACKLIST_PREFIX}${jti}`, ttl, '1');
  }
}

async function isTokenRevoked(jti: string): Promise<boolean> {
  return await redis.exists(`${BLACKLIST_PREFIX}${jti}`) === 1;
}
```

### Логирование

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "event": "auth_success",
  "service": "users-service",
  "caller": "svc-payment",
  "scope": "read:users",
  "request_id": "req-abc-123",
  "latency_ms": 2
}
```

**Не логировать:** сам токен, private keys.

---

## Примеры реализации

### Создание токена (auth service)

```typescript
import { sign } from 'jsonwebtoken';
import { v4 as uuid } from 'uuid';

interface TokenRequest {
  serviceAccount: string;
  audience: string[];
  scopes: string[];
  requestId?: string;
}

export async function createServiceToken(req: TokenRequest): Promise<string> {
  const privateKey = await getPrivateKey();
  const now = Math.floor(Date.now() / 1000);

  const payload = {
    iss: 'auth-service',
    sub: req.serviceAccount,
    aud: req.audience,
    iat: now,
    exp: now + 900,  // 15 минут
    jti: uuid(),
    scope: req.scopes,
    request_id: req.requestId,
  };

  return sign(payload, privateKey, {
    algorithm: 'RS256',
    keyid: await getCurrentKeyId(),
  });
}
```

### Вызов другого сервиса

```typescript
import axios from 'axios';
import { createServiceToken } from './auth';

export async function callUsersService(userId: string): Promise<User> {
  const token = await createServiceToken({
    serviceAccount: 'svc-payment',
    audience: ['users-service'],
    scopes: ['read:users'],
    requestId: getCurrentRequestId(),
  });

  const response = await axios.get(
    `${USERS_SERVICE_URL}/api/v1/users/${userId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'X-Request-ID': getCurrentRequestId(),
      },
      timeout: 5000,
    }
  );

  return response.data;
}
```

### Защита эндпоинта

```typescript
import { Router } from 'express';
import { authMiddleware, requireScope } from './middleware/auth';

const router = Router();

// Все роуты требуют аутентификации
router.use(authMiddleware);

// Конкретный роут требует scope
router.get(
  '/users/:id',
  requireScope('read:users'),
  async (req, res) => {
    const user = await userService.findById(req.params.id);
    res.json(user);
  }
);
```

---

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование схемы аутентификации |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при изменении токенов |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Задача на ротацию ключей |

---

## Связанные инструкции

- [audit.md](./audit.md) — аудит-логи и GDPR
- [security.md](/.claude/instructions/platform/security.md) — безопасность инфраструктуры
- [resilience.md](/.claude/instructions/src/runtime/resilience.md) — устойчивость (таймауты, retry)
