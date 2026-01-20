---
type: project
description: Статические ресурсы: иконки, шрифты, брендинг
related:
  - shared/i18n.md
  - doc/structure.md
---

# Статические ресурсы (Assets)

Описание структуры и правил работы со статическими ресурсами в `/shared/assets/`.

> **Тип инструкции:** `project` — описывает конкретные ресурсы проекта. При инициализации заполнить под специфику проекта.

## Оглавление

- [Структура](#структура)
- [Категории ресурсов](#категории-ресурсов)
  - [Иконки](#иконки)
  - [Шрифты](#шрифты)
  - [Брендинг](#брендинг)
  - [Изображения](#изображения)
- [Правила](#правила)
- [Оптимизация](#оптимизация)
- [Примеры использования](#примеры-использования)
- [Связанные инструкции](#связанные-инструкции)

---

## Структура

```
/shared/
  /assets/
    /icons/                     # SVG иконки
      /ui/                      # UI иконки (кнопки, меню)
        arrow-left.svg
        arrow-right.svg
        check.svg
        close.svg
      /social/                  # Социальные сети
        facebook.svg
        twitter.svg
        linkedin.svg
      /status/                  # Статусы
        success.svg
        error.svg
        warning.svg
        info.svg
      index.ts                  # Экспорт всех иконок

    /fonts/                     # Шрифты
      /inter/                   # Основной шрифт
        Inter-Regular.woff2
        Inter-Medium.woff2
        Inter-Bold.woff2
      /fira-code/               # Моноширинный (код)
        FiraCode-Regular.woff2
      fonts.css                 # @font-face объявления

    /brand/                     # Брендинг
      /logo/
        logo.svg                # Основной логотип
        logo-dark.svg           # Для тёмной темы
        logo-small.svg          # Компактная версия
        logo.png                # PNG fallback (1024x1024)
      /colors/
        palette.json            # Цветовая палитра
        palette.css             # CSS переменные
      /guidelines/
        brand-guide.pdf         # Гайдлайны бренда

    /images/                    # Общие изображения
      /placeholders/            # Плейсхолдеры
        avatar-default.svg
        image-placeholder.svg
      /illustrations/           # Иллюстрации
        empty-state.svg
        error-404.svg
      /backgrounds/             # Фоны
        pattern.svg

    README.md                   # Документация по ресурсам
```

---

## Категории ресурсов

### Иконки

**Формат:** SVG (предпочтительно) или PNG.

**Правила именования:**

| Правило | Пример |
|---------|--------|
| kebab-case | `arrow-left.svg` |
| Описательное имя | `user-settings.svg`, не `icon1.svg` |
| Размер в имени (если фиксированный) | `logo-32x32.png` |

**Размеры SVG:**

```xml
<!-- Стандартный размер viewBox -->
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- ... -->
</svg>
```

| Категория | viewBox | Использование |
|-----------|---------|---------------|
| UI иконки | 24x24 | Кнопки, меню, формы |
| Маленькие | 16x16 | Inline, badges |
| Большие | 48x48 | Пустые состояния |

**Цвета в SVG:**

```xml
<!-- Используйте currentColor для наследования цвета -->
<svg fill="currentColor">
  <path d="..." />
</svg>
```

---

### Шрифты

**Формат:** WOFF2 (основной), WOFF (fallback).

**Структура fonts.css:**

```css
/* /shared/assets/fonts/fonts.css */

/* Inter — основной шрифт */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('./inter/Inter-Regular.woff2') format('woff2');
}

@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url('./inter/Inter-Medium.woff2') format('woff2');
}

@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url('./inter/Inter-Bold.woff2') format('woff2');
}

/* Fira Code — моноширинный */
@font-face {
  font-family: 'Fira Code';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('./fira-code/FiraCode-Regular.woff2') format('woff2');
}
```

**Правила:**

- `font-display: swap` — показывать fallback шрифт до загрузки
- Только используемые начертания (Regular, Medium, Bold)
- Подмножества (subset) для кириллицы + латиницы

---

### Брендинг

**Логотип:**

| Файл | Назначение | Размер |
|------|------------|--------|
| `logo.svg` | Основной (web) | Векторный |
| `logo-dark.svg` | Тёмная тема | Векторный |
| `logo-small.svg` | Favicon, мобильные | Векторный |
| `logo.png` | Social sharing, email | 1024x1024 |

**Цветовая палитра:**

```json
// /shared/assets/brand/colors/palette.json
{
  "primary": {
    "50": "#E3F2FD",
    "100": "#BBDEFB",
    "500": "#2196F3",
    "700": "#1976D2",
    "900": "#0D47A1"
  },
  "secondary": {
    "500": "#9C27B0"
  },
  "neutral": {
    "50": "#FAFAFA",
    "100": "#F5F5F5",
    "500": "#9E9E9E",
    "900": "#212121"
  },
  "semantic": {
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336",
    "info": "#2196F3"
  }
}
```

```css
/* /shared/assets/brand/colors/palette.css */
:root {
  --color-primary-50: #E3F2FD;
  --color-primary-500: #2196F3;
  --color-primary-700: #1976D2;

  --color-success: #4CAF50;
  --color-warning: #FF9800;
  --color-error: #F44336;
  --color-info: #2196F3;
}
```

---

### Изображения

**Форматы:**

| Формат | Когда использовать |
|--------|-------------------|
| SVG | Иллюстрации, иконки, паттерны |
| WebP | Фотографии (с PNG fallback) |
| PNG | Скриншоты, изображения с прозрачностью |
| JPEG | Фотографии без прозрачности |

**Плейсхолдеры:**

```
/images/placeholders/
  avatar-default.svg      # Дефолтный аватар
  image-placeholder.svg   # Заглушка для изображений
  product-placeholder.svg # Заглушка товара
```

---

## Правила

### Организация файлов

**Правило:** Один ресурс — один файл. Не объединять несколько иконок в спрайт.

**Правило:** Группировать по назначению, не по типу.

```
# Правильно
/icons/
  /ui/
  /social/
  /status/

# Неправильно
/svg/
/png/
/ico/
```

### Именование

| Правило | Пример |
|---------|--------|
| kebab-case | `arrow-left.svg` |
| Английский язык | `search.svg`, не `poisk.svg` |
| Без префиксов типа | `logo.svg`, не `svg-logo.svg` |
| Размер в имени (если нужен) | `favicon-32x32.png` |

### Версионирование

**Правило:** Изменение ресурса = новый hash в имени (для cache busting).

```
logo.svg           # Разработка
logo.abc123.svg    # Production (генерируется при сборке)
```

### Лицензии

**Правило:** Все ресурсы должны иметь подходящую лицензию.

```
/shared/assets/
  LICENSES.md       # Лицензии на шрифты, иконки
```

---

## Оптимизация

### SVG

**Инструмент:** SVGO

```bash
npx svgo icons/ui/*.svg --config svgo.config.js
```

**svgo.config.js:**

```javascript
module.exports = {
  plugins: [
    'removeDoctype',
    'removeComments',
    'removeMetadata',
    'removeEditorsNSData',
    'cleanupAttrs',
    'removeUselessDefs',
    'removeUnknownsAndDefaults',
    'removeEmptyContainers',
    'removeEmptyText',
    'removeEmptyAttrs',
    'cleanupNumericValues',
    'convertColors',
    'removeNonInheritableGroupAttrs',
    'sortAttrs',
    {
      name: 'removeViewBox',
      active: false  // Сохранять viewBox
    }
  ]
};
```

### Изображения

**Инструменты:**

| Формат | Инструмент |
|--------|------------|
| PNG | pngquant, optipng |
| JPEG | mozjpeg |
| WebP | cwebp |

**Размеры:**

| Использование | Максимальный размер |
|---------------|---------------------|
| Иконки | < 5 KB |
| Иллюстрации | < 50 KB |
| Фотографии | < 200 KB |

### Шрифты

**Subset:** Включать только нужные символы.

```bash
# Создание subset для кириллицы + латиницы
pyftsubset Inter-Regular.ttf \
  --unicodes="U+0000-00FF,U+0400-04FF" \
  --flavor=woff2 \
  --output-file=Inter-Regular.woff2
```

---

## Примеры использования

### Пример 1: Импорт иконок (React)

```tsx
// /shared/assets/icons/index.ts
export { ReactComponent as ArrowLeft } from './ui/arrow-left.svg';
export { ReactComponent as Check } from './ui/check.svg';
export { ReactComponent as Close } from './ui/close.svg';

// Использование
import { ArrowLeft, Check } from '@shared/assets/icons';

function Button() {
  return (
    <button>
      <ArrowLeft className="icon" />
      Назад
    </button>
  );
}
```

### Пример 2: Подключение шрифтов

```html
<!-- В HTML -->
<link rel="stylesheet" href="/shared/assets/fonts/fonts.css" />
```

```css
/* В CSS */
@import '/shared/assets/fonts/fonts.css';

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

code {
  font-family: 'Fira Code', monospace;
}
```

### Пример 3: Использование цветовой палитры

```tsx
// Импорт JSON
import palette from '@shared/assets/brand/colors/palette.json';

const primaryColor = palette.primary[500]; // #2196F3
```

```css
/* Использование CSS переменных */
@import '/shared/assets/brand/colors/palette.css';

.button-primary {
  background-color: var(--color-primary-500);
}

.alert-error {
  color: var(--color-error);
}
```

### Пример 4: Плейсхолдеры

```tsx
import defaultAvatar from '@shared/assets/images/placeholders/avatar-default.svg';

function UserAvatar({ src, alt }) {
  return (
    <img
      src={src || defaultAvatar}
      alt={alt}
      onError={(e) => { e.target.src = defaultAvatar; }}
    />
  );
}
```

---

## Связанные инструкции

- [i18n.md](i18n.md) — локализация (тексты в изображениях)
- [doc/structure.md](../doc/structure.md) — документация ресурсов
