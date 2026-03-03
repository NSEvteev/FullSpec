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
| example | Демонстрационный сервис формата документации | Node.js, PostgreSQL | [example.md](example.md) |

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
| FastAPI | [standard-fastapi.md](.technologies/standard-fastapi.md) | — |
| OpenAPI | [standard-openapi.md](.technologies/standard-openapi.md) | — |
| PostgreSQL | [standard-postgresql.md](.technologies/standard-postgresql.md) | — |
| Protobuf | [standard-protobuf.md](.technologies/standard-protobuf.md) | — |
| React | [standard-react.md](.technologies/standard-react.md) | — |
| Tailwind CSS | [standard-tailwind-css.md](.technologies/standard-tailwind-css.md) | — |
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
│   ├── security-typescript.md         # Security-стандарт TypeScript
│   ├── standard-asyncapi.md           # Конвенции AsyncAPI (events)
│   ├── standard-fastapi.md            # Конвенции FastAPI (Python web)
│   ├── standard-openapi.md            # Конвенции OpenAPI (REST)
│   ├── standard-postgresql.md         # Конвенции PostgreSQL
│   ├── standard-protobuf.md           # Конвенции Protobuf (gRPC)
│   ├── standard-react.md              # Конвенции React
│   ├── standard-tailwind-css.md       # Конвенции Tailwind CSS (палитра, z-слои, анимации)
│   └── standard-typescript.md         # Конвенции TypeScript
└── example.md                         # Пример сервисного документа
```
