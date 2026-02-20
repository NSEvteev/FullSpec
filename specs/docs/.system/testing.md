---
description: Тестирование MyApp — типы тестов, мокирование, межсервисные тесты, тестовые данные.
standard: specs/.instructions/docs/testing/standard-testing.md
standard-version: v1.1
---

> **Это визуализация.** Содержание заполнено примером из стандарта (MyApp, 4 сервиса). При реальном использовании — заменить на данные проекта по [Сценарию 6](../../../specs/.instructions/docs/testing/modify-testing.md#сценарий-6-первичное-заполнение-из-визуализации).

# Тестирование

## Типы тестов

В проекте 5 типов тестов. Unit — основа: быстрые, изолированные, покрывают бизнес-логику. Integration — проверяют работу с реальными БД и брокером. E2E — полные сценарии через HTTP/WS API. Smoke — быстрая проверка что сервисы живы после деплоя. Load — нагрузочное тестирование перед релизом.

| Тип | Что проверяет | Scope | Внешние зависимости | Когда запускается |
|-----|--------------|-------|--------------------|--------------------|
| Unit | Бизнес-логика, валидация, маппинг, утилиты | Один модуль/функция | Все мокаются | При каждом коммите (pre-commit), в CI |
| Integration | Запросы к БД, AMQP pub/sub, repository-слой | Сервис + его хранилища | Реальные БД (Docker), мок других сервисов | В CI на каждый PR |
| E2E | Полные сценарии через API: регистрация → создание задачи → уведомление | Вся система | Всё реальное (docker-compose) | В CI перед merge в main |
| Smoke | Healthcheck всех сервисов, базовый CRUD | Вся система | Всё реальное | После деплоя на staging/prod |
| Load | Пропускная способность, latency под нагрузкой | Вся система | Всё реальное | Перед релизом, по запросу |

## Структура файлов

Unit и integration тесты живут внутри сервиса — рядом с кодом, который тестируют. Системные тесты (e2e, smoke, load) — в корневой `/tests/`. Именование: файл `test_{module}.py`, функция `test_{action}_{scenario}`, класс `Test{Feature}`.

```
/
├── src/auth/tests/                  # Тесты auth-сервиса
│   ├── conftest.py                  # Fixtures: тестовая БД, мок AMQP
│   ├── test_token.py               # Unit: генерация/валидация JWT
│   └── test_repository.py          # Integration: запросы к PostgreSQL
├── src/task/tests/                  # Тесты task-сервиса
│   ├── conftest.py
│   ├── test_routes.py              # Unit: API endpoints (мок repository)
│   └── test_repository.py          # Integration: запросы к PostgreSQL
├── src/notification/tests/          # Тесты notification-сервиса
│   ├── conftest.py                  # Fixtures: тестовая БД, мок AMQP, фабрики
│   ├── test_repository.py          # Integration: запросы к PostgreSQL
│   ├── test_handlers.py            # Unit: обработка событий
│   ├── test_routes.py              # Unit: API endpoints (мок repository)
│   └── test_hub.py                 # Unit: WebSocket Hub логика
├── src/admin/tests/                 # Тесты admin-сервиса
│   ├── conftest.py
│   └── test_routes.py              # Unit: admin API
├── tests/                           # Системные тесты
│   ├── e2e/
│   │   ├── conftest.py              # docker-compose up, HTTP-клиенты, WS-клиент
│   │   ├── test_registration_flow.py  # Регистрация → welcome-уведомление
│   │   ├── test_task_notification.py  # Создание задачи → уведомление назначенному
│   │   └── test_admin_role_change.py  # Смена роли → уведомление
│   ├── integration/
│   │   ├── conftest.py              # Отдельные сервисы + реальные БД
│   │   └── test_event_delivery.py   # auth публикует → notification получает
│   ├── smoke/
│   │   └── test_health.py           # GET /health для каждого сервиса
│   └── load/
│       └── locustfile.py            # Locust-сценарии
```

## Стратегия мокирования

Принцип: чем выше уровень теста, тем меньше моков. Unit мокает всё за пределами тестируемого модуля. Integration поднимает реальные хранилища (PostgreSQL, Redis в Docker), но мокает другие сервисы. E2E не мокает ничего — все сервисы запущены реально.

| Уровень | БД | Message Broker | Другие сервисы | Shared-код | Внешние API |
|---------|-----|---------------|---------------|------------|-------------|
| Unit | Мок (in-memory) | Мок | Мок | Реальный | Мок |
| Integration | Реальный (Docker) | Реальный (Docker) | Мок (httpx mock) | Реальный | Мок |
| E2E | Реальный | Реальный | Реальный | Реальный | Мок (WireMock) |

Паттерны мокирования (pytest fixtures, AsyncMock, factory_boy) — в [standard-python.md](../.technologies/standard-python.md#тестирование) (backend).

## Межсервисные тесты

Межсервисные сценарии описаны в [overview.md](overview.md#сквозные-потоки) — это SSOT сквозных потоков. Для поднятия всех сервисов используется `docker-compose -f docker-compose.test.yml up`, который запускает все сервисы + хранилища в изолированной сети.

Паттерн написания межсервисного теста:
1. **Arrange:** создать начальное состояние (зарегистрировать пользователя, получить JWT)
2. **Act:** выполнить основное действие (создать задачу через API task-сервиса)
3. **Assert:** проверить результат минимум в двух сервисах (задача создана в task, уведомление появилось в notification, WS-сообщение отправлено)

При проверке асинхронных событий (AMQP → notification) — использовать polling с таймаутом: повторять проверку GET /notifications каждые 100ms, максимальный таймаут ожидания — 5 секунд.

## Тестовые данные

Подход: factory_boy для генерации объектов, pytest fixtures для подготовки состояния БД. Seed data для e2e хранится в `tests/e2e/fixtures/`. Каждый тест создаёт свои данные и очищает после себя (транзакционный rollback для integration, truncate для e2e).

**Принципы:**
- Каждый тест независим — не зависит от порядка запуска и данных других тестов
- Фабрики генерируют минимальный валидный объект, тест переопределяет только нужные поля
- Изоляция данных — каждый тест очищает за собой (транзакционный rollback для integration, truncate для e2e)
- Для e2e: seed data создаётся через API (не напрямую в БД), чтобы проверить полный цикл
- Чувствительные данные (JWT ключи) — фиксированные тестовые значения в `conftest.py`, не из .env

## Команды запуска

Make-таргеты для тестирования определены в [Makefile](/Makefile) (SSOT). Полный список: `make help`.

**Прямой вызов pytest** (для запуска конкретных тестов по фильтру):

```bash
pytest src/notification/tests/ -k "test_handlers"     # Тесты одного сервиса по фильтру
pytest tests/e2e/ -k "test_registration"               # Конкретный e2e-сценарий
pytest src/notification/tests/test_handlers.py -v       # Один файл, подробный вывод
```
