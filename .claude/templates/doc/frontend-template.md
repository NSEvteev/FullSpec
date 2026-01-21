# Frontend Template

> **Источник:** [/.claude/instructions/doc/structure.md](/.claude/instructions/doc/structure.md#шаблон-frontend-components-pages)

Шаблон документации для frontend-компонентов и страниц.

---

## Шаблон

```markdown
# {Название компонента}

> Исходный код: [{filename}](/{path-to-source})

{Описание компонента}

## Props

| Prop | Тип | Обязательный | Описание |
|------|-----|:------------:|----------|
| {name} | {type} | +/- | {description} |

## События

| Событие | Payload | Описание |
|---------|---------|----------|
| onClick | `{type}` | {description} |

## Примеры

\`\`\`tsx
<{Component} prop={value} />
\`\`\`

## Зависимости

- [{component}](/{path}) — {description}
```

---

<!-- Пример заполнения

# LoginForm

> Исходный код: [LoginForm.tsx](/src/auth/frontend/components/LoginForm.tsx)

Форма аутентификации пользователя с валидацией и обработкой ошибок.

## Props

| Prop | Тип | Обязательный | Описание |
|------|-----|:------------:|----------|
| onSuccess | `(user: User) => void` | + | Callback при успешном логине |
| onError | `(error: Error) => void` | - | Callback при ошибке |
| redirectUrl | `string` | - | URL для редиректа после логина |
| showRegisterLink | `boolean` | - | Показывать ссылку на регистрацию |

## События

| Событие | Payload | Описание |
|---------|---------|----------|
| onSubmit | `LoginCredentials` | Отправка формы |
| onForgotPassword | `void` | Клик по "Забыли пароль?" |

## Состояния

| Состояние | Описание |
|-----------|----------|
| idle | Начальное состояние |
| loading | Отправка запроса |
| error | Ошибка аутентификации |
| success | Успешный вход |

## Примеры

### Базовое использование

```tsx
<LoginForm
  onSuccess={(user) => navigate('/dashboard')}
/>
```

### С обработкой ошибок

```tsx
<LoginForm
  onSuccess={(user) => navigate('/dashboard')}
  onError={(error) => toast.error(error.message)}
  showRegisterLink={true}
/>
```

### С редиректом

```tsx
<LoginForm
  onSuccess={(user) => navigate('/dashboard')}
  redirectUrl="/welcome"
/>
```

## Зависимости

- [Button](/src/shared/components/Button.tsx) — кнопка отправки
- [Input](/src/shared/components/Input.tsx) — поля ввода
- [useAuth](/src/auth/frontend/hooks/useAuth.ts) — хук аутентификации
- [validateEmail](/src/shared/utils/validation.ts) — валидация email

-->
