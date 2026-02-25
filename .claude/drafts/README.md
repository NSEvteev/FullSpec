---
description: Черновики Claude — планы, анализы, спецификации в работе. Индекс активных и архивных черновиков.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: .claude/README.md
---

# /.claude/drafts/ — Черновики

Временные рабочие файлы Claude: планы, заметки, исследования.

Хранилище для размышлений, истории принятия решений и временных заметок. На основе drafts реализуется задуманное. Черновики могут быть источником материала для дискуссий в `/specs/analysis/`.

**Полезные ссылки:**
- [Claude Code окружение](../README.md)
- [Структура проекта](/.structure/README.md)

---

## Оглавление

- [1. Файлы](#1-файлы)
- [2. Подпапки](#2-подпапки)
- [3. Дерево](#3-дерево)

---

## 1. Файлы

| Файл | Описание |
|------|----------|
| [2026-02-20-post-push-review.md](./2026-02-20-post-push-review.md) | Чек-лист ревью после пушей f26c67e, 4b48e15: 6 блоков проверки |
| [2026-02-24-init-project.md](./2026-02-24-init-project.md) | G1: воркфлоу /init-project — оркестратор Фазы 0 (инструкция + скилл) |
| [2026-02-24-chain-done.md](./2026-02-24-chain-done.md) | G11: воркфлоу /chain-done — bottom-up REVIEW→DONE (инструкция + скилл) |
| [2026-02-24-pr-create.md](./2026-02-24-pr-create.md) | G2: PR Create — инструкция + агент + скрипт (не скилл) |
| [2026-02-24-release-create.md](./2026-02-24-release-create.md) | G3: скилл /release-create — оценка полноты create-release.md + план |
| [2026-02-24-commit-skill.md](./2026-02-24-commit-skill.md) | G5: скилл /commit — автогенерация Conventional Commits |
| [2026-02-24-merge-skill.md](./2026-02-24-merge-skill.md) | G6+G7: merge — инструкция + агент (не скилл) + post-merge sync |
| ~~2026-02-24-post-release.md~~ | ~~G8: post-release workflow~~ → поглощён [deploy-workflow.md](./2026-02-25-deploy-workflow.md) § 12 |
| [2026-02-24-rollback-skill.md](./2026-02-24-rollback-skill.md) | G9: скилл /rollback — откат analysis chain |
| [2026-02-24-conflict-detect.md](./2026-02-24-conflict-detect.md) | G10+: Dev-agent — блочная параллельная модель разработки + CONFLICT-детекция |
| [2026-02-24-tests-and-platform.md](./2026-02-24-tests-and-platform.md) | Аудит тестирования + CI/CD pipeline (поглотил cicd-enhancements) |
| ~~2026-02-24-cicd-enhancements.md~~ | ~~CI/CD — аудит pipeline~~ → поглощён [tests-and-platform.md](./2026-02-24-tests-and-platform.md) пробелы 9-11 |
| [2026-02-24-docker-dev.md](./2026-02-24-docker-dev.md) | Docker dev-среда + обучение пользователя |
| [2026-02-24-shared-contracts.md](./2026-02-24-shared-contracts.md) | Shared contracts — исследование покрытия |
| [2026-02-24-user-process-guide.md](./2026-02-24-user-process-guide.md) | User Process Guide — оркестрация разработчика |
| [2026-02-25-deploy-workflow.md](./2026-02-25-deploy-workflow.md) | Deploy Workflow + Post-deploy validation (поглотил smoke-tests, post-release-validation, post-release) |
| ~~2026-02-25-smoke-tests.md~~ | ~~Smoke Tests~~ → поглощён [deploy-workflow.md](./2026-02-25-deploy-workflow.md) § 12.1 |
| [2026-02-25-security-scan.md](./2026-02-25-security-scan.md) | Security Scan — трёхуровневая модель (Automated/Gated/AI-assisted), per-tech security-{tech}.md, pre-release gate, gitleaks |
| ~~2026-02-25-post-release-validation.md~~ | ~~Post-release Validation~~ → поглощён [deploy-workflow.md](./2026-02-25-deploy-workflow.md) § 12.4 |
| [2026-02-25-rename-agents-meta.md](./2026-02-25-rename-agents-meta.md) | Рефакторинг: переименование агентов amy-santiago → meta-agent, captain-holt → meta-reviewer |


---

## 2. Подпапки

### [examples/](./examples/README.md)

**Эталонные черновики.**

Коллекция "хороших" черновиков для использования как примеры в промптах. Не имеет зеркала в `.instructions/`.

---

## 3. Дерево

```
/.claude/drafts/
├── examples/                           # Эталонные примеры
│   ├── example-cross-standards-ssot-analysis.md #   Анализ SSOT между стандартами
│   ├── example-github-platform-research.md      #   Исследование GitHub платформы
│   ├── example-standards-validation-plan.md     #   План валидации стандартов
│   ├── 2026-02-08-specs-architecture.md          #   Архитектура specs/ (SDD)
│   └── README.md                                #   Индекс примеров
├── 2026-02-20-post-push-review.md      # Чек-лист ревью после пушей
├── 2026-02-24-init-project.md          # G1: воркфлоу /init-project
├── 2026-02-24-chain-done.md            # G11: воркфлоу /chain-done
├── 2026-02-24-pr-create.md             # G2: PR Create — инструкция + агент + скрипт
├── 2026-02-24-release-create.md        # G3: скилл /release-create
├── 2026-02-24-commit-skill.md         # G5: скилл /commit
├── 2026-02-24-merge-skill.md          # G6+G7: merge — инструкция + агент
├── 2026-02-24-rollback-skill.md       # G9: скилл /rollback
├── 2026-02-24-conflict-detect.md      # G10+: Dev-agent — блочная параллельная модель
├── 2026-02-24-tests-and-platform.md   # Аудит тестов + CI/CD pipeline (incl. cicd-enhancements)
├── 2026-02-24-docker-dev.md           # Docker dev-среда + обучение
├── 2026-02-24-shared-contracts.md     # Shared contracts — исследование
├── 2026-02-24-user-process-guide.md   # User Process Guide
├── 2026-02-25-deploy-workflow.md      # Deploy + Post-deploy validation (incl. smoke/post-release)
├── 2026-02-25-rename-agents-meta.md   # Рефакторинг: переименование агентов
├── 2026-02-25-security-scan.md        # Security Scan — 3-level model
└── README.md                           # Этот файл (индекс)
```
