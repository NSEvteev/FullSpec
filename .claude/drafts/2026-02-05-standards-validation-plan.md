# План валидации стандартов .github/.instructions/

Последовательный план применения holt-анализов и завершения смысловой валидации всех стандартов.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Проблемы в workflow](#проблемы-в-workflow)
  - [Общие паттерны проблем](#общие-паттерны-проблем)
  - [Последовательность: ПОДГОТОВКА](#последовательность-подготовка)
  - [Последовательность: ЦИКЛ РАЗРАБОТКИ](#последовательность-цикл-разработки)
  - [Последовательность: ОРКЕСТРАТОР](#последовательность-оркестратор)
  - [Процесс для каждого стандарта](#процесс-для-каждого-стандарта)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** Завершить смысловую валидацию всех стандартов `.github/.instructions/`.

**Почему:** Из 18 стандартов валидированы только 5. Для остальных 12 существуют файлы рекомендаций (все созданы captain-holt), которые нужно применить. Ещё 2 стандарта (draft-pr, review) не имеют файлов рекомендаций — статус уточняется. Порядок обработки следует структуре workflow: сначала ПОДГОТОВКА (Фаза 0), потом ЦИКЛ РАЗРАБОТКИ (Фаза 1).

**Связанные файлы:**
- [standard-github-workflow.md](/.github/.instructions/standard-github-workflow.md) — оркестратор (Фаза 0 + Фаза 1)
- [2026-02-05-github-instructions.md](./2026-02-05-github-instructions.md) — основной трекер реструктуризации

---

## Содержание

### Проблемы в workflow

Проверка SSOT-ссылок в `standard-github-workflow.md`:

#### ПОДГОТОВКА (Фаза 0, строки 160-196)

| # | Шаг | SSOT-ссылка | Статус |
|---|-----|-------------|--------|
| 1 | Labels | `→ standard-labels.md` | ✅ |
| 2 | CODEOWNERS | `→ standard-codeowners.md` | ✅ |
| 3 | Issue Templates | `→ standard-issue-template.md` | ✅ |
| 4 | PR Template | `→ standard-pr-template.md` | ✅ |
| 5 | Milestones | `→ standard-milestone.md` | ✅ |
| 6 | GitHub Projects | `→ standard-project.md` | ✅ |
| 7 | GitHub Actions | `→ standard-workflow-file.md` | ✅ |
| 8 | Pre-commit Hooks | `→ initialization.md` | ✅ (вне `.github/.instructions/`) |
| — | **Security** | **Отсутствует** | ❌ Нет шага для Dependabot/CodeQL/Secret Scanning |

**Проблема П-1:** Security не включён в Фазу 0. Стандарт `standard-security.md` создан, но в workflow нет шага "Настроить безопасность".

#### ЦИКЛ РАЗРАБОТКИ (Фаза 1, строки 91-143)

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
| **П4** | Нет валидационных документов | все 5 | Стандарты описывают ЧТО, но нет validation-*.md |
| **П5** | "При необходимости" без критериев | branching, development, security | "если затронуты интеграционные сценарии" — критерии? |
| **П6** | Только happy path | branching, commit, sync, development | Нет edge cases (stale ветки, пустой changelog) |
| **П7** | Граница release ↔ release-workflow | release, release-workflow | Оба описывают создание Release |

**Стратегия:** P1 исправляем обязательно. P2 — по ситуации (если правка < 5 строк). P3 — пропускаем (откладываем). Паттерны П1-П3 исправляем внутри каждого стандарта. П4 (validation-*.md) — отдельная задача после валидации. П7 — решаем при обработке release.md и release-workflow.md.

---

### Последовательность: ПОДГОТОВКА

Стандарты из Фазы 0 workflow. Первые 4 уже валидированы.

| Порядок | Стандарт | Файл рекомендаций | P1 | Действие |
|---------|----------|-------------------|-------|----------|
| ~~0.1~~ | `labels/standard-labels.md` | *применены, удалён* | — | ✅ Валидирован |
| ~~0.2~~ | `codeowners/standard-codeowners.md` | *применены, удалён* | — | ✅ Валидирован |
| ~~0.3~~ | `issues/issue-templates/standard-issue-template.md` | *применены, удалён* | — | ✅ Валидирован |
| ~~0.4~~ | `pull-requests/pr-template/standard-pr-template.md` | *применены, удалён* | — | ✅ Валидирован |
| | *`standard-draft-pr.md` влит в `standard-pull-request.md` § 2, файл удалён* | | | |
| **0.5** | `milestones/standard-milestone.md` | [recommendations](./2026-02-03-recommendations-standard-milestone.md) | 4 | Применить → удалить → ✅ |
| **0.6** | `projects/standard-project.md` | [recommendations](./2026-02-03-recommendations-standard-project.md) | 6 | Применить → удалить → ✅ |
| **0.7** | `workflows-files/standard-workflow-file.md` | [recommendations](./2026-02-03-recommendations-standard-workflow-file.md) | 8 | Применить → удалить → ✅ |
| **0.8** | `actions/security/standard-security.md` | [holt-analysis](./2026-02-05-holt-analysis-standard-security.md) | 3 | Применить → удалить → ✅ |

**Зависимости внутри фазы:** Нет — все стандарты ПОДГОТОВКИ независимы друг от друга. Можно обрабатывать параллельно.

---

### Последовательность: ЦИКЛ РАЗРАБОТКИ

Стандарты из Фазы 1 workflow, в порядке стадий.

| Порядок | Стадия | Стандарт | Файл рекомендаций | P1 | Действие |
|---------|--------|----------|-------------------|-------|----------|
| **1.1** | 1 | `issues/standard-issue.md` | [recommendations](./2026-02-03-recommendations-standard-issue.md) | 6 | Применить → удалить → ✅ |
| **1.2** | 3 | `branches/standard-branching.md` | [holt-analysis](./2026-02-05-holt-analysis-standard-branching.md) | 10 | Применить → удалить → ✅ |
| **1.3** | 4 | `development/standard-development.md` | [holt-analysis](./2026-02-05-holt-analysis-standard-development.md) | 5 | Применить → удалить → ✅ |
| **1.4** | 5 | `commits/standard-commit.md` | [holt-analysis](./2026-02-05-holt-analysis-standard-commit.md) | 8 | Применить → удалить → ✅ |
| ~~1.5~~ | 6 | `pull-requests/standard-pull-request.md` | *применены, удалён* | — | ✅ Валидирован |
| **1.6** | 7-8 | `review/standard-review.md` | [holt-analysis](./2026-02-05-holt-analysis-standard-review.md) | 6 | ⏳ |
| **1.8** | 9 | `sync/standard-sync.md` | [holt-analysis](./2026-02-05-holt-analysis-standard-sync.md) | 6 | Применить → удалить → ✅ |
| **1.9** | 10 | `releases/standard-release.md` | [recommendations](./2026-02-03-recommendations-standard-release.md) | 7 | **Решить границу П7** → применить → удалить → ✅ |
| **1.10** | 10 | `releases/standard-release-workflow.md` | [recommendations](./2026-02-03-recommendations-standard-release-workflow.md) | 6 | **Решить границу П7** → применить → удалить → ✅ |

**Зависимости внутри фазы:**
- 1.9 и 1.10 обрабатывать ВМЕСТЕ (общая граница П7)
- 1.3 зависит от 1.2 (development ссылается на branching)
- 1.8 зависит от 1.2 (sync ссылается на branching)

---

### Последовательность: ОРКЕСТРАТОР

Обрабатывается ПОСЛЕДНИМ, после всех зависимых стандартов.

| Порядок | Стандарт | Файл рекомендаций | P1 | Действие |
|---------|----------|-------------------|-------|----------|
| **2.1** | `standard-github-workflow.md` | [recommendations](./2026-02-03-recommendations-standard-development-workflow.md) | 4 | Исправить П-1 + Ц-1 → применить → удалить → ✅ |

**Перед holt-анализом оркестратора:**
1. Исправить строку 113: `→ § 6. Стадия 4` → `→ standard-development.md`
2. Добавить шаг Security в Фазу 0 (после GitHub Actions)
3. Убедиться, что все SSOT-ссылки ведут на актуальные якоря

---

### Процесс для каждого стандарта

Все файлы рекомендаций уже созданы captain-holt (и `recommendations-*`, и `holt-analysis-*`).

```
1. Прочитать файл рекомендаций
2. Проверить на зональные вторжения → заменить SSOT-ссылками
3. Применить P1 (обязательно), P2 (если правка < 5 строк)
4. Удалить файл рекомендаций → стандарт валидирован
```

---

### Сводная таблица

| # | Стандарт | Фаза | Файл рекомендаций | Статус |
|---|----------|------|-------------------|--------|
| 0.5 | standard-milestone.md | Подготовка | recommendations (4 пункта) | ⏳ |
| 0.6 | standard-project.md | Подготовка | recommendations (6 пунктов) | ⏳ |
| 0.7 | standard-workflow-file.md | Подготовка | recommendations (8 пунктов) | ⏳ |
| 0.8 | standard-security.md | Подготовка | holt-analysis (3 P1) | ⏳ |
| 1.1 | standard-issue.md | Цикл | recommendations (6 пунктов) | ⏳ |
| 1.2 | standard-branching.md | Цикл | holt-analysis (10 P1) | ⏳ |
| 1.3 | standard-development.md | Цикл | holt-analysis (5 P1) | ⏳ |
| 1.4 | standard-commit.md | Цикл | holt-analysis (8 P1) | ⏳ |
| ~~1.5~~ | ~~standard-pull-request.md~~ | ~~Цикл~~ | *применены, удалён* | ✅ |
| 1.6 | standard-review.md | Цикл | holt-analysis (6 P1) | ⏳ |
| 1.8 | standard-sync.md | Цикл | holt-analysis (6 P1) | ⏳ |
| 1.9 | standard-release.md | Цикл | recommendations (7 пунктов) | ⏳ |
| 1.10 | standard-release-workflow.md | Цикл | recommendations (6 пунктов) | ⏳ |
| 2.1 | standard-github-workflow.md | Оркестратор | recommendations (4 пункта) | ⏳ |

**Итого:** 13 стандартов с файлами рекомендаций (применить → удалить), 1 уже валидирован (pull-request). `standard-draft-pr.md` влит в `standard-pull-request.md` и удалён.

---

## Открытые вопросы

1. **Security в Фазе 0** — добавить ли шаг "9. SECURITY" в ПОДГОТОВКУ workflow? (Dependabot, CodeQL, Secret Scanning, SECURITY.md)
2. **Validation-*.md** — паттерн П4 (отсутствие валидационных документов) фиксируется как отдельная задача или создаётся в процессе?
3. **Граница release ↔ release-workflow (П7)** — решать ДО или ПОСЛЕ применения рекомендаций?
