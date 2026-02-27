---
description: Воркфлоу изменения документа дискуссии SDD — операции по статусам и переходы жизненного цикла (DRAFT, WAITING, RUNNING, REVIEW, CONFLICT, DONE).
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу изменения дискуссии

Рабочая версия стандарта: 1.1

Процессы изменения существующего документа дискуссии (`specs/analysis/NNNN-{topic}/discussion.md`).

**Полезные ссылки:**
- [Стандарт дискуссий](./standard-discussion.md)
- [Стандарт аналитического контура](../standard-analysis.md) — статусы, каскады
- [Инструкции specs/](../../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-discussion.md](./standard-discussion.md) |
| Валидация | [validation-discussion.md](./validation-discussion.md) |
| Создание | [create-discussion.md](./create-discussion.md) |
| Модификация | Этот документ |

## Оглавление

- [Принципы](#принципы)
- [Шаг 0: Определить статус документа](#шаг-0-определить-статус-документа)
- [Статус DRAFT — операции](#статус-draft-операции)
  - [Обновление контента](#обновление-контента)
  - [Разрешение маркеров](#разрешение-маркеров)
  - [Принятие предложений (PROP-N)](#принятие-предложений-prop-n)
- [Переход: DRAFT → WAITING](#переход-draft-waiting)
  - [Условия (блокирующие)](#условия-блокирующие)
  - [Шаг 1: Подтверждение пользователя](#шаг-1-подтверждение-пользователя)
  - [Шаг 2: Обновить статус](#шаг-2-обновить-статус)
  - [Шаг 3: Обновить README](#шаг-3-обновить-readme)
  - [Каскад DRAFT (возврат из WAITING)](#каскад-draft-возврат-из-waiting)
- [Upward feedback при WAITING](#upward-feedback-при-waiting)
- [Переход: WAITING → RUNNING](#переход-waiting-running)
- [Статус RUNNING — ограничения](#статус-running-ограничения)
- [Переход: RUNNING → CONFLICT](#переход-running-conflict)
- [Статус CONFLICT — операции](#статус-conflict-операции)
  - [Как Discussion попадает в CONFLICT](#как-discussion-попадает-в-conflict)
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

> **Структура по статусам.** Этот документ организован по текущему статусу объекта и переходам между статусами, а не по типам изменений. Статус определяет доступные операции.

> **Шаг 0 — точка входа.** Перед любым изменением определить статус документа (frontmatter → `status`), затем перейти к соответствующей секции.

> **Операции vs переходы.** Операции — изменения внутри текущего статуса. Переходы — смена статуса с условиями и шагами. Документ разделяет их явно.

> **SSOT — Стандарт аналитического контура.** Каскады, условия переходов, уровни обратной связи — [Стандарт analysis/ § 6](../standard-analysis.md#6-последовательность-статусов). Этот документ описывает операции на уровне Discussion, а не дублирует правила каскадов.

---

## Шаг 0: Определить статус документа

Прочитать frontmatter документа → поле `status`. По таблице ниже перейти к нужной секции.

| Текущий статус | Доступные операции | Доступные переходы |
|----------------|--------------------|--------------------|
| **DRAFT** | [Обновление контента](#обновление-контента), [Разрешение маркеров](#разрешение-маркеров), [Принятие предложений](#принятие-предложений-prop-n) | [DRAFT → WAITING](#переход-draft-waiting) |
| **WAITING** | [Upward feedback](#upward-feedback-при-waiting) | [WAITING → RUNNING](#переход-waiting-running) |
| **RUNNING** | — (прямые правки запрещены) | [RUNNING → CONFLICT](#переход-running-conflict), [RUNNING → REVIEW](#переход-running-review) |
| **REVIEW** | — (прямые правки запрещены) | [REVIEW → DONE](#переход-review-done), [REVIEW → CONFLICT](#переход-running-conflict) |
| **CONFLICT** | [Операции при CONFLICT](#операции-при-conflict) | [CONFLICT → WAITING](#переход-conflict-waiting), [→ ROLLING_BACK](#переход-rolling_back) |
| **DONE** | [Только typo](#статус-done-ограничения) | — |
| **ROLLING_BACK** | — (no-op) | [ROLLING_BACK → REJECTED](#переход-rolling_back-rejected) |
| **REJECTED** | — (финальный, изменения запрещены) | — |

---

## Статус DRAFT — операции

Все операции ниже применимы **только к документам в статусе DRAFT**.

### Обновление контента

Изменение содержания разделов документа в статусе DRAFT.

#### Шаг 1: Прочитать документ

Прочитать весь документ дискуссии.

**Проверить:** статус = DRAFT. Если статус ≠ DRAFT — **СТОП**, см. [Шаг 0](#шаг-0-определить-статус-документа).

#### Шаг 2: Внести изменения

**SSOT:** [standard-discussion.md § 5](./standard-discussion.md#5-разделы-документа)

Допустимые изменения:
- Добавление/изменение фич (F-N) — новый номер = max + 1
- Добавление/изменение User Stories (US-N)
- Добавление/изменение требований (REQ-N) — формат естественных предложений
- Добавление предложений (PROP-N) — с указанием "Влияет на"
- Прямое редактирование фич, User Stories, требований
- Изменение критериев успеха
- Изменение "Проблема / Контекст"
- Обновление frontmatter (description, milestone)

**Правила нумерации:** При добавлении — следующий номер. При удалении — **не перенумеровывать**.

#### Шаг 3: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-discussion.py specs/analysis/NNNN-{topic}/discussion.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-discussion.md](./validation-discussion.md).

#### Шаг 4: Обновить README

Если изменился `description` или другие отображаемые поля — обновить запись в `specs/analysis/README.md`.

#### Шаг 5: Отчёт о выполнении

```
## Отчёт об изменении дискуссии

Изменена дискуссия: `specs/analysis/NNNN-{topic}/discussion.md`

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
python specs/.instructions/.scripts/validate-analysis-discussion.py specs/analysis/NNNN-{topic}/discussion.md
```

Скрипт покажет количество неразрешённых маркеров (если есть).

#### Шаг 2: Уточнить у пользователя

Показать маркеры пользователю через AskUserQuestion. Для каждого маркера предложить несколько решений, включая рекомендацию, и получить ответ от пользователя.

#### Шаг 3: Заменить маркеры

Заменить каждый `[ТРЕБУЕТ УТОЧНЕНИЯ: вопрос]` на ответ пользователя.

**Dependency Barrier** ([Стандарт analysis/ § 8.3](../standard-analysis.md#83-dependency-barrier)): при создании документа LLM может остановить генерацию блоком `⛔ DEPENDENCY BARRIER`, если следующая секция зависит от неразрешённого маркера. Если в документе есть такой блок — после разрешения маркеров продолжить генерацию оставшихся секций.

#### Шаг 4: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-discussion.py specs/analysis/NNNN-{topic}/discussion.md
```

Проверить: маркеров не осталось.

### Принятие предложений (PROP-N)

**SSOT:** [standard-discussion.md § 5](./standard-discussion.md#5-разделы-документа) → механика итеративного уточнения.

Применение одобренного PROP-N к секциям документа.

#### Шаг 1: Идентифицировать PROP-N

Прочитать предложение. Определить затронутые элементы по строке "Влияет на: ...".

#### Шаг 2: Подтверждение пользователя

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Принять PROP-N: {описание}? Затронутые элементы: {список}"

#### Шаг 3: Обновить затронутые секции

На основе "Влияет на" обновить:
- Секцию "Фичи" — изменить/добавить/удалить F-N
- Секцию "User Stories" — изменить/добавить/удалить US-N
- Секцию "Критерии успеха" — если затронуты

**Правила:** При удалении элемента — **не перенумеровывать** остальные. История — через git.

#### Шаг 4: Пакетная обработка

После того как пользователь принял/отклонил **ВСЕ** PROP в секции — LLM удаляет все записи PROP (независимо от решения) и заменяет секцию заглушкой: _Все предложения обработаны._

#### Шаг 5: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-discussion.py specs/analysis/NNNN-{topic}/discussion.md
```

---

## Переход: DRAFT → WAITING

**SSOT:** [standard-discussion.md § 4](./standard-discussion.md#4-переходы-статусов) | [Стандарт analysis/ § 6.1](../standard-analysis.md#61-draft-to-waiting)

Единственный переход, управляемый на уровне Discussion. Все последующие переходы — на уровне цепочки.

### Условия (блокирующие)

Все условия должны быть выполнены:

| Условие | Проверка |
|---------|----------|
| Статус = DRAFT | frontmatter `status: DRAFT` |
| Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]` | Ни одного маркера в документе |
| Нет [Dependency Barrier](../standard-analysis.md#83-dependency-barrier) | Нет `⛔ DEPENDENCY BARRIER` |
| Валидация пройдена | Скрипт validate-analysis-discussion.py → 0 ошибок |

```bash
python specs/.instructions/.scripts/validate-analysis-discussion.py specs/analysis/NNNN-{topic}/discussion.md
```

**Если условия не выполнены:** сообщить пользователю какие — предложить разрешить маркеры или исправить ошибки.

### Шаг 1: Подтверждение пользователя

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Дискуссия готова к переводу в WAITING. Подтверждаете?"

| Ответ | Действие |
|-------|----------|
| Да | Перевести в WAITING |
| Нет | Оставить в DRAFT |

### Шаг 2: Обновить статус через `chain_status.py`

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="WAITING", document="discussion")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

- `result.auto_propose` — предложение следующего шага (`/design-create NNNN`)

### Каскад DRAFT (возврат из WAITING)

**SSOT:** [Стандарт analysis/ § 6.1](../standard-analysis.md#61-draft-to-waiting)

При возврате документа из WAITING → DRAFT (контекст родителя изменился) все его WAITING-дочерние тоже → DRAFT.

**Через `chain_status.py`:**
```python
result = mgr.transition(to="DRAFT", document="discussion")
# T2: автокаскад — дочерние WAITING-документы тоже → DRAFT
```

**На уровне Discussion:** если Discussion возвращается в DRAFT — её Design (если в WAITING) тоже → DRAFT. Дискуссия снова открыта для операций из секции [Статус DRAFT — операции](#статус-draft-операции).

**Когда это происходит:**
- Пользователь решил внести изменения после одобрения
- Discussion вернулась из CONFLICT → при разрешении пользователь изменил контент (→ DRAFT вместо WAITING)

---

## Upward feedback при WAITING

**SSOT:** [Стандарт analysis/ § 3.5 — Upward feedback](../standard-analysis.md#35-upward-feedback)

При работе на нижестоящих уровнях (Design, Plan Tests, Plan Dev) LLM может обнаружить информацию, которая должна быть отражена в Discussion. **Статус остаётся WAITING** — без перевода в DRAFT.

**Отличие от "Каскад DRAFT":** Каскад DRAFT (WAITING → DRAFT) — пользователь решил переработать документ. Upward feedback — LLM дополняет документ точечно, пользователь подтверждает. Это разные сценарии.

#### Шаг 1: LLM предлагает дополнение

LLM формулирует конкретное дополнение (новое требование, уточнение критерия, расширение контекста) и предлагает пользователю через AskUserQuestion.

#### Шаг 2: Пользователь подтверждает

Пользователь подтверждает, корректирует или отклоняет предложение.

#### Шаг 3: Внести изменения

Дополнить затронутые секции Discussion. Нумерация элементов продолжается (следующий номер = max + 1).

#### Шаг 4: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-discussion.py specs/analysis/NNNN-{topic}/discussion.md
```

---

## Переход: WAITING → RUNNING

**SSOT:** [Стандарт analysis/ § 6.2](../standard-analysis.md#62-waiting-to-running)

> **Tree-level.** Переход управляется на уровне цепочки, не Discussion.

**Триггер:** все документы цепочки (Discussion → Design → Plan Tests → Plan Dev) в WAITING. После `/docs-sync` (синхронизация specs/docs/) — LLM предлагает через AskUserQuestion: "Все спецификации готовы. Перейти в RUNNING?" Пользователь подтверждает.

**На уровне Discussion:** статус меняется `WAITING` → `RUNNING`. Операций нет — документ просто переходит в режим реализации.

---

## Статус RUNNING — ограничения

> **Прямые изменения запрещены.** Документ в RUNNING — согласованная спецификация. Изменения возможны только через CONFLICT ([Стандарт analysis/ § 6.3](../standard-analysis.md#63-running-to-conflict)).

Если обнаружена необходимость изменить Discussion в RUNNING — это сигнал CONFLICT-уровня. См. [Переход: RUNNING → CONFLICT](#переход-running-conflict).

---

## Переход: RUNNING → CONFLICT

**SSOT:** [Стандарт analysis/ § 6.3](../standard-analysis.md#63-running-to-conflict)

> **Tree-level каскад.** При обнаружении CONFLICT-уровня проблемы **все** документы цепочки → CONFLICT.

**Триггер:** обратная связь от кода выявила несовместимость со спецификациями на уровне Design или выше ([Стандарт analysis/ § 6.3 — уровни обратной связи](../standard-analysis.md#63-running-to-conflict)).

**На уровне Discussion:** статус меняется `RUNNING` → `CONFLICT`. Переход инициируется на уровне цепочки — Discussion сама его не вызывает.

---

## Статус CONFLICT — операции

### Как Discussion попадает в CONFLICT

Discussion попадает в CONFLICT через tree-level каскад ([Стандарт analysis/ § 6.3](../standard-analysis.md#63-running-to-conflict)): при обнаружении CONFLICT на любом уровне **все** документы цепочки → CONFLICT, включая Discussion.

LLM определяет самый высокий затронутый документ — снизу вверх, от Plan до Discussion: "Содержание этого документа стало неверным?"

### Операции при CONFLICT

**Если Discussion затронута** (утверждения стали фактически неверными из-за изменений в коде):

1. LLM читает **весь документ** целиком
2. Вносит **точечные правки** в затронутые секции (фичи, требования, критерии успеха), сохраняя остальной контент
3. Пользователь ревьюит изменения → документ → WAITING ([Переход: CONFLICT → WAITING](#переход-conflict-waiting))

**Если Discussion НЕ затронута** (самый частый случай — Discussion как самый высокий уровень обычно не затрагивается):

1. LLM и пользователь **верифицируют** документ без изменений
2. Подтверждают, что утверждения остаются верными
3. Документ → WAITING ([Переход: CONFLICT → WAITING](#переход-conflict-waiting))

---

## Переход: CONFLICT → WAITING

**SSOT:** [Стандарт analysis/ § 6.4](../standard-analysis.md#64-conflict-to-waiting)

> **Per-document.** Каждый документ переходит в WAITING независимо после разрешения.

**Разрешение — сверху вниз:** начиная с самого высокого затронутого документа. Если Discussion — самый высокий затронутый, разрешение начинается с неё.

**Шаги:**

1. LLM исправляет документ (или верифицирует без изменений)
2. Пользователь ревьюит → одобряет
3. Через `chain_status.py`:
   ```python
   result = mgr.transition(to="WAITING", document="discussion")
   # Модуль автоматически: обновляет frontmatter + README dashboard
   ```
4. Когда **все** документы цепочки в WAITING → каскад RUNNING ([Стандарт analysis/ § 6.2](../standard-analysis.md#62-waiting-to-running))

**Если пользователь отклоняет разрешение:**

| Исход | Переход |
|-------|---------|
| Конфликт разрешён | CONFLICT → WAITING |
| Конфликт неразрешим | → ROLLING_BACK ([Стандарт analysis/ § 6.7](../standard-analysis.md#67-to-rolling_back)) |
| Пользователь отклоняет | → ROLLING_BACK ([Стандарт analysis/ § 6.7](../standard-analysis.md#67-to-rolling_back)) |

---

## Переход: RUNNING → REVIEW

**SSOT:** [Стандарт analysis/ § 6.5](../standard-analysis.md#65-running-to-review)

> **Tree-level переход.** Все документы цепочки переходят в REVIEW одновременно.
> `/review-create` создаёт review.md. `/review` запускает ревью.

**На уровне Discussion:** статус меняется `RUNNING` → `REVIEW`.

Обновить README: `RUNNING` → `REVIEW`.

---

## Переход: REVIEW → DONE

**SSOT:** [Стандарт analysis/ § 6.6](../standard-analysis.md#66-review-to-done)

> **Bottom-up каскад.** Discussion → DONE когда Design (единственный child, 1:1) → DONE.

**На уровне Discussion:** статус меняется `REVIEW` → `DONE` автоматически. Операций нет — переход инициируется снизу вверх.

После перехода в DONE:
- Обновить README: `REVIEW` → `DONE`
- Discussion становится архивной записью реализованного решения

---

## Статус DONE — ограничения

**SSOT:** [standard-discussion.md § 1](./standard-discussion.md#1-назначение) → "После DONE"

> **Discussion — архивная запись.** Изменения запрещены.

**Допустимые изменения:**
- Исправление опечаток (typo corrections)
- Исправление битых ссылок

**Новые требования:** создать **новую** Discussion со ссылкой на DONE-дискуссию в секции "Проблема / Контекст".

**Отмена решения:** если новая Discussion частично или полностью отменяет решение DONE-дискуссии — в секции "Проблема / Контекст" явно указать: "Решение NNNN (DONE) отменяется по причине [X]. Новый подход: [Y]."

---

## Переход: → ROLLING_BACK

**SSOT:** [Стандарт analysis/ § 6.7](../standard-analysis.md#67-to-rolling_back)

> **Tree-level.** Все документы цепочки → ROLLING_BACK.

**Триггеры:**
- Пользователь даёт команду на откат
- Конфликт неразрешим ([Стандарт analysis/ § 6.4](../standard-analysis.md#64-conflict-to-waiting))
- Пользователь отклоняет разрешение конфликта

**На уровне Discussion:** Discussion не имеет артефактов — откат = **no-op**, только смена статуса → ROLLING_BACK.

Через `chain_status.py` (tree-level):
```python
result = mgr.transition(to="ROLLING_BACK")
# Модуль автоматически: все 4 документа → ROLLING_BACK (кроме DONE/REJECTED), README dashboard
```

---

## Переход: ROLLING_BACK → REJECTED

**SSOT:** [Стандарт analysis/ § 6.8](../standard-analysis.md#68-rolling_back-to-rejected)

> **REJECTED — финальный статус.** Изменения запрещены.

**Условие:** LLM проверяет, что все документы цепочки в ROLLING_BACK и артефакты каждого уровня откачены → вся цепочка → REJECTED.

**На уровне Discussion:** статус меняется `ROLLING_BACK` → `REJECTED`.

Через `chain_status.py` (tree-level):
```python
result = mgr.transition(to="REJECTED")
# Модуль автоматически: все документы → REJECTED, README dashboard
```

**Перезапуск:** если бизнес-потребность остаётся актуальной, создать **новую** Discussion со ссылкой на отклонённую в секции "Проблема / Контекст".

---

## Обновление ссылок

Дискуссия содержит минимум ссылок (только frontmatter `children`). При изменении пути Design-документа:

1. Обновить `children` в frontmatter дискуссии
2. Обновить запись в `specs/analysis/README.md` (колонка Design)

---

## Чек-лист

### Статус DRAFT — обновление
- [ ] Статус = DRAFT
- [ ] Изменения внесены
- [ ] Нумерация корректна (нет дублей, нет перенумерации)
- [ ] Валидация пройдена
- [ ] README обновлён (если нужно)

### Разрешение маркеров
- [ ] Все маркеры собраны
- [ ] Ответы получены от пользователя
- [ ] Маркеры заменены на ответы
- [ ] [Dependency Barrier](../standard-analysis.md#83-dependency-barrier) разрешён (если был)
- [ ] Валидация пройдена — маркеров нет

### Принятие предложений
- [ ] PROP-N идентифицирован
- [ ] Пользователь подтвердил
- [ ] Затронутые секции обновлены
- [ ] Нумерация не нарушена
- [ ] Пакетная обработка: все PROP обработаны → секция заменена на заглушку
- [ ] Валидация пройдена

### Upward feedback при WAITING
- [ ] Статус = WAITING
- [ ] LLM предложил дополнение
- [ ] Пользователь подтвердил
- [ ] Секции дополнены, нумерация продолжена
- [ ] Валидация пройдена
- [ ] Статус остаётся WAITING (без перевода в DRAFT)

### Переход DRAFT → WAITING
- [ ] Статус = DRAFT
- [ ] Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]`
- [ ] Нет [Dependency Barrier](../standard-analysis.md#83-dependency-barrier)
- [ ] Валидация пройдена — 0 ошибок
- [ ] Пользователь подтвердил перевод через AskUserQuestion
- [ ] Статус обновлён в frontmatter
- [ ] Статус обновлён в README

### Переход CONFLICT → WAITING
- [ ] Определено: Discussion затронута или нет
- [ ] Если затронута — точечные правки внесены
- [ ] Если не затронута — верификация пройдена
- [ ] Пользователь одобрил разрешение
- [ ] Статус обновлён в frontmatter
- [ ] Статус обновлён в README

### Статус DONE
- [ ] Только typo corrections или битые ссылки
- [ ] Новые требования → новая Discussion

### Переход → ROLLING_BACK / REJECTED
- [ ] Статус обновлён в frontmatter
- [ ] Статус обновлён в README
- [ ] Артефакты Discussion = no-op (нет артефактов)

---

## Примеры

### Добавление фичи (DRAFT)

```
Пользователь: "Добавь фичу — поддержка API-ключей для сервисных аккаунтов"

1. Прочитать specs/analysis/0001-oauth2-authorization/discussion.md
2. Шаг 0: статус = DRAFT → секция "Статус DRAFT — операции"
3. Определить следующий номер: F-3 удалена → F-4
4. Добавить: | F-4 | API-ключи для сервисных аккаунтов | ... |
5. Валидация → ОК
```

### Разрешение маркеров перед WAITING (DRAFT)

```
Маркеры в 0001-oauth2-authorization/discussion.md:
- [ТРЕБУЕТ УТОЧНЕНИЯ: какой SLA по времени авторизации?]
- [ТРЕБУЕТ УТОЧНЕНИЯ: поддержка offline-режима?]

1. Шаг 0: статус = DRAFT → секция "Разрешение маркеров"
2. Показать маркеры пользователю
3. Ответы: "p99 < 100ms при 10k RPS", "Нет, только online"
4. Заменить маркеры на ответы
5. Валидация → 0 маркеров → можно в WAITING
```

### Перевод в WAITING (DRAFT → WAITING)

```
1. Шаг 0: статус = DRAFT → секция "Переход: DRAFT → WAITING"
2. Проверить условия: маркеров нет, валидация ОК
3. AskUserQuestion: "Перевести Discussion в WAITING?"
4. Пользователь: "Да"
5. status: DRAFT → status: WAITING
6. README обновлён
```

### Разрешение CONFLICT (CONFLICT → WAITING)

```
Ситуация: вся цепочка → CONFLICT из-за обратной связи от кода.
LLM определил самый высокий затронутый уровень: Design.
Discussion НЕ затронута.

1. Шаг 0: статус = CONFLICT → секция "Статус CONFLICT — операции"
2. Discussion не затронута → верификация без изменений
3. LLM и пользователь подтверждают: утверждения верны
4. status: CONFLICT → status: WAITING
5. README обновлён
```

### Discussion → REVIEW → DONE

```
Ситуация: Все TASK-N выполнены → цепочка → REVIEW → review.md RESOLVED → каскад DONE.

1. Discussion автоматически → REVIEW (tree-level)
2. README обновлён: RUNNING → REVIEW
3. review.md RESOLVED → каскад DONE (bottom-up)
4. Discussion автоматически → DONE
5. README обновлён: REVIEW → DONE
6. Discussion — архивная запись. Новые требования → новая Discussion
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-analysis-discussion.py](../../.scripts/validate-analysis-discussion.py) | Валидация документа (все статусы) | [validation-discussion.md](./validation-discussion.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/discussion-modify](/.claude/skills/discussion-modify/SKILL.md) | Изменение документа дискуссии | Этот документ |
