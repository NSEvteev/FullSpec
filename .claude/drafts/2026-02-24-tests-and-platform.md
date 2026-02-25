---
description: Аудит тестирования + CI/CD pipeline — пробелы в тестах, расширение ci.yml, pre-release pipeline
type: audit
status: ready
created: 2026-02-24
---

# Аудит тестирования и CI/CD pipeline — пробелы и план закрытия

Проверка полноты регламентации тестов по всей цепочке (планирование → стратегия → код → запуск → CI). Расширение CI pipeline: concurrency, dependency review, pre-release validation.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** Проверить, нет ли пробелов в регламентации работы с тестами
**Почему создан:** Тестирование покрыто на уровне планирования (Plan Tests) и стратегии (testing.md), но `tests/.instructions/` пуст — нет стандартов для самого кода тестов. CI не запускает тесты кода. Standard-process.md не упоминает integration/e2e/load/smoke.
**Связанные файлы:**
- `specs/.instructions/analysis/plan-test/standard-plan-test.md` — планирование тестов (TC-N)
- `specs/.instructions/docs/testing/standard-testing.md` — стратегия тестирования (testing.md)
- `.github/.instructions/development/standard-development.md` — когда запускать тесты
- `tests/.instructions/README.md` — **пуст**, нет стандартов
- `.github/workflows/ci.yml` — **не запускает тесты кода** (только pre-commit хуки)
- `Makefile` — `make test`, `make test-e2e`, `make test-load` (заглушки)

**Docker-часть:** Стандарты platform/ (standard-docker.md, docker-compose) вынесены в отдельный черновик [docker-dev.md](./2026-02-24-docker-dev.md).

**Поглощённый черновик:** [cicd-enhancements.md](./2026-02-24-cicd-enhancements.md) — 3 уникальных пункта (concurrency, dependency-review, pre-release.yml) перенесены сюда как пробелы 9-11. Остальные 5 из 8 пунктов cicd-enhancements были дублями: 2 с этим черновиком (ci.yml jobs, standard-process.md), 2 с другими черновиками (deploy.yml → deploy-workflow, codeql.yml → security-scan), 1 преждевременный (reusable workflows — нет сервисов). Оригинал удалён.

## Содержание

### Карта покрытия (AS IS)

| Аспект | Где описан | Полнота |
|--------|-----------|---------|
| ЧТО тестировать (acceptance criteria) | Plan Tests (TC-N) | Полная |
| ГДЕ размещать тесты | testing.md + CLAUDE.md + tests/README.md | Полная |
| КАК мокировать | testing.md (Стратегия мокирования) | Полная |
| КАК писать тесты per-tech | standard-{tech}.md (секция Тестирование) | Полная (при наличии per-tech) |
| КОГДА запускать | standard-development.md + validation-development.md | Полная |
| КАКИЕ команды | Makefile (test, test-e2e, test-load) | Частичная (test-load не в CLAUDE.md) |
| Coverage requirements | standard-testing.md (секция 6, по критичности) | Полная |
| Тестовые данные | testing.md + Plan Tests (fixtures) | Полная |
| Code review тестов | validation-review.md (критерий 5, код E004) | Полная |
| Валидация Plan Tests | validate-analysis-plan-test.py + pre-commit | Полная |
| Валидация testing.md | validate-docs-testing.py + pre-commit | Полная |

### Выявленные пробелы

| # | Пробел | Серьёзность | Решение |
|---|--------|-------------|---------|
| 1 | **CI не запускает тесты кода** | Высокая | Добавить jobs `test:` и `test-e2e:` в ci.yml |
| 2 | **standard-process.md не упоминает e2e/integration** | Средняя | Расширить Фазу 3 шаг 3.2: `make test` + `make test-e2e` |
| 3 | **Pre-release тесты не в process.md** | Средняя | Расширить Фазу 6: load перед release |
| 4 | **`make test-load` не в CLAUDE.md** | Низкая | Добавить в секцию команд |
| 5 | **tests/.instructions/ пуст** | Низкая | Не нужен отдельный стандарт (см. Решения) |
| 6 | **Coverage check не в CI** | Средняя | Добавить в CI при реализации тестов |
| 7 | **Именование тестовых функций** не стандартизировано | Низкая | Покрыть в per-tech стандартах |
| 8 | **Нет per-service make таргетов** | Средняя | Добавить `make test-{svc}`, `make lint-{svc}` для параллельной работы dev-агентов |
| 9 | **Нет concurrency в ci.yml** *(из cicd-enhancements)* | Средняя | Добавить `concurrency` group с `cancel-in-progress: true` |
| 10 | **Нет dependency review в ci.yml** *(из cicd-enhancements)* | Средняя | Добавить `actions/dependency-review-action@v4` для PR |
| 11 | **Нет pre-release pipeline** *(из cicd-enhancements)* | Средняя | Создать `pre-release.yml` с `workflow_dispatch` |

### Пробел 1: CI не запускает тесты кода

**Текущее состояние:** `.github/workflows/ci.yml` запускает **только** pre-commit хуки. Не запускает `make test`, `make test-e2e`, `make lint`, `make build`.

**Решение:** Добавить jobs в ci.yml по шаблону из `standard-action.md`:
- `test:` — `make test` (unit + integration)
- `test-e2e:` — `make test-e2e` (e2e, зависит от docker-compose.test.yml из [docker-dev](./2026-02-24-docker-dev.md))
- `lint:` — `make lint`

**Зависимость:** docker-compose.test.yml из docker-dev нужен для `test-e2e` job.

### Пробел 2-3: standard-process.md — тесты в Фазах 3 и 6

**Шаг 3.2** сейчас: "`make test`, `make lint`". Нужно: "`make test` (unit + integration) + `make test-e2e` (при изменениях API/DB/inter-service)".

**Фаза 6** сейчас: только `gh release create`. Нужно: pre-release проверка с `make test-load` (если критичность high/medium).

**§ 8 (таблица):** Добавить `standard-testing.md` в строки 3.1-3.2.

### Пробел 8: Per-service make таргеты

При параллельной работе dev-агентов (из [conflict-detect draft](./2026-02-24-conflict-detect.md)) каждый агент тестирует только свой сервис. Нужны:
- `make test-{svc}` — unit + integration одного сервиса
- `make lint-{svc}` — линтинг одного сервиса

Системные тесты (`make test-e2e`) запускаются main LLM после завершения волны.

### Пробел 9: Concurrency в ci.yml (из cicd-enhancements)

**Проблема:** Без concurrency при быстрых пушах в feature-ветку запускаются множественные параллельные CI runs, из которых актуален только последний. Впустую тратятся CI-минуты.

**Решение:** Добавить concurrency group с `cancel-in-progress: true` (по `standard-action.md` § 17):

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Примечание:** Для `deploy.yml` — `cancel-in-progress: false` (не отменять деплой посередине). Concurrency применяется только к CI.

### Пробел 10: Dependency Review в ci.yml (из cicd-enhancements)

**Проблема:** PR с уязвимыми зависимостями не блокируется. Dependabot создаёт PR для обновления существующих зависимостей, но **не блокирует** PR, которые добавляют новые уязвимые зависимости.

**Решение:** Добавить `actions/dependency-review-action@v4` в ci.yml:

```yaml
  dependency-review:
    name: Dependency Review
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    timeout-minutes: 5
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v6
      - uses: actions/dependency-review-action@v4
```

**Что проверяет:** Сравнивает зависимости в PR с base branch. Если добавлены зависимости с known vulnerabilities (CVE) — блокирует PR.

**Условие запуска:** Только для `pull_request` (не для push в main). На push зависимости уже прошли review.

### Пробел 11: Pre-release pipeline (из cicd-enhancements)

**Проблема:** `validate-pre-release.py` запускается только локально. Нет CI-воркфлоу для полного pre-release тестирования перед Release.

**Решение:** Создать `pre-release.yml` с триггером `workflow_dispatch`:

```yaml
name: Pre-release Validation

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to validate (e.g., v1.0.0)'
        required: true
        type: string

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - uses: actions/cache@v5
        with:
          path: ~/.cache/pre-commit
          key: pre-commit-${{ hashFiles('.pre-commit-config.yaml') }}
      - name: Pre-commit checks
        run: |
          pip install pre-commit
          pre-commit run --all-files
      - name: Unit & Integration tests
        run: make test
      - name: Lint
        run: make lint
      - name: E2E tests
        run: make test-e2e
      - name: Pre-release validation script
        run: python .github/.instructions/.scripts/validate-pre-release.py --version ${{ inputs.version }} --skip-tests
```

**Почему `workflow_dispatch`, а не `on: push: tags:`:** `standard-release.md` § 8: "Release — это решение, не событие". Pre-release проверка запускается человеком **перед** созданием тега, а не после. Тег создаётся только после успешной валидации.

**Зависимость:** `make test` и `make test-e2e` — заглушки (exit 0). Pipeline заработает по-настоящему при появлении реальных тестов. Но он будет уже настроен.

### Связь с другими черновиками (из cicd-enhancements)

| Компонент из cicd-enhancements | Покрыт в |
|-------------------------------|---------|
| CodeQL workflow (codeql.yml) | [security-scan.md](./2026-02-25-security-scan.md) — создание codeql.yml |
| Deploy workflow (deploy.yml) | [deploy-workflow.md](./2026-02-25-deploy-workflow.md) — standard-deploy.md + deploy.yml |
| Reusable workflows | Отложено — нет сервисов в `/src/`. Добавить при 2+ сервисах |
| Docker в CI | [docker-dev.md](./2026-02-24-docker-dev.md) — docker-compose.test.yml |

### Паттерн расширенного ci.yml

Итоговый вид ci.yml после применения **всех** пробелов (1, 9, 10):

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  pre-commit:
    name: Pre-commit checks
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - uses: actions/cache@v5
        with:
          path: ~/.cache/pre-commit
          key: pre-commit-${{ hashFiles('.pre-commit-config.yaml') }}
      - run: |
          pip install pre-commit
          pre-commit run --all-files

  test:
    name: Unit & Integration tests
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: make test

  lint:
    name: Lint
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: make lint

  dependency-review:
    name: Dependency Review
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    timeout-minutes: 5
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v6
      - uses: actions/dependency-review-action@v4
```

**Примечания:**
- `make test` и `make lint` — заглушки (exit 0). CI настраивается сейчас, заглушки заменяются при разработке сервисов.
- `concurrency` с `cancel-in-progress: true` — экономит CI-минуты при быстрых пушах (по `standard-action.md` § 17).
- `dependency-review` — только для PR (`if: github.event_name == 'pull_request'`).
- `test-e2e` job добавляется позже (задача 4, зависит от docker-compose.test.yml из docker-dev).

### Порядок выполнения

| # | Действие | Инструмент | Зависимости |
|---|---------|------------|-------------|
| 1 | Обновить standard-process.md | Edit | — |
| 2 | Обновить CLAUDE.md (make test-load) | Edit | — |
| 3 | Добавить per-service таргеты в Makefile | Edit | — |
| 4 | Обновить ci.yml (test + lint + e2e jobs) | Edit | ← docker-dev (docker-compose.test.yml) |
| 5 | Добавить coverage check в CI | Edit | ← 4 |
| 6 | Добавить concurrency в ci.yml | Edit | — |
| 7 | Добавить dependency-review в ci.yml | Edit | — |
| 8 | Создать pre-release.yml | Write | ← docker-dev |

## Решения

- **`tests/.instructions/standard-tests.md` не создаём** — per-tech стандарты (секция Тестирование) + testing.md (стратегия) + standard-development.md (процесс) достаточно покрывают. Отдельный стандарт для кода тестов создал бы дублирование
- **Cross-tech правила тестов** (именование функций, arrange-act-assert) — покрыть в per-tech стандартах, не в отдельном документе
- **CI обновляется после docker-dev** — тестовые jobs зависят от docker-compose.test.yml
- **Per-service make таргеты** нужны для параллельной работы dev-агентов
- **Contract tests** — добавить как тип в testing.md при появлении нескольких реальных сервисов, сейчас преждевременно
- **Platform/ стандарты** — вынесены в [docker-dev](./2026-02-24-docker-dev.md)
- **cicd-enhancements поглощён** — 3 уникальных пункта (concurrency, dependency-review, pre-release.yml) перенесены как пробелы 9-11. Остальные 5 пунктов — дубли (этот черновик × 2, deploy-workflow × 1, security-scan × 1, преждевременный × 1)
- **Reusable workflows отложены** — нет сервисов в `/src/`. Создать `.github/workflows/reusable-test.yml` при появлении 2+ сервисов
- **CodeQL → security-scan** — codeql.yml создаётся в рамках security-scan черновика, не здесь
- **Concurrency и dependency-review** не зависят от docker-dev — можно добавить в ci.yml прямо сейчас (задачи 6, 7)
- **Pre-release.yml использует `workflow_dispatch`** — Release = решение человека, не автоматический trigger по тегу. Запуск перед созданием тега

## Открытые вопросы

*Нет открытых вопросов.*

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Обновить standard-process.md — тесты в Фазах 3 и 6
  description: >
    Драфт: .claude/drafts/2026-02-24-tests-and-platform.md (секция "Пробел 2-3")
    Шаг 3.2: расширить "make test, make lint" → добавить make test-e2e
    при изменениях API/DB/inter-service (ссылка на standard-development.md §4).
    Фаза 6: добавить pre-release make test-load для critical-high/medium.
    §8 таблица: добавить standard-testing.md в строки 3.1-3.2.
  activeForm: Обновляю standard-process.md (тесты)

TASK 2: Обновить CLAUDE.md — make test-load
  description: >
    Драфт: .claude/drafts/2026-02-24-tests-and-platform.md (пробел 4)
    Добавить make test-load в секцию команд CLAUDE.md
    (рядом с make test и make test-e2e).
  activeForm: Обновляю CLAUDE.md

TASK 3: Добавить per-service make таргеты
  description: >
    Драфт: .claude/drafts/2026-02-24-tests-and-platform.md (пробел 8)
    Добавить в Makefile шаблон per-service таргетов:
    make test-{svc} (unit + integration одного сервиса),
    make lint-{svc} (линтинг одного сервиса).
    Обновить standard-development.md если нужно.
  activeForm: Добавляю per-service make таргеты

TASK 4: Обновить ci.yml — jobs для тестов
  blockedBy: [docker-dev]
  description: >
    Драфт: .claude/drafts/2026-02-24-tests-and-platform.md (пробел 1)
    Добавить в .github/workflows/ci.yml:
    - job test: make test (unit + integration)
    - job test-e2e: make test-e2e (docker-compose.test.yml)
    - job lint: make lint
    По шаблону из standard-action.md.
    ЗАВИСИМОСТЬ: docker-compose.test.yml из docker-dev должен существовать.
  activeForm: Обновляю CI pipeline

TASK 5: Добавить coverage check в CI
  blockedBy: [4]
  description: >
    Драфт: .claude/drafts/2026-02-24-tests-and-platform.md (пробел 6)
    Добавить coverage threshold check в CI job test:.
    Пороги из standard-testing.md секция 6 (по критичности сервиса).
    Инструмент: pytest-cov / c8 (зависит от tech stack).
  activeForm: Добавляю coverage check

TASK 6: Добавить concurrency в ci.yml
  description: >
    Драфт: .claude/drafts/2026-02-24-tests-and-platform.md (пробел 9, из cicd-enhancements)
    Добавить concurrency group в ci.yml на уровне workflow:
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
      cancel-in-progress: true
    По standard-action.md § 17. Экономит CI-минуты при быстрых пушах.
    НЕ применять cancel-in-progress для deploy.yml (deploy не отменяется).
  activeForm: Добавляю concurrency в CI

TASK 7: Добавить dependency-review в ci.yml
  description: >
    Драфт: .claude/drafts/2026-02-24-tests-and-platform.md (пробел 10, из cicd-enhancements)
    Добавить job dependency-review в ci.yml:
    actions/dependency-review-action@v4
    Условие: if: github.event_name == 'pull_request' (только PR, не push).
    permissions: contents: read, pull-requests: write.
    Блокирует PR с уязвимыми зависимостями (CVE).
    Timeout: 5 минут.
  activeForm: Добавляю dependency-review в CI

TASK 8: Создать pre-release.yml
  blockedBy: [docker-dev]
  description: >
    Драфт: .claude/drafts/2026-02-24-tests-and-platform.md (пробел 11, из cicd-enhancements)
    Создать .github/workflows/pre-release.yml с workflow_dispatch.
    Input: version (string, required).
    Steps: pre-commit run --all-files, make test, make lint, make test-e2e,
    validate-pre-release.py --version ${{ inputs.version }} --skip-tests.
    Timeout: 30 минут.
    По шаблону из standard-action.md.
    Обновить .github/workflows/README.md — зарегистрировать pre-release.yml.
    ЗАВИСИМОСТЬ: docker-compose.test.yml из docker-dev нужен для make test-e2e.
  activeForm: Создаю pre-release pipeline
```
