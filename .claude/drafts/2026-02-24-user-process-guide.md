---
description: Инструкция create-chain.md + скилл /chain — оркестратор полного цикла через TaskList. Заменяет user-guide.md.
type: feature
status: draft
created: 2026-02-24
---

# /chain — оркестратор полного цикла через TaskList

Скилл `/chain` читает standard-process.md и создаёт TaskList с полной последовательностью шагов от идеи до релиза. Каждая задача содержит конкретный скилл/агент и blockedBy-зависимости — ничего не будет пропущено ни LLM, ни человеком.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблема](#1-проблема)
  - [2. Решение — /chain + TaskList](#2-решение--chain--tasklist)
  - [3. TaskList: Happy Path](#3-tasklist-happy-path)
  - [4. TaskList: CONFLICT](#4-tasklist-conflict)
  - [5. TaskList: Альтернативные пути](#5-tasklist-альтернативные-пути)
  - [6. create-chain.md — инструкция](#6-create-chainmd--инструкция)
  - [7. /chain SKILL.md](#7-chain-skillmd)
  - [8. Интеграция в CLAUDE.md и rules](#8-интеграция-в-claudemd-и-rules)
  - [9. Возобновление после прерывания](#9-возобновление-после-прерывания)
  - [10. Изменения в стандартах](#10-изменения-в-стандартах)
- [Решения](#решения)
- [Закрытые вопросы](#закрытые-вопросы)
- [Задачи](#задачи)

---

## Контекст

**Задача:** Заменить идею "user-guide.md" (статичный документ) динамическим оркестратором процесса
**Почему создан:** standard-process.md описывает систему для Claude, но не даёт пошаговую последовательность. Статичный user-guide.md устаревает и не трекает прогресс. TaskList решает обе проблемы: порядок зафиксирован зависимостями, прогресс видим, контекст не теряется между сессиями.
**Связанные файлы:**
- `specs/.instructions/standard-process.md` — SSOT процесса (§§ 1-10)
- `specs/.instructions/analysis/standard-analysis.md` — 4 уровня, статусы, каскады
- `.github/.instructions/standard-github-workflow.md` — GitHub workflow
- `.github/.instructions/development/standard-development.md` — процесс разработки
- `.github/.instructions/releases/standard-release.md` — релизный процесс

**Предшественник:** Этот черновик заменяет исследование "User Process Guide — оркестрация разработчика". Выводы исследования: статичный документ не решает проблему потери контекста и трекинга прогресса. TaskList — динамическая альтернатива.

---

## Содержание

### 1. Проблема

**Три проблемы с текущим процессом:**

| Проблема | Последствие |
|----------|------------|
| standard-process.md написан для Claude | Человек не знает "что мне делать на каждом шаге" |
| LLM теряет контекст между сессиями | Возобновление требует перечитывания всех документов |
| Нет трекинга прогресса | Ни человек, ни LLM не видят "где мы сейчас" |

**Почему статичный user-guide.md не решает:**
- Устаревает при изменении standard-process.md
- Не трекает прогресс — человек должен сам помнить "на каком шаге"
- LLM не использует его при работе — читает инструкции, не гайды
- Дублирует information из standard-process.md в другом формате

### 2. Решение — /chain + TaskList

**`/chain`** — скилл, который:
1. Читает standard-process.md (SSOT)
2. Определяет путь (A: Happy Path, B: CONFLICT, C: альтернативный)
3. Создаёт TaskList через TaskCreate с **конкретным скиллом** в каждой задаче
4. Устанавливает blockedBy-зависимости — нельзя пропустить шаг
5. Берёт первую задачу в работу

**Что это даёт:**

| Было | Стало |
|------|-------|
| Человек читает документ, пытается понять порядок | Видит TaskList: pending → in_progress → completed |
| LLM перечитывает standard-process.md каждую сессию | LLM читает TaskList → знает где остановился |
| Неправильный скилл, пропущен шаг | Каждая задача = конкретный скилл, blockedBy = порядок |
| "Что дальше?" | TaskList → следующая pending задача без blockers |

**Ключевое отличие от user-guide.md:** TaskList — не документ для чтения, а **исполняемый план**. LLM не просто знает порядок — он **работает по нему**, отмечая задачи completed.

### 3. TaskList: Happy Path

При вызове `/chain` для нового изменения (Путь A) создаётся следующий TaskList:

```
TASK 1: Создать Discussion
  description: >
    /discussion-create — описать проблему, требования, критерии успеха.
    Пользователь описывает идею → Claude задаёт уточняющие вопросы (Clarify) →
    генерирует discussion.md → пользователь ревьюит → WAITING.
    SSOT: standard-discussion.md
  activeForm: Создаю Discussion
  blockedBy: —

TASK 2: Создать Design
  description: >
    /design-create — Unified Scan (5 источников), SVC-N секции (9 подсекций),
    INT-N контракты, STS-N системные тесты.
    Claude читает discussion.md + docs/ → проектирует → пользователь ревьюит → WAITING.
    При WAITING: Planned Changes в docs/, заглушки новых сервисов, per-tech стандарты.
    SSOT: standard-design.md
  activeForm: Создаю Design
  blockedBy: [1]

TASK 3: Создать Plan Tests
  description: >
    /plan-test-create — TC-N acceptance-сценарии, тестовые данные, матрица покрытия.
    Claude читает design.md → генерирует тест-сценарии → пользователь ревьюит → WAITING.
    SSOT: standard-plan-test.md
  activeForm: Создаю Plan Tests
  blockedBy: [2]

TASK 4: Создать Plan Dev
  description: >
    /plan-dev-create — TASK-N задачи, подзадачи, BLOCK-N, зависимости, маппинг Issues.
    Автоматически вызывает /review-create (review.md).
    Claude читает design.md + plan-test.md → генерирует план → пользователь ревьюит → WAITING.
    SSOT: standard-plan-dev.md
  activeForm: Создаю Plan Dev
  blockedBy: [3]

TASK 5: Запустить разработку
  description: >
    /dev-create {NNNN} — создание GitHub Issues, Milestone, Branch.
    Все 4 документа → RUNNING. Claude создаёт Issues по TASK-N, привязывает к Milestone,
    создаёт feature-ветку.
    Пользователь проверяет на GitHub: Issues, Milestone, Branch.
    SSOT: create-development.md
  activeForm: Запускаю разработку
  blockedBy: [4]

TASK 6: Разработка
  description: >
    /dev — dev-agent выполняет BLOCK-N (код, тесты, коммиты, CONFLICT-детекция).
    Параллельные агенты по волнам. Per-service тесты внутри блока,
    системные тесты после волны.
    При CONFLICT → см. Путь B (новые задачи добавляются динамически).
    SSOT: modify-development.md
  activeForm: Разработка
  blockedBy: [5]

TASK 7: Ревью ветки
  description: >
    /review — локальное ревью ветки перед PR.
    code-reviewer агенты проверяют diff по 7 критериям.
    Вердикт: READY → продолжить, NOT READY → исправить, CONFLICT → Путь B.
    SSOT: validation-review.md
  activeForm: Ревью ветки
  blockedBy: [6]

TASK 8: Создать PR
  description: >
    /pr-create — git push + gh pr create.
    Claude собирает Issues цепочки, формирует body, привязывает labels.
    Пользователь проверяет PR на GitHub.
    SSOT: standard-pull-request.md
  activeForm: Создаю PR
  blockedBy: [7]

TASK 9: Ревью PR
  description: >
    /review {PR-N} — code-reviewer агенты проверяют PR на GitHub.
    Итерации: замечания → исправления → повторный /review.
    Вердикт READY → мержить. NOT READY → исправить. CONFLICT → Путь B.
    SSOT: standard-review.md
  activeForm: Ревью PR
  blockedBy: [8]

TASK 10: Merge
  description: >
    /merge — squash merge PR, закрытие Issues, синхронизация main.
    Claude мержит PR, синхронизирует локальный main.
    SSOT: standard-review.md § 3, standard-sync.md
  activeForm: Merge
  blockedBy: [9]

TASK 11: Завершить цепочку
  description: >
    /chain-done {NNNN} — RUNNING → REVIEW → DONE.
    Bottom-up каскад: plan-dev → plan-test → design → discussion.
    Обновление docs/: Planned Changes → AS IS, Changelog.
    Cross-chain проверка (check_cross_chain).
    SSOT: standard-analysis.md §§ 6.5-6.6, 7.3
  activeForm: Завершаю цепочку
  blockedBy: [10]

TASK 12: Релиз (опционально)
  description: >
    Пользователь решает: создавать релиз сейчас или накопить изменения.
    Если да → создать GitHub Release: changelog, tag, milestone close.
    SSOT: standard-release.md, create-release.md
  activeForm: Создаю релиз
  blockedBy: [11]
```

**Динамическое поведение:**
- Task 12 (Релиз) — опциональная. LLM спрашивает через AskUserQuestion: "Создать релиз?" Если нет → задача удаляется (status: deleted)
- При CONFLICT на любом шаге → LLM добавляет задачи Пути B (§ 4) в TaskList динамически
- {NNNN} подставляется из Task 1 (номер цепочки)

### 4. TaskList: CONFLICT

При обнаружении CONFLICT (во время Task 6, 7 или 9) LLM **динамически** добавляет задачи разрешения в TaskList:

```
TASK 6.1: Каскад CONFLICT
  description: >
    Вся цепочка → CONFLICT (chain_status.py T4/T8).
    Claude классифицирует уровень: Design / Plan Tests / Plan Dev / Discussion.
    Определяет самый высокий затронутый документ.
    SSOT: standard-analysis.md § 6.3
  activeForm: Каскад CONFLICT
  blockedBy: —  (вставляется сразу при обнаружении)

TASK 6.2: Разрешить CONFLICT (сверху вниз)
  description: >
    /{level}-modify для каждого затронутого документа, сверху вниз.
    Пользователь ревьюит каждый изменённый документ → WAITING.
    SSOT: standard-analysis.md § 6.4
  activeForm: Разрешаю CONFLICT
  blockedBy: [6.1]

TASK 6.3: Повторный запуск
  description: >
    /dev-create {NNNN} --resume — все WAITING → RUNNING.
    Новые Issues для задач, появившихся после разрешения.
    SSOT: standard-analysis.md § 6.2
  activeForm: Повторный запуск
  blockedBy: [6.2]
```

После TASK 6.3 → возврат к TASK 6 (разработка продолжается с оставшихся BLOCK-N).

### 5. TaskList: Альтернативные пути

**Rollback (C.1):** Пользователь говорит "откати цепочку" → LLM создаёт TaskList:

```
TASK R1: Откат цепочки
  description: >
    /rollback {NNNN} — rollback-agent: T9 → откат артефактов → T10 → REJECTED.
    SSOT: standard-analysis.md §§ 6.7-6.8
  activeForm: Откат цепочки
```

**Hotfix (C.2):** `/chain --hotfix` → тот же TaskList что Happy Path, но Discussion краткая + метки `bug` + `critical`.

**Doc-only (C.4):** `/chain --doc-only` → укороченный TaskList:

```
TASK 1: Создать ветку и PR
  description: >
    Issue (опционально) → Branch → исправления → PR → Merge.
    Без analysis chain. Commit type: docs: или fix:.
    SSOT: standard-process.md § 7 C.4
  activeForm: Doc-only изменение
```

### 6. create-chain.md — инструкция

Расположение: `specs/.instructions/analysis/create-chain.md`

**Формат:** инструкция по стандарту `.instructions/standard-instruction.md`. SSOT для скилла `/chain`.

**Структура инструкции:**

```markdown
# Воркфлоу запуска цепочки

## Принципы
- /chain — ЕДИНСТВЕННАЯ точка входа для изменений системы
- TaskList = исполняемый план, не документ
- Каждая задача = конкретный скилл + SSOT-ссылка
- blockedBy гарантирует порядок
- Возобновление: LLM читает TaskList, продолжает с первой pending

## Шаги

### Шаг 1: Определить путь
Прочитать standard-process.md § 3. Спросить пользователя через AskUserQuestion:
- "Что вы хотите сделать?" → определить тип изменения
- Путь A (Happy Path) — поведение системы
- Путь C.2 (Hotfix) — критический баг
- Путь C.3 (Bug-fix bundle) — несколько мелких багов
- Путь C.4 (Doc-only) — опечатки, форматирование

### Шаг 2: Создать TaskList
На основе пути создать задачи через TaskCreate:
- Happy Path → 12 задач (§ 3 этого черновика)
- Hotfix → 12 задач + метки bug/critical
- Bug-fix bundle → 12 задач, Discussion группирует фиксы
- Doc-only → 1 задача

Для каждой задачи:
- subject: глагол + объект ("Создать Discussion")
- description: скилл + что происходит + что делает пользователь + SSOT
- activeForm: present continuous ("Создаю Discussion")
- blockedBy: зависимости по порядку

### Шаг 3: Подтвердить TaskList
Показать TaskList пользователю. AskUserQuestion: "План из N задач создан. Начинаем?"

### Шаг 4: Начать выполнение
TaskUpdate первой задачи → in_progress. Запустить соответствующий скилл.

### Шаг 5: Возобновление (при прерывании)
При входе в существующую сессию с TaskList:
1. TaskList → найти первую pending без blockers
2. Прочитать описание задачи → запустить скилл
3. Продолжить

## Чек-лист
- [ ] Путь определён (A/C.2/C.3/C.4)
- [ ] TaskList создан с корректными blockedBy
- [ ] Каждая задача содержит скилл и SSOT-ссылку
- [ ] Пользователь подтвердил план
```

### 7. /chain SKILL.md

Расположение: `.claude/skills/chain/SKILL.md`

**Формат:** скилл по стандарту `.claude/.instructions/skills/standard-skill.md`.

```yaml
---
name: chain
description: Оркестратор полного цикла — создаёт TaskList от идеи до релиза по standard-process.md.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.0
index: .claude/.instructions/skills/README.md
ssot: specs/.instructions/analysis/create-chain.md
version: v1.0
---
```

**Формат вызова:**

```
/chain              — Happy Path (Путь A)
/chain --hotfix     — Hotfix (Путь C.2)
/chain --bug-bundle — Bug-fix bundle (Путь C.3)
/chain --doc-only   — Doc-only (Путь C.4)
/chain --resume     — Возобновить существующий TaskList
```

### 8. Интеграция в CLAUDE.md и rules

**CLAUDE.md — главная ссылка:**

```markdown
## Разработка

**Любое изменение системы начинается с:** `/chain`

Скилл `/chain` создаёт TaskList с полной последовательностью от идеи до релиза.
Каждая задача — конкретный скилл в правильном порядке. Прогресс виден в TaskList.

| Команда | Когда |
|---------|-------|
| `/chain` | Новая фича, изменение поведения |
| `/chain --hotfix` | Критический баг в production |
| `/chain --doc-only` | Опечатки, форматирование |
| `/chain --resume` | Продолжить после прерывания |
```

**Rule (новый) — `.claude/rules/chain.md`:**

```markdown
При запросе на добавление функциональности, фичи, изменения поведения системы,
исправления бага — предложить `/chain`.

Не начинать напрямую с `/discussion-create`, `/design-create` и т.д.
`/chain` создаёт TaskList с полным планом и гарантирует правильный порядок.

Исключение: если пользователь явно просит конкретный скилл (например,
"/discussion-create для OAuth2") — выполнить запрос напрямую.
```

**Триггер rule:** Глобальный (без path-фильтра) — срабатывает при любом сообщении о добавлении функциональности.

### 9. Возобновление после прерывания

**Сценарий:** Сессия прервалась на Task 6 (разработка). Пользователь возвращается.

**Что делает LLM:**
1. Видит существующий TaskList (TaskList сохраняется между сессиями)
2. TaskList → задачи 1-5 completed, задача 6 in_progress, задачи 7-12 pending
3. Читает описание Task 6 → `/dev`
4. Читает chain status (`chain_status.py status()`) → цепочка RUNNING
5. Продолжает разработку

**Что видит пользователь:**
```
Задачи:
✓ 1. Создать Discussion
✓ 2. Создать Design
✓ 3. Создать Plan Tests
✓ 4. Создать Plan Dev
✓ 5. Запустить разработку
→ 6. Разработка (в процессе)
○ 7. Ревью ветки
○ 8. Создать PR
...
```

**`/chain --resume`:** Явный вызов для возобновления. LLM читает TaskList + chain status, синхронизирует (если LLM пометил задачу in_progress, но скилл не завершился — LLM проверяет реальное состояние и корректирует).

### 10. Изменения в стандартах

#### 10.1 standard-process.md

| Секция | Изменение |
|--------|-----------|
| § 1 или новая секция | Добавить: "**Точка входа:** `/chain` создаёт TaskList с полным планом. См. create-chain.md" |
| § 9 Quick Reference | Добавить в начало: `/chain` — оркестратор полного цикла (TaskList) |
| § 10 Пробелы | Нет нового пробела — `/chain` закрывает потребность в user-guide |

#### 10.2 CLAUDE.md

| Секция | Изменение |
|--------|-----------|
| Секция "Разработка" (новая, после "Паттерны") | Добавить блок из § 8 этого черновика: `/chain` как главная ссылка |

#### 10.3 onboarding.md

| Секция | Изменение |
|--------|-----------|
| "Первые шаги" | Добавить: "Любое изменение начинай с `/chain`" |

#### 10.4 .claude/rules/

| Файл | Действие |
|------|----------|
| `chain.md` (новый) | Rule из § 8 этого черновика |

#### 10.5 specs/.instructions/analysis/README.md

| Секция | Изменение |
|--------|-----------|
| Таблица инструкций | Добавить строку: create-chain.md — "Оркестратор полного цикла (TaskList)" |

#### 10.6 .structure/quick-start.md

| Секция | Изменение |
|--------|-----------|
| "Процесс поставки ценности" (строки 51-55) | Добавить `/chain` как точку входа: "Любое изменение системы начинается с `/chain`". Ссылка на standard-process.md остаётся как SSOT |

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| R1 | TaskList вместо user-guide.md | Динамический, трекает прогресс, переживает контекстные потери, используется LLM при работе |
| R2 | /chain — единственная точка входа | Гарантирует правильный порядок и набор скиллов. Исключение: пользователь явно просит конкретный скилл |
| R3 | create-chain.md в specs/.instructions/analysis/ | Рядом с create-discussion.md, create-design.md — тот же уровень (инструкция создания) |
| R4 | Скилл, не агент | /chain создаёт TaskList в основном контексте (нужен доступ к TaskCreate). Не тяжёлая операция — не нужен subprocess |
| R5 | blockedBy для порядка | Нельзя начать Design без завершения Discussion. TaskList enforcement, не документационное соглашение |
| R6 | Динамическое добавление задач при CONFLICT | CONFLICT непредсказуем — задачи разрешения добавляются в TaskList в момент обнаружения |
| R7 | Rule chain.md — глобальный | При любом запросе на изменение системы — предложить /chain. Не path-specific |
| R8 | CLAUDE.md — главная ссылка | `/chain` — первое что видит Claude при работе с проектом |
| R9 | --resume для возобновления | Явный вызов для продолжения после прерывания. LLM синхронизирует TaskList с реальным состоянием |
| R10 | Не заменяет standard-process.md | standard-process.md — SSOT системы. /chain — фронтенд к нему. create-chain.md читает standard-process.md, не дублирует |

---

## Закрытые вопросы

### Q1. Где размещать user guide?

**Ответ: нигде.** Вместо статичного документа — `/chain` + TaskList. TaskList = динамический user guide, который трекает прогресс, переживает потери контекста и использует правильные скиллы.

### Q2. Как обновлять при изменении standard-process.md?

**Ответ: автоматически.** create-chain.md читает standard-process.md при каждом вызове `/chain`. Если standard-process.md изменился — TaskList генерируется по новой версии. Нет ручной синхронизации.

### Q3. Скилл или агент?

**Ответ: скилл.** `/chain` создаёт TaskList (TaskCreate) и запускает первый скилл. Это координация, не тяжёлая работа. Нужен основной контекст LLM для доступа к TaskCreate и AskUserQuestion.

→ R4

### Q4. Что если пользователь хочет конкретный скилл напрямую?

**Ответ: допускается.** Rule chain.md предлагает /chain, но если пользователь явно говорит "/discussion-create для OAuth2" — выполнить напрямую. /chain — рекомендация, не принуждение. Опытный пользователь может работать без TaskList.

### Q5. Нужен ли cheat sheet / памятка?

**Ответ: нет.** TaskList IS the cheat sheet. Пользователь видит список задач с описаниями — это и есть памятка, причём контекстная (показывает где ты сейчас).

---

## Задачи

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Создать create-chain.md
  description: >
    Драфт: .claude/drafts/2026-02-24-user-process-guide.md (секция "§ 6")
    /instruction-create для specs/.instructions/analysis/create-chain.md.
    Инструкция по стандарту standard-instruction.md: принципы, шаги (определить путь,
    создать TaskList, подтвердить, начать выполнение, возобновление), чек-лист.
    SSOT: standard-process.md (читается при генерации TaskList).
    Шаблон TaskList: 12 задач Happy Path (§ 3 черновика) + динамические CONFLICT (§ 4)
    + альтернативные пути (§ 5).
  activeForm: Создаю create-chain.md

TASK 2: Создать /chain SKILL.md
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-user-process-guide.md (секция "§ 7")
    /skill-create для .claude/skills/chain/SKILL.md.
    SSOT: specs/.instructions/analysis/create-chain.md.
    Параметры: --hotfix, --bug-bundle, --doc-only, --resume.
    Воркфлоу: прочитать create-chain.md → выполнить шаги.
  activeForm: Создаю /chain SKILL.md

TASK 3: Создать rule chain.md
  description: >
    Драфт: .claude/drafts/2026-02-24-user-process-guide.md (секция "§ 8")
    /rule-create для .claude/rules/chain.md.
    Глобальный rule (без path-фильтра): при запросе на изменение системы — предложить /chain.
    Исключение: пользователь явно просит конкретный скилл.
  activeForm: Создаю rule chain.md

TASK 4: Обновить CLAUDE.md — главная ссылка
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-user-process-guide.md (секция "§ 8")
    Добавить секцию "Разработка" в CLAUDE.md (после "Паттерны"):
    "/chain — точка входа для любого изменения системы".
    Таблица: /chain, /chain --hotfix, /chain --doc-only, /chain --resume.
  activeForm: Обновляю CLAUDE.md

TASK 5: Обновить onboarding.md
  blockedBy: [2]
  description: >
    Обновить .claude/onboarding.md:
    - Секция "Первые шаги": добавить "Любое изменение начинай с /chain"
    - Ссылка на create-chain.md как SSOT
  activeForm: Обновляю onboarding.md

TASK 5.1: Обновить quick-start.md
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-user-process-guide.md (секция "§ 10.6")
    Обновить .structure/quick-start.md:
    - Секция "Процесс поставки ценности": добавить "/chain — точка входа"
    - Ссылка на standard-process.md остаётся как SSOT
  activeForm: Обновляю quick-start.md

TASK 6: Обновить standard-process.md
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-user-process-guide.md (секция "§ 10.1")
    Обновить specs/.instructions/standard-process.md:
    - § 1 или новая секция: "Точка входа: /chain создаёт TaskList"
    - § 9 Quick Reference: добавить /chain в начало
  activeForm: Обновляю standard-process.md

TASK 7: Обновить specs/.instructions/analysis/README.md
  blockedBy: [1]
  description: >
    Добавить строку в таблицу инструкций:
    create-chain.md — "Оркестратор полного цикла (TaskList)"
  activeForm: Обновляю analysis README

TASK 8: Миграция standard-process.md
  blockedBy: [6]
  description: >
    /migration-create для standard-process.md.
    Синхронизировать зависимые файлы.
  activeForm: Мигрирую зависимости

TASK 9: Валидация миграции
  blockedBy: [8]
  description: >
    /migration-validate для standard-process.md.
    Убедиться что все зависимые файлы синхронизированы.
  activeForm: Валидирую миграцию

TASK 10: Обновить CLAUDE.md — отметка выполнения
  blockedBy: [7]
  description: >
    В CLAUDE.md отметить user-process-guide как [x] выполненный.
  activeForm: Обновляю CLAUDE.md
```
