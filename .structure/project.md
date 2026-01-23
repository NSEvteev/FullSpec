# Структура папок проекта

---

## Корневые файлы

```
/
├── README.md                    # Главный README проекта
├── CLAUDE.md                    # Точка входа для Claude Code
├── Makefile                     # Команды проекта (make help)
└── .gitignore                   # Git ignore
```

---

## Дерево папок (полное)

```
/
├── src/                         # Исходный код сервисов
│   └── {service}/
│       ├── *.md, *.yaml         #   Точка входа: README, Makefile, dependencies.yaml, .env.example
│       ├── backend/
│       │   ├── v*/              #   Версионированный API: handlers, routes, services
│       │   │   └── *.ts
│       │   ├── shared/
│       │   │   └── *.ts         #   Общий код между версиями: models, utils
│       │   └── health/
│       │       └── *.ts         #   Health endpoints: /health, /ready
│       ├── database/
│       │   ├── *.sql            #   Схема БД: schema.sql
│       │   └── migrations/
│       │       └── *.sql        #   Миграции: 001_init.sql, 002_add_users.sql
│       ├── frontend/
│       │   └── *.*              #   Клиентский код (опционально)
│       ├── tests/
│       │   ├── unit/
│       │   │   └── *.test.ts    #   Unit тесты сервиса
│       │   └── integration/
│       │       └── *.test.ts    #   Integration тесты сервиса
│       └── docs/
│           └── *.md             #   Документация сервиса: API, guides, runbooks
│
├── platform/                    # Общая инфраструктура
│   ├── docker/
│   │   └── *.yml                #   Docker конфигурации: docker-compose.yml, docker-compose.dev.yml
│   ├── gateway/
│   │   └── *.*                  #   API Gateway: Traefik/Nginx конфиги
│   ├── monitoring/
│   │   ├── prometheus/
│   │   │   └── *.yml            #   Сбор метрик: prometheus.yml, alerts.yml
│   │   ├── grafana/
│   │   │   └── *.json           #   Дашборды: dashboards/*.json
│   │   └── loki/
│   │       └── *.yml            #   Сбор логов: loki-config.yml
│   ├── k8s/
│   │   └── *.yaml               #   Kubernetes манифесты: deployments, services
│   ├── scripts/
│   │   └── *.sh                 #   Инфраструктурные скрипты: deploy.sh, backup.sh
│   ├── docs/
│   │   └── *.md                 #   Документация инфраструктуры
│   └── runbooks/
│       └── *.md                 #   Runbooks: deploy.md, rollback.md, database-full.md
│
├── tests/                       # Системные тесты
│   ├── e2e/
│   │   └── *.test.ts            #   End-to-end сценарии: user-flow.test.ts
│   ├── integration/
│   │   └── *.test.ts            #   Интеграция между сервисами: auth-users.test.ts
│   ├── load/
│   │   └── *.js                 #   Нагрузочные тесты (k6): load-test.js
│   ├── smoke/
│   │   └── *.test.ts            #   Smoke тесты: health-check.test.ts
│   └── fixtures/
│       └── *.json               #   Общие тестовые данные: users.json
│
├── shared/                      # Общий код между сервисами
│   ├── contracts/
│   │   ├── openapi/
│   │   │   └── *.yaml           #   REST контракты: auth.yaml, users.yaml
│   │   └── protobuf/
│   │       └── *.proto          #   gRPC контракты: auth.proto
│   ├── events/
│   │   └── *.json               #   Схемы событий: user.created.json
│   ├── libs/
│   │   └── *.*                  #   Общие библиотеки: errors, logging, validation
│   ├── assets/
│   │   └── *.*                  #   Статические ресурсы: иконки, шрифты
│   ├── i18n/
│   │   └── *.json               #   Локализация: en.json, ru.json
│   └── docs/
│       └── *.md                 #   Документация общего кода
│
├── config/                      # Конфигурации окружений
│   ├── *.yaml                   #   Окружения: development.yaml, staging.yaml, production.yaml
│   └── feature-flags/
│       └── *.yaml               #   Feature flags: flags.yaml
│
├── specs/                       # Спецификации проекта
│   ├── discussions/
│   │   └── *.md                 #   Дискуссии: 001-new-feature.md
│   ├── impact/
│   │   └── *.md                 #   Импакт-анализ: 001-feature-impact.md
│   ├── services/
│   │   └── {service}/
│   │       ├── *.md             #   Описание сервиса: README.md, architecture.md
│   │       ├── adr/
│   │       │   └── *.md         #   Архитектурные решения: 001-initial.md
│   │       └── plans/
│   │           └── *.md         #   Планы реализации: feature-plan.md
│   └── glossary.md              #   Глоссарий терминов проекта
│
├── .github/                     # GitHub платформа ⚠️ ТРЕБОВАНИЕ GITHUB
│   ├── workflows/               #   ⚠️ Путь фиксирован платформой
│   │   └── *.yml                #   CI/CD pipelines: ci.yml, deploy.yml
│   ├── ISSUE_TEMPLATE/          #   ⚠️ Путь фиксирован платформой
│   │   └── *.md                 #   Шаблоны Issues: bug.md, feature.md
│   ├── PULL_REQUEST_TEMPLATE.md #   Шаблон PR
│   └── CODEOWNERS               #   Владельцы кода
│
└── .claude/                     # Инструменты Claude
    ├── .instructions/
    │   └── *.md                 #   Инструкции для LLM (зеркальная структура)
    ├── skills/
    │   └── */SKILL.md           #   Скиллы: skill-create/, docs-update/
    ├── agents/
    │   └── *.md                 #   Агенты: researcher.md, coder.md
    ├── templates/               #   Шаблоны (по категориям)
    │   ├── specs/               #     Шаблоны спецификаций: adr, discussion, impact, plan
    │   ├── git/                 #     Шаблоны git: commit-message, pr-template
    │   ├── platform/            #     Шаблоны инфраструктуры: runbooks, deployment
    │   ├── doc/                 #     Шаблоны документации: backend, frontend, database
    │   └── tests/               #     Шаблоны тестов: smoke, e2e
    ├── scripts/
    │   └── *.py                 #   Скрипты автоматизации: validate-deps.py
    ├── state/
    │   └── *.json               #   Состояния агентов (не в git)
    ├── drafts/
    │   └── *.md                 #   Черновики: планы, заметки, SSOT (в git)
    ├── settings.json            #   Настройки Claude (в git)
    └── settings.local.json      #   Локальные настройки (не в git)
```

---

## Общие правила

1. **README.md обязателен** — каждая папка ДОЛЖНА иметь README.md как индекс
2. **SSOT в drafts/** — документы-первоисточники хранятся в `/.claude/drafts/`
3. **settings.local.json не в git** — локальные настройки игнорируются
4. **state/ не в git** — состояния агентов игнорируются
