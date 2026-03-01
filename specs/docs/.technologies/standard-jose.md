---
description: Стандарт кодирования JOSE (jose) — конвенции именования, паттерны JWT/JWS/JWE/JWK, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: jose
---

# Стандарт JOSE v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | jose 5.x |
| Ключевые библиотеки | `jose ^5.0` (npm) — JWS, JWE, JWT, JWK, JWKS |
| Конфигурация | Параметры алгоритмов и аудитории в `config/{env}/auth.yaml`; секреты в переменных окружения (`JWT_SECRET`, `JWT_PUBLIC_KEY`) |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|-----------|--------|
| Файл с JWT-логикой | kebab-case, суффикс `-token` | `access-token.ts`, `refresh-token.ts` |
| Файл с JWKS / ключами | kebab-case, суффикс `-keys` | `signing-keys.ts`, `jwks.ts` |
| Функция создания токена | camelCase, префикс `sign` | `signAccessToken`, `signRefreshToken` |
| Функция верификации | camelCase, префикс `verify` | `verifyAccessToken`, `verifyIdToken` |
| Функция декодирования (без проверки) | camelCase, префикс `decode` | `decodeTokenPayload` |
| Тип payload | PascalCase, суффикс `Payload` | `AccessTokenPayload`, `RefreshTokenPayload` |
| Константа алгоритма | SCREAMING_SNAKE | `JWT_ALGORITHM`, `KEY_ALGORITHM` |
| Переменная окружения (секрет) | SCREAMING_SNAKE | `JWT_SECRET`, `JWT_PUBLIC_KEY` |

## Паттерны кода

### Создание симметричного JWT (HS256)

Используется для простых случаев, когда и издатель, и проверяющий сторона разделяют один секрет. В сервисе `auth` — для access-токенов при монолитной/одно-сервисной верификации.

```typescript
import { SignJWT } from "jose";

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET!);
const JWT_ALGORITHM = "HS256";

export interface AccessTokenPayload {
  sub: string;        // user id
  role: string;
  sessionId: string;
}

export async function signAccessToken(
  payload: AccessTokenPayload,
  expiresIn: string = "15m"
): Promise<string> {
  return new SignJWT({ ...payload })
    .setProtectedHeader({ alg: JWT_ALGORITHM })
    .setIssuedAt()
    .setIssuer("auth-service")
    .setAudience("api")
    .setExpirationTime(expiresIn)
    .sign(JWT_SECRET);
}
```

### Создание JWT с асимметричным ключом (RS256 / ES256)

Используется когда несколько сервисов верифицируют токен без доступа к приватному ключу. Подписывает `auth`, верифицируют остальные сервисы через JWKS endpoint.

```typescript
import { SignJWT, importPKCS8 } from "jose";

const PRIVATE_KEY_PEM = process.env.JWT_PRIVATE_KEY!;
const JWT_ALGORITHM = "ES256";

export async function signAccessTokenAsymmetric(
  payload: AccessTokenPayload
): Promise<string> {
  const privateKey = await importPKCS8(PRIVATE_KEY_PEM, JWT_ALGORITHM);

  return new SignJWT({ ...payload })
    .setProtectedHeader({ alg: JWT_ALGORITHM, kid: "auth-key-1" })
    .setIssuedAt()
    .setIssuer("auth-service")
    .setAudience("api")
    .setExpirationTime("15m")
    .sign(privateKey);
}
```

### Верификация JWT и извлечение payload

Верификация всегда выполняется с явным указанием алгоритмов (`algorithms`), издателя (`issuer`) и аудитории (`audience`). Нельзя оставлять эти параметры пустыми.

```typescript
import { jwtVerify } from "jose";

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET!);

export async function verifyAccessToken(
  token: string
): Promise<AccessTokenPayload> {
  const { payload } = await jwtVerify(token, JWT_SECRET, {
    algorithms: ["HS256"],
    issuer: "auth-service",
    audience: "api",
  });

  // payload автоматически содержит стандартные claims; дополнительные — кастомные
  return payload as unknown as AccessTokenPayload;
}
```

### Верификация через JWKS URI (remote public keys)

Используется в downstream-сервисах, которые не хранят ключи локально. `createRemoteJWKSet` кэширует ключи автоматически.

```typescript
import { jwtVerify, createRemoteJWKSet } from "jose";

const JWKS = createRemoteJWKSet(
  new URL(process.env.JWKS_URI ?? "http://auth-service/.well-known/jwks.json")
);

export async function verifyTokenRemote(token: string): Promise<AccessTokenPayload> {
  const { payload } = await jwtVerify(token, JWKS, {
    algorithms: ["ES256"],
    issuer: "auth-service",
    audience: "api",
  });

  return payload as unknown as AccessTokenPayload;
}
```

### Обработка ошибок верификации

`jose` бросает именованные ошибки из `jose/errors`. Всегда различать истёкший токен (→ 401 с refresh-потоком) и невалидный (→ 401 без retry).

```typescript
import { jwtVerify, errors } from "jose";

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET!);

export async function verifyTokenSafe(
  token: string
): Promise<{ payload: AccessTokenPayload } | { error: "expired" | "invalid" }> {
  try {
    const { payload } = await jwtVerify(token, JWT_SECRET, {
      algorithms: ["HS256"],
      issuer: "auth-service",
      audience: "api",
    });
    return { payload: payload as unknown as AccessTokenPayload };
  } catch (err) {
    if (err instanceof errors.JWTExpired) {
      return { error: "expired" };
    }
    if (
      err instanceof errors.JWTInvalid ||
      err instanceof errors.JWSSignatureVerificationFailed ||
      err instanceof errors.JWSInvalid
    ) {
      return { error: "invalid" };
    }
    throw err; // неожиданная ошибка — пробросить вверх
  }
}
```

### Генерация и экспорт JWK / JWKS

Используется при инициализации сервиса для генерации ключевой пары и публикации JWKS endpoint.

```typescript
import { generateKeyPair, exportJWK, exportPKCS8 } from "jose";

export interface KeySet {
  privateKeyPem: string;
  jwks: { keys: object[] };
}

export async function generateSigningKeyPair(): Promise<KeySet> {
  const { privateKey, publicKey } = await generateKeyPair("ES256", {
    extractable: true,
  });

  const privateKeyPem = await exportPKCS8(privateKey);
  const publicJwk = await exportJWK(publicKey);

  return {
    privateKeyPem,
    jwks: {
      keys: [{ ...publicJwk, use: "sig", alg: "ES256", kid: "auth-key-1" }],
    },
  };
}
```

### Refresh-токен

Refresh-токен отличается от access-токена тремя ключевыми параметрами: длинный TTL (7–30 дней), `audience` указывает на endpoint обновления, а `jti` (JWT ID) хранится в БД для возможности отзыва. При использовании refresh-токена всегда проверять `jti` по БД перед выдачей нового access-токена.

```typescript
import { SignJWT, jwtVerify } from "jose";

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET!);
const JWT_ALGORITHM = "HS256";

export interface RefreshTokenPayload {
  sub: string;        // user id
  jti: string;        // уникальный ID токена — хранится в БД для отзыва
  sessionId: string;
}

// Создать refresh-токен (TTL 30 дней, audience — endpoint обновления)
export async function signRefreshToken(
  payload: RefreshTokenPayload,
  expiresIn: string = "30d"
): Promise<string> {
  return new SignJWT({ jti: payload.jti, sessionId: payload.sessionId })
    .setProtectedHeader({ alg: JWT_ALGORITHM })
    .setSubject(payload.sub)
    .setIssuedAt()
    .setIssuer("auth-service")
    .setAudience("auth-service/refresh")  // отличается от access-токена
    .setJti(payload.jti)
    .setExpirationTime(expiresIn)
    .sign(JWT_SECRET);
}

// Верифицировать refresh-токен (audience и issuer строго отличаются от access)
export async function verifyRefreshToken(
  token: string
): Promise<RefreshTokenPayload> {
  const { payload } = await jwtVerify(token, JWT_SECRET, {
    algorithms: ["HS256"],
    issuer: "auth-service",
    audience: "auth-service/refresh",  // намеренно другой audience
  });

  // ОБЯЗАТЕЛЬНО: проверить jti по БД — токен не был отозван
  // const isValid = await tokenStore.exists(payload.jti!);
  // if (!isValid) throw new Error("Refresh token revoked");

  return payload as unknown as RefreshTokenPayload;
}
```

Отличия от access-токена:

| Параметр | Access-токен | Refresh-токен |
|----------|-------------|---------------|
| TTL | 15 мин | 7–30 дней |
| `audience` | `"api"` | `"auth-service/refresh"` |
| `jti` | не обязателен | обязателен — хранить в БД |
| Хранение на клиенте | память / `Authorization` header | `httpOnly cookie` |
| Отзыв | по TTL | удалить `jti` из БД |

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| Верификация без указания `algorithms` | Позволяет downgrade-атаку: злоумышленник может подменить алгоритм на `none` или слабый. JWT с `alg: none` будет принят | Всегда передавать `algorithms: ["HS256"]` (или конкретный алгоритм) в `jwtVerify` |
| Хранить `JWT_SECRET` в коде | Секрет попадает в репозиторий, все выпущенные токены компрометируются | Использовать переменные окружения; секрет никогда не коммитить |
| Не проверять `issuer` и `audience` | Токен от другого сервиса или приложения будет принят — нарушение изоляции | Всегда указывать `issuer` и `audience` в `jwtVerify` |
| Decode без verify для авторизации | `decodeTokenPayload` не проверяет подпись — любой может сфабриковать payload | `decode`-функции использовать только для логирования/дебага; авторизацию строить на `verifyAccessToken` |
| Слишком длинный TTL access-токена | Компрометированный токен действует долго, нет механизма отзыва | Access-токен: 15 мин; refresh-токен: 7–30 дней с хранением в БД |
| Использовать симметричный HS256 в мультисервисной архитектуре | Все сервисы должны знать общий секрет — утечка в одном сервисе компрометирует всю систему | RS256 / ES256: приватный ключ только в `auth`, публичный — через JWKS |
| Игнорировать ошибки `JWTExpired` | Истёкший токен обрабатывается как невалидный — клиент не может обновить его | Различать `JWTExpired` (→ 401 + refresh) и `JWSSignatureVerificationFailed` (→ 401 без retry) |

## Структура файлов

```
src/auth/
├── backend/
│   └── src/
│       ├── tokens/
│       │   ├── access-token.ts    # signAccessToken, verifyAccessToken
│       │   ├── refresh-token.ts   # signRefreshToken, verifyRefreshToken
│       │   └── index.ts           # re-export
│       ├── keys/
│       │   ├── signing-keys.ts    # generateSigningKeyPair, loadPrivateKey
│       │   └── jwks.ts            # JWKS endpoint handler, createRemoteJWKSet
│       └── middleware/
│           └── auth.middleware.ts # Express/Fastify middleware для верификации
└── tests/
    └── unit/
        └── tokens/
            ├── access-token.test.ts
            └── refresh-token.test.ts
```

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется вручную по чек-листу из [validation-technology.md](../../.instructions/docs/technology/validation-technology.md).*

## Тестирование

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| Фреймворк | `vitest ^1.x` или `jest ^29.x` | Основной test runner |
| Типы | `@types/node` | Node.js типы для `TextEncoder` / `process.env` |

### Фикстуры

Фикстуры создают ключи и подписанные токены один раз на suite, чтобы не генерировать ключи в каждом тесте.

```typescript
// tests/unit/tokens/fixtures.ts
import { SignJWT } from "jose";

export const TEST_SECRET = new TextEncoder().encode("test-secret-min-32-bytes-long-key!");
export const JWT_OPTIONS = {
  algorithms: ["HS256"] as const,
  issuer: "auth-service",
  audience: "api",
};

export async function makeAccessToken(
  payload: Partial<AccessTokenPayload> = {},
  overrides: { expiresIn?: string } = {}
): Promise<string> {
  const defaults: AccessTokenPayload = {
    sub: "user-123",
    role: "user",
    sessionId: "sess-abc",
  };

  return new SignJWT({ ...defaults, ...payload })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setIssuer("auth-service")
    .setAudience("api")
    .setExpirationTime(overrides.expiresIn ?? "15m")
    .sign(TEST_SECRET);
}
```

### Мокирование

- **Unit-тесты токенов:** используем реальный `jose` с тестовым секретом — мокирование JOSE не нужно, библиотека детерминирована.
- **Unit-тесты middleware:** мокируем функции `verifyAccessToken` / `verifyTokenRemote` — тестируем логику middleware без криптографии.
- **JWKS remote:** мокируем `fetch` через `vi.spyOn(global, "fetch")` или `jest.spyOn` — не делаем реальных HTTP-запросов.

```typescript
// Мок verifyAccessToken для тестирования middleware
import { vi } from "vitest";
import * as tokenModule from "../../tokens/access-token.js";

export function mockVerifyAccessToken(result: AccessTokenPayload) {
  return vi.spyOn(tokenModule, "verifyAccessToken").mockResolvedValue(result);
}

export function mockVerifyAccessTokenFail(error: Error) {
  return vi.spyOn(tokenModule, "verifyAccessToken").mockRejectedValue(error);
}
```

### Паттерны тестов

```typescript
import { describe, it, expect } from "vitest";
import { errors } from "jose";
import { signAccessToken, verifyAccessToken } from "../../tokens/access-token.js";
import { TEST_SECRET, makeAccessToken } from "./fixtures.js";

// Подменяем секрет для тестов
vi.stubEnv("JWT_SECRET", "test-secret-min-32-bytes-long-key!");

describe("signAccessToken", () => {
  it("returns a JWT string", async () => {
    const token = await signAccessToken({
      sub: "user-1",
      role: "admin",
      sessionId: "s1",
    });
    expect(typeof token).toBe("string");
    expect(token.split(".")).toHaveLength(3);
  });
});

describe("verifyAccessToken", () => {
  it("returns payload for valid token", async () => {
    const token = await makeAccessToken({ sub: "user-42" });
    const payload = await verifyAccessToken(token);
    expect(payload.sub).toBe("user-42");
  });

  it("throws JWTExpired for expired token", async () => {
    const expired = await makeAccessToken({}, { expiresIn: "1ms" });
    // небольшая задержка, чтобы токен истёк
    await new Promise((r) => setTimeout(r, 5));
    await expect(verifyAccessToken(expired)).rejects.toBeInstanceOf(
      errors.JWTExpired
    );
  });

  it("throws JWSSignatureVerificationFailed for tampered token", async () => {
    const token = await makeAccessToken();
    const tampered = token.slice(0, -3) + "xxx"; // повредить подпись
    await expect(verifyAccessToken(tampered)).rejects.toBeInstanceOf(
      errors.JWSSignatureVerificationFailed
    );
  });
});
```

## Логирование

JOSE сам не логирует — логирование результатов верификации делается в middleware или use-case.

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| Токен успешно верифицирован | DEBUG | `auth.token_verified sub="user-123" session="sess-abc"` |
| Токен истёк | INFO | `auth.token_expired sub="user-123" expired_at="2026-01-15T10:00:00Z"` |
| Невалидная подпись | WARNING | `auth.token_invalid reason="signature_mismatch" ip="1.2.3.4"` |
| Неизвестный алгоритм / некорректный формат | WARNING | `auth.token_malformed reason="invalid_format" ip="1.2.3.4"` |
| Ошибка загрузки JWKS | ERROR | `auth.jwks_fetch_failed url="http://auth/.well-known/jwks.json" error="timeout"` |

```typescript
import { jwtVerify, errors } from "jose";
import { logger } from "@shared/logger";

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET!);

export async function verifyAndLog(token: string, ip: string): Promise<AccessTokenPayload> {
  try {
    const { payload } = await jwtVerify(token, JWT_SECRET, {
      algorithms: ["HS256"],
      issuer: "auth-service",
      audience: "api",
    });
    const p = payload as unknown as AccessTokenPayload;
    logger.debug("auth.token_verified", { sub: p.sub, session: p.sessionId });
    return p;
  } catch (err) {
    if (err instanceof errors.JWTExpired) {
      logger.info("auth.token_expired", { sub: (err.payload as any).sub });
      throw err;
    }
    if (err instanceof errors.JWSSignatureVerificationFailed) {
      logger.warn("auth.token_invalid", { reason: "signature_mismatch", ip });
      throw err;
    }
    logger.warn("auth.token_malformed", { reason: "invalid_format", ip });
    throw err;
  }
}
```
