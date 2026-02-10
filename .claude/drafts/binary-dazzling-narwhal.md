# План: Переименование конвенций SDD

## Контекст

Текущий формат именования файлов `NNN-topic.md` (3 цифры, без типа) не позволяет различать файлы разных типов во вкладках, поиске и git log. Уровни 5 и 6 SDD неточно названы ("Тест-спек" и "План"), хотя оба являются планами разного назначения. Папки `test-specs/` и `plans/` в specs/services/ не согласованы с instruction-папками `plan-test/` и `plan-dev/`.

## Три изменения

1. **Формат файлов:** `NNN-topic.md` → `{type}-NNNN-{topic}.md`
2. **Терминология:** "Тест-спек" → "План тестов", "План" → "План разработки"
3. **Папки в specs tree:** `test-specs/` → `plan-test/`, `plans/` → `plan-dev/`

Типы: `disc`, `impact`, `design`, `adr`, `plan-test`, `plan-dev`
Regex: `^(disc|impact|design|adr|plan-test|plan-dev)-(\d{4})-(.+)\.md$`

## Файлы и изменения

### Приоритет 1 — Стандарты (SSOT)

#### 1. `specs/.instructions/standard-specs-reference.md`

| Где | Что → На что |
|-----|-------------|
| :59-62 frontmatter пример | `001-oauth2-*` → `impact-0001-*`, `adr-0001-*` |
| :75-77 таблица связей | "Тест-спек" → "План тестов", "План" → "План разработки" |
| :162-173 mermaid DONE | "Plan → DONE" → "План разработки → DONE", "Test Spec → DONE" → "План тестов → DONE", "все тест-спеки" → "все планы тестов", "все планы DONE" → "все планы разработки DONE" |
| :198-202 таблица DONE | Аналогично mermaid |
| :219-248 примеры REJECTED | "Test Spec" → "План тестов", "Plan" → "План разработки" |
| :256-263 таблица отката | "Test Spec" → "План тестов", "Plan" → "План разработки" |
| :286-287 Code-Specs границы | "Plan / Test Spec" → "План разработки / План тестов" |
| :326-401 примеры обратной связи | "Test Spec" → "План тестов", "Plan" → "План разработки" (во всех 3 сценариях) |
| :437,440 живые документы | "Test Spec → DONE" → "План тестов → DONE" |
| :456-457 таблица Clarify | "Тест-спек" → "План тестов", "План" → "План разработки" |
| :536-557 КЛЮЧЕВОЕ — таблица именования | Полная замена таблицы, regex, удаление исключения планов |
| :555 пример README | `001` → `0001`, `001-oauth2-authorization.md` → `disc-0001-oauth2-authorization.md` |
| :585,593 решения | "Plan/Test Spec" → "План разработки/План тестов" |

#### 2. `specs/.instructions/standard-specs-workflow.md`

| Где | Что → На что |
|-----|-------------|
| :42 оглавление | anchor `#фильтрация-adr--тест-спек` → `#фильтрация-adr--план-тестов` |
| :106-128 mermaid уровней | "ТЕСТ-СПЕК" → "ПЛАН ТЕСТОВ", "ПЛАН" → "ПЛАН РАЗРАБОТКИ", "тест-спеки" → "планы тестов", "Test Spec → DONE" → "План тестов → DONE" |
| :146 mermaid edge | "Test Spec → DONE" → "План тестов → DONE" |
| :157-158 таблица уровней | "Тест-спек" → "План тестов", "План" → "План разработки" |
| :160 поток | "Тест-спек(и) → План(ы)" → "План(ы) тестов → План(ы) разработки" |
| :169-171 таблица объектов | "Тест-спек" → "План тестов", "План" → "План разработки", `test-specs/` → `plan-test/`, `plans/` → `plan-dev/` |
| :203-204 зоны ответственности | `test-specs/` → `plan-test/`, `plans/` → `plan-dev/`, "тест-спеки" → "планы тестов" |
| :221 границы | "Test Spec" → "План тестов" |
| :280-305 mermaid воркфлоу | "Тест-спек svc" → "План тестов svc", "тест-спека" → "плана тестов" |
| :341 прямой поток | "Test Spec" → "План тестов" |
| :460 заголовок секции | "Фильтрация ADR → Тест-спек" → "Фильтрация ADR → План тестов" |
| :462-468 текст фильтрации | "Тест-спек" → "План тестов" |
| :538-539 upward feedback | "Тест-спек" → "План тестов", "План" → "План разработки", "Тест-спек / ADR" → "План тестов / ADR" |
| :567-569 Planned Changes пример | `001-*` → `disc-0001-*`, `design-0001-*` |
| :588-589 таблица стандартов | "Тест-спек" → "План тестов", "План" → "План разработки" |
| :603,620,630 решения | Обновить описания с "тест-спек" → "план тестов" |

### Приоритет 2 — Стандарты объектов

#### 3. `specs/.instructions/plan-dev/standard-plan.md`

| Где | Что |
|-----|-----|
| :12 | `plans/` → `plan-dev/` |
| :26 | "Тест-спек" → "План тестов" |
| :71,85 | "Тест-спек:" → "План тестов:", `001-oauth2-tests.md` → `plan-test-0001-oauth2-tests.md` |
| :100 | "Тест-спек" → "План тестов", "Test Spec" → "план тестов" |
| :130 | `plans/jwt-migration-plan.md` → `plan-dev/plan-dev-0001-jwt-migration.md` |
| :150 | "Тест-спек" → "План тестов" |

#### 4. `specs/.instructions/living-docs/architecture/standard-architecture.md`

| Где | Что |
|-----|-----|
| :84 | "Plan → Test Spec → ADR" → "План разработки → План тестов → ADR" |
| :143,152 | "Test Spec" → "План тестов" |
| :256-258 | `001-*` → `disc-0001-*`, `design-0001-*` |

### Приоритет 3 — README

#### 5. `specs/README.md`

- :50 — "тест-спеки, планы реализации" → "планы тестов, планы разработки"
- :73 — "Стандарт тест-спеков" → "Стандарт планов тестов"
- :84 — `NNN-topic.md` → `disc-NNNN-topic.md`
- :88 — `NNN-topic.md` → `impact-NNNN-topic.md`
- :92 — `NNN-topic.md` → `design-NNNN-topic.md`
- :98 — `NNN-topic.md` → `adr-NNNN-topic.md`
- :100-101 — `test-specs/` → `plan-test/`, `NNN-topic.md` → `plan-test-NNNN-topic.md`
- :103-104 — `plans/` → `plan-dev/`, `topic-plan.md` → `plan-dev-NNNN-topic.md`

#### 6. `specs/.instructions/README.md`

- :46 — "тест-спеков" → "планов тестов"
- :90 — "планов реализации" → "планов разработки"
- :92 — "тест-спеков" → "планов тестов"

#### 7. `specs/.instructions/plan-test/README.md`

- :2 — "тест-планов" → "планов тестов"
- :8 — "тест-спеков" → "планов тестов"
- :10 — "тестовыми спецификациями" → "планами тестов", `test-specs/` → `plan-test/`

#### 8. `specs/.instructions/plan-dev/README.md`

- :8 — "для планов" → "для планов разработки"
- :10 — "планами реализации" → "планами разработки", `plans/` → `plan-dev/`
- :28 — "планов реализации" → "планов разработки"
- :36 — "планов реализации" → "планов разработки"

#### 9. `specs/.instructions/living-docs/README.md`

- :10 — "Test Spec→DONE" → "План тестов→DONE"

### Приоритет 4 — Черновики

#### 10. `.claude/drafts/2026-02-10-specs-documents-plan.md`

~6 мест: "тест-спеков", `NNN-topic`, folder refs.

#### 11. `.claude/drafts/examples/2026-02-08-specs-architecture.md`

~40 мест. Большой файл (1500+ строк). Использовать `replace_all` для массовых замен.

#### 12-13. maybe-archive/ файлы

`2026-02-09-task-master-analysis.md`, `2026-02-09-specs-architecture-review.md` — по 2-5 мест.

#### 14. `.claude/drafts/2026-02-08-specification-driven-development.md`

~5 мест: `NNN-topic.md`, `topic-plan.md`, `plans/`.

## Порядок выполнения

1. standard-specs-reference.md (SSOT именования)
2. standard-specs-workflow.md (SSOT воркфлоу)
3. standard-plan.md (стандарт объекта)
4. standard-architecture.md (стандарт объекта)
5. specs/README.md (дерево)
6. specs/.instructions/README.md, plan-test/README.md, plan-dev/README.md, living-docs/README.md
7. Черновики (batch replace_all)

## Стратегия реализации

Для каждого файла приоритета 1-3: точечные Edit-правки по секциям.
Для черновиков (приоритет 4): `replace_all` по паттернам:
- "Тест-спек" → "План тестов" (и все склонения)
- "тест-спек" → "план тестов"
- `test-specs/` → `plan-test/`
- `plans/` → `plan-dev/`
- `NNN-topic` → `{type}-NNNN-topic` (в контексте)
- `topic-plan.md` → `plan-dev-NNNN-topic.md`

## Проверка

1. `Grep "тест-спек" specs/` — 0 результатов
2. `Grep "NNN-topic" specs/` — 0 результатов
3. `Grep "test-specs/" specs/` — 0 результатов (кроме specs/tests/)
4. `Grep "plans/" specs/` — 0 результатов (кроме контекстных упоминаний)
5. `git diff --stat` — оценить масштаб
6. Pre-commit hooks — должны пройти
