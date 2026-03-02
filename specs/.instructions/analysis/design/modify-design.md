---
description: Воркфлоу изменения документа проектирования SDD — операции по статусам и переходы жизненного цикла (DRAFT, WAITING, RUNNING, REVIEW, CONFLICT, DONE).
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу изменения проектирования

Рабочая версия стандарта: 2.2

Процессы изменения существующего документа проектирования (`specs/analysis/NNNN-{topic}/design.md`).

**Полезные ссылки:**
- [Стандарт проектирования](./standard-design.md)
- [Стандарт аналитического контура](../standard-analysis.md) — статусы, каскады
- [Инструкции specs/](../../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-design.md](./standard-design.md) |
| Валидация | [validation-design.md](./validation-design.md) |
| Создание | [create-design.md](./create-design.md) |
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
  - [Как Design попадает в CONFLICT](#как-design-попадает-в-conflict)
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

> **SSOT — Стандарт аналитического контура.** Каскады, условия переходов — [Стандарт analysis/ § 6](../standard-analysis.md#6-последовательность-статусов). Этот документ описывает операции на уровне Design.

> **Design самостоятельно управляет только DRAFT → WAITING.** При последующих переходах Design является объектом изменений, а не инициатором.

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
| **DONE** | [Только typo](#статус-done-ограничения) | — |
| **ROLLING_BACK** | — (откат артефактов) | [ROLLING_BACK → REJECTED](#переход-rolling_back-rejected) |
| **REJECTED** | — (финальный, изменения запрещены) | — |

---

## Статус DRAFT — операции

Все операции ниже применимы **только к документам в статусе DRAFT**.

### Обновление контента

Изменение содержания разделов документа в статусе DRAFT.

#### Шаг 1: Прочитать документ

Прочитать весь документ проектирования.

**Проверить:** статус = DRAFT. Если статус ≠ DRAFT — **СТОП**, см. [Шаг 0](#шаг-0-определить-статус-документа).

#### Шаг 2: Внести изменения

**SSOT:** [standard-design.md § 5](./standard-design.md#5-разделы-документа)

Допустимые изменения:

**Резюме:**
- Обновление scope, ключевых решений, количества INT/STS

**SVC-N:**
- Добавление нового SVC-N (новый номер = max + 1). **Примечание:** при добавлении нового SVC-N может потребоваться пересмотр секции "Выбор технологий" — проверить нужны ли новые категории для нового сервиса
- Удаление SVC-N (номер не переиспользуется)
- Изменение подсекций §§ 1-9. **При обновлении § 5 Code Map** — проверить соответствие конвенции путей монорепо ([standard-design.md § 5, Правила путей](./standard-design.md#5-разделы-документа)): `src/{svc}/` без вложенного `src/`
- Обновление описания (1-2 абзаца)
- Изменение решения (подтверждён/изменён/добавлен)

**INT-N:**
- Добавление нового INT-N (новый номер = max + 1)
- Удаление INT-N (номер не переиспользуется, пометка `[deprecated]` если был ссылаемым)
- Изменение контракта, метаданных, sequence

**STS-N:**
- Добавление/удаление/изменение строк в таблице

**Правила нумерации:** При добавлении — следующий номер. При удалении — **не перенумеровывать**.

**При изменении SVC-N § 6 «Зависимости»:** обновить перекрёстные ссылки с INT-N.

**Перезапуск агентов:** При изменении SVC-N без изменения технологий — достаточно перезапуска design-agent-second. При изменении технологического стека — перезапуск обоих агентов (design-agent-first + design-agent-second).

#### Шаг 3: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-design.py specs/analysis/NNNN-{topic}/design.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-design.md](./validation-design.md).

#### Шаг 4: Обновить README

Если изменился `description` или другие отображаемые поля — обновить запись в `specs/analysis/README.md`.

#### Шаг 5: Отчёт о выполнении

```
## Отчёт об изменении проектирования

Изменено проектирование: `specs/analysis/NNNN-{topic}/design.md`

Тип изменения: Обновление

Что изменено:
- {список изменений}

Валидация: пройдена
```

### Разрешение маркеров

Замена `[ТРЕБУЕТ УТОЧНЕНИЯ]` маркеров на ответы пользователя.

#### Шаг 1: Собрать маркеры

Найти все `[ТРЕБУЕТ УТОЧНЕНИЯ: ...]` в документе.

```bash
python specs/.instructions/.scripts/validate-analysis-design.py specs/analysis/NNNN-{topic}/design.md
```

#### Шаг 2: Уточнить у пользователя

Показать маркеры пользователю через AskUserQuestion. Для каждого маркера предложить решения.

#### Шаг 3: Заменить маркеры

Заменить каждый `[ТРЕБУЕТ УТОЧНЕНИЯ: вопрос]` на ответ пользователя.

**Dependency Barrier** ([Стандарт analysis/ § 8.3](../standard-analysis.md#83-dependency-barrier)): если в документе есть `⛔ DEPENDENCY BARRIER` — после разрешения маркеров продолжить генерацию оставшихся секций.

#### Шаг 4: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-design.py specs/analysis/NNNN-{topic}/design.md
```

---

## Переход: DRAFT → WAITING

**SSOT:** [standard-design.md § 4](./standard-design.md#4-переходы-статусов) | [Стандарт analysis/ § 6.1](../standard-analysis.md#61-draft-to-waiting)

Единственный переход, управляемый на уровне Design.

### Условия (блокирующие)

| Условие | Проверка |
|---------|----------|
| Статус = DRAFT | frontmatter `status: DRAFT` |
| Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]` | Ни одного маркера в документе |
| Нет [Dependency Barrier](../standard-analysis.md#83-dependency-barrier) | Нет `⛔ DEPENDENCY BARRIER` |
| Валидация пройдена | Скрипт validate-analysis-design.py → 0 ошибок |

```bash
python specs/.instructions/.scripts/validate-analysis-design.py specs/analysis/NNNN-{topic}/design.md
```

**Если условия не выполнены:** сообщить пользователю — предложить разрешить маркеры или исправить ошибки.

### Шаг 1: Подтверждение пользователя

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: «Проектирование готово к переводу в WAITING. Подтверждаете?»

| Ответ | Действие |
|-------|----------|
| Да | Создать артефакты → перевести в WAITING |
| Нет | Оставить в DRAFT |

### Шаг 2: Обновить статус

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="WAITING", document="design")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

**Auto-propose:** `result.auto_propose` — предложения для следующих шагов.

> **Артефакты specs/docs/ НЕ создаются при Design → WAITING.** Они создаются на отдельном шаге `/docs-sync` после завершения аналитической цепочки. См. [create-docs-sync.md](../../create-docs-sync.md).

### Каскад DRAFT (возврат из WAITING)

**SSOT:** [Стандарт analysis/ § 6.1](../standard-analysis.md#61-draft-to-waiting)

При возврате Design из WAITING → DRAFT — Plan Tests (если в WAITING) тоже → DRAFT.

**Когда это происходит:**
- Пользователь решил внести изменения после одобрения
- Design вернулся из CONFLICT → при разрешении пользователь решил переработать
- Parent Discussion вернулась в DRAFT (каскад сверху)

```python
result = mgr.transition(to="DRAFT", document="design")
# T2: автокаскад — дочерние WAITING-документы тоже → DRAFT
```

**Артефакты при возврате в DRAFT:** Если `/docs-sync` уже выполнялся (`docs-synced: true`), артефакты specs/docs/ **остаются** (не откатываются). Маркер `docs-synced` сбрасывается — потребуется повторный `/docs-sync`.

---

## Upward feedback при WAITING

**SSOT:** [standard-design.md § 5 → Upward feedback](./standard-design.md#5-разделы-документа), [Стандарт analysis/ § 3.5](../standard-analysis.md#35-upward-feedback)

При работе на нижестоящих уровнях (Plan Tests, Plan Dev) LLM может обнаружить информацию, которая должна быть отражена в Design. **Статус остаётся WAITING**.

#### Шаг 1: LLM предлагает дополнение

LLM формулирует конкретное дополнение (новый SVC-N, уточнение контракта INT-N, расширение STS-N) и предлагает пользователю через AskUserQuestion.

#### Шаг 2: Пользователь подтверждает

Пользователь подтверждает, корректирует или отклоняет.

#### Шаг 3: Внести изменения

Дополнить затронутые секции Design. Нумерация продолжается (следующий номер = max + 1).

**Если изменение затрагивает Discussion:** сначала upward feedback к Discussion, затем обновить Design.

#### Шаг 4: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-design.py specs/analysis/NNNN-{topic}/design.md
```

---

## Переход: WAITING → RUNNING

**SSOT:** [Стандарт analysis/ § 6.2](../standard-analysis.md#62-waiting-to-running)

> **Tree-level.** Переход управляется на уровне цепочки, не Design.

**Триггер:** все документы цепочки (Discussion → Design → Plan Tests → Plan Dev) в WAITING. Пользователь подтверждает.

**На уровне Design:** статус `WAITING` → `RUNNING`. Операций нет.

```python
result = mgr.transition(to="RUNNING")
# Tree-level: все документы цепочки WAITING → RUNNING, README dashboard
```

---

## Статус RUNNING — ограничения

> **Прямые изменения запрещены.** Design в RUNNING — согласованная спецификация. Изменения только через CONFLICT.

---

## Переход: RUNNING → CONFLICT

**SSOT:** [Стандарт analysis/ § 6.3](../standard-analysis.md#63-running-to-conflict)

> **Tree-level каскад.** При CONFLICT все документы цепочки → CONFLICT.

**Триггер:** обратная связь от кода выявила несовместимость на уровне Design или выше.

**На уровне Design:** статус `RUNNING` → `CONFLICT`.

```python
result = mgr.transition(to="CONFLICT")
# Tree-level каскад: все документы цепочки → CONFLICT, README dashboard
```

---

## Статус CONFLICT — операции

### Как Design попадает в CONFLICT

Design попадает в CONFLICT через tree-level каскад. LLM определяет самый высокий затронутый документ — снизу вверх.

### Операции при CONFLICT

**Если Design затронут** (проектные решения стали неверными):

1. LLM читает **весь документ** целиком
2. Re-scan: прочитать актуальное состояние `specs/docs/{svc}.md` для затронутых сервисов (структура секций — [standard-service.md § 3](/specs/.instructions/docs/service/standard-service.md))
3. Вносит **точечные правки** в затронутые секции:
   - Обновление SVC-N подсекций (delta пересчитывается)
   - Обновление INT-N контрактов
   - Обновление STS-N
   - Обновление Резюме
4. Пользователь ревьюит → Design → WAITING

**Если Design НЕ затронут:**

1. LLM и пользователь **верифицируют** документ без изменений
2. Design → WAITING

---

## Переход: CONFLICT → WAITING

**SSOT:** [Стандарт analysis/ § 6.4](../standard-analysis.md#64-conflict-to-waiting)

> **Per-document.** Каждый документ переходит в WAITING независимо.

**Разрешение — сверху вниз:** начиная с самого высокого затронутого документа.

**Шаги:**

1. LLM исправляет документ (или верифицирует без изменений)
2. Пользователь ревьюит → одобряет
3. **Обновить артефакты:** Planned Changes в `specs/docs/{svc}.md` § 9 — пересчитать по обновлённым SVC-N
4. Обновить статус:

```python
result = mgr.transition(to="WAITING", document="design")
# Модуль автоматически: обновляет frontmatter CONFLICT → WAITING + README dashboard
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

**На уровне Design:** статус `RUNNING` → `REVIEW`.

```python
result = mgr.transition(to="REVIEW")
# Tree-level: все документы цепочки → REVIEW, README dashboard
```

---

## Переход: REVIEW → DONE

**SSOT:** [Стандарт analysis/ § 6.6](../standard-analysis.md#66-review-to-done)

> **Bottom-up каскад.** Design → DONE когда Plan Tests (child, 1:1) → DONE.

**На уровне Design:** статус `REVIEW` → `DONE` автоматически.

**Побочные эффекты Design → DONE** ([standard-design.md § 4](./standard-design.md#4-переходы-статусов)):

| # | Действие |
|---|----------|
| 1 | `specs/docs/{svc}.md` §§ 1-8: Planned Changes → AS IS (по маппингу SVC-N) |
| 2 | `specs/docs/{svc}.md` § 10: добавить запись в Changelog |
| 3 | `specs/docs/.system/overview.md`: Planned Changes → AS IS + Changelog |
| 4 | `specs/docs/.system/conventions.md`: Planned Changes → AS IS + Changelog (если были) |
| 5 | `specs/docs/.system/infrastructure.md`: Planned Changes → AS IS + Changelog (если были) |

**Механика записи §§ 1-8:** Для каждой подсекции K с контентом — **заменить** содержимое секции K в {svc}.md, убрав маркеры ADDED/MODIFIED/REMOVED. Заглушки — секция не изменяется. § 8 (таблица) конвертируется в bullet list.

**INT-N при DONE:** не записываются отдельно — уже включены в SVC-N § 2.

```python
result = mgr.transition(to="DONE")
# Bottom-up каскад: Design → DONE когда child → DONE, README dashboard
```

---

## Статус DONE — ограничения

**SSOT:** [standard-design.md § 1](./standard-design.md#1-назначение) → «После DONE»

> **Design — архивная запись.** Изменения запрещены.

**Допустимые изменения:**
- Исправление опечаток (typo corrections)
- Исправление битых ссылок

**Новый scope:** создать **новую** Discussion → Design.

---

## Переход: → ROLLING_BACK

**SSOT:** [Стандарт analysis/ § 6.7](../standard-analysis.md#67-to-rolling_back)

> **Tree-level.** Все документы цепочки → ROLLING_BACK.

**Откат артефактов:** Артефакты specs/docs/ (per-service, per-tech, overview.md) создаются `/docs-sync`, а не Design → WAITING. Откат этих артефактов выполняется в [create-rollback.md](../../create-rollback.md). При откате также сбрасывается поле `docs-synced` из frontmatter design.md.

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

Design содержит ссылки в frontmatter (`parent`, `children`) и перекрёстные ссылки (INT-N ↔ SVC-N § 6).

При изменении путей:
1. Обновить `parent` / `children` в frontmatter
2. Обновить запись в `specs/analysis/README.md`
3. Обновить children в parent Discussion

---

## Чек-лист

### Статус DRAFT — обновление
- [ ] Статус = DRAFT
- [ ] Изменения внесены
- [ ] При изменении § 5 Code Map: пути по конвенции монорепо (`src/{svc}/`, без вложенного `src/`)
- [ ] Нумерация корректна (нет дублей, нет перенумерации)
- [ ] Перекрёстные ссылки INT-N ↔ SVC-N § 6 обновлены
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
- [ ] Секции дополнены, нумерация продолжена
- [ ] Валидация пройдена
- [ ] Статус остаётся WAITING

### Переход DRAFT → WAITING
- [ ] Статус = DRAFT
- [ ] Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]`
- [ ] Нет Dependency Barrier
- [ ] Валидация пройдена — 0 ошибок
- [ ] Пользователь подтвердил перевод
- [ ] `mgr.transition(to="WAITING", document="design")` — frontmatter + README

### Переход CONFLICT → WAITING
- [ ] Определено: Design затронут или нет
- [ ] Если затронут — re-scan + точечные правки
- [ ] Если не затронут — верификация пройдена
- [ ] Пользователь одобрил
- [ ] `mgr.transition(to="WAITING", document="design")` — frontmatter + README

### Переход RUNNING → REVIEW
- [ ] Все TASK-N выполнены
- [ ] `mgr.transition(to="REVIEW")` — tree-level, frontmatter + README

### Переход REVIEW → DONE
- [ ] review.md RESOLVED (вердикт READY)
- [ ] specs/docs/{svc}.md §§ 1-8: Planned Changes → AS IS
- [ ] specs/docs/{svc}.md § 10: Changelog обновлён
- [ ] overview.md: Planned Changes → AS IS + Changelog
- [ ] § 8: таблица конвертирована в bullet list
- [ ] `mgr.transition(to="DONE")` — bottom-up каскад, frontmatter + README

### Переход → ROLLING_BACK / REJECTED
- [ ] Артефакты specs/docs/ откачены (см. [create-rollback.md](../../create-rollback.md))
- [ ] `docs-synced` сброшен из frontmatter design.md
- [ ] `mgr.transition(to="ROLLING_BACK")` / `mgr.transition(to="REJECTED")` — frontmatter + README

---

## Примеры

### Добавление SVC-N (DRAFT)

```
Пользователь: "Добавь notification-service в Design"

1. Прочитать specs/analysis/0001-oauth2-authorization/design.md
2. Шаг 0: статус = DRAFT → секция "Статус DRAFT — операции"
3. Определить следующий номер: SVC-3 → SVC-4
4. Добавить SVC-4 (notification-service) с 9 подсекциями
5. Добавить INT-5 (auth → notification-service)
6. Обновить STS: добавить STS-4
7. Обновить Резюме
8. Валидация → OK
```

### Разрешение CONFLICT

```
Ситуация: обратная связь от кода — auth API изменился.
Вся цепочка → CONFLICT.
LLM определил: Design затронут (SVC-1 § 2 API контракты).

1. Шаг 0: статус = CONFLICT → секция "Операции при CONFLICT"
2. Re-scan: прочитать актуальный auth.md
3. Обновить SVC-1 § 2: MODIFIED endpoint → пересчитать delta
4. Обновить INT-1: обновить контракт и sequence
5. Пользователь ревьюит → одобряет
6. Пересчитать Planned Changes в auth.md § 9
7. mgr.transition(to="WAITING", document="design")  # frontmatter + README
```

### Design → REVIEW → DONE

```
Ситуация: Все TASK-N выполнены → цепочка → REVIEW → review.md RESOLVED → каскад DONE.

1. mgr.transition(to="REVIEW")  # tree-level, все документы → REVIEW
2. review.md RESOLVED → каскад DONE (bottom-up)
3. Для каждого SVC-N с контентом:
   - auth.md §§ 1-8: Planned Changes → AS IS (убрать маркеры)
   - auth.md § 10: Changelog += "0001: OAuth2 авторизация"
   - gateway.md аналогично
   - users.md аналогично
4. overview.md: Planned Changes → AS IS + Changelog
5. mgr.transition(to="DONE")  # bottom-up каскад, frontmatter + README
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-analysis-design.py](../../.scripts/validate-analysis-design.py) | Валидация документа (все статусы) | [validation-design.md](./validation-design.md) |
| [chain_status.py](../../.scripts/chain_status.py) | Переходы статусов (ChainManager) | Этот документ |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/design-modify](/.claude/skills/design-modify/SKILL.md) | Изменение документа проектирования | Этот документ |
