---
description: Стандарт кодирования Tailwind CSS — палитра, z-слои, типографика, анимации, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: tailwind-css
---

# Стандарт Tailwind CSS v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | Tailwind CSS 4.x |
| Ключевые библиотеки | tailwindcss-animate 1.x (анимации), @tailwindcss/typography 0.5 (prose) |
| Линтер | eslint-plugin-tailwindcss (`tailwindcss/classnames-order`, `tailwindcss/no-contradicting-classname`) |
| Конфигурация | `tailwind.config.ts` — кастомная палитра, шрифты, z-index шкала |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| Кастомный цвет | семантическое имя по назначению, не по оттенку | `primary`, `surface`, `destructive` |
| Расширение палитры | `theme.extend.colors` в конфиге | `primary: { DEFAULT: '#2563eb', light: '#60a5fa' }` |
| Кастомный шрифт | `fontFamily` с fallback-стеком | `heading: ['Inter', 'sans-serif']` |
| Z-index токен | именованная шкала через `theme.extend.zIndex` | `dropdown: '100'`, `modal: '200'`, `toast: '300'` |
| Breakpoint | стандартные Tailwind (`sm`, `md`, `lg`, `xl`, `2xl`) | `md:grid-cols-2` |
| Компонентный класс | `@apply` запрещён за пределами base-слоя | Использовать composition через JSX |
| CSS-переменная | `--{category}-{name}` в kebab-case | `--color-primary`, `--font-heading` |

## Паттерны кода

### Подключение (PostCSS + Vite)

Tailwind подключается через PostCSS. В `globals.css` — директивы и CSS-переменные. В `main.tsx` — импорт `globals.css`.

```javascript
// postcss.config.js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

```css
/* styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --color-primary: #2563eb;
    --color-surface: #ffffff;
  }

  body {
    @apply font-body text-base antialiased;
  }
}
```

```tsx
// app/main.tsx — подключение стилей
import "../styles/globals.css";

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

### Кастомная палитра (Anti-Generic)

Проект использует семантическую палитру вместо дефолтных цветов Tailwind. Дефолтные цвета (`indigo-500`, `blue-600`, `purple-500`) запрещены в компонентах — они создают "пластиковый" AI-сгенерированный вид.

```typescript
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Семантическая палитра — все компоненты ссылаются на эти токены
        primary: {
          DEFAULT: "#2563eb",
          light: "#60a5fa",
          dark: "#1d4ed8",
        },
        surface: {
          DEFAULT: "#ffffff",
          secondary: "#f8fafc",
          tertiary: "#f1f5f9",
        },
        border: {
          DEFAULT: "#e2e8f0",
          strong: "#cbd5e1",
        },
        destructive: {
          DEFAULT: "#dc2626",
          light: "#fecaca",
        },
        muted: "#64748b",
      },
    },
  },
};

export default config;
```

Использование в компонентах:

```tsx
{/* ✅ Правильно: семантические токены */}
<button className="bg-primary text-white hover:bg-primary-dark">Save</button>
<div className="bg-surface-secondary border border-border">Card</div>

{/* ❌ Запрещено: дефолтные цвета Tailwind */}
<button className="bg-indigo-500 text-white hover:bg-indigo-600">Save</button>
<div className="bg-gray-50 border border-gray-200">Card</div>
```

### Система глубины (z-слои)

Три уровня глубины создают визуальную иерархию. Тени — многослойные и цветные, не плоский `shadow-md`.

```typescript
// tailwind.config.ts — extend
{
  zIndex: {
    base: "0",       // Основной контент
    dropdown: "100",  // Выпадающие меню
    sticky: "150",    // Sticky-элементы
    modal: "200",     // Модальные окна
    toast: "300",     // Уведомления
    tooltip: "400",   // Тултипы
  },
  boxShadow: {
    // Многослойные тени с цветовым оттенком вместо плоского shadow-md
    "elevated": "0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04)",
    "floating": "0 4px 16px rgba(0,0,0,0.12), 0 1px 4px rgba(0,0,0,0.06)",
    "overlay": "0 8px 32px rgba(0,0,0,0.16), 0 2px 8px rgba(0,0,0,0.08)",
  },
}
```

Использование:

```tsx
{/* Базовый слой — контент на странице */}
<div className="z-base bg-surface">Page content</div>

{/* Приподнятый слой — карточки */}
<div className="z-base shadow-elevated rounded-lg bg-surface p-6">Card</div>

{/* Плавающий слой — dropdown */}
<div className="z-dropdown shadow-floating rounded-md bg-surface">Menu</div>

{/* Оверлей — модальное окно */}
<div className="z-modal shadow-overlay rounded-xl bg-surface">Modal</div>
```

### Парные шрифты (типографика)

Заголовки и основной текст используют разные шрифты. Один шрифт для всего — признак AI-генерации.

```typescript
// tailwind.config.ts — extend
{
  fontFamily: {
    heading: ['"DM Serif Display"', 'Georgia', 'serif'],
    body: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['"JetBrains Mono"', 'Consolas', 'monospace'],
  },
}
```

```tsx
{/* Заголовки — serif, тело — sans-serif */}
<h1 className="font-heading text-4xl font-bold tracking-tight">Dashboard</h1>
<p className="font-body text-base text-muted leading-relaxed">
  Welcome to the admin panel. Here you can manage users and settings.
</p>
<code className="font-mono text-sm bg-surface-tertiary px-1.5 py-0.5 rounded">
  npm install
</code>
```

### Анимации (только transform и opacity)

Анимировать только `transform` и `opacity` — они не вызывают layout/paint. `transition-all` запрещён.

```tsx
{/* ✅ Правильно: конкретные свойства */}
<button className="transition-colors duration-200 hover:bg-primary-dark">
  Button
</button>

<div className="transition-transform duration-300 ease-out hover:scale-105">
  Card with hover
</div>

<div className="transition-opacity duration-200 opacity-0 data-[visible]:opacity-100">
  Fade in
</div>

{/* ❌ Запрещено: transition-all (триггерит layout для всех свойств) */}
<button className="transition-all duration-200">Bad</button>
```

### Полные интерактивные состояния

Каждый интерактивный элемент ДОЛЖЕН иметь hover, focus-visible и active. Пустой hover без визуального изменения — антипаттерн.

```tsx
<button
  className={[
    "rounded-lg px-4 py-2 text-sm font-medium",
    "bg-primary text-white",
    "hover:bg-primary-dark",                    // Hover: затемнение
    "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary", // Focus: обводка
    "active:scale-[0.98]",                      // Active: лёгкое сжатие
    "disabled:opacity-50 disabled:cursor-not-allowed", // Disabled
  ].join(" ")}
>
  Save changes
</button>
```

### Связь с SDD процессом

| Момент SDD | Действие с Tailwind CSS |
|------------|------------------------|
| Design (SVC-N § UI) | Определяет UI-сервис и компоненты. Цветовая схема и шрифты из секции "UI-компоненты" → значения для `tailwind.config.ts` |
| INFRA-блок (wave 0) | Dev-agent создаёт `tailwind.config.ts`: палитра из Design, шрифты, z-шкала, тени |
| Per-service блок | Dev-agent использует семантические токены из конфига, не дефолтные цвета |
| Design → DONE | Конфиг финализирован, все компоненты используют кастомные токены |

```typescript
// INFRA-блок: значения из Design (SVC-N § UI-компоненты → цветовая схема)
// primary: "#2563eb" ← Design → primary color
// heading font: "DM Serif Display" ← Design → typography
import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: { extend: { colors: { primary: "#2563eb" } } },
};
export default config;
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| Дефолтные цвета (`indigo-500`, `blue-600`, `purple-500`) | "Пластиковый" AI-вид, нет бренда, невозможно переключить тему | Семантические токены (`primary`, `surface`, `destructive`) |
| `shadow-md` / `shadow-lg` без кастомизации | Плоские серые тени без глубины | Многослойные цветные тени (`shadow-elevated`, `shadow-floating`) |
| Один шрифт для всего (`font-sans` везде) | Монотонная типографика, нет иерархии | Парные шрифты: serif для заголовков, sans-serif для текста |
| `transition-all` | Триггерит layout/paint для всех свойств, проседание FPS | `transition-colors`, `transition-transform`, `transition-opacity` |
| `@apply` в компонентах | Скрывает утилиты, ломает поиск по классам, теряется composition | Inline-классы в JSX, `@apply` только в `@layer base` |
| Магические z-index (`z-[999]`, `z-50`) | Коллизии слоёв, невозможно предсказать порядок | Именованная шкала (`z-dropdown`, `z-modal`, `z-toast`) |
| Hover без визуального отличия | Элемент кажется не интерактивным | Явное изменение цвета, тени или масштаба |
| `!important` через `!` модификатор | Нарушает каскад, усложняет отладку | Повысить специфичность через структуру разметки |

## Структура файлов

```
src/frontend/
├── tailwind.config.ts        # Кастомная палитра, шрифты, z-шкала, тени
├── postcss.config.js         # PostCSS с tailwindcss плагином
├── styles/
│   └── globals.css           # @tailwind base/components/utilities, CSS-переменные
├── components/
│   └── ui/                   # Shared UI-компоненты (Button, Card, Input)
├── app/
│   └── main.tsx              # Entry point — import "../styles/globals.css"
└── ...
```

> **Согласованность с React:** Плоская структура `src/frontend/` без вложенного `src/` — как в [standard-react.md](/specs/docs/.technologies/standard-react.md).

Правила размещения:
- `tailwind.config.ts` — единственный источник правды для палитры, шрифтов, z-index
- `globals.css` — только `@tailwind` директивы и CSS-переменные для тем
- `@apply` допустим только в `globals.css` в `@layer base` для reset-стилей
- Компоненты используют inline-классы Tailwind в JSX

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется линтером: `eslint --ext .ts,.tsx src/{svc}/frontend/` с плагином `eslint-plugin-tailwindcss`. Pre-commit hook `eslint` запускает проверку для изменённых `.ts`/`.tsx` файлов.*

## Тестирование

*Тестирование не применимо — Tailwind CSS является декларативным CSS-фреймворком, не исполняемым кодом. Визуальное тестирование (Chromatic, Percy) опционально и настраивается per-service. Корректность классов проверяется линтером.*

## Логирование

*Логирование не применимо — технология не генерирует событий, требующих логирования.*
