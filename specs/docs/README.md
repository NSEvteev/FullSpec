---
description: Индекс сервисов и навигация по docs/
standard: specs/.instructions/docs/readme/standard-readme.md
standard-version: v1.0
---

# Документация для поставки

Рабочий контекст LLM-разработчика — всё, что нужно для написания кода.

**Архитектура:** [overview.md](.system/overview.md) — связи сервисов, data flows, контекстная карта доменов.

## Сервисы

| Сервис | Назначение | Технологии | Документ |
|--------|-----------|-----------|---------|
| auth | JWT-аутентификация, управление пользователями | Node.js, Express, PostgreSQL, Prisma, jose | [auth.md](auth.md) |
| example | Демонстрационный сервис формата документации | Node.js, PostgreSQL | [example.md](example.md) |
| frontend | SPA: канбан-доска, логин, фильтрация задач | React 18, TanStack Query, Zustand, Vite | [frontend.md](frontend.md) |
| task | CRUD задач, фильтрация, полнотекстовый поиск, история | Node.js, Express, PostgreSQL, Prisma | [task.md](task.md) |

## Системные документы

| Документ | Описание |
|----------|----------|
| [overview.md](.system/overview.md) | Архитектура системы: связи сервисов, сквозные потоки, контекстная карта |
| [conventions.md](.system/conventions.md) | Конвенции API: формат ошибок, пагинация, auth + shared-интерфейсы |
| [infrastructure.md](.system/infrastructure.md) | Платформа: деплой, сети, мониторинг, окружения |
| [testing.md](.system/testing.md) | Тестирование: типы, структура, мокирование, команды |

## Стандарты технологий

| Технология | Стандарт | Security |
|-----------|---------|----------|
| AsyncAPI | [standard-asyncapi.md](.technologies/standard-asyncapi.md) | — |
| Express | [standard-express.md](.technologies/standard-express.md) | — |
| JOSE | [standard-jose.md](.technologies/standard-jose.md) | — |
| OpenAPI | [standard-openapi.md](.technologies/standard-openapi.md) | — |
| PostgreSQL | [standard-postgresql.md](.technologies/standard-postgresql.md) | — |
| Prisma | [standard-prisma.md](.technologies/standard-prisma.md) | — |
| Protobuf | [standard-protobuf.md](.technologies/standard-protobuf.md) | — |
| React | [standard-react.md](.technologies/standard-react.md) | — |
| TypeScript | [standard-typescript.md](.technologies/standard-typescript.md) | [security-typescript.md](.technologies/security-typescript.md) |

## Дерево

```
specs/docs/
├── .system/
│   ├── conventions.md                 # Конвенции API, shared-интерфейсы
│   ├── infrastructure.md              # Платформа, деплой, мониторинг
│   ├── overview.md                    # Архитектура, связи, потоки
│   └── testing.md                     # Тестирование: типы, структура, команды
├── .technologies/
│   ├── standard-asyncapi.md           # Конвенции AsyncAPI (events)
│   ├── standard-express.md            # Конвенции Express 4.x (REST API, Zod)
│   ├── standard-jose.md               # Конвенции JOSE (JWT/JWS/JWE/JWK)
│   ├── standard-openapi.md            # Конвенции OpenAPI (REST)
│   ├── standard-postgresql.md         # Конвенции PostgreSQL (SQLAlchemy, Alembic)
│   ├── standard-prisma.md             # Конвенции Prisma (ORM для Node.js/TypeScript)
│   ├── standard-protobuf.md           # Конвенции Protobuf (gRPC)
│   ├── standard-react.md              # Конвенции React 18 (TanStack Query, Zustand)
│   ├── security-typescript.md         # Security-инструменты TypeScript (npm audit, ESLint security)
│   └── standard-typescript.md         # Конвенции TypeScript 5.x
├── auth.md                            # JWT-аутентификация, управление пользователями
├── example.md                         # Пример сервисного документа
├── frontend.md                        # SPA: канбан-доска, логин, фильтрация задач
└── task.md                            # CRUD задач, фильтрация, поиск, история
```
