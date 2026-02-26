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
  - [Путь A: Happy Path (12 задач)](#путь-a-happy-path-12-задач)
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

Прочитать [standard-process.md § 3](../standard-process.md#3-выбор-пути). Спросить пользователя через AskUserQuestion:

**Вопрос:** "Что вы хотите сделать?"

**Опции:**

| Опция | Путь | Описание |
|-------|------|----------|
| Новая фича / изменение поведения | A (Happy Path) | Полная цепочка: Discussion → Design → Plan Tests → Plan Dev → Development → PR → Merge → Release |
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

**Оптимизация создания (2 раунда вместо 23 вызовов):**
1. **Раунд 1:** Все 12 TaskCreate параллельно в одном сообщении (без blockedBy — TaskCreate не поддерживает)
2. **Раунд 2:** Все 11 TaskUpdate (addBlockedBy) параллельно — ID предсказуемы (последовательные числа от первого созданного)

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

При входе в сессию с существующим TaskList (вызов `/chain --resume`):

1. TaskList → найти первую pending задачу без blockers
2. Проверить реальное состояние: `chain_status.py status {NNNN}` (если цепочка уже создана)
3. Если задача in_progress, но скилл не завершился — проверить артефакты и скорректировать статус
4. Запустить скилл из описания задачи

---

## TaskList: шаблоны

### Путь A: Happy Path (12 задач)

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
    Скилл: /design-create — Unified Scan (5 источников), SVC-N секции (9 подсекций),
    INT-N контракты, STS-N системные тесты.
    Агент: design-agent (генерация SDD в изолированном контексте).
    Claude читает discussion.md + docs/ → проектирует → пользователь ревьюит → WAITING.
    При WAITING: Planned Changes в docs/, заглушки новых сервисов, per-tech стандарты.
    SSOT: standard-design.md
  activeForm: Создаю Design
  blockedBy: [1]

TASK 3: Создать Plan Tests
  description: >
    Скилл: /plan-test-create — TC-N acceptance-сценарии, тестовые данные, матрица покрытия.
    Claude читает design.md → генерирует тест-сценарии → пользователь ревьюит → WAITING.
    SSOT: standard-plan-test.md
  activeForm: Создаю Plan Tests
  blockedBy: [2]

TASK 4: Создать Plan Dev
  description: >
    Скилл: /plan-dev-create — TASK-N задачи, подзадачи, BLOCK-N, зависимости, маппинг Issues.
    Автоматически вызывает /review-create (review.md).
    Claude читает design.md + plan-test.md → генерирует план → пользователь ревьюит → WAITING.
    SSOT: standard-plan-dev.md
  activeForm: Создаю Plan Dev
  blockedBy: [3]

TASK 5: Запустить разработку
  description: >
    Скилл: /dev-create {NNNN} — создание GitHub Issues, Milestone, Branch.
    Все 4 документа → RUNNING. Claude создаёт Issues по TASK-N, привязывает к Milestone,
    создаёт feature-ветку.
    Пользователь проверяет на GitHub: Issues, Milestone, Branch.
    SSOT: create-development.md
  activeForm: Запускаю разработку
  blockedBy: [4]

TASK 6: Разработка
  description: >
    Скилл: /dev — оркестрация разработки.
    Агент: dev-agent (код, тесты по BLOCK-N в изолированном контексте).
    Агент: commit-agent (коммиты по Conventional Commits).
    Параллельные агенты по волнам. Per-service тесты внутри блока,
    системные тесты после волны.
    При CONFLICT → динамические задачи добавляются в TaskList (см. CONFLICT).
    SSOT: standard-development.md
  activeForm: Разработка
  blockedBy: [5]

TASK 7: Ревью ветки
  description: >
    Скилл: /review — локальное ревью ветки перед PR.
    Агент: code-reviewer (анализ diff по 7 критериям, сверка со specs/analysis/).
    Вердикт: READY → продолжить, NOT READY → исправить, CONFLICT → Путь B.
    SSOT: standard-review.md
  activeForm: Ревью ветки
  blockedBy: [6]

TASK 8: Создать PR
  description: >
    Агент: pr-create-agent (git push, gh pr create, сбор Issues через collect-pr-issues.py).
    Формирует body, привязывает labels.
    Пользователь проверяет PR на GitHub.
    SSOT: standard-pull-request.md, create-pull-request.md
  activeForm: Создаю PR
  blockedBy: [7]

TASK 9: Ревью PR
  description: >
    Скилл: /review {PR-N} — ревью PR на GitHub.
    Агент: code-reviewer (анализ diff по 7 критериям).
    Итерации: замечания → исправления → повторный /review.
    Вердикт READY → мержить. NOT READY → исправить. CONFLICT → Путь B.
    SSOT: standard-review.md
  activeForm: Ревью PR
  blockedBy: [8]

TASK 10: Merge
  description: >
    Агент: merge-agent (squash merge PR, закрытие Issues, синхронизация main).
    Claude мержит PR, синхронизирует локальный main.
    SSOT: create-merge.md, standard-sync.md
  activeForm: Merge
  blockedBy: [9]

TASK 11: Завершить цепочку
  description: >
    Агент: chain-done-agent (RUNNING → REVIEW → DONE, обновление docs/).
    Bottom-up каскад: plan-dev → plan-test → design → discussion.
    Обновление docs/: Planned Changes → AS IS, Changelog.
    Cross-chain проверка (check_cross_chain).
    SSOT: standard-analysis.md §§ 6.5-6.6, 7.3, create-chain-done.md
  activeForm: Завершаю цепочку
  blockedBy: [10]

TASK 12: Релиз (опционально)
  description: >
    Скилл: /release-create — GitHub Release: changelog, tag, milestone close.
    Пользователь решает: создавать релиз сейчас или накопить изменения.
    AskUserQuestion: "Создать релиз?" Если нет → задача удаляется (status: deleted).
    SSOT: standard-release.md, create-release.md
  activeForm: Создаю релиз
  blockedBy: [11]
```

**Динамическое поведение:**
- Task 12 (Релиз) — опциональная. Спросить через AskUserQuestion. Если нет — `TaskUpdate status: deleted`
- При CONFLICT на любом шаге — добавить задачи CONFLICT (ниже) в TaskList динамически
- `{NNNN}` подставляется из Task 1 (номер цепочки)

### CONFLICT (динамические задачи)

При обнаружении CONFLICT (во время Task 6, 7 или 9) добавить задачи разрешения в TaskList:

```
TASK N+1: Каскад CONFLICT
  description: >
    Скрипт: chain_status.py T4/T8 — вся цепочка → CONFLICT.
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

После TASK N+3 → возврат к задаче разработки (Task 6). blockedBy обновляется динамически.

### Путь C.1: Rollback

```
TASK R1: Откат цепочки
  description: >
    Агент: rollback-agent — T9 → откат артефактов → T10 → REJECTED.
    SSOT: standard-analysis.md §§ 6.7-6.8, create-rollback.md
  activeForm: Откат цепочки
```

### Путь C.2: Hotfix

Тот же TaskList что Happy Path (12 задач), но:
- Task 1 (Discussion): пометка "краткая Discussion, фокус на баге"
- Task 5 (dev-create): метки `bug` + `critical`, ветка `{NNNN}-hotfix-{topic}`
- Task 12 (Release): PATCH-версия (обязательна, не опциональна)

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
# Шаг 2: TaskCreate × 12 задач (шаблон Happy Path)
# Шаг 3: "План из 12 задач создан. Начинаем?" → Да
# Шаг 4: Task 1 → in_progress → /discussion-create
```

### Возобновление после прерывания

```
# Пользователь: "/chain --resume"

# TaskList → задачи 1-5 completed, задача 6 in_progress
# chain_status.py status {NNNN} → RUNNING
# Продолжить с Task 6 → dev-agent (modify-development.md)
```

### Hotfix

```
# Пользователь: "/chain --hotfix"

# Шаг 1: Путь C.2 (Hotfix)
# Шаг 2: TaskCreate × 12 задач (Happy Path + метки bug/critical)
# Task 12: Release — обязательна, PATCH-версия
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
