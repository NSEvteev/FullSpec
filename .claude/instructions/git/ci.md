---
type: standard
description: CI/CD pipeline структура, GitHub Actions, quality gates
related:
  - git/workflow.md
  - git/commits.md
  - git/review.md
  - git/issues.md
---

# CI/CD Pipeline

Правила организации CI/CD: структура pipeline, GitHub Actions, quality gates.

## Оглавление

- [Правила](#правила)
  - [Структура pipeline](#структура-pipeline)
  - [Quality gates](#quality-gates)
  - [GitHub Actions](#github-actions)
  - [Секреты и переменные](#секреты-и-переменные)
  - [Rollback при failed deploy](#rollback-при-failed-deploy)
  - [Alerting при failure](#alerting-при-failure)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Структура pipeline

**Правило:** Pipeline состоит из последовательных стадий (stages).

| Стадия | Назначение | Блокирует |
|--------|------------|-----------|
| `lint` | Проверка стиля кода | Да |
| `test` | Unit и integration тесты | Да |
| `build` | Сборка артефактов | Да |
| `security` | Сканирование уязвимостей | Да (для main) |
| `deploy` | Деплой в окружение | — |

**Правило:** Стадии выполняются последовательно. Провал любой стадии останавливает pipeline.

```yaml
# Порядок стадий
stages:
  - lint
  - test
  - build
  - security
  - deploy
```

### Quality gates

**Правило:** Merge в main разрешён только при выполнении всех качественных критериев.

| Критерий | Порог | Обязательность |
|----------|-------|----------------|
| Все тесты проходят | 100% | Обязательно |
| Покрытие кода | >= 80% | Обязательно |
| Линтер без ошибок | 0 errors | Обязательно |
| Без критических уязвимостей | 0 critical | Обязательно |
| Code review approved | >= 1 | Обязательно |

**Правило:** Quality gates настраиваются в Branch Protection Rules.

```yaml
# .github/branch-protection.yml (концептуально)
main:
  required_status_checks:
    - lint
    - test
    - security
  required_reviews: 1
  dismiss_stale_reviews: true
```

### GitHub Actions

**Правило:** Workflows располагаются в `.github/workflows/`.

| Файл | Назначение | Триггер |
|------|------------|---------|
| `ci.yml` | Основной CI pipeline | push, pull_request |
| `release.yml` | Релиз и changelog | tag push |
| `security.yml` | Сканирование безопасности | schedule, push to main |
| `deploy-*.yml` | Деплой в окружение | workflow_dispatch, push to main |

**Правило:** Используем reusable workflows для переиспользования.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: make lint

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Test
        run: make test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: make build
```

**Правило:** Job dependencies определяют порядок выполнения через `needs`.

### Секреты и переменные

**Правило:** Секреты хранятся в GitHub Secrets, не в коде.

| Тип | Где хранить | Пример |
|-----|-------------|--------|
| API ключи | GitHub Secrets | `${{ secrets.API_KEY }}` |
| Переменные окружения | GitHub Variables | `${{ vars.ENVIRONMENT }}` |
| Конфигурации | Repository files | `.env.example` |

**Правило:** Никогда не логировать секреты. GitHub автоматически маскирует их.

```yaml
# Использование секретов
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}
```

**Правило:** Для разных окружений используем GitHub Environments.

```yaml
jobs:
  deploy:
    environment: production
    steps:
      - name: Deploy
        env:
          API_URL: ${{ vars.API_URL }}  # из environment
```

### Rollback при failed deploy

**Правило:** При падении деплоя — автоматический откат на предыдущую версию.

| Ситуация | Действие |
|----------|----------|
| Health check failed | Откат на предыдущий image |
| Tests failed в prod | Откат + alert |
| Manual rollback | `gh workflow run rollback.yml` |

**Правило:** Rollback должен завершиться за < 5 минут.

```yaml
# .github/workflows/rollback.yml
name: Rollback

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: Rollback deployment
        run: |
          kubectl set image deployment/app app=${{ inputs.version }}
          kubectl rollout status deployment/app --timeout=5m
```

### Alerting при failure

**Правило:** При падении CI/CD — уведомление в канал команды.

| Событие | Канал | Приоритет |
|---------|-------|-----------|
| Deploy failed | Slack #alerts | High |
| Tests failed на main | Slack #ci | Medium |
| Security scan failed | Slack #security | High |

```yaml
# В workflow после failed step
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    channel-id: ${{ secrets.SLACK_CHANNEL }}
    slack-message: "❌ ${{ github.workflow }} failed: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

---

## Примеры

### Пример 1: Полный CI workflow

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  GO_VERSION: '1.21'
  NODE_VERSION: '20'

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}

      - name: Run linters
        run: make lint

  test:
    name: Test
    needs: lint
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}

      - name: Run tests
        run: make test
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  build:
    name: Build
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t app:${{ github.sha }} .

      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USER }} --password-stdin
          docker push app:${{ github.sha }}

  security:
    name: Security Scan
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
```

### Пример 2: Release workflow

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        uses: conventional-changelog/standard-version@v9

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          body_path: CHANGELOG.md
          generate_release_notes: true
```

### Пример 3: Deploy workflow с environments

```yaml
name: Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    name: Deploy to ${{ inputs.environment }}
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        run: |
          echo "Deploying to ${{ inputs.environment }}"
          # kubectl apply -f k8s/${{ inputs.environment }}/
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG }}
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| `ci-check` | Проверка статуса CI *(планируется)* |
| `ci-fix` | Исправление ошибок CI *(планируется)* |
| `ci-rerun` | Перезапуск failed jobs *(планируется)* |

---

## Связанные инструкции

- [workflow.md](workflow.md) — Git workflow, ветки, PR
- [commits.md](commits.md) — Conventional commits для changelog
- [review.md](review.md) — Code review перед merge
- [issues.md](issues.md) — GitHub Issues, задачи
