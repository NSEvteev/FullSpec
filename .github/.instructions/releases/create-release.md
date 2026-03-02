---
description: Воркфлоу создания GitHub Release — подготовка changelog, тегирование, публикация, post-release действия.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/releases/README.md
---

# Воркфлоу создания Release

Рабочая версия стандарта: 1.1

Пошаговый процесс создания GitHub Release: определение версии, pre-release проверки, сборка Release Notes, публикация, синхронизация CHANGELOG.md.

**Полезные ссылки:**
- [Инструкции Releases](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-release.md](./standard-release.md) |
| Валидация | [validation-release.md](./validation-release.md) |
| Создание | Этот документ |
| Модификация | *Не требуется — операции описаны в standard-release.md § 18* |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 0: Проверить готовность](#шаг-0-проверить-готовность)
  - [Шаг 1: Определить версию](#шаг-1-определить-версию)
  - [Шаг 2: Release Freeze](#шаг-2-release-freeze)
  - [Шаг 3: Pre-release валидация](#шаг-3-pre-release-валидация)
  - [Шаг 4: Собрать Release Notes (body)](#шаг-4-собрать-release-notes-body)
  - [Шаг 5: Создать Release](#шаг-5-создать-release)
  - [Шаг 6: Синхронизировать CHANGELOG.md](#шаг-6-синхронизировать-changelogmd)
  - [Шаг 7: Post-release валидация](#шаг-7-post-release-валидация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Release — это решение, не событие.** Релиз создаётся явно (человеком), не автоматически при merge.

> **Один Release = один Git-тег = один деплой.** Никогда не переиспользовать теги.

> **Release создаётся ТОЛЬКО после закрытия Milestone.** Нет Milestone — нет Release.

> **Merge в main ≠ деплой.** Код в main → production ТОЛЬКО через Release.

> **Release Freeze обязателен.** Во время подготовки не мержить PR.

---

## Шаги

### Шаг 0: Проверить готовность

**SSOT:** [standard-process.md § 5](../../specs/.instructions/standard-process.md#5-путь-a-happy-path) Фаза 8

Убедиться что все analysis chains для этого Milestone завершены:

1. Получить dashboard:

```bash
python specs/.instructions/.scripts/chain_status.py dashboard
```

2. **Все цепочки** привязанные к Milestone должны быть в статусе **DONE**.
3. Если есть цепочки НЕ в DONE → **СТОП**.
   - RUNNING → завершить разработку
   - REVIEW → завершить ревью (`/chain-done`)
   - CONFLICT → разрешить конфликт
   - DRAFT/WAITING → цепочка не запущена

> **Исключение:** Hotfix (`--skip-chains`). При hotfix цепочка может быть в RUNNING — релиз критического фикса не ждёт завершения цепочки.

---

### Шаг 1: Определить версию

**SSOT:** [standard-release.md § 3](./standard-release.md#3-версионирование-semver), [standard-milestone.md § 4](../milestones/standard-milestone.md#4-версионирование-semver)

**Определить OWNER/REPO:**

```bash
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')
```

**Определить версию из Milestone:**

```bash
# Найти закрытый Milestone (кандидат на Release)
gh api repos/$OWNER/$REPO/milestones --method GET -q \
  '.[] | select(.state == "closed") | "\(.title) — closed: \(.closed_at)"'
```

**Если закрытых Milestones нет:**
1. Спросить пользователя: «Какую версию создаём?»
2. Если пользователь указал версию — проверить что Milestone существует
3. Если Milestone не существует — **СТОП**. Сначала создать и закрыть Milestone

**Установить переменную:**

```bash
VERSION="v1.0.0"  # ← версия из Milestone
```

---

### Шаг 2: Release Freeze

**SSOT:** [standard-release.md § 9](./standard-release.md#9-подготовка-релиза)

**Действие:** Сообщить пользователю о начале Release Freeze.

```
⚠️ RELEASE FREEZE для {VERSION}
Не мержить PR в main до завершения создания Release.
Исключение: PR с меткой "critical".
```

**LLM не может заблокировать merge технически.** Freeze — организационная мера. Ответственность на пользователе.

---

### Шаг 3: Pre-release валидация

**SSOT:** [validation-release.md](./validation-release.md), шаги 1–2

**Автоматически:**

```bash
python .github/.instructions/.scripts/validate-pre-release.py --version $VERSION
```

**Если валидация провалилась → СТОП.** Скрипт покажет какая проверка не прошла. Исправить проблему и повторить.

---

### Шаг 4: Собрать Release Notes (body)

**SSOT:** [standard-release.md § 5](./standard-release.md#5-changelog), [§ 7](./standard-release.md#7-связь-с-milestones)

**4.1. Получить URL Milestone:**

```bash
MILESTONE_NUMBER=$(gh api repos/$OWNER/$REPO/milestones?state=closed --method GET \
  -q ".[] | select(.title == \"$VERSION\") | .number")

MILESTONE_URL=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER \
  --method GET -q '.html_url')

CLOSED_ISSUES=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER \
  --method GET -q '.closed_issues')
```

**4.2. Сгенерировать changelog из PR:**

```bash
# Получить предыдущий тег
PREVIOUS_TAG=$(git tag --sort=-version:refname | head -1)

# Если первый релиз (нет предыдущего тега)
if [ -z "$PREVIOUS_TAG" ]; then
  PREVIOUS_TAG=""
  COMPARE_URL="Первый релиз"
else
  COMPARE_URL="https://github.com/$OWNER/$REPO/compare/$PREVIOUS_TAG...$VERSION"
fi
```

**4.3. Собрать body:**

Шаблон Release Notes (**обязательный формат**):

```markdown
## Milestone

Этот релиз основан на [Milestone {VERSION}]({MILESTONE_URL}).

**Прогресс:** {CLOSED_ISSUES}/{CLOSED_ISSUES} Issues завершено (100%)

## What's Changed

{автогенерация из PR — добавляется через --generate-notes}

## Breaking Changes

*Нет*

**Full Changelog**: {COMPARE_URL}
```

**Создать файл body:**

```bash
cat > /tmp/release-notes.md << EOF
## Milestone

Этот релиз основан на [Milestone $VERSION]($MILESTONE_URL).

**Прогресс:** $CLOSED_ISSUES/$CLOSED_ISSUES Issues завершено (100%)

## Breaking Changes

*Нет*

**Full Changelog**: $COMPARE_URL
EOF
```

> **Примечание:** Секция «What's Changed» добавляется автоматически через `--generate-notes` на шаге 5. Если `--generate-notes` не найдёт PR — добавить вручную.

---

### Шаг 5: Создать Release

**SSOT:** [standard-release.md § 10](./standard-release.md#10-создание-релиза)

```bash
# Переключиться на main
git checkout main
git pull origin main

# Создать Release с автогенерацией + кастомным body
gh release create $VERSION \
  --title "Release $VERSION" \
  --notes-file /tmp/release-notes.md \
  --generate-notes
```

> **`--generate-notes` + `--notes-file`:** GitHub объединяет кастомный body с автогенерированным списком PR. Кастомный body идёт ПЕРЕД автогенерацией.

**Проверить создание:**

```bash
# Тег создан
git fetch --tags
git tag | grep $VERSION

# Release опубликован
gh release view $VERSION
```

**Если Release нужен как Draft (публикация позже):**

```bash
gh release create $VERSION \
  --title "Release $VERSION" \
  --notes-file /tmp/release-notes.md \
  --generate-notes \
  --draft
```

---

### Шаг 6: Синхронизировать CHANGELOG.md

**SSOT:** [standard-release.md § 17](./standard-release.md#17-синхронизация-changelogmd-с-release)

**6.1. Если CHANGELOG.md не существует — создать:**

```bash
if [ ! -f CHANGELOG.md ]; then
  echo "CHANGELOG.md не найден — создаю по шаблону"
  # Создать из шаблона (см. standard-release.md § 5)
fi
```

**6.2. Получить Release Notes:**

```bash
gh release view $VERSION --json body -q '.body' > /tmp/release-body.md
```

**6.3. Добавить секцию в CHANGELOG.md:**

Вставить ПЕРЕД секцией `[Unreleased]` (или после неё, перед предыдущей версией):

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- {из Release Notes — feat PR}

### Fixed
- {из Release Notes — fix PR}
```

**6.4. Закоммитить:**

```bash
git add CHANGELOG.md
git commit -m "docs: update changelog for $VERSION"
git push origin main
```

> **Важно:** Коммит с CHANGELOG.md НЕ попадает в тег (тег уже создан). Это нормально.

---

### Шаг 7: Post-release валидация

**SSOT:** [validation-release.md](./validation-release.md), шаги 3–6

**Автоматически:**

```bash
python .github/.instructions/.scripts/validate-post-release.py --version $VERSION
```

**Если валидация показала ошибки — исправить:**

| Ошибка | Исправление |
|--------|-------------|
| Release Notes не содержит Milestone | `gh release edit $VERSION --notes "..."` |
| CHANGELOG.md не обновлён | Обновить и закоммитить |
| Деплой провалился | См. standard-release.md § 11 |

**Release Freeze снят.** Можно мержить PR в main.

---

## Чек-лист

- [ ] Analysis chains проверены (все DONE или --skip-chains)
- [ ] Версия определена из Milestone
- [ ] Release Freeze объявлен
- [ ] Pre-release валидация пройдена (скрипт)
- [ ] Release Notes собраны (Milestone link + changelog)
- [ ] Release создан (`gh release create`)
- [ ] Git-тег создан автоматически
- [ ] CHANGELOG.md синхронизирован
- [ ] Post-release валидация пройдена (скрипт)
- [ ] Release Freeze снят

---

## Примеры

### Стандартный Release

```bash
VERSION="v1.0.0"
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

# 1. Pre-release валидация
python .github/.instructions/.scripts/validate-pre-release.py --version $VERSION

# 2. Получить Milestone URL
MILESTONE_NUMBER=$(gh api repos/$OWNER/$REPO/milestones?state=closed --method GET \
  -q ".[] | select(.title == \"$VERSION\") | .number")
MILESTONE_URL=$(gh api repos/$OWNER/$REPO/milestones/$MILESTONE_NUMBER --method GET -q '.html_url')

# 3. Создать Release
git checkout main && git pull origin main
gh release create $VERSION \
  --title "Release $VERSION" \
  --generate-notes \
  --notes "## Milestone
Этот релиз основан на [Milestone $VERSION]($MILESTONE_URL).
"

# 4. Post-release валидация
python .github/.instructions/.scripts/validate-post-release.py --version $VERSION --skip-deploy
```

### Hotfix Release

```bash
VERSION="v1.0.1"

# Процесс hotfix описан в standard-release.md § 12
# После merge fix-PR в main:
python .github/.instructions/.scripts/validate-pre-release.py --version $VERSION --skip-tests
gh release create $VERSION --title "Release $VERSION" --generate-notes
python .github/.instructions/.scripts/validate-post-release.py --version $VERSION
```

### Первый Release (нет предыдущих тегов)

```bash
VERSION="v0.1.0"

python .github/.instructions/.scripts/validate-pre-release.py --version $VERSION
gh release create $VERSION \
  --title "Release $VERSION" \
  --notes "## Initial Release

Первый релиз проекта.

## What's Changed
- Начальная структура проекта
- CI/CD pipeline
- Документация
"
python .github/.instructions/.scripts/validate-post-release.py --version $VERSION --skip-deploy
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-pre-release.py](../.scripts/validate-pre-release.py) | Pre-release валидация | [validation-release.md](./validation-release.md) |
| [validate-post-release.py](../.scripts/validate-post-release.py) | Post-release валидация | [validation-release.md](./validation-release.md) |

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/release-create](/.claude/skills/release-create/SKILL.md) | Обёртка этой инструкции |
| [/post-release](/.claude/skills/post-release/SKILL.md) | Post-release валидация (Шаг 7) |
