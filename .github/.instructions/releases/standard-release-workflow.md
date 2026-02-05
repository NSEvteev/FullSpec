---
description: Процесс релиза от решения до публикации и hotfix
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/releases/README.md
---

# Стандарт Release Workflow

Версия стандарта: 1.0

Полный процесс релиза: подготовка → создание → публикация → hotfix → rollback.

**Полезные ссылки:**
- [Инструкции releases](./README.md)
- [GitHub Workflow](../standard-github-workflow.md) — цикл разработки от Issue до Merge

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | *Будет создан* |
| Создание | *Будет создан* |
| Модификация | *Будет создан* |

**Зависимые стандарты:**

| Область | Документ | Что регулирует |
|---------|----------|----------------|
| Development | [standard-github-workflow.md](../standard-github-workflow.md) | Issue → PR → Merge цикл |
| Releases | [standard-release.md](./standard-release.md) | Версионирование, теги, changelog |
| Milestones | [standard-milestone.md](../milestones/standard-milestone.md) | Группировка задач по релизам |

> **Примечание:** `standard-release.md` будет создан в рамках Волны 4. До его создания используется информация из [github-platform-research.md](/.claude/drafts/2026-02-03-github-platform-research.md).

## Оглавление

- [1. Зона ответственности](#1-зона-ответственности)
- [2. Полный цикл релиза](#2-полный-цикл-релиза)
- [3. Подготовка релиза](#3-подготовка-релиза)
- [4. Создание релиза](#4-создание-релиза)
- [5. Публикация на production](#5-публикация-на-production)
- [6. Hotfix-релиз](#6-hotfix-релиз)
- [7. Rollback процесс](#7-rollback-процесс)
- [8. Связь с Development Workflow](#8-связь-с-development-workflow)
- [9. Граничные случаи](#9-граничные-случаи)

---

## 1. Зона ответственности

### Этот стандарт регулирует

**Процесс релиза:**
- Решение "делаем релиз" → публикация на production
- Подготовка релиза (проверки перед созданием)
- Создание Release в GitHub
- Деплой на production (триггер)
- Hotfix-релизы (критичные исправления)
- Rollback процесс (откат релиза)

### НЕ регулирует (смежные зоны)

| Что | Где регулируется |
|-----|------------------|
| Версионирование (формат v1.0.0) | [standard-release.md](./standard-release.md) |
| Теги и changelog | [standard-release.md](./standard-release.md) |
| CI/CD workflows (`.yml` файлы) | [standard-workflow-file.md](../workflows-files/standard-workflow-file.md) |
| Milestones (создание, закрытие) | [standard-milestone.md](../milestones/standard-milestone.md) |
| Issue → PR → Merge | [standard-github-workflow.md](../standard-github-workflow.md) |

### Принципы

> **Merge в main ≠ деплой.** Код попадает в main после merge PR, но на production попадает ТОЛЬКО через Release.

> **Release — это решение, не событие.** Релиз создаётся явно, а не автоматически при merge в main.

> **Один Release = один деплой.** Каждый релиз триггерит деплой на production (через GitHub Actions).

> **Hotfix — это тоже Release.** Hotfix создаётся как отдельный релиз с патч-версией (v1.0.1).

---

## 2. Полный цикл релиза

```
┌─────────────────────────────────────────────────────────────────┐
│                        RELEASE WORKFLOW                           │
└─────────────────────────────────────────────────────────────────┘

1. РЕШЕНИЕ О РЕЛИЗЕ
   └─ Человек: "Делаем релиз"
   └─ Критерий: минимум 1 смерженный PR с момента последнего релиза ИЛИ deadline milestone

2. ПОДГОТОВКА РЕЛИЗА
   └─ Проверить main: нет открытых PR с priority:critical
   └─ Проверить тесты: make test пройдены локально
   └─ Определить версию: v1.0.0 (major.minor.patch)
   └─ Закрыть milestone

3. СОЗДАНИЕ RELEASE В GITHUB
   └─ gh release create v1.0.0 --generate-notes
   └─ Тег создаётся автоматически (v1.0.0 → main HEAD)
   └─ Changelog генерируется автоматически (из PR titles)

4. ПУБЛИКАЦИЯ НА PRODUCTION
   └─ GitHub Actions триггерится событием "release published"
   └─ Workflow: .github/workflows/deploy.yml
   └─ Деплой на сервер (docker pull, restart services)
   └─ Проверка health check

5. HOTFIX (если production сломался)
   └─ Создать Issue с priority:critical
   └─ Создать ветку fix/{issue}-{description}
   └─ Исправить → PR → merge в main
   └─ Создать hotfix-релиз: gh release create v1.0.1
   └─ Деплой на production (автоматически)

6. ROLLBACK (если релиз критично сломал production)
   └─ Откатить деплой вручную (вернуть предыдущую версию)
   └─ Удалить проблемный релиз: gh release delete v1.0.0
   └─ Revert merge в main: git revert {commit}
```

**Ключевое:**
- **Релиз создаётся вручную** (не автоматически при merge)
- **Деплой триггерится релизом** (не merge в main)
- **Hotfix — это новый релиз** (не изменение существующего)

---

## 3. Подготовка релиза

### Критерии готовности к релизу

**Обязательные проверки перед созданием Release:**

| Проверка | Команда | Результат |
|----------|---------|-----------|
| **Нет критичных PR** | `gh pr list --label priority:critical --state open` | Список пустой |
| **Main стабильна** | `git checkout main && git pull origin main` | Локальная main синхронизирована |
| **Тесты проходят** | `make test` | Все тесты ✅ |
| **Pre-commit hooks** | `make setup` (если не установлены) | Hooks установлены |
| **Milestone закрыт** | `gh api repos/{owner}/{repo}/milestones/{number}` | `state: closed` |
| **Все Issues milestone закрыты** | `gh issue list --milestone "v1.0" --state open` | Список пустой |

**Порядок проверок (СТРОГО последовательно):**
1. Синхронизация main (`git checkout main && git pull`) — предусловие для всех проверок
2. Проверка критичных PR
3. Запуск тестов (ПОСЛЕ синхронизации main)
4. Проверка и закрытие Milestone

### Определение версии

**SSOT:** [standard-milestone.md § 4](../milestones/standard-milestone.md#4-версионирование-semver)

Версия определяется по правилам SemVer:
- **MAJOR** — breaking changes
- **MINOR** — новые фичи (обратно совместимые)
- **PATCH** — багфиксы

Детали и pre-release версии — см. SSOT.

### Закрытие Milestone

**Полная проверка перед созданием Release:**

```bash
OWNER="owner"
REPO="repo"
VERSION="v1.0.0"

# 1. Проверить существование Milestone
MILESTONE_NUMBER=$(gh api repos/$OWNER/$REPO/milestones -q ".[] | select(.title == \"$VERSION\") | .number")

if [ -z "$MILESTONE_NUMBER" ]; then
  echo "ERROR: Milestone $VERSION не найден"
  exit 1
fi

# 2. Проверить открытые Issues
OPEN_ISSUES=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER -q '.open_issues')

if [ "$OPEN_ISSUES" -gt 0 ]; then
  echo "ERROR: В Milestone есть $OPEN_ISSUES открытых Issues"
  echo "Действия: перенести в следующий Milestone или закрыть"
  gh issue list --milestone "$VERSION" --state open
  exit 1
fi

# 3. Закрыть Milestone
gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER -X PATCH -f state="closed"

# 4. Проверить статус
MILESTONE_STATE=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER -q '.state')

if [ "$MILESTONE_STATE" != "closed" ]; then
  echo "ERROR: Milestone не удалось закрыть"
  exit 1
fi

echo "Milestone $VERSION закрыт. Готов к созданию Release."
```

**Что делать с незавершёнными Issues:** см. [standard-milestone.md § 8](../milestones/standard-milestone.md#8-закрытие-milestone)

---

## 4. Создание релиза

### Процесс

```bash
# 1. Переключиться на main
git checkout main

# 2. Обновить main
git pull origin main

# 3. Создать релиз
gh release create v1.0.0 \
  --title "Release v1.0.0" \
  --generate-notes

# 4. GitHub автоматически:
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

### Ссылка на Milestone в Release Notes

**Правило:** В Release Notes ОБЯЗАТЕЛЬНА ссылка на Milestone.

**Получить URL Milestone:**

```bash
MILESTONE_URL=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER -q '.html_url')
```

**Шаблон Release Notes:**

```markdown
## Milestone

Этот релиз основан на [Milestone v1.0.0](https://github.com/{owner}/{repo}/milestone/{number}).

**Прогресс:** 15/15 Issues завершено (100%)

## What's Changed

- Add OAuth2 (#123)
- Update API to v2 (#124)
- Fix file upload (#125)

## Breaking changes

*Нет*

**Full Changelog**: https://github.com/{owner}/{repo}/compare/v0.9.0...v1.0.0
```

### Опциональные элементы

| Элемент | Когда добавлять | Пример |
|---------|-----------------|--------|
| **--draft** | Если релиз ещё не готов к публикации | `gh release create v1.0.0 --draft` |
| **--prerelease** | Если релиз тестовый (beta, rc) | `gh release create v1.0.0-rc1 --prerelease` |
| **Assets** | Если нужны артефакты (бинарники, архивы) | `gh release create v1.0.0 ./dist/*.zip` |

### Changelog

**SSOT:** [standard-release.md § 5](./standard-release.md#5-changelog)

Changelog генерируется автоматически при создании Release:
```bash
gh release create v1.0.0 --generate-notes
```

Формат и правила — см. SSOT.

---

## 5. Публикация на production

### Триггер деплоя

**GitHub Actions триггерится событием:**
```yaml
# .github/workflows/deploy.yml
on:
  release:
    types: [published]
```

**Workflow выполняет:**
1. Checkout кода на тег релиза
2. Build Docker образов
3. Push образов в Registry
4. Деплой на production сервер (SSH, Kubernetes, etc.)
5. Health check (проверка доступности сервисов)

**Важно:** Деплой происходит АВТОМАТИЧЕСКИ после создания релиза (если настроен `deploy.yml`).

### Проверка статуса деплоя

```bash
# Просмотр запусков workflow
gh run list --workflow=deploy.yml

# Детали конкретного запуска
gh run view {run-id}

# Логи запуска
gh run view {run-id} --log
```

### Если деплой провалился

**Проверить логи:**
```bash
gh run view {run-id} --log
```

**Классификация ошибок:**

| Тип ошибки | Признаки в логах | Действие |
|------------|------------------|----------|
| **Ошибка в коде** | `Error:`, `Exception:`, test failure | Создать hotfix (см. секцию 6) |
| **Ошибка инфраструктуры** | `Connection refused`, `403 Forbidden`, `No space left` | Исправить инфру → retry |
| **Таймаут** | `timeout`, `deadline exceeded` | Проверить доступность сервера → retry |

**Действия:**
1. Если ошибка в коде → создать hotfix (см. секцию 6)
2. Если ошибка в инфраструктуре → исправить инфраструктуру → перезапустить деплой вручную:
   ```bash
   gh workflow run deploy.yml --ref v1.0.0
   ```

### Проверка health check после деплоя

После завершения GitHub Actions:

1. Проверить статус деплоя:
   ```bash
   gh run view {run-id} --log | grep 'Health check'
   ```

2. Проверить доступность сервиса:
   ```bash
   curl https://example.com/health
   # Ожидаемый ответ: {"status": "ok"}
   ```

3. Если health check провалился:
   - Проверить логи сервиса
   - Если критично → rollback (секция 7)
   - Если не критично → создать hotfix (секция 6)

---

## 6. Hotfix-релиз

### Когда создавать hotfix

**Критерии:**
- Production сломался (критичный баг)
- Сервис недоступен или работает некорректно
- Требуется срочное исправление

### Процесс hotfix

```
1. СОЗДАТЬ ISSUE
   └─ gh issue create --title "Критичный баг: ..." --label type:bug --label priority:critical

2. СОЗДАТЬ ВЕТКУ ОТ MAIN
   └─ git checkout main
   └─ git pull origin main
   └─ git checkout -b fix/{issue-number}-{description}

3. ИСПРАВИТЬ БАГ
   └─ Внести изменения
   └─ Написать тесты (воспроизвести баг → исправить → проверить)
   └─ git commit -m "fix: {description}"

4. СОЗДАТЬ PR
   └─ git push -u origin fix/{issue-number}-{description}
   └─ gh pr create --title "fix: {description}" --body "Closes #{issue-number}" \
        --label type:bug --label priority:critical

5. РЕВЬЮ (упрощённый процесс для hotfix)
   └─ Минимум 1 approval от другого разработчика (НЕ автор PR)
   └─ Self-approve ЗАПРЕЩЁН даже для hotfix
   └─ Проверить ТОЛЬКО: исправление бага, наличие теста, отсутствие breaking changes
   └─ Полный code review НЕ требуется (читаемость, рефакторинг — можно пропустить)
   └─ gh pr review {PR-number} --approve
   └─ gh pr merge {PR-number} --squash

6. СОЗДАТЬ HOTFIX-РЕЛИЗ
   └─ git checkout main && git pull origin main
   └─ gh release create v1.0.1 --generate-notes
   └─ GitHub Actions деплоит на production автоматически

7. ПРОВЕРИТЬ PRODUCTION
   └─ Проверить health check
   └─ Проверить логи (баг исправлен)
```

**Важно:**
- Hotfix НЕ пропускает Issue и PR (даже для критичных багов)
- Hotfix-релиз создаётся как новый релиз с PATCH-версией (v1.0.0 → v1.0.1)
- Деплой происходит автоматически после создания релиза

### Множественные hotfix

**Если несколько критичных багов:**

```bash
# Вариант 1: Объединить hotfix в один релиз
# Создать Issues #130, #131
# Исправить оба бага в одной ветке fix/130-131-critical-bugs
# Один PR, один релиз v1.0.1

# Вариант 2: Последовательные hotfix
# Issue #130 → PR → merge → релиз v1.0.1
# Issue #131 → PR → merge → релиз v1.0.2
```

**Объединять hotfix в один релиз если ВЫПОЛНЕНЫ ОБА условия:**
1. Баги обнаружены в течение 1 часа друг от друга
2. Баги НЕ блокируют друг друга (можно исправить параллельно)

Если хотя бы одно условие НЕ выполнено — создавать последовательные релизы (v1.0.1, v1.0.2).

---

## 7. Rollback процесс

### Когда делать rollback

**Критерии:**
- Релиз критично сломал production (сервис недоступен)
- Hotfix невозможен в течение 30 минут (с момента обнаружения критичного бага)
- Требуется немедленный откат к предыдущей версии

### Процесс rollback

```
1. ОТКАТИТЬ ДЕПЛОЙ (ВРУЧНУЮ)
   └─ Определить тип инфраструктуры: проверить файлы `/.platform/docker/` или `/.platform/kubernetes/`
   └─ Выбрать команду rollback в зависимости от используемой инфраструктуры (выполнить ОДНУ из команд ниже):
      - Docker: docker pull {image}:v0.9.0 && docker restart
      - Kubernetes: kubectl rollout undo deployment/{name}
      - SSH: rsync предыдущей версии на сервер

2. ОПРЕДЕЛИТЬ ПРОБЛЕМНУЮ ВЕРСИЮ
   └─ Определить проблемную версию: `gh release list --limit 1` (последний релиз)
   └─ Записать версию в переменную: PROBLEM_VERSION=v1.0.0

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
        --label type:bug --label priority:critical

6. ИСПРАВИТЬ ПРОБЛЕМУ
   └─ Создать ветку fix/{issue}-...
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

**Сценарий:** Релиз v1.0.0 удалён из GitHub Releases, но тег существует в Git.

**Процесс:**

1. Найти последний стабильный тег:
   ```bash
   git tag --sort=-version:refname | grep -v 'rc\|beta\|alpha' | head -1
   ```

2. Деплоить версию по тегу (напрямую, без создания Release):
   ```bash
   gh workflow run deploy.yml --ref v0.9.0
   ```

3. НЕ создавать новый Release в GitHub (деплой напрямую по тегу)

**Важно:** Это альтернативный путь для экстренных случаев, когда Release был удалён.

---

## 8. Связь с Development Workflow

### Разделение ответственности

| Workflow | Зона ответственности | Где код |
|----------|---------------------|---------|
| **Development** | Issue → PR → Merge в main | main (локальная разработка, code review) |
| **Release** | Main → Production | Production сервер (реальные пользователи) |

**Ключевое:**
```
main (код смержен) ≠ production (код доступен пользователям)

Development:  Issue → PR → Merge → main
                                    ↓
Release:                        Release → production
```

### Когда создавать релиз

**Решение принимает человек (не автоматически).**

**Критерии для релиза:**

| Критерий | Описание |
|----------|----------|
| **Достаточно изменений** | Минимум 1 смерженный PR с момента последнего релиза |
| **Deadline milestone** | Milestone завершён (все Issues закрыты) |
| **Критичный bugfix** | Hotfix должен попасть на production срочно |
| **Регулярный релиз (опционально)** | Релиз создаётся по расписанию (каждую неделю/месяц) ТОЛЬКО ЕСЛИ в main есть минимум 1 смерженный PR с момента последнего релиза. Если изменений нет — релиз пропускается. |

**НЕ создавать релиз автоматически после каждого merge в main** (continuous deployment) — релизы контролируются вручную.

### Координация workflow

**Правило:** Во время подготовки релиза НЕ мержить PR в main.

**Процесс:**
1. Человек: "Готовимся к релизу v1.0.0"
2. Команда: НЕ создавать новые PR, НЕ мержить существующие PR (кроме hotfix)
3. Человек: Проверка → создание релиза
4. Команда: Возобновление работы (можно мержить PR)

**Важно:** Если PR смержен в main ПОСЛЕ решения о релизе, но ДО создания релиза — этот PR попадёт в релиз (может быть нежелательно).

---

## 9. Граничные случаи

### Релиз с draft PR

**Сценарий:** В main смержены PR, но есть открытый Draft PR (не готов к релизу).

**Решение:**
- Draft PR НЕ влияет на релиз (не смержен в main)
- Создать релиз как обычно
- Draft PR попадёт в следующий релиз (после merge)

### Hotfix без предварительного Milestone

**Сценарий:** Критический баг в production — нужен срочный hotfix-релиз.

**Решение:**
- Создать Milestone `vX.Y.Z` (hotfix-версия) с одним Issue
- Закрыть Issue и Milestone
- Создать Release по стандартному процессу (§ 3–4)

### Множественные релизы в день

**Сценарий:** Создано несколько hotfix за день (v1.0.1, v1.0.2, v1.0.3).

**Решение:**
- Каждый hotfix — отдельный релиз
- Версия инкрементируется последовательно
- GitHub Actions деплоит каждый релиз автоматически

**Важно:** НЕ перезаписывать теги (не использовать одну и ту же версию для разных релизов).

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
3. Revert merge в обратном хронологическом порядке (от НОВЫХ к СТАРЫМ):
   ```bash
   # Сначала v1.0.2 (последний проблемный)
   git revert {commit-hash-v1.0.2}
   # Затем v1.0.1
   git revert {commit-hash-v1.0.1}
   # Затем v1.0.0 (первый проблемный)
   git revert {commit-hash-v1.0.0}
   git push origin main
   ```
   **ВАЖНО:** Порядок критичен для предотвращения merge-конфликтов.

4. Создать новый релиз v1.0.0 (после исправления проблем)

### Релиз с breaking changes

**Сценарий:** Релиз содержит breaking changes (несовместимые изменения API).

**Процесс:**
1. Увеличить MAJOR версию (v1.0.0 → v2.0.0)
2. В changelog явно указать breaking changes:
   ```markdown
   ## Breaking Changes
   - API endpoint `/api/v1/users` удалён (используйте `/api/v2/users`)
   - Формат ответа изменён: `{data: {...}}` → `{result: {...}}`
   ```
3. Уведомить команду/пользователей о breaking changes (email, Slack, etc.)
4. Создать релиз как обычно:
   ```bash
   gh release create v2.0.0 --generate-notes
   ```

### Hotfix для старой версии

**Сценарий:** Production на v1.0.0, main на v1.1.0, нужен hotfix для v1.0.0.

**Процесс (НЕ поддерживается в текущей модели):**
- Текущая модель: один production, один main
- Hotfix всегда создаётся от текущего main
- Если нужен hotfix для старой версии → обновить production до v1.1.0, затем создать hotfix v1.1.1

**Альтернатива (для поддержки нескольких версий):**
- Создать ветку `release/v1.0` от тега v1.0.0
- Применить hotfix в ветке `release/v1.0`
- Создать релиз v1.0.1 от ветки `release/v1.0`
- **Важно:** Это усложняет workflow, рекомендуется ТОЛЬКО для критичных случаев

### Pre-release (тестовый релиз)

**Сценарий:** Нужно протестировать релиз на staging без деплоя в production.

**Процесс:**

1. Создать pre-release:
   ```bash
   gh release create v1.0.0-rc1 --prerelease --title "Release Candidate 1" --generate-notes
   ```

2. Pre-release НЕ триггерит деплой на production (workflow должен проверять `types: [published]` и `!prerelease`)

3. После тестирования — создать стабильный Release `v1.0.0` (см. [standard-release.md § 12](./standard-release.md#12-переход-pre-release-stable))

### Параллельное создание релизов

**Сценарий:** Разработчик A создаёт v1.0.0, Разработчик B одновременно создаёт v1.0.0.

**Решение:**
1. ПЕРЕД созданием релиза проверить:
   ```bash
   gh release list --limit 1
   ```
2. Если версия уже существует → инкрементировать версию (v1.0.0 → v1.0.1)
3. Создание релиза — атомарная операция в GitHub (второй релиз с тем же тегом вернёт ошибку)

**Важно:** Координируйте создание релизов в команде (один человек отвечает за релизы).

---

## Скиллы

*Будут созданы после семантического анализа.*
