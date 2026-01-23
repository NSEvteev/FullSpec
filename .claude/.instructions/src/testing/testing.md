---
type: standard
description: КАК писать unit/integration тесты внутри сервисов (практика, инструменты, примеры)
related:
  - /.claude/.instructions/src/dev/local.md
  - /.claude/.instructions/tests/unit.md
  - /.claude/.instructions/tests/integration.md
  - /.claude/.instructions/tests/fixtures.md
  - /.claude/.instructions/tests/claude-testing.md
---

# Тестирование сервисов

Практическое руководство по написанию unit и integration тестов внутри сервисов (`/src/{service}/tests/`).

> **Разделение ответственности:**
> - Этот файл: КАК писать unit-тесты внутри сервиса (практика, инструменты, примеры)
> - [tests/unit.md](/.claude/.instructions/tests/unit.md): СТАНДАРТЫ unit-тестов для всего проекта (требования, метрики)

> **Полные инструкции по тестированию:** [/.claude/.instructions/tests/](/.claude/.instructions/tests/)
> **Тестирование Claude скиллов:** [/.claude/.instructions/tests/claude-testing.md](/.claude/.instructions/tests/claude-testing.md)

## Оглавление

- [Структура тестов](#структура-тестов)
- [Unit тесты](#unit-тесты)
- [Integration тесты](#integration-тесты)
- [Моки и стабы](#моки-и-стабы)
- [Покрытие кода](#покрытие-кода)
- [Запуск тестов](#запуск-тестов)
- [Best practices](#best-practices)
- [Связанные инструкции](#связанные-инструкции)

---

## Структура тестов

### Расположение

```
/src/{service}/
  /tests/
    /unit/                    ← unit тесты
      user.service.test.ts
      auth.utils.test.ts
    /integration/             ← integration тесты
      auth.api.test.ts
      database.test.ts
    /fixtures/                ← тестовые данные сервиса
      users.json
      tokens.json
    /mocks/                   ← моки внешних зависимостей
      external-api.mock.ts
    setup.ts                  ← глобальная настройка
    teardown.ts               ← очистка после тестов
```

### Именование файлов

| Тип | Паттерн | Пример |
|-----|---------|--------|
| Unit | `{module}.test.{ext}` | `user.service.test.ts` |
| Integration | `{module}.integration.test.{ext}` | `auth.api.integration.test.ts` |
| E2E (вне сервиса) | `{scenario}.e2e.test.{ext}` | `login-flow.e2e.test.ts` |

### Правило соседства

Тест должен находиться рядом с тестируемым кодом:

```
/src/auth/backend/v1/
  services/
    user.service.ts           ← код
  /tests/unit/
    user.service.test.ts      ← тест для этого кода
```

---

## Unit тесты

> **Стандарты и правила:** см. [tests/unit.md](/.claude/.instructions/tests/unit.md)

### Пример unit теста в сервисе

```typescript
// /src/auth/tests/unit/user.service.test.ts
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange (подготовка)
      const userData = { email: 'test@example.com', name: 'Test' };
      const mockRepo = { save: jest.fn().mockResolvedValue({ id: 1, ...userData }) };
      const service = new UserService(mockRepo);

      // Act (действие)
      const result = await service.createUser(userData);

      // Assert (проверка)
      expect(result.id).toBe(1);
      expect(result.email).toBe('test@example.com');
      expect(mockRepo.save).toHaveBeenCalledWith(userData);
    });
  });
});
```

### Что тестировать в сервисе

| Тестировать unit | Тестировать integration |
|------------------|------------------------|
| Бизнес-логика (сервисы) | Взаимодействие с БД |
| Утилиты и хелперы | HTTP запросы |
| Валидаторы | Файловая система |
| Трансформеры данных | Внешние API |
| Чистые функции | Очереди сообщений |

---

## Integration тесты

### Принципы

| Принцип | Описание |
|---------|----------|
| **Реальные зависимости** | БД, Redis, очереди — реальные (в Docker) |
| **Изоляция данных** | Каждый тест работает с чистой БД |
| **Транзакции** | Откат изменений после теста |

### Тестовая БД

```typescript
// setup.ts
import { testDb } from './test-db';

beforeAll(async () => {
  await testDb.connect();
  await testDb.migrate();
});

afterAll(async () => {
  await testDb.disconnect();
});

beforeEach(async () => {
  await testDb.truncateAll();  // очистка перед каждым тестом
});
```

### Пример integration теста

```typescript
describe('Auth API', () => {
  describe('POST /api/v1/auth/login', () => {
    it('should return JWT token for valid credentials', async () => {
      // Arrange: создать пользователя в тестовой БД
      await testDb.users.create({
        email: 'user@example.com',
        password: hashPassword('password123')
      });

      // Act: выполнить HTTP запрос
      const response = await request(app)
        .post('/api/v1/auth/login')
        .send({ email: 'user@example.com', password: 'password123' });

      // Assert
      expect(response.status).toBe(200);
      expect(response.body.token).toBeDefined();
      expect(response.body.token).toMatch(/^eyJ/);  // JWT формат
    });
  });
});
```

### Docker для тестов

```yaml
# docker-compose.test.yml
services:
  test-db:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    ports:
      - "5433:5432"  # другой порт, чтобы не конфликтовать с dev

  test-redis:
    image: redis:7
    ports:
      - "6380:6379"
```

---

## Моки и стабы

### Когда использовать

| Ситуация | Инструмент |
|----------|------------|
| Внешний API | Mock (имитация ответа) |
| Зависимость сервиса | Stub (заглушка) |
| Проверка вызовов | Spy (шпион) |
| Время/дата | Fake (контролируемое значение) |

### Примеры моков

**Mock внешнего API:**

```typescript
// mocks/payment-gateway.mock.ts
export const mockPaymentGateway = {
  charge: jest.fn().mockResolvedValue({
    transactionId: 'txn_123',
    status: 'success'
  }),
  refund: jest.fn().mockResolvedValue({ status: 'refunded' })
};

// В тесте
jest.mock('../services/payment-gateway', () => mockPaymentGateway);
```

**Stub репозитория:**

```typescript
const stubUserRepo = {
  findById: async (id: string) => ({ id, name: 'Test User' }),
  save: async (user: User) => ({ ...user, id: 'generated-id' })
};
```

**Spy для проверки вызовов:**

```typescript
const emailSpy = jest.spyOn(emailService, 'send');

await userService.register(userData);

expect(emailSpy).toHaveBeenCalledWith({
  to: userData.email,
  template: 'welcome'
});
```

### Библиотеки для моков

| Язык | Библиотека |
|------|------------|
| TypeScript/JavaScript | Jest, Sinon, nock (HTTP) |
| Python | unittest.mock, pytest-mock, responses |
| Go | gomock, testify/mock |

---

## Покрытие кода

### Целевые показатели

| Метрика | Минимум | Рекомендуемо |
|---------|---------|--------------|
| Lines | 70% | 80% |
| Branches | 60% | 70% |
| Functions | 70% | 80% |
| Statements | 70% | 80% |

### Настройка (Jest)

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      lines: 70,
      branches: 60,
      functions: 70,
      statements: 70
    }
  },
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/**/*.mock.ts'
  ]
};
```

### Исключения из покрытия

- Файлы конфигурации
- Индексные файлы (re-exports)
- Моки и фикстуры
- Сгенерированный код
- Миграции БД

---

## Запуск тестов

### Makefile команды

```makefile
# Все тесты сервиса
test-auth:
	cd src/auth && npm test

# Только unit
test-auth-unit:
	cd src/auth && npm run test:unit

# Только integration
test-auth-integration:
	cd src/auth && npm run test:integration

# С покрытием
test-auth-coverage:
	cd src/auth && npm run test:coverage

# Watch mode (для разработки)
test-auth-watch:
	cd src/auth && npm run test:watch
```

### Скрипты в package.json

```json
{
  "scripts": {
    "test": "jest",
    "test:unit": "jest --testPathPattern=unit",
    "test:integration": "jest --testPathPattern=integration",
    "test:coverage": "jest --coverage",
    "test:watch": "jest --watch",
    "test:ci": "jest --ci --coverage --reporters=default --reporters=jest-junit"
  }
}
```

### CI интеграция

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:ci
      - uses: codecov/codecov-action@v3
```

---

## Best practices в сервисах

> **Полные правила и антипаттерны:** см. [tests/unit.md](/.claude/.instructions/tests/unit.md)

### Использовать фабрики для тестовых данных

```typescript
// /src/auth/tests/factories/user.factory.ts
export const createTestUser = (overrides = {}) => ({
  id: 'user-123',
  email: 'test@example.com',
  name: 'Test User',
  createdAt: new Date('2024-01-01'),
  ...overrides
});

// В тесте
const user = createTestUser({ name: 'Custom Name' });
```

### Тестировать граничные случаи

- Пустые значения (null, undefined, '')
- Граничные значения (0, -1, MAX_INT)
- Невалидные входные данные
- Ошибки и исключения
- Таймауты

---

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/test-create](/.claude/skills/test-create/SKILL.md) | Создание теста |
| [/test-update](/.claude/skills/test-update/SKILL.md) | Обновление теста |
| [/test-execute](/.claude/skills/test-execute/SKILL.md) | Запуск тестов |
| [/test-review](/.claude/skills/test-review/SKILL.md) | Ревью теста |
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование тестов |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок |

---

## Связанные инструкции

- [local.md](./local.md) — локальная разработка
- [unit.md](/.claude/.instructions/tests/unit.md) — детали unit тестов
- [integration.md](/.claude/.instructions/tests/integration.md) — детали integration тестов
- [fixtures.md](/.claude/.instructions/tests/fixtures.md) — тестовые данные
