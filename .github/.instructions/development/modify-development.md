---
description: Воркфлоу процесса разработки в feature-ветке — взятие задачи, код, тестирование, коммит, переходы статусов RUNNING+ (CONFLICT, REVIEW, DONE, ROLLING_BACK, REJECTED).
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/development/README.md
---

# Воркфлоу процесса разработки

Рабочая версия стандарта: 1.3

Процесс разработки в feature-ветке: определение состояния, взятие задачи, написание кода, тестирование, завершение Issue. Используется когда ветка уже в RUNNING.

**Полезные ссылки:**
- [Инструкции development](./README.md)

**SSOT-зависимости:**
- [standard-development.md](./standard-development.md) — стандарт процесса разработки (§§ 1-9)
- [standard-analysis.md](/specs/.instructions/analysis/standard-analysis.md) — статусы цепочки, каскады (§ 6)
- [CLAUDE.md](/CLAUDE.md) — make-команды проекта
- [standard-issue.md](../issues/standard-issue.md) — формат Issue, критерии готовности
- [standard-commit.md](../commits/standard-commit.md) — формат коммитов
- [standard-principles.md](/.instructions/standard-principles.md) — принципы программирования

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-development.md](./standard-development.md) |
| Валидация | [validation-development.md](./validation-development.md) |
| Создание | [create-development.md](./create-development.md) |
| Модификация | Этот документ |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Определить состояние](#шаг-1-определить-состояние)
  - [Шаг 2: Взять задачу](#шаг-2-взять-задачу)
  - [Шаг 3: Разработка](#шаг-3-разработка)
  - [Шаг 4: Тестирование и проверки](#шаг-4-тестирование-и-проверки)
  - [Шаг 5: Завершение работы над Issue](#шаг-5-завершение-работы-над-issue)
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

> **Итеративность.** Цикл код → тест → линт → коммит повторяется для каждой задачи. Одна задача = один Issue.

> **Атомарные коммиты.** Каждый коммит — логически завершённое изменение. Формат → [standard-commit.md](../commits/standard-commit.md).

---

## Шаги

### Шаг 1: Определить состояние

**SSOT:** [standard-development.md § 0](./standard-development.md#0-запуск-разработки)

```bash
python .github/.instructions/.scripts/dev-next-issue.py
```

Скрипт автоматически определяет ветку, читает plan-dev.md, запрашивает Issues и выводит следующий незаблокированный Issue. Если скрипт недоступен — выполнить вручную:

1. Определить текущую ветку:
   ```bash
   git branch --show-current
   ```
   Имя ветки = `{NNNN}-{topic}` — номер analysis chain.

2. Прочитать plan-dev.md → получить список TASK-N:
   ```bash
   # Путь: specs/analysis/{NNNN}-{topic}/plan-dev.md
   ```

3. Получить список открытых Issues:
   ```bash
   gh issue list --milestone "{milestone}" --state open
   ```

4. Определить первый незаблокированный Issue по порядку из plan-dev.md.

---

### Шаг 2: Взять задачу

**SSOT:** [standard-development.md § 1](./standard-development.md#1-взятие-задачи)

1. Прочитать Issue:
   ```bash
   gh issue view {number} --json title,body
   ```

2. Проверить зависимости TASK-N — все блокирующие задачи должны быть закрыты.

3. Прочитать описание задачи, критерии готовности, подзадачи.

---

### Шаг 3: Разработка

**SSOT:** [standard-development.md § 2](./standard-development.md#2-процесс-разработки)

Цикл разработки:

1. **Написать код** — следовать [standard-principles.md](/.instructions/standard-principles.md)
2. **Запустить тесты** — `make test` (→ [standard-development.md § 4](./standard-development.md#4-тестирование))
3. **Запустить линтер** — `make lint` (→ [standard-development.md § 5](./standard-development.md#5-проверки-качества))
4. **Коммит** — `git commit` по [standard-commit.md](../commits/standard-commit.md)

Повторять цикл до завершения всех подзадач Issue.

**Make-команды** (→ [standard-development.md § 3](./standard-development.md#3-make-команды)):

| Команда | Когда |
|---------|-------|
| `make test` | После изменений кода |
| `make lint` | Перед коммитом |
| `make build` | Перед завершением Issue |
| `make dev` | При ошибках "connection refused" |

---

### Шаг 4: Тестирование и проверки

**SSOT:** [standard-development.md §§ 4-5](./standard-development.md#4-тестирование)

1. **Unit-тесты** — новый код покрыт тестами, `make test` проходит
2. **Линтер** — `make lint` без ERRORS, warnings исправлены в изменённых файлах
3. **Сборка** — `make build` проходит без ошибок

| Проверка | Команда | Критерий |
|----------|---------|----------|
| Тесты | `make test` | Exit code 0 |
| Линтер | `make lint` | Нет ERRORS |
| Сборка | `make build` | Exit code 0 |

---

### Шаг 5: Завершение работы над Issue

**SSOT:** [standard-development.md § 7](./standard-development.md#7-завершение-работы-над-issue)

1. Убедиться, что все подзадачи Issue выполнены
2. Убедиться, что критерии готовности Issue выполнены
3. Закрыть Issue:
   ```bash
   gh issue close {number} --comment "Реализовано в коммитах {hashes}"
   ```

4. **Следующая задача:** Вернуться к [Шаг 1](#шаг-1-определить-состояние) для следующего Issue.

5. **Все задачи завершены:** Все Issues закрыты → готово к REVIEW (→ [Переход: RUNNING → REVIEW](#переход-running-review)).

---

## Переход: RUNNING → CONFLICT

**SSOT:** [Стандарт analysis/ § 6.3](/specs/.instructions/analysis/standard-analysis.md#63-running-to-conflict)

> **Tree-level каскад.** При обнаружении CONFLICT-уровня проблемы **все** документы цепочки → CONFLICT.

**Триггер:** обратная связь от кода выявила несовместимость со спецификациями на уровне Design или выше. LLM-агент обнаруживает при написании кода, при падении тестов, или разработчик сообщает вручную.

**Через `chain_status.py`:**

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="CONFLICT")
# Модуль автоматически: все 4 документа → CONFLICT (кроме DONE/REJECTED), README dashboard
```

Выполнить побочные эффекты из `result.side_effects` (Issues остаются открытыми — работа приостановлена, не отменена).

**После перехода:** разрешение CONFLICT — через [Стандарт analysis/ § 6.4](/specs/.instructions/analysis/standard-analysis.md#64-conflict-to-waiting). Каждый документ ревьюится top-down → WAITING. Когда все 4 в WAITING → каскад RUNNING.

---

## Переход: RUNNING → REVIEW

**SSOT:** [Стандарт analysis/ § 6.5](/specs/.instructions/analysis/standard-analysis.md#65-running-to-review)

> **Tree-level переход.** Все документы цепочки переходят в REVIEW одновременно.

**Триггер:** все TASK-N из Plan Dev выполнены, все Issues закрыты. LLM предлагает через AskUserQuestion: "Разработка завершена. Перейти в REVIEW?"

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
- [ ] Plan-dev.md прочитан
- [ ] Открытые Issues получены

### Разработка (для каждого Issue)
- [ ] Issue прочитан, зависимости проверены
- [ ] Код написан по принципам программирования
- [ ] `make test` — exit code 0
- [ ] `make lint` — нет ERRORS
- [ ] `make build` — exit code 0
- [ ] Коммит создан по standard-commit.md
- [ ] Критерии готовности Issue выполнены
- [ ] Issue закрыт

### Завершение
- [ ] Все Issues ветки закрыты
- [ ] Все тесты проходят (`make test`)
- [ ] Сборка успешна (`make build`)

### Переходы статусов (chain_status.py)
- [ ] RUNNING → CONFLICT: `mgr.transition(to="CONFLICT")`, `result.side_effects` выполнены
- [ ] RUNNING → REVIEW: все Issues закрыты, проверки пройдены, `mgr.transition(to="REVIEW")`, `/review` запущен
- [ ] REVIEW → DONE: review.md RESOLVED, `mgr.transition(to="DONE")`, `result.side_effects` выполнены
- [ ] → ROLLING_BACK: `mgr.transition(to="ROLLING_BACK")`, артефакты откачены
- [ ] ROLLING_BACK → REJECTED: `mgr.transition(to="REJECTED")`, `result.side_effects` выполнены

---

## Примеры

### Полный цикл разработки Issue

```
1. git branch → 0001-auth
2. Читаю plan-dev.md → TASK-1, TASK-2, TASK-3
3. gh issue list → #42 (TASK-1), #43 (TASK-2), #44 (TASK-3)
4. gh issue view 42 → "Добавить POST /auth/token"
5. Пишу код → make test → make lint → git commit
6. gh issue close 42
7. Следующий: gh issue view 43
```

### Цикл код-тест-линт-коммит

```
1. Написать реализацию эндпоинта
2. make test → 1 failing → исправить
3. make test → pass
4. make lint → 2 warnings → исправить
5. make lint → pass
6. git commit -m "feat(auth): add POST /auth/token endpoint"
```

### Переход RUNNING → REVIEW → DONE

```
1. Все Issues закрыты → make test → make lint → make build
2. AskUserQuestion: "Все TASK-N выполнены. Перейти в REVIEW?" → Да
3. mgr.transition(to="REVIEW") → все документы → REVIEW
4. /review → code-reviewer → review.md → вердикт READY
5. mgr.transition(to="DONE") → bottom-up каскад → все документы → DONE
```

### Обнаружение CONFLICT при разработке

```
1. Пишу код → обнаруживаю несовместимость с Design (API контракт изменился)
2. mgr.transition(to="CONFLICT") → все документы → CONFLICT
3. Разрешение top-down: Discussion → Design → Plan Tests → Plan Dev → WAITING
4. Все в WAITING → каскад RUNNING → продолжить разработку
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [dev-next-issue.py](../.scripts/dev-next-issue.py) | Определение следующего незаблокированного Issue | Этот документ |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/dev](/.claude/skills/dev/SKILL.md) | Процесс разработки в feature-ветке | Этот документ |
