# Скилл /merge — оценка и план

Скилл для squash merge PR с проверками перед мержем.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G6 из standard-process.md — нет `/merge` скилла
**Почему создан:** Определить нужен ли скилл или достаточно `gh pr merge --squash`
**Связанные файлы:**
- `/.github/.instructions/review/standard-review.md` — § 3 Merge стратегии
- `specs/.instructions/standard-process.md` — §5 Фаза 4, шаг 4.4

## Содержание

### Что уже покрыто

- `standard-review.md § 3` — стратегия: всегда squash merge
- Одна команда: `gh pr merge {PR-N} --squash`

### Что мог бы добавить скилл

| Функция | Сейчас | С `/merge` |
|---------|--------|-----------|
| Merge команда | Одна команда вручную | Тот же `gh pr merge` |
| Pre-merge проверки | Ручные | Автоматические: CI passed, approvals, no conflicts |
| Post-merge sync | Отдельная команда | Автоматически `git checkout main && git pull` |
| Issue закрытие | Автоматически через `Closes #N` | Проверка что Issues закрылись |

### Артефакты

| # | Артефакт | Путь | Статус |
|---|---------|------|--------|
| 1 | **Инструкция** (SSOT) | `/.github/.instructions/review/create-merge.md` | **Нужно создать** |
| 2 | **Скилл** (обёртка) | `/.claude/skills/merge/SKILL.md` | **Нужно создать** |

### Формат вызова

```
/merge {PR-N}
```

### Порядок создания

1. `/instruction-create create-merge --path .github/.instructions/review/`
2. `/skill-create merge`

## Решения

- Приоритет низкий — одна команда CLI
- Ценность в pre/post-merge проверках, не в самом merge

## Открытые вопросы

- Объединить с `/sync` в один скилл `/merge-and-sync`?
- Нужны ли pre-merge проверки если CI уже проверяет?

---

## Что уже описано в проекте

### standard-review.md — полный SSOT merge-процесса

**Файл:** `/.github/.instructions/review/standard-review.md`

- **§ 3 Merge стратегии** — default: squash merge (`gh pr merge {N} --squash`). Описаны три стратегии: squash, merge commit, rebase. Формат итогового commit message: `{type}: {описание} (#{PR})` + `Closes #{issue}`.
- **§ 3 Auto-merge** — `gh pr merge {N} --auto --squash`. Условия: CI success, approvals, no requested changes, no conflicts. Когда использовать: ожидание CI 5+ минут, вне рабочего времени, ожидание approval. Граничные случаи auto-merge подробно описаны (CI перезапуск, отзыв approval, новые коммиты, конфликты). Отмена: `gh pr merge {N} --disable-auto`.
- **§ 3 Разрешение конфликтов** — `git pull origin main` в feature-ветке, разрешить, push. Правило: >3 файлов ИЛИ >50 строк -- сообщить пользователю.
- **§ 3 После merge** — remote ветка удаляется, Issues закрываются (через `Closes #N`), PR --> "Merged". Локальная очистка --> standard-branching.md. Синхронизация --> standard-sync.md.
- **§ 2 Approve и Merge** — обязательный порядок: `gh pr review {N} --approve` --> `gh pr merge {N} --squash`. Агент НЕ выполняет approve автоматически.
- **§ 4 Branch Protection Rules** — таблица рекомендуемых правил для main (require PR, require approvals, require status checks, require up-to-date, require conversation resolution, require signed commits).
- **§ 5 Блокирующие условия** — PR не мержится при: CI fails, requested changes, merge conflicts, draft status, branch protection violation.
- **§ 7 CLI команды** — все варианты `gh pr merge`: `--squash`, `--merge`, `--rebase`, `--auto --squash`, `--squash --delete-branch`. Таблица обработки ошибок (403, clean status, conflict, required checks, review required).
- **§ 6 Граничные случаи** — закрытие PR без merge, провал CI checks (процесс исправления), откат после merge (revert через PR и через CLI).

### standard-pull-request.md — жизненный цикл PR

**Файл:** `/.github/.instructions/pull-requests/standard-pull-request.md`

- **§ 2 Жизненный цикл** — стадия 4 (MERGE): все проверки пройдены, 1+ approval, нет requested changes, нет conflicts --> squash merge --> ветка удаляется --> Issues закрываются.
- **§ 6 Связь с Issues** — `Closes #N` формат, группировка Issues (одна фича = один PR). Issues закрываются ТОЛЬКО после merge.
- **§ 8 Review и Merge** — ссылается на standard-review.md как SSOT.
- **§ 9 CLI** — полный набор `gh pr merge` команд (идентичен standard-review.md § 7).
- **§ 10 Граничные случаи** — hotfix процесс, длительная разработка, координация зависимых PR.

### standard-sync.md — синхронизация после merge

**Файл:** `/.github/.instructions/sync/standard-sync.md`

- **§ 2 Обязательные триггеры** — "После merge PR в main" --> `main` с remote.
- **§ 3 Синхронизация main** — `git checkout main && git pull origin main`. Проверка актуальности: `git fetch origin && git rev-parse main` vs `git rev-parse origin/main`.
- Ошибки: `fatal: unable to access` (сеть), `error: Your local changes` (stash), `CONFLICT` (нарушение workflow --> `git reset --hard origin/main`).

### standard-branching.md — удаление ветки после merge

**Файл:** `/.github/.instructions/branches/standard-branching.md`

- **§ 3 Завершение** — после merge ветка ДОЛЖНА быть удалена. Рекомендуется: Settings --> "Automatically delete head branches". Вручную: `git branch -d {branch} && git fetch --prune`.

### standard-process.md — место merge в общем процессе

**Файл:** `/specs/.instructions/standard-process.md`

- **Фаза 4 (Доставка в main):** шаг 4.4 Merge (squash merge, Issues закрываются) --> шаг 4.5 Sync main.
- **Quick Reference:** `gh pr merge {PR-N} --squash` --> `git checkout main && git pull`.
- **§ 10 Пробелы:** G6 -- нет `/merge` скилла (низкий приоритет), G7 -- нет `/sync` скилла (низкий приоритет). Оба могут быть объединены.
- **§ 8 Сводная таблица:** шаг 4.4 Merge -- инструкция: standard-review.md § 3, скилл: нет, агент: нет, скрипт: нет.

### standard-github-workflow.md — оркестратор

**Файл:** `/.github/.instructions/standard-github-workflow.md`

- **§ 10 Стадия 8: Merge** — SSOT: standard-review.md. Default: squash merge. После merge: ветка удаляется, Issues закрываются. Синхронизация: § 11.

### validation-review.md — проверки перед merge

**Файл:** `/.github/.instructions/review/validation-review.md`

- **Шаг 8 Вердикт** — READY (0 P1, 0 P2) --> "PR готов к approve". NOT READY (есть P2) --> "PR требует исправлений". CONFLICT (есть P1) --> CONFLICT цепочки.
- Агент НЕ выполняет approve. Пользователь вручную: `gh pr review --approve` --> `gh pr merge --squash`.

### /review скилл — предшествующий скилл

**Файл:** `/.claude/skills/review/SKILL.md`

- Шаг 10: если PR-режим -- пишет `gh pr comment` с резюме. НЕ делает merge. Merge -- отдельный шаг после review.
- Prerequisite check: проверяет `status:` в plan-dev.md (RUNNING/WAITING/CONFLICT/DONE).

### /sync драфт — смежный скилл

**Файл:** `/.claude/drafts/2026-02-24-sync-skill.md`

- Открытый вопрос: "Объединить с `/merge` в один скилл?"
- Функции /sync: stash/unstash, `git branch -d`, предложить `/analysis-status`.

### /pr-create драфт — предшествующий скилл

**Файл:** `/.claude/drafts/2026-02-24-pr-create.md`

- Создаёт PR с автосбором Issues из plan-dev.md. Preview перед созданием. Скилл-цепочка: `/pr-create` --> `/review {N}` --> `/merge {N}`.

---

## Best practices

### Squash merge: когда и зачем

- **Чистая история main** -- один коммит на фичу, легко читать `git log`, легко находить изменения по `git blame`.
- **Atomic rollback** -- `git revert {single-hash}` откатывает всю фичу целиком. Нет необходимости откатывать N коммитов.
- **Changelog-friendly** -- автоматическая генерация changelog по commit messages (каждый коммит = одна фича/PR).
- **CI/CD atomic deployments** -- каждый push в main = один коммит = один деплой. Линейная история упрощает автоматизацию.
- **Ограничение** -- squash уничтожает историю промежуточных коммитов. Для восстановления контекста полагаться на ссылку `(#{PR})` в commit message, которая ведёт к полной дискуссии и diff в PR.
- **git bisect** -- squash merge ухудшает гранулярность bisect (один большой коммит вместо N мелких). Для проектов с analysis chain это приемлемо: PR привязан к analysis chain, контекст всегда доступен.

### Pre-merge checks: что проверять программно

| # | Проверка | Команда/API | Блокирующая? |
|---|---------|-------------|:------------:|
| 1 | CI status (все checks passed) | `gh pr checks {N} --json name,state,conclusion` | Да |
| 2 | PR approved (минимум 1 approval) | `gh pr view {N} --json reviewDecision` -- значение `APPROVED` | Да |
| 3 | No merge conflicts | `gh pr view {N} --json mergeable` -- значение `MERGEABLE` | Да |
| 4 | PR не Draft | `gh pr view {N} --json isDraft` -- значение `false` | Да |
| 5 | No requested changes | `gh pr view {N} --json reviewDecision` -- не `CHANGES_REQUESTED` | Да |
| 6 | Branch up-to-date with base | `gh pr view {N} --json mergeStateStatus` -- значение `CLEAN` | Рекомендуемая |
| 7 | Body содержит `Closes #` | `gh pr view {N} --json body` + regex check | Рекомендуемая |
| 8 | Labels присутствуют (type + priority) | `gh pr view {N} --json labels` | Рекомендуемая |
| 9 | Milestone привязан | `gh pr view {N} --json milestone` | Рекомендуемая |

**Почему pre-merge checks полезны даже при наличии CI и Branch Protection:**
- Branch Protection Rules могут быть не настроены (новый репозиторий, solo-developer).
- Проверки 7-9 (body, labels, milestone) НЕ покрываются CI и Branch Protection -- это бизнес-правила проекта.
- Скилл дает human-readable сообщение об ошибке вместо cryptic GitHub API error.
- Скилл может предложить fix: "Нет milestone -- запустить `/milestone-create`?"

### Post-merge automation: что делать после merge

| # | Действие | Команда | Обоснование |
|---|---------|---------|-------------|
| 1 | Sync main | `git checkout main && git pull origin main` | Локальная main устарела |
| 2 | Удалить локальную ветку | `git branch -d {branch}` | Очистка (remote удалён автоматически) |
| 3 | Prune remote-tracking | `git fetch --prune` | Удалить stale remote-tracking refs |
| 4 | Проверить закрытие Issues | `gh issue view {N} --json state` для каждого Issue | Убедиться что `Closes #N` сработал |
| 5 | Предложить `/analysis-status` | Если chain в RUNNING --> подсказать перевод в REVIEW | Продолжение workflow (Фаза 5) |
| 6 | Предложить Release | Если все Issues milestone закрыты --> подсказать `/milestone-validate` | Продолжение workflow (Фаза 6) |

### GitHub auto-merge (`--auto`)

- `gh pr merge {N} --auto --squash` -- ставит PR в очередь на merge при выполнении всех условий.
- Подходит когда: CI ещё выполняется (5+ минут), ожидание approval, вне рабочего времени.
- НЕ подходит когда: все условия уже выполнены (мержить сразу), срочный hotfix (мержить сразу).
- Граничные случаи: новые коммиты отключают auto-merge; отзыв approval блокирует; конфликты блокируют.
- Скилл может: определять нужен ли `--auto` или прямой merge, и выбирать автоматически.

### GitHub Merge Queue (продвинутая фича)

- Merge Queue создаёт виртуальную очередь, где PR тестируются последовательно с учётом изменений предыдущих PR в очереди.
- Требует настройки CI для `merge_group` event в GitHub Actions.
- Полезен для команд 20+ разработчиков с высокой частотой merge.
- Для solo/small team (текущий проект) -- избыточен. Branch Protection + `--auto` достаточно.
- При масштабировании проекта -- рассмотреть включение Merge Queue через Settings --> Branches --> Branch protection rules --> "Require merge queue".

### Merge + Sync = один скилл?

**Аргументы за объединение (`/merge-and-sync`):**
- В стандарте шаги 4.4 и 4.5 идут строго последовательно, без промежуточных действий.
- Пользователь всегда выполняет sync после merge. Два вызова вместо одного -- рутина.
- `/pr-create` объединяет push + create -- аналогичный паттерн.

**Аргументы против объединения:**
- Принцип single responsibility: merge -- GitHub operation, sync -- git operation.
- Sync может потребоваться без merge (например, коллега смержил свой PR).
- `/sync` имеет собственную ценность (stash/unstash, prune, предложить analysis-status).

**Компромисс:** `/merge {N}` выполняет merge + предлагает sync. `/sync` существует отдельно для standalone синхронизации. `/merge` в post-merge шагах вызывает логику sync автоматически, но `/sync` может быть вызван независимо.

### Паттерн скилла: скрипт vs LLM

- **Не нужен скрипт.** В отличие от `/pr-create` (где скрипт собирает Issues из plan-dev.md), `/merge` работает с одним PR -- все данные доступны через `gh pr view {N} --json ...`.
- **Не нужен агент.** Процесс формульный: проверки --> approve --> merge --> cleanup.
- **LLM-оркестратор достаточен:** прочитать SSOT, выполнить pre-checks через gh CLI, показать результат пользователю, выполнить merge, cleanup.

### Безопасность: подтверждение перед merge

- Скилл ДОЛЖЕН показать preview (PR title, Issues, checks status) и запросить подтверждение через AskUserQuestion перед `gh pr merge`.
- Это защита от случайного merge не того PR или merge при неготовых проверках.
- `--dry-run` опция: показать что будет сделано, не выполнять merge.
