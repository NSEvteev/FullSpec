# Web UI (Фронтенд)

Клиентское веб-приложение проекта.

## Структура

```
web/
├── public/                # Статические файлы (favicon, robots.txt, images)
├── src/                   # Исходный код фронтенда
├── tests/                 # Тесты фронтенда
├── .env.example           # Пример переменных окружения
├── package.json           # Зависимости (после выбора стека)
└── README.md              # Этот файл
```

## Технологический стек

**TODO:** Выбрать и настроить стек фронтенда:
- React + TypeScript + Vite
- Vue 3 + TypeScript + Vite
- Next.js
- Другой вариант

## Переменные окружения

После выбора стека создать `.env` файл на основе `.env.example`:

```bash
cp .env.example .env
```

## Установка зависимостей

```bash
# TODO: Добавить команду после выбора стека
# Например для npm:
npm install

# Для yarn:
yarn install

# Для pnpm:
pnpm install
```

## Запуск в режиме разработки

```bash
# TODO: Добавить команду после выбора стека
# Например:
npm run dev
```

Приложение будет доступно по адресу: http://localhost:3000

## Сборка для продакшена

```bash
# TODO: Добавить команду после выбора стека
# Например:
npm run build
```

## Тестирование

```bash
# TODO: Добавить команду после выбора стека
# Например:
npm test
```

## Интеграция с бэкендом

Фронтенд взаимодействует с бэкенд-сервисами через API Gateway:
- **API Gateway URL:** `http://localhost:8000` (dev) / настраивается через .env

### Основные эндпоинты

- **Auth Service:** `/api/auth/*`
  - POST `/api/auth/login` — авторизация
  - POST `/api/auth/register` — регистрация
  - POST `/api/auth/logout` — выход
  - POST `/api/auth/refresh` — обновление токена

- **Users Service:** `/api/users/*`
  - GET `/api/users/me` — текущий пользователь
  - PUT `/api/users/me` — обновить профиль
  - GET `/api/users/:id` — получить пользователя по ID

## Структура src/ (рекомендуемая)

После выбора стека рекомендуется следующая структура:

```
src/
├── assets/               # Изображения, шрифты, стили
├── components/           # Переиспользуемые компоненты
│   ├── common/           # Общие компоненты (Button, Input, etc.)
│   ├── layout/           # Компоненты layout (Header, Footer, Sidebar)
│   └── features/         # Специфичные компоненты функций
├── pages/                # Страницы приложения
│   ├── auth/             # Страницы авторизации
│   ├── profile/          # Страницы профиля
│   └── dashboard/        # Дашборд
├── hooks/                # Custom hooks
├── services/             # API клиенты
│   ├── api.ts            # Базовый API клиент
│   ├── auth.service.ts   # Auth API
│   └── users.service.ts  # Users API
├── store/                # State management (Redux/Zustand/Pinia)
├── utils/                # Утилиты
├── types/                # TypeScript типы
├── config/               # Конфигурации
├── App.tsx               # Главный компонент
└── main.tsx              # Точка входа
```

## Зависимости от других модулей

- **packages/shared** — общие типы и утилиты
- **packages/ui** — общая UI библиотека (если создана)
- **packages/validation** — схемы валидации

## Дополнительная информация

- [Документация архитектуры](../../general_docs/02_architecture/)
- [API документация](../../general_docs/05_resources/api/)
