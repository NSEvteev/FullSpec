---
type: project
description: Индекс инструкций тестирования проекта
related:
  - tools/claude-testing.md
  - src/dev/testing.md
  - git/ci.md
---

# Тестирование проекта

Индекс инструкций для тестирования проекта (`/tests/`).

> **Отличие от [claude-testing.md](claude-testing.md):** Этот раздел описывает тесты для кода проекта (unit, integration, e2e). Claude-testing описывает тесты для скиллов, инструкций и агентов Claude Code.

## Оглавление

- [Структура папки /tests/](#структура-папки-tests)
- [Инструкции](#инструкции)
- [Связанные инструкции](#связанные-инструкции)

---

## Общие правила

**Правило:** Все тесты запускаются через Makefile.

```bash
make test           # Все тесты
make test-unit      # Только unit
make test-e2e       # Только e2e
make test-smoke     # Smoke-тесты (быстрые)
```

**Правило:** Тесты должны быть идемпотентны — повторный запуск даёт тот же результат.

**Правило:** Тесты не должны зависеть от порядка выполнения.

---

## Структура папки /tests/

```
/tests/
  /unit/           # Юнит-тесты сервисов
  /integration/    # Интеграционные тесты
  /e2e/            # End-to-end тесты
  /smoke/          # Smoke-тесты (быстрая проверка)
  /load/           # Нагрузочные тесты
  /fixtures/       # Тестовые данные
```

---

## Инструкции

| Инструкция | Описание | Тип | Статус |
|------------|----------|-----|:------:|
| [unit.md](../tests/unit.md) | Unit-тесты: изоляция, моки, покрытие | standard | ⬜ |
| [integration.md](../tests/integration.md) | Интеграционные тесты: БД, API, сервисы | standard | ⬜ |
| [e2e.md](../tests/e2e.md) | End-to-end тесты: сценарии пользователя | standard | ⬜ |
| [smoke.md](../tests/smoke.md) | Smoke-тесты: быстрая проверка работоспособности | standard | ⬜ |
| [load.md](../tests/load.md) | Нагрузочные тесты: k6, пороги производительности | standard | ⬜ |
| [fixtures.md](../tests/fixtures.md) | Тестовые данные: фикстуры, фабрики, seeds | standard | ⬜ |

---

## Связанные инструкции

- [claude-testing.md](claude-testing.md) — тестирование Claude Code (скиллы, инструкции)
- [src/dev/testing.md](../src/dev/testing.md) — тесты внутри сервисов (co-located)
- [git/ci.md](../git/ci.md) — CI/CD pipeline (запуск тестов)
