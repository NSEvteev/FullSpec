---
type: standard
description: Smoke-тесты: быстрая проверка работоспособности
related:
  - tests/project-testing.md
  - tests/e2e.md
  - git/ci.md
  - src/runtime/health.md
---

# Smoke-тесты

Правила написания smoke-тестов для быстрой проверки работоспособности системы.

## Оглавление

- [Что такое Smoke-тесты](#что-такое-smoke-тесты)
- [Когда запускать](#когда-запускать)
- [Что проверять](#что-проверять)
- [Структура](#структура)
- [Правила](#правила)
- [Примеры](#примеры)
- [CI/CD интеграция](#cicd-интеграция)
- [Мониторинг и алерты](#мониторинг-и-алерты)
- [Связанные инструкции](#связанные-инструкции)

---

## Что такое Smoke-тесты

**Smoke-тесты** (sanity tests) — минимальный набор проверок, что система запустилась и базово работает.

> **Происхождение:** Термин из электроники — если при включении устройства пошёл дым, тест провален.

### Характеристики

| Свойство | Значение |
|----------|----------|
| **Время выполнения** | < 2 минут (весь набор) |
| **Количество тестов** | 5-15 на сервис |
| **Глубина** | Поверхностная |
| **Цель** | "Система живая?" |

### Отличие от других тестов

| Тип | Цель | Время | Глубина |
|-----|------|-------|---------|
| **Smoke** | Система работает | Секунды | Минимальная |
| **E2E** | Сценарии работают | Минуты | Полная |
| **Integration** | Компоненты связаны | Секунды | Средняя |
| **Unit** | Логика верна | ms | Детальная |

---

## Когда запускать

### Обязательно

| Событие | Почему |
|---------|--------|
| **После деплоя** | Проверить, что релиз не сломал систему |
| **Перед E2E тестами** | Fail-fast если система не работает |
| **При старте CI pipeline** | Быстрая обратная связь |
| **Периодически (cron)** | Мониторинг продакшна |

### Частота в продакшне

```
┌─────────────────────────────────────────┐
│  Production Smoke Tests                 │
│                                         │
│  Every 5 min:  Health checks            │
│  Every 15 min: Critical paths           │
│  Every 1 hour: Full smoke suite         │
└─────────────────────────────────────────┘
```

---

## Что проверять

### Обязательные проверки

| Категория | Проверки |
|-----------|----------|
| **Health endpoints** | `/health`, `/ready` для каждого сервиса |
| **Авторизация** | Логин работает |
| **Главные страницы** | Homepage, Dashboard загружаются |
| **Критический API** | Основные endpoints отвечают |
| **База данных** | Подключение работает |
| **Внешние сервисы** | Критичные интеграции доступны |

### Чек-лист для нового сервиса

- [ ] Health check endpoint (`/health`)
- [ ] Readiness check (`/ready`)
- [ ] Главный endpoint отвечает
- [ ] Авторизация (если требуется)
- [ ] Подключение к БД (если есть)

### НЕ проверять в smoke

| Что | Почему |
|-----|--------|
| Бизнес-логику | Это unit/integration тесты |
| Все endpoints | Только критические |
| Edge cases | Это E2E тесты |
| Производительность | Это load тесты |

---

## Структура

### Расположение файлов

```
/tests/
  /smoke/
    health.smoke.ts         ← Health checks всех сервисов
    auth.smoke.ts           ← Авторизация
    api.smoke.ts            ← Критические API endpoints
    frontend.smoke.ts       ← Главные страницы
    database.smoke.ts       ← Подключение к БД
    external.smoke.ts       ← Внешние сервисы
```

### Именование

| Паттерн | Пример |
|---------|--------|
| `*.smoke.ts` | `health.smoke.ts` |
| `*.smoke.spec.ts` | `auth.smoke.spec.ts` |
| `smoke_*.py` | `smoke_health.py` |

---

## Правила

### 1. Быстрота — главный приоритет

```typescript
// Плохо — долгий smoke тест
test('should complete full checkout', async () => {
  // 30 секунд на один тест — слишком долго
});

// Хорошо — быстрая проверка
test('should load checkout page', async () => {
  const response = await fetch('/checkout');
  expect(response.status).toBe(200);
});
```

**Правило:** Один smoke тест < 5 секунд.

### 2. Независимость от данных

```typescript
// Плохо — зависит от конкретных данных
test('should return user John', async () => {
  const response = await fetch('/api/users/john-123');
  expect(response.json().name).toBe('John');
});

// Хорошо — проверяет структуру, не данные
test('should return user list', async () => {
  const response = await fetch('/api/users?limit=1');
  expect(response.status).toBe(200);
  expect(response.json()).toHaveProperty('data');
});
```

### 3. Понятные сообщения об ошибках

```typescript
// Плохо
expect(response.status).toBe(200);

// Хорошо
expect(response.status).toBe(200,
  `Auth service returned ${response.status}: ${await response.text()}`
);

// Или с описанием
test('Auth service should be healthy', async () => {
  const response = await fetch(`${AUTH_URL}/health`);
  expect(response.ok).toBe(true);
});
```

### 4. Таймауты

```typescript
// Smoke тесты должны быть быстрыми
const SMOKE_TIMEOUT = 5000; // 5 секунд max

test('API should respond', async () => {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), SMOKE_TIMEOUT);

  try {
    const response = await fetch('/api/health', { signal: controller.signal });
    expect(response.ok).toBe(true);
  } finally {
    clearTimeout(timeout);
  }
});
```

### 5. Параллельное выполнение

```typescript
// Smoke тесты независимы — запускаем параллельно
test.describe.parallel('Smoke Tests', () => {
  test('auth health', async () => { /* ... */ });
  test('users health', async () => { /* ... */ });
  test('orders health', async () => { /* ... */ });
});
```

---

## Примеры

### Пример 1: Health checks

```typescript
// tests/smoke/health.smoke.ts
import { test, expect } from '@playwright/test';

const SERVICES = [
  { name: 'auth', url: process.env.AUTH_URL },
  { name: 'users', url: process.env.USERS_URL },
  { name: 'orders', url: process.env.ORDERS_URL },
  { name: 'notifications', url: process.env.NOTIFICATIONS_URL },
];

test.describe('Health Checks', () => {
  for (const service of SERVICES) {
    test(`${service.name} should be healthy`, async ({ request }) => {
      const response = await request.get(`${service.url}/health`);

      expect(response.ok()).toBe(true);

      const body = await response.json();
      expect(body.status).toBe('healthy');
    });

    test(`${service.name} should be ready`, async ({ request }) => {
      const response = await request.get(`${service.url}/ready`);

      expect(response.ok()).toBe(true);
    });
  }
});
```

### Пример 2: Авторизация

```typescript
// tests/smoke/auth.smoke.ts
import { test, expect } from '@playwright/test';

test.describe('Auth Smoke Tests', () => {
  test('login page should load', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByTestId('login-form')).toBeVisible();
  });

  test('should login with valid credentials', async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: process.env.SMOKE_TEST_USER,
        password: process.env.SMOKE_TEST_PASSWORD,
      },
    });

    expect(response.ok()).toBe(true);
    const body = await response.json();
    expect(body).toHaveProperty('token');
  });

  test('should reject invalid credentials', async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: 'invalid@example.com',
        password: 'wrongpassword',
      },
    });

    expect(response.status()).toBe(401);
  });
});
```

### Пример 3: Критические API

```typescript
// tests/smoke/api.smoke.ts
import { test, expect } from '@playwright/test';

test.describe('Critical API Smoke Tests', () => {
  let authToken: string;

  test.beforeAll(async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: process.env.SMOKE_TEST_USER,
        password: process.env.SMOKE_TEST_PASSWORD,
      },
    });
    const body = await response.json();
    authToken = body.token;
  });

  test('GET /api/users should return list', async ({ request }) => {
    const response = await request.get('/api/users', {
      headers: { Authorization: `Bearer ${authToken}` },
    });

    expect(response.ok()).toBe(true);
    const body = await response.json();
    expect(body).toHaveProperty('data');
    expect(Array.isArray(body.data)).toBe(true);
  });

  test('GET /api/products should return list', async ({ request }) => {
    const response = await request.get('/api/products');

    expect(response.ok()).toBe(true);
    const body = await response.json();
    expect(body.data.length).toBeGreaterThan(0);
  });
});
```

### Пример 4: Bash-версия для быстрой проверки

```bash
#!/bin/bash
# tests/smoke/smoke.sh

set -e

echo "🔥 Running Smoke Tests..."

# Health checks
echo "Checking health endpoints..."
curl -sf "${AUTH_URL}/health" > /dev/null || { echo "❌ Auth unhealthy"; exit 1; }
curl -sf "${USERS_URL}/health" > /dev/null || { echo "❌ Users unhealthy"; exit 1; }
curl -sf "${ORDERS_URL}/health" > /dev/null || { echo "❌ Orders unhealthy"; exit 1; }

# Frontend
echo "Checking frontend..."
curl -sf "${FRONTEND_URL}" > /dev/null || { echo "❌ Frontend down"; exit 1; }

# API
echo "Checking API..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${API_URL}/api/health")
[ "$STATUS" = "200" ] || { echo "❌ API returned $STATUS"; exit 1; }

echo "✅ All smoke tests passed!"
```

---

## CI/CD интеграция

### GitHub Actions

```yaml
# .github/workflows/smoke.yml
name: Smoke Tests

on:
  deployment_status:
  schedule:
    - cron: '*/15 * * * *'  # Каждые 15 минут
  workflow_dispatch:

jobs:
  smoke:
    if: github.event.deployment_status.state == 'success' || github.event_name != 'deployment_status'
    runs-on: ubuntu-latest
    timeout-minutes: 5  # Быстрый таймаут

    steps:
      - uses: actions/checkout@v4

      - name: Run Smoke Tests
        run: npm run test:smoke
        env:
          BASE_URL: ${{ secrets.PRODUCTION_URL }}
          SMOKE_TEST_USER: ${{ secrets.SMOKE_TEST_USER }}
          SMOKE_TEST_PASSWORD: ${{ secrets.SMOKE_TEST_PASSWORD }}

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "🔥 Smoke tests failed in production!"
            }
```

### Post-deploy hook

```yaml
# В deploy workflow
deploy:
  # ... deploy steps ...

smoke-after-deploy:
  needs: deploy
  runs-on: ubuntu-latest
  steps:
    - name: Wait for deployment
      run: sleep 30

    - name: Run smoke tests
      run: |
        curl -sf "${{ env.DEPLOY_URL }}/health" || exit 1
        npm run test:smoke

    - name: Rollback on failure
      if: failure()
      run: |
        echo "Smoke tests failed, initiating rollback..."
        # rollback commands
```

---

## Мониторинг и алерты

### Интеграция с мониторингом

```typescript
// После smoke тестов — отправляем метрики
afterAll(async () => {
  const duration = Date.now() - startTime;
  const status = failedTests > 0 ? 'failed' : 'passed';

  // Отправляем в Prometheus/Datadog
  await sendMetric('smoke_tests_duration_seconds', duration / 1000);
  await sendMetric('smoke_tests_status', status === 'passed' ? 1 : 0);
});
```

### Алерты

| Условие | Действие |
|---------|----------|
| Smoke тест упал | Slack/PagerDuty алерт |
| Время > 2 мин | Warning в мониторинг |
| 3 падения подряд | Автоматический rollback |

### Пример алерта в Grafana

```yaml
# Alertmanager rule
- alert: SmokeTestsFailed
  expr: smoke_tests_status == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Smoke tests failed in production"
    description: "Smoke tests have been failing for more than 1 minute"
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/test-create](/.claude/skills/test-create/SKILL.md) | Создание теста |
| [/test-execute](/.claude/skills/test-execute/SKILL.md) | Выполнение тестов |
| [/test-review](/.claude/skills/test-review/SKILL.md) | Проверка качества теста |

---

## Связанные инструкции

- [project-testing.md](./project-testing.md) — индекс тестирования
- [e2e.md](./e2e.md) — полные E2E тесты
- [git/ci.md](../git/ci.md) — CI/CD pipeline
- [src/runtime/health.md](../src/runtime/health.md) — health checks
