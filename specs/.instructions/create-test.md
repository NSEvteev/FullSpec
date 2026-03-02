---
description: Воркфлоу финальной валидации — sync main, docker up, make test/lint/build/test-e2e, проверка полноты реализации, отчёт с вердиктом READY/NOT READY.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу финальной валидации

Рабочая версия стандарта: 1.3

Оркестрация финальной валидации после завершения разработки (Task 8 в chain). Последовательно: sync main, docker up, полный прогон тестов, проверка полноты реализации, отчёт с вердиктом.

**Полезные ссылки:**
- [Инструкции specs/](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | *Standalone воркфлоу (нет отдельного стандарта)* |
| Валидация | *Не требуется* |
| Создание | Этот документ |
| Модификация | *Не требуется* |

**SSOT-зависимости:**
- [validation-development.md](/.github/.instructions/development/validation-development.md) — чек-лист проверок перед push
- [standard-docker.md](/platform/.instructions/standard-docker.md) § 8 — тестовое окружение (docker-compose.test.yml, health checks)
- [standard-testing-system.md](/tests/.instructions/standard-testing-system.md) — паттерны системных тестов
- [standard-sync.md](/.github/.instructions/sync/standard-sync.md) — синхронизация с main

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить предусловия](#шаг-1-проверить-предусловия)
  - [Шаг 2: Синхронизация с main](#шаг-2-синхронизация-с-main)
  - [Шаг 3: Поднять тестовое окружение](#шаг-3-поднять-тестовое-окружение)
  - [Шаг 4: Unit/Integration тесты](#шаг-4-unitintegration-тесты)
  - [Шаг 5: Линтинг](#шаг-5-линтинг)
  - [Шаг 6: Сборка](#шаг-6-сборка)
  - [Шаг 7: E2E тесты](#шаг-7-e2e-тесты)
  - [Шаг 8: Остановить тестовое окружение](#шаг-8-остановить-тестовое-окружение)
  - [Шаг 9: Проверка полноты реализации](#шаг-9-проверка-полноты-реализации)
  - [Шаг 10: Отчёт](#шаг-10-отчёт)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Финальная валидация — точка качества.** Все TASK-N завершены → полный прогон тестов → вердикт. Между разработкой и ревью.

> **Автоматический E2E по diff.** Анализ `git diff` определяет обязательность E2E — без вопросов пользователю.

> **Вердикт блокирует ревью.** NOT READY = возврат к разработке (Task 7). READY = переход к ревью (Task 9).

---

## Шаги

### Шаг 1: Проверить предусловия

**Проверки:**

| Предусловие | Как проверить | При failure |
|-------------|---------------|-------------|
| Feature-ветка (не main) | `git branch --show-current` ≠ `main` | СТОП: "Финальная валидация запускается только в feature-ветке" |
| docker-compose.test.yml доступен | `test -f platform/docker/docker-compose.test.yml` | СТОП: "Docker-конфигурация не найдена. См. standard-docker.md § 8" |
| Все TASK-N из plan-dev.md done | Прочитать plan-dev.md, проверить `[x]` для всех TASK-N | СТОП: "Не все задачи завершены: {список незавершённых TASK-N}" |

### Шаг 2: Синхронизация с main

```bash
git fetch origin
git merge origin/main --no-edit
```

| Результат | Действие |
|-----------|----------|
| Merge успешен | Продолжить |
| Конфликт | СТОП: показать конфликтные файлы. Вернуть к dev-agent для разрешения |

> **SSOT:** [standard-sync.md](/.github/.instructions/sync/standard-sync.md) — процесс синхронизации.

### Шаг 3: Поднять тестовое окружение

```bash
docker compose -f platform/docker/docker-compose.test.yml up -d --wait
```

> **SSOT:** [standard-docker.md](/platform/.instructions/standard-docker.md) § 8 — конфигурация docker-compose.test.yml, health checks.

Флаг `--wait` ожидает прохождения health checks, настроенных в docker-compose.test.yml:

| Сервис | Healthcheck |
|--------|-------------|
| PostgreSQL | `pg_isready` |
| Redis | `redis-cli ping` |
| RabbitMQ | `rabbitmq-diagnostics -q ping` |

**Таймаут:** 60s. Если health check не пройден за 60s:
1. Выполнить `docker compose -f platform/docker/docker-compose.test.yml logs {service}`
2. Выполнить `docker inspect {container}` для диагностики
3. СТОП с ошибкой и логами

### Шаг 4: Unit/Integration тесты

```bash
make test
```

| Результат | Действие |
|-----------|----------|
| exit code 0 | Продолжить |
| exit code ≠ 0 | Записать failing тесты в отчёт. Продолжить (собрать все результаты) |

### Шаг 5: Линтинг

```bash
make lint
```

| Результат | Действие |
|-----------|----------|
| Нет ERRORS | Продолжить |
| Есть ERRORS | Записать ошибки в отчёт. Продолжить |

### Шаг 6: Сборка

```bash
make build
```

| Результат | Действие |
|-----------|----------|
| exit code 0 | Продолжить |
| exit code ≠ 0 | Записать ошибку в отчёт. Продолжить |

### Шаг 7: E2E тесты

**Анализ необходимости:**

```bash
git diff --name-only origin/main...HEAD
```

**E2E обязателен**, если затронуты:
- `src/*/routes/`, `src/*/api/` — API эндпоинты
- `shared/contracts/` — контракты между сервисами
- `src/*/database/` — схема или миграции БД
- `platform/docker/gateway` — конфигурация gateway

**E2E пропускается** с пометкой "No API/DB/inter-service changes", если затронуты только:
- Внутренняя логика сервиса (без изменений API/DB)
- Документация, конфигурация, стили

> **SSOT:** Маппинг "сценарий → обязательные команды" из [validation-development.md](/.github/.instructions/development/validation-development.md).

```bash
# Если E2E обязателен:
make test-e2e
```

| Результат | Действие |
|-----------|----------|
| PASS | Записать в отчёт |
| SKIP | Записать причину skip в отчёт |
| FAIL | Записать failing тесты в отчёт |

### Шаг 8: Остановить тестовое окружение

```bash
docker compose -f platform/docker/docker-compose.test.yml down -v
```

> Выполняется независимо от результатов тестов.

### Шаг 9: Проверка полноты реализации

1. Прочитать `plan-dev.md` → все TASK-N
2. Проверить GitHub Issues → все closed
3. Сверить критерии готовности каждого Issue

| Результат | Действие |
|-----------|----------|
| Все TASK-N done, Issues closed | PASS |
| Есть незавершённые | Записать список в отчёт |

### Шаг 10: Отчёт

**Вывести таблицу результатов:**

```markdown
## Финальная валидация

| Проверка | Результат | Детали |
|----------|-----------|--------|
| Sync main | OK / CONFLICT | merge commit / конфликтные файлы |
| Docker test env | UP / FAIL | health checks status |
| make test | PASS / FAIL | N tests, N failures |
| make lint | PASS / FAIL | N errors |
| make build | PASS / FAIL | — |
| make test-e2e | PASS / SKIP / FAIL | причина skip или failures |
| Полнота | PASS / FAIL | N/M TASK-N done |

**Вердикт: READY / NOT READY**
```

**Вердикт:**

| Условие | Вердикт | Действие |
|---------|---------|----------|
| Все PASS/SKIP | **READY** | Переход к ревью (Task 9) |
| Есть FAIL или CONFLICT | **NOT READY** | Возврат к разработке (Task 7). Показать список проблем |

**Что НЕ входит в /test (и почему):**
- `make test-load` — pre-release (Фаза 7), не Фаза 4.4
- `make test-smoke` — post-deploy, не разработка

---

## Чек-лист

### Предусловия
- [ ] Feature-ветка (не main)
- [ ] docker-compose.test.yml существует
- [ ] Все TASK-N из plan-dev.md помечены `[x]`

### Валидация
- [ ] Sync с main выполнен (нет конфликтов)
- [ ] Docker test env поднят (health checks OK)
- [ ] `make test` — exit code 0
- [ ] `make lint` — нет ERRORS
- [ ] `make build` — exit code 0
- [ ] `make test-e2e` — PASS или обоснованный SKIP
- [ ] Полнота реализации — все TASK-N done, Issues closed

### Отчёт
- [ ] Таблица результатов выведена
- [ ] Вердикт READY / NOT READY определён
- [ ] При NOT READY — список проблем для исправления

---

## Примеры

### Успешная валидация (READY)

```
Шаг 1: Предусловия ✓ (feature-ветка, docker-compose.test.yml, 5/5 TASK-N done)
Шаг 2: git merge origin/main — OK (no conflicts)
Шаг 3: docker compose up --wait — OK (3/3 healthy)
Шаг 4: make test — PASS (42 tests, 0 failures)
Шаг 5: make lint — PASS (0 errors)
Шаг 6: make build — PASS
Шаг 7: git diff → src/auth/routes/ changed → E2E обязателен → make test-e2e — PASS
Шаг 8: docker compose down -v — OK
Шаг 9: 5/5 TASK-N done, 5/5 Issues closed
Шаг 10: Вердикт: READY
```

### Валидация с проблемами (NOT READY)

```
Шаг 4: make test — FAIL (2 failures: auth.service.test.ts, notification.handler.test.ts)
Шаг 7: E2E SKIP (no API/DB changes)
Шаг 10: Вердикт: NOT READY
  Проблемы:
  - make test: 2 failing tests
  → Вернуться к Task 7 для исправления
```

---

## Скрипты

*Нет скриптов.*

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/test](/.claude/skills/test/SKILL.md) | Финальная валидация | Этот документ |
