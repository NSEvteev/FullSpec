# Backend Template

> **Источник:** [/.claude/instructions/doc/structure.md](/.claude/instructions/doc/structure.md#шаблон-backend-handlers-services-controllers)

Шаблон документации для backend-кода: handlers, services, controllers.

---

## Шаблон

```markdown
# {Название модуля}

> Исходный код: [{filename}](/{path-to-source})

{Краткое описание — 1-2 предложения}

## API

### {FunctionName}

{Описание функции}

**Сигнатура:**
\`\`\`{language}
{signature}
\`\`\`

**Параметры:**
| Параметр | Тип | Описание |
|----------|-----|----------|
| {name} | {type} | {description} |

**Возвращает:** {return type and description}

**Ошибки:**
| Код | Описание |
|-----|----------|
| 400 | Невалидные данные |
| 401 | Не авторизован |

## Примеры

\`\`\`{language}
// Пример вызова
{example}
\`\`\`

## Зависимости

- [{dependency}](/{path}) — {description}
```

---

<!-- Пример заполнения

# Auth Handlers

> Исходный код: [handlers.ts](/src/auth/backend/handlers.ts)

Обработчики HTTP-запросов для аутентификации и авторизации пользователей.

## API

### login

Аутентификация пользователя по email и паролю.

**Сигнатура:**
```typescript
async function login(request: LoginRequest): Promise<AuthResponse>
```

**Параметры:**
| Параметр | Тип | Описание |
|----------|-----|----------|
| email | string | Email пользователя |
| password | string | Пароль пользователя |

**Возвращает:** `AuthResponse` — объект с JWT токенами (access + refresh).

**Ошибки:**
| Код | Описание |
|-----|----------|
| 400 | Некорректный email или пароль |
| 401 | Неверные учётные данные |
| 429 | Превышен лимит попыток |

## Примеры

```typescript
const response = await login({
  email: 'user@example.com',
  password: 'SecurePass123!'
});

console.log(response.accessToken);
```

## Зависимости

- [UserService](/src/users/backend/service.ts) — получение данных пользователя
- [TokenService](/src/auth/backend/token-service.ts) — генерация JWT

-->
