---
description: Воркфлоу создания документа плана тестов SDD — чтение Design, Clarify, генерация TC-N/fixtures/матрицы покрытия, валидация, перевод DRAFT → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.4
index: specs/.instructions/README.md
---

# Воркфлоу создания плана тестов

Рабочая версия стандарта: 1.4

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
  - [Шаг 2: Создать файл скриптом](#шаг-2-создать-файл-скриптом)
  - [Шаг 3: Определить scope](#шаг-3-определить-scope)
  - [Шаг 4: Clarify](#шаг-4-clarify)
  - [Шаг 5: plantest-agent](#шаг-5-plantest-agent)
  - [Шаг 6: plantest-reviewer](#шаг-6-plantest-reviewer)
  - [Шаг 7: Исправления](#шаг-7-исправления)
  - [Шаг 8: README и валидация](#шаг-8-readme-и-валидация)
  - [Шаг 9: Ревью пользователем](#шаг-9-ревью-пользователем)
  - [Шаг 10: Отчёт и авто-предложение](#шаг-10-отчёт-и-авто-предложение)
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

### Шаг 2: Создать файл скриптом

**SSOT:** [standard-plan-test.md § 7](./standard-plan-test.md#7-шаблон)

Создать файл с заполненным frontmatter и пустыми per-service секциями:

```bash
python specs/.instructions/.scripts/create-analysis-plan-test-file.py NNNN-{topic}
```

Скрипт автоматически:
- Читает milestone из parent Discussion (fallback — из Design)
- Извлекает SVC-N заголовки из Design (для пустых per-service секций)
- Создаёт `specs/analysis/NNNN-{topic}/plan-test.md` с frontmatter (status=DRAFT, standard-version=v1.3) и пустыми секциями

**При ошибке скрипта:** проверить что Design в WAITING, папка цепочки существует, plan-test.md не существует.

### Шаг 3: Определить scope

Оркестратор извлекает минимальный контекст для Clarify и промпта агента:

| # | Что извлечь | Откуда |
|---|-------------|--------|
| 1 | Список SVC-N (имена сервисов) | Заголовки `## SVC-N:` из Design |
| 2 | Список STS-N | Таблица STS-N из Design |
| 3 | Список REQ-N | Нумерованные требования из Discussion |
| 4 | Список INT-N | Заголовки `## INT-N:` из Design |

**Discussion без REQ-N:** Если Discussion не содержит пронумерованных REQ-N — поставить маркер `[ТРЕБУЕТ УТОЧНЕНИЯ: Discussion не содержит REQ-N — невозможно построить матрицу покрытия]`.

**Примечание:** Оркестратор НЕ читает документы целиком — только извлекает ID и названия. Полное чтение — задача plantest-agent.

### Шаг 4: Clarify

**SSOT:** [standard-plan-test.md § 6](./standard-plan-test.md#6-clarify), [Стандарт analysis/ § 8](../standard-analysis.md#8-clarify-и-блокирующие-правила)

> **Оркестратор проводит Clarify** до запуска агента — ответы передаются агенту в промпте.

**Если `--auto-clarify` НЕ указан:**

LLM **сам предлагает** и уточняет через AskUserQuestion:

| Что предлагает LLM | Пример |
|---------------------|--------|
| Полнота типов тестов | «Какие из 5 типов (unit, integration, e2e, load, smoke) применимы? Предлагаю: unit + integration + e2e. Load — нет (нет SLA). Smoke — нет (нет деплоя)» |
| Покрытие | «REQ-3 (rate limiting) — достаточно ли одного e2e теста?» |
| Тестовые данные | «Какие edge cases для refresh-токена? Истёкший, отозванный, невалидный?» |
| Граничные кейсы | «Тестировать ли concurrent refresh (два запроса одновременно)?» |
| Мокирование | «Для интеграционных тестов auth: мокировать users-сервис или поднимать?» |

**Если `--auto-clarify` указан:**

LLM пропускает Clarify, генерирует документ на основе источников и ставит маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` на все неясности.

### Шаг 5: plantest-agent

Запустить агента генерации содержимого:

```
Task tool:
  subagent_type: plantest-agent
  prompt: |
    Заполни содержимое plan-test.md.

    Документ: specs/analysis/NNNN-{topic}/plan-test.md
    Design: specs/analysis/NNNN-{topic}/design.md
    Discussion: specs/analysis/NNNN-{topic}/discussion.md

    Сервисы: {список SVC-N из Шага 3}
    STS-N: {список STS-N из Шага 3}
    REQ-N: {список REQ-N из Шага 3}

    Ответы Clarify:
    {ответы из Шага 4}

    ОБЯЗАТЕЛЬНО: оценить применимость ВСЕХ 5 типов тестов (unit, integration,
    e2e, load, smoke) на основе testing.md. Для каждого неприменимого типа —
    записать обоснование в Резюме.
```

**Агент самостоятельно:**
1. Читает Design, Discussion, specs/docs/{svc}.md, testing.md
2. Оценивает применимость всех 5 типов тестов (unit, integration, e2e, load, smoke)
3. Генерирует TC-N, fixtures, матрицу покрытия, блоки тестирования
4. Записывает в plan-test.md инкрементально через Edit

**По завершении:** агент возвращает резюме (кол-во TC, покрытие, маркеры).

### Шаг 6: plantest-reviewer

Запустить ревьюера для проверки и записи замечаний:

```
Task tool:
  subagent_type: plantest-reviewer
  prompt: |
    Проверь plan-test.md на полноту и корректность.
    Запиши замечания как PROP-N в секцию "Предложения".

    Документ: specs/analysis/NNNN-{topic}/plan-test.md
    Design: specs/analysis/NNNN-{topic}/design.md
    Discussion: specs/analysis/NNNN-{topic}/discussion.md
```

**Ревьюер проверяет 7 критериев:**
1. Покрытие REQ-N (каждый REQ → ≥ 1 TC)
2. Покрытие STS-N (каждый STS → ≥ 1 TC)
3. Согласованность SVC-N (каждый SVC имеет per-service раздел)
4. Формат TC-N (естественные предложения, типы, источники)
5. Fixtures (каждый упомянутый fixture существует)
6. BLOCK-N (каждый TC принадлежит блоку)
7. Антигаллюцинации (нет MISSING/INVENTED/DISTORTED)

**Результат:** PROP-N записаны в plan-test.md → секция "Предложения". Вердикт по PROP-N: нет P1 и ≤ 2 P2 → ACCEPT. Иначе REVISE.

### Шаг 7: Исправления

**Если ACCEPT:** классифицировать и обработать PROP-N (оркестратор, НЕ агент):
   **Классификация предложений** (перед обработкой):
   Для каждого PROP определить тип:
   | Тип | Критерий | Действие |
   |-----|----------|----------|
   | **Формальный** | Очевидное уточнение, идемпотентность, safety, единственный разумный вариант | Принять автоматически |
   | **Решение** | Есть несколько разумных вариантов, требуется выбор пользователя | AskUserQuestion с рекомендацией |
   - Формальные PROP: применить все, показать пользователю список "Автоматически приняты: PROP-X, PROP-Y, PROP-Z"
   - Решения: обрабатывать пачками по 4 через AskUserQuestion, рекомендованный вариант первым + "(рекомендуется)"
   **Обработка:**
   - PROP-N типа "Решение" обрабатываются пачками по 4 через AskUserQuestion (лимит инструмента — 4 вопроса)
   - Каждый AskUserQuestion содержит до 4 PROP с вариантами (принять / отклонить), рекомендованный вариант первым + "(рекомендуется)"
   - Если PROP больше 4 — следующая пачка после ответа на предыдущую
   - **ВАЖНО: обрабатывать PROP по одному через Edit, НЕ заменять секцию «Предложения» целиком.**
     Для каждого PROP после получения ответа:
     - Принятый PROP:
       (a) применить основную правку к содержимому документа
       (b) Grep по документу на все связанные термины/секции из правки
       (c) распространить изменение на все затронутые места (TC-N, fixtures, матрица покрытия, блоки тестирования)
       (d) удалить строку PROP из секции «Предложения»
     - Отклонённый PROP: (a) удалить строку PROP из секции «Предложения», (b) добавить в секцию «Отвергнутые предложения» (с указанием причины)
   - После обработки всех PROP: оставить секцию с текстом `_Все предложения обработаны._`. Секция «Отвергнутые предложения» сохраняется.
   Перейти к шагу 8.

**Если REVISE:** перезапуск plantest-agent с PROP-N из документа (макс 3 итерации):

1. Прочитать P1/P2 PROP-N из секции "Предложения" plan-test.md
2. Передать P1/P2 PROP-N в промпт plantest-agent
3. Запустить plantest-agent (исправления)
4. Запустить plantest-reviewer (повторная проверка, новые PROP-N)
5. Если снова REVISE и итерации < 3 — повторить
6. Если итерации ≥ 3 и REVISE — предупредить пользователя, перейти к ручной правке
7. После финального ACCEPT: обработать PROP-N пачками по 4 через AskUserQuestion (принять/отклонить каждый). Отклонённые → "Отвергнутые предложения" (с причиной). Применить принятые через Edit.

**Разрешение маркеров (обязательно перед продолжением):**

После завершения волн:
1. Проверить документ на наличие `[ТРЕБУЕТ УТОЧНЕНИЯ]` маркеров
2. Если маркеры есть — для каждого маркера уточнить через AskUserQuestion
3. Заменить маркеры на ответы пользователя
4. Повторять пока маркеров = 0

### Шаг 8: README и валидация

**README:** Обновить запись в `specs/analysis/README.md` — колонка Plan Tests:

```markdown
| NNNN | {topic} | WAITING | ... | plan-test.md | vX.Y.Z | {Описание} |
```

**Валидация:**

```bash
python specs/.instructions/.scripts/validate-analysis-plan-test.py specs/analysis/NNNN-{topic}/plan-test.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-plan-test.md](./validation-plan-test.md).

Исправить ошибки до продолжения.

### Шаг 9: Ревью пользователем

**Перед вопросом:** проверить что маркеров = 0 и валидация пройдена. Если нет — вернуться к шагу 7.

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

### Шаг 10: Отчёт и авто-предложение

Вывести отчёт:

```
## Отчёт о создании плана тестов

Создан план тестов: `specs/analysis/NNNN-{topic}/plan-test.md`

Описание: {description}

Milestone: {vX.Y.Z}

Сервисы:
- SVC-1: {сервис 1}: {N} TC-N
- ...

Системные тесты: {N} TC-N
Всего TC-N: {итого}

Покрытие:
- REQ-N: {X}/{Y} (100%)
- STS-N: {X}/{Y} (100%)

Волны: {N} итераций (ACCEPT на волне {N})

Статус: DRAFT → WAITING

Следующий шаг: Создать Plan Dev

Валидация: пройдена
```

AskUserQuestion: «Перейти к созданию Plan Dev?»

| Ответ | Действие |
|-------|----------|
| Да | Вызвать воркфлоу создания Plan Dev с путём к текущему Plan Tests |
| Нет | Завершить воркфлоу |

---

## Чек-лист

### Подготовка
- [ ] Parent Design в статусе WAITING
- [ ] Файл создан скриптом (`create-analysis-plan-test-file.py`)
- [ ] Scope определён (SVC-N, STS-N, REQ-N, INT-N)

### Clarify
- [ ] Clarify проведён (или `--auto-clarify`)
- [ ] Типы тестов определены
- [ ] Edge cases определены

### Агенты
- [ ] Волна 1: plantest-agent завершён (TC-N, fixtures, матрица, блоки)
- [ ] Волна 2: plantest-reviewer — вердикт ACCEPT
- [ ] Волна 3: исправления (если REVISE, макс 3 итерации)
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
2. Файл создан скриптом → plan-test.md (frontmatter + пустые секции SVC-1..3)
3. Scope: SVC-1..3, INT-1..4, STS-1..3, REQ-1..5
4. Clarify: load-тесты — да, edge cases refresh — 3 варианта
5. Волна 1: plantest-agent → SVC-1: auth (TC-1..7), SVC-2: gateway (TC-8..9),
   SVC-3: users (TC-10..11), системные (TC-12..14), матрица, блоки
6. Волна 2: plantest-reviewer → ACCEPT (покрытие 100%, формат OK)
7. Исправления — не требуются
8. README + Валидация → OK
9. Ревью: "Да" → DRAFT → WAITING
10. Отчёт: 3 сервиса, 14 TC-N, 100% покрытие → "Создать Plan Dev?" → Да
```

### Создание с --auto-clarify

```
Пользователь: "Создать Plan Tests для 0003-cache-optimization, --auto-clarify"

1. Parent: design.md → WAITING ✓
2. Файл создан скриптом → plan-test.md (пустые секции SVC-1)
3. Scope: SVC-1, REQ-1..2
4. Clarify пропущен — маркеры на неясности
5. Волна 1: plantest-agent → SVC-1: catalog (TC-1..4) + системные (заглушка)
6. Волна 2: plantest-reviewer → REVISE (REQ-2 не покрыт)
7. Волна 3: plantest-agent (исправления) → plantest-reviewer → ACCEPT
   → Разрешение маркеров: AskUserQuestion → замена → 0 маркеров
8-9. README + Валидация + Ревью → WAITING
10. Отчёт
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [create-analysis-plan-test-file.py](../../.scripts/create-analysis-plan-test-file.py) | Создание файла с frontmatter и пустыми секциями (шаг 2) | Этот документ |
| [validate-analysis-plan-test.py](../../.scripts/validate-analysis-plan-test.py) | Валидация созданного документа (шаг 8) | [validation-plan-test.md](./validation-plan-test.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/plan-test-create](/.claude/skills/plan-test-create/SKILL.md) | Создание документа плана тестов | Этот документ |
