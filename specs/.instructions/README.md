---
description: Индекс инструкций для specs/
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: specs/.instructions/README.md
---

# Инструкции /specs/

Индекс инструкций для папки specs/.

**Полезные ссылки:**
- [specs/](../README.md)

**Содержание:** документация для поставки (specs/docs/), типы документов, межсервисная информация.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [Вложенные области](#вложенные-области) | — | Подобласти инструкций |
| [1. Стандарты](#1-стандарты) | standard-process.md, standard-docs.md, standard-analysis.md | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | validation-docs.md | Проверка согласованности |
| [4. Per-document стандарты (specs/docs/)](#4-per-document-стандарты-docs) | docs/*/ | Стандарт каждого типа документа specs/docs/ |
| [5. Per-object стандарты (analysis/)](#5-per-object-стандарты-analysis) | analysis/*/ | Стандарт каждого типа объекта analysis/ |
| [6. Скрипты](#6-скрипты) | validate-docs.py | Автоматизация |
| [7. Скиллы](#7-скиллы) | — | Скиллы для этой области |

```
/specs/.instructions/
├── .scripts/
├── analysis/
├── docs/
├── hotfixes/               # Инструкции для hotfixes/
├── standard-process.md     # Мета-стандарт процесса поставки ценности (оркестратор)
├── create-chain.md         # Воркфлоу запуска analysis chain (TaskList от идеи до релиза)
├── create-chain-done.md    # Воркфлоу завершения analysis chain (REVIEW → DONE)
├── create-rollback.md      # Воркфлоу отката analysis chain (ROLLING_BACK → REJECTED)
├── create-docs-sync.md     # Воркфлоу синхронизации specs/docs/ (агенты + ревью)
├── create-docker-env.md    # Воркфлоу поднятия Docker dev-окружения (up, healthcheck, troubleshooting)
├── create-test.md          # Воркфлоу финальной валидации (sync, tests, отчёт READY/NOT READY)
├── create-test-ui.md       # Воркфлоу Playwright UI smoke-тестов (SMOKE-NNN сценарии, скриншоты)
└── README.md               # Этот файл (индекс)
```

---

## Вложенные области

Инструкции разделены на подобласти:

| Область | Описание | Индекс |
|---------|----------|--------|
| [pipelines/](./pipelines/) | Инструкции для pipelines/ | [README](./pipelines/README.md) |
| [hotfixes/](./hotfixes/) | Инструкции для hotfixes/ | [README](./hotfixes/README.md) |

---

# 1. Стандарты

| Инструкция | Описание |
|------------|----------|
| [standard-process.md](./standard-process.md) | Мета-стандарт процесса поставки ценности — полный цикл от идеи до релиза, три пути, маппинг шагов на инструменты |
| [standard-docs.md](./docs/standard-docs.md) | Стандарт документации для поставки (контур specs/docs/) — структура, типы документов, принципы |
| [standard-analysis.md](./analysis/standard-analysis.md) | Стандарт аналитического контура (analysis/) — 4 уровня, воркфлоу, статусы, каскады, обновление specs/docs/ |

---

# 2. Воркфлоу

| Инструкция | Описание |
|------------|----------|
| [create-chain.md](./create-chain.md) | Воркфлоу запуска analysis chain — TaskList от идеи до релиза, 4 пути (Happy Path, Hotfix, Bug-bundle, Doc-only) |
| [create-chain-done.md](./create-chain-done.md) | Воркфлоу завершения analysis chain — pre-flight, T7 DONE каскад, Planned Changes → AS IS, cross-chain |
| [create-rollback.md](./create-rollback.md) | Воркфлоу отката analysis chain — T9 ROLLING_BACK, откат артефактов top-down, верификация, T10 REJECTED |
| [create-docs-sync.md](./create-docs-sync.md) | Воркфлоу синхронизации specs/docs/ — оркестрация service/technology/system агентов с ревью (после Plan Dev, перед Dev) |
| [create-docker-env.md](./create-docker-env.md) | Воркфлоу поднятия Docker dev-окружения — docker compose up, healthcheck всех сервисов, troubleshooting (шаг 5.1) |
| [create-test.md](./create-test.md) | Воркфлоу финальной валидации — sync main, полный прогон тестов, проверка полноты, отчёт READY/NOT READY (шаг 5.2) |
| [create-test-ui.md](./create-test-ui.md) | Воркфлоу Playwright UI smoke-тестов — SMOKE-NNN сценарии, скриншоты, отчёт (шаг 5.3) |

---

# 3. Валидация

| Инструкция | Описание |
|------------|----------|
| [validation-docs.md](./docs/validation-docs.md) | Валидация структуры specs/docs/ — наличие обязательных документов, файлов-примеров |

---

# 4. Per-document стандарты (specs/docs/)

Стандарты для каждого типа документа в `specs/docs/`. Расположены в подпапках `docs/{тип}/`.

| Тип документа | Стандарт | Статус |
|---------------|---------|--------|
| specs/docs/README.md | [standard-readme.md](./docs/readme/standard-readme.md) | done |
| {svc}.md | [standard-service.md](./docs/service/standard-service.md) | done |
| overview.md | [standard-overview.md](./docs/overview/standard-overview.md) | done |
| conventions.md | [standard-conventions.md](./docs/conventions/standard-conventions.md) | done |
| infrastructure.md | [standard-infrastructure.md](./docs/infrastructure/standard-infrastructure.md) | done |
| testing.md | [standard-testing.md](./docs/testing/standard-testing.md) | done |
| standard-{tech}.md | [standard-technology.md](./docs/technology/standard-technology.md) | done |

---

# 5. Per-object стандарты (analysis/)

Стандарты для каждого типа объекта в `specs/analysis/`. Расположены в подпапках `analysis/{тип}/`. Корневой стандарт: [standard-analysis.md](./analysis/standard-analysis.md).

| Тип объекта | Стандарт | Статус |
|-------------|---------|--------|
| Discussion | [standard-discussion.md](./analysis/discussion/standard-discussion.md) | done |
| Design | [standard-design.md](./analysis/design/standard-design.md) | done |
| Plan Tests | [standard-plan-test.md](./analysis/plan-test/standard-plan-test.md) | done |
| Plan Dev | [standard-plan-dev.md](./analysis/plan-dev/standard-plan-dev.md) | done |
| Review (артефакт) | [standard-review.md](./analysis/review/standard-review.md) | done |

---

# 6. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-docs.py](./.scripts/validate-docs.py) | Проверка наличия обязательных документов specs/docs/ | [validation-docs.md](./docs/validation-docs.md) |
| [validate-docs-conventions.py](./.scripts/validate-docs-conventions.py) | Валидация формата specs/docs/.system/conventions.md | [validation-conventions.md](./docs/conventions/validation-conventions.md) |
| [validate-docs-infrastructure.py](./.scripts/validate-docs-infrastructure.py) | Валидация формата specs/docs/.system/infrastructure.md | [validation-infrastructure.md](./docs/infrastructure/validation-infrastructure.md) |
| [validate-docs-overview.py](./.scripts/validate-docs-overview.py) | Валидация формата specs/docs/.system/overview.md | [validation-overview.md](./docs/overview/validation-overview.md) |
| [validate-docs-readme.py](./.scripts/validate-docs-readme.py) | Валидация формата specs/docs/README.md | [validation-readme.md](./docs/readme/validation-readme.md) |
| [validate-docs-testing.py](./.scripts/validate-docs-testing.py) | Валидация формата specs/docs/.system/testing.md | [validation-testing.md](./docs/testing/validation-testing.md) |
| [validate-docs-readme-services.py](./.scripts/validate-docs-readme-services.py) | Синхронизация specs/docs/README.md с деревом файлов | [validation-readme.md](./docs/readme/validation-readme.md) |
| [validate-docs-service.py](./.scripts/validate-docs-service.py) | Валидация формата specs/docs/{svc}.md | [validation-service.md](./docs/service/validation-service.md) |
| [validate-docs-technology.py](./.scripts/validate-docs-technology.py) | Валидация формата specs/docs/.technologies/standard-{tech}.md | [validation-technology.md](./docs/technology/validation-technology.md) |
| [validate-analysis-discussion.py](./.scripts/validate-analysis-discussion.py) | Валидация документа дискуссии specs/analysis/NNNN-{topic}/discussion.md | [validation-discussion.md](./analysis/discussion/validation-discussion.md) |
| [validate-analysis-design.py](./.scripts/validate-analysis-design.py) | Валидация документа проектирования specs/analysis/NNNN-{topic}/design.md | [validation-design.md](./analysis/design/validation-design.md) |
| [validate-analysis-plan-test.py](./.scripts/validate-analysis-plan-test.py) | Валидация документа плана тестов specs/analysis/NNNN-{topic}/plan-test.md | [validation-plan-test.md](./analysis/plan-test/validation-plan-test.md) |
| [validate-analysis-plan-dev.py](./.scripts/validate-analysis-plan-dev.py) | Валидация документа плана разработки specs/analysis/NNNN-{topic}/plan-dev.md | [validation-plan-dev.md](./analysis/plan-dev/validation-plan-dev.md) |
| [validate-analysis-review.py](./.scripts/validate-analysis-review.py) | Валидация документа ревью specs/analysis/NNNN-{topic}/review.md | [validation-review.md](./analysis/review/validation-review.md) |
| [create-analysis-design-file.py](./.scripts/create-analysis-design-file.py) | Создание файла design.md по шаблону (frontmatter + структура SVC-N/INT-N/STS-N) | [create-design.md](./analysis/design/create-design.md) |
| [create-analysis-plan-test-file.py](./.scripts/create-analysis-plan-test-file.py) | Создание файла plan-test.md по шаблону (frontmatter + per-service секции из SVC-N) | [create-plan-test.md](./analysis/plan-test/create-plan-test.md) |
| [create-analysis-plan-dev-file.py](./.scripts/create-analysis-plan-dev-file.py) | Создание файла plan-dev.md по шаблону (frontmatter + per-service секции из SVC-N) | [create-plan-dev.md](./analysis/plan-dev/create-plan-dev.md) |
| [create-review-file.py](./.scripts/create-review-file.py) | Создание файла review.md по шаблону (frontmatter + секции Контекст ревью) | [create-review.md](./analysis/review/create-review.md) |
| [extract-svc-context.py](./.scripts/extract-svc-context.py) | Извлечение SVC-N контекста из design.md — список сервисов с затронутыми §§ и технологиями | [create-review.md](./analysis/review/create-review.md) |
| [chain_status.py](./.scripts/chain_status.py) | SSOT-модуль управления статусами analysis chain — переходы, prerequisites, README dashboard, cross-chain | [standard-analysis.md](./analysis/standard-analysis.md) |
| [analysis-status.py](./.scripts/analysis-status.py) | Отображение статусов analysis chain цепочек (одна/все/dashboard) | [standard-analysis.md](./analysis/standard-analysis.md) |

---

# 7. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/docker-up](/.claude/skills/docker-up/SKILL.md) | Поднятие Docker dev-окружения | [create-docker-env.md](./create-docker-env.md) |
| [/test](/.claude/skills/test/SKILL.md) | Финальная валидация | [create-test.md](./create-test.md) |
| [/test-ui](/.claude/skills/test-ui/SKILL.md) | Playwright UI smoke-тесты | [create-test-ui.md](./create-test-ui.md) |
