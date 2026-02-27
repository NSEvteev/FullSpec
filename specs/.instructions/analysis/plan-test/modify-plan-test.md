---
description: Воркфлоу изменения документа плана тестов SDD — операции по статусам и переходы жизненного цикла (DRAFT, WAITING, RUNNING, REVIEW, CONFLICT, DONE).
standard: .instructions/standard-instruction.md
standard-version: v1.4
index: specs/.instructions/README.md
---

# Воркфлоу изменения плана тестов

Рабочая версия стандарта: 1.4

Процессы изменения существующего документа плана тестов (`specs/analysis/NNNN-{topic}/plan-test.md`).

**Полезные ссылки:**
- [Стандарт плана тестов](./standard-plan-test.md)
- [Стандарт аналитического контура](../standard-analysis.md) — статусы, каскады
- [Инструкции specs/](../../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-plan-test.md](./standard-plan-test.md) |
| Валидация | [validation-plan-test.md](./validation-plan-test.md) |
| Создание | [create-plan-test.md](./create-plan-test.md) |
| Модификация | Этот документ |

## Оглавление

- [Принципы](#принципы)
- [Шаг 0: Определить статус документа](#шаг-0-определить-статус-документа)
- [Статус DRAFT — операции](#статус-draft-операции)
  - [Обновление контента](#обновление-контента)
  - [Разрешение маркеров](#разрешение-маркеров)
- [Переход: DRAFT → WAITING](#переход-draft-waiting)
  - [Условия (блокирующие)](#условия-блокирующие)
  - [Шаг 1: Подтверждение пользователя](#шаг-1-подтверждение-пользователя)
  - [Шаг 2: Обновить статус](#шаг-2-обновить-статус)
  - [Каскад DRAFT (возврат из WAITING)](#каскад-draft-возврат-из-waiting)
- [Upward feedback при WAITING](#upward-feedback-при-waiting)
- [Переход: WAITING → RUNNING](#переход-waiting-running)
- [Статус RUNNING — ограничения](#статус-running-ограничения)
- [Переход: RUNNING → CONFLICT](#переход-running-conflict)
- [Статус CONFLICT — операции](#статус-conflict-операции)
  - [Как Plan Tests попадает в CONFLICT](#как-plan-tests-попадает-в-conflict)
  - [Операции при CONFLICT](#операции-при-conflict)
- [Переход: CONFLICT → WAITING](#переход-conflict-waiting)
- [Переход: RUNNING → REVIEW](#переход-running-review)
- [Переход: REVIEW → DONE](#переход-review-done)
- [Статус DONE — ограничения](#статус-done-ограничения)
- [Переход: → ROLLING_BACK](#переход-rolling_back)
- [Переход: ROLLING_BACK → REJECTED](#переход-rolling_back-rejected)
- [Обновление ссылок](#обновление-ссылок)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Структура по статусам.** Этот документ организован по текущему статусу объекта и переходам между статусами. Статус определяет доступные операции.

> **Шаг 0 — точка входа.** Перед любым изменением определить статус документа (frontmatter → `status`), затем перейти к соответствующей секции.

> **Операции vs переходы.** Операции — изменения внутри текущего статуса. Переходы — смена статуса с условиями и шагами.

> **SSOT — Стандарт аналитического контура.** Каскады, условия переходов — [Стандарт analysis/ § 6](../standard-analysis.md#6-последовательность-статусов). Этот документ описывает операции на уровне Plan Tests.

> **Plan Tests самостоятельно управляет только DRAFT → WAITING.** При последующих переходах Plan Tests является объектом изменений, а не инициатором.

---

## Шаг 0: Определить статус документа

Прочитать frontmatter документа → поле `status`. По таблице ниже перейти к нужной секции.

| Текущий статус | Доступные операции | Доступные переходы |
|----------------|--------------------|--------------------|
| **DRAFT** | [Обновление контента](#обновление-контента), [Разрешение маркеров](#разрешение-маркеров) | [DRAFT → WAITING](#переход-draft-waiting) |
| **WAITING** | [Upward feedback](#upward-feedback-при-waiting) | [WAITING → RUNNING](#переход-waiting-running) |
| **RUNNING** | — (прямые правки запрещены) | [RUNNING → CONFLICT](#переход-running-conflict), [RUNNING → REVIEW](#переход-running-review) |
| **REVIEW** | — (прямые правки запрещены) | [REVIEW → DONE](#переход-review-done), [REVIEW → CONFLICT](#переход-running-conflict) |
| **CONFLICT** | [Операции при CONFLICT](#операции-при-conflict) | [CONFLICT → WAITING](#переход-conflict-waiting), [→ ROLLING_BACK](#переход-rolling_back) |
| **DONE** | [Только орфография](#статус-done-ограничения) | — |
| **ROLLING_BACK** | — | [ROLLING_BACK → REJECTED](#переход-rolling_back-rejected) |
| **REJECTED** | — (финальный, изменения запрещены) | — |

---

## Статус DRAFT — операции

Все операции ниже применимы **только к документам в статусе DRAFT**.

### Обновление контента

Изменение содержания разделов документа в статусе DRAFT.

#### Шаг 1: Прочитать документ

Прочитать весь документ плана тестов.

**Проверить:** статус = DRAFT. Если статус ≠ DRAFT — **СТОП**, см. [Шаг 0](#шаг-0-определить-статус-документа).

#### Шаг 2: Внести изменения

**SSOT:** [standard-plan-test.md § 5](./standard-plan-test.md#5-разделы-документа)

Допустимые изменения:

**Резюме:**
- Обновление scope, покрытия, ключевых решений

**Per-service разделы:**
- Добавление нового per-service раздела (при добавлении SVC-N в Design)
- Удаление per-service раздела (при удалении SVC-N из Design)
- Добавление/удаление/изменение TC-N в таблице Acceptance-сценариев
- Добавление/удаление/изменение fixtures в таблице Тестовых данных

**Системные тест-сценарии:**
- Добавление/удаление/изменение TC-N
- Замена контента на заглушку (или наоборот)

**Матрица покрытия:**
- Обновление трассируемости REQ-N/STS-N → TC-N

**Блоки тестирования:**
- Обновление таблицы BLOCK-N при добавлении/удалении TC-N
- Перегруппировка TC-N между блоками (синхронизация с plan-dev)

**Правила нумерации TC-N:** При добавлении — следующий номер (max + 1). При удалении — **не перенумеровывать**.

#### Шаг 3: Обновить матрицу покрытия и блоки тестирования

После изменения TC-N — **обязательно** обновить матрицу покрытия. Каждый REQ-N и STS-N должен быть покрыт.

Если TC-N добавлены или удалены — **обязательно** обновить таблицу «Блоки тестирования» (BLOCK-N). Каждый TC-N должен принадлежать ровно одному BLOCK-N.

#### Шаг 4: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-plan-test.py specs/analysis/NNNN-{topic}/plan-test.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-plan-test.md](./validation-plan-test.md).

#### Шаг 5: Обновить README

Если изменился `description` или другие отображаемые поля — обновить запись в `specs/analysis/README.md`.

#### Шаг 6: Отчёт о выполнении

```
## Отчёт об изменении плана тестов

Изменён план тестов: `specs/analysis/NNNN-{topic}/plan-test.md`

Тип изменения: Обновление

Что изменено:
- {список изменений}

Валидация: пройдена
```

### Разрешение маркеров

Замена `[ТРЕБУЕТ УТОЧНЕНИЯ]` маркеров на ответы пользователя.

#### Шаг 1: Собрать маркеры

Найти все `[ТРЕБУЕТ УТОЧНЕНИЯ: ...]` в документе.

#### Шаг 2: Уточнить у пользователя

Показать маркеры пользователю через AskUserQuestion. Для каждого маркера предложить решения.

#### Шаг 3: Заменить маркеры

Заменить каждый `[ТРЕБУЕТ УТОЧНЕНИЯ: вопрос]` на ответ пользователя.

**Dependency Barrier** ([Стандарт analysis/ § 8.3](../standard-analysis.md#83-dependency-barrier)): если в документе есть `⛔ DEPENDENCY BARRIER` — после разрешения маркеров продолжить генерацию оставшихся секций.

#### Шаг 4: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-plan-test.py specs/analysis/NNNN-{topic}/plan-test.md
```

---

## Переход: DRAFT → WAITING

**SSOT:** [standard-plan-test.md § 4](./standard-plan-test.md#4-переходы-статусов) | [Стандарт analysis/ § 6.1](../standard-analysis.md#61-draft-to-waiting)

Единственный переход, управляемый на уровне Plan Tests.

### Условия (блокирующие)

| Условие | Проверка |
|---------|----------|
| Статус = DRAFT | frontmatter `status: DRAFT` |
| Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]` | Ни одного маркера в документе |
| Нет [Dependency Barrier](../standard-analysis.md#83-dependency-barrier) | Нет `⛔ DEPENDENCY BARRIER` |
| Валидация пройдена | Скрипт validate-analysis-plan-test.py → 0 ошибок |

```bash
python specs/.instructions/.scripts/validate-analysis-plan-test.py specs/analysis/NNNN-{topic}/plan-test.md
```

**Если условия не выполнены:** сообщить пользователю — предложить разрешить маркеры или исправить ошибки.

### Шаг 1: Подтверждение пользователя

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: «План тестов готов к переводу в WAITING. Подтверждаете?»

| Ответ | Действие |
|-------|----------|
| Да | Перевести в WAITING |
| Нет | Оставить в DRAFT |

### Шаг 2: Обновить статус

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="WAITING", document="plan-test")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

**Артефакты Plan Tests → WAITING:** нет артефактов в specs/docs/. Plan Tests не создаёт Planned Changes.

### Каскад DRAFT (возврат из WAITING)

**SSOT:** [Стандарт analysis/ § 6.1](../standard-analysis.md#61-draft-to-waiting)

При возврате Plan Tests из WAITING → DRAFT — Plan Dev (если в WAITING) тоже → DRAFT.

```python
result = mgr.transition(to="DRAFT", document="plan-test")
# T2: автокаскад — дочерние WAITING-документы (plan-dev) тоже → DRAFT
```

**Когда это происходит:**
- Пользователь решил внести изменения после одобрения
- Parent Design вернулся в DRAFT (каскад сверху)

---

## Upward feedback при WAITING

**SSOT:** [standard-plan-test.md § 5 → Upward feedback](./standard-plan-test.md#5-разделы-документа), [Стандарт analysis/ § 3.5](../standard-analysis.md#35-upward-feedback)

При работе на нижестоящих уровнях (Plan Dev) LLM может обнаружить информацию, которая должна быть отражена в Plan Tests. **Статус остаётся WAITING**.

#### Шаг 1: LLM предлагает дополнение

LLM формулирует конкретное дополнение (новый TC-N, уточнение fixture) и предлагает пользователю через AskUserQuestion.

#### Шаг 2: Пользователь подтверждает

Пользователь подтверждает, корректирует или отклоняет.

#### Шаг 3: Внести изменения

Дополнить затронутые секции Plan Tests. Нумерация TC-N продолжается (max + 1). Обновить матрицу покрытия.

**Если изменение затрагивает Design:** сначала upward feedback к Design, затем обновить Plan Tests.

#### Шаг 4: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-plan-test.py specs/analysis/NNNN-{topic}/plan-test.md
```

---

## Переход: WAITING → RUNNING

**SSOT:** [Стандарт analysis/ § 6.2](../standard-analysis.md#62-waiting-to-running)

> **Tree-level.** Переход управляется на уровне цепочки, не Plan Tests.

**Триггер:** все документы цепочки (Discussion → Design → Plan Tests → Plan Dev) в WAITING. Пользователь подтверждает.

**На уровне Plan Tests:** статус `WAITING` → `RUNNING`. Операций нет.

```python
result = mgr.transition(to="RUNNING")
# Модуль автоматически: все документы цепочки → RUNNING, README dashboard
```

---

## Статус RUNNING — ограничения

> **Прямые изменения запрещены.** Plan Tests в RUNNING — согласованная спецификация. Изменения только через CONFLICT.

---

## Переход: RUNNING → CONFLICT

**SSOT:** [Стандарт analysis/ § 6.3](../standard-analysis.md#63-running-to-conflict)

> **Tree-level каскад.** При CONFLICT все документы цепочки → CONFLICT.

**Триггер:** обратная связь от кода выявила несовместимость на уровне Plan Tests или выше.

**На уровне Plan Tests:** статус `RUNNING` → `CONFLICT`.

```python
result = mgr.transition(to="CONFLICT")
# Модуль автоматически: все документы цепочки → CONFLICT, README dashboard
```

---

## Статус CONFLICT — операции

### Как Plan Tests попадает в CONFLICT

Plan Tests попадает в CONFLICT через tree-level каскад. LLM определяет самый высокий затронутый документ — снизу вверх.

### Операции при CONFLICT

**Если Plan Tests затронут** (тест-сценарии стали неверными):

1. LLM читает **весь документ** целиком
2. Сверяет с обновлённым Design (после его разрешения CONFLICT → WAITING)
3. Вносит **точечные правки** в затронутые секции:
   - Обновление TC-N (описание, тип, источник, данные)
   - Добавление/удаление TC-N
   - Обновление fixtures
   - Обновление матрицы покрытия
   - Обновление таблицы «Блоки тестирования» (BLOCK-N) — синхронизация с plan-dev
   - Обновление Резюме
4. Пользователь ревьюит → Plan Tests → WAITING

**Если Plan Tests НЕ затронут:**

1. LLM и пользователь **верифицируют** документ без изменений
2. Plan Tests → WAITING

---

## Переход: CONFLICT → WAITING

**SSOT:** [Стандарт analysis/ § 6.4](../standard-analysis.md#64-conflict-to-waiting)

> **Per-document.** Каждый документ переходит в WAITING независимо.

**Разрешение — сверху вниз:** начиная с самого высокого затронутого документа.

**Шаги:**

1. LLM исправляет документ (или верифицирует без изменений)
2. Пользователь ревьюит → одобряет
3. Обновить статус:

```python
result = mgr.transition(to="WAITING", document="plan-test")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

**Если пользователь отклоняет:**

| Исход | Переход |
|-------|---------|
| Конфликт разрешён | CONFLICT → WAITING |
| Конфликт неразрешим | → ROLLING_BACK |
| Пользователь отклоняет | → ROLLING_BACK |

---

## Переход: RUNNING → REVIEW

**SSOT:** [Стандарт analysis/ § 6.5](../standard-analysis.md#65-running-to-review)

> **Tree-level переход.** Все документы цепочки переходят в REVIEW одновременно.
> `/review-create` создаёт review.md. `/review` запускает ревью.

**На уровне Plan Tests:** статус `RUNNING` → `REVIEW`.

```python
result = mgr.transition(to="REVIEW")
# Модуль автоматически: все документы цепочки → REVIEW, README dashboard
```

---

## Переход: REVIEW → DONE

**SSOT:** [Стандарт analysis/ § 6.6](../standard-analysis.md#66-review-to-done)

> **Bottom-up каскад.** Plan Tests → DONE когда Plan Dev (child, 1:1) → DONE.

**На уровне Plan Tests:** статус `REVIEW` → `DONE` автоматически.

**Побочные эффекты Plan Tests → DONE** ([standard-plan-test.md § 4](./standard-plan-test.md#4-переходы-статусов)):

| # | Действие | SSOT |
|---|----------|------|
| 1 | `specs/docs/.system/testing.md` — обновить стратегию тестирования (если изменилась) | [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) |

```python
result = mgr.transition(to="DONE")
# Модуль автоматически: bottom-up каскад, обновляет frontmatter + README dashboard
```

---

## Статус DONE — ограничения

**SSOT:** [standard-plan-test.md § 1](./standard-plan-test.md#1-назначение) → «После DONE»

> **Plan Tests — архивная запись.** Изменения ограничены.

**Допустимые изменения:**
- Исправление орфографических ошибок, не изменяющих смысл описания, тип, источник или данные ни одного TC-N

**Любое изменение смысла TC-N** (добавление, удаление, переформулировка) → CONFLICT-цикл.

**Новый scope:** создать **новую** Discussion → Design → Plan Tests.

---

## Переход: → ROLLING_BACK

**SSOT:** [Стандарт analysis/ § 6.7](../standard-analysis.md#67-to-rolling_back)

> **Tree-level.** Все документы цепочки → ROLLING_BACK.

**Откат артефактов Plan Tests:** нет артефактов в specs/docs/ для отката (Plan Tests не создаёт Planned Changes).

```python
result = mgr.transition(to="ROLLING_BACK")
# Модуль автоматически: все 4 документа → ROLLING_BACK (кроме DONE/REJECTED), README dashboard
```

---

## Переход: ROLLING_BACK → REJECTED

**SSOT:** [Стандарт analysis/ § 6.8](../standard-analysis.md#68-rolling_back-to-rejected)

> **REJECTED — финальный статус.** Изменения запрещены.

**Условие:** LLM проверяет, что все документы цепочки в ROLLING_BACK и артефакты откачены.

```python
result = mgr.transition(to="REJECTED")
# Модуль автоматически: все документы → REJECTED, README dashboard
```

---

## Обновление ссылок

Plan Tests содержит ссылки в frontmatter (`parent`, `children`).

При изменении путей:
1. Обновить `parent` / `children` в frontmatter
2. Обновить запись в `specs/analysis/README.md`
3. Обновить children в parent Design

---

## Чек-лист

### Статус DRAFT — обновление
- [ ] Статус = DRAFT
- [ ] Изменения внесены
- [ ] Нумерация TC-N корректна (нет дублей, нет перенумерации)
- [ ] Матрица покрытия обновлена
- [ ] Блоки тестирования обновлены (если TC-N добавлены/удалены)
- [ ] Валидация пройдена
- [ ] README обновлён (если нужно)

### Разрешение маркеров
- [ ] Все маркеры собраны
- [ ] Ответы получены от пользователя
- [ ] Маркеры заменены на ответы
- [ ] Dependency Barrier разрешён (если был)
- [ ] Валидация пройдена — маркеров нет

### Upward feedback при WAITING
- [ ] Статус = WAITING
- [ ] LLM предложил дополнение
- [ ] Пользователь подтвердил
- [ ] TC-N/fixtures дополнены, нумерация продолжена
- [ ] Матрица покрытия обновлена
- [ ] Валидация пройдена
- [ ] Статус остаётся WAITING

### Переход DRAFT → WAITING
- [ ] Статус = DRAFT
- [ ] Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]`
- [ ] Нет Dependency Barrier
- [ ] Валидация пройдена — 0 ошибок
- [ ] Пользователь подтвердил перевод
- [ ] `chain_status.py` → transition(to="WAITING", document="plan-test")

### Переход CONFLICT → WAITING
- [ ] Определено: Plan Tests затронут или нет
- [ ] Если затронут — точечные правки TC-N/fixtures/матрица
- [ ] Если затронут — таблица «Блоки тестирования» обновлена (синхронизация с plan-dev)
- [ ] Если не затронут — верификация пройдена
- [ ] Пользователь одобрил
- [ ] `chain_status.py` → transition(to="WAITING", document="plan-test")

### Переход RUNNING → REVIEW
- [ ] Все TASK-N выполнены
- [ ] `chain_status.py` → transition(to="REVIEW") (tree-level)

### Переход REVIEW → DONE
- [ ] review.md RESOLVED (вердикт READY)
- [ ] specs/docs/.system/testing.md обновлён (если стратегия изменилась)
- [ ] `chain_status.py` → transition(to="DONE")

### Переход → ROLLING_BACK / REJECTED
- [ ] `chain_status.py` → transition(to="ROLLING_BACK") / transition(to="REJECTED")

---

## Примеры

### Добавление TC-N (DRAFT)

```
Пользователь: "Добавь тест на concurrent refresh в Plan Tests"

1. Прочитать specs/analysis/0001-oauth2-authorization/plan-test.md
2. Шаг 0: статус = DRAFT → секция "Статус DRAFT — операции"
3. Определить следующий номер: TC-14 → TC-15
4. Добавить TC-15 в auth → Acceptance-сценарии
5. Добавить fixture concurrent_refresh_tokens
6. Обновить матрицу покрытия: REQ-2 → TC-4, TC-5, TC-6, TC-15
7. Валидация → OK
```

### Разрешение CONFLICT

```
Ситуация: Design изменился — auth API изменён.
Вся цепочка → CONFLICT.
LLM определил: Plan Tests затронут (TC-1, TC-4 используют старый endpoint).

1. Шаг 0: статус = CONFLICT → секция "Операции при CONFLICT"
2. Сверить с обновлённым Design (уже WAITING)
3. Обновить TC-1, TC-4: новый endpoint в описании
4. Обновить fixtures: обновить поля
5. Матрица покрытия — без изменений (те же REQ-N)
6. Пользователь ревьюит → одобряет
7. chain_status.py → transition(to="WAITING", document="plan-test")
```

### Plan Tests → REVIEW → DONE

```
Ситуация: Все TASK-N выполнены → цепочка → REVIEW → review.md RESOLVED → каскад DONE.

1. chain_status.py → transition(to="REVIEW") (tree-level)
2. review.md RESOLVED → каскад DONE (bottom-up)
3. Проверить: стратегия тестирования изменилась? → Нет
4. chain_status.py → transition(to="DONE")
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-analysis-plan-test.py](../../.scripts/validate-analysis-plan-test.py) | Валидация документа (все статусы) | [validation-plan-test.md](./validation-plan-test.md) |
| [chain_status.py](../../.scripts/chain_status.py) | Переходы статусов (frontmatter + README) | [standard-analysis.md § 6](../standard-analysis.md#6-последовательность-статусов) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/plan-test-modify](/.claude/skills/plan-test-modify/SKILL.md) | Изменение документа плана тестов | Этот документ |
