# Users Service (Сервис управления пользователями)

Сервис отвечает за управление профилями и данными пользователей.

## Функциональность

- ✅ Управление профилями пользователей
- ✅ Обновление личных данных
- ✅ Загрузка аватаров
- ✅ Настройки пользователя
- ✅ Роли и права доступа (RBAC)
- ✅ История активности пользователя
- ✅ Управление подписками/тарифами

## Структура

```
users/
├── src/                   # Исходный код сервиса
├── tests/                 # Тесты сервиса
├── static/                # Статические файлы (аватары по умолчанию)
├── .env.example           # Пример переменных окружения
├── Dockerfile             # Docker конфигурация
├── package.json           # Зависимости (Node.js)
│                          # или requirements.txt (Python)
│                          # или go.mod (Go)
└── README.md              # Этот файл
```

## Технологический стек

**TODO:** Выбрать стек для users сервиса:
- Node.js + Express + TypeScript
- Python + FastAPI/Django
- Go + Gin/Fiber
- Другой вариант

## Переменные окружения

```bash
cp .env.example .env
```

### Основные переменные

```env
# Порт сервиса
PORT=8002

# База данных
DATABASE_URL=postgresql://user:password@postgres:5432/users_db

# Redis для кэширования профилей
REDIS_URL=redis://redis:6379

# Файловое хранилище для аватаров
STORAGE_TYPE=s3  # или local
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET=user-avatars
AWS_REGION=us-east-1

# Локальное хранилище (если STORAGE_TYPE=local)
UPLOAD_DIR=./uploads/avatars
MAX_FILE_SIZE=5mb

# Auth Service (для валидации токенов)
AUTH_SERVICE_URL=http://auth:8001
```

## API Эндпоинты

### Профиль пользователя

```
GET    /api/users/me                 # Получить свой профиль
PUT    /api/users/me                 # Обновить свой профиль
DELETE /api/users/me                 # Удалить свой аккаунт
```

### Управление пользователями (admin)

```
GET    /api/users                    # Список пользователей (пагинация)
GET    /api/users/:id                # Получить пользователя по ID
PUT    /api/users/:id                # Обновить пользователя (admin)
DELETE /api/users/:id                # Удалить пользователя (admin)
```

### Аватар

```
POST   /api/users/me/avatar          # Загрузить аватар
DELETE /api/users/me/avatar          # Удалить аватар
GET    /api/users/:id/avatar         # Получить URL аватара
```

### Настройки

```
GET    /api/users/me/settings        # Получить настройки
PUT    /api/users/me/settings        # Обновить настройки
```

### Роли и права

```
GET    /api/users/:id/roles          # Получить роли пользователя
POST   /api/users/:id/roles          # Назначить роль (admin)
DELETE /api/users/:id/roles/:roleId  # Убрать роль (admin)
GET    /api/users/:id/permissions    # Получить права
```

### История активности

```
GET    /api/users/me/activity        # История своей активности
GET    /api/users/:id/activity       # История активности (admin)
```

## Схема данных

### UserProfile

```typescript
interface UserProfile {
  id: string;
  userId: string;              // Связь с Auth Service
  email: string;               // Дубликат для быстрого доступа

  // Личная информация
  firstName: string;
  lastName: string;
  displayName: string;
  bio?: string;
  avatarUrl?: string;

  // Контактная информация
  phone?: string;
  country?: string;
  city?: string;
  timezone?: string;
  language: string;

  // Метаданные
  createdAt: Date;
  updatedAt: Date;
  lastActiveAt: Date;
}
```

### UserSettings

```typescript
interface UserSettings {
  userId: string;

  // Уведомления
  emailNotifications: boolean;
  pushNotifications: boolean;
  notificationFrequency: 'instant' | 'daily' | 'weekly';

  // Приватность
  profileVisibility: 'public' | 'private' | 'friends';
  showEmail: boolean;
  showPhone: boolean;

  // Интерфейс
  theme: 'light' | 'dark' | 'auto';
  language: string;
}
```

### UserRole

```typescript
interface UserRole {
  userId: string;
  roleId: string;
  assignedAt: Date;
  assignedBy: string;
}

interface Role {
  id: string;
  name: 'admin' | 'moderator' | 'user' | 'premium';
  permissions: string[];
  description: string;
}
```

### ActivityLog

```typescript
interface ActivityLog {
  id: string;
  userId: string;
  action: string;             // 'profile_updated', 'avatar_uploaded', etc.
  details?: object;
  ipAddress: string;
  userAgent: string;
  createdAt: Date;
}
```

## Взаимодействие с другими сервисами

### Auth Service
При регистрации нового пользователя:
```
Auth Service → Users Service (создать профиль)
```

Валидация запросов:
```
Users Service → Auth Service (проверить токен, получить userId)
```

### API Gateway
Все запросы идут через Gateway:
```
Client → API Gateway → Users Service
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
docker build -t users-service .
docker run -p 8002:8002 users-service
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

## Кэширование

Для оптимизации используется Redis кэш:
- Профили пользователей (TTL: 5 минут)
- Настройки пользователей (TTL: 10 минут)
- Списки с пагинацией (TTL: 1 минута)

Инвалидация кэша при обновлении данных.

## Загрузка файлов

### Поддерживаемые форматы аватаров:
- JPG/JPEG
- PNG
- WebP
- GIF (статические)

### Ограничения:
- Максимальный размер: 5 МБ
- Автоматическое изменение размера: 400x400px
- Сжатие качества: 85%

## Безопасность

- ✅ Валидация всех входных данных
- ✅ Защита от injection атак
- ✅ Rate limiting на эндпоинты
- ✅ Проверка прав доступа (RBAC)
- ✅ Sanitization загружаемых файлов
- ✅ CORS настройки

## Зависимости

### От других модулей:
- **packages/shared** — общие типы
- **packages/validation** — схемы валидации

### От других сервисов:
- **Auth Service** — валидация токенов

### Внешние зависимости:
- PostgreSQL — хранение профилей
- Redis — кэширование
- S3/Local Storage — хранение аватаров

## Мониторинг

```bash
# Логи сервиса
docker logs -f users-service

# Метрики
GET /metrics

# Health check
GET /health
```

## Дополнительная информация

- [Архитектура](../../general_docs/architecture/)
- [API документация](../../general_docs/resources/api/users_service_api.md)
- [Схема базы данных](../../general_docs/resources/database/)
