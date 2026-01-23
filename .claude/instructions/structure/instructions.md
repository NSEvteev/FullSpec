# Структура инструкций

**SSOT:** [new_structure_of_project_v3.md](/.claude/drafts/new_structure_of_project_v3.md) — §4

---

## Принцип

Строгое зеркалирование — каждая папка проекта = папка инструкций.

```
Папка /X/  →  Инструкции /.claude/instructions/X/
Правила    →  Инструкции /.claude/instructions/meta/
```

---

## Дерево инструкций (полное)

```
/.claude/instructions/
│
├── structure/                   # Фундамент: определяет всё остальное
│   └── *.md                     #   project, instructions, mapping, lifecycle, responsibilities, examples
│
├── src/                         # → /src/{service}/
│   ├── *.md                     #   lifecycle, structure, dependencies
│   ├── api/                     # → backend/v*/
│   ├── data/                    # → backend/ (форматы данных)
│   ├── database/                # → database/
│   │   └── migrations/          # → database/migrations/
│   ├── dev/                     #   Локальная разработка
│   ├── health/                  # → backend/health/
│   ├── resilience/              # → backend/ (устойчивость)
│   ├── security/                # → backend/ (безопасность)
│   ├── testing/                 # → tests/
│   │   ├── unit/                # → tests/unit/
│   │   └── integration/         # → tests/integration/
│   ├── frontend/                # → frontend/
│   └── docs/                    # → docs/
│
├── platform/                    # → /platform/
│   ├── *.md                     #   deployment, operations, caching, security
│   ├── docker/                  # → docker/
│   ├── gateway/                 # → gateway/
│   ├── monitoring/              # → monitoring/
│   │   ├── prometheus/          # → monitoring/prometheus/
│   │   ├── grafana/             # → monitoring/grafana/
│   │   └── loki/                # → monitoring/loki/
│   ├── k8s/                     # → k8s/
│   ├── scripts/                 # → scripts/
│   ├── docs/                    # → docs/
│   └── runbooks/                # → runbooks/
│
├── tests/                       # → /tests/
│   ├── *.md                     #   formats, project-testing
│   ├── e2e/                     # → e2e/
│   ├── integration/             # → integration/
│   ├── load/                    # → load/
│   ├── smoke/                   # → smoke/
│   └── fixtures/                # → fixtures/
│
├── shared/                      # → /shared/
│   ├── *.md                     #   общие правила
│   ├── contracts/               # → contracts/
│   │   ├── openapi/             # → contracts/openapi/
│   │   └── protobuf/            # → contracts/protobuf/
│   ├── events/                  # → events/
│   ├── libs/                    # → libs/
│   ├── assets/                  # → assets/
│   ├── i18n/                    # → i18n/
│   └── docs/                    # → docs/
│
├── config/                      # → /config/
│   ├── *.md                     #   environments
│   └── feature-flags/           # → feature-flags/
│
├── specs/                       # → /specs/
│   ├── *.md                     #   glossary, workflow, statuses, rules
│   ├── discussions/             # → discussions/
│   ├── impact/                  # → impact/
│   └── services/                # → services/ (шаблон для сервисов)
│       ├── adr/                 # → {service}/adr/
│       └── plans/               # → {service}/plans/
│
├── github/                      # → /.github/
│   ├── *.md                     #   actions, templates, CODEOWNERS
│   ├── workflows/               # → workflows/
│   └── issues/                  # → ISSUE_TEMPLATE/
│
└── meta/                        # → /.claude/ + правила
    ├── git/                     #   Git правила: commits, branches, review
    ├── instructions/            #   Правила инструкций
    ├── links/                   #   Правила ссылок
    ├── skills/                  #   Правила скиллов
    ├── agents/                  #   Правила агентов
    ├── scripts/                 #   Правила скриптов
    ├── state/                   #   Правила состояний
    └── drafts/                  #   Правила черновиков
```

---

## Разделы инструкций

| Раздел | Папка проекта | Описание |
|--------|---------------|----------|
| `structure/` | — | Фундамент: структура проекта и инструкций |
| `src/` | `/src/` | Разработка сервисов |
| `platform/` | `/platform/` | Инфраструктура |
| `tests/` | `/tests/` | Системные тесты |
| `shared/` | `/shared/` | Общий код |
| `config/` | `/config/` | Конфигурации |
| `specs/` | `/specs/` | Спецификации |
| `github/` | `/.github/` | GitHub платформа |
| `meta/` | `/.claude/` | Claude-сущности + правила |
