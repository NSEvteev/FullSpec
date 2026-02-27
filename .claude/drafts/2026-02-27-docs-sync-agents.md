# Docs Sync — агенты для specs/docs/ и новый шаг в /chain

Выделение артефактов Design (шаг 7) в отдельный шаг цепочки с тремя парами агентов для трёх сущностей specs/docs/.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблема](#1-проблема)
  - [2. Решение: три пары агентов](#2-решение-три-пары-агентов)
  - [3. Новый шаг: /docs-sync](#3-новый-шаг-docs-sync)
  - [4. Изменения в существующих файлах](#4-изменения-в-существующих-файлах)
  - [5. Детали агентов](#5-детали-агентов)
  - [6. Оркестрация](#6-оркестрация)
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
- Design SVC-N §§ 1-9 → напрямую маппятся на 8 из 10 секций {svc}.md
- Design INT-N → § 6 Зависимости
- Discussion REQ-N → контекст для § 1 Назначение

**Маппинг Design SVC-N → {svc}.md:**

| Design SVC-N § | {svc}.md § | Действие |
|----------------|-----------|----------|
| § 1 Назначение | § 1 Назначение | Копировать + расширить |
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
- Если в Design SVC-N нет данных для секции — оставить секцию пустой с маркером `_Нет данных в Design SVC-N._`
- ЗАПРЕЩЕНО: добавлять "очевидные" поля, дефолтные значения, примеры из "общих знаний"

**Tools:** Read, Grep, Glob, Edit, Write, Bash (для валидации)

#### 2.2 service-reviewer (NEW)

**Роль:** Сверка specs/docs/{svc}.md с Design SVC-N — обнаружение расхождений.

**Что проверяет:**
1. **Полнота:** Каждый факт из Design SVC-N §§ 1-8 присутствует в {svc}.md
2. **Точность:** Ни один факт в {svc}.md не "придуман" (отсутствует в Design SVC-N)
3. **Целостность:** Данные не искажены при копировании (переформулировка, потеря деталей)
4. **Формат:** 10 секций соответствуют standard-service.md

**Алгоритм:**
1. Прочитать Design SVC-N (источник правды)
2. Прочитать {svc}.md (результат агента)
3. Для каждой секции §§ 1-8 построить diff: что в Design vs что в {svc}.md
4. Выявить: пропущенное (в Design есть, в {svc}.md нет), придуманное (в {svc}.md есть, в Design нет), искажённое (факт есть, но изменён)
5. Вердикт: ACCEPT (нет расхождений) / REVISE (список расхождений с цитатами из Design)

**Параллельный запуск:** Один ревьюер на один сервис (по аналогии с агентом).

**Tools:** Read, Grep, Glob (только чтение — ревьюер НЕ модифицирует файлы)

#### 2.3 system-agent (NEW)

**Роль:** Обновление specs/docs/.system/ (overview.md, conventions.md, infrastructure.md, testing.md) на основе Design.

**Режимы:**
- `update` — основной: обновляет системные документы из Design (новые сервисы, связи, конвенции)
- `create` — только при инициализации проекта (/init-project), обычно не используется

**Входные данные:**
```
design-path: specs/analysis/NNNN-{topic}/design.md
mode: update (default)
```

**Что обновляет в каждом файле:**

| Файл | Секция | Источник данных из Design |
|------|--------|--------------------------|
| overview.md | § Карта сервисов | Новые SVC-N (type: новый) |
| overview.md | § Связи между сервисами | INT-N (паттерн, участники) |
| overview.md | § Сквозные потоки | Design SVC-N § 4 (ключевые потоки) |
| overview.md | § Контекстная карта доменов | Design SVC-N § 7 (агрегаты, события) |
| conventions.md | § API конвенции | Если Design вводит новые паттерны |
| conventions.md | § Формат ответов/ошибок | Если Design определяет новые форматы |
| infrastructure.md | § Docker Compose | Новые сервисы + их порты |
| infrastructure.md | § Переменные окружения | Новые env из Design (JWT_SECRET и пр.) |
| testing.md | § Системные тест-сценарии | Design STS-N |
| testing.md | § Межсервисные сценарии | Design INT-N |

**Запуск:** Один агент на все системные файлы (они связаны между собой).

**Антигаллюцинации (КРИТИЧЕСКИ ВАЖНО):**
- ЗАПРЕЩЕНО придумывать, додумывать, интерпретировать, расширять информацию из Design
- Каждое изменение в .system/ файлах ОБЯЗАНО прослеживаться до конкретного места в Design (SVC-N §X, INT-N, STS-N)
- Если Design не содержит данных для секции — НЕ ТРОГАТЬ секцию
- ЗАПРЕЩЕНО: добавлять "очевидные" порты, "стандартные" переменные, "типичные" конвенции
- Формат каждого изменения: `<!-- Source: Design SVC-N §X / INT-N / STS-N -->`

**Tools:** Read, Grep, Glob, Edit, Write, Bash

#### 2.4 system-reviewer (NEW)

**Роль:** Сверка изменений в specs/docs/.system/ с Design — обнаружение расхождений.

**Что проверяет:**
1. **Прослеживаемость:** Каждое изменение в .system/ файлах имеет источник в Design (SVC-N, INT-N, STS-N)
2. **Полнота:** Все релевантные данные из Design перенесены в .system/ файлы
3. **Точность:** Ни одно изменение не "придумано" (отсутствует в Design)
4. **Согласованность:** Данные между 4 файлами .system/ не противоречат друг другу

**Алгоритм:**
1. Прочитать Design полностью (Резюме, SVC-N, INT-N, STS-N)
2. Прочитать все 4 файла .system/ (текущее состояние после system-agent)
3. Определить diff: что изменил system-agent
4. Для каждого изменения проверить: есть ли источник в Design?
5. Проверить обратное: есть ли в Design данные, не отражённые в .system/?
6. Вердикт: ACCEPT / REVISE (список расхождений с цитатами из Design)

**Запуск:** Один ревьюер на все .system/ файлы (по аналогии с system-agent).

**Tools:** Read, Grep, Glob (только чтение — ревьюер НЕ модифицирует файлы)

---

### 3. Новый шаг: /docs-sync

**Идея:** Выделить артефакты Design (текущий шаг 7 create-design.md) в отдельный шаг цепочки, который оркестрирует все три пары агентов.

**Характеристики шага:**
- Task в TaskList `/chain` (между Design и Plan Tests)
- **БЕЗ собственного state-документа** (нет docs-sync.md со статусами DRAFT/WAITING/RUNNING/DONE)
- НЕ участвует в DONE-каскаде и rollback (chain_status.py, create-chain-done.md, create-rollback.md — без изменений)
- Артефакты specs/docs/ откатываются через git при rollback ветки

**Место в цепочке:**

```
Было:
  Task 2: /design-create (включая шаг 7 — артефакты)
  Task 3: /plan-test-create

Стало:
  Task 2: /design-create (DRAFT → WAITING, БЕЗ артефактов)
  Task 3: /docs-sync (NEW — артефакты из Design)
  Task 4: /plan-test-create
```

**Воркфлоу /docs-sync:**

1. **Вход:** Design в WAITING, путь к design.md
2. **Анализ:** Определить затронутые сервисы (SVC-N), технологии (Выбор технологий), системные файлы
3. **Параллельный запуск агентов:**

```
┌──────────────────────────────────────────────────────────────────┐
│                        /docs-sync                                │
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
│  ┌──────────────────────────────────────┐                       │
│  │ system-agent (overview, conventions, │                       │
│  │   infrastructure, testing)           │                       │
│  └──────────────────────────────────────┘                       │
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

4. **Волна 1 (параллельно):**
   - N × service-agent (один на сервис, параллельно)
   - M × technology-agent (один на технологию, параллельно) — уже существует
   - 1 × system-agent (один на все .system/ файлы)
5. **Волна 2 (после Волны 1, параллельно):**
   - N × service-reviewer (один на сервис — сверка {svc}.md с Design SVC-N)
   - 1 × technology-reviewer (сверка per-tech стандартов — уже существует)
   - 1 × system-reviewer (сверка .system/ файлов с Design)
6. **Волна 3 (если REVISE):** перезапуск только тех агентов, чьи ревьюеры вернули REVISE → повторный ревью
7. **Выход:** Все specs/docs/ обновлены, ревью всех трёх сущностей пройдено

---

### 4. Изменения в существующих файлах

**Файлы design/:**

| Файл | Что изменить |
|------|-------------|
| `create-design.md` | Шаг 7: оставить ТОЛЬКО DRAFT → WAITING через chain_status.py. Удалить: таблицу артефактов (строки 1-6), Planned Changes, заглушки, per-tech, шаг 7.5 (ревью per-tech). Шаг 8 (отчёт): убрать артефакты, добавить "Следующий шаг: /docs-sync". **Шаг 9 (авто-предложение): изменить "Plan Tests" → "/docs-sync"**. Чек-лист: убрать пункты артефактов |
| `standard-design.md` | § 4 Переходы: убрать побочные эффекты артефактов при WAITING. § Связи: добавить "/docs-sync между Design и Plan Tests" |
| `modify-design.md` | Строка 305: `Discussion → Design → Plan Tests → Plan Dev` → `Discussion → Design → /docs-sync → Plan Tests → Plan Dev` |

**Файлы plan-test/:**

| Файл | Что изменить |
|------|-------------|
| `standard-plan-test.md` | Принцип: "После одобрения Design (WAITING)" → "После выполнения /docs-sync (которая запускается после Design WAITING)". § Когда создавать: аналогично |
| `create-plan-test.md` | Строка 52: "Plan Tests — после Design" → "Plan Tests — после /docs-sync". Добавить в шаг 1 проверку: "/docs-sync был выполнен" |

**Файлы discussion/:**

| Файл | Что изменить |
|------|-------------|
| `modify-discussion.md` | Строка 313: `Discussion → Design → Plan Tests → Plan Dev` → `Discussion → Design → /docs-sync → Plan Tests → Plan Dev` |

**Оркестрационные файлы:**

| Файл | Что изменить |
|------|-------------|
| `create-chain.md` | Добавить Task /docs-sync между Design и Plan Tests (Task 3). Сдвинуть нумерацию 3-12 → 4-13. Обновить blockedBy. Обновить таблицу Happy Path: 12 → 13 задач |
| `standard-process.md` | Фаза 1: добавить шаг 1.2.1 "Docs Sync" после Design. Таблица инструментов (§ 8.1): добавить строку /docs-sync. Диаграмма: добавить шаг |

**Файлы БЕЗ изменений (обоснование):**

| Файл | Почему не меняется |
|------|-------------------|
| `create-chain-done.md` | DONE каскад по state-документам (plan-dev → plan-test → design → discussion). У /docs-sync нет state-документа |
| `create-rollback.md` | Откат по state-документам. Артефакты specs/docs/ откатываются через git при откате ветки |
| `chain_status.py` | DONE_CASCADE_ORDER не затронут — /docs-sync не участвует в каскаде |
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

### 5. Детали агентов

#### 5.1 service-agent

**Паттерн:** Аналог technology-agent. Один агент на один сервис. Параллельный запуск.

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
6. Обновить specs/docs/README.md (добавить сервис)
7. Запустить валидацию: validate-service.py
8. Self-review перед возвратом

**Алгоритм (mode=update):**
1. Прочитать существующий {svc}.md
2. Прочитать Design SVC-N
3. Обновить § 9 Planned Changes
4. Обновить §§ 1-8 если есть MODIFIED маркеры
5. Запустить валидацию

**Tools:** Read, Grep, Glob, Edit, Write, Bash (для валидации)

**Антигаллюцинации:** См. секцию 2.1.

#### 5.2 service-reviewer

**Паттерн:** Аналог technology-reviewer. Один ревьюер на один сервис. Параллельный запуск.

**Алгоритм:**
1. Прочитать Design SVC-N §§ 1-8 (источник правды)
2. Прочитать {svc}.md §§ 1-8 (результат service-agent)
3. Построить diff по каждой секции: Design vs {svc}.md
4. Выявить расхождения:
   - **MISSING:** факт есть в Design, отсутствует в {svc}.md
   - **INVENTED:** факт есть в {svc}.md, отсутствует в Design
   - **DISTORTED:** факт есть в обоих, но изменён/переформулирован
5. Проверить § 9 Planned Changes: каждый ADDED/MODIFIED маркер соответствует Design
6. Вердикт:
   - **ACCEPT:** нет расхождений
   - **REVISE:** список расхождений с цитатами из Design SVC-N

**Формат вывода при REVISE:**
```
REVISE — {svc}.md

| # | Тип | Секция | В Design SVC-N | В {svc}.md | Рекомендация |
|---|-----|--------|----------------|-----------|--------------|
| 1 | INVENTED | § 3 Data Model | — | "поле updatedAt" | Удалить — отсутствует в Design |
| 2 | MISSING | § 2 API | "PATCH /tasks/:id" | — | Добавить из Design SVC-N § 2 |
```

**Tools:** Read, Grep, Glob (только чтение)

#### 5.3 system-agent

**Паттерн:** Отличается от technology-agent — один агент на все 4 файла (они связаны между собой).

**SSOT-зависимости:**
- [standard-overview.md](/specs/.instructions/docs/overview/standard-overview.md)
- [standard-conventions.md](/specs/.instructions/docs/conventions/standard-conventions.md)
- [standard-infrastructure.md](/specs/.instructions/docs/infrastructure/standard-infrastructure.md)
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md)

**Алгоритм (mode=update):**
1. Прочитать Design полностью (Резюме, SVC-N, INT-N, STS-N)
2. Прочитать текущие 4 файла .system/
3. Для каждого файла определить delta (что добавить/изменить)
4. Применить изменения: overview → conventions → infrastructure → testing (порядок важен)
5. Записать Planned Changes в overview.md § 8 (если существует такая секция)
6. Запустить валидацию каждого файла

**Tools:** Read, Grep, Glob, Edit, Write, Bash

**Антигаллюцинации:** См. секцию 2.3.

#### 5.4 system-reviewer

**Паттерн:** Один ревьюер на все 4 файла (по аналогии с system-agent).

**Алгоритм:**
1. Прочитать Design полностью (источник правды)
2. Прочитать все 4 файла .system/ (результат system-agent)
3. Определить: что изменил system-agent (diff с предыдущей версией через git)
4. Для каждого изменения проверить: есть ли источник в Design? (SVC-N §X, INT-N, STS-N)
5. Проверить обратное: есть ли в Design данные, не отражённые в .system/?
6. Проверить согласованность: данные между 4 файлами не противоречат друг другу
7. Вердикт:
   - **ACCEPT:** нет расхождений
   - **REVISE:** список расхождений с цитатами из Design

**Формат вывода при REVISE:**
```
REVISE — .system/

| # | Тип | Файл | Секция | В Design | В .system/ | Рекомендация |
|---|-----|------|--------|----------|-----------|--------------|
| 1 | INVENTED | infrastructure.md | § Docker | — | "порт 6379 Redis" | Удалить — отсутствует в Design |
| 2 | MISSING | overview.md | § Связи | INT-2 REST | — | Добавить из Design INT-2 |
```

**Tools:** Read, Grep, Glob (только чтение)

---

### 6. Оркестрация

**Скилл /docs-sync:**

```
/docs-sync <design-path>
```

| Параметр | Описание | Обязательный |
|----------|---------|-------------|
| design-path | Путь к design.md (в WAITING) | Да |

**SSOT:** specs/.instructions/create-docs-sync.md

**Шаги:**

1. Проверить Design в WAITING
2. Определить: какие сервисы (SVC-N), какие технологии ("Выбрано"), какие .system/ файлы затронуты
3. Волна 1 — запуск агентов параллельно:
   - service-agent × N (Task tool, параллельно)
   - technology-agent × M (Task tool, параллельно) — через существующий /technology-create
   - system-agent × 1 (Task tool)
4. Дождаться завершения Волны 1
5. Волна 2 — запуск ревьюеров параллельно:
   - service-reviewer × N (Task tool, параллельно — один на сервис)
   - technology-reviewer × 1 (через существующий шаг)
   - system-reviewer × 1 (Task tool)
6. Обработка результатов:
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

---

## Решённые вопросы

| # | Вопрос | Решение | Обоснование |
|---|--------|---------|-------------|
| Q-1 | ~~service-reviewer нужен?~~ | ~~**Нет**~~ → **Да** | Агент может исказить факты при копировании. Ревьюер сверяет {svc}.md с Design SVC-N и выявляет: MISSING, INVENTED, DISTORTED. Жёстко пресекает расхождения |
| Q-2 | system-agent: scope? | **Все 4 файла** | Агент сам определяет "нет изменений". Проще оркестрация |
| Q-3 | service-agent: контент? | **Строго из Design** | Агент НЕ придумывает ничего, берёт информацию ИСКЛЮЧИТЕЛЬНО из Design SVC-N и распределяет по секциям {svc}.md |
| Q-4 | Название? | **/docs-sync** | Универсальное: и create, и update. Sync = Design → specs/docs/ |
| Q-5 | standard-docs-sync.md? | **Нет, только воркфлоу** | create-docs-sync.md в `specs/.instructions/` (рядом с другими create-*.md). Стандарты у сущностей уже есть |
| Q-6 | system-reviewer нужен? | **Да** | Аналогичная логика Q-1: system-agent тоже может исказить факты. Ревьюер сверяет .system/ с Design |
| Q-7 | chain-done/rollback менять? | **Нет** | /docs-sync без state-документа. Не участвует в DONE-каскаде. Артефакты откатываются через git |

**Следствия Q-1 + Q-6 (пересмотр):**
- Добавлены service-reviewer и system-reviewer
- Волна 2 теперь включает ВСЕ три ревьюера (не только technology-reviewer)
- Формат ревью: ACCEPT / REVISE (с классификацией MISSING/INVENTED/DISTORTED)

**Следствия Q-5:**
- SSOT: `specs/.instructions/create-docs-sync.md` (не в подпапке docs-sync/)
- Нет standard-docs-sync.md, validation-docs-sync.md, modify-docs-sync.md

---

## Открытые вопросы

> Результат проверки 10 параллельными агентами (self-review, external review, 8 agents по specs/.instructions/)

### CRITICAL — нужно решить до реализации

**OQ-1: .system/ файлы НЕ имеют секции "Planned Changes"**

Драфт ссылается на "Planned Changes в overview.md § 8" — но overview.md имеет только 6 секций (Назначение системы, Карта сервисов, Связи, Сквозные потоки, Контекстная карта доменов, Shared-код). НИ ОДИН .system/ файл не имеет секции Planned Changes или Changelog. Эта концепция существует ТОЛЬКО в {svc}.md (§ 9, § 10).

Варианты решения:
1. Добавить Planned Changes в стандарты .system/ (4 миграции standard-*.md + validation-*.py)
2. system-agent делает inline-правки (не Planned Changes), ревьюер проверяет diff
3. Переосмыслить system-agent: он обновляет ТОЛЬКО то, что можно механически перенести

**OQ-2: Данные Design НЕ маппятся на .system/ механически (~50% success rate)**

Детальный анализ показал фундаментальное несоответствие:

| .system/ файл | Что МОЖНО из Design | Что НЕЛЬЗЯ из Design |
|---------------|---------------------|---------------------|
| overview.md | Карта сервисов (имена, зоны, API из SVC-N), Связи (из INT-N), Контекстная карта (агрегаты из SVC-N § 7) | Shared-код интерфейсы, Сквозные потоки (нужна переработка формата) |
| conventions.md | Аутентификация (JWT из SVC-2), Формат ответов (частично из API контрактов) | Логирование, формат ошибок (таблица кодов), критичность, пагинация, версионирование |
| infrastructure.md | — | Порты, docker-compose, env-переменные, хранилища, Service Discovery (ВСЁ из имплементации, не из Design) |
| testing.md | — | Стратегия тестирования, мокирование, структура файлов (из Plan Tests, не из Design) |

**infrastructure.md и testing.md фактически НЕ могут быть заполнены из Design.** Infrastructure = данные из docker-compose/Dockerfile. Testing = стратегия из Plan Tests.

**OQ-3: testing.md обновляется при Plan Tests DONE, не при Design WAITING**

Per standard-analysis.md, testing.md обновляется на этапе Plan Tests → DONE. system-agent на этапе /docs-sync (после Design WAITING) НЕ должен трогать testing.md. Нужно убрать testing.md из scope system-agent.

**OQ-4: service-agent vs /service-create — конфликт механизмов**

Скилл `/service-create` уже существует (SKILL.md + create-service.md workflow). service-agent mode=create делает то же самое. Два механизма создания {svc}.md = путаница. Варианты:
1. service-agent заменяет /service-create для chain-контекста
2. service-agent вызывает /service-create внутри себя
3. service-agent использует create-service.md workflow напрямую

**OQ-5: "Копировать + расширить" противоречит антигаллюцинациям**

В маппинге: `§ 1 Назначение | Копировать + расширить`. Антигаллюцинации: "ЗАПРЕЩЕНО расширять". Что значит "расширить"? Если из Discussion REQ-N — указать явно. Иначе это дыра для галлюцинаций.

**OQ-6: Plan Tests blockedBy /docs-sync — нужно ли ждать?**

Plan Tests читает ТОЛЬКО Design (SVC-N, INT-N, STS-N), а НЕ specs/docs/. Если blockedBy [docs-sync], Plan Tests не может начаться пока ВСЕ docs/ обновлены + reviewed. При 3 сервисах + 7 технологий = значительная задержка. Альтернатива: /docs-sync ПАРАЛЛЕЛЬНО с Plan Tests (оба читают Design, не зависят друг от друга).

**OQ-7: /chain --resume state detection**

/docs-sync не имеет state-документа. Если сессия прервалась mid-Wave-2, как `/chain --resume` определяет прогресс? Нужна стратегия: проверить какие файлы созданы, какие reviewed.

### IMPORTANT — нужно решить или учесть

**OQ-8: chain_status.py нуждается в обновлении**

AUTO_PROPOSE dict (строка 149): `"design": "/plan-test-create {chain_id}"` → нужно `/docs-sync {chain_id}`. SIDE_EFFECTS dict: артефакты при Design WAITING → убрать/переместить.

**OQ-9: standard-analysis.md не упомянут в изменениях**

Содержит chain sequence (Discussion → Design → Plan Tests → Plan Dev) в нескольких местах. § 7.1 описывает создание артефактов при Design WAITING. Матрица документов. Всё нужно обновить.

**OQ-10: CLAUDE.md не упомянут**

Фаза 1 таблица: "Discussion → Design → Plan Tests → Plan Dev" — нужно добавить /docs-sync. Таблица "6 фаз процесса" — нужна строка /docs-sync.

**OQ-11: Параллельный доступ к specs/docs/README.md**

Несколько service-agents (параллельно) обновляют один README.md при создании сервисов → конфликт записи. Решение: README.md обновляет оркестратор ПОСЛЕ Волны 1, а не каждый агент.

**OQ-12: system-reviewer git diff в dirty working tree**

system-reviewer хочет определить "что изменил system-agent" через git diff. Но в working tree также изменения service-agents и technology-agents. Нужен per-file diff или другой механизм.

**OQ-13: Agent metadata отсутствует**

Для 4 новых агентов не указаны: model, max_turns, type, permissionMode. technology-agent: model=sonnet, max_turns=75. Нужно определить аналоги.

**OQ-14: Wave 3 feedback mechanism**

Как ревьюер передаёт замечания обратно агенту? Ревьюер возвращает REVISE-таблицу. Агент должен получить её как входные данные при перезапуске. Механизм не описан.

**OQ-15: Modify workflows для .system/ уже существуют**

modify-overview.md (7 сценариев), modify-conventions.md (7), modify-infrastructure.md (6), modify-testing.md (6). system-agent должен ИСПОЛЬЗОВАТЬ эти workflows (читать стандарты, вызывать валидацию), а не изобретать свои. Но может ли агент вызвать modify-workflow?

**OQ-16: Валидационные скрипты для .system/ существуют**

validate-docs-overview.py, validate-docs-conventions.py, validate-docs-infrastructure.py, validate-docs-testing.py. Агенты должны вызывать их после обновления. Это не описано в алгоритмах.

**OQ-17: SVC-N §§ 1-9 vs §§ 1-8**

Строка 95: "Design SVC-N §§ 1-9 → маппятся на 8 из 10 секций". § 9 (Решения по реализации) — Design-only, не переносится. Текст вводит в заблуждение. Нужно: "SVC-N §§ 1-8 → маппятся на 8 секций. § 9 — Design-only."

**OQ-18: technology-agent вызывается через Skill, не через Task**

Строка 472: "technology-agent × M (Task tool)". На самом деле technology-agent вызывается через `/technology-create` (Skill tool). Смешение механизмов запуска.

---

## Дополнительные файлы для обновления

> Результат проверки 8 агентами по specs/.instructions/ — файлы, которых НЕТ в секции 4

### Скрипты

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `chain_status.py` | AUTO_PROPOSE: "design" → "/docs-sync". SIDE_EFFECTS: убрать артефакты из Design WAITING | CRITICAL |
| `analysis-status.py` | DOCS_DISPLAY — зависит от chain_status.py, может потребовать новую строку для /docs-sync | MEDIUM |

### Стандарты analysis/

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `standard-analysis.md` | Chain sequence (строки 12, 325, 446, 1044+). § 7.1 артефакты при Design WAITING. Матрица документов | CRITICAL |

### Инструкции analysis/discussion/

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `standard-discussion.md` | Строка 107: "(Design, Plan Tests, Plan Dev)" → добавить docs-sync | LOW |
| `create-discussion.md` | Строка 51: "(Design, Plan Tests, Plan Dev)" → добавить docs-sync | LOW |

### Инструкции analysis/plan-test/ (дополнительные строки)

| Файл | Строки | Что менять | Приоритет |
|------|--------|-----------|-----------|
| `standard-plan-test.md` | 75, 93 | "После Design (WAITING)" → "после /docs-sync" (в дополнение к строке 52) | HIGH |
| `create-plan-test.md` | 66-72 | Шаг 1 целиком: "Проверить parent Design" → добавить проверку /docs-sync | HIGH |
| `create-plan-test.md` | 72 | Сообщение об ошибке: обновить текст | MEDIUM |
| `create-plan-test.md` | 258 | Чек-лист: "Parent Design в WAITING" → добавить /docs-sync | MEDIUM |
| `modify-plan-test.md` | 285 | Chain sequence: добавить /docs-sync | MEDIUM |

### Инструкции analysis/plan-dev/

| Файл | Строки | Что менять | Приоритет |
|------|--------|-----------|-----------|
| `modify-plan-dev.md` | 255, 420 | Chain sequence: "Discussion → Design → Plan Tests → Plan Dev" → добавить /docs-sync | LOW |

### Инструкции docs/

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `create-technology.md` | Строки 174-176: ссылка на create-design.md Шаг 10 → заменить на /docs-sync оркестрацию | HIGH |
| `standard-docs.md` | Строка 126: "LLM обновляет" → уточнить: service-agent, system-agent, technology-agent | MEDIUM |
| `create-service.md` | Добавить секцию: автоматическое создание через /docs-sync (service-agent) | MEDIUM |
| `modify-service.md` | Сценарии 5-6: уточнить что Planned Changes генерируются service-agent | LOW |

### Корневые файлы

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `CLAUDE.md` | Фаза 1 таблица + "6 фаз процесса" → добавить /docs-sync | HIGH |
| `specs/.instructions/README.md` | Добавить create-docs-sync.md в дерево и таблицу | MEDIUM |
| `create-chain.md` строка 156 | TASK 2 Design описание содержит "При WAITING: Planned Changes, заглушки, per-tech" → удалить | HIGH |
| `standard-process.md` строки 227-229 | "При Design → WAITING: Planned Changes..." → перенести на /docs-sync | HIGH |

### Файлы БЕЗ изменений (подтверждено)

| Файл | Почему не меняется |
|------|-------------------|
| `create-chain-done.md` | DONE каскад по state-документам, у /docs-sync нет state-документа |
| `create-rollback.md` | Откат по state-документам, артефакты через git |
| `validation-design.md` | Зональные границы, не chain sequence |
| `validation-discussion.md` | Чисто валидационные правила |
| Все `validate-docs-*.py` | Валидация контента, не chain workflow |
| Все `validate-analysis-*.py` | Проверяют parent-child, не chain sequence |
| `create-review.md`, `standard-review.md`, `validation-review.md` | Ревью 4 финальных документов, /docs-sync не затрагивает |
| Все plan-dev/ (кроме modify) | Plan Dev после Plan Tests, не затронут |

---

## Tasklist

TASK 1: Создать service-agent
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секции "2.1" и "5.1")
    Создать `.claude/agents/service-agent/AGENT.md` через `/agent-create`.
    Промпт: create/update specs/docs/{svc}.md на основе Design SVC-N.
    Входные данные: service, design-path, svc-section, mode.
    Маппинг Design SVC-N §§ 1-8 → {svc}.md §§ 1-8 (строго из Design, ничего не придумывать).
    Delta-формат: ADDED/MODIFIED/DELETED в Planned Changes.
    SSOT-зависимости: standard-service.md, create-service.md, validation-service.md.
    Tools: Read, Grep, Glob, Edit, Write, Bash.
    АНТИГАЛЛЮЦИНАЦИИ: ЖЁСТКИЙ запрет на придумывание. Каждый факт — источник в Design.
    Нет данных в Design = пустая секция с маркером.
  activeForm: Создание service-agent

TASK 2: Создать service-reviewer
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "2.2" и "5.2")
    Создать `.claude/agents/service-reviewer/AGENT.md` через `/agent-create`.
    Промпт: сверка {svc}.md с Design SVC-N — обнаружение MISSING/INVENTED/DISTORTED.
    Один ревьюер на один сервис (параллельный запуск).
    Вердикт: ACCEPT / REVISE (с таблицей расхождений и цитатами из Design).
    Tools: Read, Grep, Glob (только чтение — НЕ модифицирует файлы).
  activeForm: Создание service-reviewer

TASK 3: Создать system-agent
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секции "2.3" и "5.3")
    Создать `.claude/agents/system-agent/AGENT.md` через `/agent-create`.
    Промпт: обновление specs/docs/.system/ (overview, conventions, infrastructure, testing) на основе Design.
    Один агент на все 4 файла (связаны между собой). Строго из Design, ничего не придумывать.
    SSOT-зависимости: standard-overview.md, standard-conventions.md, standard-infrastructure.md, standard-testing.md.
    Tools: Read, Grep, Glob, Edit, Write, Bash.
    АНТИГАЛЛЮЦИНАЦИИ: ЖЁСТКИЙ запрет на придумывание. Каждое изменение — источник в Design.
  activeForm: Создание system-agent

TASK 4: Создать system-reviewer
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секции "2.4" и "5.4")
    Создать `.claude/agents/system-reviewer/AGENT.md` через `/agent-create`.
    Промпт: сверка .system/ файлов с Design — обнаружение MISSING/INVENTED/DISTORTED.
    Один ревьюер на все 4 файла (по аналогии с system-agent).
    Проверка прослеживаемости: каждое изменение → источник в Design (SVC-N §X, INT-N, STS-N).
    Проверка согласованности между 4 файлами.
    Вердикт: ACCEPT / REVISE.
    Tools: Read, Grep, Glob (только чтение).
  activeForm: Создание system-reviewer

TASK 5: Создать SSOT-инструкцию create-docs-sync.md
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секции "3" и "6")
    Создать `specs/.instructions/create-docs-sync.md` — SSOT воркфлоу.
    Шаги: проверка Design WAITING → определение сервисов/технологий →
    Волна 1 (service-agent × N + technology-agent × M + system-agent × 1, параллельно) →
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
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "4")
    Изменить `specs/.instructions/analysis/design/create-design.md`:
    - Шаг 7: оставить ТОЛЬКО DRAFT → WAITING через chain_status.py
    - Удалить: таблицу артефактов (строки 1-6), Planned Changes, заглушки, per-tech
    - Удалить: шаг 7.5 (ревью per-tech — перенесён в /docs-sync)
    - Обновить отчёт (шаг 8): убрать артефакты, добавить "Следующий шаг: /docs-sync"
    - Шаг 9 (авто-предложение): изменить "Plan Tests" → "/docs-sync"
    - Обновить чек-лист: убрать пункты артефактов
    Также изменить:
    - `standard-design.md`: § 4 побочные эффекты WAITING, § Связи (добавить /docs-sync)
    - `modify-design.md`: строка 305 последовательность → добавить /docs-sync
  activeForm: Обновление design/ инструкций

TASK 8: Обновить plan-test/ инструкции
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "4")
    Изменить `specs/.instructions/analysis/plan-test/standard-plan-test.md`:
    - "После одобрения Design (WAITING)" → "После выполнения /docs-sync"
    - § Когда создавать: аналогично
    Изменить `specs/.instructions/analysis/plan-test/create-plan-test.md`:
    - Строка 52: "Plan Tests — после Design" → "Plan Tests — после /docs-sync"
    - Шаг 1: добавить проверку "/docs-sync был выполнен"
  activeForm: Обновление plan-test/ инструкций

TASK 9: Обновить modify-discussion.md
  description: >
    Изменить `specs/.instructions/analysis/discussion/modify-discussion.md`:
    - Строка 313: `Discussion → Design → Plan Tests → Plan Dev` →
      `Discussion → Design → /docs-sync → Plan Tests → Plan Dev`
  activeForm: Обновление modify-discussion.md

TASK 10: Обновить create-chain.md — добавить /docs-sync в TaskList
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "4")
    Изменить `specs/.instructions/create-chain.md`:
    - Добавить задачу /docs-sync между Design и Plan Tests
    - Было: Task 2 Design → Task 3 Plan Tests
    - Стало: Task 2 Design → Task 3 /docs-sync → Task 4 Plan Tests
    - Сдвинуть нумерацию задач 3-12 → 4-13
    - Обновить blockedBy зависимости
    - Обновить таблицу Happy Path: 12 → 13 задач
  activeForm: Обновление create-chain.md

TASK 11: Обновить standard-process.md
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "4")
    Изменить `specs/.instructions/standard-process.md`:
    - Фаза 1: добавить шаг 1.2.1 "Docs Sync" после Design (1.2)
    - Таблица инструментов (§ 8.1): добавить строку /docs-sync с агентами
    - Диаграмма обзора: добавить шаг между Design и Plan Tests
    Запустить `/migration-create` после изменения стандарта.
  activeForm: Обновление standard-process.md

TASK 12: Валидация и тест
  description: >
    1. `/draft-validate` на черновик
    2. Валидация всех изменённых файлов (агенты, инструкции, стандарты)
    3. Тест: запустить `/docs-sync` на цепочке 0001-task-dashboard (Design WAITING)
    4. Проверить: 3 сервиса (task.md, auth.md, frontend.md) + per-tech стандарты + .system/ обновлены
    5. Проверить: ревью всех трёх сущностей пройдено (service-reviewer, technology-reviewer, system-reviewer)
  activeForm: Валидация и тестирование
