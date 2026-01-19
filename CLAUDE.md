# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

## Инициализация проекта

> **Блокирующее требование:** Все инструкции из [/.claude/instructions/README.md](/.claude/instructions/README.md) должны быть созданы и заполнены перед началом работы с проектом.

Для создания инструкции используйте `/instruction-create <путь>`.

### Типы инструкций

| Тип | Назначение | При инициализации |
|-----|------------|-------------------|
| `standard` | Стандарты качества (КАК делать) | Использовать as-is |
| `project` | Специфика проекта (ЧТО есть) | Заполнить под проект |

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

**Все команды:** [Makefile](Makefile) или `make help`

```bash
make dev           # Запустить для разработки
make test          # Запустить тесты
make lint          # Линтинг
```

## Подробнее

Полное описание структуры и правил: [refactoring.md](refactoring.md)
