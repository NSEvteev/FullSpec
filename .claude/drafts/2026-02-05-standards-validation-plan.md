# План валидации стандартов .github/.instructions/

Последовательный план: валидация стандарта → создание документов (validation, create, modify) → создание первых объектов.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Подход](#подход)
  - [Сводная таблица](#сводная-таблица)
  - [Цикл разработки](#цикл-разработки)
  - [Оркестратор](#оркестратор)
  - [Общие паттерны проблем](#общие-паттерны-проблем)
- [Открытые вопросы](#открытые-вопросы)
- [Журнал изменений](#журнал-изменений)

---

## Контекст

**Задача:** Для каждого стандарта `.github/.instructions/` выполнить полный цикл: валидация → документы → первые объекты.

**Почему:** Стандарт без документов и объектов — это описание "как надо" без инструментов "как сделать". Валидация фиксирует смысл, документы дают процедуры, первые объекты подтверждают работоспособность.

**Связанные файлы:**
- [standard-github-workflow.md](/.github/.instructions/standard-github-workflow.md) — оркестратор (Фаза 0 + Фаза 1)
- [2026-02-05-github-instructions.md](./2026-02-05-github-instructions.md) — основной трекер реструктуризации
- [2026-02-06-holt-zone-intrusions.md](./2026-02-06-holt-zone-intrusions.md) — зональный анализ (7/15 разрешены)

---

## Содержание


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
│   │   ├── standard-milestone.md
│   │   ├── validation-milestone.md
│   │   ├── create-milestone.md
│   │   └── modify-milestone.md
│   └── projects/
│       ├── README.md
│       └── standard-project.md
│
├── [ЭТАПЫ ЖИЗНЕННОГО ЦИКЛА]                  (порядок = стадии workflow)
│   ├── issues/                        ← стадия 1: планирование
│   │   ├── README.md
│   │   ├── standard-issue.md
│   │   ├── validation-issue.md
│   │   ├── create-issue.md
│   │   ├── modify-issue.md
│   │   └── issue-templates/
│   │       ├── README.md
│   │       ├── standard-issue-template.md
│   │       └── validation-type-templates.md
│   │
│   ├── branches/                      ← стадия 3: создание ветки
│   │   ├── README.md
│   │   ├── standard-branching.md
│   │   ├── validation-branch.md
│   │   └── create-branch.md
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
│   └── actions/
│       ├── README.md
│       └── standard-action.md
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
| **actions/standard-action.md** | Структура YAML, триггеры, jobs/steps, secrets |
| **actions/security/** | Dependabot, CodeQL, Secret Scanning |


### Подход

Для каждого стандарта — полный цикл из 3 этапов:

```
ЭТАП 1: ВАЛИДАЦИЯ СТАНДАРТА
  1. Прочитать файл рекомендаций (holt-analysis или recommendations)
  2. Решить что применяем: P1 (обязательно), P2 (если < 5 строк), P3 (пропуск)
  3. Применить выбранные рекомендации
  4. Удалить файл рекомендаций

ЭТАП 2: ДОКУМЕНТЫ
  5. /instruction-create validation-{name}.md --path .github/.instructions/{area}/
  6. /instruction-create create-{name}.md  (если применимо)
  7. /instruction-create modify-{name}.md  (если применимо)
  8. Обновить таблицу "Связанные документы" в стандарте

ЭТАП 3: ПЕРВЫЕ ОБЪЕКТЫ
  9. Создать объект(ы) по create-{name}.md
  10. Проверить через validation-{name}.md
```

Примечание: зональные вторжения уже проверены при создании рекомендаций → [2026-02-06-holt-zone-intrusions.md](./2026-02-06-holt-zone-intrusions.md).

**Какие документы нужны каждому типу стандарта:**

| Тип стандарта | validation | create | modify | Первый объект |
|---------------|:----------:|:------:|:------:|---------------|
| Объект GitHub (milestone, issue, label, project) | да | да | да | Да — первый экземпляр |
| Шаблон/конфиг (issue-template, pr-template, codeowners, workflow-file, security) | да | да | да | Да — первый файл |
| Конвенция (branching, commit, sync) | да | нет | нет | Нет |
| Процесс (development, review) | да | нет | нет | Нет |
| Составной (pull-request, release, release-workflow) | да | да | да | По ситуации |

---

### Сводная таблица

| # | Стандарт | Фаза | Этап 1 | Этап 2 | Этап 3 |
|---|----------|------|:------:|:------:|:------:|
| ~~0.1~~ | standard-labels.md | Подготовка | ✅ | ✅ | ✅ |
| ~~0.2~~ | standard-codeowners.md | Подготовка | ✅ | ✅ | ✅ |
| ~~0.3~~ | standard-issue-template.md | Подготовка | ✅ | ✅ | ✅ |
| ~~0.4~~ | standard-pr-template.md | Подготовка | ✅ | ✅ | ✅ |
| ~~0.5~~ | standard-milestone.md | Подготовка | ✅ | ✅ | ✅ |
| ~~0.6~~ | standard-project.md | Подготовка | ✅ деактивирован | — | — |
| ~~0.7~~ | standard-action.md | Подготовка | ✅ | ✅ | ✅ |
| ~~0.8~~ | standard-security.md | Подготовка | ✅ | ✅ | ✅ |
| ~~0.9~~ | standard-secrets.md | Подготовка | ✅ | ✅ | — |
| ~~1.1~~ | standard-issue.md | Цикл | ✅ | ✅ | ✅ |
| ~~1.2~~ | standard-branching.md | Цикл | ✅ | ✅ | ✅ |
| ~~1.3~~ | standard-development.md | Цикл | ✅ | ✅ | — |
| ~~1.4~~ | standard-commit.md | Цикл | ✅ | ✅ | — |
| ~~1.5~~ | standard-pull-request.md | Цикл | ✅ | ✅ | — |
| ~~1.6~~ | standard-review.md | Цикл | ✅ | ✅ | — |
| ~~1.8~~ | standard-sync.md | Цикл | ✅ | ✅ | — |
| 1.9 | standard-release.md | Цикл | ⏳ | ⏳ | ⏳ |
| 1.10 | standard-release-workflow.md | Цикл | ⏳ | ⏳ | — |
| 2.1 | standard-github-workflow.md | Оркестратор | ⏳ | ⏳ | — |

**Итого:** 19 стандартов. Этап 1: 15 ✅, 4 ⏳. Этап 2: 15 ✅, 4 ⏳. Этап 3: 8 ✅, 1 ⏳, 10 н/п.

**ПОДГОТОВКА:** Завершена (0.1-0.9).

**ЦИКЛ:** 1.1 ✅ (все 3 этапа), 1.2 ✅ (все 3 этапа, ветка task/standards-validation-34). 1.3 ✅ (Этап 1 v1.2 + Этап 2 validation + rule, Этап 3 н/п — процесс), 1.4 ✅ (Этап 1 v1.2 + Этап 2 rule в development.md, Этап 3 н/п — конвенция), 1.5 ✅ (Этап 1 ранее + Этап 2 rule в development.md, Этап 3 н/п), 1.6 ✅ (Этап 1 v1.1 + Этап 2 rule в development.md + initialization.md § 7, Этап 3 н/п — процесс), 1.8 ✅ (Этап 1 v1.2 + Этап 2 rule в development.md, Этап 3 н/п — конвенция).

---

### Цикл разработки

Активная область. Стандарты из Фазы 1 workflow, в порядке стадий.

| # | Стадия | Стандарт | Этап 1 | Этап 2 (docs) | Этап 3 |
|---|--------|----------|:------:|:-------------:|:------:|
| ~~1.1~~ | 1 | `issues/standard-issue.md` | ✅ v1.4 | ✅ validation + create + modify + скрипт + 3 скилла + rule | ✅ Issue #34 |
| ~~1.2~~ | 3 | `branches/standard-branching.md` | ✅ v1.2 | ✅ validation + create + скрипт + скилл + pre-commit | ✅ task/standards-validation-34 |
| ~~1.3~~ | 4 | `development/standard-development.md` | ✅ v1.2 | ✅ validation + rule | — |
| ~~1.4~~ | 5 | `commits/standard-commit.md` | ✅ v1.2 | ✅ rule в development.md | — |
| ~~1.5~~ | 6 | `pull-requests/standard-pull-request.md` | ✅ | ✅ rule в development.md | — |
| ~~1.6~~ | 7-8 | `review/standard-review.md` | ✅ v1.1 | ✅ rule в development.md | — |
| ~~1.8~~ | 9 | `sync/standard-sync.md` | ✅ v1.2 | ✅ rule в development.md | — |
| **1.9** | 10 | `releases/standard-release.md` | ⏳ | ⏳ validation, create, modify | ⏳ |
| **1.10** | 10 | `releases/standard-release-workflow.md` | ⏳ | ⏳ validation | — |

**Зависимости:**
- 1.9 и 1.10 обрабатывать ВМЕСТЕ (общая граница П7)
- 1.3 зависит от 1.2 ✅ (разблокирован)
- 1.8 зависит от 1.2 ✅ (разблокирован)

**Следующий шаг:** 1.9 + 1.10 (standard-release.md + standard-release-workflow.md) — обрабатывать ВМЕСТЕ (граница П7).

---

### Оркестратор

Обрабатывается ПОСЛЕДНИМ, после всех зависимых стандартов.

| # | Стандарт | Этап 1 | Этап 2 (docs) | Этап 3 |
|---|----------|:------:|:-------------:|:------:|
| **2.1** | `standard-github-workflow.md` | ⏳ | ⏳ validation | — |

**Перед валидацией:**
1. Исправить самоссылку Ц-1: `→ § 6. Стадия 4` → `→ standard-development.md`
2. Убедиться, что все SSOT-ссылки ведут на актуальные якоря

---

### Общие паттерны проблем

Из 5 holt-анализов выявлено **100 проблем** (32 P1, 34 P2, 34 P3). Повторяющиеся паттерны:

| ID | Паттерн | Файлы | Статус |
|----|---------|-------|--------|
| **П1** | Размытые временные критерии | branching, sync, development | ✅ branching v1.2, development v1.1 |
| **П2** | Ручное vs автоматическое | commit, development | ✅ development v1.1 |
| **П3** | Нет алгоритмов для LLM | branching, commit, sync | ✅ branching v1.2 |
| **П5** | "При необходимости" без критериев | branching, development, security | Частично ✅ |
| **П6** | Только happy path | branching, commit, sync, development | ✅ branching v1.2, development v1.1 |
| **П7** | Граница release ↔ release-workflow | release, release-workflow | ⏳ Решать при 1.9+1.10 |

**Стратегия:** P1 — обязательно, P2 — если < 5 строк, P3 — пропуск.

---

## Открытые вопросы

1. **Граница release ↔ release-workflow (П7)** — решать ДО или ПОСЛЕ применения рекомендаций?

---
