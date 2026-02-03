# GitHub Platform Research

Исследование возможностей GitHub как платформы и определение инструкций для `.github/`.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Объекты GitHub](#1-объекты-github)
  - [2. Детальное описание объектов](#2-детальное-описание-объектов)
  - [3. Релизный цикл и ветвление](#3-релизный-цикл-и-ветвление)
  - [4. Организация работы команды](#4-организация-работы-команды)
  - [5. Структура .github/](#5-структура-github)
    - [5.1 Принцип: три категории](#51-принцип-три-категории-в-github)
    - [5.2 Полная структура .github/](#52-полная-структура-github)
    - [5.3 Разделение: что где](#53-разделение-что-где)
    - [5.4 Связи между компонентами](#54-связи-между-компонентами)
    - [5.5 Что НЕ входит в .github/](#55-что-не-входит-в-github)
  - [6. Порядок создания](#6-порядок-создания)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [План создания документации .github/](#план-создания-документации-github)
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

### 5. Структура .github/

#### 5.1 Принцип: три категории в .github/

```
.github/
│
│   # ─── Файлы и папки GitHub (GitHub требует/распознаёт) ───
│
├── ISSUE_TEMPLATE/                # GitHub показывает при создании Issue
├── workflows/                     # GitHub запускает Actions
├── PULL_REQUEST_TEMPLATE.md       # GitHub подставляет при создании PR
├── CODEOWNERS                     # GitHub назначает reviewers
│
│   # ─── Наши инструкции (GitHub игнорирует) ───
│
├── .instructions/                 # Документация "как работать"
│
│   # ─── Наши справочники (GitHub игнорирует) ───
│
├── labels/                        # Словарь меток для этого репо
│
└── README.md                      # Описание папки
```

**Три категории (всё на одном уровне):**
1. **Файлы GitHub** — строго определённые пути, GitHub их использует
2. **Инструкции** — документация "как работать", для LLM/разработчиков
3. **Справочники** — конфигурация специфичная для этого репо (labels, etc.)

**Принцип связи:**

Если в `.instructions/` есть папка — она регламентирует соответствующую папку/файл в `.github/`:

| Инструкции | Регламентирует | Тип |
|------------|----------------|-----|
| `.instructions/issue-templates/` | `.github/ISSUE_TEMPLATE/` | Файлы репо |
| `.instructions/pr-template/` | `.github/PULL_REQUEST_TEMPLATE.md` | Файл репо |
| `.instructions/workflows-files/` | `.github/workflows/` | Файлы репо |
| `.instructions/codeowners/` | `.github/CODEOWNERS` | Файл репо |
| `.instructions/labels/` | `.github/labels/` | Справочник |
| `.instructions/milestones/` | `.github/milestones/` + **GitHub** | Справочник + Объект |
| `.instructions/releases/` | `.github/releases/` + **GitHub** | Справочник + Объект |
| `.instructions/issues/` | **GitHub** (не папка!) | Объект GitHub |
| `.instructions/pull-requests/` | **GitHub** (не папка!) | Объект GitHub |
| `.instructions/projects/` | **GitHub** (не папка!) | Объект GitHub |

**Ключевое:**
- Инструкции для **файлов** → регламентируют папки/файлы в `.github/`
- Инструкции для **объектов GitHub** → регламентируют сущности в GitHub (через CLI)

---

#### 5.2 Полная структура .github/

```
.github/
│
│   # ═══════════════════════════════════════════════════════════════════
│   # ФАЙЛЫ И ПАПКИ GITHUB (GitHub требует именно эти пути)
│   # ═══════════════════════════════════════════════════════════════════
│
├── ISSUE_TEMPLATE/                        # Шаблоны Issues
│   │                                      # ← Регламентирует: .instructions/issue-templates/
│   ├── bug.yml                            #   Баг-репорт (YAML форма)
│   ├── feature.yml                        #   Запрос фичи (YAML форма)
│   ├── task.yml                           #   Техническая задача (YAML форма)
│   └── config.yml                         #   Конфигурация chooser
│
├── workflows/                             # GitHub Actions
│   │                                      # ← Регламентирует: .instructions/workflows-files/
│   ├── ci.yml                             #   CI — тесты, линтинг (опционально)
│   └── deploy.yml                         #   Деплой на production по Release
│
├── PULL_REQUEST_TEMPLATE.md               # Шаблон PR (Markdown)
│                                          # ← Регламентирует: .instructions/pr-template/
│
├── CODEOWNERS                             # Авто-назначение reviewers
│                                          # ← Регламентирует: .instructions/codeowners/
│
│   # ═══════════════════════════════════════════════════════════════════
│   # НАШИ СПРАВОЧНИКИ (GitHub игнорирует, для этого репозитория)
│   # Создаются по инструкциям из .instructions/
│   # ═══════════════════════════════════════════════════════════════════
│
├── labels/                                # Справочник меток
│   │                                      # ← Регламентирует: .instructions/labels/
│   ├── README.md                          #   Описание системы меток проекта
│   └── labels.yml                         #   КОНФИГ: все метки (синхр. → GitHub)
│
├── milestones/                            # Справочник milestones (опционально)
│   │                                      # ← Регламентирует: .instructions/milestones/
│   ├── README.md                          #   Описание системы milestones
│   └── milestones.yml                     #   КОНФИГ: текущие milestones
│
├── releases/                              # История релизов (опционально)
│   │                                      # ← Регламентирует: .instructions/releases/
│   ├── README.md                          #   Описание процесса релизов
│   └── CHANGELOG.md                       #   История версий
│
│   # ═══════════════════════════════════════════════════════════════════
│   # НАШИ ИНСТРУКЦИИ (GitHub игнорирует)
│   # ═══════════════════════════════════════════════════════════════════
│
├── .instructions/                         # Инструкции для LLM/разработчиков
│   │
│   ├── README.md                          # Индекс всех инструкций
│   │
│   │   # ─── Процессные документы (без validation/create/modify) ───
│   │
│   ├── standard-github.md                 # Общие правила работы с GitHub
│   ├── standard-development-workflow.md   # Цикл: Issue → Branch → PR → Merge
│   ├── standard-release-workflow.md       # Процесс релизов
│   │
│   │   # ─── Скрипты автоматизации ───
│   │
│   ├── .scripts/
│   │   ├── setup-labels.py                #   labels.yml → GitHub
│   │   ├── validate-issue-template.py     #   Валидация ISSUE_TEMPLATE/*.yml
│   │   ├── validate-pr-template.py        #   Валидация PULL_REQUEST_TEMPLATE.md
│   │   └── validate-workflow.py           #   Валидация workflows/*.yml
│   │
│   │   # ─── Инструкции для ФАЙЛОВ в .github/ ───
│   │
│   ├── issue-templates/                   # → Регламентирует: ISSUE_TEMPLATE/
│   │   ├── README.md
│   │   ├── standard-issue-template.md     #   Формат YAML, обязательные поля
│   │   ├── validation-issue-template.md   #   Проверка синтаксиса
│   │   ├── create-issue-template.md       #   Воркфлоу создания шаблона
│   │   └── modify-issue-template.md       #   Редактирование, деактивация
│   │
│   ├── pr-template/                       # → Регламентирует: PULL_REQUEST_TEMPLATE.md
│   │   ├── README.md
│   │   ├── standard-pr-template.md        #   Структура MD, секции
│   │   ├── validation-pr-template.md      #   Проверка структуры
│   │   └── modify-pr-template.md          #   Редактирование
│   │
│   ├── workflows-files/                   # → Регламентирует: workflows/
│   │   ├── README.md
│   │   ├── standard-workflow-file.md      #   Структура YAML, триггеры, jobs
│   │   ├── validation-workflow-file.md    #   Проверка синтаксиса
│   │   ├── create-workflow-file.md        #   Воркфлоу создания
│   │   └── modify-workflow-file.md        #   Редактирование
│   │
│   ├── codeowners/                        # → Регламентирует: CODEOWNERS
│   │   ├── README.md
│   │   ├── standard-codeowners.md         #   Синтаксис, паттерны
│   │   └── modify-codeowners.md           #   Добавление правил
│   │
│   │   # ─── Инструкции для СПРАВОЧНИКОВ в .github/ ───
│   │
│   ├── labels/                            # → Регламентирует: labels/
│   │   ├── README.md
│   │   ├── standard-labels.md             #   Категории, именование, цвета
│   │   ├── create-label.md                #   Добавление метки
│   │   └── modify-label.md                #   Изменение, удаление
│   │
│   │   # ─── Инструкции для ОБЪЕКТОВ GITHUB (живут в GitHub, не в папке) ───
│   │
│   ├── issues/                            # → Регламентирует: GitHub Issues
│   │   ├── README.md
│   │   ├── standard-issue.md              #   Свойства Issue, CLI команды
│   │   ├── validation-issue.md            #   Чек-лист перед закрытием
│   │   ├── create-issue.md                #   Воркфлоу создания Issue
│   │   └── modify-issue.md                #   Редактирование, labels, закрытие
│   │
│   ├── pull-requests/                     # → Регламентирует: GitHub Pull Requests
│   │   ├── README.md
│   │   ├── standard-pull-request.md       #   Свойства PR, CLI команды
│   │   ├── validation-pull-request.md     #   Чек-лист перед мержем
│   │   ├── create-pull-request.md         #   Воркфлоу создания PR
│   │   └── modify-pull-request.md         #   Ревью, мерж, редактирование
│   │
│   ├── releases/                          # → Регламентирует: GitHub Releases
│   │   ├── README.md
│   │   ├── standard-release.md            #   Semver, changelog, теги
│   │   ├── validation-release.md          #   Проверка перед релизом
│   │   ├── create-release.md              #   Воркфлоу создания релиза
│   │   └── modify-release.md              #   Редактирование, hotfix
│   │
│   ├── milestones/                        # → Регламентирует: GitHub Milestones
│   │   ├── README.md
│   │   ├── standard-milestone.md          #   Свойства, типы (Sprint, Release)
│   │   ├── create-milestone.md            #   Воркфлоу создания
│   │   └── modify-milestone.md            #   Продление, закрытие
│   │
│   └── projects/                          # → Регламентирует: GitHub Projects
│       ├── README.md
│       ├── standard-project.md            #   Views, поля, автоматизация
│       ├── create-project.md              #   Воркфлоу создания
│       └── modify-project.md              #   Настройка, архивация
│
└── README.md                              # Описание папки .github/
```

---

#### 5.3 Разделение: что где

| Тип | Где хранится | Где инструкции | Пример |
|-----|--------------|----------------|--------|
| **Объект GitHub** | В GitHub | `.instructions/issues/` | Issue #123 |
| **Файл шаблона** | `.github/ISSUE_TEMPLATE/` | `.instructions/issue-templates/` | `bug.yml` |
| **Справочник labels** | `.github/labels/` | `.instructions/labels/` | `labels.yml` |
| **Справочник milestones** | `.github/milestones/` | `.instructions/milestones/` | `milestones.yml` |
| **Справочник releases** | `.github/releases/` | `.instructions/releases/` | `CHANGELOG.md` |
| **Workflow файл** | `.github/workflows/` | `.instructions/workflows-files/` | `ci.yml` |

**Ключевое:**
- Файлы GitHub (ISSUE_TEMPLATE/, workflows/) — в корне `.github/`
- Инструкции как с ними работать — в `.github/.instructions/`
- Справочники — в отдельных папках `.github/labels/`, `.github/milestones/`, `.github/releases/`

---

#### 5.4 Связи между компонентами

```
┌─────────────────────────────────────────────────────────────────────┐
│                              .github/                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  labels/labels.yml          .instructions/issues/create-issue.md   │
│  ┌──────────────┐           ┌──────────────┐                        │
│  │ type:bug     │ ←──────── │ "Выбрать     │                        │
│  │ type:feature │           │  метки из    │                        │
│  │ priority:... │           │  labels.yml" │                        │
│  └──────────────┘           └──────────────┘                        │
│         │                                                           │
│         ↓ setup-labels.py                                           │
│  ┌──────────────┐                                                   │
│  │   GitHub     │  (метки синхронизируются в GitHub)                │
│  │   Labels     │                                                   │
│  └──────────────┘                                                   │
│                                                                     │
│  ISSUE_TEMPLATE/bug.yml     .instructions/issue-templates/          │
│  ┌──────────────┐           ┌──────────────┐                        │
│  │ name: Bug    │ ←──────── │ standard-    │  "Как писать          │
│  │ description: │           │ issue-       │   YAML шаблон"         │
│  │ body: ...    │           │ template.md  │                        │
│  └──────────────┘           └──────────────┘                        │
│         │                                                           │
│         ↓ GitHub использует                                         │
│  ┌──────────────┐           .instructions/issues/                   │
│  │  Новый Issue │ ←──────── ┌──────────────┐                        │
│  │  (в GitHub)  │           │ create-      │  "Как создать Issue"   │
│  └──────────────┘           │ issue.md     │                        │
│                             └──────────────┘                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

#### 5.5 Что НЕ входит в .github/

| Что | Где должно быть | Почему |
|-----|-----------------|--------|
| Скрипты деплоя | `platform/scripts/` | Инфраструктура |
| Docker для CI | `platform/docker/` | Инфраструктура |
| Тесты | `tests/` | Код тестов |
| Конфиги окружений | `config/` | Не GitHub-специфично |

---

### 6. Порядок создания

> **Примечание:** Полная структура и зоны ответственности описаны в разделе 5.

#### 6.1 Скиллы Claude

**Статус:** Преждевременно планировать.

Скиллы создаются через `/skill-create` ПОСЛЕ создания соответствующих инструкций. Порядок:
1. Создать инструкцию (standard → validation → create → modify)
2. Вызвать `/skill-create` для инструкции
3. Скилл автоматически связывается с инструкцией

**Принцип:** Сначала инструкции, потом скиллы. Не наоборот.

#### 6.2 Порядок создания инструкций

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
7. **Labels:** Создать собственную систему (удалить дефолтные)
8. **Branch Protection:** Опционально сейчас, обязательно при росте команды
9. **CODEOWNERS:** Добавить при росте команды
10. **Агент-ревьюер:** Планируется (Claude автоматически ревьюит PR)

---

## Открытые вопросы

### 1. CI в GitHub Actions

**Вопрос:** Нужен ли CI помимо pre-commit?

**Решение:** Пока НЕТ. Pre-commit хуки запускаются локально и на коммит. Этого достаточно для текущей команды (2 человека). CI добавим когда:
- Команда вырастет (нужна проверка на сервере, т.к. не все запускают pre-commit)
- Появятся тяжёлые тесты (e2e, integration), которые долго запускать локально

**Действие:** Отложить. Вернуться при масштабировании команды.

---

### 2. Production и Platform

**Вопросы:**
- Где будет хоститься? (VPS, Cloud, etc.)
- Docker Registry?
- Нужна ли папка `platform/` вообще?

**Решение:** Это вопрос для `platform/`, не для `.github/`. Папка `platform/` нужна для:
- Docker-конфигураций
- Kubernetes манифестов
- Скриптов деплоя
- Конфигурации мониторинга

**Действие:** Создать отдельный черновик для `platform/` когда дойдём до деплоя.

---

### 3. Агент-ревьюер

**Вопросы:**
- Как запускать?
- Какие проверки делать?

**Решение:** Отложить. Агент будет использовать:
- Скиллы из `.github/.instructions/` (когда будут созданы)
- Скрипты валидации
- Существующие инструкции

**Действие:** Вернуться после создания базовых инструкций.

---

### 4. Changelog

**Вопрос:** Автоматический (`--generate-notes`) или вручную?

**Решение:** Автоматический через `gh release create --generate-notes`.

**Открытые подвопросы:**
- Где хранить CHANGELOG.md? (корень репо или releases/)
- Нужно ли добавить в pre-commit проверку формата?
- Где писать инструкции? (в `.github/.instructions/releases/` или отдельно)

**Действие:** Проработать при создании `releases/` инструкций.

---

### 5. Labels (система меток)

**Текущее состояние:** В репозитории стандартные метки GitHub (9 штук).

**Решение:** Удалить стандартные, создать собственную систему с префиксами.

**План действий:**
1. Удалить все стандартные метки
2. Создать собственную систему:
   - `type:` — тип задачи (bug, feature, task, docs, refactor)
   - `priority:` — приоритет (critical, high, medium, low)
   - `area:` — область кода (backend, frontend, infra, api)
   - `status:` — статус (blocked, in-review, ready)
3. Добавить `setup-labels.py` в `.structure/initialization.md`

**Действие:** Выполнить после согласования системы меток.

---

## План создания документации .github/

> **Статус:** В процессе выполнения

### Этап 1: Создание папок

Через `/structure-create` создать папки (последовательно):

**Основные папки .github/:**
1. `.github/.instructions/` — корень инструкций
2. `.github/labels/` — справочник меток
3. `.github/milestones/` — справочник milestones
4. `.github/releases/` — история релизов

**Папки инструкций (внутри .instructions/):**
5. `.github/.instructions/.scripts/` — скрипты автоматизации
6. `.github/.instructions/issue-templates/` — инструкции для ISSUE_TEMPLATE/
7. `.github/.instructions/pr-template/` — инструкции для PR template
8. `.github/.instructions/workflows-files/` — инструкции для workflows/
9. `.github/.instructions/codeowners/` — инструкции для CODEOWNERS
10. `.github/.instructions/labels/` — инструкции для labels/
11. `.github/.instructions/issues/` — инструкции для GitHub Issues
12. `.github/.instructions/pull-requests/` — инструкции для GitHub PR
13. `.github/.instructions/releases/` — инструкции для GitHub Releases
14. `.github/.instructions/milestones/` — инструкции для GitHub Milestones
15. `.github/.instructions/projects/` — инструкции для GitHub Projects

---

### Этап 2: Создание стандартов (по волнам)

Создание инструкций через `/instruction-create` с валидацией captain-holt.

**Требования к агентам (Amy Santiago):**
- Прочитать этот черновик ПЕРЕД созданием
- Использовать ТОЛЬКО `/instruction-create`
- Создавать ТОЛЬКО standard-* (не validation, create, modify)
- Не выходить за рамки своей зоны ответственности
- **В процессе создания** — вызвать captain-holt для семантического анализа

**Интеграция с captain-holt:**
Amy ДОЛЖНА вызвать captain-holt через Task tool со следующим промптом:
```
Проанализируй стандарт: {путь_к_созданному_стандарту}

Контекст: прочитай черновик .claude/drafts/2026-02-03-github-platform-research.md
для понимания общей картины, но анализируй ТОЛЬКО указанный стандарт.

Верни P1-проблемы (если есть) и рекомендации.
```
Amy исправляет P1-проблемы по рекомендациям captain-holt до завершения задачи.

**Волна 1 — Базовые (без зависимостей):**

| # | Путь | Зона ответственности |
|---|------|---------------------|
| 1 | `.instructions/labels/standard-labels.md` | Система меток (управление метками) |
| 2 | `.instructions/codeowners/standard-codeowners.md` | Синтаксис CODEOWNERS |

**Волна 2 — Зависят от labels:**

| # | Путь | Зависит от |
|---|------|------------|
| 3 | `.instructions/issues/standard-issue.md` | labels |
| 4 | `.instructions/pull-requests/standard-pull-request.md` | labels |
| 5 | `.instructions/issue-templates/standard-issue-template.md` | labels |
| 6 | `.instructions/pr-template/standard-pr-template.md` | pull-request |

**Волна 3 — Зависят от issues/PR:**

| # | Путь | Зависит от |
|---|------|------------|
| 7 | `.instructions/milestones/standard-milestone.md` | issues |
| 8 | `.instructions/standard-development-workflow.md` | issues, PR |

**Волна 4 — Зависят от workflow:**

| # | Путь | Зависит от |
|---|------|------------|
| 9 | `.instructions/releases/standard-release.md` | milestones, PR |
| 10 | `.instructions/standard-release-workflow.md` | release, dev-workflow |
| 11 | `.instructions/workflows-files/standard-workflow-file.md` | dev-workflow |

**Волна 5 — Projects:**

| # | Путь | Зависит от |
|---|------|------------|
| 12 | `.instructions/projects/standard-project.md` | всё (канбан объединяет) |

**Волна 6 — Финальная (обобщающий стандарт):**

| # | Путь | Зависит от |
|---|------|------------|
| 13 | `.instructions/standard-github.md` | ВСЕ предыдущие стандарты (обобщает naming, workflow, review, merge после уточнения всех сущностей) |

---

### Прогресс

**Этап 1: Создание папок**
- [x] Основные папки .github/ (4/4)
- [x] Папки инструкций (11/11)

**Этап 2: Создание стандартов**
- [x] Волна 1: Базовые (2/2 завершено)
- [x] Волна 2: Labels-зависимые (4/4 завершено)
- [x] Волна 3: Issues/PR-зависимые (2/2 завершено)
- [x] Волна 4: Workflow-зависимые (3/3 завершено)
- [x] Волна 5: Projects (1/1 завершено)
- [x] Волна 6: Обобщающий standard-github.md (1/1 завершено)

**Статус: ВЫПОЛНЕНО** — все стандарты созданы и прошли семантический анализ captain-holt (P1/P2 исправления применены)

---

## Ссылки

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [About issue and PR templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [About branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
