---
description: Стандарт Plan Tests SDD — per-service acceptance-сценарии (TC-N), тестовые данные, системные тест-сценарии, матрица покрытия REQ-N/STS-N → TC-N, шаблон, чек-лист.
standard: .instructions/standard-instruction.md
standard-version: v1.4
index: specs/.instructions/README.md
---

# Стандарт плана тестов

Версия стандарта: 1.4

Формат и правила оформления документов плана тестов (`specs/analysis/NNNN-{topic}/plan-test.md`). План тестов — третий уровень SDD-иерархии: структурированный документ для определения acceptance-сценариев (TC-N), тестовых данных и матрицы покрытия требований тестами.

**Полезные ссылки:**
- [Стандарт аналитического контура](../standard-analysis.md) — статусы, каскады, воркфлоу, общий паттерн объекта
- [Инструкции specs/](../../README.md)

**SSOT-зависимости:**
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) — стратегия тестирования (§ read/write testing.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-plan-test.md](./validation-plan-test.md) |
| Создание | [create-plan-test.md](./create-plan-test.md) |
| Модификация | [modify-plan-test.md](./modify-plan-test.md) |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Расположение и именование](#2-расположение-и-именование)
- [3. Frontmatter](#3-frontmatter)
- [4. Переходы статусов](#4-переходы-статусов)
- [5. Разделы документа](#5-разделы-документа)
  - [Резюме](#резюме)
  - [SVC-N: {сервис} — per-service разделы](#svc-n-сервис-per-service-разделы)
  - [Системные тест-сценарии](#системные-тест-сценарии)
  - [Матрица покрытия](#матрица-покрытия)
  - [Блоки тестирования](#блоки-тестирования)
  - [Предложения](#предложения)
  - [Отвергнутые предложения](#отвергнутые-предложения)
- [6. Clarify](#6-clarify)
- [7. Шаблон](#7-шаблон)
- [8. Чек-лист качества](#8-чек-лист-качества)
- [9. Примеры по типам](#9-примеры-по-типам)

---

## 1. Назначение

**Зона ответственности:** HOW TO VERIFY ([Стандарт analysis/ § 2.2](../standard-analysis.md#22-таблица-объектов)).

Plan Tests отвечает на вопрос: **Как проверяем решение?**

**Содержит:**
- Per-service разделы: acceptance-сценарии (TC-N), тестовые данные
- Системные тест-сценарии (покрытие STS-N из Design)
- Матрица покрытия (трассируемость REQ-N/STS-N → TC-N)

**НЕ содержит:**
- Бизнес-обоснование и требования (→ Discussion)
- Распределение ответственностей, контракты API (→ Design)
- Реализацию тестов — конкретный код, фреймворки (→ Plan Dev / разработка)
- Задачи на реализацию (→ Plan Dev)

**Граничные случаи (Plan Tests vs Design / Plan Dev):**
- Допустимо: "Пользователь с валидными credentials отправляет POST /auth/token — ответ 200" — acceptance-сценарий
- Допустимо: "Fixture: user_valid_credentials = {username, password}" — тестовые данные
- Допустимо: "Покрытие STS-1: полный цикл логин → токен → запрос → успех" — системный сценарий
- Недопустимо: "Использовать pytest + httpx для тестирования" — выбор инструментов (→ Plan Dev)
- Недопустимо: "Задача: написать тест для POST /auth/token" — задача (→ Plan Dev)
- Недопустимо: "auth-сервис отвечает за генерацию JWT" — распределение ответственностей (→ Design)

**Когда создавать:**
- После одобрения Design (статус WAITING)
- Всегда один Plan Tests на один Design (1:1)

**Связи:** Parent — Design (обязателен, 1:1). Дочерний объект — Plan Dev (1:1). ([Стандарт analysis/ § 3.1](../standard-analysis.md#31-frontmatter-и-навигация))

**Входные данные (фильтрация Design → Plan Tests):** ([Стандарт analysis/ § 3.3](../standard-analysis.md#33-фильтрация-design-plan-tests))

Для каждого per-service раздела Plan Tests читает:

| # | Источник | Что читается | Назначение |
|---|----------|-------------|------------|
| 1 | **SVC-N секция** из Design | Ответственность, компоненты, решения по реализации (§ 9) | Понять scope сервиса для тестов |
| 2 | **INT-N блоки** из Design | Контракты, где участвует сервис | Интеграционные тесты |
| 3 | **STS-N** из Design | Системные тест-сценарии | E2e тесты |
| 4 | **REQ-N** из Discussion | Требования — acceptance criteria | Маппинг требований в тесты |
| 5 | **`specs/docs/{svc}.md`** | Текущее AS IS | Регрессионные тесты |
| 6 | **`specs/docs/.system/testing.md`** | Стратегия тестирования — применять как дефолтную стратегию мокирования и типов тестов (**SSOT:** [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md)) | При отклонении от стратегии — зафиксировать в Резюме |

**Блокирующее условие:** Plan Tests создаётся **только** после того, как Design перешёл в статус WAITING. LLM **обязан** проверить `status` в frontmatter Design перед началом работы. Если Design в DRAFT — Plan Tests не создаётся.

**Discussion без REQ-N:** Если Discussion не содержит пронумерованных REQ-N (секция "Требования" — заглушка) — при создании Plan Tests поставить маркер `[ТРЕБУЕТ УТОЧНЕНИЯ: Discussion не содержит REQ-N — невозможно построить матрицу покрытия]` и инициировать upward feedback.

**После DONE:** Plan Tests становится архивной записью тестовых решений. Допустимо исправлять только орфографические ошибки, не изменяющие смысл описания, тип, источник или данные ни одного TC-N. Любое изменение смысла TC-N — включая добавление, удаление или переформулировку — требует перехода через CONFLICT-цикл ([§ 6.3](../standard-analysis.md#63-running-to-conflict)).

**Выходные данные Plan Tests → Plan Dev:** все TC-N таблиц acceptance-сценариев и системных тест-сценариев, тестовые данные (fixtures). Plan Dev формирует задачи реализации тестов на основе TC-N. Детали — в [standard-plan-dev.md](../plan-dev/standard-plan-dev.md).

**Побочные эффекты Plan Tests → DONE:** обновить `specs/docs/.system/testing.md` если стратегия тестирования изменилась (новые типы тестов, изменение подхода к мокированию). **SSOT:** [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md).

---

## 2. Расположение и именование

**Расположение:** `specs/analysis/NNNN-{topic}/plan-test.md`

**Имя файла:** `plan-test.md` (фиксированное)

NNNN и topic определяются папкой цепочки. Все документы цепочки (Discussion, Design, Plan Tests, Plan Dev) расположены в одной папке `specs/analysis/NNNN-{topic}/`.

**Заголовок документа:** `# NNNN: {Тема} — Plan Tests`

**Формат `{Тема}`:** совпадает с темой Discussion из той же цепочки. Свободный текст, язык проекта (русский), первое слово с заглавной буквы, без точки, до 80 символов. Пример: `# 0001: OAuth2 авторизация — Plan Tests`.

---

## 3. Frontmatter

**SSOT frontmatter:** [standard-frontmatter.md](/.structure/.instructions/standard-frontmatter.md) ([§ 1 — базовые поля](/.structure/.instructions/standard-frontmatter.md#1-обязательные-поля) + [§ 4 — поля specs](/.structure/.instructions/standard-frontmatter.md#4-дополнительные-поля-для-спецификаций-specs))

| Поле | Значение для Plan Tests | Обязательность |
|------|------------------------|----------------|
| `description` | Описание плана тестов (до 1024 символов) | Обязательно |
| `standard` | `specs/.instructions/analysis/plan-test/standard-plan-test.md` | Обязательно |
| `standard-version` | `v1.3` | Обязательно |
| `index` | `specs/analysis/README.md` | Обязательно |
| `parent` | Путь к Design-документу (обязателен) | Обязательно |
| `children` | Путь к Plan Dev документу (1:1) | Обязательно (присутствие поля; `children: []` до создания Plan Dev, `[plan-dev.md]` — после) |
| `status` | Текущий статус ([Стандарт analysis/ § 5](../standard-analysis.md#5-статусы)) | Обязательно |
| `milestone` | Наследуется от parent Discussion | Обязательно |

```yaml
---
description: Plan Tests OAuth2 авторизации — 12 acceptance-сценариев для auth/gateway/users, 3 системных e2e, матрица покрытия REQ-1..REQ-5.
standard: specs/.instructions/analysis/plan-test/standard-plan-test.md
standard-version: v1.4
index: specs/analysis/README.md
parent: design.md
children:
  - plan-dev.md
status: DRAFT
milestone: v1.2.0
---
```

**Parent (обязателен):** Путь к Design-документу в той же папке цепочки. Plan Tests всегда имеет parent — Design (1:1). Без parent документ невалиден.

**Children (1:1):** Plan Dev создаётся после Plan Tests. Один Plan Tests порождает один Plan Dev.

**Milestone:** Наследуется от parent Discussion (через Design). Значение milestone в Plan Tests **всегда совпадает** с milestone в parent Discussion. Вопросы о milestone на уровне Plan Tests не задаются.

---

## 4. Переходы статусов

Happy path — нормальный поток жизненного цикла Plan Tests ([Стандарт analysis/ § 6](../standard-analysis.md#6-последовательность-статусов)).

**Зона ответственности Plan Tests:** Plan Tests самостоятельно управляет только переходом DRAFT → WAITING (создание и модификация документа). При последующих переходах Plan Tests является **объектом изменений**, а не инициатором.

| Текущий статус | Условие перехода | Следующий статус | Кто управляет |
|---|---|---|---|
| **DRAFT** | Пользователь одобрил. Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]`. Нет Dependency Barrier | **WAITING** | Plan Tests |
| **WAITING** | Все документы цепочки в WAITING. Пользователь подтвердил запуск | **RUNNING** | Цепочка ([§ 6.2](../standard-analysis.md#62-waiting-to-running)) |
| **RUNNING** | Обратная связь от кода затронула Plan Tests ([§ 6.3](../standard-analysis.md#63-running-to-conflict)) | **CONFLICT** | Цепочка (tree-level) |
| **CONFLICT** | LLM исправил, пользователь одобрил ([§ 6.4](../standard-analysis.md#64-conflict-to-waiting)) | **WAITING** | Цепочка (top-down) |
| **RUNNING** | Все TASK-N выполнены → REVIEW ([§ 6.5](../standard-analysis.md#65-running-to-review)) | **REVIEW** | Tree-level |
| **REVIEW** | review.md RESOLVED. Каскад снизу вверх ([§ 6.6](../standard-analysis.md#66-review-to-done)) | **DONE** | Цепочка (bottom-up) |

Откат и отклонение (ROLLING_BACK, REJECTED): [Стандарт analysis/ § 6.7–6.8](../standard-analysis.md#67-to-rolling_back).

**Управление статусами:** [`chain_status.py`](../../.scripts/chain_status.py) — SSOT-модуль для всех переходов. Вызовы `ChainManager.transition()` — в `create-plan-test.md` и `modify-plan-test.md`.

**Артефакты Plan Tests → WAITING:** Нет артефактов в specs/docs/. Plan Tests не создаёт Planned Changes — только определяет тестовые сценарии.

**Побочные эффекты Plan Tests → DONE** ([standard-analysis.md § 7.3](../standard-analysis.md#73-обновление-при-реализации-to-done)):

| Файл specs/docs/ | Действие | SSOT |
|-----------|----------|------|
| `.system/testing.md` | Обновить стратегию тестирования (если изменилась) | [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) |

---

## 5. Разделы документа

Plan Tests — **структурированный документ с per-service разделами**: каждый сервис из Design (SVC-N) получает свой раздел h2 с acceptance-сценариями и тестовыми данными, плюс общие разделы для системных тестов и матрицы покрытия.

| Раздел | Уровень | Обязательность | Заглушка |
|--------|---------|---------------|----------|
| **Резюме** | h2 | Обязательный (контент) | — |
| **SVC-N: {сервис}** (per-service) | h2 | Обязательный (мин. 1) | — |
| ├── Acceptance-сценарии | h3 | Обязательный (контент) | — |
| └── Тестовые данные | h3 | Обязательный | _Использует общие тестовые данные._ |
| **Системные тест-сценарии** | h2 | Обязательный | _Системных тест-сценариев нет._ |
| ├── Тестовые данные | h3 | Обязательный (если секция содержит TC-N и требует fixtures, отсутствующих в per-service разделах) | — |
| **Матрица покрытия** | h2 | Обязательный (контент) | — |
| **Блоки тестирования** | h2 | Обязательный | — |
| **Предложения** | h2 | Обязательный | _Предложений нет._ |
| **Отвергнутые предложения** | h2 | Обязательный | _Отвергнутых предложений нет._ |

**Структура документа:** Резюме → секции по сервисам (Acceptance-сценарии + Тестовые данные) → Системные тест-сценарии → Матрица покрытия → Блоки тестирования → Предложения → Отвергнутые предложения.

**Порядок per-service разделов:** как в Design (Основной → Вторичный → Новый). Каждый SVC-N из Design получает свой раздел h2 в Plan Tests.

**Правила нумерации (TC-N):** Последовательная автоинкрементная, **сквозная по всему документу** (не по сервису) в порядке следования разделов: сначала per-service разделы (в том же порядке, что и в Design), затем системные тест-сценарии. При удалении — **не перенумеровывать** (пропуски допустимы).

**Формат тест-сценария (TC-N):** Естественные предложения на русском. **НЕ** Given/When/Then.

| Колонка | Содержание |
|---------|-----------|
| **ID** | TC-N (Test Case), нумерация сквозная |
| **Описание** | Что делаем → что ожидаем (естественное предложение) |
| **Тип** | unit / integration / e2e / load / smoke |
| **Источник** | Обязательно ≥ 1 из: REQ-N, STS-N, SVC-N § K, INT-N. Предпочтительно REQ-N/STS-N; SVC-N § K или INT-N допустимы для edge-case тестов |
| **Данные** | Ссылка на fixture/factory из секции "Тестовые данные" |

**Типы тестов:**

| Тип | Что тестирует | Где |
|-----|-------------|-----|
| **unit** | Логика одного компонента, модуля или функции сервиса | `/src/{svc}/tests/` |
| **integration** | Взаимодействие между компонентами внутри сервиса или с внешними зависимостями | `/src/{svc}/tests/` |
| **e2e** | Кросс-сервисный сценарий, полный путь от клиента через несколько сервисов | `/tests/` |
| **load** | Нагрузочное тестирование (RPS, latency, конкурентность) | `/tests/` |
| **smoke** | Минимальная проверка работоспособности после деплоя (health endpoints) | `/tests/` |

**Upward feedback:** При создании Plan Tests может обнаружиться информация, затрагивающая Design или Discussion.

**Механика ([Стандарт analysis/ § 3.5](../standard-analysis.md#35-upward-feedback)):**
1. LLM сохраняет plan-test.md в текущем виде (все уже заполненные секции сохраняются без изменений). В ту секцию, генерация которой потребовала обновления вышестоящего уровня, ставится маркер: `[ТРЕБУЕТ УТОЧНЕНИЯ: upward feedback — ожидается обновление Design]`. Незаполненные следующие секции остаются пустыми заголовками. Работа с Plan Tests **приостанавливается**
2. LLM обновляет Design (статус остаётся WAITING), затем проверяет Discussion
3. Пользователь подтверждает изменения
4. Работа с Plan Tests **возобновляется** после подтверждения пользователем изменений в Design

**Критерий:** обнаруженная информация **изменяет проектные решения, контракты или требования** вышестоящих уровней. Детализация тестовых сценариев в рамках уже определённого — не триггер.

### Резюме

Краткое описание тестового плана. Формат: свободный текст (1–3 абзаца).

**Обязательное содержимое:**
- Scope: количество сервисов, общее количество TC-N
- Покрытие STS-N из Design (сколько системных сценариев)
- Покрытие REQ-N из Discussion (сколько требований покрыто)
- Ключевые тестовые решения: решения, принятые специально для данной цепочки и отличающиеся от стратегии в `specs/docs/.system/testing.md`. Если отличий нет — указать: «Стратегия стандартная, см. `specs/docs/.system/testing.md`»

### SVC-N: {сервис} — per-service разделы

Каждый сервис из Design (SVC-N) — **отдельная секция h2** с acceptance-сценариями и тестовыми данными.

**Заголовок:** `## SVC-N: {имя сервиса}` — совпадает с заголовком в Design.

#### Acceptance-сценарии

Таблица TC-N — acceptance-сценарии для конкретного сервиса.

```markdown
### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-1 | Пользователь с валидными credentials отправляет POST /auth/token — ответ 200 с access_token и refresh_token. Время < 100ms | unit | REQ-1, SVC-1 § 2 | user_valid_credentials |
| TC-2 | Пользователь с невалидным паролем отправляет POST /auth/token — ответ 401 Unauthorized | unit | REQ-1 | user_invalid_password |
| TC-3 | Refresh token: отправка на POST /auth/token с grant_type=refresh_token — новый access_token, старый refresh инвалидирован | integration | REQ-2, INT-1 | valid_refresh_token |
```

**Правила описания:**
- Одно предложение: субъект + действие → ожидаемый результат
- Конкретные данные (статус-коды, значения, метрики) если есть в требованиях
- В колонке Описание — без «должен», «следует»: констатация факта

#### Тестовые данные

Описание fixtures, factories, seed data для этого сервиса.

```markdown
### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| user_valid_credentials | Пользователь с корректными данными | username: "testuser", password: "ValidP@ss1" |
| user_invalid_password | Пользователь с невалидным паролем | username: "testuser", password: "wrong" |
| valid_refresh_token | Валидный refresh-токен | token: "rt_abc123", user_id: "uuid-1", expires_at: +24h |
```

**Формат:** Таблица с 3 колонками (Fixture, Описание, Поля). Каждый fixture — уникальное имя (snake_case), описание, ключевые поля.

**Заглушка:** `*Использует общие тестовые данные.*`

### Системные тест-сценарии

Покрытие STS-N из Design. Кросс-сервисные e2e/integration/load тесты. Секция общая для документа.

**Формат:** таблица TC-N (тот же формат, что и per-service).

```markdown
## Системные тест-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-10 | Полный цикл: логин с валидными credentials → получение токена → запрос к защищённому ресурсу → ответ 200 | e2e | STS-1, INT-1, INT-3 | user_valid_credentials, protected_resource |
| TC-11 | Refresh-цикл: access_token истёк → refresh → новый access → запрос → 200 | e2e | STS-2, INT-2 | expired_access_token, valid_refresh_token |
| TC-12 | Rate limiting: 101 запрос за минуту от одного client_id → 429 на 101-м | load | STS-3, INT-1 | rate_limit_client |
```

**Связь с Design:** каждый STS-N из Design должен быть покрыт хотя бы одним TC-N в этой секции.

**Тестовые данные (подсекция h3):** общие данные для системных тестов (если отличаются от per-service).

**Заглушка (всей секции):** `*Системных тест-сценариев нет.*` (допустимо если Design не содержит STS-N — например, один сервис без взаимодействий).

### Матрица покрытия

Трассируемость: каждый REQ-N и STS-N должен быть покрыт хотя бы одним TC-N.

```markdown
## Матрица покрытия

| Источник | TC |
|----------|----|
| REQ-1 | TC-1, TC-2 |
| REQ-2 | TC-3 |
| REQ-3 | TC-12 |
| STS-1 | TC-10 |
| STS-2 | TC-11 |
| STS-3 | TC-12 |
```

**Правила:**
- Каждый REQ-N из Discussion должен быть покрыт ≥ 1 TC-N
- Каждый STS-N из Design должен быть покрыт ≥ 1 TC-N
- Если REQ-N или STS-N не покрыт — маркер `[ТРЕБУЕТ УТОЧНЕНИЯ: нет покрытия для {ID}]`
- Один TC-N может покрывать несколько REQ-N/STS-N — в этом случае TC-N указывается в **каждой** строке источника, который он покрывает

### Блоки тестирования

Раздел после "Матрица покрытия". Зеркалит блоки из plan-dev: каждый dev-BLOCK имеет соответствующий test-BLOCK с TC-N для тех же сервисов. Системные TC (e2e/load из "Системные тест-сценарии") выделяются в отдельный test-BLOCK в последней волне.

**Формат:**

```markdown
## Блоки тестирования

| BLOCK | TC | Сервисы | Dev BLOCK |
|-------|----|---------|-----------|
| BLOCK-1 | TC-1 | shared (INFRA) | BLOCK-1 |
| BLOCK-2 | TC-2..TC-4 | auth | BLOCK-2 |
| BLOCK-3 | TC-5, TC-6 | auth | BLOCK-3 |
| BLOCK-4 | TC-7 | gateway | BLOCK-4 |
| BLOCK-5 | TC-8, TC-9 | users | BLOCK-5 |
| BLOCK-6 | TC-10, TC-11 | users | BLOCK-6 |
| BLOCK-7 | TC-12..TC-14 | e2e (system) | BLOCK-7 |
```

**Двухуровневое тестирование:**

| Уровень | Кто выполняет | Когда | Команда | Тип TC |
|---------|--------------|-------|---------|--------|
| Per-service | Dev-agent | Во время разработки блока | `make test-{svc}` | unit, integration |
| System/e2e | Main LLM (или test-agent) | После завершения волны | `make test-e2e` | e2e, load |

**Правила:**
- Нумерация BLOCK-N сквозная и совпадает с plan-dev
- Маппинг через колонку "Dev BLOCK"
- Per-service TC (unit/integration) → в том же BLOCK-N, что и dev
- Системные TC (e2e/load) → отдельный BLOCK в последней волне
- Каждый TC-N принадлежит ровно одному BLOCK-N

### Предложения

Записи PROP-N от plantest-reviewer, сгруппированные по `###` аспектам. Нумерация PROP-N сквозная по всей секции.

**Формат:**

```markdown
## Предложения

### {Аспект}

| ID | Приоритет | Предложение | Влияет на |
|----|-----------|-------------|-----------|
| PROP-1 | P1 | {Описание предложения} | {TC-N, секция} |
```

**Аспекты:** Покрытие требований, Формат и данные, Блоки тестирования, Антигаллюцинации, Зона ответственности.

**Заглушка:** `_Предложений нет._`

### Отвергнутые предложения

PROP-N, отклонённые пользователем. Перемещаются из секции "Предложения" с указанием причины отклонения.

**Формат:**

```markdown
## Отвергнутые предложения

| ID | Приоритет | Предложение | Причина отклонения |
|----|-----------|-------------|-------------------|
| PROP-1 | P1 | {Описание} | {Причина} |
```

**Заглушка:** `_Отвергнутых предложений нет._`

---

## 6. Clarify

**SSOT:** [Стандарт analysis/ § 8](../standard-analysis.md#8-clarify-и-блокирующие-правила) — полные правила Clarify, маркер `[ТРЕБУЕТ УТОЧНЕНИЯ]`, Dependency Barrier.

**Паттерн объекта:** [Стандарт analysis/ § 2.4](../standard-analysis.md#24-общий-паттерн-объекта) — цикл CLARIFY → GENERATE → VALIDATE → REVIEW.

На уровне Plan Tests LLM уточняет через AskUserQuestion:

| Что уточняется | Пример вопроса |
|----------------|---------------|
| Типы тестов | "Нужны ли load-тесты для auth? SLA = 10k RPS" |
| Покрытие | "REQ-3 (rate limiting) — достаточно ли одного e2e теста?" |
| Тестовые данные | "Какие edge cases для refresh-токена? Истёкший, отозванный, невалидный?" |
| Граничные кейсы | "Тестировать ли concurrent refresh (два запроса одновременно)?" |
| Мокирование | "Для интеграционных тестов auth: мокировать users-сервис или поднимать?" |

**Маркер `[ТРЕБУЕТ УТОЧНЕНИЯ]`:** ставится на неясности. Блокирует WAITING.

**Пропуск:** `--auto-clarify` — LLM генерирует на основе Design/Discussion, ставит маркеры. USER REVIEW обязателен.

---

## 7. Шаблон

`````markdown
---
description: {Описание плана тестов — до 1024 символов}
standard: specs/.instructions/analysis/plan-test/standard-plan-test.md
standard-version: v1.4
index: specs/analysis/README.md
parent: design.md
children: []
status: DRAFT
milestone: {vX.Y.Z — наследуется от parent Discussion}
---

# {NNNN}: {Тема} — Plan Tests

## Резюме

{Scope, кол-во сервисов, кол-во TC-N, покрытие STS-N и REQ-N}

## SVC-1: {сервис 1}

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-1 | {Субъект + действие → ожидаемый результат} | {unit/integration/e2e/load} | {REQ-N, SVC-N § K, INT-N} | {fixture_name} |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| {fixture_name} | {Описание} | {Ключевые поля} |

## SVC-2: {сервис 2}

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-N | {Описание} | {Тип} | {Источник} | {Данные} |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| {fixture_name} | {Описание} | {Поля} |

## Системные тест-сценарии

<!-- Вариант A: Design содержит STS-N -->
| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-N | {Описание кросс-сервисного сценария} | {e2e/integration/load} | {STS-N, INT-N} | {fixture_name} |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| {fixture_name} | {Описание} | {Поля} |

<!-- Вариант B: Design НЕ содержит STS-N -->
*Системных тест-сценариев нет.*

## Матрица покрытия

| Источник | TC |
|----------|----|
| REQ-1 | TC-N, TC-N |
| STS-1 | TC-N |

## Блоки тестирования

| BLOCK | TC | Сервисы | Dev BLOCK |
|-------|----|---------|-----------|
| BLOCK-1 | TC-1..TC-N | SVC-1: {сервис 1} | BLOCK-1 |
| BLOCK-2 | TC-N..TC-N | SVC-2: {сервис 2} | BLOCK-2 |
| BLOCK-3 | TC-N..TC-N | e2e (system) | BLOCK-3 |

## Предложения

_Предложений нет._

## Отвергнутые предложения

_Отвергнутых предложений нет._
`````

---

## 8. Чек-лист качества

> Для автоматической проверки: `python specs/.instructions/.scripts/validate-analysis-plan-test.py {путь}`. Ручной чек-лист — при отсутствии скрипта.

### Frontmatter
- [ ] `description` — до 1024 символов
- [ ] `standard` указывает на этот документ
- [ ] `parent` — путь к Design-документу (обязателен)
- [ ] `children` — путь к Plan Dev (или `[]` до создания)
- [ ] `status` — валидный ([Стандарт analysis/ § 5](../standard-analysis.md#5-статусы))
- [ ] `milestone` — совпадает с parent Discussion

### Структура документа
- [ ] Секция "Резюме" заполнена контентом
- [ ] Минимум 1 per-service раздел (h2)
- [ ] Каждый per-service раздел: Acceptance-сценарии (h3) + Тестовые данные (h3)
- [ ] Acceptance-сценарии: таблица TC-N с 5 колонками (ID, Описание, Тип, Источник, Данные)
- [ ] Секция "Системные тест-сценарии" — контент или заглушка
- [ ] Секция "Матрица покрытия" заполнена контентом

### Формат TC-N
- [ ] Описание — естественное предложение (НЕ Given/When/Then)
- [ ] Тип — один из: unit, integration, e2e, load, smoke
- [ ] Источник — ссылки на REQ-N, STS-N, SVC-N, INT-N
- [ ] Данные — ссылка на fixture из секции "Тестовые данные" (или `—` если не требуется)

### Нумерация
- [ ] TC-N — сквозная по всему документу (не по сервису)
- [ ] Пропуски допустимы, перенумерация запрещена

### Покрытие
- [ ] Каждый REQ-N из Discussion покрыт ≥ 1 TC-N в матрице
- [ ] Каждый STS-N из Design покрыт ≥ 1 TC-N в матрице
- [ ] Нет REQ-N/STS-N без покрытия (иначе маркер `[ТРЕБУЕТ УТОЧНЕНИЯ]`)

### Per-service разделы
- [ ] Каждый SVC-N из Design имеет per-service раздел в Plan Tests
- [ ] Порядок per-service разделов совпадает с Design (Основной → Вторичный → Новый)

### Источники
- [ ] Parent Design прочитан целиком (SVC-N, INT-N, STS-N)
- [ ] Discussion прочитана (REQ-N)
- [ ] `specs/docs/{svc}.md` прочитаны (AS IS)
- [ ] `specs/docs/.system/testing.md` прочитан (стратегия)

### Зона ответственности
- [ ] Нет бизнес-обоснований (→ Discussion)
- [ ] Нет распределения ответственностей (→ Design)
- [ ] Нет контрактов API (→ Design)
- [ ] Нет задач на реализацию (→ Plan Dev)
- [ ] Нет реализации тестов — кода, фреймворков (→ Plan Dev / разработка)

### Блоки тестирования (BLOCK-N)
- [ ] Каждый TC-N принадлежит ровно одному BLOCK-N
- [ ] Нумерация BLOCK-N сквозная, совпадает с plan-dev
- [ ] Системные TC (e2e/load) в отдельном BLOCK последней волны
- [ ] Колонка "Dev BLOCK" указывает на соответствующий блок в plan-dev

### Предложения (PROP-N)
- [ ] Секция "Предложения" присутствует (h2, после "Блоки тестирования")
- [ ] Контент или заглушка "_Предложений нет._"
- [ ] PROP-N сгруппированы по аспектам (### подзаголовки)
- [ ] Каждый PROP-N: ID, Приоритет (P1/P2/P3), Предложение, Влияет на
- [ ] Нумерация PROP-N сквозная по всей секции
- [ ] Секция "Отвергнутые предложения" присутствует (h2, после "Предложения")
- [ ] Контент или заглушка "_Отвергнутых предложений нет._"

### Маркеры
- [ ] Нет `[ТРЕБУЕТ УТОЧНЕНИЯ]` (если статус > DRAFT)
- [ ] Нет Dependency Barrier (если статус > DRAFT)

### Именование
- [ ] Файл: `specs/analysis/NNNN-{topic}/plan-test.md`
- [ ] Заголовок: `# NNNN: {Тема} — Plan Tests`

---

## 9. Примеры по типам

### Пример 1: Новая функциональность (OAuth2)

```markdown
# 0001: OAuth2 авторизация — Plan Tests

## Резюме

Plan Tests для OAuth2 авторизации. 3 сервиса (auth, gateway, users), 12 acceptance-сценариев,
3 системных e2e-теста. Покрытие: REQ-1..REQ-3 (100%), STS-1..STS-3 (100%).
Стратегия мокирования: для unit-тестов — моки внешних зависимостей, для integration — тестовая БД.

## SVC-1: auth

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-1 | Пользователь с валидными credentials отправляет POST /auth/token с grant_type=password — ответ 200 с access_token (JWT) и refresh_token (opaque). Время < 100ms | unit | REQ-1, SVC-1 § 2 | user_valid_credentials |
| TC-2 | Пользователь с невалидным паролем отправляет POST /auth/token — ответ 401 Unauthorized | unit | REQ-1 | user_invalid_password |
| TC-3 | Пользователь с несуществующим username отправляет POST /auth/token — ответ 401 Unauthorized | unit | REQ-1 | user_nonexistent |
| TC-4 | Валидный refresh_token отправляется на POST /auth/token с grant_type=refresh_token — новый access_token, старый refresh_token инвалидирован в БД | integration | REQ-2, INT-2 | valid_refresh_token |
| TC-5 | Отозванный refresh_token отправляется на POST /auth/token — ответ 400 | unit | REQ-2 | revoked_refresh_token |
| TC-6 | Истёкший refresh_token отправляется на POST /auth/token — ответ 400 | unit | REQ-2 | expired_refresh_token |
| TC-7 | DELETE /auth/token/{id} с валидным refresh_token_id — токен отозван, ответ 204 | unit | SVC-1 § 2 | valid_refresh_token |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| user_valid_credentials | Пользователь с корректными данными | username: "testuser", password: "ValidP@ss1", user_id: "uuid-1" |
| user_invalid_password | Пользователь с невалидным паролем | username: "testuser", password: "wrong" |
| user_nonexistent | Несуществующий пользователь | username: "ghost", password: "any" |
| valid_refresh_token | Валидный refresh-токен | token_hash: "sha256_abc", user_id: "uuid-1", expires_at: now+24h |
| revoked_refresh_token | Отозванный refresh-токен | token_hash: "sha256_def", revoked_at: now-1h |
| expired_refresh_token | Истёкший refresh-токен | token_hash: "sha256_ghi", expires_at: now-1h |

## SVC-2: gateway

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-8 | Запрос с валидным JWT в заголовке Authorization — gateway пропускает запрос к целевому сервису | unit | SVC-2 § 4 | valid_jwt |
| TC-9 | Запрос с истёкшим JWT — gateway возвращает 401 без обращения к целевому сервису | unit | SVC-2 § 4 | expired_jwt |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| valid_jwt | Валидный JWT (RS256) | sub: "uuid-1", exp: now+1h, roles: ["user"] |
| expired_jwt | Истёкший JWT | sub: "uuid-1", exp: now-1h |

## SVC-3: users

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-10 | GET /users/{user_id}/roles для существующего пользователя — ответ 200 со списком ролей | unit | INT-3, SVC-3 § 2 | existing_user |
| TC-11 | GET /users/{user_id}/roles для несуществующего пользователя — ответ 404 | unit | INT-3 | nonexistent_user_id |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| existing_user | Пользователь с ролями | user_id: "uuid-1", roles: ["admin", "user"] |
| nonexistent_user_id | Несуществующий user_id | user_id: "uuid-999" |

## Системные тест-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-12 | Полный цикл: логин с валидными credentials → получение токена → запрос к защищённому ресурсу через gateway → ответ 200 | e2e | STS-1, INT-1, INT-3 | user_valid_credentials, protected_resource |
| TC-13 | Refresh-цикл: access_token истёк → отправка refresh_token → новый access_token → запрос → 200 | e2e | STS-2, INT-2 | expired_access_token, valid_refresh_token |
| TC-14 | Rate limiting: 101 запрос за минуту от одного client_id → 429 на 101-м запросе | load | STS-3, INT-1 | rate_limit_client |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| protected_resource | Защищённый ресурс для e2e | endpoint: "/api/v1/products", method: "GET" |
| expired_access_token | Истёкший access JWT | sub: "uuid-1", exp: now-5m |
| rate_limit_client | Клиент для нагрузочного теста | client_id: "load-test-1", requests_per_minute: 101 |

## Матрица покрытия

| Источник | TC |
|----------|----|
| REQ-1 | TC-1, TC-2, TC-3 |
| REQ-2 | TC-4, TC-5, TC-6 |
| REQ-3 | TC-14 |
| STS-1 | TC-12 |
| STS-2 | TC-13 |
| STS-3 | TC-14 |
```

### Пример 2: Минимальный Plan Tests (один сервис, нет взаимодействий)

```markdown
# 0003: Оптимизация кэша — Plan Tests

## Резюме

Plan Tests для оптимизации кэша catalog. 1 сервис, 4 acceptance-сценария, 0 системных тестов.
Покрытие: REQ-1..REQ-2 (100%).

## SVC-1: catalog

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|
| TC-1 | Первый запрос GET /products/{id} — данные читаются из PostgreSQL, кэшируются в Redis | integration | REQ-1, SVC-1 § 4 | product_not_cached |
| TC-2 | Повторный запрос GET /products/{id} в течение 5 мин — данные читаются из Redis, PostgreSQL не вызывается | integration | REQ-1 | product_cached |
| TC-3 | Запрос GET /products/{id} после истечения TTL (5 мин) — данные снова читаются из PostgreSQL | integration | REQ-1 | product_expired_cache |
| TC-4 | При нагрузке 1000 concurrent GET /products/{id} — p99 < 50ms, все запросы возвращают 200 | load | REQ-2 | load_test_products |

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|
| product_not_cached | Продукт без записи в Redis | product_id: "prod-1", exists_in_db: true, exists_in_redis: false |
| product_cached | Продукт с записью в Redis | product_id: "prod-1", redis_key: "catalog:cache:prod-1", ttl: 300s |
| product_expired_cache | Продукт с истёкшим кэшем | product_id: "prod-1", redis_ttl: expired |
| load_test_products | Набор продуктов для нагрузки | count: 100, seeded_in_db: true |

## Системные тест-сценарии

*Системных тест-сценариев нет.*

## Матрица покрытия

| Источник | TC |
|----------|----|
| REQ-1 | TC-1, TC-2, TC-3 |
| REQ-2 | TC-4 |
```
