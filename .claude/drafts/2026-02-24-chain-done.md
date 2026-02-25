# Воркфлоу завершения цепочки — инструкция + скилл

Последовательный bottom-up переход цепочки из REVIEW в DONE с обновлением docs/ на каждом уровне.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G11 из standard-process.md — переход в DONE должен быть отдельным скиллом
**Почему создан:** Определить формат инструкции и скилла `/chain-done` перед реализацией
**Связанные файлы:**
- `specs/.instructions/standard-process.md` — §5 Фаза 5 (Завершение цепочки)
- `specs/.instructions/analysis/standard-analysis.md` — §6.6 REVIEW to DONE, §7.3 Обновление при реализации
- `specs/.instructions/.scripts/chain_status.py` — ChainManager.transition(to="DONE")
- `specs/.instructions/analysis/review/standard-review.md` — вердикт READY

## Содержание

### Проблема

Переход REVIEW → DONE — сложный многошаговый процесс:

1. **Bottom-up каскад:** Plan Dev → Plan Tests → Design → Discussion — каждый документ переводится в DONE последовательно снизу вверх
2. **Обновление docs/:** При Design → DONE: Planned Changes переносятся в AS IS (§7.3)
3. **Сервисные документы:** {svc}.md обновляются — Planned Changes → основной контент, Changelog
4. **Per-tech стандарты:** standard-{tech}.md обновляются если были изменены
5. **review.md:** Должен быть RESOLVED с вердиктом READY

Сейчас это делается вручную: пользователь последовательно вызывает скиллы на модификацию каждого документа.

### Артефакты

По архитектуре проекта: **инструкция (SSOT) → скилл (обёртка)**. Скилл без SSOT-инструкции запрещён.

| # | Артефакт | Путь | Назначение |
|---|---------|------|------------|
| 1 | **Воркфлоу-инструкция** (SSOT) | `specs/.instructions/analysis/create-chain-done.md` | Пошаговый процесс bottom-up DONE перехода — шаги, чек-лист, примеры |
| 2 | **Скилл** (обёртка) | `/.claude/skills/chain-done/SKILL.md` | Ссылка на SSOT, формат вызова `/chain-done` |

Инструкция регистрируется в `specs/.instructions/analysis/README.md` или `specs/.instructions/README.md`.

> **Расположение:** `specs/.instructions/analysis/` — потому что DONE-переход относится к analysis chain, а не к GitHub или structure.

### Порядок создания

1. `/instruction-create create-chain-done --path specs/.instructions/analysis/` — инструкция
2. `/skill-create chain-done` — скилл, SSOT → create-chain-done.md

### Предлагаемая связка

**Инструкция:** `create-chain-done.md` (SSOT — шаги, чек-лист, примеры)
**Скилл:** `/chain-done` (обёртка — ссылка на SSOT, формат вызова)
**Тип:** Оркестратор bottom-up перехода

### Формат вызова

```
/chain-done {NNNN}
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `NNNN` | Номер analysis chain | Да |

### Шаги инструкции (create-chain-done.md)

```
/chain-done 0001
```

| Шаг | Действие | Детали | Инструмент |
|-----|---------|--------|------------|
| 1 | Проверить prerequisites | Цепочка в REVIEW, review.md RESOLVED с READY | chain_status.py (check_prerequisites) |
| 2 | Подтверждение пользователя | AskUserQuestion: "Цепочка NNNN готова к завершению?" | AskUserQuestion |
| 3 | Plan Dev → DONE | Вызвать `/plan-dev-modify` с переходом в DONE | `/plan-dev-modify`, chain_status.py (T7) |
| 4 | Plan Tests → DONE | Вызвать `/plan-test-modify` с переходом в DONE | `/plan-test-modify`, chain_status.py (T7) |
| 5 | Design → DONE | Вызвать `/design-modify` с переходом в DONE. **Триггер обновления docs/:** Planned Changes → AS IS | `/design-modify`, chain_status.py (T7) |
| 6 | Обновить docs/ | Для каждого SVC-N: {svc}.md Planned Changes → AS IS, Changelog | `/service-modify` per SVC-N |
| 7 | Обновить per-tech | Если standard-{tech}.md были изменены — финализировать | `/technology-modify` (если нужно) |
| 8 | Discussion → DONE | Вызвать `/discussion-modify` с переходом в DONE | `/discussion-modify`, chain_status.py (T7) |
| 9 | Проверить cross-chain | check_cross_chain() — не затронуты ли другие цепочки | chain_status.py |
| 10 | Обновить README | Dashboard в specs/analysis/README.md | chain_status.py (авто) |
| 11 | Отчёт | Что обновлено, какие docs/ затронуты | Вывод |

### Порядок bottom-up

```
Plan Dev (REVIEW → DONE)
    ↓
Plan Tests (REVIEW → DONE)
    ↓
Design (REVIEW → DONE)
    ↓ → docs/ update (Planned Changes → AS IS)
    ↓ → per-tech update
    ↓
Discussion (REVIEW → DONE)
    ↓
cross-chain check
    ↓
Отчёт
```

### Что обновляется в docs/ (Шаг 6)

Из standard-analysis.md §7.3:

| Документ | Что обновляется |
|----------|----------------|
| `{svc}.md` §§ 1-8 | Planned Changes → AS IS (основной контент) |
| `{svc}.md` § 10 Changelog | Новая запись: версия, дата, описание изменений |
| `overview.md` | Обновление если затронута архитектура |
| `conventions.md` | Обновление если затронуты конвенции |
| `infrastructure.md` | Обновление если затронута инфраструктура |
| `testing.md` | Обновление если затронуто тестирование |

### Обработка ошибок

| Ситуация | Реакция |
|----------|---------|
| review.md не RESOLVED | СТОП: "review.md должен быть RESOLVED с вердиктом READY" |
| review.md вердикт CONFLICT | СТОП: "Вердикт CONFLICT — необходим переход в CONFLICT, не DONE" |
| Цепочка не в REVIEW | СТОП: "Цепочка должна быть в статусе REVIEW" |
| cross-chain конфликт | WARN: "Обнаружен конфликт с цепочкой MMMM, необходимо проверить" |
| Ошибка -modify | СТОП на текущем документе, откат невозможен — пользователю решать |

### Идемпотентность

Если документ уже в DONE — пропустить с сообщением. Позволяет перезапуск при частичном выполнении.

## Решения

- **Архитектура: агент, а не просто скилл.** chain-done — это агент (AGENT.md) с вызовами скиллов модификации внутри. Причина: много вызовов -modify для каждого документа цепочки, обновление docs/ через /service-modify для каждого SVC-N — это слишком тяжело для обычного скилла-обёртки. Агент получает полный контекст цепочки и последовательно вызывает нужные скиллы.
- **Связь с /review:** /review при вердикте READY ставит review.md → RESOLVED, затем спрашивает пользователя через AskUserQuestion: "Завершить цепочку? (запустить /chain-done)". При подтверждении — вызывает /chain-done (который делегирует агенту).
- **Инструкция → скилл → агент:** create-chain-done.md (SSOT) → /chain-done (скилл-обёртка) → chain-done агент (AGENT.md) — оркестрирует вызовы -modify скиллов
- Bottom-up порядок: Plan Dev → Plan Tests → Design → Discussion (от терминального к корню)
- Design → DONE — триггер обновления docs/ (самый тяжёлый шаг)
- Каждый -modify вызов делает свою работу по обновлению документа: агент только оркестрирует порядок
- chain_status.py обрабатывает T7 переход для каждого документа

## Открытые вопросы

- Нужно ли автоматически предлагать `/milestone-validate` после DONE (следующий шаг — Release)?
- Нужен ли `--dry-run` режим для предварительного просмотра изменений?
- Как обрабатывать ситуацию когда один из -modify шагов не прошёл (частичный DONE)?
- Какие tools доступны агенту? (Read, Bash, Glob, Grep — минимум; Write, Edit — для docs/ update через -modify скиллы)
- Как агент вызывает скиллы? Через Skill tool или напрямую читает SSOT и выполняет шаги?

---

## Что уже описано в проекте

### 1. standard-analysis.md — SSOT аналитического контура

**Путь:** `specs/.instructions/analysis/standard-analysis.md`

- **§ 5 Статусы (строки 366-428):** Полная таблица TRANSITION_MATRIX с 10 переходами. T7 (REVIEW → DONE) описан как per-document bottom-up каскад. DONE — финальный статус, из него нет переходов. DONE-документы не затрагиваются каскадом CONFLICT (строка 496).
- **§ 6.5 RUNNING to REVIEW (строки 608-626):** Определяет prerequisites перехода в REVIEW: все TASK-N выполнены. Вердикты review.md: READY → DONE, NOT READY → остаётся REVIEW, CONFLICT → каскад CONFLICT.
- **§ 6.6 REVIEW to DONE (строки 628-663):** Единственный per-document каскад. Порядок: Plan Dev → Plan Tests → Design → Discussion. При Design → DONE: Planned Changes переносятся в AS IS (§ 7.3). Кросс-цепочечная обратная связь обязательна при обновлении docs/. Шаг T7 `transition(to="DONE", document="plan-dev")` — chain_status.py автоматически каскадирует bottom-up.
- **§ 7.3 Обновление при реализации (строки 769-787):** Конкретная таблица: `{svc}.md §§ 1-8` — Planned Changes → AS IS, `{svc}.md § 10` — Planned Changes → Changelog, `overview.md` → AS IS + Changelog, `infrastructure.md` и `conventions.md` — если были Planned Changes.
- **Решение #14 (строка 1031):** "Каскад DONE — Per-document, bottom-up. Plan Dev → Plan Tests → Design → Discussion."
- **§ 2.3 Design v2 (строка 178):** Маппинг SVC-N → {svc}.md — подсекции §§ 1-8 в SVC-N имеют идентичные названия с секциями §§ 1-8 в `docs/{svc}.md`. § 9 «Решения по реализации» — Design-only, не пишется в {svc}.md.

### 2. standard-process.md — Стандарт процесса поставки ценности

**Путь:** `specs/.instructions/standard-process.md`

- **Фаза 5: Завершение цепочки (строки 261-268):** Три шага — 5.1 RUNNING → REVIEW, 5.2 Review iterations, 5.3 REVIEW → DONE. Для шага 5.3 указаны скиллы: `/analysis-status`, `/service-modify`. SSOT ссылается на standard-analysis.md §§ 6.5, 6.6.
- **§ 8.1 Сводная таблица инструментов (строка 424):** Шаг 5.3 → DONE перечисляет скрипт `chain_status.py` и скиллы `/analysis-status`, `/service-modify`. Агенты не указаны.
- **§ 10 Пробелы и планы (строка 521):** G11 — "Нет `/chain-done` скилла". Приоритет: Средний. Указан драфт `.claude/drafts/2026-02-24-chain-done.md`.
- **§ 9 Quick Reference (строка 493):** Фаза 5 описана тремя командами: `/analysis-status` для обоих переходов (RUNNING → REVIEW и REVIEW → DONE) и `/review` для итераций.

### 3. chain_status.py — SSOT модуль управления статусами

**Путь:** `specs/.instructions/.scripts/chain_status.py`

- **DONE_CASCADE_ORDER (строка 87):** `["plan-dev", "plan-test", "design", "discussion"]` — bottom-up порядок закодирован явно.
- **SIDE_EFFECTS (строки 98-143):** Для каждого перехода определены побочные эффекты:
  - `("design", "DONE")` (строки 118-124): 4 эффекта — Planned Changes → AS IS, Changelog, overview.md, кросс-цепочечная проверка.
  - `("plan-test", "DONE")` (строки 126-128): обновить docs/.system/testing.md.
  - При T7 (строки 577-582): метод `_collect_side_effects` собирает side_effects для КАЖДОГО уровня в DONE_CASCADE_ORDER.
- **transition() метод (строки 591-723):** Для T7 (строки 671-679): итерирует DONE_CASCADE_ORDER, пропускает уже DONE, вызывает `_update_status` для каждого документа. README dashboard обновляется автоматически.
- **_check_t7() (строки 467-482):** Prerequisites: review.md должен иметь status==RESOLVED. Если нет — PrerequisiteError PRE009.
- **dry_run=True (строки 651-667):** chain_status.py уже поддерживает dry_run — собирает from_statuses и side_effects без записи. Это отвечает на открытый вопрос о `--dry-run`.
- **check_cross_chain() (строки 732-822):** Сканирует docs/ на `<!-- chain: NNNN-{topic} -->` маркеры, определяет severity (info/warning/critical), возвращает CrossChainAlert[]. Должен вызываться после обновления docs/.

### 4. analysis-status.py — Скрипт отображения статусов

**Путь:** `specs/.instructions/.scripts/analysis-status.py`

- Делегирует работу ChainManager (строки 42, 96-108). Функция `update_readme` (строки 174-190) вызывает `mgr._update_readme_dashboard()`. Скилл `/analysis-status` — обёртка над этим скриптом.
- В текущем виде `/analysis-status` не выполняет переходы, только читает и обновляет dashboard. Для chain-done нужен другой скилл, который оркестрирует T7 переход.

### 5. standard-review.md (analysis) — Стандарт review.md

**Путь:** `specs/.instructions/analysis/review/standard-review.md`

- **§ 4 Переходы статусов (строки 159-175):** Только OPEN → RESOLVED. `RESOLVED` блокирует Plan Dev → DONE. review.md НЕ участвует в каскадах DONE как субъект (строка 172).
- **§ 1 Lifecycle (строки 58-91):** Ветка 1 — вердикт READY → status: RESOLVED → каскад DONE. Каскад DONE запускается ПОСЛЕ RESOLVED.
- **§ 5.2 Итерация N (строки 204-235):** Критерий READY: нет open P1, нет open P2, все P3 resolved или wontfix. Open P3 блокирует READY (строка 230).

### 6. modify-service.md — Воркфлоу изменения сервисной документации

**Путь:** `specs/.instructions/docs/service/modify-service.md`

- **Сценарий 5: Завершён analysis/ (строки 121-134):** Конкретные шаги при analysis/ → DONE: (1) удалить запись Planned Changes, (2) добавить запись в Changelog, (3) обновить затронутые секции (API, Data Model и т.д. по сценариям 1-4). Это то, что `/service-modify --scenario 5` делает.
- **Сценарий 6: Добавлен новый analysis/ (строки 136-147):** Обратный процесс — добавление Planned Changes.

### 7. Скилл /service-modify — Обёртка над modify-service.md

**Путь:** `.claude/skills/service-modify/SKILL.md`

- Принимает `--scenario 5` для завершения analysis/. Вызов: `/service-modify {svc} --scenario 5`. Это инструмент, который chain-done будет вызывать для обновления docs/{svc}.md на шаге 6.

### 8. Скиллы -modify (plan-dev, plan-test, design, discussion)

**Пути:**
- `.claude/skills/plan-dev-modify/SKILL.md` — SSOT: `modify-plan-dev.md`
- `.claude/skills/plan-test-modify/SKILL.md` — SSOT: `modify-plan-test.md`
- `.claude/skills/design-modify/SKILL.md` — SSOT: `modify-design.md`
- `.claude/skills/discussion-modify/SKILL.md` — SSOT: `modify-discussion.md`

Все принимают `--status WAITING`, но НЕ принимают `--status DONE`. Это значит, что chain-done НЕ может делегировать переход в DONE через `-modify` скиллы. chain_status.py уже делает `_update_status()` для каждого документа в DONE_CASCADE_ORDER (строки 671-679). Фактически, -modify скиллы нужны chain-done только для обновления контента docs/, а не для переходов статусов.

### 9. Скилл /dev-create — Аналог-оркестратор (WAITING → RUNNING)

**Путь:** `.claude/skills/dev-create/SKILL.md`, SSOT: `.github/.instructions/development/create-development.md`

- 8-шаговый воркфлоу: prerequisite check → подтверждение → Issues → Milestone → Branch → RUNNING → отчёт → предложение `/dev`. Это ближайший аналог для chain-done по структуре: оба — оркестраторы перехода статуса с side effects.
- Шаг 2 — блокирующее подтверждение пользователя через AskUserQuestion. chain-done имеет аналогичный шаг 2.
- Шаг 6 — вызов `ChainManager.transition(to="RUNNING")`. chain-done аналогично: `ChainManager.transition(to="DONE", document="plan-dev")`.
- Шаг 7 — отчёт. chain-done аналогичный шаг 11.

### 10. check-chain-readiness.py — Скрипт проверки prerequisites

**Путь:** `.github/.instructions/.scripts/check-chain-readiness.py`

- Проверяет 4/4 WAITING + 0 маркеров. Аналог для chain-done: нужно проверять все 4 в REVIEW + review.md RESOLVED. Этот скрипт — пример паттерна "скрипт prerequisites перед оркестрацией".

### 11. Правило analysis-status-transition

**Путь:** `.claude/rules/analysis-status-transition.md`

- Правило активируется при работе с `specs/analysis/**`. Напоминает: все переходы статусов — через `chain_status.py`, ручное изменение `status:` запрещено. chain-done должен следовать этому правилу.

### 12. Скилл /technology-modify

**Путь:** `.claude/skills/technology-modify/SKILL.md`

- Сценарии A-D. chain-done может вызывать для финализации per-tech стандартов (шаг 7 из черновика). Нет специального сценария "DONE", но возможно подойдёт сценарий B (обновление конвенций).

---

## Best practices

### 1. Saga Pattern для multi-step orchestration

chain-done — это по сути Saga (distributed transactions pattern): последовательность шагов, где каждый шаг меняет состояние, и при ошибке нужна компенсация. В проекте уже принято решение "откат невозможен — пользователю решать" (строка 131 черновика). Это соответствует Forward Recovery Saga: при ошибке не откатываемся, а повторяем (идемпотентность) или передаём управление. Конкретная рекомендация: каждый шаг chain-done должен записывать в TransitionResult промежуточный прогресс (какие документы уже DONE), чтобы при перезапуске пропускать выполненные шаги. chain_status.py уже реализует это: `if doc_status == "DONE": continue` (строка 676).

### 2. Idempotent Operations

Раздел "Идемпотентность" черновика (строка 133) уже декларирует: "если документ уже в DONE — пропустить". Но идемпотентность нужна на КАЖДОМ под-шаге, а не только на уровне документов:
- Обновление docs/{svc}.md: если Planned Changes уже перенесены в AS IS — пропустить (проверка: маркер `<!-- chain: NNNN-{topic} -->` отсутствует в секции Planned Changes).
- Обновление Changelog: если запись для данной цепочки уже есть — пропустить (проверка: grep по `analysis/{NNNN}` в секции Changelog).
- check_cross_chain(): безусловно безопасен для повторного вызова — возвращает alerts без side effects.

### 3. Checkpoint and Resume Pattern

При длинных оркестрациях (11 шагов) целесообразно сохранять чекпоинт прогресса. В контексте проекта чекпоинт — это сами frontmatter файлов цепочки. `ChainManager.status()` — это чтение чекпоинта. При перезапуске chain-done после сбоя: (1) вызвать `mgr.status()`, (2) определить, какие документы уже DONE (шаги 3-5, 8 завершены), (3) определить, обновлены ли docs/ (проверить отсутствие chain-маркера в Planned Changes), (4) продолжить с незавершённого шага. Конкретно: если `status()` показывает plan-dev: DONE, plan-test: DONE, design: REVIEW — значит шаг 5 (Design → DONE + docs/ update) не завершён.

### 4. Pre-flight Validation (Fail Fast)

Шаг 1 (проверить prerequisites) должен быть максимально строгим и проверять ВСЁ до начала мутаций:
- Все 4 документа в REVIEW (не только проверка через chain_status.py T7, но и ручная валидация файлов).
- review.md существует и status: RESOLVED (уже есть в `_check_t7()`).
- Вердикт последней итерации review.md = READY (chain_status.py проверяет только status, не вердикт).
- Все docs/{svc}.md, упомянутые в design.md SVC-N, существуют и доступны для записи.
- Design.md содержит хотя бы один SVC-N (иначе шаг 6 пуст).
Пример аналогии: `check-chain-readiness.py` для /dev-create проверяет 4/4 WAITING + 0 маркеров ДО начала создания Issues. chain-done должен иметь аналогичный скрипт или расширенную проверку.

### 5. Observability: Structured Reporting

Шаг 11 (отчёт) должен выводить структурированный результат, а не произвольный текст. Паттерн из `/dev-create` шаг 7: вывести Issues, Milestone, Branch, статус. Для chain-done конкретный формат отчёта:
```
Chain NNNN-{topic} → DONE
  plan-dev.md:    REVIEW → DONE
  plan-test.md:   REVIEW → DONE
  design.md:      REVIEW → DONE (+ docs/ updated)
  discussion.md:  REVIEW → DONE

  docs/ updated:
    - auth.md: §§ 1,2,3,5 updated, Changelog added
    - gateway.md: §§ 2,4 updated, Changelog added
    - overview.md: AS IS updated

  Cross-chain alerts:
    - 0002-payment: WARNING — Planned Changes context changed

  Next: /milestone-validate
```

### 6. Separation of Concerns: Orchestrator vs Executor

Черновик правильно декларирует: "скилл только оркестрирует порядок" (строка 142). Это паттерн Orchestrator/Choreography. Конкретные разграничения:
- chain-done НЕ редактирует файлы docs/ напрямую — делегирует `/service-modify --scenario 5` для каждого сервиса.
- chain-done НЕ меняет frontmatter напрямую — делегирует `ChainManager.transition(to="DONE")`.
- chain-done НЕ валидирует обновлённые docs/ — делегирует `validate-docs-service.py` через `/service-modify`.
Проект уже следует этому: `/dev-create` не создаёт Issues напрямую — делегирует `/issue-create`.

### 7. Defensive Cross-chain Check Placement

`check_cross_chain()` должен вызываться ПОСЛЕ обновления docs/ и ПЕРЕД завершением каскада (между шагами 6-7 и шагом 8). Это соответствует standard-analysis.md § 7.2 (строка 765): "Проверка происходит до завершения текущего каскада DONE/CONFLICT". Если `check_cross_chain()` возвращает critical alert (другая цепочка в RUNNING) — chain-done должен ПРЕДУПРЕДИТЬ пользователя, но НЕ прерывать каскад (DONE — финальный, нельзя откатить). Действие на critical: пользователь вручную запускает `/analysis-status` для затронутой цепочки.

### 8. Graceful Degradation при частичном DONE

Открытый вопрос "как обрабатывать ситуацию когда один из -modify шагов не прошёл" имеет практическое решение из паттерна Circuit Breaker / Partial Completion:
- Шаги 3-5 (переходы статусов) через chain_status.py атомарны для каждого документа — если план тестов уже DONE, а дизайн — нет, это валидное промежуточное состояние.
- Шаг 6 (обновление docs/) — самый рискованный. Если `/service-modify --scenario 5` упал на втором сервисе — первый уже обновлён. Рекомендация: обработать каждый SVC-N отдельным вызовом, собирая ошибки. По завершению вывести: "3/5 сервисов обновлены, 2 с ошибками: {svc1}: {reason}, {svc2}: {reason}". Пользователь решает: исправить вручную или перезапустить chain-done (идемпотентность гарантирует безопасность).

### 9. Dry-run как Pre-commit Gate

Открытый вопрос о `--dry-run`: chain_status.py УЖЕ поддерживает `dry_run=True` (строка 651) — возвращает TransitionResult без записи. Для chain-done `--dry-run` должен:
1. Вызвать `mgr.transition(to="DONE", document="plan-dev", dry_run=True)` — получить side_effects.
2. Для каждого SVC-N из design.md — вывести список файлов docs/ и секций, которые будут обновлены.
3. Вызвать `mgr.check_cross_chain()` — вывести потенциальные alerts.
4. НЕ менять ни одного файла.
Это даёт пользователю полный preview перед необратимым DONE.

### 10. Post-DONE Proposal

Открытый вопрос о `/milestone-validate`: в standard-process.md Фаза 6 следует непосредственно после Фазы 5. Паттерн уже реализован в `/dev-create` (шаг 8: "Предложить начать разработку `/dev`"). chain-done аналогично: после шага 11 (отчёт) — AskUserQuestion: "Цепочка NNNN-{topic} завершена. Все цепочки Milestone {vX.Y} завершены? Запустить `/milestone-validate`?" Проверка: `mgr.check_cross_chain()` может показать, есть ли другие RUNNING/REVIEW цепочки в том же Milestone — если есть, не предлагать milestone-validate.
