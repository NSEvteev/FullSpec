---
description: Воркфлоу финальной валидации — sync main, make test/lint/build/test-e2e, проверка полноты реализации, отчёт с вердиктом READY/NOT READY.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу финальной валидации

Рабочая версия стандарта: 1.3

Оркестрация финальной валидации после завершения разработки (Task 9 в chain). Предусловие: Docker-окружение поднято (Task 8, шаг 5.1). Последовательно: sync main, полный прогон тестов, проверка полноты реализации, отчёт с вердиктом.

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
- [standard-testing-system.md](/tests/.instructions/standard-testing-system.md) — паттерны системных тестов
- [standard-sync.md](/.github/.instructions/sync/standard-sync.md) — синхронизация с main
- [create-docker-env.md](/specs/.instructions/create-docker-env.md) — prerequisite: Docker-окружение (шаг 5.1)

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить предусловия](#шаг-1-проверить-предусловия)
  - [Шаг 2: Синхронизация с main](#шаг-2-синхронизация-с-main)
  - [Шаг 3: Unit/Integration тесты](#шаг-3-unitintegration-тесты)
  - [Шаг 4: Линтинг](#шаг-4-линтинг)
  - [Шаг 5: Сборка](#шаг-5-сборка)
  - [Шаг 6: E2E тесты](#шаг-6-e2e-тесты)
  - [Шаг 7: Проверка полноты реализации](#шаг-7-проверка-полноты-реализации)
  - [Шаг 8: Отчёт](#шаг-8-отчёт)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Финальная валидация — точка качества.** Все TASK-N завершены → полный прогон тестов → вердикт. Между разработкой и ревью.

> **Автоматический E2E по diff.** Анализ `git diff` определяет обязательность E2E — без вопросов пользователю.

> **Вердикт блокирует ревью.** NOT READY = возврат к разработке (Task 7). READY = переход к ревью (Task 11).

---

## Шаги

### Шаг 1: Проверить предусловия

**Проверки:**

| Предусловие | Как проверить | При failure |
|-------------|---------------|-------------|
| Docker-окружение поднято (шаг 5.1) | `docker ps` — все сервисы healthy | СТОП: "Выполните `/docker-up` перед `/test`" |
| Feature-ветка (не main) | `git branch --show-current` ≠ `main` | СТОП: "Финальная валидация запускается только в feature-ветке" |
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

### Шаг 3: Unit/Integration тесты

```bash
make test
```

| Результат | Действие |
|-----------|----------|
| exit code 0 | Продолжить |
| exit code ≠ 0 | Записать failing тесты в отчёт. Продолжить (собрать все результаты) |

### Шаг 4: Линтинг

```bash
make lint
```

| Результат | Действие |
|-----------|----------|
| Нет ERRORS | Продолжить |
| Есть ERRORS | Записать ошибки в отчёт. Продолжить |

### Шаг 5: Сборка

```bash
make build
```

| Результат | Действие |
|-----------|----------|
| exit code 0 | Продолжить |
| exit code ≠ 0 | Записать ошибку в отчёт. Продолжить |

### Шаг 6: E2E тесты

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

### Шаг 7: Проверка полноты реализации

1. Прочитать `plan-dev.md` → все TASK-N
2. Проверить GitHub Issues → все closed
3. Сверить критерии готовности каждого Issue

| Результат | Действие |
|-----------|----------|
| Все TASK-N done, Issues closed | PASS |
| Есть незавершённые | Записать список в отчёт |

### Шаг 8: Отчёт

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
| Все PASS/SKIP | **READY** | Переход к ревью (Task 11) |
| Есть FAIL или CONFLICT | **NOT READY** | Возврат к разработке (Task 7). Показать список проблем |

**Что НЕ входит в /test (и почему):**
- `make test-load` — pre-release (Фаза 8), не Фаза 5
- `make test-smoke` — post-deploy, не разработка

---

## Чек-лист

### Предусловия
- [ ] Docker-окружение поднято — все сервисы healthy (`/docker-up` выполнен)
- [ ] Feature-ветка (не main)
- [ ] Все TASK-N из plan-dev.md помечены `[x]`

### Валидация
- [ ] Sync с main выполнен (нет конфликтов)
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
Шаг 1: Предусловия ✓ (Docker healthy, feature-ветка, 5/5 TASK-N done)
Шаг 2: git merge origin/main — OK (no conflicts)
Шаг 3: make test — PASS (42 tests, 0 failures)
Шаг 4: make lint — PASS (0 errors)
Шаг 5: make build — PASS
Шаг 6: git diff → src/auth/routes/ changed → E2E обязателен → make test-e2e — PASS
Шаг 7: 5/5 TASK-N done, 5/5 Issues closed
Шаг 8: Вердикт: READY
```

### Валидация с проблемами (NOT READY)

```
Шаг 3: make test — FAIL (2 failures: auth.service.test.ts, notification.handler.test.ts)
Шаг 6: E2E SKIP (no API/DB changes)
Шаг 8: Вердикт: NOT READY
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
