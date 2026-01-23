# /src/api/ -- Проектирование REST API

Правила проектирования REST API: URL naming, HTTP методы, версионирование, документация.

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Design](#1-design) | [design.md](./design.md) | URL naming (kebab-case), HTTP методы, статус-коды, partial update, bulk operations |
| [2. Versioning](#2-versioning) | [versioning.md](./versioning.md) | Версионирование через URL (/v1/, /v2/), gRPC package versioning |
| [3. Deprecation](#3-deprecation) | [deprecation.md](./deprecation.md) | Вывод API: Sunset header, Deprecation header, сроки, migration guide |
| [4. Swagger](#4-swagger) | [swagger.md](./swagger.md) | OpenAPI спецификация, Swagger UI на /docs, автогенерация |

---

## 1. Design

**Файл:** [design.md](./design.md)

**Тип:** standard

**Описание:** Правила проектирования REST API: URL naming, HTTP методы, статус-коды.

**Ключевые правила:**
- URL в kebab-case: `/api/v1/user-profiles`
- Ресурсы во множественном числе: `/users`, не `/user`
- Максимум 2 уровня вложенности в URL
- Действия через отдельный endpoint: `POST /users/{id}/activate`

**Связанные инструкции:**
- [versioning.md](./versioning.md) -- версионирование API
- [deprecation.md](./deprecation.md) -- вывод API
- [swagger.md](./swagger.md) -- документация
- [../data/errors.md](../data/errors.md) -- формат ошибок
- [../data/pagination.md](../data/pagination.md) -- пагинация

---

## 2. Versioning

**Файл:** [versioning.md](./versioning.md)

**Тип:** standard

**Описание:** Правила версионирования API: URL versioning для REST, package versioning для gRPC.

**Ключевые правила:**
- Версия в URL path: `/api/v1/users`
- Формат версии: `v{N}` (только major version)
- Префикс `/api/` обязателен
- gRPC: версия в package name (`myservice.v1`)

**Связанные инструкции:**
- [design.md](./design.md) -- базовый дизайн API
- [deprecation.md](./deprecation.md) -- вывод старых версий
- [swagger.md](./swagger.md) -- документация версий

---

## 3. Deprecation

**Файл:** [deprecation.md](./deprecation.md)

**Тип:** standard

**Описание:** Правила вывода API из эксплуатации: заголовки, сроки, миграция.

**Ключевые правила:**
- HTTP заголовки: `Deprecation`, `Sunset`, `Link` (RFC 8594)
- Минимальный срок до sunset: 6 месяцев (12 для критичных API)
- После sunset: `410 Gone` с указанием новой версии
- Обязательный Migration Guide

**Связанные инструкции:**
- [versioning.md](./versioning.md) -- создание новых версий
- [design.md](./design.md) -- проектирование нового API
- [swagger.md](./swagger.md) -- документация deprecated endpoints

---

## 4. Swagger

**Файл:** [swagger.md](./swagger.md)

**Тип:** standard

**Описание:** Правила документирования API: OpenAPI спецификация, Swagger UI, автогенерация.

**Ключевые правила:**
- OpenAPI 3.0+ для описания REST API
- Swagger UI доступен на `/docs` или `/api/docs`
- Один файл спецификации на версию API
- Спецификация -- source of truth для API

**Связанные инструкции:**
- [design.md](./design.md) -- правила проектирования API
- [versioning.md](./versioning.md) -- документация версий
- [deprecation.md](./deprecation.md) -- пометка deprecated
- [../../shared/contracts.md](../../shared/contracts.md) -- контракты между сервисами

---

## Граф связей

```
                    ┌───────────────┐
                    │   design.md   │
                    │ (URL, методы) │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
    ┌─────────────┐  ┌───────────┐  ┌──────────────┐
    │versioning.md│  │swagger.md │  │   ../data/   │
    │ (URL /v1/)  │  │ (OpenAPI) │  │errors,pagin. │
    └──────┬──────┘  └───────────┘  └──────────────┘
           │
           ▼
    ┌─────────────┐
    │deprecation.md│
    │(Sunset, 410) │
    └─────────────┘
```

---

## Когда какую инструкцию читать

| Ситуация | Инструкция |
|----------|------------|
| Проектирую новый endpoint | design.md |
| Выбираю HTTP метод и статус-код | design.md |
| Создаю новую версию API | versioning.md |
| Выводим старый API из эксплуатации | deprecation.md |
| Документирую API в OpenAPI | swagger.md |
| Настраиваю Swagger UI | swagger.md |

---

## Связанные разделы

- [../data/](../data/) -- форматы данных (ошибки, пагинация)
- [../runtime/](../runtime/) -- runtime (health checks)
- [../../shared/](../../shared/) -- контракты между сервисами
