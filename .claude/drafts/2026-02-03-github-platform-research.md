# GitHub Platform Research

Исследование возможностей GitHub как платформы и определение инструкций для `.github/`.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Объекты GitHub](#1-объекты-github)
  - [2. Детальное описание объектов](#2-детальное-описание-объектов)
  - [3. Релизный цикл и ветвление](#3-релизный-цикл-и-ветвление)
  - [4. Организация работы команды (10 человек)](#4-организация-работы-команды-10-человек)
  - [5. Что должно быть в .github/](#5-что-должно-быть-в-github)
  - [6. Необходимые инструкции](#6-необходимые-инструкции)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Ссылки](#ссылки)

---

## Контекст

**Задача:** Организация `.github/` папки и создание инструкций для работы с GitHub
**Почему создан:** Папка `.github/` существует, но пустая. Нужно понять что туда добавить, какие объекты GitHub использовать, как организовать работу команды из 10 разработчиков.
**Связанные файлы:** `/.github/README.md`, `/.structure/README.md`, `/.structure/initialization.md`

---

## Содержание

### 1. Объекты GitHub

GitHub предоставляет следующие объекты для управления проектом:

| Объект | Назначение | Управление через CLI |
|--------|------------|---------------------|
| **Issue** | Задачи, баги, фичи | `gh issue` |
| **Pull Request** | Код-ревью, мерж | `gh pr` |
| **Release** | Версионирование, публикация | `gh release` |
| **Label** | Категоризация Issues/PR | `gh label` |
| **Milestone** | Группировка по целям/спринтам | `gh api` |
| **Project** | Канбан-доски | `gh project` |
| **Branch** | Ветки кода | `git branch` |
| **Tag** | Метки версий | `git tag` |
| **Workflow** | CI/CD автоматизация | `gh workflow`, `gh run` |
| **Secret** | Секреты для CI/CD | `gh secret` |
| **Variable** | Переменные для CI/CD | `gh variable` |

---

### 2. Детальное описание объектов

#### 2.1 Issue (Задача)

**Что это:** Единица работы — баг, фича, задача, вопрос.

**Свойства:**

| Свойство | Тип | Описание | CLI параметр |
|----------|-----|----------|--------------|
| `title` | string | Заголовок | `--title` |
| `body` | string | Описание (markdown) | `--body` |
| `assignees` | user[] | Исполнители | `--assignee` |
| `labels` | label[] | Метки | `--label` |
| `milestone` | milestone | Веха/спринт | `--milestone` |
| `project` | project | Канбан-доска | `--project` |
| `state` | enum | open/closed | `gh issue close/reopen` |
| `author` | user | Создатель (авто) | — |
| `created_at` | datetime | Дата создания (авто) | — |
| `number` | int | Номер (авто) | — |

**Команды CLI:**

```bash
# Создание
gh issue create --title "Название" --body "Описание" --label bug --assignee @me

# Просмотр
gh issue list                    # Список
gh issue view 123                # Детали
gh issue view 123 --comments     # С комментариями

# Редактирование
gh issue edit 123 --title "Новый заголовок"
gh issue edit 123 --add-label priority:high
gh issue edit 123 --add-assignee user1,user2
gh issue edit 123 --milestone "Sprint 1"

# Статус
gh issue close 123
gh issue reopen 123
gh issue pin 123                 # Закрепить
gh issue lock 123                # Заблокировать комменты

# Поиск
gh issue list --label bug
gh issue list --assignee @me
gh issue list --milestone "Sprint 1"
gh issue list --state closed
```

**Шаблоны Issue:**
- Размещаются в `.github/ISSUE_TEMPLATE/`
- Форматы: `.md` (простой) или `.yml` (форма)
- `config.yml` — конфигурация выбора шаблона

---

#### 2.2 Pull Request (PR)

**Что это:** Запрос на слияние изменений из одной ветки в другую.

**Свойства:**

| Свойство | Тип | Описание | CLI параметр |
|----------|-----|----------|--------------|
| `title` | string | Заголовок | `--title` |
| `body` | string | Описание | `--body` |
| `head` | branch | Исходная ветка | `--head` |
| `base` | branch | Целевая ветка | `--base` |
| `assignees` | user[] | Исполнители | `--assignee` |
| `reviewers` | user[] | Ревьюеры | `--reviewer` |
| `labels` | label[] | Метки | `--label` |
| `milestone` | milestone | Веха | `--milestone` |
| `project` | project | Доска | `--project` |
| `draft` | bool | Черновик | `--draft` |
| `state` | enum | open/closed/merged | — |
| `checks` | check[] | CI проверки (авто) | — |

**Команды CLI:**

```bash
# Создание
gh pr create --title "feat: новая фича" --body "Описание"
gh pr create --fill                  # Заполнить из коммитов
gh pr create --draft                 # Как черновик
gh pr create --reviewer user1,user2
gh pr create --base develop          # В другую ветку

# Просмотр
gh pr list
gh pr view 123
gh pr view 123 --comments
gh pr diff 123
gh pr checks 123                     # Статус CI

# Ревью
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Нужны правки"
gh pr review 123 --comment --body "Вопрос по строке 42"

# Мерж
gh pr merge 123                      # Интерактивно
gh pr merge 123 --squash             # Squash merge
gh pr merge 123 --rebase             # Rebase merge
gh pr merge 123 --merge              # Merge commit
gh pr merge 123 --auto               # Auto-merge когда CI пройдёт

# Редактирование
gh pr edit 123 --title "Новый заголовок"
gh pr edit 123 --add-reviewer user3
gh pr ready 123                      # Убрать draft
```

**Шаблон PR:**
- Файл: `.github/PULL_REQUEST_TEMPLATE.md`
- Или папка: `.github/PULL_REQUEST_TEMPLATE/` для нескольких шаблонов

**Связь Issue → PR:**
- В теле PR написать `Fixes #123` или `Closes #123`
- Issue автоматически закроется при мерже

---

#### 2.3 Label (Метка)

**Что это:** Категория для классификации Issues и PR.

**Свойства:**

| Свойство | Тип | Описание |
|----------|-----|----------|
| `name` | string | Название |
| `description` | string | Описание |
| `color` | hex | Цвет (#RRGGBB) |

**Команды CLI:**

```bash
# Список
gh label list

# Создание
gh label create "priority:high" --description "Высокий приоритет" --color FF0000
gh label create "type:bug" --color d73a4a
gh label create "type:feature" --color a2eeef

# Редактирование
gh label edit "bug" --name "type:bug"
gh label edit "type:bug" --color 00FF00

# Удаление
gh label delete "old-label"

# Клонирование из другого репо
gh label clone owner/repo
```

**Рекомендуемая система Labels:**

```
# Тип
type:bug          - Баг
type:feature      - Новая функциональность
type:task         - Техническая задача
type:docs         - Документация
type:refactor     - Рефакторинг

# Приоритет
priority:critical - Блокирует релиз
priority:high     - Важно
priority:medium   - Средний приоритет
priority:low      - Низкий приоритет

# Статус
status:blocked    - Заблокировано
status:in-review  - На ревью
status:ready      - Готово к работе

# Область
area:backend      - Бэкенд
area:frontend     - Фронтенд
area:infra        - Инфраструктура
area:api          - API
```

---

#### 2.4 Milestone (Веха)

**Что это:** Группировка Issues/PR по целям или спринтам.

**Свойства:**

| Свойство | Тип | Описание |
|----------|-----|----------|
| `title` | string | Название |
| `description` | string | Описание |
| `due_on` | date | Дедлайн |
| `state` | enum | open/closed |

**Команды CLI (через API):**

```bash
# Список
gh api repos/{owner}/{repo}/milestones

# Создание
gh api repos/{owner}/{repo}/milestones -f title="Sprint 1" -f due_on="2026-02-14T00:00:00Z"

# Редактирование
gh api repos/{owner}/{repo}/milestones/1 -X PATCH -f title="Sprint 1 (Extended)"

# Закрытие
gh api repos/{owner}/{repo}/milestones/1 -X PATCH -f state="closed"
```

**Применение:**
- Спринты: `Sprint 1`, `Sprint 2`
- Релизы: `v1.0`, `v1.1`, `v2.0`
- Цели: `MVP`, `Beta`, `GA`

---

#### 2.5 Project (Канбан-доска)

**Что это:** Визуализация работы в формате канбан.

**Свойства:**

| Свойство | Тип | Описание |
|----------|-----|----------|
| `title` | string | Название |
| `fields` | field[] | Поля (Status, Priority, etc.) |
| `items` | item[] | Issues/PR/Draft |
| `views` | view[] | Виды (Board, Table) |

**Команды CLI:**

```bash
# Авторизация (нужен scope project)
gh auth refresh -s project

# Список
gh project list

# Создание
gh project create --owner @me --title "Roadmap"

# Добавление Issue/PR
gh project item-add 1 --owner @me --url https://github.com/owner/repo/issues/123

# Поля
gh project field-list 1 --owner @me
gh project field-create 1 --owner @me --name "Priority" --data-type "SINGLE_SELECT"

# Просмотр
gh project view 1 --owner @me --web
```

---

#### 2.6 Release (Релиз)

**Что это:** Публикация версии с тегом, changelog и артефактами.

**Свойства:**

| Свойство | Тип | Описание | CLI параметр |
|----------|-----|----------|--------------|
| `tag` | string | Git тег | позиционный |
| `title` | string | Название | `--title` |
| `notes` | string | Changelog | `--notes` |
| `draft` | bool | Черновик | `--draft` |
| `prerelease` | bool | Пре-релиз | `--prerelease` |
| `assets` | file[] | Артефакты | позиционные |
| `target` | branch | Ветка для тега | `--target` |

**Команды CLI:**

```bash
# Список
gh release list

# Создание
gh release create v1.0.0 --title "Release v1.0.0" --notes "Changelog..."
gh release create v1.0.0 --generate-notes       # Авто-changelog
gh release create v1.0.0 -F CHANGELOG.md        # Из файла
gh release create v1.0.0 ./dist/*.zip           # С артефактами

# Просмотр
gh release view v1.0.0

# Редактирование
gh release edit v1.0.0 --draft=false

# Удаление
gh release delete v1.0.0
```

---

#### 2.7 Workflow (CI/CD)

**Что это:** Автоматизация через GitHub Actions.

**Файлы:** `.github/workflows/*.yml`

**Команды CLI:**

```bash
# Список workflows
gh workflow list

# Запуск вручную
gh workflow run ci.yml
gh workflow run ci.yml --ref feature-branch
gh workflow run ci.yml -f param1=value1

# Просмотр запусков
gh run list
gh run view 123456
gh run view 123456 --log

# Перезапуск
gh run rerun 123456
gh run rerun 123456 --failed  # Только упавшие jobs

# Отмена
gh run cancel 123456
```

---

#### 2.8 Branch Protection Rules

**Что это:** Правила защиты веток (настраиваются через Web UI или API).

**Возможности:**
- Требовать PR перед мержем
- Требовать ревью (N апрувов)
- Требовать прохождение CI
- Запретить force push
- Запретить удаление ветки

```bash
# Просмотр через API
gh api repos/{owner}/{repo}/branches/main/protection

# Создание (сложная структура — лучше через Web UI)
gh api repos/{owner}/{repo}/branches/main/protection -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["ci"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}'
```

---

### 3. Релизный цикл и ветвление

#### 3.1 Окружения

| Окружение | Где | Зачем |
|-----------|-----|-------|
| **local** | Ноутбук разработчика | Разработка и тестирование (`make dev`) |
| **production** | Сервер | Боевая система (деплой по Release) |

> **Примечание:** Staging не используется — достаточно локального тестирования для команды из 2 человек.

#### 3.2 Модель ветвления (упрощённый Git Flow)

```
main ─────●─────●─────●─────●─────●───→  (готовый код)
          │     ↑     │     ↑     │
          │     │     │     │     │
          └──●──┘     └──●──┘     └── Release v1.0 → production
            feature     feature
            branch      branch
```

**Ключевое:** merge в main ≠ деплой. Деплой происходит только при создании Release.

**Ветки:**

| Ветка | Назначение | Защита |
|-------|------------|--------|
| `main` | Готовый, проверенный код | Protected: PR required, CI pass |
| `feature/*` | Разработка фич | Нет защиты |
| `fix/*` | Исправление багов | Нет защиты |

#### 3.3 Workflow разработки

```
1. ISSUE
   └─ Создаётся задача в GitHub Issues
   └─ Labels: type:feature, priority:high

2. ЛОКАЛЬНАЯ РАЗРАБОТКА
   └─ git checkout -b feature/123-description
   └─ make dev → проект работает на localhost
   └─ Разработка и тестирование локально
   └─ git commit, git push

3. PULL REQUEST
   └─ gh pr create
   └─ Pre-commit проверки проходят
   └─ Code review (Claude или самопроверка)

4. MERGE
   └─ Squash merge в main
   └─ Issue автоматически закрывается (Fixes #123)
   └─ Код в main, но НЕ на production

5. RELEASE (когда готовы к деплою)
   └─ gh release create v1.0.0 --generate-notes
   └─ GitHub Actions деплоит на production
```

#### 3.4 Как код попадает на сервер

```
Разработчик        GitHub              Production
     │                │                     │
     ├─ make dev      │                     │
     │  (локально)    │                     │
     │                │                     │
     ├─ push ────────→│                     │
     │                │                     │
     ├─ PR ──────────→│                     │
     │                ├─ pre-commit         │
     │                │                     │
     ├─ merge ───────→│                     │
     │                ├─ код в main         │
     │                │  (не на сервере!)   │
     │                │                     │
     └─ release ─────→│                     │
                      ├─ GitHub Actions ───→│
                      │                     ├─ production обновлён
```

#### 3.5 Версионирование (Semantic Versioning)

```
v MAJOR . MINOR . PATCH
  │       │       │
  │       │       └── Исправления багов (1.0.1, 1.0.2)
  │       └────────── Новые фичи, обратно совместимые (1.1.0, 1.2.0)
  └────────────────── Ломающие изменения (2.0.0)
```

**Примеры:**
- `v0.1.0` — первая рабочая версия (MVP)
- `v0.2.0` — добавлена авторизация
- `v0.2.1` — исправлен баг в авторизации
- `v1.0.0` — первый стабильный релиз

---

### 4. Организация работы команды

#### 4.1 Текущая команда (2 человека)

| Роль | Кто | Обязанности |
|------|-----|-------------|
| **Владелец/Аналитик** | Человек | Постановка задач, приёмка, архитектурные решения |
| **Разработчик** | Claude Code | Написание кода, code review, документация |

#### 4.2 Процесс работы (Human + AI)

```
1. ПОСТАНОВКА ЗАДАЧИ
   └─ Человек создаёт Issue в GitHub
   └─ Описывает что нужно сделать
   └─ Labels: type:feature, priority:high

2. РАЗРАБОТКА (Claude Code)
   └─ Claude читает Issue
   └─ Создаёт ветку feature/123-...
   └─ Разрабатывает локально (make dev)
   └─ Тестирует
   └─ Создаёт PR

3. REVIEW
   └─ Pre-commit проверки автоматически
   └─ Человек смотрит PR (или доверяет Claude)
   └─ При необходимости — правки

4. MERGE
   └─ Squash merge в main
   └─ Issue закрывается автоматически

5. RELEASE (по решению человека)
   └─ Человек: "Делаем релиз"
   └─ Claude: gh release create v1.0.0
   └─ Деплой на production
```

#### 4.3 Масштабирование до 10 человек

Шаблон готов к росту команды. При добавлении разработчиков:

| Что добавить | Зачем |
|--------------|-------|
| **Branch Protection** | Require 1-2 approvals |
| **CODEOWNERS** | Автоматическое назначение reviewers по областям |
| **Milestones** | Спринты для планирования |
| **Project Board** | Kanban для визуализации |

**Пример CODEOWNERS для команды:**
```
# .github/CODEOWNERS
* @owner

/src/backend/     @backend-team
/src/frontend/    @frontend-team
/platform/        @devops
/.claude/         @owner
```

#### 4.4 Что настроить сейчас

**1. Labels (система меток):**
```bash
# Тип задачи
gh label create "type:bug" --description "Баг" --color d73a4a
gh label create "type:feature" --description "Новая функциональность" --color a2eeef
gh label create "type:task" --description "Техническая задача" --color 0075ca
gh label create "type:docs" --description "Документация" --color 0e8a16

# Приоритет
gh label create "priority:high" --description "Высокий приоритет" --color FF0000
gh label create "priority:medium" --description "Средний приоритет" --color FFA500
gh label create "priority:low" --description "Низкий приоритет" --color 008000
```

**2. Issue Templates:**
- `bug.yml` — баг-репорт
- `feature.yml` — запрос фичи
- `task.yml` — техническая задача

**3. PR Template:**
- Summary (что сделано)
- Related Issue (ссылка на #123)
- How to test (как проверить)

**4. Branch Protection (опционально сейчас):**
- Require PR before merge
- Require status checks (pre-commit)

---

### 5. Что должно быть в .github/

#### 5.1 Структура .github/

```
.github/
│
├── .instructions/                    # Инструкции (см. 5.2)
│
├── ISSUE_TEMPLATE/                   # Шаблоны Issues
│   ├── bug.yml                       #   Баг-репорт (форма)
│   ├── feature.yml                   #   Запрос фичи (форма)
│   ├── task.yml                      #   Техническая задача (форма)
│   └── config.yml                    #   Конфигурация chooser
│
├── workflows/                        # GitHub Actions
│   ├── ci.yml                        #   Continuous Integration (опционально)
│   └── deploy.yml                    #   Деплой по Release
│
├── PULL_REQUEST_TEMPLATE.md          # Шаблон PR
├── CODEOWNERS                        # Ответственные за код (при росте команды)
└── README.md                         # Описание .github/
```

#### 5.2 Структура .github/.instructions/

```
.github/.instructions/
│
├── README.md                         # Индекс всех инструкций
├── standard-github.md                # Общий стандарт работы с GitHub
├── standard-development-workflow.md  # Процесс: Issue → PR → Merge → Release
├── standard-release-workflow.md      # Процесс релизов
│
├── .scripts/                         # ВСЕ скрипты
│   ├── setup-labels.py               #   Создание системы меток
│   ├── validate-issue-template.py    #   Валидация шаблонов Issues
│   └── validate-workflow.py          #   Валидация workflows
│
├── issues/                           # Объект: Issue
│   ├── README.md                     #   Индекс папки
│   ├── standard-issue.md             #   Что такое Issue, свойства, CLI
│   ├── validation-issue.md           #   Как проверить шаблон
│   ├── create-issue.md               #   Как создать Issue/шаблон
│   └── modify-issue.md               #   Как изменить Issue/шаблон
│
├── pull-requests/                    # Объект: Pull Request
│   ├── README.md
│   ├── standard-pull-request.md
│   ├── validation-pull-request.md
│   ├── create-pull-request.md
│   └── modify-pull-request.md
│
├── labels/                           # Объект: Label
│   ├── README.md
│   ├── standard-label.md
│   ├── validation-label.md
│   ├── create-label.md
│   └── modify-label.md
│
├── milestones/                       # Объект: Milestone
│   ├── README.md
│   ├── standard-milestone.md
│   ├── validation-milestone.md
│   ├── create-milestone.md
│   └── modify-milestone.md
│
├── releases/                         # Объект: Release
│   ├── README.md
│   ├── standard-release.md
│   ├── validation-release.md
│   ├── create-release.md
│   └── modify-release.md
│
├── workflows/                        # Объект: GitHub Actions
│   ├── README.md
│   ├── standard-workflow.md
│   ├── validation-workflow.md
│   ├── create-workflow.md
│   └── modify-workflow.md
│
└── projects/                         # Объект: Project (Kanban)
    ├── README.md
    ├── standard-project.md
    ├── validation-project.md
    ├── create-project.md
    └── modify-project.md
```

#### 5.3 Зачем каждый элемент

**Файлы .github/ (GitHub требует именно тут):**

| Файл | Зачем | Для кого |
|------|-------|----------|
| `ISSUE_TEMPLATE/*.yml` | Стандартизация создания задач | Все разработчики |
| `PULL_REQUEST_TEMPLATE.md` | Стандартизация описания PR | Все разработчики |
| `CODEOWNERS` | Автоматическое назначение reviewers | GitHub (автоматика) |
| `workflows/*.yml` | CI/CD — тесты, деплой | GitHub Actions |

**Инструкции .github/.instructions/:**

| Папка/Файл | Зачем |
|------------|-------|
| `standard-github.md` | Общие правила работы с GitHub в проекте |
| `workflow-development.md` | Полный цикл разработки |
| `workflow-release.md` | Как делать релизы |
| `issues/` | Всё про Issues: что это, как создавать шаблоны |
| `pull-requests/` | Всё про PR: что это, как оформлять |
| `labels/` | Система меток проекта |
| `milestones/` | Вехи и спринты |
| `releases/` | Версионирование, changelog |
| `workflows/` | GitHub Actions — как писать CI/CD |
| `projects/` | Канбан-доски |

#### 5.4 Связь с другими папками проекта

| Что | Где | Почему там |
|-----|-----|------------|
| Скрипты деплоя | `platform/scripts/` | Инфраструктура — ответственность platform/ |
| Docker для CI | `platform/docker/` | Там Docker-конфигурации |
| Процесс разработки | `.github/.instructions/` | Специфика GitHub |
| Тесты для CI | `tests/` | Там все тесты |

**Пример связи:**

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    steps:
      - run: ./platform/scripts/deploy.sh  # Скрипт из platform/
```

---

### 6. Необходимые инструкции

#### 6.1 Корневые инструкции

| Файл | Тип | Описание |
|------|-----|----------|
| `standard-github.md` | standard | Общие правила работы с GitHub |
| `standard-development-workflow.md` | standard | Процесс: Issue → PR → Merge → Release |
| `standard-release-workflow.md` | standard | Как делать релизы |

#### 6.2 Инструкции по объектам

Каждый объект GitHub имеет полный набор инструкций:

| Объект | standard | validation | create | modify |
|--------|----------|------------|--------|--------|
| **Issue** | Свойства, CLI | Проверка шаблонов | Создание Issue/шаблона | Изменение |
| **Pull Request** | Свойства, CLI | Проверка template | Создание PR | Изменение |
| **Label** | Система меток | Проверка именования | Создание метки | Изменение |
| **Milestone** | Вехи, спринты | — | Создание вехи | Изменение |
| **Release** | Версионирование | Проверка semver | Создание релиза | Изменение |
| **Workflow** | GitHub Actions | Проверка YAML | Создание workflow | Изменение |
| **Project** | Канбан-доски | — | Создание доски | Изменение |

#### 6.3 Скиллы Claude

| Скилл | Описание | Инструкция |
|-------|----------|------------|
| `/issue-create` | Создать Issue | `issues/create-issue.md` |
| `/pr-create` | Создать PR | `pull-requests/create-pull-request.md` |
| `/release-create` | Создать релиз | `releases/create-release.md` |
| `/labels-setup` | Настроить метки | `labels/create-label.md` |
| `/milestone-create` | Создать веху | `milestones/create-milestone.md` |

#### 6.4 Порядок создания инструкций

По стандарту `.instructions/standard-instruction.md`:

```
standard → validation → create → modify
```

**Рекомендуемый порядок объектов:**

1. **labels/** — базовая категоризация
2. **issues/** — задачи используют labels
3. **pull-requests/** — PR связаны с issues
4. **milestones/** — группировка issues
5. **releases/** — версионирование
6. **workflows/** — CI/CD
7. **projects/** — канбан (опционально)

---

## Решения

1. **Команда:** 2 человека (Человек + Claude Code), готово к масштабированию до 10
2. **Окружения:** local + production (без staging)
3. **Модель ветвления:** Упрощённый Git Flow (main + feature branches)
4. **Деплой:** По Release (не по merge в main)
5. **Версионирование:** Semantic Versioning (v1.0.0)
6. **Issue Templates:** YAML формы (bug, feature, task)
7. **Labels:** Система type + priority
8. **Branch Protection:** Опционально сейчас, обязательно при росте команды
9. **CODEOWNERS:** Добавить при росте команды
10. **Агент-ревьюер:** Планируется (Claude автоматически ревьюит PR)

---

## Открытые вопросы

1. **CI в GitHub Actions:**
   - Нужен ли CI помимо pre-commit?
   - Какие тесты запускать на PR? (pre-commit уже есть локально)

2. **Production:**
   - Где будет хоститься? (VPS, Cloud, etc.)
   - Docker Registry?

3. **Агент-ревьюер:**
   - Как запускать? (вручную, по расписанию, на событие PR)
   - Какие проверки делать?

4. **Changelog:**
   - Автоматический (`--generate-notes`) или вручную?

---

## Ссылки

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [About issue and PR templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [About branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
