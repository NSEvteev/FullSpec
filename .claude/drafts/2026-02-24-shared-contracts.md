# Shared contracts — исследование покрытия

Исследование: как управление контрактами (shared/contracts/, shared/events/) покрыто в текущих инструкциях и что нужно дополнить.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** Проверить, описано ли управление shared contracts и events в текущих инструкциях, найти пробелы
**Почему создан:** `shared/contracts/` (OpenAPI, Protobuf) и `shared/events/` существуют в структуре, но неясно, какие инструкции покрывают их создание, обновление и валидацию
**Связанные файлы:**
- `shared/contracts/openapi/` — REST контракты (OpenAPI)
- `shared/contracts/protobuf/` — gRPC контракты (Protobuf)
- `shared/events/` — схемы событий
- `shared/.instructions/` — стандарты общего кода
- `specs/.instructions/analysis/design/standard-design.md` — Design определяет контракты (INT-N)
- `specs/.instructions/analysis/standard-analysis.md` — общий паттерн, обновление docs/
- `.github/.instructions/development/standard-development.md` — процесс разработки

## Содержание

### Где контракты упоминаются сейчас

| Документ | Что ожидается | Статус | Что найдено |
|----------|--------------|--------|-------------|
| `standard-design.md` § 5 INT-N | INT-N блоки определяют контракты между сервисами | **Покрыто** | INT-N содержит подсекции "Контракт" и "Sequence". Полная спецификация: endpoint, method, request/response, errors. Паттерны: sync (REST), sync (gRPC), async (events), async (queue). Breaking changes помечаются. Версионирование: новый INT-N при v2, старый с `[deprecated]` |
| `standard-design.md` § 5 SVC-N § 2 | API контракты per-service | **Покрыто** | SVC-N § 2 "API контракты" — delta (ADDED/MODIFIED/REMOVED) endpoints. ADDED требует полный контракт. Разграничение: SVC-N § 2 = все API-изменения, INT-N = межсервисный контракт с sequence. Endpoint из INT-N ДОЛЖЕН быть в SVC-N § 2 провайдера |
| `standard-design.md` § 5 SVC-N § 6 | Зависимости от shared/ | **Покрыто** | SVC-N § 6 "Зависимости" — bullet list по направлениям: Предоставляет / Потребляет / Публикует / Подписан / Shared. Ссылки на INT-N |
| `standard-analysis.md` § 3.4 | Shared код (/shared/) — правила | **Покрыто** | 5 правил: (1) владение = SVC-N провайдера включает дельту для shared/, потребители указывают внешнюю зависимость; (2) зависимости в docs/{svc}.md § 6; (3) задачи в Plan Dev с `**Зависит от:** #N`; (4) изменение контракта в shared/ = CONFLICT уровня Design; (5) код одного сервиса — внутри сервиса, выносить в shared/ при 2+ потребителях |
| `standard-analysis.md` § 7.1 | Обновление docs/ при Design → WAITING | **Покрыто (для docs/)** | Planned Changes записываются в `{svc}.md` § 9, `overview.md` § 8, `conventions.md`, `infrastructure.md`. Заглушки для новых сервисов. Но **НЕТ** упоминания обновления файлов в `shared/contracts/` или `shared/events/` |
| `standard-analysis.md` § 7.3 | Обновление docs/ при Design → DONE | **Покрыто (для docs/)** | INT-N контракты **не записываются** отдельно при DONE — они уже включены в SVC-N § 2 провайдеров. INT-N остаётся в design.md как архив. Но **НЕТ** упоминания генерации файлов в `shared/contracts/` |
| `standard-development.md` § 9 | Уровни критичности — документация API | **Частично** | Таблица: `critical-high` и `critical-medium` = "Документация API обязательна (OpenAPI/AsyncAPI)". Но **НЕТ** деталей: как именно генерировать OpenAPI, куда класть, в какой момент цикла |
| `standard-docs.md` § 4 conventions | Конвенции и shared-интерфейсы | **Покрыто** | conventions.md содержит секцию "Shared-пакеты" с полными интерфейсами. Пример: shared/auth (JWT middleware), shared/events (схемы AMQP). Сигнатуры, параметры, примеры вызова |
| `standard-docs.md` § 4 overview | Архитектура — shared-код | **Покрыто** | overview.md § 6 "Shared-код" — таблица пакетов (пакет, назначение, владелец, потребители). Ссылка на conventions.md для полных интерфейсов |
| `standard-docs.md` § 5 | Межсервисная информация | **Покрыто** | Провайдер владеет контрактом (описывает в `{svc}.md` § 2). Потребитель ссылается, не дублирует. Дублирование запрещено |
| `standard-service.md` § 3 API контракты | Формат endpoint-ов | **Покрыто** | Имплементационный уровень. REST (H3 per endpoint), WebSocket, Event channel. Формат: path, method, Auth, Request, Response, Errors. Паттерн и протокол |
| `standard-service.md` § 3 Зависимости | shared-зависимости | **Покрыто** | Формат: `### shared/{package}/ — {зачем}`. Роль, владелец, ссылка на conventions.md |
| `standard-conventions.md` § 2 Shared-пакеты | Интерфейсы shared-пакетов | **Покрыто** | Каждый пакет = H3. 4 элемента: владелец, интерфейс (code), параметры (таблица), пример (code). Ссылка на overview.md для списка |
| `standard-conventions.md` § 2 Версионирование | Версионирование API | **Покрыто** | Правила обратной совместимости: добавление поля = ОК, удаление/переименование = несовместимо. Схема `/api/v1/...` |
| `standard-overview.md` § 2 Shared-код | Таблица shared-пакетов | **Покрыто** | Вводный абзац + таблица: Пакет, Назначение, Владелец, Потребители |
| `standard-overview.md` § 2 Сквозные потоки | Ключевые контракты | **Покрыто** | Каждый поток содержит "Ключевые контракты" — ссылки на endpoints из шагов. Минимум 1 ссылка на поток |
| `standard-codeowners.md` | CODEOWNERS для shared/ | **Покрыто** | `/shared/contracts/` → `@backend-team @frontend-team`; `/shared/events/` → `@backend-team @platform-team` |
| `shared/.instructions/README.md` | Стандарт для shared/ кода | **ПУСТО** | Индекс существует, но все секции пустые: "Нет стандартов", "Нет воркфлоу", "Нет валидаций", "Нет скриптов", "Нет скиллов" |
| `shared/contracts/README.md` | Описание папки контрактов | **Минимально** | Одна строка: `openapi/*.yaml, protobuf/*.proto → Код handlers (→ /src/)`. Нет деталей формата, именования, процесса |
| `shared/contracts/openapi/README.md` | Описание OpenAPI папки | **Минимально** | Одна строка: `auth.yaml, users.yaml → gRPC (→ protobuf/)`. Нет актуальных файлов |
| `shared/contracts/protobuf/README.md` | Описание Protobuf папки | **Минимально** | Одна строка: `auth.proto, users.proto → REST (→ openapi/)`. Нет актуальных файлов |
| `shared/events/README.md` | Описание папки событий | **Минимально** | Одна строка: `user.created.json, order.placed.json → Код publishers (→ /src/)`. Нет актуальных файлов |
| `standard-process.md` § 3 | Выбор пути, hotfix | **Контекст** | Даже hotfix = полная цепочка, потому что "может сломать контракты". Исключение: изменение не затрагивает API контракты, data model, схему интеграций |
| `standard-process.md` § 5 Фаза 1.2 | Design определяет контракты | **Контекст** | Вопрос Design: "Как распределить ответственности?" → `/design-create`. Контракты — фаза "Contract" внутри Design |
| `standard-testing.md` § 2 | Типы тестов — расширяемость | **Упоминание** | "Если проект использует дополнительные типы (Contract, Visual Regression, Property-based) — добавить строки". Contract-тесты упомянуты как опция, но не описаны |
| `design-reviewer AGENT.md` | Ревью контрактов INT-N | **Покрыто** | Проверяет: INT-N полнота, endpoint из INT-N в SVC-N § 2 провайдера, breaking changes, mermaid sequence |
| `create-issue.md` | Зависимости задач shared/ | **Покрыто** | Пример: "B использует результат A" = `shared/ контракты → src/ сервисы` |
| `PR Template` | Breaking changes секция | **Покрыто** | Секция "Breaking changes" в PR template — ломающие изменения API/контрактов |

### Что нужно понять — ответы по результатам исследования

1. **Кто генерирует контракты?**
   - **Аналитический уровень (specs):** Design (INT-N) определяет полный контракт в markdown — endpoint, method, request/response, errors. Контракт описывается в `design.md` и остаётся там как архив.
   - **Документационный уровень (docs):** При Design → WAITING контракты попадают в `{svc}.md` § 2 (через SVC-N § 2) как Planned Changes. При Design → DONE — переносятся в AS IS. Shared-пакеты описываются в `conventions.md` (интерфейсы) и `overview.md` (таблица пакетов).
   - **Кодовый уровень (shared/contracts, shared/events):** **ПРОБЕЛ.** Нет явной инструкции, описывающей: (a) когда создавать файлы `*.yaml` / `*.proto` / `*.json` в `shared/contracts/` и `shared/events/`; (b) кто это делает — Design-агент автоматически или разработчик при реализации; (c) в каком формате. README-файлы в этих папках содержат только по одной строке.

2. **Когда обновляются?**
   - **docs/ уровень:** При Design → WAITING (Planned Changes) и Design → DONE (AS IS). Чётко описано в `standard-analysis.md` § 7.
   - **shared/ файлы:** **ПРОБЕЛ.** Нет описания момента создания/обновления файлов в `shared/contracts/` и `shared/events/`. По логике проекта, SVC-N провайдера включает дельту для файлов в shared/ (standard-analysis.md § 3.4 правило 1), но это правило описывает дельту в *Design-документе*, а не процесс создания физических файлов.

3. **Валидация: есть ли проверка согласованности?**
   - **Аналитический уровень:** design-reviewer агент проверяет: INT-N полноту, пересечение INT-N с SVC-N § 2, breaking changes. Скрипт `validate-analysis-design.py` проверяет структуру.
   - **Документационный уровень:** `validate-docs-conventions.py` проверяет conventions.md. Валидация `{svc}.md` — через `validate-service.py`.
   - **Кодовый уровень:** **ПРОБЕЛ.** Нет скрипта валидации согласованности `shared/contracts/` с `design.md` или `{svc}.md`. Нет pre-commit хука для OpenAPI/Protobuf. Нет contract testing (Pact и пр.).

4. **Events: кто определяет схему и когда обновляются?**
   - **Аналитический уровень:** INT-N с паттерном `async (events)` определяет схему (пример: INT-4 Auth Events в standard-design.md). Формат события — JSON с полями event_type, user_id и т.д.
   - **Документационный уровень:** `conventions.md` → секция "shared/events" описывает: базовый класс `DomainEvent`, таблицу доступных событий, publish/subscribe интерфейсы.
   - **Технология:** AMQP/JSON (RabbitMQ, судя по примерам). Канал: `system.events`. TypedDict-определения в Python.
   - **Кодовый уровень:** `shared/events/README.md` упоминает `user.created.json, order.placed.json`, но это скорее шаблоны — реальных файлов нет. Фактические схемы событий описаны в `conventions.md` как Python TypedDict, а не как JSON Schema.

5. **Версионирование: shared/contracts/ — как?**
   - **API версионирование:** `conventions.md` § 5 "Версионирование API" — `/api/v1/...`, правила обратной совместимости (добавление поля = ОК, удаление = breaking).
   - **INT-N версионирование:** `standard-design.md` § 5 INT-N — при v2 создаётся новый INT-N, старый с `[deprecated: vX.Y.Z]`.
   - **Файловое версионирование shared/contracts/:** **ПРОБЕЛ.** Нет описания: как версионируются файлы `*.yaml` и `*.proto` внутри `shared/contracts/`. Нет соглашения о именовании (v1/, v2/ или internal).

### Интеграция в standard-process.md

Обнаруженные пробелы и рекомендации:

- **Фаза 1 (шаг 1.2):** Design уже определяет контракты через INT-N. Ссылка на shared/ есть в standard-analysis.md § 3.4. **Достаточно** на уровне Design — пробела нет.
- **Фаза 3 (шаг 3.1):** При реализации разработчик создаёт файлы в shared/contracts/ и shared/events/. **ПРОБЕЛ:** Нет инструкции, определяющей: (a) формат файлов (OpenAPI YAML, Protobuf, JSON Schema); (b) именование; (c) момент создания (до кода = spec-first, после кода = code-first); (d) валидацию.
- **§8:** Нужен `shared/.instructions/standard-shared.md` или как минимум расширение README-файлов в shared/ папках.

### Карта покрытия по жизненному циклу контракта

```
Жизненный цикл контракта     | Где описано                              | Статус
─────────────────────────────────────────────────────────────────────────────────────
1. Определение (WHAT)         | Design INT-N (markdown)                  | ПОКРЫТО
2. Согласование (REVIEW)      | design-reviewer + USER REVIEW            | ПОКРЫТО
3. Планирование (PLAN)        | SVC-N § 2, § 6 → Plan Dev TASK-N        | ПОКРЫТО
4. Документирование (DOCS)    | {svc}.md § 2, conventions.md, overview.md| ПОКРЫТО
5. Создание файлов (CODE)     | shared/contracts/, shared/events/        | ПРОБЕЛ
6. Валидация файлов (CI)      | pre-commit, CI pipeline                  | ПРОБЕЛ
7. Тестирование (TEST)        | contract tests                           | ПРОБЕЛ
8. Версионирование (VERSION)  | INT-N deprecated, conventions.md § 5     | ЧАСТИЧНО
9. Breaking change detection  | design-reviewer (аналитика)              | ЧАСТИЧНО
10. Deprecation/Sunset        | INT-N [deprecated]                       | ЧАСТИЧНО
```

## Решения

По результатам исследования:

1. **Аналитический и документационный уровни покрыты хорошо.** Design (INT-N), docs/ ({svc}.md, conventions.md, overview.md), design-reviewer — контракты определяются, описываются, ревьюятся. Пробелов на этих уровнях нет.

2. **Кодовый уровень (shared/contracts/, shared/events/) — основной пробел.** Нет инструкций по:
   - Созданию физических файлов (OpenAPI YAML, Protobuf, JSON Schema)
   - Именованию и структуре
   - Процессу (spec-first vs code-first)
   - Валидации и CI-проверкам
   - Contract testing

3. **Рекомендация — минимальный набор:**
   - Расширить README-файлы в shared/contracts/ и shared/events/ — добавить формат, именование, примеры
   - Определить подход: code-first (FastAPI генерирует OpenAPI) или spec-first
   - Добавить в standard-development.md § 2 или modify-development.md: шаг "обновить shared/contracts/ при изменении API"
   - Опционально: pre-commit хук для linting OpenAPI (`spectral`) и Protobuf (`buf lint`)

4. **Рекомендация — продвинутый набор (при масштабировании):**
   - `shared/.instructions/standard-shared.md` — стандарт для shared/ кода
   - Скиллы `/contract-create`, `/contract-validate`
   - Contract testing (Pact) в CI
   - Breaking change detection (`openapi-diff`, `buf breaking`)
   - JSON Schema для events вместо TypedDict (машинно-валидируемые)

## Открытые вопросы

- Покрывает ли Design (INT-N) → shared/contracts/ трансфер, или это неявная связь?
  - **Ответ:** Неявная связь. Design (INT-N) описывает контракт в markdown. SVC-N провайдера включает дельту для shared/. Но нет инструкции "при реализации создай файл X.yaml в shared/contracts/". Трансфер подразумевается, но не формализован.
- Нужен ли скилл `/contract-create` или `/contract-validate`?
  - **Ответ:** Зависит от подхода. Если code-first (код генерирует OpenAPI) — нужен скрипт генерации + валидации. Если spec-first (OpenAPI первичен) — нужен скилл создания. Текущий проект не определил подход.
- OpenAPI first или code first — какой подход в проекте?
  - **Ответ:** Не определён явно. Контракты описываются в Design (markdown), реализуются в коде. OpenAPI/Protobuf файлы в shared/contracts/ предполагаются структурой, но нет инструкции по их генерации. FastAPI может генерировать OpenAPI автоматически — это code-first.
- Events (shared/events/) — какая технология (Kafka, RabbitMQ, просто схемы)?
  - **Ответ:** AMQP/JSON (RabbitMQ). Канал: `system.events`. Схемы как Python TypedDict (не JSON Schema, не Avro, не Protobuf). Описано в conventions.md секция "shared/events". infrastructure.md § 4 — "Брокер сообщений".

---

## Что уже описано в проекте

### Сильные стороны (хорошо покрытые области)

1. **Аналитический контур (Design INT-N) полностью покрывает определение контрактов.** INT-N блоки содержат: участников, паттерн (sync/async), полный контракт (endpoint, request/response, errors), sequence-диаграмму. Breaking changes помечаются. Версионирование через новый INT-N с deprecated.

2. **Документационный контур (docs/) хорошо структурирован для контрактов.** Три уровня описания:
   - `{svc}.md` § 2 "API контракты" — per-service, имплементационный уровень, все endpoints
   - `conventions.md` § 6 "Shared-пакеты" — интерфейсы shared-кода с сигнатурами и примерами
   - `overview.md` § 6 "Shared-код" — таблица пакетов (назначение, владелец, потребители)

3. **Принцип "провайдер владеет контрактом" чётко закреплён** в standard-docs.md § 5 и standard-service.md § 3 Зависимости. Потребитель ссылается, не дублирует.

4. **Правила shared/ в standard-analysis.md § 3.4** — 5 правил: владение, зависимости, задачи, обратная связь Code → Specs, порог выноса (2+ потребителя).

5. **Обратная связь Code → Specs** при изменении контракта в shared/ = CONFLICT уровня Design (standard-analysis.md § 3.4 правило 4, § 6.3).

6. **CODEOWNERS настроен** — `/shared/contracts/` требует ревью от `@backend-team @frontend-team`, `/shared/events/` — от `@backend-team @platform-team`.

7. **design-reviewer** проверяет качество INT-N: полноту контрактов, пересечение с SVC-N § 2, breaking changes.

8. **Версионирование API** описано в conventions.md § 5 — правила обратной совместимости, URL-схема `/api/v1/...`.

9. **Events (shared/events/)** хорошо описаны в conventions.md: базовый класс DomainEvent, таблица событий, publish/subscribe интерфейсы с рабочими примерами Python-кода.

10. **Требования к документации API по критичности** — standard-development.md § 9: `critical-high` и `critical-medium` = "Документация API обязательна (OpenAPI/AsyncAPI)".

### Пробелы (области без покрытия)

1. **Нет инструкции по созданию/обновлению физических файлов в shared/contracts/ и shared/events/.** Design (INT-N) определяет контракт в markdown, docs/ описывает контракты в текстовом формате, но нигде не сказано: "на шаге X создай файл shared/contracts/openapi/auth.yaml". Цепочка Design → docs/ описана, цепочка Design → shared/ файлы — нет.

2. **shared/.instructions/ полностью пустой.** Индекс существует, но все секции ("Стандарты", "Воркфлоу", "Валидация", "Скрипты", "Скиллы") = пусто. Нет `standard-shared.md`, нет воркфлоу создания shared-пакета.

3. **README-файлы в shared/ папках минимальны.** Содержат только одну строку (IN/OUT). Нет:
   - Формата именования файлов
   - Правил структуры OpenAPI-спецификаций
   - Правил структуры Protobuf-определений
   - Правил структуры JSON-схем событий
   - Примеров

4. **Нет процесса генерации OpenAPI/Protobuf.** Не определён подход: spec-first (OpenAPI первичен, код генерируется) или code-first (код первичен, OpenAPI генерируется из декораторов FastAPI). standard-development.md § 9 требует OpenAPI/AsyncAPI для critical-high и critical-medium, но не описывает как.

5. **Нет валидации согласованности shared/ с Design/docs/.** Нет скрипта, который проверяет: "контракт в shared/contracts/openapi/auth.yaml соответствует описанию в docs/auth.md § 2". Нет pre-commit хука для linting OpenAPI/Protobuf.

6. **Нет contract testing.** standard-testing.md упоминает "Contract" как расширяемый тип тестов, но не описывает: что тестировать, как настроить (Pact, Schemathesis, dredd и пр.), когда запускать.

7. **Нет описания процесса при breaking change контракта в shared/.** standard-design.md INT-N имеет пометку "Breaking change" и `[deprecated]`, но нет формализованного процесса: (a) уведомление потребителей; (b) migration period; (c) удаление deprecated версии.

8. **Нет стратегии файлового версионирования в shared/contracts/.** Нет соглашения: v1/ и v2/ поддиректории? Или единый файл с version field? Или git-теги?

9. **Нет связи между conventions.md "shared/events" и shared/events/ файлами.** Интерфейсы описаны в conventions.md как Python TypedDict. В shared/events/ ожидаются JSON-файлы (user.created.json). Формат не сходится — TypedDict в коде vs JSON Schema в файлах.

10. **Нет скилла для создания shared-пакетов.** Скиллы `/service-create`, `/technology-create` существуют, но нет `/shared-create` или `/contract-create`.

## Best practices

### 1. Contract-First API Design (OpenAPI, AsyncAPI)

**Что это:** API-спецификация (OpenAPI для REST, AsyncAPI для events) создаётся до написания кода. Код генерируется из спецификации или валидируется против неё.

**Как применить:**
- OpenAPI-спецификация для REST: `shared/contracts/openapi/{svc}.yaml` — SSOT для endpoint-ов
- AsyncAPI-спецификация для events: `shared/contracts/asyncapi/{channel}.yaml` — SSOT для событий
- Генерация серверных стабов и клиентов из спецификации
- Валидация в CI: код соответствует спецификации

**Релевантность для проекта:** Текущий подход скорее code-first (контракт описывается в markdown в Design, затем реализуется). Переход к spec-first потребует: (1) генерации OpenAPI/AsyncAPI из INT-N при Design → WAITING; (2) валидации кода против спецификации.

**Альтернатива (code-first):** FastAPI автоматически генерирует OpenAPI из декораторов. Можно экспортировать спецификацию в shared/contracts/ после реализации. Менее строгий контроль, но проще в рамках текущего процесса.

### 2. Consumer-Driven Contract Testing (Pact)

**Что это:** Потребитель API определяет ожидаемый контракт (pact). Провайдер проверяет, что его API соответствует всем pact-ам потребителей. Ломающие изменения обнаруживаются до деплоя.

**Как применить:**
- Pact-файлы генерируются потребителями в unit-тестах
- Провайдер запускает pact-верификацию в CI
- Pact Broker хранит контракты и отслеживает совместимость

**Релевантность для проекта:** standard-testing.md уже упоминает Contract-тесты как расширяемый тип. В текущей архитектуре (4 backend-сервиса + AMQP) — покрытие REST-контрактов через Pact + message pacts для AMQP-событий.

### 3. Schema Registry для Events (Avro, Protobuf, JSON Schema)

**Что это:** Централизованное хранилище схем событий. Producer регистрирует схему перед публикацией. Consumer читает схему из реестра. Эволюция схем контролируется (backward/forward compatibility).

**Как применить:**
- Confluent Schema Registry или AWS Glue Schema Registry
- JSON Schema для AMQP-событий (вместо TypedDict)
- Compatibility checks: BACKWARD, FORWARD, FULL
- Валидация при publish: событие соответствует зарегистрированной схеме

**Релевантность для проекта:** Текущие схемы — Python TypedDict в shared/events/. Для MVP достаточно JSON Schema файлов в shared/events/ с валидацией в pre-commit. Schema Registry — при масштабировании до 10+ типов событий.

### 4. API Versioning Strategies

**Что это:** Стратегия управления несколькими версиями API.

**Текущее состояние:** conventions.md описывает `/api/v1/...` и правила совместимости. INT-N поддерживает `[deprecated: vX.Y.Z]`. Базовое покрытие есть.

**Что можно добавить:**
- Sunset headers (`Sunset: Sat, 01 Jan 2028 00:00:00 GMT`) в deprecated endpoints
- Deprecation policy: минимум N месяцев warning перед удалением
- API changelog (автоматический из INT-N или commits)

### 5. Breaking Change Detection

**Что это:** Автоматическое обнаружение ломающих изменений в контрактах.

**Как применить:**
- `openapi-diff` — сравнение двух OpenAPI-спецификаций, отчёт о breaking/non-breaking changes
- `buf breaking` — для Protobuf: обнаружение обратно-несовместимых изменений
- CI pipeline: PR с изменением shared/contracts/ → автоматическая проверка на breaking changes
- Интеграция с design-reviewer: проверка INT-N пометки "Breaking change"

**Релевантность для проекта:** CODEOWNERS уже требует ревью от frontend-team при изменении shared/contracts/. Автоматическая проверка breaking changes — следующий шаг.

### 6. Backward/Forward Compatibility

**Что это:** Гарантия, что новая версия API/события не ломает существующих потребителей.

**Ключевые правила (уже частично в conventions.md § 5):**
- **Backward compatible:** добавление нового поля, добавление опционального параметра, добавление нового endpoint
- **Breaking:** удаление поля, переименование поля, изменение типа, изменение семантики существующего поля
- **Для events:** добавление нового поля в data = OK, удаление обязательного поля = breaking, изменение имени события = breaking

**Что можно добавить:**
- Формализовать правила для events (сейчас только для REST в conventions.md § 5)
- Тестовая проверка: пример "старого" consumer-а обрабатывает "новое" событие — должен работать
- Явная политика deprecation для событий (аналогично INT-N `[deprecated]`)
