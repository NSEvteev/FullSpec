# Документация проекта

Централизованное хранилище всей документации проекта.

**Полные правила ведения документации:** [general_docs.md](../llm_instructions/general_docs.md)

---

## Структура

```
general_docs/
├── glossary.md              # Глоссарий терминов проекта
├── 01_discuss/              # Дискуссии (идея → решение)
├── 02_architecture/         # Архитектурные документы
├── 03_diagrams/             # Диаграммы (.drawio, Mermaid)
├── 04_decisions/            # Architecture Decision Records (ADR)
├── 05_resources/            # Описания ресурсов
│   ├── backend/             # Бэкенд ресурсы
│   ├── database/            # Схемы БД
│   ├── frontend/            # Фронтенд ресурсы
│   └── infra/               # Инфраструктурные ресурсы
└── 06_imp_plans/            # Планы реализации
```

---

## Ключевые документы

| Документ | Назначение |
|----------|------------|
| [glossary.md](glossary.md) | Глоссарий терминов проекта (14 терминов) |
| [01_discuss/](01_discuss/) | [📖 Дискуссии](glossary.md#дискуссия) — обсуждение архитектурных решений |
| [02_architecture/](02_architecture/) | Архитектурные документы — решения и их обоснования |
| [03_diagrams/](03_diagrams/) | Диаграммы архитектуры (.drawio, Mermaid) |
| [04_decisions/](04_decisions/) | [📖 Decision (ADR)](glossary.md#decision-adr) — зафиксированные архитектурные решения |
| [05_resources/](05_resources/) | Описания ресурсов (БД, API, компоненты) |
| [06_imp_plans/](06_imp_plans/) | [📖 Планы реализации](glossary.md#план-реализации) — задачи и этапы разработки |

---

## Цепочка зависимостей документов

**Прямая цепочка:**

```
Дискуссия → Архитектура → Decision (ADR) → Ресурсы → План реализации → Документация папок (README.md)
```

**При изменениях:**
- Изменение [📖 Decision (ADR)](glossary.md#decision-adr) → обновить связанные дискуссии и архитектуру
- Изменение ресурса → обновить Decision (ADR) и документацию папок
- Изменение кода → обновить документацию папки, при существенных изменениях — ресурс и Decision (ADR)

**Подробнее:** См. [general_docs.md](../llm_instructions/general_docs.md) — полные правила ведения документации

---

## Быстрый старт

### Для разработчиков

**Ищете архитектурное решение?**
→ Начните с [04_decisions/](04_decisions/) (краткие ADR) или [01_discuss/](01_discuss/) / [02_architecture/](02_architecture/) (детали)

**Нужна схема БД?**
→ Смотрите [05_resources/database/](05_resources/database/)

**Незнакомый термин?**
→ Проверьте [glossary.md](glossary.md)

### Для LLM

**Начало работы:**
1. Прочитать [general_docs.md](../llm_instructions/general_docs.md)
2. Ознакомиться с [glossary.md](glossary.md)
3. Следовать [📖 workflow статусов](glossary.md#workflow-статусов)

**При создании документа:**
1. Использовать шаблон из [llm_instructions/templates/](../llm_instructions/templates/)
2. Добавить новые термины в [glossary.md](glossary.md)
3. Связать с существующими документами через [📖 цепочку зависимостей](glossary.md#цепочка-зависимостей)

---

## Правила работы с документацией

### Создание нового документа

1. **Выбрать тип документа:**
   - [📖 Дискуссия](glossary.md#дискуссия) → `01_discuss/XXX_название.md`
   - Архитектурный документ → `02_architecture/XXX_название.md`
   - [📖 Decision (ADR)](glossary.md#decision-adr) → `04_decisions/DEC-XXX_название.md`
   - [📖 План реализации](glossary.md#план-реализации) → `06_imp_plans/XXX_план_название.md`
   - Описание ресурса → `05_resources/[категория]/XXX_название.md`

2. **Использовать шаблон** из `llm_instructions/templates/`

3. **Указать метаданные:**
   - Статус (draft, in_progress, review, approved, final)
   - Дата создания
   - Автор
   - Связанные документы

4. **Добавить ссылки** на связанные документы

### Workflow статусов

См. [📖 Workflow статусов](glossary.md#workflow-статусов) в глоссарии.

**Краткая версия:**
- `draft` → `in_progress` → `feedback` → `review` → `approved` → `final`

---

## Глоссарий

Все специфичные термины проекта документируются в [glossary.md](glossary.md).

**Формат ссылок на глоссарий:**
```markdown
[📖 Термин](glossary.md#термин)
```

Эмодзи 📖 визуально отличает ссылки на глоссарий от обычных ссылок.

**Текущие термины:** 14
- [📖 Агент](glossary.md#агент)
- [📖 Бэклог](glossary.md#бэклог)
- [📖 Decision (ADR)](glossary.md#decision-adr)
- [📖 Дискуссия](glossary.md#дискуссия)
- [📖 Документация папок](glossary.md#документация-папок)
- [📖 LLM-сессия](glossary.md#llm-сессия)
- [📖 План реализации](glossary.md#план-реализации)
- [📖 Ресурс](glossary.md#ресурс)
- [📖 Скилл](glossary.md#скилл)
- [📖 Слэш-команда](glossary.md#слэш-команда)
- [📖 Цепочка зависимостей](glossary.md#цепочка-зависимостей)
- [📖 Feedback](glossary.md#feedback)
- [📖 Workflow статусов](glossary.md#workflow-статусов)
- и другие (см. глоссарий)

---

## Проверка документации

### Автоматическая проверка

```bash
# Полная проверка документации
make docs-health

# Проверка только ссылок
make docs-links

# Проверка глоссария
make gloss-health

# Полная проверка (документация + глоссарий)
make docs-check
```

### Скиллы Claude Code

- `/doc-health` — проверка здоровья документации
- `/glossary-link` — добавление ссылок на глоссарий во все .md файлы
- `/glossary-candidates` — поиск терминов-кандидатов в глоссарий
- `/glossary-review` — интерактивная обработка кандидатов

---

## Примеры

См. задачу [ID-001] в [llm_tasks/future/0_task_index.md](../llm_tasks/future/0_task_index.md) — создание примеров документации запланировано после реализации сервисов.

---

**Последнее обновление:** 2026-01-15
