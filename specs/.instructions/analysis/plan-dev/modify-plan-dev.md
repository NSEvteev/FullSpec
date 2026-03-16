---
description: Воркфлоу изменения документа плана разработки SDD — операции по статусам, переходы жизненного цикла, GitHub Issues синхронизация, рабочие правки.
standard: .instructions/standard-instruction.md
standard-version: v1.7
index: specs/.instructions/README.md
---

# Воркфлоу изменения плана разработки

Рабочая версия стандарта: 1.7

Процессы изменения существующего документа плана разработки (`specs/analysis/NNNN-{topic}/plan-dev.md`).

**Полезные ссылки:**
- [Стандарт плана разработки](./standard-plan-dev.md)
- [Стандарт аналитического контура](../standard-analysis.md) — статусы, каскады
- [Инструкции specs/](../../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-plan-dev.md](./standard-plan-dev.md) |
| Валидация | [validation-plan-dev.md](./validation-plan-dev.md) |
| Создание | [create-plan-dev.md](./create-plan-dev.md) |
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
- [Переход: WAITING → RUNNING](#переход-waiting-running)
- [Статус RUNNING — рабочие правки](#статус-running-рабочие-правки)
- [Переход: RUNNING → CONFLICT](#переход-running-conflict)
- [Статус CONFLICT — операции](#статус-conflict-операции)
  - [Как Plan Dev попадает в CONFLICT](#как-plan-dev-попадает-в-conflict)
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

> **SSOT — Стандарт аналитического контура.** Каскады, условия переходов — [Стандарт analysis/ § 6](../standard-analysis.md#6-последовательность-статусов). Этот документ описывает операции на уровне Plan Dev.

> **Plan Dev — терминальный.** Plan Dev управляет DRAFT → WAITING. RUNNING → REVIEW триггерится выполнением всех TASK-N. REVIEW → DONE — после ревью кода.

---

## Шаг 0: Определить статус документа

Прочитать frontmatter документа → поле `status`. По таблице ниже перейти к нужной секции.

| Текущий статус | Доступные операции | Доступные переходы |
|----------------|--------------------|--------------------|
| **DRAFT** | [Обновление контента](#обновление-контента), [Разрешение маркеров](#разрешение-маркеров) | [DRAFT → WAITING](#переход-draft-waiting) |
| **WAITING** | — | [WAITING → RUNNING](#переход-waiting-running) |
| **RUNNING** | [Рабочие правки](#статус-running-рабочие-правки) | [RUNNING → CONFLICT](#переход-running-conflict), [RUNNING → REVIEW](#переход-running-review) |
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

Прочитать весь документ плана разработки.

**Проверить:** статус = DRAFT. Если статус ≠ DRAFT — **СТОП**, см. [Шаг 0](#шаг-0-определить-статус-документа).

#### Шаг 2: Внести изменения

**SSOT:** [standard-plan-dev.md § 5](./standard-plan-dev.md#5-разделы-документа)

Допустимые изменения:

**Резюме:**
- Обновление scope, количества задач, средней сложности

**Per-service разделы:**
- Добавление нового per-service раздела (при добавлении SVC-N в Design)
- Удаление per-service раздела (при удалении SVC-N из Design)
- Добавление/удаление/изменение TASK-N
- Добавление/удаление/изменение подзадач

**Кросс-сервисные зависимости:**
- Обновление таблицы зависимостей

**Правила нумерации TASK-N:** При добавлении — следующий номер (max + 1). При удалении — **не перенумеровывать**. Переименование существующих TASK-N запрещено.

#### Шаг 3: Обновить кросс-сервисные зависимости

После изменения TASK-N — **обязательно** обновить таблицу кросс-сервисных зависимостей.

#### Шаг 4: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-plan-dev.py specs/analysis/NNNN-{topic}/plan-dev.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-plan-dev.md](./validation-plan-dev.md).

#### Шаг 5: Обновить README

Если изменился `description` или другие отображаемые поля — обновить запись в `specs/analysis/README.md`.

#### Шаг 6: Отчёт о выполнении

```
## Отчёт об изменении плана разработки

Изменён план разработки: `specs/analysis/NNNN-{topic}/plan-dev.md`

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
python specs/.instructions/.scripts/validate-analysis-plan-dev.py specs/analysis/NNNN-{topic}/plan-dev.md
```

---

## Переход: DRAFT → WAITING

**SSOT:** [standard-plan-dev.md § 4](./standard-plan-dev.md#4-переходы-статусов) | [Стандарт analysis/ § 6.1](../standard-analysis.md#61-draft-to-waiting)

Единственный переход, управляемый на уровне Plan Dev.

### Условия (блокирующие)

| Условие | Проверка |
|---------|----------|
| Статус = DRAFT | frontmatter `status: DRAFT` |
| Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]` | Ни одного маркера в документе |
| Нет [Dependency Barrier](../standard-analysis.md#83-dependency-barrier) | Нет `⛔ DEPENDENCY BARRIER` |
| Валидация пройдена | Скрипт validate-analysis-plan-dev.py → 0 ошибок |

```bash
python specs/.instructions/.scripts/validate-analysis-plan-dev.py specs/analysis/NNNN-{topic}/plan-dev.md
```

**Если условия не выполнены:** сообщить пользователю — предложить разрешить маркеры или исправить ошибки.

### Шаг 1: Подтверждение пользователя

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: «План разработки готов к переводу в WAITING. Подтверждаете?»

| Ответ | Действие |
|-------|----------|
| Да | Перевести в WAITING |
| Нет | Оставить в DRAFT |

### Шаг 2: Обновить статус

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="WAITING", document="plan-dev")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

**Артефакты Plan Dev → WAITING:** нет артефактов в docs/. Plan Dev не создаёт Planned Changes.

### Шаг 3: Проверить готовность цепочки

Проверить: все ли 4 документа цепочки в WAITING.

| Все в WAITING? | Действие |
|----------------|----------|
| Да | AskUserQuestion: "Все спецификации готовы. Начать разработку через `/dev-create {NNNN}`?" |
| Нет | Вывести: "Plan Dev → WAITING. Ожидают: {список документов не в WAITING}" |

### Каскад DRAFT (возврат из WAITING)

**SSOT:** [Стандарт analysis/ § 6.1](../standard-analysis.md#61-draft-to-waiting)

Plan Dev — терминальный. При возврате из WAITING → DRAFT — каскад вниз невозможен (нет дочерних).

```python
result = mgr.transition(to="DRAFT", document="plan-dev")
# plan-dev — leaf, без дочерних
```

**Когда это происходит:**
- Пользователь решил внести изменения после одобрения
- Parent Plan Tests вернулся в DRAFT (каскад сверху)

---

## Переход: WAITING → RUNNING

**SSOT:** [Стандарт analysis/ § 6.2](../standard-analysis.md#62-waiting-to-running)

> **Tree-level.** Переход управляется на уровне цепочки, не Plan Dev.

**Триггер:** все документы цепочки (Discussion → Design → Plan Tests → Plan Dev) в WAITING. Пользователь подтверждает.

**На уровне Plan Dev:** статус `WAITING` → `RUNNING`.

**GitHub Issues:** по команде пользователя LLM создаёт каждый TASK-N → Issue через `/issue-create`. Привязка к Milestone из frontmatter Discussion.

---

## Статус RUNNING — рабочие правки

**SSOT:** [standard-plan-dev.md § 4](./standard-plan-dev.md#4-переходы-статусов)

> **Рабочие правки допустимы** при уровне «Флаг» ([Стандарт analysis/ § 6.3](../standard-analysis.md#63-running-to-conflict)).

**Допустимые рабочие правки (без CONFLICT):**
- Добавление подзадач
- Уточнение описаний подзадач
- Изменение порядка внутри задачи
- Добавление новых TASK-N **в конец** per-service раздела (номер = max(TASK-N) + 1)
- Добавление нового TASK-N в существующий BLOCK-N (если не создаёт file overlap и BLOCK не превышает 3 TASK-N)

**Запрещено:**
- Переименование существующих TASK-N (ломает ссылки в GitHub Issues)
- Удаление TASK-N
- Изменение 5 обязательных полей существующих TASK-N (→ CONFLICT)
- Перемещение TASK-N между BLOCK-N (→ CONFLICT)
- Изменение волн (wave) существующих BLOCK-N (→ CONFLICT)

**Отметка выполнения подзадач:**
- `- [ ]` → `- [x]` при выполнении подзадачи

---

## Переход: RUNNING → CONFLICT

**SSOT:** [Стандарт analysis/ § 6.3](../standard-analysis.md#63-running-to-conflict)

> **Tree-level каскад.** При CONFLICT все документы цепочки → CONFLICT.

**Триггер:** обратная связь от кода выявила несовместимость на уровне Plan Dev или выше.

**На уровне Plan Dev:** статус `RUNNING` → `CONFLICT`. Issues остаются открытыми.

---

## Статус CONFLICT — операции

### Как Plan Dev попадает в CONFLICT

Plan Dev попадает в CONFLICT через tree-level каскад. LLM определяет самый высокий затронутый документ — снизу вверх.

### Операции при CONFLICT

**Если Plan Dev затронут** (задачи стали неверными):

1. LLM читает **весь документ** целиком
2. Сверяет с обновлёнными Plan Tests / Design (после их разрешения CONFLICT → WAITING)
3. Вносит **точечные правки** в затронутые секции:
   - Обновление полей TASK-N (Сложность, Приоритет, Зависимости, TC, Источник)
   - Добавление новых TASK-N (в конец per-service раздела, номер max + 1)
   - Удаление TASK-N (при удалении SVC-N из Design)
   - Обновление подзадач — **отметки `[x]` сохраняются** (прогресс не сбрасывается)
   - Обновление кросс-сервисных зависимостей
   - Обновление таблицы «Блоки выполнения» (BLOCK-N) — перегруппировка задач, пересчёт волн
   - Обновление Резюме
4. Пользователь ревьюит → Plan Dev → WAITING

**Если Plan Dev НЕ затронут:**

1. LLM и пользователь **верифицируют** документ без изменений
2. Plan Dev → WAITING

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
   result = mgr.transition(to="WAITING", document="plan-dev")
   ```
4. **Проверить готовность цепочки.** Если Plan Dev — последний документ, возвращённый в WAITING (все 4 документа цепочки в WAITING):
   AskUserQuestion: "Конфликт разрешён. Все спецификации снова в WAITING. Возобновить разработку через `/dev-create {NNNN}`?"
   При подтверждении → выполнить `/dev-create {NNNN}` (Issues уже существуют — `/dev-create --resume` обнаружит и пропустит создание).

**Синхронизация Issues** ([standard-issue.md](/.github/.instructions/issues/standard-issue.md))**:** LLM сравнивает TASK-N в обновлённом Plan Dev с существующими Issues. Критерий изменения: изменились поля Сложность, Приоритет, Зависимости, TC или подзадачи.

| Результат сравнения | Действие |
|---------------------|----------|
| TASK-N изменился | `/issue-modify` — обновить Issue |
| TASK-N удалён | Close Issue `--reason "not planned"` |
| Новый TASK-N | `/issue-create` — создать Issue |
| TASK-N не изменился | Не обновлять Issue |

**Если пользователь отклоняет:**

| Исход | Переход |
|-------|---------|
| Конфликт разрешён | CONFLICT → WAITING |
| Конфликт неразрешим | → ROLLING_BACK |
| Пользователь отклоняет | → ROLLING_BACK |

---

## Переход: RUNNING → REVIEW

**SSOT:** [Стандарт analysis/ § 6.5](../standard-analysis.md#65-running-to-review)

**Триггер:** все задачи TASK-N выполнены. Критерий выполненности: все подзадачи отмечены `[x]` и соответствующий GitHub Issue закрыт.

> **Tree-level переход.** Все документы цепочки переходят в REVIEW одновременно.
> `/review-create` создаёт review.md (если ещё не создан). `/review` запускает ревью.

**На уровне Plan Dev:**

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="REVIEW", document="plan-dev")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

---

## Переход: REVIEW → DONE

**SSOT:** [Стандарт analysis/ § 6.6](../standard-analysis.md#66-review-to-done)

**Триггер:** review.md RESOLVED (вердикт READY).

**На уровне Plan Dev:**

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="DONE", document="plan-dev")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

**Побочные эффекты Plan Dev → DONE:**

> **Bottom-up каскад DONE:** Plan Dev → DONE триггерит каскад: Plan Tests → Design → Discussion → DONE ([Стандарт analysis/ § 6.6](../standard-analysis.md#66-review-to-done)). Каждый документ выполняет свои побочные эффекты при переходе в DONE.

---

## Статус DONE — ограничения

**SSOT:** [standard-plan-dev.md § 1](./standard-plan-dev.md#1-назначение)

> **Plan Dev — архивная запись.** Изменения ограничены.

**Допустимые изменения:**
- Исправление орфографических ошибок, не изменяющих смысл полей TASK-N

**Любое изменение смысла TASK-N** (добавление, удаление, изменение полей) → CONFLICT-цикл.

**Новый scope:** создать **новую** Discussion → Design → Plan Tests → Plan Dev.

---

## Переход: → ROLLING_BACK

**SSOT:** [Стандарт analysis/ § 6.7](../standard-analysis.md#67-to-rolling_back)

> **Tree-level.** Все документы цепочки → ROLLING_BACK.

**Откат артефактов Plan Dev:**
- GitHub Issues закрываются `--reason "not planned"` с комментарием "rolled back"
- Feature-ветка удаляется

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
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

Plan Dev содержит ссылку в frontmatter (`parent`).

При изменении путей:
1. Обновить `parent` в frontmatter
2. Обновить запись в `specs/analysis/README.md`
3. Обновить `children` в parent Plan Tests

---

## Чек-лист

### Статус DRAFT — обновление
- [ ] Статус = DRAFT
- [ ] Изменения внесены
- [ ] Нумерация TASK-N корректна (нет дублей, нет перенумерации)
- [ ] Кросс-сервисные зависимости обновлены
- [ ] Валидация пройдена
- [ ] README обновлён (если нужно)

### Разрешение маркеров
- [ ] Все маркеры собраны
- [ ] Ответы получены от пользователя
- [ ] Маркеры заменены на ответы
- [ ] Dependency Barrier разрешён (если был)
- [ ] Валидация пройдена — маркеров нет

### Переход DRAFT → WAITING
- [ ] Статус = DRAFT
- [ ] Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]`
- [ ] Нет Dependency Barrier
- [ ] Валидация пройдена — 0 ошибок
- [ ] Пользователь подтвердил перевод
- [ ] Статус обновлён в frontmatter
- [ ] Статус обновлён в README
- [ ] Предложен запуск разработки (если все 4 в WAITING)

### Рабочие правки (RUNNING)
- [ ] Только допустимые правки (подзадачи, описания, новые TASK-N в конец)
- [ ] Нет переименования существующих TASK-N
- [ ] Нет изменения полей существующих TASK-N
- [ ] Нет перемещения TASK-N между BLOCK-N
- [ ] Новые TASK-N добавлены в существующий BLOCK-N (без file overlap)
- [ ] Валидация пройдена

### Переход CONFLICT → WAITING
- [ ] Определено: Plan Dev затронут или нет
- [ ] Если затронут — точечные правки TASK-N/подзадач/зависимостей
- [ ] Если затронут — таблица «Блоки выполнения» обновлена (BLOCK-N, волны)
- [ ] Отметки `[x]` сохранены
- [ ] Если не затронут — верификация пройдена
- [ ] Пользователь одобрил
- [ ] Issues синхронизированы (изменённые, удалённые, новые)
- [ ] Статус обновлён в frontmatter и README
- [ ] Предложено возобновление разработки (если все 4 в WAITING)

### Переход RUNNING → REVIEW
- [ ] Все TASK-N выполнены (подзадачи `[x]`, Issues закрыты)
- [ ] Цепочка переведена в REVIEW (tree-level)
- [ ] README обновлён

### Переход REVIEW → DONE
- [ ] review.md RESOLVED (вердикт READY)
- [ ] Статус обновлён в frontmatter и README
- [ ] Bottom-up каскад DONE запущен (Plan Tests → Design → Discussion)

### Переход → ROLLING_BACK / REJECTED
- [ ] Issues закрыты `--reason "not planned"`
- [ ] Feature-ветка удалена
- [ ] Статус обновлён в frontmatter и README

---

## Примеры

### Добавление TASK-N (DRAFT)

```
Пользователь: "Добавь задачу на настройку rate limiting в Plan Dev"

1. Прочитать specs/analysis/0001-oauth2-authorization/plan-dev.md
2. Шаг 0: статус = DRAFT → секция "Статус DRAFT — операции"
3. Определить следующий номер: TASK-9 → TASK-10
4. Добавить TASK-10 в gateway → Задачи
5. Обновить кросс-сервисные зависимости (если нужно)
6. Валидация → OK
```

### Рабочие правки (RUNNING)

```
Ситуация: агент-кодер обнаружил, что для TASK-3 нужна дополнительная подзадача.

1. Шаг 0: статус = RUNNING → секция "Рабочие правки"
2. Добавить подзадачу 3.4 в TASK-3
3. Валидация → OK (рабочие правки допустимы)
```

### Разрешение CONFLICT

```
Ситуация: Design изменился — auth API изменён.
Вся цепочка → CONFLICT.
LLM определил: Plan Dev затронут (TASK-1, TASK-2 ссылаются на изменённые подсекции).

1. Шаг 0: статус = CONFLICT → секция "Операции при CONFLICT"
2. Сверить с обновлённым Plan Tests/Design (уже WAITING)
3. Обновить TASK-1: Сложность 7 → 8, Источник SVC-1 § 5 → SVC-1 § 6
4. Обновить TASK-2: подзадачи — добавить 2.4, сохранить [x] на 2.1 и 2.2
5. Кросс-зависимости — без изменений
6. Пользователь ревьюит → одобряет
7. Синхронизация Issues: TASK-1 → /issue-modify, TASK-2 → /issue-modify
8. status: CONFLICT → WAITING
9. README обновлён
```

### Plan Dev → REVIEW → DONE

```
Ситуация: последний TASK-9 выполнен (все подзадачи [x], Issue закрыт).

1. Проверить: все TASK-N выполнены? → Да
2. Цепочка → REVIEW (tree-level). README: RUNNING → REVIEW
3. /review → review.md RESOLVED (вердикт READY)
4. status: REVIEW → DONE
3. README обновлён
4. Bottom-up каскад: Plan Tests → DONE → Design → DONE → Discussion → DONE
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-analysis-plan-dev.py](../../.scripts/validate-analysis-plan-dev.py) | Валидация документа (все статусы) | [validation-plan-dev.md](./validation-plan-dev.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/plan-dev-modify](/.claude/skills/plan-dev-modify/SKILL.md) | Изменение документа плана разработки | Этот документ |
