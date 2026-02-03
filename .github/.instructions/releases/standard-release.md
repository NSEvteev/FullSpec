---
description: Стандарт управления GitHub Releases
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/releases/README.md
---

# Стандарт Release

Версия стандарта: 1.0

Правила версионирования, создания Releases и управления changelog.

**Полезные ссылки:**
- [Инструкции Releases](./README.md)
- [Milestones](../milestones/standard-milestone.md) — связь с Milestones
- [Pull Requests](../pull-requests/standard-pull-request.md) — что попадает в Release

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | *Будет создан* |
| Создание | *Будет создан* |
| Модификация | *Будет создан* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Свойства Release](#2-свойства-release)
- [3. Версионирование (SemVer)](#3-версионирование-semver)
  - [Правила инкремента версий](#правила-инкремента-версий)
  - [Pre-release версии](#pre-release-версии)
  - [Специальные случаи](#специальные-случаи)
- [4. Git-теги](#4-git-теги)
- [5. Changelog](#5-changelog)
  - [Структура CHANGELOG.md](#структура-changelogmd)
  - [Автогенерация через GitHub](#автогенерация-через-github)
  - [Категории изменений](#категории-изменений)
- [6. Release как объект GitHub](#6-release-как-объект-github)
  - [Обязательные поля](#обязательные-поля)
  - [Опциональные поля](#опциональные-поля)
- [7. Связь с Milestones](#7-связь-с-milestones)
- [8. Жизненный цикл Release](#8-жизненный-цикл-release)
- [9. CLI команды](#9-cli-команды)
- [10. Правила создания Release](#10-правила-создания-release)
- [11. Yanking Release (отзыв версии)](#11-yanking-release-отзыв-версии)
- [12. Переход Pre-release → Stable](#12-переход-pre-release--stable)
- [13. Draft Release (черновик)](#13-draft-release-черновик)
- [14. Синхронизация CHANGELOG.md с Release](#14-синхронизация-changelogmd-с-release)

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
- Один Release = один Git-тег
- Release создаётся ТОЛЬКО после завершения всех Issues в связанном Milestone
- Версионирование следует Semantic Versioning 2.0.0
- Changelog должен быть информативным и структурированным

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

**Примеры:**

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

Release следует [Semantic Versioning 2.0.0](https://semver.org/).

**Формат:** `vMAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

| Элемент | Правило | Пример |
|---------|---------|--------|
| `v` | Префикс (ОБЯЗАТЕЛЬНО) | `v` |
| `MAJOR` | Версия с breaking changes | `1` |
| `MINOR` | Версия с новой функциональностью (обратно совместимо) | `2` |
| `PATCH` | Версия с исправлениями (обратно совместимо) | `3` |
| `PRERELEASE` | Опциональный суффикс для pre-release | `-alpha`, `-beta.1`, `-rc.2` |
| `BUILD` | Опциональный build metadata | `+20250315` |

**Примеры:**
- `v1.0.0` — первый стабильный релиз
- `v1.1.0` — добавлена новая функциональность
- `v1.1.1` — исправлен баг
- `v2.0.0` — breaking changes (несовместимо с v1.x.x)
- `v1.0.0-alpha` — alpha-версия перед v1.0.0
- `v1.0.0-beta.2` — вторая beta-версия
- `v1.0.0-rc.1` — первый release candidate

### Правила инкремента версий

**MAJOR (X.0.0):** Увеличивается при breaking changes.

**Breaking changes — изменения, которые:**
- Нарушают обратную совместимость API (изменился формат запроса/ответа)
- Требуют изменений от пользователей/клиентов API
- Удаляют публичные методы/эндпоинты
- Меняют поведение существующих методов несовместимым образом

**Примеры:**
- Удаление эндпоинта `DELETE /api/v1/users`
- Изменение формата ответа `{ "user": {} }` → `{ "data": {} }`
- Переименование обязательного поля в запросе

**MINOR (x.Y.0):** Увеличивается при добавлении новой функциональности (обратно совместимо).

**Новая функциональность — изменения, которые:**
- Добавляют новые эндпоинты/методы
- Добавляют опциональные параметры
- Добавляют новые поля в ответ (не удаляя старые)
- Улучшают существующую функциональность без нарушения совместимости

**Примеры:**
- Добавление эндпоинта `POST /api/v1/auth/refresh`
- Добавление опционального параметра `?page_size=20`
- Добавление поля `created_at` в ответ (старые поля остаются)

**PATCH (x.y.Z):** Увеличивается при исправлении багов (обратно совместимо).

**Багфиксы — изменения, которые:**
- Исправляют некорректное поведение
- Не добавляют новой функциональности
- Не меняют публичный API

**Примеры:**
- Исправление ошибки 500 при загрузке файлов
- Исправление опечатки в тексте ошибки
- Исправление утечки памяти

**Когда сбрасывать младшие версии:**
- При инкременте MAJOR — MINOR и PATCH сбрасываются в 0: `v1.5.3` → `v2.0.0`
- При инкременте MINOR — PATCH сбрасывается в 0: `v1.5.3` → `v1.6.0`

### Pre-release версии

**Формат:** `vX.Y.Z-{identifier}.{number}`

| Тип | Формат | Когда использовать | Пример |
|-----|--------|-------------------|--------|
| **alpha** | `vX.Y.Z-alpha` или `vX.Y.Z-alpha.N` | Ранняя версия для внутреннего тестирования | `v1.0.0-alpha`, `v1.0.0-alpha.1` |
| **beta** | `vX.Y.Z-beta` или `vX.Y.Z-beta.N` | Версия для публичного тестирования | `v1.0.0-beta`, `v1.0.0-beta.2` |
| **rc** | `vX.Y.Z-rc.N` | Release Candidate (финальное тестирование перед релизом) | `v1.0.0-rc.1` |

**Правила:**
- Pre-release идёт ПЕРЕД стабильным релизом: `v1.0.0-alpha` → `v1.0.0-beta` → `v1.0.0-rc.1` → `v1.0.0`
- Нумерация начинается с 1: `v1.0.0-alpha.1`, `v1.0.0-beta.1`
- Pre-release помечается флагом `--prerelease` при создании Release

**Сортировка версий (по возрастанию):**
```
v1.0.0-alpha
v1.0.0-alpha.1
v1.0.0-beta
v1.0.0-beta.1
v1.0.0-rc.1
v1.0.0
v1.0.1
v1.1.0
v2.0.0
```

### Специальные случаи

**Версия 0.x.x (начальная разработка):**
- До первого стабильного релиза используются версии `v0.x.x`
- Версия `v0.x.x` НЕ гарантирует обратную совместимость
- Первый стабильный релиз — `v1.0.0`

**Примеры:**
- `v0.1.0` — первая рабочая версия (MVP)
- `v0.2.0` — добавлена авторизация
- `v0.2.1` — исправлен баг в авторизации
- `v1.0.0` — первый стабильный релиз

**Build metadata (+):**
- Опционален для GitHub Releases. НЕ используется в стандартной практике проекта.
- Примеры применения (если потребуется в будущем): `v1.0.0+20250315`, `v1.0.0+sha.abc123`
- По умолчанию: тег Release содержит ТОЛЬКО `vX.Y.Z` без build metadata.

**Примеры:**
- `v1.0.0+20250315` — build от 15 марта 2025
- `v1.0.0+sha.abc123` — build с коммитом abc123

**Важно:** Build metadata НЕ используется для определения старшинства версий. `v1.0.0+build1` == `v1.0.0+build2`.

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
# Список всех тегов
git tag

# Информация о теге
git show v1.0.0

# Коммит, на который указывает тег
git rev-parse v1.0.0
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

### Структура CHANGELOG.md

**Расположение:** `/CHANGELOG.md` (корень репозитория)

**Формат:** Keep a Changelog 1.1.0

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
- Каждая версия имеет заголовок `## [X.Y.Z] - YYYY-MM-DD`
- Секция `[Unreleased]` — для изменений в разработке
- Ссылки на Issues/PR в формате `(#123)`

### Автогенерация через GitHub

GitHub может автоматически создать changelog из PR между двумя тегами.

**Команда:**

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

**Пример автогенерированного changelog:**

```markdown
## What's Changed
* Add OAuth2 by @user1 in https://github.com/owner/repo/pull/123
* Update API to v2 by @user2 in https://github.com/owner/repo/pull/124
* Fix file upload by @user1 in https://github.com/owner/repo/pull/125

## New Contributors
* @user2 made their first contribution in https://github.com/owner/repo/pull/124

**Full Changelog**: https://github.com/owner/repo/compare/v0.9.0...v1.0.0
```

**Кастомизация через `.github/release.yml` — опциональна.** Использовать, если:
- Требуется группировка PR по категориям в changelog
- Нужны нестандартные названия секций

Если кастомизация не нужна — GitHub сгенерирует плоский список PR.

**Пример `.github/release.yml`:**

```yaml
changelog:
  categories:
    - title: 🚀 Features
      labels:
        - type:feature
    - title: 🐛 Bug Fixes
      labels:
        - type:bug
    - title: 📚 Documentation
      labels:
        - type:docs
    - title: 🔧 Other Changes
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
| **Added** | `type:feature` | MINOR |
| **Changed** | `type:refactor` | MINOR |
| **Fixed** | `type:bug` | PATCH |
| **Removed** | `type:feature` + breaking | MAJOR |

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

**Примеры:**

```bash
# Стандартный релиз
gh release create v1.0.0 \
  --title "Release v1.0.0" \
  --notes "$(cat CHANGELOG.md)"

# Черновик (draft)
gh release create v1.1.0 \
  --title "Release v1.1.0" \
  --notes "WIP" \
  --draft

# Pre-release
gh release create v1.0.0-beta.1 \
  --title "Release v1.0.0 Beta 1" \
  --notes "..." \
  --prerelease

# С артефактами
gh release create v1.0.0 \
  --title "Release v1.0.0" \
  --notes "..." \
  ./dist/app-linux-amd64.tar.gz \
  ./dist/app-windows-amd64.zip
```

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

**Пример с Docker:**

```markdown
## Docker

```bash
docker pull ghcr.io/owner/repo:v1.0.0
```
```

---

## 7. Связь с Milestones

**Правило:** Release ДОЛЖЕН быть связан с закрытым Milestone.

### Процесс создания Release из Milestone

1. **Milestone создан:** `v1.0.0` (тип: Release Milestone)
2. **Issues завершены:** Все Issues в Milestone закрыты
3. **Milestone закрыт:**
   ```bash
   gh api PATCH /repos/{owner}/{repo}/milestones/{number} -f state=closed
   ```
4. **Release создан:**
   ```bash
   gh release create v1.0.0 \
     --title "Release v1.0.0" \
     --notes "См. Milestone: [v1.0.0](https://github.com/{owner}/{repo}/milestone/{number})\n\n$(gh release view --json body -q .body)"
   ```

**Переменные окружения:**

```bash
OWNER="owner"  # Заменить на имя владельца репозитория
REPO="repo"    # Заменить на имя репозитория
VERSION="v1.0.0"  # Версия создаваемого Release
```

**Проверка перед созданием Release:**

```bash
# 1. Проверить существование Milestone
MILESTONE_NUMBER=$(gh api repos/$OWNER/$REPO/milestones -q ".[] | select(.title == \"$VERSION\") | .number")

if [ -z "$MILESTONE_NUMBER" ]; then
  echo "ERROR: Milestone $VERSION не найден"
  exit 1
fi

# 2. Проверить статус Milestone
MILESTONE_STATE=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER -q '.state')

if [ "$MILESTONE_STATE" != "closed" ]; then
  echo "ERROR: Milestone должен быть закрыт перед созданием Release"
  exit 1
fi

# 3. Проверить открытые Issues
OPEN_ISSUES=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER -q '.open_issues')

if [ "$OPEN_ISSUES" -gt 0 ]; then
  echo "ERROR: В Milestone есть $OPEN_ISSUES открытых Issues"
  exit 1
fi
```

**Структура Release Notes с ссылкой на Milestone:**

```markdown
# Release v1.0.0

## Milestone

Этот релиз основан на [Milestone v1.0.0](https://github.com/{owner}/{repo}/milestone/5).

**Прогресс:** 15/15 Issues завершено (100%)

## What's Changed

- Add OAuth2 (#123)
- Update API to v2 (#124)
- Fix file upload (#125)

## Breaking changes

*Нет*

**Full Changelog**: https://github.com/{owner}/{repo}/compare/v0.9.0...v1.0.0
```

**Важно:** В body Release ОБЯЗАТЕЛЬНА markdown-ссылка на Milestone в секции "Milestone":

```markdown
## Milestone

Этот релиз основан на [Milestone v1.0.0](https://github.com/{owner}/{repo}/milestone/{number}).
```

---

## 8. Жизненный цикл Release

```
1. ПЛАНИРОВАНИЕ
   └─ Создан Milestone для релиза (v1.0.0)
   └─ Issues добавлены в Milestone

2. РАЗРАБОТКА
   └─ Issues реализуются через PR
   └─ PR мержатся в main
   └─ Прогресс Milestone отслеживается

3. ЗАВЕРШЕНИЕ MILESTONE
   └─ Все Issues закрыты
   └─ Milestone закрыт

4. ПОДГОТОВКА RELEASE
   └─ Обновлён CHANGELOG.md
   └─ Проверен Milestone (state=closed, open_issues=0)
   └─ Определена версия по SemVer

5. СОЗДАНИЕ RELEASE
   └─ Создан Release через gh release create
   └─ Git-тег создан автоматически
   └─ Release Notes содержат ссылку на Milestone

6. ПУБЛИКАЦИЯ
   └─ Release опубликован (не draft)
   └─ Деплой на production (через CI/CD workflow)

7. HOTFIX (если нужен)
   └─ Создан hotfix-PR в main
   └─ PR смержен
   └─ Создан PATCH-релиз (v1.0.1)
```

**Переходы:**

- **Draft → Published:** `gh release edit v1.0.0 --draft=false`
- **Pre-release → Stable:** `gh release edit v1.0.0-rc.1 --prerelease=false` (НЕ рекомендуется — лучше создать новый Release `v1.0.0`)

---

## 9. CLI команды

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
# Список всех Releases
gh release list

# Детали конкретного Release
gh release view v1.0.0

# Скачать артефакты
gh release download v1.0.0

# Скачать конкретный артефакт
gh release download v1.0.0 -p "app-linux-amd64.tar.gz"
```

### Редактирование Release

```bash
# Изменить title
gh release edit v1.0.0 --title "New title"

# Обновить body (changelog)
gh release edit v1.0.0 --notes "Updated changelog"

# Снять draft
gh release edit v1.0.0 --draft=false

# Пометить как stable (убрать prerelease)
gh release edit v1.0.0 --prerelease=false

# Добавить артефакты
gh release upload v1.0.0 ./dist/new-file.zip
```

### Удаление Release

**Когда можно удалить:**
- Release создан по ошибке (draft)
- Версия некорректная

**Когда НЕЛЬЗЯ удалить:**
- Release уже опубликован и используется (нарушение воспроизводимости)

**Шаги:**

```bash
# 1. Удалить Release
gh release delete v1.0.0 --yes

# 2. Удалить Git-тег
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

**Важно:** Удаление Release НЕ удаляет Milestone и Issues.

---

## 10. Правила создания Release

**Обязательные проверки перед созданием:**

1. **Milestone закрыт:**
   ```bash
   MILESTONE_STATE=$(gh api repos/$OWNER/$REPO/milestones/{number} -q '.state')
   [ "$MILESTONE_STATE" = "closed" ] || exit 1
   ```
2. **Нет открытых Issues в Milestone:**
   ```bash
   OPEN_ISSUES=$(gh api repos/$OWNER/$REPO/milestones/{number} -q '.open_issues')
   [ "$OPEN_ISSUES" -eq 0 ] || exit 1
   ```
3. **Версия следует SemVer:**
   - Формат: `vX.Y.Z` (или с pre-release суффиксом)
4. **Changelog подготовлен:**
   - Либо через `--generate-notes`
   - Либо вручную в CHANGELOG.md
5. **Нет незакоммиченных изменений в main:**
   ```bash
   git diff --quiet || (echo "ERROR: Uncommitted changes" && exit 1)
   ```

**Обработка ошибок:**
- Если хотя бы одна проверка не прошла → **ОСТАНОВИТЬ** процесс создания Release
- Вернуть ошибку с указанием, какая проверка не прошла
- Исправить проблему, затем повторить процесс с начала

**Два способа создания changelog:**

**Способ 1: Автогенерация (`--generate-notes`)**
- Пропустить обновление CHANGELOG.md
- GitHub сгенерирует changelog автоматически из PR
- Использовать: `gh release create v1.0.0 --generate-notes`

**Способ 2: Вручную из CHANGELOG.md**
- Обновить CHANGELOG.md
- Закоммитить изменения
- Создать Release с `-F CHANGELOG.md` вместо `--generate-notes`

**Последовательность действий:**

1. Проверить Milestone (state, open_issues)
2. Обновить CHANGELOG.md (ТОЛЬКО если используется Способ 2)
3. Закоммитить изменения в main (ТОЛЬКО если обновляли CHANGELOG.md):
   ```bash
   git add CHANGELOG.md
   git commit -m "docs: update changelog for v1.0.0"
   git push
   ```
4. Создать Release:
   ```bash
   # Способ 1 (автогенерация):
   gh release create v1.0.0 --title "Release v1.0.0" --generate-notes

   # Способ 2 (из файла):
   gh release create v1.0.0 --title "Release v1.0.0" -F CHANGELOG.md
   ```
5. Проверить создание тега:
   ```bash
   git fetch --tags
   git tag | grep v1.0.0
   ```

**Важно:** Commit с обновлением CHANGELOG.md ДОЛЖЕН быть смержен в main ПЕРЕД созданием Release (иначе тег не будет содержать актуальный CHANGELOG).

---

## 11. Yanking Release (отзыв версии)

**Когда применять:**
- Release содержит уязвимость (CVE)
- Release содержит баг, ломающий критичную функциональность

**Процедура:**

1. Обновить Release Notes с предупреждением:
   ```bash
   gh release edit v1.0.0 --notes "**⚠️ YANKED:** Содержит уязвимость CVE-2025-1234. Используйте v1.0.1 или новее.

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

## 12. Переход Pre-release → Stable

**Когда применять:**
- Pre-release версия (`v1.0.0-rc.1`) протестирована и готова к публикации

**НЕ рекомендуется:**
```bash
gh release edit v1.0.0-rc.1 --prerelease=false  # ❌ меняет статус, но тег остаётся -rc.1
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

## 13. Draft Release (черновик)

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

## 14. Синхронизация CHANGELOG.md с Release

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

## Скиллы

*Нет скиллов.*
