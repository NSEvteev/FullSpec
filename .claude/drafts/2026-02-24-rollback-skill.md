# Скилл /rollback — оценка и план

Скилл для отката analysis chain (ROLLING_BACK → REJECTED) и GitHub артефактов.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G9 из standard-process.md — нет `/rollback` скилла
**Почему создан:** Определить нужен ли скилл-оркестратор или достаточно -modify скиллов
**Связанные файлы:**
- `specs/.instructions/analysis/standard-analysis.md` — § 6.7 to ROLLING_BACK
- `specs/.instructions/.scripts/chain_status.py` — T9, T10
- `specs/.instructions/standard-process.md` — §7 C.1 Rollback / Reject

## Содержание

### Что уже покрыто

- `standard-analysis.md § 6.7` — полное описание ROLLING_BACK процесса
- `chain_status.py` — T9 (→ ROLLING_BACK), T10 (→ REJECTED)
- `-modify` скиллы — откат каждого документа отдельно

### Что делает rollback (из standard-analysis.md)

1. Вся цепочка → ROLLING_BACK (T9)
2. Откат артефактов:
   - Issues закрыты (`/issue-modify`)
   - Ветка удалена
   - Planned Changes убраны из docs/ (`/service-modify`)
   - Per-tech стандарты откачены (`/technology-modify`)
3. ROLLING_BACK → REJECTED (T10)

### Что даёт скилл

| Функция | Сейчас | С `/rollback` |
|---------|--------|--------------|
| Переход статуса | `/analysis-status` | Один вызов |
| Откат docs/ | Ручной через -modify | Автоматический bottom-up |
| Закрытие Issues | `/issue-modify` per issue | Автоматическое batch-закрытие |
| Удаление ветки | `git branch -D` вручную | Автоматическое |

### Артефакты

| # | Артефакт | Путь | Статус |
|---|---------|------|--------|
| 1 | **Инструкция** (SSOT) | `specs/.instructions/analysis/create-rollback.md` | **Нужно создать** |
| 2 | **Скилл** (обёртка) | `/.claude/skills/rollback/SKILL.md` | **Нужно создать** |

### Формат вызова

```
/rollback {NNNN}
```

### Порядок создания

1. `/instruction-create create-rollback --path specs/.instructions/analysis/`
2. `/skill-create rollback`

## Решения

- Приоритет низкий — можно откатить вручную через -modify скиллы
- Скилл оркестрирует порядок, аналогично `/chain-done` (но в обратном направлении)

## Открытые вопросы

- Аналог `/chain-done` но для отката — повторить паттерн оркестратора?
- Нужно ли подтверждение пользователя перед каждым шагом или один раз в начале?
- Как обрабатывать частичный rollback (часть артефактов уже откачена)?

---

## Что уже описано в проекте

### standard-analysis.md — полная спецификация ROLLING_BACK / REJECTED

**§ 6.7 to ROLLING_BACK (T9):**
- Триггеры: пользователь отменяет, CONFLICT неразрешим, пользователь отклоняет разрешение конфликта
- Переход tree-level: все не-DONE документы цепочки одновременно переводятся в ROLLING_BACK
- DONE-документы не затрагиваются (DONE — финальный статус)
- `chain_status.py` T9: допустим из любого статуса кроме DONE и REJECTED — кодифицировано 5 записей в TRANSITION_MATRIX: `(DRAFT, ROLLING_BACK)`, `(WAITING, ROLLING_BACK)`, `(RUNNING, ROLLING_BACK)`, `(REVIEW, ROLLING_BACK)`, `(CONFLICT, ROLLING_BACK)`
- `result.side_effects` возвращает список действий для LLM (4 категории)

**§ 6.8 ROLLING_BACK to REJECTED (T10):**
- REJECTED — финальный статус
- Условие: все 4 документа цепочки в ROLLING_BACK (`_check_t10()` проверяет каждый документ)
- Перезапуск: если потребность актуальна — новая Discussion со ссылкой на отклонённую

**§ 7.5 Обновление docs/ при откате:**
- При Design → REJECTED: удалить Planned Changes из `{svc}.md § 9`, `overview.md`, `conventions.md`, `infrastructure.md`; удалить заглушки новых сервисов; удалить per-tech стандарты + rule + строку реестра; удалить метки `svc:{svc}`
- При Design (уже DONE) → REJECTED: откат AS IS по SVC-N секциям — ADDED удалить, MODIFIED вернуть, REMOVED восстановить
- При Plan Tests → REJECTED: откат `testing.md` (если были изменения)
- При Plan Dev: Issues закрываются `--reason "not planned"` + комментарий "rolled back"; feature-ветка удаляется
- При Discussion: no-op (нет артефактов)

### chain_status.py — SSOT-реализация T9/T10

**T9 (→ ROLLING_BACK):**
- `TREE_LEVEL_TRANSITIONS` включает T9 — все документы переходят одновременно
- Метод `transition()` пропускает DONE/REJECTED документы (`doc_status in ("DONE", "REJECTED")`)
- `SIDE_EFFECTS[("*", "ROLLING_BACK")]` содержит 4 действия:
  1. Удалить Planned Changes по chain-маркеру
  2. Удалить заглушки `{svc}.md` (если уникальны)
  3. Закрыть Issues `--reason 'not planned'`
  4. Удалить feature-ветку
- Автоматически обновляет README dashboard

**T10 (ROLLING_BACK → REJECTED):**
- `_check_t10()`: Prerequisites — все 4 документа должны быть в ROLLING_BACK (PRE010)
- `transition()` tree-level: все не-DONE/REJECTED документы → REJECTED

**Ограничение:** chain_status.py обновляет frontmatter и README, но **не выполняет** откат артефактов (docs/, Issues, ветка) — это задача LLM/скилла

### standard-process.md — C.1 Rollback / Reject

Путь C.1 описан лаконично (3 строки):
1. Любой → ROLLING_BACK (пользователь отменяет или CONFLICT неразрешим)
2. Откат артефактов: Issues закрыты, ветка удалена, Planned Changes убраны, per-tech откачены
3. ROLLING_BACK → REJECTED (финальный статус)

Инструменты: `/discussion-modify`, `/design-modify`, `/plan-test-modify`, `/plan-dev-modify`, `/issue-modify`

### modify-*.md — откат в каждом документе

Каждый из 4 modify-файлов содержит секции "Переход: → ROLLING_BACK" и "Переход: ROLLING_BACK → REJECTED":

| Документ | Артефакты при откате | Сложность |
|----------|---------------------|-----------|
| **modify-design.md** | 6 типов артефактов: Planned Changes в {svc}.md, overview, conventions, infrastructure; заглушки сервисов (`/service-modify --deactivate`); per-tech стандарты (`/technology-modify --deactivate`) | Высокая — основной блок отката |
| **modify-plan-dev.md** | Issues `--reason "not planned"` + комментарий "rolled back"; feature-ветка удаляется | Средняя — batch-операции GitHub |
| **modify-plan-test.md** | Нет артефактов для отката (Plan Tests не создаёт Planned Changes) | Низкая — только смена статуса |
| **modify-discussion.md** | No-op — Discussion не имеет артефактов | Нулевая |

### modify-development.md — переходы ROLLING_BACK

Файл содержит полный воркфлоу с примерами Python-кода для `ChainManager.transition(to="ROLLING_BACK")` и `transition(to="REJECTED")`. Чек-лист включает пункты для обоих переходов.

### chain-done draft (аналогичный оркестратор)

Draft `2026-02-24-chain-done.md` описывает аналогичную задачу, но для bottom-up DONE перехода. Ключевые паттерны, применимые к rollback:

- **Архитектура:** Инструкция (SSOT) `create-chain-done.md` + Скилл (обёртка) `/chain-done`
- **Оркестрация:** 11 последовательных шагов с проверкой prerequisites, подтверждением, per-document вызовами -modify, обновлением docs/, cross-chain проверкой, отчётом
- **Идемпотентность:** Если документ уже в целевом статусе — пропустить с сообщением
- **Обработка ошибок:** СТОП на текущем документе при ошибке -modify; пользователю решать

### review.md — поведение при ROLLING_BACK

review.md **не участвует** в каскадах ROLLING_BACK как субъект — при откате остаётся в текущем статусе (OPEN/RESOLVED). Его статусная модель (OPEN → RESOLVED) отдельна от 8 статусов chain.

### standard-release.md § 13 — Rollback процесс (production)

Отдельный rollback для production-релизов (не analysis chain). Процесс:
1. Откатить деплой вручную (Docker/Kubernetes/SSH)
2. Определить проблемную версию
3. Удалить проблемный Release и тег
4. Revert merge в main (`git revert`)
5. Создать Issue для исправления
6. Создать новый релиз после исправления

**Ключевое отличие от analysis rollback:** production rollback — откат кода и деплоя; analysis rollback — откат спецификаций и GitHub-артефактов. Два независимых процесса, никогда не пересекаются.

### Существующие скиллы, задействованные при откате

| Скилл | Роль при откате | Когда вызывается |
|-------|----------------|------------------|
| `/issue-modify` | Закрытие Issues `--reason "not planned"` | Plan Dev → ROLLING_BACK |
| `/service-modify` | Удаление Planned Changes, деактивация заглушек | Design → ROLLING_BACK |
| `/technology-modify --scenario D` | Деактивация per-tech стандартов | Design → ROLLING_BACK |
| `/labels-modify` | Удаление меток `svc:{svc}` | Design → ROLLING_BACK (если сервис создан этой цепочкой) |
| `/analysis-status` | Отображение текущих статусов (мониторинг) | До/после rollback |

### Порядок отката (top-down, зеркало chain-done)

chain-done идёт bottom-up (plan-dev → discussion). Rollback — **top-down** по сложности артефактов:
1. **Plan Dev** (Issues, ветка) — самые "внешние" артефакты, зависят от GitHub
2. **Design** (docs/, per-tech, заглушки, метки) — основной блок отката
3. **Plan Tests** (testing.md) — минимальный или no-op
4. **Discussion** (no-op) — только смена статуса

Этот порядок логичен: сначала откатываем то, что видно "снаружи" (Issues, ветка), затем внутренние артефакты (docs/), в конце — формальности.

## Best practices

### 1. Saga Pattern — Orchestration vs Choreography

Rollback analysis chain — классический пример **Saga Orchestration**: центральный координатор (`/rollback` скилл) последовательно вызывает compensating transactions (откат артефактов каждого уровня) в определённом порядке. Это соответствует паттерну orchestration-based saga, где:
- Скилл = Saga Execution Coordinator (SEC)
- Каждый -modify вызов = локальная compensating transaction
- chain_status.py = Saga Log (хранит состояние цепочки)

Choreography (каждый сервис сам реагирует на события) здесь не подходит — порядок отката важен, и нужна единая точка контроля.

### 2. Compensating Transactions — принципы

**Каждый шаг создания имеет симметричный шаг отката:**

| Шаг создания (forward) | Compensating transaction (rollback) |
|------------------------|--------------------------------------|
| Design → WAITING: создать Planned Changes | Удалить Planned Changes по chain-маркеру |
| Design → WAITING: создать заглушку {svc}.md | `/service-modify --deactivate` (удалить если уникальна) |
| Design → WAITING: создать per-tech стандарт | `/technology-modify --scenario D` (деактивация) |
| Design → WAITING: создать метку `svc:{svc}` | `/labels-modify` (удалить метку) |
| Plan Dev → WAITING: review.md создан | review.md остаётся (не участвует в каскаде) |
| dev-create: Issues созданы | `/issue-modify` close `--reason "not planned"` |
| dev-create: ветка создана | `git branch -D`, `git push origin --delete` |
| Design → DONE: Planned Changes → AS IS | Откат AS IS (ADDED → удалить, MODIFIED → вернуть, REMOVED → восстановить) |

**Не все шаги имеют compensating:** Discussion не создаёт артефактов → no-op. Plan Tests (до DONE) не создаёт docs/ артефактов → no-op.

### 3. Idempotent Cleanup — ключевой принцип

Каждая compensating transaction должна быть **идемпотентной** — безопасна при повторном выполнении:
- Удаление Planned Changes по chain-маркеру: если маркера нет — ничего не происходит
- Закрытие Issues: если Issue уже закрыт — ничего не происходит
- Удаление ветки: если ветки нет — ничего не происходит
- Деактивация per-tech: если файла нет — ничего не происходит

Это критично для обработки **частичного rollback** (один из открытых вопросов): если rollback прервался на середине, повторный запуск `/rollback` безопасно повторяет все шаги. Уже откаченные артефакты пропускаются, неоткаченные — обрабатываются.

### 4. Forward-Fix vs Rollback — когда что выбирать

| Стратегия | Когда | В контексте проекта |
|-----------|-------|---------------------|
| **Forward-fix** (исправить и продолжить) | Проблема локализована, исправление простое | CONFLICT → разрешение → WAITING → RUNNING |
| **Rollback** (откатить всё) | Проблема фундаментальная, исправление невозможно или нецелесообразно | CONFLICT → ROLLING_BACK → REJECTED |

В проекте это уже формализовано в § 6.4: при разрешении CONFLICT три исхода — разрешён, неразрешим (→ ROLLING_BACK), пользователь отклоняет (→ ROLLING_BACK). Forward-fix — это путь B (CONFLICT), rollback — путь C.1.

### 5. Partial Rollback — стратегии

**Проблема:** часть артефактов уже откачена, другая — нет. Прерывание может произойти:
- LLM-контекст исчерпан посреди отката
- Ошибка GitHub API (rate limit, network)
- Пользователь прервал сессию

**Стратегия "Resume from failure point"** (рекомендуемая):
1. При запуске `/rollback` — прочитать текущее состояние (chain_status.py + проверка артефактов)
2. Для каждого артефакта: если уже откачен — пропустить (идемпотентность)
3. Продолжить с первого неоткаченного артефакта
4. Чек-лист в конце: все ли артефакты откачены? → T10 (REJECTED)

**Определение "уже откачен":**
- Planned Changes: нет блока с chain-маркером в docs/ файле
- Issues: все Issues milestone закрыты с reason "not planned"
- Ветка: `git branch -r --list "origin/{branch}"` не возвращает результат
- Заглушка: `docs/{svc}.md` не существует (или не содержит `created-by: {chain}`)
- Per-tech: `docs/.technologies/standard-{tech}.md` не существует

### 6. Git Revert vs Branch Deletion — стратегия для analysis chain

В проекте код **не мержится в main до REVIEW → DONE**. При ROLLING_BACK:
- Feature-ветка удаляется (код не попал в main → revert не нужен)
- Если код уже попал в main (Design DONE, потом ROLLING_BACK) — нужен `git revert` для merge-коммита (аналогично standard-release.md § 13)

**Текущий стандарт:** "Код в main отсутствует — revert не нужен" (standard-analysis.md § 6.7). Это корректно для большинства сценариев, но не покрывает edge case когда часть цепочки уже DONE.

### 7. Pivot Transaction — точка невозврата

В Saga Pattern "pivot transaction" — операция после которой rollback невозможен. В analysis chain это **DONE** — финальный статус, из которого нет переходов. Если часть документов уже в DONE, ROLLING_BACK затрагивает только не-DONE документы. Полный rollback DONE-цепочки невозможен — нужна новая Discussion.

### 8. Подтверждение: одно vs per-step

**Рекомендация: одно подтверждение в начале + отчёт в конце.**

Аргументы:
- Rollback — деструктивная операция, пользователь должен осознанно подтвердить
- Per-step подтверждения замедляют процесс и не добавляют ценности (артефакты отката предопределены стандартом)
- Идемпотентность гарантирует безопасность повторного запуска

Исключение: если Design уже DONE (нужен откат AS IS из docs/) — дополнительное подтверждение перед деструктивным изменением docs/.

### 9. Порядок отката — Risk-Based

Рекомендуемый порядок отката основан на **минимизации видимых последствий**:
1. **Plan Dev** (Issues + ветка) — закрыть Issues сразу, чтобы они не висели в open; удалить ветку
2. **Design** (docs/) — основной блок, самый сложный; Planned Changes, заглушки, per-tech
3. **Plan Tests** (testing.md) — обычно no-op
4. **Discussion** — no-op, только финальная смена статуса

Альтернативный порядок (top-down по иерархии: Discussion → Design → Plan Tests → Plan Dev) тоже допустим, но менее эффективен — Discussion/Plan Tests почти всегда no-op.

### 10. Cross-chain при откате

При удалении Planned Changes из docs/ **обязательно** вызвать `check_cross_chain()` — другие цепочки могли учитывать эти Planned Changes при своём проектировании. Реакции по стандарту:
- Другая цепочка в DRAFT: перегенерировать затронутые документы
- Другая цепочка в WAITING: дообновить контекст
- Другая цепочка в RUNNING: → CONFLICT
- Другая цепочка в DONE: предложить новую Discussion
