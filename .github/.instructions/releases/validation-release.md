---
description: Валидация GitHub Release — версия, changelog, теги, артефакты. Чек-лист перед и после публикации.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/releases/README.md
---

# Валидация Release

Рабочая версия стандарта: 1.1

Проверка корректности GitHub Release: pre-release готовность, объект Release, Release Notes, CHANGELOG.md, деплой.

**Полезные ссылки:**
- [Инструкции Releases](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-release.md](./standard-release.md) |
| Валидация | Этот документ |
| Создание | [create-release.md](./create-release.md) |
| Модификация | *Не требуется — операции описаны в standard-release.md § 18* |

## Оглавление

- [Когда валидировать](#когда-валидировать)
- [Шаги](#шаги)
  - [Шаг 1: Проверить готовность main (pre-release)](#шаг-1-проверить-готовность-main-pre-release)
  - [Шаг 2: Проверить Milestone (pre-release)](#шаг-2-проверить-milestone-pre-release)
  - [Шаг 3: Проверить объект Release (post-release)](#шаг-3-проверить-объект-release-post-release)
  - [Шаг 4: Проверить Release Notes (post-release)](#шаг-4-проверить-release-notes-post-release)
  - [Шаг 5: Проверить CHANGELOG.md (post-release)](#шаг-5-проверить-changelogmd-post-release)
  - [Шаг 6: Проверить деплой (post-release)](#шаг-6-проверить-деплой-post-release)
- [Чек-лист](#чек-лист)
- [Типичные ошибки](#типичные-ошибки)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Когда валидировать

Запускать валидацию:

1. **Перед созданием Release (pre-release)** — шаги 1–2. Проверить готовность main и Milestone
2. **После создания Release (post-release)** — шаги 3–6. Проверить объект, Release Notes, CHANGELOG, деплой
3. **При аудите Releases** — шаги 3–5. Проверить существующие Releases на соответствие стандарту

---

## Шаги

### Шаг 1: Проверить готовность main (pre-release)

**SSOT:** [standard-release.md § 9](./standard-release.md#9-подготовка-релиза)

**Автоматически:**
```bash
python .github/.instructions/.scripts/validate-pre-release.py --version v1.0.0
```

**Вручную:**

Выполнить 5 проверок строго последовательно:

```bash
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')
```

| # | Проверка | Команда | Ожидаемый результат |
|---|----------|---------|---------------------|
| 1 | Main синхронизирована | `git checkout main && git pull origin main` | Локальная main актуальна |
| 2 | Нет критичных PR | `gh pr list --label critical --state open` | Список пустой |
| 3 | Тесты проходят | `make test` | Все тесты пройдены |
| 4 | Milestone закрыт | См. Шаг 2 | `state: closed`, `open_issues: 0` |
| 5 | Нет незакоммиченных изменений | `git diff --quiet` | Пустой вывод |

**Критерий:** Если хотя бы одна проверка не пройдена → **СТОП**. Сообщить какая проверка провалилась.

---

### Шаг 2: Проверить Milestone (pre-release)

**SSOT:** [standard-release.md § 7](./standard-release.md#7-связь-с-milestones)

**Вручную:**

```bash
VERSION="v1.0.0"  # ← подставить версию

# 1. Найти Milestone
MILESTONE_NUMBER=$(gh api repos/$OWNER/$REPO/milestones --method GET \
  -q ".[] | select(.title == \"$VERSION\") | .number")

# 2. Проверить существование
if [ -z "$MILESTONE_NUMBER" ]; then
  echo "FAIL: Milestone $VERSION не найден"
fi

# 3. Проверить открытые Issues
OPEN_ISSUES=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER \
  --method GET -q '.open_issues')

if [ "$OPEN_ISSUES" -gt 0 ]; then
  echo "FAIL: В Milestone есть $OPEN_ISSUES открытых Issues"
  gh issue list --milestone "$VERSION" --state open
fi

# 4. Проверить статус
STATE=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER \
  --method GET -q '.state')

if [ "$STATE" != "closed" ]; then
  echo "FAIL: Milestone не закрыт (state: $STATE)"
fi
```

| Правило | Проверка |
|---------|----------|
| Milestone существует | `MILESTONE_NUMBER` не пустой |
| Все Issues закрыты | `open_issues == 0` |
| Milestone закрыт | `state == "closed"` |

**Критерий:** Все 3 проверки пройдены.

---

### Шаг 3: Проверить объект Release (post-release)

**SSOT:** [standard-release.md § 6](./standard-release.md#6-release-как-объект-github)

**Автоматически:**
```bash
python .github/.instructions/.scripts/validate-post-release.py --version v1.0.0
```

**Вручную:**

```bash
VERSION="v1.0.0"  # ← подставить версию

# Получить данные Release
gh release view $VERSION --json tagName,name,body,isDraft,isPrerelease,targetCommitish
```

| Поле | Правило | Проверка |
|------|---------|----------|
| `tagName` | Формат `vX.Y.Z` | Соответствует SemVer |
| `name` | Формат `Release vX.Y.Z` | `name == "Release $VERSION"` |
| `body` | Не пустой | `body != ""` |
| `isDraft` | `false` (для опубликованных) | `isDraft == false` |
| `targetCommitish` | `main` | Тег на main |

**Проверить тег:**

```bash
# Тег существует
git fetch --tags
git tag | grep $VERSION

# Тег указывает на main HEAD (на момент создания)
git rev-parse $VERSION
```

**Критерий:** Все поля заполнены корректно, тег существует.

---

### Шаг 4: Проверить Release Notes (post-release)

**SSOT:** [standard-release.md § 5](./standard-release.md#5-changelog), [§ 7](./standard-release.md#7-связь-с-milestones)

**Вручную:**

```bash
BODY=$(gh release view $VERSION --json body -q '.body')
```

| Правило | Проверка |
|---------|----------|
| Содержит ссылку на Milestone | `## Milestone` секция в body |
| Содержит changelog | `## What's Changed` или список PR |
| Содержит ссылку на Full Changelog | `**Full Changelog**:` в body |
| Нет placeholder-текстов | Нет `TODO`, `WIP`, `TBD` в body |

**Критерий:** Release Notes содержит ссылку на Milestone и changelog.

---

### Шаг 5: Проверить CHANGELOG.md (post-release)

**SSOT:** [standard-release.md § 17](./standard-release.md#17-синхронизация-changelogmd-с-release)

**Вручную:**

1. Проверить существование файла:
   ```bash
   test -f CHANGELOG.md && echo "OK" || echo "FAIL: CHANGELOG.md не найден"
   ```

2. Проверить наличие секции для версии:
   ```bash
   grep -q "## \[$VERSION_WITHOUT_V\]" CHANGELOG.md && echo "OK" || echo "WARN: Версия не найдена в CHANGELOG.md"
   ```
   Где `VERSION_WITHOUT_V` — версия без `v` (например `1.0.0`).

3. Проверить формат (Keep a Changelog):

| Правило | Проверка |
|---------|----------|
| Заголовок `# Changelog` | Первая строка файла |
| Секция `[Unreleased]` | Присутствует |
| Версия с датой | `## [X.Y.Z] - YYYY-MM-DD` |
| Категории | Added, Changed, Fixed и т.д. |

**Критерий:** CHANGELOG.md существует и содержит секцию для текущей версии.

**Примечание:** CHANGELOG.md обновляется ПОСЛЕ создания Release. Коммит с обновлением не попадает в тег текущего Release — это нормально.

---

### Шаг 6: Проверить деплой (post-release)

**SSOT:** [standard-release.md § 11](./standard-release.md#11-публикация-на-production)

**Вручную:**

1. Проверить запуск workflow:
   ```bash
   gh run list --workflow=deploy.yml --limit 1
   ```

2. Проверить статус:

| Статус | Значение | Действие |
|--------|----------|----------|
| `completed` + `success` | Деплой успешен | Продолжить проверки |
| `completed` + `failure` | Деплой провалился | См. standard-release.md § 11 |
| `in_progress` | Деплой в процессе | Подождать |
| Нет запусков | Workflow не настроен | Деплоить вручную или настроить deploy.yml |

3. Post-deploy verification (если деплой успешен):

| # | Проверка | Критерий |
|---|----------|----------|
| 1 | Health check | `{"status": "ok"}` |
| 2 | Smoke tests | Критичные пути работают |
| 3 | Error rate (15 мин) | Не вырос |

**Критерий:** Деплой завершён успешно, health check пройден.

---

## Чек-лист

### Pre-release
- [ ] Main синхронизирована (`git pull`)
- [ ] Нет открытых PR с меткой `critical`
- [ ] Тесты проходят (`make test`)
- [ ] Milestone существует и закрыт
- [ ] Все Issues в Milestone закрыты
- [ ] Нет незакоммиченных изменений

### Release объект
- [ ] Tag формат `vX.Y.Z`
- [ ] Title формат `Release vX.Y.Z`
- [ ] Body не пустой
- [ ] Target = `main`
- [ ] Git-тег создан

### Release Notes
- [ ] Содержит ссылку на Milestone (`## Milestone`)
- [ ] Содержит changelog (список изменений)
- [ ] Содержит ссылку Full Changelog
- [ ] Нет placeholder-текстов (TODO, WIP)

### CHANGELOG.md
- [ ] Файл существует
- [ ] Секция `[Unreleased]` присутствует
- [ ] Секция для текущей версии добавлена
- [ ] Формат Keep a Changelog 1.1.0
- [ ] Дата в ISO 8601

### Деплой
- [ ] Workflow запущен
- [ ] Деплой завершён успешно
- [ ] Health check пройден
- [ ] Smoke tests пройдены

---

## Типичные ошибки

| Ошибка | Код | Причина | Решение |
|--------|-----|---------|---------|
| Milestone не найден | E001 | Milestone не создан или title не совпадает | Создать Milestone с title = версия Release |
| Milestone не закрыт | E002 | Есть открытые Issues | Закрыть или перенести Issues, закрыть Milestone |
| Tag не SemVer | E003 | Формат тега некорректный | Удалить Release, пересоздать с `vX.Y.Z` |
| Title не `Release vX.Y.Z` | E004 | Нестандартное название | `gh release edit $V --title "Release $V"` |
| Body пустой | E005 | `--generate-notes` не нашёл PR | Добавить changelog вручную: `gh release edit $V --notes "..."` |
| Нет ссылки на Milestone | E006 | Не добавлена секция Milestone | Обновить Release Notes: `gh release edit $V --notes "..."` |
| CHANGELOG.md не существует | E007 | Файл не создан | Создать по шаблону из standard-release.md § 5 |
| CHANGELOG.md не обновлён | E008 | Забыли синхронизировать | Скопировать Release Notes → CHANGELOG.md → commit |
| Деплой провалился | E009 | Ошибка в коде или инфраструктуре | См. standard-release.md § 11 (таблица ошибок) |
| Тег на неправильной ветке | E010 | `--target` не main | Удалить Release и тег, пересоздать на main |
| Placeholder в Release Notes | E011 | TODO/WIP не убраны | Обновить Release Notes |

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-pre-release.py](../.scripts/validate-pre-release.py) | Pre-release: main, critical PR, тесты, Milestone, working tree | Этот документ |
| [validate-post-release.py](../.scripts/validate-post-release.py) | Post-release: объект Release, notes, CHANGELOG, деплой | Этот документ |

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/post-release](/.claude/skills/post-release/SKILL.md) | Post-release валидация |
