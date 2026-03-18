---
description: Воркфлоу процесса разработки в feature-ветке — блоки (BLOCK-N), волны, параллельные dev-agent, CONFLICT-детекция, переходы статусов RUNNING+ (CONFLICT, REVIEW, DONE, ROLLING_BACK, REJECTED).
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/development/README.md
---

# Воркфлоу процесса разработки

Рабочая версия стандарта: 1.3

Процесс разработки в feature-ветке: определение блоков и волн, запуск dev-agent для каждого блока, сбор результатов, обработка CONFLICT. Используется когда ветка уже в RUNNING.

**Полезные ссылки:**
- [Инструкции development](./README.md)

**SSOT-зависимости:**
- [standard-development.md](./standard-development.md) — стандарт процесса разработки (§§ 1-9)
- [standard-analysis.md](/specs/.instructions/analysis/standard-analysis.md) — статусы цепочки, каскады (§ 6)
- [CLAUDE.md](/CLAUDE.md) — make-команды проекта
- [standard-issue.md](../issues/standard-issue.md) — формат Issue, критерии готовности
- [standard-commit.md](../commits/standard-commit.md) — формат коммитов
- [standard-principles.md](/.instructions/standard-principles.md) — принципы программирования
- [dev-agent](/.claude/agents/dev-agent/AGENT.md) — агент разработки (выполняет BLOCK-N)
- [docker-agent](/.claude/agents/docker-agent/AGENT.md) — Docker-операции (mode=update, вызывается по сигналу DOCKER_UPDATES)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-development.md](./standard-development.md) |
| Валидация | [validation-development.md](./validation-development.md) |
| Создание | [create-development.md](./create-development.md) |
| Модификация | Этот документ |

## Оглавление

- [Принципы](#принципы)
- [Модель выполнения](#модель-выполнения)
- [Шаги](#шаги)
  - [Шаг 1: Определить блоки и волны](#шаг-1-определить-блоки-и-волны)
  - [Шаг 2: Запустить волну](#шаг-2-запустить-волну)
  - [Шаг 3: Собрать результаты](#шаг-3-собрать-результаты)
  - [Шаг 4: Следующая волна или REVIEW](#шаг-4-следующая-волна-или-review)
  - [Fix-итерация после review](#fix-итерация-после-review)
- [Переход: RUNNING → CONFLICT](#переход-running-conflict)
- [Переход: RUNNING → REVIEW](#переход-running-review)
- [Переход: REVIEW → DONE](#переход-review-done)
- [Переход: → ROLLING_BACK](#переход-rolling_back)
- [Переход: ROLLING_BACK → REJECTED](#переход-rolling_back-rejected)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **SSOT — standard-development.md.** Детали каждого шага — в стандарте. Этот документ описывает порядок выполнения, не дублируя правила.

> **Блочная параллельная модель.** Задачи (TASK-N) группируются в блоки (BLOCK-N) по 1-2 задачи (макс 3), блоки распределяются по волнам. Каждый блок выполняется отдельным dev-agent.

> **CONFLICT → остановить всех.** При обнаружении CONFLICT любым агентом — остановить все запущенные агенты, собрать частичные результаты, разрешить CONFLICT, перезапустить.

> **Двухуровневое тестирование.** Агент запускает per-service тесты (`make test-{svc}`). Main LLM запускает системные тесты (`make test-e2e`) после волны.

> **Один агент = один сервис. Без исключений.** Каждый dev-agent работает ТОЛЬКО с файлами одного сервиса (src/{svc}/, shared/{pkg}/, tests/ данного сервиса). ЗАПРЕЩЕНО объединять задачи или исправления нескольких сервисов в одного агента — включая fix-итерации после review. При fix-итерации: N замечаний для M сервисов = M параллельных агентов (по одному на сервис). Нарушение этого принципа приводит к: (1) потере изоляции — ошибка в одном сервисе блокирует все, (2) конфликтам при параллельной работе с другими агентами, (3) увеличению времени вместо сокращения.

---

## Модель выполнения

```
plan-dev.md → Блоки выполнения (1-2 TASK-N каждый) → Волны
                                    │
                        ┌───────────┼───────────┐
                   Wave 0      Wave 1       Wave 2
                   BLOCK-1     BLOCK-3      BLOCK-6
                   BLOCK-2     BLOCK-4      BLOCK-7
                               BLOCK-5
                                    │
                            dev-agent × N (параллельно)
                                    │
                            Сбор результатов
                                    │
                   ┌────────────────┼────────────────┐
              Все COMPLETED     CONFLICT          PARTIAL
                   │               │                  │
           Следующая волна    TaskStop всех    Перезапуск блока
```

**Участники:**

| Роль | Ответственность |
|------|----------------|
| Main LLM | Парсинг блоков и волн, запуск/остановка агентов, системные тесты, переходы статусов |
| Dev-agent | Выполнение BLOCK-N из 1-2 Issues (код → test → lint → commit → CONFLICT-CHECK → close Issue), отчёт |

---

## Шаги

### Шаг 1: Определить блоки и волны

**SSOT:** [standard-development.md § 0](./standard-development.md#0-запуск-разработки)

1. Определить текущую ветку:
   ```bash
   git branch --show-current
   ```
   Имя ветки = `{NNNN}-{topic}` — номер analysis chain.

2. Прочитать plan-dev.md → секция "Блоки выполнения":
   ```bash
   # Путь: specs/analysis/{NNNN}-{topic}/plan-dev.md
   ```

3. Парсить таблицу блоков:

   | BLOCK | Задачи | Сервисы | Зависимости | Wave |
   |-------|--------|---------|-------------|------|
   | BLOCK-1 | TASK-1, TASK-2 | auth | — | 0 |
   | BLOCK-2 | TASK-3 | notification | BLOCK-1 | 1 |
   | BLOCK-3 | TASK-4, TASK-5 | payment | BLOCK-1 | 1 |
   | BLOCK-4 | TASK-6 | auth, notification | BLOCK-2, BLOCK-3 | 2 |

4. Определить текущую волну: первая волна, все блоки которой ещё не завершены.

5. Получить Issues каждого блока:
   ```bash
   gh issue list --milestone "{milestone}" --state open --json number,title
   ```

---

### Шаг 2: Запустить волну

Для каждого блока текущей волны — запустить dev-agent через Task tool **параллельно** (один вызов с множественными Tool Use).

**Формат запуска:**

```
Task(
  subagent_type="dev-agent",
  description="BLOCK-{N}: {сервисы}",
  prompt="""
    BLOCK: BLOCK-{N}
    ISSUES: [#{issue1}, #{issue2}, ...]
    SERVICES: [{svc1}, {svc2}]

    Контекст:
    - plan-dev: specs/analysis/{NNNN}-{topic}/plan-dev.md
    - plan-test: specs/analysis/{NNNN}-{topic}/plan-test.md
    - design: specs/analysis/{NNNN}-{topic}/design.md
    - docs: specs/docs/{svc}.md (для каждого сервиса)
    - conventions: specs/docs/.system/conventions.md
  """
)
```

**При partial resume** (после CONFLICT или PARTIAL):

```
Task(
  subagent_type="dev-agent",
  prompt="""
    BLOCK: BLOCK-{N}
    ISSUES: [#{issue1}, #{issue2}, #{issue3}]
    REMAINING_ISSUES: [#{issue3}]
    SERVICES: [{svc1}]
    ...
  """
)
```

Main LLM определяет REMAINING_ISSUES:
```bash
gh issue list --milestone "{milestone}" --state closed --json number --jq '.[].number'
```

**Правила запуска:**
- Все блоки одной волны запускаются параллельно (один message с множественными Task tool calls)
- Блок запускается только если все его зависимости (blockedBy) завершены
- INFRA-блоки (wave 0) запускаются первыми

---

### Шаг 3: Собрать результаты

Дождаться завершения всех агентов волны. Для каждого агента прочитать отчёт:

**Если любой STATUS=CONFLICT:**

1. Остановить все ещё работающие агенты: `TaskStop(agent_id)`
2. Собрать частичные результаты из всех агентов (COMPLETED_ISSUES, REMAINING_ISSUES)
3. Перейти к [Переход: RUNNING → CONFLICT](#переход-running-conflict)

**Если любой STATUS=PAUSED:**

1. Прочитать DOCKER_UPDATES из отчёта
2. Для каждого action вызвать docker-agent mode=update:
   ```
   Agent tool:
     subagent_type: docker-agent
     prompt: |
       mode: update
       service: {svc}
       action: {action}
       details: {параметры из DOCKER_UPDATES}
   ```
3. Resume dev-agent по agent ID (Agent tool с параметром `resume`)
4. Повторить цикл — dev-agent может снова вернуть PAUSED

**Если любой STATUS=PARTIAL:**

1. Записать REMAINING_ISSUES
2. Перезапустить блок с REMAINING_ISSUES (Шаг 2)

**Если все STATUS=COMPLETED:**

1. Если DOCKER_UPDATES непуст в любом отчёте → вызвать docker-agent mode=update для каждого action

1. Проверить FLAGS всех агентов — есть ли рабочие правки, влияющие на следующие волны
2. Запустить системные тесты:
   ```bash
   make test-e2e
   ```
3. Если системные тесты прошли → перейти к Шаг 4
4. Если системные тесты упали → диагностировать, исправить, повторить

---

### Шаг 4: Следующая волна или REVIEW

1. Если есть следующая волна → вернуться к [Шаг 2](#шаг-2-запустить-волну)

2. Если все волны завершены:
   a. Все Issues закрыты
   b. Системные тесты пройдены
   c. Перейти к [Переход: RUNNING → REVIEW](#переход-running-review)

---

### Fix-итерация после review

При вердикте NOT READY code-reviewer возвращает замечания RV-N с приоритетами P1/P2/P3. Исправления выполняются параллельными dev-agent — **по одному на сервис**.

**Алгоритм:**

1. Сгруппировать замечания RV-N по сервисам:
   ```
   data-store: RV-1 (P1), RV-3 (P2), RV-4 (P2)
   market-timer: RV-1 (P2), RV-2 (P2)
   trading-calendar: RV-1 (P2)
   admin-frontend: RV-2 (P2)
   system-tests: RV-5 (P3), RV-6 (P3)
   ```

2. Запустить dev-agent × M параллельно (один message, M = количество затронутых сервисов):
   ```
   Agent(subagent_type="dev-agent", prompt="FIX-ITERATION: data-store\nЗамечания: RV-1 (P1): ..., RV-3 (P2): ..., RV-4 (P2): ...")
   Agent(subagent_type="dev-agent", prompt="FIX-ITERATION: market-timer\nЗамечания: RV-1 (P2): ..., RV-2 (P2): ...")
   Agent(subagent_type="dev-agent", prompt="FIX-ITERATION: trading-calendar\nЗамечания: RV-1 (P2): ...")
   Agent(subagent_type="dev-agent", prompt="FIX-ITERATION: admin-frontend\nЗамечания: RV-2 (P2): ...")
   Agent(subagent_type="dev-agent", prompt="FIX-ITERATION: system-tests\nЗамечания: RV-5 (P3): ..., RV-6 (P3): ...")
   ```

3. Дождаться завершения ВСЕХ агентов
4. **ОБЯЗАТЕЛЬНО** запустить повторный `/review` (итерация N+1 в review.md)
5. Если повторный review → READY → переход к PR
6. Если повторный review → NOT READY → вернуться к шагу 1 (новая fix-итерация)
7. Максимум 3 итерации fix-review. После 3-й — эскалация пользователю

**Цикл fix-review ОБЯЗАТЕЛЕН.** После fix-итерации ЗАПРЕЩЕНО переходить к PR/merge без повторного `/review`. Исправления могут быть некорректными, неполными или внести новые дефекты. Только code-reviewer подтверждает что замечания устранены (RESOLVED) и новых нет.

```
review (итерация 1) → NOT READY (P1/P2/P3)
  → fix per-service agents (параллельно)
  → review (итерация 2) → NOT READY (оставшиеся P2)
    → fix per-service agents
    → review (итерация 3) → READY
      → PR
```

**ЗАПРЕЩЕНО:**
- Объединять замечания нескольких сервисов в одного агента (даже "для скорости")
- Исправлять замечания напрямую без dev-agent — оркестратор НЕ пишет код
- Пропускать повторный `/review` после fix-итерации — переходить к PR без подтверждения READY
- Пропускать P3 замечания без явного решения пользователя (wontfix)
- Запускать fix-агенты последовательно, если они могут работать параллельно

**Почему per-service обязательно:**
- **Изоляция:** агент data-store не может сломать market-timer и наоборот
- **Параллельность:** M агентов × T мин << 1 агент × (M × T) мин
- **Blast radius:** ошибка одного агента не блокирует остальных
- **Git:** каждый агент коммитит свои файлы, нет merge-конфликтов между агентами

**Почему повторный review обязателен:**
- Fix-агент может исправить одно замечание и сломать другое
- Агент может не полностью исправить замечание (частичный fix)
- Новый код может содержать новые P1/P2 дефекты
- Без повторного review вердикт остаётся NOT READY — PR с NOT READY запрещён

---

## Переход: RUNNING → CONFLICT

**SSOT:** [Стандарт analysis/ § 6.3](/specs/.instructions/analysis/standard-analysis.md#63-running-to-conflict)

> **Tree-level каскад.** При обнаружении CONFLICT-уровня проблемы **все** документы цепочки → CONFLICT.

**Триггер:** dev-agent вернул STATUS=CONFLICT (CONFLICT-CHECK обнаружил несовместимость с границами автономии LLM).

**Шаги:**

1. Остановить все работающие агенты текущей волны (`TaskStop`)
2. Собрать частичные результаты из всех агентов
3. AskUserQuestion: "CONFLICT обнаружен: {description}. Разрешить?"
4. Через `chain_status.py`:

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="CONFLICT")
# Модуль автоматически: все 4 документа → CONFLICT (кроме DONE/REJECTED), README dashboard
```

5. Выполнить побочные эффекты из `result.side_effects` (Issues остаются открытыми — работа приостановлена, не отменена)

**После перехода:** разрешение CONFLICT — через [Стандарт analysis/ § 6.4](/specs/.instructions/analysis/standard-analysis.md#64-conflict-to-waiting). Каждый документ ревьюится top-down → WAITING. Когда все 4 в WAITING → каскад RUNNING. После перехода в RUNNING — пересобрать блоки (BLOCK-N могли измениться) и перезапустить незавершённые блоки.

---

## Переход: RUNNING → REVIEW

**SSOT:** [Стандарт analysis/ § 6.5](/specs/.instructions/analysis/standard-analysis.md#65-running-to-review)

> **Tree-level переход.** Все документы цепочки переходят в REVIEW одновременно.

**Триггер:** все волны завершены, все Issues закрыты, системные тесты пройдены. LLM предлагает через AskUserQuestion: "Разработка завершена. Перейти в REVIEW?"

**Шаги:**

1. Убедиться, что все Issues ветки закрыты
2. Убедиться, что все проверки пройдены (`make test`, `make lint`, `make build`)
3. **БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Все TASK-N выполнены. Перейти в REVIEW?"
4. Через `chain_status.py`:

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="REVIEW")
# Модуль автоматически: все 4 документа → REVIEW, README dashboard
```

5. Выполнить побочные эффекты из `result.side_effects`
6. Запустить `/review` для code review

**Вердикты review.md:**

| Вердикт | Переход |
|---------|---------|
| READY | → DONE ([Переход: REVIEW → DONE](#переход-review-done)) |
| NOT READY | Остаётся REVIEW — правки кода → повторный `/review` |
| CONFLICT | → CONFLICT ([Переход: RUNNING → CONFLICT](#переход-running-conflict)) |

---

## Переход: REVIEW → DONE

**SSOT:** [Стандарт analysis/ § 6.6](/specs/.instructions/analysis/standard-analysis.md#66-review-to-done)

> **Bottom-up каскад.** Plan Dev → Plan Tests → Design → Discussion.

**Триггер:** review.md RESOLVED (вердикт READY).

**Через `chain_status.py`:**

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="DONE")
# Модуль автоматически: bottom-up каскад plan-dev → plan-test → design → discussion, README dashboard
```

Выполнить побочные эффекты из `result.side_effects` (обновление docs/ при Design → DONE, кросс-цепочечная проверка).

**После перехода:** цепочка завершена. Спецификации — архивная запись реализованного решения.

---

## Переход: → ROLLING_BACK

**SSOT:** [Стандарт analysis/ § 6.7](/specs/.instructions/analysis/standard-analysis.md#67-to-rolling_back)

> **Tree-level.** Все документы цепочки → ROLLING_BACK (кроме DONE).

**Триггеры:**
- Пользователь даёт команду на откат
- Конфликт неразрешим ([Стандарт analysis/ § 6.4](/specs/.instructions/analysis/standard-analysis.md#64-conflict-to-waiting))
- Пользователь отклоняет разрешение конфликта

**Через `chain_status.py`:**

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="ROLLING_BACK")
# Модуль автоматически: все 4 документа → ROLLING_BACK (кроме DONE/REJECTED), README dashboard
```

Выполнить побочные эффекты из `result.side_effects` (откат артефактов per-document).

---

## Переход: ROLLING_BACK → REJECTED

**SSOT:** [Стандарт analysis/ § 6.8](/specs/.instructions/analysis/standard-analysis.md#68-rolling_back-to-rejected)

> **REJECTED — финальный статус.** Изменения запрещены.

**Условие:** все документы цепочки в ROLLING_BACK и артефакты каждого уровня откачены.

**Через `chain_status.py`:**

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="REJECTED")
# Модуль автоматически: все документы → REJECTED, README dashboard
```

Выполнить побочные эффекты из `result.side_effects`.

**Перезапуск:** если бизнес-потребность остаётся актуальной, создать новую Discussion.

---

## Чек-лист

### Подготовка
- [ ] Ветка определена (`git branch --show-current`)
- [ ] Plan-dev.md прочитан → секция "Блоки выполнения"
- [ ] Блоки и волны определены
- [ ] Issues для каждого блока получены

### Волна (для каждой волны)
- [ ] Все блоки волны запущены параллельно (dev-agent × N)
- [ ] Все агенты вернули результат
- [ ] PAUSED обработан (если был): docker-agent mode=update → resume dev-agent
- [ ] DOCKER_UPDATES из COMPLETED обработаны (если непусты)
- [ ] CONFLICT обработан (если был)
- [ ] Системные тесты пройдены (`make test-e2e`)
- [ ] FLAGS проверены (рабочие правки)

### Fix-итерация (если review NOT READY)
- [ ] Замечания сгруппированы по сервисам
- [ ] Агенты запущены per-service (один агент = один сервис)
- [ ] НЕ объединены замечания нескольких сервисов в одного агента
- [ ] После fix-итерации: повторный `/review` запущен (итерация N+1)
- [ ] Повторный review: вердикт READY получен ДО перехода к PR
- [ ] Итераций fix-review <= 3 (иначе эскалация пользователю)

### Завершение
- [ ] Все волны завершены
- [ ] Все Issues ветки закрыты
- [ ] Все тесты проходят (`make test`, `make test-e2e`)
- [ ] Сборка успешна (`make build`)

### Переходы статусов (chain_status.py)
- [ ] RUNNING → CONFLICT: все агенты остановлены, `mgr.transition(to="CONFLICT")`, `result.side_effects` выполнены
- [ ] RUNNING → REVIEW: все Issues закрыты, проверки пройдены, `mgr.transition(to="REVIEW")`, `/review` запущен
- [ ] REVIEW → DONE: review.md RESOLVED, `mgr.transition(to="DONE")`, `result.side_effects` выполнены
- [ ] → ROLLING_BACK: `mgr.transition(to="ROLLING_BACK")`, артефакты откачены
- [ ] ROLLING_BACK → REJECTED: `mgr.transition(to="REJECTED")`, `result.side_effects` выполнены

---

## Примеры

### Полный цикл с двумя волнами

```
1. git branch → 0001-auth
2. Читаю plan-dev.md → "Блоки выполнения":
   BLOCK-1 (auth) → Wave 0
   BLOCK-2 (notification) → Wave 1, blockedBy BLOCK-1

3. Wave 0: запускаю dev-agent для BLOCK-1
   Task(subagent_type="dev-agent", prompt="BLOCK: BLOCK-1, ISSUES: [#42, #43], SERVICES: [auth]")
   → STATUS: COMPLETED, COMPLETED_ISSUES: [#42, #43]

4. make test-e2e → pass

5. Wave 1: запускаю dev-agent для BLOCK-2
   Task(subagent_type="dev-agent", prompt="BLOCK: BLOCK-2, ISSUES: [#44], SERVICES: [notification]")
   → STATUS: COMPLETED, COMPLETED_ISSUES: [#44]

6. make test-e2e → pass

7. Все волны завершены → AskUserQuestion: "Перейти в REVIEW?" → Да
8. mgr.transition(to="REVIEW") → /review → READY → mgr.transition(to="DONE")
```

### Параллельная волна с CONFLICT

```
1. Wave 1: запускаю 2 агента параллельно:
   Task(subagent_type="dev-agent", prompt="BLOCK-2, ISSUES: [#44], SERVICES: [notification]")
   Task(subagent_type="dev-agent", prompt="BLOCK-3, ISSUES: [#45, #46], SERVICES: [payment]")

2. BLOCK-2 → STATUS: CONFLICT
   CONFLICT_INFO: level=design, affected_doc="SVC-1 (auth)",
   description="API контракт POST /auth/token изменился"

3. TaskStop(BLOCK-3 agent_id) → собираю partial result

4. AskUserQuestion: "CONFLICT обнаружен: API контракт изменился. Разрешить?"
5. mgr.transition(to="CONFLICT")
6. Разрешение top-down → WAITING → RUNNING
7. Пересобрать блоки, перезапустить незавершённые
```

### Partial resume после CONFLICT

```
1. BLOCK-2 выполнил #44, CONFLICT на #45
   COMPLETED_ISSUES: [#44], REMAINING_ISSUES: [#45]

2. После разрешения CONFLICT:
   gh issue list --state closed → [#42, #43, #44] (уже закрыты)

3. Перезапуск BLOCK-2:
   Task(subagent_type="dev-agent", prompt="BLOCK: BLOCK-2, ISSUES: [#44, #45],
     REMAINING_ISSUES: [#45], SERVICES: [notification]")
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [dev-next-issue.py](../.scripts/dev-next-issue.py) | Определение следующего незаблокированного Issue (используется dev-agent внутри блока) | Этот документ |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [dev-agent](/.claude/agents/dev-agent/AGENT.md) | Агент разработки (выполняет BLOCK-N) | Этот документ |
