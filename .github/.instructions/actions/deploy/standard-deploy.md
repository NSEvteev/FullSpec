---
description: Стандарт deploy workflow — триггеры, environments, dynamic service discovery, rollback, health checks.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/actions/deploy/README.md
---

# Стандарт Deploy Workflow

Версия стандарта: 1.0

Правила deploy workflow для проекта. Определяет триггеры, dynamic service discovery, environments, rollback и health checks. НЕ определяет конкретную инфраструктуру (Docker Compose SSH, Kubernetes, Cloud) — это решается при `/init-project`.

**Полезные ссылки:**
- [Инструкции Deploy](./README.md)
- [Standard Release](../../releases/standard-release.md)
- [Standard Action](../standard-action.md)
- [Standard Docker](/platform/.instructions/standard-docker.md)

**SSOT-зависимости:**

| Зона | Документ | Зона ответственности |
|------|----------|---------------------|
| Release | [standard-release.md](../../releases/standard-release.md) | Версионирование, changelog, публикация — § 11 ссылается сюда |
| Actions | [standard-action.md](../standard-action.md) | Формат YAML workflow, jobs, steps |
| Docker | [standard-docker.md](/platform/.instructions/standard-docker.md) | Dockerfile формат, multi-stage build |
| Development | [standard-development.md](../../development/standard-development.md) | Dev-agent создаёт Dockerfile при разработке |

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-deploy.md](./validation-deploy.md) |
| Создание | *Не требуется — deploy.yml создаётся при /init-project* |
| Модификация | *Не требуется — deploy.yml не меняется вручную* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Файлы и расположение](#2-файлы-и-расположение)
- [3. Триггер](#3-триггер)
- [4. Dynamic service discovery](#4-dynamic-service-discovery)
- [5. Container registry](#5-container-registry)
- [6. Build](#6-build)
- [7. Environments](#7-environments)
- [8. Secrets и переменные](#8-secrets-и-переменные)
- [9. Health checks и smoke tests](#9-health-checks-и-smoke-tests)
- [10. Rollback](#10-rollback)
- [11. Не включено](#11-не-включено)

---

## 1. Назначение

Deploy workflow — автоматический деплой при публикации GitHub Release.

**Применяется для:**
- Автоматического build и push Docker образов при Release
- Деплоя на staging (auto) и production (manual approval)
- Автоматического rollback при failure

**Принципы:**

> **Dynamic discovery.** Workflow не содержит хардкоженных имён сервисов. Добавление нового сервиса = добавление Dockerfile. Удаление = удаление Dockerfile.

> **Dockerfile = deployable.** Если в `src/{svc}/` есть Dockerfile — сервис деплоится. Нет Dockerfile — не деплоится (библиотеки в `shared/`, утилиты без runtime).

> **Шаблон, не конкретика.** Deploy target (Docker Compose SSH, K8s apply, cloud deploy) — плейсхолдер. Конкретная команда деплоя определяется при `/init-project`.

### Зона ответственности

**Этот стандарт регулирует:**
- Структуру deploy.yml (jobs, triggers, permissions)
- Dynamic service discovery (сканирование Dockerfiles)
- Environments (staging, production)
- Health checks и rollback
- Secrets для деплоя

**НЕ регулирует:**

| Что | Где регулируется |
|-----|------------------|
| Формат Dockerfile (multi-stage, targets) | [standard-docker.md](/platform/.instructions/standard-docker.md) |
| Создание Dockerfile (при разработке сервиса) | [standard-development.md](../../development/standard-development.md) |
| Процесс Release (версионирование, changelog) | [standard-release.md](../../releases/standard-release.md) |
| Формат YAML workflow (синтаксис, best practices) | [standard-action.md](../standard-action.md) |

---

## 2. Файлы и расположение

| Файл | Назначение |
|------|-----------|
| `.github/workflows/deploy.yml` | Deploy workflow (триггер: release published) |
| `src/{svc}/Dockerfile` | Dockerfile сервиса (создаётся dev-agent) |

### Кто что создаёт

| Кто | Что создаёт | Когда |
|-----|------------|-------|
| `/init-project` | `deploy.yml` (из шаблона) | Phase 0 (один раз) |
| dev-agent (BLOCK-N) | `src/{svc}/Dockerfile` | При разработке сервиса |
| `deploy.yml` | Сканирует `src/*/Dockerfile` → build → push → deploy | При каждом Release |

---

## 3. Триггер

```yaml
on:
  release:
    types: [published]
```

**Правила:**
- Только `published` (не `created`, не `edited`)
- Draft Release НЕ триггерит деплой (GitHub не отправляет `published` для draft)
- Pre-release НЕ триггерит деплой — deploy jobs должны иметь guard:
  ```yaml
  if: "!github.event.release.prerelease"
  ```
- Ручной dispatch (`workflow_dispatch`) не включён осознанно — деплой через Release

---

## 4. Dynamic service discovery

**Механизм:** сканирование `src/*/Dockerfile`.

```bash
find src -maxdepth 2 -name Dockerfile \
  | xargs -I{} dirname {} \
  | xargs -I{} basename {}
# → ["auth", "gateway", "users"]
```

**Результат передаётся через job outputs → matrix:** discover job сохраняет JSON-массив в `$GITHUB_OUTPUT`, downstream jobs используют `needs.discover.outputs.services`. Каждый сервис собирается и пушится параллельно через `fromJson()`.

**Что деплоится:**
- `src/{svc}/` с Dockerfile — деплоится

**Что НЕ деплоится:**
- `shared/` — библиотека, нет Dockerfile
- `src/{svc}/` без Dockerfile — сервис не готов к деплою
- `platform/` — инфраструктура, не application

**Когда Dockerfile появляется:** dev-agent при работе над BLOCK-N создаёт `src/{svc}/Dockerfile` как часть service scaffold. Формат — по [standard-docker.md](/platform/.instructions/standard-docker.md) § 1.

> **Deploy всех сервисов.** Workflow всегда деплоит ВСЕ сервисы с Dockerfile, а не только изменённые. Это сознательное решение template — упрощает конфигурацию. Partial deploy (по diff) добавляется при необходимости.

---

## 5. Container registry

**Default:** GHCR (GitHub Container Registry).

| Аспект | Значение |
|--------|----------|
| Registry URL | `ghcr.io/${{ github.repository_owner }}/${{ github.event.repository.name }}` |
| Image path | `ghcr.io/{owner}/{repo}/{service}:{tag}` |
| Auth | `GITHUB_TOKEN` (permissions: packages: write) |
| Альтернатива | Docker Hub (переключение через переменную `REGISTRY`) |

**Преимущества GHCR:**
- Интегрирован с GitHub (auth через GITHUB_TOKEN)
- Не нужны дополнительные credentials
- Привязан к организации/пользователю

---

## 6. Build

**Permissions (workflow-level):**

```yaml
permissions:
  contents: read
  packages: write
  deployments: write
```

**Timeout:** Все deploy jobs должны иметь `timeout-minutes: 30` (предотвращает зависание pipeline и бесконтрольный расход минут GitHub Actions).

```yaml
- uses: docker/build-push-action@v6
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
```

**Правила:**
- Target: `production` (multi-stage из standard-docker.md)
- Tags: release version + `latest`
- Кэширование: GitHub Actions cache (`type=gha`)
- `fail-fast: true` — остановить все builds при failure одного

---

## 7. Environments

**GitHub Environments** настраиваются при `/init-project`:

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

**Настройка environments** при `/init-project`:

```bash
# Создать environment "staging"
gh api repos/{owner}/{repo}/environments/staging -X PUT

# Создать environment "production" с protection rules
gh api repos/{owner}/{repo}/environments/production -X PUT \
  --input '{"reviewers":[{"type":"User","id":USER_ID}]}'
```

---

## 8. Secrets и переменные

**Repository secrets** (настраиваются при `/init-project`):

| Secret | Назначение | Пример |
|--------|-----------|--------|
| `REGISTRY_URL` | Container registry URL (если не GHCR) | `ghcr.io/myorg` |
| `DEPLOY_HOST` | SSH host для деплоя | `deploy.example.com` |
| `DEPLOY_SSH_KEY` | SSH private key | (generated) |

**Примечание:** При GHCR `GITHUB_TOKEN` достаточно. `REGISTRY_URL` нужен только для внешних registry.

**Environment secrets** (per-environment):

| Secret | Environment | Назначение |
|--------|-------------|-----------|
| `DATABASE_URL` | staging, production | Connection string к БД |
| `REDIS_URL` | staging, production | Connection string к Redis |

---

## 9. Health checks и smoke tests

### 9.1. Health checks

Каждый сервис с Dockerfile ДОЛЖЕН иметь endpoint `/health`:

```json
GET /health → 200 OK
{
  "status": "healthy",
  "service": "{svc}",
  "version": "{tag}"
}
```

**Post-deploy проверка** (встроена в deploy job):

```bash
for svc in $(echo $SERVICES | jq -r '.[]'); do
  curl --fail --retry 5 --retry-delay 10 --max-time 60 \
    "https://${DEPLOY_HOST}/${svc}/health"
done
```

### 9.2. Smoke tests

Отдельный job после `deploy-staging`. Проверяет critical paths, а не только доступность.

| Характеристика | Значение |
|---------------|----------|
| Количество сценариев | 3-10 |
| Время выполнения | < 2 минут |
| Что проверяет | Critical paths (auth flow, основные API endpoints) |
| Расположение | `tests/smoke/` |
| Запуск | `make test-smoke` |

---

## 10. Rollback

**Триггер:** `if: failure()` на job `deploy-production`.

**Действие:** redeploy предыдущий release tag.

```bash
# Получить предыдущий тег
prev_tag=$(gh api repos/{owner}/{repo}/releases \
  --jq '.[1].tag_name // "none"')

# Первый деплой — rollback невозможен
if [ "$prev_tag" == "none" ]; then
  echo "::warning::No previous release — rollback skipped"
  exit 0
fi

# Redeploy
# PLACEHOLDER: зависит от инфраструктуры
```

**Правила:**
- Rollback = redeploy предыдущий тег, не revert в git
- Автоматический при failure health check — если `curl --retry 5 --retry-delay 10 --max-time 60` завершается ненулевым кодом для любого сервиса
- Автоматический при failure smoke tests
- Ручной rollback при error rate > 5% — не автоматизирован в template (нет Prometheus/Datadog). Добавляется при подключении мониторинга
- При partial failure (один сервис из матрицы упал): `fail-fast: true` в build останавливает все сборки. Rollback откатывает ВСЕ сервисы к предыдущему тегу (атомарный деплой)
- При rollback тег `latest` НЕ перетегируется (остаётся на последнем failed release). Не рекомендуется использовать `latest` в docker-compose — использовать конкретный тег

---

## 11. Не включено

Следующие темы реализуются при конкретном деплое, не в template:

| Тема | Почему отложена |
|------|----------------|
| Database migrations | Не автоматизированы в template. При наличии migration-сервиса: добавить job `migrate` перед `deploy-production` с `needs: [migrate]` |
| Canary / blue-green deployment | Нет Kubernetes / service mesh |
| SLO/SLI / error budget | Нет мониторинга |
| Observability (Prometheus, Loki, Jaeger) | `platform/monitoring/` — только .gitkeep |
| Feature flags integration | `config/feature-flags/` пуст |
| Incident response | Организационный процесс, не tooling |
| Post-release notifications (Slack) | Нет webhook URL |
| Kubernetes / Terraform / cloud-specific | Выбор инфраструктуры — при `/init-project` |
