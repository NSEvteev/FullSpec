---
type: standard
description: Unit-тесты: изоляция, моки, покрытие
related:
  - tests/project-testing.md
  - tests/integration.md
  - tests/fixtures.md
  - src/dev/testing.md
---

# Unit-тесты

Правила написания unit-тестов для изолированного тестирования отдельных модулей.

## Оглавление

- [Принципы](#принципы)
- [Структура](#структура)
- [Правила](#правила)
- [Моки и стабы](#моки-и-стабы)
- [Покрытие кода](#покрытие-кода)
- [Примеры](#примеры)
- [Антипаттерны](#антипаттерны)
- [Связанные инструкции](#связанные-инструкции)

---

## Принципы

### FIRST

| Принцип | Описание |
|---------|----------|
| **F**ast | Быстрые — миллисекунды на тест |
| **I**solated | Изолированные — не зависят от других тестов |
| **R**epeatable | Повторяемые — одинаковый результат при каждом запуске |
| **S**elf-validating | Самопроверяющиеся — pass/fail без ручной проверки |
| **T**imely | Своевременные — пишутся вместе с кодом |

### Что тестировать unit-тестами

| Тестировать | Не тестировать |
|-------------|----------------|
| Бизнес-логика | Внешние сервисы (мокать) |
| Чистые функции | БД напрямую (integration) |
| Валидаторы | UI-взаимодействия (e2e) |
| Трансформации данных | Приватные методы |
| Edge cases | Конфигурации |

---

## Структура

### Расположение файлов

```
/src/auth/
  /backend/
    token.ts
    token.test.ts       ← co-located с кодом
  /tests/
    token.spec.ts       ← альтернатива: отдельная папка

/tests/unit/
  /auth/
    token.test.ts       ← системные unit-тесты
```

**Правило:** Co-located тесты предпочтительны (рядом с кодом).

### Именование файлов

| Паттерн | Пример |
|---------|--------|
| `*.test.ts` | `token.test.ts` |
| `*.spec.ts` | `token.spec.ts` |
| `test_*.py` | `test_token.py` |

### Структура теста (AAA)

```typescript
describe('TokenService', () => {
  describe('validate', () => {
    it('should return true for valid token', () => {
      // Arrange (подготовка)
      const token = createValidToken();
      const service = new TokenService();

      // Act (действие)
      const result = service.validate(token);

      // Assert (проверка)
      expect(result).toBe(true);
    });
  });
});
```

---

## Правила

### 1. Один тест — одна проверка

```typescript
// Плохо — много проверок
it('should validate token', () => {
  expect(service.validate(validToken)).toBe(true);
  expect(service.validate(expiredToken)).toBe(false);
  expect(service.validate(null)).toBe(false);
});

// Хорошо — отдельные тесты
it('should return true for valid token', () => {
  expect(service.validate(validToken)).toBe(true);
});

it('should return false for expired token', () => {
  expect(service.validate(expiredToken)).toBe(false);
});

it('should return false for null token', () => {
  expect(service.validate(null)).toBe(false);
});
```

### 2. Понятные названия тестов

**Формат:** `should {ожидаемое поведение} when {условие}`

```typescript
// Плохо
it('test token', () => {});
it('works', () => {});

// Хорошо
it('should throw ValidationError when token is expired', () => {});
it('should return user id when token is valid', () => {});
```

### 3. Изоляция от внешних зависимостей

```typescript
// Плохо — реальный HTTP запрос
const response = await fetch('/api/users');

// Хорошо — мок
const mockFetch = jest.fn().mockResolvedValue({ data: [] });
const response = await mockFetch('/api/users');
```

### 4. Не тестировать приватные методы

```typescript
class Calculator {
  private validate(n: number): boolean { ... }

  public calculate(n: number): number {
    if (!this.validate(n)) throw new Error();
    return n * 2;
  }
}

// Плохо — тестируем приватный метод
it('validate should return false for negative', () => {
  expect(calculator['validate'](-1)).toBe(false);
});

// Хорошо — тестируем через публичный интерфейс
it('should throw when number is negative', () => {
  expect(() => calculator.calculate(-1)).toThrow();
});
```

### 5. Детерминированность

```typescript
// Плохо — зависит от времени
it('should check expiration', () => {
  const token = { exp: Date.now() + 1000 };
  expect(isExpired(token)).toBe(false);
});

// Хорошо — фиксированное время
it('should check expiration', () => {
  jest.useFakeTimers().setSystemTime(new Date('2024-01-15'));
  const token = { exp: new Date('2024-01-16').getTime() };
  expect(isExpired(token)).toBe(false);
});
```

---

## Моки и стабы

### Когда использовать

| Тип | Когда | Пример |
|-----|-------|--------|
| **Mock** | Проверка вызова | `expect(mock).toHaveBeenCalledWith(...)` |
| **Stub** | Подмена возвращаемого значения | `stub.returns(fixedValue)` |
| **Spy** | Наблюдение без изменения | `spy.on(object, 'method')` |
| **Fake** | Упрощённая реализация | In-memory DB вместо реальной |

### Примеры

```typescript
// Mock — проверяем, что метод вызван
const emailService = { send: jest.fn() };
await userService.register(user);
expect(emailService.send).toHaveBeenCalledWith(user.email);

// Stub — подменяем возвращаемое значение
const userRepo = { findById: jest.fn().mockResolvedValue(mockUser) };
const result = await userService.getUser('123');
expect(result).toEqual(mockUser);

// Spy — наблюдаем за реальным методом
const spy = jest.spyOn(console, 'log');
logger.info('test');
expect(spy).toHaveBeenCalled();
```

### Правила мокирования

1. **Мокать только внешние зависимости** — БД, API, файловая система
2. **Не мокать тестируемый модуль** — тестируем реальный код
3. **Сбрасывать моки между тестами** — `beforeEach(() => jest.clearAllMocks())`
4. **Минимум моков** — чем больше моков, тем меньше уверенности

---

## Покрытие кода

### Целевые показатели

| Тип кода | Coverage | Обоснование |
|----------|:--------:|-------------|
| Бизнес-логика | **80%+** | Критично для стабильности |
| Утилиты | **90%+** | Простой код, легко покрыть |
| API handlers | **70%+** | Включая error cases |
| UI компоненты | **60%+** | Сложно тестировать |

### Команды

```bash
# Генерация отчёта
npm test -- --coverage

# Проверка порогов
npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'
```

### Что покрывать обязательно

- Happy path (основной сценарий)
- Edge cases (граничные случаи)
- Error handling (обработка ошибок)
- Null/undefined inputs

### Что можно пропустить

- Геттеры/сеттеры без логики
- Делегирующие методы
- Конфигурации
- Типы и интерфейсы

---

## Примеры

### Пример 1: Тест валидатора

```typescript
// validators/email.ts
export function isValidEmail(email: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// validators/email.test.ts
describe('isValidEmail', () => {
  it('should return true for valid email', () => {
    expect(isValidEmail('user@example.com')).toBe(true);
  });

  it('should return false for email without @', () => {
    expect(isValidEmail('userexample.com')).toBe(false);
  });

  it('should return false for empty string', () => {
    expect(isValidEmail('')).toBe(false);
  });

  it('should return false for email with spaces', () => {
    expect(isValidEmail('user @example.com')).toBe(false);
  });
});
```

### Пример 2: Тест сервиса с моками

```typescript
// services/user.service.ts
export class UserService {
  constructor(private repo: UserRepository, private email: EmailService) {}

  async register(data: CreateUserDto): Promise<User> {
    const user = await this.repo.create(data);
    await this.email.sendWelcome(user.email);
    return user;
  }
}

// services/user.service.test.ts
describe('UserService', () => {
  let service: UserService;
  let mockRepo: jest.Mocked<UserRepository>;
  let mockEmail: jest.Mocked<EmailService>;

  beforeEach(() => {
    mockRepo = { create: jest.fn() };
    mockEmail = { sendWelcome: jest.fn() };
    service = new UserService(mockRepo, mockEmail);
  });

  describe('register', () => {
    it('should create user and send welcome email', async () => {
      const userData = { email: 'test@example.com', name: 'Test' };
      const createdUser = { id: '1', ...userData };
      mockRepo.create.mockResolvedValue(createdUser);

      const result = await service.register(userData);

      expect(mockRepo.create).toHaveBeenCalledWith(userData);
      expect(mockEmail.sendWelcome).toHaveBeenCalledWith(userData.email);
      expect(result).toEqual(createdUser);
    });

    it('should not send email if user creation fails', async () => {
      mockRepo.create.mockRejectedValue(new Error('DB error'));

      await expect(service.register({})).rejects.toThrow('DB error');
      expect(mockEmail.sendWelcome).not.toHaveBeenCalled();
    });
  });
});
```

---

## Антипаттерны

### 1. Тест знает слишком много о реализации

```typescript
// Плохо — проверяем внутреннюю структуру
expect(service._cache.size).toBe(1);

// Хорошо — проверяем поведение
expect(service.get('key')).toBe('value');
```

### 2. Shared state между тестами

```typescript
// Плохо — тесты влияют друг на друга
let counter = 0;
it('test 1', () => { counter++; });
it('test 2', () => { expect(counter).toBe(0); }); // Fail!

// Хорошо — изоляция
beforeEach(() => { counter = 0; });
```

### 3. Слишком много моков

```typescript
// Плохо — мокаем всё
const result = await service.process(
  mockInput, mockConfig, mockLogger, mockCache, mockDb
);
// Что вообще тестируем?

// Хорошо — мокаем только внешнее
const result = await service.process(realInput, { db: mockDb });
```

### 4. Тесты без assertions

```typescript
// Плохо — тест ничего не проверяет
it('should work', async () => {
  await service.process(data);
  // ???
});

// Хорошо
it('should return processed data', async () => {
  const result = await service.process(data);
  expect(result.status).toBe('processed');
});
```

---

## Связанные инструкции

- [project-testing.md](./project-testing.md) — индекс тестирования проекта
- [integration.md](./integration.md) — интеграционные тесты
- [fixtures.md](./fixtures.md) — тестовые данные
- [src/dev/testing.md](../src/dev/testing.md) — тесты внутри сервисов
