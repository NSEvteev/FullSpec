---
description: Стандарт процесса поставки ценности — полный цикл от идеи до релиза, три пути (happy path, CONFLICT, альтернативные маршруты), маппинг шагов на инструменты.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Стандарт процесса поставки ценности

Версия стандарта: 1.0

Полный цикл поставки изменения: Идея → Analysis Chain → Development → Merge → Release. Описывает три пути прохождения, маппинг каждого шага на инструменты проекта и пробелы покрытия.

**Полезные ссылки:**
- [Инструкции specs/](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | — (оркестратор, не имеет экземпляров) |
| Создание | — |
| Модификация | — |

**SSOT-зависимости:**

| Зона | Документ | Зона ответственности |
|------|----------|---------------------|
| Analysis chain | [standard-analysis.md](./analysis/standard-analysis.md) | 4 уровня, статусы, каскады, обновление docs/ |
| Documentation | [standard-docs.md](./docs/standard-docs.md) | Контур docs/, типы документов |
| GitHub workflow | [standard-github-workflow.md](/.github/.instructions/standard-github-workflow.md) | Issue → Branch → PR → Merge → Release |
| Development | [standard-development.md](/.github/.instructions/development/standard-development.md) | Процесс разработки в feature-ветке |

**Зоны ответственности:**

> Этот документ — HIGH-LEVEL оркестратор всего процесса. Каждый шаг описан 1-2 предложениями + ссылка на SSOT. Детали — в зависимых стандартах. Не дублирует содержание.

## Оглавление

- [1. Обзорная диаграмма](#1-обзорная-диаграмма)
- [2. Модель статусов](#2-модель-статусов)
- [3. Выбор пути](#3-выбор-пути)
- [4. Три пути (обзор)](#4-три-пути-обзор)
  - [Фаза 0: Инициализация проекта](#фаза-0-инициализация-проекта)
- [5. Путь A: Happy Path](#5-путь-a-happy-path)
  - [Фаза 1: Аналитическая цепочка](#фаза-1-аналитическая-цепочка)
  - [Фаза 2: Запуск реализации](#фаза-2-запуск-реализации)
  - [Фаза 3: Реализация](#фаза-3-реализация)
  - [Фаза 4: Доставка в main](#фаза-4-доставка-в-main)
  - [Фаза 5: Завершение цепочки](#фаза-5-завершение-цепочки)
  - [Фаза 6: Поставка](#фаза-6-поставка)
- [6. Путь B: CONFLICT](#6-путь-b-conflict)
- [7. Путь C: Альтернативные маршруты](#7-путь-c-альтернативные-маршруты)
- [8. Сводная таблица инструментов](#8-сводная-таблица-инструментов)
- [9. Quick Reference](#9-quick-reference)
- [10. Пробелы и планы](#10-пробелы-и-планы)

---

## 1. Обзорная диаграмма

```mermaid
graph TD
    IDEA["Идея / Потребность"]

    subgraph phase1["Фаза 1: Аналитическая цепочка<br/>(per-document: DRAFT - WAITING)"]
        DISC["1.1 Discussion<br/>WHY + WHAT"]
        DESIGN["1.2 Design<br/>HOW (Unified Scan)"]
        PTEST["1.3 Plan Tests<br/>HOW TO VERIFY"]
        PDEV["1.4 Plan Dev<br/>WHAT TASKS"]
    end

    subgraph phase2["Фаза 2: Запуск"]
        DEVSTART["2.1 /dev-create<br/>Issues + Milestone + Branch<br/>RUNNING"]
    end

    subgraph phase3["Фаза 3: Реализация<br/>(цикл per TASK-N)"]
        DEV["3.1 Development"]
        VALIDATE["3.2 Локальная валидация"]
        COMMIT["3.3 Commits"]
    end

    subgraph phase4["Фаза 4: Доставка в main"]
        BREVIEW["4.1 Branch Review"]
        PR["4.2 PR Create"]
        PRREVIEW["4.3 PR Review"]
        MERGE["4.4 Merge"]
        SYNC["4.5 Sync main"]
    end

    subgraph phase5["Фаза 5: Завершение"]
        REVIEW["5.1 RUNNING - REVIEW"]
        REVITER["5.2 Review iterations"]
        DONE["5.3 REVIEW - DONE<br/>docs/ update"]
    end

    subgraph phase6["Фаза 6: Поставка"]
        RELEASE["6.1 Release"]
    end

    CONFLICT["CONFLICT<br/>Путь B"]

    IDEA --> DISC --> DESIGN --> PTEST --> PDEV
    PDEV --> DEVSTART
    DEVSTART --> DEV --> VALIDATE --> COMMIT
    COMMIT -- "ещё TASK-N?" --> DEV
    COMMIT -- "все TASK-N done" --> BREVIEW
    BREVIEW --> PR --> PRREVIEW --> MERGE --> SYNC
    SYNC --> REVIEW --> REVITER --> DONE
    DONE --> RELEASE

    DEV -. "обратная связь" .-> CONFLICT
    PRREVIEW -. "P1 замечание" .-> CONFLICT
    REVITER -. "P1 замечание" .-> CONFLICT
    CONFLICT -. "разрешение - WAITING - RUNNING" .-> DEV
```

---

## 2. Модель статусов

> Краткая навигационная модель. Полное описание: [standard-analysis.md § 5](./analysis/standard-analysis.md#5-статусы).

```mermaid
graph LR
    DRAFT["DRAFT<br/>per-doc"]
    WAITING["WAITING<br/>per-doc"]
    RUNNING["RUNNING<br/>tree"]
    REVIEW["REVIEW<br/>tree"]
    DONE["DONE<br/>per-document, финальный"]
    CONFLICT["CONFLICT<br/>tree"]
    ROLLING_BACK["ROLLING_BACK<br/>tree"]
    REJECTED["REJECTED<br/>tree-level, финальный"]

    DRAFT -- "T1: user ok" --> WAITING
    WAITING -- "T3: все 4 WAITING" --> RUNNING
    RUNNING -- "T6: все TASK-N done" --> REVIEW
    REVIEW -- "T7: review READY" --> DONE

    RUNNING -- "T4: feedback" --> CONFLICT
    REVIEW -- "T8: review P1" --> CONFLICT
    CONFLICT -- "T5: resolved" --> WAITING

    RUNNING -.-> ROLLING_BACK
    REVIEW -.-> ROLLING_BACK
    CONFLICT -.-> ROLLING_BACK
    ROLLING_BACK -- "T10" --> REJECTED
```

| Статус | Скоуп | Когда |
|--------|-------|-------|
| DRAFT | per-document | Документ создаётся и итерируется (Фаза 1) |
| WAITING | per-document | Пользователь одобрил документ (между Фазой 1 и 2) |
| RUNNING | tree-level | Все 4 документа согласованы, идёт разработка (Фазы 3-4) |
| REVIEW | tree-level | Реализация завершена, ожидает ревью (Фаза 5) |
| DONE | per-document (финальный) | Всё готово, docs/ обновлён (конец Фазы 5) |
| CONFLICT | tree-level | Обратная связь код → спеки (Путь B) |
| ROLLING_BACK | tree-level | Откат артефактов (Путь C.1) |
| REJECTED | tree-level (финальный) | Отклонён (Путь C.1) |

**Автоматизация:** Все переходы — через `chain_status.py` → `ChainManager.transition()`. Ручное изменение `status:` в frontmatter **запрещено**.

---

## 3. Выбор пути

> **Принцип:** Даже "мелкий" фикс проходит полную аналитическую цепочку. Изменение, которое кажется тривиальным, может затрагивать API контракты, data model или cross-service интеграции. Analysis chain выявляет это **до** написания кода, а не после.

| Что меняется | Путь | Обоснование |
|---|---|---|
| Поведение системы (API, data model, логика, UI) | **A — полная цепочка** | Любое изменение поведения требует проектирования, тестов и ревью |
| Баг в production (критический, блокирует пользователей) | **A — полная цепочка** (ускоренная) | Discussion может быть краткой, но цепочка обязательна — даже hotfix может сломать другие контракты |
| Несколько мелких багов без затрагивания API | **A через C.3 (bug-fix bundle)** | Одна Discussion группирует фиксы, далее полная цепочка |
| Опечатки, форматирование, комментарии | **C.4 (doc-only)** | Единственное исключение — изменение **не меняет поведение** системы |

**Исключение из analysis chain (C.4):** Допускается ТОЛЬКО когда изменение не затрагивает API контракты, data model, схему интеграций и не меняет поведение системы. Примеры: опечатка в README, исправление форматирования, обновление комментария.

---

## 4. Три пути (обзор)

### Фаза 0: Инициализация проекта

> Выполняется **однократно** при создании проекта. Не зависит от пути — обязательный нулевой шаг.

| # | Шаг | Описание | SSOT |
|---|------|---------|------|
| 0.1 | Настройка GitHub | Labels, Issue Templates, PR Template, CODEOWNERS, Actions, Security | [standard-github-workflow.md § 2](/.github/.instructions/standard-github-workflow.md#2-фаза-0-подготовка-инфраструктуры) |
| 0.2 | Настройка docs/ | Стартовый набор: README, .system/, .technologies/, примеры | [standard-docs.md § 7](./docs/standard-docs.md#7-жизненный-цикл) |
| 0.3 | Настройка среды | `make setup` — pre-commit hooks, зависимости | [initialization.md](/.structure/initialization.md) |

**Скиллы:** `/labels-modify`, `/milestone-create`

### Три пути

| Путь | Описание | Частота |
|------|---------|---------|
| **A: Happy Path** | Линейный поток от идеи до релиза без конфликтов | Идеальный сценарий |
| **B: CONFLICT** | Обратная связь код → спецификации. Обнаружение → классификация → каскад → разрешение → повторный запуск | Частый — код регулярно выявляет несовместимость |
| **C: Альтернативные** | Rollback, Hotfix, Bug-fix bundle, Doc-only changes, Cross-chain координация | По ситуации |

---

## 5. Путь A: Happy Path

### Фаза 1: Аналитическая цепочка

> Каждое изменение проходит 4 уровня: Discussion → Design → Plan Tests → Plan Dev. Каждый уровень — цикл CLARIFY → GENERATE → VALIDATE → USER REVIEW → WAITING.

| # | Шаг | Вопрос | Скилл | SSOT |
|---|------|--------|-------|------|
| 1.1 | Discussion | Зачем это нужно? Какие требования? | `/discussion-create` | [standard-discussion.md](./analysis/discussion/standard-discussion.md) |
| 1.2 | Design | Какие сервисы затронуты? Как распределить ответственности? | `/design-create` | [standard-design.md](./analysis/design/standard-design.md) |
| 1.3 | Plan Tests | Как проверяем решение? | `/plan-test-create` | [standard-plan-test.md](./analysis/plan-test/standard-plan-test.md) |
| 1.4 | Plan Dev | Какие задачи? | `/plan-dev-create` | [standard-plan-dev.md](./analysis/plan-dev/standard-plan-dev.md) |

**Общий паттерн объекта (7 шагов):** PREPARE → CLARIFY → GENERATE → VALIDATE → AGENT REVIEW → USER REVIEW → REPORT. → [standard-analysis.md § 2.4](./analysis/standard-analysis.md#24-общий-паттерн-объекта)

**Агенты:** design-agent (обяз. при Design), discussion-reviewer (опц.), design-reviewer (опц.)

**`/review-create` — автоматически:** Вызывается внутри `/plan-dev-create` (Шаг 10) после одобрения пользователем. Отдельный вызов не требуется.

**При Design → WAITING:** Planned Changes добавляются в docs/, заглушки {svc}.md для новых сервисов, per-tech стандарты. → [standard-analysis.md § 7.1](./analysis/standard-analysis.md#71-обновление-при-планировании-to-waiting)

### Фаза 2: Запуск реализации

> Когда все 4 документа цепочки в WAITING — запуск реализации.

| # | Шаг | Описание | Скилл | SSOT |
|---|------|---------|-------|------|
| 2.1 | dev-create | Создание Issues, Milestone, Branch → вся цепочка → RUNNING | `/dev-create` | [create-development.md](/.github/.instructions/development/create-development.md) |

**Результат:** GitHub Issues привязаны к Milestone, feature-ветка создана, все документы RUNNING.

### Фаза 3: Реализация

> Цикл по TASK-N из plan-dev.md. Повторяется для каждой задачи.

| # | Шаг | Описание | Скилл | SSOT |
|---|------|---------|-------|------|
| 3.1 | Development | Код + unit-тесты по TASK-N | `/dev` | [standard-development.md](/.github/.instructions/development/standard-development.md) |
| 3.2 | Локальная валидация | `make test`, `make lint` | `/principles-validate` | [validation-development.md](/.github/.instructions/development/validation-development.md) |
| 3.3 | Commits | Conventional Commits, [25 pre-commit хуков](/.structure/pre-commit.md) | — | [standard-commit.md](/.github/.instructions/commits/standard-commit.md) |

**Обратная связь:** При обнаружении несовместимости → [Путь B: CONFLICT](#6-путь-b-conflict).

### Фаза 4: Доставка в main

| # | Шаг | Описание | Скилл | SSOT |
|---|------|---------|-------|------|
| 4.1 | Branch Review | Локальное ревью ветки перед PR | `/review` | [validation-review.md](/.github/.instructions/review/validation-review.md) |
| 4.2 | PR Create | `git push` + `gh pr create` с привязкой Issues | — | [standard-pull-request.md](/.github/.instructions/pull-requests/standard-pull-request.md) |
| 4.3 | PR Review | Code-reviewer агенты проверяют PR | `/review {N}` | [standard-review.md](/.github/.instructions/review/standard-review.md) |
| 4.4 | Merge | Squash merge, Issues закрываются | — | [standard-review.md § 3](/.github/.instructions/review/standard-review.md#3-merge-стратегии) |
| 4.5 | Sync main | Локальная синхронизация | — | [standard-sync.md](/.github/.instructions/sync/standard-sync.md) |

### Фаза 5: Завершение цепочки

| # | Шаг | Описание | Скилл | SSOT |
|---|------|---------|-------|------|
| 5.1 | RUNNING → REVIEW | Все TASK-N выполнены → вся цепочка → REVIEW | `/analysis-status` | [standard-analysis.md § 6.5](./analysis/standard-analysis.md#65-running-to-review) |
| 5.2 | Review iterations | code-reviewer → итерации в review.md → вердикт | `/review` | [standard-review.md (analysis)](./analysis/review/standard-review.md) |
| 5.3 | REVIEW → DONE | Bottom-up каскад + обновление docs/ (Planned Changes → AS IS) | `/analysis-status` | [standard-analysis.md § 6.6](./analysis/standard-analysis.md#66-review-to-done) |

**При Design → DONE:** docs/ обновляются — Planned Changes переносятся в AS IS, Changelog обновляется. → [standard-analysis.md § 7.3](./analysis/standard-analysis.md#73-обновление-при-реализации-to-done)

### Фаза 6: Поставка

| # | Шаг | Описание | Скилл | SSOT |
|---|------|---------|-------|------|
| 6.1 | Release | Milestone complete → changelog → tag → GitHub Release | `/milestone-validate` | [standard-release.md](/.github/.instructions/releases/standard-release.md), [create-release.md](/.github/.instructions/releases/create-release.md) |

---

## 6. Путь B: CONFLICT

> Обратная связь код → спецификации. Частый сценарий — код регулярно выявляет несовместимость с проектированием.

**SSOT:** [standard-analysis.md §§ 6.3–6.4](./analysis/standard-analysis.md#63-running-to-conflict)

### Источники

| Источник | Когда | Пример |
|----------|-------|--------|
| Код | При Development (шаг 3.1) | Алгоритм из Design невозможно реализовать |
| Тесты | При Development (шаг 3.2) | Тесты падают из-за неверных спецификаций |
| Branch Review | При Branch Review (шаг 4.1) | P1 замечание code-reviewer |
| PR Review | При PR Review (шаг 4.3) | P1 замечание code-reviewer |
| Review iterations | При Review (шаг 5.2) | Вердикт CONFLICT в review.md |

### Классификация уровня

| Граница (из Code Map docs/{svc}.md) | Уровень | Действие |
|--------------------------------------|---------|---------|
| **Свободно** (внутри пакета) | Спецификации не затронуты | Нет реакции |
| **Флаг** (между пакетами) | Plan Dev / Plan Tests | Рабочие правки — LLM автономно, статус не меняется |
| **CONFLICT** (API, data model, архитектура) | Design или выше | → Вся цепочка → CONFLICT |

**Автоматизация:** `chain_status.py` → `classify_feedback(level)` принимает `level`: `"free"` / `"flag"` / `"conflict"`, возвращает dict с ключами `allowed`, `action`, `reason`

### Процесс разрешения CONFLICT

```mermaid
graph TD
    DETECT["B.1 Обнаружение<br/>Код/тесты/ревью"]
    CLASSIFY["B.2 Классификация<br/>free / flag / CONFLICT"]
    CASCADE["B.3 Каскад<br/>Вся цепочка - CONFLICT"]
    FIND["B.4 Обнаружение уровня<br/>Снизу вверх до первого<br/>незатронутого"]
    RESOLVE["B.5 Разрешение<br/>Сверху вниз:<br/>исправление документов"]
    WAITING["B.6 Per-doc - WAITING<br/>Пользователь ревьюит<br/>каждый документ"]
    RUNNING["B.7 Повторный запуск<br/>Все WAITING - RUNNING"]

    DETECT --> CLASSIFY
    CLASSIFY -- "CONFLICT" --> CASCADE
    CASCADE --> FIND --> RESOLVE --> WAITING --> RUNNING
    RUNNING --> DETECT
```

| # | Шаг | Описание | Инструменты |
|---|------|---------|-------------|
| B.1 | Обнаружение | Код/тесты выявили несовместимость или P1 на ревью | chain_status.py (classify_feedback) |
| B.2 | Классификация | free → ничего, flag → рабочие правки, CONFLICT → стоп | [standard-analysis.md § 6.3](./analysis/standard-analysis.md#63-running-to-conflict) |
| B.3 | Каскад CONFLICT | Вся цепочка → CONFLICT (tree-level) | chain_status.py (T4/T8) |
| B.4 | Обнаружение уровня | Проверка снизу вверх: Plan Dev → … → Discussion | LLM (не автоматизировано) |
| B.5 | Разрешение сверху вниз | От самого высокого затронутого до Plan Dev | `/discussion-modify`, `/design-modify`, `/plan-test-modify`, `/plan-dev-modify` |
| B.6 | Per-doc → WAITING | Пользователь ревьюит каждый изменённый документ | chain_status.py (T5) |
| B.7 | Повторный запуск | Все 4 в WAITING → каскад RUNNING | chain_status.py (T3), `/issue-modify` (обновление Issues) |

**Кросс-цепочечная обратная связь:** При обновлении docs/ автоматически вызывается `check_cross_chain()` — может затронуть другие цепочки. → [standard-analysis.md § 7.2](./analysis/standard-analysis.md#72-конфликт-исполнения-conflict)

---

## 7. Путь C: Альтернативные маршруты

### C.1 Rollback / Reject

Отмена цепочки на любом этапе (кроме DONE).

| Шаг | Описание | SSOT |
|-----|---------|------|
| Любой → ROLLING_BACK | Пользователь отменяет или CONFLICT неразрешим | [standard-analysis.md § 6.7](./analysis/standard-analysis.md#67-to-rolling_back) |
| Откат артефактов | Issues закрыты, ветка удалена, Planned Changes убраны, per-tech откачены | chain_status.py (T9) |
| ROLLING_BACK → REJECTED | Финальный статус | chain_status.py (T10) |

**Инструменты:** `/discussion-modify`, `/design-modify`, `/plan-test-modify`, `/plan-dev-modify`, `/issue-modify`

### C.2 Hotfix

Критический баг в production, требующий немедленного исправления.

**SSOT:** [standard-release.md](/.github/.instructions/releases/standard-release.md) (упоминание)

> **GAP:** Нет отдельного workflow для hotfix. Сейчас: стандартная цепочка в сокращённом формате или прямой фикс через Issue → Branch → PR → Merge.

### C.3 Bug-fix bundle

Группировка мелких фиксов, не затрагивающих API/data model, в одну Discussion.

**SSOT:** [standard-analysis.md решение #33](./analysis/standard-analysis.md#12-решения)

**Правило:** Если хотя бы один фикс затрагивает API или data model — отдельная Discussion.

### C.4 Documentation-only changes

Опечатки, форматирование — без analysis chain.

**SSOT:** [standard-analysis.md § 10](./analysis/standard-analysis.md#10-запреты) (исключение)

**Критерий:** Изменение **не меняет поведение системы** — не затрагивает API контракты, data model, схему интеграций.

### C.5 Кросс-цепочечная координация

Параллельные цепочки: Planned Changes видны в docs/, `check_cross_chain()` при каждом обновлении.

**SSOT:** [standard-analysis.md §§ 7.2, 7.4](./analysis/standard-analysis.md#74-параллельные-цепочки)

| Статус другой цепочки | Реакция |
|----------------------|---------|
| DRAFT | Перегенерация затронутых документов |
| WAITING | Дообновление |
| RUNNING | → CONFLICT |
| DONE | Новая Discussion для приведения к общему знаменателю |

---

## 8. Сводная таблица инструментов

### 8.1 Основная таблица: инструкции, скиллы, агенты, скрипты

| Шаг | Инструкция | Скилл | Агент | Script |
|-----|-----------|-------|-------|--------|
| **Фаза 1: Аналитическая цепочка** | | | | |
| 1.1 Discussion | standard/create/modify/validation-discussion | /discussion-create, -modify, -validate | discussion-reviewer | validate-analysis-discussion.py, chain_status.py |
| 1.2 Design | standard/create/modify/validation-design | /design-create, -modify, -validate, /technology-create, /service-create | design-agent, design-reviewer, technology-agent | validate-analysis-design.py, chain_status.py |
| 1.3 Plan Tests | standard/create/modify/validation-plan-test | /plan-test-create, -modify, -validate | — | validate-analysis-plan-test.py, chain_status.py |
| 1.4 Plan Dev | standard/create/modify/validation-plan-dev, create-review | /plan-dev-create (включает /review-create), -modify, -validate | — | validate-analysis-plan-dev.py, create-review-file.py, chain_status.py |
| **Фаза 2: Запуск** | | | | |
| 2.1 dev-create | create-development, standard-issue, standard-milestone, standard-branching | /dev-create, /issue-create, /milestone-create, /branch-create | — | chain_status.py |
| **Фаза 3: Реализация** | | | | |
| 3.1 Development | standard-development, modify-development | /dev | — | — |
| 3.2 Validation | validation-development | /principles-validate | — | validate-principles.py |
| 3.3 Commits | standard-commit | — | — | — |
| **Фаза 4: Доставка** | | | | |
| 4.1 Branch Review | validation-review (github) | /review | code-reviewer | — |
| 4.2 PR Create | standard-pull-request, standard-pr-template | — | — | — |
| 4.3 PR Review | standard-review (github) | /review {N} | code-reviewer | — |
| 4.4 Merge | standard-review § 3 | — | — | — |
| 4.5 Sync | standard-sync | — | — | — |
| **Фаза 5: Завершение** | | | | |
| 5.1 → REVIEW | standard-analysis § 6.5 | /analysis-status | — | chain_status.py |
| 5.2 Review iter. | standard-review (analysis), create-review | /review | code-reviewer | extract-svc-context.py |
| 5.3 → DONE | standard-analysis § 6.6, § 7.3 | /analysis-status, /service-modify | — | chain_status.py |
| **Фаза 6: Поставка** | | | | |
| 6.1 Release | standard-release, create-release | /milestone-validate | — | — |
| **Путь B: CONFLICT** | | | | |
| B.1-B.3 Обнаружение → Каскад | standard-analysis §§ 6.3 | /analysis-status | — | chain_status.py (classify_feedback, T4/T8) |
| B.5-B.7 Разрешение → RUNNING | modify-discussion/design/plan-test/plan-dev | -modify скиллы | — | chain_status.py (T5, T3) |

### 8.2 Pre-commit хуки по шагам

> Полный список: [pre-commit.md](/.structure/pre-commit.md)

| Шаг | Pre-commit хуки |
|-----|----------------|
| 1.1 Discussion | discussion-validate |
| 1.2 Design | design-validate |
| 1.3 Plan Tests | plan-test-validate |
| 1.4 Plan Dev | plan-dev-validate, review-validate |
| 2.1 dev-create | branch-validate, type-templates-validate |
| 3.2 Validation | [25 pre-commit хуков](/.structure/pre-commit.md) (все) |
| 3.3 Commits | [25 pre-commit хуков](/.structure/pre-commit.md) (все) |
| 4.1 Branch Review | review-validate |
| 4.2 PR Create | pr-template-validate |
| 5.2 Review iter. | review-validate |
| 5.3 → DONE | service-validate, docs-validate |

### 8.3 Rules по шагам

> Расположение: [/.claude/rules/](/.claude/rules/)

| Rule | Активируется на шагах |
|------|-----------------------|
| core | Все шаги (глобальный) |
| code | 3.1 Development, 3.2 Validation |
| development | 2.1 dev-create, 3.1-3.3, 4.1-4.5, 6.1 Release |
| analysis-status-transition | 1.1-1.4, 2.1, 5.1, 5.3, B.1-B.7 |
| service-architecture | 1.2 Design, 5.3 → DONE |

---

## 9. Quick Reference

Компактный список команд для каждой фазы.

```
Фаза 1 — Аналитическая цепочка:
  /discussion-create    → discussion.md (DRAFT → WAITING)
  /design-create        → design.md (DRAFT → WAITING)
  /plan-test-create     → plan-test.md (DRAFT → WAITING)
  /plan-dev-create      → plan-dev.md (DRAFT → WAITING) + review.md (авто)

Фаза 2 — Запуск реализации:
  /dev-create {NNNN}    → Issues + Milestone + Branch → RUNNING

Фаза 3 — Реализация (per TASK-N):
  /dev                  → код + тесты
  make test && make lint
  git commit            → pre-commit hooks автоматически

Фаза 4 — Доставка в main:
  /review               → локальное ревью ветки
  git push -u origin {branch}
  gh pr create --title "..." --body "Closes #N, #N"
  /review {PR-N}        → ревью PR
  gh pr merge {PR-N} --squash
  git checkout main && git pull

Фаза 5 — Завершение цепочки:
  /analysis-status      → RUNNING → REVIEW (когда все TASK-N done)
  /review               → итерации review.md → вердикт READY
  /analysis-status      → REVIEW → DONE (bottom-up каскад + docs/ update)

Фаза 6 — Поставка:
  gh release create vX.Y.Z --generate-notes

CONFLICT:
  /analysis-status      → RUNNING → CONFLICT
  /{level}-modify       → разрешение сверху вниз
  /analysis-status      → CONFLICT → WAITING (per-doc)
  /dev-create {NNNN}    → WAITING → RUNNING (повторный запуск)
```

---

## 10. Пробелы и планы

| # | Пробел | Приоритет | Описание | План |
|---|--------|-----------|---------|------|
| G1 | Нет единого `/project-init` | Средний | Фаза 0 разрозненна — 3 процесса без оркестратора | Создать скилл, объединяющий GitHub setup + docs/ init + make setup |
| G2 | Нет `/pr-create` скилла | Средний | PR создаётся `gh pr create`, но сбор Issues chain'а, формирование body и labels — рутина. Скрипт `collect-pr-issues.py` + скилл автоматизируют | Драфт: `.claude/drafts/2026-02-24-pr-create.md` |
| G3 | Нет `/release-create` скилла | Средний | Инструкция create-release.md есть, скилла нет | Создать скилл по create-release.md |
| G4 | Нет hotfix workflow | Средний | Упоминается в release, нет отдельного маршрута | Определить: сокращённая цепочка или Issue → Branch → PR → Merge |
| G5 | Нет `/commit` скилла | Низкий | Процесс покрыт standard-commit + pre-commit hooks | Скилл удобен но не критичен |
| G6 | Нет `/merge` скилла | Низкий | Одна команда gh pr merge --squash | Покрыт стандартом |
| G7 | Нет `/sync` скилла | Низкий | Две команды git | Покрыт стандартом |
| G8 | Нет post-release workflow | Низкий | Мониторинг зависит от инфраструктуры | Отложить до первого реального деплоя |
| G9 | Нет `/rollback` скилла | Низкий | chain_status.py покрывает статусы, откат — по modify-* | Скилл для удобства |
| G10 | Определение уровня CONFLICT не автоматизировано | Низкий | Полностью на LLM, формализовано в стандарте | Оставить как есть — LLM справляется |
| G11 | Нет `/chain-done` скилла | Средний | Переход REVIEW → DONE: последовательно снизу вверх (plan-dev → plan-test → design → discussion) вызывает -modify с обновлением docs/ | Создать скилл-оркестратор bottom-up DONE перехода |

**Покрытие:** 19 из 21 шага happy path имеют хотя бы один инструмент (~90%). Все 7 шагов CONFLICT покрыты инструкциями. 3 из 5 альтернативных маршрутов полностью покрыты.

---

## Скиллы

— (оркестратор не имеет собственных скиллов; скиллы определены в зависимых стандартах)
