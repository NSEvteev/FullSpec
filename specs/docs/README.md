# Документация для поставки

Рабочий контекст LLM-разработчика — всё, что нужно для написания кода.

## Сервисы

| Сервис | Описание | Технологии |
|--------|----------|-----------|
| [example](./example.md) | Пример сервисного документа | — |

## Системные документы

| Документ | Назначение |
|----------|-----------|
| [overview.md](./.system/overview.md) | Архитектура системы |
| [conventions.md](./.system/conventions.md) | Конвенции API и shared-интерфейсы |
| [infrastructure.md](./.system/infrastructure.md) | Платформа и окружения |
| [testing.md](./.system/testing.md) | Стратегия тестирования |

## Стандарты технологий

| Стандарт | Технология |
|----------|-----------|
| [standard-example.md](./.technologies/standard-example.md) | Пример per-tech стандарта |

## Дерево

```
specs/docs/
├── README.md                          # Этот файл (индекс)
├── example.md                         # Пример сервисного документа
├── .system/
│   ├── overview.md                    # Архитектура системы
│   ├── conventions.md                 # Конвенции API и shared-интерфейсы
│   ├── infrastructure.md              # Платформа и окружения
│   └── testing.md                     # Стратегия тестирования
└── .technologies/
    └── standard-example.md            # Пример per-tech стандарта
```
