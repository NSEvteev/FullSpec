# /src/ -- Инструкции для разработки сервисов

Правила разработки микросервисов: API, данные, runtime, безопасность.

## Оглавление

- [Архитектура микросервисов](#архитектура-микросервисов)
- [Подпапки](#подпапки)
- [Матрица выбора инструкции](#матрица-выбора-инструкции)
- [Связи между инструкциями](#связи-между-инструкциями)

---

## Архитектура микросервисов

```
┌─────────────────────────────────────────────────────────────────────┐
│                        /src/ Instructions                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────┐     ┌─────────┐     ┌───────────┐     ┌──────────┐   │
│   │   api/  │────▶│  data/  │────▶│  runtime/ │────▶│ security/│   │
│   │         │     │         │     │           │     │          │   │
│   │ Design  │     │ Errors  │     │ Database  │     │  Auth    │   │
│   │ Version │     │ Logging │     │ Health    │     │  Audit   │   │
│   │ Swagger │     │ Valid.  │     │ Realtime  │     │          │   │
│   │ Deprec. │     │ Pagin.  │     │ Resilience│     │          │   │
│   └─────────┘     └─────────┘     └───────────┘     └──────────┘   │
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                         dev/                                  │   │
│   │         Local development  |  Testing  |  Performance        │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Принципы

| Принцип | Описание |
|---------|----------|
| **Service isolation** | Каждый сервис автономен, имеет свою БД |
| **API-first** | Контракт описывается до реализации |
| **Resilience** | Сервисы устойчивы к сбоям зависимостей |
| **Observability** | Логи, метрики, трейсы стандартизированы |

---

## Подпапки

| Подпапка | Описание | README |
|----------|----------|--------|
| [api/](./api/) | Проектирование REST API: URL, методы, версионирование | [api/README.md](./api/README.md) |
| [data/](./data/) | Форматы данных: ошибки, логи, валидация, пагинация | [data/README.md](./data/README.md) |
| [dev/](./dev/) | Разработка: локальный запуск, тесты, производительность | [dev/README.md](./dev/README.md) |
| [runtime/](./runtime/) | Runtime: БД, health checks, resilience, real-time | [runtime/README.md](./runtime/README.md) |
| [security/](./security/) | Безопасность: аутентификация, аудит | [security/README.md](./security/README.md) |

---

## Матрица выбора инструкции

### По ситуации

| Ситуация | Инструкция | Подпапка |
|----------|------------|----------|
| Проектирую новый endpoint | [design.md](./api/design.md) | api/ |
| Нужна новая версия API | [versioning.md](./api/versioning.md) | api/ |
| Выводим API из эксплуатации | [deprecation.md](./api/deprecation.md) | api/ |
| Документирую API в Swagger | [swagger.md](./api/swagger.md) | api/ |
| Формат ответа об ошибке | [errors.md](./data/errors.md) | data/ |
| Логирование в сервисе | [logging.md](./data/logging.md) | data/ |
| Валидация входных данных | [validation.md](./data/validation.md) | data/ |
| Пагинация списков | [pagination.md](./data/pagination.md) | data/ |
| Запуск локально (make dev) | [local.md](./dev/local.md) | dev/ |
| Написание unit/integration тестов | [testing.md](./dev/testing.md) | dev/ |
| Оптимизация производительности | [performance.md](./dev/performance.md) | dev/ |
| Работа с БД (pool, миграции) | [database.md](./runtime/database.md) | runtime/ |
| Эндпоинты /health, /ready | [health.md](./runtime/health.md) | runtime/ |
| Выбор polling/SSE/WebSocket | [realtime.md](./runtime/realtime.md) | runtime/ |
| Таймауты, retry, circuit breaker | [resilience.md](./runtime/resilience.md) | runtime/ |
| JWT между сервисами | [auth.md](./security/auth.md) | security/ |
| Аудит-логи, GDPR, PII | [audit.md](./security/audit.md) | security/ |

### По типу задачи

| Задача | Начать с | Затем |
|--------|----------|-------|
| Новый сервис | api/design.md | runtime/health.md, security/auth.md |
| Новый endpoint | api/design.md | data/validation.md, data/errors.md |
| Добавить real-time | runtime/realtime.md | runtime/resilience.md |
| Настроить CI/CD тесты | dev/testing.md | dev/performance.md |
| Подключить к БД | runtime/database.md | runtime/health.md |
| Защита данных | security/audit.md | data/logging.md |

---

## Связи между инструкциями

```
api/design.md
├── api/versioning.md ── api/deprecation.md
├── api/swagger.md
├── data/errors.md
└── data/pagination.md

data/logging.md
├── data/errors.md
└── platform/observability/logging.md (внешняя)

runtime/health.md
├── runtime/database.md
└── runtime/resilience.md

security/auth.md
├── security/audit.md
└── runtime/resilience.md

dev/testing.md
├── dev/local.md
└── dev/performance.md
```

---

## Типы инструкций

| Тип | Описание | Файлы |
|-----|----------|-------|
| `standard` | Стандарты качества (КАК делать) | api/*, data/*, runtime/*, security/*, dev/performance.md, dev/testing.md |
| `project` | Специфика проекта (ЧТО есть) | dev/local.md |

---

## Связанные разделы

- [/.claude/instructions/platform/](../platform/) -- инфраструктура (Docker, K8s, observability)
- [/.claude/instructions/shared/](../shared/) -- общий код между сервисами
- [/.claude/instructions/tests/](../tests/) -- системное тестирование
- [/.claude/instructions/config/](../config/) -- конфигурации окружений
