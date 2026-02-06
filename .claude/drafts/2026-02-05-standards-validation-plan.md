# План валидации стандартов .github/.instructions/

Последовательный план: валидация стандарта → создание документов (validation, create, modify) → создание первых объектов.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Подход](#подход)
  - [Проблемы в workflow](#проблемы-в-workflow)
  - [Общие паттерны проблем](#общие-паттерны-проблем)
  - [Последовательность: ПОДГОТОВКА](#последовательность-подготовка)
  - [Последовательность: ЦИКЛ РАЗРАБОТКИ](#последовательность-цикл-разработки)
  - [Последовательность: ОРКЕСТРАТОР](#последовательность-оркестратор)
  - [Процесс для каждого стандарта](#процесс-для-каждого-стандарта)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** Для каждого стандарта `.github/.instructions/` выполнить полный цикл: валидация → документы → первые объекты.

**Почему:** Стандарт без документов и объектов — это описание "как надо" без инструментов "как сделать". Валидация фиксирует смысл, документы дают процедуры, первые объекты подтверждают работоспособность.

**Связанные файлы:**
- [standard-github-workflow.md](/.github/.instructions/standard-github-workflow.md) — оркестратор (Фаза 0 + Фаза 1)
- [2026-02-05-github-instructions.md](./2026-02-05-github-instructions.md) — основной трекер реструктуризации

---

## Содержание

### Подход

Для каждого стандарта — полный цикл из 3 этапов:

```
ЭТАП 1: ВАЛИДАЦИЯ СТАНДАРТА
  1. Прочитать файл рекомендаций (holt-analysis или recommendations)
  2. Решить что применяем: P1 (обязательно), P2 (если правка < 5 строк), P3 (пропускаем)
  3. Применить выбранные рекомендации
  4. Удалить файл рекомендаций
  Примечание: зональные вторжения уже проверены при создании рекомендаций.

ЭТАП 2: СОЗДАНИЕ ДОКУМЕНТОВ
  5. Создать validation-*.md (как проверить соответствие стандарту)
  6. Создать create-*.md (как создать объект по стандарту) — если применимо
  7. Создать modify-*.md (как изменить объект по стандарту) — если применимо
  8. Обновить таблицу "Связанные документы" в стандарте (убрать "Будет создан")

ЭТАП 3: СОЗДАНИЕ ПЕРВЫХ ОБЪЕКТОВ
  9. Создать реальные объекты по стандарту (если применимо)
  10. Проверить объекты через validation-*.md
```

**Какие документы нужны каждому типу стандарта:**

| Тип стандарта | validation | create | modify | Первый объект |
|---------------|:----------:|:------:|:------:|---------------|
| Объект GitHub (milestone, issue, label, project) | да | да | да | Да — первый экземпляр |
| Шаблон/конфиг (issue-template, pr-template, codeowners, workflow-file, security) | да | да | да | Да — первый файл |
| Конвенция (branching, commit, sync) | да | нет | нет | Нет |
| Процесс (development, review) | да | нет | нет | Нет |
| Составной (pull-request, release, release-workflow) | да | да | да | По ситуации |

---

### Проблемы в workflow

Проверка SSOT-ссылок в `standard-github-workflow.md`:

#### ПОДГОТОВКА (Фаза 0)

| # | Шаг | SSOT-ссылка | Статус |
|---|-----|-------------|--------|
| 1 | Labels | `→ standard-labels.md` | ✅ |
| 2 | CODEOWNERS | `→ standard-codeowners.md` | ✅ |
| 3 | Issue Templates | `→ standard-issue-template.md` | ✅ |
| 4 | PR Template | `→ standard-pr-template.md` | ✅ |
| 5 | Milestones | `→ standard-milestone.md` | ✅ |
| 6 | GitHub Projects | `→ standard-project.md` | ✅ |
| 7 | GitHub Actions | `→ standard-action.md` | ✅ |
| 8 | Security | `→ standard-security.md` | ✅ |
| 9 | Secrets | `→ standard-secrets.md` | ✅ (конвенция, без шага в Фазе 0) |
| 10 | Pre-commit Hooks | `→ initialization.md` | ✅ (вне `.github/.instructions/`) |

~~**Проблема П-1:** Security не включён в Фазу 0.~~ **Решено:** добавлен шаг 8. SECURITY в Фазу 0 + строка в таблицу зон "Автоматизация".

#### ЦИКЛ РАЗРАБОТКИ (Фаза 1)

| # | Шаг | SSOT-ссылка | Статус |
|---|-----|-------------|--------|
| 1 | Планирование | `→ standard-issue.md` | ✅ |
| 2 | Группировка | `→ standard-pull-request.md § 6, standard-milestone.md` | ✅ |
| 3 | Создание ветки | `→ standard-branching.md` | ✅ |
| 4 | Разработка | `→ § 6. Стадия 4` | ❌ **Самоссылка!** |
| 5 | Коммиты | `→ standard-commit.md` | ✅ |
| 6 | Создание PR | `→ standard-pull-request.md` | ✅ |
| 7 | Code Review | `→ standard-review.md § 2` | ✅ |
| 8 | Merge | `→ standard-review.md § 3` | ✅ |
| 9 | Синхронизация | `→ standard-sync.md` | ✅ |
| 10 | Релиз | `→ standard-release-workflow.md` | ✅ |

**Проблема Ц-1:** Строка 113 — `→ § 6. Стадия 4` вместо `→ standard-development.md`. Все остальные шаги ссылаются на SSOT-стандарт, а этот — на собственную секцию.

---

### Общие паттерны проблем

Из 5 holt-анализов (branching, commit, sync, development, security) выявлено **100 проблем** (32 P1, 34 P2, 34 P3). Повторяющиеся паттерны:

| ID | Паттерн | Файлы | Примеры |
|----|---------|-------|---------|
| **П1** | Размытые временные критерии | branching, sync, development | ">2 дней разработки" — календарные или рабочие? |
| **П2** | Ручное vs автоматическое | commit, development | "make lint перед коммитом" при наличии pre-commit hooks |
| **П3** | Нет алгоритмов для LLM | branching, commit, sync | Правила текстом, но нет step-by-step инструкций |
| **П5** | "При необходимости" без критериев | branching, development, security | "если затронуты интеграционные сценарии" — критерии? |
| **П6** | Только happy path | branching, commit, sync, development | Нет edge cases (stale ветки, пустой changelog) |
| **П7** | Граница release ↔ release-workflow | release, release-workflow | Оба описывают создание Release |

**Стратегия:** P1 исправляем обязательно. P2 — по ситуации (если правка < 5 строк). P3 — пропускаем (откладываем). Паттерны П1-П3 исправляем внутри каждого стандарта. П7 — решаем при обработке release.md и release-workflow.md.

---

### Последовательность: ПОДГОТОВКА

Стандарты из Фазы 0 workflow. Первые 4 уже валидированы (этап 1), но без документов и объектов (этапы 2-3).

| # | Стандарт | Этап 1 | Этап 2 (docs) | Этап 3 (объекты) |
|---|----------|:------:|:-------------:|:----------------:|
| ~~0.1~~ | `labels/standard-labels.md` | ✅ | ✅ validation + modify (create не нужен) | ✅ `labels.yml` |
| ~~0.2~~ | `codeowners/standard-codeowners.md` | ✅ | ✅ validation (create/modify не нужны) | ✅ `CODEOWNERS` |
| ~~0.3~~ | `issues/issue-templates/standard-issue-template.md` | ✅ | ⚠️ validation ✅ (ссылки исправлены на `validation-type-templates.md`); **create и modify отсутствуют** (*не нужны к созданию*) | ✅ 6 шаблонов + config.yml |
| ~~0.4~~ | `pull-requests/pr-template/standard-pr-template.md` | ✅ | ✅ validation (create/modify не нужны) | ✅ `PULL_REQUEST_TEMPLATE.md` |
| | *`standard-draft-pr.md` влит в `standard-pull-request.md` § 2, файл удалён* | | | |
| ~~0.5~~ | `milestones/standard-milestone.md` | ✅ | ✅ validation + create + modify + 3 скрипта + 3 скилла | ✅ Milestone `v0.1.0` создан (#1) |
| ~~0.6~~ | `projects/standard-project.md` | ✅ деактивирован | — | — |
| ~~0.7~~ | `actions/standard-action.md` | ✅ | ✅ validation (create/modify не нужны) + скрипт + pre-commit хук | ✅ `.github/workflows/ci.yml` |
| **0.8** | `actions/security/standard-security.md` | ⏳ | ⏳ validation, create, modify | ⏳ Dependabot, CodeQL, SECURITY.md |
| **0.9** | `actions/security/standard-secrets.md` | ✅ (holt-анализ — правки отложены) | ⏳ validation | — (конвенция) |

**Зависимости:** Нет — все стандарты ПОДГОТОВКИ независимы. Можно обрабатывать параллельно.

**Долг:** 0.1, 0.2, 0.4, 0.5 — полностью завершены (все 3 этапа ✅). 0.3 — validation имя не совпадает, create/modify отсутствуют.

---

### Последовательность: ЦИКЛ РАЗРАБОТКИ

Стандарты из Фазы 1 workflow, в порядке стадий.

| # | Стадия | Стандарт | Этап 1 | Этап 2 (docs) | Этап 3 (объекты) |
|---|--------|----------|:------:|:-------------:|:----------------:|
| **1.1** | 1 | `issues/standard-issue.md` | ⏳ | ⏳ validation, create, modify | ⏳ Первый Issue |
| **1.2** | 3 | `branches/standard-branching.md` | ⏳ | ⏳ validation | — (конвенция) |
| **1.3** | 4 | `development/standard-development.md` | ⏳ | ⏳ validation | — (процесс) |
| **1.4** | 5 | `commits/standard-commit.md` | ⏳ | ⏳ validation | — (конвенция) |
| ~~1.5~~ | 6 | `pull-requests/standard-pull-request.md` | ✅ | ⏳ validation, create, modify | — (PR создаётся в процессе) |
| **1.6** | 7-8 | `review/standard-review.md` | ⏳ | ⏳ validation | — (процесс) |
| **1.8** | 9 | `sync/standard-sync.md` | ⏳ | ⏳ validation | — (конвенция) |
| **1.9** | 10 | `releases/standard-release.md` | ⏳ | ⏳ validation, create, modify | ⏳ Первый Release (когда будет готов) |
| **1.10** | 10 | `releases/standard-release-workflow.md` | ⏳ | ⏳ validation | — (процесс) |

**Зависимости:**
- 1.9 и 1.10 обрабатывать ВМЕСТЕ (общая граница П7)
- 1.3 зависит от 1.2 (development ссылается на branching)
- 1.8 зависит от 1.2 (sync ссылается на branching)

---

### Последовательность: ОРКЕСТРАТОР

Обрабатывается ПОСЛЕДНИМ, после всех зависимых стандартов.

| # | Стандарт | Этап 1 | Этап 2 (docs) | Этап 3 (объекты) |
|---|----------|:------:|:-------------:|:----------------:|
| **2.1** | `standard-github-workflow.md` | ⏳ | ⏳ validation | — (оркестратор) |

**Перед валидацией оркестратора:**
1. Исправить строку 113: `→ § 6. Стадия 4` → `→ standard-development.md`
2. Добавить шаг Security в Фазу 0 (после GitHub Actions)
3. Убедиться, что все SSOT-ссылки ведут на актуальные якоря

---

### Процесс для каждого стандарта

Все файлы рекомендаций уже созданы captain-holt (и `recommendations-*`, и `holt-analysis-*`).

```
ЭТАП 1: ВАЛИДАЦИЯ
  1. Прочитать файл рекомендаций
  2. Решить что применяем: P1 (обязательно), P2 (если < 5 строк), P3 (пропуск)
  3. Применить выбранные рекомендации
  4. Удалить файл рекомендаций
  Примечание: зональные вторжения уже проверены при создании рекомендаций.

ЭТАП 2: ДОКУМЕНТЫ
  5. /instruction-create validation-{name}.md --path .github/.instructions/{area}/
  6. /instruction-create create-{name}.md --path .github/.instructions/{area}/  (если применимо)
  7. /instruction-create modify-{name}.md --path .github/.instructions/{area}/  (если применимо)
  8. Обновить таблицу "Связанные документы" в стандарте

ЭТАП 3: ПЕРВЫЕ ОБЪЕКТЫ
  9. Создать объект(ы) по create-{name}.md
  10. Проверить через validation-{name}.md
```

---

### Сводная таблица

| # | Стандарт | Фаза | Этап 1 | Этап 2 | Этап 3 |
|---|----------|------|:------:|:------:|:------:|
| 0.1 | standard-labels.md | Подготовка | ✅ | ✅ | ✅ |
| 0.2 | standard-codeowners.md | Подготовка | ✅ | ✅ | ✅ |
| 0.3 | standard-issue-template.md | Подготовка | ✅ | ⚠️ | ✅ |
| 0.4 | standard-pr-template.md | Подготовка | ✅ | ✅ | ✅ |
| 0.5 | standard-milestone.md | Подготовка | ✅ | ✅ | ✅ |
| ~~0.6~~ | standard-project.md | Подготовка | ✅ деактивирован | — | — |
| ~~0.7~~ | standard-action.md | Подготовка | ✅ | ✅ | ✅ |
| 0.8 | standard-security.md | Подготовка | ⏳ | ⏳ | ⏳ |
| 0.9 | standard-secrets.md | Подготовка | ✅ | ⏳ | — |
| 1.1 | standard-issue.md | Цикл | ⏳ | ⏳ | ⏳ |
| 1.2 | standard-branching.md | Цикл | ⏳ | ⏳ | — |
| 1.3 | standard-development.md | Цикл | ⏳ | ⏳ | — |
| 1.4 | standard-commit.md | Цикл | ⏳ | ⏳ | — |
| ~~1.5~~ | ~~standard-pull-request.md~~ | ~~Цикл~~ | ✅ | ⏳ | — |
| 1.6 | standard-review.md | Цикл | ⏳ | ⏳ | — |
| 1.8 | standard-sync.md | Цикл | ⏳ | ⏳ | — |
| 1.9 | standard-release.md | Цикл | ⏳ | ⏳ | ⏳ |
| 1.10 | standard-release-workflow.md | Цикл | ⏳ | ⏳ | — |
| 2.1 | standard-github-workflow.md | Оркестратор | ⏳ | ⏳ | — |

**Итого:** 19 стандартов. Этап 1: 8 ✅, 11 ⏳. Этап 2: 5 ✅, 1 ⚠️, 13 ⏳. Этап 3: 8 применимо (5 ✅, 3 ⏳), 11 не применимо.

---

## Открытые вопросы

1. ~~**Security в Фазе 0**~~ — **Решено:** шаг 8. SECURITY добавлен в Фазу 0.
2. **Граница release ↔ release-workflow (П7)** — решать ДО или ПОСЛЕ применения рекомендаций?
3. **Долг 0.3** — ссылки на validation исправлены. Создать create-issue-template.md и modify-issue-template.md?
4. ~~**Долг 0.5**~~ — **Решено:** все 3 этапа завершены. Docs: validation + create + modify + 3 скрипта + 3 скилла. Объект: Milestone `v0.1.0` создан (#1). Багфикс: `gh_api()` — `--method GET` + `encoding="utf-8"` в 3 скриптах.
