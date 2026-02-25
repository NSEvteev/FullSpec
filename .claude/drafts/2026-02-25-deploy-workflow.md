# Deploy Workflow — стандарт деплоя + шаблон deploy.yml

Стандарт `standard-deploy.md` (triggers, environments, secrets, rollback, health checks) + шаблон `deploy.yml` с dynamic service discovery. Dockerfile создаётся dev-агентом при разработке сервиса — deploy.yml подхватывает автоматически.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [§ 1. AS IS — что уже есть](#-1-as-is--что-уже-есть)
  - [§ 2. Архитектура: кто что создаёт](#-2-архитектура-кто-что-создаёт)
  - [§ 3. standard-deploy.md](#-3-standard-deploymd)
  - [§ 4. Шаблон deploy.yml](#-4-шаблон-deployyml)
  - [§ 5. Dynamic service discovery](#-5-dynamic-service-discovery)
  - [§ 6. Environments: staging и production](#-6-environments-staging-и-production)
  - [§ 7. Secrets и переменные](#-7-secrets-и-переменные)
  - [§ 8. Health checks и rollback](#-8-health-checks-и-rollback)
  - [§ 9. Связь с docker-dev](#-9-связь-с-docker-dev)
  - [§ 10. Связь с dev-agent (conflict-detect)](#-10-связь-с-dev-agent-conflict-detect)
  - [§ 11. Интеграция в процесс](#-11-интеграция-в-процесс)
  - [§ 12. Post-deploy validation](#-12-post-deploy-validation)
- [Решения](#решения)
- [Закрытые вопросы](#закрытые-вопросы)
- [Задачи](#задачи)

---

## Контекст

**Задача:** `deploy.yml` не существует. `standard-release.md § 11` описывает триггер (`on: release: published`) и концептуальные шаги деплоя, но workflow-файла нет. `validate-post-release.py` обходит проверку деплоя через `--skip-deploy`.

**Почему создан:** Без `deploy.yml` Release не триггерит деплой. Это шаблон проекта — нужен параметризованный workflow с dynamic discovery, а не конкретная инфраструктура. Конкретные значения (registry, deploy target) заполняются при `/init-project`.

**Связанные файлы:**
- `.github/.instructions/releases/standard-release.md` — § 11 Публикация на production (триггер + шаги)
- `.github/.instructions/actions/standard-action.md` — стандарт GitHub Actions workflows
- `.github/workflows/ci.yml` — текущий CI (pre-commit + будущие security jobs)
- `.github/workflows/README.md` — реестр workflows
- `.claude/drafts/2026-02-24-docker-dev.md` — Dockerfile формат, compose (dev/test)
- `.claude/drafts/2026-02-24-conflict-detect.md` — dev-agent создаёт Dockerfile при разработке сервиса
- `specs/docs/.system/infrastructure.md` — спецификация инфраструктуры

**Поглощённые черновики** (контент перенесён в § 12):
- ~~`2026-02-25-smoke-tests.md`~~ — определение smoke tests, критерии pass/fail
- ~~`2026-02-25-post-release-validation.md`~~ — расширение standard-release.md § 11
- ~~`2026-02-24-post-release.md`~~ — G8: post-release workflow, best practices

Все три черновика описывали одну тему: "что делать после деплоя". 80% полезного контента уже было в этом черновике (§ 8 Health checks, § 4 smoke test step). Оставшиеся 20% перенесены в § 12. Теоретические best practices (canary, SLO/SLI, feature flags, incident response) отрезаны как over-engineering для template.

---

## Содержание

### § 1. AS IS — что уже есть

| Компонент | Файл | Статус |
|-----------|------|--------|
| Триггер деплоя | `standard-release.md § 11` | Описан: `on: release: published` |
| Deploy workflow | `.github/workflows/deploy.yml` | **Не существует** |
| Dockerfile формат | `standard-docker.md § 1` (docker-dev draft) | Запланирован: multi-stage, non-root |
| Docker Compose (dev) | `platform/docker/docker-compose.yml` (docker-dev draft) | Запланирован: инфра + stub-сервисы |
| Docker Compose (test) | `platform/docker/docker-compose.test.yml` (docker-dev draft) | Запланирован |
| Container registry | нигде | **Не определён** |
| Environments (staging/prod) | `standard-release.md § 11` | Концептуально: staging → production |
| Health checks | `standard-docker.md § 6` (docker-dev draft) | Запланированы: `/health` endpoint |
| Post-deploy validation | `validate-post-release.py` | `--skip-deploy` — обходит проверку |

**Пробелы:**
1. Нет `deploy.yml` — Release не триггерит деплой
2. Нет стандарта деплоя — нигде не описаны правила для deploy workflow
3. Нет выбора registry — GHCR vs Docker Hub vs self-hosted
4. Нет environment protection rules — staging/production не настроены
5. Нет rollback-механизма в workflow

---

### § 2. Архитектура: кто что создаёт

```
Кто                        Что создаёт                    Когда
─────────────────────────  ─────────────────────────────── ──────────────────────
/init-project              deploy.yml (из шаблона)         Phase 0 (один раз)
                           .env.example (registry URL)
                           GitHub Environments (staging/prod)

docker-dev                 standard-docker.md § 1          Phase 0 (один раз)
                           (Dockerfile формат)

dev-agent (BLOCK-N)        src/{svc}/Dockerfile            При разработке сервиса
                           (по стандарту standard-docker.md)

deploy.yml                 Сканирует src/*/Dockerfile      При каждом Release
(dynamic discovery)        → build → push → deploy
```

**Ключевой принцип:** `deploy.yml` НЕ нужно менять при добавлении нового сервиса. Dev-agent создаёт `src/{svc}/Dockerfile` → `deploy.yml` обнаруживает его автоматически.

---

### § 3. standard-deploy.md

**Путь:** `.github/.instructions/actions/deploy/standard-deploy.md`
**Действие:** Создать через `/instruction-create`.

Стандарт deploy workflow для проекта. Определяет правила, но НЕ конкретную инфраструктуру (она определяется при `/init-project`).

| # | Секция | Содержание |
|---|--------|-----------|
| 1 | Назначение | Deploy workflow — автоматический деплой при публикации Release |
| 2 | Файлы и расположение | `.github/workflows/deploy.yml`, шаблон в `platform/.github/templates/` |
| 3 | Триггер | `on: release: types: [published]`. Только из main. Нет ручного dispatch (осознанно) |
| 4 | Dynamic service discovery | Сканирование `src/*/Dockerfile`. Правило: есть Dockerfile = деплоится |
| 5 | Container registry | GHCR (default) или Docker Hub. Конфигурируется через secrets |
| 6 | Build | Multi-stage: target `production`. Tag = release version. Latest = stable only |
| 7 | Environments | staging (auto-deploy, smoke tests) → production (manual approval или auto) |
| 8 | Secrets | `REGISTRY_URL`, `REGISTRY_USERNAME`, `REGISTRY_PASSWORD`, `DEPLOY_HOST`, `DEPLOY_SSH_KEY` |
| 9 | Health checks | POST-deploy: HTTP GET `{host}:{port}/health` для каждого сервиса, timeout 60s |
| 10 | Rollback | При failure health check → redeploy предыдущий тег. Автоматический rollback |
| 11 | Не включено | Kubernetes, Terraform, cloud-specific (AWS ECS, GCP Cloud Run) — вне scope шаблона |

**Принципы:**

> **Dynamic discovery.** Workflow не содержит хардкоженных имён сервисов. Добавление нового сервиса = добавление Dockerfile. Удаление = удаление Dockerfile.

> **Dockerfile = deployable.** Если в `src/{svc}/` есть Dockerfile — сервис деплоится. Нет Dockerfile — не деплоится (библиотеки в `shared/`, утилиты без runtime).

> **Шаблон, не конкретика.** Deploy target (Docker Compose SSH, K8s apply, cloud deploy) — плейсхолдер. Конкретная команда деплоя определяется при `/init-project` на основе выбранной инфраструктуры.

---

### § 4. Шаблон deploy.yml

**Путь:** `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  release:
    types: [published]

permissions:
  contents: read
  packages: write  # для GHCR

env:
  REGISTRY: ghcr.io/${{ github.repository_owner }}
  TAG: ${{ github.event.release.tag_name }}

jobs:
  # ──────────────────────────────────────────
  # 1. Discover services with Dockerfiles
  # ──────────────────────────────────────────
  discover:
    runs-on: ubuntu-latest
    outputs:
      services: ${{ steps.find.outputs.services }}
    steps:
      - uses: actions/checkout@v4

      - id: find
        name: Find services with Dockerfile
        run: |
          services=$(find src -maxdepth 2 -name Dockerfile \
            | xargs -I{} dirname {} \
            | xargs -I{} basename {} \
            | jq -R -s -c 'split("\n") | map(select(. != ""))')
          echo "services=$services" >> "$GITHUB_OUTPUT"
          echo "Discovered services: $services"

  # ──────────────────────────────────────────
  # 2. Build & push images (parallel per service)
  # ──────────────────────────────────────────
  build:
    needs: [discover]
    runs-on: ubuntu-latest
    if: needs.discover.outputs.services != '[]'
    strategy:
      fail-fast: true
      matrix:
        service: ${{ fromJson(needs.discover.outputs.services) }}
    steps:
      - uses: actions/checkout@v4

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & push
        uses: docker/build-push-action@v6
        with:
          context: src/${{ matrix.service }}
          file: src/${{ matrix.service }}/Dockerfile
          target: production
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ matrix.service }}:${{ env.TAG }}
            ${{ env.REGISTRY }}/${{ matrix.service }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ──────────────────────────────────────────
  # 3. Deploy to staging
  # ──────────────────────────────────────────
  deploy-staging:
    needs: [build, discover]
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        env:
          SERVICES: ${{ needs.discover.outputs.services }}
        run: |
          # PLACEHOLDER: заменить при /init-project
          # Варианты:
          #   Docker Compose + SSH: ssh $HOST "cd /app && docker compose pull && docker compose up -d"
          #   Kubernetes: kubectl set image deployment/$svc $svc=$REGISTRY/$svc:$TAG
          #   Cloud: aws ecs update-service / gcloud run deploy
          echo "Deploy to staging: $SERVICES (tag: $TAG)"
          echo "TODO: implement deploy command"

      - name: Smoke test staging
        env:
          SERVICES: ${{ needs.discover.outputs.services }}
        run: |
          # PLACEHOLDER: health check для каждого сервиса
          # for svc in $(echo $SERVICES | jq -r '.[]'); do
          #   curl --fail --retry 5 --retry-delay 10 "https://staging.example.com/$svc/health"
          # done
          echo "TODO: implement smoke tests"

  # ──────────────────────────────────────────
  # 4. Deploy to production
  # ──────────────────────────────────────────
  deploy-production:
    needs: [deploy-staging, discover]
    runs-on: ubuntu-latest
    environment: production  # requires manual approval (GitHub Environment protection)
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        env:
          SERVICES: ${{ needs.discover.outputs.services }}
        run: |
          # PLACEHOLDER: аналогично staging
          echo "Deploy to production: $SERVICES (tag: $TAG)"
          echo "TODO: implement deploy command"

      - name: Health check production
        env:
          SERVICES: ${{ needs.discover.outputs.services }}
        run: |
          # PLACEHOLDER: health check
          echo "TODO: implement health checks"

  # ──────────────────────────────────────────
  # 5. Rollback on failure
  # ──────────────────────────────────────────
  rollback:
    needs: [deploy-production]
    runs-on: ubuntu-latest
    if: failure()
    steps:
      - name: Get previous release tag
        id: prev
        run: |
          prev_tag=$(gh api repos/${{ github.repository }}/releases \
            --jq '.[1].tag_name // "none"')
          echo "tag=$prev_tag" >> "$GITHUB_OUTPUT"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Rollback to previous version
        if: steps.prev.outputs.tag != 'none'
        run: |
          # PLACEHOLDER: redeploy предыдущий тег
          echo "Rolling back to ${{ steps.prev.outputs.tag }}"
          echo "TODO: implement rollback"
```

---

### § 5. Dynamic service discovery

**Принцип:** `src/{svc}/Dockerfile` = "этот сервис деплоится".

**Discover job:**
```bash
find src -maxdepth 2 -name Dockerfile | xargs -I{} dirname {} | xargs -I{} basename {}
# → ["auth", "gateway", "users"]
```

**Результат передаётся через `matrix`:** Каждый сервис собирается и пушится параллельно.

**Что НЕ деплоится:**
- `shared/` — библиотека, нет Dockerfile, нет runtime
- `src/{svc}/` без Dockerfile — сервис в разработке, ещё не готов к деплою
- `platform/` — инфраструктура, не application

**Когда Dockerfile появляется:** Dev-agent создаёт `src/{svc}/Dockerfile` при разработке сервиса (BLOCK-N в conflict-detect). Формат Dockerfile — по `standard-docker.md § 1` (multi-stage, target development/production, non-root user).

---

### § 6. Environments: staging и production

**GitHub Environments** — настраиваются при `/init-project`:

| Environment | Protection rules | Назначение |
|-------------|-----------------|-----------|
| `staging` | Нет (auto-deploy) | Smoke tests после деплоя |
| `production` | Required reviewers (1+) | Manual approval перед деплоем |

**Поток:**
```
Release published
  → build (parallel per service)
    → deploy-staging (auto)
      → smoke tests
        → deploy-production (manual approval)
          → health check
            → OK: done
            → FAIL: rollback job
```

**Конфигурация environments** — часть initialization.md (настройка нового репозитория):

```bash
# Создать environment "staging"
gh api repos/{owner}/{repo}/environments/staging -X PUT

# Создать environment "production" с protection rules
gh api repos/{owner}/{repo}/environments/production -X PUT \
  --input '{"reviewers":[{"type":"User","id":USER_ID}]}'
```

---

### § 7. Secrets и переменные

**Repository secrets** (настраиваются при `/init-project`):

| Secret | Назначение | Пример |
|--------|-----------|--------|
| `REGISTRY_URL` | Container registry URL | `ghcr.io/myorg` |
| `DEPLOY_HOST` | SSH host для деплоя | `deploy.example.com` |
| `DEPLOY_SSH_KEY` | SSH private key | (generated) |

**Примечание:** При использовании GHCR — `GITHUB_TOKEN` достаточно (permissions: packages: write). `REGISTRY_URL` и credentials нужны только для внешних registry.

**Environment secrets** (per-environment, настраиваются при `/init-project`):

| Secret | Environment | Назначение |
|--------|-------------|-----------|
| `DATABASE_URL` | staging, production | Connection string к БД |
| `REDIS_URL` | staging, production | Connection string к Redis |

---

### § 8. Health checks и rollback

**Health check стандарт:**

Каждый сервис с Dockerfile ДОЛЖЕН иметь endpoint `/health`:

```json
GET /health → 200 OK
{
  "status": "healthy",
  "service": "{svc}",
  "version": "{tag}"
}
```

**Post-deploy проверка:**
```bash
for svc in $(echo $SERVICES | jq -r '.[]'); do
  curl --fail --retry 5 --retry-delay 10 --max-time 60 \
    "https://${DEPLOY_HOST}/${svc}/health"
done
```

**Rollback:**
- Триггер: `if: failure()` на job `deploy-production`
- Действие: redeploy предыдущий release tag
- Предыдущий тег: `gh api repos/{owner}/{repo}/releases --jq '.[1].tag_name'`
- Ограничение: rollback к предыдущей версии, не к произвольной

**Связь с standard-docker.md:**

`standard-docker.md § 6` (docker-dev draft) описывает health checks для dev-окружения (`pg_isready`, `redis-cli ping`). Deploy health checks — для application-уровня (`/health` endpoint). Не пересекаются: docker-dev = инфраструктура, deploy = приложение.

---

### § 9. Связь с docker-dev

| Аспект | docker-dev (draft #10) | deploy-workflow (этот draft) |
|--------|------------------------|------------------------------|
| Dockerfile формат | `standard-docker.md § 1` — multi-stage, targets | Использует `target: production` |
| Compose | dev + test конфигурации | Не использует compose (production = orchestrator) |
| Registry | Не нужен (локальные образы) | GHCR / Docker Hub |
| Health checks | Инфраструктурные (pg_isready) | Application (/health endpoint) |
| Ports | Фиксированные из infrastructure.md | Определяются orchestrator / load balancer |

**Shared:** Один и тот же `src/{svc}/Dockerfile` используется и в dev (target: development), и в deploy (target: production). Multi-stage build из `standard-docker.md` обеспечивает оба сценария.

---

### § 10. Связь с dev-agent (conflict-detect)

**Когда dev-agent создаёт Dockerfile:**

Dev-agent при работе над BLOCK-N (per-service блок) создаёт `src/{svc}/Dockerfile` как часть service scaffold. Это происходит при первом TASK-N для сервиса.

**Контекст dev-agent** (из conflict-detect § 5.1):
- `docs/{svc}.md` — Tech Stack секция определяет базовый образ
- `standard-docker.md` — формат Dockerfile (multi-stage, non-root, layer caching)
- `docs/.system/infrastructure.md` — порты, зависимости

**INFRA-блок (wave 0):**

INFRA-блок НЕ создаёт Dockerfiles — он создаёт shared-контракты и конфигурации. Dockerfiles — ответственность per-service блоков (wave 1+).

**Что означает для deploy.yml:**

1. Wave 0 (INFRA) завершён → shared/ готов, config/ готов
2. Wave 1 (per-service) завершён → `src/{svc}/Dockerfile` созданы
3. Release published → deploy.yml сканирует `src/*/Dockerfile` → деплоит всё
4. Нет ручной синхронизации — dynamic discovery решает проблему

---

### § 11. Интеграция в процесс

**Где deploy-workflow встраивается в standard-process.md:**

| Фаза процесса | Deploy action |
|----------------|--------------|
| Phase 0: Init | `/init-project` создаёт deploy.yml из шаблона, настраивает environments |
| Development | Dev-agent создаёт `src/{svc}/Dockerfile` (per-service BLOCK-N) |
| Pre-release | `validate-pre-release.py` — deploy.yml должен существовать |
| Release | `gh release create` → triggers deploy.yml |
| Post-release | Health checks, rollback при failure |

**Обновление standard-process.md:**

В § 8 (Tool summary) добавить строку:
```
| Deploy workflow | standard-deploy.md + deploy.yml | on: release published, dynamic discovery |
```

**Обновление standard-release.md § 11:**

Заменить концептуальное описание ссылкой на `standard-deploy.md`:
```markdown
## 11. Публикация на production

**SSOT:** [standard-deploy.md](../actions/deploy/standard-deploy.md)

Деплой выполняется автоматически при публикации Release через `deploy.yml`.
Workflow использует dynamic service discovery — сканирует `src/*/Dockerfile`.
```

**Обновление standard-action.md:**

Добавить deploy.yml в таблицу обязательных workflows:
```markdown
| deploy.yml | Deploy | `on: release: [published]` | Build & deploy сервисов |
```

**Обновление validate-post-release.py:**

Убрать `--skip-deploy` — проверка деплоя становится обязательной (deploy.yml существует, workflow run succeeded).

---

### § 12. Post-deploy validation

> **Поглощённые черновики:** smoke-tests.md, post-release-validation.md, post-release.md — объединены сюда. Оригиналы удалены.

#### 12.1 Что такое smoke test

Smoke test — **минимальная** проверка "система не сломана" после деплоя. Это НЕ полный e2e-тестовый набор.

| Характеристика | Значение |
|---------------|----------|
| Количество сценариев | 3-10 (не 500) |
| Время выполнения | < 2 минут |
| Что проверяет | Health + critical paths |
| Где запускать | В deploy.yml после каждого деплоя (staging и production) |
| Тестовые данные | Не загрязняют production (read-only или sandbox) |

**Минимальный smoke test для сервиса:**

1. `GET /health` → 200 + `{"status": "healthy"}` (из § 8)
2. Один read endpoint → 200 (подтверждает что API отвечает)
3. Один write endpoint → создание + удаление тестовой сущности (если safe)

**Где живут smoke tests в проекте:**

| Путь | Назначение |
|------|-----------|
| `tests/smoke/` | Smoke-скрипты для всех сервисов |
| `tests/smoke/{svc}/` | Smoke-скрипты конкретного сервиса |
| `make test-smoke` | Запуск всех smoke tests |
| `make test-smoke-{svc}` | Smoke test одного сервиса |

**Связь с analysis chain:** Smoke-сценарии определяются НЕ здесь, а в `plan-test.md` (TC-N). Здесь — только инфраструктура запуска и минимальные требования.

#### 12.2 Post-deploy checklist

Упрощённый чек-лист для template-проекта (без мониторинга):

| # | Проверка | Автоматизация | Когда |
|---|---------|--------------|-------|
| 1 | deploy.yml завершён успешно | `gh run list --workflow=deploy.yml` | Сразу |
| 2 | Health check `GET /health` → 200 | curl в deploy.yml (§ 8) | После деплоя |
| 3 | Smoke tests пройдены | `make test-smoke` в deploy.yml | После health check |
| 4 | `validate-post-release.py --version vX.Y.Z` | Скрипт (303 строки, существует) | После smoke |
| 5 | Release Freeze снят | Ручное | После успешной валидации |

**Мониторинг** (error rate, latency, logs) — реализуется при настройке Prometheus/Grafana. Для template не блокирует. Структура `platform/monitoring/` уже заложена.

#### 12.3 Rollback criteria

| Условие | Действие | Автоматизация |
|---------|---------|---------------|
| Health check fail после 3 retry (60s) | Rollback | Автоматический (rollback job в deploy.yml § 4) |
| Smoke test fail | Rollback | Автоматический |
| Error rate > 5% за 15 мин | Rollback | Ручной (нет мониторинга в template) |
| Hotfix возможен < 30 мин | Hotfix вместо rollback | Ручной (standard-release.md § 12) |

Rollback = redeploy предыдущий тег (R5), не revert в git. Предыдущий тег: `gh api repos/{owner}/{repo}/releases --jq '.[1].tag_name'`.

#### 12.4 Расширение standard-release.md § 11

Текущий § 11 содержит 3 строки (health check, smoke tests, мониторинг). При реализации задач этого черновика — **заменить** концептуальное описание ссылкой на `standard-deploy.md`:

```markdown
## 11. Публикация на production

**SSOT:** [standard-deploy.md](../actions/deploy/standard-deploy.md)

Деплой выполняется автоматически при публикации Release через `deploy.yml`.
Workflow использует dynamic service discovery — сканирует `src/*/Dockerfile`.

Post-deploy verification: health check (12.2 #2), smoke tests (12.2 #3),
rollback при failure (12.3). Детали в standard-deploy.md.
```

#### 12.5 Что вне scope template

Следующие темы реализуются при **первом реальном деплое**, а не в template:

| Тема | Почему отложена |
|------|----------------|
| Canary / blue-green deployment | Нет Kubernetes / service mesh |
| SLO/SLI / error budget | Нет мониторинга (Prometheus/Grafana не настроены) |
| Observability (Prometheus, Loki, Jaeger) | `platform/monitoring/` — только .gitkeep |
| Feature flags integration | `config/feature-flags/` пуст |
| Incident response / severity levels | Организационный процесс, не tooling |
| Post-release notifications (Slack) | Нет webhook URL |
| Latency / throughput baseline | Нет данных — нет сервисов |
| Error rate monitoring | Нет инструментов — нет трафика |

При появлении инфраструктуры — создать `standard-post-release.md` (отдельный стандарт post-deploy проверок). Сейчас: health check + smoke tests в deploy.yml достаточно.

#### 12.6 Скилл /post-release

**Deliverable:** Скилл-обёртка над `validate-post-release.py`.

| Поле | Значение |
|------|----------|
| Скилл | `/post-release` |
| SSOT | `/.github/.instructions/releases/validation-release.md` |
| Что делает | Запускает validate-post-release.py, проверяет Release + деплой |
| Когда вызывать | После `gh release create` (шаг 7 в create-release.md) |
| Параметры | `--version vX.Y.Z` (обязательный), `--skip-deploy` (опциональный) |

Формат вызова: `/post-release v1.0.0`

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| R1 | Dynamic service discovery (`find src/*/Dockerfile`), а не хардкоженный список | Добавление сервиса = добавление Dockerfile (dev-agent). Deploy.yml не нужно менять. Единственная точка правды — файловая система. |
| R2 | Отдельный `standard-deploy.md`, а не секция в `standard-action.md` | Deploy достаточно сложен (environments, rollback, health checks, secrets) для отдельного стандарта. `standard-action.md` описывает формат workflow, не семантику деплоя. |
| R3 | GHCR как default registry (не Docker Hub) | GHCR интегрирован с GitHub (auth через GITHUB_TOKEN, permissions через packages:write). Нет дополнительных credentials. Переключение на Docker Hub — одна переменная. |
| R4 | Staging → Production с manual approval | Staging = auto-deploy + smoke tests. Production = manual approval через GitHub Environment protection. Баланс автоматизации и контроля. |
| R5 | Rollback = redeploy предыдущий тег (не revert) | Revert в git создаёт новый коммит, путает историю. Redeploy предыдущего тега — чистый, предсказуемый, не меняет git историю. |
| R6 | Placeholder для deploy command (не конкретная реализация) | Шаблон проекта не знает target platform (Docker Compose SSH, K8s, cloud). Placeholder заполняется при `/init-project`. |
| R7 | `/health` endpoint как стандарт для health checks | Универсальный, простой, проверяем curl-ом. Нет зависимости от orchestrator-specific health probes. |
| R8 | Dockerfile = deployable (нет Dockerfile = не деплоится) | Чёткое правило без конфигурации. `shared/` не имеет Dockerfile → не деплоится. Новый сервис без Dockerfile → не деплоится пока не готов. |
| R9 | Dev-agent создаёт Dockerfile как часть service scaffold | Dockerfile — часть кода сервиса, не инфраструктурная задача. Dev-agent знает tech stack из `docs/{svc}.md` и формат из `standard-docker.md`. |
| R10 | Не создавать отдельный скилл `/deploy` | Деплой триггерится автоматически через Release publish. Ручной деплой = ручной запуск workflow через GitHub UI (`workflow_dispatch` можно добавить позже). |
| R11 | Post-deploy validation минимальна: health + smoke (3-10 сценариев) | Template не имеет ни сервисов, ни мониторинга. Canary, SLO, feature flags — при первом реальном деплое, не сейчас. Over-engineering теоретическими стандартами не добавляет ценности. |
| R12 | Поглощение 3 черновиков (smoke-tests, post-release-validation, post-release) | 80% полезного контента уже было в §4/§8 этого черновика. Три отдельных черновика создавали искусственные зависимости и путаницу. Единый § 12 покрывает всю тему. |

---

## Закрытые вопросы

| # | Вопрос | Ответ |
|---|--------|-------|
| Q1 | Какой тип деплоя? Docker Compose / K8s / SSH? | Placeholder (R6). Шаблон не определяет target platform — это решение при `/init-project`. |
| Q2 | Какой container registry? | GHCR по умолчанию (R3). Переключение — одна переменная `REGISTRY`. |
| Q3 | Нужен ли staging? | Да (R4). Staging = auto-deploy + smoke tests. Production = manual approval. |
| Q4 | Кто обновляет deploy.yml при новом сервисе? | Никто (R1). Dynamic discovery. Dev-agent создаёт Dockerfile → deploy.yml подхватывает. |
| Q5 | Где описать стандарт — в standard-action.md или отдельно? | Отдельный standard-deploy.md (R2). Deploy достаточно сложен для своего стандарта. |

---

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Создать standard-deploy.md
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (секция "§ 3")
    /instruction-create для .github/.instructions/actions/deploy/standard-deploy.md.
    11 секций: назначение, файлы, триггер (on: release: published),
    dynamic service discovery (src/*/Dockerfile), container registry (GHCR default),
    build (multi-stage target production), environments (staging → production),
    secrets (REGISTRY_URL, DEPLOY_HOST, DEPLOY_SSH_KEY),
    health checks (GET /health, timeout 60s), rollback (redeploy prev tag),
    не включено (K8s, Terraform, cloud-specific).
    Создать также: validation-deploy.md, README.md для подпапки deploy/.
  activeForm: Создаю standard-deploy.md

TASK 2: Создать шаблон deploy.yml
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (секция "§ 4")
    Создать .github/workflows/deploy.yml.
    5 jobs: discover (find src/*/Dockerfile → matrix), build (parallel per service,
    GHCR push, cache-from/to gha), deploy-staging (environment: staging, PLACEHOLDER),
    deploy-production (environment: production, manual approval, PLACEHOLDER),
    rollback (if: failure(), redeploy prev tag, PLACEHOLDER).
    Все deploy-команды — PLACEHOLDER с комментариями вариантов (Docker Compose SSH, K8s, Cloud).
  activeForm: Создаю deploy.yml

TASK 3: Обновить .github/workflows/README.md
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (задача 3)
    Зарегистрировать deploy.yml в .github/workflows/README.md:
    - Добавить строку в таблицу workflows
    - Обновить дерево
  activeForm: Обновляю workflows/README.md

TASK 4: Обновить standard-release.md § 11
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (секция "§ 11" + "§ 12.4")
    Заменить концептуальное описание в .github/.instructions/releases/standard-release.md § 11
    ссылкой на standard-deploy.md. Текущие 3 строки (health check, smoke tests, мониторинг)
    → SSOT-ссылка + краткое описание (deploy.yml, dynamic discovery, post-deploy verification).
  activeForm: Обновляю standard-release.md

TASK 5: Обновить standard-action.md
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (задача 5)
    Добавить deploy.yml в таблицу обязательных workflows
    в .github/.instructions/actions/standard-action.md.
    Строка: deploy.yml | Deploy | on: release: [published] | Build & deploy сервисов.
  activeForm: Обновляю standard-action.md

TASK 6: Обновить validate-post-release.py
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (задача 6)
    Файл: .github/.instructions/.scripts/validate-post-release.py.
    Убрать --skip-deploy как дефолтное поведение — проверка деплоя обязательна
    (deploy.yml существует). Добавить проверку workflow run status:
    E-POST-003 "deploy.yml workflow run succeeded".
    --skip-deploy оставить как явный флаг.
  activeForm: Обновляю validate-post-release.py

TASK 7: Создать validate-deploy.py
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (задача 7)
    /script-create для .github/.instructions/.scripts/validate-deploy.py.
    Проверки: trigger=release:published, discover job существует,
    matrix strategy из discover outputs, environments (staging, production),
    rollback job с if: failure(), permissions packages:write.
  activeForm: Создаю validate-deploy.py

TASK 8: Добавить pre-commit хук для deploy.yml
  blockedBy: [7]
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (задача 8)
    Добавить хук в .pre-commit-config.yaml:
    - Триггер: .github/workflows/deploy.yml
    - Entry: validate-deploy.py
    Обновить .structure/pre-commit.md — добавить строку в таблицу "Активные хуки".
  activeForm: Добавляю pre-commit хук deploy

TASK 9: Обновить standard-process.md
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (секция "§ 11")
    Обновить specs/.instructions/standard-process.md:
    - § 8 (Tool summary): добавить строку Deploy workflow (standard-deploy.md + deploy.yml)
    - Связь с Phase 5 (Поставка): deploy.yml триггерится при Release published
  activeForm: Обновляю standard-process.md

TASK 10: Обновить initialization.md
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (секция "§ 6")
    Обновить .structure/initialization.md — секция настройки environments:
    - Создание GitHub Environments (staging, production) через gh api
    - Production: required reviewers, deployment protection rules
    - Секреты: REGISTRY_URL, DEPLOY_HOST, DEPLOY_SSH_KEY (per-environment)
  activeForm: Обновляю initialization.md

TASK 11: Создать скилл /post-release
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (секция "§ 12.6", из поглощённого post-release.md)
    /skill-create для .claude/skills/post-release/SKILL.md.
    SSOT: /.github/.instructions/releases/validation-release.md.
    Обёртка: запуск validate-post-release.py --version $VERSION.
    Параметры: --version (обязательный), --skip-deploy (опциональный).
    Формат вызова: /post-release v1.0.0.
  activeForm: Создаю /post-release skill

TASK 12: Добавить make test-smoke в Makefile
  description: >
    Драфт: .claude/drafts/2026-02-25-deploy-workflow.md (секция "§ 12.1", из поглощённого smoke-tests.md)
    Добавить таргет test-smoke в Makefile (заглушка, аналогично test-e2e):
    @echo "TODO: настроить smoke тесты".
    Добавить make test-smoke в CLAUDE.md секцию команд.
    Smoke tests запускаются в deploy.yml § 4 (deploy-staging job).
  activeForm: Добавляю make test-smoke
```
