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

### Текущая сессия — 20 черновиков по зависимостям

Последовательность по графу зависимостей: ранние фазы расширяют возможности поздних.
Порядок: пользователь читает и валидирует черновик → подтверждает → берём в работу.
После каждого артефакта — обновить SSOT-ссылки в `standard-process.md` §8/§10.

**Фаза 1 — Quick wins (SSOT существует, только /skill-create, 0 зависимостей):**
1. [ ] **commit-skill (G5)** — `.claude/drafts/2026-02-24-commit-skill.md`
2. [ ] **sync-skill (G7)** — `.claude/drafts/2026-02-24-sync-skill.md`
3. [ ] **merge-skill (G6)** — `.claude/drafts/2026-02-24-merge-skill.md`

**Фаза 2 — Процессные скиллы (самодостаточные, средняя сложность):**
4. [ ] **pr-create (G2)** — `.claude/drafts/2026-02-24-pr-create.md`
5. [ ] **conflict-detect (G10)** — `.claude/drafts/2026-02-24-conflict-detect.md`
6. [ ] **rollback-skill (G9)** — `.claude/drafts/2026-02-24-rollback-skill.md`
7. [ ] **chain-done (G11)** — `.claude/drafts/2026-02-24-chain-done.md` *(instruction + skill + agent)*

**Фаза 3 — Аудиты и определения (выявляют пробелы, определяют инфраструктуру):**
8. [ ] **tests-and-platform** — `.claude/drafts/2026-02-24-tests-and-platform.md`
9. [ ] **shared-contracts** — `.claude/drafts/2026-02-24-shared-contracts.md`
10. [ ] **docker-dev** — `.claude/drafts/2026-02-24-docker-dev.md`
11. [ ] **user-process-guide** — `.claude/drafts/2026-02-24-user-process-guide.md`

**Фаза 4 — Новые стандарты (используют решения из Фазы 3):**
12. [ ] **security-scan** — `.claude/drafts/2026-02-25-security-scan.md`
13. [ ] **feature-freeze** — `.claude/drafts/2026-02-25-feature-freeze.md`
14. [ ] **deploy-workflow** — `.claude/drafts/2026-02-25-deploy-workflow.md` *(← docker-dev)*
15. [ ] **smoke-tests** — `.claude/drafts/2026-02-25-smoke-tests.md` *(← tests-and-platform, docker-dev)*

**Фаза 5 — Интеграция (зависит от стандартов Фазы 4):**
16. [ ] **cicd-enhancements** — `.claude/drafts/2026-02-24-cicd-enhancements.md` *(← deploy, smoke tests)*
17. [ ] **post-release-validation** — `.claude/drafts/2026-02-25-post-release-validation.md` *(← deploy, smoke tests)*
18. [ ] **post-release (G8)** — `.claude/drafts/2026-02-24-post-release.md` *(← deploy, post-release-validation)*

**Фаза 6 — Оркестраторы (зависят от всего предыдущего):**
19. [ ] **init-project (G1)** — `.claude/drafts/2026-02-24-init-project.md`
20. [ ] **release-create (G3)** — `.claude/drafts/2026-02-24-release-create.md` *(← deploy, smoke, security, freeze, post-release, chain-done)*
