---
type: standard
description: Тестовые данные: фикстуры, фабрики, seeds
related:
  - tests/project-testing.md
  - tests/unit.md
  - tests/integration.md
  - tests/e2e.md
---

# Тестовые данные (Fixtures)

Правила организации тестовых данных: фикстуры, фабрики, seeds.

## Оглавление

- [Что такое fixtures](#что-такое-fixtures)
- [Типы тестовых данных](#типы-тестовых-данных)
- [Структура](#структура)
- [Правила](#правила)
- [Фабрики](#фабрики)
- [Статические фикстуры](#статические-фикстуры)
- [Seeds](#seeds)
- [Примеры](#примеры)
- [Антипаттерны](#антипаттерны)
- [Связанные инструкции](#связанные-инструкции)

---

## Что такое fixtures

**Fixtures** — предопределённые тестовые данные, используемые для создания воспроизводимых условий тестирования.

### Зачем нужны

| Проблема без fixtures | Решение с fixtures |
|----------------------|-------------------|
| Тесты зависят от состояния БД | Каждый тест создаёт свои данные |
| Нельзя воспроизвести баг | Фиксированные данные → воспроизводимость |
| Тесты медленные (создание данных) | Переиспользование общих fixtures |
| Захардкоженные данные в тестах | Централизованное управление |

---

## Типы тестовых данных

### Сравнение подходов

| Тип | Когда использовать | Плюсы | Минусы |
|-----|-------------------|-------|--------|
| **Фабрики** | Unit/Integration тесты | Гибкость, типизация | Код для каждой сущности |
| **Статические fixtures** | E2E, snapshot тесты | Простота, стабильность | Сложно менять |
| **Seeds** | Разработка, демо | Реалистичные данные | Синхронизация с миграциями |
| **Inline данные** | Простые unit тесты | Читаемость | Дублирование |

### Когда что использовать

```
┌────────────────────────────────────────────────────────┐
│                    Unit Tests                          │
│  → Фабрики (создаём только нужные поля)               │
├────────────────────────────────────────────────────────┤
│                Integration Tests                       │
│  → Фабрики + Seeds для справочников                   │
├────────────────────────────────────────────────────────┤
│                   E2E Tests                            │
│  → Статические fixtures + API setup                   │
├────────────────────────────────────────────────────────┤
│               Local Development                        │
│  → Seeds (полный набор данных)                        │
└────────────────────────────────────────────────────────┘
```

---

## Структура

### Расположение файлов

```
/tests/
  /fixtures/
    /factories/               ← Фабрики для генерации
      user.factory.ts
      order.factory.ts
      product.factory.ts
      index.ts                ← Экспорт всех фабрик
    /static/                  ← Статические данные
      users.json
      products.json
      api-responses/
        success.json
        error.json
    /seeds/                   ← Seeds для БД
      users.seed.ts
      products.seed.ts
      run-seeds.ts
    /mocks/                   ← Моки внешних сервисов
      payment-provider.mock.ts
      email-service.mock.ts

/src/{service}/
  /tests/
    /fixtures/                ← Фикстуры сервиса (co-located)
      user.factory.ts
```

### Именование

| Тип | Паттерн | Пример |
|-----|---------|--------|
| Фабрика | `*.factory.ts` | `user.factory.ts` |
| Статические | `*.json` | `users.json` |
| Seeds | `*.seed.ts` | `users.seed.ts` |
| Моки | `*.mock.ts` | `stripe.mock.ts` |

---

## Правила

### 1. Минимальные данные

```typescript
// Плохо — слишком много полей
const user = createUser({
  id: '123',
  email: 'test@example.com',
  name: 'Test User',
  phone: '+1234567890',
  address: '123 Test St',
  city: 'Test City',
  country: 'Test Country',
  createdAt: new Date(),
  updatedAt: new Date(),
  // ... ещё 20 полей
});

// Хорошо — только нужное для теста
const user = createUser({ email: 'test@example.com' });
// Остальное — defaults из фабрики
```

### 2. Изоляция данных

```typescript
// Плохо — shared данные между тестами
const testUser = { id: '1', email: 'shared@test.com' };

test('test 1', () => { /* использует testUser */ });
test('test 2', () => { /* тоже использует testUser — конфликт! */ });

// Хорошо — каждый тест создаёт свои данные
test('test 1', () => {
  const user = createUser();
  // ...
});

test('test 2', () => {
  const user = createUser();
  // ...
});
```

### 3. Детерминированность

```typescript
// Плохо — случайные данные без seed
const user = {
  id: uuid(),  // Каждый раз разный!
  name: faker.name.fullName(),
};

// Хорошо — фиксированный seed для воспроизводимости
faker.seed(12345);
const user = {
  id: faker.string.uuid(),
  name: faker.person.fullName(),
};
// Или явное значение
const user = createUser({ id: 'fixed-id-123' });
```

### 4. Типизация

```typescript
// Хорошо — типизированные фабрики
interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
}

function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    role: 'user',
    ...overrides,
  };
}
```

### 5. Очистка после тестов

```typescript
// В integration/e2e тестах
afterEach(async () => {
  // Удаляем созданные данные
  await db.query('TRUNCATE users, orders CASCADE');
});

// Или через transaction rollback
beforeEach(async () => {
  await db.query('BEGIN');
});

afterEach(async () => {
  await db.query('ROLLBACK');
});
```

---

## Фабрики

### Базовая фабрика

```typescript
// tests/fixtures/factories/user.factory.ts
import { faker } from '@faker-js/faker';

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
  createdAt: Date;
}

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    role: 'user',
    createdAt: new Date(),
    ...overrides,
  };
}

// Хелперы для частых случаев
export function createAdmin(overrides: Partial<User> = {}): User {
  return createUser({ role: 'admin', ...overrides });
}

export function createUsers(count: number, overrides: Partial<User> = {}): User[] {
  return Array.from({ length: count }, () => createUser(overrides));
}
```

### Связанные сущности

```typescript
// tests/fixtures/factories/order.factory.ts
import { createUser, User } from './user.factory';
import { createProduct, Product } from './product.factory';

export interface Order {
  id: string;
  user: User;
  products: Product[];
  total: number;
  status: 'pending' | 'paid' | 'shipped';
}

export function createOrder(overrides: Partial<Order> = {}): Order {
  const products = overrides.products ?? [createProduct(), createProduct()];
  const total = products.reduce((sum, p) => sum + p.price, 0);

  return {
    id: faker.string.uuid(),
    user: overrides.user ?? createUser(),
    products,
    total,
    status: 'pending',
    ...overrides,
  };
}
```

### Фабрика с builder-паттерном

```typescript
// tests/fixtures/factories/user.builder.ts
export class UserBuilder {
  private user: Partial<User> = {};

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  withRole(role: 'user' | 'admin'): this {
    this.user.role = role;
    return this;
  }

  asAdmin(): this {
    return this.withRole('admin');
  }

  build(): User {
    return createUser(this.user);
  }
}

// Использование
const admin = new UserBuilder()
  .withEmail('admin@example.com')
  .asAdmin()
  .build();
```

### Индекс фабрик

```typescript
// tests/fixtures/factories/index.ts
export * from './user.factory';
export * from './order.factory';
export * from './product.factory';

// Использование в тестах
import { createUser, createOrder, createProduct } from '../fixtures/factories';
```

---

## Статические фикстуры

### JSON fixtures

```json
// tests/fixtures/static/users.json
{
  "validUser": {
    "id": "user-123",
    "email": "valid@example.com",
    "name": "Valid User",
    "role": "user"
  },
  "adminUser": {
    "id": "admin-456",
    "email": "admin@example.com",
    "name": "Admin User",
    "role": "admin"
  },
  "invalidUser": {
    "id": "",
    "email": "invalid-email",
    "name": ""
  }
}
```

### API response fixtures

```json
// tests/fixtures/static/api-responses/users-list.json
{
  "data": [
    { "id": "1", "email": "user1@example.com", "name": "User 1" },
    { "id": "2", "email": "user2@example.com", "name": "User 2" }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 2,
    "totalPages": 1
  }
}
```

### Загрузка fixtures

```typescript
// tests/fixtures/static/loader.ts
import { readFileSync } from 'fs';
import { join } from 'path';

export function loadFixture<T>(name: string): T {
  const path = join(__dirname, `${name}.json`);
  return JSON.parse(readFileSync(path, 'utf-8'));
}

// Использование
const users = loadFixture<UserFixtures>('users');
const response = loadFixture<ApiResponse>('api-responses/users-list');
```

---

## Seeds

### Seed файл

```typescript
// tests/fixtures/seeds/users.seed.ts
import { db } from '../../setup/database';
import { createUser, createAdmin } from '../factories';

export async function seedUsers() {
  // Очистка
  await db.query('TRUNCATE users CASCADE');

  // Создание тестовых пользователей
  const users = [
    createUser({ id: 'user-1', email: 'user1@example.com' }),
    createUser({ id: 'user-2', email: 'user2@example.com' }),
    createAdmin({ id: 'admin-1', email: 'admin@example.com' }),
  ];

  for (const user of users) {
    await db.query(
      'INSERT INTO users (id, email, name, role) VALUES ($1, $2, $3, $4)',
      [user.id, user.email, user.name, user.role]
    );
  }

  console.log(`Seeded ${users.length} users`);
  return users;
}
```

### Запуск seeds

```typescript
// tests/fixtures/seeds/run-seeds.ts
import { seedUsers } from './users.seed';
import { seedProducts } from './products.seed';
import { seedOrders } from './orders.seed';

async function runSeeds() {
  console.log('Starting seeds...');

  // Порядок важен (зависимости)
  await seedUsers();
  await seedProducts();
  await seedOrders();

  console.log('Seeds completed!');
}

runSeeds().catch(console.error);
```

```bash
# package.json
{
  "scripts": {
    "db:seed": "ts-node tests/fixtures/seeds/run-seeds.ts",
    "db:seed:test": "NODE_ENV=test npm run db:seed"
  }
}
```

---

## Примеры

### Пример 1: Unit тест с фабрикой

```typescript
// services/user.service.test.ts
import { createUser, createAdmin } from '../fixtures/factories';
import { UserService } from './user.service';

describe('UserService', () => {
  describe('canAccessAdminPanel', () => {
    it('should return true for admin', () => {
      const admin = createAdmin();
      expect(UserService.canAccessAdminPanel(admin)).toBe(true);
    });

    it('should return false for regular user', () => {
      const user = createUser({ role: 'user' });
      expect(UserService.canAccessAdminPanel(user)).toBe(false);
    });
  });
});
```

### Пример 2: Integration тест с seeds

```typescript
// tests/integration/orders.test.ts
import { seedUsers } from '../fixtures/seeds/users.seed';
import { createOrder } from '../fixtures/factories';

describe('Orders Integration', () => {
  beforeAll(async () => {
    await seedUsers(); // Создаём пользователей
  });

  it('should create order for existing user', async () => {
    const order = createOrder({
      user: { id: 'user-1' } as User // Используем seeded user
    });

    const result = await orderService.create(order);
    expect(result.id).toBeDefined();
  });
});
```

### Пример 3: E2E с API setup

```typescript
// tests/e2e/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { createUser, createProduct } from '../fixtures/factories';

test.describe('Checkout', () => {
  let testUser;
  let testProduct;

  test.beforeAll(async ({ request }) => {
    // Создаём данные через API
    testUser = createUser();
    const userRes = await request.post('/api/test/users', { data: testUser });
    testUser.id = (await userRes.json()).id;

    testProduct = createProduct({ price: 99.99 });
    const productRes = await request.post('/api/test/products', { data: testProduct });
    testProduct.id = (await productRes.json()).id;
  });

  test.afterAll(async ({ request }) => {
    // Cleanup
    await request.delete(`/api/test/users/${testUser.id}`);
    await request.delete(`/api/test/products/${testProduct.id}`);
  });

  test('should complete checkout', async ({ page }) => {
    // Тест использует созданные данные
    await page.goto(`/products/${testProduct.id}`);
    // ...
  });
});
```

---

## Антипаттерны

### 1. Глобальные fixtures

```typescript
// Плохо — один объект на все тесты
export const TEST_USER = { id: '1', email: 'test@example.com' };

// Хорошо — фабрика
export const createUser = () => ({ id: uuid(), email: faker.internet.email() });
```

### 2. Fixtures в БД без очистки

```typescript
// Плохо — данные накапливаются
beforeAll(async () => {
  await db.insert(testUser);
});
// afterAll отсутствует!

// Хорошо — cleanup
afterAll(async () => {
  await db.delete('users', { email: testUser.email });
});
```

### 3. Захардкоженные ID

```typescript
// Плохо — конфликт ID
const user = { id: '1', ... };

// Хорошо — уникальные ID
const user = createUser(); // ID генерируется
```

### 4. Слишком сложные fixtures

```typescript
// Плохо — fixture с бизнес-логикой
function createOrderWithDiscount() {
  const order = createOrder();
  order.discount = calculateDiscount(order); // Логика в fixture!
  return order;
}

// Хорошо — простые данные
function createOrder(overrides) {
  return {
    ...defaults,
    ...overrides,
  };
}
```

---

## Связанные инструкции

- [project-testing.md](./project-testing.md) — индекс тестирования
- [unit.md](./unit.md) — unit-тесты
- [integration.md](./integration.md) — интеграционные тесты
- [e2e.md](./e2e.md) — E2E тесты
