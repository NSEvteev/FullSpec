---
description: Воркфлоу создания документа плана тестов SDD — чтение Design, Clarify, генерация TC-N/fixtures/матрицы покрытия, валидация, перевод DRAFT → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу создания плана тестов

Рабочая версия стандарта: 1.1

Пошаговый процесс создания нового документа плана тестов (`specs/analysis/NNNN-{topic}/plan-test.md`).

**Полезные ссылки:**
- [Стандарт плана тестов](./standard-plan-test.md)
- [Стандарт аналитического контура](../standard-analysis.md) — статусы, Clarify, маркеры, общий паттерн объекта
- [Инструкции specs/](../../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-plan-test.md](./standard-plan-test.md) |
| Валидация | [validation-plan-test.md](./validation-plan-test.md) |
| Создание | Этот документ |
| Модификация | [modify-plan-test.md](./modify-plan-test.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить parent Design](#шаг-1-проверить-parent-design)
  - [Шаг 2: Создать файл из шаблона](#шаг-2-создать-файл-из-шаблона)
  - [Шаг 3: Заполнить frontmatter](#шаг-3-заполнить-frontmatter)
  - [Шаг 4: Прочитать источники](#шаг-4-прочитать-источники)
  - [Шаг 5: Clarify](#шаг-5-clarify)
  - [Шаг 6: Заполнить разделы](#шаг-6-заполнить-разделы)
  - [Шаг 7: Регистрация в README](#шаг-7-регистрация-в-readme)
  - [Шаг 8: Валидация](#шаг-8-валидация)
  - [Шаг 9: Ревью пользователем](#шаг-9-ревью-пользователем)
  - [Шаг 10: Отчёт о выполнении](#шаг-10-отчёт-о-выполнении)
  - [Шаг 11: Авто-предложение следующего этапа](#шаг-11-авто-предложение-следующего-этапа)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Plan Tests — после Design.** Plan Tests создаётся только после одобрения Design (статус WAITING). Без Design — нет Plan Tests.

> **Зона: HOW TO VERIFY.** Plan Tests определяет acceptance-сценарии и тестовые данные. Бизнес-требования — Discussion, архитектура — Design, задачи — Plan Dev.

> **Файл до чтения источников.** Сначала создать файл из шаблона и заполнить frontmatter — затем читать источники. Это обеспечивает resumability при прерывании.

> **Естественные предложения.** Формат TC-N — «субъект + действие → результат» на русском. НЕ Given/When/Then.

> **LLM предлагает, пользователь подтверждает.** LLM сам генерирует тест-сценарии на основе Design/Discussion. НЕ спрашивает «какие тесты писать?»

---

## Шаги

### Шаг 1: Проверить parent Design

**SSOT:** [standard-plan-test.md § 1](./standard-plan-test.md#1-назначение)

1. Проверить, что Design существует в `specs/analysis/NNNN-{topic}/design.md`
2. Проверить, что `status: WAITING` в frontmatter Design
3. Если Design не в WAITING — **СТОП**: «Plan Tests может быть создан только после одобрения Design»

### Шаг 2: Создать файл из шаблона

**SSOT:** [standard-plan-test.md § 7](./standard-plan-test.md#7-шаблон)

1. Скопировать шаблон из [standard-plan-test.md § 7](./standard-plan-test.md#7-шаблон)
2. Создать файл `specs/analysis/NNNN-{topic}/plan-test.md`

### Шаг 3: Заполнить frontmatter

**SSOT:** [standard-plan-test.md § 3](./standard-plan-test.md#3-frontmatter)

Заполнить поля:

| Поле | Значение |
|------|----------|
| `description` | Краткое описание (до 1024 символов) |
| `standard` | `specs/.instructions/analysis/plan-test/standard-plan-test.md` |
| `standard-version` | `v1.1` |
| `index` | `specs/analysis/README.md` |
| `parent` | `design.md` |
| `children` | `[]` (Plan Dev ещё не создан) |
| `status` | `DRAFT` |
| `milestone` | Скопировать из parent Discussion |

### Шаг 4: Прочитать источники

**SSOT:** [standard-plan-test.md § 1 → Входные данные](./standard-plan-test.md#1-назначение)

Последовательно прочитать 6 источников:

| # | Источник | Что извлечь |
|---|---------|-------------|
| 1 | **SVC-N секции** из Design | Ответственность, компоненты, решения — scope для тестов |
| 2 | **INT-N блоки** из Design | Контракты — интеграционные тесты |
| 3 | **STS-N** из Design | Системные тест-сценарии — e2e тесты |
| 4 | **REQ-N** из Discussion | Требования — acceptance criteria |
| 5 | **`docs/{svc}.md`** | Текущее AS IS — регрессионные тесты |
| 6 | **`docs/.system/testing.md`** | Стратегия тестирования — дефолтная стратегия |

**Discussion без REQ-N:** Если Discussion не содержит пронумерованных REQ-N — поставить маркер `[ТРЕБУЕТ УТОЧНЕНИЯ: Discussion не содержит REQ-N — невозможно построить матрицу покрытия]`.

### Шаг 5: Clarify

**SSOT:** [standard-plan-test.md § 6](./standard-plan-test.md#6-clarify), [Стандарт analysis/ § 8](../standard-analysis.md#8-clarify-и-блокирующие-правила)

**Если `--auto-clarify` НЕ указан:**

LLM **сам предлагает** и уточняет через AskUserQuestion:

| Что предлагает LLM | Пример |
|---------------------|--------|
| Типы тестов | «Нужны ли load-тесты для auth? SLA = 10k RPS» |
| Покрытие | «REQ-3 (rate limiting) — достаточно ли одного e2e теста?» |
| Тестовые данные | «Какие edge cases для refresh-токена? Истёкший, отозванный, невалидный?» |
| Граничные кейсы | «Тестировать ли concurrent refresh (два запроса одновременно)?» |
| Мокирование | «Для интеграционных тестов auth: мокировать users-сервис или поднимать?» |

**Если `--auto-clarify` указан:**

LLM пропускает Clarify, генерирует документ на основе источников и ставит маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` на все неясности.

### Шаг 6: Заполнить разделы

**SSOT:** [standard-plan-test.md § 5](./standard-plan-test.md#5-разделы-документа)

На основе источников (шаг 4) и Clarify (шаг 5) заполнить **все разделы**:

1. **Резюме** — scope, кол-во TC-N, покрытие STS-N и REQ-N, ключевые тестовые решения (отличия от testing.md)
2. **Per-service разделы** для каждого SVC-N из Design:
   - Acceptance-сценарии — таблица TC-N
   - Тестовые данные — таблица fixtures (или заглушка)
3. **Системные тест-сценарии** — таблица TC-N для STS-N из Design (или заглушка)
4. **Матрица покрытия** — трассируемость REQ-N/STS-N → TC-N

**Порядок per-service:** как в Design (Основной → Вторичный → Новый).

**Нумерация TC-N:** сквозная по документу, сначала per-service, затем системные.

**Маркеры:** Если информации недостаточно — ставить `[ТРЕБУЕТ УТОЧНЕНИЯ: вопрос]`.

**Upward feedback:** Если при генерации обнаружена информация, затрагивающая Design или Discussion:
1. Сохранить plan-test.md в текущем виде, поставить маркер `[ТРЕБУЕТ УТОЧНЕНИЯ: upward feedback — ожидается обновление Design]`
2. Обновить Design (статус остаётся WAITING), проверить Discussion
3. Дождаться подтверждения пользователя
4. Продолжить генерацию Plan Tests

**Разрешение маркеров (обязательно перед продолжением):**

После заполнения всех разделов:
1. Проверить документ на наличие `[ТРЕБУЕТ УТОЧНЕНИЯ]` маркеров
2. Если маркеры есть — для каждого маркера уточнить через AskUserQuestion
3. Заменить маркеры на ответы пользователя
4. Повторять пока маркеров = 0

### Шаг 7: Регистрация в README

Обновить запись в `specs/analysis/README.md` — колонка Plan Tests:

```markdown
| NNNN | {topic} | WAITING | ... | plan-test.md | vX.Y.Z | {Описание} |
```

### Шаг 8: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-plan-test.py specs/analysis/NNNN-{topic}/plan-test.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-plan-test.md](./validation-plan-test.md).

Исправить ошибки до продолжения.

### Шаг 9: Ревью пользователем

**Перед вопросом:** проверить что маркеров = 0 и валидация пройдена. Если нет — вернуться к шагу 6.

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: «План тестов готов. Всё корректно?»

| Ответ | Действие |
|-------|----------|
| Да, всё корректно | Перевести DRAFT → WAITING через `chain_status.py` (см. ниже) → отчёт |
| Нет, нужны правки | Внести изменения → продолжить с шага 8 |

**Переход DRAFT → WAITING** — через модуль `chain_status.py` (SSOT статусов):

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="WAITING", document="plan-test")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

- `result.auto_propose` — предложение следующего шага (`/plan-dev-create NNNN`)

### Шаг 10: Отчёт о выполнении

Вывести отчёт:

```
## Отчёт о создании плана тестов

Создан план тестов: `specs/analysis/NNNN-{topic}/plan-test.md`

Описание: {description}

Milestone: {vX.Y.Z}

Сервисы:
- {Сервис 1}: {N} TC-N
- ...

Системные тесты: {N} TC-N
Всего TC-N: {итого}

Покрытие:
- REQ-N: {X}/{Y} (100%)
- STS-N: {X}/{Y} (100%)

Статус: DRAFT → WAITING

Следующий шаг: Создать Plan Dev

Валидация: пройдена
```

### Шаг 11: Авто-предложение следующего этапа

AskUserQuestion: «Перейти к созданию Plan Dev?»

| Ответ | Действие |
|-------|----------|
| Да | Вызвать воркфлоу создания Plan Dev с путём к текущему Plan Tests |
| Нет | Завершить воркфлоу |

---

## Чек-лист

### Подготовка
- [ ] Parent Design в статусе WAITING
- [ ] Файл создан из шаблона
- [ ] Frontmatter заполнен (базовые поля, milestone из Discussion)

### Источники
- [ ] Design прочитан целиком (SVC-N, INT-N, STS-N)
- [ ] Discussion прочитана (REQ-N)
- [ ] docs/{svc}.md прочитаны (AS IS)
- [ ] docs/.system/testing.md прочитан (стратегия)

### Clarify
- [ ] Clarify проведён (или `--auto-clarify`)
- [ ] Типы тестов определены
- [ ] Edge cases определены

### Содержание
- [ ] Резюме заполнено (scope, покрытие, ключевые решения)
- [ ] Per-service разделы для каждого SVC-N
- [ ] Acceptance-сценарии — таблицы TC-N
- [ ] Тестовые данные — таблицы fixtures (или заглушки)
- [ ] Системные тест-сценарии — TC-N для STS-N (или заглушка)
- [ ] Матрица покрытия — 100% REQ-N и STS-N
- [ ] Все маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` разрешены (0 неразрешённых)

### Проверка
- [ ] Валидация пройдена (скрипт или чек-лист)
- [ ] Запись обновлена в README
- [ ] Ревью пользователем пройдено
- [ ] Статус переведён в WAITING
- [ ] README обновлён (статус WAITING)
- [ ] Отчёт выведен
- [ ] Авто-предложение следующего этапа (Plan Dev)

---

## Примеры

### Создание Plan Tests для OAuth2

```
Пользователь: "Создать Plan Tests для OAuth2 авторизации"

1. Parent: specs/analysis/0001-oauth2-authorization/design.md → WAITING ✓
2. Файл создан из шаблона → plan-test.md
3. Frontmatter: status=DRAFT, parent=design.md, milestone=v1.2.0
4. Источники: Design (SVC-1..3, INT-1..4, STS-1..3) + Discussion (REQ-1..5) + docs/ + testing.md
5. Clarify: load-тесты — да, edge cases refresh — 3 варианта
6. Разделы: auth (TC-1..7), gateway (TC-8..9), users (TC-10..11), системные (TC-12..14)
   → Матрица: REQ-1..5 покрыты, STS-1..3 покрыты → OK
   → Маркеров: 0 → OK
7. README обновлён
8. Валидация → OK
9. Ревью: "Да" → DRAFT → WAITING
10. Отчёт: 3 сервиса, 14 TC-N, 100% покрытие
11. "Создать Plan Dev?" → Да
```

### Создание с --auto-clarify

```
Пользователь: "Создать Plan Tests для 0003-cache-optimization, --auto-clarify"

1. Parent: design.md → WAITING ✓
2-3. Файл + frontmatter
4. Источники: Design (SVC-1) + Discussion (REQ-1..2) + docs/ + testing.md
5. Clarify пропущен — маркеры на неясности
6. Разделы: catalog (TC-1..4) + заглушка системных
   → Разрешение маркеров: AskUserQuestion → замена → 0 маркеров
7-8. README + Валидация
9. Ревью → WAITING
10. Отчёт
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-analysis-plan-test.py](../../.scripts/validate-analysis-plan-test.py) | Валидация созданного документа (шаг 8) | [validation-plan-test.md](./validation-plan-test.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/plan-test-create](/.claude/skills/plan-test-create/SKILL.md) | Создание документа плана тестов | Этот документ |
