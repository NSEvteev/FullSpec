# Шаг тестирования в chain + стандарт системных тестов

Три связанных изменения: (1) Task 8 "Валидация и тесты" в chain между разработкой и ревью, (2) стандарт написания системных тестов в tests/.instructions/, (3) связывание dev-agent и /test с Docker-инструкциями.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблема: три пробела](#1-проблема-три-пробела)
  - [2. Решение: новый шаг в chain](#2-решение-новый-шаг-в-chain)
  - [3. Скилл /test](#3-скилл-test)
  - [4. Стандарт системных тестов](#4-стандарт-системных-тестов)
  - [5. Связывание: кто о чём знает](#5-связывание-кто-о-чём-знает)
  - [6. Верификация: дополнительные пробелы](#6-верификация-дополнительные-пробелы)
  - [7. Изменения в файлах](#7-изменения-в-файлах)
  - [8. Детальные изменения (AS IS → TO BE)](#8-детальные-изменения-as-is--to-be)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** В цепочке `/chain` нет явного шага тестирования между разработкой и ревью. Параллельно: инструкции для написания системных тестов отсутствуют, а Docker-инструкции изолированы от агентов и скиллов.

**Почему создан:** Обнаружены три связанных пробела: (1) нет финальной точки качества в chain, (2) dev-agent не знает КАК писать системные тесты, (3) dev-agent и будущий /test не знают о Docker-конфигурациях для тестового окружения.

**Связанные файлы:**
- [create-chain.md](/specs/.instructions/create-chain.md) — TaskList `/chain` (Task 7 → Task 8)
- [standard-process.md](/specs/.instructions/standard-process.md) — Фаза 4 (4.1-4.3) и Фаза 5 (5.1)
- [validation-development.md](/.github/.instructions/development/validation-development.md) — 6 шагов проверки перед push
- [standard-development.md](/.github/.instructions/development/standard-development.md) — § 4 Тестирование
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) — стратегия тестирования (документ)
- [standard-docker.md](/platform/.instructions/standard-docker.md) — Docker конфигурации, § 8 Тестовое окружение
- [dev-agent AGENT.md](/.claude/agents/dev-agent/AGENT.md) — агент разработки (нет ссылок на docker/тесты)
- [Makefile](/Makefile) — make test, make lint, make build, make test-e2e
- [tests/.instructions/README.md](/tests/.instructions/README.md) — пустой индекс
- [tests/README.md](/tests/README.md) — зона ответственности системных тестов

---

## Содержание

### 1. Проблема: три пробела

#### Пробел A: нет финального шага тестирования в chain

**Текущее состояние (AS IS):**

```
Task 7: Разработка (dev-agent, BLOCK-N, per-task тесты)
                    ↓ (ничего)
Task 8: Ревью ветки (/review, code-reviewer)
```

В standard-process.md Фаза 4 содержит:
- 4.1 Development — блоки, волны, dev-agent
- 4.2 Локальная валидация — `make test`, `make lint`, `make test-e2e`
- 4.3 Commits — Conventional Commits

Но 4.2 **встроена** в цикл 4.1 (повторяется per-task). Нет **финального** прогона после завершения **всех** TASK-N.

| Аспект | Per-task (4.2 внутри 4.1) | Финальный (отсутствует) |
|--------|--------------------------|------------------------|
| Когда | После каждого TASK-N | После ВСЕХ TASK-N |
| Scope | Тесты изменённого сервиса (`make test-{svc}`) | ВСЕ тесты (unit + integration + e2e) |
| Цель | Быстрая обратная связь | Гарантия "всё зелёное" |
| Блокирует | Следующий TASK-N | Ревью ветки |

**Последствия:**
1. Code-reviewer на Task 8 может обнаружить failing тесты — потеря времени
2. E2E-тесты (`make test-e2e`) per-task запускаются только при изменениях API/DB — финальный прогон не гарантирован
3. `make build` не входит в per-task цикл — нет задачи в chain

#### Пробел B: нет инструкций для написания системных тестов

`tests/.instructions/` — **пустой индекс**. Карта покрытия:

| Что покрыто | Где | Для кого |
|-------------|-----|----------|
| Стратегия (типы, мокирование, данные) | `specs/.instructions/docs/testing/standard-testing.md` | system-agent (документация) |
| Per-tech паттерны (pytest, Jest) | `specs/docs/.technologies/standard-{tech}.md` | dev-agent (per-tech) |
| КОГДА запускать тесты | `.github/.instructions/development/standard-development.md § 4` | dev-agent (процесс) |

| Что НЕ покрыто | Для кого нужно |
|-----------------|---------------|
| КАК писать e2e-тест (Arrange/Act/Assert для межсервисного теста) | dev-agent |
| КАК работать с docker-compose.test.yml | dev-agent, /test |
| КАК организовать fixtures/factories | dev-agent |
| КАК писать load-тест (k6/locust сценарий) | dev-agent |
| КАК делать polling для асинхронных событий | dev-agent |

#### Пробел C: Docker-инструкции изолированы

`platform/.instructions/standard-docker.md` **существует** и содержит § 8 "Тестовое окружение" (docker-compose.test.yml, tmpfs, сети, testcontainers). Но:

| Кто | Знает о standard-docker.md? | Последствия |
|-----|------------------------------|-------------|
| dev-agent | **НЕТ** (не в AGENT.md) | Не знает как поднять тестовое окружение |
| Скилл /test (планируемый) | **НЕТ** (ещё не создан) | Не поднимет docker-compose.test.yml |
| validation-development.md | **НЕТ** (нет ссылки) | Чек-лист не упоминает docker |
| standard-development.md | **ДА** (ссылка в SSOT-зависимостях) | Но dev-agent читает только AGENT.md |

**Корневая причина:** Знание о Docker-окружении замкнуто в `platform/.instructions/` и не "прорастает" в инструменты, которые реально запускают тесты.

### 2. Решение: новый шаг в chain

**Целевое состояние (TO BE):**

```
Task 7:  Разработка (dev-agent, per-task тесты)
                    ↓
Task 8:  Валидация и тесты (/test — финальный прогон)
                    ↓
Task 9:  Ревью ветки (/review, code-reviewer)
Task 10: Создать PR
Task 11: Ревью PR
Task 12: Merge
Task 13: Завершить цепочку
Task 14: Релиз (опционально)
```

**Новая задача (Task 8 в обновлённом TaskList):**

```
TASK 8: Валидация и тесты
  description: >
    Скилл: /test — финальный прогон всех тестов и проверок после завершения разработки.
    Последовательно: make test → make lint → make build → make test-e2e.
    Проверка полноты реализации: все TASK-N из plan-dev.md покрыты.
    Вердикт: всё зелёное → ревью. Есть красное → вернуться к Task 7.
    SSOT: create-test.md → validation-development.md
  activeForm: Валидация и тесты
  blockedBy: [7]
```

**Обновление standard-process.md — Фаза 4 расширяется:**

| # | Шаг | Описание | Скилл | SSOT |
|---|-----|---------|-------|------|
| 4.1 | Development | Блоки, волны, dev-agent | dev-agent | modify-development.md |
| 4.2 | Локальная валидация | Per-task: `make test-{svc}`, `make lint-{svc}` | — | validation-development.md |
| 4.3 | Commits | Conventional Commits | `/commit` | standard-commit.md |
| **4.4** | **Финальная валидация** | **Все TASK-N done → полный прогон тестов** | **`/test`** | **create-test.md** |

**Нумерация задач в create-chain.md (TO BE):**

| # | Задача | Было |
|---|--------|------|
| 1-7 | Без изменений | 1-7 |
| **8** | **Валидация и тесты** | **НОВЫЙ** |
| 9 | Ревью ветки | 8 |
| 10 | Создать PR | 9 |
| 11 | Ревью PR | 10 |
| 12 | Merge | 11 |
| 13 | Завершить цепочку | 12 |
| 14 | Релиз (опционально) | 13 |

### 3. Скилл /test

**Назначение:** Оркестрация финальной валидации после завершения разработки. Запускает все проверки из validation-development.md последовательно, генерирует отчёт.

**SSOT-цепочка:**
```
/test (скилл) → create-test.md (воркфлоу оркестрации) → validation-development.md (чек-лист проверок)
                                                       → standard-docker.md § 8 (тестовое окружение)
                                                       → standard-testing-system.md (паттерны тестов)
```

**Шаги скилла (обновлено после верификации — пробелы C1-C4):**

```
Шаг 1: Проверить предусловия
  - Ветка = feature-ветка (не main)
  - docker-compose.test.yml доступен (→ standard-docker.md § 8)
  - Все TASK-N из plan-dev.md отмечены [x]

Шаг 1.5: Синхронизация с main (NEW — C2)
  - git fetch origin
  - git merge origin/main --no-edit
  - При конфликте: СТОП, показать конфликтные файлы, вернуть к dev-agent

Шаг 2: Поднять тестовое окружение (расширен — C3)
  - docker compose -f platform/docker/docker-compose.test.yml up -d --wait
  - Ожидаемые health checks (→ standard-docker.md § 6):
    PostgreSQL: pg_isready
    Redis: redis-cli ping
    RabbitMQ: rabbitmq-diagnostics -q ping
  - При failure: docker compose logs {service}, docker inspect {container}
  - Таймаут: 60s. Если не прошёл → СТОП с диагностикой

Шаг 3: Unit/Integration тесты
  - make test
  - Критерий: exit code 0
  - При failure: СТОП, показать failing тесты

Шаг 4: Линтинг
  - make lint
  - Критерий: нет ERRORS

Шаг 5: Сборка
  - make build
  - Критерий: exit code 0

Шаг 6: E2E тесты (обновлён — C1, C4)
  - Анализ: git diff --name-only origin/main...HEAD
  - Если затронуты src/*/routes/, src/*/api/, shared/contracts/,
    src/*/database/, platform/docker/gateway → E2E ОБЯЗАТЕЛЕН
  - Иначе: E2E SKIP с пометкой "No API/DB/inter-service changes"
  - make test-e2e
  - Маппинг из validation-development.md (сценарий → обязательные команды)

Шаг 7: Остановить тестовое окружение
  - docker compose -f platform/docker/docker-compose.test.yml down -v

Шаг 8: Проверка полноты реализации
  - Прочитать plan-dev.md → все TASK-N
  - Проверить Issues → все closed
  - Сверить критерии готовности каждого Issue

Шаг 9: Отчёт
  - Вывести таблицу результатов:
    | Проверка | Результат | Детали |
    |----------|-----------|--------|
    | Sync main | OK / CONFLICT | merge commit / конфликтные файлы |
    | Docker test env | UP / FAIL | health checks status |
    | make test | PASS / FAIL | N tests, N failures |
    | make lint | PASS / FAIL | N errors |
    | make build | PASS / FAIL | — |
    | make test-e2e | PASS / SKIP / FAIL | причина skip или failures |
    | Полнота | PASS / FAIL | N/M TASK-N done |
  - Вердикт: READY (все PASS/SKIP) / NOT READY (есть FAIL/CONFLICT)
```

**Что НЕ входит в /test (и почему):**
- `make test-load` — pre-release (Фаза 7), не Фаза 4.4
- `make test-smoke` — post-deploy, не разработка

**Отличие от validation-development.md:**
- validation-development.md — **чек-лист** (что проверить, ручная проверка)
- create-test.md — **воркфлоу** (как оркестрировать: предусловия, docker, порядок, отчёт, вердикт)
- `/test` — **скилл** (точка входа, ссылается на create-test.md)

### 4. Стандарт системных тестов

**Новый файл:** `tests/.instructions/standard-testing-system.md`

**Назначение:** Инструкции для dev-agent и LLM по написанию системных тестов (e2e, integration, load, smoke). КАК реализовывать тесты — паттерны, fixtures, docker, polling.

**Разграничение с существующими документами:**

| Документ | Отвечает на вопрос | Аудитория |
|----------|-------------------|-----------|
| standard-testing.md (specs/.instructions/docs/testing/) | КАК документировать стратегию тестирования в testing.md | system-agent |
| standard-development.md § 4 | КОГДА запускать тесты в процессе разработки | dev-agent (процесс) |
| standard-{tech}.md | КАК использовать конкретный фреймворк (pytest fixtures, Jest mocks) | dev-agent (per-tech) |
| **standard-testing-system.md (NEW)** | **КАК писать системный тест в этом проекте** | **dev-agent (реализация)** |

**Предварительная структура секций:**

```
1. Назначение и разграничение
   - Что покрывает этот документ (реализация системных тестов)
   - Что НЕ покрывает (стратегия → standard-testing.md, per-tech → standard-{tech}.md)
   - SSOT-зависимости

2. Тестовое окружение
   - Ссылка: standard-docker.md § 8 (SSOT docker-compose.test.yml)
   - Поднятие: docker compose -f docker-compose.test.yml up -d --wait
   - Остановка: docker compose -f docker-compose.test.yml down -v
   - Health checks: ждать condition: service_healthy
   - Сети: myapp-test (изоляция от dev)

3. Паттерн E2E-теста
   - Arrange: подготовка состояния через API (не напрямую в БД)
   - Act: выполнение действия через HTTP/WS API
   - Assert: проверка результата минимум в 2 сервисах
   - Пример: регистрация → проверка в auth + notification

4. Паттерн Integration-теста (межсервисного)
   - Отличие от e2e: 2 сервиса, остальные замокированы
   - Пример: auth публикует событие → notification получает

5. Асинхронные события
   - Polling: интервал 100ms, таймаут 5s (ссылка на standard-testing.md)
   - Паттерн: retry loop с assertion
   - Пример кода

6. Fixtures и тестовые данные
   - Расположение: tests/fixtures/
   - Factories: минимальный валидный объект
   - Seed data: через API (e2e), через repository (integration)
   - Очистка: truncate между тестами
   - Ссылка на standard-testing.md § Тестовые данные (принципы)

7. Load-тесты
   - Инструмент: k6 / locust (определяется в Design)
   - Расположение: tests/load/
   - Запуск: make test-load
   - Метрики: latency p95, throughput, error rate

8. Smoke-тесты
   - Расположение: tests/smoke/
   - Запуск: make test-smoke (post-deploy)
   - Минимум: GET /health для каждого сервиса
```

### 5. Связывание: кто о чём знает

**Текущее состояние (AS IS) — изолированные острова знаний:**

```
platform/.instructions/standard-docker.md    ← (§ 8 тестовое окружение)
     ↑ никто не ссылается

specs/.instructions/docs/testing/            ← (стратегия документа)
     ↑ system-agent знает

tests/.instructions/                         ← (пусто)

dev-agent AGENT.md                           ← (не знает про docker и тесты)

validation-development.md                    ← (чек-лист, не знает про docker)
```

**Целевое состояние (TO BE) — связанный граф:**

```
platform/.instructions/standard-docker.md § 8
     ↑                    ↑                ↑
     |                    |                |
dev-agent AGENT.md    create-test.md    standard-testing-system.md
  (ссылка в            (ссылка в         (ссылка в
   "Инструкции")        "Предусловия")    § 2 "Тестовое окружение")
     |                    |
     ↓                    ↓
standard-testing-      validation-development.md
system.md              (чек-лист проверок)
  (ссылка в
   "Инструкции")
```

**Конкретные изменения для связывания:**

| Файл | Что добавить |
|------|-------------|
| dev-agent AGENT.md → секция "Инструкции и SSOT" | + `standard-docker.md § 8` — тестовое окружение |
| dev-agent AGENT.md → секция "Инструкции и SSOT" | + `standard-testing-system.md` — паттерны системных тестов |
| dev-agent AGENT.md → Алгоритм, шаг 1 | + `standard-testing-system.md` — прочитать при написании системных тестов |
| create-test.md (новый) → SSOT-зависимости | + `standard-docker.md § 8` — поднятие тестового окружения |
| create-test.md (новый) → SSOT-зависимости | + `standard-testing-system.md` — паттерны тестов (для проверки полноты) |
| standard-testing-system.md (новый) → § 2 | Ссылка на `standard-docker.md § 8` (не дублировать docker) |
| validation-development.md → SSOT-зависимости | + `standard-docker.md` — тестовое окружение |

### 6. Верификация: дополнительные пробелы

Проведена проверка по 4 точкам цепочки: Plan Tests → Issues/Dev-agent → /test → Review. Найдены пробелы помимо трёх исходных (A/B/C).

#### 6.1 Plan Tests: smoke и полнота типов

**Пробел A1:** `standard-plan-test.md` перечисляет только 4 типа в TC-N: `unit | integration | e2e | load`. **Smoke отсутствует**, хотя `standard-testing.md` определяет 5 типов (включая smoke).

**Пробел A2:** `create-plan-test.md` (Шаг 4: Clarify) не требует от LLM предложить ВСЕ типы тестов. Только вопрос про load-тесты в примере. plantest-agent (Шаг 5) не имеет явного требования оценить применимость всех типов.

**Пробел A3:** `plantest-reviewer` (Шаг 6) проверяет покрытие REQ-N/STS-N, но **не проверяет полноту типов** тестов.

| Файл | Что исправить |
|------|-------------|
| `standard-plan-test.md` § 5 | Добавить `smoke` в список типов TC-N |
| `validation-plan-test.md` | Обновить PT014: допустимые типы `unit, integration, e2e, load, smoke` |
| `create-plan-test.md` Шаг 4 | Добавить Clarify-вопрос: "Какие типы тестов применимы?" (ВСЕ 5 типов) |
| `create-plan-test.md` Шаг 5 | plantest-agent: "Оценить применимость всех типов тестов из testing.md" |

#### 6.2 Issues + Dev-agent: передача правил тестирования

**Пробел B1 (КРИТИЧНЫЙ):** dev-agent AGENT.md **не ссылается** на `standard-testing.md` и не читает `specs/docs/.system/testing.md`. Агент знает, что нужны тесты (шаг "make test-{svc}"), но не знает **стратегию**: типы, мокирование, размещение.

**Пробел B2:** Docker-инструкции (`standard-docker.md § 8`) **не прорастают** в dev-agent AGENT.md и validation-development.md. Агент и чек-лист не знают о docker-compose.test.yml, health checks и тестовых сетях. Подробнее: [§ 5 Связывание](#5-связывание-кто-о-чём-знает), исходный Пробел C.

**Пробел B3:** `create-issue.md` включает `testing.md` в body Issue **условно** — только если в TASK-N указано поле `TC:` или тип задачи = "test". Если TC пропущен → testing.md не попадает в Issue → dev-agent не получит ссылку.

**Пробел B4:** Нет стандарта **написания** системных тестов. `tests/.instructions/` — пустой индекс. dev-agent знает КОГДА запускать тесты (standard-development.md § 4) и per-tech паттерны (standard-{tech}.md), но не знает КАК писать e2e/integration тест в этом проекте: docker setup, Arrange/Act/Assert для межсервисного теста, fixtures, polling. Подробнее: [§ 1 Пробел B](#пробел-b-нет-инструкций-для-написания-системных-тестов), [§ 4 Стандарт системных тестов](#4-стандарт-системных-тестов).

| Файл | Что исправить | Пробел |
|------|-------------|--------|
| dev-agent `AGENT.md` → "Инструкции и SSOT" | + `standard-testing.md` — стратегия тестирования | B1 |
| dev-agent `AGENT.md` → "Инструкции и SSOT" | + `standard-docker.md § 8` — тестовое окружение | B2 |
| dev-agent `AGENT.md` → "Алгоритм", шаг 1 | + "Прочитать testing.md перед написанием тестов" | B1 |
| `validation-development.md` → SSOT-зависимости | + `standard-docker.md` — тестовое окружение | B2 |
| `create-issue.md` → матрица документов | testing.md: **всегда** включать (backend, frontend, infra), не только при TC | B3 |
| `tests/.instructions/standard-testing-system.md` | Создать стандарт написания системных тестов | B4 |

#### 6.3 /test: самодостаточность

**Пробел C1:** Шаг 6 (E2E) спрашивает пользователя `AskUserQuestion: "Запустить E2E тесты?"` вместо анализа `git diff`. Пользователь может ответить "нет" → межсервисные баги пройдут.

**Пробел C2:** Нет синхронизации с main перед тестами. Если main обновился → тесты могут упасть в неизменённом коде → ложные результаты.

**Пробел C3:** Шаг 2 (Docker up) использует `--wait`, но не документирует: какие health checks ожидаются, что делать при failure, команды диагностики.

**Пробел C4:** Нет маппинга "code diff → обязательные команды". validation-development.md содержит таблицу (API/DB → e2e обязателен), но /test не использует её автоматически.

| Изменение в описании /test | Где |
|---------------------------|-----|
| Шаг 1.5: `git merge origin/main` перед тестами | create-test.md |
| Шаг 2: Явные health checks + диагностика при failure | create-test.md |
| Шаг 6: Анализ `git diff` → если API/DB/inter-service → e2e обязателен (без AskUser) | create-test.md |
| Шаг 6: Маппинг из validation-development.md (сценарий → команды) | create-test.md |

#### 6.4 Review: покрытие тестов по стандартам

**Пробел D1:** code-reviewer `AGENT.md` **не ссылается** на `standard-docker.md`. Не проверяет конфигурацию docker-compose.test.yml.

**Пробел D2:** TC-N сверка поверхностная — только счётчик "X/Y реализовано", без деталей какие TC пропущены и почему.

**Пробел D3:** `.github/.instructions/review/standard-review.md` говорит "покрытие тестами" без детализации (coverage %, типы тестов, мокирование по стратегии).

| Файл | Что исправить |
|------|-------------|
| code-reviewer `AGENT.md` → Проход 5 | Расширить: проверка типов тестов, мокирования по testing.md |
| code-reviewer `AGENT.md` → Формат вывода | TC-N: список нереализованных, не только счётчик |
| code-reviewer `AGENT.md` → SSOT | + `standard-docker.md` — инфраструктура тестов |

### 7. Изменения в файлах

| # | Файл | Что изменить | Тип | Пробел |
|---|------|-------------|-----|--------|
| 1 | `.github/.instructions/development/create-test.md` | Создать SSOT-инструкцию скилла /test (воркфлоу оркестрации) | Новый | A, C1-C4 |
| 2 | `.claude/skills/test/SKILL.md` | Создать скилл /test | Новый | A |
| 3 | `tests/.instructions/standard-testing-system.md` | Создать стандарт написания системных тестов | Новый | B4 |
| 4 | `.claude/agents/dev-agent/AGENT.md` | + docker + testing-system + standard-testing.md | Изменение | B1, B2 |
| 5 | `specs/.instructions/create-chain.md` | Task 8, перенумерация 13→14 задач | Изменение | A |
| 6 | `specs/.instructions/standard-process.md` | Шаг 4.4, диаграмма, таблица § 8 | Изменение | A |
| 7 | `.github/.instructions/development/validation-development.md` | + ссылка на standard-docker.md | Изменение | B2 |
| 8 | `specs/.instructions/analysis/plan-test/standard-plan-test.md` | + smoke в типы TC-N | Изменение | A1 |
| 9 | `specs/.instructions/analysis/plan-test/validation-plan-test.md` | PT014: + smoke в допустимые типы | Изменение | A1 |
| 10 | `specs/.instructions/analysis/plan-test/create-plan-test.md` | Clarify: "Какие типы тестов?" + agent: "оценить все 5 типов" | Изменение | A2, A3 |
| 11 | `.github/.instructions/issues/create-issue.md` | testing.md: всегда включать, не только при TC | Изменение | B3 |
| 12 | `.claude/agents/code-reviewer/AGENT.md` | + standard-docker.md, расширить Проход 5, TC-N детализация | Изменение | D1-D3 |
| 13 | `.github/.instructions/development/README.md` | Зарегистрировать create-test.md | Индекс | — |
| 14 | `.claude/skills/README.md` | Зарегистрировать /test | Индекс | — |
| 15 | `tests/.instructions/README.md` | Зарегистрировать standard-testing-system.md | Индекс | — |
| 16 | `.github/.instructions/review/standard-review.md` | + note про содержательные критерии в code-reviewer AGENT.md | Изменение | D3 |

### 8. Детальные изменения (AS IS → TO BE)

Для каждого модифицируемого файла — точный текущий текст и целевой текст. Достаточно для исполнения без дополнительного чтения файлов.

#### 8.1 TASK 4: dev-agent AGENT.md

**Файл:** `.claude/agents/dev-agent/AGENT.md`

**Изменение 4.1 — Секция "Инструкции и SSOT" (строки 86-91)**

AS IS:
```markdown
## Инструкции и SSOT

Релевантные инструкции:
- `/.instructions/standard-principles.md` — принципы кода
- `/.github/.instructions/commits/standard-commit.md` — формат коммитов
- `/.github/.instructions/development/standard-development.md` — процесс разработки
```

TO BE:
```markdown
## Инструкции и SSOT

Релевантные инструкции:
- `/.instructions/standard-principles.md` — принципы кода
- `/.github/.instructions/commits/standard-commit.md` — формат коммитов
- `/.github/.instructions/development/standard-development.md` — процесс разработки
- `/platform/.instructions/standard-docker.md` § 8 — тестовое окружение (docker-compose.test.yml, tmpfs, сети)
- `/tests/.instructions/standard-testing-system.md` — паттерны системных тестов (e2e, integration, fixtures)
- `/specs/.instructions/docs/testing/standard-testing.md` — стратегия тестирования (типы, мокирование, данные)
```

**Изменение 4.2 — Алгоритм работы, шаг 1 "Прочитать контекст" (строки 37-42)**

AS IS:
```markdown
1. **Прочитать контекст:**
   - `plan-dev.md` — задачи BLOCK-N (TASK-N, подзадачи, чекбоксы)
   - `plan-test.md` — TC-N acceptance-сценарии для блока
   - `specs/docs/{svc}.md` для каждого сервиса — Code Map, API контракты, Границы автономии LLM
   - `design.md` — SVC-N секции (контекст решений, INT-N контракты)
   - `specs/docs/.system/conventions.md` — shared-интерфейсы, конвенции API, форматы ответов
```

TO BE:
```markdown
1. **Прочитать контекст:**
   - `plan-dev.md` — задачи BLOCK-N (TASK-N, подзадачи, чекбоксы)
   - `plan-test.md` — TC-N acceptance-сценарии для блока
   - `specs/docs/{svc}.md` для каждого сервиса — Code Map, API контракты, Границы автономии LLM
   - `design.md` — SVC-N секции (контекст решений, INT-N контракты)
   - `specs/docs/.system/conventions.md` — shared-интерфейсы, конвенции API, форматы ответов
   - `specs/docs/.system/testing.md` — стратегия тестирования (типы, мокирование, размещение)
   - Если BLOCK содержит e2e/integration задачи → прочитать `tests/.instructions/standard-testing-system.md` (паттерны системных тестов)
```

---

#### 8.2 TASK 5: validation-development.md

**Файл:** `.github/.instructions/development/validation-development.md`

**Изменение 5.1 — SSOT-зависимости (строки 17-26): добавить ссылку на standard-docker.md**

AS IS:
```markdown
**SSOT-зависимости:**
- [standard-development.md](./standard-development.md) — стандарт процесса разработки (SSOT правил)

**Управление статусами:** [`chain_status.py`](/specs/.instructions/.scripts/chain_status.py) — SSOT-модуль для переходов статусов analysis chain.
- [CLAUDE.md](/CLAUDE.md) — make-команды проекта
- [standard-branching.md](../branches/standard-branching.md) — имя ветки = имя папки analysis chain, § 6 валидация имени
- [standard-principles.md](/.instructions/standard-principles.md) — принципы программирования
- [standard-issue.md](../issues/standard-issue.md) — критерии готовности, описание задачи
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) — стратегия тестирования
- [standard-sync.md](../sync/standard-sync.md) — синхронизация main перед запуском тестов
```

TO BE:
```markdown
**SSOT-зависимости:**
- [standard-development.md](./standard-development.md) — стандарт процесса разработки (SSOT правил)

**Управление статусами:** [`chain_status.py`](/specs/.instructions/.scripts/chain_status.py) — SSOT-модуль для переходов статусов analysis chain.
- [CLAUDE.md](/CLAUDE.md) — make-команды проекта
- [standard-branching.md](../branches/standard-branching.md) — имя ветки = имя папки analysis chain, § 6 валидация имени
- [standard-principles.md](/.instructions/standard-principles.md) — принципы программирования
- [standard-issue.md](../issues/standard-issue.md) — критерии готовности, описание задачи
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) — стратегия тестирования
- [standard-sync.md](../sync/standard-sync.md) — синхронизация main перед запуском тестов
- [standard-docker.md](/platform/.instructions/standard-docker.md) § 8 — тестовое окружение (docker-compose.test.yml, health checks)
```

---

#### 8.3 TASK 6: create-chain.md

**Файл:** `specs/.instructions/create-chain.md`

**Изменение 6.1 — Заголовок Happy Path (строка 141)**

AS IS:
```markdown
### Путь A: Happy Path (13 задач)
```

TO BE:
```markdown
### Путь A: Happy Path (14 задач)
```

**Изменение 6.2 — Вставить Task 8, перенумеровать Tasks 8-13 → 9-14 (строки 203-254)**

AS IS (Task 7 и Task 8):
```
TASK 7: Разработка
  description: >
    Скилл: /dev — оркестрация разработки.
    Агент: dev-agent (код, тесты по BLOCK-N в изолированном контексте).
    Коммиты: скилл /commit (Conventional Commits).
    Параллельные агенты по волнам. Per-service тесты внутри блока,
    системные тесты после волны.
    При CONFLICT → динамические задачи добавляются в TaskList (см. CONFLICT).
    SSOT: standard-development.md
  activeForm: Разработка
  blockedBy: [6]

TASK 8: Ревью ветки
  description: >
    Скилл: /review — локальное ревью ветки перед PR.
    Агент: code-reviewer (анализ diff по 7 критериям, сверка со specs/analysis/).
    Вердикт: READY → продолжить, NOT READY → исправить, CONFLICT → Путь B.
    SSOT: standard-review.md
  activeForm: Ревью ветки
  blockedBy: [7]
```

TO BE (Task 7, новый Task 8, перенумерованный Task 9):
```
TASK 7: Разработка
  description: >
    Скилл: /dev — оркестрация разработки.
    Агент: dev-agent (код, тесты по BLOCK-N в изолированном контексте).
    Коммиты: скилл /commit (Conventional Commits).
    Параллельные агенты по волнам. Per-service тесты внутри блока,
    системные тесты после волны.
    При CONFLICT → динамические задачи добавляются в TaskList (см. CONFLICT).
    SSOT: standard-development.md
  activeForm: Разработка
  blockedBy: [6]

TASK 8: Валидация и тесты
  description: >
    Скилл: /test — финальный прогон всех тестов и проверок после завершения разработки.
    Последовательно: sync main → docker up → make test → make lint → make build →
    make test-e2e (если API/DB/inter-service изменения по git diff) → docker down →
    проверка полноты реализации → отчёт.
    Вердикт: READY → ревью. NOT READY → вернуться к Task 7.
    SSOT: create-test.md → validation-development.md
  activeForm: Валидация и тесты
  blockedBy: [7]

TASK 9: Ревью ветки
  description: >
    Скилл: /review — локальное ревью ветки перед PR.
    Агент: code-reviewer (анализ diff по 7 критериям, сверка со specs/analysis/).
    Вердикт: READY → продолжить, NOT READY → исправить, CONFLICT → Путь B.
    SSOT: standard-review.md
  activeForm: Ревью ветки
  blockedBy: [8]
```

**Полная перенумерация оставшихся задач (Tasks 9-13 → 10-14):**

| Было | Стало | blockedBy |
|------|-------|-----------|
| TASK 9: Создать PR, blockedBy: [8] | TASK 10: Создать PR, blockedBy: [9] |
| TASK 10: Ревью PR, blockedBy: [9] | TASK 11: Ревью PR, blockedBy: [10] |
| TASK 11: Merge, blockedBy: [10] | TASK 12: Merge, blockedBy: [11] |
| TASK 12: Завершить цепочку, blockedBy: [11] | TASK 13: Завершить цепочку, blockedBy: [12] |
| TASK 13: Релиз (опционально), blockedBy: [12] | TASK 14: Релиз (опционально), blockedBy: [13] |

**Изменение 6.3 — Оглавление (строка 41)**

AS IS:
```markdown
- [Путь A: Happy Path (13 задач)](#путь-a-happy-path-13-задач)
```

TO BE:
```markdown
- [Путь A: Happy Path (14 задач)](#путь-a-happy-path-14-задач)
```

**Изменение 6.4 — Шаг 2, Раунды (строки 107-108)**

AS IS:
```
1. **Раунд 1:** Создать 13 TaskCreate **последовательно** (по одному за вызов). Каждый TaskCreate — отдельное сообщение. Без blockedBy (TaskCreate не поддерживает). Результат: 13 задач с последовательными ID.
2. **Раунд 2:** Отправить ВСЕ 12 TaskUpdate (addBlockedBy) **параллельно** в одном сообщении. ID известны из Раунда 1.
```

TO BE:
```
1. **Раунд 1:** Создать 14 TaskCreate **последовательно** (по одному за вызов). Каждый TaskCreate — отдельное сообщение. Без blockedBy (TaskCreate не поддерживает). Результат: 14 задач с последовательными ID.
2. **Раунд 2:** Отправить ВСЕ 13 TaskUpdate (addBlockedBy) **параллельно** в одном сообщении. ID известны из Раунда 1.
```

**Изменение 6.5 — Динамическое поведение (строка 273)**

AS IS:
```markdown
- Task 13 (Релиз) — опциональная. Спросить через AskUserQuestion. Если нет — `TaskUpdate status: deleted`
```

TO BE:
```markdown
- Task 14 (Релиз) — опциональная. Спросить через AskUserQuestion. Если нет — `TaskUpdate status: deleted`
```

**Изменение 6.6 — CONFLICT (строка 279): Task 8 → 9, Task 10 → 11**

AS IS:
```markdown
При обнаружении CONFLICT (во время Task 7, 8 или 10) добавить задачи разрешения в TaskList:
```

TO BE:
```markdown
При обнаружении CONFLICT (во время Task 7, 9 или 11) добавить задачи разрешения в TaskList:
```

> Task 7 (Разработка) — без изменений. Task 8 (Ревью ветки) → Task 9, Task 10 (Ревью PR) → Task 11. Шаблоны CONFLICT (N+1, N+2, N+3) — динамические, не меняются.

**Изменение 6.7 — Путь C.2 Hotfix (строки 322-325)**

AS IS:
```markdown
Тот же TaskList что Happy Path (13 задач), но:
- Task 1 (Discussion): пометка "краткая Discussion, фокус на баге"
- Task 6 (dev-create): метки `bug` + `critical`, ветка `{NNNN}-hotfix-{topic}`
- Task 13 (Release): PATCH-версия (обязательна, не опциональна)
```

TO BE:
```markdown
Тот же TaskList что Happy Path (14 задач), но:
- Task 1 (Discussion): пометка "краткая Discussion, фокус на баге"
- Task 6 (dev-create): метки `bug` + `critical`, ветка `{NNNN}-hotfix-{topic}`
- Task 14 (Release): PATCH-версия (обязательна, не опциональна)
```

**Изменение 6.8 — Примеры (строки 357-380)**

AS IS (Запуск новой фичи):
```
# Шаг 2: TaskCreate × 13 задач (шаблон Happy Path)
# Шаг 3: "План из 13 задач создан. Начинаем?" → Да
```

TO BE:
```
# Шаг 2: TaskCreate × 14 задач (шаблон Happy Path)
# Шаг 3: "План из 14 задач создан. Начинаем?" → Да
```

AS IS (Hotfix):
```
# Шаг 2: TaskCreate × 13 задач (Happy Path + метки bug/critical)
# Task 13: Release — обязательна, PATCH-версия
```

TO BE:
```
# Шаг 2: TaskCreate × 14 задач (Happy Path + метки bug/critical)
# Task 14: Release — обязательна, PATCH-версия
```

---

#### 8.4 TASK 7: standard-process.md

**Файл:** `specs/.instructions/standard-process.md`

**Изменение 7.1 — Mermaid-диаграмма Фазы 4 (строки 85-89): добавить узел FINALTEST**

AS IS:
```
    subgraph phase4["Фаза 4: Реализация<br/>(цикл per TASK-N)"]
        DEV["4.1 Development"]
        VALIDATE["4.2 Локальная валидация"]
        COMMIT["4.3 Commits"]
    end
```

TO BE:
```
    subgraph phase4["Фаза 4: Реализация<br/>(цикл per TASK-N)"]
        DEV["4.1 Development"]
        VALIDATE["4.2 Локальная валидация"]
        COMMIT["4.3 Commits"]
        FINALTEST["4.4 Финальная валидация<br/>/test"]
    end
```

**Изменение 7.2 — Mermaid-стрелки (строка 116): COMMIT → FINALTEST → BREVIEW**

AS IS:
```
    COMMIT -- "все TASK-N done" --> BREVIEW
```

TO BE:
```
    COMMIT -- "все TASK-N done" --> FINALTEST
    FINALTEST -- "READY" --> BREVIEW
    FINALTEST -- "NOT READY" --> DEV
```

**Изменение 7.3 — Таблица Фазы 4 (строки 260-264): добавить строку 4.4**

AS IS:
```markdown
| 4.1 | Development | Блоки (BLOCK-N) по волнам, dev-agent параллельно, CONFLICT-детекция | dev-agent | [modify-development.md](/.github/.instructions/development/modify-development.md) |
| 4.2 | Локальная валидация | `make test`, `make lint` + `make test-e2e` (при изменениях API/DB/inter-service) | `/principles-validate` | [validation-development.md](/.github/.instructions/development/validation-development.md) |
| 4.3 | Commits | Conventional Commits, [29 pre-commit хуков](/.structure/pre-commit.md) | — | [standard-commit.md](/.github/.instructions/commits/standard-commit.md) |
```

TO BE:
```markdown
| 4.1 | Development | Блоки (BLOCK-N) по волнам, dev-agent параллельно, CONFLICT-детекция | dev-agent | [modify-development.md](/.github/.instructions/development/modify-development.md) |
| 4.2 | Локальная валидация | `make test`, `make lint` + `make test-e2e` (при изменениях API/DB/inter-service) | `/principles-validate` | [validation-development.md](/.github/.instructions/development/validation-development.md) |
| 4.3 | Commits | Conventional Commits, [29 pre-commit хуков](/.structure/pre-commit.md) | — | [standard-commit.md](/.github/.instructions/commits/standard-commit.md) |
| 4.4 | Финальная валидация | Все TASK-N done → sync main → полный прогон тестов → отчёт | `/test` | [create-test.md](/.github/.instructions/development/create-test.md) |
```

**Изменение 7.4 — Сводная таблица § 8 (строки 434-437): добавить строку 4.4**

AS IS:
```markdown
| **Фаза 4: Реализация** | | | | |
| 4.1 Development | standard-development, modify-development, standard-testing | — | dev-agent | — |
| 4.2 Validation | validation-development, standard-testing | /principles-validate | — | validate-principles.py |
| 4.3 Commits | standard-commit, create-commit | /commit | — | validate-commit-msg.py |
```

TO BE:
```markdown
| **Фаза 4: Реализация** | | | | |
| 4.1 Development | standard-development, modify-development, standard-testing | — | dev-agent | — |
| 4.2 Validation | validation-development, standard-testing | /principles-validate | — | validate-principles.py |
| 4.3 Commits | standard-commit, create-commit | /commit | — | validate-commit-msg.py |
| 4.4 Финальная валидация | create-test, validation-development, standard-docker § 8 | /test | — | — |
```

---

#### 8.5 TASK 8: plan-test (3 файла)

##### 8.5.1 standard-plan-test.md

**Файл:** `specs/.instructions/analysis/plan-test/standard-plan-test.md`

**Изменение 8.1a — Формат TC-N, колонка "Тип" (строка 216)**

AS IS:
```markdown
| **Тип** | unit / integration / e2e / load |
```

TO BE:
```markdown
| **Тип** | unit / integration / e2e / load / smoke |
```

**Изменение 8.1b — Таблица типов тестов (строки 222-227): добавить smoke**

AS IS:
```markdown
| **unit** | Логика одного компонента, модуля или функции сервиса | `/src/{svc}/tests/` |
| **integration** | Взаимодействие между компонентами внутри сервиса или с внешними зависимостями | `/src/{svc}/tests/` |
| **e2e** | Кросс-сервисный сценарий, полный путь от клиента через несколько сервисов | `/tests/` |
| **load** | Нагрузочное тестирование (RPS, latency, конкурентность) | `/tests/` |
```

TO BE:
```markdown
| **unit** | Логика одного компонента, модуля или функции сервиса | `/src/{svc}/tests/` |
| **integration** | Взаимодействие между компонентами внутри сервиса или с внешними зависимостями | `/src/{svc}/tests/` |
| **e2e** | Кросс-сервисный сценарий, полный путь от клиента через несколько сервисов | `/tests/` |
| **load** | Нагрузочное тестирование (RPS, latency, конкурентность) | `/tests/` |
| **smoke** | Минимальная проверка работоспособности после деплоя (health endpoints) | `/tests/` |
```

**Изменение 8.1c — Чек-лист § 8, формат TC-N (строка 540)**

AS IS:
```markdown
- [ ] Тип — один из: unit, integration, e2e, load
```

TO BE:
```markdown
- [ ] Тип — один из: unit, integration, e2e, load, smoke
```

##### 8.5.2 validation-plan-test.md

**Файл:** `specs/.instructions/analysis/plan-test/validation-plan-test.md`

**Изменение 8.2a — Шаг 5, таблица проверки TC-N (строка 146)**

AS IS:
```markdown
| Тип | Одно из: `unit`, `integration`, `e2e`, `load` |
```

TO BE:
```markdown
| Тип | Одно из: `unit`, `integration`, `e2e`, `load`, `smoke` |
```

**Изменение 8.2b — Чек-лист, формат TC-N (строка 266)**

AS IS:
```markdown
- [ ] Тип — один из: unit, integration, e2e, load
```

TO BE:
```markdown
- [ ] Тип — один из: unit, integration, e2e, load, smoke
```

**Изменение 8.2c — Типичные ошибки, PT014 (строка 332)**

AS IS:
```markdown
| TC-N: невалидный тип | PT014 | Тип не из списка: unit, integration, e2e, load | Исправить тип |
```

TO BE:
```markdown
| TC-N: невалидный тип | PT014 | Тип не из списка: unit, integration, e2e, load, smoke | Исправить тип |
```

##### 8.5.3 create-plan-test.md

**Файл:** `specs/.instructions/analysis/plan-test/create-plan-test.md`

**Изменение 8.3a — Шаг 4 Clarify, первая строка таблицы (строки 115-116)**

AS IS:
```markdown
| Типы тестов | «Нужны ли load-тесты для auth? SLA = 10k RPS» |
```

TO BE:
```markdown
| Полнота типов тестов | «Какие из 5 типов (unit, integration, e2e, load, smoke) применимы? Предлагаю: unit + integration + e2e. Load — нет (нет SLA). Smoke — нет (нет деплоя)» |
```

**Изменение 8.3b — Шаг 5 plantest-agent, промпт агента (строки 131-147): добавить инструкцию про 5 типов**

AS IS:
```
    Ответы Clarify:
    {ответы из Шага 4}
```

TO BE:
```
    Ответы Clarify:
    {ответы из Шага 4}

    ОБЯЗАТЕЛЬНО: оценить применимость ВСЕХ 5 типов тестов (unit, integration,
    e2e, load, smoke) на основе testing.md. Для каждого неприменимого типа —
    записать обоснование в Резюме.
```

**Изменение 8.3c — Шаг 5, описание действий агента (строки 149-153)**

AS IS:
```markdown
**Агент самостоятельно:**
1. Читает Design, Discussion, specs/docs/{svc}.md, testing.md
2. Генерирует TC-N, fixtures, матрицу покрытия, блоки тестирования
3. Записывает в plan-test.md инкрементально через Edit
```

TO BE:
```markdown
**Агент самостоятельно:**
1. Читает Design, Discussion, specs/docs/{svc}.md, testing.md
2. Оценивает применимость всех 5 типов тестов (unit, integration, e2e, load, smoke)
3. Генерирует TC-N, fixtures, матрицу покрытия, блоки тестирования
4. Записывает в plan-test.md инкрементально через Edit
```

---

#### 8.6 TASK 9: create-issue.md

**Файл:** `.github/.instructions/issues/create-issue.md`

**Изменение 9.1 — Шаг 6 "Фильтрация .system/ по типу сервиса", таблица (строки 195-200)**

AS IS:
```markdown
| Тип задачи | overview.md | conventions.md | infrastructure.md | testing.md |
|------------|:-----------:|:--------------:|:-----------------:|:----------:|
| frontend | + | + | — | + (если есть TC) |
| backend | + | + | + | + (если есть TC) |
| infra | + | — | + | + (если есть TC) |
| test | + | + | + | + |
```

TO BE:
```markdown
| Тип задачи | overview.md | conventions.md | infrastructure.md | testing.md |
|------------|:-----------:|:--------------:|:-----------------:|:----------:|
| frontend | + | + | — | + |
| backend | + | + | + | + |
| infra | + | — | + | + |
| test | + | + | + | + |
```

**Изменение 9.2 — Шаг 6, текст условия включения testing.md (строка 172)**

AS IS:
```markdown
   Если есть TC → ОБЯЗАТЕЛЬНО включить testing.md
```

TO BE:
```markdown
   testing.md ОБЯЗАТЕЛЬНО включить для всех типов задач
```

---

#### 8.7 TASK 10: code-reviewer AGENT.md + standard-review.md

##### 8.7.1 code-reviewer AGENT.md

**Файл:** `.claude/agents/code-reviewer/AGENT.md`

**Изменение 10.1 — Секция "Инструкции и SSOT" (строки 235-242): добавить standard-docker.md**

AS IS:
```markdown
## Инструкции и SSOT

Релевантные инструкции:
- `specs/.instructions/analysis/review/standard-review.md` — стандарт review.md, приоритеты P1/P2/P3, формат RV-N
- `.github/.instructions/review/validation-review.md` — SSOT процесса ревью GitHub
- `.github/.instructions/review/standard-review.md` — стандарт GitHub review и merge
- `.instructions/standard-principles.md` — принципы кода
- `specs/.instructions/analysis/standard-analysis.md` — структура analysis chain
```

TO BE:
```markdown
## Инструкции и SSOT

Релевантные инструкции:
- `specs/.instructions/analysis/review/standard-review.md` — стандарт review.md, приоритеты P1/P2/P3, формат RV-N
- `.github/.instructions/review/validation-review.md` — SSOT процесса ревью GitHub
- `.github/.instructions/review/standard-review.md` — стандарт GitHub review и merge
- `.instructions/standard-principles.md` — принципы кода
- `specs/.instructions/analysis/standard-analysis.md` — структура analysis chain
- `/platform/.instructions/standard-docker.md` — инфраструктура тестов (docker-compose.test.yml, health checks)
```

**Изменение 10.2 — Проход 5, проверка тестов (строка 162): расширить**

AS IS:
```markdown
- Тесты не соответствуют `testing.md` (типы, мокирование)
```

TO BE:
```markdown
- Тесты не соответствуют `testing.md`:
  - Типы тестов: unit/integration/e2e/load/smoke — применены корректные типы по testing.md
  - Размещение файлов: per-service в `src/{svc}/tests/`, системные в `tests/`
  - Мокирование: стратегия соответствует testing.md (что мокировать, что поднимать)
  - Docker-зависимости: тесты, требующие инфраструктуру, ссылаются на docker-compose.test.yml
```

**Изменение 10.3 — Формат вывода, секция "Сверка с постановкой" (строки 293-296): добавить детализацию TC-N**

AS IS:
```markdown
- TASK-N для {svc}: {X}/{Y} выполнено
- TC-N для {svc}: {X}/{Y} реализовано
- Расхождения: {есть / нет}
- Вне scope: {есть / нет}
```

TO BE:
```markdown
- TASK-N для {svc}: {X}/{Y} выполнено
- TC-N для {svc}: {X}/{Y} реализовано
  Нереализованные: {TC-N1: описание, TC-N2: описание} (если есть)
- Расхождения: {есть / нет}
- Вне scope: {есть / нет}
```

##### 8.7.2 standard-review.md

**Файл:** `.github/.instructions/review/standard-review.md`

**Изменение 10.4 — Секция "Агент проверяет" (строки 76-82): добавить note**

AS IS:
```markdown
**Агент проверяет:**
- Соответствие требованиям Issue
- Качество кода (читаемость, принципы)
- Очевидные ошибки (опечатки, debug-код)
- TODO/FIXME без Issue
- Покрытие тестами
```

TO BE:
```markdown
**Агент проверяет:**
- Соответствие требованиям Issue
- Качество кода (читаемость, принципы)
- Очевидные ошибки (опечатки, debug-код)
- TODO/FIXME без Issue
- Покрытие тестами (содержательные критерии — в [code-reviewer AGENT.md](/.claude/agents/code-reviewer/AGENT.md), Проходы 4-5)
```

---

## Решения

1. **Task 8 (Валидация и тесты) — отдельная задача в chain, не часть Task 7.** Финальная валидация — отдельная точка качества с чётким входом (все TASK-N done) и выходом (все тесты зелёные). При resume — знаем что разработка завершена.

2. **Три артефакта вместо одного.** create-test.md (воркфлоу оркестрации) + standard-testing-system.md (паттерны написания тестов) + обновление dev-agent (связывание). Каждый решает свою задачу, не дублирует.

3. **standard-testing-system.md в tests/.instructions/, не в specs/.instructions/.** Это инструкции для написания кода тестов — рядом с кодом тестов. specs/.instructions/docs/testing/ — про документирование стратегии (другая аудитория, другой жизненный цикл).

4. **Не дублировать Docker.** standard-testing-system.md ссылается на standard-docker.md § 8 для деталей docker-compose.test.yml. Только высокоуровневые команды (up/down/wait) в стандарте тестов.

5. **Нумерация chain: 13 → 14 задач.** В CONFLICT-задачах ссылки динамические (N+1, N+2, N+3) — не ломаются.

6. **create-test.md — нужен.** validation-development.md = чек-лист "что проверить". create-test.md = воркфлоу "как оркестрировать" (предусловия, docker up, порядок, docker down, отчёт, вердикт). Разная зона ответственности.

7. **smoke добавить в plan-test, но НЕ добавлять security/chaos/contract.** Smoke = обязательный тип в testing.md. Остальные = расширяемые, их место в конкретном Design, а не в стандарте plan-test.

8. **testing.md всегда включать в Issue.** Условие "только при TC" слишком узкое — даже backend-задача без явных TC может требовать тестов (регрессия, unit для нового кода).

9. **E2E в /test — обязателен по git diff, без AskUser.** Анализ `git diff --name-only main...HEAD` → если затронуты API/DB/inter-service файлы → e2e запускается автоматически. Иначе — skip с пометкой в отчёте.

10. **Load и smoke НЕ в /test — правильно.** Load = pre-release (Фаза 7). Smoke = post-deploy. Это другие фазы процесса, не Task 8.

11. **Plan-test миграция: вручную все 3 файла + /migration-validate.** Изменения точечные (добавление "smoke" в списки), /migration-create избыточен. Обновить standard → validation → create вручную по AS IS → TO BE из секции 8.5, затем /migration-validate для проверки согласованности.

12. **Review scope: AGENT.md (детали) + note в standard-review.md (ссылка).** Содержательные критерии проверки тестов — в code-reviewer AGENT.md (Проходы 4-5). standard-review.md получает только note-ссылку, не дублирует содержание.

---

## Открытые вопросы

*Нет открытых вопросов. Все решения приняты.*

---

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

TASK 1: Создать стандарт системных тестов
  description: >
    Драфт: секция "4. Стандарт системных тестов" | Пробел: B4
    Скилл: /instruction-create
    Создать tests/.instructions/standard-testing-system.md — стандарт написания
    системных тестов (e2e, integration, load, smoke). 8 секций: назначение,
    тестовое окружение (ссылка на standard-docker.md § 8), паттерн e2e-теста,
    паттерн integration-теста, асинхронные события, fixtures, load-тесты, smoke-тесты.
    Зарегистрировать в tests/.instructions/README.md.
  activeForm: Создаю стандарт системных тестов

TASK 2: Создать SSOT-инструкцию create-test.md
  description: >
    Драфт: секция "3. Скилл /test" + секция "6.3 /test: самодостаточность" | Пробелы: C1-C4
    Скилл: /instruction-create
    Создать .github/.instructions/development/create-test.md — воркфлоу финальной
    валидации. Обновлённые шаги (с учётом верификации):
    Шаг 1: Предусловия (ветка, docker-compose.test.yml, TASK-N done)
    Шаг 1.5: Sync с main — git fetch origin && git merge origin/main (C2)
    Шаг 2: Docker up + явные health checks + диагностика при failure (C3)
    Шаг 3: make test
    Шаг 4: make lint
    Шаг 5: make build
    Шаг 6: E2E — анализ git diff → если API/DB/inter-service → обязателен (C1, C4)
    Шаг 7: Docker down
    Шаг 8: Полнота реализации (plan-dev.md, Issues)
    Шаг 9: Отчёт (таблица + вердикт READY/NOT READY)
    SSOT-зависимости: validation-development.md, standard-docker.md § 8,
    standard-testing-system.md.
    Зарегистрировать в .github/.instructions/development/README.md.
  activeForm: Создаю инструкцию create-test.md

TASK 3: Создать скилл /test
  blockedBy: [2]
  description: >
    Драфт: секция "3. Скилл /test"
    Скилл: /skill-create
    Создать .claude/skills/test/SKILL.md — скилл финальной валидации.
    SSOT-ссылка: .github/.instructions/development/create-test.md (из TASK 2).
    Зарегистрировать в .claude/skills/README.md.
  activeForm: Создаю скилл /test

TASK 4: Обновить dev-agent — добавить ссылки на docker, тесты, стратегию
  blockedBy: [1]
  description: >
    Драфт: секция "5. Связывание" + секция "6.2" | Пробелы: B1, B2
    Скилл: /agent-modify
    Обновить .claude/agents/dev-agent/AGENT.md:
    1. В секцию "Инструкции и SSOT" добавить:
       - platform/.instructions/standard-docker.md § 8 — тестовое окружение (B2)
       - tests/.instructions/standard-testing-system.md — паттерны системных тестов (B4)
       - specs/.instructions/docs/testing/standard-testing.md — стратегия тестирования (B1)
    2. В "Алгоритм работы", шаг 1 "Прочитать контекст" добавить:
       - "Прочитать testing.md из Issue перед написанием тестов" (B1)
       - standard-testing-system.md — при BLOCK с e2e/integration (B4)
  activeForm: Обновляю dev-agent

TASK 5: Обновить validation-development.md — добавить ссылку на docker
  description: >
    Драфт: секция "5. Связывание" | Пробел: B2
    Обновить .github/.instructions/development/validation-development.md:
    Добавить в SSOT-зависимости ссылку на standard-docker.md (тестовое окружение).
  activeForm: Обновляю validation-development.md

TASK 6: Обновить create-chain.md — добавить Task 8 (Валидация и тесты)
  blockedBy: [3]
  description: >
    Драфт: секция "2. Решение"
    Обновить specs/.instructions/create-chain.md:
    1. Вставить Task 8 (Валидация и тесты) между текущими Task 7 и Task 8
    2. Перенумеровать Task 8→9, 9→10, 10→11, 11→12, 12→13, 13→14
    3. Обновить blockedBy во всех задачах
    4. Обновить "13 задач" → "14 задач" (оглавление, заголовок, Шаг 2 раунды, примеры)
    5. Обновить "12 TaskUpdate" → "13 TaskUpdate" (Шаг 2 Раунд 2)
    6. Обновить CONFLICT: "Task 7, 8 или 10" → "Task 7, 9 или 11" (шаблоны N+1/N+2/N+3 — динамические, не меняются)
    7. Обновить Hotfix: "13 задач" → "14 задач", "Task 13" → "Task 14"
    8. Обновить Динамическое поведение: "Task 13 (Релиз)" → "Task 14 (Релиз)"
    Точные изменения: см. драфт секция "8.3 TASK 6"
  activeForm: Обновляю create-chain.md

TASK 7: Обновить standard-process.md — добавить шаг 4.4
  blockedBy: [3]
  description: >
    Драфт: секция "2. Решение"
    Обновить specs/.instructions/standard-process.md:
    1. Добавить строку "4.4 Финальная валидация" в таблицу Фазы 4
    2. Обновить диаграмму mermaid (VALIDATE → стрелка между COMMIT и BREVIEW)
    3. Обновить сводную таблицу инструментов § 8
    4. Запустить /migration-create для синхронизации зависимостей
  activeForm: Обновляю standard-process.md

TASK 8: Обновить plan-test — добавить smoke и требование полноты типов
  description: >
    Драфт: секция "6.1 Plan Tests" | Пробелы: A1, A2, A3
    1. standard-plan-test.md § 5: добавить "smoke" в типы TC-N (unit/integration/e2e/load/smoke)
    2. validation-plan-test.md PT014: обновить допустимые типы (+ smoke)
    3. create-plan-test.md Шаг 4 (Clarify): добавить вопрос "Какие типы тестов применимы?" (все 5)
    4. create-plan-test.md Шаг 5 (plantest-agent): "Оценить применимость всех 5 типов из testing.md"
    5. Миграция: вручную обновить все 3 файла (standard + validation + create),
       затем /migration-validate для standard-plan-test.md (стандарт изменился).
       НЕ использовать /migration-create — изменения точечные, описаны в секции 8.5.
    Точные изменения: см. драфт секция "8.5 TASK 8"
  activeForm: Обновляю plan-test инструкции

TASK 9: Обновить create-issue.md — testing.md всегда включать
  description: >
    Драфт: секция "6.2 Issues" | Пробел: B3
    Обновить .github/.instructions/issues/create-issue.md:
    В матрице документов (§ 4.2.2): testing.md — ВСЕГДА включать для backend, frontend, infra.
    Убрать условие "только если есть TC". Обоснование: даже задача без явных TC
    может требовать тестов (регрессия, unit для нового кода).
  activeForm: Обновляю create-issue.md

TASK 10: Обновить code-reviewer + standard-review.md — тесты, docker, TC-N детализация
  description: >
    Драфт: секция "6.4 Review" + секция "8.7" | Пробелы: D1, D2, D3
    Скилл: /agent-modify (для AGENT.md), ручная правка (для standard-review.md)
    1. code-reviewer AGENT.md → SSOT: + standard-docker.md — инфраструктура тестов (D1)
    2. code-reviewer AGENT.md → Проход 5: расширить проверку — типы тестов по testing.md, мокирование, размещение, docker (D3)
    3. code-reviewer AGENT.md → Формат вывода: TC-N — список нереализованных TC, не только счётчик X/Y (D2)
    4. standard-review.md → "Покрытие тестами" + note "(содержательные критерии — в code-reviewer AGENT.md, Проходы 4-5)" (D3)
    Точные изменения: см. драфт секция "8.7 TASK 10"
  activeForm: Обновляю code-reviewer и standard-review.md

TASK 11: Валидация всех изменений
  blockedBy: [4, 5, 6, 7, 8, 9, 10]
  description: >
    Проверить согласованность всех изменений:
    1. /instruction-validate tests/.instructions/standard-testing-system.md
    2. /instruction-validate .github/.instructions/development/create-test.md
    3. /skill-validate test
    4. /agent-validate dev-agent
    5. /agent-validate code-reviewer
    6. Скилл /test упомянут в standard-process.md § 8 (сводная таблица)
    7. Task 8 в create-chain.md ссылается на /test и create-test.md
    8. Нумерация TaskList корректна (14 задач, blockedBy последовательные)
    9. dev-agent содержит ссылки на docker, testing-system, standard-testing.md
    10. standard-testing-system.md ссылается на standard-docker.md § 8
    11. smoke в standard-plan-test.md § 5 + validation-plan-test.md PT014
    12. create-issue.md: testing.md без условия TC
    13. code-reviewer: standard-docker.md в SSOT, TC-N детализация
    14. /draft-validate для этого черновика
  activeForm: Валидация всех изменений
