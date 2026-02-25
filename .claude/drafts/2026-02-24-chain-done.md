---
description: Инструкция create-chain-done.md + chain-done-agent для автономного завершения analysis chain (REVIEW → DONE)
type: feature
status: ready
created: 2026-02-24
---

# Завершение цепочки — инструкция + агент

Вместо скилла `/chain-done`: инструкция процесса завершения и chain-done-agent для экономии контекста основного LLM.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** G11 из standard-process.md — переход REVIEW → DONE должен быть автоматизирован
**Почему создан:** Завершение цепочки — сложная многошаговая операция: bottom-up каскад по 4 документам, перенос Planned Changes → AS IS в docs/, обновление Changelog, cross-chain проверка. Ручной вызов 6-10 команд тратит контекст основного LLM.
**Связанные файлы:**
- `specs/.instructions/analysis/standard-analysis.md` — § 6.6 REVIEW to DONE, § 7.3 обновление docs/ при реализации
- `specs/.instructions/.scripts/chain_status.py` — T7, DONE_CASCADE_ORDER, side_effects, dry_run, check_cross_chain
- `specs/.instructions/standard-process.md` — § 5 Фаза 5 (Завершение), § 8/§ 10
- `.claude/rules/analysis-status-transition.md` — rule для status transitions

## Содержание

### Почему не скилл

| Критерий | Скилл `/chain-done` | Агент `chain-done-agent` |
|----------|---------------------|--------------------------|
| Контекст основного LLM | Тратит (скилл = промпт в основном контексте) | Не тратит (subprocess) |
| Чтение стандарта | Каждый раз в основном контексте | Один раз в subprocess |
| Вложенность скиллов | 3-4 уровня (chain-done → modify → service-modify → ...) | 0 — агент работает напрямую с инструментами |
| Обновление docs/ | Через вложенные `/service-modify --scenario 5` | Напрямую через Edit (читает design SVC-N, редактирует docs/) |
| Вызов | Явный `/chain-done` | Автоматический через Task tool |

Агент работает **напрямую** с Bash, Read, Edit, Grep, Glob — без вложенных скиллов. Читает инструкцию `create-chain-done.md` и выполняет все шаги автономно.

### Архитектура

```
standard-analysis.md §§ 6.6, 7.3         (правила — что делать при DONE)
       ↓ ссылается
create-chain-done.md                       (инструкция — как завершать)
       ↓ SSOT для
chain-done-agent (AGENT.md)                (исполнитель — делает)
```

**Поток вызова:**

```
1. Пользователь: "завершить цепочку NNNN" (или /review выдал вердикт READY)
2. Основной LLM: читает chain status, проверяет review.md RESOLVED + вердикт READY
3. Основной LLM: AskUserQuestion — подтверждение
4. Основной LLM: Task tool → chain-done-agent с промптом "Заверши цепочку NNNN"
5. chain-done-agent: читает create-chain-done.md → выполняет все шаги → возвращает отчёт
6. Основной LLM: показывает отчёт, предлагает /milestone-validate (если все цепочки milestone завершены)
```

Подтверждение — **одно, до запуска агента**. Агент работает автономно после подтверждения.

### Артефакт 1: Инструкция `create-chain-done.md`

**Путь:** `specs/.instructions/analysis/create-chain-done.md`
**Действие:** Создать через `/instruction-create`.
**Тип:** воркфлоу (create-*)

Содержание инструкции — полный алгоритм завершения analysis chain:

#### 1.1. Pre-flight проверки (Fail Fast)

Все проверки — **до** любых мутаций:

1. `python chain_status.py status {NNNN}` — все 4 документа в REVIEW
2. `review.md` существует, `status: RESOLVED`, вердикт последней итерации = `READY`
3. Design.md содержит хотя бы один SVC-N
4. Все `docs/{svc}.md` из SVC-N существуют и содержат блоки Planned Changes с маркером цепочки

Если любая проверка не прошла — **СТОП** с описанием причины.

#### 1.2. Переход T7 (→ DONE)

```python
python chain_status.py transition {NNNN} DONE
```

Bottom-up каскад: Plan Dev → Plan Tests → Design → Discussion. `chain_status.py` итерирует `DONE_CASCADE_ORDER`, пропускает уже DONE. Возвращает `side_effects` для обновления docs/.

#### 1.3. Обновление docs/ (Design → DONE)

Основной блок — перенос Planned Changes → AS IS:

| Файл docs/ | Действие |
|-----------|----------|
| `{svc}.md` §§ 1-8 | Контент из Planned Changes → основные секции (ADDED — добавить, MODIFIED — заменить, REMOVED — удалить) |
| `{svc}.md` § 9 Planned Changes | Удалить блок `<!-- chain: NNNN-{topic} -->` |
| `{svc}.md` § 10 Changelog | Новая запись: номер цепочки, дата, описание изменений |
| `.system/overview.md` | Planned Changes → AS IS + Changelog (если затронута архитектура) |
| `.system/conventions.md` | Planned Changes → AS IS + Changelog (если затронуты конвенции) |
| `.system/infrastructure.md` | Planned Changes → AS IS + Changelog (если затронута инфраструктура) |

**Как агент определяет что менять:** Читает design.md SVC-N секции (§§ 1-8 маппятся 1:1 на docs/{svc}.md §§ 1-8). Каждая подсекция SVC-N содержит дельты ADDED/MODIFIED/REMOVED — агент применяет их к соответствующим секциям docs/.

**Идемпотентность:** Проверить наличие chain-маркера `<!-- chain: NNNN-{topic} -->` в Planned Changes. Если маркера нет — docs/ уже обновлены, skip.

#### 1.4. Обновление testing.md (Plan Tests → DONE)

| Файл docs/ | Действие |
|-----------|----------|
| `.system/testing.md` | Обновить стратегию тестирования (если Plan Tests вносил изменения). Обычно no-op |

#### 1.5. Cross-chain проверка

```python
python chain_status.py check_cross_chain {NNNN}
```

Вызывается **после** обновления docs/ и **до** финального отчёта. Реакции (информировать в отчёте):
- Другая цепочка в DRAFT: перегенерировать затронутые документы
- Другая цепочка в WAITING: дообновить контекст
- Другая цепочка в RUNNING: → CONFLICT (critical alert)
- Другая цепочка в DONE: предложить новую Discussion

При critical alert — **предупредить в отчёте**, но НЕ прерывать (DONE — финальный, откат невозможен).

#### 1.6. Отчёт

Структурированный формат:

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
    - (none)

  Next: /milestone-validate (если все цепочки milestone завершены)
```

### Артефакт 2: Агент `chain-done-agent`

**Путь:** `/.claude/agents/chain-done-agent/AGENT.md`
**Действие:** Создать через `/agent-create`.

**Конфигурация:**

| Поле | Значение |
|------|---------|
| name | chain-done-agent |
| description | Завершение analysis chain (REVIEW → DONE) с обновлением docs/ |
| model | sonnet (трансформация docs/ из Planned Changes в AS IS требует понимания контекста) |
| allowed-tools | Bash, Read, Edit, Grep, Glob |
| ssot | `specs/.instructions/analysis/create-chain-done.md` |

**Промпт агента (суть):**
- Прочитать SSOT-инструкцию `create-chain-done.md`
- Получить номер цепочки {NNNN} из промпта вызова
- Выполнить алгоритм: pre-flight → T7 → обновление docs/ → cross-chain → отчёт
- При ошибке на шаге docs/ — собрать ошибки, продолжить с остальными сервисами, сообщить в отчёте
- Вернуть отчёт: что обновлено, ошибки, cross-chain alerts

**Вызов из основного LLM:**
```
Task tool → subagent_type: "general-purpose"
prompt: "Заверши analysis chain {NNNN}. Прочитай инструкцию create-chain-done.md и следуй ей."
```

### Порядок создания

| # | Артефакт | Инструмент | Зависимости |
|---|---------|------------|-------------|
| 1 | Инструкция `create-chain-done.md` | `/instruction-create` | — |
| 2 | Агент `chain-done-agent` | `/agent-create` | ← 1 |
| 3 | Обновление rule `analysis-status-transition.md` | Ручное | ← 2 |
| 4 | Обновление `analysis/README.md` | Автоматически (шаги 1, 2) | ← 1, 2 |
| 5 | Обновление `standard-process.md` §8/§10 | Ручное | ← 2 |

### Обновления существующих файлов

#### Rule `analysis-status-transition.md`

Добавить секцию:

```markdown
**Завершение цепочки (REVIEW → DONE):**
Делегировать агенту `chain-done-agent` через Task tool (SSOT: [create-chain-done.md](/specs/.instructions/analysis/create-chain-done.md)).
Перед запуском агента — проверить review.md RESOLVED + вердикт READY, подтвердить с пользователем.
```

#### `standard-process.md`

**§ 8 (таблица):** Добавить/обновить строку:

```
| 5.3 → DONE | standard-analysis §§ 6.6, 7.3, create-chain-done | — | chain-done-agent | chain_status.py |
```

**§ 10 (пробелы):** G11 → закрыт:

```
| G11 | ~~Нет `/chain-done` скилла~~ | ~~Средний~~ | Завершение через chain-done-agent (subprocess, экономит контекст) | **Закрыт** — chain-done-agent |
```

## Решения

- **Скилл `/chain-done` не создаём** — агент решает задачу экономии контекста лучше и избегает 3-4 уровней вложенности скиллов
- **Агент работает напрямую с инструментами** (Bash, Read, Edit, Grep, Glob) — без вложенных скиллов. Обновление docs/ — через Edit напрямую, не через `/service-modify`
- **Модель агента: sonnet** — трансформация Planned Changes → AS IS требует понимания контента design SVC-N
- **Одно подтверждение до запуска агента** — основной LLM подтверждает с пользователем, агент работает автономно
- **Идемпотентность всех шагов** — проверка chain-маркера в Planned Changes, безопасный перезапуск
- **Bottom-up порядок** (Plan Dev → Plan Tests → Design → Discussion) — закодирован в `chain_status.py DONE_CASCADE_ORDER`
- **Pre-flight все проверки до мутаций** — fail fast паттерн (review RESOLVED, вердикт READY, SVC-N существуют, docs/ доступны)
- **cross_chain проверка после docs/ update** — alerts в отчёте, не прерывают (DONE — финальный)
- **Dry-run через chain_status.py** — `dry_run=True` уже поддерживается, агент может использовать для preview
- **Post-DONE предложение** — основной LLM предлагает `/milestone-validate` если все цепочки milestone завершены

## Открытые вопросы

*Нет открытых вопросов.*

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Создать инструкцию create-chain-done.md
  description: >
    Драфт: .claude/drafts/2026-02-24-chain-done.md (секция "Артефакт 1")
    /instruction-create для specs/.instructions/analysis/create-chain-done.md.
    Содержание:
    - 1.1. Pre-flight проверки (4 документа REVIEW, review.md RESOLVED + READY, SVC-N, docs/)
    - 1.2. T7 переход (chain_status.py, bottom-up каскад)
    - 1.3. Обновление docs/ (Planned Changes → AS IS, Changelog, overview, conventions, infrastructure)
    - 1.4. Обновление testing.md (обычно no-op)
    - 1.5. Cross-chain проверка
    - 1.6. Отчёт (структурированный формат)
    Включить: маппинг SVC-N §§1-8 → docs/{svc}.md §§1-8, идемпотентность через chain-маркер, dry_run поддержку.
  activeForm: Создаю create-chain-done.md

TASK 2: Создать агент chain-done-agent
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-chain-done.md (секция "Артефакт 2")
    /agent-create для .claude/agents/chain-done-agent/AGENT.md.
    Конфигурация: model=sonnet, tools=Bash/Read/Edit/Grep/Glob,
    ssot=create-chain-done.md.
    Промпт: прочитать SSOT → pre-flight → T7 → docs/ update → cross-chain → отчёт.
    При ошибке docs/ — собрать, продолжить, сообщить.
  activeForm: Создаю chain-done-agent

TASK 3: Обновить rule analysis-status-transition.md
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-chain-done.md (секция "Обновления", rule)
    Добавить секцию про делегирование завершения chain-done-agent через Task tool.
    SSOT: create-chain-done.md. Подтверждение перед запуском.
  activeForm: Обновляю rule analysis-status-transition

TASK 4: Обновить analysis/README.md
  blockedBy: [1, 2]
  description: >
    Драфт: .claude/drafts/2026-02-24-chain-done.md (секция "Порядок создания", шаг 4)
    Обновить specs/.instructions/analysis/README.md:
    - Добавить ссылку на create-chain-done.md (инструкция)
    - Добавить ссылку на chain-done-agent (агент)
    README обновляется автоматически при создании артефактов, но проверить полноту.
  activeForm: Обновляю analysis/README.md

TASK 5: Обновить standard-process.md §8/§10
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-chain-done.md (секция "Обновления", standard-process)
    Обновить specs/.instructions/standard-process.md:
    - §8: обновить строку 5.3 → DONE с create-chain-done, chain-done-agent, chain_status.py
    - §10 G11: отметить как закрытый gap
  activeForm: Обновляю standard-process.md
```
