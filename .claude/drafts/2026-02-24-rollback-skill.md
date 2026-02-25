---
description: Инструкция create-rollback.md + rollback-agent для автономного отката analysis chain
type: feature
status: ready
created: 2026-02-24
---

# Откат цепочки — инструкция + агент

Вместо скилла `/rollback`: инструкция процесса отката и rollback-agent для экономии контекста основного LLM.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** G9 из standard-process.md — нет автоматизации отката цепочки
**Почему создан:** Откат цепочки — многошаговая операция (T9, артефакты per-document, T10). Ручной вызов 4-6 команд работает, но тратит контекст основного LLM. Агент-subprocess решает это.
**Связанные файлы:**
- `specs/.instructions/analysis/standard-analysis.md` — §§ 6.7-6.8 ROLLING_BACK/REJECTED, § 7.5 обновление docs/ при откате
- `specs/.instructions/.scripts/chain_status.py` — T9, T10, side_effects
- `specs/.instructions/standard-process.md` — § 7 C.1 Rollback / Reject, § 8/§ 10
- `.claude/rules/analysis-status-transition.md` — rule для status transitions

## Содержание

### Почему не скилл

| Критерий | Скилл `/rollback` | Агент `rollback-agent` |
|----------|-------------------|------------------------|
| Контекст основного LLM | Тратит (скилл = промпт в основном контексте) | Не тратит (subprocess) |
| Чтение стандарта | Каждый раз в основном контексте | Один раз в subprocess |
| Вложенность скиллов | 3-4 уровня (rollback → modify → service-modify → ...) | 0 — агент работает напрямую с инструментами |
| Вызов | Явный `/rollback` | Автоматический через Task tool |

Агент работает **напрямую** с Bash, Read, Edit, Grep, Glob — без вложенных скиллов. Читает инструкцию `create-rollback.md` и выполняет все шаги автономно.

### Архитектура

```
standard-analysis.md §§ 6.7-6.8, 7.5   (правила — что откатывать)
       ↓ ссылается
create-rollback.md                       (инструкция — как откатывать)
       ↓ SSOT для
rollback-agent (AGENT.md)                (исполнитель — делает)
```

**Поток вызова:**

```
1. Пользователь: "откатить цепочку NNNN"
2. Основной LLM: читает chain status, показывает scope отката
3. Основной LLM: AskUserQuestion — подтверждение (деструктивная операция)
4. Основной LLM: Task tool → rollback-agent с промптом "Откати цепочку NNNN"
5. rollback-agent: читает create-rollback.md → выполняет все шаги → возвращает отчёт
6. Основной LLM: показывает отчёт пользователю
```

Подтверждение — **одно, до запуска агента**. Агент работает автономно после подтверждения. Исключение: если Design уже DONE (откат AS IS из docs/) — основной LLM предупреждает об этом **до подтверждения**.

### Артефакт 1: Инструкция `create-rollback.md`

**Путь:** `specs/.instructions/analysis/create-rollback.md`
**Действие:** Создать через `/instruction-create`.
**Тип:** воркфлоу (create-*)

Содержание инструкции — полный алгоритм отката analysis chain:

#### 1.1. Чтение состояния цепочки

1. `python chain_status.py status {NNNN}` — текущие статусы всех 4 документов
2. Определить scope: какие документы не в DONE/REJECTED (они будут откатываться)
3. Прочитать design.md — определить затронутые сервисы, технологии, метки из SVC-N секций
4. Прочитать plan-dev.md — определить TASK-N и привязанные Issues, имя ветки

#### 1.2. Переход T9 (→ ROLLING_BACK)

```python
python chain_status.py transition {NNNN} ROLLING_BACK
```

Tree-level: все не-DONE документы → ROLLING_BACK. Возвращает `side_effects` — список действий для отката.

#### 1.3. Откат Plan Dev (Issues + ветка)

**Артефакты:**
- Закрыть все Issues milestone: `gh issue close {N} --reason "not planned" --comment "Rolled back: chain {NNNN} rejected"`
- Удалить feature-ветку: `git push origin --delete {branch}` + `git branch -D {branch}` (если существует локально)

**Идемпотентность:** `gh issue close` на уже закрытом Issue — no-op. `git push origin --delete` на несуществующей ветке — ошибка, игнорировать.

#### 1.4. Откат Design (docs/, per-tech, заглушки, метки)

Основной блок — 6 типов артефактов:

| # | Артефакт | Действие | Идемпотентность |
|---|---------|----------|----------------|
| 1 | Planned Changes в `{svc}.md` § 9 | Удалить блок `<!-- chain: NNNN-{topic} -->` | Нет маркера → skip |
| 2 | Planned Changes в `overview.md` | Удалить блок `<!-- chain: NNNN-{topic} -->` | Нет маркера → skip |
| 3 | Planned Changes в `conventions.md`, `infrastructure.md` | Удалить блоки (если были) | Нет маркера → skip |
| 4 | Заглушка `{svc}.md` | Удалить файл если `created-by: {NNNN}` и нет других цепочек | Файл не существует → skip |
| 5 | Per-tech: `standard-{tech}.md`, `validation-{tech}.md`, `.claude/rules/{tech}.md`, строка в `.technologies/README.md` | Удалить файлы и строку реестра | Файл не существует → skip |
| 6 | Метка `svc:{svc}` | `gh label delete "svc:{svc}" --yes` | Метка не существует → skip |

**Design (DONE) → REJECTED — особый случай:**
Если Design уже был DONE (AS IS обновлён в docs/), откат по SVC-N секциям:
- ADDED → удалить из docs/
- MODIFIED → вернуть к предыдущему состоянию (из git history)
- REMOVED → восстановить (из git history)

Для восстановления: `git show HEAD~N:specs/docs/{file}` — найти версию до DONE-каскада.

#### 1.5. Откат Plan Tests

| Файл docs/ | Действие |
|-----------|----------|
| `.system/testing.md` | Откат изменений (если Plan Tests вносил изменения). Обычно no-op |

#### 1.6. Откат Discussion

No-op — Discussion не создаёт артефактов в docs/.

#### 1.7. Cross-chain проверка

```python
python chain_status.py check_cross_chain {NNNN}
```

Реакции (информировать в отчёте):
- Другая цепочка в DRAFT: перегенерировать затронутые документы
- Другая цепочка в WAITING: дообновить контекст
- Другая цепочка в RUNNING: → CONFLICT
- Другая цепочка в DONE: предложить новую Discussion

#### 1.8. Верификация и T10

Чек-лист перед T10 (каждый пункт — идемпотентная проверка):
- [ ] Planned Changes: `grep -r "chain: {NNNN}" specs/docs/` — пусто
- [ ] Issues: `gh issue list --milestone {milestone} --state open` — пусто
- [ ] Ветка: `git ls-remote --heads origin {branch}` — пусто
- [ ] Заглушки: `{svc}.md` с `created-by: {NNNN}` — не существуют
- [ ] Per-tech: `standard-{tech}.md` введённые этой цепочкой — не существуют

Если все пункты пройдены:

```python
python chain_status.py transition {NNNN} REJECTED
```

#### 1.9. Отчёт

Вернуть структурированный отчёт:
- Цепочка NNNN: статус → REJECTED
- Per-document: что было откачено (Issues × N закрыты, ветка удалена, Planned Changes удалены из N файлов, ...)
- Cross-chain alerts (если есть)
- Ошибки (если были, с описанием что не удалось)

### Артефакт 2: Агент `rollback-agent`

**Путь:** `/.claude/agents/rollback-agent/AGENT.md`
**Действие:** Создать через `/agent-create`.

**Конфигурация:**

| Поле | Значение |
|------|---------|
| name | rollback-agent |
| description | Откат analysis chain (ROLLING_BACK → REJECTED) |
| model | sonnet (многошаговая операция с парсингом docs/) |
| allowed-tools | Bash, Read, Edit, Grep, Glob |
| ssot | `specs/.instructions/analysis/create-rollback.md` |

**Промпт агента (суть):**
- Прочитать SSOT-инструкцию `create-rollback.md`
- Получить номер цепочки {NNNN} из промпта вызова
- Выполнить алгоритм: T9 → откат артефактов top-down → верификация → T10
- При ошибке на шаге — сообщить в отчёте, продолжить с остальными шагами (идемпотентность позволяет перезапуск)
- Вернуть отчёт: что откачено, ошибки, cross-chain alerts

**Вызов из основного LLM:**
```
Task tool → subagent_type: "general-purpose"
prompt: "Откати analysis chain {NNNN}. Прочитай инструкцию create-rollback.md и следуй ей."
```

### Порядок создания

| # | Артефакт | Инструмент | Зависимости |
|---|---------|------------|-------------|
| 1 | Инструкция `create-rollback.md` | `/instruction-create` | — |
| 2 | Агент `rollback-agent` | `/agent-create` | ← 1 |
| 3 | Обновление rule `analysis-status-transition.md` | Ручное | ← 2 |
| 4 | Обновление `analysis/README.md` | Автоматически (шаги 1, 2) | ← 1, 2 |
| 5 | Обновление `standard-process.md` §8/§10 | Ручное | ← 2 |

### Обновления существующих файлов

#### Rule `analysis-status-transition.md`

Добавить секцию:

```markdown
**Откат цепочки (ROLLING_BACK → REJECTED):**
Делегировать агенту `rollback-agent` через Task tool (SSOT: [create-rollback.md](/specs/.instructions/analysis/create-rollback.md)).
Перед запуском агента — подтвердить с пользователем (деструктивная операция).
```

#### `standard-process.md`

**§ 8 (таблица):** Добавить строку:

```
| C.1 Rollback | standard-analysis §§ 6.7-6.8, create-rollback | — | rollback-agent | chain_status.py |
```

**§ 10 (пробелы):** G9 → закрыт:

```
| G9 | ~~Нет `/rollback` скилла~~ | ~~Низкий~~ | Откат через rollback-agent (subprocess, экономит контекст) | **Закрыт** — rollback-agent |
```

## Решения

- **Скилл `/rollback` не создаём** — агент решает задачу экономии контекста лучше и избегает 3-4 уровней вложенности скиллов
- **Агент работает напрямую с инструментами** (Bash, Read, Edit, Grep, Glob) — без вложенных скиллов
- **Модель агента: sonnet** — задача многошаговая, требует парсинга docs/ и design.md
- **Одно подтверждение до запуска агента** — основной LLM подтверждает с пользователем, агент работает автономно
- **Идемпотентность всех шагов** — безопасный перезапуск при частичном откате
- **Top-down порядок** (Plan Dev → Design → Plan Tests → Discussion) — сначала внешние артефакты (Issues, ветка), затем внутренние (docs/)
- **DONE-документы не откатываются** (DONE — финальный статус). Если Design DONE — особый случай с AS IS, основной LLM предупреждает до подтверждения
- **cross_chain проверка** включена в алгоритм — alerts возвращаются в отчёте

## Открытые вопросы

*Нет открытых вопросов.*

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Создать инструкцию create-rollback.md
  description: >
    Драфт: .claude/drafts/2026-02-24-rollback-skill.md (секция "Артефакт 1")
    /instruction-create для specs/.instructions/analysis/create-rollback.md.
    Содержание:
    - 1.1. Чтение состояния цепочки (chain_status.py status)
    - 1.2. T9 переход (→ ROLLING_BACK)
    - 1.3. Откат Plan Dev (Issues close, branch delete)
    - 1.4. Откат Design (6 типов артефактов: Planned Changes, заглушки, per-tech, метки)
    - 1.5. Откат Plan Tests (testing.md, обычно no-op)
    - 1.6. Откат Discussion (no-op)
    - 1.7. Cross-chain проверка
    - 1.8. Верификация + T10 переход (→ REJECTED)
    - 1.9. Отчёт
    Включить: таблицу идемпотентности, чек-лист верификации, особый случай Design DONE.
  activeForm: Создаю create-rollback.md

TASK 2: Создать агент rollback-agent
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-rollback-skill.md (секция "Артефакт 2")
    /agent-create для .claude/agents/rollback-agent/AGENT.md.
    Конфигурация: model=sonnet, tools=Bash/Read/Edit/Grep/Glob,
    ssot=create-rollback.md.
    Промпт: прочитать SSOT → T9 → откат артефактов top-down → верификация → T10 → отчёт.
    При ошибке — сообщить в отчёте, продолжить (идемпотентность).
  activeForm: Создаю rollback-agent

TASK 3: Обновить rule analysis-status-transition.md
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-rollback-skill.md (секция "Обновления", rule)
    Добавить секцию про делегирование отката rollback-agent через Task tool.
    SSOT: create-rollback.md. Подтверждение перед запуском.
  activeForm: Обновляю rule analysis-status-transition

TASK 4: Обновить analysis/README.md
  blockedBy: [1, 2]
  description: >
    Драфт: .claude/drafts/2026-02-24-rollback-skill.md (секция "Порядок создания", шаг 4)
    Обновить specs/.instructions/analysis/README.md:
    - Добавить ссылку на create-rollback.md (инструкция)
    - Добавить ссылку на rollback-agent (агент)
    README обновляется автоматически при создании артефактов, но проверить полноту.
  activeForm: Обновляю analysis/README.md

TASK 5: Обновить standard-process.md §8/§10
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-rollback-skill.md (секция "Обновления", standard-process)
    Обновить specs/.instructions/standard-process.md:
    - §8: добавить строку C.1 Rollback с create-rollback, rollback-agent, chain_status.py
    - §10 G9: отметить как закрытый gap
  activeForm: Обновляю standard-process.md
```
