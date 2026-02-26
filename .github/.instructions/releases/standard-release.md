---
description: Стандарт управления GitHub Releases — версионирование (SemVer), changelog, теги, артефакты.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/releases/README.md
---

# Стандарт Release

Версия стандарта: 1.1

Правила версионирования, создания Releases, управления changelog и полный процесс релиза: подготовка → создание → публикация → hotfix → rollback.

**Полезные ссылки:**
- [Инструкции Releases](./README.md)
- [Milestones](../milestones/standard-milestone.md) — связь с Milestones
- [Pull Requests](../pull-requests/standard-pull-request.md) — что попадает в Release
- [GitHub Workflow](../standard-github-workflow.md) — цикл разработки от Issue до Merge

**SSOT-зависимости:**
- [standard-milestone.md](../milestones/standard-milestone.md) — версионирование SemVer, связь Release-Milestone
- [standard-commit.md](../commits/standard-commit.md) — Conventional Commits для автоопределения версии, § 7 тип "revert" для rollback
- [standard-pull-request.md](../pull-requests/standard-pull-request.md) — PR, попадающие в Release
- [standard-action.md](../actions/standard-action.md) — CI/CD workflows для деплоя
- [standard-sync.md](../sync/standard-sync.md) — синхронизация main перед подготовкой Release
- [standard-issue.md](../issues/standard-issue.md) — связь Issues с Milestones (§ 9)
- [standard-branching.md](../branches/standard-branching.md) — hotfix-ветки, формат именования

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-release.md](./validation-release.md) |
| Создание | [create-release.md](./create-release.md) |
| Модификация | *Не требуется — операции описаны в § 18* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Свойства Release](#2-свойства-release)
- [3. Версионирование (SemVer)](#3-версионирование-semver)
- [4. Git-теги](#4-git-теги)
- [5. Changelog](#5-changelog)
- [6. Release как объект GitHub](#6-release-как-объект-github)
- [7. Связь с Milestones](#7-связь-с-milestones)
- [8. Жизненный цикл Release](#8-жизненный-цикл-release)
- [9. Подготовка релиза](#9-подготовка-релиза)
- [10. Создание релиза](#10-создание-релиза)
- [11. Публикация на production](#11-публикация-на-production)
- [12. Hotfix-релиз](#12-hotfix-релиз)
- [13. Rollback процесс](#13-rollback-процесс)
- [14. Yanking Release (отзыв версии)](#14-yanking-release-отзыв-версии)
- [15. Переход Pre-release - Stable](#15-переход-pre-release---stable)
- [16. Draft Release (черновик)](#16-draft-release-черновик)
- [17. Синхронизация CHANGELOG.md с Release](#17-синхронизация-changelogmd-с-release)
- [18. CLI команды](#18-cli-команды)
- [19. Граничные случаи](#19-граничные-случаи)
- [20. Скрипты](#20-скрипты)

---

## 1. Назначение

GitHub Release — публикация версии продукта с тегом, changelog и опциональными артефактами (бинарники, архивы).

**Применяется для:**
- Публикации стабильных версий продукта
- Документирования изменений между версиями
- Распространения бинарников и артефактов
- Привязки версии к конкретному коммиту (через Git-тег)

**Цель:**
- Создать snapshot кодовой базы на момент релиза
- Предоставить пользователям changelog с описанием изменений
- Обеспечить воспроизводимость деплоя (конкретная версия → конкретный коммит)

**Принципы:**

> **Merge в main ≠ деплой.** Код попадает в main после merge PR, но на production попадает ТОЛЬКО через Release.

> **Release — это решение, не событие.** Релиз создаётся явно (человеком), а не автоматически при merge в main.

> **Один Release = один Git-тег = один деплой.** Каждый релиз создаёт тег и триггерит деплой на production.

> **Hotfix — это тоже Release.** Hotfix создаётся как отдельный релиз с PATCH-версией (v1.0.0 → v1.0.1).

> **Release создаётся ТОЛЬКО после завершения всех Issues в связанном Milestone.**

> **Версионирование следует Semantic Versioning 2.0.0.**

### Зона ответственности

**Этот стандарт регулирует:**
- Свойства Release (версионирование, теги, changelog)
- Процесс релиза: подготовка → создание → публикация
- Hotfix-релизы (критичные исправления)
- Rollback процесс (откат релиза)

**НЕ регулирует:**

| Что | Где регулируется |
|-----|------------------|
| CI/CD workflows (`.yml` файлы) | [standard-action.md](../actions/standard-action.md) |
| Milestones (создание, закрытие) | [standard-milestone.md](../milestones/standard-milestone.md) |
| Issue → PR → Merge | [standard-github-workflow.md](../standard-github-workflow.md) |

---

## 2. Свойства Release

**Базовые свойства:**

| Свойство | Тип | Обязательно | Описание | Как установить |
|----------|-----|-------------|----------|----------------|
| `tag_name` | string | да | Git-тег (формат: `vX.Y.Z`) | позиционный аргумент |
| `name` | string | да | Человеко-читаемое название | `--title` |
| `body` | markdown | да | Changelog (описание изменений) | `--notes` / `--generate-notes` |
| `target_commitish` | string | нет | Коммит/ветка для тега (по умолчанию: HEAD main) | `--target` |
| `draft` | bool | нет | Черновик (не виден публично) | `--draft` |
| `prerelease` | bool | нет | Pre-release версия (alpha, beta, rc) | `--prerelease` |

**Дополнительные свойства:**

| Свойство | Тип | Описание | Как установить |
|----------|-----|----------|----------------|
| `created_at` | datetime | Дата создания (авто) | — |
| `published_at` | datetime | Дата публикации (авто) | — |
| `author` | user | Создатель (авто) | — |
| `assets` | file[] | Прикреплённые файлы (бинарники, архивы) | позиционные аргументы после тега |

**Пример:**

```json
{
  "tag_name": "v1.0.0",
  "name": "Release v1.0.0",
  "body": "## What's Changed\n- Add OAuth2 (#123)\n- Update API to v2 (#124)\n",
  "draft": false,
  "prerelease": false,
  "target_commitish": "main",
  "created_at": "2025-03-15T12:00:00Z",
  "assets": []
}
```

---

## 3. Версионирование (SemVer)

**SSOT:** [standard-milestone.md § 4](../milestones/standard-milestone.md#4-версионирование-semver)

Версия определяется при создании Milestone и наследуется Release. Формат, правила инкремента (MAJOR/MINOR/PATCH), pre-release, специальные случаи — см. SSOT.

### Автоопределение версии по Conventional Commits

Тип коммита (из [standard-commit.md](../commits/standard-commit.md)) определяет инкремент версии:

| Тип коммита | Инкремент SemVer | Пример |
|-------------|-----------------|--------|
| `fix:` | PATCH (x.y.**Z**) | `fix: исправить утечку памяти` |
| `feat:` | MINOR (x.**Y**.0) | `feat: добавить OAuth2` |
| `feat:` + `BREAKING CHANGE:` в footer | MAJOR (**X**.0.0) | `feat: новый формат API` |
| `refactor:`, `docs:`, `chore:` | Нет инкремента | — |

**Важно:** Автоопределение — ориентир. Финальное решение о версии принимает человек на основе Milestone.

---

## 4. Git-теги

Release создаёт Git-тег автоматически.

**Правила:**
- Один Release = один Git-тег
- Тег указывает на конкретный коммит в истории
- Тег НЕЛЬЗЯ переместить после создания (иначе теряется воспроизводимость)
- Имя тега совпадает с `tag_name` в Release

**Создание тега:**

```bash
# Автоматически через gh release create
gh release create v1.0.0 --title "Release v1.0.0" --notes "..."
# → создаст тег v1.0.0 на текущем коммите (HEAD main)

# С указанием целевой ветки
gh release create v1.0.0 --target develop --title "..." --notes "..."
# → создаст тег v1.0.0 на HEAD ветки develop
```

**Просмотр тегов:**

```bash
git tag                # Список всех тегов
git show v1.0.0        # Информация о теге
git rev-parse v1.0.0   # Коммит, на который указывает тег
```

**Удаление тега:**

> **ВНИМАНИЕ:** Удаление тега — операция, нарушающая воспроизводимость. Выполнять ТОЛЬКО в случае ошибки.

```bash
# Локально
git tag -d v1.0.0

# На удалённом репозитории
git push origin :refs/tags/v1.0.0
```

**Важно:** Перед удалением тега ОБЯЗАТЕЛЬНО удалить соответствующий GitHub Release (иначе тег восстановится).

---

## 5. Changelog

Changelog — описание изменений в Release.

### Release Notes vs CHANGELOG.md

| Аспект | Release Notes | CHANGELOG.md |
|--------|---------------|--------------|
| Расположение | GitHub UI (в Release) | Файл `/CHANGELOG.md` в репозитории |
| Формат | Markdown (свободный) | Keep a Changelog 1.1.0 |
| Генерация | `--generate-notes` (из PR) | Ручная или скрипт |
| Аудитория | Пользователи GitHub | Разработчики, пакетные менеджеры |
| Обновление | Автоматически при создании Release | Вручную после Release |

### Структура CHANGELOG.md

**Расположение:** `/CHANGELOG.md` (корень репозитория)

**Формат:** Keep a Changelog 1.1.0. Дата в формате ISO 8601 (`YYYY-MM-DD`).

```markdown
# Changelog

Все заметные изменения в этом проекте документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
версионирование следует [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Новая функциональность в разработке

## [1.1.0] - 2025-03-20

### Added
- Добавлен эндпоинт POST /api/auth/refresh (#145)
- Добавлена поддержка pagination для /api/users (#146)

### Changed
- Улучшена производительность GET /api/posts (#147)

### Fixed
- Исправлена ошибка 500 при загрузке больших файлов (#148)

## [1.0.0] - 2025-03-15

### Added
- Первый стабильный релиз
- OAuth2 авторизация (#123)
- API v2 (#124)

### Fixed
- Исправлена ошибка загрузки файлов (#125)

[unreleased]: https://github.com/owner/repo/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/owner/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/owner/repo/releases/tag/v1.0.0
```

**Принципы:**
- Новые версии добавляются сверху (над старыми)
- Каждая версия: `## [X.Y.Z] - YYYY-MM-DD` (ISO 8601)
- Секция `[Unreleased]` — для изменений в разработке
- Ссылки на Issues/PR в формате `(#123)`
- Ссылки внизу файла — рекомендуются, но опциональны
- Порядок секций: Added, Changed, Deprecated, Removed, Fixed, Security

### Автогенерация через GitHub

GitHub может автоматически создать changelog из PR между двумя тегами.

```bash
# Автогенерация при создании Release
gh release create v1.1.0 --generate-notes

# С кастомизацией диапазона
gh release create v1.1.0 --notes "$(gh api repos/{owner}/{repo}/releases/generate-notes \
  -f tag_name=v1.1.0 \
  -f target_commitish=main \
  -f previous_tag_name=v1.0.0 \
  -q .body)"
```

**Что генерируется:**
- Список PR между предыдущим тегом и текущим
- Группировка по меткам (если настроено в `.github/release.yml`)
- Список contributors

**Кастомизация через `.github/release.yml` — опциональна.** Без неё GitHub генерирует плоский список PR. Использовать, если требуется группировка PR по категориям.

**Пример `.github/release.yml`:**

```yaml
changelog:
  categories:
    - title: Features
      labels:
        - feature
    - title: Bug Fixes
      labels:
        - bug
    - title: Documentation
      labels:
        - docs
    - title: Other Changes
      labels:
        - "*"
```

### Категории изменений

**Рекомендуемые категории (Keep a Changelog):**

| Категория | Описание | Примеры |
|-----------|----------|---------|
| **Added** | Новая функциональность | Новые эндпоинты, фичи |
| **Changed** | Изменения существующей функциональности | Улучшения, рефакторинг |
| **Deprecated** | Функциональность, которая будет удалена | Предупреждение о будущих breaking changes |
| **Removed** | Удалённая функциональность | Удалённые эндпоинты, методы |
| **Fixed** | Исправления багов | Багфиксы |
| **Security** | Исправления уязвимостей | CVE, security patches |

**Соответствие категорий типам PR:**

| Категория | Метка PR | Тип в SemVer |
|-----------|----------|--------------|
| **Added** | `feature` | MINOR |
| **Changed** | `refactor` | MINOR |
| **Fixed** | `bug` | PATCH |
| **Removed** | `feature` + breaking | MAJOR |

**Важно:** Если в Release есть секция **Removed** или **Breaking changes** — версия ДОЛЖНА инкрементировать MAJOR.

---

## 6. Release как объект GitHub

Release — объект в GitHub, хранящий метаданные версии.

### Обязательные поля

| Поле | Формат | Пример |
|------|--------|--------|
| `tag_name` | `vX.Y.Z` | `v1.0.0` |
| `name` | `Release vX.Y.Z` | `Release v1.0.0` |
| `body` | Markdown | См. [5. Changelog](#5-changelog) |

### Опциональные поля

| Поле | Когда использовать | Пример |
|------|-------------------|--------|
| `draft` | Релиз не готов к публикации | `--draft` |
| `prerelease` | Pre-release версия (alpha, beta, rc) | `--prerelease` |
| `target` | Создать тег на другой ветке (не main) | `--target develop` |
| `assets` | Приложить бинарники/архивы | `./dist/*.zip` |

**Артефакты (assets):**

- Бинарники (для разных платформ: linux, windows, macos)
- Архивы с исходным кодом (GitHub создаёт автоматически: `.zip` и `.tar.gz`)
- Docker images (ссылка в body, сам образ в Docker Registry)
- Документация (PDF, HTML)

**Прикрепление артефактов:**

```bash
# При создании Release
gh release create v1.0.0 --notes "..." \
  ./dist/app-linux-amd64.tar.gz \
  ./dist/app-windows-amd64.zip

# К существующему Release
gh release upload v1.0.0 ./dist/app-macos-amd64.tar.gz
```

---

## 7. Связь с Milestones

Release ДОЛЖЕН быть связан с закрытым Milestone.

**Проверка Milestone перед созданием Release:**

```bash
OWNER="owner"
REPO="repo"
VERSION="v1.0.0"

# 1. Проверить существование Milestone
MILESTONE_NUMBER=$(gh api repos/$OWNER/$REPO/milestones --method GET -q ".[] | select(.title == \"$VERSION\") | .number")

if [ -z "$MILESTONE_NUMBER" ]; then
  echo "ERROR: Milestone $VERSION не найден"
  exit 1
fi

# 2. Проверить открытые Issues
OPEN_ISSUES=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER --method GET -q '.open_issues')

if [ "$OPEN_ISSUES" -gt 0 ]; then
  echo "ERROR: В Milestone есть $OPEN_ISSUES открытых Issues"
  gh issue list --milestone "$VERSION" --state open
  exit 1
fi

# 3. Закрыть Milestone (если открыт)
gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER -X PATCH -f state="closed"
```

**Что делать с незавершёнными Issues:** см. [standard-milestone.md § 8](../milestones/standard-milestone.md#8-закрытие-milestone)

**Ссылка на Milestone в Release Notes обязательна.** Получить URL:

```bash
MILESTONE_URL=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER --method GET -q '.html_url')
```

**Шаблон Release Notes:**

```markdown
## Milestone

Этот релиз основан на [Milestone v1.0.0]({MILESTONE_URL}).

**Прогресс:** 15/15 Issues завершено (100%)

## What's Changed

- Add OAuth2 (#123)
- Update API to v2 (#124)

## Breaking changes

*Нет*

**Full Changelog**: https://github.com/{owner}/{repo}/compare/v0.9.0...v1.0.0
```

---

## 8. Жизненный цикл Release

### Обзор

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   РЕШЕНИЕ    │ →  │  ПОДГОТОВКА  │ →  │   СОЗДАНИЕ   │ →  │  PRODUCTION  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                               │                    │
                                               │            ┌──────────────┐
                                               └─ ─ ─ ─ ─ →│   HOTFIX     │
                                                            └──────────────┘
```

### Полный цикл

```
1. РЕШЕНИЕ О РЕЛИЗЕ
   └─ Человек: "Делаем релиз"
   └─ Критерий: минимум 1 смерженный PR с момента последнего релиза ИЛИ deadline milestone

2. ПОДГОТОВКА РЕЛИЗА (§ 9)
   └─ Проверить main: нет открытых PR с меткой critical
   └─ Проверить тесты: make test пройдены локально
   └─ Определить версию: v1.0.0 (major.minor.patch)
   └─ Закрыть Milestone

3. СОЗДАНИЕ RELEASE В GITHUB (§ 10)
   └─ gh release create v1.0.0 --generate-notes
   └─ Тег создаётся автоматически (v1.0.0 → main HEAD)
   └─ Changelog генерируется автоматически (из PR titles)

4. ПУБЛИКАЦИЯ НА PRODUCTION (§ 11)
   └─ GitHub Actions триггерится событием "release published"
   └─ Деплой на сервер (docker pull, restart services)
   └─ Health check + Smoke tests

5. HOTFIX (§ 12, если production сломался)
   └─ Создать Issue с меткой critical
   └─ Создать ветку {NNNN}-hotfix-{topic}
   └─ Исправить → PR → merge в main
   └─ Создать hotfix-релиз: gh release create v1.0.1
   └─ Деплой на production (автоматически)

6. ROLLBACK (§ 13, если релиз критично сломал production)
   └─ Откатить деплой вручную (вернуть предыдущую версию)
   └─ Удалить проблемный релиз
   └─ Revert merge в main
```

### Связь с Development Workflow

| Workflow | Зона ответственности |
|----------|---------------------|
| **Development** | Issue → PR → Merge в main |
| **Release** | Main → Production |

```
main (код смержен) ≠ production (код доступен пользователям)

Development:  Issue → PR → Merge → main
                                    ↓
Release:                        Release → production
```

### Когда создавать релиз

**Решение принимает человек (не автоматически).**

| Критерий | Описание |
|----------|----------|
| **Достаточно изменений** | Минимум 1 смерженный PR с момента последнего релиза |
| **Deadline milestone** | Milestone завершён (все Issues закрыты) |
| **Критичный bugfix** | Hotfix должен попасть на production срочно |
| **Регулярный релиз** | По расписанию, ТОЛЬКО ЕСЛИ есть минимум 1 смерженный PR. Если изменений нет — релиз пропускается. |

**НЕ создавать релиз автоматически после каждого merge в main** — релизы контролируются вручную.

### Переходы состояний

- **Draft → Published:** `gh release edit v1.0.0 --draft=false`
- **Pre-release - Stable:** создать новый Release `v1.0.0` (см. [§ 15](#15-переход-pre-release---stable))

---

## 9. Подготовка релиза

### Критерии готовности

**Обязательные проверки перед созданием Release (СТРОГО последовательно):**

| # | Проверка | Команда | Ожидаемый результат |
|---|----------|---------|---------------------|
| 1 | **Main синхронизирована** | `git checkout main && git pull origin main` | Локальная main актуальна |
| 2 | **Нет критичных PR** | `gh pr list --label critical --state open` | Список пустой |
| 3 | **Тесты проходят** | `make test` | Все тесты пройдены |
| 4 | **Milestone закрыт** | См. [§ 7](#7-связь-с-milestones) | `state: closed`, `open_issues: 0` |
| 5 | **Нет незакоммиченных изменений** | `git diff --quiet` | Пустой вывод |

**Обработка ошибок:** Если хотя бы одна проверка не прошла → **ОСТАНОВИТЬ** процесс создания Release. Вернуть ошибку с указанием, какая проверка не прошла. Исправить проблему, затем повторить процесс с начала.

### Определение версии

**SSOT:** [standard-milestone.md § 4](../milestones/standard-milestone.md#4-версионирование-semver)

Версия определяется по правилам SemVer (MAJOR/MINOR/PATCH). Ориентир для инкремента — типы коммитов (см. [§ 3](#3-версионирование-semver)). Финальное решение — человек на основе Milestone.

### Release Freeze

Во время подготовки релиза действует freeze — запрет на merge PR в main.

**Процесс:**
1. Человек принимает решение: "Готовимся к релизу v1.0.0"
2. Freeze: НЕ мержить PR (кроме hotfix с меткой `critical`)
3. Выполнить проверки (таблица выше)
4. Создать Release
5. Freeze снят: можно мержить PR

**Важно:** Если PR смержен в main ПОСЛЕ решения о релизе, но ДО создания Release — этот PR попадёт в релиз (может быть нежелательно).

---

## 10. Создание релиза

### Процесс

```bash
# 1. Переключиться на main и обновить
git checkout main
git pull origin main

# 2. Создать релиз
gh release create v1.0.0 \
  --title "Release v1.0.0" \
  --generate-notes

# 3. GitHub автоматически:
# - Создаёт тег v1.0.0 на текущем HEAD main
# - Генерирует changelog из merged PR
# - Публикует релиз (status: published)
# - Триггерит GitHub Actions (deploy.yml)
```

### Обязательные элементы Release

| Элемент | Формат | Пример |
|---------|--------|--------|
| **Tag** | `v{MAJOR}.{MINOR}.{PATCH}` | `v1.0.0` |
| **Title** | `Release {tag}` | `Release v1.0.0` |
| **Notes** | Auto-generated + ссылка на Milestone | Changelog из PR |
| **Target** | `main` (всегда) | `main` |

### Два способа создания changelog

**Способ 1: Автогенерация (`--generate-notes`)**
- GitHub генерирует changelog автоматически из PR
- `gh release create v1.0.0 --generate-notes`

**Способ 2: Из файла CHANGELOG.md**
- Обновить CHANGELOG.md → закоммитить → создать Release:
  ```bash
  git add CHANGELOG.md
  git commit -m "docs: update changelog for v1.0.0"
  git push
  gh release create v1.0.0 --title "Release v1.0.0" -F CHANGELOG.md
  ```

**Важно:** Commit с обновлением CHANGELOG.md ДОЛЖЕН быть смержен в main ПЕРЕД созданием Release (иначе тег не будет содержать актуальный CHANGELOG).

### Проверка создания

```bash
# Проверить создание тега
git fetch --tags
git tag | grep v1.0.0

# Проверить Release
gh release view v1.0.0
```

---

## 11. Публикация на production

**SSOT:** [standard-deploy.md](../actions/deploy/standard-deploy.md)

Деплой выполняется автоматически при публикации Release через `deploy.yml`. Workflow использует dynamic service discovery — сканирует `src/*/Dockerfile`.

**Поток:** staging (auto) → smoke tests → production (manual approval) → health check → OK / rollback.

**Post-deploy verification:** health check (`GET /health`), smoke tests (`make test-smoke`), rollback при failure. Детали — в [standard-deploy.md](../actions/deploy/standard-deploy.md).

### Проверка после деплоя

```bash
# Просмотр запусков workflow
gh run list --workflow=deploy.yml

# Детали конкретного запуска
gh run view {run-id}
```

**Если деплой провалился** — rollback автоматический (redeploy предыдущего тега). Для ручного вмешательства см. [§ 13](#13-rollback-процесс) и [standard-deploy.md § 10](../actions/deploy/standard-deploy.md#10-rollback).

---

## 12. Hotfix-релиз

### Когда создавать hotfix

**Критерии:**
- Production сломался (критичный баг)
- Сервис недоступен или работает некорректно
- Требуется срочное исправление

### Процесс hotfix

```
1. СОЗДАТЬ ISSUE
   └─ gh issue create --title "Критичный баг: ..." --label bug --label critical

2. СОЗДАТЬ ВЕТКУ ОТ MAIN
   └─ git checkout main
   └─ git pull origin main
   └─ git checkout -b {NNNN}-hotfix-{topic}

3. ИСПРАВИТЬ БАГ
   └─ Внести изменения
   └─ Написать тесты (воспроизвести баг → исправить → проверить)
   └─ git commit -m "fix: {topic}"

4. СОЗДАТЬ PR
   └─ git push -u origin {NNNN}-hotfix-{topic}
   └─ gh pr create --title "fix: {description}" --body "Closes #{issue-number}" \
        --label bug --label critical

5. РЕВЬЮ (упрощённый процесс для hotfix)
   └─ Минимум 1 approval от другого разработчика (НЕ автор PR)
   └─ Self-approve ЗАПРЕЩЁН даже для hotfix
   └─ Проверить ТОЛЬКО: исправление бага, наличие теста, отсутствие breaking changes
   └─ gh pr review {PR-number} --approve
   └─ gh pr merge {PR-number} --squash

6. СОЗДАТЬ HOTFIX-РЕЛИЗ
   └─ git checkout main && git pull origin main
   └─ gh release create v1.0.1 --generate-notes
   └─ GitHub Actions деплоит на production автоматически

7. ПРОВЕРИТЬ PRODUCTION
   └─ Health check + Smoke tests (см. § 11)
```

**Важно:**
- Hotfix НЕ пропускает Issue и PR (даже для критичных багов)
- Hotfix-релиз создаётся как новый релиз с PATCH-версией (v1.0.0 → v1.0.1)
- Деплой происходит автоматически после создания релиза

### Критерий перехода к Rollback

Если hotfix невозможен в течение **30 минут** с момента обнаружения критичного бага — выполнить rollback ([§ 13](#13-rollback-процесс)). 30 минут — ориентировочное SLA для критичных багов, которое может быть скорректировано в зависимости от специфики проекта. После rollback — исправление без спешки.

### Множественные hotfix

**Объединять hotfix в один релиз если ВЫПОЛНЕНЫ ОБА условия:**
1. Баги обнаружены в течение 1 часа друг от друга
2. Баги НЕ блокируют друг друга (можно исправить параллельно)

Если хотя бы одно условие НЕ выполнено — создавать последовательные релизы (v1.0.1, v1.0.2).

---

## 13. Rollback процесс

### Когда делать rollback

**Критерии:**
- Релиз критично сломал production (сервис недоступен)
- Hotfix невозможен в течение 30 минут (см. [§ 12](#12-hotfix-релиз))
- Требуется немедленный откат к предыдущей версии

### Процесс rollback

```
1. ОТКАТИТЬ ДЕПЛОЙ (ВРУЧНУЮ)
   └─ Определить тип инфраструктуры: проверить файлы /.platform/docker/ или /.platform/kubernetes/
   └─ Выбрать команду rollback:
      - Docker: docker pull {image}:v0.9.0 && docker restart
      - Kubernetes: kubectl rollout undo deployment/{name}
      - SSH: rsync предыдущей версии на сервер

2. ОПРЕДЕЛИТЬ ПРОБЛЕМНУЮ ВЕРСИЮ
   └─ gh release list --limit 1
   └─ PROBLEM_VERSION=v1.0.0

3. УДАЛИТЬ ПРОБЛЕМНЫЙ РЕЛИЗ
   └─ gh release delete $PROBLEM_VERSION --yes
   └─ gh api repos/{owner}/{repo}/git/refs/tags/$PROBLEM_VERSION -X DELETE

4. REVERT MERGE В MAIN
   └─ git checkout main
   └─ git pull origin main
   └─ git log --oneline -10   # Найти commit merge проблемного PR
   └─ git revert {commit-hash}
   └─ git push origin main

5. СОЗДАТЬ ISSUE ДЛЯ ИСПРАВЛЕНИЯ
   └─ gh issue create --title "Исправить проблему релиза v1.0.0" \
        --label bug --label critical

6. ИСПРАВИТЬ ПРОБЛЕМУ
   └─ Создать ветку {NNNN}-hotfix-{topic}
   └─ Исправить баг → PR → merge
   └─ Создать новый релиз v1.0.1 (после исправления)
```

**Важно:**
- Rollback НЕ отменяет историю Git (создаётся revert-коммит)
- Проблемный релиз удаляется из GitHub Releases
- После rollback создаётся новый релиз с исправлением (не переиспользуется старый тег)

### Альтернатива: откат через GitHub UI

```bash
# 1. Открыть проблемный PR в GitHub
gh pr view {PR-number} --web

# 2. В UI GitHub нажать "Revert" (создаст revert-PR)

# 3. Смержить revert-PR
gh pr merge {revert-PR-number} --squash

# 4. Создать новый релиз
gh release create v1.0.1 --generate-notes
```

### Rollback к старой версии (релиз удалён)

**Сценарий:** Релиз удалён из GitHub Releases, но тег существует в Git.

1. Найти последний стабильный тег:
   ```bash
   git tag --sort=-version:refname | grep -v 'rc\|beta\|alpha' | head -1
   ```

2. Деплоить версию по тегу (напрямую, без создания Release):
   ```bash
   gh workflow run deploy.yml --ref v0.9.0
   ```

**Важно:** Это альтернативный путь для экстренных случаев.

---

## 14. Yanking Release (отзыв версии)

**Когда применять:**
- Release содержит уязвимость (CVE)
- Release содержит баг, ломающий критичную функциональность

**Процедура:**

1. Обновить Release Notes с предупреждением:
   ```bash
   gh release edit v1.0.0 --notes "**YANKED:** Содержит уязвимость CVE-2025-1234. Используйте v1.0.1 или новее.

   $(gh release view v1.0.0 --json body -q .body)"
   ```

2. Пометить Release как pre-release (чтобы скрыть из "Latest"):
   ```bash
   gh release edit v1.0.0 --prerelease
   ```

3. Создать Issue с описанием проблемы

4. Выпустить PATCH-релиз с исправлением (v1.0.1)

**Важно:** Yanked Release НЕ удаляется — сохраняется история, но пользователи предупреждены.

---

## 15. Переход Pre-release - Stable

**Когда применять:**
- Pre-release версия (`v1.0.0-rc.1`) протестирована и готова к публикации

**НЕ рекомендуется:**
```bash
gh release edit v1.0.0-rc.1 --prerelease=false  # тег остаётся -rc.1
```

**Рекомендуется:**

1. Создать новый Release с тегом `v1.0.0`:
   ```bash
   gh release create v1.0.0 --title "Release v1.0.0" --generate-notes
   ```

2. (Опционально) Пометить pre-release как устаревший:
   ```bash
   gh release edit v1.0.0-rc.1 --notes "Заменён стабильным релизом v1.0.0"
   ```

**Почему:** Тег `v1.0.0-rc.1` указывает на другой коммит, чем `v1.0.0`. Изменение флага `--prerelease=false` не меняет тег.

---

## 16. Draft Release (черновик)

**Когда использовать:**
- Release готовится заранее (за несколько дней до публикации)
- Требуется подготовить changelog и артефакты до официального анонса

**Создание draft:**
```bash
gh release create v1.0.0 --title "Release v1.0.0" --notes "WIP" --draft
```

**Публикация draft:**

1. Обновить Release Notes:
   ```bash
   gh release edit v1.0.0 --notes "$(cat CHANGELOG.md)"
   ```

2. Снять флаг draft:
   ```bash
   gh release edit v1.0.0 --draft=false
   ```

3. Деплой на production (автоматически через CI/CD при публикации)

**Важно:** Draft Release НЕ виден публично и НЕ триггерит workflows с `types: [published]`.

---

## 17. Синхронизация CHANGELOG.md с Release

**После создания Release с автогенерацией:**

1. Скопировать Release Notes в CHANGELOG.md:
   ```bash
   # Получить body Release
   gh release view v1.0.0 --json body -q .body > release-notes.tmp

   # Вручную отредактировать и добавить в CHANGELOG.md
   # (добавить заголовок ## [1.0.0] - YYYY-MM-DD)
   ```

2. Закоммитить:
   ```bash
   git add CHANGELOG.md
   git commit -m "docs: update changelog for v1.0.0"
   git push
   ```

**Важно:** Коммит с CHANGELOG.md НЕ попадёт в тег v1.0.0 (тег уже создан). Это нормально — CHANGELOG.md обновляется для будущих версий и документации.

---

## 18. CLI команды

### Создание Release

```bash
# Базовое создание
gh release create v1.0.0 --title "Release v1.0.0" --notes "Changelog..."

# С автогенерацией changelog
gh release create v1.0.0 --generate-notes

# Из файла CHANGELOG.md
gh release create v1.0.0 -F CHANGELOG.md

# Черновик (draft)
gh release create v1.0.0 --draft --notes "WIP"

# Pre-release
gh release create v1.0.0-beta.1 --prerelease --notes "..."

# С артефактами
gh release create v1.0.0 --notes "..." ./dist/*.zip

# На другой ветке
gh release create v1.0.0 --target develop --notes "..."
```

### Просмотр Release

```bash
gh release list                                  # Список всех Releases
gh release view v1.0.0                           # Детали конкретного Release
gh release download v1.0.0                       # Скачать артефакты
gh release download v1.0.0 -p "app-*.tar.gz"     # Скачать конкретный артефакт
```

### Редактирование Release

```bash
gh release edit v1.0.0 --title "New title"       # Изменить title
gh release edit v1.0.0 --notes "Updated changelog" # Обновить body
gh release edit v1.0.0 --draft=false             # Снять draft
gh release edit v1.0.0 --prerelease=false        # Пометить как stable
gh release upload v1.0.0 ./dist/new-file.zip     # Добавить артефакты
```

### Удаление Release

**Когда можно удалить:** Release создан по ошибке (draft), версия некорректная.

**Когда НЕЛЬЗЯ удалить:** Release уже опубликован и используется (нарушение воспроизводимости).

```bash
# 1. Удалить Release
gh release delete v1.0.0 --yes

# 2. Удалить Git-тег
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

**Важно:** Удаление Release НЕ удаляет Milestone и Issues.

---

## 19. Граничные случаи

### Релиз с пустым changelog

**Сценарий:** `--generate-notes` не находит PR (первый релиз или все изменения через direct commits).

**Решение:**
- Для первого релиза: написать changelog вручную с `--notes "Initial release"`
- Direct commits не попадают в автогенерацию — использовать ручной changelog (`-F CHANGELOG.md`)

### Релиз с draft PR

**Сценарий:** В main смержены PR, но есть открытый Draft PR.

**Решение:** Draft PR НЕ влияет на релиз (не смержен в main). Создать релиз как обычно. Draft PR попадёт в следующий релиз.

### Hotfix без предварительного Milestone

**Сценарий:** Критический баг в production — нужен срочный hotfix-релиз.

**Решение:**
- Создать Milestone `vX.Y.Z` (hotfix-версия) с одним Issue
- Закрыть Issue и Milestone
- Создать Release по стандартному процессу (§ 9–10)

### Множественные релизы в день

**Сценарий:** Создано несколько hotfix за день (v1.0.1, v1.0.2, v1.0.3).

**Решение:** Каждый hotfix — отдельный релиз, версия инкрементируется последовательно. **НЕ перезаписывать теги.**

### Откат нескольких релизов

**Сценарий:** Релизы v1.0.0, v1.0.1, v1.0.2 все сломаны, нужно откатиться к v0.9.0.

**Процесс:**
1. Откатить деплой вручную к v0.9.0
2. Удалить проблемные релизы:
   ```bash
   gh release delete v1.0.0 --yes
   gh release delete v1.0.1 --yes
   gh release delete v1.0.2 --yes
   ```
3. Revert merge в **обратном хронологическом порядке** (от НОВЫХ к СТАРЫМ):
   ```bash
   git revert {commit-hash-v1.0.2}   # Сначала последний
   git revert {commit-hash-v1.0.1}
   git revert {commit-hash-v1.0.0}   # Затем первый
   git push origin main
   ```
   **ВАЖНО:** Порядок критичен для предотвращения merge-конфликтов.
4. Создать новый релиз v1.0.0 (после исправления проблем)

### Релиз с breaking changes

**Сценарий:** Релиз содержит несовместимые изменения API.

**Процесс:**
1. Увеличить MAJOR версию (v1.0.0 → v2.0.0)
2. В changelog явно указать breaking changes:
   ```markdown
   ## Breaking Changes
   - API endpoint `/api/v1/users` удалён (используйте `/api/v2/users`)
   ```
3. Создать релиз: `gh release create v2.0.0 --generate-notes`

### Hotfix для старой версии

**Сценарий:** Production на v1.0.0, main на v1.1.0, нужен hotfix для v1.0.0.

**Процесс (НЕ поддерживается в текущей модели):**
- Текущая модель: один production, один main
- Hotfix всегда создаётся от текущего main
- Если нужен hotfix для старой версии → обновить production до v1.1.0, затем создать hotfix v1.1.1

### Pre-release (тестовый релиз)

**Сценарий:** Нужно протестировать релиз на staging без деплоя в production.

**Процесс:**
1. `gh release create v1.0.0-rc1 --prerelease --title "Release Candidate 1" --generate-notes`
2. Pre-release НЕ триггерит деплой на production (workflow должен проверять `!prerelease`)
3. После тестирования — создать стабильный Release `v1.0.0` (см. [§ 15](#15-переход-pre-release---stable))

### Параллельное создание релизов

**Сценарий:** Два разработчика одновременно создают v1.0.0.

**Решение:**
1. Перед созданием проверить: `gh release list --limit 1`
2. Если версия существует → инкрементировать
3. GitHub вернёт ошибку при попытке создать релиз с существующим тегом

**Координируйте создание релизов в команде** (один человек отвечает за релизы).

---

## 20. Скрипты

*Нет скриптов.*
