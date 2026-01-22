# /src/ — Исходный код сервисов

Корень сервисов проекта.

## Содержимое

| IN | OUT |
|----|-----|
| Папки сервисов (`{service}/`) | Общий код (→ `/shared/`) |

## Структура сервиса

```
{service}/
├── backend/          # Бэкенд: handlers, routes, services
├── database/         # БД: schema.sql, migrations/
├── frontend/         # Фронтенд (опционально)
└── tests/            # Unit и integration тесты
```

## Связанные ресурсы

- [Инструкции](/.claude/instructions/service/) — правила разработки
- [Документация](/doc/src/) — документация сервисов
- [Спецификации](/specs/services/) — архитектура сервисов
