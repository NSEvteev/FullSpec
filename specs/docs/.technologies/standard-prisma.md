---
description: Стандарт кодирования Prisma — конвенции именования, паттерны, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: prisma
---

# Стандарт Prisma v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | Prisma 5.x |
| Ключевые библиотеки | `@prisma/client` 5.x, `prisma` 5.x (CLI) |
| Конфигурация | `prisma/schema.prisma` — модели, datasource, generator; `DATABASE_URL` в `.env` |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| Модель (model) | PascalCase, единственное число | `User`, `TaskItem` |
| Поле модели | camelCase | `userId`, `createdAt`, `isActive` |
| Таблица в БД (@@map) | snake_case, множественное число | `users`, `task_items` |
| Колонка в БД (@map) | snake_case | `user_id`, `created_at` |
| Enum | PascalCase | `TaskStatus`, `UserRole` |
| Значение enum | SCREAMING_SNAKE_CASE | `IN_PROGRESS`, `DONE` |
| Relation field | camelCase, совпадает с именем модели (строчная) | `user`, `taskItems` |
| Файл schema | без суффикса, в папке `prisma/` | `prisma/schema.prisma` |
| Файл миграции (папка) | `{timestamp}_{описание}` | `20240101120000_create_users` |
| Индекс | Prisma генерирует автоматически; явное `@@index` — описательное имя | `@@index([userId, status])` |

## Паттерны кода

### Инициализация клиента

Создавать единственный экземпляр PrismaClient на весь сервис. В production использовать глобальный синглтон для предотвращения исчерпания пула соединений при hot-reload.

```typescript
// src/{svc}/database/prisma.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ?? new PrismaClient({ log: ["error", "warn"] });

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}
```

### Определение схемы

Стандартный шаблон schema.prisma с datasource PostgreSQL и generator.

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  role      UserRole @default(USER)
  tasks     Task[]
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("users")
}

model Task {
  id          String     @id @default(uuid())
  title       String
  description String?
  status      TaskStatus @default(PENDING)
  userId      String     @map("user_id")
  user        User       @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt   DateTime   @default(now()) @map("created_at")
  updatedAt   DateTime   @updatedAt @map("updated_at")

  @@index([userId, status])
  @@map("tasks")
}

enum UserRole {
  USER
  ADMIN
}

enum TaskStatus {
  PENDING
  IN_PROGRESS
  DONE
  CANCELLED
}
```

### Запрос с фильтрацией и пагинацией

Стандартный паттерн для GET-списков с курсорной или offset-пагинацией. Использовать `findMany` с `skip`/`take` для offset, `cursor` — для курсорной пагинации.

```typescript
// src/{svc}/database/task.repository.ts
import { prisma } from "./prisma";
import { Prisma, TaskStatus } from "@prisma/client";

interface FindTasksParams {
  userId: string;
  status?: TaskStatus;
  skip?: number;
  take?: number;
}

export async function findTasks(
  params: FindTasksParams
): Promise<{ items: Prisma.TaskGetPayload<{}>[] ; total: number }> {
  const { userId, status, skip = 0, take = 20 } = params;

  const where: Prisma.TaskWhereInput = {
    userId,
    ...(status ? { status } : {}),
  };

  const [items, total] = await prisma.$transaction([
    prisma.task.findMany({
      where,
      orderBy: { createdAt: "desc" },
      skip,
      take,
    }),
    prisma.task.count({ where }),
  ]);

  return { items, total };
}
```

### Создание и обновление (CRUD)

Базовые операции CRUD с типизацией через `Prisma.TaskCreateInput` / `Prisma.TaskUpdateInput`.

```typescript
// src/{svc}/database/task.repository.ts
import { prisma } from "./prisma";
import { Prisma, Task } from "@prisma/client";

export async function createTask(
  data: Prisma.TaskCreateInput
): Promise<Task> {
  return prisma.task.create({ data });
}

export async function updateTask(
  id: string,
  data: Prisma.TaskUpdateInput
): Promise<Task> {
  return prisma.task.update({ where: { id }, data });
}

export async function deleteTask(id: string): Promise<Task> {
  return prisma.task.delete({ where: { id } });
}

export async function findTaskById(id: string): Promise<Task | null> {
  return prisma.task.findUnique({ where: { id } });
}
```

### Обработка ошибок

Ловить `PrismaClientKnownRequestError` для типизированной обработки ошибок БД. Код `P2002` — unique constraint, `P2025` — запись не найдена.

```typescript
// src/{svc}/database/task.repository.ts
import { Prisma } from "@prisma/client";

export async function createTaskSafe(
  data: Prisma.TaskCreateInput
): Promise<{ ok: true; task: Awaited<ReturnType<typeof createTask>> } | { ok: false; code: string }> {
  try {
    const task = await createTask(data);
    return { ok: true, task };
  } catch (e) {
    if (e instanceof Prisma.PrismaClientKnownRequestError) {
      if (e.code === "P2002") {
        return { ok: false, code: "UNIQUE_CONSTRAINT_VIOLATION" };
      }
      if (e.code === "P2025") {
        return { ok: false, code: "NOT_FOUND" };
      }
    }
    throw e;
  }
}
```

### Транзакция

Использовать `prisma.$transaction([...])` для атомарных операций над несколькими моделями. Для интерактивных транзакций с условной логикой — `prisma.$transaction(async (tx) => { ... })`.

```typescript
// src/{svc}/database/task.repository.ts
import { prisma } from "./prisma";
import { Prisma, Task } from "@prisma/client";

// Batch транзакция: несколько запросов одновременно
export async function batchCreateTasks(
  tasks: Prisma.TaskCreateInput[]
): Promise<Task[]> {
  return prisma.$transaction(
    tasks.map((data) => prisma.task.create({ data }))
  );
}

// Интерактивная транзакция: условная логика внутри
export async function completeTaskAndNotify(
  taskId: string,
  userId: string
): Promise<Task> {
  return prisma.$transaction(async (tx) => {
    const task = await tx.task.update({
      where: { id: taskId, userId },
      data: { status: "DONE" },
    });
    // Дополнительные операции в рамках той же транзакции
    await tx.user.update({
      where: { id: userId },
      data: { updatedAt: new Date() },
    });
    return task;
  });
}
```

### Миграции

Команды Prisma Migrate для управления схемой БД.

```bash
# Создать миграцию после изменения schema.prisma
npx prisma migrate dev --name add_task_status_index

# Применить все pending-миграции (CI/production)
npx prisma migrate deploy

# Сбросить БД и применить все миграции заново (только dev)
npx prisma migrate reset

# Просмотреть статус миграций
npx prisma migrate status

# Сгенерировать Prisma Client после изменения schema
npx prisma generate

# Открыть Prisma Studio (GUI для БД)
npx prisma studio
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| Создавать `new PrismaClient()` в каждом модуле | Исчерпание пула соединений (по умолчанию 10): при hot-reload или каждом запросе создаётся новый пул, что приводит к `PrismaClientInitializationError` | Один синглтон `prisma` на весь сервис (см. паттерн инициализации) |
| Использовать `prisma` напрямую в контроллерах/хэндлерах | Нарушает разделение ответственности; невозможно мокировать в тестах | Все запросы — через `*.repository.ts` |
| Вызывать `prisma.$disconnect()` в обработчике каждого запроса | Закрывает пул соединений; следующий запрос вынужден переподключаться | `$disconnect()` только при завершении процесса (SIGTERM/SIGINT) |
| Использовать `select: undefined` или не указывать `select` при работе с большими моделями | Тянет все поля, включая чувствительные (пароли, токены) | Явно указывать `select` или использовать `omit` для исключения полей |
| Строить `where` через строковую интерполяцию | SQL-инъекция через `$queryRawUnsafe` | Использовать `$queryRaw` с тегированным шаблоном: `` prisma.$queryRaw`SELECT ...` `` |
| Запускать `prisma migrate dev` в production | Создаёт теневую БД, может разрушить данные | Только `prisma migrate deploy` в production и CI |
| Не добавлять `@@index` на поля в `WHERE`/`ORDER BY` | Полный скан таблицы при росте данных; деградация производительности | Добавлять `@@index([field])` для частых фильтров/сортировок |
| Использовать `findFirst` вместо `findUnique` для поиска по ID | `findFirst` не гарантирует уникальность, медленнее из-за отсутствия оптимизации по PK | `findUnique({ where: { id } })` для поиска по уникальному ключу |

## Структура файлов

```
src/{svc}/
├── database/
│   ├── prisma.ts           # Синглтон PrismaClient
│   ├── user.repository.ts  # CRUD и запросы для модели User
│   └── task.repository.ts  # CRUD и запросы для модели Task
├── prisma/                 # (или корневой prisma/ для монорепы)
│   ├── schema.prisma       # Схема БД: модели, enums, datasource
│   └── migrations/         # Папки с SQL-миграциями
│       ├── 20240101_create_users/
│       │   └── migration.sql
│       └── migration_lock.toml
└── ...
```

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется вручную по чек-листу из [validation-technology.md](../../.instructions/docs/technology/validation-technology.md).*

## Тестирование

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| Фреймворк | `jest` / `vitest` | Основной test runner |
| Мокирование Prisma | `jest-mock-extended` | Типизированный мок PrismaClient |
| Integration DB | `@prisma/client` + Docker PostgreSQL | Реальная БД для integration-тестов |

### Фикстуры

Базовая фикстура создаёт изолированный мок PrismaClient для unit-тестов. Для integration-тестов — отдельная тестовая БД с применёнными миграциями.

```typescript
// src/{svc}/tests/fixtures/prisma.fixture.ts
import { PrismaClient } from "@prisma/client";
import { mockDeep, DeepMockProxy } from "jest-mock-extended";

export type MockPrismaClient = DeepMockProxy<PrismaClient>;

export function createMockPrisma(): MockPrismaClient {
  return mockDeep<PrismaClient>();
}

// Для integration-тестов: реальная тестовая БД
// jest.config.ts задаёт DATABASE_URL=postgresql://test:test@localhost:5433/test_db
export async function setupTestDb(): Promise<PrismaClient> {
  const prisma = new PrismaClient({
    datasources: { db: { url: process.env.TEST_DATABASE_URL } },
  });
  await prisma.$connect();
  return prisma;
}

export async function teardownTestDb(prisma: PrismaClient): Promise<void> {
  await prisma.$disconnect();
}
```

### Мокирование

- **Unit-тесты:** мокируем `PrismaClient` через `jest-mock-extended` — тестируем логику сервиса/репозитория без реальной БД.
- **Integration-тесты:** реальная БД (Docker), не мокируем — тестируем запросы и транзакции.
- **НЕ мокировать** при тестировании репозитория напрямую (это integration-тест).

```typescript
// src/{svc}/tests/unit/task.service.test.ts
import { createMockPrisma, MockPrismaClient } from "../fixtures/prisma.fixture";
import { Prisma, TaskStatus } from "@prisma/client";

// Вариант findTasks с dependency injection для unit-тестов:
// принимает prisma-клиент как параметр вместо использования синглтона
async function findTasksWithClient(
  client: Pick<MockPrismaClient, "task">,
  params: { userId: string; status?: TaskStatus; skip?: number; take?: number }
): Promise<{ items: Prisma.TaskGetPayload<{}>[] ; total: number }> {
  const { userId, status, skip = 0, take = 20 } = params;
  const where: Prisma.TaskWhereInput = {
    userId,
    ...(status ? { status } : {}),
  };
  const [items, total] = await client.task.$transaction
    // eslint-disable-next-line @typescript-eslint/no-explicit-any -- dependency injection для тестов: Pick<> не включает $transaction
    ? (client as any).$transaction([
        client.task.findMany({ where, orderBy: { createdAt: "desc" }, skip, take }),
        client.task.count({ where }),
      ])
    : [
        await client.task.findMany({ where, orderBy: { createdAt: "desc" }, skip, take }),
        await client.task.count({ where }),
      ];
  return { items, total };
}

// Внедряем мок через dependency injection
describe("findTasks unit", () => {
  let mockPrisma: MockPrismaClient;

  beforeEach(() => {
    mockPrisma = createMockPrisma();
  });

  it("returns empty list when no tasks", async () => {
    mockPrisma.task.findMany.mockResolvedValue([]);
    mockPrisma.task.count.mockResolvedValue(0);
    const result = await findTasksWithClient(mockPrisma, { userId: "user-1" });
    expect(result.total).toBe(0);
    expect(result.items).toHaveLength(0);
  });
});
```

### Паттерны тестов

```typescript
// src/{svc}/tests/integration/task.repository.test.ts
import { PrismaClient, TaskStatus } from "@prisma/client";
import { setupTestDb, teardownTestDb } from "../fixtures/prisma.fixture";
import { createTask, createTaskSafe, findTasks, deleteTask } from "../../database/task.repository";

describe("task.repository integration", () => {
  let prisma: PrismaClient;
  const TEST_USER_ID = "550e8400-e29b-41d4-a716-446655440001";

  beforeAll(async () => {
    prisma = await setupTestDb();
    // Создать тестового пользователя
    await prisma.user.create({
      data: { id: TEST_USER_ID, email: "test@example.com", name: "Test User" },
    });
  });

  afterAll(async () => {
    await prisma.task.deleteMany({ where: { userId: TEST_USER_ID } });
    await prisma.user.delete({ where: { id: TEST_USER_ID } });
    await teardownTestDb(prisma);
  });

  afterEach(async () => {
    await prisma.task.deleteMany({ where: { userId: TEST_USER_ID } });
  });

  it("creates and finds task", async () => {
    await createTask({ title: "Test task", user: { connect: { id: TEST_USER_ID } } });
    const { items, total } = await findTasks({ userId: TEST_USER_ID });
    expect(total).toBe(1);
    expect(items[0].title).toBe("Test task");
  });

  it("filters tasks by status", async () => {
    await createTask({ title: "A", status: "PENDING", user: { connect: { id: TEST_USER_ID } } });
    await createTask({ title: "B", status: "DONE", user: { connect: { id: TEST_USER_ID } } });
    const { items, total } = await findTasks({ userId: TEST_USER_ID, status: TaskStatus.DONE });
    expect(total).toBe(1);
    expect(items[0].title).toBe("B");
  });

  it("returns NOT_FOUND for missing task update", async () => {
    const result = await createTaskSafe({ title: "X", user: { connect: { id: "non-existent" } } });
    expect(result.ok).toBe(false);
  });
});
```

## Логирование

Prisma поддерживает query-логирование через опцию `log` в конструкторе. В production логировать только ошибки и медленные запросы (через event-based API).

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| Запрос выполнен (dev) | DEBUG | `prisma.query duration=12ms query="SELECT ..."` |
| Медленный запрос (>500ms) | WARNING | `prisma.slow_query duration=1250ms query="SELECT ..."` |
| Ошибка подключения | ERROR | `prisma.error message="Can't reach database server"` |
| P2002 UniqueConstraint | WARNING | `prisma.unique_violation model="User" field="email"` |
| P2025 RecordNotFound | WARNING | `prisma.not_found model="Task" id="abc-123"` |
| Миграция применена (deploy) | INFO | `prisma.migration_applied name="20240101_create_users"` |

```typescript
// src/{svc}/database/prisma.ts
import { PrismaClient, Prisma } from "@prisma/client";

const isDev = process.env.NODE_ENV !== "production";

export const prisma = new PrismaClient({
  log: isDev
    ? ["query", "warn", "error"]
    : [{ level: "warn", emit: "event" }, { level: "error", emit: "event" }],
});

// Production: event-based логирование для slow query detection
if (!isDev) {
  prisma.$on("warn" as never, (e: Prisma.LogEvent) => {
    console.warn({ msg: "prisma.warn", message: e.message, timestamp: e.timestamp });
  });
  prisma.$on("error" as never, (e: Prisma.LogEvent) => {
    console.error({ msg: "prisma.error", message: e.message, timestamp: e.timestamp });
  });
}

// Graceful shutdown
process.on("SIGTERM", async () => {
  await prisma.$disconnect();
});
process.on("SIGINT", async () => {
  await prisma.$disconnect();
});
```
