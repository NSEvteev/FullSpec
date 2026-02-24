# Воркфлоу инициализации проекта — инструкция + скилл

Единый процесс инициализации нового проекта, объединяющий три разрозненных процесса в один.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G1 из standard-process.md — Фаза 0 разрозненна, три процесса без оркестратора
**Почему создан:** Определить формат инструкции и скилла `/init-project` перед реализацией
**Связанные файлы:**
- `specs/.instructions/standard-process.md` — §4 Фаза 0
- `/.github/.instructions/standard-github-workflow.md` — §2 Фаза 0: Подготовка инфраструктуры
- `specs/.instructions/docs/standard-docs.md` — §7 Жизненный цикл (минимальный стартовый набор)
- `/.structure/initialization.md` — make setup

## Содержание

### Проблема

Фаза 0 состоит из трёх независимых шагов, каждый со своим SSOT:

| # | Шаг | SSOT | Текущий способ |
|---|-----|------|----------------|
| 0.1 | Настройка GitHub | standard-github-workflow.md §2 | Ручной: labels, issue templates, PR template, CODEOWNERS, Actions, Security — всё по отдельности |
| 0.2 | Настройка docs/ | standard-docs.md §7 | Ручной: создание README, .system/, .technologies/, примеров |
| 0.3 | Настройка среды | initialization.md | `make setup` |

Нет единой точки входа. Пользователь должен знать о трёх процессах и выполнять их вручную.

### Артефакты

По архитектуре проекта: **инструкция (SSOT) → скилл (обёртка)**. Скилл без SSOT-инструкции запрещён.

| # | Артефакт | Путь | Назначение |
|---|---------|------|------------|
| 1 | **Воркфлоу-инструкция** (SSOT) | `/.structure/.instructions/create-initialization.md` | Пошаговый процесс инициализации — шаги, чек-лист, примеры |
| 2 | **Скилл** (обёртка) | `/.claude/skills/init-project/SKILL.md` | Ссылка на SSOT, формат вызова `/init-project` |

Инструкция регистрируется в `/.structure/.instructions/README.md`.

> **Расположение:** `.structure/.instructions/` — потому что инициализация относится к структуре проекта, а не к GitHub или specs.

### Порядок создания

1. `/instruction-create create-initialization --path .structure/.instructions/` — инструкция
2. `/skill-create init-project` — скилл, SSOT → create-initialization.md

### Предлагаемая связка

**Инструкция:** `create-initialization.md` (SSOT — шаги, чек-лист, примеры)
**Скилл:** `/init-project` (обёртка — ссылка на SSOT, формат вызова)
**Тип:** Оркестратор (вызывает существующие скиллы и команды)

### Шаги инструкции (create-initialization.md)

```
/init-project [--skip-github] [--skip-docs] [--skip-setup]
```

| Шаг | Действие | Детали | Скилл/Команда |
|-----|---------|--------|---------------|
| 1 | Проверить prerequisites | Python 3.8+, pre-commit, gh, git | `python --version`, `pre-commit --version`, `gh --version` |
| 2 | Проверить gh auth | `gh auth status` | Если не авторизован — стоп с инструкцией |
| 3 | Настройка GitHub Labels | Создать/синхронизировать labels по labels.yml | `/labels-modify` |
| 4 | Настройка GitHub Security | Напомнить включить Dependabot, Secret Scanning (Settings не автоматизируются) | Вывод инструкции |
| 5 | Настройка Branch Protection | Предложить настроить через gh api | Вывод инструкции или `gh api` |
| 6 | Настройка docs/ | Стартовый набор: README, .system/, .technologies/ | Проверить наличие, создать недостающие |
| 7 | make setup | Pre-commit hooks, зависимости | `make setup` |
| 8 | Проверка | `pre-commit run --all-files` | Должно пройти |
| 9 | Отчёт | Что настроено, что нужно настроить вручную (Security Settings) | Вывод |

### Поведение при частичном выполнении

Скилл должен быть **идемпотентным**: если что-то уже настроено — пропустить с сообщением. Это позволяет запускать повторно для проверки.

### Зависимости от существующих скиллов

| Скилл | Для чего |
|-------|---------|
| `/labels-modify` | Шаг 3: создание labels |
| `/milestone-create` | Опционально: создание первого milestone |

### Что НЕ входит в скилл

- Создание сервисов (`/service-create`) — это Фаза 1, шаг 1.2 (Design → WAITING)
- Создание per-tech стандартов (`/technology-create`) — это Фаза 1, шаг 1.2
- Создание analysis chain — это `/discussion-create` (после инициализации)

## Решения

- **Инструкция → скилл:** create-initialization.md (SSOT) → /init-project (обёртка), по архитектуре проекта
- Скилл является оркестратором — не дублирует логику, вызывает существующие инструменты
- Шаги 4-5 (Security, Branch Protection) не полностью автоматизируемы — скилл выводит инструкции
- Issue Templates, PR Template, CODEOWNERS, Actions — уже в template, скилл проверяет наличие

## Открытые вопросы

- Нужно ли создавать первый Milestone в рамках инициализации?
- Как обрабатывать случай когда GitHub repo ещё не создан (только локальный git)?
- Нужен ли `--interactive` режим с пошаговым подтверждением каждого шага?

---

## Что уже описано в проекте

### Шаг 0.1 — Настройка GitHub (9 подшагов)

**SSOT:** `/.github/.instructions/standard-github-workflow.md` — §2 «Фаза 0: Подготовка инфраструктуры» (строки 160–204). Перечислены 9 пунктов в явном порядке:

| # | Подшаг | Что уже есть в template | Что нужно делать при инициализации | SSOT |
|---|--------|------------------------|-----------------------------------|------|
| 1 | Labels | `/.github/labels.yml` — 27 меток (TYPE: 4, PRIORITY: 4, STATUS: 4, AREA: 7, EFFORT: 5, ENV: 3) + SVC динамический | Синхронизировать `labels.yml` → GitHub через `python .github/.instructions/.scripts/sync-labels.py --apply` | `standard-labels.md` §11, `sync-labels.py` |
| 2 | CODEOWNERS | `/.github/CODEOWNERS` — уже настроен (все пути → @NSEvteev) | Проверить наличие, напомнить обновить при смене команды | `standard-codeowners.md` |
| 3 | Issue Templates | `/.github/ISSUE_TEMPLATE/` — 4 шаблона (`bug-report.yml`, `task.yml`, `docs.yml`, `refactor.yml`) + `config.yml` | Проверить наличие, валидировать: `python .github/.instructions/.scripts/validate-type-templates.py` | `standard-issue-template.md` §7 |
| 4 | PR Template | `/.github/PULL_REQUEST_TEMPLATE.md` — уже в template | Проверить наличие, валидировать: pre-commit hook `pr-template-validate` | `standard-pr-template.md` |
| 5 | Milestones | Нет (создаётся для каждого проекта индивидуально) | Опционально: `/milestone-create v0.1.0` — создать первый milestone | `standard-milestone.md`, `create-milestone.md`, скилл `/milestone-create` |
| 6 | GitHub Projects | Опционально (для команд 5+) | Только вывод инструкции — настройка через UI | `standard-project.md` (деактивирован) |
| 7 | GitHub Actions | `/.github/workflows/ci.yml` — pre-commit checks on push/PR, `/.github/workflows/codeql.yml` — CodeQL | Проверить наличие файлов | `standard-action.md` |
| 8 | Security | `/.github/dependabot.yml`, `/.github/workflows/codeql.yml`, `/.github/SECURITY.md` — файлы в template | **Settings НЕ копируются из template** — нужно включить вручную: (1) Dependabot alerts → Enable, (2) Dependabot security updates → Enable, (3) Secret scanning → Enable, (4) Push protection → Enable. Также: обновить email в SECURITY.md, обновить директории в dependabot.yml, обновить `matrix.language` в codeql.yml. НЕ включать Default Setup CodeQL | `standard-security.md` §7, `initialization.md` §6 |
| 9 | Pre-commit hooks | `/.pre-commit-config.yaml` — минимум 5 хуков (structure-sync, rules-validate, scripts-validate, skills-validate, pr-template-validate) + другие | `make setup` (pip install pre-commit, pre-commit install) | `initialization.md` §1 |

**Скрипт синхронизации labels (`sync-labels.py`):** Полноценный скрипт уже реализован (`/.github/.instructions/.scripts/sync-labels.py`, 312 строк). Умеет: загрузить `labels.yml` (с fallback на простой парсер без PyYAML), получить метки из GitHub через `gh label list`, вычислить diff (create/delete/update), показать план (dry-run) или применить (`--apply`, `--force`). Это основной инструмент для шага 3 (Labels) — вместо ручного `gh label create`.

**Скрипт валидации Issue Templates:** `/.github/.instructions/.scripts/validate-type-templates.py` — проверяет соответствие TYPE-меток из `labels.yml` и шаблонов в `.github/ISSUE_TEMPLATE/`.

### Шаг 0.2 — Настройка docs/

**SSOT:** `specs/.instructions/docs/standard-docs.md` — §7 «Жизненный цикл» (строки 366–409). Определяет минимальный стартовый набор:

**Обязательные документы (5 штук):**
- `specs/docs/README.md` — индекс сервисов + навигация
- `specs/docs/.system/overview.md` — архитектура системы
- `specs/docs/.system/conventions.md` — конвенции API и shared-интерфейсы
- `specs/docs/.system/infrastructure.md` — платформа и окружения
- `specs/docs/.system/testing.md` — стратегия тестирования

**Примеры (для шаблона):**
- `specs/docs/example.md` — пример per-service документа (10 секций)
- `specs/docs/.technologies/standard-example.md` — пример per-tech стандарта (8 секций)

**Текущее состояние template:** Все 7 файлов уже существуют в template (`specs/docs/README.md`, `specs/docs/example.md`, `specs/docs/.system/overview.md`, `specs/docs/.system/conventions.md`, `specs/docs/.system/infrastructure.md`, `specs/docs/.system/testing.md`, `specs/docs/.technologies/standard-example.md`). Скилл должен проверить наличие, а не создавать с нуля.

**Валидация:** `python specs/.instructions/.scripts/validate-docs.py` — проверяет наличие обязательных документов docs/, включён в pre-commit hook.

**Валидация архитектуры:** `python specs/.instructions/.scripts/validate-architecture.py --verbose` — проверяет 4 обязательных файла (`system/overview.md`, `system/data-flows.md`, `system/infrastructure.md`, `domains/context-map.md`), frontmatter и обязательные секции (описано в `initialization.md` строка 129–133).

### Шаг 0.3 — Настройка среды

**SSOT:** `/.structure/initialization.md` — полный документ (305 строк).

**`make setup` (Makefile, строки 42–65):** Три проверки: (1) `python --version`, (2) `pip install pre-commit && pre-commit install`, (3) `gh --version && gh auth status`. При ошибке — стоп с инструкцией.

**`make init` (Makefile, строка 67–69):** Вызывает `make setup` + placeholder `TODO: дополнительная инициализация (копирование .env.example и т.д.)`. Это готовая точка расширения — `/init-project` может превратить `make init` в полноценный оркестратор.

**Документ `initialization.md`:** Содержит 8 разделов: (1) Быстрый старт, (2) Зависимости (Python 3.8+, pre-commit, Git, gh CLI), (3) Установка вручную (Windows/macOS/Linux), (4) Проверка установки, (5) Решение проблем, (6) Настройка GitHub Security, (7) Настройка Branch Protection Rules, (8) Настройка GitHub Labels. Разделы 6–8 — ручные инструкции для Settings (с `gh api` командами для Branch Protection).

### Существующие скиллы-зависимости

| Скилл | Путь | Что делает | Как используется |
|-------|------|-----------|-----------------|
| `/labels-modify` | `/.claude/skills/labels-modify/SKILL.md` | Add/delete/rename/update метки с синхронизацией labels.yml. SSOT: `modify-labels.md`. Действия: `add-category`, `add-label`, `update`, `rename`, `rename-category`, `delete` | Шаг 3: создание/синхронизация labels |
| `/milestone-create` | `/.claude/skills/milestone-create/SKILL.md` | Создание Milestone по SemVer. SSOT: `create-milestone.md`. Параметры: `[version]`, `[--due <date>]` | Шаг 5 (опционально): первый milestone |
| `/labels-validate` | `/.claude/skills/labels-validate/SKILL.md` | Проверка labels.yml и меток на GitHub — аудит, синхронизация | Шаг 9: финальная проверка |

### Процесс поставки ценности — привязка к Фазе 0

**SSOT:** `specs/.instructions/standard-process.md` — §4 «Три пути (обзор)», подсекция «Фаза 0: Инициализация проекта» (строки 186–197):

> Выполняется **однократно** при создании проекта. Не зависит от пути — обязательный нулевой шаг.

Три подшага: 0.1 Настройка GitHub, 0.2 Настройка docs/, 0.3 Настройка среды. Указанные скиллы: `/labels-modify`, `/milestone-create`. Здесь же G1 в таблице пробелов (строка 511): «Нет единого `/init-project`» → этот драфт.

### Onboarding

**SSOT:** `/.claude/onboarding.md` — описывает «Первые шаги» (§2): прочитать CLAUDE.md → quick-start → artifacts → structure. Не упоминает Фазу 0 напрямую, но задаёт контекст — `/init-project` должен быть совместим с onboarding flow. Новый пользователь: (1) клонирует repo, (2) читает CLAUDE.md → видит `make setup`, (3) далее `/init-project` как расширенная инициализация.

### Что уже в template (не нужно создавать, только проверять)

| Артефакт | Путь | Статус |
|----------|------|--------|
| Issue Templates | `/.github/ISSUE_TEMPLATE/*.yml` | 4 шаблона + config.yml |
| PR Template | `/.github/PULL_REQUEST_TEMPLATE.md` | Есть |
| CODEOWNERS | `/.github/CODEOWNERS` | Есть, настроен |
| CI workflow | `/.github/workflows/ci.yml` | Есть |
| CodeQL workflow | `/.github/workflows/codeql.yml` | Нужно проверить наличие |
| Dependabot config | `/.github/dependabot.yml` | Нужно проверить наличие |
| SECURITY.md | `/.github/SECURITY.md` | Нужно проверить наличие, обновить email |
| Pre-commit config | `/.pre-commit-config.yaml` | Есть |
| Labels SSOT | `/.github/labels.yml` | 27 меток, нужна синхронизация с GitHub |
| Docs structure | `specs/docs/` | 7 файлов, нужна проверка наличия |

### Branch Protection — команды gh api

В `initialization.md` §7 (строки 243–280) приведены готовые команды:

```bash
# Просмотр текущих правил
gh api repos/{owner}/{repo}/branches/main/protection --method GET

# Настройка правил
gh api repos/{owner}/{repo}/branches/main/protection --method PUT \
  -f required_status_checks='{"strict":true,"contexts":["ci"]}' \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f enforce_admins=true \
  -f restrictions=null
```

Скилл может предложить выполнить эти команды автоматически (с подтверждением пользователя) или вывести их для ручного выполнения.

---

## Best practices

### Идемпотентность (Idempotent initialization)

Драфт уже указывает на идемпотентность (секция «Поведение при частичном выполнении»). Best practices усиливают это:

- **Check-before-act pattern:** Для каждого шага: (1) проверить текущее состояние, (2) если уже настроено — skip с сообщением `[SKIP] Labels: already synced (27/27)`, (3) если нет — выполнить. Это позволяет запускать `/init-project` повторно как healthcheck.
- **Идемпотентность sync-labels.py:** Скрипт уже реализует diff-подход (compute_diff) — создаёт только недостающие, удаляет только лишние, обновляет только расхождения. Не пересоздаёт существующие.
- **Idempotent file checks:** Проверка наличия файлов docs/ через `os.path.exists()` или `test -f` — не пересоздавать существующие, только сообщать об отсутствующих.

### Отчёт и прозрачность (Report-driven output)

- **Structured output:** Финальный отчёт в формате таблицы: шаг, статус (DONE / SKIP / MANUAL / FAIL), детали. Пример:

```
=== /init-project Report ===

| # | Step              | Status | Details                          |
|---|-------------------|--------|----------------------------------|
| 1 | Prerequisites     | DONE   | Python 3.12, pre-commit 4.x, gh 2.x |
| 2 | gh auth           | DONE   | Authenticated as @user           |
| 3 | Labels            | DONE   | Created 27, deleted 5 (default)  |
| 4 | Security Settings | MANUAL | Enable Dependabot, Secret Scanning in Settings |
| 5 | Branch Protection | MANUAL | Run `gh api ...` or configure in Settings |
| 6 | docs/             | SKIP   | All 7 files present              |
| 7 | make setup        | DONE   | Pre-commit hooks installed        |
| 8 | Verification      | DONE   | pre-commit run --all-files passed |
```

- **MANUAL items:** Для шагов, которые невозможно автоматизировать (GitHub Settings — Dependabot alerts, Secret Scanning, Push Protection), выводить пошаговую инструкцию с конкретными путями в UI (`Settings > Code security and analysis > ...`).

### Scaffolding patterns (cookiecutter-inspired)

- **Template variables:** Для файлов, требующих кастомизации (SECURITY.md email, dependabot.yml directories, codeql.yml languages), использовать паттерн detect-and-suggest: скилл обнаруживает placeholder/default значения и предлагает заменить, а не перезаписывает молча.
- **Selective generation:** Флаги `--skip-github`, `--skip-docs`, `--skip-setup` позволяют пропускать блоки целиком. Это полезно при повторном запуске — например, `--skip-setup` если hooks уже установлены.

### Error handling и graceful degradation

- **Non-blocking errors:** Если `gh` недоступен, скилл не должен падать целиком. Шаги, требующие `gh` (Labels, Branch Protection), помечаются как FAIL, но остальные шаги выполняются.
- **Prerequisite gating:** Проверка prerequisites (шаг 1) как gate — если Python или git не найден, стоп с инструкцией. Если `gh` не найден — продолжить без GitHub-шагов с предупреждением.
- **Timeout для API-вызовов:** `gh api` и `gh label` могут зависнуть при проблемах с сетью. Рекомендуется timeout 30 секунд на операцию.

### Separation of concerns (оркестратор vs. исполнители)

- **Thin orchestrator pattern:** Скилл `/init-project` не содержит логику — только последовательность вызовов. Логика синхронизации labels — в `sync-labels.py`. Логика проверки docs/ — в `validate-docs.py`. Логика установки — в `make setup`. Скилл координирует и собирает отчёт.
- **Delegation to existing tools:** Вместо дублирования — делегация. Labels → `sync-labels.py --apply --force`. Docs → `validate-docs.py`. Prerequisites → `make setup`. Это гарантирует, что при обновлении стандарта скилл автоматически использует актуальную логику.

### Обработка edge cases

- **Repo без remote:** Если `git remote -v` пуст, GitHub-шаги невозможны. Скилл должен обнаружить это на шаге 2 (`gh auth status` или `gh repo view`) и пометить все GitHub-шаги как SKIP с сообщением «No remote repository configured».
- **Repo не из template:** Если файлы template (Issue Templates, PR Template, CODEOWNERS) отсутствуют, скилл должен сообщить, какие файлы нужно создать — но не создавать их самостоятельно (это ответственность конкретных стандартов/скиллов).
- **Частично настроенный проект:** Самый частый сценарий — проект уже частично инициализирован. Идемпотентность + check-before-act обрабатывают этот случай естественно.

### Версионирование и расширяемость

- **Step registry:** Шаги инструкции описаны как таблица (уже в драфте). При добавлении нового шага (например, настройка GitHub Projects) — добавить строку в таблицу, реализовать check/act, обновить отчёт.
- **Hook points:** `make init` в Makefile (строка 67) уже содержит placeholder для расширения (`TODO: дополнительная инициализация`). `/init-project` может стать заменой или расширением `make init`.

### Удаление default GitHub labels

При создании нового репозитория (даже из template) GitHub может добавить свои default labels (bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix). `sync-labels.py` обрабатывает это через diff: метки, которые есть в GitHub, но отсутствуют в `labels.yml`, попадают в `delete`. Скилл должен явно предупредить пользователя о удалении default labels перед применением.

### Порядок выполнения шагов

Best practice: шаги, от которых зависят другие, выполняются первыми. Текущий порядок в драфте корректен:
1. Prerequisites (gate) — без них ничего не работает
2. gh auth (gate) — без него GitHub-шаги невозможны
3. Labels — нужны до создания Issues/Milestones
4-5. Security + Branch Protection — независимые, порядок не важен
6. docs/ — независимый
7. make setup — pre-commit hooks
8. Verification — финальный шаг, зависит от всех предыдущих
9. Report — итог
