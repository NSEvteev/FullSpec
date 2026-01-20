---
type: standard
description: Интеграционные тесты: БД, API, сервисы
related:
  - tests/project-testing.md
  - tests/unit.md
  - tests/fixtures.md
  - src/runtime/database.md
---

# Интеграционные тесты

Правила написания интеграционных тестов для проверки взаимодействия компонентов системы.

## Оглавление

- [Отличие от unit-тестов](#отличие-от-unit-тестов)
- [Что тестировать](#что-тестировать)
- [Структура](#структура)
- [Правила](#правила)
- [Тестирование БД](#тестирование-бд)
- [Тестирование API](#тестирование-api)
- [Тестирование сервисов](#тестирование-сервисов)
- [Примеры](#примеры)
- [Антипаттерны](#антипаттерны)
- [Связанные инструкции](#связанные-инструкции)

---

## Отличие от unit-тестов

| Аспект | Unit-тесты | Интеграционные тесты |
|--------|------------|---------------------|
| **Scope** | Один модуль | Несколько модулей |
| **Зависимости** | Мокаются | Реальные (БД, API) |
| **Скорость** | Миллисекунды | Секунды |
| **Изоляция** | Полная | Частичная |
| **Цель** | Логика модуля | Взаимодействие |

### Пирамида тестирования

```
        /\
       /  \      E2E (мало, медленные)
      /----\
     /      \    Integration (средне)
    /--------\
   /          \  Unit (много, быстрые)
  /____________\
```

**Правило:** 70% unit, 20% integration, 10% e2e.

---

## Что тестировать

### Обязательно

| Компонент | Что проверять |
|-----------|---------------|
| **БД** | CRUD операции, транзакции, миграции |
| **API endpoints** | Request/response, статус-коды, валидация |
| **Межсервисное** | HTTP вызовы между сервисами |
| **Очереди** | Отправка и получение сообщений |
| **Кэш** | Запись, чтение, инвалидация |

### Не тестировать интеграционно

- Бизнес-логику (unit-тесты)
- UI-взаимодействия (e2e)
- Внешние API (contract tests)

---

## Структура

### Расположение файлов

```
/tests/
  /integration/
    /auth/
      login.integration.test.ts
      register.integration.test.ts
    /users/
      crud.integration.test.ts
    /setup/
      database.ts          ← setup/teardown для БД
      testcontainers.ts    ← Docker контейнеры
```

### Именование

| Паттерн | Пример |
|---------|--------|
| `*.integration.test.ts` | `login.integration.test.ts` |
| `*.integration.spec.ts` | `users.integration.spec.ts` |
| `test_*_integration.py` | `test_auth_integration.py` |

---

## Правила

### 1. Изолированное окружение

Каждый тест должен работать с чистым состоянием:

```typescript
// setup/database.ts
export async function resetDatabase() {
  await db.query('TRUNCATE users, orders, payments CASCADE');
}

// В тесте
beforeEach(async () => {
  await resetDatabase();
});
```

### 2. Testcontainers для зависимостей

```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';

let container: PostgreSqlContainer;

beforeAll(async () => {
  container = await new PostgreSqlContainer()
    .withDatabase('test_db')
    .start();

  process.env.DATABASE_URL = container.getConnectionUri();
});

afterAll(async () => {
  await container.stop();
});
```

### 3. Транзакционная изоляция

```typescript
// Вариант 1: Откат транзакции после теста
beforeEach(async () => {
  await db.query('BEGIN');
});

afterEach(async () => {
  await db.query('ROLLBACK');
});

// Вариант 2: Truncate таблиц
afterEach(async () => {
  await db.query('TRUNCATE users CASCADE');
});
```

### 4. Реальные данные, не моки

```typescript
// Плохо — мок БД в интеграционном тесте
const mockDb = { query: jest.fn() };

// Хорошо — реальная БД (testcontainers)
const result = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
expect(result.rows[0].email).toBe('test@example.com');
```

### 5. Таймауты

```typescript
// Интеграционные тесты медленнее — увеличиваем таймаут
jest.setTimeout(30000); // 30 секунд

// Или для конкретного теста
it('should process large dataset', async () => {
  // ...
}, 60000);
```

---

## Тестирование БД

### Подготовка тестовой БД

```typescript
// setup/database.ts
import { Pool } from 'pg';

const testPool = new Pool({
  connectionString: process.env.TEST_DATABASE_URL
});

export async function setupTestDb() {
  // Применить миграции
  await runMigrations(testPool);
}

export async function teardownTestDb() {
  await testPool.end();
}

export async function cleanTables() {
  const tables = ['users', 'orders', 'payments'];
  for (const table of tables) {
    await testPool.query(`TRUNCATE ${table} CASCADE`);
  }
}
```

### Тестирование CRUD

```typescript
describe('UserRepository', () => {
  let repo: UserRepository;

  beforeAll(async () => {
    await setupTestDb();
    repo = new UserRepository(testPool);
  });

  afterAll(async () => {
    await teardownTestDb();
  });

  beforeEach(async () => {
    await cleanTables();
  });

  describe('create', () => {
    it('should insert user into database', async () => {
      const userData = { email: 'test@example.com', name: 'Test' };

      const user = await repo.create(userData);

      expect(user.id).toBeDefined();
      expect(user.email).toBe(userData.email);

      // Проверяем, что данные реально в БД
      const dbUser = await repo.findById(user.id);
      expect(dbUser).toEqual(user);
    });
  });

  describe('update', () => {
    it('should update existing user', async () => {
      const user = await repo.create({ email: 'old@example.com', name: 'Old' });

      await repo.update(user.id, { name: 'New' });

      const updated = await repo.findById(user.id);
      expect(updated.name).toBe('New');
      expect(updated.email).toBe('old@example.com'); // Не изменилось
    });
  });
});
```

### Тестирование транзакций

```typescript
describe('OrderService transactions', () => {
  it('should rollback on payment failure', async () => {
    const user = await userRepo.create({ balance: 100 });

    // Платёж должен упасть
    await expect(
      orderService.createOrder(user.id, { amount: 200 })
    ).rejects.toThrow('Insufficient balance');

    // Проверяем, что баланс не изменился (откат)
    const freshUser = await userRepo.findById(user.id);
    expect(freshUser.balance).toBe(100);
  });
});
```

---

## Тестирование API

### Supertest для HTTP

```typescript
import request from 'supertest';
import { app } from '../src/app';

describe('POST /api/users', () => {
  it('should create user and return 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'new@example.com', name: 'New User' })
      .expect(201);

    expect(response.body.id).toBeDefined();
    expect(response.body.email).toBe('new@example.com');
  });

  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid', name: 'Test' })
      .expect(400);

    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });

  it('should return 409 for duplicate email', async () => {
    // Сначала создаём пользователя
    await request(app)
      .post('/api/users')
      .send({ email: 'exists@example.com', name: 'First' });

    // Пытаемся создать с тем же email
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'exists@example.com', name: 'Second' })
      .expect(409);

    expect(response.body.error.code).toBe('USER_EXISTS');
  });
});
```

### Аутентификация в тестах

```typescript
describe('Protected endpoints', () => {
  let authToken: string;

  beforeAll(async () => {
    // Создаём тестового пользователя и получаем токен
    const user = await createTestUser();
    authToken = generateToken(user);
  });

  it('should return 401 without token', async () => {
    await request(app)
      .get('/api/profile')
      .expect(401);
  });

  it('should return profile with valid token', async () => {
    const response = await request(app)
      .get('/api/profile')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);

    expect(response.body.email).toBeDefined();
  });
});
```

---

## Тестирование сервисов

### HTTP между сервисами

```typescript
import nock from 'nock';

describe('PaymentService', () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it('should call external payment API', async () => {
    // Мокаем внешний сервис
    nock('https://payment-provider.com')
      .post('/charge')
      .reply(200, { transactionId: 'tx_123', status: 'success' });

    const result = await paymentService.charge({
      amount: 100,
      currency: 'USD'
    });

    expect(result.transactionId).toBe('tx_123');
  });

  it('should handle payment provider timeout', async () => {
    nock('https://payment-provider.com')
      .post('/charge')
      .delay(5000)
      .reply(200);

    await expect(
      paymentService.charge({ amount: 100 })
    ).rejects.toThrow('Payment timeout');
  });
});
```

### Очереди сообщений

```typescript
describe('NotificationService', () => {
  let rabbitConnection: Connection;
  let channel: Channel;

  beforeAll(async () => {
    rabbitConnection = await amqp.connect(process.env.RABBITMQ_URL);
    channel = await rabbitConnection.createChannel();
  });

  afterAll(async () => {
    await channel.close();
    await rabbitConnection.close();
  });

  it('should publish message to queue', async () => {
    const messages: any[] = [];

    // Подписываемся на очередь
    await channel.consume('notifications', (msg) => {
      messages.push(JSON.parse(msg.content.toString()));
    });

    // Отправляем уведомление
    await notificationService.send({
      userId: '123',
      type: 'welcome'
    });

    // Ждём получения
    await waitFor(() => messages.length > 0);

    expect(messages[0]).toEqual({
      userId: '123',
      type: 'welcome'
    });
  });
});
```

---

## Примеры

### Полный пример: тест регистрации

```typescript
// tests/integration/auth/register.integration.test.ts
import request from 'supertest';
import { app } from '../../../src/app';
import { db, cleanTables } from '../../setup/database';
import { mailhog } from '../../setup/mailhog';

describe('User Registration Flow', () => {
  beforeEach(async () => {
    await cleanTables();
    await mailhog.deleteAll();
  });

  it('should register user, save to DB, and send welcome email', async () => {
    // 1. Регистрация через API
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'newuser@example.com',
        password: 'SecurePass123!',
        name: 'New User'
      })
      .expect(201);

    const userId = response.body.id;

    // 2. Проверяем, что пользователь в БД
    const dbUser = await db.query(
      'SELECT * FROM users WHERE id = $1',
      [userId]
    );
    expect(dbUser.rows[0].email).toBe('newuser@example.com');
    expect(dbUser.rows[0].password_hash).not.toBe('SecurePass123!'); // Захеширован

    // 3. Проверяем, что email отправлен
    const emails = await mailhog.getMessages();
    expect(emails).toHaveLength(1);
    expect(emails[0].to).toBe('newuser@example.com');
    expect(emails[0].subject).toContain('Welcome');
  });
});
```

---

## Антипаттерны

### 1. Зависимость от порядка тестов

```typescript
// Плохо — тесты зависят друг от друга
it('should create user', async () => {
  createdUserId = await createUser();
});

it('should get created user', async () => {
  const user = await getUser(createdUserId); // Зависит от предыдущего!
});

// Хорошо — каждый тест независим
it('should get user by id', async () => {
  const user = await createUser(); // Создаём внутри теста
  const fetched = await getUser(user.id);
  expect(fetched).toEqual(user);
});
```

### 2. Shared state без очистки

```typescript
// Плохо — данные накапливаются
it('test 1', async () => { await db.insert(user1); });
it('test 2', async () => { await db.insert(user2); });
// К тесту N в БД уже N пользователей!

// Хорошо — очистка перед каждым тестом
beforeEach(async () => { await cleanTables(); });
```

### 3. Hardcoded URLs и порты

```typescript
// Плохо
const response = await fetch('http://localhost:3000/api/users');

// Хорошо
const response = await request(app).get('/api/users');
// или
const response = await fetch(`${process.env.API_URL}/api/users`);
```

---

## Связанные инструкции

- [project-testing.md](./project-testing.md) — индекс тестирования
- [unit.md](./unit.md) — unit-тесты
- [fixtures.md](./fixtures.md) — тестовые данные
- [src/runtime/database.md](../src/runtime/database.md) — работа с БД
