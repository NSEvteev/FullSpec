---
description: Стандарт кодирования TypeScript — конвенции именования, паттерны, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: typescript
---

# Стандарт TypeScript v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | TypeScript 5.x |
| Ключевые библиотеки | `typescript 5.x`, `ts-node 10.x`, `tsx 4.x` |
| Конфигурация | `tsconfig.json` в корне сервиса; `strict: true`, `target: "ES2022"`, `module: "NodeNext"` |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|-----------|--------|
| Файлы (модули) | kebab-case | `user-service.ts`, `auth-middleware.ts` |
| Файлы (компоненты React) | PascalCase | `UserCard.tsx`, `TaskList.tsx` |
| Классы | PascalCase | `UserService`, `TaskRepository` |
| Интерфейсы | PascalCase, без префикса `I` | `UserRepository`, `TaskPayload` |
| Type aliases | PascalCase | `UserId`, `TaskStatus` |
| Enums | PascalCase (имя), SCREAMING_SNAKE (значения) | `enum TaskStatus { IN_PROGRESS = "IN_PROGRESS" }` |
| Функции / методы | camelCase | `getUserById`, `createTask` |
| Переменные | camelCase | `userId`, `taskList` |
| Константы модульного уровня | SCREAMING_SNAKE | `MAX_RETRIES`, `DEFAULT_PAGE_SIZE` |
| React-компоненты | PascalCase | `TaskCard`, `UserAvatar` |
| React props-типы | PascalCase + `Props` суффикс | `TaskCardProps`, `UserAvatarProps` |
| Обобщённые параметры типов | T, TEntity, TResult (один символ или префикс T) | `function find<TEntity>(id: string): TEntity` |

## Паттерны кода

### Инициализация модуля (tsconfig.json)

Минимальная конфигурация для Node.js-сервиса с ESM и strict-режимом.

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Типизация данных — интерфейсы и type aliases

Использовать `interface` для расширяемых объектов (сущности, DTO). Использовать `type` для union-типов, utility-типов и псевдонимов примитивов.

```typescript
// Сущность домена
interface Task {
  readonly id: string;
  title: string;
  status: TaskStatus;
  assigneeId: string | null;
  createdAt: Date;
}

// Union-тип для статуса
type TaskStatus = "TODO" | "IN_PROGRESS" | "DONE";

// Псевдоним для Brand-типа (предотвращает перепутывание ID)
type TaskId = string & { readonly __brand: "TaskId" };
type UserId = string & { readonly __brand: "UserId" };

// DTO (входные данные API)
interface CreateTaskDto {
  title: string;
  assigneeId?: string;
}

// Partial update DTO — из интерфейса сущности
type UpdateTaskDto = Partial<Pick<Task, "title" | "status" | "assigneeId">>;
```

### Обработка ошибок — Result-паттерн

Использовать вместо `throw` для предсказуемых ошибок (бизнес-логика, валидация). `throw` оставлять для инфраструктурных ошибок (БД упала, сеть недоступна).

```typescript
// Определение Result-типа
type Result<T, E = Error> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly error: E };

// Фабрики для удобства
function ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

// Типы бизнес-ошибок
type TaskError =
  | { readonly code: "NOT_FOUND"; readonly id: string }
  | { readonly code: "ALREADY_DONE"; readonly taskId: string }
  | { readonly code: "VALIDATION_FAILED"; readonly field: string; readonly message: string };

// Использование в сервисе
async function completeTask(
  taskId: string,
  userId: string
): Promise<Result<Task, TaskError>> {
  const task = await taskRepository.findById(taskId);

  if (!task) {
    return err({ code: "NOT_FOUND", id: taskId });
  }

  if (task.status === "DONE") {
    return err({ code: "ALREADY_DONE", taskId });
  }

  const updated = await taskRepository.update(taskId, {
    status: "DONE",
    assigneeId: userId,
  });

  return ok(updated);
}

// Обработка на вызывающей стороне
const result = await completeTask(id, userId);
if (!result.ok) {
  switch (result.error.code) {
    case "NOT_FOUND":
      return res.status(404).json({ error: `Task ${result.error.id} not found` });
    case "ALREADY_DONE":
      return res.status(409).json({ error: "Task already completed" });
    case "VALIDATION_FAILED":
      return res.status(400).json({ error: result.error.message });
  }
}
```

### Async/await и обработка инфраструктурных ошибок

Инфраструктурные ошибки (сеть, БД) — пробрасывать через `throw`. Обрабатывать на границе (HTTP-обработчик, очередь событий).

```typescript
import { logger } from "@shared/logger";

// Сервисный слой — пробрасывает инфраструктурные ошибки
async function getUserById(id: string): Promise<User | null> {
  // Не оборачиваем в try/catch — пусть пробрасывается выше
  return userRepository.findById(id);
}

// HTTP-обработчик — граница обработки инфраструктурных ошибок
async function handleGetUser(req: Request, res: Response): Promise<void> {
  try {
    const user = await getUserById(req.params.id);
    if (!user) {
      res.status(404).json({ error: "User not found" });
      return;
    }
    res.json(user);
  } catch (error) {
    // Инфраструктурная ошибка: логируем и возвращаем 500
    logger.error("user.get_failed", {
      userId: req.params.id,
      error: error instanceof Error ? error.message : String(error),
    });
    res.status(500).json({ error: "Internal server error" });
  }
}
```

### Narrowing и type guards

Использовать type guards для безопасного сужения типов. Предпочитать `instanceof` и `in` оператор перед кастом `as`.

```typescript
// Discriminated union + exhaustive check
type Event =
  | { readonly type: "TASK_CREATED"; readonly taskId: string; readonly title: string }
  | { readonly type: "TASK_COMPLETED"; readonly taskId: string; readonly completedBy: string }
  | { readonly type: "USER_REGISTERED"; readonly userId: string; readonly email: string };

function handleEvent(event: Event): void {
  switch (event.type) {
    case "TASK_CREATED":
      // Здесь TypeScript знает: event.taskId и event.title доступны
      logger.info("task.created", { taskId: event.taskId });
      break;
    case "TASK_COMPLETED":
      logger.info("task.completed", { taskId: event.taskId, by: event.completedBy });
      break;
    case "USER_REGISTERED":
      logger.info("user.registered", { userId: event.userId });
      break;
    default: {
      // Exhaustive check — compile error если добавлен новый тип без обработки
      const _exhaustive: never = event;
      throw new Error(`Unknown event type: ${JSON.stringify(_exhaustive)}`);
    }
  }
}

// Пользовательский type guard
function isTaskError(error: unknown): error is TaskError {
  return (
    typeof error === "object" &&
    error !== null &&
    "code" in error &&
    typeof (error as Record<string, unknown>).code === "string"
  );
}
```

### Generics — типобезопасные утилиты

Использовать generics для переиспользуемых функций вместо `any`.

```typescript
// Пагинированный ответ — generic
interface PagedResult<T> {
  readonly items: T[];
  readonly total: number;
  readonly page: number;
  readonly pageSize: number;
}

// Generic repository-интерфейс
interface Repository<TEntity, TId = string> {
  findById(id: TId): Promise<TEntity | null>;
  findAll(options?: FindAllOptions): Promise<PagedResult<TEntity>>;
  create(data: Omit<TEntity, "id" | "createdAt">): Promise<TEntity>;
  update(id: TId, data: Partial<TEntity>): Promise<TEntity>;
  delete(id: TId): Promise<void>;
}

interface FindAllOptions {
  readonly page?: number;
  readonly pageSize?: number;
  readonly sortBy?: string;
  readonly sortOrder?: "asc" | "desc";
}

// Конкретная реализация
class TaskRepositoryImpl implements Repository<Task> {
  async findById(id: string): Promise<Task | null> {
    // реализация
    return null;
  }

  async findAll(options?: FindAllOptions): Promise<PagedResult<Task>> {
    const page = options?.page ?? 1;
    const pageSize = options?.pageSize ?? 20;
    // реализация
    return { items: [], total: 0, page, pageSize };
  }

  async create(data: Omit<Task, "id" | "createdAt">): Promise<Task> {
    // реализация
    throw new Error("Not implemented");
  }

  async update(id: string, data: Partial<Task>): Promise<Task> {
    // реализация
    throw new Error("Not implemented");
  }

  async delete(id: string): Promise<void> {
    // реализация
  }
}
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| `any` тип | Отключает проверку типов целиком — ошибки обнаруживаются только в runtime, а не при компиляции | Использовать `unknown` (требует narrowing) или конкретный тип; `as unknown as T` — только в крайнем случае |
| `as T` каст без проверки | Runtime-ошибка: компилятор не проверяет, реально ли объект соответствует `T` | Использовать type guard (`isT(x)`) или parse-функцию (zod `schema.parse`) |
| `!` non-null assertion | Маскирует возможный `null`/`undefined` — NPE в runtime | Использовать optional chaining `?.`, nullish coalescing `??`, или явную проверку `if (x == null)` |
| `interface IUserService` с префиксом `I` | Нарушает соглашение TypeScript-сообщества, создаёт избыточный шум | `interface UserService` без префикса |
| `enum` с числовыми значениями | Числовые enum не self-documenting и допускают присваивание произвольных чисел | String-enum: `enum Status { ACTIVE = "ACTIVE" }` или union-тип `type Status = "ACTIVE" \| "INACTIVE"` |
| `require()` в TypeScript | Обходит ES-модульную систему, теряется статический анализ | `import` / `import type` |
| `ts-ignore` без объяснения | Скрывает ошибки без понимания причины, накапливается технический долг | Если нужно — `@ts-expect-error` с комментарием причины |
| Мутабельные публичные поля класса | Нарушает инкапсуляцию, усложняет отслеживание изменений | `readonly` поля + методы-мутаторы с явной семантикой |
| `Promise<void>` без обработки (`fire and forget`) | Необработанный rejection не логируется, приложение молча теряет ошибки | `void asyncFn().catch(err => logger.error(...))` — явный catch |

## Структура файлов

```
src/{svc}/
├── backend/
│   └── src/
│       ├── index.ts               # Точка входа: инициализация, запуск HTTP-сервера
│       ├── routes/                # HTTP-обработчики (Express/Fastify routes)
│       │   └── tasks.ts           # Обработчики для /tasks эндпоинтов
│       ├── services/              # Бизнес-логика (use cases)
│       │   └── task-service.ts    # TaskService: createTask, completeTask, ...
│       ├── repositories/          # Доступ к данным (интерфейс + реализация)
│       │   ├── task-repository.ts # Интерфейс Repository<Task>
│       │   └── pg-task-repository.ts  # Реализация через PostgreSQL
│       ├── domain/                # Сущности, value objects, domain-ошибки
│       │   ├── task.ts            # interface Task, type TaskStatus, type TaskId
│       │   └── errors.ts          # type TaskError (discriminated union)
│       └── types/                 # Общие utility-типы, DTO
│           └── common.ts          # PagedResult<T>, Result<T,E>, FindAllOptions
└── tests/
    ├── unit/                      # Unit-тесты (мокируем зависимости)
    │   └── task-service.test.ts
    └── integration/               # Integration-тесты (реальная БД в Docker)
        └── task-repository.test.ts
```

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется вручную по чек-листу из [validation-technology.md](../../.instructions/docs/technology/validation-technology.md).*

Линтинг выполняется через ESLint с плагином `@typescript-eslint`:

```bash
npx eslint src --ext .ts,.tsx
npx tsc --noEmit   # Проверка типов без генерации файлов
```

Ключевые правила ESLint (`@typescript-eslint`):
- `no-explicit-any` — запрет `any`
- `no-non-null-assertion` — запрет `!`
- `strict-boolean-expressions` — явные boolean-выражения
- `no-floating-promises` — все Promise должны быть обработаны

## Тестирование

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| Фреймворк | `vitest 1.x` | Основной test runner (или `jest 29.x`) |
| Типизация Jest | `@types/jest 29.x` | TypeScript types для Jest (если используется Jest) |
| Мокирование | встроено в vitest / `jest.mock` | Моки, шпионы, фейки |
| Coverage | `@vitest/coverage-v8` | Покрытие кода |

### Фикстуры

```typescript
// tests/fixtures/task.ts
import type { Task } from "../../src/domain/task.ts";

export function makeTask(overrides: Partial<Task> = {}): Task {
  return {
    id: "task-001",
    title: "Test task",
    status: "TODO",
    assigneeId: null,
    createdAt: new Date("2026-01-01T00:00:00Z"),
    ...overrides,
  };
}

// Использование в тестах
const task = makeTask({ status: "IN_PROGRESS", assigneeId: "user-42" });
```

### Мокирование

Мокировать зависимости на уровне интерфейсов, не конкретных классов.
- **Unit-тесты:** мокируем repositories и внешние сервисы.
- **Integration-тесты:** реальная БД/инфраструктура в Docker — не мокируем.

```typescript
import { vi, type MockedObject } from "vitest";
import type { Repository } from "../../src/types/common.ts";
import type { Task } from "../../src/domain/task.ts";

// Фабрика мока репозитория
function makeTaskRepositoryMock(): MockedObject<Repository<Task>> {
  return {
    findById: vi.fn(),
    findAll: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  };
}

// Использование
const mockRepo = makeTaskRepositoryMock();
mockRepo.findById.mockResolvedValue(makeTask());
```

### Паттерны тестов

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { TaskService } from "../../src/services/task-service.ts";
import { makeTask } from "../fixtures/task.ts";

describe("TaskService.completeTask", () => {
  let service: TaskService;
  let mockRepo: ReturnType<typeof makeTaskRepositoryMock>;

  beforeEach(() => {
    mockRepo = makeTaskRepositoryMock();
    service = new TaskService(mockRepo);
  });

  it("returns ok with updated task when task exists and is not done", async () => {
    const task = makeTask({ status: "IN_PROGRESS" });
    const completedTask = makeTask({ status: "DONE", assigneeId: "user-1" });

    mockRepo.findById.mockResolvedValue(task);
    mockRepo.update.mockResolvedValue(completedTask);

    const result = await service.completeTask(task.id, "user-1");

    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.value.status).toBe("DONE");
    }
  });

  it("returns err NOT_FOUND when task does not exist", async () => {
    mockRepo.findById.mockResolvedValue(null);

    const result = await service.completeTask("nonexistent-id", "user-1");

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error.code).toBe("NOT_FOUND");
    }
  });

  it("returns err ALREADY_DONE when task status is DONE", async () => {
    mockRepo.findById.mockResolvedValue(makeTask({ status: "DONE" }));

    const result = await service.completeTask("task-001", "user-1");

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error.code).toBe("ALREADY_DONE");
    }
  });
});
```

## Логирование

TypeScript-код в этом проекте использует структурированный логгер `@shared/logger` (Winston или Pino под капотом). TypeScript обеспечивает типизацию контекста через перегрузки.

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| Успешное создание сущности | INFO | `task.created taskId=task-001 userId=user-42` |
| Обращение к сущности не нашло результат | DEBUG | `task.not_found taskId=task-001` |
| Бизнес-правило нарушено | WARNING | `task.complete_rejected reason=ALREADY_DONE taskId=task-001` |
| Инфраструктурная ошибка | ERROR | `task.repository_error operation=findById error="connection refused"` |
| Входящий HTTP-запрос | INFO | `http.request method=POST path=/tasks duration_ms=45` |

```typescript
// src/shared/logger.ts — типизированная обёртка
import pino from "pino";

const baseLogger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
});

export const logger = {
  debug(event: string, context?: Record<string, unknown>): void {
    baseLogger.debug({ ...context }, event);
  },
  info(event: string, context?: Record<string, unknown>): void {
    baseLogger.info({ ...context }, event);
  },
  warn(event: string, context?: Record<string, unknown>): void {
    baseLogger.warn({ ...context }, event);
  },
  error(event: string, context?: Record<string, unknown>): void {
    baseLogger.error({ ...context }, event);
  },
};

// Использование в коде сервиса
// logger.info("task.created", { taskId: task.id, userId });
// logger.error("task.repository_error", { operation: "findById", error: err.message });
```
