# /src/dev/ -- Разработка сервисов

Правила локальной разработки, тестирования и производительности.

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Local](#1-local) | [local.md](./local.md) | Локальная разработка: make dev, hot reload, debug порты, IDE |
| [2. Testing](#2-testing) | [testing.md](./testing.md) | КАК писать unit/integration тесты внутри сервисов (практика, инструменты, примеры) |
| [3. Performance](#3-performance) | [performance.md](./performance.md) | Профилирование, бенчмарки, лимиты: p99 < 200ms, память < 512MB |

---

## 1. Local

**Файл:** [local.md](./local.md)

**Тип:** project

**Описание:** Правила и инструменты для локальной разработки сервисов.

**Ключевые правила:**
- Запуск через `make dev`, остановка через `make stop`
- Hot reload через volume mount + nodemon/uvicorn/air
- Debug порты: 9229 (Node), 5678 (Python), 2345 (Go)
- Переменные окружения через `.env` файлы

**Связанные инструкции:**
- [testing.md](./testing.md) -- тестирование сервисов
- [performance.md](./performance.md) -- профилирование
- [../../platform/docker.md](../../platform/docker.md) -- Docker конфигурация
- [../../config/environments.md](../../config/environments.md) -- окружения

---

## 2. Testing

**Файл:** [testing.md](./testing.md)

**Тип:** standard

**Описание:** Практическое руководство по написанию unit и integration тестов внутри сервисов.

**Ключевые правила:**
- Структура: `/src/{service}/tests/unit/`, `/src/{service}/tests/integration/`
- Именование: `{module}.test.ts`, `{module}.integration.test.ts`
- Правило соседства: тест рядом с тестируемым кодом
- Моки в `/tests/mocks/`, фикстуры в `/tests/fixtures/`

**Связанные инструкции:**
- [local.md](./local.md) -- запуск тестов локально
- [../../tests/unit.md](../../tests/unit.md) -- стандарты unit-тестов
- [../../tests/integration.md](../../tests/integration.md) -- стандарты integration-тестов
- [../../tests/fixtures.md](../../tests/fixtures.md) -- управление фикстурами
- [../../tests/claude-testing.md](../../tests/claude-testing.md) -- тестирование Claude скиллов

---

## 3. Performance

**Файл:** [performance.md](./performance.md)

**Тип:** standard

**Описание:** Правила профилирования, бенчмарки и лимиты производительности сервисов.

**Ключевые правила:**
- Лимиты: p99 < 200ms, p95 < 100ms, память < 512MB
- Startup time < 30s
- Нагрузка: 100 RPS обычная, 500 RPS пиковая
- Error rate < 0.1% при нормальной нагрузке

**Связанные инструкции:**
- [local.md](./local.md) -- профилирование локально
- [../../tests/load.md](../../tests/load.md) -- нагрузочное тестирование
- [../../platform/observability/metrics.md](../../platform/observability/metrics.md) -- метрики производительности
- [../runtime/health.md](../runtime/health.md) -- health checks

---

## Граф связей

```
                    ┌───────────────┐
                    │   local.md    │
                    │ (make dev)    │
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │   testing.md    │         │ performance.md  │
    │ (unit/integr.)  │         │ (p99, memory)   │
    └────────┬────────┘         └────────┬────────┘
             │                           │
             ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │   /tests/       │         │ platform/       │
    │ unit, integr.   │         │ observability/  │
    │ fixtures        │         │ metrics         │
    └─────────────────┘         └─────────────────┘
```

---

## Когда какую инструкцию читать

| Ситуация | Инструкция |
|----------|------------|
| Запускаю проект локально | local.md |
| Настраиваю hot reload | local.md |
| Подключаю debugger | local.md |
| Пишу unit тест | testing.md |
| Пишу integration тест | testing.md |
| Создаю моки для внешних API | testing.md |
| Профилирую сервис | performance.md |
| Проверяю соответствие лимитам | performance.md |
| Оптимизирую latency | performance.md |

---

## Типы инструкций в этой папке

| Файл | Тип | Описание |
|------|-----|----------|
| local.md | `project` | Специфика проекта -- команды, порты, структура |
| testing.md | `standard` | Стандарты -- применимы к любому проекту |
| performance.md | `standard` | Стандарты -- пороги и метрики |

---

## Связанные разделы

- [../runtime/](../runtime/) -- runtime (health, resilience)
- [../../tests/](../../tests/) -- системное тестирование
- [../../platform/](../../platform/) -- Docker, observability
- [../../config/](../../config/) -- конфигурации окружений
