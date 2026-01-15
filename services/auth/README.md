# Auth Service (Сервис авторизации)

Сервис отвечает за аутентификацию и авторизацию пользователей.

## Функциональность

- ✅ Регистрация пользователей
- ✅ Авторизация (login/logout)
- ✅ Управление JWT токенами
- ✅ Обновление токенов (refresh)
- ✅ Валидация токенов
- ✅ OAuth интеграция (Google, GitHub, etc.)
- ✅ Восстановление пароля
- ✅ Подтверждение email

## Структура

```
auth/
├── src/                   # Исходный код сервиса
├── tests/                 # Тесты сервиса
├── static/                # Статические файлы (email шаблоны)
├── .env.example           # Пример переменных окружения
├── Dockerfile             # Docker конфигурация
├── package.json           # Зависимости (Node.js)
│                          # или requirements.txt (Python)
│                          # или go.mod (Go)
└── README.md              # Этот файл
```

## Технологический стек

**TODO:** Выбрать стек для auth сервиса:
- Node.js + Express + TypeScript
- Python + FastAPI
- Go + Gin/Fiber
- Другой вариант

## Переменные окружения

```bash
# Скопировать example файл
cp .env.example .env
```

### Основные переменные

```env
# Порт сервиса
PORT=8001

# База данных (для хранения пользователей)
DATABASE_URL=postgresql://user:password@postgres:5432/auth_db

# JWT секреты
JWT_SECRET=your-secret-key-256-bit
JWT_ACCESS_TOKEN_EXPIRES=15m
JWT_REFRESH_TOKEN_EXPIRES=7d

# Redis для сессий и blacklist токенов
REDIS_URL=redis://redis:6379

# SMTP для отправки писем
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=your-smtp-password

# OAuth провайдеры
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# Безопасность
BCRYPT_ROUNDS=10
RATE_LIMIT_WINDOW=15m
RATE_LIMIT_MAX=100
```

## API Эндпоинты

### Регистрация и авторизация

```
POST   /api/auth/register          # Регистрация нового пользователя
POST   /api/auth/login              # Авторизация
POST   /api/auth/logout             # Выход (инвалидация токена)
POST   /api/auth/refresh            # Обновление access токена
```

### Восстановление пароля

```
POST   /api/auth/forgot-password    # Запрос восстановления пароля
POST   /api/auth/reset-password     # Установка нового пароля
```

### Email подтверждение

```
POST   /api/auth/resend-verification  # Отправить письмо повторно
GET    /api/auth/verify-email/:token  # Подтвердить email по токену
```

### OAuth

```
GET    /api/auth/oauth/google         # Google OAuth
GET    /api/auth/oauth/github         # GitHub OAuth
GET    /api/auth/oauth/callback       # OAuth callback
```

### Валидация

```
POST   /api/auth/validate-token       # Проверить токен (для других сервисов)
GET    /api/auth/me                   # Получить данные текущего пользователя
```

## Схема данных

### User (базовая структура)

```typescript
interface User {
  id: string;
  email: string;
  passwordHash: string;
  isEmailVerified: boolean;
  emailVerificationToken?: string;
  passwordResetToken?: string;
  passwordResetExpires?: Date;
  oauthProvider?: 'google' | 'github' | null;
  oauthId?: string;
  createdAt: Date;
  updatedAt: Date;
}
```

### Tokens

```typescript
interface RefreshToken {
  id: string;
  userId: string;
  token: string;
  expiresAt: Date;
  createdAt: Date;
}
```

## Взаимодействие с другими сервисами

### Users Service
Auth Service создает базовую запись пользователя, а Users Service управляет профилем:
- После успешной регистрации → вызов Users Service для создания профиля
- Передача `userId` для связи

### API Gateway
Все запросы к Auth Service идут через API Gateway:
```
Client → API Gateway → Auth Service
```

## Установка и запуск

```bash
# TODO: Добавить команды после выбора стека

# Установка зависимостей
npm install

# Миграции БД
npm run migrate

# Запуск в dev режиме
npm run dev

# Запуск с Docker
docker build -t auth-service .
docker run -p 8001:8001 auth-service
```

## Тестирование

```bash
# Unit тесты
npm test

# Integration тесты
npm run test:integration

# E2E тесты
npm run test:e2e
```

## Безопасность

### Реализовано:
- ✅ Хеширование паролей (bcrypt)
- ✅ JWT токены с коротким временем жизни
- ✅ Refresh tokens с ротацией
- ✅ Rate limiting на эндпоинты
- ✅ Blacklist для отозванных токенов (Redis)
- ✅ CORS настройки
- ✅ Валидация входных данных
- ✅ Protection от timing attacks

### TODO:
- ⬜ Two-Factor Authentication (2FA)
- ⬜ Account lockout после N неудачных попыток
- ⬜ Аудит логирование (кто, когда, откуда)
- ⬜ IP whitelist/blacklist

## Зависимости

### От других модулей:
- **packages/shared** — общие типы
- **packages/validation** — схемы валидации

### Внешние зависимости:
- PostgreSQL — хранение пользователей
- Redis — сессии, blacklist токенов
- SMTP сервер — отправка писем

## Мониторинг и логи

```bash
# Логи сервиса
docker logs -f auth-service

# Метрики
GET /metrics
```

## Дополнительная информация

- [Архитектура аутентификации](../../general_docs/02_architecture/)
- [API документация](../../general_docs/05_resources/api/auth_service_api.md)
- [Схема базы данных](../../general_docs/05_resources/database/)
