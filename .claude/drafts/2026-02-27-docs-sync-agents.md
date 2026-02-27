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
- [Открытые вопросы](#открытые-вопросы)
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
- Нет ревью сервисных и системных документов (только per-tech имеет reviewer)

**Целевое состояние (TO BE):**

Три пары агентов покрывают все три сущности specs/docs/:

| Сущность | Путь | Create-агент | Review | Обоснование |
|----------|------|-------------|--------|-------------|
| Per-tech стандарты | specs/docs/.technologies/ | technology-agent ✅ | technology-reviewer ✅ | Генерируют контент → ревью нужен |
| Per-service документы | specs/docs/{svc}.md | **service-agent** (NEW) | validate-service.py | Копируют факты из Design → ревью не нужен |
| Системная архитектура | specs/docs/.system/ | **system-agent** (NEW) | валидация стандартов | Копируют факты из Design → ревью не нужен |

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

**Ревью не нужен:** Агент берёт факты из Design SVC-N (не генерирует контент). Достаточно validate-service.py для проверки формата 10 секций.

#### 2.2 system-agent (NEW)

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

**Ревью не нужен:** Агент берёт факты из Design (не генерирует контент). Достаточно валидации по стандартам каждого файла.

---

### 3. Новый шаг: /docs-sync

**Идея:** Выделить артефакты Design (текущий шаг 7 create-design.md) в отдельный шаг цепочки, который оркестрирует все три пары агентов.

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
┌─────────────────────────────────────────────────────────────┐
│                     /docs-sync                               │
│                                                              │
│  Волна 1: Создание (параллельно)                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │service-agent │ │service-agent │ │service-agent │        │
│  │  (task.md)   │ │  (auth.md)   │ │(frontend.md) │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │tech-agent    │ │tech-agent    │ │tech-agent    │ ...    │
│  │ (react)      │ │ (express)    │ │ (prisma)     │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                              │
│  ┌──────────────────────────────────────┐                   │
│  │ system-agent (overview, conventions, │                   │
│  │   infrastructure, testing)           │                   │
│  └──────────────────────────────────────┘                   │
│                                                              │
│  Волна 2: Ревью per-tech (после завершения Волны 1)          │
│  ┌──────────────────┐                                       │
│  │technology-reviewer│  (только per-tech — они генерируются) │
│  │(все standard-*.md)│                                       │
│  └──────────────────┘                                       │
│                                                              │
│  Волна 3: Исправления per-tech (если REVISE)                │
│  → Перезапуск technology-agent → Повторный ревью            │
└─────────────────────────────────────────────────────────────┘
```

4. **Волна 1 (параллельно):**
   - N × service-agent (один на сервис, параллельно)
   - M × technology-agent (один на технологию, параллельно) — уже существует
   - 1 × system-agent (один на все .system/ файлы)
5. **Волна 2 (после Волны 1):**
   - 1 × technology-reviewer (только per-tech — они генерируются, а не копируются)
   - service-agent и system-agent ревью НЕ нужен (данные = факт из Design)
6. **Волна 3 (если REVISE per-tech):** исправления technology-agent → повторный technology-reviewer
7. **Выход:** Все specs/docs/ обновлены, per-tech ревью пройдено

---

### 4. Изменения в существующих файлах

| Файл | Что изменить |
|------|-------------|
| `specs/.instructions/analysis/design/create-design.md` | Шаг 7: удалить артефакты 1-5 (оставить только DRAFT → WAITING). Артефакт 6 (per-tech) тоже вынести. Шаги 7.5, 8, 9 перенумеровать. Шаг 8 (отчёт) — убрать артефакты из отчёта |
| `specs/.instructions/create-chain.md` | Добавить задачу `/docs-sync` между Design и Plan Tests (Task 3). Сдвинуть нумерацию задач 3-12 → 4-13. Обновить blockedBy |
| `specs/.instructions/standard-process.md` | Фаза 1: добавить шаг 1.2.1 "Docs Sync" после Design. Обновить таблицу инструментов (§ 8.1). Обновить диаграмму |
| `specs/.instructions/analysis/design/standard-design.md` | § 4 Переходы статусов: убрать побочные эффекты артефактов при WAITING. Ссылка на /docs-sync |

**Новые файлы:**

| Файл | Тип |
|------|-----|
| `.claude/agents/service-agent/AGENT.md` | Агент |
| `.claude/agents/system-agent/AGENT.md` | Агент |
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

#### 5.2 system-agent

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
   - service-reviewer × 1
   - technology-reviewer × 1 — через существующий шаг 7.5
   - system-reviewer × 1
6. Обработка результатов:
   - Все ACCEPT → завершить
   - Есть REVISE → исправить → повторить ревью

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| D-1 | Выделить артефакты в отдельный шаг /docs-sync | Шаг 7 create-design.md перегружен; отдельный шаг позволяет параллельный запуск и ревью |
| D-2 | service-agent: один на сервис (параллельно) | По аналогии с technology-agent; каждый сервис независим |
| D-3 | system-agent: один на все файлы | 4 файла .system/ связаны между собой (overview ссылается на conventions); раздельные агенты создали бы конфликты |
| D-4 | Без reviewer для service/system | Агенты копируют факты из Design (не генерируют). Ревью факта избыточен — достаточно скриптовой валидации. Reviewer только для per-tech (technology-reviewer) — per-tech генерируют контент |
| D-5 | /docs-sync вызывается из /chain, а не из /design-create | Чистое разделение: Design отвечает за проектирование, /docs-sync — за синхронизацию документации |
| D-6 | SSOT в корне specs/.instructions/ | create-docs-sync.md рядом с create-chain.md (оба — оркестрационные воркфлоу верхнего уровня) |

---

## Решённые вопросы

| # | Вопрос | Решение | Обоснование |
|---|--------|---------|-------------|
| Q-1 | service-reviewer нужен? | **Нет** | Агент берёт ФАКТ из Design (не генерирует), пишет Planned Changes в delta-формате (ADDED/MODIFIED/DELETED). Ревью факта не нужно — достаточно validate-service.py |
| Q-2 | system-agent: scope? | **Все 4 файла** | Агент сам определяет "нет изменений". Проще оркестрация |
| Q-3 | service-agent: контент? | **Строго из Design** | Агент НЕ придумывает ничего, берёт информацию ИСКЛЮЧИТЕЛЬНО из Design SVC-N и распределяет по секциям {svc}.md |
| Q-4 | Название? | **/docs-sync** | Универсальное: и create, и update. Sync = Design → specs/docs/ |
| Q-5 | standard-docs-sync.md? | **Нет, только воркфлоу** | create-docs-sync.md в `specs/.instructions/` (рядом с другими create-*.md). Стандарты у сущностей уже есть |

**Следствия Q-1:**
- Убран service-reviewer из плана (был 2.2)
- Убран system-reviewer из плана (аналогичная логика: system-agent тоже берёт факты из Design)
- Волна 2 (ревью) остаётся только для technology-reviewer (per-tech стандарты генерируются, а не копируются)

**Следствия Q-5:**
- SSOT: `specs/.instructions/create-docs-sync.md` (не в подпапке docs-sync/)
- Нет standard-docs-sync.md, validation-docs-sync.md, modify-docs-sync.md

---

## Tasklist

TASK 1: Создать service-agent
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "5.1 service-agent")
    Создать `.claude/agents/service-agent/AGENT.md` через `/agent-create`.
    Промпт: create/update specs/docs/{svc}.md на основе Design SVC-N.
    Входные данные: service, design-path, svc-section, mode.
    Маппинг Design SVC-N §§ 1-8 → {svc}.md §§ 1-8 (строго из Design, ничего не придумывать).
    Delta-формат: ADDED/MODIFIED/DELETED в Planned Changes.
    SSOT-зависимости: standard-service.md, create-service.md, validation-service.md.
    Tools: Read, Grep, Glob, Edit, Write, Bash.
    Ревьюер НЕ нужен — данные из Design = факт, достаточно validate-service.py.
  activeForm: Создание service-agent

TASK 2: Создать system-agent
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "5.3 system-agent")
    Создать `.claude/agents/system-agent/AGENT.md` через `/agent-create`.
    Промпт: обновление specs/docs/.system/ (overview, conventions, infrastructure, testing) на основе Design.
    Один агент на все 4 файла (связаны между собой). Строго из Design, ничего не придумывать.
    SSOT-зависимости: standard-overview.md, standard-conventions.md, standard-infrastructure.md, standard-testing.md.
    Tools: Read, Grep, Glob, Edit, Write, Bash.
    Ревьюер НЕ нужен — данные из Design = факт.
  activeForm: Создание system-agent

TASK 3: Создать SSOT-инструкцию create-docs-sync.md
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "3. Новый шаг" и "6. Оркестрация")
    Создать `specs/.instructions/create-docs-sync.md` — SSOT воркфлоу.
    Шаги: проверка Design WAITING → определение сервисов/технологий →
    Волна 1 (service-agent × N + technology-agent × M + system-agent × 1, параллельно) →
    Волна 2 (technology-reviewer × 1, только для per-tech) →
    Волна 3 (если REVISE — только per-tech).
    Файл в корне specs/.instructions/ (рядом с create-chain.md).
  activeForm: Создание create-docs-sync.md

TASK 4: Создать скилл /docs-sync
  description: >
    Создать `.claude/skills/docs-sync/SKILL.md` через `/skill-create`.
    SSOT: specs/.instructions/create-docs-sync.md.
    Формат: `/docs-sync <design-path>`.
  activeForm: Создание скилла /docs-sync

TASK 5: Обновить create-design.md — вынести артефакты
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "4. Изменения")
    Изменить `specs/.instructions/analysis/design/create-design.md`:
    - Шаг 7: оставить ТОЛЬКО DRAFT → WAITING через chain_status.py
    - Удалить: таблицу артефактов (строки 1-6), Planned Changes, заглушки, per-tech
    - Удалить: шаг 7.5 (ревью per-tech — перенесён в /docs-sync)
    - Обновить отчёт (шаг 8): убрать артефакты, добавить "Следующий шаг: /docs-sync"
    - Шаг 9 (авто-предложение): изменить на "/docs-sync" вместо "Plan Tests"
    - Обновить чек-лист: убрать пункты артефактов
    Также обновить standard-design.md § 4 (побочные эффекты WAITING).
  activeForm: Обновление create-design.md

TASK 6: Обновить create-chain.md — добавить /docs-sync в TaskList
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "4. Изменения")
    Изменить `specs/.instructions/create-chain.md`:
    - Добавить задачу /docs-sync между Design и Plan Tests
    - Было: Task 2 Design → Task 3 Plan Tests
    - Стало: Task 2 Design → Task 3 /docs-sync → Task 4 Plan Tests
    - Сдвинуть нумерацию задач 3-12 → 4-13
    - Обновить blockedBy зависимости
    - Обновить таблицу Happy Path
  activeForm: Обновление create-chain.md

TASK 7: Обновить standard-process.md
  description: >
    Драфт: .claude/drafts/2026-02-27-docs-sync-agents.md (секция "4. Изменения")
    Изменить `specs/.instructions/standard-process.md`:
    - Фаза 1: добавить шаг 1.2.1 "Docs Sync" после Design (1.2)
    - Таблица инструментов (§ 8.1): добавить строку /docs-sync с агентами
    - Диаграмма обзора: добавить шаг между Design и Plan Tests
    Запустить `/migration-create` после изменения стандарта.
  activeForm: Обновление standard-process.md

TASK 8: Валидация и тест
  description: >
    1. `/draft-validate` на черновик
    2. Валидация всех изменённых файлов
    3. Тест: запустить `/docs-sync` на цепочке 0001-task-dashboard (Design WAITING)
    4. Проверить: 3 сервиса (task.md, auth.md, frontend.md) + per-tech стандарты + .system/ обновлены
  activeForm: Валидация и тестирование
