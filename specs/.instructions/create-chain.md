---
description: Воркфлоу запуска analysis chain — определение пути, создание TaskList с полной последовательностью от идеи до релиза, возобновление после прерывания.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу запуска цепочки

Рабочая версия стандарта: 1.3

Оркестратор полного цикла: читает standard-process.md, создаёт TaskList через TaskCreate, устанавливает blockedBy-зависимости. Каждая задача = конкретный скилл + SSOT-ссылка.

**Полезные ссылки:**
- [Инструкции specs/](./README.md)

**SSOT-зависимости:**
- [standard-process.md](./standard-process.md) — маппинг шагов на инструменты (§§ 5-7)
- [standard-analysis.md](./analysis/standard-analysis.md) — 4 уровня, статусы, каскады
- [chain_status.py](./.scripts/chain_status.py) — управление статусами chain

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-analysis.md](./analysis/standard-analysis.md) |
| Валидация | *Не применимо* |
| Создание | Этот документ |
| Модификация | *Не применимо* |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Определить путь](#шаг-1-определить-путь)
  - [Шаг 2: Создать TaskList](#шаг-2-создать-tasklist)
  - [Шаг 3: Подтвердить TaskList](#шаг-3-подтвердить-tasklist)
  - [Шаг 4: Начать выполнение](#шаг-4-начать-выполнение)
  - [Шаг 5: Возобновление (при прерывании)](#шаг-5-возобновление-при-прерывании)
- [TaskList: шаблоны](#tasklist-шаблоны)
  - [Путь A: Happy Path (14 задач)](#путь-a-happy-path-14-задач)
  - [CONFLICT (динамические задачи)](#conflict-динамические-задачи)
  - [Путь C.1: Rollback](#путь-c1-rollback)
  - [Путь C.2: Hotfix](#путь-c2-hotfix)
  - [Путь C.4: Doc-only](#путь-c4-doc-only)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **`/chain` — ЕДИНСТВЕННАЯ рекомендуемая точка входа для изменений системы.** Гарантирует правильный порядок и набор скиллов. Исключение: пользователь явно просит конкретный скилл.

> **TaskList = исполняемый план, не документ.** LLM не просто знает порядок — он работает по нему, отмечая задачи completed. Прогресс виден и человеку, и LLM.

> **Каждая задача = конкретный скилл + SSOT-ссылка.** Нет абстрактных шагов — только вызовы инструментов.

> **blockedBy гарантирует порядок.** Нельзя начать Design без завершения Discussion. Это enforcement, не соглашение.

> **Возобновление через TaskList.** При прерывании LLM читает TaskList, находит первую pending без blockers и продолжает. Контекст не теряется.

> **Не заменяет standard-process.md.** standard-process.md — SSOT системы. `/chain` — фронтенд к нему. Эта инструкция читает standard-process.md, не дублирует.

---

## Шаги

### Шаг 1: Определить путь

Прочитать [standard-process.md § 3](./standard-process.md#3-выбор-пути). Спросить пользователя через AskUserQuestion:

**Вопрос:** "Что вы хотите сделать?"

**Опции:**

| Опция | Путь | Описание |
|-------|------|----------|
| Новая фича / изменение поведения | A (Happy Path) | Полная цепочка: Discussion → Design → Plan Tests → Plan Dev → Docs Sync → Development → PR → Merge → Release |
| Критический баг (hotfix) | A через C.2 | Полная цепочка + метки `bug`/`critical`, ветка `{NNNN}-hotfix-{topic}` |
| Несколько мелких багов | A через C.3 | Одна Discussion группирует фиксы, далее полная цепочка |
| Опечатки, форматирование | C.4 (Doc-only) | Без analysis chain: Issue → Branch → PR → Merge |

### Шаг 2: Создать TaskList

На основе пути создать задачи через TaskCreate. Шаблоны задач — см. [TaskList: шаблоны](#tasklist-шаблоны).

Для каждой задачи:
- `subject`: глагол + объект ("Создать Discussion")
- `description`: инструмент + что происходит + что делает пользователь + SSOT
- `activeForm`: present continuous ("Создаю Discussion")
- `blockedBy`: зависимости по порядку (IDs из TaskCreate)

**Формат инструмента в description:**
- Скилл → `Скилл: /skill-name` (вызывается через Skill tool)
- Агент → `Агент: agent-name` (вызывается через Task tool с subagent_type)
- Если задача использует и скилл, и агента — указать оба

**Подстановка `{NNNN}`:** Номер цепочки определяется в задаче 1 (Discussion создаёт `specs/analysis/{NNNN}-{topic}/`). В последующих задачах `{NNNN}` подставляется после завершения задачи 1.

**Создание задач (последовательно, 2 раунда):**

> **Параллельный TaskCreate не гарантирует последовательные ID.** При отправке N TaskCreate в одном сообщении система обрабатывает их в произвольном порядке → ID перемешиваются. Это ломает blockedBy и делает TaskList нечитаемым.

1. **Раунд 1:** Создать 16 TaskCreate **последовательно** (по одному за вызов). Каждый TaskCreate — отдельное сообщение. Без blockedBy (TaskCreate не поддерживает). Результат: 16 задач с последовательными ID.
2. **Раунд 2:** Отправить ВСЕ 13 TaskUpdate (addBlockedBy) **параллельно** в одном сообщении. ID известны из Раунда 1.

### Шаг 3: Подтвердить TaskList

Показать TaskList пользователю. AskUserQuestion: "План из N задач создан. Начинаем?"

| Опция | Действие |
|-------|----------|
| Да, начинаем | Перейти к Шагу 4 |
| Нужны корректировки | Пользователь указывает что изменить → внести изменения → повторить Шаг 3 |

### Шаг 4: Начать выполнение

TaskUpdate первой задачи → `in_progress`. Запустить соответствующий скилл из описания задачи.

При завершении задачи:
1. TaskUpdate → `completed`
2. Найти следующую pending задачу без blockers
3. TaskUpdate → `in_progress`, запустить скилл

### Шаг 5: Возобновление (при прерывании)

При `/chain --resume`:

**Шаг 5.1: Определить цепочку**
Если пользователь указал NNNN → использовать. Иначе → `chain_status.py status --all` → найти RUNNING цепочку.

**Шаг 5.2: Определить прогресс по артефактам**
Проверить реальное состояние цепочки, не полагаясь на TaskList:

| Артефакт | Как проверить | Если есть → TASK completed |
|----------|--------------|---------------------------|
| discussion.md | Файл существует, status ≠ DRAFT | TASK 1 |
| design.md | Файл существует, status ≠ DRAFT | TASK 2 |
| plan-test.md | Файл существует, status ≠ DRAFT | TASK 3 |
| plan-dev.md | Файл существует, status ≠ DRAFT | TASK 4 |
| specs/docs/{svc}.md | docs-synced: true в design.md | TASK 5 |
| Issues в plan-dev.md | Поле `Issue:` содержит `[#N]` (не `—`) | TASK 6 |
| Ветка + код | git branch, git log | TASK 7 (частично) |
| PR | gh pr list --head {branch} | TASK 10 |
| Merge | gh pr view --json merged | TASK 12 |

**Шаг 5.3: Восстановить TaskList**
Создать TaskList (шаблон Happy Path), пометить completed задачи по результатам Шаг 5.2.

**Шаг 5.4: Продолжить**
Найти первую pending задачу без blockers → запустить скилл.

---

## TaskList: шаблоны

### Путь A: Happy Path (16 задач)

```
TASK 1: Создать Discussion
  description: >
    Скилл: /discussion-create — описать проблему, требования, критерии успеха.
    Пользователь описывает идею → Claude задаёт уточняющие вопросы (Clarify) →
    генерирует discussion.md → пользователь ревьюит → WAITING.
    SSOT: standard-discussion.md
  activeForm: Создаю Discussion
  blockedBy: —

TASK 2: Создать Design
  description: >
    Скилл: /design-create — два агента последовательно:
    design-agent-first: Unified Scan (5 источников) → Clarify → Резюме + Выбор технологий → user подтверждает выбор.
    design-agent-second: детальные SVC-N (9 подсекций) + INT-N контракты + STS-N системные тесты.
    design-reviewer — один раз после обоих.
    SSOT: standard-design.md
  activeForm: Создаю Design
  blockedBy: [1]

TASK 3: Создать Plan Tests
  description: >
    Скилл: /plan-test-create — два агента последовательно:
    plantest-agent: генерация TC-N, fixtures, матрица покрытия, блоки тестирования.
    plantest-reviewer — проверка покрытия REQ-N/STS-N и формата.
    Файл создаётся скриптом create-analysis-plan-test-file.py → пользователь ревьюит → WAITING.
    SSOT: standard-plan-test.md
  activeForm: Создаю Plan Tests
  blockedBy: [2]

TASK 4: Создать Plan Dev
  description: >
    Скилл: /plan-dev-create — два агента последовательно:
    plandev-agent: генерация TASK-N, зависимости, BLOCK-N (per-service + INFRA + system).
    plandev-reviewer — проверка покрытия TC-N, формат TASK-N, PROP-N запись.
    Файл создаётся скриптом create-analysis-plan-dev-file.py → пользователь ревьюит → WAITING.
    SSOT: standard-plan-dev.md
  activeForm: Создаю Plan Dev
  blockedBy: [3]

TASK 5: Синхронизировать docs/
  description: >
    Скилл: /docs-sync {design-path} — параллельные агенты: service-agent × N,
    technology-agent × M, system-agent mode=sync (overview.md),
    docker-agent mode=scaffold (Docker scaffolding для новых сервисов).
    Три волны: создание → ревью → исправления (max 3 итерации).
    Маркер docs-synced: true в design.md.
    SSOT: create-docs-sync.md
  activeForm: Синхронизирую docs/
  blockedBy: [4]

TASK 6: Запустить разработку
  description: >
    Скилл: /dev-create {NNNN} — создание GitHub Issues, Milestone, Branch.
    Все 4 документа → RUNNING. Оркестрация Issues:
    - Волна 1: issue-agent × K параллельно (K = кол-во блоков в plan-dev.md) — создание Issues
    - Волна 2: issue-reviewer × K параллельно — дополнение + проверка по 7 критериям
    - Повторный запуск reviewer — по запросу пользователя
    Привязка к Milestone, создание feature-ветки.
    Пользователь проверяет на GitHub: Issues, Milestone, Branch.
    SSOT: create-development.md
  activeForm: Запускаю разработку
  blockedBy: [5]

TASK 7: Разработка
  description: >
    Агент: dev-agent — оркестрация разработки (код, тесты по BLOCK-N в изолированном контексте).
    dev-agent сигнализирует DOCKER_UPDATES → основной LLM вызывает docker-agent mode=update
    (паттерн pause/resume для Docker-операций).
    Коммиты: скилл /commit (Conventional Commits).
    Параллельные агенты по волнам. Per-service тесты внутри блока,
    системные тесты после волны.
    При CONFLICT → динамические задачи добавляются в TaskList (см. CONFLICT).
    SSOT: standard-development.md
  activeForm: Разработка
  blockedBy: [6]

TASK 8: Docker dev-окружение
  description: >
    Скилл: /docker-up — поднять Docker dev-окружение перед тестами.
    docker compose up -d --build, healthcheck всех сервисов.
    Предусловие: .env файл, Docker Desktop запущен.
    При unhealthy — СТОП, чинить Docker.
    SSOT: create-docker-env.md
  activeForm: Поднимаю Docker окружение
  blockedBy: [7]

TASK 9: Валидация и тесты
  description: >
    Скилл: /test — финальный прогон всех тестов и проверок после завершения разработки.
    Предусловие: Docker-окружение поднято (Task 8).
    Последовательно: sync main → make test → make lint → make build →
    make test-e2e (если API/DB/inter-service изменения по git diff) →
    проверка полноты реализации → отчёт.
    Вердикт: READY → ревью. NOT READY → вернуться к Task 7.
    SSOT: create-test.md → validation-development.md
  activeForm: Валидация и тесты
  blockedBy: [8]

TASK 10: Playwright UI smoke-тесты
  description: >
    Скилл: /test-ui — UI smoke-тесты через Playwright CLI (playwright-cli, agent).
    Предусловие: Docker-окружение (Task 8) + /test READY (Task 9).
    Выполнить SMOKE-NNN сценарии, сохранить скриншоты, сформировать отчёт.
    Вердикт: PASS → ревью ветки. FAIL → чинить UI, повторить /test-ui.
    SSOT: create-test-ui.md
  activeForm: Playwright UI smoke-тесты
  blockedBy: [9]

TASK 11: Ревью ветки
  description: >
    Скилл: /review — локальное ревью ветки перед PR.
    Агент: code-reviewer (анализ diff по 7 критериям, сверка со specs/analysis/).
    Вердикт: READY → продолжить, NOT READY → исправить, CONFLICT → Путь B.
    SSOT: standard-review.md
  activeForm: Ревью ветки
  blockedBy: [10]

TASK 12: Создать PR
  description: >
    Скилл: /pr-create (git push, gh pr create, сбор Issues через collect-pr-issues.py).
    Формирует body, привязывает labels.
    Пользователь проверяет PR на GitHub.
    SSOT: standard-pull-request.md, create-pull-request.md
  activeForm: Создаю PR
  blockedBy: [11]

TASK 13: Ревью PR
  description: >
    Скилл: /review {PR-N} — ревью PR на GitHub.
    Агент: code-reviewer (анализ diff по 7 критериям).
    Итерации: замечания → исправления → повторный /review.
    Вердикт READY → мержить. NOT READY → исправить. CONFLICT → Путь B.
    SSOT: standard-review.md
  activeForm: Ревью PR
  blockedBy: [12]

TASK 14: Merge
  description: >
    Скилл: /merge (squash merge PR, закрытие Issues, синхронизация main).
    Claude мержит PR, синхронизирует локальный main.
    SSOT: create-merge.md, standard-sync.md
  activeForm: Merge
  blockedBy: [13]

TASK 15: Завершить цепочку
  description: >
    Скилл: /chain-done — RUNNING → REVIEW → DONE, обновление docs/.
    Bottom-up каскад: plan-dev → plan-test → design → discussion.
    system-agent mode=done (все 4 .system/ файла) + system-reviewer mode=done.
    Обновление docs/: Planned Changes → AS IS, Changelog.
    Cross-chain проверка (check_cross_chain).
    SSOT: standard-analysis.md §§ 6.5-6.6, 7.3, create-chain-done.md
  activeForm: Завершаю цепочку
  blockedBy: [14]

TASK 16: Релиз (опционально)
  description: >
    Скилл: /release-create — GitHub Release: changelog, tag, milestone close.
    Пользователь решает: создавать релиз сейчас или накопить изменения.
    AskUserQuestion: "Создать релиз?" Если нет → задача удаляется (status: deleted).
    SSOT: standard-release.md, create-release.md
  activeForm: Создаю релиз
  blockedBy: [15]
```

**Динамическое поведение:**
- Task 16 (Релиз) — опциональная. Спросить через AskUserQuestion. Если нет — `TaskUpdate status: deleted`
- При CONFLICT на любом шаге — добавить задачи CONFLICT (ниже) в TaskList динамически
- `{NNNN}` подставляется из Task 1 (номер цепочки)

### CONFLICT (динамические задачи)

При обнаружении CONFLICT (во время Task 7, 11 или 13) добавить задачи разрешения в TaskList:

```
TASK N+1: Каскад CONFLICT
  description: >
    Скрипт: chain_status.py T4/T10 — вся цепочка → CONFLICT.
    Claude классифицирует уровень: Design / Plan Tests / Plan Dev / Discussion.
    Определяет самый высокий затронутый документ.
    SSOT: standard-analysis.md § 6.3
  activeForm: Каскад CONFLICT
  blockedBy: —  (вставляется сразу при обнаружении)

TASK N+2: Разрешить CONFLICT (сверху вниз)
  description: >
    Скилл: /{level}-modify для каждого затронутого документа, сверху вниз.
    Пользователь ревьюит каждый изменённый документ → WAITING.
    SSOT: standard-analysis.md § 6.4
  activeForm: Разрешаю CONFLICT
  blockedBy: [N+1]

TASK N+3: Повторный запуск
  description: >
    Скилл: /dev-create {NNNN} --resume — все WAITING → RUNNING.
    Новые Issues для задач, появившихся после разрешения.
    SSOT: standard-analysis.md § 6.2
  activeForm: Повторный запуск
  blockedBy: [N+2]
```

После TASK N+3 → возврат к задаче разработки (Task 7). blockedBy обновляется динамически.

### Путь C.1: Rollback

```
TASK R1: Откат цепочки
  description: >
    Агент: rollback-agent — T9 → откат артефактов → T10 → REJECTED.
    SSOT: standard-analysis.md §§ 6.7-6.8, create-rollback.md
  activeForm: Откат цепочки
```

### Путь C.2: Hotfix

Тот же TaskList что Happy Path (14 задач), но:
- Task 1 (Discussion): пометка "краткая Discussion, фокус на баге"
- Task 6 (dev-create): метки `bug` + `critical`, ветка `{NNNN}-hotfix-{topic}`
- Task 14 (Release): PATCH-версия (обязательна, не опциональна)

### Путь C.4: Doc-only

```
TASK 1: Doc-only изменение
  description: >
    Issue (опционально) → Branch → исправления → PR → Merge.
    Без analysis chain. Commit type: docs: или fix:.
    SSOT: standard-process.md § 7 C.4
  activeForm: Doc-only изменение
```

---

## Чек-лист

- [ ] Путь определён (A / C.2 / C.3 / C.4)
- [ ] TaskList создан с корректными blockedBy
- [ ] Каждая задача содержит скилл и SSOT-ссылку
- [ ] Пользователь подтвердил план
- [ ] Первая задача запущена

---

## Примеры

### Запуск новой фичи

```
# Пользователь: "Хочу добавить OAuth2 аутентификацию"

# Шаг 1: Определить путь → A (Happy Path)
# Шаг 2: TaskCreate × 14 задач (шаблон Happy Path)
# Шаг 3: "План из 14 задач создан. Начинаем?" → Да
# Шаг 4: Task 1 → in_progress → /discussion-create
```

### Возобновление после прерывания

```
# Пользователь: "/chain --resume"

# TaskList → задачи 1-6 completed, задача 7 in_progress
# chain_status.py status {NNNN} → RUNNING
# Продолжить с Task 7 → dev-agent (modify-development.md)
```

### Hotfix

```
# Пользователь: "/chain --hotfix"

# Шаг 1: Путь C.2 (Hotfix)
# Шаг 2: TaskCreate × 14 задач (Happy Path + метки bug/critical)
# Task 14: Release — обязательна, PATCH-версия
```

### Doc-only

```
# Пользователь: "/chain --doc-only"

# Шаг 1: Путь C.4
# Шаг 2: TaskCreate × 1 задача
# Task 1: Branch → fix → PR → Merge
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [chain_status.py](./.scripts/chain_status.py) | Управление статусами chain (status, transition) | [standard-analysis.md](./analysis/standard-analysis.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/chain](/.claude/skills/chain/SKILL.md) | Оркестратор полного цикла (TaskList) | Этот документ |
