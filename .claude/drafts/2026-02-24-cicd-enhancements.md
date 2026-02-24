# CI/CD — аудит и расширение pipeline

Оценка текущего CI/CD покрытия и план расширения: pre-release тесты с полным покрытием, линтинг, security checks.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** Проверить покрытие CI/CD и определить, что ещё нужно для полноценной автоматизации
**Почему создан:** `ci.yml` существует, но запускает только pre-commit хуки. Нет запуска тестов, нет pre-release проверок
**Связанные файлы:**
- `.github/.instructions/actions/standard-action.md` — стандарт GitHub Actions (полный, 19 секций)
- `.github/.instructions/actions/validation-action.md` — валидация workflows
- `.github/.instructions/actions/security/` — стандарты безопасности (secrets, security)
- `.github/workflows/ci.yml` — текущий CI (только pre-commit)
- `specs/.instructions/standard-process.md` — нужна интеграция CI/CD в процесс

## Содержание

### Текущее состояние

`ci.yml` запускает:
- Pre-commit hooks на push в main и PR в main
- Python 3.12, кэш pre-commit
- Permissions: read-only

**Что НЕ делает:**
- Не запускает `make test` (unit-тесты)
- Не запускает `make test-e2e` (e2e-тесты)
- Не запускает `make lint` (линтинг кода)
- Не проверяет security (dependency scanning, secret leaks)
- Нет pre-release pipeline (full coverage перед тегом)

### Какие workflows нужны

| Workflow | Триггер | Что делает | Приоритет |
|----------|---------|-----------|-----------|
| `ci.yml` (обновить) | push, PR | Pre-commit + `make test` + `make lint` | Высокий |
| `test-integration.yml` | PR to main | Интеграционные тесты в Docker | Высокий |
| `test-e2e.yml` | PR to main | E2E тесты в Docker | Средний |
| `pre-release.yml` | tag v*.*.* | Полное покрытие: unit + integration + e2e + load | Высокий |
| `security.yml` | schedule (weekly) + PR | Dependency audit, secret scanning | Средний |

### Связь со standard-action.md

`standard-action.md` уже содержит:
- Структуру YAML файла
- Best practices (timeout, permissions, caching)
- Reusable workflows
- Security (secrets, variables)
- Environments (staging, production)

Дополнительных стандартов для Actions создавать не нужно — `standard-action.md` покрывает. Нужно только **создать сами workflow файлы** по этому стандарту.

### Интеграция в standard-process.md

| Фаза | Где CI/CD | Что добавить |
|------|-----------|-------------|
| Фаза 3 (шаг 3.2) | Локальная валидация | Ссылка: CI повторяет те же проверки на GitHub |
| Фаза 4 (шаг 4.2) | PR Create | CI checks обязательны перед merge |
| Фаза 6 (шаг 6.1) | Release | Pre-release pipeline: полное покрытие тестами |
| §8 Сводная таблица | — | Добавить `standard-action.md` в строку 4.2 и 6.1 |

## Решения

- `standard-action.md` уже покрывает стандарт — новых стандартов не нужно
- Нужно расширить `ci.yml` и создать дополнительные workflow файлы
- Pre-release pipeline — обязательный блокер перед тегом
- Нужна интеграция в standard-process.md (Фаза 4 и 6)

## Открытые вопросы

- Docker в CI: нужен ли docker-compose для интеграционных тестов в GitHub Actions, или достаточно service containers?
- Pre-release pipeline: блокировать release при падении тестов или предупреждать?
- Load тесты в CI: запускать при каждом PR (дорого) или только pre-release?
- Нужны ли environment-specific tests (staging deploy + smoke)?

---

## Что уже описано в проекте

### 1. Текущий CI workflow

**Файл:** `.github/workflows/ci.yml` (53 строки)
- Единственный workflow в проекте. Других `.yml` файлов в `.github/workflows/` нет.
- Триггеры: `push` на `main`, `pull_request` на `main`.
- Единственный job `pre-commit`: checkout, setup-python 3.12, cache pre-commit, `pre-commit run --all-files`.
- `permissions: contents: read` — минимальные права (соответствует стандарту).
- `timeout-minutes: 10` — указан (соответствует стандарту).
- Использует `actions/checkout@v6`, `actions/setup-python@v6`, `actions/cache@v5` — версии стабильные.
- **Не вызывает:** `make test`, `make lint`, `make test-e2e`, `make build`. Не запускает security-проверки.

### 2. Makefile — доступные make-команды

**Файл:** `Makefile` (85 строк)
- `make test` — строка 21: `@echo "TODO: настроить запуск тестов"` (заглушка).
- `make test-e2e` — строка 24: `@echo "TODO: настроить e2e тесты"` (заглушка).
- `make test-load` — строка 27: `@echo "TODO: настроить нагрузочные тесты (k6)"` (заглушка).
- `make lint` — строка 32: `@echo "TODO: настроить линтеры"` (заглушка).
- `make build` — строка 17: `docker-compose build`.
- `make dev` — строка 9: `docker-compose -f docker-compose.dev.yml up`.
- **Вывод:** CI не может запускать `make test` / `make lint` / `make test-e2e` — они все ещё заглушки. Перед расширением CI нужно реализовать сами команды.

### 3. Pre-commit хуки (25 хуков)

**Файл:** `.pre-commit-config.yaml` (252 строки)
- 25 хуков проверяют: структуру, rules, scripts, skills, PR template, CODEOWNERS, type-templates, actions, security, branch name, github-required, docs, services, technologies, analysis documents, review.
- CI запускает `pre-commit run --all-files` — все 25 хуков выполняются.
- Документация: `.structure/pre-commit.md` — полный список хуков и их назначение.
- Хук `actions-validate` (строка 82-89) — вызывает `validate-action.py` для валидации workflow файлов (правила A001-A007).
- Хук `security-validate` (строка 91-99) — вызывает `validate-security.py` для `dependabot.yml`, `SECURITY.md`, `codeql.yml`.

### 4. Стандарт Actions

**Файл:** `.github/.instructions/actions/standard-action.md` (1417 строк, 19 секций)
- Секция 2 (строка 130): именование файлов — рекомендованные имена: `ci.yml`, `deploy.yml`, `test-{service}.yml`, `release.yml`, `scheduled-{task}.yml`.
- Секция 4 (строка 239): триггеры — push, PR, release, schedule, workflow_dispatch, workflow_run.
- Секция 7 (строка 673): secrets и variables — использование через `${{ secrets.NAME }}` и `${{ vars.NAME }}`.
- Секция 8 (строка 741): reusable workflows — `workflow_call` для переиспользования (тесты в нескольких workflows).
- Секция 9 (строка 806): матричные стратегии — тестирование на нескольких OS/версиях.
- Секция 11 (строка 907): артефакты и кэширование — `actions/cache@v4`, `actions/upload-artifact@v4`.
- Секция 12 (строка 986): best practices — разделение CI/CD (строка 1086), timeout (строка 1065), минимальные права (строка 1024), версионирование actions (строка 996).
- Секция 15 (строка 1193): composite actions — переиспользуемые steps (`setup-node-with-cache`).
- Секция 16 (строка 1247): environments — staging, production с protection rules.
- Секция 17 (строка 1284): concurrency — `cancel-in-progress: true` для CI, `false` для deploy.
- Секция 19 (строка 1377): локальное тестирование — `act` для локального запуска workflows.

### 5. Валидация Actions

**Файл:** `.github/.instructions/actions/validation-action.md` (128 строк)
- Скрипт: `.github/.instructions/.scripts/validate-action.py` — проверяет правила A001-A007.
- Правила: A001 (name), A002 (permissions), A003 (timeout-minutes), A004 (версии actions), A005 (secrets в env), A006 (runs-on), A007 (расположение).
- Ручные проверки при review: триггеры, разделение CI/CD, concurrency, environment.

### 6. Безопасность

**Файл:** `.github/.instructions/actions/security/standard-security.md` (496 строк)
- Секция 3 (строка 81): Dependabot — alerts, security updates, version updates. Конфигурация в `.github/dependabot.yml`.
- Секция 4 (строка 223): CodeQL — Advanced Setup через `codeql.yml` workflow. Матрица языков `["python", "javascript-typescript"]`. Триггеры: push/PR в main + еженедельный cron.
- Секция 5 (строка 300): Secret Scanning + Push Protection.
- Секция 6 (строка 350): SECURITY.md — политика безопасности.
- **Важно:** Файл `codeql.yml` описан в стандарте (полный шаблон в секции 4, строки 237-283), но НЕ существует в `.github/workflows/`. Нужно создать.

**Файл:** `.github/.instructions/actions/security/standard-secrets.md` (379 строк)
- Секция 2: именование `{КАТЕГОРИЯ}_{СЕРВИС}_{НАЗНАЧЕНИЕ}` (UPPER_SNAKE_CASE).
- Секция 3: 3 уровня — Repository, Environment, Organization.
- Секция 4: категории — DB_, API_, DEPLOY_, REGISTRY_, NOTIFY_, SIGN_, AUTH_.
- Секция 5: ротация — 90/180/365 дней. Скрипт `rotate-secret.py`. Scheduled workflow для напоминаний.

### 7. Существующие файлы безопасности

**Файл:** `.github/dependabot.yml` (66 строк)
- 5 ecosystems настроены: pip (auth, api), npm (frontend), docker (platform), github-actions.
- Все с weekly interval, группировкой minor/patch, labels "dependencies".

**Файл:** `.github/SECURITY.md` — существует (создан по стандарту).

**Отсутствует:** `.github/workflows/codeql.yml` — описан в standard-security.md секция 4 (полный шаблон), но файл не создан.

**Отсутствует:** `.github/release.yml` — кастомизация changelog categories (описан в standard-release.md секция 5, строки 306-324). Опционален.

### 8. Процесс релиза

**Файл:** `.github/.instructions/releases/standard-release.md` (1117 строк, 20 секций)
- Секция 9 (строка 542): подготовка релиза — 5 обязательных проверок (main sync, no critical PR, `make test`, milestone closed, clean working tree).
- Секция 11 (строка 639): публикация на production — триггер `on: release: types: [published]`, workflow `deploy.yml`.
- **Deploy workflow:** Описан как будущий `deploy.yml` (строка 645-649), но файл не существует.

**Файл:** `.github/.instructions/releases/create-release.md` (396 строк, 7 шагов)
- Шаг 3 (строка 110): pre-release валидация — скрипт `validate-pre-release.py`.
- Шаг 7 (строка 284): post-release валидация — скрипт `validate-post-release.py`.

**Файл:** `.github/.instructions/releases/validation-release.md` (325 строк)
- Шаг 1: pre-release проверки main (5 последовательных).
- Шаг 6: проверка deploy workflow (`gh run list --workflow=deploy.yml`).
- Скрипты: `validate-pre-release.py` (существует, 236 строк), `validate-post-release.py` (существует).

### 9. Процесс поставки ценности

**Файл:** `specs/.instructions/standard-process.md` (530 строк)
- Фаза 3, шаг 3.2 (строка 246): локальная валидация — `make test`, `make lint`, 25 pre-commit хуков.
- Фаза 4, шаг 4.2 (строка 255): PR Create — упомянут, но CI checks как обязательные перед merge явно не прописаны.
- Фаза 6, шаг 6.1 (строка 275): Release — ссылка на `standard-release.md` и `create-release.md`. Pre-release pipeline не упомянут отдельно.
- Секция 8, таблица 8.1 (строка 402): сводная таблица инструментов — в строке 6.1 Release указан `standard-release.md`, но `standard-action.md` не упомянут.
- Секция 8, таблица 8.2 (строка 432): pre-commit хуки по шагам — actions-validate на шаге 3.2/3.3.
- Секция 10, пробел G8 (строка 518): "Нет post-release workflow" — мониторинг зависит от инфраструктуры.

### 10. Docker-инфраструктура

- `docker-compose.dev.yml` — **не существует** (Makefile ссылается на него, строка 9).
- `docker-compose.yml` — **не существует**.
- Нет Dockerfile'ов в корне проекта (шаблон ещё не заполнен конкретными сервисами).

---

## Best practices

### 1. Расширение ci.yml: порядок действий

**Проблема:** `make test`, `make lint`, `make test-e2e` — заглушки (TODO). CI не может вызывать то, что не реализовано.

**Рекомендация:** Двухфазный подход:
1. **Фаза A (сейчас):** Добавить в `ci.yml` вызов `make test` и `make lint` как отдельные jobs. Они пройдут (echo "TODO" возвращает exit code 0). Когда сервисы появятся — CI уже будет настроен.
2. **Фаза B (при появлении сервисов):** Заменить заглушки в Makefile реальными командами. CI автоматически начнёт проверять.

**Конкретный паттерн для ci.yml (по standard-action.md, секция 12.7):**

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
    name: Unit tests
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
```

**Добавлено по стандарту:** `concurrency` с `cancel-in-progress: true` (standard-action.md, секция 17, строка 1316-1322) — экономит CI-минуты при быстрых пушах.

### 2. CodeQL workflow: создать немедленно

**Файл `codeql.yml` описан в standard-security.md (строки 237-283) с полным шаблоном.** Это единственный security workflow, который нужно создать как файл. Dependabot и Secret Scanning настраиваются через Settings.

**Шаблон готов к использованию:** копировать из standard-security.md секция 4 → `.github/workflows/codeql.yml`. Матрица: `["python", "javascript-typescript"]`. Триггеры: push/PR в main + cron `0 6 * * 1`.

### 3. Pre-release pipeline: архитектура

**Рекомендация для `pre-release.yml`:**

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
      - run: python .github/.instructions/.scripts/validate-pre-release.py --version ${{ inputs.version }} --skip-tests
      - run: make test
      - run: make lint
      - run: make test-e2e
```

**Триггер `workflow_dispatch`** вместо `on: push: tags:` — потому что стандарт Release (standard-release.md, секция 8, строка 82-83) утверждает "Release — это решение, не событие" и "Release создаётся явно (человеком)". Pre-release проверка запускается человеком ПЕРЕД созданием тега, а не после.

**Альтернатива:** Скрипт `validate-pre-release.py` уже включает проверку `make test` (строка 121-129 скрипта). Можно запускать его локально и в CI.

### 4. Security scanning: что уже настроено и что нет

| Инструмент | Статус | Что нужно |
|-----------|--------|-----------|
| Dependabot Alerts | Настройка через Settings (не файл) | Включить в Settings при первом использовании |
| Dependabot Version Updates | `.github/dependabot.yml` существует (66 строк, 5 ecosystems) | Готово |
| CodeQL (SAST) | Шаблон описан в standard-security.md, файл НЕ создан | Создать `.github/workflows/codeql.yml` |
| Secret Scanning | Настройка через Settings | Включить в Settings |
| Push Protection | Настройка через Settings | Включить в Settings |
| `detect-secrets` (pre-commit) | НЕ настроен | Рассмотреть для private repos без GHAS |
| Dependency review (PR) | НЕ настроен | GitHub Action `actions/dependency-review-action@v4` — блокирует PR с уязвимыми зависимостями |

**Рекомендация:** Добавить `actions/dependency-review-action@v4` в ci.yml для PR:

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

### 5. Docker в CI: service containers vs docker-compose

**Для микросервисного проекта с интеграционными тестами:**

- **Service containers** (GitHub Actions native) — подходят для единичных зависимостей (PostgreSQL, Redis). Описываются в `services:` блоке job. Просты в настройке, автоматически управляются runner'ом.
- **docker-compose** — необходим когда тесты требуют запуска нескольких связанных сервисов проекта (backend + database + cache). Работает в GitHub Actions: `docker-compose -f docker-compose.test.yml up -d`.

**Рекомендация:** Начать с service containers для unit/integration тестов одного сервиса. Переходить на docker-compose только при появлении cross-service integration тестов.

```yaml
  test-integration:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v6
      - run: make test
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
```

### 6. Reusable workflows для микросервисов

**Проблема:** При N сервисах, каждый с тестами — дублирование workflow кода.

**Решение (standard-action.md, секция 8, строка 741):** Создать reusable workflow `.github/workflows/reusable-test.yml`:

```yaml
name: Reusable Service Test
on:
  workflow_call:
    inputs:
      service:
        required: true
        type: string
      python-version:
        required: false
        type: string
        default: "3.12"
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    defaults:
      run:
        working-directory: src/${{ inputs.service }}
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ inputs.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

Вызов из ci.yml:

```yaml
jobs:
  test-auth:
    uses: ./.github/workflows/reusable-test.yml
    with:
      service: auth
  test-api:
    uses: ./.github/workflows/reusable-test.yml
    with:
      service: api
```

### 7. Кэширование в CI: стратегия

**По standard-action.md, секция 11 (строка 941):**

| Что кэшировать | Ключ | Путь |
|----------------|------|------|
| Pre-commit environments | `pre-commit-${{ hashFiles('.pre-commit-config.yaml') }}` | `~/.cache/pre-commit` |
| pip зависимости | `pip-${{ runner.os }}-${{ hashFiles('**/requirements*.txt') }}` | `~/.cache/pip` |
| npm зависимости | `node-${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}` | `node_modules` |
| Docker layers | `docker-${{ runner.os }}-${{ hashFiles('**/Dockerfile') }}` | `/tmp/.buildx-cache` |

**Docker layer caching** (для build job):

```yaml
  - uses: docker/setup-buildx-action@v3
  - uses: docker/build-push-action@v5
    with:
      context: .
      push: false
      cache-from: type=gha
      cache-to: type=gha,mode=max
```

GitHub Actions native cache (`type=gha`) хранит Docker layers в GitHub Cache API (10 GB лимит на репозиторий).

### 8. Test parallelization

**Матричная стратегия (standard-action.md, секция 9, строка 806)** для параллельного запуска тестов:

```yaml
strategy:
  fail-fast: false
  matrix:
    service: [auth, api, frontend]
```

`fail-fast: false` — все сервисы тестируются независимо, полный отчёт.

**Для большого количества тестов внутри одного сервиса:** pytest-split или pytest-xdist для параллелизации внутри одного runner'а. В CI:

```yaml
- run: pip install pytest-xdist
- run: pytest tests/ -n auto  # auto определяет количество CPU
```

### 9. Load тесты: только pre-release

**Ответ на открытый вопрос:** Load тесты (k6, Locust) — только в pre-release pipeline и по `workflow_dispatch`. Причины:
- Стоимость: load тесты занимают 10-30 минут CI, требуют инфраструктуру.
- Частота: при каждом PR — слишком дорого. При release — обязательно.
- Makefile уже определяет `make test-load` (строка 27) — будущая команда для k6.

### 10. Deploy workflow: блокирующая рекомендация

**standard-release.md, секция 11 (строка 639)** описывает deploy.yml с триггером `on: release: types: [published]`. Workflow:

1. Checkout по тегу.
2. Build Docker images.
3. Push в Registry.
4. Deploy на production.
5. Health check + smoke tests.

**Рекомендация:** Создавать `deploy.yml` только при наличии конкретной инфраструктуры (Kubernetes, Docker Swarm, SSH-сервер). Сейчас проект — шаблон, инфраструктуры нет.

### 11. Concurrency: обязательно для CI

**standard-action.md, секция 17 (строка 1284):**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Для CI — экономия минут
```

Без concurrency: при 3 быстрых пушах в feature-ветку запускаются 3 параллельных CI — 2 из них бесполезны. С `cancel-in-progress: true` — только последний.

### 12. Интеграция CI в standard-process.md

**Конкретные изменения в `specs/.instructions/standard-process.md`:**

1. **Фаза 4, шаг 4.2 (строка 255):** Добавить столбец "SSOT" → `standard-action.md`. Добавить описание: "CI checks (pre-commit + test + lint) обязательны для merge".
2. **Фаза 6, шаг 6.1 (строка 275):** Добавить: "Pre-release валидация: `validate-pre-release.py` или `pre-release.yml` workflow".
3. **Таблица 8.1 (строка 402):** В строку 4.2 PR Create добавить `standard-action.md` в столбец "Инструкция". В строку 6.1 Release — `create-release.md` уже есть, добавить `pre-release.yml` в столбец "Script".

### 13. Минимальный action plan (приоритизированный)

| # | Действие | Зависимость | Файл | Блокер |
|---|----------|-------------|------|--------|
| 1 | Расширить ci.yml: добавить jobs test и lint | Нет | `.github/workflows/ci.yml` | Нет (заглушки пройдут) |
| 2 | Добавить concurrency в ci.yml | Нет | `.github/workflows/ci.yml` | Нет |
| 3 | Создать codeql.yml из шаблона standard-security.md | Нет | `.github/workflows/codeql.yml` | Нет |
| 4 | Добавить dependency-review в ci.yml | Нет | `.github/workflows/ci.yml` | Нет |
| 5 | Создать pre-release.yml (workflow_dispatch) | `make test` не заглушка | `.github/workflows/pre-release.yml` | Реализация тестов |
| 6 | Создать reusable-test.yml | Наличие сервисов в /src/ | `.github/workflows/reusable-test.yml` | Структура сервисов |
| 7 | Обновить standard-process.md (фазы 4, 6, таблица 8) | Нет | `specs/.instructions/standard-process.md` | Нет |
| 8 | Создать deploy.yml | Инфраструктура (Docker Registry, сервер) | `.github/workflows/deploy.yml` | Наличие инфраструктуры |

**Шаги 1-4 и 7 можно выполнить прямо сейчас** — не зависят от наличия сервисов или инфраструктуры.
