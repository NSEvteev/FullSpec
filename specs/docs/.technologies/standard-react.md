---
description: Стандарт кодирования React — конвенции именования, компоненты, хуки, TanStack Query, Zustand, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: react
---

# Стандарт React v1.1

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | React 18 |
| Ключевые библиотеки | TanStack Query (tanstack/react-query) 5.x, Zustand 4.x, react-router-dom 6.x, TypeScript 5.x, Vite 5.x |
| Конфигурация | `src/frontend/vite.config.ts`, `src/frontend/tsconfig.json`; TanStack Query: `QueryClient` в `src/frontend/app/providers.tsx`; Zustand: store-файлы в `src/frontend/store/` |

### Конфигурация Vite в монорепо

В монорепо используется **плоская структура**: `src/frontend/` содержит код напрямую, без вложенного `src/`. Scaffold Vite создаёт `src/` при инициализации — эта вложенность убирается.

**Расположение файлов в корне сервиса (`src/frontend/`):**

| Файл | Назначение |
|------|-----------|
| `vite.config.ts` | Конфигурация сборки |
| `tsconfig.json` | Конфигурация TypeScript |
| `index.html` | Entry HTML (Vite dev server) |
| `app/main.tsx` | Entry point React (ReactDOM.createRoot) |

**Пример `vite.config.ts`:**

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, '.'),
    },
  },
});
```

**Ключевые моменты:**
- `index.html` в корне сервиса (`src/frontend/index.html`), не в `src/frontend/src/`
- Entry point: `app/main.tsx` (относительно корня сервиса)
- Alias `@` указывает на корень сервиса для удобных импортов (`@/components/...`, `@/store/...`)

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| Компонент (файл) | PascalCase, `.tsx` | `UserCard.tsx`, `LoginForm.tsx` |
| Компонент (функция) | PascalCase | `function UserCard(props: UserCardProps)` |
| Хук (файл) | camelCase с префиксом `use`, `.ts` | `useAuth.ts`, `useUserList.ts` |
| Хук (функция) | camelCase с префиксом `use` | `useAuth`, `useUserList` |
| Пропсы (интерфейс) | `{ComponentName}Props` | `UserCardProps`, `LoginFormProps` |
| Store (Zustand, файл) | camelCase с суффиксом `Store`, `.ts` | `authStore.ts`, `uiStore.ts` |
| Store (Zustand, хук) | camelCase с префиксом `use` + суффиксом `Store` | `useAuthStore`, `useUiStore` |
| TanStack Query ключ | массив строк, kebab-case элементы | `['users', 'list']`, `['users', userId]` |
| Страница (файл) | PascalCase с суффиксом `Page`, `.tsx` | `UserListPage.tsx`, `LoginPage.tsx` |
| Папка компонента | kebab-case | `user-card/`, `login-form/` |
| CSS-модуль | `{ComponentName}.module.css` | `UserCard.module.css` |
| Контекст | PascalCase с суффиксом `Context` | `ThemeContext`, `AuthContext` |
| Enum / константа | UPPER_SNAKE_CASE | `USER_ROLES`, `API_ENDPOINTS` |

## Паттерны кода

### Компонент с пропсами

Стандартный функциональный компонент с явным интерфейсом пропсов. Экспорт — именованный. Деструктуризация пропсов прямо в параметре.

```tsx
interface UserCardProps {
  userId: string;
  name: string;
  email: string;
  onSelect?: (userId: string) => void;
}

export function UserCard({ userId, name, email, onSelect }: UserCardProps) {
  return (
    <div className="user-card" onClick={() => onSelect?.(userId)}>
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
}
```

### TanStack Query — запрос данных (useQuery)

Использовать при получении данных с сервера. Ключ запроса — массив строк. Функция запроса возвращает типизированные данные. Обрабатывать состояния `isLoading`, `isError`, `data`.

```tsx
import { useQuery } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

async function fetchUsers(): Promise<User[]> {
  const response = await fetch('/api/v1/users');
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  return response.json();
}

export function UserList() {
  const { data: users, isLoading, isError, error } = useQuery<User[], Error>({
    queryKey: ['users', 'list'],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000, // 5 минут
  });

  if (isLoading) return <div>Загрузка...</div>;
  if (isError) return <div>Ошибка: {error.message}</div>;

  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>{user.name} — {user.email}</li>
      ))}
    </ul>
  );
}
```

### TanStack Query — мутация данных (useMutation)

Использовать при изменении данных (POST/PUT/DELETE). После успешной мутации инвалидировать связанные запросы через `queryClient.invalidateQueries`.

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface CreateUserPayload {
  name: string;
  email: string;
}

interface User {
  id: string;
  name: string;
  email: string;
}

async function createUser(payload: CreateUserPayload): Promise<User> {
  const response = await fetch('/api/v1/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  return response.json();
}

export function CreateUserForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation<User, Error, CreateUserPayload>({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users', 'list'] });
    },
    onError: (error) => {
      console.error('Ошибка создания пользователя:', error.message);
    },
  });

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    mutation.mutate({
      name: data.get('name') as string,
      email: data.get('email') as string,
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" placeholder="Имя" required />
      <input name="email" type="email" placeholder="Email" required />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Создание...' : 'Создать'}
      </button>
      {mutation.isError && <p>Ошибка: {mutation.error.message}</p>}
    </form>
  );
}
```

### Zustand — определение store

Каждый store — отдельный файл. Store содержит состояние и экшены в одном объекте. Использовать `immer`-middleware только при сложной вложенности. Экспортировать типизированный хук.

```ts
import { create } from 'zustand';

interface AuthState {
  userId: string | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (userId: string, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  userId: null,
  token: null,
  isAuthenticated: false,
  login: (userId, token) =>
    set({ userId, token, isAuthenticated: true }),
  logout: () =>
    set({ userId: null, token: null, isAuthenticated: false }),
}));
```

### Zustand — использование store в компоненте

Подписываться только на нужные поля через селектор — предотвращает лишние перерендеры.

```tsx
import { useAuthStore } from '@/store/authStore';

export function Header() {
  // Подписка только на нужные поля
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const logout = useAuthStore((state) => state.logout);

  return (
    <header>
      {isAuthenticated ? (
        <button onClick={logout}>Выйти</button>
      ) : (
        <a href="/login">Войти</a>
      )}
    </header>
  );
}
```

### Пользовательский хук

Инкапсулировать логику в хуки — компонент содержит только рендеринг. Хук объединяет TanStack Query, Zustand и локальное состояние.

```ts
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '@/store/authStore';

interface User {
  id: string;
  name: string;
  email: string;
}

async function fetchCurrentUser(userId: string): Promise<User> {
  const response = await fetch(`/api/v1/users/${userId}`);
  if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
  return response.json();
}

export function useCurrentUser() {
  const userId = useAuthStore((state) => state.userId);

  const query = useQuery<User, Error>({
    queryKey: ['users', userId],
    queryFn: () => fetchCurrentUser(userId!),
    enabled: !!userId, // Запрос только при наличии userId
  });

  return {
    user: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    error: query.error,
  };
}
```

### Настройка QueryClient и провайдеры

Точка входа приложения — все провайдеры в одном файле `providers.tsx`. QueryClient создаётся вне компонента.

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,       // 1 минута — данные считаются свежими
      retry: 2,                    // Повторить 2 раза при ошибке
      refetchOnWindowFocus: false, // Не рефетчить при фокусе окна
    },
    mutations: {
      retry: 0, // Мутации не повторять
    },
  },
});

interface ProvidersProps {
  children: React.ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
}
```

### Роутинг (React Router)

Использовать `createBrowserRouter` + `RouterProvider` (React Router 6.4+). Описывать маршруты декларативно. Страницы — компоненты с суффиксом `Page`. Вложенные маршруты — через `children`.

```tsx
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';
import { UserListPage } from '@/pages/UserListPage';
import { LoginPage } from '@/pages/LoginPage';
import { NotFoundPage } from '@/pages/NotFoundPage';

// Layout-компонент для маршрутов с навигацией
function AppLayout() {
  return (
    <div className="app-layout">
      <header>Navigation</header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <UserListPage /> },
      { path: 'login', element: <LoginPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
]);

export function App() {
  return <RouterProvider router={router} />;
}
```

Добавить `RouterProvider` в `providers.tsx` или `main.tsx` — на одном уровне с `QueryClientProvider`.

### Обработка ошибок

Использовать Error Boundary для компонентного дерева. Для асинхронных ошибок — состояния TanStack Query (`isError`). Глобальные ошибки обрабатывать в `QueryClient.defaultOptions`.

```tsx
import { Component, type ReactNode } from 'react';

interface ErrorBoundaryProps {
  fallback: ReactNode;
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('ErrorBoundary caught:', error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| Использовать `useState` + `useEffect` для серверных данных | Race condition, дублирование логики кэширования, нет retry/stale — данные устаревают незаметно | Использовать `useQuery` из TanStack Query |
| Хранить серверные данные в Zustand store | Дублирование кэша TanStack Query, рассинхронизация при мутациях, ручное управление стейлом | Серверный стейт — в TanStack Query; Zustand — только для UI/клиентского состояния |
| Подписка на весь store целиком: `useAuthStore()` | Каждое изменение любого поля вызывает перерендер компонента | Использовать селектор: `useAuthStore((state) => state.userId)` |
| Default export для компонентов | Имя теряется при импорте, рефакторинг сложнее, плохо работает с Fast Refresh | Named export: `export function UserCard(...)` |
| Пропсы без TypeScript-интерфейса | Нет автодополнения, ошибки типов появляются в рантайме | Всегда объявлять `interface {Component}Props` перед компонентом |
| Inline-функции в JSX как event handlers | Новая функция на каждый рендер, дочерние компоненты перерендериваются | Определять обработчики вне JSX или через `useCallback` (только при реальной проблеме) |
| QueryKey без полной зависимости от параметров | Кэш возвращает данные для другого userId/фильтра | `queryKey: ['users', userId, filters]` — включать все параметры, влияющие на результат |
| Создавать новый `QueryClient` внутри компонента | QueryClient пересоздаётся на каждый рендер, кэш сбрасывается | Создавать `QueryClient` вне компонента (на уровне модуля) |
| Мутировать состояние Zustand напрямую | Zustand не увидит изменение, компоненты не перерендерятся | Использовать `set(...)` внутри экшена store |
| `useEffect` без зависимостей как componentDidMount | Скрытые баги с Strict Mode (двойной вызов в dev), потенциальная утечка подписок | Явно указывать массив зависимостей; использовать cleanup-функцию |

## Структура файлов

```
src/frontend/
├── app/
│   ├── main.tsx            # Точка входа: ReactDOM.createRoot
│   └── providers.tsx       # QueryClientProvider, ErrorBoundary и пр.
├── pages/
│   └── UserListPage.tsx    # Страница-маршрут (роутер подключается здесь)
├── components/
│   └── user-card/
│       ├── UserCard.tsx    # Компонент
│       └── UserCard.module.css
├── hooks/
│   ├── useCurrentUser.ts   # Пользовательский хук (TanStack Query + логика)
│   └── useAuth.ts          # Хук аутентификации
├── store/
│   ├── authStore.ts        # Zustand store: аутентификация
│   └── uiStore.ts          # Zustand store: UI-состояние (модалки, тема)
├── api/
│   └── users.ts            # Fetch-функции (передаются в queryFn)
├── types/
│   └── user.ts             # Общие TypeScript-интерфейсы
└── utils/
    └── formatDate.ts       # Утилиты без зависимости от React
```

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется вручную по чек-листу из [validation-technology.md](../../.instructions/docs/technology/validation-technology.md).*

Ключевые проверки при code review:
- Все компоненты именованно экспортируются (no default export)
- Серверный стейт через TanStack Query, не `useState`+`useEffect`
- `queryKey` включает все параметры запроса
- Zustand-селекторы (не весь store)
- TypeScript-интерфейс для каждого компонента
- `QueryClient` создан вне компонента

## Тестирование

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| Фреймворк | `vitest 1.x` | Test runner (интеграция с Vite) |
| DOM | `@testing-library/react 14.x` | Рендер компонентов, запросы к DOM |
| User events | `@testing-library/user-event 14.x` | Симуляция действий пользователя |
| TanStack Query | `@tanstack/react-query` (встроен) | Использовать `QueryClientWrapper` в фикстурах |
| Mocks | `vitest` (встроен) | `vi.fn()`, `vi.spyOn()`, `vi.mock()` |
| jsdom | `jsdom` (через vitest config) | Эмуляция браузерного DOM |

### Фикстуры

Обёртка для рендеринга компонентов с провайдерами. Создать один раз — использовать во всех тестах.

```tsx
import { render, type RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import type { ReactNode } from 'react';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },   // Не повторять в тестах — быстрее и предсказуемее
      mutations: { retry: false },
    },
  });
}

interface WrapperProps {
  children: ReactNode;
}

function createWrapper() {
  const queryClient = createTestQueryClient();
  function Wrapper({ children }: WrapperProps) {
    return (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );
  }
  return { Wrapper, queryClient };
}

export function renderWithProviders(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  const { Wrapper, queryClient } = createWrapper();
  return {
    ...render(ui, { wrapper: Wrapper, ...options }),
    queryClient,
  };
}
```

### Мокирование

- **Компоненты без запросов (unit):** рендерить напрямую, проверять DOM через `@testing-library/react`.
- **TanStack Query запросы:** мокировать `fetch` (через `vi.stubGlobal`) или сам `queryFn`. Использовать `waitFor` для асинхронных обновлений DOM.
- **Zustand store:** сбрасывать состояние между тестами через `useStore.setState({...})`. Не мокировать сам store.
- **Сложные зависимости (роутер, контекст):** использовать реальные провайдеры в `renderWithProviders`.

```tsx
import { vi, beforeEach } from 'vitest';
import { useAuthStore } from '@/store/authStore';

// Мок fetch для TanStack Query
const mockFetch = vi.fn();
vi.stubGlobal('fetch', mockFetch);

beforeEach(() => {
  // Сброс Zustand store между тестами
  useAuthStore.setState({
    userId: null,
    token: null,
    isAuthenticated: false,
  });
  mockFetch.mockReset();
});

// Настройка ответа fetch
mockFetch.mockResolvedValueOnce({
  ok: true,
  json: async () => ([{ id: '1', name: 'Alice', email: 'alice@example.com' }]),
} as Response);
```

### Паттерны тестов

```tsx
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderWithProviders } from '@/test/utils';
import { UserList } from '@/components/user-list/UserList';
import { CreateUserForm } from '@/components/create-user-form/CreateUserForm';

// --- Unit-тест компонента без запросов ---
import { UserCard } from '@/components/user-card/UserCard';

describe('UserCard', () => {
  it('отображает имя и email пользователя', () => {
    renderWithProviders(<UserCard userId="1" name="Alice" email="alice@example.com" />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
  });
});

// --- Integration-тест с TanStack Query ---
describe('UserList', () => {
  const mockFetch = vi.fn();

  beforeEach(() => {
    vi.stubGlobal('fetch', mockFetch);
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => [
        { id: '1', name: 'Alice', email: 'alice@example.com' },
      ],
    } as Response);
  });

  it('загружает и отображает список пользователей', async () => {
    renderWithProviders(<UserList />);

    // Показывает загрузку
    expect(screen.getByText('Загрузка...')).toBeInTheDocument();

    // После загрузки — данные
    await waitFor(() => {
      expect(screen.getByText('Alice')).toBeInTheDocument();
    });
  });

  it('показывает ошибку при сбое запроса', async () => {
    mockFetch.mockResolvedValue({ ok: false, status: 500 } as Response);
    renderWithProviders(<UserList />);

    await waitFor(() => {
      expect(screen.getByText(/ошибка/i)).toBeInTheDocument();
    });
  });
});

// --- Тест мутации (useMutation) ---
describe('CreateUserForm', () => {
  it('вызывает POST и инвалидирует кэш после успеха', async () => {
    const user = userEvent.setup();
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ id: '2', name: 'Bob', email: 'bob@example.com' }),
    } as Response);
    vi.stubGlobal('fetch', mockFetch);

    renderWithProviders(<CreateUserForm />);
    await user.type(screen.getByPlaceholderText('Имя'), 'Bob');
    await user.type(screen.getByPlaceholderText('Email'), 'bob@example.com');
    await user.click(screen.getByRole('button', { name: /создать/i }));

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith(
        '/api/v1/users',
        expect.objectContaining({ method: 'POST' })
      );
    });
  });
});
```

## Логирование

*Логирование не применимо — технология не генерирует событий, требующих логирования.*
