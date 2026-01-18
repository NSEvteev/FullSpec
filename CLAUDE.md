# CLAUDE.md

Точка входа для Claude Code. Краткий справочник со ссылками на инструкции.

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
    /src/                   # Правила для /src/
    /doc/                   # Правила для /doc/
    /shared/                # Правила для /shared/
    /config/                # Правила для /config/
    /platform/              # Правила для /platform/
    /tests/                 # Правила для /tests/
    /git/                   # Git workflow, commits, issues
    /tools/                 # Агенты и скиллы
  /agents/                  # Агенты
  /skills/                  # Скиллы
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

**Правило:** При работе с папкой `/X/` — читать `/.claude/instructions/X/README.md`.

| Папка | Инструкция |
|-------|------------|
| `/src/` | `/.claude/instructions/src/README.md` |
| `/doc/` | `/.claude/instructions/doc/README.md` |
| `/shared/` | `/.claude/instructions/shared/README.md` |
| `/config/` | `/.claude/instructions/config/README.md` |
| `/platform/` | `/.claude/instructions/platform/README.md` |
| `/tests/` | `/.claude/instructions/tests/README.md` |

**Дополнительные инструкции:**
- Git workflow: `/.claude/instructions/git/README.md`
- Агенты и скиллы: `/.claude/instructions/tools/README.md`

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
