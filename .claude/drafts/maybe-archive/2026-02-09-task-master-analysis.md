# Анализ Claude Task Master: механики управления задачами

Детальное исследование трёх ключевых механизмов Task Master для адаптации в нашем SDD-подходе.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Модель данных задачи](#1-модель-данных-задачи)
  - [2. Анализ сложности](#2-анализ-сложности)
  - [3. Авто-декомпозиция](#3-авто-декомпозиция)
  - [4. Алгоритм find-next-task](#4-алгоритм-find-next-task)
  - [5. Пайплайн: как механизмы связаны](#5-пайплайн-как-механизмы-связаны)
  - [6. Что применимо к нашему SDD](#6-что-применимо-к-нашему-sdd)

---

## Контекст

**Задача:** Изучить механики Task Master (анализ сложности, авто-декомпозиция, find-next-task) для адаптации в `standard-plan.md` нашего SDD-подхода.

**Почему создан:** Открытый вопрос #1 архитектуры specs/: "Task management в Plan — как реализовать?"

**Связанные файлы:**
- [2026-02-08-specs-architecture.md](../examples/2026-02-08-specs-architecture.md) — архитектура specs/
- [2026-02-09-sdd-framework-comparison.md](./2026-02-09-sdd-framework-comparison.md) — сравнение с фреймворками

**Источник:** https://github.com/eyaltoledano/claude-task-master

---

## Содержание

### 1. Модель данных задачи

#### 1.1. Структура задачи

```
Task {
  id: number                    # автоинкремент (1, 2, 3...)
  title: string                 # 1-200 символов
  description: string           # описание
  status: enum                  # pending | in-progress | blocked | done | cancelled | deferred
  dependencies: number[]        # ID задач, от которых зависит
  priority: enum                # low | medium | high | critical
  details: string | null        # детали реализации
  testStrategy: string | null   # стратегия тестирования
  subtasks: Subtask[]           # вложенные подзадачи
}
```

#### 1.2. Структура подзадачи

```
Subtask {
  id: number                    # последовательный внутри родителя (1, 2, 3)
  title: string                 # 5-200 символов
  description: string           # min 10 символов
  dependencies: number[]        # ID сиблингов-подзадач
  details: string               # min 20 символов
  status: enum                  # pending | done
  testStrategy: string | null
}
```

**Адресация:** Точечная нотация — `parentId.subtaskId` (напр. "4.3" = подзадача 3 задачи 4).

#### 1.3. Зависимости

- Задача может зависеть только от задач с **меньшим ID** (enforced при генерации)
- Подзадачи зависят от сиблингов внутри того же родителя
- Циклические зависимости проверяются рекурсивно
- При установке `done` — проверяются зависимые задачи

#### 1.4. Хранение

Всё в одном `tasks.json`, организованном по тегам (параллельные наборы задач):

```json
{
  "master": {
    "tasks": [...],
    "metadata": { "created": "...", "updated": "...", "description": "..." }
  },
  "feature-x": { "tasks": [...], "metadata": {...} }
}
```

#### 1.5. Отличия от нашего SDD

| Аспект | Task Master | Наш SDD (Plan) |
|--------|------------|----------------|
| Формат | JSON | Markdown |
| Иерархия | task → subtask (2 уровня) | Plan → задачи (чек-лист) |
| Зависимости | Числовые ID с валидацией | Ссылки на планы тестов |
| Тест-стратегия | Поле `testStrategy` | Отдельный уровень План тестов |
| Контекст | PRD → задачи (без спецификаций) | Discussion → ... → План тестов → Plan |

---

### 2. Анализ сложности

**Файл:** `analyze-task-complexity.js`

#### 2.1. Алгоритм

```
1. Загрузить задачи из tasks.json
2. Отфильтровать активные (pending, blocked, in-progress)
3. Собрать контекст проекта (FuzzyTaskSearch по файлам)
4. Загрузить существующий отчёт (если есть — для мерджа)
5. Построить промпт с задачами + контекстом
6. Вызвать AI → получить структурированный ответ (Zod-валидация)
7. Заполнить пропущенные задачи дефолтами (score=5, subtasks=3)
8. Смерджить с существующим отчётом
9. Записать в .taskmaster/reports/task-complexity-report.json
```

#### 2.2. Что оценивает AI

Системный промпт:

> You are an expert software architect and project manager analyzing task complexity. Your analysis should consider **implementation effort**, **technical challenges**, **dependencies**, and **testing requirements**.

Для каждой задачи AI возвращает:

| Поле | Тип | Описание |
|------|-----|----------|
| `taskId` | number | ID задачи |
| `taskTitle` | string | Название |
| `complexityScore` | 1-10 | Оценка сложности |
| `recommendedSubtasks` | number | Рекомендованное кол-во подзадач (0 = не нужно) |
| `expansionPrompt` | string | Промпт для генерации подзадач |
| `reasoning` | string | Обоснование оценки |

#### 2.3. Пример выхода

```json
{
  "taskId": 24,
  "taskTitle": "Implement AI-Powered Test Generation",
  "complexityScore": 8,
  "recommendedSubtasks": 6,
  "expansionPrompt": "Expand task 24 into 6 subtasks focusing on: 1) Command structure, 2) AI prompt engineering...",
  "reasoning": "High complexity due to: AI integration, multi-framework support, MCP tool integration..."
}
```

#### 2.4. Классификация

| Диапазон | Уровень |
|----------|---------|
| 8-10 | Высокая сложность |
| 5-7 | Средняя сложность |
| 1-4 | Низкая сложность |

#### 2.5. Ключевой инсайт

**`expansionPrompt`** — самое ценное поле. AI при анализе сложности уже понимает задачу и генерирует **конкретные инструкции** для будущей декомпозиции. Это создаёт цепочку: анализ → экспертное понимание → направленная декомпозиция.

---

### 3. Авто-декомпозиция

Два этапа: парсинг PRD → задачи, затем расширение задач → подзадачи.

#### 3.1. Парсинг PRD (parse-prd)

**Файл:** `parse-prd.js`

**Алгоритм:**

```
1. Загрузить существующие задачи, определить nextId
2. Прочитать PRD-документ
3. Построить промпт (system + user)
4. Вызвать AI → массив задач
5. Постобработка:
   a. Валидация последовательных ID
   b. Ремаппинг ID начиная с nextId
   c. Ремаппинг зависимостей
   d. Фильтр: зависимость только на меньший ID
   e. Дефолты: priority=medium, status=pending
6. Записать в tasks.json
```

**Системный промпт:**

> You are an AI assistant specialized in analyzing PRDs and generating a structured, logically ordered, dependency-aware and sequenced list of development tasks.
>
> Guidelines:
> 1. Create exactly N tasks, numbered sequentially
> 2. Each task atomic, single responsibility
> 3. Order logically — dependencies and implementation sequence
> 4. Early tasks: setup, core; later: advanced features
> 5. Dependencies only reference lower IDs
> 6. Include detailed implementation guidance in "details"
> 7. STRICTLY ADHERE to PRD's specified tech stacks

#### 3.2. Расширение задачи (expand-task)

**Файл:** `expand-task.js`

**Алгоритм:**

```
1. Загрузить задачу по ID
2. Собрать контекст (ContextGatherer + FuzzyTaskSearch)
3. Найти анализ сложности для этой задачи (если есть)
4. Определить кол-во подзадач:
   a. Явный параметр --num (приоритет)
   b. recommendedSubtasks из отчёта сложности
   c. Дефолт из конфига (5)
5. Выбрать вариант промпта:
   a. "complexity-report" — если есть expansionPrompt
   b. "research" — режим исследования
   c. "default" — стандартный
6. Рассчитать nextSubtaskId
7. Вызвать AI → массив подзадач
8. Постобработка: дефолты (dependencies=[], status=pending)
9. ДОПИСАТЬ подзадачи к существующим (не заменить!)
10. Записать в tasks.json
```

**Промпт (default):**

> Break down this task into exactly N specific subtasks:
>
> Task ID: {id}, Title: {title}, Description: {description}, Details: {details}
>
> CRITICAL: Use sequential IDs starting from {nextSubtaskId}

**Промпт (complexity-report):** Использует `expansionPrompt` из отчёта сложности — гораздо более конкретные инструкции.

#### 3.3. Расширение всех задач (expand-all)

```
1. Загрузить все задачи
2. Отфильтровать: status = pending | in-progress, нет подзадач (или --force)
3. Для каждой → expand-task (последовательно)
4. Агрегировать результаты
```

#### 3.4. Scope Adjustment (дополнительный механизм)

Корректировка сложности после создания: scope-up (усложнить) / scope-down (упростить).

```
Уровни: light | regular | heavy

1. Загрузить задачу, текущий complexity score
2. AI переписывает: title, description, details, testStrategy
3. Сохранённые подзадачи: done, in-progress, review, cancelled, deferred, blocked
4. Перегенерированные подзадачи: только pending
5. Новое кол-во подзадач = f(direction, strength, complexity)
```

---

### 4. Алгоритм find-next-task

**Файл:** `find-next-task.js`

**Чисто детерминистический алгоритм — без AI.**

#### 4.1. Алгоритм

```
Фаза 0: Построить множество completedIds
  → Все task.id со status done/completed
  → Все "parentId.subtaskId" со status done/completed

Фаза 1: Поиск среди подзадач (приоритетный путь)
  → Найти родителей со status = in-progress И есть подзадачи
  → Для каждого: найти подзадачи с status = pending | in-progress
  → Проверить: ВСЕ зависимости в completedIds
  → Отсортировать кандидатов:
    1. priority DESC (high=3, medium=2, low=1)
    2. dependencies.length ASC (меньше зависимостей — лучше)
    3. parentId ASC (меньший ID родителя — первый)
    4. subtaskId ASC (меньший ID подзадачи — первый)
  → Если есть кандидаты → вернуть первого

Фаза 2: Fallback на верхнеуровневые задачи
  → Найти задачи с status = pending | in-progress
  → Проверить: ВСЕ зависимости в completedIds
  → Отсортировать:
    1. priority DESC
    2. dependencies.length ASC
    3. id ASC
  → Вернуть первого или null

Фаза 3: Обогатить complexity score (если есть отчёт)
```

#### 4.2. Ключевые решения

1. **Подзадачи приоритетнее задач** — если родитель `in-progress`, его pending подзадачи выбираются первыми. Гранулярная работа завершается до начала новых задач.
2. **Без AI** — чистая сортировка по priority → deps count → ID. Быстро, предсказуемо, детерминированно.
3. **Зависимости блокируют** — задача не может быть выбрана, пока все её зависимости не `done`.

#### 4.3. Вход/Выход

**Вход:** массив задач + опциональный отчёт сложности

**Выход:**
```
{
  id: number | string,      # 5 (задача) или "3.2" (подзадача)
  title: string,
  status: string,
  priority: "high" | "medium" | "low",
  dependencies: array,
  parentId: number,         # только для подзадач
  complexityScore: number   # только если есть отчёт
}
// или null — нет доступной работы
```

---

### 5. Пайплайн: как механизмы связаны

```
PRD-документ
    │
    ▼
┌─────────────┐
│  parse-prd  │  AI генерирует N задач с зависимостями
└──────┬──────┘
       │
       ▼
  tasks.json (верхнеуровневые задачи)
       │
       ▼
┌──────────────────────┐
│  analyze-complexity  │  AI оценивает 1-10, рекомендует подзадачи,
│                      │  генерирует expansionPrompt
└──────────┬───────────┘
           │
           ▼
  complexity-report.json
           │
           ▼
┌──────────────────┐
│  expand-task     │  AI декомпозирует задачу, используя:
│  (или expand-all)│  — кол-во подзадач из отчёта
│                  │  — expansionPrompt из отчёта (конкретные инструкции)
└──────────┬───────┘
           │
           ▼
  tasks.json (задачи + подзадачи)
           │
           ▼
┌──────────────────┐
│  find-next-task  │  Детерминистический выбор:
│  (без AI)        │  priority → deps → ID
└──────────┬───────┘
           │
           ▼
  Следующая задача для работы
```

**Цепочка ценности:** Анализ сложности → `expansionPrompt` → качественная декомпозиция. Без анализа сложности декомпозиция менее точная (generic промпт vs конкретные инструкции).

---

### 6. Что применимо к нашему SDD

#### 6.1. Что берём

| Механизм | Как адаптируем | Где в нашем SDD |
|----------|---------------|-----------------|
| **Анализ сложности** | LLM оценивает задачи из Plan (1-10) в одном проходе с генерацией | Поле задачи в Plan |
| **expansionPrompt** | LLM при генерации Plan сразу пишет инструкции для декомпозиции | Поле задачи в Plan |
| **Порядок выполнения** | Задачи в Plan упорядочены — агент-кодер идёт сверху вниз | Порядок задач в Plan |
| **testStrategy на задаче** | Ссылки на конкретные сценарии из План тестов | Поле задачи в Plan |
| **Зависимости < ID** | Задача зависит только от задач с меньшим номером | Правило в Plan |
| **scope-adjustment** | Покрыт CONFLICT-механизмом: pending подзадачи перегенерируются, done сохраняются | CONFLICT-разрешение на уровне Plan |

#### 6.2. Что НЕ берём

| Механизм | Почему | Наша альтернатива |
|----------|--------|-------------------|
| JSON-формат | Markdown читаемее, git diff понятнее | Чек-листы в Markdown |
| Теги (параллельные наборы) | У нас каждый Plan привязан к сервису через цепочку | Иерархия specs/ |
| PRD-парсинг | У нас 5 уровней спецификаций до Plan | Discussion → ... → План тестов |
| 2-уровневая иерархия (task → subtask) | Достаточно для Plan | Задачи + подзадачи в чек-листе |

#### 6.3. Как это выглядит в нашем Plan

**Связь с существующей инфраструктурой Issues:**

У нас уже есть полный комплект инструкций для GitHub Issues: [.github/.instructions/issues/](/.github/.instructions/issues/). Ключевые моменты интеграции:

| Наша инфраструктура | Как связана с Plan |
|---------------------|-------------------|
| `standard-issue.md` § 8 — декомпозиция | Parent Issue = Plan, sub-issues = задачи из Plan |
| `standard-issue.md` § 8 — зависимости | `**Зависит от:** #N` в body Issue = deps в Plan |
| `create-issue.md` — batch-создание | LLM создаёт все Issues из Plan за один вызов |
| `standard-issue.md` § 9 — milestones | Milestone определён на уровне Discussion (решение #44) |
| Labels: type + priority | type из контекста задачи, priority из поля приоритета Plan |
| `standard-issue-template.md` — шаблоны | Каждый Issue создаётся по соответствующему шаблону (task, bug-report, refactor, docs) |

**Маппинг Plan → GitHub Issues:**

```
Plan (specs/services/auth/plan-dev/jwt-migration-plan.md)
    │
    ├── Задача 1 → Issue #201 "Создать модуль auth.tokens"
    │     ├── Подзадача 1.1 → чек-лист в body Issue #201
    │     ├── Подзадача 1.2 → чек-лист в body Issue #201
    │     └── ...
    │
    ├── Задача 2 → Issue #202 "Создать middleware JWT-валидации"
    │     └── **Зависит от:** #201
    │
    └── Задача 3 → Issue #203 "Настроить ротацию ключей"
          └── **Зависит от:** #201, #202
```

**Правило:** Задача → отдельный Issue, подзадачи → чек-лист в body (если не требуют отдельных PR). Если подзадача требует отдельного PR → sub-issue.

**Пример задачи в Plan (структурированный блок):**

```markdown
## Задачи

### Задача 1: Создать модуль auth.tokens
- **Сложность:** 7/10
- **Приоритет:** high
- **Зависимости:** —
- **План тестов:** [001-oauth2-tests.md#token-generation](...)
- **Дельта:** ADDED auth.tokens (из ADR)

Подзадачи:
- [ ] 1.1. Интерфейс TokenGenerator
- [ ] 1.2. JWT-реализация с ES256 (deps: 1.1)
- [ ] 1.3. Refresh-token хранение в Redis (deps: 1.1)
- [ ] 1.4. TTL-конфигурация (deps: 1.2, 1.3)
- [ ] 1.5. Unit-тесты TokenGenerator (deps: 1.2, 1.3, 1.4)

### Задача 2: Middleware JWT-валидации
- **Сложность:** 5/10
- **Приоритет:** high
- **Зависимости:** Задача 1
- **План тестов:** [001-oauth2-tests.md#middleware-validation](...)
- **Дельта:** MODIFIED auth.middleware (из ADR)

Подзадачи:
- [ ] 2.1. Заменить session_middleware на jwt_middleware
- [ ] 2.2. Интеграционные тесты (deps: 2.1)
```

**Порядок задач = порядок выполнения.** Агент-кодер получает ссылку на Plan и идёт сверху вниз, проверяя зависимости.

#### 6.4. Решённые вопросы

| # | Вопрос | Решение |
|---|--------|---------|
| 1 | Формат задач в Plan | **Структурированные блоки.** Каждая задача = заголовок + метаданные (сложность, приоритет, зависимости, план тестов, дельта) + чек-лист подзадач |
| 2 | Где хранить complexity report | **В самом Plan.** Сложность — поле задачи (7/10). Отдельный файл не нужен: LLM уже имеет полный контекст из 5 уровней спецификаций |
| 3 | Нужен ли отдельный шаг analyze-complexity | **Нет.** LLM оценивает сложность при генерации Plan в одном проходе. В Task Master отдельный шаг нужен потому, что PRD → задачи идёт без контекста. У нас контекст есть (Discussion → ... → План тестов) |
| 4 | Как scope-adjustment работает с CONFLICT | **Покрыт CONFLICT-механизмом.** При обратной связи Code → Specs, если Plan → CONFLICT, фаза 2 (разрешение ↓) переписывает pending подзадачи. Done подзадачи сохраняются как факт выполненной работы. Отдельный scope-adjustment не нужен |
| 5 | find-next-task: внутри одного Plan или кросс-Plans | **Порядок внутри одного Plan.** Агент-кодер получает ссылку на конкретный Plan и идёт сверху вниз по задачам, проверяя зависимости. Кросс-Plans координация — через порядок Issues в Milestone |
