# Docs Sync — агенты для specs/docs/ и новый шаг в /chain

Выделение артефактов Design (шаг 7) в отдельный шаг цепочки с тремя парами агентов. Позиция: **после Plan Dev, перед Dev** — все 4 документа готовы. Двухфазный system-agent: overview.md при /docs-sync (cross-chain), остальные .system/ при DONE (реальные данные).

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
| Системная архитектура | specs/docs/.system/ | **system-agent** (NEW, двухфазный) | **system-reviewer** (NEW) | Фаза 1 (/docs-sync): только overview.md. Фаза 2 (DONE): все 4 файла из реального кода |

---

### 2. Решение: три пары агентов

#### 2.1 service-agent (NEW)

**Роль:** Создание и обновление specs/docs/{svc}.md (10 секций по standard-service.md).

**Режимы** (оба вызываются при `/docs-sync`, mode определяет оркестратор по наличию файла):
- `create` — `specs/docs/{svc}.md` **не существует** → создаёт из шаблона, заполняет 10 секций на основе Design SVC-N (workflow: create-service.md)
- `update` — `specs/docs/{svc}.md` **уже существует** → записывает дельты (ADDED/MODIFIED/REMOVED) в § 9 Planned Changes. §§ 1-8 **не трогает** — обновятся при DONE (workflow: modify-service.md)

> **При DONE** service-agent **не вызывается** — скилл /chain-done переносит Planned Changes → AS IS.

**Входные данные:**
```
service: task | auth | frontend (kebab-case)
design-path: specs/analysis/NNNN-{topic}/design.md
discussion-path: specs/analysis/NNNN-{topic}/discussion.md
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
| — | § 9 Planned Changes | Генерировать из delta-маркеров (ADDED/MODIFIED), обернуть в chain-маркер `<!-- chain: NNNN-{topic} -->` ... `<!-- /chain: NNNN-{topic} -->` |
| — | § 10 Changelog | Пустой (заполняется при DONE) |

**При update (Planned Changes):**
- Читает Design SVC-N, находит все ADDED/MODIFIED маркеры
- Записывает в § 9 Planned Changes, оборачивая блок в chain-маркер:
  ```
  <!-- chain: NNNN-{topic} -->
  Из Design NNNN: {список изменений}
  <!-- /chain: NNNN-{topic} -->
  ```
- Chain-маркер обязателен — pre-flight DONE (#6) и rollback проверяют его наличие

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
- [modify-service.md](/specs/.instructions/docs/service/modify-service.md) — воркфлоу обновления (mode=update)
- [validation-service.md](/specs/.instructions/docs/service/validation-service.md) — валидация

**Алгоритм (mode=create):**
1. Прочитать Design SVC-N (целевая секция)
2. Прочитать шаблон из standard-service.md § 5
3. Создать {svc}.md, заполнить §§ 1-8 из Design SVC-N (маппинг 8:8)
4. Заполнить § 9 Planned Changes из delta-маркеров, обернуть в chain-маркер `<!-- chain: NNNN-{topic} -->` ... `<!-- /chain: NNNN-{topic} -->`
5. Оставить § 10 Changelog пустым
6. Запустить валидацию: validate-docs-service.py
7. Self-review перед возвратом

**Алгоритм (mode=update):**
1. Прочитать существующий {svc}.md
2. Прочитать Design SVC-N
3. Записать дельты (ADDED/MODIFIED/REMOVED) в § 9 Planned Changes с chain-маркером
4. §§ 1-8 **НЕ ТРОГАТЬ** — обновятся при DONE (/chain-done применяет Planned Changes → AS IS)
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

#### 2.3 system-agent (NEW, двухфазный)

**Роль:** Обновление specs/docs/.system/ — двухфазный агент с разным scope в зависимости от контекста вызова.

**Обоснование двухфазности:** .system/ файлы неоднородны по доступности данных:

| Файл | Данные из Design | Данные из кода | Когда заполнять |
|------|-----------------|----------------|-----------------|
| **overview.md** | ~70% (карта сервисов, связи) | ~30% (финализация) | **Рано** — нужен для cross-chain |
| **conventions.md** | ~40% (API паттерны) | ~60% (подтверждённые конвенции) | При DONE |
| **infrastructure.md** | ~0% | ~100% (порты, docker, env) | **Только при DONE** |
| **testing.md** | ~0% из Design | ~100% (стратегия, результаты) | **Только при DONE** |

**Режимы:**

- `sync` — при /docs-sync (после Plan Dev, перед Dev): обновляет **ТОЛЬКО overview.md** из Design (карта сервисов, связи, потоки, домены). Цель: "общий знаменатель" архитектуры для cross-chain.
- `done` — при create-chain-done.md (REVIEW → DONE): обновляет **все 4 файла** из Design + Plan Tests + **реального кода**. Цель: финальное состояние .system/ с реальными данными.

**Входные данные (mode=sync):**
```
design-path: specs/analysis/NNNN-{topic}/design.md
mode: sync
```

**Входные данные (mode=done):**
```
design-path: specs/analysis/NNNN-{topic}/design.md
plan-test-path: specs/analysis/NNNN-{topic}/plan-test.md
src-path: src/ (реальный код для infrastructure.md, testing.md)
mode: done
```

**Что обновляет (mode=sync — ТОЛЬКО overview.md):**

| Файл | Секция | Источник данных |
|------|--------|----------------|
| overview.md | § Карта сервисов | Design: новые SVC-N (type: новый) |
| overview.md | § Связи между сервисами | Design: INT-N (паттерн, участники) |
| overview.md | § Сквозные потоки | Design: SVC-N § 4 (ключевые потоки) |
| overview.md | § Контекстная карта доменов | Design: SVC-N § 7 (агрегаты, события) |

**Что обновляет (mode=done — все 4 файла):**

| Файл | Секция | Источник данных |
|------|--------|----------------|
| overview.md | Все секции | Design + финализация из реального кода |
| conventions.md | § API конвенции | Design + реальные паттерны из кода |
| conventions.md | § Формат ответов/ошибок | Design + реальные форматы из кода |
| infrastructure.md | § Docker Compose | **Реальный код**: docker-compose.yml, порты, имена |
| infrastructure.md | § Переменные окружения | **Реальный код**: .env.example, конфигурации |
| testing.md | § Стратегия тестирования | **Plan Tests + реальные тесты** |
| testing.md | § Системные тест-сценарии | **Plan Tests TC-N + реальные тест-файлы** |
| testing.md | § Межсервисные сценарии | **Plan Tests TC-N + Design INT-N + реальные тесты** |
| testing.md | § Покрытие | **Plan Tests: матрица + реальное покрытие** |

**SSOT-зависимости:**
- [standard-overview.md](/specs/.instructions/docs/overview/standard-overview.md)
- [modify-overview.md](/specs/.instructions/docs/overview/modify-overview.md) — workflow обновления overview.md
- [standard-conventions.md](/specs/.instructions/docs/conventions/standard-conventions.md) (только mode=done)
- [modify-conventions.md](/specs/.instructions/docs/conventions/modify-conventions.md) (только mode=done)
- [standard-infrastructure.md](/specs/.instructions/docs/infrastructure/standard-infrastructure.md) (только mode=done)
- [modify-infrastructure.md](/specs/.instructions/docs/infrastructure/modify-infrastructure.md) (только mode=done)
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) (только mode=done)
- [modify-testing.md](/specs/.instructions/docs/testing/modify-testing.md) (только mode=done)

**Алгоритм (mode=sync):**
1. Прочитать Design (Резюме, SVC-N, INT-N)
2. Прочитать текущий overview.md
3. Определить delta: новые сервисы, новые связи, новые потоки
4. Применить inline-правки к overview.md
5. Запустить валидацию: validate-docs-overview.py

**Алгоритм (mode=done):**
1. Прочитать Design полностью (Резюме, SVC-N, INT-N, STS-N)
2. Прочитать Plan Tests (TC-N, стратегия тестирования, матрица покрытия)
3. Прочитать реальный код: docker-compose.yml, .env.example, тест-файлы, src/ структуру
4. Прочитать текущие 4 файла .system/
5. Для каждого файла определить delta:
   - overview.md ← финализация (подтверждение из кода)
   - conventions.md ← Design + реальные паттерны из кода
   - infrastructure.md ← **реальный код** (docker-compose, .env, порты)
   - testing.md ← Plan Tests TC-N + реальные тест-файлы
6. Применить inline-правки (НЕ Planned Changes — .system/ файлы не имеют этой секции)
7. Порядок: overview → conventions → infrastructure → testing
8. Запустить валидацию каждого файла (validate-docs-*.py)

**Запуск:** Один агент на все затронутые файлы (они связаны между собой).

**Антигаллюцинации (КРИТИЧЕСКИ ВАЖНО):**
- ЗАПРЕЩЕНО придумывать, додумывать, интерпретировать, расширять информацию
- mode=sync: каждое изменение в overview.md ОБЯЗАНО прослеживаться до Design (SVC-N §X, INT-N)
- mode=done: каждое изменение ОБЯЗАНО прослеживаться до Design, Plan Tests ИЛИ реального кода (конкретный файл, строка)
- Если источник не содержит данных для секции — НЕ ТРОГАТЬ секцию
- ЗАПРЕЩЕНО: добавлять "очевидные" порты, "стандартные" переменные, "типичные" конвенции
- Формат: `<!-- Source: Design SVC-N §X / INT-N / Plan Tests TC-N / Code: path/to/file -->`

**Tools:** Read, Grep, Glob, Edit, Write, Bash

#### 2.4 system-reviewer (NEW, двухфазный)

**Роль:** Сверка изменений в specs/docs/.system/ с источниками — обнаружение расхождений. Scope зависит от фазы вызова.

**Фазы:**
- **При /docs-sync (mode=sync):** проверяет **ТОЛЬКО overview.md** против Design
- **При DONE (mode=done):** проверяет **все 4 файла** против Design + Plan Tests + реального кода

**Что проверяет (mode=sync — только overview.md):**
1. **Прослеживаемость:** Каждое изменение в overview.md имеет источник в Design (SVC-N, INT-N)
2. **Полнота:** Все новые сервисы и связи из Design отражены в overview.md
3. **Точность:** Ни одно изменение не "придумано" (отсутствует в Design)

**Что проверяет (mode=done — все 4 файла):**
1. **Прослеживаемость:** Каждое изменение имеет источник в Design, Plan Tests или реальном коде
2. **Полнота:** Все релевантные данные перенесены
3. **Точность:** Ни одно изменение не "придумано"
4. **Согласованность:** Данные между 4 файлами .system/ не противоречат друг другу

**Алгоритм (mode=sync):**
1. Прочитать Design (Резюме, SVC-N, INT-N)
2. Прочитать overview.md (текущее состояние после system-agent)
3. Определить diff: `git diff -- specs/docs/.system/overview.md`
4. Для каждого изменения проверить: есть ли источник в Design?
5. Проверить обратное: есть ли в Design данные для overview.md, не отражённые?
6. Вердикт: ACCEPT / REVISE

**Алгоритм (mode=done):**
1. Прочитать Design полностью (Резюме, SVC-N, INT-N, STS-N)
2. Прочитать Plan Tests (TC-N, стратегия, матрица покрытия)
3. Прочитать реальный код (docker-compose.yml, .env.example, тест-файлы)
4. Прочитать все 4 файла .system/ (текущее состояние после system-agent)
5. Определить diff: `git diff -- specs/docs/.system/`
6. Для каждого изменения проверить: есть ли источник в Design, Plan Tests или коде?
7. Проверить обратное: есть ли данные, не отражённые в .system/?
8. Проверить согласованность между 4 файлами
9. Вердикт: ACCEPT / REVISE

**Формат вывода при REVISE:**
```
REVISE — .system/ (mode={sync|done})

| # | Тип | Файл | Секция | В источнике | В .system/ | Рекомендация |
|---|-----|------|--------|-------------|-----------|--------------|
| 1 | INVENTED | overview.md | § Связи | — | "auth↔billing REST" | Удалить — отсутствует в Design |
| 2 | MISSING | overview.md | § Карта | Design SVC-3 (frontend) | — | Добавить из Design SVC-3 |
```

**Запуск:** Один ревьюер на все затронутые файлы (по аналогии с system-agent).

**Tools:** Read, Grep, Glob (только чтение — ревьюер НЕ модифицирует файлы)

---

### 3. Новый шаг: /docs-sync

**Идея:** Выделить артефакты Design (текущий шаг 7 create-design.md) в отдельный шаг цепочки, который оркестрирует все три пары агентов.

**Характеристики шага:**
- Task в TaskList `/chain` (**после Plan Dev, перед Dev**)
- **БЕЗ собственного state-документа** (нет docs-sync.md со статусами DRAFT/WAITING/RUNNING/DONE)
- НЕ участвует в DONE-каскаде и rollback (chain_status.py DONE_CASCADE_ORDER — без изменений). create-rollback.md получает новый артефакт #7 (сброс docs-synced)
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
| testing.md данные | 0% из Design | **При DONE: ~100% из кода + Plan Tests** |
| Конфликт timing testing.md | Да (OQ-3) | **Нет — testing.md при DONE** |
| Per-tech до кодирования | Да | **Да** |
| Code Map для dev-agent | Да | **Да** |
| Planned Changes для review | Да | **Да** |
| CONFLICT-детекция | Ранняя | **Ранняя** |

**Воркфлоу /docs-sync:**

1. **Вход:** Все 4 документа в WAITING (Discussion, Design, Plan Tests, Plan Dev), путь к design.md
2. **Анализ:** Определить затронутые сервисы (SVC-N), технологии (Выбор технологий)

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
│  │ system-agent mode=sync                           │           │
│  │   (ТОЛЬКО overview.md — карта для cross-chain)   │           │
│  │   Источник: Design SVC-N, INT-N                  │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
│  Волна 2: Ревью (после завершения Волны 1, параллельно)         │
│  ┌──────────────────┐ ┌──────────────────┐ ┌────────────────┐  │
│  │service-reviewer  │ │technology-reviewer│ │system-reviewer │  │
│  │(× N, по сервису) │ │(все standard-*.md)│ │(overview.md)   │  │
│  └──────────────────┘ └──────────────────┘ └────────────────┘  │
│                                                                  │
│  Волна 3: Исправления (если REVISE)                             │
│  → Перезапуск ТОЛЬКО агентов с REVISE → Повторный ревью         │
└──────────────────────────────────────────────────────────────────┘

  ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
  │         create-chain-done.md (REVIEW → DONE)                 │
  │                                                               │
  │  system-agent mode=done                                       │
  │    (все 4 файла: overview финализация + conventions +          │
  │     infrastructure + testing)                                  │
  │    Источники: Design + Plan Tests + реальный код              │
  │                                                               │
  │  system-reviewer mode=done                                    │
  │    (все 4 файла — сверка с Design + Plan Tests + код)          │
  └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
```

3. **Волна 1 (параллельно):**
   - N × service-agent (один на сервис, параллельно)
   - M × technology-agent (один на технологию, параллельно) — уже существует
   - 1 × system-agent **mode=sync** (ТОЛЬКО overview.md из Design)
4. **Волна 2 (после Волны 1, параллельно):**
   - N × service-reviewer (один на сервис — сверка {svc}.md с Design SVC-N)
   - 1 × technology-reviewer (сверка per-tech стандартов — уже существует)
   - 1 × system-reviewer **mode=sync** (сверка ТОЛЬКО overview.md с Design)
5. **Волна 3 (если REVISE):** перезапуск только тех агентов, чьи ревьюеры вернули REVISE → повторный ревью
6. **Выход:** Per-service docs, per-tech стандарты, overview.md обновлены и отревьюены

**При DONE (create-chain-done.md):** Отдельный запуск system-agent mode=done + system-reviewer mode=done. См. секцию 4 → create-chain-done.md.

---

### 4. Изменения в существующих файлах

> **Ключевое упрощение:** Позиция после Plan Dev означает, что аналитическая цепочка (Discussion → Design → Plan Tests → Plan Dev) НЕ меняется. /docs-sync — отдельный шаг ПОСЛЕ аналитики, ПЕРЕД dev. Файлы plan-test/ НЕ требуют изменений.

**Файлы design/:**

| Файл | Что изменить |
|------|-------------|
| `create-design.md` | Шаг 7: оставить ТОЛЬКО DRAFT → WAITING через chain_status.py. Удалить: таблицу артефактов (все строки), Planned Changes, заглушки, per-tech, шаг 7.5 (ревью per-tech). Шаг 8 (отчёт): убрать артефакты. **Шаг 9 (авто-предложение): НЕ менять** — Design по-прежнему предлагает Plan Tests. Чек-лист: убрать пункты артефактов |
| `standard-design.md` | § 4 Переходы: убрать побочные эффекты артефактов при WAITING. § Связи: добавить "После аналитической цепочки → /docs-sync → Dev". **§ Frontmatter: добавить опциональное поле `docs-synced: true/false`** (проставляется /docs-sync, проверяется check_pending_docs_sync) |
| `validation-design.md` | **Добавить проверку:** если `docs-synced` присутствует — значение boolean. Поле опционально (отсутствие = не синхронизировано) |
| `modify-design.md` | Где упоминается аналитическая цепочка: оставить `Discussion → Design → Plan Tests → Plan Dev` (это анализ, /docs-sync — отдельный шаг) |

**Файлы plan-test/: НЕТ ИЗМЕНЕНИЙ**

Plan Tests идёт сразу после Design (как и раньше). "После одобрения Design (WAITING)" — корректно. Никаких blockedBy /docs-sync.

**Файлы plan-dev/:**

| Файл | Что изменить |
|------|-------------|
| `modify-plan-dev.md` | Где упоминается полная цепочка (включая Dev) — добавить /docs-sync после Plan Dev |

**Файлы discussion/:**

| Файл | Что изменить |
|------|-------------|
| `modify-discussion.md` | Если упоминает полную цепочку с Dev — добавить /docs-sync. Если только аналитическую (Discussion → Design → Plan Tests → Plan Dev) — оставить |

**Оркестрационные файлы:**

| Файл | Что изменить |
|------|-------------|
| `create-chain.md` | Добавить Task /docs-sync между Plan Dev и Dev (Task 5). Сдвинуть нумерацию 5-12 → 6-13. Обновить blockedBy. Обновить таблицу Happy Path: 12 → 13 задач |
| `standard-process.md` | Добавить шаг "Docs Sync" между Фазой 1 (аналитика) и Фазой 2 (Dev). Таблица инструментов: добавить строку /docs-sync. Диаграмма: добавить шаг |

**Файлы chain-done и rollback (НОВОЕ — двухфазный system-agent, docs-synced):**

| Файл | Что изменить |
|------|-------------|
| `create-chain-done.md` | **Шаг 3:** Заменить нечёткие "Planned Changes → AS IS" для .system/ на запуск system-agent mode=done + system-reviewer mode=done. Шаг 3 остаётся для {svc}.md (Planned Changes → AS IS). **Новый Шаг 3.5:** system-agent mode=done (все 4 файла из Design + Plan Tests + реальный код) → system-reviewer mode=done → Волна 3 при REVISE. **Шаг 4:** Убрать отдельное обновление testing.md — покрывается system-agent mode=done |
| `create-rollback.md` | **Шаг 4:** Артефакт #2 — заменить "удалить chain-маркер из overview.md" → "откатить inline-правки по Design SVC-N (если docs-synced:true)". Артефакт #7 — сброс `docs-synced` из design.md frontmatter |

**Файлы БЕЗ изменений (обоснование):**

| Файл | Почему не меняется |
|------|-------------------|
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
| `.claude/skills/chain-done/SKILL.md` | Скилл (замена chain-done-agent, D-13) |
| `specs/.instructions/create-docs-sync.md` | Воркфлоу (SSOT для скилла /docs-sync) |

**Деактивация агентов:**

| Файл | Действие |
|------|----------|
| `.claude/agents/chain-done-agent/AGENT.md` | Деактивировать через `/agent-modify --deactivate` (D-13). SSOT create-chain-done.md остаётся |

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
2. Определить: какие сервисы (SVC-N), какие технологии ("Выбрано")
4. Волна 1 — запуск агентов параллельно:
   - service-agent × N (Task tool, параллельно)
   - technology-agent × M (Task tool, параллельно) — через существующий /technology-create
   - system-agent × 1 **mode=sync** (Task tool, ТОЛЬКО overview.md из Design)
5. Дождаться завершения Волны 1
6. Обновить specs/docs/README.md (оркестратор, не агенты — избежать конфликтов)
7. Волна 2 — запуск ревьюеров параллельно:
   - service-reviewer × N (Task tool, параллельно — один на сервис)
   - technology-reviewer × 1 (через существующий шаг)
   - system-reviewer × 1 **mode=sync** (Task tool, ТОЛЬКО overview.md)
8. Обработка результатов:
   - Все ACCEPT → завершить
   - Есть REVISE → перезапуск ТОЛЬКО агентов с REVISE → повторный ревью (Волна 3)
   - Максимум 3 итерации Волна 3, потом эскалация пользователю
9. **Маркер:** Записать `docs-synced: true` в frontmatter design.md (для cross-chain guard D-12)

> **Остальные .system/ файлы** (conventions.md, infrastructure.md, testing.md) обновляются при DONE — см. create-chain-done.md (system-agent mode=done).

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| D-1 | Выделить артефакты в отдельный шаг /docs-sync | Шаг 7 create-design.md перегружен; отдельный шаг позволяет параллельный запуск и ревью |
| D-2 | service-agent: один на сервис (параллельно) | По аналогии с technology-agent; каждый сервис независим |
| D-3 | system-agent: один на все затронутые файлы (в рамках одного mode) | Файлы .system/ связаны между собой; раздельные агенты создали бы конфликты |
| D-4 | ~~Без reviewer для service/system~~ → **С reviewer для всех трёх сущностей** | Агенты могут исказить факты при копировании: пропустить, добавить лишнее, переформулировать. Ревьюер сверяет результат с Design и ЖЁСТКО пресекает расхождения |
| D-5 | /docs-sync вызывается из /chain, а не из /design-create | Чистое разделение: Design отвечает за проектирование, /docs-sync — за синхронизацию документации |
| D-6 | SSOT в корне specs/.instructions/ | create-docs-sync.md рядом с create-chain.md (оба — оркестрационные воркфлоу верхнего уровня) |
| D-7 | /docs-sync — шаг БЕЗ state-документа | Не участвует в DONE-каскаде и rollback. Артефакты specs/docs/ откатываются через git. chain-done обновляется (Шаг 3.5: system-agent mode=done), rollback обновляется (П-3.7: артефакты #1, #2, #7) |
| D-8 | Антигаллюцинации в промптах всех агентов | ЖЁСТКИЙ запрет на придумывание. Каждый факт — источник в Design. Нет данных = пустая секция |
| D-9 | **Позиция /docs-sync: после Plan Dev, перед Dev** | Снимает блокировку Plan Tests (OQ-6). Сохраняет все преимущества: per-tech до кодирования, Code Map для dev, Planned Changes для review. Аналитическая цепочка (4 документа) не меняется |
| D-10 | **Двухфазный system-agent: sync (overview) при /docs-sync, done (все 4) при DONE** | overview.md нужен рано для cross-chain ("общий знаменатель" архитектуры). conventions/infrastructure/testing нуждаются в реальных данных из кода — доступны только при DONE. Решает OQ-1 и OQ-2 |
| D-11 | **service-agent выполняет create-service.md / modify-service.md workflow напрямую** | Агент (Task tool) не может вызывать Skill tool. Агент читает Design SVC-N → выполняет SSOT-инструкцию. Скиллы /service-create и /service-modify остаются для ручного вызова вне chain |
| D-12 | **Cross-chain: мягкая блокировка при Design → WAITING + маркер `docs-synced: true`** | Дискуссии создаются и принимаются свободно (Discussion не читает specs/docs/). При переходе **Design → WAITING** скрипт `chain_status.py check_pending_docs_sync()` проверяет: есть ли цепочка M < N с Design+ в WAITING, но без `docs-synced: true`? Если да → отказ: "Завершите /docs-sync для цепочки {M}". /docs-sync пишет `docs-synced: true` в frontmatter design.md |
| D-13 | **Заменить chain-done-agent на скилл /chain-done** | chain-done-agent (Task tool) не имеет Task tool → не может запустить system-agent mode=done. Скилл выполняется main LLM, который имеет все инструменты (Task, Skill, Edit). Прецедент: commit-agent → /commit, pr-create-agent → /pr-create, merge-agent → /merge. На этапе DONE экономия контекста не критична |

---

## Решённые вопросы

| # | Вопрос | Решение | Обоснование |
|---|--------|---------|-------------|
| Q-1 | ~~service-reviewer нужен?~~ | ~~**Нет**~~ → **Да** | Агент может исказить факты при копировании. Ревьюер сверяет {svc}.md с Design SVC-N и выявляет: MISSING, INVENTED, DISTORTED |
| Q-2 | system-agent: scope? | **Двухфазный: sync (overview only) / done (все 4)** | overview.md нужен рано для cross-chain. Остальные 3 файла нуждаются в реальных данных из кода → при DONE |
| Q-3 | service-agent: контент? | **Строго из Design** | Агент НЕ придумывает ничего, берёт информацию ИСКЛЮЧИТЕЛЬНО из Design SVC-N и распределяет по секциям {svc}.md |
| Q-4 | Название? | **/docs-sync** | Универсальное: и create, и update. Sync = Design → specs/docs/ |
| Q-5 | standard-docs-sync.md? | **Нет, только воркфлоу** | create-docs-sync.md в `specs/.instructions/` (рядом с другими create-*.md). Стандарты у сущностей уже есть |
| Q-6 | system-reviewer нужен? | **Да** | Аналогичная логика Q-1: system-agent тоже может исказить факты |
| Q-7 | chain-done/rollback менять? | **chain-done: ДА (system-agent mode=done). rollback: ДА (П-3.7)** | chain-done получает Шаг 3.5 (system-agent mode=done для .system/). rollback: артефакт #1 (закрывающий тег), #2 (inline rollback overview.md), #7 (docs-synced) |
| Q-8 | ~~Plan Tests blockedBy /docs-sync?~~ | **Нет — позиция решает** | /docs-sync после Plan Dev. Plan Tests идёт сразу после Design как раньше. Блокировки нет |
| Q-9 | ~~testing.md при Design WAITING?~~ | **Нет — при DONE** | testing.md заполняется system-agent mode=done при DONE из Plan Tests + реальных тестов (~100%) |
| Q-10 | ~~"Копировать + расширить"?~~ | **Уточнено** | "Дополнить § 1" = ТОЛЬКО из Discussion REQ-N (явный источник). Записано в маппинге и антигаллюцинациях |
| Q-11 | service-agent vs /service-create? | **Агент выполняет workflow напрямую (D-11)** | Агент (Task tool) не может вызывать Skill. Выполняет create-service.md / modify-service.md. Скиллы для ручного вызова |
| Q-12 | Cross-chain guard? | **Мягкая блокировка при Design → WAITING (D-12)** | Discussion свободно. При Design → WAITING — check_pending_docs_sync() проверяет цепочки M < N с Design+ WAITING без docs-synced. Маркер `docs-synced: true` |
| Q-13 | Agent metadata? | **model=sonnet, max_turns=75** | По аналогии с technology-agent. Детали при /agent-create |

**Следствия Q-1 + Q-6 (пересмотр):**
- Добавлены service-reviewer и system-reviewer
- Волна 2 теперь включает ВСЕ три ревьюера (не только technology-reviewer)
- Формат ревью: ACCEPT / REVISE (с классификацией MISSING/INVENTED/DISTORTED)

**Следствия Q-5:**
- SSOT: `specs/.instructions/create-docs-sync.md` (не в подпапке docs-sync/)
- Нет standard-docs-sync.md, validation-docs-sync.md, modify-docs-sync.md

**Следствия Q-11 (OQ-4):**
- service-agent: mode=create выполняет create-service.md, mode=update выполняет modify-service.md
- Скиллы /service-create и /service-modify сохраняются для ручного вызова (вне chain)

**Следствия Q-12 (OQ-19):**
- chain_status.py получает функцию `check_pending_docs_sync()` — сканирует цепочки M < N с Design+ в WAITING без `docs-synced: true`
- Проверка вызывается при T1 (**Design → WAITING**, не Discussion)
- /docs-sync пишет `docs-synced: true` в frontmatter design.md после завершения
- Discussion создаётся и принимается свободно (не читает specs/docs/) — блокировка только при Design → WAITING

---

## Открытые вопросы

> Все вопросы решены. Секция сохранена для трассируемости.

**Открытых вопросов нет.** Все OQ-1..OQ-19 решены — см. таблицу ниже.

| OQ | Статус | Решение | Обоснование |
|---|---|---|---|
| ~~OQ-1~~ | **РЕШЁН (D-10)** | Двухфазный system-agent: inline-правки | .system/ не имеют Planned Changes — и не будут |
| ~~OQ-2~~ | **РЕШЁН (D-10)** | overview при /docs-sync (~70%), остальные при DONE (~100% из кода) | infrastructure.md ~0% из Design → при DONE из реального кода |
| ~~OQ-4~~ | **РЕШЁН (D-11)** | service-agent выполняет create-service.md / modify-service.md workflow напрямую | Агент (Task tool) не может вызывать Skill tool. Скиллы остаются для ручного вызова |
| ~~OQ-8~~ | **РЕШЁН** | chain_status.py: AUTO_PROPOSE двухступенчатый — plan-dev WAITING + !docs-synced → "/docs-sync", plan-dev WAITING + docs-synced:true → "/dev-create". SIDE_EFFECTS: убрать артефакты из Design WAITING. Новая функция `check_pending_docs_sync()` | Описано в Tasklist TASK 10, TASK 8 |
| ~~OQ-9~~ | **РЕШЁН** | standard-analysis.md: § 7.1 артефакты → /docs-sync. Полная цепочка → добавить /docs-sync. Аналитическая (4 документа) — без изменений | Описано в Tasklist TASK 10 |
| ~~OQ-10~~ | **РЕШЁН** | CLAUDE.md: "6 фаз" → добавить /docs-sync | Описано в Tasklist TASK 12 |
| ~~OQ-11~~ | **РЕШЁН** | specs/docs/README.md обновляет оркестратор ПОСЛЕ Волны 1 (не агенты) | Избежать конфликтов записи |
| ~~OQ-12~~ | **РЕШЁН** | system-reviewer: mode=sync → `git diff -- specs/docs/.system/overview.md`. mode=done → `git diff -- specs/docs/.system/` | Per-file diff |
| ~~OQ-13~~ | **РЕШЁН** | 4 новых агента: model=sonnet, max_turns=75 (по аналогии с technology-agent). type и permissionMode — из /agent-create | Паттерн: technology-agent |
| ~~OQ-14~~ | **РЕШЁН** | Ревьюер возвращает REVISE-таблицу как текст → оркестратор передаёт в prompt при перезапуске агента | Wave 3 feedback через prompt |
| ~~OQ-15~~ | **РЕШЁН** | system-agent ИСПОЛЬЗУЕТ существующие modify-*.md workflows. mode=sync → modify-overview.md. mode=done → все четыре | Не дублировать логику |
| ~~OQ-16~~ | **РЕШЁН** | Агенты вызывают validate-docs-*.py. mode=sync → validate-docs-overview.py. mode=done → все четыре | Существующие скрипты |
| ~~OQ-17~~ | **РЕШЁН** | SVC-N §§ 1-8 → 8 секций {svc}.md. § 9 (Решения) — Design-only, не переносится | Исправлено в маппинге |
| ~~OQ-18~~ | **РЕШЁН** | technology-agent вызывается через `/technology-create` (Skill tool из оркестратора). service-agent/system-agent вызываются через Task tool (не Skill) | Разные механизмы для разных агентов |
| ~~OQ-19~~ | **РЕШЁН (D-12)** | Мягкая блокировка: Discussion создаётся и принимается свободно. При **Design → WAITING** скрипт `check_pending_docs_sync()` проверяет: есть ли цепочка M < N с Design+ WAITING без `docs-synced: true`. Маркер `docs-synced: true` в design.md | Discussion не читает specs/docs/. Design читает (Unified Scan). Блокировка на Design → WAITING не даёт проектировать с устаревшими данными |

---

## Дополнительные файлы для обновления

> Результат проверки 8 агентами по specs/.instructions/ — с учётом новой позиции

### Скрипты

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `chain_status.py` | AUTO_PROPOSE двухступенчатый: plan-dev WAITING + !docs-synced → "/docs-sync", plan-dev WAITING + docs-synced:true → "/dev-create". SIDE_EFFECTS: убрать артефакты из Design WAITING. **Новая функция `check_pending_docs_sync()`** — вызывается при T1 (**Design → WAITING**), проверяет: есть ли цепочка M < N с Design+ WAITING без `docs-synced: true` в design.md | CRITICAL |
| `analysis-status.py` | DOCS_DISPLAY — может потребовать новую строку для /docs-sync | MEDIUM |

### Стандарты analysis/

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `standard-analysis.md` | § 7.1 артефакты при Design WAITING → убрать/перенести на /docs-sync. Полная цепочка (с Dev) → добавить /docs-sync. Аналитическая цепочка (4 документа) — БЕЗ ИЗМЕНЕНИЙ | CRITICAL |

### Инструкции analysis/ — УПРОЩЕНИЕ

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| **plan-test/*** | **НЕТ ИЗМЕНЕНИЙ** (Plan Tests сразу после Design) | — |
| `modify-plan-dev.md` | Где упоминается полная цепочка (включая Dev) → добавить /docs-sync после Plan Dev | LOW |
| `modify-discussion.md` | Если полная цепочка → добавить /docs-sync. Если аналитическая — оставить | LOW |

### Инструкции docs/

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `create-technology.md` | Ссылка на create-design.md Шаг 10 (секция "Вызов из Design") → заменить на /docs-sync оркестрацию | HIGH |
| `standard-docs.md` | "LLM обновляет" (§ Жизненный цикл) → уточнить: service-agent, system-agent, technology-agent | MEDIUM |
| `create-service.md` | Добавить: автоматическое создание через /docs-sync (service-agent). § 9 Planned Changes: обязательный chain-маркер `<!-- chain: NNNN-{topic} -->` ... `<!-- /chain: NNNN-{topic} -->` | MEDIUM |
| `modify-service.md` | Сценарий 6: шаблон Planned Changes → обернуть в chain-маркер `<!-- chain: NNNN-{topic} -->` ... `<!-- /chain: NNNN-{topic} -->`. Сценарии 5-6: Planned Changes генерируются service-agent | MEDIUM |

### Корневые файлы

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `CLAUDE.md` | "6 фаз процесса" → добавить /docs-sync между аналитикой и Dev | HIGH |
| `specs/.instructions/README.md` | Добавить create-docs-sync.md в дерево и таблицу | MEDIUM |
| `create-chain.md` TASK 2 | TASK 2 Design описание: "При WAITING: Planned Changes, заглушки, per-tech" → удалить | HIGH |
| `standard-process.md` § 5 "При Design → WAITING" | "При Design → WAITING: Planned Changes..." → перенести на /docs-sync | HIGH |

### Файлы chain-done и rollback (НОВОЕ)

| Файл | Что менять | Приоритет |
|------|-----------|-----------|
| `create-chain-done.md` | Шаг 3: .system/ обновление → system-agent mode=done + system-reviewer mode=done. Новый Шаг 3.5. Шаг 4 (testing.md): убрать — покрыт mode=done | HIGH |
| `create-rollback.md` | Шаг 4: артефакт #2 — inline rollback overview.md по Design SVC-N. Артефакт #7 — сброс `docs-synced` | MEDIUM |

### Файлы БЕЗ изменений (подтверждено)

| Файл | Почему не меняется |
|------|-------------------|
| **Все plan-test/ файлы** | **Plan Tests после Design — позиция не изменилась** |
| `validation-discussion.md` | Чисто валидационные правила |
| Все `validate-docs-*.py` | Валидация контента, не chain workflow |
| Все `validate-analysis-*.py` | Проверяют parent-child, не chain sequence |
| `create-review.md`, `standard-review.md`, `validation-review.md` | Ревью 4 финальных документов |
| Все plan-dev/ (кроме modify) | Plan Dev перед /docs-sync, не затронут |

---

## Точные правки

> Конкретный контент для 4 файлов с модификациями, где высокоуровневое описание недостаточно.

### П-1: create-chain.md — новая Task 5

**Файл:** `specs/.instructions/create-chain.md`

**Заголовок секции:** Изменить `### Путь A: Happy Path (12 задач)` → `### Путь A: Happy Path (13 задач)`

**TASK 2 description:** Удалить строку:
```
При WAITING: Planned Changes в docs/, заглушки новых сервисов, per-tech стандарты.
```

**Новая задача (вставить между TASK 4 и текущим TASK 5):**
```
TASK 5: Синхронизация docs/
  description: >
    Скилл: /docs-sync — синхронизация specs/docs/ с Design.
    Три волны параллельных агентов:
    Волна 1: service-agent × N (per-service docs) + technology-agent × M (per-tech) +
      system-agent mode=sync (overview.md).
    Волна 2: service-reviewer × N + technology-reviewer × 1 + system-reviewer mode=sync.
    Волна 3: перезапуск при REVISE (макс. 3 итерации).
    Маркер: docs-synced: true в design.md.
    SSOT: create-docs-sync.md
  activeForm: Синхронизирую docs/
  blockedBy: [4]
```

**Сдвиг нумерации:** Текущие TASK 5-12 → TASK 6-13. blockedBy обновить:
- TASK 6 (бывший 5, dev-create): blockedBy: [5] (вместо [4])
- TASK 7-13: blockedBy сдвигается на +1

**Секция "Динамическое поведение":** `Task 12 (Релиз)` → `Task 13 (Релиз)`

**Секция "Оптимизация создания":** `12 TaskCreate` → `13 TaskCreate`, `11 TaskUpdate` → `12 TaskUpdate`

**Quick Reference / Примеры:** `12 задач` → `13 задач`

**TASK 12 (бывший 11, Завершить цепочку) description:** Заменить:
```
    Агент: chain-done-agent (RUNNING → REVIEW → DONE, обновление docs/).
```
На:
```
    Скилл: /chain-done — RUNNING → REVIEW → DONE, обновление docs/.
    Main LLM выполняет create-chain-done.md: T7 каскад, {svc}.md → AS IS,
    system-agent mode=done (Task tool), cross-chain, отчёт.
    SSOT: create-chain-done.md
```

---

### П-2: standard-process.md — новый шаг /docs-sync

**Файл:** `specs/.instructions/standard-process.md`

#### П-2.1: Mermaid-диаграмма (§ 1)

Между `PDEV` и `DEVSTART` добавить блок и стрелку:

```mermaid
    DOCSYNC["1.5 /docs-sync<br/>specs/docs/ sync"]
```

Стрелки: заменить `PDEV --> DEVSTART` на:
```mermaid
    PDEV --> DOCSYNC --> DEVSTART
```

#### П-2.2: § 5 Фаза 1 — "При Design → WAITING"

**Было:**
```
**При Design → WAITING:** Planned Changes добавляются в specs/docs/, заглушки {svc}.md для новых сервисов, per-tech стандарты (с ревью technology-reviewer). → [standard-analysis.md § 7.1](./analysis/standard-analysis.md#71-обновление-при-планировании-to-waiting)
```

**Стало:**
```
**После аналитической цепочки:** /docs-sync синхронизирует specs/docs/ с Design — per-service docs (service-agent), per-tech стандарты (technology-agent), overview.md (system-agent mode=sync). Остальные .system/ файлы обновляются при DONE (system-agent mode=done). → [create-docs-sync.md](./create-docs-sync.md)
```

#### П-2.3: Новый шаг между Фазой 1 и Фазой 2 (§ 5)

Вставить после таблицы Фазы 1 (после строки "/review-create — автоматически"):

```markdown
### Фаза 1.5: Синхронизация docs/

> После одобрения всех 4 документов — синхронизация specs/docs/ с Design через агентов.

| # | Шаг | Описание | Скилл | SSOT |
|---|------|---------|-------|------|
| 1.5 | /docs-sync | service-agent (per-service), technology-agent (per-tech), system-agent mode=sync (overview.md). Три волны: create → review → fix | `/docs-sync` | [create-docs-sync.md](./create-docs-sync.md) |

**Агенты:** service-agent + service-reviewer (per-service), technology-agent + technology-reviewer (per-tech), system-agent + system-reviewer mode=sync (overview.md)

**При DONE (Фаза 5):** system-agent mode=done обновляет все 4 файла .system/ из реального кода.
```

#### П-2.4: Таблица § 8.1 — новая строка

Вставить между строкой "1.4 Plan Dev" и строкой "**Фаза 2: Запуск**":

```markdown
| **Фаза 1.5: Docs Sync** | | | | |
| 1.5 /docs-sync | create-docs-sync | /docs-sync | service-agent, service-reviewer, system-agent (sync), system-reviewer (sync) | — |
```

Строку "5.3 → DONE" обновить — добавить system-agent (done):
```markdown
| 5.3 → DONE | standard-analysis § 6.6, § 7.3, create-chain-done | /analysis-status, **/chain-done** | **system-agent (done), system-reviewer (done)** | chain_status.py |
```

#### П-2.5: Quick Reference (§ 9)

**Было:**
```
Фаза 1 — Аналитическая цепочка:
  ...
  /plan-dev-create      → plan-dev.md (DRAFT → WAITING) + review.md (авто)

Фаза 2 — Запуск реализации:
```

**Стало:**
```
Фаза 1 — Аналитическая цепочка:
  ...
  /plan-dev-create      → plan-dev.md (DRAFT → WAITING) + review.md (авто)

Фаза 1.5 — Docs Sync:
  /docs-sync {path}     → service/tech/system agents, overview.md sync, docs-synced marker

Фаза 2 — Запуск реализации:
```

**Счётчик:** `/chain → TaskList (Happy Path, 12 задач)` → `13 задач`

#### П-2.6: § 5 Фаза 1 — "Агенты"

**Было:**
```
**Агенты:** design-agent-first + design-agent-second (обяз. при Design, последовательно; WAITING один раз — после обоих + обработки PROP), discussion-reviewer (опц.), design-reviewer (опц.), technology-reviewer (опц., при per-tech)
```

**Стало:**
```
**Агенты:** design-agent-first + design-agent-second (обяз. при Design, последовательно; WAITING один раз — после обоих + обработки PROP), discussion-reviewer (опц.), design-reviewer (опц.), technology-reviewer (опц., при per-tech), **service-agent + service-reviewer (при /docs-sync), system-agent + system-reviewer (sync при /docs-sync, done при DONE)**
```

---

### П-3: standard-analysis.md — перенос артефактов на /docs-sync

**Файл:** `specs/.instructions/analysis/standard-analysis.md`

#### П-3.1: § 4.1 Прямой поток

**Было:**
```
2. Design: DRAFT → [Unified Scan + итерации] → WAITING. **При переходе в WAITING** (одновременно): Planned Changes добавляются в specs/docs/ ([§ 7.1](#71-обновление-при-планировании-to-waiting)), заглушки `{svc}.md` создаются для новых сервисов
```

**Стало:**
```
2. Design: DRAFT → [Unified Scan + итерации] → WAITING
```

Добавить после пункта 4 (Plan Dev):
```
5. **Docs Sync:** `/docs-sync` — агенты синхронизируют specs/docs/ с Design ([§ 7.1](#71-обновление-при-планировании-to-waiting)): per-service docs (service-agent), per-tech стандарты (technology-agent), overview.md (system-agent mode=sync). Маркер `docs-synced: true` в design.md
```

#### П-3.2: Матрица обновлений (§ 7)

**Было:**
```
| `specs/docs/.system/overview.md` | R+W | W | DEL |
| `specs/docs/.system/conventions.md` | W? | W? | DEL? |
| `specs/docs/.system/infrastructure.md` | W? | W? | DEL? |
| `specs/docs/.system/testing.md` | — | W? | — |
```

**Стало:**
```
| `specs/docs/.system/overview.md` | R+W (sync) | W (done) | DEL |
| `specs/docs/.system/conventions.md` | — | W? (done) | DEL? |
| `specs/docs/.system/infrastructure.md` | — | W? (done) | DEL? |
| `specs/docs/.system/testing.md` | — | W? (done) | — |
```

Колонка "При WAITING" переименовать → "При /docs-sync".

#### П-3.3: § 7.1 Обновление при планировании

**Было (заголовок + вводная):**
```
### 7.1 Обновление при планировании (to WAITING)

**Заглушка** — минимальный `{svc}.md` ...

При переходе Design в WAITING создаются **Planned Changes** — ...
```

**Стало:**
```
### 7.1 Обновление при планировании (/docs-sync)

> Обновление specs/docs/ выполняется отдельным шагом `/docs-sync` (после Plan Dev, перед Dev), а не при переходе Design → WAITING. Агенты работают параллельно. Маркер завершения: `docs-synced: true` в frontmatter design.md.

**Заглушка** — минимальный `{svc}.md` ...

При запуске `/docs-sync` создаются **Planned Changes** — ...
```

**Таблица "Design → WAITING":** Переименовать заголовок → "Design → /docs-sync". Строки overview.md, conventions.md, infrastructure.md:

**Было:**
```
| Архитектурные изменения | `.system/overview.md` § 8 | Добавить Planned Changes | ... |
| Новые конвенции | `.system/conventions.md` | Добавить записи | ... |
| Инфраструктурные изменения | `.system/infrastructure.md` | Добавить записи | ... |
```

**Стало:**
```
| Архитектурные изменения | `.system/overview.md` | Обновить inline (system-agent mode=sync) | [standard-overview.md](...) |
```

Строки conventions.md и infrastructure.md — **удалить** (обновляются при DONE, не при /docs-sync).

#### П-3.4: § 7.3 Design → DONE

**Было:**
```
| `.system/overview.md` | Planned Changes → AS IS + Changelog |
| `.system/infrastructure.md` | Planned Changes → AS IS + Changelog (если были) |
| `.system/conventions.md` | Planned Changes → AS IS + Changelog (если были) |
```

**Стало:**
```
| `.system/overview.md` | Финализация из реального кода (system-agent mode=done) |
| `.system/conventions.md` | Обновить из Design + реального кода (system-agent mode=done) |
| `.system/infrastructure.md` | Обновить из реального кода (system-agent mode=done) |
```

#### П-3.5: § 7.4 Параллельные цепочки

Добавить после текущего текста:

```
**Cross-chain guard (D-12):** При переходе **Design → WAITING** скрипт `check_pending_docs_sync()` проверяет: есть ли цепочка M < N с Design+ в WAITING, но без `docs-synced: true` в design.md? Если да — отказ в переходе с сообщением "Завершите /docs-sync для цепочки {M}". Discussion создаётся и принимается свободно (не читает specs/docs/), блокировка только при Design → WAITING.
```

#### П-3.6: § 6.8 Откат артефактов

**Было:**
```
| **Design** | Откат изменений в specs/docs/: удаление Planned Changes из `{svc}.md` § 9, `overview.md` § 8. Удаление заглушек новых сервисов (если уникальны). Удаление per-tech стандартов + rule + строки реестра (если технология введена этим Design). Удаление меток `svc:{svc}` (если сервис создан этим Design) |
```

**Стало:**
```
| **Design** | Откат изменений в specs/docs/: удаление Planned Changes из `{svc}.md` § 9, откат inline-правок в `overview.md`. Удаление заглушек новых сервисов (если уникальны). Удаление per-tech стандартов + rule + строки реестра (если технология введена этим Design). Удаление меток `svc:{svc}` (если сервис создан этим Design). Сброс `docs-synced: true` в design.md |
```

---

### П-3.7: create-rollback.md — артефакты overview.md и docs-synced

**Файл:** `specs/.instructions/create-rollback.md`

**Артефакт #1 — обновить описание действия:**

**Было:**
```
| 1 | Planned Changes в `{svc}.md` § 9 | Удалить блок `<!-- chain: {NNNN}-{topic} -->` | Нет маркера → skip |
```

**Стало:**
```
| 1 | Planned Changes в `{svc}.md` § 9 | Удалить всё между `<!-- chain: {NNNN}-{topic} -->` и `<!-- /chain: {NNNN}-{topic} -->` (включая оба тега) | Нет маркера → skip |
```

**Артефакт #2 — заменить:**

**Было:**
```
| 2 | Planned Changes в `overview.md` | Удалить блок `<!-- chain: {NNNN}-{topic} -->` | Нет маркера → skip |
```

**Стало:**
```
| 2 | Inline-правки в `overview.md` | Если `docs-synced: true` в design.md: прочитать Design SVC-N, определить добавленные/изменённые записи (карта сервисов, связи, потоки, домены), удалить их из overview.md | docs-synced отсутствует → skip (overview.md не обновлялся) |
```

**Артефакт #7 — добавить после строки #6:**
```
| 7 | `docs-synced` в design.md | Удалить поле `docs-synced` из frontmatter design.md | Поле отсутствует → skip |
```

---

### П-4: create-chain-done.md — новый Шаг 3.5

**Файл:** `specs/.instructions/create-chain-done.md`

#### П-4.1: Шаг 3 — убрать .system/ из таблицы

**Было:**
```
| `.system/overview.md` | Planned Changes → AS IS + Changelog (если затронута архитектура) |
| `.system/conventions.md` | Planned Changes → AS IS + Changelog (если затронуты конвенции) |
| `.system/infrastructure.md` | Planned Changes → AS IS + Changelog (если затронута инфраструктура) |
```

**Стало:** Удалить эти 3 строки. Вместо них добавить примечание:
```
> **Обновление .system/ файлов** (overview, conventions, infrastructure, testing) — см. Шаг 3.5 (system-agent mode=done).
```

**Дополнительно:** Строку `{svc}.md` § 9 Planned Changes обновить — удаление chain-блока должно захватывать всё между открывающим `<!-- chain: {NNNN}-{topic} -->` и закрывающим `<!-- /chain: {NNNN}-{topic} -->` тегами (включая оба тега).

#### П-4.2: Новый Шаг 3.5 (вставить между Шагом 3 и Шагом 4)

```markdown
### Шаг 3.5: Обновление .system/ (system-agent mode=done)

Полноценное обновление всех 4 файлов specs/docs/.system/ из Design + Plan Tests + реального кода.

**Запуск system-agent mode=done:**

```bash
# Task tool с subagent_type=system-agent
# Входные данные:
#   design-path: specs/analysis/{NNNN}-{topic}/design.md
#   plan-test-path: specs/analysis/{NNNN}-{topic}/plan-test.md
#   src-path: src/
#   mode: done
```

| Файл .system/ | Источники данных | Действие |
|------|--------|----------|
| `overview.md` | Design SVC-N, INT-N + реальный код | Финализация: подтвердить/уточнить данные из /docs-sync (mode=sync) |
| `conventions.md` | Design + реальные паттерны из кода | Обновить API конвенции, форматы ответов/ошибок |
| `infrastructure.md` | Реальный код: docker-compose.yml, .env.example | Обновить Docker Compose, переменные окружения, порты |
| `testing.md` | Plan Tests TC-N + реальные тест-файлы | Обновить стратегию, системные сценарии, покрытие |

**Запуск system-reviewer mode=done:**

После system-agent — сверка всех 4 файлов с источниками. Вердикт: ACCEPT / REVISE.

При REVISE: перезапуск system-agent mode=done с REVISE-таблицей в prompt. Макс. 3 итерации, потом — в отчёт как warning.

**При ошибке:** записать ошибку, продолжить с Шагом 4. Отразить в отчёте.
```

#### П-4.3: Шаг 4 — убрать (покрыт Шагом 3.5)

**Было:**
```
### Шаг 4: Обновление testing.md (Plan Tests DONE)

| Файл docs/ | Действие |
|-----------|----------|
| `.system/testing.md` | Обновить стратегию тестирования (если Plan Tests вносил изменения). Обычно no-op |
```

**Стало:** Удалить Шаг 4 полностью. Перенумеровать: Шаг 5 → Шаг 4, Шаг 6 → Шаг 5.

#### П-4.4: Оглавление — обновить

```
- [Шаг 3: Обновление docs/ (Design DONE)](#шаг-3-обновление-docs-design-done)
- [Шаг 3.5: Обновление .system/ (system-agent mode=done)](#шаг-35-обновление-system-system-agent-modedone)
- [Шаг 4: Cross-chain проверка](#шаг-4-cross-chain-проверка)
- [Шаг 5: Отчёт](#шаг-5-отчёт)
```

#### П-4.5: Чек-лист — обновить

Заменить:
```
- [ ] overview.md обновлён (если затронут)
- [ ] conventions.md обновлён (если затронут)
- [ ] infrastructure.md обновлён (если затронут)
- [ ] testing.md обновлён (если затронут)
```

На:
```
- [ ] system-agent mode=done запущен (все 4 .system/ файла)
- [ ] system-reviewer mode=done: ACCEPT (или warnings в отчёте)
```

---

## Tasklist

TASK 1: Создать service-agent
  description: >
    Драфт: секция "2.1".
    Создать `.claude/agents/service-agent/AGENT.md` через `/agent-create`.
    Промпт: create/update specs/docs/{svc}.md на основе Design SVC-N.
    Входные данные: service, design-path, discussion-path, svc-section, mode.
    mode=create → выполняет create-service.md workflow напрямую (D-11).
    mode=update → выполняет modify-service.md workflow напрямую (D-11).
      ВАЖНО: update пишет ТОЛЬКО § 9 Planned Changes. §§ 1-8 НЕ ТРОГАТЬ — обновятся при DONE.
    Агент НЕ вызывает Skill tool — читает SSOT-инструкцию и выполняет шаги.
    Маппинг Design SVC-N §§ 1-8 → {svc}.md §§ 1-8 (строго из Design, ничего не придумывать).
    "Дополнить § 1" = ТОЛЬКО из Discussion REQ-N.
    Delta-формат: ADDED/MODIFIED/DELETED в Planned Changes.
    ОБЯЗАТЕЛЬНО: § 9 Planned Changes оборачивать в chain-маркер `<!-- chain: NNNN-{topic} -->` ... `<!-- /chain: NNNN-{topic} -->`.
    SSOT-зависимости: standard-service.md, create-service.md, modify-service.md, validation-service.md.
    Валидация: validate-docs-service.py.
    Tools: Read, Grep, Glob, Edit, Write, Bash.
    АНТИГАЛЛЮЦИНАЦИИ: ЖЁСТКИЙ запрет на придумывание.
  activeForm: Создание service-agent

TASK 2: Создать service-reviewer
  description: >
    Драфт: секции "2.2" и "5" (Волна 2).
    Создать `.claude/agents/service-reviewer/AGENT.md` через `/agent-create`.
    Промпт: сверка {svc}.md с Design SVC-N — обнаружение MISSING/INVENTED/DISTORTED.
    Один ревьюер на один сервис (параллельный запуск).
    Вердикт: ACCEPT / REVISE (с таблицей расхождений и цитатами из Design).
    Tools: Read, Grep, Glob (только чтение — НЕ модифицирует файлы).
  activeForm: Создание service-reviewer

TASK 3: Создать system-agent (двухфазный)
  description: >
    Драфт: секции "2.3".
    Создать `.claude/agents/system-agent/AGENT.md` через `/agent-create`.
    Двухфазный агент:
    - mode=sync: ТОЛЬКО overview.md из Design (карта сервисов, связи, потоки, домены).
      Вызывается при /docs-sync. Валидация: validate-docs-overview.py.
      SSOT: standard-overview.md + modify-overview.md.
    - mode=done: ВСЕ 4 файла из Design + Plan Tests + реальный код.
      Вызывается при create-chain-done.md (REVIEW → DONE).
      Валидация: все validate-docs-*.py.
      SSOT: standard-*/modify-* для overview/conventions/infrastructure/testing.
    Tools: Read, Grep, Glob, Edit, Write, Bash.
    АНТИГАЛЛЮЦИНАЦИИ: ЖЁСТКИЙ запрет на придумывание. Каждое изменение — источник.
  activeForm: Создание system-agent

TASK 4: Создать system-reviewer (двухфазный)
  description: >
    Драфт: секции "2.4".
    Создать `.claude/agents/system-reviewer/AGENT.md` через `/agent-create`.
    Двухфазный ревьюер:
    - mode=sync: сверка ТОЛЬКО overview.md с Design.
      git diff -- specs/docs/.system/overview.md.
    - mode=done: сверка ВСЕХ 4 файлов с Design + Plan Tests + реальный код.
      git diff -- specs/docs/.system/.
      Проверка согласованности между 4 файлами.
    Вердикт: ACCEPT / REVISE (MISSING/INVENTED/DISTORTED).
    Tools: Read, Grep, Glob (только чтение).
  activeForm: Создание system-reviewer

TASK 5: Создать SSOT-инструкцию create-docs-sync.md
  description: >
    Драфт: секции "3" и "5".
    Создать `specs/.instructions/create-docs-sync.md` — SSOT воркфлоу.
    Вход: все 4 документа в WAITING + путь к design.md.
    Cross-chain guard (OQ-19): проверить pending /docs-sync.
    Шаги: проверка WAITING → определение сервисов/технологий →
    Волна 1 (service-agent × N + technology-agent × M + system-agent mode=sync × 1, параллельно) →
    README.md update (оркестратор, не агенты) →
    Волна 2 (service-reviewer × N + technology-reviewer × 1 + system-reviewer mode=sync × 1, параллельно) →
    Волна 3 (если REVISE — перезапуск только агентов с REVISE, макс. 3 итерации).
    ВАЖНО: system-agent при /docs-sync обновляет ТОЛЬКО overview.md.
    Файл в корне specs/.instructions/ (рядом с create-chain.md).
  activeForm: Создание create-docs-sync.md

TASK 6: Создать скилл /docs-sync
  description: >
    Драфт: секция "5" (оркестрация → скилл /docs-sync).
    Создать `.claude/skills/docs-sync/SKILL.md` через `/skill-create`.
    SSOT: specs/.instructions/create-docs-sync.md.
    Формат: `/docs-sync <design-path>`.
  activeForm: Создание скилла /docs-sync

TASK 7: Обновить create-design.md — вынести артефакты
  description: >
    Драфт: секция "4" (Файлы design/).
    Изменить `specs/.instructions/analysis/design/create-design.md`:
    - Шаг 7: оставить ТОЛЬКО DRAFT → WAITING через chain_status.py
    - Удалить: таблицу артефактов (все строки), Planned Changes, заглушки, per-tech
    - Удалить: шаг 7.5 (ревью per-tech — перенесён в /docs-sync)
    - Обновить отчёт (шаг 8): убрать артефакты
    - Шаг 9 (авто-предложение): НЕ МЕНЯТЬ — Design → Plan Tests (корректно)
    - Обновить чек-лист: убрать пункты артефактов
    Также изменить:
    - `standard-design.md`: § 4 побочные эффекты WAITING, § Связи, § Frontmatter: добавить `docs-synced` (опц., boolean)
    - `validation-design.md`: добавить проверку `docs-synced` (если присутствует — boolean)
    - `modify-design.md`: полная цепочка → добавить /docs-sync (если упоминается)

  activeForm: Обновление design/ инструкций

TASK 8: Обновить create-chain.md — добавить /docs-sync в TaskList
  description: >
    Драфт: секция "4" (Оркестрационные файлы) + "П-1" (Точные правки).
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
    Драфт: "П-2" (Точные правки standard-process.md).
    Изменить `specs/.instructions/standard-process.md`:
    - Добавить шаг "Docs Sync" между Фазой 1 (аналитика) и Фазой 2 (Dev)
    - Таблица инструментов (§ 8.1): добавить строку /docs-sync с агентами
    - Диаграмма обзора: добавить шаг после Plan Dev, перед Dev
    - § 5 "При Design → WAITING: Planned Changes..." → перенести на /docs-sync
    Запустить `/migration-create` после изменения стандарта.
  activeForm: Обновление standard-process.md

TASK 10: Обновить chain_status.py, analysis-status.py и standard-analysis.md
  description: >
    Драфт: "Доп. файлы" (Скрипты + Стандарты analysis/) + "П-3" (Точные правки).
    chain_status.py:
    - AUTO_PROPOSE двухступенчатый (читает docs-synced из design.md frontmatter):
      (a) plan-dev WAITING + !docs-synced → "/docs-sync {chain_id}"
      (b) plan-dev WAITING + docs-synced:true → "/dev-create {chain_id}"
    - SIDE_EFFECTS[("design", "WAITING")]: убрать артефакты
    - Новая функция check_pending_docs_sync(): сканирует цепочки M < N с Design+
      в WAITING без `docs-synced: true` в design.md. Вызывается при T1 (Design → WAITING).
      Если найдены → отказ с сообщением "Завершите /docs-sync для цепочки {M}"
    - _CHAIN_MARKER_PATTERN: обновить regex для поддержки закрывающего тега
      `<!-- /chain: NNNN-{topic} -->`. Используется при DONE-cleanup и rollback
    standard-analysis.md:
    - § 7.1: убрать артефакты из Design WAITING → описать /docs-sync
    - Полная цепочка: добавить /docs-sync
    - Аналитическая цепочка (4 документа): БЕЗ ИЗМЕНЕНИЙ
    analysis-status.py:
    - DOCS_DISPLAY: добавить строку для /docs-sync (если требуется)
  activeForm: Обновление chain_status.py, analysis-status.py и standard-analysis.md

TASK 11: Обновить create-chain-done.md + создать скилл /chain-done + деактивировать chain-done-agent
  description: >
    Драфт: секция "4" (chain-done и rollback) + "П-4" (Точные правки).
    1. Изменить `specs/.instructions/create-chain-done.md`:
       - Шаг 3: оставить {svc}.md (Planned Changes → AS IS) как есть
       - Шаг 3 таблица "Файл docs/": убрать строки .system/ (overview, conventions, infrastructure)
       - Новый Шаг 3.5: запуск system-agent mode=done (все 4 .system/ файла из Design + Plan Tests + реальный код)
         → system-reviewer mode=done → Волна 3 при REVISE (макс. 3 итерации)
       - Шаг 4 (testing.md): убрать — покрывается system-agent mode=done
       - Обновить чек-лист: .system/ обновлён через system-agent mode=done
    2. Создать скилл `/chain-done` через `/skill-create`:
       - SSOT: create-chain-done.md
       - Формат: `/chain-done {NNNN}`
    3. Деактивировать chain-done-agent через `/agent-modify chain-done-agent --deactivate` (D-13)
  activeForm: Обновление chain-done + скилл + деактивация

TASK 12: Обновить остальные файлы (docs/, minor)
  description: >
    Драфт: секция "4" (Доп. файлы) + "П-3.7" (Точные правки create-rollback.md).
    CLAUDE.md и README.md уже обновлены (до реализации драфта).
    - specs/.instructions/README.md: добавить create-docs-sync.md
    - create-technology.md: секция "Вызов из Design" → /docs-sync
    - standard-docs.md: "LLM обновляет" → агенты
    - create-service.md: автоматическое создание через /docs-sync + chain-маркер в § 9 Planned Changes
    - modify-service.md: Сценарий 6 — chain-маркер `<!-- chain: NNNN-{topic} -->` в шаблоне Planned Changes
    - modify-plan-dev.md: полная цепочка → добавить /docs-sync
    - modify-discussion.md: полная цепочка → добавить /docs-sync (если есть)
    - create-rollback.md: Шаг 4 артефакт #1 — обновить cleanup: удалять всё между `<!-- chain: -->` и `<!-- /chain: -->`. Артефакт #2 — inline rollback overview.md по Design SVC-N (если docs-synced:true). Артефакт #7 — сброс `docs-synced` (П-3.7)
  activeForm: Обновление остальных файлов

TASK 13: Валидация и тест
  description: >
    Драфт: весь документ (валидация полноты реализации).
    1. `/draft-validate` на черновик
    2. Валидация всех изменённых файлов (агенты, инструкции, стандарты)
    3. Тест: запустить `/docs-sync` на цепочке 0001-task-dashboard (все 4 документа в WAITING)
    4. Проверить: 3 сервиса (task.md, auth.md, frontend.md) + per-tech стандарты + overview.md обновлены
    5. Проверить: conventions.md, infrastructure.md, testing.md НЕ затронуты (ждут DONE)
    6. Проверить: ревью service + technology + overview пройдено
    7. Тест DONE: запустить `/chain-done` → проверить все 4 .system/ файла обновлены через system-agent mode=done
  activeForm: Валидация и тестирование
