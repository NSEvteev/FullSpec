---
type: standard
description: СТАНДАРТЫ unit-тестов для всего проекта (требования, метрики, naming)
related:
  - /.claude/instructions/tests/project-testing.md
  - /.claude/instructions/tests/integration.md
  - /.claude/instructions/tests/fixtures.md
  - /.claude/instructions/src/dev/testing.md
---

# Unit-тесты: Стандарты

Стандарты качества unit-тестов для всего проекта: требования, метрики покрытия, naming conventions.

> **Разделение ответственности:**
> - Этот файл: СТАНДАРТЫ unit-тестов для всего проекта (требования, метрики, naming)
> - [src/dev/testing.md](/.claude/instructions/src/dev/testing.md): КАК писать unit-тесты внутри сервиса (практика, примеры)

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

## Структура и Naming Conventions

### Стандарты именования файлов

| Язык | Паттерн | Пример |
|------|---------|--------|
| TypeScript/JavaScript | `*.test.ts` | `token.test.ts` |
| TypeScript/JavaScript | `*.spec.ts` | `token.spec.ts` |
| Python | `test_*.py` | `test_token.py` |
| Go | `*_test.go` | `token_test.go` |

### Стандарт структуры теста (AAA)

Все unit-тесты ДОЛЖНЫ следовать паттерну **Arrange-Act-Assert**:

```typescript
it('should {expected behavior} when {condition}', () => {
  // Arrange (подготовка)
  // ... setup test data and mocks

  // Act (действие)
  // ... execute the code under test

  // Assert (проверка)
  // ... verify the expected outcome
});
```

### Стандарт расположения

| Тип | Расположение |
|-----|--------------|
| Unit тесты сервиса | `/src/{service}/tests/unit/` |
| Системные unit тесты | `/tests/unit/{domain}/` |

> **Практика:** см. [src/dev/testing.md](/.claude/instructions/src/dev/testing.md) для примеров структуры папок

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

## Стандарты мокирования

### Классификация тестовых дублёров

| Тип | Назначение | Когда использовать |
|-----|------------|-------------------|
| **Mock** | Проверка взаимодействия | Нужно убедиться, что метод вызван с правильными аргументами |
| **Stub** | Подмена возвращаемого значения | Нужно контролировать ответ зависимости |
| **Spy** | Наблюдение без изменения | Нужно проверить вызов без изменения поведения |
| **Fake** | Упрощённая реализация | In-memory DB, локальный storage |

### Обязательные правила

1. **Мокать только внешние зависимости** — БД, API, файловая система, время
2. **НЕ мокать тестируемый модуль** — тестируем реальный код
3. **Сбрасывать моки между тестами** — изоляция обязательна
4. **Минимум моков** — чем больше моков, тем меньше уверенности в тесте
5. **Один мок = одна зависимость** — не объединять моки разных сервисов

### Запрещено

- Мокать приватные методы тестируемого класса
- Использовать глобальные моки без очистки
- Мокать стандартные библиотеки без необходимости

> **Примеры кода:** см. [src/dev/testing.md](/.claude/instructions/src/dev/testing.md)

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

## Примеры соответствия стандартам

> **Шаблон:** [/.claude/templates/tests/unit-test-example.ts](/.claude/templates/tests/unit-test-example.ts)

### Эталонный тест (соответствует всем стандартам)

```typescript
describe('TokenValidator', () => {
  // Стандарт: beforeEach для изоляции
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // Стандарт: describe для группировки по методу
  describe('validate', () => {
    // Стандарт: формат "should {behavior} when {condition}"
    it('should return true when token is valid', () => {
      // Arrange (AAA pattern)
      const token = 'valid-token';

      // Act
      const result = validator.validate(token);

      // Assert (один assert на тест)
      expect(result).toBe(true);
    });

    // Стандарт: edge cases в отдельных тестах
    it('should return false when token is empty', () => {
      expect(validator.validate('')).toBe(false);
    });

    it('should return false when token is null', () => {
      expect(validator.validate(null)).toBe(false);
    });
  });
});
```

> **Больше примеров:** см. [src/dev/testing.md](/.claude/instructions/src/dev/testing.md)

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

## Скиллы

Скиллы для автоматизации работы с unit-тестами:

| Скилл | Назначение |
|-------|------------|
| [/test-create](/.claude/skills/test-create/SKILL.md) | Создание нового unit-теста |
| [/test-update](/.claude/skills/test-update/SKILL.md) | Обновление существующего теста |
| [/test-execute](/.claude/skills/test-execute/SKILL.md) | Запуск тестов |
| [/test-review](/.claude/skills/test-review/SKILL.md) | Проверка качества теста |
| [/test-coverage](/.claude/skills/test-coverage/SKILL.md) | Анализ покрытия тестами |

---

## Связанные инструкции

| Инструкция | Содержание |
|------------|------------|
| [src/dev/testing.md](/.claude/instructions/src/dev/testing.md) | **КАК** писать тесты (практика, примеры) |
| [project-testing.md](./project-testing.md) | Индекс тестирования проекта |
| [integration.md](./integration.md) | Стандарты интеграционных тестов |
| [fixtures.md](./fixtures.md) | Стандарты тестовых данных |
