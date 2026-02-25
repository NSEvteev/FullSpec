---
description: Инструкция create-merge.md + merge-agent — squash merge с pre/post проверками и post-merge sync
type: feature
status: ready
created: 2026-02-24
---

# Merge — инструкция + агент (не скилл)

Вместо скилла `/merge`: создать инструкцию процесса и merge-agent для экономии контекста основного LLM.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G6+G7 из standard-process.md — нет `/merge` и `/sync` скиллов
**Почему создан:** Анализ показал, что скилл расходует контекст основного LLM без необходимости. Вместо этого: инструкция (SSOT процесса) + агент (subprocess). `/sync` как отдельный скилл не нужен — post-merge sync включён в merge-agent.
**Связанные файлы:**
- `/.github/.instructions/review/standard-review.md` — § 3 Merge стратегии (SSOT правил)
- `/.github/.instructions/sync/standard-sync.md` — стандарт синхронизации (post-merge sync)
- `specs/.instructions/standard-process.md` — §5 Фаза 4, шаг 4.4-4.5
- `.claude/drafts/2026-02-24-commit-skill.md` — паттерн: инструкция + агент

## Содержание

### Почему не скилл

| Критерий | Скилл `/merge` | Агент `merge-agent` |
|----------|----------------|---------------------|
| Контекст основного LLM | Тратит (скилл = промпт в основном контексте) | Не тратит (subprocess) |
| Чтение стандарта | Каждый раз в основном контексте | Один раз в subprocess |
| Вызов | Явный `/merge {N}` | Автоматический через Task tool |
| Поддержка | Скилл + инструкция | Агент + инструкция |

Агент решает главную проблему — **экономия контекста** — лучше, чем скилл.

### Архитектура

```
standard-review.md § 3         (правила merge — что)
standard-sync.md               (правила sync — что)
       ↓ ссылаются
create-merge.md                (инструкция процесса — как)
       ↓ SSOT для
merge-agent (AGENT.md)         (исполнитель — делает)
```

### Обогащение стандартов: не требуется

- **standard-review.md** — уже покрывает merge исчерпывающе: стратегии (§3), блокирующие условия (§5), CLI команды (§7), граничные случаи (§6).
- **standard-sync.md** — уже покрывает sync полностью: триггеры (§2), процесс (§3), конфликты (§4).
- Операционные детали (exact `--json` поля, порядок шагов cleanup) — контент для инструкции, не для стандарта.

### Артефакт 1: Инструкция `create-merge.md`

**Путь:** `/.github/.instructions/review/create-merge.md`
**Действие:** Создать через `/instruction-create`.
**Тип:** воркфлоу (create-*)

Содержание инструкции — операционные детали процесса merge:

#### 1.1. Получение информации о PR

1. `gh pr view {N} --json number,title,body,labels,milestone,isDraft,mergeable,reviewDecision,mergeStateStatus,headRefName,baseRefName` — полная информация одним запросом.
2. Парсинг `Closes #N` из body для определения связанных Issues.
3. Извлечение branch name для post-merge cleanup.

#### 1.2. Pre-merge checks (9 проверок)

| # | Проверка | Поле `--json` | Блокирующая |
|---|---------|---------------|:-----------:|
| 1 | CI passed | `gh pr checks {N}` → все `conclusion: SUCCESS` | Да |
| 2 | PR approved | `reviewDecision` = `APPROVED` | Да |
| 3 | No conflicts | `mergeable` = `MERGEABLE` | Да |
| 4 | Not draft | `isDraft` = `false` | Да |
| 5 | No requested changes | `reviewDecision` ≠ `CHANGES_REQUESTED` | Да |
| 6 | Branch up-to-date | `mergeStateStatus` = `CLEAN` | Рекомендуемая |
| 7 | Body содержит `Closes #` | `body` + regex | Рекомендуемая |
| 8 | Labels присутствуют | `labels` непустой | Рекомендуемая |
| 9 | Milestone привязан | `milestone` не null | Рекомендуемая |

Результат: таблица ✅/❌ по каждой проверке. Если хоть одна блокирующая ❌ — merge невозможен, показать причину и рекомендацию.

#### 1.3. Preview и подтверждение

Показать пользователю через AskUserQuestion:
- PR title, номер, branch
- Связанные Issues (`Closes #N`)
- Статус checks (✅/❌)
- Labels, milestone
- Рекомендуемый способ: `--squash` (default) или `--auto --squash`

Запросить подтверждение: "Выполнить merge?" — обязательно, необратимое действие.

#### 1.4. Merge execution

1. Определить способ:
   - Все checks passed + approved → прямой `gh pr merge {N} --squash --delete-branch`
   - CI ещё выполняется / ожидание approval → `gh pr merge {N} --auto --squash --delete-branch`
2. Выполнить merge.
3. Обработка ошибок: 403 (permissions), conflict, required checks, review required — таблица из standard-review.md §7.

#### 1.5. Post-merge sync

SSOT: standard-sync.md.

1. `git status --porcelain` — если не пусто, `git stash save "WIP: pre-merge-sync"`
2. `git fetch origin`
3. Проверить актуальность: `git rev-parse main` vs `git rev-parse origin/main`
4. Если SHA различаются: `git checkout main && git pull --ff-only origin main`
5. Если stash был — `git stash pop`

#### 1.6. Post-merge cleanup

1. `git branch -d {branch}` — удалить локальную ветку (remote удалён `--delete-branch`)
2. `git fetch --prune` — удалить stale remote-tracking refs
3. Orphaned branches: `git branch -vv | grep ': gone]'` — показать если есть

#### 1.7. Post-merge verification

1. Проверить каждый `Closes #N` Issue: `gh issue view {N} --json state` = `CLOSED`
2. Если Issue не закрылся — предупредить (возможно `Closes` не было в body)

#### 1.8. Workflow continuation

1. Проверить наличие analysis chain в RUNNING: `python specs/.instructions/.scripts/chain_status.py --status`
2. Если chain RUNNING — спросить пользователя: "Все задачи завершены? Перейти к `/analysis-status` для RUNNING → REVIEW?"
3. Проверить milestone: `gh issue list --milestone {M} --state open --json number` — если открытых Issues нет, предложить `/milestone-validate`

### Артефакт 2: Агент `merge-agent`

**Путь:** `/.claude/agents/merge-agent/AGENT.md`
**Действие:** Создать через `/agent-create`.

**Конфигурация:**

| Поле | Значение |
|------|---------|
| name | merge-agent |
| description | Merge PR с pre/post проверками и sync |
| model | haiku (задача формульная) |
| allowed-tools | Bash, Read, Glob, Grep, AskUserQuestion |
| ssot | `/.github/.instructions/review/create-merge.md` |

**Промпт агента (суть):**
- Прочитать SSOT-инструкцию `create-merge.md`
- Получить PR номер из аргументов
- Выполнить алгоритм: info → pre-checks → preview → confirm → merge → sync → cleanup → verify → suggest next
- Вернуть результат: merge выполнен / ошибка + причина

**Вызов из основного LLM:**
```
Task tool → subagent_type: "general-purpose"
prompt: "Выполни merge PR #{N}. Прочитай инструкцию create-merge.md и следуй ей."
```

Rule `development.md` будет обновлён — добавить указание делегировать merge агенту.

**Изменение в rule:**
```
- Review и Merge: [standard-review.md](путь)
+ Review: [standard-review.md](путь)
+ Merge: делегировать агенту `merge-agent` через Task tool (SSOT: [create-merge.md](путь))
```

### Порядок создания

| # | Артефакт | Инструмент | Зависимости |
|---|---------|------------|-------------|
| 1 | Инструкция `create-merge.md` | `/instruction-create` | — |
| 2 | Агент `merge-agent` | `/agent-create` | ← 1 |
| 3 | Обновление `review/README.md` | Автоматически (шаги 1, 2) | ← 1, 2 |
| 4 | Обновление rule `development.md` | Ручное | ← 2 |
| 5 | Обновление `standard-process.md` §8/§10 | Ручное | ← 2 |
| 6 | Обновление `CLAUDE.md` | Ручное | ← 5 |

## Решения

- **Скилл `/merge` не создаём** — агент решает задачу экономии контекста лучше
- **Скилл `/sync` не создаём** — post-merge sync включён в merge-agent, standalone sync покрыт standard-sync.md
- **Стандарты не обогащаем** — standard-review.md и standard-sync.md уже исчерпывающие
- **Инструкция `create-merge.md`** — SSOT для операционных деталей (pre-checks, sync, cleanup, verification)
- **Агент `merge-agent`** — subprocess, читает инструкцию, выполняет merge + sync, экономит контекст
- **Модель агента: haiku** — задача формульная, шаблон в инструкции. Сменить на sonnet если качества недостаточно
- **AskUserQuestion** — обязательное подтверждение перед merge (необратимое действие)
- **Rule `development.md` обновить** — разделить review и merge, merge делегировать агенту
- **Review и merge раздельно** — намеренно: разные задачи, разные модели, разные точки выхода
- **`--delete-branch` всегда передавать** — идемпотентно, явно, без проверки настроек GitHub
- **Скрипт validate-merge-readiness.py не создавать** — YAGNI, вернуться при cicd-enhancements (Фаза 5)

## Открытые вопросы

- ~~Объединить с `/sync` в один скилл `/merge-and-sync`?~~ → **Решено:** `/sync` как отдельный скилл не нужен. Post-merge sync включён в merge-agent.
- ~~Нужны ли pre-merge проверки если CI уже проверяет?~~ → **Решено:** Проверки 7-9 (body, labels, milestone) НЕ покрываются CI/Branch Protection — это бизнес-правила проекта.

### Решённые вопросы (обсуждены с пользователем)

1. ~~**haiku vs sonnet для merge-agent**~~ → **haiku.** Задача формульная, шаблон preview зашит в инструкции. Если качества недостаточно — сменить на sonnet позже.

2. ~~**Нужен ли скрипт `validate-merge-readiness.py`?**~~ → **Не сейчас.** YAGNI. Вернуться при работе над cicd-enhancements (Фаза 5), если понадобится pre-merge gate в CI.

3. ~~**Review + Merge в одном агенте?**~~ → **Раздельно.** Намеренное разделение: review оценивает качество (sonnet/opus), merge — операция доставки (haiku). Разные задачи, разные модели, разные точки выхода.

4. ~~**`--delete-branch` в merge команде**~~ → **Всегда передавать.** Идемпотентно, явно, без лишних API calls. Проще одна строка в инструкции чем блок с проверкой настройки.

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
- **§ 10 Пробелы:** G6 -- нет `/merge` скилла (низкий приоритет), G7 -- закрыт (объединён с G6).
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

### /sync драфт — объединён в этот драфт

**Файл:** `/.claude/drafts/2026-02-24-sync-skill.md` *(удалён)*

- Решение: `/sync` как отдельный скилл не нужен. Post-merge sync включён в merge-agent.
- Функции из sync перенесены: stash/unstash, `git branch -d`, prune, `/analysis-status`.
- Standalone sync покрыт standard-sync.md без скилла.

### /pr-create драфт — предшествующий скилл

**Файл:** `/.claude/drafts/2026-02-24-pr-create.md`

- Создаёт PR с автосбором Issues из plan-dev.md. Preview перед созданием. Скилл-цепочка: `/pr-create` --> `/review {N}` --> merge-agent.

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
- Агент дает human-readable сообщение об ошибке вместо cryptic GitHub API error.
- Агент может предложить fix: "Нет milestone -- запустить `/milestone-create`?"

### Post-merge automation: что делать после merge

| # | Действие | Команда | Обоснование |
|---|---------|---------|-------------|
| 1 | Sync main | `git checkout main && git pull --ff-only origin main` | Локальная main устарела |
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
- Агент может: определять нужен ли `--auto` или прямой merge, и выбирать автоматически.

### GitHub Merge Queue (продвинутая фича)

- Merge Queue создаёт виртуальную очередь, где PR тестируются последовательно с учётом изменений предыдущих PR в очереди.
- Требует настройки CI для `merge_group` event в GitHub Actions.
- Полезен для команд 20+ разработчиков с высокой частотой merge.
- Для solo/small team (текущий проект) -- избыточен. Branch Protection + `--auto` достаточно.
- При масштабировании проекта -- рассмотреть включение Merge Queue через Settings --> Branches --> Branch protection rules --> "Require merge queue".

### Merge + Sync → решение

> **Решено:** `/sync` как отдельный скилл не создаётся. Post-merge sync включён в merge-agent. Standalone sync покрыт standard-sync.md без скилла.

**Аргументы за объединение (принято):**
- Шаги 4.4 и 4.5 идут строго последовательно — один вызов merge-agent покрывает оба.
- Standalone sync — 2 команды git, стандарт достаточен без скилла.
- `/pr-create` объединяет push + create — аналогичный паттерн.

**Post-merge sync включает (из драфта /sync):**
- `git checkout main && git pull --ff-only origin main` (безопаснее чем plain `git pull`)
- `git fetch --prune` — удалить stale remote-tracking refs
- `git branch -d {branch}` — удалить локальную merged-ветку
- Orphaned branch detection: `git branch -vv | grep ': gone]'`
- Idempotent: проверка SHA (`git rev-parse main` vs `git rev-parse origin/main`) перед pull
- Pre-sync safety: `git status --porcelain` → auto-stash если не пусто
- Предложить `/analysis-status` если chain в RUNNING

### Безопасность: подтверждение перед merge

- Агент ДОЛЖЕН показать preview (PR title, Issues, checks status) и запросить подтверждение через AskUserQuestion перед `gh pr merge`.
- Это защита от случайного merge не того PR или merge при неготовых проверках.
- `--dry-run` опция: показать что будет сделано, не выполнять merge.

---

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Создать инструкцию create-merge.md
  description: >
    Драфт: .claude/drafts/2026-02-24-merge-skill.md (секция "Артефакт 1")
    /instruction-create для .github/.instructions/review/create-merge.md.
    Содержание:
    - 1.1. Получение информации о PR (gh pr view --json)
    - 1.2. Pre-merge checks (9 проверок, таблица)
    - 1.3. Preview и подтверждение (AskUserQuestion)
    - 1.4. Merge execution (squash vs auto, обработка ошибок)
    - 1.5. Post-merge sync (standard-sync.md, --ff-only)
    - 1.6. Post-merge cleanup (branch -d, prune, orphaned)
    - 1.7. Post-merge verification (Issues closed)
    - 1.8. Workflow continuation (analysis-status, milestone)
  activeForm: Создаю create-merge.md

TASK 2: Создать агент merge-agent
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-merge-skill.md (секция "Артефакт 2")
    /agent-create для .claude/agents/merge-agent/AGENT.md.
    Конфигурация: model=haiku, tools=Bash/Read/Glob/Grep/AskUserQuestion,
    ssot=create-merge.md.
    Промпт: прочитать SSOT → info → pre-checks → preview → confirm → merge → sync → cleanup → verify.
  activeForm: Создаю merge-agent

TASK 3: Обновить review/README.md
  blockedBy: [1, 2]
  description: >
    Драфт: .claude/drafts/2026-02-24-merge-skill.md (секция "Порядок создания", шаг 3)
    Обновить .github/.instructions/review/README.md:
    - Добавить ссылку на create-merge.md (инструкция)
    - Добавить ссылку на merge-agent (агент)
    README обновляется автоматически при создании артефактов, но проверить полноту.
  activeForm: Обновляю review/README.md

TASK 4: Обновить rule development.md
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-merge-skill.md (секция "Артефакт 2", блок "Изменение в rule")
    В .claude/rules/development.md:
    - Разделить строку "Review и Merge" на две
    - Review: ссылка на standard-review.md
    - Merge: делегировать агенту merge-agent через Task tool
      (SSOT: create-merge.md)
  activeForm: Обновляю rule development.md

TASK 5: Обновить standard-process.md §8/§10
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-merge-skill.md (секция "Порядок создания", шаг 5)
    Обновить /specs/.instructions/standard-process.md:
    - §8: добавить ссылки на create-merge.md и merge-agent для шага 4.4
    - §10 G6: отметить как закрытый gap (инструкция + агент вместо скилла)
  activeForm: Обновляю standard-process.md

TASK 6: Обновить CLAUDE.md
  blockedBy: [5]
  description: >
    Драфт: .claude/drafts/2026-02-24-merge-skill.md (секция "Порядок создания", шаг 6)
    В CLAUDE.md отметить merge-skill (G6+G7) как [x] выполненный.
  activeForm: Обновляю CLAUDE.md
```
