---
description: Стандарт планов реализации — формат задач, создание GitHub Issues, маппинг Plan→Issues, обработка CONFLICT.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/.instructions/plan-dev/README.md
---

# Стандарт планов реализации

Версия стандарта: 1.0

Правила создания и обновления планов реализации (`specs/services/{svc}/plans/`). Формат задач, интеграция с GitHub Issues, обработка CONFLICT.

**Полезные ссылки:**
- [Справочник SDD](../standard-specs-reference.md) — статусы, каскады, обратная связь
- [Навигатор SDD](../standard-specs-workflow.md) — полный воркфлоу
- [Инструкции specs/](../README.md)
- [Архитектура specs/ (черновик)](/.claude/drafts/examples/2026-02-08-specs-architecture.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Справочник | [standard-specs-reference.md](../standard-specs-reference.md) |
| Навигатор | [standard-specs-workflow.md](../standard-specs-workflow.md) |
| Тест-спек | [standard-test-spec.md](../plan-test/standard-test-spec.md) *(будет создан)* |
| Валидация | — |
| Создание | — |
| Модификация | — |

## Оглавление

- [1. Версионирование](#1-версионирование)
- [2. Формат задач](#2-формат-задач)
  - [Поля задачи](#поля-задачи)
  - [Порядок и подзадачи](#порядок-и-подзадачи)
- [3. Создание GitHub Issues](#3-создание-github-issues)
  - [Механика](#механика)
  - [Маппинг Plan → Issues](#маппинг-plan--issues)
  - [Sub-issues](#sub-issues)
- [4. CONFLICT и задачи](#4-conflict-и-задачи)

---

## 1. Версионирование

Документы не имеют файловых версий. Версионирование — через цепочку ADR:

```
ADR 001 (DONE) → architecture/services/{svc}.md + tests/ обновлены
ADR 002 (RUNNING) → LLM видит:
    AS IS: текущий architecture/services/{svc}.md
    TO BE: требования из ADR 002
```

DONE-ADR никогда не удаляется — это история принятых решений.

**Очистка REJECTED:** По команде пользователя LLM собирает список REJECTED-документов (включая REJECTED-ADR) и предлагает для удаления. REJECTED-документы — отклонённые решения, не часть истории. Пользователь решает, какие удалить, какие оставить.

---

## 2. Формат задач

Задачи в Plan — **структурированные блоки** (не плоский чек-лист). Каждая задача содержит метаданные и подзадачи:

```markdown
### Задача 1: Создать модуль auth.tokens
- **Сложность:** 7/10
- **Приоритет:** high
- **Зависимости:** —
- **Тест-спек:** [001-oauth2-tests.md#token-generation](...)
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
- **Тест-спек:** [001-oauth2-tests.md#middleware-validation](...)
- **Дельта:** MODIFIED auth.middleware (из ADR)

Подзадачи:
- [ ] 2.1. Заменить session_middleware на jwt_middleware
- [ ] 2.2. Интеграционные тесты (deps: 2.1)
```

### Поля задачи

| Поле | Описание |
|------|----------|
| **Сложность** | 1-10. LLM оценивает при генерации Plan (отдельный шаг анализа не нужен — контекст из 5 уровней спецификаций уже есть) |
| **Приоритет** | high / medium / low. Маппится на label приоритета в Issue |
| **Зависимости** | Внутри Plan — на задачи с меньшим номером. Между Plans — по имени: `Plan auth → Задача 1 "Создать схему UserCreatedEvent"`. При создании Issues LLM превращает именные ссылки в `#N`. Блокирующие — задача не берётся, пока зависимости не done |
| **Тест-спек** | Ссылка на конкретный сценарий из Test Spec. Определяет, что именно тестировать |
| **Дельта** | Ссылка на ADDED/MODIFIED/REMOVED из ADR. Определяет, что именно менять в коде |

### Порядок и подзадачи

**Порядок задач = порядок выполнения.** Агент-кодер получает ссылку на Plan и идёт **строго последовательно сверху вниз**. Если задача заблокирована незавершённой зависимостью — пропустить, взять следующую незаблокированную. Параллельное выполнение задач не предусмотрено.

**Подзадачи:** чек-лист внутри задачи. Могут иметь зависимости на сиблингов (deps: 1.1). Адресуются точечной нотацией (1.2 = подзадача 2 задачи 1).

---

## 3. Создание GitHub Issues

### Механика

GitHub Issues и Milestones создаются **только отдельной командой**, **только после подтверждения плана** пользователем. LLM не создаёт Issues автоматически.

1. Пользователь подтверждает Plan → вся цепочка переходит в RUNNING
2. LLM формирует список Issues из задач Plan (один Plan → много Issues)
3. Milestone берётся из frontmatter Discussion. LLM проверяет, существует ли такой Milestone в GitHub, и создаёт при необходимости
4. Пользователь подтверждает / корректирует
5. LLM создаёт Issues + привязывает к Milestone

**Корректировка даты Milestone:** Если по итогам формирования задач становится ясно, что объём работ не укладывается в дату Milestone (слишком близка) или Milestone слишком далёк — LLM предлагает **сдвинуть дату** того же Milestone ([standard-milestone.md](/.github/.instructions/milestones/standard-milestone.md)). Milestone остаётся тем же (не создавать новый, не переносить Issues). Решение о сдвиге — за пользователем.

### Маппинг Plan → Issues

Интеграция с существующей инфраструктурой: [standard-issue.md](/.github/.instructions/issues/standard-issue.md), [create-issue.md](/.github/.instructions/issues/create-issue.md).

```
Plan (specs/services/auth/plans/jwt-migration-plan.md)
    │
    ├── Задача 1 → Issue #201 "Создать модуль auth.tokens"
    │     ├── Подзадача 1.1 → чек-лист в body Issue
    │     ├── Подзадача 1.2 → чек-лист в body Issue
    │     └── ...
    │
    ├── Задача 2 → Issue #202 "Создать middleware JWT-валидации"
    │     └── **Зависит от:** #201
    │
    └── Задача 3 → Issue #203 "Настроить ротацию ключей"
          └── **Зависит от:** #201, #202
```

| Элемент Plan | GitHub Issue |
|-------------|-------------|
| Задача | Отдельный Issue (по соответствующему шаблону из `.github/ISSUE_TEMPLATE/`: task, bug-report, refactor, docs) |
| Подзадачи | Чек-лист в body Issue (или sub-issues, если нужен отдельный PR) |
| Приоритет | Label приоритета (critical/high/medium/low) |
| Зависимости | `**Зависит от:** #N` в body ([standard-issue.md § 8](/.github/.instructions/issues/standard-issue.md#8-декомпозиция-и-зависимости)) |
| Тест-спек | Ссылка в секции "Связанная документация" |
| Milestone | Определён на уровне Discussion (решение #44) |
| Дельта из ADR | В секции "Описание" Issue |

### Sub-issues

**Когда подзадача → sub-issue:** Если подзадача требует отдельного PR или другого исполнителя ([standard-issue.md § 8](/.github/.instructions/issues/standard-issue.md#8-декомпозиция-и-зависимости)).

---

## 4. CONFLICT и задачи

При CONFLICT-разрешении Plan обновляется → задачи могут измениться. Код в main отсутствует (одна дискуссия = одна ветка = один PR, merge только после завершения всех задач — [standard-github-workflow.md](/.github/.instructions/standard-github-workflow.md)). Действия с Issues по результатам обновлённого Plan:

| Что произошло с задачей | Действие с Issue | SSOT |
|---|---|---|
| **Не изменилась** | Остаётся как есть | — |
| **Изменилась** (описание, критерии, зависимости) | Обновить body/title/labels через `gh issue edit` | [modify-issue.md](/.github/.instructions/issues/modify-issue.md) |
| **Удалена** из обновлённого Plan | Закрыть `--reason "not planned"` с комментарием-ссылкой на CONFLICT | [standard-issue.md § 6](/.github/.instructions/issues/standard-issue.md#6-закрытие-issue) |
| **Новая** в обновлённом Plan | Создать новый Issue | [create-issue.md](/.github/.instructions/issues/create-issue.md) |

Done-подзадачи (чек-лист в body) сохраняются как факт выполненной работы — код в feature-ветке, адаптируется при необходимости.
