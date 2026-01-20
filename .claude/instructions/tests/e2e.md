---
type: standard
description: End-to-end тесты: сценарии пользователя, инструменты
related:
  - tests/project-testing.md
  - tests/integration.md
  - tests/smoke.md
  - tests/fixtures.md
---

# End-to-End тесты

Правила написания E2E-тестов для проверки полных пользовательских сценариев.

## Оглавление

- [Что такое E2E](#что-такое-e2e)
- [Когда использовать](#когда-использовать)
- [Инструменты](#инструменты)
- [Структура](#структура)
- [Правила](#правила)
- [Паттерны](#паттерны)
- [Примеры](#примеры)
- [CI/CD интеграция](#cicd-интеграция)
- [Отладка](#отладка)
- [Антипаттерны](#антипаттерны)
- [Связанные инструкции](#связанные-инструкции)

---

## Что такое E2E

**End-to-End тесты** проверяют приложение целиком — от UI до базы данных, имитируя действия реального пользователя.

```
┌─────────────────────────────────────────────────────┐
│                    E2E Test                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │ Browser │───▶│ Frontend│───▶│ Backend │───▶ DB  │
│  └─────────┘    └─────────┘    └─────────┘         │
│       ▲                                             │
│       │ Playwright/Cypress                          │
└───────┼─────────────────────────────────────────────┘
        │
   Test Script
```

### Отличие от других типов

| Аспект | Unit | Integration | E2E |
|--------|------|-------------|-----|
| **Scope** | Функция | Модули | Вся система |
| **Скорость** | ms | секунды | минуты |
| **Хрупкость** | Низкая | Средняя | Высокая |
| **Confidence** | Низкий | Средний | Высокий |
| **Количество** | Много | Средне | Мало |

---

## Когда использовать

### Тестировать E2E

| Сценарий | Пример |
|----------|--------|
| **Критические пути** | Регистрация, оплата, оформление заказа |
| **Основные user flows** | Логин → Просмотр каталога → Покупка |
| **Интеграция frontend + backend** | Формы, авторизация, навигация |
| **Smoke после деплоя** | Проверка, что продакшн работает |

### НЕ тестировать E2E

| Сценарий | Почему | Альтернатива |
|----------|--------|--------------|
| Бизнес-логика | Медленно, хрупко | Unit-тесты |
| Все edge cases | Комбинаторный взрыв | Integration |
| Визуальные детали | Нестабильно | Visual regression |
| API контракты | Излишне | Contract tests |

---

## Инструменты

### Рекомендуемые

| Инструмент | Когда использовать |
|------------|-------------------|
| **Playwright** | Основной выбор (быстрый, надёжный, кроссбраузерный) |
| **Cypress** | Альтернатива (хороший DX, только Chromium) |

### Сравнение

| Критерий | Playwright | Cypress |
|----------|------------|---------|
| Браузеры | Chrome, Firefox, Safari, Edge | Chrome, Edge, Firefox |
| Скорость | Быстрее | Медленнее |
| Параллелизм | Из коробки | Платная фича |
| Mobile | Эмуляция | Нет |
| API тесты | Поддержка | Поддержка |
| Отладка | Trace viewer | Time travel |

### Установка Playwright

```bash
npm init playwright@latest

# Структура после установки
/tests/
  /e2e/
    example.spec.ts
  playwright.config.ts
```

---

## Структура

### Расположение файлов

```
/tests/
  /e2e/
    /auth/
      login.spec.ts
      register.spec.ts
      password-reset.spec.ts
    /checkout/
      cart.spec.ts
      payment.spec.ts
      order-confirmation.spec.ts
    /fixtures/
      test-users.ts
      test-products.ts
    /pages/                    ← Page Object Models
      login.page.ts
      checkout.page.ts
    /utils/
      helpers.ts
      api-client.ts
  playwright.config.ts
```

### Именование

| Паттерн | Пример |
|---------|--------|
| `*.spec.ts` | `login.spec.ts` |
| `*.e2e.ts` | `checkout.e2e.ts` |
| `*.e2e-spec.ts` | `payment.e2e-spec.ts` |

---

## Правила

### 1. Независимость тестов

Каждый тест должен работать изолированно:

```typescript
// Плохо — зависит от предыдущего теста
test('should show cart', async () => {
  // Предполагает, что пользователь уже залогинен
  await page.goto('/cart');
});

// Хорошо — полный сценарий
test('should show cart for logged user', async ({ page }) => {
  await loginAs(page, testUser);
  await page.goto('/cart');
  await expect(page.locator('.cart')).toBeVisible();
});
```

### 2. Стабильные селекторы

```typescript
// Плохо — хрупкие селекторы
await page.click('.btn-primary');
await page.click('div > div > button');
await page.click(':nth-child(3)');

// Хорошо — data-testid
await page.click('[data-testid="submit-button"]');
await page.getByRole('button', { name: 'Submit' });
await page.getByTestId('login-form');
```

**Правило:** Добавлять `data-testid` к интерактивным элементам.

### 3. Ожидания вместо задержек

```typescript
// Плохо — фиксированная задержка
await page.click('button');
await page.waitForTimeout(3000);

// Хорошо — ожидание условия
await page.click('button');
await page.waitForSelector('.success-message');
await expect(page.locator('.loader')).toBeHidden();
```

### 4. Изоляция данных

```typescript
// Каждый тест создаёт свои данные
test('should create order', async ({ page, request }) => {
  // Создаём тестового пользователя через API
  const user = await createTestUser(request);

  // Логинимся
  await loginAs(page, user);

  // Тест...

  // Cleanup (опционально — можно в afterEach)
  await deleteTestUser(request, user.id);
});
```

### 5. Retry для flaky тестов

```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,

  // Или для конкретного теста
  use: {
    // ...
  }
});

// В тесте
test('flaky network test', async ({ page }) => {
  test.info().annotations.push({ type: 'flaky' });
  // ...
});
```

---

## Паттерны

### Page Object Model (POM)

```typescript
// pages/login.page.ts
export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByTestId('email-input');
    this.passwordInput = page.getByTestId('password-input');
    this.submitButton = page.getByTestId('login-submit');
    this.errorMessage = page.getByTestId('login-error');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }
}

// Использование в тесте
test('should show error for invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('wrong@email.com', 'wrongpass');
  await loginPage.expectError('Invalid credentials');
});
```

### API Setup для ускорения

```typescript
// Вместо UI-логина — используем API
test.beforeEach(async ({ page, request }) => {
  // Логин через API (быстрее)
  const response = await request.post('/api/auth/login', {
    data: { email: 'test@example.com', password: 'password' }
  });
  const { token } = await response.json();

  // Устанавливаем токен в браузер
  await page.goto('/');
  await page.evaluate((t) => {
    localStorage.setItem('auth_token', t);
  }, token);
});
```

### Fixtures для переиспользования

```typescript
// fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/login.page';

type AuthFixtures = {
  loginPage: LoginPage;
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  authenticatedPage: async ({ page, request }, use) => {
    // Setup: логин через API
    const response = await request.post('/api/auth/login', {
      data: { email: 'test@example.com', password: 'password' }
    });
    const { token } = await response.json();

    await page.goto('/');
    await page.evaluate((t) => localStorage.setItem('token', t), token);

    await use(page);

    // Teardown: logout
    await page.evaluate(() => localStorage.removeItem('token'));
  }
});

// Использование
test('should show dashboard', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/dashboard');
  await expect(authenticatedPage.locator('h1')).toContainText('Dashboard');
});
```

---

## Примеры

### Пример 1: Полный сценарий покупки

```typescript
// tests/e2e/checkout/purchase-flow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Purchase Flow', () => {
  test('should complete purchase as new user', async ({ page }) => {
    // 1. Регистрация
    await page.goto('/register');
    await page.getByTestId('email').fill('newuser@example.com');
    await page.getByTestId('password').fill('SecurePass123!');
    await page.getByTestId('register-submit').click();
    await expect(page).toHaveURL('/dashboard');

    // 2. Добавление товара в корзину
    await page.goto('/products');
    await page.getByTestId('product-card').first().click();
    await page.getByTestId('add-to-cart').click();
    await expect(page.getByTestId('cart-count')).toHaveText('1');

    // 3. Оформление заказа
    await page.getByTestId('cart-icon').click();
    await page.getByTestId('checkout-button').click();

    // 4. Заполнение адреса
    await page.getByTestId('address-street').fill('123 Test St');
    await page.getByTestId('address-city').fill('Test City');
    await page.getByTestId('continue-to-payment').click();

    // 5. Оплата (тестовая карта)
    await page.getByTestId('card-number').fill('4242424242424242');
    await page.getByTestId('card-expiry').fill('12/25');
    await page.getByTestId('card-cvc').fill('123');
    await page.getByTestId('pay-button').click();

    // 6. Подтверждение
    await expect(page.getByTestId('order-confirmation')).toBeVisible();
    await expect(page.getByTestId('order-number')).toHaveText(/ORD-\d+/);
  });
});
```

### Пример 2: Тест с API setup

```typescript
test.describe('Dashboard', () => {
  let authToken: string;

  test.beforeAll(async ({ request }) => {
    // Создаём тестового пользователя через API
    const response = await request.post('/api/test/create-user', {
      data: { email: 'dashboard-test@example.com' }
    });
    const data = await response.json();
    authToken = data.token;
  });

  test.beforeEach(async ({ page }) => {
    // Устанавливаем токен
    await page.goto('/');
    await page.evaluate((token) => {
      localStorage.setItem('auth_token', token);
    }, authToken);
  });

  test('should display user stats', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page.getByTestId('user-stats')).toBeVisible();
    await expect(page.getByTestId('orders-count')).toHaveText('0');
  });
});
```

---

## CI/CD интеграция

### GitHub Actions

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Start application
        run: npm run start:test &
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

      - name: Wait for app
        run: npx wait-on http://localhost:3000

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
```

### Параллельный запуск

```typescript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 4 : undefined,
  fullyParallel: true,
});
```

---

## Отладка

### Playwright Inspector

```bash
# Запуск в режиме отладки
npx playwright test --debug

# Запуск конкретного теста
npx playwright test login.spec.ts --debug
```

### Trace Viewer

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on-first-retry', // Записывать trace при retry
  },
});

// Просмотр trace
npx playwright show-trace trace.zip
```

### Скриншоты при падении

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
});
```

---

## Антипаттерны

### 1. Слишком много E2E тестов

```
❌ 500 E2E тестов — медленно, хрупко
✅ 50 E2E на критические пути + unit/integration
```

### 2. Тестирование бизнес-логики через UI

```typescript
// Плохо — проверяем калькуляцию через UI
test('should calculate discount', async ({ page }) => {
  await page.fill('#price', '100');
  await page.fill('#discount', '10');
  await page.click('#calculate');
  await expect(page.locator('#result')).toHaveText('90');
});

// Хорошо — это unit-тест
test('calculateDiscount', () => {
  expect(calculateDiscount(100, 10)).toBe(90);
});
```

### 3. Хрупкие селекторы

```typescript
// Плохо
await page.click('body > div:nth-child(2) > button.blue');

// Хорошо
await page.click('[data-testid="submit"]');
```

### 4. Фиксированные задержки

```typescript
// Плохо
await page.waitForTimeout(5000);

// Хорошо
await page.waitForSelector('.loaded');
await expect(page.locator('.spinner')).toBeHidden();
```

---

## Связанные инструкции

- [project-testing.md](./project-testing.md) — индекс тестирования
- [integration.md](./integration.md) — интеграционные тесты
- [smoke.md](./smoke.md) — smoke-тесты
- [fixtures.md](./fixtures.md) — тестовые данные
