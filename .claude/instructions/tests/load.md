---
type: standard
description: Нагрузочные тесты: k6, пороги производительности
related:
  - tests/project-testing.md
  - tests/smoke.md
  - platform/observability/metrics.md
  - src/dev/performance.md
---

# Нагрузочные тесты

Правила написания нагрузочных тестов для проверки производительности и устойчивости системы.

## Оглавление

- [Что такое нагрузочные тесты](#что-такое-нагрузочные-тесты)
- [Типы нагрузочного тестирования](#типы-нагрузочного-тестирования)
- [Инструменты](#инструменты)
- [Структура](#структура)
- [Правила](#правила)
- [k6 — основы](#k6--основы)
- [Примеры](#примеры)
- [Пороги и метрики](#пороги-и-метрики)
- [CI/CD интеграция](#cicd-интеграция)
- [Анализ результатов](#анализ-результатов)
- [Связанные инструкции](#связанные-инструкции)

---

## Что такое нагрузочные тесты

**Нагрузочные тесты** проверяют поведение системы под нагрузкой — много пользователей, много запросов.

### Зачем нужны

| Цель | Что выявляем |
|------|--------------|
| **Производительность** | Время отклика под нагрузкой |
| **Масштабируемость** | Сколько пользователей выдержит |
| **Стабильность** | Утечки памяти, деградация |
| **Пределы** | Точка отказа системы |

---

## Типы нагрузочного тестирования

```
        Нагрузка
           ▲
           │     ┌─────────────────────────┐
Stress ────┤     │█████████████████████████│ Breakpoint
           │     │████████████████████     │
Spike  ────┤     │█████████      ████████  │
           │     │████████████████████████ │
Load   ────┤     │████████████████████████ │
           │     │████████████████████████ │
Smoke  ────┤     │██                       │
           │     └─────────────────────────┘
           └──────────────────────────────────▶ Время
```

| Тип | Цель | Нагрузка | Длительность |
|-----|------|----------|--------------|
| **Smoke** | Базовая проверка | Минимальная (1-5 VU) | 1-2 мин |
| **Load** | Типичная нагрузка | Ожидаемая (50-100 VU) | 10-30 мин |
| **Stress** | Предел системы | Выше нормы (200+ VU) | 10-30 мин |
| **Spike** | Резкие пики | Скачки нагрузки | 5-10 мин |
| **Soak** | Утечки памяти | Средняя, долго | 1-4 часа |
| **Breakpoint** | Точка отказа | Рост до падения | До отказа |

**VU** = Virtual Users (виртуальные пользователи)

---

## Инструменты

### Рекомендуемый: k6

| Плюсы | Минусы |
|-------|--------|
| JavaScript синтаксис | Нет GUI (CLI-first) |
| Легковесный | Меньше протоколов чем JMeter |
| Отличная интеграция с CI | |
| Встроенные метрики | |
| Cloud-версия доступна | |

### Установка k6

```bash
# macOS
brew install k6

# Windows
choco install k6

# Docker
docker run -i grafana/k6 run - <script.js
```

### Альтернативы

| Инструмент | Когда использовать |
|------------|-------------------|
| **k6** | Основной выбор |
| **JMeter** | Сложные протоколы, GUI |
| **Gatling** | Scala-проекты |
| **Locust** | Python-проекты |

---

## Структура

### Расположение файлов

```
/tests/
  /load/
    /services/              ← Изолированные тесты сервисов
      auth.k6.js
      users.k6.js
      orders.k6.js
    /scenarios/             ← Сценарные тесты
      checkout-flow.k6.js
      user-journey.k6.js
    /system/                ← Системные тесты
      peak-load.k6.js
      stress-test.k6.js
      soak-test.k6.js
    /config/
      thresholds.js         ← Общие пороги
      options.js            ← Общие настройки
    /utils/
      helpers.js
      data-generators.js
```

### Именование

| Паттерн | Пример |
|---------|--------|
| `*.k6.js` | `auth.k6.js` |
| `*-load.k6.js` | `checkout-load.k6.js` |
| `*-stress.k6.js` | `api-stress.k6.js` |

---

## Правила

### 1. Реалистичные сценарии

```javascript
// Плохо — нереалистично
export default function() {
  // Бесконечный цикл запросов без пауз
  http.get('/api/users');
}

// Хорошо — реалистичное поведение
export default function() {
  http.get('/api/users');
  sleep(randomIntBetween(1, 5)); // Пауза как у реального пользователя
}
```

### 2. Постепенное наращивание

```javascript
// Плохо — резкий старт
export const options = {
  vus: 1000,
  duration: '10m',
};

// Хорошо — ramp-up
export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Наращиваем
    { duration: '5m', target: 100 },  // Держим
    { duration: '2m', target: 0 },    // Снижаем
  ],
};
```

### 3. Определённые пороги

```javascript
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],     // 95% запросов < 500ms
    http_req_failed: ['rate<0.01'],       // < 1% ошибок
    http_reqs: ['rate>100'],              // > 100 RPS
  },
};
```

### 4. Изоляция окружения

```bash
# Нагрузочные тесты только на staging/load-test окружении
# Никогда на production!

export BASE_URL=https://load-test.example.com
k6 run load-test.k6.js
```

---

## k6 — основы

### Базовый скрипт

```javascript
// tests/load/services/auth.k6.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function() {
  const response = http.post('https://api.example.com/auth/login', {
    email: 'test@example.com',
    password: 'password123',
  });

  check(response, {
    'status is 200': (r) => r.status === 200,
    'has token': (r) => r.json('token') !== undefined,
  });

  sleep(1);
}
```

### Stages (этапы)

```javascript
export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp-up до 50 VU
    { duration: '3m', target: 50 },   // Держим 50 VU
    { duration: '1m', target: 100 },  // Увеличиваем до 100 VU
    { duration: '3m', target: 100 },  // Держим 100 VU
    { duration: '2m', target: 0 },    // Ramp-down
  ],
};
```

### Scenarios (сценарии)

```javascript
export const options = {
  scenarios: {
    // Сценарий 1: Постоянная нагрузка
    constant_load: {
      executor: 'constant-vus',
      vus: 50,
      duration: '5m',
    },
    // Сценарий 2: Наращивание
    ramping_load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '3m', target: 100 },
      ],
      startTime: '5m', // Начать после первого сценария
    },
  },
};
```

---

## Примеры

### Пример 1: Тест API сервиса

```javascript
// tests/load/services/users.k6.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

export const options = {
  stages: [
    { duration: '1m', target: 20 },
    { duration: '3m', target: 20 },
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<300', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
    'http_req_duration{name:GetUsers}': ['p(95)<200'],
    'http_req_duration{name:GetUser}': ['p(95)<100'],
  },
};

export default function() {
  group('Users API', () => {
    // GET /users
    const listResponse = http.get(`${BASE_URL}/api/users`, {
      tags: { name: 'GetUsers' },
    });
    check(listResponse, {
      'list status 200': (r) => r.status === 200,
      'list has data': (r) => r.json('data').length > 0,
    });

    sleep(randomIntBetween(1, 3));

    // GET /users/:id
    const userId = listResponse.json('data.0.id');
    const getResponse = http.get(`${BASE_URL}/api/users/${userId}`, {
      tags: { name: 'GetUser' },
    });
    check(getResponse, {
      'get status 200': (r) => r.status === 200,
      'get has id': (r) => r.json('id') === userId,
    });
  });

  sleep(randomIntBetween(2, 5));
}
```

### Пример 2: Сценарий покупки

```javascript
// tests/load/scenarios/checkout-flow.k6.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL;

export const options = {
  scenarios: {
    checkout: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },
        { duration: '5m', target: 50 },
        { duration: '2m', target: 0 },
      ],
    },
  },
  thresholds: {
    'group_duration{group:::Checkout Flow}': ['p(95)<10000'],
    http_req_failed: ['rate<0.05'],
  },
};

export default function() {
  let token;

  group('Checkout Flow', () => {
    // 1. Логин
    group('Login', () => {
      const loginRes = http.post(`${BASE_URL}/api/auth/login`, {
        email: `user${__VU}@test.com`,
        password: 'password',
      });
      check(loginRes, { 'logged in': (r) => r.status === 200 });
      token = loginRes.json('token');
    });

    sleep(2);

    // 2. Просмотр каталога
    group('Browse Products', () => {
      const productsRes = http.get(`${BASE_URL}/api/products`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      check(productsRes, { 'got products': (r) => r.status === 200 });
    });

    sleep(3);

    // 3. Добавление в корзину
    group('Add to Cart', () => {
      const cartRes = http.post(`${BASE_URL}/api/cart`,
        JSON.stringify({ productId: '123', quantity: 1 }),
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );
      check(cartRes, { 'added to cart': (r) => r.status === 201 });
    });

    sleep(2);

    // 4. Оформление заказа
    group('Place Order', () => {
      const orderRes = http.post(`${BASE_URL}/api/orders`,
        JSON.stringify({ paymentMethod: 'card' }),
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );
      check(orderRes, { 'order placed': (r) => r.status === 201 });
    });
  });

  sleep(5);
}
```

### Пример 3: Stress-тест

```javascript
// tests/load/system/stress-test.k6.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Нормальная нагрузка
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },   // Повышенная
    { duration: '5m', target: 200 },
    { duration: '2m', target: 300 },   // Стресс
    { duration: '5m', target: 300 },
    { duration: '2m', target: 400 },   // Критическая
    { duration: '5m', target: 400 },
    { duration: '5m', target: 0 },     // Recovery
  ],
  thresholds: {
    http_req_duration: ['p(99)<2000'],  // Даже под стрессом < 2s
    http_req_failed: ['rate<0.10'],     // < 10% ошибок
  },
};

export default function() {
  const response = http.get(`${__ENV.BASE_URL}/api/health`);
  check(response, {
    'status 200': (r) => r.status === 200,
  });
  sleep(1);
}
```

---

## Пороги и метрики

### Стандартные пороги

| Метрика | Порог | Описание |
|---------|-------|----------|
| `http_req_duration` | `p(95)<500` | 95% запросов < 500ms |
| `http_req_failed` | `rate<0.01` | < 1% ошибок |
| `http_reqs` | `rate>100` | > 100 RPS |
| `vus` | `value>50` | > 50 активных VU |

### Рекомендуемые пороги по типу

| Тип теста | p95 latency | Error rate | Min RPS |
|-----------|-------------|------------|---------|
| Smoke | < 200ms | < 0.1% | — |
| Load | < 500ms | < 1% | 100 |
| Stress | < 2000ms | < 10% | — |
| Spike | < 3000ms | < 15% | — |

---

## CI/CD интеграция

### GitHub Actions

```yaml
# .github/workflows/load-tests.yml
name: Load Tests

on:
  schedule:
    - cron: '0 2 * * *'  # Каждую ночь
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install k6
        run: |
          sudo gpg -k
          sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6

      - name: Run Load Tests
        run: k6 run tests/load/services/auth.k6.js
        env:
          BASE_URL: ${{ secrets.LOAD_TEST_URL }}

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results/
```

---

## Анализ результатов

### k6 output

```bash
# JSON output
k6 run --out json=results.json script.k6.js

# InfluxDB (для Grafana)
k6 run --out influxdb=http://localhost:8086/k6 script.k6.js

# Cloud
k6 cloud script.k6.js
```

### Ключевые метрики

```
     data_received..................: 1.2 GB  2.0 MB/s
     data_sent......................: 150 MB  250 kB/s
     http_req_blocked...............: avg=1.2ms   p(95)=3.5ms
     http_req_duration..............: avg=120ms   p(95)=450ms   ← Важно!
     http_req_failed................: 0.5%    ← Важно!
     http_reqs......................: 150000  250/s           ← Важно!
     vus............................: 100
```

---

## Связанные инструкции

- [project-testing.md](./project-testing.md) — индекс тестирования
- [smoke.md](./smoke.md) — smoke-тесты
- [platform/observability/metrics.md](../platform/observability/metrics.md) — метрики
- [src/dev/performance.md](../src/dev/performance.md) — производительность
