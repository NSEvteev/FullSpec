---
description: Стандарт документа ревью кода — артефакт Plan Dev, создаётся при WAITING, итерации заполняются при REVIEW.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Стандарт review

Версия стандарта: 1.2

Стандарт документа `review.md` — формализованного результата ревью кода. Артефакт Plan Dev, не уровень analysis chain.

**Полезные ссылки:**
- [Инструкции](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-review.md](./validation-review.md) |
| Создание | [create-review.md](./create-review.md) |
| Модификация | *Не требуется (добавление итераций через `/review`)* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Расположение и именование](#2-расположение-и-именование)
- [3. Frontmatter](#3-frontmatter)
- [4. Переходы статусов](#4-переходы-статусов)
- [5. Разделы документа](#5-разделы-документа)
- [6. Clarify](#6-clarify)
- [7. Шаблон](#7-шаблон)
- [8. Чек-лист качества](#8-чек-лист-качества)
- [9. Примеры](#9-примеры)
- [Скиллы](#скиллы)

---

## 1. Назначение

`review.md` — формализованный результат ревью кода. Фиксирует замечания (RV-N), приоритеты (P1/P2/P3), вердикт и историю итераций.

**Зона ответственности:**
- Что проверяется при ревью (контур постановки, кода, стандартов)
- Как документируются замечания (RV-N, приоритеты, статусы)
- Как определяется вердикт (READY / NOT READY / CONFLICT)
- Жизненный цикл (OPEN → RESOLVED)

**Не является 5-м уровнем analysis chain.** `review.md` — артефакт ревью кода. Шаблон (Контекст ревью) создаётся при Plan Dev → WAITING. Итерации заполняются при статусе REVIEW (`/review`). REVIEW — tree-level статус цепочки:
- Не имеет `children` (нет дочерних документов)
- Не участвует в каскадах DONE/CONFLICT как субъект
- P1 в review.md → инициирует CONFLICT Plan Dev (каскад согласно § 6.3 standard-analysis.md)
- RESOLVED блокирует переход REVIEW → DONE

**Lifecycle:**

```
Plan Dev → WAITING
  → /review-create → основной LLM создаёт review.md с "Контекст ревью":
      читает цепочку, запускает extract-svc-context.py, извлекает сервисы и технологии
  → разработчик видит, что будет проверяться, до старта

Plan Dev → RUNNING (разработка идёт)

Разработка завершена, все TASK-N Issues помечены как готовые к ревью
  → вся цепочка → REVIEW (§ 6.5 standard-analysis.md)
  → /review → основной LLM читает "Контекст ревью" → запускает N+1 агентов параллельно:
      - по одному code-reviewer на каждый сервис из "Контекст ревью"
      - отдельный code-reviewer для интеграции (INT-N, shared/)
      каждый агент возвращает результат в чат (не пишет в файл)
  → основной LLM собирает все выводы → формирует "## Итерация N" → записывает в review.md

  Ветка 1 — нет замечаний:
    → вердикт READY → /review устанавливает status: RESOLVED → каскад DONE (§ 6.6 standard-analysis.md)

  Ветка 2 — есть P1:
    → вердикт CONFLICT → /review устанавливает Plan Dev статус CONFLICT
    → каскад CONFLICT по цепочке (§ 6.3 standard-analysis.md)
    → specs/код правятся → /review → "## Итерация N+1"

  Ветка 3 — есть P2/P3, нет P1:
    → вердикт NOT READY → review.md остаётся OPEN, цепочка остаётся в REVIEW
    → основной LLM задаёт AskUserQuestion по каждому open P2/P3
    → код правится или wontfix
    → /review → "## Итерация N+1"

  Итерация N+1:
    → все P1/P2 resolved или wontfix → вердикт READY → status: RESOLVED
```

**Классификация замечаний:**

| Приоритет | Название | Суть | Действие |
|-----------|----------|------|----------|
| **P1** | Расхождение | Реализация противоречит постановке (REQ-N, SVC-N, INT-N) | → Plan Dev → CONFLICT → каскад по цепочке (§ 6.3 standard-analysis.md) |
| **P2** | Дефект | Неполная реализация, баг, пропущен edge case | → AskUserQuestion: исправлять или принять как есть |
| **P3** | Нарушение | Несоответствие стандартам, стилистика | → AskUserQuestion: исправлять или принять как есть |

**P1 — единственный приоритет, автоматически инициирующий CONFLICT Plan Dev.** P1 не может быть wontfix. Единственный способ снять P1 — исправить код или обновить постановку (через CONFLICT цепочки). Переклассификация P1 → P2/P3 — только через CONFLICT.

---

## 2. Расположение и именование

```
specs/analysis/NNNN-{topic}/
├── discussion.md
├── design.md
├── plan-test.md
├── plan-dev.md
└── review.md          ← фиксированное имя
```

**Имя файла:** всегда `review.md` — нет суффиксов и вариантов.

**Ветка = папка:** `git branch --show-current` возвращает `NNNN-{topic}`, что равно имени папки `specs/analysis/NNNN-{topic}/` (→ [standard-branching.md § 2](/.github/.instructions/branches/standard-branching.md)).

**Один review.md на ветку.** Analysis chain — один набор документов на ветку, не на сервис. Мультисервисные изменения фиксируются в одном файле через подразделы `### {svc}` внутри итераций.

---

## 3. Frontmatter

```yaml
---
description: Ревью кода для {NNNN}-{topic}.
standard: specs/.instructions/analysis/review/standard-review.md
standard-version: v1.2
parent: specs/analysis/{NNNN}-{topic}/plan-dev.md
index: specs/analysis/README.md
milestone: v{X.Y}
status: OPEN
---
```

| Поле | Значение | Примечание |
|------|----------|------------|
| `description` | `Ревью кода для {NNNN}-{topic}.` | |
| `standard` | `specs/.instructions/analysis/review/standard-review.md` | Этот документ |
| `standard-version` | `v1.2` | Версия стандарта |
| `parent` | `specs/analysis/{NNNN}-{topic}/plan-dev.md` | review.md — дочерний артефакт Plan Dev |
| `index` | `specs/analysis/README.md` | |
| `milestone` | `v{X.Y}` | Наследуется от Discussion |
| `status` | `OPEN` / `RESOLVED` | Только эти два значения |

**Отличия от 4 уровней chain:**

| Поле | 4 уровня chain | review.md |
|------|----------------|-----------|
| `parent` | Путь к родительскому документу | `plan-dev.md` |
| `children` | Путь к дочернему | **Нет** |
| `status` | DRAFT/WAITING/RUNNING/REVIEW/DONE/CONFLICT/ROLLING_BACK/REJECTED | **OPEN/RESOLVED** |
| `iteration` | Нет | **Нет** (итерации — секции `## Итерация N`) |

---

## 4. Переходы статусов

Только два статуса: `OPEN` → `RESOLVED`.

| Событие | Действие с `status` |
|---------|---------------------|
| `/review-create` создаёт файл | Устанавливает `status: OPEN` |
| Итерация с наибольшим N содержит вердикт `READY` | `/review` устанавливает `status: RESOLVED` |

**`OPEN` остаётся при:** вердикте `NOT READY` или `CONFLICT` — `/review` не меняет статус.

**`RESOLVED` блокирует Plan Dev → DONE.** Merge без `RESOLVED` невозможен (pre-commit hook `review-validate`, вызывает `validate-analysis-review.py`).

**review.md не участвует** в каскадах DONE, CONFLICT, ROLLING_BACK как субъект. При откате цепочки (ROLLING_BACK) review.md остаётся в текущем статусе. При повторном прохождении цепочки к RUNNING — запускается новая итерация `/review`.

**Связь с chain_status.py:** [`chain_status.py`](../../.scripts/chain_status.py) читает review.md через `mgr.status()` → `{"review": "OPEN"}`, проверяет prerequisites T7 (`review.md status==RESOLVED`), но **не управляет** переходами OPEN/RESOLVED — это делает `/review`.

---

## 5. Разделы документа

Документ состоит из двух типов разделов:

### 5.1 Контекст ревью (заполняется при /review-create)

Фиксируется **до начала разработки** (при Plan Dev → WAITING). Содержит все ссылки, необходимые агентам при запуске `/review`.

| Подраздел | Содержание | Кто заполняет |
|-----------|------------|---------------|
| `### Постановка` | Таблица со ссылками на 4 документа цепочки | `/review-create` |
| `### {svc} (critical-{level})` | Таблица §§ (только присутствующие в SVC-N design.md). Колонка "Что проверяем" заполняется `/review-create` на основе SVC-N из design.md — конкретные изменения (ADDED/MODIFIED/REMOVED из § 9 Planned Changes) | `/review-create` через `extract-svc-context.py` |
| `### Системная документация` | `specs/docs/.system/overview.md`, `conventions.md`, `testing.md`, `infrastructure.md` | `/review-create` |
| `### Процесс разработки` | `validation-development.md` — чек-лист процесса разработки (тесты, линт, сборка, зависимости, полнота) | `/review-create` |
| `### Tech-стандарты` | Таблица `{технология} → standard-{tech}.md` | `/review-create` |

**`critical-{level}` в заголовке блока** — criticality level сервиса из `specs/docs/{svc}.md § 1`. Определяет пороги покрытия тестами (см. ниже). Агент code-reviewer использует его для определения минимального coverage.

| Criticality | Unit-test coverage | Integration tests | E2E tests |
|-------------|-------------------|-------------------|-----------|
| critical-high | >= 80% | Обязательны | Обязательны |
| critical-medium | >= 60% | Обязательны | Обязательны |
| critical-low | >= 40% | Рекомендуются | Опционально |

**Scope документов** определяется при `/review-create` через `extract-svc-context.py` (парсит SVC-N из design.md) + всегда `specs/docs/.system/*`.

### 5.2 Итерация N (заполняется при /review)

Итерации заполняются при статусе цепочки REVIEW — `/review` запускается только когда цепочка в REVIEW.

Добавляется при каждом запуске `/review`. История сохраняется — итерации не перезаписываются.

**Нумерация итераций:** последовательная (1, 2, 3...). Следующая итерация = `max(N) + 1`.

**Нумерация RV-N:** сброс в каждой итерации. Каждый сервис начинает с RV-1 в каждой новой итерации. Ссылка на конкретное замечание: "Итерация N / {svc} / RV-M".

**Кто создаёт итерацию:** основной LLM (skill `/review`) — запускает N+1 code-reviewer агентов параллельно, собирает выводы, формирует `## Итерация N` и записывает в review.md. Агенты НЕ пишут в файл напрямую.

**Сервисные блоки `### {svc}`** создаются для каждого сервиса, зафиксированного в разделе `### {svc} (critical-{level})` Контекста ревью.

**Обработка ошибки агента:** если code-reviewer агент вернул ошибку или пустой результат — LLM фиксирует в блоке `### {svc}`: "Ревью не выполнено (ошибка агента)". Итерация остаётся OPEN.

**Невыполненные TASK-N при запуске `/review`:** фиксируются как P2 (дефект: неполная реализация). Если TASK-N является prerequisite для других задач из того же Plan Dev — P1 (расхождение с постановкой: prerequisite-задача обязана быть выполнена первой).

Структура итерации:
- `### {svc}` — per-service блок
  - `#### Сверка с постановкой` — счётчики TASK-N, TC-N; расхождения; вне scope
  - `#### Замечания` — блоки `##### RV-N`
- `### Интеграция (INT-N)` — от system-агента (INT-N контракты, shared/, глобальные нарушения)
- `### Итого` — сводная таблица по сервисам (P1/P2/P3, Open/Resolved/Wontfix)
- `**Вердикт:**` — READY / NOT READY / CONFLICT

**Критерий READY:** нет open P1, нет open P2, все P3 — resolved или wontfix. Open P3 блокирует READY.

**`status` в frontmatter обновляет `/review` skill автоматически:**
- Вердикт READY → `status: RESOLVED`
- Вердикт NOT READY / CONFLICT → `status` остаётся `OPEN`

---

## 6. Clarify

Не применимо. `review.md` создаётся автоматически по шаблону через `/review-create` — интерактивное уточнение требований не нужно.

---

## 7. Шаблон

````markdown
---
description: Ревью кода для {NNNN}-{topic}.
standard: specs/.instructions/analysis/review/standard-review.md
standard-version: v1.2
parent: specs/analysis/{NNNN}-{topic}/plan-dev.md
index: specs/analysis/README.md
milestone: v{X.Y}
status: OPEN
---

# review: {NNNN} {Тема}

**Ветка:** {branch-name}
**Base:** {base-branch}

## Контекст ревью

> Секция заполняется при /review-create (до начала разработки).
> Содержит все ссылки, необходимые code-reviewer при запуске /review.

### Постановка

| Документ | Путь |
|----------|------|
| Discussion | `specs/analysis/{branch}/discussion.md` |
| Design | `specs/analysis/{branch}/design.md` |
| Plan Tests | `specs/analysis/{branch}/plan-test.md` |
| Plan Dev | `specs/analysis/{branch}/plan-dev.md` |

### {svc1} (critical-{level})

Блок на каждый затронутый сервис. Секции — только те, которые реально меняются (есть в SVC-N design.md).

| Секция | Путь | Что проверяем |
|--------|------|----------------|
| § 2 API контракты | `specs/docs/{svc1}.md#api-контракты` | Planned Changes: {кратко что ADDED/MODIFIED/REMOVED} |
| § 3 Data Model | `specs/docs/{svc1}.md#data-model` | Planned Changes: {кратко} |
| § 8 Автономия | `specs/docs/{svc1}.md#границы-автономии-llm` | Что можно без флага, что требует CONFLICT |
| § 9 Planned Changes | `specs/docs/{svc1}.md#planned-changes` | **Эталон для P1-сверки** |

*Незатронутые секции не включаются.*

### {svc2} (critical-{level})

...

### Системная документация

- `specs/docs/.system/overview.md`
- `specs/docs/.system/conventions.md`
- `specs/docs/.system/testing.md`
- `specs/docs/.system/infrastructure.md` *(при изменениях в platform/)*

### Процесс разработки

- [validation-development.md](/.github/.instructions/development/validation-development.md)

### Tech-стандарты

| Технология | Стандарт |
|------------|----------|
| {tech} | `specs/docs/.technologies/standard-{tech}.md` |

---

## Итерация 1

**Дата:** {YYYY-MM-DD}
**Коммит / PR:** {git SHA или #N}

### {svc1}

#### Сверка с постановкой

- TASK-N для сервиса: {X}/{Y} выполнено
- TC-N для сервиса: {X}/{Y} реализовано
- Расхождения: {есть (RV-1, RV-2) / нет}
- Вне scope: {есть (RV-N) / нет}

#### Замечания

##### RV-1: {краткое описание}

- **Файл:** `{path}:{line}`
- **Приоритет:** {P1 расхождение / P2 дефект / P3 нарушение}
- **Ссылка:** {REQ-N / TASK-N / TC-N / SVC-N § {1-9} / INT-N / standard-{tech}.md / —}
- **Контекст:** {почему это проблема — что говорит код vs что говорит постановка/стандарт}
- **Рекомендация:** {что исправить}
- **Статус:** {open / resolved / wontfix}

### {svc2}

...

### Интеграция (INT-N)

> Проверяет system-агент: контракты между сервисами, shared/, глобальные нарушения conventions.

#### Замечания

##### RV-1: ...

### Итого

| Сервис | P1 | P2 | P3 | Open | Resolved | Wontfix |
|--------|----|----|-----|------|----------|---------|
| {svc1} | {N} | {N} | {N} | {N} | {N} | {N} |
| {svc2} | {N} | {N} | {N} | {N} | {N} | {N} |
| Интеграция | {N} | {N} | {N} | {N} | {N} | {N} |
| **Итого** | **{N}** | **{N}** | **{N}** | **{N}** | **{N}** | **{N}** |

**Вердикт:** {READY / NOT READY / CONFLICT}

- **CONFLICT** — есть хотя бы 1 open P1 → Plan Dev переходит в CONFLICT → каскад по цепочке (§ 6.3 standard-analysis.md)
- **NOT READY** — нет P1, но есть open P2 или open P3 → основной LLM задаёт AskUserQuestion по каждому
- **READY** — нет open P1/P2, все P3 resolved или wontfix
````

---

## 8. Чек-лист качества

Проверки выполняются pre-commit хуком `review-validate`, который вызывает скрипт `validate-analysis-review.py` (`specs/.instructions/.scripts/validate-analysis-review.py`):

| # | Проверка | Правило |
|---|----------|---------|
| 1 | Наличие `review.md` | При наличии `specs/analysis/{branch}/` — файл должен существовать |
| 2 | `status: RESOLVED` | Push блокируется, если статус не `RESOLVED` |
| 3 | Наличие `## Итерация N` | Хотя бы одна секция итерации в документе |
| 4 | Вердикт `READY` | Итерация с **наибольшим N** содержит `**Вердикт:** READY` |

Hook **не проверяет** конкретные RV-N (их может не быть при чистом коде). Проверяется факт завершённого ревью.

---

## 9. Примеры

### Пример: review.md с одной итерацией, нет замечаний

```yaml
---
description: Ревью кода для 0001-oauth2-authorization.
standard: specs/.instructions/analysis/review/standard-review.md
standard-version: v1.2
parent: specs/analysis/0001-oauth2-authorization/plan-dev.md
index: specs/analysis/README.md
milestone: v1.0
status: RESOLVED
---
```

```markdown
# review: 0001 OAuth2 Authorization

**Ветка:** 0001-oauth2-authorization
**Base:** main

## Контекст ревью

### Постановка

| Документ | Путь |
|----------|------|
| Discussion | `specs/analysis/0001-oauth2-authorization/discussion.md` |
| Design | `specs/analysis/0001-oauth2-authorization/design.md` |
| Plan Tests | `specs/analysis/0001-oauth2-authorization/plan-test.md` |
| Plan Dev | `specs/analysis/0001-oauth2-authorization/plan-dev.md` |

### auth (critical-high)

| Секция | Путь | Что проверяем |
|--------|------|----------------|
| § 2 API контракты | `specs/docs/auth.md#api-контракты` | ADDED: POST /auth/token, POST /auth/refresh |
| § 3 Data Model | `specs/docs/auth.md#data-model` | ADDED: таблица refresh_tokens |
| § 8 Автономия | `specs/docs/auth.md#границы-автономии-llm` | — |
| § 9 Planned Changes | `specs/docs/auth.md#planned-changes` | Эталон для P1-сверки |

### Системная документация

- `specs/docs/.system/overview.md`
- `specs/docs/.system/conventions.md`
- `specs/docs/.system/testing.md`

### Процесс разработки

- [validation-development.md](/.github/.instructions/development/validation-development.md)

### Tech-стандарты

| Технология | Стандарт |
|------------|----------|
| Python | `specs/docs/.technologies/standard-python.md` |

---

## Итерация 1

**Дата:** 2026-02-22
**Коммит / PR:** a1b2c3d

### auth

#### Сверка с постановкой

- TASK-N для сервиса: 4/4 выполнено
- TC-N для сервиса: 6/6 реализовано
- Расхождения: нет
- Вне scope: нет

#### Замечания

*Замечаний нет.*

### Интеграция (INT-N)

#### Замечания

*Замечаний нет.*

### Итого

| Сервис | P1 | P2 | P3 | Open | Resolved | Wontfix |
|--------|----|----|-----|------|----------|---------|
| auth | 0 | 0 | 0 | 0 | 0 | 0 |
| Интеграция | 0 | 0 | 0 | 0 | 0 | 0 |
| **Итого** | **0** | **0** | **0** | **0** | **0** | **0** |

**Вердикт:** READY
```

### Пример: итерация с P1 (CONFLICT)

```markdown
## Итерация 1

**Дата:** 2026-02-22
**Коммит / PR:** d4e5f6g

### auth

#### Сверка с постановкой

- TASK-N для сервиса: 3/4 выполнено
- TC-N для сервиса: 5/6 реализовано
- Расхождения: есть (RV-1)
- Вне scope: нет

#### Замечания

##### RV-1: POST /auth/token возвращает access_token без expires_in

- **Файл:** `src/auth/backend/api/routes/auth.py:47`
- **Приоритет:** P1 расхождение
- **Ссылка:** SVC-1 § 2, INT-1
- **Контекст:** Design SVC-1 § 2 определяет поле `expires_in` в ответе. В коде поле отсутствует, что нарушает контракт INT-1 с сервисом gateway.
- **Рекомендация:** Добавить `expires_in` в схему ответа `TokenResponse`.
- **Статус:** open

### Интеграция (INT-N)

#### Замечания

*Замечаний нет (P1 уже зафиксирован в auth).*

### Итого

| Сервис | P1 | P2 | P3 | Open | Resolved | Wontfix |
|--------|----|----|-----|------|----------|---------|
| auth | 1 | 0 | 0 | 1 | 0 | 0 |
| Интеграция | 0 | 0 | 0 | 0 | 0 | 0 |
| **Итого** | **1** | **0** | **0** | **1** | **0** | **0** |

**Вердикт:** CONFLICT
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/review-create](/.claude/skills/review-create/SKILL.md) | Создание review.md с "Контекст ревью" — при Plan Dev → WAITING |
| [/review](/.claude/skills/review/SKILL.md) | Запуск N+1 code-reviewer агентов → добавление "## Итерация N" |
