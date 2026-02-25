# Скилл /release-create — оценка инструкции и план

Оценка полноты create-release.md и план создания скилла-обёртки.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G3 из standard-process.md — создать скилл `/release-create` по существующей инструкции
**Почему создан:** Определить, достаточна ли инструкция create-release.md для создания скилла или нужна доработка
**Связанные файлы:**
- `/.github/.instructions/releases/create-release.md` — SSOT-инструкция (кандидат)
- `/.github/.instructions/releases/standard-release.md` — стандарт Release
- `/.github/.instructions/releases/validation-release.md` — валидация Release
- `specs/.instructions/standard-process.md` — §5 Фаза 6 (Поставка)

## Содержание

### Оценка полноты create-release.md

**Вердикт: Инструкция достаточно полная.** Можно создавать скилл-обёртку без доработки SSOT. 

#### Что есть в инструкции (7 шагов)

| Шаг | Содержание | Полнота |
|-----|-----------|---------|
| 1. Определить версию | Из закрытого Milestone, OWNER/REPO | ✓ Полная |
| 2. Release Freeze | Организационная мера, предупреждение пользователю | ✓ Полная |
| 3. Pre-release валидация | `validate-pre-release.py --version $VERSION` | ✓ Полная |
| 4. Собрать Release Notes | Milestone URL + changelog + шаблон body | ✓ Полная |
| 5. Создать Release | `gh release create` с `--generate-notes` + `--notes-file` | ✓ Полная |
| 6. Синхронизировать CHANGELOG.md | Получить body → добавить секцию → закоммитить | ✓ Полная |
| 7. Post-release валидация | `validate-post-release.py --version $VERSION` | ✓ Полная |

#### Что есть дополнительно

- Чек-лист (9 пунктов)
- 3 примера (стандартный, hotfix, первый Release)
- 2 скрипта (validate-pre-release.py, validate-post-release.py)
- Обработка ошибок (СТОП при провале валидации)

#### Что отсутствует или требует внимания

| # | Пункт | Статус | Комментарий |
|---|-------|--------|-------------|
| 1 | Связь с analysis chain | Отсутствует | Инструкция не знает про analysis chain — нужно ли предлагать `/chain-done` перед Release? |
| 2 | Связь с Milestone validate | Частично | Шаг 1 проверяет Milestone, но не вызывает `/milestone-validate` |
| 3 | Draft Release поддержка | Есть | `--draft` флаг описан |
| 4 | Hotfix Release | Есть | Пример с `--skip-tests` |
| 5 | Скрипты существуют? | Неизвестно | Нужно проверить наличие validate-pre-release.py и validate-post-release.py |

### Артефакты

По архитектуре проекта: **инструкция (SSOT) → скилл (обёртка)**. Инструкция уже существует.

| # | Артефакт | Путь | Статус |
|---|---------|------|--------|
| 1 | **Инструкция** (SSOT) | `/.github/.instructions/releases/create-release.md` | **Существует** — полная, 7 шагов |
| 2 | **Скилл** (обёртка) | `/.claude/skills/release-create/SKILL.md` | **Нужно создать** |

### Формат вызова

```
/release-create [--draft] [--skip-tests]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `--draft` | Создать Draft Release | Нет |
| `--skip-tests` | Пропустить make test (для hotfix) | Нет |

### Порядок создания

1. `/skill-create release-create` — скилл, SSOT → create-release.md

Инструкция уже есть — создавать не нужно. Достаточно только скилла-обёртки.

### Рекомендации по доработке SSOT (опционально)

Если решим доработать create-release.md перед созданием скилла:

1. **Добавить шаг 0: Проверить analysis chain** — все цепочки в DONE? `/analysis-status` показывает чистый dashboard?
2. **Добавить вызов `/milestone-validate`** перед шагом 1 — формальная проверка milestone
3. **Проверить наличие скриптов** — validate-pre-release.py и validate-post-release.py могут не существовать

## Решения

- **Инструкция достаточна** — create-release.md содержит 7 шагов, чек-лист, примеры, скрипты
- **Скрипты существуют** — validate-pre-release.py (236 строк) и validate-post-release.py (303 строки) реализованы и работоспособны
- **Нужен Шаг 0** — добавить проверку analysis chain (все цепочки DONE) в create-release.md перед Шагом 1
- **release.yml** — создать `.github/release.yml` с метками `task` (не `feature`, метки `feature` нет в labels.yml)
- **Labels:** используем `task` вместо `feature` в release.yml и standard-release.md § 5
- **Milestone validate** — покрывается validate-pre-release.py (E004-E006), отдельный вызов не нужен
- **Нужен скилл** — `/skill-create release-create`, SSOT → create-release.md

## Открытые вопросы

*Все вопросы решены. Черновик готов к реализации.*

## Вынесено в отдельные драфты

Следующие темы выходят за рамки создания скилла /release-create и вынесены:

| Тема | Драфт | Что делать |
|------|-------|------------|
| deploy.yml workflow | `2026-02-25-deploy-workflow.md` | Стандарт + шаблон deploy.yml |
| Smoke tests / pre-release тесты | `2026-02-25-smoke-tests.md` | Формализация smoke tests |
| Security scan / dependency audit | `2026-02-25-security-scan.md` | Отдельный стандарт |
| Post-release validation расширение | `2026-02-25-post-release-validation.md` | Расширить standard-release.md § 11 |
| Feature freeze как технический блок | `2026-02-25-feature-freeze.md` | Branch protection механизм |

---

## Что уже описано в проекте

### Полный стек документации Release

Проект имеет **три уровня документации** для Releases:

| Уровень | Документ | Путь | Содержание |
|---------|----------|------|------------|
| Стандарт | standard-release.md | `/.github/.instructions/releases/standard-release.md` | 20 секций: SemVer, теги, changelog, жизненный цикл, подготовка, создание, публикация, hotfix, rollback, yanking, pre-release, draft, CLI команды, граничные случаи |
| Воркфлоу | create-release.md | `/.github/.instructions/releases/create-release.md` | 7 шагов: версия из Milestone, freeze, pre-release валидация, Release Notes (body), `gh release create`, синхронизация CHANGELOG.md, post-release валидация |
| Валидация | validation-release.md | `/.github/.instructions/releases/validation-release.md` | 6 шагов: готовность main, Milestone, объект Release, Release Notes, CHANGELOG.md, деплой. 11 кодов ошибок (E001-E011 pre, E001-E015 post) |

### Скрипты автоматизации (существуют и работоспособны)

| Скрипт | Путь | Проверки | Флаги |
|--------|------|----------|-------|
| validate-pre-release.py | `/.github/.instructions/.scripts/validate-pre-release.py` | Текущая ветка main, main синхронизирована с remote, нет critical PR, make test, Milestone существует/закрыт/нет open Issues, чистый working tree | `--version`, `--skip-tests`, `--json` |
| validate-post-release.py | `/.github/.instructions/.scripts/validate-post-release.py` | Объект Release (tag SemVer, title, body, draft, target=main), Git-тег, Release Notes (Milestone link, changelog, placeholders), CHANGELOG.md (существует, формат, версия), деплой (deploy.yml status) | `--version`, `--skip-deploy`, `--json` |

**Ответ на открытый вопрос #1:** Скрипты validate-pre-release.py и validate-post-release.py **существуют**, полностью реализованы (236 и 303 строк соответственно), покрывают все проверки из validation-release.md. Имеют коды ошибок E001-E008 (pre) и E001-E015 (post), поддерживают JSON-вывод.

### Формат CHANGELOG.md (уже создан)

Файл `/CHANGELOG.md` существует в корне проекта. Содержит:
- Заголовок `# Changelog`
- Ссылки на Keep a Changelog 1.1.0 и Semantic Versioning 2.0.0
- Секция `[Unreleased]`
- Релизов пока нет (файл готов к первому Release)

### Стандарт версионирования (SemVer)

Описан в standard-release.md SS 3 и delegирован к standard-milestone.md SS 4:
- Формат: `vMAJOR.MINOR.PATCH` (с префиксом `v`)
- Автоопределение из Conventional Commits: `fix:` = PATCH, `feat:` = MINOR, `BREAKING CHANGE:` = MAJOR
- Финальное решение о версии принимает человек на основе Milestone
- Pre-release формат: `v1.0.0-rc.1`, `v1.0.0-beta.1`

### Связь Release с Milestones

| Правило | Источник |
|---------|----------|
| Release создаётся ТОЛЬКО после закрытия Milestone | standard-release.md SS 1, SS 7 |
| Версия Release = Title Milestone | standard-release.md SS 3 |
| Release Notes обязательно содержат ссылку на Milestone URL | standard-release.md SS 7, validation-release.md шаг 4 |
| Milestone проверяется в pre-release валидации | validate-pre-release.py (E004-E006) |

### Связь Release с Analysis Chain (standard-process.md)

| Элемент | Описание |
|---------|----------|
| Фаза 6 (Поставка) | Шаг 6.1: `Release` — Milestone complete, changelog, tag, GitHub Release |
| Скилл в Фазе 6 | `/milestone-validate` (не `/release-create` — его пока нет) |
| Предшествующая фаза | Фаза 5 (Завершение): все цепочки в DONE, docs/ обновлён |
| Отсутствующий переход | Нет формальной проверки "все analysis chains в DONE" перед Release |

### Существующие связанные скиллы

| Скилл | Назначение | Релевантность для /release-create |
|-------|------------|-----------------------------------|
| `/milestone-validate` | Проверка Milestone (формат, Issues, статус) | Может вызываться как pre-check перед шагом 1 |
| `/milestone-modify` | Закрытие Milestone | Может вызываться если Milestone открыт |
| `/analysis-status` | Dashboard analysis chains | Может показать что не все chains в DONE |
| `/dev-create` | Пример скилла-обёртки | Референс для формата SKILL.md |

### Отсутствующая инфраструктура

| Элемент | Статус | Влияние |
|---------|--------|---------|
| `.github/release.yml` (кастомизация auto-generated notes) | Не существует | `--generate-notes` создаст плоский список PR без группировки. Опционально |
| `.github/workflows/deploy.yml` | Не существует | Post-release шаг 6 (деплой) будет пропускаться. `--skip-deploy` в validate-post-release.py |
| Скилл `/chain-done` (G11) | Не существует | Переход REVIEW -> DONE не автоматизирован скиллом. Указан как пробел в standard-process.md |

### Паттерн существующих скиллов-обёрток

Все скиллы в проекте следуют единому формату (из standard-skill.md):

```
---
name: {name}
description: {description}
allowed-tools: Read, Bash, Glob, Grep [, Write, Edit]
ssot-version: v1.0
argument-hint: {format}
---
# {Title}
**SSOT:** [{ssot-file}]({ssot-path})
## Формат вызова
## Воркфлоу
## Чек-лист
## Примеры
```

Скиллы минимальны: 30-50 строк, делегируют логику SSOT-инструкции. Пример: `/dev-create` (40 строк), `/milestone-validate` (48 строк).

## Best practices

### 1. Semantic Versioning (semver.org)

**Формат:** `MAJOR.MINOR.PATCH` (проект использует с префиксом `v`)

| Инкремент | Когда | Пример |
|-----------|-------|--------|
| MAJOR | Breaking changes — несовместимые изменения API | v1.0.0 -> v2.0.0 |
| MINOR | Новая функциональность, обратно совместимая | v1.0.0 -> v1.1.0 |
| PATCH | Исправления багов, обратно совместимые | v1.0.0 -> v1.0.1 |

**Дополнительные правила:**
- Pre-release: `v1.0.0-alpha.1`, `v1.0.0-beta.1`, `v1.0.0-rc.1` — имеют меньший приоритет чем стабильная версия
- Build metadata: `v1.0.0+20130313144700` — игнорируется при определении приоритета
- Версия 0.y.z — нестабильный API, breaking changes допустимы в MINOR
- Начальная разработка начинается с 0.1.0 (не с 0.0.1)
- После публикации конкретной версии содержимое НЕЛЬЗЯ изменять — любое изменение = новая версия

**Соответствие с проектом:** Полностью реализовано. standard-release.md SS 3 ссылается на standard-milestone.md SS 4 как SSOT для SemVer. Автоопределение из Conventional Commits описано.

### 2. Keep a Changelog (keepachangelog.com 1.1.0)

**Принципы:**
- Changelogs для людей, не для машин
- Каждая версия имеет свою запись
- Одинаковые типы изменений группируются
- Версии и секции linkable (могут быть ссылками)
- Последняя версия идёт первой
- Дата каждого Release указана в ISO 8601 (YYYY-MM-DD)
- Обязательная секция `[Unreleased]` для отслеживания текущих изменений

**Категории (в рекомендованном порядке):**
- `Added` — новая функциональность
- `Changed` — изменения существующей функциональности
- `Deprecated` — скоро удаляемая функциональность
- `Removed` — удалённая функциональность
- `Fixed` — исправления багов
- `Security` — исправления уязвимостей

**Соответствие с проектом:** Полностью реализовано. standard-release.md SS 5 описывает формат Keep a Changelog 1.1.0 с шаблоном, CHANGELOG.md создан по стандарту.

### 3. GitHub Releases — автогенерация и кастомизация

**Автогенерация (`--generate-notes`):**
- GitHub создаёт changelog автоматически из merged PR между предыдущим и текущим тегом
- Группировка по labels (если настроен `.github/release.yml`)
- Список contributors добавляется автоматически
- Ссылка на Full Changelog (compare view)

**Кастомизация через `.github/release.yml`:**
```yaml
changelog:
  categories:
    - title: Breaking Changes
      labels: [breaking-change]
    - title: Features
      labels: [feature]
    - title: Bug Fixes
      labels: [bug]
    - title: Documentation
      labels: [docs]
    - title: Other Changes
      labels: ["*"]
  exclude:
    labels: [skip-changelog]
```

**Комбинирование `--generate-notes` + `--notes-file`:** GitHub объединяет кастомный body (из файла) с автогенерированным списком PR. Кастомный body идёт ПЕРЕД автогенерацией. Проект уже использует этот подход в create-release.md шаг 5.

**Рекомендация:** Создать `.github/release.yml` для группировки PR по категориям. Без него `--generate-notes` создаёт плоский список.

### 4. Conventional Commits и автоматическое определение версии

**Стандарт:** `<type>[scope]: <description>`

| Тип | SemVer инкремент | Пример |
|-----|-----------------|--------|
| `fix:` | PATCH | `fix: утечка памяти в кэше` |
| `feat:` | MINOR | `feat: OAuth2 авторизация` |
| `feat!:` или `BREAKING CHANGE:` в footer | MAJOR | `feat!: новый формат API` |
| `docs:`, `chore:`, `refactor:`, `test:`, `ci:` | Нет | `docs: обновить README` |

**Инструменты автоматизации (индустрия):**
- **release-please** (Google) — создаёт PR с changelog и version bump при каждом push в main
- **semantic-release** — полная автоматизация: версия, changelog, npm publish, GitHub Release
- **commit-and-tag-version** — замена npm version, bumps + CHANGELOG генерация
- **commitlint + husky** — валидация формата коммитов (проект использует pre-commit hooks)

**Соответствие с проектом:** Проект использует Conventional Commits (standard-commit.md), pre-commit хуки для валидации. Автоопределение версии описано, но финальное решение за человеком.

### 5. Pre-release Validation Gates

**Индустриальные best practices — многоуровневые quality gates:**

| Gate | Проверки | В проекте |
|------|----------|-----------|
| Design Gate | Архитектура, feasibility | Analysis chain (Фаза 1) |
| Development Gate | Code review, linting, unit tests | `/principles-validate`, `/review` |
| Integration Gate | Code coverage, dependency scan, build | `make test`, `make lint` |
| Testing Gate | Regression, functional, performance | `make test`, `make test-e2e` |
| Deployment Gate | Readiness, environment, rollback plan | validate-pre-release.py |

**Конкретные проверки validate-pre-release.py (уже реализовано):**
1. Текущая ветка = main (E008)
2. Main синхронизирована с remote (E001)
3. Нет открытых critical PR (E002)
4. Тесты проходят — make test (E003, skippable)
5. Milestone существует, закрыт, нет open Issues (E004-E006)
6. Чистый working tree (E007)

**Чего не хватает (по сравнению с best practices):**
- Проверка analysis chain (все chains в DONE) — **отсутствует**
- Security scan / dependency audit — **отсутствует** (за пределами скоупа Release)
- Проверка что нет открытых Dependabot alerts — **отсутствует**
- Feature freeze формализация — описана как организационная мера, технически не блокируется

### 6. Post-release Validation и мониторинг

**Индустриальные best practices:**

| Проверка | Время | Описание |
|----------|-------|----------|
| Health check | Сразу | HTTP endpoint /health возвращает 200 |
| Smoke tests | 0-5 мин | Критичные user flows работают |
| Error rate monitoring | 15 мин | Error rate не вырос по сравнению с pre-release |
| Performance baseline | 30 мин | Latency, throughput в пределах нормы |
| Rollback readiness | Всегда | Предыдущая версия доступна, rollback план протестирован |

**Соответствие с проектом:** validate-post-release.py проверяет объект Release, Notes, CHANGELOG, деплой. Post-deploy verification описан в standard-release.md SS 11 (health check, smoke tests, monitoring). Rollback описан в SS 13 с критерием 30 минут.

### 7. Release Notes — что включать

**Рекомендации индустрии:**
- Номер версии и дата релиза
- Краткое summary назначения релиза
- Категоризированные изменения (features, fixes, deprecations, removals)
- Ссылка на Milestone/Sprint (для трекинга)
- Breaking changes выделены отдельно (важно для downstream)
- Известные проблемы (known issues)
- Ссылка на Full Changelog (compare view между тегами)
- Credits контрибьюторам

**Соответствие с проектом:** create-release.md шаг 4 описывает шаблон Release Notes с секциями Milestone, What's Changed, Breaking Changes, Full Changelog. Контрибьюторы добавляются автоматически через `--generate-notes`.

### 8. Squash Merge и чистая история для релизов

**Рекомендация:** Использовать squash merge для PR (один коммит = один PR). Это даёт:
- Чистую историю в main для `--generate-notes`
- Каждый PR-title становится строкой в changelog
- Упрощает revert (один коммит = один revert)

**Соответствие с проектом:** standard-review.md SS 3 определяет squash merge как стратегию. Используется в Фазе 4.4.

### 9. Release cadence и принятие решения

**Рекомендация:** Не создавать релиз после каждого merge. Агрегировать изменения и выпускать по:
- Расписанию (weekly/biweekly) — если есть смерженные PR
- Milestone completion — когда все Issues закрыты
- Hotfix — критический баг в production

**Соответствие с проектом:** standard-release.md SS 8 описывает критерии (достаточно изменений, deadline milestone, hotfix, регулярный релиз). Принятие решения человеком, не автоматически.

### 10. Идемпотентность и retry

**Рекомендация:** Release workflow должен быть идемпотентен — повторный запуск не должен создавать дубликаты. GitHub возвращает ошибку при попытке создать Release с существующим тегом.

**Соответствие с проектом:** standard-release.md SS 19 описывает граничный случай "Параллельное создание релизов" — проверка `gh release list --limit 1` перед созданием.
