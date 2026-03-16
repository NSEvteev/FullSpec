---
description: Инициализация проекта — установка зависимостей, pre-commit хуки, branch protection, labels. Руководство после клонирования.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
---

# Инициализация проекта

После клонирования репозитория необходимо выполнить инициализацию для настройки локального окружения.

**Полезные ссылки:**
- [Структура проекта](./README.md)
- [Pre-commit хуки](./pre-commit.md)

---

## Оглавление

- [0. Создание проекта из template](#0-создание-проекта-из-template)
- [1. Быстрый старт](#1-быстрый-старт)
- [2. Зависимости](#2-зависимости)
- [3. Установка вручную](#3-установка-вручную)
- [4. Проверка установки](#4-проверка-установки)
- [5. Решение проблем](#5-решение-проблем)
- [CI (автоматически)](#ci-автоматически)
- [6. Настройка GitHub Security](#6-настройка-github-security)
- [7. Настройка Branch Protection Rules](#7-настройка-branch-protection-rules)
- [8. Настройка GitHub Labels (опционально)](#8-настройка-github-labels-опционально)
- [9. Настройка GitHub Environments (деплой)](#9-настройка-github-environments-деплой)
- [10. Claude-assisted инициализация](#10-claude-assisted-инициализация)
- [11. Backport улучшений в template](#11-backport-улучшений-в-template)
- [12. Forward port: template → проект](#12-forward-port-template--проект)

---

## 0. Создание проекта из template

> Этот шаг выполняется **один раз** при создании нового проекта. Если вы клонировали существующий проект — переходите к [§ 1](#1-быстрый-старт).

### Шаг 1: Создать репозиторий

На GitHub: **"Use this template" → "Create a new repository"**.

Копируется вся структура (код, инструкции, скиллы, агенты, rules, хуки), но **НЕ копируются Settings:**
- Branch Protection Rules
- Environments (staging/production)
- Labels (нужно sync)
- Secrets
- GitHub Pages settings

### Шаг 2: Клонировать и настроить

```bash
git clone https://github.com/{owner}/{new-repo}.git
cd {new-repo}
make setup    # pre-commit хуки
```

### Шаг 3: Инициализация через Claude

```
/init-project
```

Интерактивная настройка: Labels, Security, Branch Protection, Environments, CODEOWNERS. Подробнее — [§ 10](#10-claude-assisted-инициализация).

### Шаг 4: Очистить project-specific данные

| Что | Где | Действие |
|-----|-----|----------|
| Таблица цепочек | `specs/analysis/README.md` | Очистить строки таблицы (оставить заголовок) |
| Статус-трекер | `specs/analysis/README.md` | Очистить блок между `BEGIN:analysis-status` и `END:analysis-status` |
| CODEOWNERS | `.github/CODEOWNERS` | Заменить `@NSEvteev` на своего мейнтейнера |
| Черновики | `.claude/drafts/` | Удалить project-specific (оставить `examples/`) |

### Шаг 5: Первый коммит

```bash
git add -A
git commit -m "chore: инициализация проекта из template"
git push
```

Проект полностью рабочий. Все инструкции, скиллы, агенты, rules, pre-commit хуки — на месте. Начинай с `/chain`.

---

## 1. Быстрый старт

```bash
# После клонирования репозитория
make setup
```

Эта команда автоматически:
- Установит pre-commit хуки
- Проверит наличие необходимых зависимостей

---

## 2. Зависимости

### Обязательные

| Инструмент | Назначение | Установка |
|------------|------------|-----------|
| **Python 3.8+** | Скрипты валидации | [python.org](https://www.python.org/downloads/) |
| **pre-commit** | Хуки перед коммитом | `pip install pre-commit` |
| **Git** | Контроль версий | [git-scm.com](https://git-scm.com/) |
| **GitHub CLI (gh)** | Работа с Issues, PR, Releases | `winget install GitHub.cli` |
| **Docker Desktop** | Контейнеризация сервисов | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **WSL2** (Windows) | Linux-ядро для Docker | `wsl --install` |

---

## 3. Установка вручную

### Windows

```powershell
# 1. WSL2 + Docker Desktop
wsl --install                     # Перезагрузить после установки
# Скачать Docker Desktop: https://www.docker.com/products/docker-desktop/
# При установке: "Use WSL 2 based engine"
# Settings → Resources → WSL Integration → включить для дистрибутива
docker compose version            # Проверить

# 2. Pre-commit
pip install pre-commit

# 3. GitHub CLI
winget install GitHub.cli

# 4. Авторизация в GitHub (один раз)
gh auth login

# 5. Установка хуков
pre-commit install
```

### macOS

```bash
# 1. Docker Desktop
# Скачать: https://www.docker.com/products/docker-desktop/
docker compose version            # Проверить

# 2. Pre-commit
pip install pre-commit

# 3. GitHub CLI
brew install gh

# 4. Авторизация в GitHub (один раз)
gh auth login

# 5. Установка хуков
pre-commit install
```

### Linux

```bash
# 1. Docker Engine
# https://docs.docker.com/engine/install/
docker compose version            # Проверить

# 2. Pre-commit
pip install pre-commit

# 3. GitHub CLI (Ubuntu/Debian)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# 4. Авторизация в GitHub (один раз)
gh auth login

# 5. Установка хуков
pre-commit install
```

---

## 4. Проверка установки

```bash
# Проверить версии
python --version          # Python 3.8+
pre-commit --version      # pre-commit 3.x
gh --version              # gh 2.x
git --version             # git 2.x
docker compose version    # Docker Compose v2.x

# Проверить авторизацию GitHub
gh auth status

# Проверить pre-commit хуки
pre-commit run --all-files
```

**Ожидаемый результат pre-commit:**
```
Check README structure sync..........................Passed
Validate rules format................................Passed (или Skipped)
Validate scripts format..............................Passed (или Skipped)
Validate skills format...............................Passed (или Skipped)
Validate branch name.................................Passed
```

---

## 5. Решение проблем

### Pre-commit не запускается

```bash
# Переустановить хуки
pre-commit install -f
```

### gh: command not found

После установки gh CLI нужно перезапустить терминал или добавить в PATH:

**Windows:** `C:\Program Files\GitHub CLI`

### gh auth: not logged in

```bash
gh auth login
# Выбрать: GitHub.com → HTTPS → Login with browser
```

### Python не найден

Убедитесь что Python добавлен в PATH при установке.

---

## Что происходит при `make setup`

```
make setup
    │
    ├── pip install pre-commit     # Установка pre-commit
    │
    ├── pre-commit install         # Установка git hooks
    │
    └── Готово!
        │
        └── При каждом git commit
            автоматически запускаются
            проверки из .pre-commit-config.yaml
```

---

## CI (автоматически)

CI workflow уже настроен в репозитории — действий не требуется.

**Файл:** [`.github/workflows/ci.yml`](/.github/workflows/ci.yml)

**Что проверяет:** При каждом push в `main` и pull request запускаются те же pre-commit хуки на **всех** файлах. Если хуки были обойдены локально (`--no-verify`), CI поймает ошибку.

**Где смотреть результаты:** Вкладка Actions в GitHub → последний run, или:

```bash
gh run list --limit 5
gh run view <run-id> --log
```

---

## 6. Настройка GitHub Security

Файлы безопасности (`dependabot.yml`, `codeql.yml`, `SECURITY.md`) уже в репозитории из шаблона. Но **Settings не копируются** из template — их нужно настроить для каждого нового репозитория.

**SSOT:** [standard-security.md](/.github/.instructions/actions/security/standard-security.md)

### Шаг 1: Включить Dependabot

```
Settings → Code security and analysis →
  ✅ Dependabot alerts → Enable
  ✅ Dependabot security updates → Enable
```

### Шаг 2: Включить Secret Scanning

```
Settings → Code security and analysis →
  ✅ Secret scanning → Enable
  ✅ Push protection → Enable
```

### Шаг 3: Проверить файлы из шаблона

```bash
# Обновить контактный email в SECURITY.md
# Обновить директории сервисов в dependabot.yml
# Обновить matrix.language в codeql.yml
```

> **ВАЖНО:** НЕ включать Code Scanning → Default Setup в Settings. Используется Advanced Setup через `codeql.yml` (уже в репозитории). См. [standard-security.md § 4](/.github/.instructions/actions/security/standard-security.md#4-code-scanning-codeql).

---

## 7. Настройка Branch Protection Rules

Защита ветки main от некачественных изменений. Settings не копируются из template — настроить для каждого нового репозитория.

**SSOT:** [standard-review.md § 4](/.github/.instructions/review/standard-review.md#4-branch-protection-rules)

### Через GitHub UI

```
Settings → Branches → Branch protection rules → Add rule
  Branch name pattern: main

  ✅ Require a pull request before merging
  ✅ Require approvals: 1
  ✅ Require status checks to pass before merging
  ✅ Require branches to be up to date before merging
  □  Require conversation resolution (для команд 2+ человек)
  □  Require signed commits (для публичных проектов)

  → Save changes
```

### Через CLI (gh api)

```bash
# Посмотреть текущие правила
gh api repos/{owner}/{repo}/branches/main/protection --method GET

# Настроить правила (заменить {owner}/{repo})
gh api repos/{owner}/{repo}/branches/main/protection --method PUT \
  -f required_status_checks='{"strict":true,"contexts":["ci"]}' \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f enforce_admins=true \
  -f restrictions=null
```

> **Примечание:** Точные `contexts` для status checks зависят от имён CI workflows в `.github/workflows/`.

---

## 8. Настройка GitHub Labels (опционально)

После первоначальной настройки рекомендуется настроить систему меток GitHub:

```bash
# Показать diff (dry-run по умолчанию)
python .github/.instructions/.scripts/sync-labels.py

# Применить изменения (удаление default + создание проектных)
python .github/.instructions/.scripts/sync-labels.py --apply --force
```

Скрипт:
- Удалит стандартные метки GitHub (bug, documentation, enhancement, ...)
- Создаст систему меток проекта (type:, priority:, area:, status:)

> **Примечание:** `--force` удаляет default GitHub labels. Используйте `--apply` без `--force` для добавления без удаления.

---

## 9. Настройка GitHub Environments (деплой)

Для работы `deploy.yml` необходимо настроить GitHub Environments. Settings не копируются из template — настроить вручную.

**SSOT:** [standard-deploy.md](/.github/.instructions/actions/deploy/standard-deploy.md)

### Шаг 1: Создать environments

```bash
# Получить данные репозитория
OWNER=$(gh repo view --json owner -q .owner.login)
REPO=$(gh repo view --json name -q .name)

# Создать environment "staging" (auto-deploy)
gh api repos/$OWNER/$REPO/environments/staging -X PUT

# Создать environment "production" (manual approval)
# Заменить USER_ID на ID пользователя-ревьюера
gh api repos/$OWNER/$REPO/environments/production -X PUT \
  --input '{"reviewers":[{"type":"User","id":USER_ID}]}'
```

### Шаг 2: Настроить secrets (per-environment)

```bash
# Environment secrets (настраиваются администратором)
gh secret set DATABASE_URL --env staging --body "postgres://..."
gh secret set DATABASE_URL --env production --body "postgres://..."
gh secret set REDIS_URL --env staging --body "redis://..."
gh secret set REDIS_URL --env production --body "redis://..."
```

### Шаг 3: Repository secrets (опционально)

```bash
# Нужны только для внешних registry (не GHCR)
gh secret set DEPLOY_HOST --body "deploy.example.com"
gh secret set DEPLOY_SSH_KEY < ~/.ssh/deploy_key
```

> **Примечание:** При использовании GHCR — `GITHUB_TOKEN` достаточно (не нужны дополнительные registry credentials).

---

## 10. Claude-assisted инициализация

Для полной интерактивной настройки с Claude Code:

```
/init-project
```

Скилл оркестрирует все шаги из этого документа (§ 1–§ 9), проверяет состояние, задаёт вопросы через AskUserQuestion и генерирует итоговый отчёт.

| Режим | Описание |
|-------|----------|
| `/init-project` | Полная настройка (интерактивная) |
| `/init-project --check` | Только проверка, без мутаций (healthcheck) |
| `/init-project --skip-github` | Пропустить GitHub-шаги (§ 4–§ 7) |
| `/init-project --skip-docs` | Пропустить проверку docs/ (§ 8) |

**SSOT:** [create-initialization.md](./.instructions/create-initialization.md)

---

## 11. Backport улучшений в template

Когда в проекте улучшили инструкцию, скрипт, агента или rule — и хотим вернуть это в template для всех будущих проектов.

### Принципы

> **Не всё нужно возвращать.** Project-specific правки (API-контракты, конкретные сервисы, бизнес-логика) остаются в проекте. В template возвращаются только **универсальные** улучшения.

> **Template = generic.** Шаблон не должен содержать знания о конкретном проекте.

> **Атомарные PR.** Каждый backport — отдельный PR в template-репозиторий. Не смешивать несколько улучшений.

> **Копировать файлы напрямую через `cp`, не вручную.** Это гарантирует, что ничего не забыто и нет расхождений. Вручную редактируется только project-specific содержимое после копирования.

### Что возвращать

| Тип | Пример | Возвращать? |
|-----|--------|-------------|
| Исправление бага в скрипте | `validate-agent.py` принимает и файл, и папку | Да |
| Новый универсальный агент | `docker-agent` | Да |
| Улучшение инструкции | Новый шаг в `create-docs-sync.md` | Да |
| Новый per-tech стандарт | `standard-fastapi.md` | Да |
| Новый rule | `fastapi.md` в `.claude/rules/` | Да |
| Project-specific сервис | `specs/docs/auth.md` | Нет |
| Бизнес-дискуссия | `specs/analysis/0001-*/discussion.md` | Нет |
| Project-specific env | `.env.example` с конкретными переменными | Нет |

### Процесс

```
Проект (feature-repo)              Template (fullspec)
─────────────────────              ────────────────────────────
1. Улучшил инструкцию
   в проекте
                              2. cd в template-репозиторий
                              3. git checkout -b backport/{topic}
                              4. cp файлы из проекта 1:1 (не вручную!)
                              5. Отредактировать только project-specific
                                 секции (см. таблицу ниже)
                              6. pre-commit run --all-files
                              7. Commit + Push + PR в template
                              8. Merge PR
```

**Шаг 1: Определить что backport'ить**

```bash
# В проекте: показать изменённые инструкции/скрипты/агенты
git log --oneline --all -- '.instructions/' '.claude/' 'specs/.instructions/'
```

**Шаг 2: Подготовить template**

```bash
cd /path/to/fullspec
git checkout main && git pull
git checkout -b backport/{краткое-описание}
```

**Шаг 3: Скопировать файлы напрямую**

```bash
# Копировать файлы из проекта 1:1 — не редактировать вручную
PROJECT=/path/to/project
cp $PROJECT/specs/.instructions/some-file.md specs/.instructions/some-file.md
cp $PROJECT/.claude/skills/some-skill/SKILL.md .claude/skills/some-skill/SKILL.md
# ... и т.д. для каждого файла из списка backport
```

**Шаг 4: Адаптировать project-specific секции**

Большинство файлов не требуют адаптации и переносятся 1:1. Адаптация нужна только если файл содержит project-specific секции:

| Тип секции | Признак | Что делать |
|------------|---------|------------|
| Текущее состояние (сервисы, порты) | Конкретные имена: `postgres:5432`, `auth:8001` | Заменить на `{svc}:{PORT}`, пометить "заполняется в проекте" |
| Примеры сценариев (SMOKE-NNN) | Конкретные URL, тексты кнопок | Убрать конкретные примеры, оставить формат + пустую таблицу |
| Предусловия с конкретными портами | `5432/8001/3000` в таблице | Обобщить до "порты сервисов проекта" |

Убрать project-specific: конкретные имена сервисов → `{svc}`, порты → `{PORT}`, URL → плейсхолдеры, ссылки на project-specific docs → убрать.

**Шаг 5: Валидация и PR**

```bash
pre-commit run --all-files
git add {файлы}
git commit -m "feat(instructions): backport {описание} из {project}"
git push -u origin backport/{topic}
gh pr create --title "Backport: {описание}" --body "Из проекта {name}: {что улучшено}"
```

---

## 12. Forward port: template → проект

Когда template обновился и хочется подтянуть улучшения в существующий проект.

### Подключить template как remote (один раз)

```bash
# В проекте
git remote add template https://github.com/{owner}/fullspec.git
```

### Посмотреть что нового

```bash
git fetch template
git log --oneline template/main --since="2026-03-01" -- '.instructions/' '.claude/'
```

### Подтянуть изменения

```bash
# Вариант 1: cherry-pick конкретных коммитов
git cherry-pick {hash1} {hash2}

# Вариант 2: скопировать конкретный файл
git show template/main:.instructions/some-file.md > .instructions/some-file.md

# Вариант 3: diff + apply (если файл менялся в обоих местах)
git diff HEAD...template/main -- .instructions/some-file.md | git apply
```

> При конфликтах — разрешать вручную, project-specific правки имеют приоритет.

### После forward port — обновить другие проекты

Если backport прошёл в template, все проекты на его основе могут подтянуть через тот же forward port.

---

## Связанные документы

- [Pre-commit хуки](./pre-commit.md) — детали работы pre-commit
- [Процесс поставки ценности](/specs/.instructions/standard-process.md) — полный цикл от идеи до релиза (после инициализации — Фаза 1)
- [Makefile](/Makefile) — все команды проекта
- [CLAUDE.md](/CLAUDE.md) — инструкции для Claude Code
