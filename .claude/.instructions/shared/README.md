# Инструкции /shared/

Индекс инструкций для работы с общим кодом и ресурсами в `/shared/`, а также общие правила для скиллов.

**Содержание:** общие библиотеки, статические ресурсы, локализация, API контракты, события, определение scope.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [0. Scope](#0-scope) | [scope.md](./scope.md) | **Определение scope (claude/project)** |
| [1. Libs](#1-libs) | [libs.md](./libs.md) | Общие библиотеки: errors, logging, validation |
| [2. Assets](#2-assets) | [assets.md](./assets.md) | Статические ресурсы: иконки, шрифты, брендинг |
| [3. I18n](#3-i18n) | [i18n.md](./i18n.md) | Локализация: ключи, плюрализация, форматирование |
| [4. Contracts](#4-contracts) | [contracts.md](./contracts.md) | API контракты: OpenAPI, Protobuf, JSON Schema |
| [5. Events](#5-events) | [events.md](./events.md) | События: naming, идемпотентность, DLQ |

---

# 0. Scope

Определение scope (claude/project) для test-* и doc-* скиллов.

**Содержание:** алгоритм автоопределения scope по пути, маппинг путей, правила для тестов и документации.

| Scope | Описание |
|-------|----------|
| `claude` | Инструменты Claude (скиллы, инструкции, агенты) |
| `project` | Код и документация проекта |

**Используется в:** test-*, doc-* скиллы

**Инструкция:** [scope.md](./scope.md)

---

# 1. Libs

Описание переиспользуемых библиотек в `/shared/libs/`. Каждая библиотека решает одну задачу и используется всеми сервисами.

**Содержание:** структура библиотек, API каждой библиотеки (errors, logging, validation, http-client, features), правила версионирования, документация, тесты.

| Библиотека | Назначение |
|------------|------------|
| `errors` | Единый формат ошибок (коды AUTH_, VAL_, DB_) |
| `logging` | Структурированное логирование JSON |
| `validation` | Переиспользуемые валидаторы |
| `http-client` | HTTP клиент с retry и circuit breaker |
| `features` | Проверка feature flags |

**Инструкция:** [libs.md](./libs.md)

---

# 2. Assets

Описание структуры и правил работы со статическими ресурсами в `/shared/assets/`.

**Содержание:** структура (icons, fonts, brand, images), форматы (SVG, WOFF2, WebP), правила именования (kebab-case), оптимизация (SVGO, pngquant), лицензии.

| Категория | Формат | Примеры |
|-----------|--------|---------|
| Иконки | SVG (viewBox 24x24) | arrow-left.svg, check.svg |
| Шрифты | WOFF2 | Inter, Fira Code |
| Логотипы | SVG + PNG fallback | logo.svg, logo-dark.svg |
| Изображения | SVG, WebP, PNG | placeholders, illustrations |

**Инструкция:** [assets.md](./assets.md)

---

# 3. I18n

Правила интернационализации и локализации приложения. Структура переводов, формат ключей, работа с плюрализацией.

**Содержание:** структура `/shared/i18n/{locale}/`, формат ключей (`{namespace}.{section}.{element}`), файлы переводов (common, errors, validation, auth), плюрализация для русского, форматирование дат и чисел.

| Файл | Содержание |
|------|------------|
| `common.json` | Общие строки (кнопки, статусы) |
| `errors.json` | Сообщения об ошибках |
| `validation.json` | Ошибки валидации |
| `auth.json` | Аутентификация |

**Правило:** Русский — базовый язык. Ключи на английском в dot-notation.

**Инструкция:** [i18n.md](./i18n.md)

---

# 4. Contracts

Правила создания и поддержки контрактов между сервисами. Контракты — единственный источник правды для межсервисного взаимодействия.

**Содержание:** структура `/shared/contracts/` (rest, grpc, events, pacts), contract-first подход, обратная совместимость, OpenAPI для REST, Protobuf для gRPC, JSON Schema для событий, версионирование, contract testing.

| Тип | Формат | Расположение |
|-----|--------|--------------|
| REST | OpenAPI 3.0 YAML | `/contracts/rest/` |
| gRPC | Protocol Buffers | `/contracts/grpc/` |
| Events | JSON Schema | `/contracts/events/` |

**Правило:** Сначала контракт, потом код. Breaking changes требуют новую версию (v2).

**Инструкция:** [contracts.md](./contracts.md)

---

# 5. Events

Правила работы с событиями в событийно-ориентированной архитектуре (Event-Driven Architecture).

**Содержание:** именование событий (`{service}.{entity}.{action}`), формат события (event_id, event_type, version, timestamp, source, data), идемпотентность обработки, Dead Letter Queue, retry с exponential backoff.

| Поле | Описание |
|------|----------|
| `event_id` | UUID для идемпотентности |
| `event_type` | `users.user.created` |
| `timestamp` | ISO 8601 UTC |
| `correlation_id` | ID для трассировки |
| `data` | Полезная нагрузка |

**Правило:** Событие — факт (что произошло), не команда (что сделать).

**Инструкция:** [events.md](./events.md)

