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

**Статус:** Реструктуризация ВЫПОЛНЕНА (Фаза 1-8). Зональный анализ ВЫПОЛНЕН. Валидация: Волна 1 частично (1-4 ✅, 5-8 ⏳), Волны 2-4 ожидают.

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

8 фаз выполнено за 2026-02-04/05:

| Фаза | Дата | Суть |
|------|------|------|
| 1 | 2026-02-04 | Реструктуризация файлов: переименование workflow, удаление github.md, перенос templates в подпапки |
| 2 | 2026-02-05 | Переконфигурация workflow: зоны ответственности, Фаза 0, цикл 10 шагов → v1.1 |
| 3 | 2026-02-05 | Выделение git-конвенций: branches/, commits/, sync/ из секций workflow → v1.2 |
| 4 | 2026-02-05 | Выравнивание секций 1:1: 14 секций (§ = стадия + 2) → v1.3 |
| 5 | 2026-02-05 | Устранение дублирования: SSOT-ссылки вместо дублей → v1.4 |
| 6 | 2026-02-05 | Доработка git-конвенций: v2 через `/instruction-create`, сравнение v1↔v2, объединение → v1.1 стандартов |
| 7 | 2026-02-05 | Зональный анализ: 16 стандартов + 12 файлов рекомендаций. 30 вторжений удалены |
| 8 | 2026-02-05 | Исправление дерева: [GIT-КОНВЕНЦИИ] → [ЭТАПЫ ЖЦ], создан development/, projects/ → [НЕЗАВИСИМЫЕ] → workflow v1.5 |

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
| 5 | `branches/standard-branching.md` | ⏳ holt-анализ готов |
| 6 | `commits/standard-commit.md` | ⏳ holt-анализ готов |
| 7 | `sync/standard-sync.md` | ⏳ holt-анализ готов |
| 8 | `development/standard-development.md` | ⏳ holt-анализ готов |

##### Волна 2: PR, Milestone, Release, Draft PR

| # | Файл | Зависит от | Статус |
|---|------|------------|--------|
| 9 | `pull-requests/standard-pull-request.md` | labels, pr-template | ⏳ |
| 10 | `milestones/standard-milestone.md` | ↔issue, ↔release | ⏳ |
| 11 | `releases/standard-release.md` | milestone, pull-request | ⏳ |

##### Волна 3: Issue, Project, Review

| # | Файл | Зависит от | Статус |
|---|------|------------|--------|
| 13 | `issues/standard-issue.md` | labels, templates, PR, milestone | ⏳ |
| 14 | `projects/standard-project.md` | issue, pr, milestone | ⏳ |
| 15 | `review/standard-review.md` | pull-request | ⏳ |

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
| 5 | branches/standard-branching.md | — | — | *Holt-анализ готов, не применён* |
| 6 | commits/standard-commit.md | — | — | *Holt-анализ готов, не применён* |
| 7 | sync/standard-sync.md | — | — | *Holt-анализ готов, не применён* |
| 8 | development/standard-development.md | — | — | *Holt-анализ готов, не применён* |
| 9 | pull-requests/standard-pull-request.md | 8/10 | 7/10 | Нет self-review, эскалации |
| 10 | milestones/standard-milestone.md | 8/10 | 7/10 | Нет автоматизации Sprint |
| 11 | releases/standard-release.md | 9/10 | 9/10 | Пересечение с release-workflow |
| 12 | issues/standard-issue.md | 8/10 | 7/10 | Нет процедуры для stale Issues |
| 14 | projects/standard-project.md | 8/10 | 7/10 | Сложный item-edit без скрипта |
| 15 | review/standard-review.md | — | — | *Не валидировано* |
| 16 | standard-github-workflow.md | 9/10 | 8/10 | — |
| 17 | releases/standard-release-workflow.md | 8/10 | 8/10 | Нет release freeze процедуры |
| 18 | workflows-files/standard-workflow-file.md | 9/10 | 9/10 | Слишком большой (~1300 строк) |

#### Общие паттерны проблем

##### 1. Пересечение standard-release.md и standard-release-workflow.md

**Проблема:** Оба документа описывают создание Release. Границы размыты.

**Рекомендация:** Чётко разделить:
- **standard-release.md:** ЧТО (свойства, формат, версионирование)
- **standard-release-workflow.md:** КОГДА и КАК (процесс, проверки)

##### 2. Отсутствие процедур для edge cases

**Примеры:** stale Issues, срыв сроков Milestone, эскалация review.

**Рекомендация:** Добавить секции "Граничные случаи" в каждый стандарт.

##### 3. Нет автоматизации для рутинных операций

**Примеры:** Sprint Milestone, валидация меток, определение версии по commits.

**Рекомендация:** Добавить скрипты или GitHub Actions.

---

### Зональный анализ

Дата: 2026-02-05. Проанализировано 16 standard-файлов + 12 файлов рекомендаций.

**Итог:** Общая оценка разделения зон — **7.5/10**. Все критичные проблемы решены (дерево Д1-Д3, пересечения З1-З2, 30 вторжений рекомендаций удалены).

#### Допустимые пересечения (оставлены)

| # | Что | Файлы | Вердикт |
|---|-----|-------|---------|
| З3 | Merge стратегия упомянута в PR | `standard-pull-request.md §8`, `standard-review.md §3` | OK — summary-ссылка на SSOT |
| З4 | Workflow automation в нескольких | workflow, release-workflow | OK — разделение КОГДА vs КАК |

#### Hub-зависимости

| Стандарт | Используется в | Кол-во зависимых |
|----------|----------------|-----------------|
| `standard-labels.md` | issue, PR, issue-template, branching, project, workflow | 6 |
| `standard-issue.md` | PR, review, milestone, project, branching | 5 |
| `standard-milestone.md` | release, release-workflow, project | 3 |

---

### Рекомендации

#### Приоритизация доработок

##### Критичные (влияют на workflow)

1. **Разделить** standard-release.md и standard-release-workflow.md (уточнить границы)
2. **Добавить критерии приоритетов** в standard-labels.md

##### Важные (улучшают понимание)

3. **Добавить checklist** перед созданием PR
4. **Добавить процедуру stale Issues** в standard-issue.md
5. **Добавить release freeze** в releases/standard-release-workflow.md

##### Желательные (полировка)

6. Quick Reference для standard-workflow-file.md
7. Скрипт item-edit для standard-project.md
8. Глоссарий терминов — рассмотреть как отдельный документ

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

### TODO

| Задача | Приоритет | Источник |
|--------|-----------|----------|
| Применить holt-анализы: branching, commit, sync, development | Высокий | validation |
| Валидировать Волну 2: milestone, release | Высокий | validation |
| Валидировать Волну 3: issue, project, review | Высокий | validation |
| Валидировать Волну 4: workflow, release-workflow, workflow-file | Высокий | validation |
| Разделить границы release.md / release-workflow.md | Средний | results |
| Добавить критерии приоритетов в labels.md | Средний | results |
| Добавить checklist перед созданием PR | Средний | results |
| Добавить процедуру stale Issues | Средний | results |
| Добавить release freeze в release-workflow | Средний | results |
| ~~Создать `actions/security/standard-security.md`~~ | ~~Низкий~~ | ✅ |
| ~~Исправить якоря в `projects/README.md`~~ | ~~Низкий~~ | ✅ |
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
| development/standard-development.md | [holt-analysis-standard-development.md](./2026-02-05-holt-analysis-standard-development.md) | Актуально |
