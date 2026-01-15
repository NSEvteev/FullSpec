# Документация проекта

Централизованное хранилище всей документации проекта.

**Полные правила ведения документации:** [instructions_general_docs.md](../llm_instructions/instructions_general_docs.md)

---

## Структура

```
general_docs/
├── glossary.md              # Глоссарий терминов проекта
├── discuss/                 # Дискуссии (идея → решение)
├── architecture/            # Архитектурные документы
├── decisions/               # Architecture Decision Records (ADR)
├── diagrams/                # Диаграммы (.drawio, Mermaid)
├── imp_plans/               # Планы реализации
└── resources/               # Описания ресурсов
    ├── api/                 # API документация
    ├── backend/             # Бэкенд ресурсы
    ├── database/            # Схемы БД
    ├── frontend/            # Фронтенд ресурсы
    └── infra/               # Инфраструктурные ресурсы
```

---

## Ключевые документы

| Документ | Назначение |
|----------|------------|
| [glossary.md](glossary.md) | Глоссарий терминов проекта (14 терминов) |
| [discuss/](discuss/) | [📖 Дискуссии](glossary.md#дискуссия) — обсуждение архитектурных решений |
| [architecture/](architecture/) | Архитектурные документы — решения и их обоснования |
| [decisions/](decisions/) | [📖 Decision (ADR)](glossary.md#decision-adr) — зафиксированные архитектурные решения |
| [diagrams/](diagrams/) | Диаграммы архитектуры (.drawio, Mermaid) |
| [imp_plans/](imp_plans/) | [📖 Планы реализации](glossary.md#план-реализации) — задачи и этапы разработки |
| [resources/](resources/) | Описания ресурсов (БД, API, компоненты) |

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

См. [instructions_general_docs.md](../llm_instructions/instructions_general_docs.md#цепочка-зависимостей-документов)

---

## Быстрый старт

### Для разработчиков

**Ищете архитектурное решение?**
→ Начните с [decisions/](decisions/) (краткие ADR) или [discuss/](discuss/) / [architecture/](architecture/) (детали)

**Нужна схема БД или API?**
→ Смотрите [resources/database/](resources/database/) или [resources/api/](resources/api/)

**Незнакомый термин?**
→ Проверьте [glossary.md](glossary.md)

### Для LLM

**Начало работы:**
1. Прочитать [instructions_general_docs.md](../llm_instructions/instructions_general_docs.md)
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
   - [📖 Дискуссия](glossary.md#дискуссия) → `discuss/XXX_название.md`
   - Архитектурный документ → `architecture/XXX_название.md`
   - [📖 Decision (ADR)](glossary.md#decision-adr) → `decisions/DEC-XXX_название.md`
   - [📖 План реализации](glossary.md#план-реализации) → `imp_plans/XXX_план_название.md`
   - Описание ресурса → `resources/[категория]/XXX_название.md`

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

См. задачу [ID-001] в [llm_tasks/future_tasks.md](../llm_tasks/future_tasks.md) — создание примеров документации запланировано после реализации сервисов.

---

**Последнее обновление:** 2026-01-15
