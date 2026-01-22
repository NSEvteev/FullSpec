# Шаблоны

Шаблоны документов для генерации скиллами и ручного использования.

## Назначение

Шаблоны — это готовые структуры документов, которые используются:
- Скиллами для генерации файлов (doc-create, spec-create и др.)
- Вручную для создания типовых документов

> **Примечание:** Инструкции (правила для скиллов) перенесены в [/.claude/instructions/](/.claude/instructions/).

---

## Индекс шаблонов

### /doc/ — Шаблоны документации

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [backend-template.md](./doc/backend-template.md) | Шаблон для handlers, services, controllers | doc-create |
| [database-template.md](./doc/database-template.md) | Шаблон для schema, migrations | doc-create |
| [frontend-template.md](./doc/frontend-template.md) | Шаблон для components, pages | doc-create |
| [minimal-template.md](./doc/minimal-template.md) | Минимальный шаблон для утилит, констант | doc-create |

### /git/ — Шаблоны Git

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [codeowners.md](./git/codeowners.md) | Шаблон CODEOWNERS | Ручное использование |
| [commit-message.md](./git/commit-message.md) | Формат commit message | issue-execute |
| [pr-template.md](./git/pr-template.md) | Шаблон Pull Request | issue-execute |

### /platform/ — Шаблоны инфраструктуры

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [runbook-template.md](./platform/runbook-template.md) | Шаблон runbook для операций | Ручное использование |

### /specs/ — Шаблоны спецификаций

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [discussion.md](./specs/discussion.md) | Шаблон дискуссии | spec-create |
| [impact.md](./specs/impact.md) | Шаблон импакт-анализа | spec-create |
| [adr.md](./specs/adr.md) | Шаблон ADR | spec-create |
| [plan.md](./specs/plan.md) | Шаблон плана реализации | spec-create |
| [architecture.md](./specs/architecture.md) | Шаблон архитектуры сервиса | spec-create |

### /tests/ — Шаблоны тестов

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [smoke-test.md](./tests/smoke-test.md) | Шаблон smoke-теста для скиллов | test-create |

---

## Связанные ресурсы

- [/.claude/instructions/](/.claude/instructions/) — инструкции (правила для скиллов)
- [/.claude/skills/README.md](/.claude/skills/README.md) — индекс скиллов
- [/.claude/instructions/docs/templates.md](/.claude/instructions/docs/templates.md) — правила выбора шаблона документации
