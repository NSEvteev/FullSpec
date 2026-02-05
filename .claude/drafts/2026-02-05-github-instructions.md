# GitHub-инструкции: реструктуризация и валидация

Объединённый черновик: архитектура `.github/.instructions/`, смысловая валидация стандартов, результаты и рекомендации.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Архитектура](#архитектура)
  - [История реструктуризации](#история-реструктуризации)
  - [Смысловая валидация](#смысловая-валидация)
  - [Зональный анализ](#зональный-анализ)
  - [Рекомендации](#рекомендации)
  - [Принятые решения](#принятые-решения)
  - [TODO](#todo)
  - [Файлы рекомендаций](#файлы-рекомендаций)

---

## Контекст

**Задача:** Реструктуризация и валидация документации `.github/.instructions/`.

**Почему:** Исходное распределение контента не соответствовало логике разделения ответственности. Дублирование между стандартами, размытые границы, отсутствие единого workflow.

**Источники:** Объединяет 3 черновика:
- `2026-02-03-github-instructions-validation.md` — план и чек-лист валидации
- `2026-02-03-github-instructions-validation-results.md` — итоги валидации (оценки, паттерны)
- `2026-02-04-github-docs-restructure.md` — архитектура, операции, решения

**Статус:** Реструктуризация ВЫПОЛНЕНА (Фаза 1-8, 2026-02-04/05). Зональный анализ ВЫПОЛНЕН (Фаза 7 + development). Валидация: Волна 1 частично (1-4 ✅, 5-8 структурная ✅, семантическая ⏳), Волны 2-4 ожидают.

---

## Содержание

### Архитектура

#### Дерево файлов

```
.github/.instructions/
│
├── standard-github-workflow.md        ← HIGH-LEVEL оркестратор: ссылки на этапы
│
├── [НЕЗАВИСИМЫЕ]
│   ├── codeowners/
│   │   ├── README.md
│   │   ├── standard-codeowners.md
│   │   └── validation-codeowners.md
│   ├── labels/
│   │   ├── README.md
│   │   ├── standard-labels.md
│   │   ├── modify-labels.md
│   │   └── validation-labels.md
│   ├── milestones/
│   │   ├── README.md
│   │   └── standard-milestone.md
│   └── projects/
│       ├── README.md
│       └── standard-project.md
│
├── [ЭТАПЫ ЖИЗНЕННОГО ЦИКЛА]                  (порядок = стадии workflow)
│   ├── issues/                        ← стадия 1: планирование
│   │   ├── README.md
│   │   ├── standard-issue.md
│   │   └── issue-templates/
│   │       ├── README.md
│   │       ├── standard-issue-template.md
│   │       └── validation-type-templates.md
│   │
│   ├── branches/                      ← стадия 3: создание ветки
│   │   ├── README.md
│   │   └── standard-branching.md
│   │
│   ├── development/                   ← стадия 4: разработка
│   │   ├── README.md
│   │   └── standard-development.md
│   │
│   ├── commits/                       ← стадия 5: коммиты
│   │   ├── README.md
│   │   └── standard-commit.md
│   │
│   ├── pull-requests/                 ← стадия 6: создание PR
│   │   ├── README.md
│   │   ├── standard-pull-request.md
│   │   └── pr-template/
│   │       ├── README.md
│   │       ├── standard-pr-template.md
│   │       ├── standard-draft-pr.md
│   │       └── validation-pr-template.md
│   │
│   ├── review/                        ← стадия 7-8: ревью и merge
│   │   ├── README.md
│   │   └── standard-review.md
│   │
│   ├── sync/                          ← стадия 9: синхронизация
│   │   ├── README.md
│   │   └── standard-sync.md
│   │
│   └── releases/                      ← стадия 10: релиз
│       ├── README.md
│       ├── standard-release.md
│       └── standard-release-workflow.md
│
├── [АВТОМАТИЗАЦИЯ]
│   ├── actions/
│   │   ├── README.md
│   │   └── security/
│   │       └── README.md
│   └── workflows-files/
│       ├── README.md
│       └── standard-workflow-file.md
│
└── [СЛУЖЕБНЫЕ]
    └── .scripts/
        └── *.py
```

#### Ответственности документов

| Документ | Отвечает за |
|----------|-------------|
| **standard-github-workflow.md** | HIGH-LEVEL оркестратор: Фаза 0 + цикл 10 стадий, SSOT-ссылки |
| **branches/standard-branching.md** | Модель GitHub Flow, naming convention, жизненный цикл ветки, запреты, граничные случаи |
| **development/standard-development.md** | Процесс работы в feature-ветке, make-команды, тестирование, локальные проверки качества |
| **commits/standard-commit.md** | Conventional Commits, типы, scope, body/footer, правила оформления, процесс коммита, pre-commit hooks |
| **sync/standard-sync.md** | Триггеры синхронизации, процесс (main и feature-ветки), разрешение конфликтов, запреты |
| **issues/standard-issue.md** | Жизненный цикл Issues |
| **issues/issue-templates/standard-issue-template.md** | YAML-шаблоны Issues |
| **pull-requests/standard-pull-request.md** | Создание PR, связь с Issues, Draft PR |
| **pull-requests/pr-template/standard-pr-template.md** | Шаблон body PR |
| **pull-requests/pr-template/standard-draft-pr.md** | Работа с черновиками PR |
| **review/standard-review.md** | Code Review, Merge стратегии, Branch Protection |
| **releases/standard-release.md** | SemVer, Git-теги, Changelog |
| **releases/standard-release-workflow.md** | Процесс релиза: подготовка → публикация → hotfix → rollback |
| **labels/standard-labels.md** | Naming convention, правила применения меток |
| **milestones/standard-milestone.md** | Типы milestone, жизненный цикл |
| **codeowners/standard-codeowners.md** | Синтаксис CODEOWNERS, автоназначение ревьюеров |
| **projects/standard-project.md** | Канбан-доски, views, fields, автоматизация |
| **workflows-files/standard-workflow-file.md** | Структура YAML, триггеры, jobs/steps, secrets |
| **actions/security/** | Dependabot, CodeQL, Secret Scanning |

---

### История реструктуризации

5 фаз выполнено за 2026-02-04/05:

| Фаза | Дата | Суть | Операции |
|------|------|------|----------|
| 1 | 2026-02-04 | Реструктуризация файлов | Переименование workflow, удаление github.md, перенос templates в подпапки, создание review/, releases/, actions/, projects/ |
| 2 | 2026-02-05 | Переконфигурация workflow | Зоны ответственности, Фаза 0, цикл 10 шагов, удаление дублирования с review/ → v1.1 |
| 3 | 2026-02-05 | Выделение git-конвенций | Создание branches/, commits/, sync/ из секций workflow → v1.2 |
| 4 | 2026-02-05 | Выравнивание секций 1:1 | 14 секций: §1 обзор, §2 Фаза 0, §3-§12 = Стадия 1-10, §13-§14 доп. → v1.3 |
| 5 | 2026-02-05 | Устранение дублирования | SSOT-ссылки вместо дублирования в §2, §6, §10, §13 → v1.4 |
| 6 | 2026-02-05 | Доработка git-конвенций | Создание v2 через `/instruction-create`, сравнение v1↔v2, объединение лучшего → v1.1 стандартов. Устранение пересечений зон с workflow, обновление зон ответственности |
| 7 | 2026-02-05 | Зональный анализ | Анализ 16 стандартов на пересечения зон, анализ 10 файлов рекомендаций на вторжения, анализ дерева папок. Найдено: 2 критичных пересечения, 22 вторжения рекомендаций |
| 8 | 2026-02-05 | Исправление дерева | [GIT-КОНВЕНЦИИ] объединены с [ЭТАПЫ ЖЦ], папки упорядочены по стадиям. projects/ → [НЕЗАВИСИМЫЕ]. Создан development/. Категория [ДОПОЛНИТЕЛЬНО] удалена → workflow v1.5 |

**Итог:** 50+ операций, все ссылки валидированы, workflow v1.5, стандарты branching/commit/sync v1.1.

---

### Смысловая валидация

#### Порядок валидации

Принцип: документ валидируется ПОСЛЕ его зависимостей.

##### Волна 1: Базовые стандарты (0-1 SSOT-ссылки)

| # | Файл | Статус |
|---|------|--------|
| 1 | `labels/standard-labels.md` | ✅ |
| 2 | `pull-requests/pr-template/standard-pr-template.md` | ✅ |
| 3 | `codeowners/standard-codeowners.md` | ✅ |
| 4 | `issues/issue-templates/standard-issue-template.md` | ✅ |
| 5 | `branches/standard-branching.md` | ✅ структурная / ⏳ семантическая |
| 6 | `commits/standard-commit.md` | ✅ структурная / ⏳ семантическая |
| 7 | `sync/standard-sync.md` | ✅ структурная / ⏳ семантическая |
| 8 | `development/standard-development.md` | ✅ структурная / ⏳ семантическая |

##### Волна 2: PR, Milestone, Release, Draft PR

| # | Файл | Зависит от | Статус |
|---|------|------------|--------|
| 9 | `pull-requests/standard-pull-request.md` | labels, pr-template | ⏳ |
| 10 | `milestones/standard-milestone.md` | ↔issue, ↔release | ⏳ |
| 11 | `releases/standard-release.md` | milestone, pull-request | ⏳ |
| 12 | `pull-requests/pr-template/standard-draft-pr.md` | pr-template | ⏳ *новый* |

##### Волна 3: Issue, Project, Review

| # | Файл | Зависит от | Статус |
|---|------|------------|--------|
| 13 | `issues/standard-issue.md` | labels, templates, PR, milestone | ⏳ |
| 14 | `projects/standard-project.md` | issue, pr, milestone | ⏳ |
| 15 | `review/standard-review.md` | pull-request | ⏳ *новый* |

##### Волна 4: Workflow-документы

| # | Файл | Зависит от | Статус |
|---|------|------------|--------|
| 16 | `standard-github-workflow.md` | issue, pr, review, labels | ⏳ |
| 17 | `releases/standard-release-workflow.md` | release, milestone, workflow | ⏳ |
| 18 | `workflows-files/standard-workflow-file.md` | workflow, release-workflow | ⏳ |

#### Оценки качества

| # | Стандарт | Качество | Полнота | Основные проблемы |
|---|----------|----------|---------|-------------------|
| 1 | labels/standard-labels.md | 8/10 | 7/10 | Нет критериев приоритетов, нет валидации |
| 2 | pr-template/standard-pr-template.md | 8/10 | 7/10 | Нет критериев выбора шаблона |
| 3 | codeowners/standard-codeowners.md | 9/10 | 8/10 | Нет процедуры добавления/удаления владельца |
| 4 | issue-templates/standard-issue-template.md | 9/10 | 8/10 | Нет объяснения зачем нужен id |
| 5 | branches/standard-branching.md | — | — | *Не валидировано* |
| 6 | commits/standard-commit.md | — | — | *Не валидировано* |
| 7 | sync/standard-sync.md | — | — | *Не валидировано* |
| 8 | pull-requests/standard-pull-request.md | 8/10 | 7/10 | Нет self-review, эскалации |
| 9 | milestones/standard-milestone.md | 8/10 | 7/10 | Нет автоматизации Sprint |
| 10 | releases/standard-release.md | 9/10 | 9/10 | Пересечение с release-workflow |
| 11 | pr-template/standard-draft-pr.md | — | — | *Не валидировано* |
| 12 | issues/standard-issue.md | 8/10 | 7/10 | Нет процедуры для stale Issues |
| 13 | projects/standard-project.md | 8/10 | 7/10 | Сложный item-edit без скрипта |
| 14 | review/standard-review.md | — | — | *Не валидировано* |
| 15 | standard-github-workflow.md | 9/10 | 8/10 | ~~Дублирование~~ → ВЫПОЛНЕНО (Фаза 5) |
| 16 | releases/standard-release-workflow.md | 8/10 | 8/10 | Нет release freeze процедуры |
| 17 | workflows-files/standard-workflow-file.md | 9/10 | 9/10 | Слишком большой (~1300 строк) |

#### Общие паттерны проблем

##### 1. Дублирование между документами — ВЫПОЛНЕНО

~~standard-github-workflow.md ↔ standard-issue.md ↔ standard-pull-request.md~~

Решено в Фазе 2-5: workflow содержит только SSOT-ссылки, детали — в специализированных стандартах.

##### 2. Пересечение standard-release.md и standard-release-workflow.md

**Проблема:** Оба документа описывают создание Release. Границы размыты.

**Рекомендация:** Чётко разделить:
- **standard-release.md:** ЧТО (свойства, формат, версионирование)
- **standard-release-workflow.md:** КОГДА и КАК (процесс, проверки)

##### 3. Отсутствие процедур для edge cases

**Примеры:** stale Issues, срыв сроков Milestone, эскалация review.

**Рекомендация:** Добавить секции "Граничные случаи" в каждый стандарт.

##### 4. Нет автоматизации для рутинных операций

**Примеры:** Sprint Milestone, валидация меток, определение версии по commits.

**Рекомендация:** Добавить скрипты или GitHub Actions.

---

### Зональный анализ

Дата: 2026-02-05. Проанализировано 16 standard-файлов + 12 файлов рекомендаций.

#### Проблемы дерева папок

| # | Проблема | Описание | Приоритет |
|---|----------|----------|-----------|
| Д1 | ~~Стадия 4 "Разработка" без папки/стандарта~~ | ✅ Создан `development/standard-development.md`, workflow §6 обновлён | ~~P0~~ |
| Д2 | ~~`projects/` в категории [ДОПОЛНИТЕЛЬНО]~~ | ✅ Перенесён в [НЕЗАВИСИМЫЕ], категория [ДОПОЛНИТЕЛЬНО] удалена | ~~P0~~ |
| Д3 | ~~Категории дерева vs стадии workflow~~ | ✅ [GIT-КОНВЕНЦИИ] объединены с [ЭТАПЫ ЖЦ]. Папки расположены по порядку стадий workflow (1→3→4→5→6→7-8→9→10) | ~~P2~~ |

#### Пересечения зон стандартов

Общая оценка: **7.5/10**. Хорошее разделение, 2 критичных пересечения.

##### Критичные пересечения (исправить)

| # | Проблема | Файлы | Решение |
|---|----------|-------|---------|
| З1 | **Правила меток дублируются в 3 местах** | `standard-labels.md`, `standard-issue.md §4`, `standard-pull-request.md §7` | Централизовать в `standard-labels.md`. В issue/PR оставить краткое правило + SSOT-ссылку |
| З2 | **TYPE-метка ↔ Issue Template — связь неявная** | `standard-labels.md §4`, `standard-issue-template.md §7` | Добавить явные двусторонние ссылки. В labels: "При добавлении type:* → создать Issue Template (→ standard-issue-template.md §7)". В templates: обратная ссылка |

##### Допустимые пересечения (оставить)

| # | Проблема | Файлы | Вердикт |
|---|----------|-------|---------|
| З3 | Merge стратегия упомянута в PR | `standard-pull-request.md §8`, `standard-review.md §3` | OK — summary-ссылка на SSOT |
| З4 | Workflow automation в нескольких | workflow, release-workflow | OK — разделение КОГДА vs КАК |

##### Hub-зависимости (стандарты, от которых зависят многие)

| Стандарт | Используется в | Кол-во зависимых |
|----------|----------------|-----------------|
| `standard-labels.md` | issue, PR, issue-template, branching, project, workflow | 6 |
| `standard-issue.md` | PR, review, milestone, project, branching | 5 |
| `standard-milestone.md` | release, release-workflow, project | 3 |

#### Вторжения рекомендаций в чужие зоны

Проанализировано 12 файлов рекомендаций. Найдено **30 вторжений** (8 P1, 10 P2, 4 P3 + 8 из development). ✅ Все вторжения удалены из файлов рекомендаций.

##### Файлы с наибольшим числом вторжений

| Файл рекомендаций | Целевой стандарт | Вторжений | Severity |
|-------------------|------------------|-----------|----------|
| `recommendations-standard-development-workflow.md` | workflow | 4 | P1 |
| `holt-analysis-standard-branching.md` | branching | 4 | P1-P2 |
| `recommendations-standard-milestone.md` | milestone | 3 | P2 |
| `recommendations-standard-release-workflow.md` | release-workflow | 2 | P1 |
| `holt-analysis-standard-commit.md` | commit | 3 | P2 |
| `recommendations-standard-issue.md` | issue | 2 | P2 |
| `holt-analysis-standard-sync.md` | sync | 2 | P2 |
| `recommendations-standard-project.md` | project | 2 | P2 |

##### Файлы БЕЗ вторжений

- `recommendations-standard-release.md` — 0
- `recommendations-standard-workflow-file.md` — 0

##### Самые "вторгаемые" зоны

| Зона (чья территория нарушается) | Кто вторгается | Кол-во |
|----------------------------------|----------------|--------|
| `standard-pull-request.md` | workflow, issue, commit, sync, branching | 5 |
| `standard-workflow-file.md` | workflow, milestone, release-workflow, project | 5 |
| `standard-release-workflow.md` | branching, commit, dev-workflow | 3 |
| `standard-labels.md` | branching, project, commit | 3 |
| `standard-project.md` | milestone, project, release | 3 |

##### Критичные вторжения (P1)

| # | Рекомендация | Из файла | Затрагивает зону | Решение |
|---|-------------|----------|------------------|---------|
| В1 | Разрешение конфликтов перед PR | dev-workflow | `sync.md §4` | Заменить на SSOT-ссылку |
| В2 | Draft PR integration в цикл | dev-workflow | `draft-pr.md` | Заменить на SSOT-ссылку |
| В3 | Co-authored-by формат | dev-workflow | `commit.md §4` | Заменить на SSOT-ссылку |
| В4 | Feature flags стратегия | dev-workflow | `release-workflow.md` | Переместить в release-workflow |
| В5 | Auto-rollback в deploy.yml (YAML) | release-workflow | `workflow-file.md` | Заменить на SSOT-ссылку |
| В6 | Notification webhook в Slack | release-workflow | `workflow-file.md` | Заменить на SSOT-ссылку |
| В7 | CI/CD для feature-веток | branching | `review.md §5` | Заменить на SSOT-ссылку |
| В8 | Hotfix для production | branching | `release-workflow.md` | Синхронизировать |

##### Корневые причины вторжений

1. **Нечёткие границы SSOT** (60%) — стандарты создавались независимо без явных boundary definitions
2. **Пробелы в workflow** (25%) — рекомендации пытаются заполнить недокументированные сценарии
3. **Смешение concerns** (15%) — путаница между "как делать" vs "когда делать"

#### Зональный анализ: standard-development.md

Дата: 2026-02-05. Проверка нового стандарта и рекомендаций Холта на вторжения в чужие зоны.

##### Стандарт: 0 вторжений

`standard-development.md` описывает только процесс внутри feature-ветки (make-команды, тестирование, линтинг, checklist). Все внешние зависимости оформлены как SSOT-ссылки на branching, commit, initialization.

##### Рекомендации Холта: 8 вторжений из 22

| # | Рекомендация | Зона-владелец | Решение |
|---|-------------|---------------|---------|
| 2.1 | Порядок первого запуска (make setup → dev) | `initialization.md` | → SSOT-ссылка |
| 4.3 | Откладывание работы (git stash, WIP) | `standard-branching.md § 5` | → SSOT-ссылка |
| 4.5 | Работа с .env файлами | `initialization.md` | → SSOT-ссылка |
| 4.7 | Связь с GitHub Workflow (Issue → Branch → PR) | `standard-github-workflow.md` | → SSOT-ссылка |
| 4.6 | Database migrations | `/src/.instructions/` | ✗ Отклонено |
| 5.1 | Работа в команде (shared branches) | `sync/ + branching/` | ✗ Отклонено |
| 5.3 | Feature flags | `/src/.instructions/` или `config/` | ✗ Отклонено |
| 5.4 | Self-review перед push | `review/ + pull-requests/` | ✗ Отклонено |

**14 рекомендаций в зоне** — подлежат согласованию и применению.

#### Сводная таблица действий

| Приоритет | ID | Действие | Источник |
|-----------|----|----------|----------|
| P0 | Д1 | Создать `development/standard-development.md` — стадия 4 без стандарта | Дерево |
| P0 | Д2 | Переместить `projects/` из [ДОПОЛНИТЕЛЬНО] в [НЕЗАВИСИМЫЕ] в дереве | Дерево |
| P1 | З1 | Централизовать правила меток в `standard-labels.md`, убрать дубли из issue/PR | Зоны |
| P1 | З2 | Добавить двусторонние ссылки TYPE-метка ↔ Issue Template | Зоны |
| P1 | В1-В8 | Пересмотреть 4 файла рекомендаций — пометить вторжения, заменить на SSOT-ссылки | Рекомендации |
| P2 | Д3 | Обновить категории дерева (рассмотреть после создания development/) | Дерево |

---

### Рекомендации

#### Приоритизация доработок

##### Критичные (влияют на workflow)

1. ~~**Убрать дублирование** в standard-github-workflow.md~~ — **ВЫПОЛНЕНО** (Фаза 2-5)
2. **Разделить** standard-release.md и standard-release-workflow.md (уточнить границы)
3. **Добавить критерии приоритетов** в standard-labels.md

##### Важные (улучшают понимание)

4. ~~**Добавить порядок изучения** в standard-github.md~~ — **НЕАКТУАЛЬНО** (файл удалён)
5. **Добавить checklist** перед созданием PR
6. **Добавить процедуру stale Issues** в standard-issue.md
7. **Добавить release freeze** в releases/standard-release-workflow.md

##### Желательные (полировка)

8. Quick Reference для standard-workflow-file.md
9. Скрипт item-edit для standard-project.md
10. Глоссарий терминов — рассмотреть как отдельный документ

#### Согласованность SSOT

**Корректные ссылки:**
- standard-issue.md → standard-labels.md ✅
- standard-issue.md → standard-issue-template.md ✅
- standard-pull-request.md → standard-pr-template.md ✅
- standard-pull-request.md → standard-labels.md ✅
- standard-milestone.md → standard-release.md ✅
- standard-release.md → standard-milestone.md ✅

**Циклические зависимости:**
- standard-milestone.md ↔ standard-release.md — допустимо, но требует ясного указания направления

**Отсутствующие ссылки:**
- standard-project.md → standard-milestone.md — добавить интеграцию Views с Milestones
- standard-github-workflow.md → standard-project.md — добавить если используется Projects

---

### Принятые решения

| Вопрос | Решение |
|--------|---------|
| **projects/** | ✅ Создать `projects/standard-project.md` |
| **Жизненный цикл PR** | ✅ Разделить: до "Ready" → PR, после → review/ |
| **Draft PR** | ✅ В `pr-template/standard-draft-pr.md` |
| **actions/security/** | ✅ Создать сейчас |
| **issue-templates/** | ✅ Перенести в `issues/issue-templates/` |
| **pr-template/** | ✅ Перенести в `pull-requests/pr-template/` |
| **standard-release-workflow.md** | ✅ Перенести в `releases/` |
| **standard-github.md** | ✅ Удалить (дублирует workflow) |
| **Git-конвенции** | ✅ Выделить в branches/, commits/, sync/ |
| **Секции workflow** | ✅ 1:1 со стадиями цикла (§ = стадия + 2) |

---

### TODO

| Задача | Приоритет | Источник |
|--------|-----------|----------|
| ~~Создать `development/standard-development.md` — стандарт стадии 4~~ | ~~Высокий~~ | ✅ Фаза 8 |
| ~~Переместить `projects/` из [ДОПОЛНИТЕЛЬНО] в [НЕЗАВИСИМЫЕ] в дереве~~ | ~~Высокий~~ | ✅ Фаза 8 |
| Централизовать правила меток — убрать дубли из issue.md §4 и pull-request.md §7 | Высокий | zone-analysis З1 |
| Добавить двусторонние ссылки TYPE-метка ↔ Issue Template | Высокий | zone-analysis З2 |
| ~~Пересмотреть все 12 файлов рекомендаций — пометить вторжения~~ | ~~Высокий~~ | ✅ 30 вторжений помечены в 9 файлах, 2 файла подтверждены чистыми (release, workflow-file), development: 8 вторжений |
| Валидировать Волну 1 (новые): branching, commit, sync | Высокий | validation |
| Валидировать Волну 2: pull-request, milestone, release, draft-pr | Высокий | validation |
| Валидировать Волну 3: issue, project, review | Высокий | validation |
| Валидировать Волну 4: workflow, release-workflow, workflow-file | Высокий | validation |
| Разделить границы release.md / release-workflow.md | Средний | results |
| Добавить критерии приоритетов в labels.md | Средний | results |
| Добавить checklist перед созданием PR | Средний | results |
| Добавить процедуру stale Issues | Средний | results |
| Добавить release freeze в release-workflow | Средний | results |
| Создать `actions/security/standard-security.md` | Низкий | restructure |
| Исправить якоря в `projects/README.md` | Низкий | restructure |
| Удалить временный файл `123.md` | Низкий | restructure |
| Quick Reference для workflow-file.md | Низкий | results |
| Скрипт item-edit для project.md | Низкий | results |

---

### Файлы рекомендаций

| Стандарт | Файл рекомендаций | Актуальность |
|----------|-------------------|--------------|
| labels/standard-labels.md | *применено, удалён* | Выполнено |
| pr-template/standard-pr-template.md | *применено, удалён* | Выполнено |
| codeowners/standard-codeowners.md | *применено, удалён* | Выполнено |
| issue-templates/standard-issue-template.md | *применено, удалён* | Выполнено |
| issues/standard-issue.md | [recommendations-standard-issue.md](./2026-02-03-recommendations-standard-issue.md) | Актуально |
| releases/standard-release.md | [recommendations-standard-release.md](./2026-02-03-recommendations-standard-release.md) | Частично |
| pull-requests/standard-pull-request.md | *применено, удалён* | Выполнено |
| milestones/standard-milestone.md | [recommendations-standard-milestone.md](./2026-02-03-recommendations-standard-milestone.md) | Актуально |
| workflows-files/standard-workflow-file.md | [recommendations-standard-workflow-file.md](./2026-02-03-recommendations-standard-workflow-file.md) | Актуально |
| projects/standard-project.md | [recommendations-standard-project.md](./2026-02-03-recommendations-standard-project.md) | Актуально |
| standard-github-workflow.md | [recommendations-standard-development-workflow.md](./2026-02-03-recommendations-standard-development-workflow.md) | Частично |
| releases/standard-release-workflow.md | [recommendations-standard-release-workflow.md](./2026-02-03-recommendations-standard-release-workflow.md) | Частично |
| branches/standard-branching.md | [holt-analysis-standard-branching.md](./2026-02-05-holt-analysis-standard-branching.md) | Актуально |
| commits/standard-commit.md | [holt-analysis-standard-commit.md](./2026-02-05-holt-analysis-standard-commit.md) | Актуально |
| sync/standard-sync.md | [holt-analysis-standard-sync.md](./2026-02-05-holt-analysis-standard-sync.md) | Актуально |
| development/standard-development.md | [holt-analysis-standard-development.md](./2026-02-05-holt-analysis-standard-development.md) | Актуально (14 в зоне, 8 вторжений) |