# Стандарт Example Technology

Пример per-tech стандарта — демонстрирует все 8 секций.

## 1. Версия и настройка

- **Технология:** Example Framework v1.0
- **Установка:** `npm install example-framework`
- **Конфигурация:** `example.config.ts` в корне проекта

## 2. Именование

| Объект | Конвенция | Пример |
|--------|-----------|--------|
| Файлы | kebab-case | `user-service.ts` |
| Классы | PascalCase | `UserService` |
| Переменные | camelCase | `userName` |
| Константы | SCREAMING_SNAKE | `MAX_RETRIES` |

## 3. Паттерны кода

### Repository Pattern

```typescript
class ExampleRepository {
  async findById(id: string): Promise<Example | null> {
    return this.db.example.findUnique({ where: { id } });
  }
}
```

## 4. Анти-паттерны

| Запрещено | Почему | Вместо этого |
|-----------|--------|-------------|
| `any` типы | Теряется типобезопасность | Использовать конкретные типы или generics |
| Бизнес-логика в routes | Нарушает SRP | Выносить в services/ |

## 5. Структура файлов

```
src/{svc}/backend/src/
├── routes/         # HTTP handlers
├── services/       # Business logic
├── repositories/   # Data access
├── types/          # TypeScript types
└── utils/          # Helpers
```

## 6. Валидация

```bash
# Запуск валидации (когда скрипт будет создан)
# python specs/.instructions/.scripts/validate-example-code.py
```

## 7. Тестирование

- **Фреймворк:** Jest
- **Конфигурация:** `jest.config.ts`
- **Фикстуры:** `tests/fixtures/`

```typescript
describe("ExampleService", () => {
  it("should create example", async () => {
    const result = await service.create({ title: "Test" });
    expect(result.id).toBeDefined();
  });
});
```

## 8. Логирование

```typescript
import { logger } from "@shared/logger";

logger.info("example.created", { id: example.id });
logger.error("example.creation_failed", { error: err.message });
```

**Уровни:** `error` > `warn` > `info` > `debug`

**Запрет PII:** Не логировать email, phone, password.
