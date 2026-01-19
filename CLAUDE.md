# CLAUDE.md

Точка входа для Claude Code. **Справочная информация** о проекте.

> 📖 **CLAUDE.md** — справочник со ссылками и статусами.
> 📋 **/.claude/instructions/** — инструкции для LLM (правила работы).

## Язык

Используй русский язык для коммуникаций и комментариев в коде.

## Статус проекта

Проект в процессе рефакторинга. Целевая структура описана в [refactoring.md](refactoring.md).

**Временные папки (для примеров):**
- `.claude_old/` — старая структура Claude
- `llm_instructions_old/` — старые инструкции

## Структура проекта

```
/.claude/                   # Инструменты Claude
  /instructions/            # Инструкции для LLM
  /agents/                  # Агенты
  /skills/                  # Скиллы
  /scripts/                 # Скрипты Python
  /templates/               # Шаблоны
  /discussions/             # Дискуссии

/src/                       # Код сервисов
/doc/                       # Документация
/shared/                    # Общий код
/config/                    # Конфигурации окружений
/platform/                  # Инфраструктура
/tests/                     # Системные тесты
```

## Инструкции

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md)

**Правило:** При работе с папкой `/X/` — читать `/.claude/instructions/X/README.md`.

### Типы инструкций

| Тип | Назначение | Когда создавать |
|-----|------------|-----------------|
| `standard` | Требования, КАК делать. Стандарты качества | Один раз, применимы ко всем проектам |
| `project` | Специфика, ЧТО есть в проекте | При старте проекта, специфичны |

**Формат frontmatter:**
```yaml
---
type: standard
description: Краткое описание
---
```

### План создания инструкций

**Фаза 1 — Критичные (🔴):**
1. `git/workflow.md` — GitHub Flow, ветки, PR
2. `git/commits.md` — Conventional commits
3. `src/api/design.md` — URL, методы, статусы
4. `src/data/errors.md` — Формат ошибок
5. `src/data/logging.md` — Формат логов
6. `src/data/validation.md` — Валидация
7. `src/runtime/health.md` — Health checks
8. `src/runtime/database.md` — Работа с БД
9. `src/security/auth.md` — JWT между сервисами
10. `shared/contracts.md` — Контракты API
11. `platform/observability/overview.md` — Observability

**Фаза 2 — Средние (🟡):** 17 инструкций

**Фаза 3 — Низкие (🟢):** 11 инструкций

## Ключевые файлы

| Файл | Назначение |
|------|------------|
| `/doc/glossary.md` | Глоссарий терминов |
| `/.claude/discussions/` | Активные дискуссии |
| `/doc/src/{service}/specs/adr/` | ADR сервиса |

## Задачи

Задачи ведутся через GitHub Issues с префиксами:
- `[AUTH]`, `[NOTIFY]`, `[PAY]` — по сервисам
- `[INFRA]` — инфраструктура
- `[DOCS]` — документация

```bash
gh issue list --state open
gh issue create --label "service:auth" --title "[AUTH] Описание"
```

## Команды

```bash
make dev           # Запустить для разработки
make test          # Запустить тесты
make lint          # Линтинг
```

## Подробнее

Полное описание структуры и правил: [refactoring.md](refactoring.md)
