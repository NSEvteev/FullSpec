---
description: Стандарт написания системных тестов (e2e, integration, load, smoke) — паттерны, тестовое окружение, fixtures, размещение файлов.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: tests/.instructions/README.md
---

# Стандарт системных тестов

Версия стандарта: 1.0

Стандарт написания системных тестов (e2e, integration, load, smoke) — паттерны, тестовое окружение, fixtures, размещение файлов.

**Полезные ссылки:**
- [Инструкции](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | *Не требуется* |
| Создание | *Не требуется* |
| Модификация | *Не требуется* |

**SSOT-зависимости:**
- [standard-docker.md](/platform/.instructions/standard-docker.md) § 8 — тестовое окружение (docker-compose.test.yml, tmpfs, сети)
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) — стратегия тестирования (типы, мокирование, данные)
- per-tech стандарты (`specs/docs/.technologies/standard-{tech}.md`) — фреймворки (pytest, Jest, k6)

## Оглавление

- [1. Назначение и разграничение](#1-назначение-и-разграничение)
- [2. Тестовое окружение](#2-тестовое-окружение)
- [3. Паттерн E2E-теста](#3-паттерн-e2e-теста)
- [4. Паттерн Integration-теста](#4-паттерн-integration-теста)
- [5. Асинхронные события](#5-асинхронные-события)
- [6. Fixtures и тестовые данные](#6-fixtures-и-тестовые-данные)
- [7. Load-тесты](#7-load-тесты)
- [8. Smoke-тесты](#8-smoke-тесты)

---

## 1. Назначение и разграничение

Этот документ определяет КАК писать системные тесты в проекте. Аудитория: dev-agent и LLM при реализации тестов из plan-test.md (TC-N).

**Что покрывает:**
- Паттерны e2e, integration, load, smoke тестов
- Работа с тестовым окружением (Docker)
- Организация fixtures и тестовых данных
- Размещение и именование файлов тестов

**Что НЕ покрывает (другие SSOT):**

| Тема | SSOT |
|------|------|
| Стратегия тестирования (типы, мокирование, принципы) | [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) |
| Per-tech паттерны (pytest fixtures, Jest mocks, k6 API) | `specs/docs/.technologies/standard-{tech}.md` |
| КОГДА запускать тесты в процессе разработки | [standard-development.md](/.github/.instructions/development/standard-development.md) § 4 |
| Docker-конфигурации (полное описание) | [standard-docker.md](/platform/.instructions/standard-docker.md) |
| Контрактные тесты (Pact, consumer-driven contracts) | Не определено (отдельный стандарт при необходимости) |

> **Когда запускать каждый тип тестов** (локально vs CI) — см. [standard-development.md](/.github/.instructions/development/standard-development.md) § 4.

---

## 2. Тестовое окружение

> **SSOT:** [standard-docker.md](/platform/.instructions/standard-docker.md) § 8 — полное описание docker-compose.test.yml, tmpfs, сетей.

**Поднятие:**

```bash
docker compose -f platform/docker/docker-compose.test.yml up -d --wait
```

**Health checks:**

Флаг `--wait` автоматически ожидает прохождения health checks, настроенных в `docker-compose.test.yml` (SSOT: [standard-docker.md](/platform/.instructions/standard-docker.md) § 8). Ниже — конфигурация, которая обеспечивает работу `--wait`:

| Сервис | Healthcheck в docker-compose.test.yml |
|--------|---------------------------------------|
| PostgreSQL | `pg_isready` |
| Redis | `redis-cli ping` |
| RabbitMQ | `rabbitmq-diagnostics -q ping` |

Таймаут: 60s. Если health check не пройден за 60s — ОСТАНОВИТЬ запуск тестов, выполнить `docker compose logs {service}` для диагностики и завершить с ошибкой.

**Остановка:**

```bash
docker compose -f platform/docker/docker-compose.test.yml down -v
```

**Сети:** `myapp-test` — изоляция от dev-окружения.

---

## 3. Паттерн E2E-теста

**Расположение:** `tests/e2e/`

**Именование файлов:** `{сценарий}.e2e.test.ts` (например: `registration.e2e.test.ts`, `password-reset.e2e.test.ts`)

**Запуск:** `make test-e2e`

**Параллельность:** E2E-тесты запускаются последовательно (не параллельно). Изоляция данных между тестами обеспечивается teardown (см. ниже).

E2E-тест проверяет полный путь через несколько сервисов. Все взаимодействия — через публичные API (не напрямую в БД).

**Паттерн Arrange/Act/Assert:**

| Фаза | Правило |
|-------|---------|
| **Arrange** | Подготовить состояние через API (POST/PUT). Прямые SQL-запросы в E2E запрещены |
| **Act** | Выполнить действие через HTTP/WS API сервиса |
| **Assert** | Проверить результат в сервисе-источнике (выполнял действие) и в сервисе-потребителе (получает результат) |

**Teardown:** Выполняется независимо от результата теста (afterEach/afterAll). Очистка данных — через тестовый API-эндпоинт или фикстуру teardown. Прямые SQL-команды в E2E запрещены.

**Пример: Регистрация пользователя**

```
Arrange:
  - Вызвать DELETE /api/test/reset (тестовый эндпоинт очистки)
    или запустить tests/fixtures/cleanup.ts (фикстура teardown)

Act:
  - POST /api/auth/register { email, password, name }

Assert (источник + потребитель):
  - auth-сервис (источник): GET /api/auth/users/{id} → 200, данные корректны
  - notification-сервис (потребитель): проверить отправку welcome-email (polling, см. § 5)
```

**Правила:**
- Один тест = одна атомарная бизнес-задача пользователя (например: "пользователь регистрируется", "пользователь восстанавливает пароль"). Несколько HTTP-запросов внутри одного теста допустимы, если они составляют единый flow
- Тесты независимы друг от друга (нет зависимости от порядка)
- Данные создаются в Arrange, удаляются в teardown (afterEach). Teardown выполняется независимо от результата теста

---

## 4. Паттерн Integration-теста

**Расположение:** `tests/integration/`

**Именование файлов:** `{сервис1}-{сервис2}.integration.test.ts` (например: `auth-notification.integration.test.ts`)

**Запуск:** `make test` (входит в общий набор)

**Параллельность:** Integration-тесты запускаются последовательно.

Integration-тест проверяет взаимодействие 2 сервисов. Остальные сервисы замокированы — способ мокирования определяется в `standard-{tech}.md` для используемого фреймворка.

**Отличие от E2E:**

| Аспект | E2E | Integration |
|--------|-----|-------------|
| Сервисы | Все поднятые | 2 реальных, остальные — моки |
| Данные | Через API | Через API (предпочтительно). Через repository — только если тестируется слой данных или API не предоставляет нужный метод |
| Scope | Полный бизнес-путь | Одно взаимодействие |

**Пример: Auth → Notification (событие)**

```
Arrange:
  - Поднять auth + notification (docker)
  - RabbitMQ реальный, остальные — моки

Act:
  - POST /api/auth/register → auth публикует событие user.registered

Assert:
  - notification-сервис: получил событие user.registered
  - notification-сервис: создал запись в outbox (polling, см. § 5)
```

---

## 5. Асинхронные события

При тестировании событий (RabbitMQ, Redis Pub/Sub) результат появляется с задержкой. Использовать polling с retry.

**Параметры polling:**

| Параметр | Значение |
|----------|----------|
| Интервал | 100ms |
| Таймаут | 5s |

> **SSOT:** Параметры определяются в [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) для конкретного проекта.

**Паттерн: retry loop с assertion**

```typescript
// Пример: ожидание появления записи после асинхронного события
async function waitFor<T>(
  fn: () => Promise<T>,
  predicate: (result: T) => boolean,
  { interval = 100, timeout = 5000 } = {}
): Promise<T> {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const result = await fn();
    if (predicate(result)) return result;
    await new Promise(r => setTimeout(r, interval));
  }
  throw new Error(`Timeout ${timeout}ms exceeded`);
}

// Использование — waitFor вызывается БЕЗ try/catch.
// Ошибка таймаута = провал теста (правильное поведение).
const notification = await waitFor(
  () => api.get('/api/notifications?userId=' + userId),
  (res) => res.data.length > 0
);
expect(notification.data[0].type).toBe('welcome');
```

**Правила:**
- Всегда использовать `waitFor` для асинхронных проверок (не `setTimeout`)
- `waitFor` НЕ оборачивается в try/catch — ошибка таймаута должна пробрасываться как провал теста
- Таймаут теста должен быть больше polling-таймаута
- При failure — логировать последнее состояние для диагностики

```typescript
// ЗАПРЕЩЕНО — подавление таймаута делает тест всегда зелёным:
try { await waitFor(...) } catch (e) { /* тест молча проходит */ }

// ПРАВИЛЬНО — таймаут = провал теста:
const result = await waitFor(...);
expect(result).toBeDefined();
```

---

## 6. Fixtures и тестовые данные

**Расположение:** `tests/fixtures/`

**Factories:** Минимальный валидный объект. Каждая factory создаёт один объект с default-значениями, переопределяемыми через параметры.

```typescript
// tests/fixtures/user.factory.ts
export function createUser(overrides?: Partial<User>): User {
  return {
    email: `test-${Date.now()}-${Math.random().toString(36).slice(2)}@example.com`,
    password: 'Test1234!',
    name: 'Test User',
    ...overrides,
  };
}
```

**Seed data:**

| Тип теста | Способ |
|-----------|--------|
| E2E | Через API (POST-запросы в Arrange). Прямые SQL-запросы запрещены |
| Integration | Через API (предпочтительно). Через repository — только если тестируется слой данных или API не предоставляет нужный метод |

**Очистка:** Truncate таблиц между тестами. Порядок: дочерние → родительские (FK constraints).

Пример порядка очистки:
```
1. notifications (дочерняя — FK на users)
2. sessions (дочерняя — FK на users)
3. users (родительская)
```

> Иерархию FK определять из Prisma schema или миграций проекта.

**Teardown:** Выполняется в `afterEach` / `afterAll` — независимо от результата теста (try/finally или встроенный механизм фреймворка).

> **SSOT:** Принципы работы с тестовыми данными — [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md).

---

## 7. Load-тесты

**Расположение:** `tests/load/`

**Именование файлов:** `{сценарий}.load.js` (например: `auth-flow.load.js`)

**Запуск:** `make test-load`

**Инструмент:** k6 (по умолчанию) или locust — зафиксирован в Design проекта в секции "Load Testing". Если Design не содержит явного выбора — использовать k6.

**Метрики и пороги:**

| Метрика | Описание | Порог (пример) |
|---------|----------|----------------|
| latency p95 | 95-й перцентиль времени ответа | < 500ms |
| throughput | Запросов в секунду (RPS) | > SLA из Design |
| error rate | Доля ошибочных ответов (%) | < 1% |

Пороговые значения фиксируются в `tests/load/config/thresholds.json`. Заполняются при реализации TC-N типа load на основе SLA из Design. Тест считается провальным, если хотя бы одна метрика выходит за порог.

**Когда запускать:** Pre-release (Фаза 7), не во время разработки (Фаза 4). Исключение — если SLA определено в Design и есть TC-N типа load.

**Структура сценария:**

```
tests/load/
├── scenarios/          # Сценарии нагрузки
│   ├── auth-flow.load.js
│   └── dashboard.load.js
├── config/
│   └── thresholds.json # Пороговые значения (SLA из Design)
└── README.md
```

---

## 8. Smoke-тесты

**Расположение:** `tests/smoke/`

**Именование файлов:** `{сервис}.smoke.test.ts` (например: `auth.smoke.test.ts`)

**Запуск:** `make test-smoke`

**Когда запускать:** Post-deploy. Не во время разработки.

**Минимальный набор:** `GET /health` для каждого сервиса.

**Паттерн:**

```
Для каждого сервиса в deployment:
  1. GET /health → ожидать 200 OK
  2. Проверить поле status в response body: значение "ok". Дополнительные поля допустимы
  3. Timeout: 10s
```

**Расширенный smoke (при наличии):**
- Проверка подключения к БД (через health endpoint)
- Проверка доступности message broker
- Проверка gateway routing (каждый сервис доступен через gateway)
