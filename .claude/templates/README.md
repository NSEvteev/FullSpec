# Шаблоны

Шаблоны документов для генерации скиллами и ручного использования.

## Назначение

Шаблоны — это готовые структуры документов, которые используются:
- Скиллами для генерации файлов (doc-create, spec-create и др.)
- Вручную для создания типовых документов

> **Структура:** Шаблоны организованы по 4 scope: service, system, workflow, meta.

---

## Индекс шаблонов

### service/ — Шаблоны сервисов

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [dependencies.yaml](./service/dependencies.yaml) | Шаблон зависимостей сервиса | service-create |

### system/ — Шаблоны системы

#### system/platform/ — Инфраструктура

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [runbook-template.md](./system/platform/runbook-template.md) | Шаблон runbook для операций | Ручное использование |
| [docker-compose.template](./system/platform/docker-compose.template) | Шаблон docker-compose | platform-create |
| [dockerfile-node.template](./system/platform/dockerfile-node.template) | Dockerfile для Node.js | platform-create |
| [dockerfile-python.template](./system/platform/dockerfile-python.template) | Dockerfile для Python | platform-create |
| [prometheus-rules.template](./system/platform/prometheus-rules.template) | Правила Prometheus | alerting-create |

#### system/tests/ — Тесты

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [smoke-test.md](./system/tests/smoke-test.md) | Шаблон smoke-теста | test-create |
| [e2e-example.spec.ts](./system/tests/e2e-example.spec.ts) | Пример e2e теста | test-create |
| [unit-test-example.ts](./system/tests/unit-test-example.ts) | Пример unit теста | test-create |

### workflow/ — Шаблоны процессов

#### workflow/docs/ — Документация

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [backend-template.md](./workflow/docs/backend-template.md) | Шаблон для handlers, services, controllers | docs-create |
| [database-template.md](./workflow/docs/database-template.md) | Шаблон для schema, migrations | docs-create |
| [frontend-template.md](./workflow/docs/frontend-template.md) | Шаблон для components, pages | docs-create |
| [minimal-template.md](./workflow/docs/minimal-template.md) | Минимальный шаблон для утилит, констант | docs-create |

#### workflow/git/ — Git

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [codeowners.md](./workflow/git/codeowners.md) | Шаблон CODEOWNERS | Ручное использование |
| [commit-message.md](./workflow/git/commit-message.md) | Формат commit message | issue-execute |
| [pr-template.md](./workflow/git/pr-template.md) | Шаблон Pull Request | issue-execute |
| [github-actions-ci.yml](./workflow/git/github-actions-ci.yml) | Шаблон CI workflow | github-actions |

#### workflow/specs/ — Спецификации

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [discussion.md](./workflow/specs/discussion.md) | Шаблон дискуссии | spec-create |
| [impact.md](./workflow/specs/impact.md) | Шаблон импакт-анализа | spec-create |
| [adr.md](./workflow/specs/adr.md) | Шаблон ADR | spec-create |
| [plan.md](./workflow/specs/plan.md) | Шаблон плана реализации | spec-create |
| [architecture.md](./workflow/specs/architecture.md) | Шаблон архитектуры сервиса | spec-create |

### meta/ — Шаблоны meta-сущностей

> **Перенесено в:** `/.claude/instructions/meta/`

#### instructions/ — Инструкции

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [template-instruction.md](/.claude/instructions/meta/instructions/template-instruction.md) | Шаблон инструкции | instruction-create |
| [template-readme.md](/.claude/instructions/meta/instructions/template-readme.md) | Шаблон README папки инструкций | instruction-create |

#### skills/ — Скиллы

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [template-skill.md](/.claude/instructions/meta/skills/template-skill.md) | Шаблон SKILL.md | skill-create |

---

## Связанные ресурсы

- [/.claude/instructions/](/.claude/instructions/) — инструкции (правила для скиллов)
- [/.claude/skills/README.md](/.claude/skills/README.md) — индекс скиллов
- [/.claude/instructions/workflow/docs/templates.md](/.claude/instructions/workflow/docs/templates.md) — правила выбора шаблона документации
