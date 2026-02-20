---
description: Стандарт кодирования Example Framework — конвенции именования, паттерны, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: example
---

# Стандарт Example Framework v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | Example Framework 1.0 |
| Ключевые библиотеки | — |
| Конфигурация | `example.config.ts` в корне проекта |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|-----------|--------|
| Файлы | kebab-case | `user-service.ts` |
| Классы | PascalCase | `UserService` |
| Переменные | camelCase | `userName` |
| Константы | SCREAMING_SNAKE | `MAX_RETRIES` |

## Паттерны кода

### Repository Pattern

Все операции с данными через Repository. Каждый агрегат — свой Repository.

```typescript
class ExampleRepository {
  async findById(id: string): Promise<Example | null> {
    return this.db.example.findUnique({ where: { id } });
  }
}
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|----------|-------------|
| `any` типы | Теряется типобезопасность | Использовать конкретные типы или generics |
| Бизнес-логика в routes | Нарушает SRP | Выносить в services/ |

## Структура файлов

```
src/{svc}/backend/src/
├── routes/         # HTTP handlers
├── services/       # Business logic
├── repositories/   # Data access
├── types/          # TypeScript types
└── utils/          # Helpers
```

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется вручную.*

## Тестирование

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| Фреймворк | `jest` | Основной test runner |
| Конфигурация | `jest.config.ts` | Настройка Jest |

### Фикстуры

```typescript
// tests/fixtures/example.ts
export const exampleFixture = {
  id: "ex-001",
  title: "Test Example",
  createdAt: new Date("2026-01-01"),
};
```

### Мокирование

- **Unit-тесты:** мокируем Repository целиком.
- **Integration-тесты:** реальная БД (Docker).

```typescript
const mockRepository = {
  findById: jest.fn().mockResolvedValue(exampleFixture),
};
```

### Паттерны тестов

```typescript
describe("ExampleService", () => {
  it("should create example", async () => {
    const result = await service.create({ title: "Test" });
    expect(result.id).toBeDefined();
  });
});
```

## Логирование

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| Создание | INFO | `example.created id=ex-001` |
| Ошибка создания | ERROR | `example.creation_failed error="validation failed"` |

```typescript
import { logger } from "@shared/logger";

logger.info("example.created", { id: example.id });
logger.error("example.creation_failed", { error: err.message });
```
