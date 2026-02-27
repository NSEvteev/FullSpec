# Plan Tests — агент, ревьюер, исправления стандарта

Делегирование создания plan-test.md агенту (plantest-agent + plantest-reviewer) по паттерну design-agent. Исправление 5 проблем стандарта/валидатора, обнаруженных при тестовом прогоне на цепочке 0001-task-dashboard. Скрипт создания файла-заглушки.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблемы](#1-проблемы)
  - [2. Решение: plantest-agent + plantest-reviewer](#2-решение-plantest-agent--plantest-reviewer)
  - [3. Исправления стандарта](#3-исправления-стандарта)
  - [4. Исправления валидатора](#4-исправления-валидатора)
  - [5. Скрипт create-analysis-plan-test-file.py](#5-скрипт-create-analysis-plan-test-filepy)
  - [6. Изменения в инструкциях plan-test/](#6-изменения-в-инструкциях-plan-test)
  - [7. Изменения в процессных стандартах](#7-изменения-в-процессных-стандартах)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** При тестовом прогоне `/plan-test-create 0001-task-dashboard` выявлено 5 проблем: стандарт/валидатор отвергают корректные тест-кейсы, формат заголовков не согласован с Design, основной LLM тратит контекст на генерацию 39 TC-N inline, нет скрипта создания файла.

**Почему:** Стандарт plan-test создавался теоретически, без реального прогона. Первый тестовый прогон обнажил рассогласования между стандартом, валидатором и реальной структурой документов.

**Связанные файлы:**

Инструкции plan-test/ (4 файла — все будут обновлены):
- [standard-plan-test.md](/specs/.instructions/analysis/plan-test/standard-plan-test.md) — стандарт Plan Tests
- [create-plan-test.md](/specs/.instructions/analysis/plan-test/create-plan-test.md) — воркфлоу создания
- [validation-plan-test.md](/specs/.instructions/analysis/plan-test/validation-plan-test.md) — воркфлоу валидации
- [modify-plan-test.md](/specs/.instructions/analysis/plan-test/modify-plan-test.md) — воркфлоу модификации

Валидатор:
- [validate-analysis-plan-test.py](/specs/.instructions/.scripts/validate-analysis-plan-test.py) — скрипт валидации (3 бага)

Паттерны (для агентов):
- [design-agent-first AGENT.md](/.claude/agents/design-agent-first/AGENT.md) — паттерн агента
- [design-reviewer AGENT.md](/.claude/agents/design-reviewer/AGENT.md) — паттерн ревьюера

Паттерн (для скрипта):
- [create-review-file.py](/specs/.instructions/.scripts/create-review-file.py) — паттерн скрипта создания файла
- [create-analysis-design-file.py](/specs/.instructions/.scripts/create-analysis-design-file.py) — аналогичный скрипт для Design

Процессные стандарты (ссылки на агентов):
- [standard-process.md](/specs/.instructions/standard-process.md) — строка 428, колонка "Агент": `—`
- [standard-analysis.md](/specs/.instructions/analysis/standard-analysis.md) — § 2.2, § 2.4, строка 230

Оркестратор chain:
- [create-chain.md](/specs/.instructions/create-chain.md) — TASK 3 description (строки 160-166)

Ссылка на Design:
- [standard-design.md](/specs/.instructions/analysis/design/standard-design.md) — Design заголовки `## SVC-N: {name}`

---

## Содержание

### 1. Проблемы

**P-1. PT015: Source требует REQ-N/STS-N для ВСЕХ TC — слишком строго**

Текущее правило в standard-plan-test.md § 5:
> Источник: **Обязательно:** REQ-N и/или STS-N. Опционально: SVC-N § K, INT-N.

При реальном прогоне обнаружено: edge-case тесты (невалидный приоритет → 400, GET несуществующего ID → 404, верификация JWT jose) не имеют прямого REQ-N. Они вытекают из Design (SVC-N § 2 API контракты, SVC-N § 3 Data Model), а не из Discussion.

**Примеры TC без REQ-N:**
| TC | Описание | Естественный источник |
|----|----------|---------------------|
| TC-3 | POST с невалидным priority ("urgent") → 400 | SVC-1 § 3 (Data Model: CHECK constraint) |
| TC-7 | GET несуществующего ID → 404 | SVC-1 § 2 (API: Errors 404) |
| TC-12 | POST с assigneeId → задача с assigneeId | SVC-1 § 2 (API: assigneeId optional) |
| TC-17 | Верификация валидного JWT через jose | SVC-2 § 4 (Потоки: JWT-валидация) |

Текущий стандарт вынуждает искусственно привязывать такие TC к REQ-N ("REQ-1 покрывает все edge cases создания" — размывает смысл REQ).

---

**P-2. PT027: Валидатор не парсит диапазон `TC-N..TC-M`**

Стандарт § 5 → Блоки тестирования содержит пример:
```
| BLOCK-1 | TC-1..TC-7 | auth | BLOCK-1 |
```

Валидатор (`check_blocks`, строка 431) использует:
```python
tc_nums = [int(m) for m in re.findall(r'TC-(\d+)', tc_str)]
```

Это находит только `TC-1` и `TC-7` из строки `TC-1..TC-7`, пропуская TC-2..TC-6. Результат: 31 TC "не принадлежит ни одному BLOCK-N".

---

**P-3. PT010/PT011: Валидатор считает "Блоки тестирования" сервисом**

Функция `check_per_service_sections` (строка 328) определяет special-секции:
```python
special = {"Резюме", "Системные тест-сценарии", "Матрица покрытия"}
```

**"Блоки тестирования" отсутствует в этом множестве.** Результат: секция `## Блоки тестирования` проверяется как per-service — и падает на отсутствии подсекций "Acceptance-сценарии" и "Тестовые данные".

---

**P-4. Несогласованность заголовков per-service: Design vs Plan Tests**

Design использует формат `## SVC-N: {name}` (пример: `## SVC-1: task`).
Standard-plan-test.md § 5 задаёт `## {Имя сервиса}` (пример: `## task`).

Это рассогласование:
- Затрудняет навигацию между документами
- Ломает автоматический маппинг "SVC-N в Design → per-service в Plan Tests"
- Валидатор не может проверить, что каждый SVC-N из Design имеет раздел в Plan Tests

---

**P-5. Основной LLM создаёт Plan Tests inline — дорого по контексту**

Текущий workflow (create-plan-test.md):
1. Основной LLM читает 6 источников (Design ~800 строк, Discussion ~70 строк, testing.md ~100 строк)
2. Основной LLM проводит Clarify
3. Основной LLM генерирует все TC-N, fixtures, матрицу, блоки
4. Основной LLM валидирует

**Проблемы:**
- Основной LLM тратит контекст на чтение больших документов и генерацию десятков TC
- Нет разделения "генерация" и "проверка" (как в design-agent/design-reviewer)
- При 39 TC для 3 сервисов — LLM может галлюцинировать (путать REQ-N, терять TC, дублировать fixtures)
- Нет специализированного ревью покрытия (каждый REQ-N и STS-N покрыт?)

**Паттерн уже решён:** Design использует design-agent-first + design-agent-second + design-reviewer. Docs Sync использует service-agent + service-reviewer. Нужно применить тот же паттерн.

---

**P-6. Нет скрипта создания файла-заглушки**

Design имеет `create-analysis-design-file.py`, review имеет `create-review-file.py`. Plan Tests создаётся вручную — LLM копирует шаблон из стандарта и заполняет frontmatter через Write. Это медленнее и подвержено ошибкам.

---

### 2. Решение: plantest-agent + plantest-reviewer

#### 2.1 plantest-agent (NEW)

**Роль:** Создание содержимого plan-test.md — чтение источников, генерация TC-N, fixtures, матрица покрытия, блоки тестирования.

**Паттерн:** Аналог design-agent-second — получает готовый файл с frontmatter + пустыми секциями, заполняет содержимое.

**Входные данные (из промпта оркестратора):**
- Путь к plan-test.md (уже создан скриптом с frontmatter + пустыми секциями)
- Путь к design.md
- Путь к discussion.md
- Ответы Clarify (из AskUserQuestion оркестратора)
- Список сервисов (SVC-1: task, SVC-2: auth, ...)
- Список STS-N из Design

**Что делает:**
1. Читает Design (SVC-N, INT-N, STS-N)
2. Читает Discussion (REQ-N)
3. Читает specs/docs/{svc}.md (AS IS, если существуют)
4. Читает specs/docs/.system/testing.md (стратегия)
5. Генерирует per-service TC-N (unit + integration)
6. Генерирует системные TC-N (e2e + load)
7. Заполняет fixtures для каждого сервиса
8. Строит матрицу покрытия (REQ-N/STS-N → TC-N)
9. Формирует блоки тестирования (BLOCK-N)
10. Записывает всё в plan-test.md

**Конфигурация:**
| Поле | Значение |
|------|----------|
| type | general-purpose |
| model | sonnet |
| tools | Read, Grep, Glob, Edit, Write |
| max_turns | 40 |

#### 2.2 plantest-reviewer (NEW)

**Роль:** Проверка plan-test.md на полноту покрытия, корректность формата, согласованность с Design.

**Паттерн:** Аналог design-reviewer — читает документ и записывает замечания.

**Что проверяет:**
1. **Покрытие REQ-N:** каждый REQ-N из Discussion покрыт ≥ 1 TC-N в матрице
2. **Покрытие STS-N:** каждый STS-N из Design покрыт ≥ 1 TC-N
3. **Согласованность SVC-N:** каждый SVC-N из Design имеет per-service раздел
4. **Формат TC-N:** естественные предложения, типы, источники
5. **Fixtures:** каждый fixture из TC-N существует в "Тестовые данные"
6. **BLOCK-N:** каждый TC-N принадлежит блоку, системные TC в отдельном BLOCK
7. **Антигаллюцинации:** TC-N не содержат информацию, отсутствующую в Design/Discussion (MISSING/INVENTED/DISTORTED)

**Вердикт:** ACCEPT или REVISE + список расхождений.

**Конфигурация:**
| Поле | Значение |
|------|----------|
| type | general-purpose |
| model | sonnet |
| tools | Read, Grep, Glob |
| max_turns | 20 |

#### 2.3 Обновлённый workflow create-plan-test.md

**Было (11 шагов, основной LLM):**
```
1. Check Design WAITING
2. Create file from template     ← LLM вручную копирует шаблон
3. Fill frontmatter              ← LLM заполняет поля
4. Read 6 sources                ← LLM читает ~1000 строк
5. Clarify (AskUserQuestion)
6. Fill sections (TC-N)          ← LLM генерирует 30-40 TC
7. README
8. Validate
9. User review
10. Report
11. Auto-propose
```

**Стало (11 шагов, оркестратор + скрипт + агенты):**
```
1. Check Design WAITING          ← оркестратор
2. Создать файл скриптом         ← NEW: create-analysis-plan-test-file.py (frontmatter + пустые секции)
3. Определить scope              ← оркестратор (список SVC-N, STS-N, REQ-N из Design/Discussion)
4. Clarify (AskUserQuestion)     ← оркестратор (интерактив с пользователем)
5. Волна 1: plantest-agent       ← агент (генерация TC-N, fixtures, матрица, блоки)
6. Волна 2: plantest-reviewer    ← ревьюер (проверка покрытия и формата)
7. Волна 3: исправления          ← при REVISE: перезапуск агента (макс 3 итерации)
8. README + Validate             ← оркестратор
9. User review + WAITING         ← оркестратор (блокирующее)
10. Report                       ← оркестратор
11. Auto-propose                 ← оркестратор
```

**Ключевые отличия:**
- Шаги 2+3 (файл + frontmatter) → один шаг с Python-скриптом (как create-review-file.py)
- Шаг 4 (чтение 6 источников) → шаг 3 "Определить scope" (оркестратор только извлекает список SVC-N/STS-N/REQ-N, не читает полностью)
- Шаги 6-8 (генерация + валидация) → шаги 5-7 (агент → ревьюер → исправления)
- Один агент генерации (не два как у Design) — нет фазы "выбор технологий"

---

### 3. Исправления стандарта

#### И-1. Source: ослабить правило PT015

**Было** (standard-plan-test.md § 5, колонка Источник):
> Обязательно: REQ-N и/или STS-N. Опционально: SVC-N § K (если вытекает из конкретной подсекции) или INT-N

**Стало:**
> Обязательно ≥ 1 из: REQ-N, STS-N, SVC-N § K, INT-N. Предпочтительно REQ-N/STS-N для трассируемости; SVC-N § K или INT-N допустимы для edge-case/граничных тестов, не привязанных к конкретному требованию.

**Влияние на матрицу покрытия:** Матрица покрытия по-прежнему требует 100% покрытие REQ-N и STS-N. Но TC с источником только SVC-N § K/INT-N не обязаны быть в матрице — они покрывают проектные решения, а не требования.

**Файлы:**
- standard-plan-test.md § 5 → колонка Источник
- validation-plan-test.md → Шаг 5 → колонка Источник
- validate-analysis-plan-test.py → check_tc_format → PT015

---

#### И-2. Per-service заголовки: `## SVC-N: {name}`

**Было** (standard-plan-test.md § 5):
> Заголовок: `## {Имя сервиса}`

**Стало:**
> Заголовок: `## SVC-N: {имя сервиса}` — совпадает с заголовком в Design.

**Примеры:**
```
## SVC-1: task       ← Plan Tests (было: ## task)
## SVC-2: auth       ← Plan Tests (было: ## auth)
## SVC-3: frontend   ← Plan Tests (было: ## frontend)
```

**Влияние:**
- Навигация: `## SVC-1: task` в Design → `## SVC-1: task` в Plan Tests (1:1 маппинг)
- Валидатор: может автоматически проверить, что все SVC-N из Design присутствуют
- Шаблон § 7: обновить `{Сервис 1}` → `SVC-1: {сервис 1}`

**Файлы:**
- standard-plan-test.md § 5 → заголовок, шаблон § 7, примеры § 9
- validation-plan-test.md → Шаг 5
- validate-analysis-plan-test.py → check_per_service_sections (regex для SVC-N)
- create-plan-test.md → примеры
- modify-plan-test.md → примеры CONFLICT

---

### 4. Исправления валидатора

#### В-1. Баг: "Блоки тестирования" не в special set (PT010/PT011)

**Файл:** validate-analysis-plan-test.py, строка 328

**Было:**
```python
special = {"Резюме", "Системные тест-сценарии", "Матрица покрытия"}
```

**Стало:**
```python
special = {"Резюме", "Системные тест-сценарии", "Матрица покрытия", "Блоки тестирования"}
```

---

#### В-2. Баг: Range `TC-N..TC-M` не парсится (PT027)

**Файл:** validate-analysis-plan-test.py, строка 431

**Было:**
```python
tc_nums = [int(m) for m in re.findall(r'TC-(\d+)', tc_str)]
```

**Стало:**
```python
def expand_tc_range(tc_str: str) -> list[int]:
    """Раскрыть TC-N..TC-M в список TC номеров."""
    result = []
    # Найти диапазоны TC-N..TC-M
    for match in re.finditer(r'TC-(\d+)\.\.TC-(\d+)', tc_str):
        start, end = int(match.group(1)), int(match.group(2))
        result.extend(range(start, end + 1))
    # Найти одиночные TC-N (не внутри диапазонов)
    cleaned = re.sub(r'TC-\d+\.\.TC-\d+', '', tc_str)
    result.extend(int(m) for m in re.findall(r'TC-(\d+)', cleaned))
    return result

tc_nums = expand_tc_range(tc_str)
```

---

#### В-3. PT015: ослабить проверку Source

**Файл:** validate-analysis-plan-test.py, строка 385-388

**Было:**
```python
has_req = bool(re.search(r'REQ-\d+', source))
has_sts = bool(re.search(r'STS-\d+', source))
if not has_req and not has_sts:
    errors.append(("PT015", f"TC-{tc_num}: нет REQ-N или STS-N в источнике"))
```

**Стало:**
```python
has_req = bool(re.search(r'REQ-\d+', source))
has_sts = bool(re.search(r'STS-\d+', source))
has_svc = bool(re.search(r'SVC-\d+', source))
has_int = bool(re.search(r'INT-\d+', source))
if not has_req and not has_sts and not has_svc and not has_int:
    errors.append(("PT015", f"TC-{tc_num}: нет источника (REQ-N, STS-N, SVC-N или INT-N)"))
```

#### В-4. Heading regex для SVC-N: {name}

**Файл:** validate-analysis-plan-test.py → check_per_service_sections

Обновить regex для per-service заголовков: вместо `## {name}` → `## SVC-N: {name}`. Валидатор должен:
- Парсить формат `## SVC-\d+: .+`
- Проверять, что каждый SVC-N из parent Design присутствует в Plan Tests

---

### 5. Скрипт create-analysis-plan-test-file.py

**Новый скрипт** по паттерну [create-review-file.py](/specs/.instructions/.scripts/create-review-file.py).

**Что делает:**
1. Принимает аргумент `<branch>` (= имя папки `NNNN-{topic}`)
2. Читает frontmatter parent design.md через ChainManager
3. Извлекает milestone из parent Discussion
4. Извлекает список SVC-N из Design (для генерации пустых per-service секций)
5. Создаёт файл `specs/analysis/{branch}/plan-test.md` с:
   - Заполненный frontmatter (description-заглушка, standard, standard-version, index, parent, children, status=DRAFT, milestone)
   - Заголовок `# NNNN: {Тема} — Plan Tests`
   - Пустые секции: `## Резюме`, `## SVC-N: {name}` (для каждого SVC из Design), `## Системные тест-сценарии`, `## Матрица покрытия`, `## Блоки тестирования`
   - Пустые подсекции per-service: `### Acceptance-сценарии`, `### Тестовые данные`

**Использование:**
```bash
python specs/.instructions/.scripts/create-analysis-plan-test-file.py 0001-task-dashboard
python specs/.instructions/.scripts/create-analysis-plan-test-file.py 0001-task-dashboard --milestone v0.1.0
```

**Возвращает:**
- 0 — файл создан
- 1 — ошибка (файл существует, папка не найдена, нет design.md)

**Зависимости:** chain_status.ChainManager (для чтения frontmatter, как в create-review-file.py)

---

### 6. Изменения в инструкциях plan-test/

#### 6.1 standard-plan-test.md

| Секция | Изменение |
|--------|-----------|
| § 5 колонка Источник | И-1: `≥ 1 из REQ-N, STS-N, SVC-N § K, INT-N` |
| § 5 per-service заголовок | И-2: `## SVC-N: {имя сервиса}` |
| § 5 Матрица покрытия | Уточнение: TC с источником только SVC-N/INT-N не обязаны быть в матрице |
| § 7 Шаблон | Обновить `{Сервис 1}` → `SVC-1: {сервис 1}`, Source → пример с SVC-N |
| § 8 Чек-лист | Source: обновить формулировку |
| § 9 Примеры | `## auth` → `## SVC-1: auth`, Source обновить |
| Версия стандарта | 1.2 → 1.3, standard-version: v1.2 → v1.3 |
| Секция "Скрипты" | Добавить create-analysis-plan-test-file.py |

#### 6.2 create-plan-test.md

| Секция | Изменение |
|--------|-----------|
| Шаг 2 | "Создать файл из шаблона" → "Создать файл скриптом": `python create-analysis-plan-test-file.py {branch}` |
| Шаг 3 | "Заполнить frontmatter" → **удалить** (скрипт заполняет) |
| Шаг 4 | "Прочитать источники" → "Определить scope" (извлечь SVC-N, STS-N, REQ-N — не читать полностью) |
| Шаг 5 | Clarify — без изменений (оркестратор, AskUserQuestion) |
| Шаг 6 | "Заполнить разделы" → "Волна 1: plantest-agent" (Task tool с промптом) |
| Новый шаг 7 | "Волна 2: plantest-reviewer" (Task tool, вердикт ACCEPT/REVISE) |
| Новый шаг 8 | "Волна 3: исправления" (при REVISE — перезапуск агента, макс 3 итерации) |
| Шаг 7+8 → 9 | "README + Validate" (объединение) |
| Шаг 9 → 10 | "User review + WAITING" — без изменений |
| Шаг 10+11 → 11 | "Report + Auto-propose" — без изменений |
| Примеры | Обновить пример с новым workflow |
| Версия | 1.2 → 1.3 |
| Секция "Скрипты" | Добавить create-analysis-plan-test-file.py |

#### 6.3 validation-plan-test.md

| Секция | Изменение |
|--------|-----------|
| Шаг 5 колонка Источник | И-1: обновить проверку Source (допустить SVC-N, INT-N) |
| Шаг 5 per-service heading | И-2: `## SVC-N: {name}` вместо `## {name}` |
| Типичные ошибки PT015 | Обновить описание: "нет источника (REQ-N, STS-N, SVC-N или INT-N)" |
| Чек-лист → Формат TC-N | Обновить строку Source |
| Версия | 1.2 → 1.3 |

#### 6.4 modify-plan-test.md

| Секция | Изменение |
|--------|-----------|
| Примеры CONFLICT | Обновить heading: `## SVC-N: {name}` |
| Версия | 1.2 → 1.3 |

---

### 7. Изменения в процессных стандартах

#### 7.1 standard-process.md

**Строка 428** (таблица § 8.1, шаг 1.3 Plan Tests):

**Было:**
```
| 1.3 Plan Tests | standard/create/modify/validation-plan-test | /plan-test-create, -modify, -validate | — | validate-analysis-plan-test.py, chain_status.py |
```

**Стало:**
```
| 1.3 Plan Tests | standard/create/modify/validation-plan-test | /plan-test-create, -modify, -validate | plantest-agent, plantest-reviewer | create-analysis-plan-test-file.py, validate-analysis-plan-test.py, chain_status.py |
```

**Строка 230** (§ 5, Фаза 1 → после "Агенты:"):

**Было:**
```
**Агенты:** design-agent-first + design-agent-second (обяз. при Design, последовательно; ...), discussion-reviewer (опц.), design-reviewer (опц.)
```

**Стало:**
```
**Агенты:** design-agent-first + design-agent-second (обяз. при Design, последовательно; ...), plantest-agent + plantest-reviewer (обяз. при Plan Tests, последовательно), discussion-reviewer (опц.), design-reviewer (опц.)
```

#### 7.2 create-chain.md

**TASK 3** (строки 160-166, Happy Path шаблон):

**Было:**
```
TASK 3: Создать Plan Tests
  description: >
    Скилл: /plan-test-create — TC-N acceptance-сценарии, тестовые данные, матрица покрытия.
    Claude читает design.md → генерирует тест-сценарии → пользователь ревьюит → WAITING.
    SSOT: standard-plan-test.md
```

**Стало:**
```
TASK 3: Создать Plan Tests
  description: >
    Скилл: /plan-test-create — два агента последовательно:
    plantest-agent: генерация TC-N, fixtures, матрица покрытия, блоки тестирования.
    plantest-reviewer — проверка покрытия REQ-N/STS-N и формата.
    Файл создаётся скриптом create-analysis-plan-test-file.py → пользователь ревьюит → WAITING.
    SSOT: standard-plan-test.md
```

#### 7.3 standard-analysis.md

**§ 2.2 Таблица объектов → строка Plan Tests:**

Добавить в колонку "Содержит": упоминание агентов (как у Design: "Два агента, один документ").

**§ 2.4 Общий паттерн → шаг 3 GENERATE:**

После текущего текста добавить:
> Для Plan Tests шаг GENERATE делегируется plantest-agent (генерация) + plantest-reviewer (проверка). Оркестратор вызывает агентов через Task tool последовательно.

---

## Решения

| ID | Решение | Обоснование |
|----|---------|-------------|
| D-1 | Source: ≥ 1 из REQ-N/STS-N/SVC-N § K/INT-N (не только REQ-N/STS-N) | Edge-case тесты вытекают из Design, а не из Discussion. Искусственная привязка к REQ размывает трассируемость |
| D-2 | Per-service заголовки `## SVC-N: {name}` в Plan Tests (как в Design) | Единообразие документов chain, автоматический маппинг SVC-N ↔ per-service |
| D-3 | Один plantest-agent (не два) — нет фазы "выбор технологий" | Design имеет 2 фазы (технологии → контент). Plan Tests — одна фаза (контент) |
| D-4 | Clarify остаётся у оркестратора (не у агента) | Clarify требует AskUserQuestion — интерактив с пользователем. Агент работает автономно |
| D-5 | plantest-reviewer как отдельный агент (не inline-проверка) | Разделение "генерация" и "проверка" — антигаллюцинации. Паттерн: design-reviewer, service-reviewer |
| D-6 | Макс 3 итерации Волна 3 (при REVISE) | Паттерн из create-docs-sync.md. При 3+ REVISE — эскалация пользователю |
| D-7 | Python-скрипт для создания файла-заглушки (вместо ручного копирования шаблона) | Паттерн: create-review-file.py, create-analysis-design-file.py. Быстрее, надёжнее, заполняет frontmatter + SVC-N секции из Design автоматически |

---

## Открытые вопросы

Все вопросы закрыты.

| ID | Вопрос | Решение |
|----|--------|---------|
| ~~OQ-1~~ | Нужен ли Plan Dev аналогичный рефакторинг (plandev-agent + plandev-reviewer)? | **Отложить.** Сначала проверить Plan Tests, потом решить по Plan Dev на основе реального опыта |

---

## Tasklist

| # | Задача | Зависимость | Описание | activeForm |
|---|--------|-------------|----------|------------|
| 1 | Исправить валидатор (В-1, В-2, В-3, В-4) | — | validate-analysis-plan-test.py: special set, range parsing, Source rule, heading regex SVC-N | Исправляю валидатор plan-test |
| 2 | Обновить standard-plan-test.md (И-1, И-2) | — | § 5 Source, heading `SVC-N:`, шаблон § 7, примеры § 9, version bump 1.2→1.3 | Обновляю standard-plan-test.md |
| 3 | Обновить validation-plan-test.md | 2 | Шаг 5 Source, heading SVC-N, PT015, version bump | Обновляю validation-plan-test.md |
| 4 | Обновить modify-plan-test.md | 2 | Примеры CONFLICT heading SVC-N, version bump | Обновляю modify-plan-test.md |
| 5 | Создать create-analysis-plan-test-file.py | — | /script-create: скрипт создания файла-заглушки по паттерну create-review-file.py | Создаю скрипт plan-test file |
| 6 | Создать plantest-agent | — | /agent-create plantest-agent (general-purpose, sonnet, max_turns=40) | Создаю plantest-agent |
| 7 | Создать plantest-reviewer | — | /agent-create plantest-reviewer (general-purpose, sonnet, max_turns=20) | Создаю plantest-reviewer |
| 8 | Обновить create-plan-test.md | 2, 5, 6, 7 | Шаги 2-8 → скрипт + scope + агенты, примеры, version bump | Обновляю create-plan-test.md |
| 9 | Обновить standard-process.md | 6, 7 | Строка 428: агенты + скрипт, строка 230: plantest-agent | Обновляю standard-process.md |
| 10 | Обновить standard-analysis.md | 6, 7 | § 2.2 + § 2.4: упоминание plantest-agent/reviewer | Обновляю standard-analysis.md |
| 11 | Обновить create-chain.md | 6, 7 | TASK 3 description: агенты + скрипт (как TASK 2 для Design) | Обновляю create-chain.md |
| 12 | /migration-create standard-plan-test.md | 2 | Миграция зависимых файлов после version bump | Запускаю миграцию standard-plan-test |
| 13 | Коммит + push | 1-12 | /commit | Коммичу изменения |
| 14 | Тест: /plan-test-create 0001-task-dashboard | 13 | Повторный прогон с исправлениями (новый контекст) | Тестирую plan-test-create |
