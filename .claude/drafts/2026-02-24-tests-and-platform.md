# Аудит тестирования и стандарты platform/ — оценка и план

Проверка полноты регламентации тестов по всей цепочке (планирование → стратегия → код → запуск) и оценка необходимости стандартов для platform/.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Часть A: Аудит тестирования](#часть-a-аудит-тестирования)
  - [Часть B: Стандарты platform/](#часть-b-стандарты-platform)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** Проверить, нет ли пробелов в регламентации работы с тестами; оценить необходимость стандартов для platform/
**Почему создан:** Тестирование покрыто на уровне планирования (Plan Tests) и стратегии (testing.md), но tests/.instructions/ пуст — нет стандартов для самого кода тестов. platform/.instructions/ тоже пуст.
**Связанные файлы:**
- `specs/.instructions/analysis/plan-test/standard-plan-test.md` — планирование тестов (TC-N)
- `specs/.instructions/docs/testing/standard-testing.md` — стратегия тестирования (testing.md)
- `tests/.instructions/README.md` — пусто, нет стандартов
- `platform/.instructions/` — стандарты инфраструктуры (пусто)
- `.structure/README.md` — описание platform/ и tests/

## Содержание

### Часть A: Аудит тестирования

#### Текущее покрытие

| Уровень | Документ | Что регламентирует | Статус |
|---------|----------|--------------------|--------|
| Планирование | `standard-plan-test.md` | HOW TO VERIFY — acceptance-сценарии TC-N, тестовые данные, матрица покрытия | Есть |
| Стратегия | `standard-testing.md` → `docs/.system/testing.md` | Типы тестов, структура файлов, мокирование, межсервисные тесты, данные, команды | Есть |
| Per-tech | `standard-{tech}.md`, секция "Тестирование" | Паттерны тестирования конкретной технологии (pytest, Jest и т.д.) | Создаётся per-tech |
| Процесс запуска | `standard-development.md` | `make test`, `make test-e2e`, порядок при разработке | Есть |
| **Код тестов** | `tests/.instructions/` | **Нет стандартов, нет воркфлоу** | **Пусто** |

#### Что потенциально отсутствует

| Тема | Описание | Где должно быть |
|------|----------|----------------|
| Структура тестового файла | Именование, группировка тестов, порядок arrange-act-assert | `tests/.instructions/standard-tests.md` или per-tech |
| Fixtures и factories | Общие паттерны для fixtures (не per-tech, а архитектурные) | `tests/.instructions/` или `docs/.system/testing.md` |
| Docker для тестов | docker-compose.test.yml — как поднимать зависимости для интеграционных/e2e | `platform/docker/` + `tests/.instructions/` |
| CI pipeline для тестов | GitHub Actions workflow для запуска тестов | `.github/workflows/` + `.github/.instructions/actions/` |
| Coverage requirements | Минимальный % покрытия, какие модули критичны | `docs/.system/testing.md` секция или отдельный стандарт |

#### Ключевой вопрос

Нужен ли `tests/.instructions/standard-tests.md` как отдельный стандарт? Или достаточно:
- `standard-testing.md` (стратегия) + per-tech стандарты (код) + `standard-development.md` (запуск)?

Аргументы **за** отдельный стандарт:
- Единое место для cross-tech правил тестирования (именование, структура, fixtures)
- Docker-окружение для тестов не покрыто ни одним существующим стандартом

Аргументы **против**:
- Per-tech стандарты уже покрывают паттерны тестирования
- `docs/.system/testing.md` покрывает стратегию
- Дублирование информации

### Часть B: Стандарты platform/

#### Текущее состояние platform/

```
platform/
├── .instructions/          # Пусто (только README.md ожидается)
├── docker/                 # .gitkeep + README
├── gateway/                # API Gateway (Traefik/Nginx)
├── k8s/                    # Kubernetes манифесты
├── monitoring/             # Grafana, Loki, Prometheus
│   ├── grafana/
│   ├── loki/
│   └── prometheus/
├── runbooks/               # Операционные runbooks
├── scripts/                # Деплой, бэкап скрипты
└── README.md
```

Все подпапки содержат только `.gitkeep` — реального контента нет.

#### Какие стандарты могут понадобиться

| Стандарт | Для чего | Приоритет |
|----------|----------|-----------|
| `standard-docker.md` | Формат Dockerfile, docker-compose, именование сервисов, сети, volumes | Высокий — нужен при первом сервисе |
| `standard-k8s.md` | Структура манифестов, namespaces, labels, resource limits | Низкий — нужен при деплое в K8s |
| `standard-monitoring.md` | Формат дашбордов, алерты, метрики, логирование | Низкий — нужен при настройке мониторинга |
| `standard-gateway.md` | Маршрутизация, rate limiting, CORS, TLS | Низкий — нужен при настройке gateway |
| `standard-runbooks.md` | Формат runbook, шаблон инцидента, escalation | Низкий — нужен при первом инциденте |
| `standard-scripts.md` | Формат инфра-скриптов (деплой, бэкап, rollback) | Средний — нужен при первом деплое |

#### Связь с тестами

`platform/docker/docker-compose.test.yml` — конфигурация для запуска тестов в Docker. Это пересечение platform/ и tests/. Стандарт Docker должен покрывать и тестовые конфигурации.

### Часть C: Интеграция в standard-process.md

#### Текущее состояние

Шаг 3.1 говорит "Код + unit-тесты по TASK-N". Это покрывает только unit-тесты внутри сервиса (`src/{svc}/tests/`). Не упоминаются:

| Тип тестов | Где живут | Когда запускаются | Упомянут в process.md? |
|------------|-----------|-------------------|----------------------|
| Unit | `src/{svc}/tests/` | Шаг 3.1 (Development) + 3.2 (`make test`) | Да, неявно |
| Integration (inter-service) | `tests/integration/` | После unit, перед PR | **Нет** |
| E2E | `tests/e2e/` | После integration, перед PR | **Нет** |
| Load | `tests/load/` | Перед release | **Нет** |
| Smoke | `tests/smoke/` | После deploy | **Нет** (связано с G8 post-release) |

#### Что добавить в standard-process.md

1. **Фаза 3:** Расширить шаг 3.2 — `make test` (unit) + `make test-integration` + `make test-e2e`
2. **Фаза 3:** Добавить ссылку на `docs/.system/testing.md` как SSOT стратегии
3. **Фаза 6:** Добавить pre-release тесты с полным покрытием (load, smoke)
4. **§8 Сводная таблица:** Добавить `standard-testing.md` в строку 3.1-3.2

#### Обновление testing.md

При изменении стратегии тестирования (новые типы тестов, изменение подхода к мокированию) — `docs/.system/testing.md` обновляется при Plan Tests → DONE. Это уже описано в `standard-plan-test.md`, но не отражено в standard-process.md.

## Решения

- Часть A: нужно провести детальный аудит — прочитать ВСЕ связанные документы и определить конкретные пробелы
- Часть B: `standard-docker.md` нужен первым — остальные стандарты platform/ отложены до реального использования
- Часть C: расширить Фазу 3 и Фазу 6 в standard-process.md для явного включения тестов
- Docker для тестов — покрыть в `standard-docker.md` секцией "Тестовые окружения"

## Открытые вопросы

- Достаточно ли per-tech + testing.md для кода тестов, или нужен `tests/.instructions/standard-tests.md`?
- Docker для тестов: отдельный `docker-compose.test.yml` или override файл (`docker-compose.override.yml`)?
- Coverage requirements: хардкодить минимальный % или оставить на усмотрение per-service?
- Приоритет: сначала аудит тестов или сначала `standard-docker.md`?
- Нужен ли `platform/.instructions/standard-platform.md` как мета-стандарт для всех подпапок platform/?
- Как интегрировать load/smoke тесты в Фазу 6 (pre-release)?

---

## Что уже описано в проекте

Полный реестр всех мест в проекте, где тестирование регламентировано, упоминается или автоматизировано.

### 1. Планирование тестов (Analysis Chain — Plan Tests)

**Файл:** `specs/.instructions/analysis/plan-test/standard-plan-test.md` (v1.1)

Полноценный стандарт третьего уровня SDD-иерархии, отвечающий на вопрос HOW TO VERIFY. Регламентирует:
- **Per-service acceptance-сценарии (TC-N):** формат 5-колоночной таблицы (ID, Описание, Тип, Источник, Данные). Описания — естественные предложения на русском (НЕ Given/When/Then). Типы: unit, integration, e2e, load.
- **Тестовые данные:** fixtures/factories в формате таблицы (Fixture, Описание, Поля). Snake_case именование. Per-service и общие для системных сценариев.
- **Системные тест-сценарии:** кросс-сервисные e2e/integration/load тесты, покрывающие STS-N из Design.
- **Матрица покрытия:** трассируемость REQ-N и STS-N к TC-N. Каждый REQ-N/STS-N должен быть покрыт минимум одним TC-N.
- **Расположение тестов по типам:** unit и integration в `/src/{svc}/tests/`, e2e и load в `/tests/`.
- **Нумерация:** TC-N сквозная по всему документу (не по сервису), пропуски допустимы, перенумерация запрещена.
- **Зона ответственности:** Plan Tests НЕ содержит реализацию тестов (код, фреймворки) — это Plan Dev / разработка. НЕ содержит задачи — это Plan Dev.
- **Побочные эффекты:** при Plan Tests -> DONE обновляется `docs/.system/testing.md` если стратегия тестирования изменилась.
- **Входные данные:** читает Design (SVC-N, INT-N, STS-N), Discussion (REQ-N), `docs/{svc}.md` (AS IS), `docs/.system/testing.md` (стратегия).

**Связанные файлы:**
- `specs/.instructions/analysis/plan-test/create-plan-test.md` — воркфлоу создания
- `specs/.instructions/analysis/plan-test/modify-plan-test.md` — воркфлоу модификации
- `specs/.instructions/analysis/plan-test/validation-plan-test.md` — валидация документа
- `specs/.instructions/.scripts/validate-analysis-plan-test.py` — скрипт валидации (25 кодов ошибок PT001-PT025)
- **Pre-commit хук:** `plan-test-validate` — автоматическая проверка при коммите (`specs/analysis/*/plan-test.md`)

**Скиллы:**
- `/plan-test-create` — создание плана тестов
- `/plan-test-modify` — изменение плана тестов
- `/plan-test-validate` — валидация по стандарту

### 2. Стратегия тестирования (docs/.system/testing.md)

**Стандарт:** `specs/.instructions/docs/testing/standard-testing.md` (v1.1)

Определяет формат и содержание `specs/docs/.system/testing.md` — единого документа стратегии тестирования для LLM-разработчика. Содержит 6 обязательных секций в фиксированном порядке:

1. **Типы тестов** — таблица из 5 колонок (Тип, Что проверяет, Scope, Внешние зависимости, Когда запускается). Базовый набор: Unit, Integration, E2E, Smoke, Load. Расширяемо (Contract, Visual Regression, Property-based).
2. **Структура файлов** — дерево с реальными именами сервисов (не шаблонные `{svc}`). Обязательно: `src/{сервис}/tests/` и `tests/` (e2e, integration, smoke, load).
3. **Стратегия мокирования** — таблица из 6 колонок по уровням (Unit/Integration/E2E) x (БД, Message Broker, Другие сервисы, Shared-код, Внешние API). Ссылка на per-tech паттерны.
4. **Межсервисные тесты** — ссылка на overview.md (Сквозные потоки), docker-compose для поднятия сервисов, паттерн Arrange -> Act -> Assert с проверкой минимум в двух сервисах. Polling для async событий с конкретными параметрами (интервал, таймаут).
5. **Тестовые данные** — подход (factories, fixtures, seed data). 3 обязательных принципа: независимость тестов, минимальность данных, изоляция данных.
6. **Команды запуска** — ссылка на Makefile как SSOT. Примеры прямого вызова для фильтрации. НЕ дублировать make-таргеты.

**Принципы разграничения:** testing.md = стратегия (какие тесты, где, что мокировать). standard-development.md = процесс (когда запускать). standard-{tech}.md = per-tech детали (pytest fixtures, Jest config). overview.md = сквозные потоки (SSOT для e2e сценариев). Makefile = SSOT команд.

**Требования по критичности (секция 6 стандарта):** Зависят от `criticality` поля в `{svc}.md`:
- critical-high: unit coverage >=80%, integration обязательны, e2e обязательны в CI, load обязательно перед релизом, chaos рекомендуется
- critical-medium: unit coverage >=60%, integration обязательны, e2e обязательны в CI, load при значительных изменениях
- critical-low: unit coverage >=40%, integration рекомендуются, e2e опционально, load не требуется

**Связанные файлы:**
- `specs/.instructions/docs/testing/modify-testing.md` — воркфлоу модификации с 6 сценариями (новый тип, добавление/удаление сервиса, изменение мокирования, смена стека, изменение команд, первичное заполнение)
- `specs/.instructions/docs/testing/validation-testing.md` — валидация с 7 кодами ошибок (TST001-TST007)
- `specs/.instructions/.scripts/validate-docs-testing.py` — скрипт валидации (проверяет frontmatter, секции, порядок, таблицы, дерево файлов, принципы тестовых данных, пустые секции)
- **Pre-commit хук:** `testing-validate` — автоматическая проверка при коммите файла `specs/docs/.system/testing.md`

### 3. Per-tech стандарты (секция Тестирование)

**Стандарт:** `specs/.instructions/docs/technology/standard-technology.md`

Каждый `standard-{tech}.md` содержит секцию #7 "Тестирование" с per-tech деталями:
- Фреймворк и инструменты (pytest, Jest, etc.)
- Fixtures/фабрики конкретной технологии
- Типовые паттерны тестов (unit с моками, integration с реальной БД)
- Coverage инструменты (pytest-cov, etc.)

**Пример (из standard-technology.md):** Секция "Тестирование" для PostgreSQL содержит: pytest + pytest-asyncio + factory_boy + pytest-cov, фикстуры db_engine/db_session, паттерн unit-тестов с AsyncMock, паттерн integration-тестов с реальной Docker БД.

**Pre-commit хук:** `technology-validate` — проверяет наличие 8 обязательных секций, включая "Тестирование".

### 4. Процесс разработки (standard-development.md)

**Файл:** `.github/.instructions/development/standard-development.md` (v1.3)

Регламентирует КОГДА запускать тесты в ходе разработки:

- **Секция 2 (Процесс):** Цикл: код -> `make test` -> `make lint` -> commit. Тесты рядом с кодом — unit-тесты создаются вместе с реализацией.
- **Секция 3 (Make-команды):** Таблица тестовых команд: `make test` (unit + integration, при каждом изменении), `make test-e2e` (e2e, перед PR).
- **Секция 4 (Тестирование):**
  - Перед коммитом: `make test` без ошибок, новый код покрыт unit-тестами.
  - Перед PR: `make test` + `make test-e2e` (обязательно при изменениях API, database schema, inter-service communication, gateway routes) + `make build`.
  - Таблица расположения: unit в `/src/{service}/tests/`, системные в `/tests/`.
  - Отладка: таблица симптомов и решений (failing test, connection refused, port in use).
- **Секция 5 (Проверки качества):** `make test` как обязательная проверка перед коммитом. Checklist перед push включает unit-тесты, e2e тесты.
- **Секция 9 (Критичность):** Требования к PR review по уровням criticality (включая test coverage).
- **SSOT-ссылка:** Явная ссылка на `standard-testing.md` для стратегии (КАК писать тесты).

### 5. Валидация разработки (validation-development.md)

**Файл:** `.github/.instructions/development/validation-development.md` (v1.3)

6-шаговая валидация перед push/PR:
- **Шаг 1:** `make test` — exit code 0, новый код покрыт unit-тестами. БЛОКИРОВКА при failing.
- **Шаг 4:** `make test-e2e` — обязательно при изменениях API/DB/inter-service/gateway. Exit code 0.
- **Коды ошибок:** DV001 (failing тесты), DV006 (e2e не запущены), DV009 (нет unit-тестов для нового кода).

### 6. Процесс поставки ценности (standard-process.md)

**Файл:** `specs/.instructions/standard-process.md` (v1.0)

Тестирование упоминается в нескольких фазах:
- **Фаза 1, шаг 1.3:** Plan Tests — HOW TO VERIFY, скилл `/plan-test-create`.
- **Фаза 3, шаг 3.1:** "Код + unit-тесты по TASK-N", скилл `/dev`.
- **Фаза 3, шаг 3.2:** "Локальная валидация", `make test`, `make lint`.
- **Путь B (CONFLICT):** Источники CONFLICT включают тесты ("Тесты падают из-за неверных спецификаций", шаг 3.2).
- **Сводная таблица (8.1):** Plan Tests имеет скрипт `validate-analysis-plan-test.py` и скиллы `/plan-test-create`, `-modify`, `-validate`.
- **Pre-commit хуки (8.2):** `plan-test-validate` на шаге 1.3.
- **Quick Reference (9):** `make test && make lint` на Фазе 3.

**Пробелы в standard-process.md:**
- Шаг 3.2 упоминает только `make test` и `make lint`, не `make test-e2e`.
- Фаза 6 (Поставка/Release) не упоминает pre-release тесты (load, smoke).
- Нет явной ссылки на `standard-testing.md` в таблице инструментов для шагов 3.1-3.2.
- Integration (inter-service), E2E, Load, Smoke тесты не упомянуты в таблице Шаг/Описание.

### 7. Code Review (validation-review.md)

**Файл:** `.github/.instructions/review/validation-review.md` (v1.1)

- **Шаг 2, критерий 5:** "Тесты — Новая функциональность покрыта тестами. Существующие тесты не сломаны".
- **Код ошибки E004:** "Нет тестов — Новая функциональность без тестов — Написать тесты".
- **Приоритет:** Отсутствие тестов — P2 (дефект), AskUserQuestion.

### 8. Makefile

**Файл:** `Makefile`

3 тестовых таргета, все TODO-заглушки:
- `make test` — "TODO: настроить запуск тестов" (unit/integration)
- `make test-e2e` — "TODO: настроить e2e тесты"
- `make test-load` — "TODO: настроить нагрузочные тесты (k6)"

**Замечание:** `make test-load` описан в Makefile, но НЕ упоминается ни в CLAUDE.md, ни в standard-development.md (там только `make test` и `make test-e2e`).

### 9. CLAUDE.md

**Файл:** `CLAUDE.md`

- Команды: `make test` (Unit/integration тесты), `make test-e2e` (E2E тесты).
- Паттерны: "Unit-тесты внутри сервиса: `/src/{service}/tests/`", "Системные тесты между сервисами: `/tests/`".
- Структура: `/src/{service}/` содержит `tests/`, `/tests/` — системные тесты.

### 10. Структура проекта (.structure/README.md)

**Файл:** `.structure/README.md`

- **tests/ описание:** "Системные тесты. Стандарты тестирования (`.instructions/`), end-to-end сценарии (`e2e/`), общие тестовые данные (`fixtures/`), интеграционные тесты между сервисами (`integration/`), нагрузочные тесты на k6 (`load/`), smoke тесты (`smoke/`)".
- **src/ описание:** "unit и integration тесты сервиса (`tests/`)".

### 11. tests/README.md

**Файл:** `tests/README.md`

- Зона ответственности: "Тесты всей системы: e2e, интеграция между сервисами, нагрузка."
- IN: e2e/, integration/, load/, smoke/, fixtures/, conftest.py
- Границы: системные тесты здесь, unit сервиса в `/src/{service}/tests/`, integration внутри сервиса в `/src/{service}/tests/integration/`.
- Структура: e2e/, integration/, load/, smoke/, fixtures/.

### 12. tests/.instructions/README.md

**Файл:** `tests/.instructions/README.md`

Индекс инструкций. ВСЕ секции пусты:
- Стандарты: "Нет стандартов."
- Воркфлоу: "Нет воркфлоу."
- Валидация: "Нет валидаций."
- Скрипты: "Нет скриптов."
- Скиллы: "Нет скиллов."

### 13. platform/.instructions/README.md

**Файл:** `platform/.instructions/README.md`

Индекс инструкций. ВСЕ секции пусты (аналогично tests/.instructions/).

### 14. platform/README.md

**Файл:** `platform/README.md`

- Зона ответственности: "Инфраструктурные конфигурации, скрипты, мониторинг."
- IN: docker/, gateway/, monitoring/, k8s/, scripts/, docs/, runbooks/
- Структура: docker/, gateway/, monitoring/ (prometheus/, grafana/, loki/), k8s/, scripts/, docs/, runbooks/.

### 15. CI Pipeline (.github/workflows/ci.yml)

**Файл:** `.github/workflows/ci.yml`

Текущий CI запускает **только pre-commit хуки** (структура, rules, скиллы, скрипты). НЕ запускает:
- `make test` (unit/integration)
- `make test-e2e` (e2e)
- `make test-load` (load)
- `make lint`
- `make build`

**Замечание:** CI полностью не покрывает тестирование кода. Это только "страховка для pre-commit хуков".

### 16. standard-action.md (GitHub Actions стандарт)

**Файл:** `.github/.instructions/actions/standard-action.md`

Содержит шаблоны для тестовых workflow:
- Job `test:` с `make test`
- Именование: `test-{service}.yml` для тестов конкретного сервиса
- `ci.yml` — общие CI проверки (тесты, линтинг)
- E2E тесты: 30-90 минут таймаут
- Deploy зависит от CI: "тесты — всегда"
- Матричная стратегия для параллелизма (OS: ubuntu/windows/macos)
- Reusable workflows для тестов

### 17. standard-docs.md (мета-стандарт docs/)

**Файл:** `specs/.instructions/docs/standard-docs.md` (v1.0)

- testing.md как один из 5 обязательных системных документов при инициализации docs/
- Секции testing.md: Типы тестов, Структура файлов, Стратегия мокирования, Межсервисные тесты, Тестовые данные, Команды запуска
- Принцип: "Два уровня для тестирования — кросс-сервисная стратегия в `.system/testing.md`, per-tech детали в `.technologies/standard-{tech}.md`"

### 18. src/README.md (структура сервиса)

**Файл:** `src/README.md`

- Каждый сервис содержит `tests/` — "Unit и integration тесты"
- Системные тесты вынесены в `/tests/`

### 19. Pre-commit хуки (.pre-commit-config.yaml + pre-commit.md)

Два хука непосредственно связаны с тестированием:
- **`testing-validate`** — проверяет `specs/docs/.system/testing.md` (формат, секции, таблицы)
- **`plan-test-validate`** — проверяет `specs/analysis/*/plan-test.md` (TC-N формат, покрытие, маркеры)

Остальные 23 хука проверяют структуру, но не тестовый код напрямую.

### 20. Сводная карта покрытия

| Аспект тестирования | Где описан | Полнота |
|---------------------|-----------|---------|
| ЧТО тестировать (acceptance criteria) | Plan Tests (TC-N) | Полная |
| ГДЕ размещать тесты | testing.md (секция Структура файлов) + CLAUDE.md + tests/README.md + src/README.md | Полная |
| КАК мокировать | testing.md (секция Стратегия мокирования) | Полная |
| КАК писать тесты per-tech | standard-{tech}.md (секция Тестирование) | Полная (при наличии per-tech) |
| КОГДА запускать | standard-development.md (секция Тестирование) + validation-development.md | Полная |
| КАКИЕ команды | Makefile (make test, test-e2e, test-load) + CLAUDE.md | Частичная (test-load не в CLAUDE.md) |
| CI pipeline | ci.yml | **Пробел: CI не запускает тесты кода** |
| Coverage requirements | standard-testing.md (секция 6) | Полная (по критичности сервиса) |
| Docker для тестов | testing.md (упоминание docker-compose.test.yml) | **Пробел: нет docker-compose.test.yml, нет стандарта** |
| Тестовые данные (стратегия) | testing.md (секция Тестовые данные) | Полная |
| Fixtures/factories (per-tech) | standard-{tech}.md (секция Тестирование) | Полная (при наличии per-tech) |
| Code review тестов | validation-review.md | Полная (критерий 5, код E004) |
| Pre-release тесты | — | **Пробел: load/smoke не описаны в процессе** |
| Post-deploy smoke | — | **Пробел: связан с G8 (post-release)** |
| Именование тестов | testing.md (вводный абзац Структура файлов) | Частичная (только файлы, не функции) |
| Cross-tech правила тестов | — | **Пробел: нет единого места** |
| Валидация Plan Tests | validate-analysis-plan-test.py + pre-commit | Полная |
| Валидация testing.md | validate-docs-testing.py + pre-commit | Полная |
| Валидация кода тестов | — | **Пробел: нет линтера/валидатора для тестового кода** |

## Best practices

### Test Pyramid (Unit > Integration > E2E)

**Принцип:** Наибольшее количество тестов — unit (быстрые, изолированные, дешёвые). Меньше — integration (медленнее, требуют инфраструктуры). Ещё меньше — e2e (самые медленные, хрупкие, дорогие). Load и smoke — специализированные, запускаются реже.

**Как соотносится с проектом:** Проект правильно разделяет уровни (unit в src/{svc}/tests/, системные в tests/). Testing.md описывает пирамиду через таблицу типов тестов и стратегию мокирования. Standard-testing.md в секции 6 задаёт пороги покрытия по критичности.

**Рекомендация:** Рассмотреть добавление рекомендуемых соотношений (например, 70/20/10 или конкретные числа для проекта) в testing.md. Сейчас есть только минимальный % unit coverage по критичности, но нет рекомендаций по балансу между типами.

### Testing Microservices

**Contract Tests:** Проверяют, что провайдер и потребитель согласованы по формату API. В проекте контракты описаны в `shared/contracts/` (OpenAPI для REST, Protobuf для gRPC), но нет стандарта для contract testing (Pact, contract-test-as-code). Testing.md допускает расширение типов тестов.

**Component Tests:** Тестирование одного сервиса в изоляции с реальной БД, но моками внешних зависимостей. В проекте это "integration" уровень (standard-testing.md: integration = сервис + его хранилища, мок других сервисов). Покрыто корректно.

**Service Mesh Testing:** При использовании gateway (Traefik/Nginx из platform/gateway/) стоит тестировать маршрутизацию, rate limiting, CORS. В testing.md упоминается e2e через docker-compose, но нет явного паттерна для тестирования gateway.

**Рекомендация:** При появлении реальных сервисов рассмотреть добавление contract tests как отдельного типа в testing.md. Для gateway добавить smoke-тесты маршрутизации.

### Testcontainers Pattern

**Принцип:** Вместо отдельного docker-compose.test.yml использовать Testcontainers — программный запуск контейнеров прямо из тестового кода. Преимущества: тесты самодостаточны, нет внешних зависимостей на CI, каждый тест может поднять свою изолированную БД.

**Как соотносится с проектом:** Проект описывает docker-compose подход в testing.md ("docker-compose -f docker-compose.test.yml up"). Testcontainers — альтернатива, особенно для integration-тестов. Per-tech стандарт может описать конкретную библиотеку (testcontainers-python, testcontainers-java).

**Рекомендация:** При определении технологического стека принять решение: docker-compose.test.yml (общий для всех) или Testcontainers (per-test isolation). Зафиксировать решение в testing.md (секция Межсервисные тесты или секция Стратегия мокирования).

### Test Data Management

**Fixtures vs Factories vs Seed Data:**
- **Fixtures** — статические данные, хранятся в файлах. Хороши для стабильных reference data.
- **Factories** (Factory Boy, Faker) — генерируют данные программно. Каждый тест получает уникальные данные, минимальный валидный объект + override нужных полей.
- **Seed Data** — предзаполненные данные для e2e. Создаются через API (не напрямую в БД) для проверки полного цикла.

**Как соотносится с проектом:** Testing.md описывает все три подхода. 3 обязательных принципа (независимость, минимальность, изоляция) зафиксированы. Per-tech стандарт описывает конкретные библиотеки (factory_boy для Python). Plan Tests определяет fixtures на уровне acceptance-сценариев.

**Рекомендация:** Хорошо покрыто. Рассмотреть добавление в testing.md или в cross-tech стандарт правил именования fixtures (snake_case уже в Plan Tests), правил хранения seed data (tests/e2e/fixtures/ уже в структуре), правил очистки данных (rollback для integration, truncate для e2e уже в принципах).

### Coverage Thresholds и Meaningful Coverage

**Принцип:** Покрытие кода (line coverage) — необходимый, но недостаточный индикатор. Высокий % без assertion quality — бесполезен. Meaningful coverage = покрытие бизнес-логики + edge cases + error paths, а не просто "строки выполнены".

**Как соотносится с проектом:** Standard-testing.md (секция 6) задаёт минимальные пороги по критичности: critical-high >=80%, critical-medium >=60%, critical-low >=40%. Пороги определены для unit-test coverage.

**Рекомендация:** Пороги есть, но не описано КАК их измерять и КАК интегрировать в CI. Нужно:
1. В per-tech стандарте — инструмент (pytest-cov, c8, etc.) и команда.
2. В CI workflow — запуск coverage check и блокировка merge при нарушении порога.
3. Рассмотреть branch coverage вместо line coverage для более надёжных метрик.

### Testing in Docker (Isolated, Reproducible)

**Принцип:** Тесты должны запускаться в изолированном Docker-окружении для воспроизводимости. Локально и в CI — одинаковые контейнеры. docker-compose.test.yml поднимает все зависимости (БД, брокер, другие сервисы для e2e).

**Как соотносится с проектом:** Testing.md упоминает docker-compose.test.yml для межсервисных тестов. Makefile использует docker-compose.dev.yml для `make dev`. Но:
- docker-compose.test.yml не существует физически
- Нет стандарта для тестовых Docker-конфигураций
- CI (ci.yml) не поднимает Docker для тестов

**Рекомендация:** При реализации первого сервиса создать:
1. `docker-compose.test.yml` в `platform/docker/` — конфигурация для тестов
2. Обновить Makefile: `make test` и `make test-e2e` должны использовать Docker
3. Обновить CI: добавить job с Docker services для тестов
4. Стандартизировать в `standard-docker.md` (секция "Тестовые окружения")

### Platform Engineering Standards (IDP, Backstage Patterns)

**Принцип:** Internal Developer Platform (IDP) — набор инструментов и стандартов, которые упрощают жизнь разработчика. Backstage-подход: self-service, golden paths, software catalog.

**Как соотносится с проектом:**
- platform/ содержит структуру для docker/, gateway/, k8s/, monitoring/, scripts/, runbooks/
- Все подпапки пусты (.gitkeep only)
- platform/.instructions/ пуст
- Нет стандартов ни для одной подобласти

**Рекомендация для стандартов platform/:**

**Приоритет 1 — standard-docker.md** (нужен при первом сервисе):
- Формат Dockerfile (multi-stage builds, non-root user, .dockerignore)
- docker-compose конвенции (именование сервисов, сети, volumes, порты)
- Тестовые конфигурации (docker-compose.test.yml)
- Health checks в Docker
- Секреты в Docker (не в Dockerfile, через env/secrets)

**Приоритет 2 — standard-scripts.md** (нужен при первом деплое):
- Формат инфра-скриптов (bash, Python)
- Именование, структура, error handling
- Шаблоны: deploy.sh, backup.sh, rollback.sh

**Приоритет 3 — standard-monitoring.md** (нужен при настройке мониторинга):
- Формат Prometheus метрик (naming conventions, labels)
- Формат Grafana дашбордов (JSON provisioning)
- Алерты: формат, severity levels, routing
- Loki: формат логов, labels

**Низкий приоритет:** standard-k8s.md, standard-gateway.md, standard-runbooks.md — при реальном использовании.

**Мета-стандарт:** Рассмотреть `platform/.instructions/standard-platform.md` как общий фреймворк (конвенции именования, структура конфигов, связь с docs/.system/infrastructure.md). Но это дополнительный слой абстракции — может быть избыточным до появления конкретных стандартов.

### Infrastructure as Code Testing

**Принцип:** Инфраструктурный код (Dockerfile, K8s manifests, Terraform, docker-compose) тоже нуждается в тестировании:
- **Linting:** hadolint для Dockerfile, kubeval/kubeconform для K8s manifests, yamllint для YAML
- **Unit tests:** Open Policy Agent (OPA) для проверки политик K8s
- **Integration tests:** docker-compose `--wait` для проверки что сервисы поднимаются
- **Security scanning:** Trivy для образов, kube-bench для K8s security

**Как соотносится с проектом:** Проект не имеет инфраструктурного кода (всё .gitkeep). Но standard-action.md описывает CI workflow структуру, которая может включать такие проверки.

**Рекомендация:** При появлении инфраструктурного кода:
1. Добавить hadolint в pre-commit для Dockerfile
2. Добавить yamllint для docker-compose.yml и K8s manifests
3. Добавить Trivy scanning в CI для Docker images
4. Описать в standard-docker.md секцию "Валидация"

### Общие рекомендации по закрытию пробелов

| # | Пробел | Рекомендация | Приоритет |
|---|--------|-------------|-----------|
| 1 | CI не запускает тесты кода | Добавить jobs `test:` и `test-e2e:` в ci.yml (по шаблону из standard-action.md) | Высокий |
| 2 | docker-compose.test.yml не существует | Создать при реализации первого сервиса, стандартизировать в standard-docker.md | Высокий |
| 3 | `make test-load` не в CLAUDE.md | Добавить в секцию команд CLAUDE.md | Низкий |
| 4 | Pre-release тесты не в process.md | Расширить Фазу 6: load перед release, smoke после deploy | Средний |
| 5 | tests/.instructions/ пуст | Решить: нужен ли standard-tests.md или достаточно testing.md + per-tech | Средний |
| 6 | platform/.instructions/ пуст | Создать standard-docker.md при первом сервисе | Средний |
| 7 | Нет cross-tech правил для тестов | Рассмотреть секцию в testing.md или standard-tests.md: именование функций, arrange-act-assert, error message quality | Низкий |
| 8 | Coverage check не в CI | Добавить coverage threshold check в CI при реализации тестов | Средний |
| 9 | Нет contract tests | Добавить тип в testing.md при появлении нескольких сервисов | Низкий |
| 10 | Инфра-код не тестируется | Добавить hadolint + yamllint при появлении Dockerfile/K8s | Низкий |
