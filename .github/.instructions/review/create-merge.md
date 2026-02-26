---
description: Воркфлоу merge PR — pre-checks, squash merge, post-merge sync, cleanup, verification.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/review/README.md
---

# Воркфлоу merge PR

Рабочая версия стандарта: 1.3

Процесс merge PR: получение информации, 9 pre-merge проверок, подтверждение, squash merge, post-merge sync и cleanup, верификация, продолжение workflow.

**Полезные ссылки:**
- [Инструкции review](./README.md)
- [Стандарт Review и Merge](./standard-review.md) — SSOT правил merge
- [Стандарт синхронизации](../sync/standard-sync.md) — SSOT post-merge sync

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-review.md](./standard-review.md) |
| Валидация | [validation-review.md](./validation-review.md) |
| Создание | Этот документ |
| Модификация | *Будет создан* |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Получение информации о PR](#шаг-1-получение-информации-о-pr)
  - [Шаг 2: Pre-merge checks](#шаг-2-pre-merge-checks)
  - [Шаг 3: Preview и подтверждение](#шаг-3-preview-и-подтверждение)
  - [Шаг 4: Merge execution](#шаг-4-merge-execution)
  - [Шаг 5: Post-merge sync](#шаг-5-post-merge-sync)
  - [Шаг 6: Post-merge cleanup](#шаг-6-post-merge-cleanup)
  - [Шаг 7: Post-merge verification](#шаг-7-post-merge-verification)
  - [Шаг 8: Workflow continuation](#шаг-8-workflow-continuation)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Подтверждение обязательно.** Merge — необратимое действие. Всегда показать preview и запросить подтверждение через AskUserQuestion.

> **Правила — из стандарта.** Все правила merge — в [standard-review.md](./standard-review.md). Эта инструкция описывает процесс, не правила.

> **Sync — часть merge.** Post-merge sync, cleanup и verification выполняются как единый процесс (шаги 5-7).

> **Auto-merge при ожидании.** Если CI ещё выполняется — использовать `--auto`, а не ждать.

---

## Шаги

### Шаг 1: Получение информации о PR

Получить полную информацию одним запросом:

```bash
gh pr view {N} --json number,title,body,labels,milestone,isDraft,mergeable,reviewDecision,mergeStateStatus,headRefName,baseRefName
```

1. Парсинг `Closes #N` из body для определения связанных Issues
2. Извлечение `headRefName` для post-merge cleanup (удаление локальной ветки)
3. Если PR не найден — сообщить: "PR #{N} не найден"

### Шаг 2: Pre-merge checks

Выполнить 9 проверок. Проверки 1-5 блокирующие, 6-9 рекомендуемые.

| # | Проверка | Источник | Блокирующая |
|---|---------|----------|:-----------:|
| 1 | CI passed | `gh pr checks {N}` — все `conclusion: SUCCESS` | Да |
| 2 | PR approved | `reviewDecision` = `APPROVED` | Да |
| 3 | No conflicts | `mergeable` = `MERGEABLE` | Да |
| 4 | Not draft | `isDraft` = `false` | Да |
| 5 | No requested changes | `reviewDecision` ≠ `CHANGES_REQUESTED` | Да |
| 6 | Branch up-to-date | `mergeStateStatus` = `CLEAN` | Рекомендуемая |
| 7 | Body содержит `Closes #` | `body` + regex | Рекомендуемая |
| 8 | Labels присутствуют | `labels` непустой | Рекомендуемая |
| 9 | Milestone привязан | `milestone` не null | Рекомендуемая |

Результат: таблица с  / X по каждой проверке.

Если хоть одна блокирующая проверка не пройдена — merge невозможен. Показать причину и рекомендацию:

| Провал | Рекомендация |
|--------|-------------|
| CI не пройден | "Дождитесь CI или исправьте ошибки" |
| Нет approve | "Выполните `gh pr review {N} --approve`" |
| Конфликты | "Разрешите конфликты: `git pull origin main` в feature-ветке" |
| Draft | "Переведите в Ready: `gh pr ready {N}`" |
| Requested changes | "Устраните замечания reviewer" |

Если блокирующие проверки пройдены, но CI ещё выполняется — предложить `--auto` (см. Шаг 4).

### Шаг 3: Preview и подтверждение

Показать пользователю через AskUserQuestion:

```
PR #{N}: {title}
Branch: {headRefName} → {baseRefName}
Issues: Closes #{...}
Checks: ✅ 5/5 блокирующих, ⚠️ 2/4 рекомендуемых
Labels: {labels}
Milestone: {milestone}
Способ: --squash --delete-branch
```

Запросить подтверждение: "Выполнить merge?"

Опции:
1. Да, merge сейчас
2. Да, auto-merge (ожидать CI)
3. Нет, отменить

### Шаг 4: Merge execution

1. Определить способ по выбору пользователя и состоянию checks:

| Условие | Команда |
|---------|---------|
| Все checks passed + пользователь выбрал "merge сейчас" | `gh pr merge {N} --squash --delete-branch` |
| CI ещё выполняется ИЛИ пользователь выбрал "auto-merge" | `gh pr merge {N} --auto --squash --delete-branch` |

2. Выполнить merge
3. Обработка ошибок (SSOT: [standard-review.md § 7](./standard-review.md#7-cli-команды)):

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `HTTP 403` | Нет прав | Проверить `gh auth status` |
| `pull request is in clean status` | PR уже смержен | Проверить `gh pr view {N}` |
| `merge conflict` | Конфликты | См. [standard-review.md § 3](./standard-review.md#разрешение-конфликтов) |
| `required status checks` | CI не пройден | Дождаться CI |
| `review is required` | Нет approve | `gh pr review {N} --approve` |

### Шаг 5: Post-merge sync

SSOT: [standard-sync.md](../sync/standard-sync.md).

1. Проверить незакоммиченные изменения:
   ```bash
   git status --porcelain
   ```
   Если не пусто — `git stash save "WIP: pre-merge-sync"`

2. Обновить remote refs:
   ```bash
   git fetch origin
   ```

3. Проверить актуальность main:
   ```bash
   git rev-parse main
   git rev-parse origin/main
   ```
   Если SHA совпадают — main уже актуальна, пропустить pull.

4. Если SHA различаются:
   ```bash
   git checkout main
   git pull --ff-only origin main
   ```

5. Если stash был создан — `git stash pop`

### Шаг 6: Post-merge cleanup

1. Удалить локальную ветку (remote удалён `--delete-branch`):
   ```bash
   git branch -d {headRefName}
   ```

2. Удалить stale remote-tracking refs:
   ```bash
   git fetch --prune
   ```

3. Проверить orphaned branches:
   ```bash
   git branch -vv | grep ': gone]'
   ```
   Если найдены — показать список пользователю.

### Шаг 7: Post-merge verification

1. Для каждого `Closes #N` из body — проверить закрытие:
   ```bash
   gh issue view {N} --json state
   ```
   Ожидаемое значение: `CLOSED`

2. Если Issue не закрылся — предупредить: "Issue #{N} не закрыт. Возможно, `Closes #{N}` отсутствовал в body PR."

### Шаг 8: Workflow continuation

1. Проверить наличие analysis chain в RUNNING:
   ```bash
   python specs/.instructions/.scripts/chain_status.py --status
   ```

2. Если chain в RUNNING — спросить пользователя: "Все задачи завершены? Перейти к `/analysis-status` для RUNNING -> REVIEW?"

3. Проверить milestone:
   ```bash
   gh issue list --milestone "{M}" --state open --json number
   ```
   Если открытых Issues нет — предложить: "Все Issues milestone закрыты. Запустить `/milestone-validate`?"

---

## Чек-лист

### Информация
- [ ] PR информация получена (`gh pr view --json`)
- [ ] Связанные Issues определены (`Closes #N`)
- [ ] Branch name извлечён

### Pre-merge
- [ ] 5 блокирующих проверок пройдены
- [ ] 4 рекомендуемые проверки проверены
- [ ] Preview показан пользователю
- [ ] Подтверждение получено

### Merge
- [ ] Способ определён (squash / auto --squash)
- [ ] Merge выполнен
- [ ] Ошибки обработаны (если были)

### Post-merge
- [ ] Main синхронизирован (`git pull --ff-only`)
- [ ] Локальная ветка удалена (`git branch -d`)
- [ ] Stale refs удалены (`git fetch --prune`)
- [ ] Issues проверены на закрытие
- [ ] Workflow continuation предложен

---

## Примеры

### Простой merge

```bash
# 1. Информация
gh pr view 42 --json number,title,body,labels,milestone,isDraft,mergeable,reviewDecision,mergeStateStatus,headRefName,baseRefName

# 2. Pre-merge checks — все пройдены
# 3. Preview → пользователь подтвердил

# 4. Merge
gh pr merge 42 --squash --delete-branch

# 5. Sync
git fetch origin
git checkout main
git pull --ff-only origin main

# 6. Cleanup
git branch -d 0042-add-login
git fetch --prune

# 7. Verification
gh issue view 130 --json state
# → CLOSED
```

### Auto-merge (CI ещё выполняется)

```bash
# Pre-merge checks: CI в процессе, approve есть
gh pr merge 42 --auto --squash --delete-branch
# PR встанет в очередь, merge произойдёт автоматически при прохождении CI
```

### Merge с stash

```bash
# Есть незакоммиченные изменения
git stash save "WIP: pre-merge-sync"
git fetch origin
git checkout main
git pull --ff-only origin main
git stash pop
# Продолжить cleanup
```

---

## Скрипты

*Нет скриптов.*

---

## Скиллы

*Нет скиллов.*
