# Packages (Общий переиспользуемый код)

Монорепо для общего кода, используемого в приложениях и сервисах.

## Структура

```
packages/
├── shared/               # Общие утилиты и типы
│   ├── src/
│   └── package.json
│
├── ui/                   # Общая UI библиотека
│   ├── components/
│   └── package.json
│
├── validation/           # Схемы валидации
│   ├── schemas/
│   └── package.json
│
└── config/               # Общие конфигурации
    ├── eslint-config/
    ├── tsconfig/
    └── prettier-config/
```

## Packages

### shared
Общие утилиты, константы и TypeScript типы

### ui
Переиспользуемые UI компоненты (кнопки, инпуты, модалы)

### validation
Схемы валидации (Zod, Yup, Joi)

### config
ESLint, TypeScript, Prettier конфигурации

## Использование

```typescript
// В apps/web или services/*
import { formatDate } from '@packages/shared';
import { Button } from '@packages/ui';
import { loginSchema } from '@packages/validation';
```
