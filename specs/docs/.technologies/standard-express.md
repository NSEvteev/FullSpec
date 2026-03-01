---
description: Стандарт кодирования Express — конвенции именования, паттерны, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: express
---

# Стандарт Express v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | Express 4.x |
| Ключевые библиотеки | zod 3.x (валидация), morgan 1.x (HTTP logging), helmet 7.x (security headers), cors 2.x (CORS); JWT: `jose 5.x` (рекомендуется в production, см. [standard-jose.md](./standard-jose.md)), `jsonwebtoken 9.x` (упрощение — используется в примерах этого документа) |
| Конфигурация | `src/{svc}/backend/src/app.ts` — инициализация приложения; `src/{svc}/backend/src/config/index.ts` — переменные окружения |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|-----------|--------|
| Файлы роутов | kebab-case, суффикс `.routes.ts` | `user-tasks.routes.ts` |
| Файлы обработчиков | kebab-case, суффикс `.handler.ts` | `create-task.handler.ts` |
| Файлы middleware | kebab-case, суффикс `.middleware.ts` | `auth.middleware.ts` |
| Файлы Zod-схем | kebab-case, суффикс `.schema.ts` | `create-task.schema.ts` |
| Zod-схемы (объекты) | PascalCase + суффикс `Schema` | `CreateTaskSchema` |
| Zod-типы (выведенные) | PascalCase | `CreateTaskInput` |
| Функции-обработчики | camelCase, глагол + существительное | `createTask`, `listTasks`, `getTaskById` |
| Middleware-функции | camelCase, описание действия | `requireAuth`, `validateBody`, `parseJsonBody` |
| Express Router | camelCase, суффикс `Router` | `tasksRouter`, `authRouter` |
| Переменные окружения | SCREAMING_SNAKE_CASE | `PORT`, `DATABASE_URL`, `JWT_SECRET` |

## Паттерны кода

### Инициализация приложения

Создавать Express-приложение в отдельном файле `app.ts`. Точка входа `server.ts` только запускает сервер. Это упрощает тестирование без запуска HTTP.

```typescript
// src/{svc}/backend/src/app.ts
import express, { Application } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import morgan from 'morgan';
import { tasksRouter } from './routes/tasks.routes';
import { errorHandler } from './middleware/error.middleware';

export function createApp(): Application {
  const app = express();

  // Security middleware
  app.use(helmet());
  app.use(cors({ origin: process.env.CORS_ORIGIN ?? '*' }));

  // Parsing middleware
  app.use(express.json({ limit: '1mb' }));
  app.use(express.urlencoded({ extended: false }));

  // Logging
  app.use(morgan('combined'));

  // Routes
  app.use('/api/tasks', tasksRouter);

  // Global error handler — должен быть последним
  app.use(errorHandler);

  return app;
}
```

```typescript
// src/{svc}/backend/src/server.ts
import { createApp } from './app';

const PORT = Number(process.env.PORT ?? 3000);
const app = createApp();

app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
});
```

### Zod-валидация входных данных

Все входные данные (body, query, params) валидировать через Zod. Схемы — в отдельных файлах `*.schema.ts`. Использовать `safeParse` для явной обработки ошибок.

```typescript
// src/{svc}/backend/src/schemas/create-task.schema.ts
import { z } from 'zod';

export const CreateTaskSchema = z.object({
  title: z.string().min(1).max(255),
  description: z.string().max(2000).optional(),
  priority: z.enum(['low', 'medium', 'high']).default('medium'),
  dueDate: z.string().datetime().optional(),
});

export type CreateTaskInput = z.infer<typeof CreateTaskSchema>;
```

```typescript
// src/{svc}/backend/src/middleware/validate.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { ZodSchema, ZodError } from 'zod';

export function validateBody<T>(schema: ZodSchema<T>) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      res.status(400).json({
        error: 'Validation failed',
        details: result.error.flatten().fieldErrors,
      });
      return;
    }
    req.body = result.data;
    next();
  };
}
```

### Роутер и обработчики

Каждый домен — отдельный Router. Обработчики-функции получают типизированные данные после валидации middleware.

```typescript
// src/{svc}/backend/src/routes/tasks.routes.ts
import { Router } from 'express';
import { requireAuth } from '../middleware/auth.middleware';
import { validateBody } from '../middleware/validate.middleware';
import { CreateTaskSchema } from '../schemas/create-task.schema';
import { createTask, getTask, listTasks, deleteTask } from '../handlers/tasks.handler';

export const tasksRouter = Router();

tasksRouter.use(requireAuth);

tasksRouter.get('/', listTasks);
tasksRouter.post('/', validateBody(CreateTaskSchema), createTask);
tasksRouter.get('/:id', getTask);
tasksRouter.delete('/:id', deleteTask);
```

```typescript
// src/{svc}/backend/src/handlers/tasks.handler.ts
import { Request, Response, NextFunction } from 'express';
import { CreateTaskInput } from '../schemas/create-task.schema';
import { TaskService } from '../services/task.service';

const taskService = new TaskService();

export async function createTask(
  req: Request<{}, {}, CreateTaskInput>,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const task = await taskService.create(req.body, req.user.id);
    res.status(201).json(task);
  } catch (err) {
    next(err);
  }
}

export async function listTasks(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const tasks = await taskService.listByUser(req.user.id);
    res.json({ items: tasks, total: tasks.length });
  } catch (err) {
    next(err);
  }
}

export async function getTask(
  req: Request<{ id: string }>,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const task = await taskService.getById(req.params.id, req.user.id);
    if (!task) {
      res.status(404).json({ error: 'Task not found' });
      return;
    }
    res.json(task);
  } catch (err) {
    next(err);
  }
}

export async function deleteTask(
  req: Request<{ id: string }>,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    await taskService.delete(req.params.id, req.user.id);
    res.status(204).send();
  } catch (err) {
    next(err);
  }
}
```

### Обработка ошибок

Централизованный error handler — последний middleware в цепочке. Все ошибки из обработчиков передаются через `next(err)`. Выделять собственные классы ошибок с HTTP-статусом.

```typescript
// src/{svc}/backend/src/errors/app.errors.ts
export class AppError extends Error {
  constructor(
    public readonly statusCode: number,
    message: string,
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, `${resource} not found`);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(403, message);
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(409, message);
  }
}
```

```typescript
// src/{svc}/backend/src/middleware/error.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../errors/app.errors';
import { logger } from '../logger';

export function errorHandler(
  err: unknown,
  req: Request,
  res: Response,
  _next: NextFunction,
): void {
  if (err instanceof AppError) {
    res.status(err.statusCode).json({ error: err.message });
    return;
  }

  logger.error('Unhandled error', {
    error: err instanceof Error ? err.message : String(err),
    path: req.path,
    method: req.method,
  });

  res.status(500).json({ error: 'Internal server error' });
}
```

### Auth middleware

Middleware для проверки JWT-токена. Расширяет `Request` через declaration merging для типизации `req.user`.

`req.user` объявлен как non-optional тип — это сознательное решение: обработчики за `requireAuth`-middleware всегда имеют `req.user`. Для маршрутов без аутентификации использовать `req.user?` в конкретном обработчике или assertion-хелпер.

```typescript
// src/{svc}/backend/src/types/express.d.ts
import 'express';

// req.user — non-optional: гарантируется middleware requireAuth.
// Используется сознательно: TypeScript не должен требовать null-check
// в каждом обработчике за requireAuth.
declare module 'express' {
  interface Request {
    user: {
      id: string;
      email: string;
    };
  }
}
```

```typescript
// src/{svc}/backend/src/middleware/assert-user.ts
// Assertion-хелпер для редких случаев, когда req.user может отсутствовать
// (например, публичные маршруты, шаренные обработчики).
import { Request } from 'express';

export function assertUser(req: Request): asserts req is Request & { user: NonNullable<Request['user']> } {
  if (!req.user) {
    throw new Error('req.user is undefined — маршрут не защищён requireAuth');
  }
}
```

```typescript
// src/{svc}/backend/src/middleware/auth.middleware.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET ?? '';

export function requireAuth(req: Request, res: Response, next: NextFunction): void {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    res.status(401).json({ error: 'Unauthorized' });
    return;
  }

  const token = authHeader.slice(7);
  try {
    const payload = jwt.verify(token, JWT_SECRET) as { sub: string; email: string };
    req.user = { id: payload.sub, email: payload.email };
    next();
  } catch {
    res.status(401).json({ error: 'Invalid or expired token' });
  }
}
```

> **Примечание:** В примере выше используется `jsonwebtoken` — синхронный API, приемлемый для простых однозначных сценариев. В production-сервисах рекомендуется `jose 5.x` (async, поддержка RS256/ES256, JWKS, Web Crypto API). Готовый production-вариант middleware с `jose` — в [standard-jose.md](./standard-jose.md). `jsonwebtoken` здесь — упрощение для иллюстрации структуры middleware.

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| Бизнес-логика в обработчике route | Нарушает SRP — handler становится нетестируемым монолитом, любое изменение логики требует менять тест HTTP-слоя | Вынести в `services/` — handler только вызывает service и формирует HTTP-ответ |
| Отсутствие валидации входных данных | Runtime crash при обращении к `req.body.field`, возможны injection-атаки или unexpected behavior | Всегда использовать Zod-схему через `validateBody()` middleware до обработчика |
| `next(err)` не вызывается при async-ошибке | Ошибка замалчивается, запрос зависает (таймаут клиента), невозможно централизованно обработать | Оборачивать async-обработчики в try/catch и передавать ошибку через `next(err)` |
| Глобальный `app.use(errorHandler)` не последний | Ошибки из роутов, зарегистрированных после, не попадают в централизованный handler | Регистрировать `errorHandler` после всех роутов |
| `req.body as SomeType` без валидации | Нет runtime-проверки — приходящие данные не совпадают с типом, TypeScript молчит о runtime | Использовать `z.infer<typeof Schema>` вместе с `safeParse` или `parse` |
| Хранение секретов в коде | Security hole — секрет попадает в git-историю | Использовать `process.env`, добавлять в `.gitignore`, шаблон — `.env.example` |
| Синхронный код в обработчике без оборачивания | Синхронное исключение разрушает процесс Node.js при отсутствии `uncaughtException` handler | Использовать async/await + try/catch или синхронный try/catch с вызовом `next(err)` |
| Возврат `res.send()` без `return` | Express выдаёт предупреждение `Cannot set headers after they are sent` из-за двойной отправки ответа | Всегда писать `return` перед ранним выходом: `return res.status(404).json(...)` |

## Структура файлов

```
src/{svc}/backend/src/
├── app.ts                  # Фабрика Express-приложения (createApp)
├── server.ts               # Точка входа: запуск HTTP-сервера
├── config/
│   └── index.ts            # Переменные окружения с типизацией
├── errors/
│   └── app.errors.ts       # Кастомные классы ошибок с statusCode
├── handlers/
│   └── tasks.handler.ts    # HTTP-обработчики (тонкий слой — вызов service)
├── middleware/
│   ├── auth.middleware.ts  # JWT-аутентификация
│   ├── error.middleware.ts # Централизованная обработка ошибок
│   └── validate.middleware.ts # Фабрика validateBody(schema)
├── routes/
│   └── tasks.routes.ts     # Роутеры Express (Router())
├── schemas/
│   └── create-task.schema.ts # Zod-схемы и выведенные типы
├── services/
│   └── task.service.ts     # Бизнес-логика
├── types/
│   └── express.d.ts        # Declaration merging для req.user
└── logger.ts               # Настройка логгера
```

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется вручную по чек-листу из [validation-technology.md](../../.instructions/docs/technology/validation-technology.md).*

## Тестирование

Тесты Express-приложения разделяются на unit (мок service-слоя) и integration (реальный HTTP через supertest). Тесты middleware проверяются изолированно — без запуска полного приложения.

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| Фреймворк | `jest 29.x` + `ts-jest` | Test runner с TypeScript |
| HTTP-тестирование | `supertest 6.x` | Запросы к Express-приложению без запуска сервера |
| Типы | `@types/supertest` | TypeScript-типы для supertest |
| Мокирование | `jest.fn()` / `jest.mock()` | Мокирование service-слоя |

### Фикстуры

```typescript
// src/{svc}/backend/tests/fixtures/task.fixture.ts
import { CreateTaskInput } from '../../src/schemas/create-task.schema';

export const createTaskInput: CreateTaskInput = {
  title: 'Test task',
  description: 'Test description',
  priority: 'medium',
};

export const taskResponse = {
  id: 'task-001',
  ...createTaskInput,
  userId: 'user-001',
  createdAt: '2026-01-01T00:00:00.000Z',
};

export const mockUser = { id: 'user-001', email: 'test@example.com' };
```

### Мокирование

- **Unit-тесты обработчиков:** мокируем весь service-класс через `jest.mock()` — тестируем только HTTP-логику (статус, заголовки, формат ответа).
- **Integration-тесты:** используем supertest с реальным `createApp()`, но мокируем зависимости БД на уровне repository.
- **Middleware:** тестируем изолированно, передавая мок `req`, `res`, `next`.

```typescript
// src/{svc}/backend/tests/unit/handlers/tasks.handler.test.ts
import { TaskService } from '../../../src/services/task.service';

// Мок всего модуля service
jest.mock('../../../src/services/task.service');
const MockTaskService = TaskService as jest.MockedClass<typeof TaskService>;

beforeEach(() => {
  MockTaskService.mockClear();
});
```

### Паттерны тестов

```typescript
// src/{svc}/backend/tests/integration/tasks.test.ts
import request from 'supertest';
import { createApp } from '../../src/app';
import { TaskService } from '../../src/services/task.service';
import { taskResponse, createTaskInput, mockUser } from '../fixtures/task.fixture';

jest.mock('../../src/services/task.service');
jest.mock('../../src/middleware/auth.middleware', () => ({
  requireAuth: (req: any, _res: any, next: any) => {
    req.user = mockUser;
    next();
  },
}));

describe('POST /api/tasks', () => {
  let app: ReturnType<typeof createApp>;

  beforeEach(() => {
    app = createApp();
    (TaskService.prototype.create as jest.Mock).mockResolvedValue(taskResponse);
  });

  it('returns 201 with created task', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .send(createTaskInput)
      .set('Authorization', 'Bearer test-token');

    expect(res.status).toBe(201);
    expect(res.body.id).toBe('task-001');
    expect(res.body.title).toBe('Test task');
  });

  it('returns 400 for invalid body', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .send({ title: '' })
      .set('Authorization', 'Bearer test-token');

    expect(res.status).toBe(400);
    expect(res.body.error).toBe('Validation failed');
  });
});

// Тест middleware в изоляции
describe('validateBody middleware', () => {
  it('calls next with parsed data when valid', () => {
    const { validateBody } = require('../../src/middleware/validate.middleware');
    const { CreateTaskSchema } = require('../../src/schemas/create-task.schema');

    const req = { body: createTaskInput } as any;
    const res = { status: jest.fn().mockReturnThis(), json: jest.fn() } as any;
    const next = jest.fn();

    validateBody(CreateTaskSchema)(req, res, next);

    expect(next).toHaveBeenCalledWith();
    expect(req.body.priority).toBe('medium');
  });
});
```

## Логирование

Express-приложения используют morgan для HTTP access log и структурированный логгер (например, pino или winston) для логирования бизнес-событий. Morgan настраивается в `createApp()`, прикладной логгер — в `logger.ts`.

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| HTTP-запрос (morgan) | INFO | `POST /api/tasks 201 45ms` |
| Необработанная ошибка | ERROR | `express.unhandled_error path="/api/tasks" method="POST" error="TaskService: DB timeout"` |
| Запуск сервера | INFO | `express.server_started port=3000 env="production"` |
| Ошибка валидации | DEBUG | `express.validation_failed path="/api/tasks" fields=["title"]` |
| 404 Not Found | DEBUG | `express.route_not_found path="/api/unknown" method="GET"` |

```typescript
// src/{svc}/backend/src/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  // В production — JSON; в development — читаемый вывод
  transport: process.env.NODE_ENV !== 'production'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,
});
```
