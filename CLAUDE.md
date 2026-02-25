# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

**Структура:** [.structure/README.md](/.structure/README.md) — SSOT структуры проекта

**Quick Start:** [quick-start.md](/.structure/quick-start.md) | [SSOT](/.structure/ssot.md) | [Артефакты](/.structure/artifacts.md)

**Onboarding:** [onboarding.md](/.claude/onboarding.md)

**Правила:** контекст загружается автоматически из `/.claude/rules/` при работе с файлами.

**AskUserQuestion:** При предложении вариантов выбора использовать `AskUserQuestion` tool.

## Команды

```bash
make setup     # Установить pre-commit хуки (ОБЯЗАТЕЛЬНО после клонирования!)
make help      # Показать все команды
make dev       # Запустить для разработки (docker-compose)
make stop      # Остановить сервисы
make test      # Unit/integration тесты
make test-e2e  # E2E тесты
make lint      # Линтинг
make build     # Сборка для production
make clean     # Очистка (docker down -v)
```

> **Первый шаг:** После клонирования выполни `make setup`. Подробнее: [initialization.md](/.structure/initialization.md)

## Архитектура

Микросервисный fullstack проект с разделением:

| Папка | Назначение |
|-------|------------|
| `/src/{service}/` | Код сервиса (backend/, database/, tests/) |
| `/shared/` | Контракты API, события, общие библиотеки |
| `/platform/` | Docker, Gateway, Kubernetes, мониторинг |
| `/config/` | Конфигурации окружений (dev/staging/prod) |
| `/tests/` | Системные тесты (e2e, integration, load) |
| `/.claude/` | Скиллы, rules, агенты, инструкции |

## Паттерны

- Unit-тесты внутри сервиса: `/src/{service}/tests/`
- Системные тесты между сервисами: `/tests/`
- Секреты НИКОГДА не коммитятся — только `.env.example`

## Задачи

### Текущая сессия — 16 черновиков по зависимостям (было 20, 4 поглощены)

Последовательность по графу зависимостей: ранние фазы расширяют возможности поздних.
Порядок: пользователь читает и валидирует черновик → подтверждает → берём в работу.
После каждого артефакта — обновить SSOT-ссылки в `standard-process.md` §8/§10.

**Фаза 0 — Рефакторинг (0 зависимостей):**
0. [x] **rename-agents-meta** — `.claude/drafts/2026-02-25-rename-agents-meta.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (7 задач: миграция 2 агентов + обновление 13 файлов)

**Фаза 1 — Quick wins (SSOT существует, только /skill-create, 0 зависимостей):**
1. [ ] **commit-skill (G5)** — `.claude/drafts/2026-02-24-commit-skill.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (4 артефакта, 10 задач)
2. [x] **~~sync-skill (G7)~~** — объединён в merge-skill (post-merge sync включён в `/merge`)
3. [ ] **merge-skill (G6+G7)** — `.claude/drafts/2026-02-24-merge-skill.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (2 артефакта, 6 задач)

**Фаза 2 — Процессные скиллы (самодостаточные, средняя сложность):**
4. [ ] **pr-create (G2)** — `.claude/drafts/2026-02-24-pr-create.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (3 артефакта, 8 задач)
5. [ ] **conflict-detect (G10)** — `.claude/drafts/2026-02-24-conflict-detect.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (dev-agent + BLOCK-N + service docs, 16 задач) ⚠️ **БЛОКИРОВАН: dev-agent зависит от docker-dev (#10) и tests-and-platform (#8) — per-service make таргеты, docker-compose**
6. [ ] **rollback-skill (G9)** — `.claude/drafts/2026-02-24-rollback-skill.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (2 артефакта, 5 задач)
7. [ ] **chain-done (G11)** — `.claude/drafts/2026-02-24-chain-done.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (2 артефакта, 5 задач)

**Фаза 3 — Аудиты и определения (выявляют пробелы, определяют инфраструктуру):**

Порядок реализации docker-dev и tests-and-platform:
1. docker-dev (8 задач) — сначала: создаёт docker-compose, Makefile переменные, standard-docker.md
2. tests-and-platform (8 задач, было 5 + 3 из cicd-enhancements) — потом: использует docker-compose.test.yml и Makefile из docker-dev
   - Задачи 4, 8 (ci.yml, pre-release.yml) блокированы docker-dev
   - Задачи 6, 7 (concurrency, dependency-review) — без зависимостей, можно сразу
   - Оба обновляют standard-process.md и Makefile — docker-dev первый (базовые переменные), tests-and-platform второй (per-service таргеты)

8. [ ] **tests-and-platform** — `.claude/drafts/2026-02-24-tests-and-platform.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (аудит тестов + CI/CD pipeline, **8 задач** — 5 оригинальных + 3 из поглощённого cicd-enhancements; platform/ → docker-dev)
9. [ ] **shared-contracts** — `.claude/drafts/2026-02-24-shared-contracts.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (3 per-tech стандарта openapi/protobuf/asyncapi + shared/ README, 9 задач)
10. [ ] **docker-dev** — `.claude/drafts/2026-02-24-docker-dev.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (standard-docker.md + compose + 8 задач)
11. [ ] **user-process-guide** — `.claude/drafts/2026-02-24-user-process-guide.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (/chain + TaskList оркестратор, create-chain.md + SKILL.md + rule, 10 задач)

**Фаза 4 — Новые стандарты (используют решения из Фазы 3):**
12. [ ] **security-scan** — `.claude/drafts/2026-02-25-security-scan.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (3-level security model, security-{tech}.md, pre-release gate E009/E010, gitleaks, 12 задач)
13. [x] ~~**feature-freeze**~~ — **ОТКЛОНЁН** (over-engineering для шаблона, организационный freeze достаточен, нет зависимостей)
14. [ ] **deploy-workflow** — `.claude/drafts/2026-02-25-deploy-workflow.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (standard-deploy.md + deploy.yml + **post-deploy validation**, **12 задач** — 10 оригинальных + 2 из поглощённых smoke-tests/post-release/post-release-validation) *(← docker-dev)*
15. [x] ~~**smoke-tests**~~ — **ПОГЛОЩЁН** deploy-workflow § 12.1 (smoke test определение, `make test-smoke`, `tests/smoke/`)
16. [x] ~~**cicd-enhancements**~~ — **ПОГЛОЩЁН** tests-and-platform пробелы 9-11 (concurrency, dependency-review, pre-release.yml). 5 из 8 пунктов были дублями.
17. [x] ~~**post-release-validation**~~ — **ПОГЛОЩЁН** deploy-workflow § 12.4 (расширение standard-release.md § 11)
18. [x] ~~**post-release (G8)**~~ — **ПОГЛОЩЁН** deploy-workflow § 12 (чек-лист, rollback criteria, /post-release skill). Best practices (canary, SLO, feature flags) отрезаны как over-engineering для template.

**Фаза 5 — Оркестраторы (зависят от всего предыдущего):**
19. [ ] **init-project (G1)** — `.claude/drafts/2026-02-24-init-project.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (create-initialization.md + скилл /init-project + консолидация quick-start/ssot/artifacts + обновления, 15 задач)
20. [ ] **release-create (G3)** — `.claude/drafts/2026-02-24-release-create.md` — **ГОТОВ К РЕАЛИЗАЦИИ** (обогащение create-release.md Шаг 0 + release.yml + скилл, 6 задач)
