# Plan Dev — улучшения процесса создания

Делегирование создания plan-dev.md агенту (plandev-agent + plandev-reviewer) по паттерну plantest-agent. Исправление 4 проблем стандарта/валидатора, обнаруженных при тестовом прогоне на цепочке 0001-task-dashboard. Скрипт создания файла-заглушки.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблемы](#1-проблемы)
  - [2. Решение: plandev-agent + plandev-reviewer](#2-решение-plandev-agent--plandev-reviewer)
  - [3. Исправления стандарта](#3-исправления-стандарта)
  - [4. Исправления валидатора](#4-исправления-валидатора)
  - [5. Скрипт create-analysis-plan-dev-file.py](#5-скрипт-create-analysis-plan-dev-filepy)
  - [6. Изменения в инструкциях plan-dev/](#6-изменения-в-инструкциях-plan-dev)
  - [7. Изменения в процессных стандартах](#7-изменения-в-процессных-стандартах)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** При тестовом прогоне `/chain --resume 0001` (цепочка `0001-task-dashboard`), на шаге "Создать Plan Dev" (`/plan-dev-create 0001`), пользователь обнаружил 4 проблемы: нет скрипта создания файла, заголовки per-service не согласованы с Design/Plan Tests, основной LLM генерирует все TASK-N inline, нет ревьюера.

**Этап обнаружения:** Шаг 9 (ревью пользователем) — после полного прогона Plan Dev (20 TASK-N, 3 сервиса, валидация пройдена), перед DRAFT -> WAITING.

**Почему:** Plan Dev (4-й уровень цепочки) был создан последним в линейке Discussion -> Design -> Plan Tests -> Plan Dev. Предыдущие уровни уже имели скрипты создания и агенты (plantest-agent, plantest-reviewer, design-agent, design-reviewer), но Plan Dev создавался полностью вручную основным LLM.

**Связанные файлы:**

Инструкции plan-dev/ (4 файла — все будут обновлены):
- [standard-plan-dev.md](/specs/.instructions/analysis/plan-dev/standard-plan-dev.md) — стандарт Plan Dev (версия 1.2)
- [create-plan-dev.md](/specs/.instructions/analysis/plan-dev/create-plan-dev.md) — воркфлоу создания: 12 шагов
- [validation-plan-dev.md](/specs/.instructions/analysis/plan-dev/validation-plan-dev.md) — воркфлоу валидации
- [modify-plan-dev.md](/specs/.instructions/analysis/plan-dev/modify-plan-dev.md) — воркфлоу модификации

Валидатор:
- [validate-analysis-plan-dev.py](/specs/.instructions/.scripts/validate-analysis-plan-dev.py) — скрипт валидации (2 бага)

Паттерны (для агентов):
- [plantest-agent AGENT.md](/.claude/agents/plantest-agent/AGENT.md) — паттерн агента
- [plantest-reviewer AGENT.md](/.claude/agents/plantest-reviewer/AGENT.md) — паттерн ревьюера
- [design-reviewer AGENT.md](/.claude/agents/design-reviewer/AGENT.md) — v2.0, пишет PROP-N в документ

Паттерн (для скрипта):
- [create-analysis-plan-test-file.py](/specs/.instructions/.scripts/create-analysis-plan-test-file.py) — аналогичный скрипт для Plan Tests

Процессные стандарты (ссылки на агентов):
- [standard-process.md](/specs/.instructions/standard-process.md) — строка 429, колонка "Агент": `—`
- [standard-analysis.md](/specs/.instructions/analysis/standard-analysis.md) — § 2.2, строка 141

Оркестратор chain:
- [create-chain.md](/specs/.instructions/create-chain.md) — TASK 4 description (строки 170-177)

Именование сервисов:
- [design.md](/specs/analysis/0001-task-dashboard/design.md) — `## SVC-1: task`, `## SVC-2: auth`, `## SVC-3: frontend`
- [plan-test.md](/specs/analysis/0001-task-dashboard/plan-test.md) — `## SVC-1: task`, `## SVC-2: auth`, `## SVC-3: frontend`
- [plan-dev.md](/specs/analysis/0001-task-dashboard/plan-dev.md) — `## Инфраструктура`, `## task`, `## auth`, `## frontend`, `## Системные тесты` (без SVC-N)

---

## Содержание

### 1. Проблемы

**P-1. Нет скрипта создания файла**

Шаги 2-3 воркфлоу (создание файла + заполнение frontmatter) выполняются вручную — LLM копирует шаблон из standard-plan-dev.md § 7 и подставляет значения. У plan-test есть скрипт `create-analysis-plan-test-file.py`, у design — `create-analysis-design-file.py`, у review — `create-review-file.py`. Plan Dev — единственный уровень без скрипта.

**Текущее состояние (create-plan-dev.md):**
```
Шаг 2: Создать файл — скопировать шаблон из standard-plan-dev.md § 7
Шаг 3: Заполнить frontmatter — вручную подставить значения
```

**Результат:** Медленнее, подвержено ошибкам (неправильный frontmatter, пропущенные поля, несогласованные per-service секции).

---

**P-2. Несогласованность заголовков per-service: Design/Plan Tests vs Plan Dev**

Design и Plan Tests используют формат `## SVC-N: {name}`. Plan Dev использует формат `## {name}` (без SVC-N префикса).

**Примеры из реального документа 0001-task-dashboard:**

| Документ | Заголовки |
|----------|-----------|
| design.md | `## SVC-1: task`, `## SVC-2: auth`, `## SVC-3: frontend` |
| plan-test.md | `## SVC-1: task`, `## SVC-2: auth`, `## SVC-3: frontend` |
| plan-dev.md | `## Инфраструктура`, `## task`, `## auth`, `## frontend`, `## Системные тесты` |

**Стандарт** (standard-plan-dev.md § 5, строка 211):
> Один h2 на сервис, название = имя сервиса из Design (SVC-N)

**Шаблон** (standard-plan-dev.md § 7, строки 384-406):
```markdown
## {Сервис 1}

### Задачи

#### TASK-1: {Название задачи}
...

## {Сервис 2}

### Задачи
```

**Оглавление** (standard-plan-dev.md, строка 38):
```
- [{Сервис} — per-service разделы](#сервис-per-service-разделы)
```

Рассогласование затрудняет навигацию между документами, ломает автоматический маппинг SVC-N и не позволяет валидатору проверить полноту покрытия.

---

**P-3. Основной LLM создаёт Plan Dev inline — дорого по контексту**

Текущий workflow (create-plan-dev.md):
1. Основной LLM читает 5 источников (Design ~800 строк, Discussion ~70 строк, Plan Tests ~500 строк, service docs)
2. Основной LLM проводит Clarify
3. Основной LLM генерирует все TASK-N для всех сервисов
4. Основной LLM валидирует

**Проблемы:**
- Контекст переполняется при большом количестве сервисов
- Нет параллелизма — задачи генерируются последовательно
- Нет специализации — один LLM должен держать в голове контекст всех сервисов
- Нет разделения "генерация" и "проверка" (как в plantest-agent/plantest-reviewer, design-agent/design-reviewer)
- При 20+ TASK-N для 3+ сервисов — LLM может галлюцинировать (путать SVC-N, терять задачи, дублировать зависимости)

**Паттерн уже решён:** Plan Tests использует plantest-agent + plantest-reviewer. Design использует design-agent-first + design-agent-second + design-reviewer. Docs Sync использует service-agent + service-reviewer. Нужно применить тот же паттерн.

---

**P-4. Нет ревьюера для Plan Dev**

У Plan Tests есть plantest-reviewer, у Design — design-reviewer. Plan Dev (20+ задач, кросс-сервисные зависимости, TC-трассируемость) нуждается в автоматической проверке:
- Все TC-N из Plan Tests покрыты TASK-N
- Все SVC-N из Design имеют per-service разделы
- Нет циклических зависимостей в depends
- Формат TASK-N корректен (5 обязательных полей)
- INFRA-задачи <= 20% от общего числа

**Паттерн:** design-reviewer v2.0 — пишет PROP-N прямо в документ (секции "Предложения" и "Отвергнутые предложения"). Необходимо добавить эти секции в standard-plan-dev.md.

---

### 2. Решение: plandev-agent + plandev-reviewer

#### 2.1 plandev-agent (NEW)

**Роль:** Создание содержимого plan-dev.md — чтение источников, генерация TASK-N для per-service + INFRA + системных тестов.

**Паттерн:** Аналог plantest-agent — получает готовый файл с frontmatter + пустыми секциями (от скрипта), заполняет содержимое.

**Входные данные (из промпта оркестратора):**
- Путь к plan-dev.md (уже создан скриптом с frontmatter + пустыми секциями)
- Путь к design.md
- Путь к plan-test.md
- Путь к discussion.md
- Ответы Clarify (из AskUserQuestion оркестратора)
- Список сервисов (SVC-1: task, SVC-2: auth, ...)
- Список STS-N из Design

**Что делает:**
1. Читает Design (SVC-N секции, INT-N, STS-N, § 5 Code Map)
2. Читает Discussion (REQ-N)
3. Читает Plan Tests (TC-N для трассируемости)
4. Читает specs/docs/{svc}.md (AS IS, если существуют)
5. Генерирует per-service TASK-N (код, тесты, зависимости)
6. Генерирует INFRA-задачи (docker-compose, shared config, CI)
7. Генерирует задачи для системных тестов (e2e, load)
8. Строит кросс-сервисные зависимости
9. Формирует блоки выполнения (BLOCK-N)
10. Записывает всё в plan-dev.md через Edit

**Один агент с mode-параметром** (не три отдельных агента):

| Режим (mode) | Что делает | Scope |
|--------------|-----------|-------|
| per-service | Читает design.md SVC-N, plan-test.md per-service TC-N, discussion.md REQ-N → генерирует TASK-N для одного сервиса | Одна SVC-N секция |
| INFRA | Читает design.md все SVC-N § 5 (Code Map) → генерирует INFRA задачи (docker-compose, shared config) | Секция "Инфраструктура" |
| system | Читает plan-test.md системные TC, design.md INT-N, STS-N → генерирует задачи для системных тестов | Секция "Системные тесты" |

**Почему один агент с mode, а не три разных:** все три режима работают с одними и теми же файлами (design.md, plan-test.md, discussion.md), просто с разными "уровнями" — per-service, инфраструктура, системные тесты. Один AGENT.md проще поддерживать и эволюционировать.

**Алгоритм оркестратора (шаг 5):**
1. Определить список SVC-N из design.md
2. Запустить **последовательно** три вызова plandev-agent с разными mode:
   - mode=INFRA (первый — генерирует INFRA TASK-N в wave 0)
   - mode=per-service × N (для каждого SVC-N — генерирует per-service TASK-N)
   - mode=system (последний — генерирует задачи системных тестов)
3. Каждый вызов дописывает TASK-N в свою секцию plan-dev.md (через Edit)
4. Оркестратор проверяет сквозную нумерацию TASK-N и кросс-сервисные зависимости

**Конфигурация:**

| Поле | Значение |
|------|----------|
| type | general-purpose |
| model | sonnet |
| tools | Read, Grep, Glob, Edit, Write |
| max_turns | 40 |

#### 2.2 plandev-reviewer (NEW)

**Роль:** Проверка plan-dev.md на полноту покрытия, корректность формата, согласованность с Design и Plan Tests.

**Паттерн:** Аналог design-reviewer v2.0 — читает документ, проверяет по 7+ критериям, записывает PROP-N замечания.

**Что проверяет:**
1. **Покрытие TC-N:** каждый TC-N из Plan Tests покрыт >= 1 TASK-N
2. **Согласованность SVC-N:** каждый SVC-N из Design имеет per-service раздел
3. **Формат TASK-N:** 5 обязательных полей (описание, подзадачи, сложность, depends, test-link)
4. **Зависимости:** нет циклических зависимостей в depends
5. **INFRA лимит:** INFRA-задачи <= 20% от общего числа TASK-N
6. **BLOCK-N:** каждый TASK-N принадлежит блоку, системные TASK в отдельном BLOCK
7. **Антигаллюцинации:** TASK-N не содержат информацию, отсутствующую в Design/Discussion (MISSING/INVENTED/DISTORTED)

**Выход:** PROP-N в секции "Предложения" plan-dev.md (как design-reviewer). Критерии приоритетов:
- P1 — блокирующее (нарушение структуры, пропущенные TC, циклические зависимости)
- P2 — важное (INFRA > 20%, нет test-link, слабые описания)
- P3 — рекомендация (оптимизация порядка BLOCK, улучшение формулировок)

**Вердикт:** ACCEPT или REVISE + список расхождений.

**Конфигурация:**

| Поле | Значение |
|------|----------|
| type | general-purpose |
| model | sonnet |
| tools | Read, Grep, Glob, Edit |
| max_turns | 20 |

#### 2.3 Обновлённый workflow create-plan-dev.md

**Было (12 шагов, основной LLM):**
```
Шаг 1:  Проверить parent Plan Tests        <- оркестратор
Шаг 2:  Создать файл из шаблона            <- LLM вручную копирует шаблон
Шаг 3:  Заполнить frontmatter              <- LLM заполняет поля
Шаг 4:  Прочитать источники                <- LLM читает 5 источников
Шаг 5:  Clarify                            <- LLM (AskUserQuestion)
Шаг 6:  Заполнить разделы                  <- LLM генерирует ВСЕ TASK-N
Шаг 7:  Регистрация в README               <- LLM
Шаг 8:  Валидация                          <- LLM
Шаг 9:  Ревью пользователем                <- LLM
Шаг 10: Создание review.md                 <- LLM
Шаг 11: Отчёт о выполнении                 <- LLM
Шаг 12: Предложить запуск разработки       <- LLM
```

**Стало (13 шагов, оркестратор + скрипт + агенты):**
```
Шаг 1:  Проверить parent Plan Tests        <- оркестратор
Шаг 2:  Создать файл скриптом              <- NEW: create-analysis-plan-dev-file.py (frontmatter + пустые секции)
Шаг 3:  Определить scope                   <- оркестратор (список SVC-N, STS-N, REQ-N, TC-N из Design/Discussion/Plan Tests)
Шаг 4:  Clarify (AskUserQuestion)          <- оркестратор (интерактив с пользователем)
Шаг 5:  Волна 1: plandev-agent             <- агент (генерация TASK-N, зависимости, BLOCK-N) — 3 вызова: INFRA + per-service × N + system
Шаг 6:  Волна 2: plandev-reviewer          <- ревьюер (проверка покрытия TC-N, формат, PROP-N)
Шаг 7:  Волна 3: исправления               <- при REVISE: перезапуск агента (макс 3 итерации)
Шаг 8:  Синхронизация plan-test.md         <- NEW: оркестратор обновляет "Блоки тестирования" в plan-test.md (BLOCK-N ↔ Dev BLOCK)
Шаг 9:  README + Validate                  <- оркестратор
Шаг 10: User review + WAITING              <- оркестратор (блокирующее)
Шаг 11: Создание review.md                 <- оркестратор
Шаг 12: Отчёт о выполнении                 <- оркестратор
Шаг 13: Предложить запуск разработки       <- оркестратор
```

**Ключевые отличия:**
- Шаги 2+3 (файл + frontmatter) → один шаг с Python-скриптом (как create-analysis-plan-test-file.py)
- Шаг 4 (чтение 5 источников) → шаг 3 "Определить scope" (оркестратор только извлекает список SVC-N/STS-N/REQ-N/TC-N, не читает полностью)
- Шаг 6 (генерация TASK-N) → шаги 5-7 (агент → ревьюер → исправления)
- Один агент генерации с тремя режимами (mode=per-service/INFRA/system), последовательные вызовы
- **NEW** Шаг 8: синхронизация "Блоки тестирования" в plan-test.md — оркестратор обновляет Dev BLOCK колонку

---

### 3. Исправления стандарта

#### И-1. Per-service заголовки: `## SVC-N: {name}`

**Было** (standard-plan-dev.md § 5, строка 186-193):
```markdown
### {Сервис} — per-service разделы

Каждый SVC-N из Design получает свой раздел h2 в Plan Dev.
...
## {Сервис}

### Задачи
```

**Стало:**
```markdown
### SVC-N: {Сервис} — per-service разделы

Каждый SVC-N из Design получает свой раздел h2 в Plan Dev. Формат заголовка совпадает с Design и Plan Tests.
...
## SVC-N: {Сервис}

### Задачи
```

**Было** (standard-plan-dev.md § 5, строка 211):
> Один h2 на сервис, название = имя сервиса из Design (SVC-N)

**Стало:**
> Один h2 на сервис, формат `## SVC-N: {name}` — совпадает с заголовком в Design и Plan Tests

**Было** (standard-plan-dev.md § 7, строки 384-406):
```markdown
## {Сервис 1}

### Задачи

#### TASK-1: {Название задачи}
...

## {Сервис 2}

### Задачи
```

**Стало:**
```markdown
## SVC-1: {Сервис 1}

### Задачи

#### TASK-1: {Название задачи}
...

## SVC-2: {Сервис 2}

### Задачи
```

**Было** (standard-plan-dev.md, строка 38, оглавление):
```
- [{Сервис} — per-service разделы](#сервис-per-service-разделы)
```

**Стало:**
```
- [SVC-N: {Сервис} — per-service разделы](#svc-n-сервис-per-service-разделы)
```

**Влияние:**
- Навигация: `## SVC-1: task` в Design -> `## SVC-1: task` в Plan Tests -> `## SVC-1: task` в Plan Dev (1:1:1 маппинг)
- Валидатор: может автоматически проверить, что каждый SVC-N из Design присутствует в Plan Dev

---

#### И-2. Секции "Предложения" + "Отвергнутые предложения"

В standard-plan-dev.md отсутствуют секции для записи замечаний plandev-reviewer (PROP-N). Необходимо добавить по паттерну design.md.

**Стало** (добавить в шаблон § 7 после "Блоки выполнения"):
```markdown
## Предложения

<!-- plandev-reviewer записывает PROP-N сюда -->

## Отвергнутые предложения

<!-- Перенос отклонённых PROP-N сюда -->
```

**Влияние:**
- plandev-reviewer пишет PROP-N (P1/P2/P3) в секцию "Предложения"
- Оркестратор/пользователь переносит отклонённые PROP-N в "Отвергнутые предложения"
- Валидатор должен включить обе секции в special set

---

### 4. Исправления валидатора

#### В-1. Heading regex для SVC-N: {name}

**Файл:** validate-analysis-plan-dev.py, строка 332

**Было:**
```python
service_name = heading.replace("## ", "").strip()
```

**Стало:**
```python
svc_match = re.match(r'## (SVC-\d+:\s*.+)', heading)
if svc_match:
    service_name = svc_match.group(1).strip()
else:
    service_name = heading.replace("## ", "").strip()
```

Валидатор должен:
- Парсить формат `## SVC-\d+: .+`
- Проверять, что каждый SVC-N из parent Design присутствует в Plan Dev

---

#### В-2. "Предложения" + "Отвергнутые предложения" в special sets

**Файл:** validate-analysis-plan-dev.py, строка 310 (check_required_sections)

**Было:**
```python
special = {"Резюме", "Кросс-сервисные зависимости", "Маппинг GitHub Issues", "Блоки выполнения"}
```

**Стало:**
```python
special = {"Резюме", "Кросс-сервисные зависимости", "Маппинг GitHub Issues", "Блоки выполнения", "Предложения", "Отвергнутые предложения"}
```

**Файл:** validate-analysis-plan-dev.py, строка 326 (check_per_service_sections)

**Было:**
```python
special = {"Резюме", "Кросс-сервисные зависимости", "Маппинг GitHub Issues", "Блоки выполнения"}
```

**Стало:**
```python
special = {"Резюме", "Кросс-сервисные зависимости", "Маппинг GitHub Issues", "Блоки выполнения", "Предложения", "Отвергнутые предложения"}
```

---

### 5. Скрипт create-analysis-plan-dev-file.py

**Новый скрипт** по паттерну [create-analysis-plan-test-file.py](/specs/.instructions/.scripts/create-analysis-plan-test-file.py).

**Что делает:**
1. Принимает аргумент `<branch>` (= имя папки `NNNN-{topic}`)
2. Читает frontmatter parent plan-test.md через ChainManager
3. Проверяет статус parent plan-test: должен быть WAITING
4. Извлекает milestone из parent Discussion
5. Извлекает список SVC-N из Design (для генерации пустых per-service секций)
6. Создаёт файл `specs/analysis/{branch}/plan-dev.md` с:
   - Заполненный frontmatter (description-заглушка, standard, standard-version, index, parent, children, status=DRAFT, milestone)
   - Заголовок `# NNNN: {Тема} — Plan Dev`
   - Пустые секции: `## Резюме`, `## SVC-N: {name}` (для каждого SVC из Design), `## Кросс-сервисные зависимости`, `## Маппинг GitHub Issues`, `## Блоки выполнения`, `## Предложения`, `## Отвергнутые предложения`
   - Пустые подсекции per-service: `### Задачи`

**Использование:**
```bash
python specs/.instructions/.scripts/create-analysis-plan-dev-file.py 0001-task-dashboard
python specs/.instructions/.scripts/create-analysis-plan-dev-file.py 0001-task-dashboard --milestone v0.1.0
```

**Возвращает:**
- 0 — файл создан
- 1 — ошибка (файл существует, папка не найдена, нет plan-test.md, parent не WAITING)

**Зависимости:** chain_status.ChainManager (для чтения frontmatter, как в create-analysis-plan-test-file.py)

---

### 6. Изменения в инструкциях plan-dev/

#### 6.1 standard-plan-dev.md

| Секция | Изменение |
|--------|-----------|
| § 5 per-service заголовок (строки 186-193) | И-1: `## SVC-N: {Сервис}` вместо `## {Сервис}` |
| § 5 правило (строка 211) | И-1: формат `## SVC-N: {name}` совпадает с Design и Plan Tests |
| § 7 Шаблон (строки 384-406) | И-1: `## SVC-1: {Сервис 1}` вместо `## {Сервис 1}`, добавить "Предложения" + "Отвергнутые предложения" |
| Оглавление (строка 38) | И-1: обновить якорную ссылку per-service |
| § 8 Чек-лист | Добавить проверку SVC-N формата, секций "Предложения" |
| Секция "Скрипты" | Добавить create-analysis-plan-dev-file.py |
| Версия стандарта (строка 10) | 1.2 -> 1.3 |

#### 6.2 create-plan-dev.md

| Секция | Изменение |
|--------|-----------|
| Шаг 2 | "Создать файл из шаблона" -> "Создать файл скриптом": `python create-analysis-plan-dev-file.py {branch}` |
| Шаг 3 | "Заполнить frontmatter" -> **удалить** (скрипт заполняет), заменить на "Определить scope" |
| Шаг 4 | "Прочитать источники" -> Clarify (AskUserQuestion), сдвиг |
| Шаг 6 | "Заполнить разделы" -> "Волна 1: plandev-agent" (Task tool с промптом) |
| Новый шаг 7 (бывший 7) | "Волна 2: plandev-reviewer" (Task tool, вердикт ACCEPT/REVISE, PROP-N) |
| Новый шаг 8 (бывший 8) | "Волна 3: исправления" (при REVISE — перезапуск агента, макс 3 итерации) |
| Шаги 8-12 -> 8-12 | Перенумерация: README + Validate, User review, review.md, Report, Auto-propose |
| Примеры | Обновить пример с новым workflow |
| Секция "Скрипты" | Добавить create-analysis-plan-dev-file.py |
| Версия | 1.2 -> 1.3 |

#### 6.3 validation-plan-dev.md

| Секция | Изменение |
|--------|-----------|
| Шаг: per-service heading | И-1: `## SVC-N: {name}` вместо `## {name}` |
| Секции special | "Предложения" + "Отвергнутые предложения" в списке допустимых |
| Чек-лист -> Формат TASK-N | Обновить проверку per-service |
| Версия | 1.2 -> 1.3 |

---

### 7. Изменения в процессных стандартах

#### 7.1 standard-process.md

**Строка 429** (таблица § 8.1, шаг 1.4 Plan Dev):

**Было:**
```
| 1.4 Plan Dev | standard/create/modify/validation-plan-dev, create-review | /plan-dev-create (включает /review-create), -modify, -validate | — | validate-analysis-plan-dev.py, create-review-file.py, chain_status.py |
```

**Стало:**
```
| 1.4 Plan Dev | standard/create/modify/validation-plan-dev, create-review | /plan-dev-create (включает /review-create), -modify, -validate | plandev-agent, plandev-reviewer | create-analysis-plan-dev-file.py, validate-analysis-plan-dev.py, create-review-file.py, chain_status.py |
```

**Строка 230** (§ 5, Фаза 1 -> "Агенты:"):

**Было:**
```
**Агенты:** design-agent-first + design-agent-second (обяз. при Design, последовательно; WAITING один раз — после обоих + обработки PROP), plantest-agent + plantest-reviewer (обяз. при Plan Tests, последовательно), discussion-reviewer (опц.), design-reviewer (опц.)
```

**Стало:**
```
**Агенты:** design-agent-first + design-agent-second (обяз. при Design, последовательно; WAITING один раз — после обоих + обработки PROP), plantest-agent + plantest-reviewer (обяз. при Plan Tests, последовательно), plandev-agent + plandev-reviewer (обяз. при Plan Dev, последовательно), discussion-reviewer (опц.), design-reviewer (опц.)
```

#### 7.2 create-chain.md

**TASK 4** (строки 170-177, Happy Path шаблон):

**Было:**
```
TASK 4: Создать Plan Dev
  description: >
    Скилл: /plan-dev-create — TASK-N задачи, подзадачи, BLOCK-N, зависимости, маппинг Issues.
    Автоматически вызывает /review-create (review.md).
    Claude читает design.md + plan-test.md → генерирует план → пользователь ревьюит → WAITING.
    SSOT: standard-plan-dev.md
  activeForm: Создаю Plan Dev
  blockedBy: [3]
```

**Стало:**
```
TASK 4: Создать Plan Dev
  description: >
    Скилл: /plan-dev-create — два агента последовательно:
    plandev-agent: генерация TASK-N, зависимости, BLOCK-N (per-service + INFRA + system).
    plandev-reviewer — проверка покрытия TC-N, формат TASK-N, PROP-N запись.
    Файл создаётся скриптом create-analysis-plan-dev-file.py → пользователь ревьюит → WAITING.
    SSOT: standard-plan-dev.md
  activeForm: Создаю Plan Dev
  blockedBy: [3]
```

#### 7.3 standard-analysis.md

**§ 2.2 Таблица объектов** (строка 141, строка Plan Dev):

**Было:**
```
| **План разработки** | `plan-dev.md` | Какие задачи? | Per-service разделы: задачи, сложность, зависимости, ссылки на планы тестов | Бизнес-обоснование, архитектуру | [standard-plan-dev.md](plan-dev/standard-plan-dev.md) |
```

**Стало:**
```
| **План разработки** | `plan-dev.md` | Какие задачи? | Per-service разделы: задачи, сложность, зависимости, ссылки на планы тестов. Два агента (plandev-agent + plandev-reviewer), один документ | Бизнес-обоснование, архитектуру | [standard-plan-dev.md](plan-dev/standard-plan-dev.md) |
```

---

## Решения

| ID | Решение | Обоснование |
|----|---------|-------------|
| D-1 | Создать скрипт `create-analysis-plan-dev-file.py` | Единообразие с plan-test (скрипт создания), автоматизация frontmatter + per-service секций |
| D-2 | Формат сервисов `## SVC-N: {name}` | Единообразие между design.md, plan-test.md и plan-dev.md; ссылочная целостность; 1:1:1 маппинг |
| D-3 | Создать plandev-agent (один агент с mode параметром: per-service/INFRA/system) | Паттерн plantest-agent; все три режима работают с одними файлами, последовательные вызовы |
| D-4 | Создать plandev-reviewer с PROP-N записью | Паттерн design-reviewer v2.0; автоматическая проверка покрытия TC-N, формата TASK-N, зависимостей |
| D-5 | Clarify остаётся у оркестратора (не у агента) | Clarify требует AskUserQuestion — интерактив с пользователем. Агент работает автономно |
| D-6 | Макс 3 итерации Волна 3 (при REVISE) | Паттерн из create-docs-sync.md. При 3+ REVISE — эскалация пользователю |
| D-7 | Секции "Предложения" + "Отвергнутые предложения" в standard-plan-dev.md | Паттерн design.md. Необходимы для записи PROP-N от plandev-reviewer |

---

## Открытые вопросы

| ID | Вопрос | Статус |
|----|--------|--------|
| OQ-1 | Должен ли plandev-agent быть одним агентом с mode параметром или тремя разными? | Решён — один агент с mode (per-service/INFRA/system), последовательные вызовы |
| OQ-2 | Нужно ли обновить plan-test.md § "Блоки тестирования" после создания plan-dev.md? | Решён — доп. шаг 8 в create-plan-dev.md, основной LLM синхронизирует BLOCK-N |
| OQ-3 | Нужно ли добавить секцию "Предложения" в текущий plan-dev.md 0001-task-dashboard? | Решён — да, задача #12 в Tasklist |

---

## Tasklist

TASK 1: Обновить standard-plan-dev.md (И-1, И-2)
  description: >
    Драфт: секция "3".
    § 5: формат per-service heading `## SVC-N: {Сервис}` вместо `## {Сервис}`.
    § 7: шаблон — обновить заголовки на SVC-N, оглавление, добавить секции
    "Предложения" + "Отвергнутые предложения" (паттерн design.md).
    Version bump 1.2 → 1.3.
  activeForm: Обновление standard-plan-dev.md

TASK 2: Исправить валидатор (В-1, В-2)
  description: >
    Драфт: секция "4".
    validate-analysis-plan-dev.py:
    - Строка 332: heading regex для SVC-N формата (вместо plain text).
    - Строки 310, 326: добавить "Предложения" и "Отвергнутые предложения" в special sets.
    Зависит от TASK 1 (новый формат heading).
  activeForm: Исправление валидатора plan-dev

TASK 3: Обновить validation-plan-dev.md
  description: >
    Драфт: секция "6".
    Per-service heading SVC-N в описании проверок, секции special, version bump.
    Зависит от TASK 1.
  activeForm: Обновление validation-plan-dev.md

TASK 4: Обновить modify-plan-dev.md
  description: >
    Драфт: секция "6".
    Примеры CONFLICT heading SVC-N, version bump.
    Зависит от TASK 1.
  activeForm: Обновление modify-plan-dev.md

TASK 5: Создать create-analysis-plan-dev-file.py
  description: >
    Драфт: секция "5".
    `/script-create`: скрипт создания файла-заглушки plan-dev.md
    по паттерну create-analysis-plan-test-file.py.
    Читает Design SVC-N headings через ChainManager, генерирует skeleton
    с frontmatter + per-service секциями в формате SVC-N.
  activeForm: Создание скрипта plan-dev file

TASK 6: Создать plandev-agent AGENT.md
  description: >
    Драфт: секция "2".
    `/agent-create plandev-agent` (general-purpose, sonnet, max_turns=40).
    Один агент с mode параметром (per-service/INFRA/system).
    Последовательные вызовы — все три режима работают с одними файлами.
    Паттерн: plantest-agent. Tools: Read, Bash, Glob, Grep, Write, Edit.
  activeForm: Создание plandev-agent

TASK 7: Создать plandev-reviewer AGENT.md
  description: >
    Драфт: секция "2".
    `/agent-create plandev-reviewer` (general-purpose, sonnet, max_turns=20).
    Ревью plan-dev.md с записью PROP-N в секцию "Предложения".
    Паттерн: design-reviewer v2.0. Tools: Read, Grep, Glob, Edit.
  activeForm: Создание plandev-reviewer

TASK 8: Обновить create-plan-dev.md
  description: >
    Драфт: секции "2" и "6".
    Workflow: 13 шагов (было 12).
    Шаг 2: скрипт create-analysis-plan-dev-file.py вместо ручного копирования.
    Шаг 3: Scope Definition (per-service/INFRA/system).
    Шаги 4-6: plandev-agent с mode параметром (последовательно 3 вызова).
    Шаг 7: plandev-reviewer с PROP-N записью.
    Шаг 8: синхронизация plan-test.md "Блоки тестирования" (BLOCK-N).
    Version bump.
    Зависит от TASK 1, 5, 6, 7.
  activeForm: Обновление create-plan-dev.md

TASK 9: Обновить standard-process.md
  description: >
    Драфт: секция "7.1".
    Строка 429: Plan Dev — добавить plandev-agent + plandev-reviewer + скрипт.
    Строка 230: список агентов — добавить plandev-agent + plandev-reviewer.
    Зависит от TASK 6, 7.
  activeForm: Обновление standard-process.md

TASK 10: Обновить standard-analysis.md
  description: >
    Драфт: секция "7.3".
    § 2.2 таблица объектов: строка Plan Dev — упоминание plandev-agent/reviewer.
    Зависит от TASK 6, 7.
  activeForm: Обновление standard-analysis.md

TASK 11: Обновить create-chain.md
  description: >
    Драфт: секция "7.2".
    TASK 4 description: агенты + скрипт (как TASK 3 для Plan Tests).
    Зависит от TASK 6, 7.
  activeForm: Обновление create-chain.md

TASK 12: Обновить plan-dev.md 0001-task-dashboard
  description: >
    Драфт: OQ-3 (решён).
    Заголовки `## {Сервис}` → `## SVC-N: {Сервис}`.
    Добавить секции "Предложения" + "Отвергнутые предложения".
    Зависит от TASK 1, 2.
  activeForm: Обновление plan-dev.md 0001

TASK 13: Миграция standard-plan-dev.md
  description: >
    `/migration-create standard-plan-dev.md`.
    Миграция зависимых файлов после version bump 1.2 → 1.3.
    Зависит от TASK 1.
  activeForm: Запуск миграции standard-plan-dev

TASK 14: Коммит
  description: >
    `/commit` — все изменения TASK 1-13.
  activeForm: Коммит изменений

TASK 15: Тест: /plan-dev-create 0001
  description: >
    Повторный прогон `/plan-dev-create` с агентами и ревьюером
    в новом контексте. Проверка полного workflow (13 шагов).
    Зависит от TASK 14.
  activeForm: Тестирование plan-dev-create
