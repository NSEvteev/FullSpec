# Маппинг: Инструкции ↔ Папки проекта

---

## Таблица маппинга

| Инструкция | Папка проекта | Описание |
|------------|---------------|----------|
| `.structure/` | `/.structure/` | Правила организации структуры |
| `src/` | `/src/{service}/` | Разработка сервисов |
| `src/api/` | `/src/{service}/backend/v*/` | Проектирование API |
| `src/data/` | `/src/{service}/backend/` | Форматы данных |
| `src/database/` | `/src/{service}/database/` | База данных |
| `src/dev/` | `/src/{service}/` | Локальная разработка |
| `src/health/` | `/src/{service}/backend/health/` | Health checks |
| `src/resilience/` | `/src/{service}/backend/` | Устойчивость |
| `src/security/` | `/src/{service}/backend/` | Безопасность |
| `src/testing/` | `/src/{service}/tests/` | Тестирование сервиса |
| `src/frontend/` | `/src/{service}/frontend/` | Клиентский код |
| `src/docs/` | `/src/{service}/docs/` | Документация сервиса |
| `platform/` | `/platform/` | Инфраструктура |
| `platform/observability/` | `/platform/monitoring/` | Наблюдаемость |
| `platform/docs/` | `/platform/docs/`, `/platform/runbooks/` | Документация, runbooks |
| `tests/` | `/tests/` | Системные тесты |
| `shared/` | `/shared/` | Общий код |
| `shared/docs/` | `/shared/docs/` | Документация общего кода |
| `config/` | `/config/` | Конфигурации |
| `specs/` | `/specs/` | Спецификации |
| `.github/` | `/.github/` | GitHub платформа |
| `.github/issues/` | `/.github/ISSUE_TEMPLATE/` | GitHub Issues |
| `.claude/` | `/.claude/` | Claude-сущности |
| `.github/git/` | — | Git правила (commits, branches, review) |
| `.claude/.instructions/` | `/.claude/.instructions/` | Правила инструкций |
| `.structure/links/` | — | Правила ссылок |
| `.claude/skills/` | `/.claude/skills/` | Правила скиллов |
| `.claude/agents/` | `/.claude/agents/` | Правила агентов |
| `.claude/scripts/` | `/.claude/scripts/` | Правила скриптов |
| `.claude/state/` | `/.claude/state/` | Правила состояний |
| `.claude/drafts/` | `/.claude/drafts/` | Правила черновиков |

---

## Диаграмма связей

```mermaid
flowchart LR
    subgraph INSTR["ИНСТРУКЦИИ"]
        structure_i[".structure/"]
        src_i["src/"]
        platform_i["platform/"]
        tests_i["tests/"]
        shared_i["shared/"]
        config_i["config/"]
        specs_i["specs/"]
        github_i[".github/"]
        dotclaude[".claude/"]
    end

    subgraph PROJECT["ПРОЕКТ"]
        structure_p["/.structure/"]
        src_p["/src/"]
        platform_p["/platform/"]
        tests_p["/tests/"]
        shared_p["/shared/"]
        config_p["/config/"]
        specs_p["/specs/"]
        github_p["/.github/"]
        claude["/.claude/"]
    end

    structure_i --> structure_p
    src_i --> src_p
    platform_i --> platform_p
    tests_i --> tests_p
    shared_i --> shared_p
    config_i --> config_p
    specs_i --> specs_p
    github_i --> github_p
    dotclaude --> claude
```

**Принцип:** Инструкция `X/` → Папка `/X/` (зеркальная структура).
