---
description: Стандарт GitHub Actions workflow — структура файла, best practices, именование, триггеры, переиспользование.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/README.md
---

# Стандарт GitHub Actions

Версия стандарта: 1.0

Правила создания, структурирования и оформления файлов GitHub Actions в `.github/workflows/`.

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [GitHub Starter Workflows](https://github.com/actions/starter-workflows) — готовые шаблоны для разных языков

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-action.md](./validation-action.md) |
| Создание | *Не планируется* |
| Модификация | *Не планируется* |

**Зависимые стандарты:**

| Область | Документ | Что регулирует |
|---------|----------|----------------|
| Development Workflow | [standard-github-workflow.md](../standard-github-workflow.md) | Цикл разработки и триггеры для workflows |

## Оглавление

- [Quick Reference](#quick-reference)
- [1. Назначение workflow файлов](#1-назначение-workflow-файлов)
- [2. Расположение и именование](#2-расположение-и-именование)
- [3. Структура YAML файла](#3-структура-yaml-файла)
- [4. Триггеры (on)](#4-триггеры-on)
- [5. Переменные окружения (env)](#5-переменные-окружения-env)
- [6. Jobs и Steps](#6-jobs-и-steps)
- [7. Secrets и Variables](#7-secrets-и-variables)
- [8. Reusable Workflows](#8-reusable-workflows)
- [9. Матричные стратегии](#9-матричные-стратегии)
- [10. Условия выполнения](#10-условия-выполнения)
- [11. Артефакты и кэширование](#11-артефакты-и-кэширование)
- [12. Best Practices](#12-best-practices)
- [13. Ограничения и квоты](#13-ограничения-и-квоты)
- [14. Debugging и troubleshooting](#14-debugging-и-troubleshooting)
- [15. Composite Actions](#15-composite-actions)
- [16. Environments](#16-environments)
- [17. Concurrency](#17-concurrency)
- [18. Валидация workflow файлов](#18-валидация-workflow-файлов)
- [19. Локальное тестирование](#19-локальное-тестирование)

---

## Quick Reference

**Минимальный CI workflow (копировать и адаптировать):**

```yaml
name: CI
on: [push, pull_request]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - run: make test
```

**Основные паттерны:**

| Паттерн | Пример |
|---------|--------|
| Тесты при PR | `on: pull_request` |
| Deploy при Release | `on: release: types: [published]` |
| Ручной запуск | `on: workflow_dispatch` |
| Кэш зависимостей | `actions/cache@v4` с `hashFiles()` |
| Минимальные права | `permissions: contents: read` |
| Timeout | `timeout-minutes: 15` |

---

## 1. Назначение workflow файлов

**Workflow** — YAML файл, описывающий автоматизированный процесс в GitHub Actions.

### Когда создавать workflow

| Сценарий | Пример |
|----------|--------|
| **CI** | Запуск тестов и линтинга при PR |
| **CD** | Деплой на production при создании Release |
| **Scheduled tasks** | Еженедельное обновление зависимостей |
| **Custom automation** | Автоматическое закрытие stale Issues |

### Когда НЕ создавать workflow

| Сценарий | Альтернатива |
|----------|--------------|
| Локальные проверки перед коммитом | Pre-commit hooks (см. [initialization.md](/.structure/initialization.md)) |
| Скрипты для ручного запуска | Bash-скрипты в `platform/scripts/` |
| Деплой на production | Использовать Release workflow (триггер: `release.published`) — см. [standard-release.md](../releases/standard-release.md). Для staging/dev окружений — создавать отдельные workflow с `workflow_dispatch` или `push` триггером. |

### Scope и границы документа

**Этот стандарт покрывает:**
- Структура YAML файлов workflow (синтаксис, поля, типы)
- Триггеры (on: push, pull_request, release, schedule, workflow_dispatch)
- Jobs и steps (структура, зависимости, условия)
- Secrets и variables (использование)
- Reusable workflows (создание и вызов)
- Best practices для workflow файлов

**Этот стандарт НЕ покрывает:**
- Процесс релиза (когда создавать Release, как версионировать) → см. [standard-release.md](../releases/standard-release.md)
- Версионирование (semver, changelog) → см. [standard-release.md](../releases/standard-release.md)
- Development workflow (Issue → Branch → PR → Merge) → см. [standard-github-workflow.md](../standard-github-workflow.md)

**Ключевое:** Этот документ описывает "КАК писать YAML", а смежные стандарты — "КОГДА и ДЛЯ ЧЕГО использовать workflows".

---

## 2. Расположение и именование

### Расположение

**Путь:**
```
.github/workflows/{name}.yml
```

**Обязательно:**
- YAML расширение: `.yml` (НЕ `.yaml`)
- Папка `.github/workflows/` (GitHub автоматически распознаёт файлы в этой папке)

### Именование файлов

**Формат:**
```
{purpose}.yml
```

**Правила:**

| Правило | Пример ✅ | Пример ❌ |
|---------|----------|----------|
| Kebab-case | `deploy-production.yml` | `deploy_production.yml` |
| Латиница | `ci.yml` | `ци.yml` |
| Нижний регистр | `ci-checks.yml` | `CI-Checks.yml` |
| Описательное имя | `test-backend.yml` | `workflow1.yml` |

**Рекомендуемые имена:**

| Имя | Назначение |
|-----|------------|
| `ci.yml` | Общие CI проверки (тесты, линтинг) |
| `pre-release.yml` | Валидация перед релизом (pre-commit + security) |
| `deploy.yml` | Деплой на production ([standard-deploy.md](./deploy/standard-deploy.md)) |
| `test-{service}.yml` | Тесты для конкретного сервиса |
| `release.yml` | Автоматизация релизов |
| `scheduled-{task}.yml` | Запланированные задачи |

---

## 3. Структура YAML файла

### Минимальный workflow

```yaml
name: {Название workflow}

on:
  {триггеры}

jobs:
  {job-id}:
    runs-on: {runner}
    steps:
      - name: {Название шага}
        run: {команда}
```

### Обязательные поля (top-level)

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `name` | string | Название workflow (отображается в GitHub UI) | `CI Checks` |
| `on` | object/array | Триггеры запуска | `push`, `pull_request` |
| `jobs` | object | Задачи для выполнения | См. [Jobs и Steps](#6-jobs-и-steps) |

### Опциональные поля (top-level)

Добавлять только при необходимости конкретной функциональности.

| Поле | Тип | Когда добавлять | Описание |
|------|-----|----------------|----------|
| `env` | object | Если переменные используются в нескольких jobs | Глобальные переменные окружения |
| `defaults` | object | Если нужно изменить shell по умолчанию | Настройки по умолчанию (shell, working-directory) |
| `permissions` | object | **Рекомендуется всегда** (принцип минимальных прав) | Разрешения для `GITHUB_TOKEN` |
| `concurrency` | object | Если нужно запретить параллельные запуски workflow | Ограничение параллельных запусков |

### Пример полной структуры

```yaml
name: CI Checks

on:
  push:
    branches: [main]
  pull_request:

env:
  NODE_VERSION: '18'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linter
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
```

---

## 4. Триггеры (on)

**Триггер** — событие, запускающее workflow.

### Типы триггеров

#### 4.1 Push события

```yaml
on:
  push:
    branches:
      - main
      - develop
    paths:
      - 'src/**'
      - '!docs/**'
```

**Фильтры:**
- `branches` — запуск при push в указанные ветки
- `paths` — запуск при изменении файлов по паттерну
- `!` в paths — исключить паттерн

#### 4.2 Pull Request события

```yaml
on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened
    branches:
      - main
```

**Типы PR событий:**

| Тип | Когда срабатывает |
|-----|-------------------|
| `opened` | PR создан |
| `synchronize` | Новый коммит в PR |
| `reopened` | PR переоткрыт |
| `closed` | PR закрыт (merged или discarded) |
| `ready_for_review` | PR убран из Draft |

**По умолчанию (без types):**

Если `types` не указан, GitHub автоматически запускает workflow при событиях:
- `opened` — PR создан
- `synchronize` — Новый коммит в PR
- `reopened` — PR переоткрыт

**Пример:**
```yaml
on:
  pull_request:  # Запустится при opened, synchronize, reopened
```

#### 4.3 Release события

```yaml
on:
  release:
    types: [published]
```

**Типы Release событий:**

| Тип | Когда срабатывает |
|-----|-------------------|
| `published` | Release опубликован (НЕ draft) |
| `created` | Release создан (может быть draft) |
| `edited` | Release изменён |

#### 4.4 Scheduled (Cron)

```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Каждое воскресенье в 00:00 UTC
```

**Формат cron:**
```
┌───────── минута (0 - 59)
│ ┌─────── час (0 - 23)
│ │ ┌───── день месяца (1 - 31)
│ │ │ ┌─── месяц (1 - 12)
│ │ │ │ ┌─ день недели (0 - 6, воскресенье = 0)
│ │ │ │ │
* * * * *
```

**Примеры:**

| Cron | Описание |
|------|----------|
| `0 0 * * *` | Каждый день в полночь |
| `0 */6 * * *` | Каждые 6 часов |
| `0 9 * * 1` | Каждый понедельник в 09:00 |

#### 4.5 Manual (workflow_dispatch)

```yaml
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
```

**Запуск:**
```bash
gh workflow run {workflow-name}.yml -f environment=production
```

#### 4.6 Комбинированные триггеры

```yaml
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
```

#### 4.7 Координация workflows (workflow_run)

```yaml
# deploy.yml — запускается после успешного CI
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

**Когда использовать:** Deploy зависит от CI. Один workflow не должен содержать и тесты, и деплой.

#### 4.8 Комбинированные триггеры

**Правило:** Workflow срабатывает при ЛЮБОМ из указанных событий.

**Связь с условиями (if):**
- Триггер определяет КОГДА запускается **весь workflow**
- Условие `if` в job определяет КАКИЕ **конкретные jobs** выполняются внутри workflow

**Пример:** Deploy только при push в main, но тесты — всегда:

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    # Выполнится всегда (при любом триггере)
    steps:
      - run: npm test

  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    # Выполнится ТОЛЬКО при push в main
    steps:
      - run: npm run deploy
```

---

## 5. Переменные окружения (env)

### Уровни переменных

#### 5.1 Глобальный уровень (workflow)

```yaml
env:
  NODE_VERSION: '18'
  DATABASE_URL: ${{ secrets.DATABASE_URL }}

jobs:
  # Все jobs имеют доступ к NODE_VERSION и DATABASE_URL
```

#### 5.2 Уровень job

```yaml
jobs:
  build:
    env:
      BUILD_ENV: 'production'
    steps:
      # Только этот job имеет доступ к BUILD_ENV
```

#### 5.3 Уровень step

```yaml
steps:
  - name: Build
    env:
      CUSTOM_VAR: 'value'
    run: echo $CUSTOM_VAR
```

### Встроенные переменные (GitHub Context)

```yaml
steps:
  - name: Print context
    run: |
      echo "Repository: ${{ github.repository }}"
      echo "Branch: ${{ github.ref_name }}"
      echo "Actor: ${{ github.actor }}"
      echo "SHA: ${{ github.sha }}"
```

**Полезные переменные:**

| Переменная | Описание | Пример |
|------------|----------|--------|
| `github.repository` | Владелец/репозиторий | `owner/repo` |
| `github.ref_name` | Имя ветки или тега | `main` |
| `github.sha` | SHA коммита | `ffac537e6cbbf934b08745a378932722df287a53` |
| `github.actor` | Логин пользователя, запустившего workflow | `username` |
| `github.event_name` | Тип события | `push`, `pull_request` |

**Документация:** [GitHub Actions contexts](https://docs.github.com/en/actions/learn-github-actions/contexts)

---

## 6. Jobs и Steps

### Структура Job

```yaml
jobs:
  {job-id}:
    name: {Отображаемое имя}
    runs-on: {runner}
    needs: [{dependency-jobs}]
    if: {условие}
    env:
      {переменные}
    steps:
      - {step 1}
      - {step 2}
```

### Обязательные поля job

| Поле | Тип | Описание |
|------|-----|----------|
| `runs-on` | string/array | Тип runner (см. ниже) |
| `steps` | array | Список шагов для выполнения |

**Runners:**

| Runner | Когда использовать |
|--------|--------------------|
| `ubuntu-latest` | По умолчанию (рекомендуется) |
| `windows-latest` | Windows-специфичные тесты |
| `macos-latest` | macOS/iOS сборки |
| `self-hosted` | Приватные окружения, специфичное железо |

**Self-hosted runners:** Settings → Actions → Runners → Add runner. Использовать для приватных окружений или когда требуется специфичное железо. Требует отдельной настройки изоляции и безопасности.

### Опциональные поля job

| Поле | Описание | Пример |
|------|----------|--------|
| `name` | Название job в UI | `Run tests` |
| `needs` | Зависимость от других jobs | `[build]` |
| `if` | Условие выполнения | `github.ref == 'refs/heads/main'` |
| `timeout-minutes` | Таймаут (по умолчанию: 360 минут) | `30` |
| `continue-on-error` | Продолжить workflow при ошибке в job | `true` |

### Структура Step

```yaml
steps:
  # Action из marketplace
  - name: Checkout code
    uses: actions/checkout@v4

  # Shell команда
  - name: Run tests
    run: npm test

  # Многострочная команда
  - name: Build
    run: |
      npm install
      npm run build
```

### Типы steps

#### 6.1 Uses (готовые Actions)

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

**Популярные Actions (примеры):**

Ниже перечислены часто используемые actions. Полный список доступен в [GitHub Marketplace](https://github.com/marketplace?type=actions).

| Action | Назначение |
|--------|------------|
| `actions/checkout@v4` | Клонирование репозитория |
| `actions/setup-node@v4` | Установка Node.js |
| `actions/setup-python@v5` | Установка Python |
| `actions/cache@v4` | Кэширование зависимостей |
| `actions/upload-artifact@v4` | Загрузка артефактов |

#### 6.2 Run (shell команды)

```yaml
- name: Run script
  run: python scripts/deploy.py
  working-directory: ./platform
  shell: bash
```

**Опции run:**

| Опция | Описание |
|-------|----------|
| `working-directory` | Директория для выполнения команды |
| `shell` | Shell (bash, pwsh, python) |

### Зависимости между jobs (needs)

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

**Правило:**
- Jobs без `needs` выполняются параллельно
- Job с `needs` ждёт завершения зависимостей

**ВАЖНО:** `needs` контролирует ТОЛЬКО порядок выполнения. Для передачи файлов между jobs используйте артефакты:

```yaml
jobs:
  build:
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-files
          path: dist/

  test:
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-files
          path: dist/
      - run: npm test
```

См. [Секция 11: Артефакты](#11-артефакты-и-кэширование) для деталей.

### Output переменные между jobs

**Output** — передача переменных (не файлов) между jobs.

**Пример:**

```yaml
jobs:
  generate-version:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - id: version
        run: echo "version=1.2.3" >> $GITHUB_OUTPUT

  build:
    needs: generate-version
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building version ${{ needs.generate-version.outputs.version }}"
```

**Когда использовать:**
- Передача версии между jobs
- Передача флагов (true/false)
- Передача metadata (build ID, commit SHA)

**Когда НЕ использовать:**
- Для передачи файлов → использовать артефакты (см. [Секция 11](#11-артефакты-и-кэширование))

---

## 7. Secrets и Variables

### Secrets

**Secrets** — конфиденциальные данные (токены, пароли, ключи).

#### Создание секрета

```bash
# Для репозитория
gh secret set DATABASE_URL --body "postgresql://..."

# Для организации
gh secret set --org {org-name} DATABASE_URL --body "postgresql://..."
```

#### Использование в workflow

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
    steps:
      - run: echo "Connecting to database..."
```

**Важно:**
- Секреты НЕ отображаются в логах (GitHub маскирует значения)
- Доступ к секретам имеют ТОЛЬКО workflows в репозитории

### Variables

**Variables** — несекретные переменные (конфигурация, версии).

#### Создание переменной

```bash
gh variable set NODE_VERSION --body "18"
```

#### Использование в workflow

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ vars.NODE_VERSION }}
```

### Где хранить secrets

Стандарт хранения и именования secrets — см. [standard-secrets.md](./security/standard-secrets.md).

### Разница: Secrets vs Variables

| Аспект | Secrets | Variables |
|--------|---------|-----------|
| **Видимость** | Скрыты в логах | Видны в логах |
| **Назначение** | Пароли, токены | Версии, конфиги |
| **Синтаксис** | `${{ secrets.NAME }}` | `${{ vars.NAME }}` |

---

## 8. Reusable Workflows

**Reusable Workflow** — workflow, который можно вызывать из других workflows.

### Создание reusable workflow

```yaml
# .github/workflows/reusable-tests.yml
name: Reusable Tests

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      npm-token:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm test
        env:
          NPM_TOKEN: ${{ secrets.npm-token }}
```

**Важно:**
- `inputs` — обычные параметры (строки, числа, булевы значения)
- `secrets` — параметры для передачи секретов (должны существовать в вызывающем репозитории или организации)
- Reusable workflow НЕ имеет прямого доступа к секретам вызывающего репозитория — секреты ДОЛЖНЫ быть явно переданы через `secrets:` при вызове

### Вызов reusable workflow

```yaml
# .github/workflows/ci.yml
name: CI

on: [push]

jobs:
  test:
    uses: ./.github/workflows/reusable-tests.yml
    with:
      node-version: '18'
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}
```

### Когда использовать

| Сценарий | Пример |
|----------|--------|
| Повторяющаяся логика | Тесты запускаются в нескольких workflows |
| Параметризация | Deploy на разные окружения с разными параметрами |
| Централизация | Обновить логику в одном месте для всех workflows |

---

## 9. Матричные стратегии

**Matrix** — запуск job с комбинациями параметров.

### Базовая матрица

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

**Результат:** 9 jobs (3 OS × 3 Node versions).

### Исключение комбинаций

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node-version: [16, 18]
    exclude:
      - os: windows-latest
        node-version: 16
```

**Результат:** 3 jobs (исключён Windows + Node 16).

### Fail-fast

```yaml
strategy:
  fail-fast: false  # Явно указывать для ясности
  matrix:
    os: [ubuntu-latest, windows-latest]
```

**По умолчанию (`fail-fast: true`):**
- При провале одного job — остальные отменяются
- **Когда использовать:** экономия CI-минут, быстрое обнаружение проблем

**С `fail-fast: false`:**
- Все jobs выполняются независимо
- **Когда использовать:** нужен полный отчёт (например, тестирование на разных OS для выявления всех проблем сразу)

---

## 10. Условия выполнения

### Условия для jobs

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
```

### Условия для steps

```yaml
steps:
  - name: Deploy to production
    if: github.event_name == 'release'
    run: npm run deploy
```

### Стандартные условия

| Условие | Описание |
|---------|----------|
| `github.ref == 'refs/heads/main'` | Только для ветки main |
| `github.event_name == 'push'` | Только при push |
| `success()` | Предыдущие шаги успешны (по умолчанию) |
| `failure()` | Предыдущий шаг провалился |
| `always()` | Выполнить всегда (даже при ошибке) |
| `cancelled()` | Workflow отменён |

### Пример: отправка уведомления при ошибке

```yaml
steps:
  - name: Run tests
    run: npm test

  - name: Notify on failure
    if: failure()
    run: curl -X POST ${{ secrets.SLACK_WEBHOOK }} -d '{"text":"Tests failed"}'
```

---

## 11. Артефакты и кэширование

### Артефакты (artifacts)

**Артефакт** — файлы, сохраняемые между jobs или для скачивания.

#### Загрузка артефакта

```yaml
steps:
  - name: Build
    run: npm run build

  - name: Upload build
    uses: actions/upload-artifact@v4
    with:
      name: build-files
      path: dist/
      retention-days: 7
```

#### Скачивание артефакта (в другом job)

```yaml
jobs:
  deploy:
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-files
          path: dist/
```

### Кэширование (cache)

**Cache** — сохранение зависимостей между запусками workflow.

```yaml
steps:
  - uses: actions/checkout@v4

  - name: Cache node_modules
    uses: actions/cache@v4
    with:
      path: node_modules
      key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
      restore-keys: |
        ${{ runner.os }}-node-

  - run: npm install
```

**Ключи кэша:**
- `key` — уникальный идентификатор (по содержимому `package-lock.json`)
- `restore-keys` — fallback ключи (если точное совпадение не найдено)

**Как работает:**
1. При первом запуске: кэш отсутствует → `npm install` выполняется полностью → `node_modules` сохраняются в кэш
2. При последующих запусках:
   - Если `package-lock.json` НЕ изменился: кэш восстанавливает `node_modules` → `npm install` выполняется, но видит что зависимости уже установлены → завершается за секунды
   - Если `package-lock.json` изменился: старый кэш НЕ подходит → `npm install` выполняется полностью → новый `node_modules` сохраняется в кэш

**Преимущество:**
- Экономия времени: `npm install` с кэшем занимает 5-10 секунд вместо 30-60 секунд
- НЕ нужно удалять `npm install` из workflow — кэш ускоряет его, но не заменяет

### Сравнение: Артефакты vs Кэш

| Аспект | Артефакты | Кэш |
|--------|-----------|-----|
| **Назначение** | Передача файлов между jobs в **текущем** workflow | Ускорение повторных запусков workflow (разные runs) |
| **Время жизни** | 1-90 дней (настраивается `retention-days`) | До удаления при превышении лимита 10GB (oldest first) |
| **Доступность** | Только внутри workflow (или для скачивания через UI) | Между разными запусками workflow (если ключ совпадает) |
| **Размер** | До 10GB на артефакт | До 10GB на репозиторий (сумма всех кэшей) |
| **Когда использовать** | Build results, тестовые отчёты, coverage | node_modules, pip cache, gradle cache |

---

## 12. Best Practices

### 12.1 Именование

| Элемент | Правило | Пример |
|---------|---------|--------|
| **Workflow name** | Глагол + объект | `Deploy to Production` |
| **Job name** | Действие | `Run tests`, `Build Docker image` |
| **Step name** | Конкретное действие | `Install dependencies`, `Upload build artifact` |

### 12.2 Версионирование Actions

**Рекомендуемый формат: версия с major.minor**

```yaml
# ✅ Хорошо (рекомендуется)
- uses: actions/checkout@v4

# ❌ Плохо
- uses: actions/checkout@main
```

**Почему:**
- `@main` может внезапно сломаться при обновлении Action
- `@v4` — стабильная минорная версия (GitHub обновляет только patch-версии автоматически)

**Альтернатива (для критичных workflows):**

```yaml
# Максимальная стабильность: commit SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

**Когда использовать SHA:**
- Production workflows
- Workflows с доступом к секретам
- Защита от supply chain атак (action может быть скомпрометирован даже на stable версии)

### 12.3 Минимизация прав (permissions)

```yaml
permissions:
  contents: read
  pull-requests: write

jobs:
  # Только указанные права
```

**По умолчанию:** `GITHUB_TOKEN` имеет широкие права. Ограничивайте для безопасности.

### 12.4 Избегать хардкода

**❌ Плохо:**
```yaml
env:
  NODE_VERSION: '18'
```

**✅ Хорошо:**
```yaml
env:
  NODE_VERSION: ${{ vars.NODE_VERSION }}
```

**Почему:** Изменение версии Node не требует правки workflow.

### 12.5 Комментарии в YAML

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    # Deploy только после manual approval (через GitHub Environment)
    environment: production
    steps:
      - run: npm run deploy
```

### 12.6 Timeout для jobs

**Рекомендуется:** Явно указывать `timeout-minutes` для всех jobs (предотвращает зависания).

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30  # Макс. 30 минут
```

**По умолчанию:** 360 минут (6 часов) — слишком много для большинства jobs.

**Критерии выбора timeout:**
- CI проверки (lint, test): 10-30 минут
- Build (компиляция): 30-60 минут
- Deploy: 10-20 минут
- E2E тесты: 30-90 минут

### 12.7 Разделение CI и CD

**Рекомендуется:**
- `ci.yml` — тесты, линтинг (триггер: `push`, `pull_request`)
- `deploy.yml` — деплой (триггер: `release`)

**Не смешивать:** CI проверки и деплой в одном workflow.

### 12.8 Secrets в переменных окружения

**❌ Плохо:**
```yaml
run: curl -H "Authorization: Bearer ${{ secrets.TOKEN }}" ...
```

**✅ Хорошо:**
```yaml
env:
  AUTH_TOKEN: ${{ secrets.TOKEN }}
run: curl -H "Authorization: Bearer $AUTH_TOKEN" ...
```

**Почему:**
- Секреты, подставленные через `${{ secrets.TOKEN }}` напрямую в `run`, попадают в command-line аргументы процесса
- Command-line аргументы видны через `ps` и другие инструменты мониторинга процессов
- Использование через `env` гарантирует, что секреты НЕ отображаются в списке процессов (они доступны только внутри окружения процесса)
- GitHub маскирует секреты в логах в обоих случаях, но защита на уровне process list работает только через `env`

---

## 13. Ограничения и квоты

### GitHub Actions квоты

| План | Минуты в месяц (public repos) | Минуты в месяц (private repos) | Concurrent jobs |
|------|-------------------------------|--------------------------------|-----------------|
| **Free** | Неограничено | 2,000 | 20 |
| **Pro** | Неограничено | 3,000 | 40 |
| **Team** | Неограничено | 10,000 | 60 |
| **Enterprise** | Неограничено | 50,000 | 180 |

### Ограничения workflow

| Лимит | Значение |
|-------|----------|
| **Макс. jobs в workflow** | 256 |
| **Макс. время выполнения job** | 6 часов |
| **Макс. время выполнения workflow** | 72 часа |
| **Макс. размер артефакта** | 10 GB |
| **Макс. хранение артефакта** | 90 дней |
| **Макс. размер кэша** | 10 GB (на репозиторий) |

### Оптимизация использования

| Проблема | Решение |
|----------|---------|
| Долгие тесты | Использовать матричную стратегию (параллелизм) |
| Частые `npm install` | Кэшировать `node_modules` (см. [Кэширование](#11-артефакты-и-кэширование)) |
| Большие артефакты | Сжимать файлы перед загрузкой |
| Много workflows | Использовать reusable workflows |

---

## 14. Debugging и troubleshooting

### Просмотр логов

```bash
# Список запусков workflow
gh run list --workflow ci.yml

# Логи конкретного запуска
gh run view 123456 --log

# Логи конкретного job
gh run view 123456 --job 789
```

### Debug режим

**Включить подробные логи:**

1. Settings → Secrets → Add secret
2. Имя: `ACTIONS_RUNNER_DEBUG`, значение: `true`
3. Имя: `ACTIONS_STEP_DEBUG`, значение: `true`

**В workflow:**

```yaml
steps:
  - name: Debug info
    run: |
      echo "Event: ${{ github.event_name }}"
      echo "Ref: ${{ github.ref }}"
      echo "Actor: ${{ github.actor }}"
      env
```

### Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `Invalid workflow file` | YAML синтаксическая ошибка | Проверить YAML через yamllint |
| `Secret not found` | Секрет не создан или неправильное имя | `gh secret list` → проверить имя |
| `Job failed` | Команда вернула ненулевой exit code | Проверить логи → исправить команду |
| `Permission denied` | Недостаточно прав для `GITHUB_TOKEN` | Добавить `permissions:` в workflow |

---

## 15. Composite Actions

**Composite Action** — переиспользуемый набор **steps** (не целый workflow).

**Когда использовать:**
- Повторяющиеся steps в разных workflows
- Нужна переиспользуемая логика на уровне steps (не jobs)

**Пример создания:**

```yaml
# .github/actions/setup-node-with-cache/action.yml
name: 'Setup Node with cache'
description: 'Установка Node.js и кэширование node_modules'
inputs:
  node-version:
    description: 'Node.js version'
    required: true
runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - uses: actions/cache@v4
      with:
        path: node_modules
        key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
```

**Использование:**

```yaml
jobs:
  build:
    steps:
      - uses: ./.github/actions/setup-node-with-cache
        with:
          node-version: '18'
```

**Разница Reusable Workflow vs Composite Action:**

| Аспект | Reusable Workflow | Composite Action |
|--------|-------------------|------------------|
| **Уровень** | Целый workflow (jobs) | Набор steps |
| **Файл** | `.github/workflows/*.yml` | `.github/actions/*/action.yml` |
| **Вызов** | `jobs: { uses: }` | `steps: [ uses: ]` |
| **Секреты** | Явная передача через `secrets:` | Наследует от вызывающего |
| **Кэширование** | В каждом job отдельно | Общее с вызывающим |
| **Когда** | Сложные flow с несколькими jobs | Повторяющаяся последовательность steps |

---

## 16. Environments

**Environment** — именованное окружение (staging, production) с собственными:
- Секретами и переменными
- Правилами защиты (required reviewers)
- Deployment history

### Создание environment

**Через Web UI:**

1. Settings → Environments → New environment
2. Имя: `production`
3. Опционально: Required reviewers (минимум N approvals перед deploy)

### Использование в workflow

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Использовать секреты из production environment
    steps:
      - run: echo "Deploying to ${{ secrets.SERVER_URL }}"
      - run: npm run deploy
```

**Преимущества:**
- Разные секреты для staging и production
- Защита production через required reviewers
- История deployments в GitHub UI

**Связь с Release workflow:**
- Environment `production` используется для deploy по Release (см. [standard-release.md](../releases/standard-release.md))

---

## 17. Concurrency

**Concurrency** — ограничение параллельных запусков workflow.

**Когда использовать:**
- Deploy workflows (только один deploy в момент времени)
- Database migrations (предотвратить конфликты)

**Пример:**

```yaml
name: Deploy

on:
  push:
    branches: [main]

concurrency:
  group: production-deploy
  cancel-in-progress: false  # НЕ отменять текущий deploy

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

**Опции:**
- `group` — имя группы (workflows с одинаковым `group` НЕ выполняются параллельно)
- `cancel-in-progress` — отменить предыдущий запуск при новом push (default: `false`)

**Пример с `cancel-in-progress: true`:**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Отменить старый build при новом push в ту же ветку
```

**Когда `cancel-in-progress: true`:**
- CI workflows (тесты, линтинг) — экономия минут CI

**Когда `cancel-in-progress: false`:**
- Deploy workflows — НЕ отменять deploy посередине

---

## 18. Валидация workflow файлов

### Проверка синтаксиса YAML

```bash
# Установить yamllint
pip install yamllint

# Проверить workflow
yamllint .github/workflows/ci.yml
```

### Проверка через actionlint

**Установка:**

```bash
# macOS
brew install actionlint

# Linux
wget https://github.com/rhysd/actionlint/releases/download/v1.6.26/actionlint_1.6.26_linux_amd64.tar.gz
tar xvf actionlint_*.tar.gz
sudo mv actionlint /usr/local/bin/
```

**Использование:**

```bash
# Проверить все workflow файлы
actionlint .github/workflows/*.yml
```

**Интеграция в pre-commit:**

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/rhysd/actionlint
  rev: v1.6.26
  hooks:
    - id: actionlint
```

---

## 19. Локальное тестирование

### act — локальный запуск GitHub Actions

**Установка:**
```bash
# macOS
brew install act

# Windows (scoop)
scoop install act

# Linux
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

**Использование:**
```bash
# Запустить все workflows по событию push
act push

# Запустить конкретный workflow
act -W .github/workflows/ci.yml

# Запустить с секретами
act --secret-file .env.act
```

**Ограничения:**
- Не все Actions работают локально (actions/cache, GitHub API)
- Не поддерживает `services:` (Docker services)
- Некоторые `github.*` контексты недоступны

**Альтернатива:** Feature-ветка → push → проверка в Actions → исправление.

---

## Скиллы

*Скилл будет создан после завершения инструкции.*
