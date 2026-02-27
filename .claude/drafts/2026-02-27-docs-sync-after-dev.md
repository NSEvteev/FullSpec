# Docs Sync — агенты для specs/docs/ и новый шаг в /chain

Выделение артефактов Design (шаг 7) в отдельный шаг цепочки с тремя парами агентов. Позиция: **после Plan Dev, перед Dev** — все 4 документа готовы, system-agent получает данные из Plan Tests.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблема](#1-проблема)
  - [2. Решение: три пары агентов](#2-решение-три-пары-агентов)
  - [3. Новый шаг: /docs-sync](#3-новый-шаг-docs-sync)
  - [4. Изменения в существующих файлах](#4-изменения-в-существующих-файлах)
  - [5. Оркестрация](#5-оркестрация)
- [Решения](#решения)
- [Решённые вопросы](#решённые-вопросы)
- [Открытые вопросы](#открытые-вопросы)
- [Дополнительные файлы для обновления](#дополнительные-файлы-для-обновления)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** При переводе Design в WAITING (шаг 7 create-design.md) создаются артефакты: заглушки сервисов, Planned Changes в specs/docs/, per-tech стандарты. Сейчас это делает основной LLM — дорого по контексту, не параллелизуемо, не единообразно.

**Почему:** Технологии уже обслуживаются парой агентов (technology-agent + technology-reviewer). Сервисные документы и системная архитектура — нет. Нужно закрыть все три сущности specs/docs/ агентами и вынести артефакты в отдельный шаг цепочки.

**Связанные файлы:**
- [create-design.md](/specs/.instructions/analysis/design/create-design.md) — текущий шаг 7 (артефакты WAITING)
- [create-chain.md](/specs/.instructions/create-chain.md) — TaskList `/chain`
- [standard-process.md](/specs/.instructions/standard-process.md) — фазы процесса
- [technology-agent AGENT.md](/.claude/agents/technology-agent/AGENT.md) — эталонный агент
- [technology-reviewer AGENT.md](/.claude/agents/technology-reviewer/AGENT.md) — эталонный ревьюер
- [standard-service.md](/specs/.instructions/docs/service/standard-service.md) — стандарт per-service docs
- [standard-overview.md](/specs/.instructions/docs/overview/standard-overview.md) — стандарт overview
- [standard-conventions.md](/specs/.instructions/docs/conventions/standard-conventions.md) — стандарт conventions
- [standard-infrastructure.md](/specs/.instructions/docs/infrastructure/standard-infrastructure.md) — стандарт infrastructure
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) — стандарт testing

---

## Содержание

### 1. Проблема

**Текущее состояние (AS IS):**

Шаг 7 create-design.md создаёт 6 типов артефактов при переводе Design в WAITING:

| # | Артефакт | Кто выполняет | Проблема |
|---|----------|---------------|----------|
| 1 | Planned Changes в specs/docs/{svc}.md § 9 | Основной LLM | Контекст раздувается |
| 2 | Planned Changes в specs/docs/.system/overview.md § 8 | Основной LLM | Нет специализации |
| 3 | Planned Changes в specs/docs/.system/conventions.md | Основной LLM | Нет специализации |
| 4 | Planned Changes в specs/docs/.system/infrastructure.md | Основной LLM | Нет специализации |
| 5 | Заглушки specs/docs/{svc}.md (/service-create) | Основной LLM через скилл | Последовательно, по одному |
| 6 | Per-tech стандарты (/technology-create) | technology-agent (параллельно) | Уже решено |

**Проблемы:**
- Основной LLM тратит контекст на генерацию содержимого specs/docs/
- Сервисные документы создаются последовательно (нельзя параллелизовать через скилл)
- Системные документы обновляются "вручную" без стандартизированного агента
- Нет ревью — агент может исказить факты при копировании (пропустить, добавить лишнее, переформулировать)

**Целевое состояние (TO BE):**

Три пары агентов покрывают все три сущности specs/docs/:

| Сущность | Путь | Create-агент | Reviewer | Обоснование ревью |
|----------|------|-------------|----------|-------------------|
| Per-tech стандарты | specs/docs/.technologies/ | technology-agent | technology-reviewer | Генерируют контент |
| Per-service документы | specs/docs/{svc}.md | **service-agent** (NEW) | **service-reviewer** (NEW) | Сверка с Design: ничего не придумано, ничего не потеряно |
| Системная архитектура | specs/docs/.system/ | **system-agent** (NEW) | **system-reviewer** (NEW) | Сверка с Design: каждое изменение прослеживается до источника |

---

### 2. Решение: три пары агентов

#### 2.1 service-agent (NEW)

**Роль:** Создание и обновление specs/docs/{svc}.md (10 секций по standard-service.md).

**Режимы:**
- `create` — создаёт новый {svc}.md из шаблона, заполняет 10 секций на основе Design SVC-N
- `update` — обновляет существующий {svc}.md: пишет Planned Changes в § 9, обновляет § 5 Tech Stack

**Входные данные:**
```
service: task | auth | frontend (kebab-case)
design-path: specs/analysis/NNNN-{topic}/design.md
svc-section: SVC-1 | SVC-2 | SVC-3 (какой SVC-N из design)
mode: create | update
```

**Источники данных (при create):**
- Design SVC-N §§ 1-8 → напрямую маппятся на 8 из 10 секций {svc}.md (§ 9 Design-only, не переносится)
- Design INT-N → § 6 Зависимости
- Discussion REQ-N → контекст для § 1 Назначение (явный источник для "расширения")

**Маппинг Design SVC-N → {svc}.md:**

| Design SVC-N § | {svc}.md § | Действие |
|----------------|-----------|----------|
| § 1 Назначение | § 1 Назначение | Копировать + дополнить из Discussion REQ-N (явный источник) |
| § 2 API контракты | § 2 API контракты | Копировать |
| § 3 Data Model | § 3 Data Model | Копировать |
| § 4 Потоки | § 4 Потоки | Копировать |
| § 5 Code Map | § 5 Code Map | Копировать |
| § 6 Зависимости | § 6 Зависимости | Копировать + INT-N ссылки |
| § 7 Доменная модель | § 7 Доменная модель | Копировать |
| § 8 Границы автономии | § 8 Границы автономии LLM | Копировать |
| — | § 9 Planned Changes | Генерировать из delta-маркеров (ADDED/MODIFIED) |
| — | § 10 Changelog | Пустой (заполняется при DONE) |

**При update (Planned Changes):**
- Читает Design SVC-N, находит все ADDED/MODIFIED маркеры
- Записывает в § 9 Planned Changes формат: `Из Design NNNN: {список изменений}`

**Параллельный запуск:** Один агент на один сервис. При 3 сервисах — 3 параллельных агента.

**Антигаллюцинации (КРИТИЧЕСКИ ВАЖНО):**
- ЗАПРЕЩЕНО придумывать, додумывать, интерпретировать, расширять информацию из Design
- Каждый факт в {svc}.md ОБЯЗАН иметь источник в Design SVC-N (конкретная секция, конкретный абзац)
- "Дополнить" § 1 = ТОЛЬКО из Discussion REQ-N (явный источник), НЕ из "общих знаний"
- Если в Design SVC-N нет данных для секции — оставить секцию пустой с маркером `_Нет данных в Design SVC-N._`
- ЗАПРЕЩЕНО: добавлять "очевидные" поля, дефолтные значения, примеры из "общих знаний"

**SSOT-зависимости:**
- [standard-service.md](/specs/.instructions/docs/service/standard-service.md) — формат 10 секций
- [create-service.md](/specs/.instructions/docs/service/create-service.md) — воркфлоу создания
- [validation-service.md](/specs/.instructions/docs/service/validation-service.md) — валидация

**Алгоритм (mode=create):**
1. Прочитать Design SVC-N (целевая секция)
2. Прочитать шаблон из standard-service.md § 5
3. Создать {svc}.md, заполнить §§ 1-8 из Design SVC-N (маппинг 8:8)
4. Заполнить § 9 Planned Changes из delta-маркеров
5. Оставить § 10 Changelog пустым
6. Запустить валидацию: validate-docs-service.py
7. Self-review перед возвратом

**Алгоритм (mode=update):**
1. Прочитать существующий {svc}.md
2. Прочитать Design SVC-N
3. Обновить § 9 Planned Changes
4. Обновить §§ 1-8 если есть MODIFIED маркеры
5. Запустить валидацию

**Важно:** specs/docs/README.md обновляет оркестратор ПОСЛЕ Волны 1 (не каждый агент — избежать конфликтов записи).

**Tools:** Read, Grep, Glob, Edit, Write, Bash (для валидации)

#### 2.2 service-reviewer (NEW)

**Роль:** Сверка specs/docs/{svc}.md с Design SVC-N — обнаружение расхождений.

**Что проверяет:**
1. **Полнота:** Каждый факт из Design SVC-N §§ 1-8 присутствует в {svc}.md
2. **Точность:** Ни один факт в {svc}.md не "придуман" (отсутствует в Design SVC-N)
3. **Целостность:** Данные не искажены при копировании (переформулировка, потеря деталей)
4. **Формат:** 10 секций соответствуют standard-service.md

**Алгоритм:**
1. Прочитать Design SVC-N §§ 1-8 (источник правды)
2. Прочитать {svc}.md §§ 1-8 (результат service-agent)
3. Для каждой секции построить diff: Design vs {svc}.md
4. Выявить расхождения:
   - **MISSING:** факт есть в Design, отсутствует в {svc}.md
   - **INVENTED:** факт есть в {svc}.md, отсутствует в Design
   - **DISTORTED:** факт есть в обоих, но изменён/переформулирован
5. Проверить § 9 Planned Changes: каждый ADDED/MODIFIED маркер соответствует Design
6. Вердикт: ACCEPT (нет расхождений) / REVISE (список расхождений с цитатами из Design)

**Формат вывода при REVISE:**
```
REVISE — {svc}.md

| # | Тип | Секция | В Design SVC-N | В {svc}.md | Рекомендация |
|---|-----|--------|----------------|-----------|--------------|
| 1 | INVENTED | § 3 Data Model | — | "поле updatedAt" | Удалить — отсутствует в Design |
| 2 | MISSING | § 2 API | "PATCH /tasks/:id" | — | Добавить из Design SVC-N § 2 |
```

**Параллельный запуск:** Один ревьюер на один сервис (по аналогии с агентом).

**Tools:** Read, Grep, Glob (только чтение — ревьюер НЕ модифицирует файлы)

#### 2.3 system-agent (NEW)

**Роль:** Обновление specs/docs/.system/ (overview.md, conventions.md, infrastructure.md, testing.md) на основе Design и Plan Tests.

**Режимы:**
- `update` — основной: обновляет системные документы из Design + Plan Tests (новые сервисы, связи, конвенции, тестирование)
- `create` — только при инициализации проекта (/init-project), обычно не используется

**Входные данные:**
```
design-path: specs/analysis/NNNN-{topic}/design.md
plan-test-path: specs/analysis/NNNN-{topic}/plan-test.md
mode: update (default)
```

**Что обновляет в каждом файле:**

| Файл | Секция | Источник данных |
|------|--------|----------------|
| overview.md | § Карта сервисов | Design: новые SVC-N (type: новый) |
| overview.md | § Связи между сервисами | Design: INT-N (паттерн, участники) |
| overview.md | § Сквозные потоки | Design: SVC-N § 4 (ключевые потоки) |
| overview.md | § Контекстная карта доменов | Design: SVC-N § 7 (агрегаты, события) |
| conventions.md | § API конвенции | Design: если вводит новые паттерны |
| conventions.md | § Формат ответов/ошибок | Design: если определяет новые форматы |
| infrastructure.md | § Docker Compose | Design: новые сервисы (имена, порты из SVC-N) |
| infrastructure.md | § Переменные окружения | Design: новые env (JWT_SECRET и пр.) |
| testing.md | § Стратегия тестирования | **Plan Tests: стратегия, типы тестов** |
| testing.md | § Системные тест-сценарии | **Plan Tests: TC-N (system-level)** |
| testing.md | § Межсервисные сценарии | **Plan Tests: TC-N (cross-service) + Design INT-N** |
| testing.md | § Покрытие | **Plan Tests: матрица покрытия** |

**SSOT-зависимости:**
- [standard-overview.md](/specs/.instructions/docs/overview/standard-overview.md)
- [standard-conventions.md](/specs/.instructions/docs/conventions/standard-conventions.md)
- [standard-infrastructure.md](/specs/.instructions/docs/infrastructure/standard-infrastructure.md)
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md)

**Алгоритм (mode=update):**
1. Прочитать Design полностью (Резюме, SVC-N, INT-N, STS-N)
2. Прочитать Plan Tests (TC-N, стратегия тестирования, матрица покрытия)
3. Прочитать текущие 4 файла .system/
4. Для каждого файла определить delta (что добавить/изменить):
   - overview.md, conventions.md, infrastructure.md ← из Design
   - testing.md ← из Design STS-N + Plan Tests TC-N
5. Применить inline-правки (НЕ Planned Changes — .system/ файлы не имеют этой секции)
6. Порядок: overview → conventions → infrastructure → testing
7. Запустить валидацию каждого файла (validate-docs-*.py)

**Запуск:** Один агент на все системные файлы (они связаны между собой).

**Антигаллюцинации (КРИТИЧЕСКИ ВАЖНО):**
- ЗАПРЕЩЕНО придумывать, додумывать, интерпретировать, расширять информацию
- Каждое изменение в .system/ файлах ОБЯЗАНО прослеживаться до конкретного места в Design (SVC-N §X, INT-N, STS-N) или Plan Tests (TC-N)
- Если Design/Plan Tests не содержат данных для секции — НЕ ТРОГАТЬ секцию
- ЗАПРЕЩЕНО: добавлять "очевидные" порты, "стандартные" переменные, "типичные" конвенции
- Формат каждого изменения: `<!-- Source: Design SVC-N §X / INT-N / STS-N / Plan Tests TC-N -->`

**Tools:** Read, Grep, Glob, Edit, Write, Bash

#### 2.4 system-reviewer (NEW)

**Роль:** Сверка изменений в specs/docs/.system/ с Design и Plan Tests — обнаружение расхождений.

**Что проверяет:**
1. **Прослеживаемость:** Каждое изменение в .system/ файлах имеет источник в Design (SVC-N, INT-N, STS-N) или Plan Tests (TC-N)
2. **Полнота:** Все релевантные данные из Design/Plan Tests перенесены в .system/ файлы
3. **Точность:** Ни одно изменение не "придумано" (отсутствует в Design/Plan Tests)
4. **Согласованность:** Данные между 4 файлами .system/ не противоречат друг другу

**Алгоритм:**
1. Прочитать Design полностью (Резюме, SVC-N, INT-N, STS-N)
2. Прочитать Plan Tests (TC-N, стратегия, матрица покрытия)
3. Прочитать все 4 файла .system/ (текущее состояние после system-agent)
4. Определить diff: что изменил system-agent
5. Для каждого изменения проверить: есть ли источник в Design или Plan Tests?
6. Проверить обратное: есть ли в Design/Plan Tests данные, не отражённые в .system/?
7. Проверить согласованность: данные между 4 файлами не противоречат друг другу
8. Вердикт:
   - **ACCEPT:** нет расхождений
   - **REVISE:** список расхождений с цитатами из Design/Plan Tests

**Формат вывода при REVISE:**
```
REVISE — .system/

| # | Тип | Файл | Секция | В Design/Plan Tests | В .system/ | Рекомендация |
|---|-----|------|--------|---------------------|-----------|--------------|
| 1 | INVENTED | infrastructure.md | § Docker | — | "порт 6379 Redis" | Удалить — отсутствует в Design |
| 2 | MISSING | overview.md | § Связи | INT-2 REST | — | Добавить из Design INT-2 |
| 3 | MISSING | testing.md | § Стратегия | Plan Tests: "unit + integration" | — | Добавить из Plan Tests |
```

**Запуск:** Один ревьюер на все .system/ файлы (по аналогии с system-agent).

**Tools:** Read, Grep, Glob (только чтение — ревьюер НЕ модифицирует файлы)

---

### 3. Новый шаг: /docs-sync

**Идея:** Выделить артефакты Design (текущий шаг 7 create-design.md) в отдельный шаг цепочки, который оркестрирует все три пары агентов.

**Характеристики шага:**
- Task в TaskList `/chain` (**после Plan Dev, перед Dev**)
- **БЕЗ собственного state-документа** (нет docs-sync.md со статусами DRAFT/WAITING/RUNNING/DONE)
- НЕ участвует в DONE-каскаде и rollback (chain_status.py, create-chain-done.md, create-rollback.md — без изменений)
- Артефакты specs/docs/ откатываются через git при rollback ветки

**Место в цепочке:**

```
Было:
  Task 2: /design-create (включая шаг 7 — артефакты)
  Task 3: /plan-test-create
  Task 4: /plan-dev-create
  Task 5: /dev-create

Стало:
  Task 2: /design-create (DRAFT → WAITING, БЕЗ артефактов)
  Task 3: /plan-test-create (читает Design напрямую — НЕ заблокирован /docs-sync)
  Task 4: /plan-dev-create
  Task 5: /docs-sync (NEW — артефакты из Design + Plan Tests)
  Task 6: /dev-create (получает per-tech, Code Map, Planned Changes)
```

**Почему после Plan Dev, а не после Design:**

| Критерий | После Design | После Plan Dev |
|----------|-------------|----------------|
| Plan Tests блокирован? | Да (blockedBy) | **Нет** |
| testing.md данные | 0% из Design | **~60% из Plan Tests** |
| Конфликт timing testing.md | Да (OQ-3) | **Нет** |
| Per-tech до кодирования | Да | **Да** |
| Code Map для dev-agent | Да | **Да** |
| Planned Changes для review | Да | **Да** |
| CONFLICT-детекция | Ранняя | **Ранняя** |

**Воркфлоу /docs-sync:**

1. **Вход:** Все 4 документа в WAITING (Discussion, Design, Plan Tests, Plan Dev), путь к design.md
2. **Анализ:** Определить затронутые сервисы (SVC-N), технологии (Выбор технологий), системные файлы
3. **Cross-chain guard:** Проверить нет ли другой цепочки с pending /docs-sync (см. OQ-19)
4. **Параллельный запуск агентов:**

```
┌──────────────────────────────────────────────────────────────────┐
│                        /docs-sync                                │
│  Вход: Design WAITING + Plan Tests WAITING + Plan Dev WAITING    │
│                                                                  │
│  Волна 1: Создание (параллельно)                                │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │service-agent │ │service-agent │ │service-agent │            │
│  │  (task.md)   │ │  (auth.md)   │ │(frontend.md) │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │tech-agent    │ │tech-agent    │ │tech-agent    │ ...        │
│  │ (react)      │ │ (express)    │ │ (prisma)     │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                                  │
│  ┌──────────────────────────────────────────────────┐           │
│  │ system-agent (overview, conventions,             │           │
│  │   infrastructure, testing)                       │           │
│  │   Источники: Design + Plan Tests                │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
│  Волна 2: Ревью (после завершения Волны 1, параллельно)         │
│  ┌──────────────────┐ ┌──────────────────┐ ┌────────────────┐  │
│  │service-reviewer  │ │technology-reviewer│ │system-reviewer │  │
│  │(× N, по сервису) │ │(все standard-*.md)│ │(все .system/)  │  │
│  └──────────────────┘ └──────────────────┘ └────────────────┘  │
│                                                                  │
│  Волна 3: Исправления (если REVISE)                             │
│  → Перезапуск ТОЛЬКО агентов с REVISE → Повторный ревью         │
└──────────────────────────────────────────────────────────────────┘
```

5. **Волна 1 (параллельно):**
   - N × service-agent (один на сервис, параллельно)
   - M × technology-agent (один на технологию, параллельно) — уже существует
   - 1 × system-agent (один на все .system/ файлы, читает Design + Plan Tests)
6. **Волна 2 (после Волны 1, параллельно):**
   - N × service-reviewer (один на сервис — сверка {svc}.md с Design SVC-N)
   - 1 × technology-reviewer (сверка per-tech стандартов — уже существует)
   - 1 × system-reviewer (сверка .system/ файлов с Design + Plan Tests)
7. **Волна 3 (если REVISE):** перезапуск только тех агентов, чьи ревьюеры вернули REVISE → повторный ревью
8. **Выход:** Все specs/docs/ обновлены, ревью всех трёх сущностей пройдено

---

### 4. Изменения в существующих файлах

> **Ключевое упрощение:** Позиция после Plan Dev означает, что аналитическая цепочка (Discussion → Design → Plan Tests → Plan Dev) НЕ меняется. /docs-sync — отдельный шаг ПОСЛЕ аналитики, ПЕРЕД dev. Файлы plan-test/ НЕ требуют изменений.

**Файлы design/:**

| Файл | Что изменить |
|------|-------------|
| `create-design.md` | Шаг 7: оставить ТОЛЬКО DRAFT → WAITING через chain_status.py. Удалить: таблицу артефактов (строки 1-6), Planned Changes, заглушки, per-tech, шаг 7.5 (ревью per-tech). Шаг 8 (отчёт): убрать артефакты. **Шаг 9 (авто-предложение): НЕ менять** — Design по-прежнему предлагает Plan Tests. Чек-лист: убрать пункты артефактов |
| `standard-design.md` | § 4 Переходы: убрать побочные эффекты артефактов при WAITING. § Связи: добавить "После аналитической цепочки → /docs-sync → Dev" |
| `modify-design.md` | Строка 305 (аналитическая цепочка): оставить `Discussion → Design → Plan Tests → Plan Dev` (это анализ, /docs-sync — отдельный шаг) |

**Файлы plan-test/: НЕТ ИЗМЕНЕНИЙ**

Plan Tests идёт сразу после Design (как и раньше). "После одобрения Design (WAITING)" — корректно. Никаких blockedBy /docs-sync.

**Файлы plan-dev/:**

| Файл | Что изменить |
|------|-------------|
| `modify-plan-dev.md` | Строки 255, 420: полная цепочка (включая /docs-sync и Dev) — добавить /docs-sync после Plan Dev |

**Файлы discussion/:**

| Файл | Что изменить |
|------|-------------|
| `modify-discussion.md` | Строка 313: если упоминает полную цепочку с Dev — добавить /docs-sync. Если только аналитическую (Discussion → Design → Plan Tests → Plan Dev) — оставить |

**Оркестрационные файлы:**

| Файл | Что изменить |
|------|-------------|
| `create-chain.md` | Добавить Task /docs-sync между Plan Dev и Dev (Task 5). Сдвинуть нумерацию 5-12 → 6-13. Обновить blockedBy. Обновить таблицу Happy Path: 12 → 13 задач |
| `standard-process.md` | Добавить шаг "Docs Sync" между Фазой 1 (аналитика) и Фазой 2 (Dev). Таблица инструментов: добавить строку /docs-sync. Диаграмма: добавить шаг |

**Файлы БЕЗ изменений (обоснование):**

| Файл | Почему не меняется |
|------|-------------------|
| `create-chain-done.md` | DONE каскад по state-документам. У /docs-sync нет state-документа |
| `create-rollback.md` | Откат по state-документам. Артефакты specs/docs/ откатываются через git |
| `chain_status.py` DONE_CASCADE_ORDER | Не затронут — /docs-sync не участвует в каскаде |
| **Все plan-test/ файлы** | **Plan Tests идёт сразу после Design — позиция не изменилась** |
| `standard-discussion.md` | Ссылается только на Discussion → Design (не на полную цепочку) |
| `create-discussion.md` | Предлагает только Design как следующий шаг (корректно) |
| `validation-discussion.md` | Чисто валидационные правила, без ссылок на цепочку |

**Новые файлы:**

| Файл | Тип |
|------|-----|
| `.claude/agents/service-agent/AGENT.md` | Агент |
| `.claude/agents/service-reviewer/AGENT.md` | Ревьюер |
| `.claude/agents/system-agent/AGENT.md` | Агент |
| `.claude/agents/system-reviewer/AGENT.md` | Ревьюер |
| `.claude/skills/docs-sync/SKILL.md` | Скилл |
| `specs/.instructions/create-docs-sync.md` | Воркфлоу (SSOT для скилла) |

---

### 5. Оркестрация

**Скилл /docs-sync:**

```
/docs-sync <design-path>
```

| Параметр | Описание | Обязательный |
|----------|---------|-------------|
| design-path | Путь к design.md (в WAITING) | Да |

**SSOT:** specs/.instructions/create-docs-sync.md

**Шаги:**

1. Проверить все 4 документа в WAITING (Discussion, Design, Plan Tests, Plan Dev)
2. **Cross-chain guard:** проверить нет ли другой цепочки с pending /docs-sync (см. OQ-19)
3. Определить: какие сервисы (SVC-N), какие технологии ("Выбрано"), какие .system/ файлы затронуты
4. Волна 1 — запуск агентов параллельно:
   - service-agent × N (Task tool, параллельно)
   - technology-agent × M (Task tool, параллельно) — через существующий /technology-create
   - system-agent × 1 (Task tool, с путём к design.md И plan-test.md)
5. Дождаться завершения Волны 1
6. Обновить specs/docs/README.md (оркестратор, не агенты — избежать конфликтов)
7. Волна 2 — запуск ревьюеров параллельно:
   - service-reviewer × N (Task tool, параллельно — один на сервис)
   - technology-reviewer × 1 (через существующий шаг)
   - system-reviewer × 1 (Task tool, с путём к design.md И plan-test.md)
8. Обработка результатов:
   - Все ACCEPT → завершить
   - Есть REVISE → перезапуск ТОЛЬКО агентов с REVISE → повторный ревью (Волна 3)
   - Максимум 3 итерации Волна 3, потом эскалация пользователю

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| D-1 | Выделить артефакты в отдельный шаг /docs-sync | Шаг 7 create-design.md перегружен; отдельный шаг позволяет параллельный запуск и ревью |
| D-2 | service-agent: один на сервис (параллельно) | По аналогии с technology-agent; каждый сервис независим |
| D-3 | system-agent: один на все файлы | 4 файла .system/ связаны между собой (overview ссылается на conventions); раздельные агенты создали бы конфликты |
| D-4 | ~~Без reviewer для service/system~~ → **С reviewer для всех трёх сущностей** | Агенты могут исказить факты при копировании: пропустить, добавить лишнее, переформулировать. Ревьюер сверяет результат с Design и ЖЁСТКО пресекает расхождения |
| D-5 | /docs-sync вызывается из /chain, а не из /design-create | Чистое разделение: Design отвечает за проектирование, /docs-sync — за синхронизацию документации |
| D-6 | SSOT в корне specs/.instructions/ | create-docs-sync.md рядом с create-chain.md (оба — оркестрационные воркфлоу верхнего уровня) |
| D-7 | /docs-sync — шаг БЕЗ state-документа | Не участвует в DONE-каскаде и rollback. Артефакты specs/docs/ откатываются через git. chain-done и rollback без изменений |
| D-8 | Антигаллюцинации в промптах всех агентов | ЖЁСТКИЙ запрет на придумывание. Каждый факт — источник в Design. Нет данных = пустая секция |
| D-9 | **Позиция /docs-sync: после Plan Dev, перед Dev** | Снимает блокировку Plan Tests (OQ-6). Даёт system-agent доступ к Plan Tests для testing.md (OQ-3). Сохраняет все преимущества: per-tech до кодирования, Code Map для dev, Planned Changes для review. Аналитическая цепочка (4 документа) не меняется |

---

## Решённые вопросы

| # | Вопрос | Решение | Обоснование |
|---|--------|---------|-------------|
| Q-1 | ~~service-reviewer нужен?~~ | ~~**Нет**~~ → **Да** | Агент может исказить факты при копировании. Ревьюер сверяет {svc}.md с Design SVC-N и выявляет: MISSING, INVENTED, DISTORTED |
| Q-2 | system-agent: scope? | **Все 4 файла** | Агент сам определяет "нет изменений". Проще оркестрация |
| Q-3 | service-agent: контент? | **Строго из Design** | Агент НЕ придумывает ничего, берёт информацию ИСКЛЮЧИТЕЛЬНО из Design SVC-N и распределяет по секциям {svc}.md |
| Q-4 | Название? | **/docs-sync** | Универсальное: и create, и update. Sync = Design → specs/docs/ |
| Q-5 | standard-docs-sync.md? | **Нет, только воркфлоу** | create-docs-sync.md в `specs/.instructions/` (рядом с другими create-*.md). Стандарты у сущностей уже есть |
| Q-6 | system-reviewer нужен? | **Да** | Аналогичная логика Q-1: system-agent тоже может исказить факты |
| Q-7 | chain-done/rollback менять? | **Нет** | /docs-sync без state-документа. Не участвует в DONE-каскаде. Артефакты откатываются через git |
| Q-8 | ~~Plan Tests blockedBy /docs-sync?~~ | **Нет — позиция решает** | /docs-sync после Plan Dev. Plan Tests идёт сразу после Design как раньше. Блокировки нет |
| Q-9 | ~~testing.md при Design WAITING?~~ | **Нет — позиция решает** | /docs-sync после Plan Dev: system-agent получает Plan Tests TC-N → testing.md заполняется на ~60% |
| Q-10 | ~~"Копировать + расширить"?~~ | **Уточнено** | "Дополнить § 1" = ТОЛЬКО из Discussion REQ-N (явный источник). Записано в маппинге и антигаллюцинациях |

**Следствия Q-1 + Q-6 (пересмотр):**
- Добавлены service-reviewer и system-reviewer
- Волна 2 теперь включает ВСЕ три ревьюера (не только technology-reviewer)
- Формат ревью: ACCEPT / REVISE (с классификацией MISSING/INVENTED/DISTORTED)

**Следствия Q-5:**
- SSOT: `specs/.instructions/create-docs-sync.md` (не в подпапке docs-sync/)
- Нет standard-docs-sync.md, validation-docs-sync.md, modify-docs-sync.md

---

## Открытые вопросы

> Результат проверки 10 параллельными агентами + анализ альтернативной позиции

### CRITICAL — нужно решить до реализации

**OQ-1: .system/ файлы НЕ имеют секции "Planned Changes"**

Драфт ссылается на "Planned Changes в overview.md § 8" — но overview.md имеет только 6 секций. НИ ОДИН .system/ файл не имеет секции Planned Changes или Changelog. Эта концепция существует ТОЛЬКО в {svc}.md (§ 9, § 10).

Решение для позиции "после Plan Dev": system-agent делает **inline-правки** (не Planned Changes). system-reviewer проверяет diff. Концепция Planned Changes НЕ добавляется в .system/ стандарты.

**OQ-2: Данные Design НЕ маппятся на .system/ механически (~50→65% success rate)**

Позиция после Plan Dev улучшает ситуацию для testing.md (0% → ~60% из Plan Tests), но infrastructure.md по-прежнему ~0%:

| .system/ файл | Из Design | Из Plan Tests | Итого |
|---------------|-----------|---------------|-------|
| overview.md | ~70% | — | ~70% |
| conventions.md | ~40% | — | ~40% |
| infrastructure.md | ~0% | — | ~0% |
| testing.md | ~0% | **~60%** | **~60%** |

**infrastructure.md остаётся проблемой.** Порты, docker-compose, env-переменные — из имплементации. Варианты:
1. system-agent пишет только то, что известно из Design (имена сервисов, DB из Tech Stack)
2. infrastructure.md заполняется на этапе DONE (когда код есть)
3. infrastructure.md исключить из scope system-agent

**OQ-4: service-agent vs /service-create — конфликт механизмов**

Скилл `/service-create` уже существует. service-agent mode=create делает то же самое. Варианты:
1. service-agent заменяет /service-create для chain-контекста
2. service-agent вызывает /service-create внутри себя
3. service-agent использует create-service.md workflow напрямую

**OQ-19: Cross-chain guard (НОВЫЙ — критический)**

Если Chain A завершила Plan Dev но /docs-sync ещё не запустился, а Chain B начинает /discussion-create — Design Chain B читает **устаревшие** specs/docs/ (без артефактов Chain A).

Окно уязвимости: время от Design WAITING до /docs-sync completion (≈ Plan Tests + Plan Dev + /docs-sync). При позиции "после Design" окно = 0.

Варианты решения:
1. **Pre-flight блокировка:** /chain проверяет нет ли цепочек с Plan Dev WAITING но без /docs-sync — СТОП, запустить /docs-sync сначала
2. **Auto-run:** Если при старте /chain обнаружен pending /docs-sync — запустить его автоматически перед Discussion
3. **Маркер:** /docs-sync пишет маркер завершения (файл `.docs-sync-done` или frontmatter в design.md: `docs-synced: true`)
4. **Принять риск:** Chain B читает design.md других цепочек напрямую (Unified Scan — 5 источников), cross-chain check при DONE поймает конфликты
5. **Запретить параллельные цепочки:** Пока /docs-sync не завершён — новая цепочка блокирована

### IMPORTANT — нужно решить или учесть

**OQ-8: chain_status.py нуждается в обновлении**

AUTO_PROPOSE dict: `"plan-dev": "/dev-create {chain_id}"` → нужно `/docs-sync {chain_id}`. SIDE_EFFECTS dict: артефакты при Design WAITING → убрать/переместить.

**OQ-9: standard-analysis.md не упомянут в изменениях**

§ 7.1 описывает создание артефактов при Design WAITING — перенести на /docs-sync. Матрица документов. Chain sequence в аналитической цепочке НЕ меняется (Discussion → Design → Plan Tests → Plan Dev), но полная цепочка с Dev — да.

**OQ-10: CLAUDE.md не упомянут**

Таблица "6 фаз процесса" — нужна строка /docs-sync (между аналитикой и Dev).

**OQ-11: Параллельный доступ к specs/docs/README.md**

Решение: README.md обновляет оркестратор ПОСЛЕ Волны 1, а не каждый агент.

**OQ-12: system-reviewer git diff в dirty working tree**

system-reviewer определяет "что изменил system-agent" через git diff. Per-file diff для .system/ файлов: `git diff -- specs/docs/.system/`.

**OQ-13: Agent metadata отсутствует**

Для 4 новых агентов не указаны: model, max_turns, type, permissionMode. technology-agent: model=sonnet, max_turns=75.

**OQ-14: Wave 3 feedback mechanism**

Как ревьюер передаёт замечания обратно агенту? Механизм: ревьюер возвращает REVISE-таблицу как текст → оркестратор передаёт её в prompt при перезапуске агента.

**OQ-15: Modify workflows для .system/ уже существуют**

modify-overview.md (7 сценариев), modify-conventions.md (7), modify-infrastructure.md (6), modify-testing.md (6). system-agent должен ИСПОЛЬЗОВАТЬ эти workflows (читать стандарты, вызывать валидацию).

**OQ-16: Валидационные скрипты для .system/ существуют**

validate-docs-overview.py, validate-docs-conventions.py, validate-docs-infrastructure.py, validate-docs-testing.py. Агенты должны вызывать их после обновления.

**OQ-17: SVC-N §§ 1-9 vs §§ 1-8**

§ 9 (Решения по реализации) — Design-only, не переносится. Исправлено в маппинге: "SVC-N §§ 1-8 → 8 секций".

**OQ-18: technology-agent вызывается через Skill, не через Task**

technology-agent вызывается через `/technology-create` (Skill tool). Оркестратор /docs-sync должен вызывать Skill, не Task напрямую.

---

## Дополнительные файлы для обновления

> Результат проверки 8 агентами по specs/.instructions/ — с учётом новой позиции

### Скрипты

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `chain_status.py` | AUTO_PROPOSE: `"plan-dev"` → "/docs-sync". SIDE_EFFECTS: убрать артефакты из Design WAITING | CRITICAL |
| `analysis-status.py` | DOCS_DISPLAY — может потребовать новую строку для /docs-sync | MEDIUM |

### Стандарты analysis/

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `standard-analysis.md` | § 7.1 артефакты при Design WAITING → убрать/перенести на /docs-sync. Полная цепочка (с Dev) → добавить /docs-sync. Аналитическая цепочка (4 документа) — БЕЗ ИЗМЕНЕНИЙ | CRITICAL |

### Инструкции analysis/ — УПРОЩЕНИЕ

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| **plan-test/*** | **НЕТ ИЗМЕНЕНИЙ** (Plan Tests сразу после Design) | — |
| `modify-plan-dev.md` | Строки 255, 420: полная цепочка → добавить /docs-sync после Plan Dev | LOW |
| `modify-discussion.md` | Если полная цепочка → добавить /docs-sync. Если аналитическая — оставить | LOW |

### Инструкции docs/

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `create-technology.md` | Строки 174-176: ссылка на create-design.md Шаг 10 → заменить на /docs-sync оркестрацию | HIGH |
| `standard-docs.md` | Строка 126: "LLM обновляет" → уточнить: service-agent, system-agent, technology-agent | MEDIUM |
| `create-service.md` | Добавить: автоматическое создание через /docs-sync (service-agent) | MEDIUM |
| `modify-service.md` | Сценарии 5-6: Planned Changes генерируются service-agent | LOW |

### Корневые файлы

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `CLAUDE.md` | "6 фаз процесса" → добавить /docs-sync между аналитикой и Dev | HIGH |
| `specs/.instructions/README.md` | Добавить create-docs-sync.md в дерево и таблицу | MEDIUM |
| `create-chain.md` строка 156 | TASK 2 Design описание: "При WAITING: Planned Changes, заглушки, per-tech" → удалить | HIGH |
| `standard-process.md` строки 227-229 | "При Design → WAITING: Planned Changes..." → перенести на /docs-sync | HIGH |

### Файлы БЕЗ изменений (подтверждено)

| Файл | Почему не меняется |
|------|-------------------|
| `create-chain-done.md` | DONE каскад по state-документам |
| `create-rollback.md` | Откат по state-документам, артефакты через git |
| **Все plan-test/ файлы** | **Plan Tests после Design — позиция не изменилась** |
| `validation-design.md` | Зональные границы, не chain sequence |
| `validation-discussion.md` | Чисто валидационные правила |
| Все `validate-docs-*.py` | Валидация контента, не chain workflow |
| Все `validate-analysis-*.py` | Проверяют parent-child, не chain sequence |
| `create-review.md`, `standard-review.md`, `validation-review.md` | Ревью 4 финальных документов |
| Все plan-dev/ (кроме modify) | Plan Dev перед /docs-sync, не затронут |

---

## Tasklist

TASK 1: Создать service-agent
  description: >
    Драфт: секции "2.1" и "5.1".
    Создать `.claude/agents/service-agent/AGENT.md` через `/agent-create`.
    Промпт: create/update specs/docs/{svc}.md на основе Design SVC-N.
    Входные данные: service, design-path, svc-section, mode.
    Маппинг Design SVC-N §§ 1-8 → {svc}.md §§ 1-8 (строго из Design, ничего не придумывать).
    "Дополнить § 1" = ТОЛЬКО из Discussion REQ-N.
    Delta-формат: ADDED/MODIFIED/DELETED в Planned Changes.
    SSOT-зависимости: standard-service.md, create-service.md, validation-service.md.
    Валидация: validate-docs-service.py.
    Tools: Read, Grep, Glob, Edit, Write, Bash.
    АНТИГАЛЛЮЦИНАЦИИ: ЖЁСТКИЙ запрет на придумывание.
  activeForm: Создание service-agent

TASK 2: Создать service-reviewer
  description: >
    Драфт: секции "2.2" и "5.2".
    Создать `.claude/agents/service-reviewer/AGENT.md` через `/agent-create`.
    Промпт: сверка {svc}.md с Design SVC-N — обнаружение MISSING/INVENTED/DISTORTED.
    Один ревьюер на один сервис (параллельный запуск).
    Вердикт: ACCEPT / REVISE (с таблицей расхождений и цитатами из Design).
    Tools: Read, Grep, Glob (только чтение — НЕ модифицирует файлы).
  activeForm: Создание service-reviewer

TASK 3: Создать system-agent
  description: >
    Драфт: секции "2.3" и "5.3".
    Создать `.claude/agents/system-agent/AGENT.md` через `/agent-create`.
    Промпт: обновление specs/docs/.system/ (overview, conventions, infrastructure, testing)
    на основе Design + Plan Tests.
    Один агент на все 4 файла (связаны между собой).
    Источники: Design SVC-N/INT-N/STS-N + Plan Tests TC-N (для testing.md).
    Inline-правки (НЕ Planned Changes — .system/ не имеют этой секции).
    Валидация: validate-docs-*.py после каждого файла.
    SSOT-зависимости: standard-overview.md, standard-conventions.md, standard-infrastructure.md, standard-testing.md.
    Tools: Read, Grep, Glob, Edit, Write, Bash.
    АНТИГАЛЛЮЦИНАЦИИ: ЖЁСТКИЙ запрет на придумывание. Каждое изменение — источник в Design/Plan Tests.
  activeForm: Создание system-agent

TASK 4: Создать system-reviewer
  description: >
    Драфт: секции "2.4" и "5.4".
    Создать `.claude/agents/system-reviewer/AGENT.md` через `/agent-create`.
    Промпт: сверка .system/ файлов с Design + Plan Tests — обнаружение MISSING/INVENTED/DISTORTED.
    Один ревьюер на все 4 файла (по аналогии с system-agent).
    Per-file git diff для .system/ файлов.
    Проверка прослеживаемости: каждое изменение → источник в Design/Plan Tests.
    Проверка согласованности между 4 файлами.
    Вердикт: ACCEPT / REVISE.
    Tools: Read, Grep, Glob (только чтение).
  activeForm: Создание system-reviewer

TASK 5: Создать SSOT-инструкцию create-docs-sync.md
  description: >
    Драфт: секции "3" и "6".
    Создать `specs/.instructions/create-docs-sync.md` — SSOT воркфлоу.
    Вход: все 4 документа в WAITING + путь к design.md.
    Cross-chain guard (OQ-19): проверить pending /docs-sync.
    Шаги: проверка WAITING → определение сервисов/технологий →
    Волна 1 (service-agent × N + technology-agent × M + system-agent × 1, параллельно) →
    README.md update (оркестратор, не агенты) →
    Волна 2 (service-reviewer × N + technology-reviewer × 1 + system-reviewer × 1, параллельно) →
    Волна 3 (если REVISE — перезапуск только агентов с REVISE, макс. 3 итерации).
    Файл в корне specs/.instructions/ (рядом с create-chain.md).
  activeForm: Создание create-docs-sync.md

TASK 6: Создать скилл /docs-sync
  description: >
    Создать `.claude/skills/docs-sync/SKILL.md` через `/skill-create`.
    SSOT: specs/.instructions/create-docs-sync.md.
    Формат: `/docs-sync <design-path>`.
  activeForm: Создание скилла /docs-sync

TASK 7: Обновить create-design.md — вынести артефакты
  description: >
    Изменить `specs/.instructions/analysis/design/create-design.md`:
    - Шаг 7: оставить ТОЛЬКО DRAFT → WAITING через chain_status.py
    - Удалить: таблицу артефактов (строки 1-6), Planned Changes, заглушки, per-tech
    - Удалить: шаг 7.5 (ревью per-tech — перенесён в /docs-sync)
    - Обновить отчёт (шаг 8): убрать артефакты
    - Шаг 9 (авто-предложение): НЕ МЕНЯТЬ — Design → Plan Tests (корректно)
    - Обновить чек-лист: убрать пункты артефактов
    Также изменить:
    - `standard-design.md`: § 4 побочные эффекты WAITING, § Связи
    - `modify-design.md`: полная цепочка → добавить /docs-sync (если упоминается)

  activeForm: Обновление design/ инструкций

TASK 8: Обновить create-chain.md — добавить /docs-sync в TaskList
  description: >
    Изменить `specs/.instructions/create-chain.md`:
    - Добавить задачу /docs-sync между Plan Dev и Dev
    - Было: Task 4 Plan Dev → Task 5 Dev
    - Стало: Task 4 Plan Dev → Task 5 /docs-sync → Task 6 Dev
    - Сдвинуть нумерацию задач 5-12 → 6-13
    - Обновить blockedBy зависимости
    - Обновить таблицу Happy Path: 12 → 13 задач
    - TASK 2 Design описание: убрать "При WAITING: Planned Changes, заглушки, per-tech"
  activeForm: Обновление create-chain.md

TASK 9: Обновить standard-process.md
  description: >
    Изменить `specs/.instructions/standard-process.md`:
    - Добавить шаг "Docs Sync" между Фазой 1 (аналитика) и Фазой 2 (Dev)
    - Таблица инструментов (§ 8.1): добавить строку /docs-sync с агентами
    - Диаграмма обзора: добавить шаг после Plan Dev, перед Dev
    - Строки 227-229: "При Design → WAITING: Planned Changes..." → перенести на /docs-sync
    Запустить `/migration-create` после изменения стандарта.
  activeForm: Обновление standard-process.md

TASK 10: Обновить chain_status.py и standard-analysis.md
  description: >
    chain_status.py:
    - AUTO_PROPOSE: "plan-dev" → "/docs-sync {chain_id}" (вместо "/dev-create")
    - SIDE_EFFECTS[("design", "WAITING")]: убрать артефакты
    standard-analysis.md:
    - § 7.1: убрать артефакты из Design WAITING → описать /docs-sync
    - Полная цепочка: добавить /docs-sync
    - Аналитическая цепочка (4 документа): БЕЗ ИЗМЕНЕНИЙ
  activeForm: Обновление chain_status.py и standard-analysis.md

TASK 11: Обновить остальные файлы (CLAUDE.md, docs/, minor)
  description: >
    - CLAUDE.md: "6 фаз" → добавить /docs-sync
    - specs/.instructions/README.md: добавить create-docs-sync.md
    - create-technology.md: строки 174-176 → /docs-sync
    - standard-docs.md: "LLM обновляет" → агенты
    - create-service.md: автоматическое создание через /docs-sync
    - modify-plan-dev.md: полная цепочка → добавить /docs-sync
    - modify-discussion.md: полная цепочка → добавить /docs-sync (если есть)
  activeForm: Обновление остальных файлов

TASK 12: Валидация и тест
  description: >
    1. `/draft-validate` на черновик
    2. Валидация всех изменённых файлов (агенты, инструкции, стандарты)
    3. Тест: запустить `/docs-sync` на цепочке 0001-task-dashboard (все 4 документа в WAITING)
    4. Проверить: 3 сервиса (task.md, auth.md, frontend.md) + per-tech стандарты + .system/ обновлены
    5. Проверить: testing.md содержит данные из Plan Tests TC-N
    6. Проверить: ревью всех трёх сущностей пройдено
  activeForm: Валидация и тестирование
