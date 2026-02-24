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

| Технология | Стандарт |
|-----------|---------|

*Per-tech стандарты добавляются при подключении технологии.*

## Дерево

```
specs/docs/
├── .system/
│   ├── conventions.md                 # Конвенции API, shared-интерфейсы
│   ├── infrastructure.md              # Платформа, деплой, мониторинг
│   ├── overview.md                    # Архитектура, связи, потоки
│   └── testing.md                     # Тестирование: типы, структура, команды
├── .technologies/
│   └── standard-example.md            # Пример per-tech стандарта
└── example.md                         # Пример сервисного документа
```
