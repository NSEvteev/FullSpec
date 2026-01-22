/**
 * E2E Test Example
 *
 * Источник: /.claude/instructions/tests/e2e.md
 *
 * Пример E2E теста с использованием Playwright:
 * - Page Object Model (POM)
 * - Стабильные селекторы (data-testid)
 * - Независимые тесты
 * - Ожидания вместо задержек
 * - API setup для ускорения
 */

import { test, expect, Page, Locator } from '@playwright/test';

// ============================================================================
// Page Object Model
// ============================================================================

/**
 * LoginPage - Page Object для страницы логина
 */
class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly successMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    // Стандарт: использовать data-testid для селекторов
    this.emailInput = page.getByTestId('email-input');
    this.passwordInput = page.getByTestId('password-input');
    this.submitButton = page.getByTestId('login-submit');
    this.errorMessage = page.getByTestId('login-error');
    this.successMessage = page.getByTestId('login-success');
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
    // Стандарт: ожидание вместо задержки
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toContainText(message);
  }

  async expectSuccess() {
    await expect(this.successMessage).toBeVisible();
  }
}

/**
 * DashboardPage - Page Object для дашборда
 */
class DashboardPage {
  readonly page: Page;
  readonly welcomeMessage: Locator;
  readonly userStats: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.getByTestId('welcome-message');
    this.userStats = page.getByTestId('user-stats');
    this.logoutButton = page.getByTestId('logout-button');
  }

  async goto() {
    await this.page.goto('/dashboard');
  }

  async expectWelcome(name: string) {
    await expect(this.welcomeMessage).toContainText(`Welcome, ${name}`);
  }

  async logout() {
    await this.logoutButton.click();
    // Стандарт: ожидание редиректа
    await this.page.waitForURL('/login');
  }
}

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Логин через API для ускорения тестов
 */
async function loginViaApi(
  page: Page,
  email: string,
  password: string
): Promise<string> {
  const response = await page.request.post('/api/auth/login', {
    data: { email, password },
  });
  const { token } = await response.json();

  // Устанавливаем токен в браузер
  await page.goto('/');
  await page.evaluate((t) => {
    localStorage.setItem('auth_token', t);
  }, token);

  return token;
}

/**
 * Создание тестового пользователя через API
 */
async function createTestUser(
  page: Page,
  email: string
): Promise<{ id: string; token: string }> {
  const response = await page.request.post('/api/test/create-user', {
    data: { email, password: 'TestPass123!' },
  });
  return response.json();
}

/**
 * Удаление тестового пользователя (cleanup)
 */
async function deleteTestUser(page: Page, userId: string): Promise<void> {
  await page.request.delete(`/api/test/users/${userId}`);
}

// ============================================================================
// Tests
// ============================================================================

test.describe('Authentication Flow', () => {
  // Стандарт: независимые тесты - каждый тест полностью самодостаточен

  test('should show error for invalid credentials', async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);

    // Act
    await loginPage.goto();
    await loginPage.login('wrong@email.com', 'wrongpassword');

    // Assert
    await loginPage.expectError('Invalid credentials');
  });

  test('should show error for empty email', async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);

    // Act
    await loginPage.goto();
    await loginPage.login('', 'somepassword');

    // Assert
    await loginPage.expectError('Email is required');
  });

  test('should redirect to dashboard after successful login', async ({
    page,
  }) => {
    // Arrange - создаём тестового пользователя через API
    const testEmail = `test-${Date.now()}@example.com`;
    const { id: userId } = await createTestUser(page, testEmail);

    const loginPage = new LoginPage(page);

    try {
      // Act
      await loginPage.goto();
      await loginPage.login(testEmail, 'TestPass123!');

      // Assert
      await expect(page).toHaveURL('/dashboard');

      const dashboardPage = new DashboardPage(page);
      await expect(dashboardPage.welcomeMessage).toBeVisible();
    } finally {
      // Cleanup - удаляем тестового пользователя
      await deleteTestUser(page, userId);
    }
  });
});

test.describe('Dashboard', () => {
  let testUserId: string;
  let testEmail: string;

  test.beforeAll(async ({ browser }) => {
    // Стандарт: setup через API вместо UI
    const page = await browser.newPage();
    testEmail = `dashboard-test-${Date.now()}@example.com`;
    const user = await createTestUser(page, testEmail);
    testUserId = user.id;
    await page.close();
  });

  test.afterAll(async ({ browser }) => {
    // Cleanup
    const page = await browser.newPage();
    await deleteTestUser(page, testUserId);
    await page.close();
  });

  test.beforeEach(async ({ page }) => {
    // Стандарт: логин через API для ускорения
    await loginViaApi(page, testEmail, 'TestPass123!');
  });

  test('should display user stats', async ({ page }) => {
    // Arrange
    const dashboardPage = new DashboardPage(page);

    // Act
    await dashboardPage.goto();

    // Assert
    await expect(dashboardPage.userStats).toBeVisible();
  });

  test('should logout successfully', async ({ page }) => {
    // Arrange
    const dashboardPage = new DashboardPage(page);
    await dashboardPage.goto();

    // Act
    await dashboardPage.logout();

    // Assert
    await expect(page).toHaveURL('/login');
  });
});

// ============================================================================
// Full User Flow Example
// ============================================================================

test.describe('Purchase Flow', () => {
  test('should complete purchase as new user', async ({ page }) => {
    const uniqueEmail = `buyer-${Date.now()}@example.com`;

    // 1. Регистрация
    await page.goto('/register');
    await page.getByTestId('email').fill(uniqueEmail);
    await page.getByTestId('password').fill('SecurePass123!');
    await page.getByTestId('register-submit').click();

    // Стандарт: ожидание вместо задержки
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
    await page.getByTestId('address-zip').fill('12345');
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
