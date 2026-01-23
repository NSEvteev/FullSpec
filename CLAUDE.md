# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Точка входа для Claude Code. **Справочная информация** о проекте.

> 📖 **CLAUDE.md** — справочник со ссылками и статусами.
> 📋 **/.claude/instructions/** — инструкции для LLM (правила работы).

---

## ⚠️ ШАГ 0: Проверка скиллов (ОБЯЗАТЕЛЬНО)

> **КРИТИЧЕСКОЕ ПРАВИЛО:** Перед выполнением ЛЮБОГО запроса пользователя — проверить скиллы!

### Алгоритм (выполнять ВСЕГДА)

```
1. Получил запрос пользователя
2. СТОП — не начинаю выполнение
3. Читаю список скиллов: /.claude/skills/README.md
4. Проверяю: есть ли скилл для этой задачи?
   - Создать инструкцию → /instruction-create
   - Создать скилл → /skill-create
   - Создать документ → /doc-create
   - Создать issue → /issue-create
   - Обновить ссылки → /links-update
   - Создать спецификацию → /spec-create
   - Изменить статус спецификации → /spec-status
   - Работать со спецификацией → /spec-update
   - И т.д.
5. Если скилл ЕСТЬ → использую скилл
6. Если скилла НЕТ → выполняю вручную
```

### Самопроверка перед действием

Перед использованием `Write`, `Edit`, `mkdir` для файлов в `/.claude/`:

```
⚠️ ПРОВЕРКА: {путь к файлу}
Тип: {skill | instruction | agent | doc | other}
Скилл существует: {да → название | нет}
→ Использую: {/skill-name | ручное создание}
```

**Если скилл существует, но я собираюсь делать вручную → СТОП → использовать скилл.**

### Блокирующие пути

| Путь | Скилл | Ручное создание |
|------|-------|-----------------|
| `/.claude/skills/*/SKILL.md` | `/skill-create` | ❌ ЗАПРЕЩЕНО |
| `/.claude/instructions/**/*.md` | `/instruction-create` | ❌ ЗАПРЕЩЕНО |
| `/.claude/agents/*.md` | спросить пользователя | ⚠️ уточнить |
| `/specs/**` | [/spec-create](/.claude/skills/spec-create/SKILL.md), [/spec-update](/.claude/skills/spec-update/SKILL.md), [/spec-status](/.claude/skills/spec-status/SKILL.md) | ❌ ЗАПРЕЩЕНО |

---

## Блокирующее подтверждение

**СТОП-ПРАВИЛО:** Если в воркфлоу скилла есть шаг с:
- "подтверждение"
- "спросить пользователя"
- "[Y/n]"
- "Применить?"

То Claude ОБЯЗАН:
1. Вывести информацию
2. Задать вопрос
3. **ОСТАНОВИТЬСЯ И ЖДАТЬ ОТВЕТА**
4. НЕ продолжать выполнение до ответа пользователя

Нарушение этого правила = критическая ошибка.

## Использование скиллов

**КРИТИЧНО:** При любом запросе пользователя проверять, можно ли использовать пользовательские скиллы из [/.claude/skills/](/.claude/skills/).

Список скиллов: [/.claude/skills/README.md](/.claude/skills/README.md)

Приоритет: пользовательские скиллы > ручное выполнение.

## Критичные скиллы

**Критичные скиллы** — базовые скиллы управления сущностями проекта. Для них действуют особые правила:

### Список критичных скиллов

| Категория | Скиллы |
|-----------|--------|
| skill-management | `skill-create`, `skill-update`, `skill-delete` |
| instruction-management | `instruction-create`, `instruction-update`, `instruction-delete` |
| git | `issue-create`, `issue-update`, `issue-execute`, `issue-review`, `issue-complete`, `issue-delete` |

### Правила для критичных скиллов

1. **Нельзя удалять единственный тест** критичного скилла через `/test-delete`
2. При **failed тесте** критичного скилла — автоматическое предложение создать Issue
3. Критичные скиллы **приоритетны** в CI/CD проверках

### Как определить критичность

Скилл критичен, если:
- Паттерн имени: `skill-*`, `instruction-*`, `issue-*`
- Или поле `critical: true` в frontmatter SKILL.md

## Статус проекта

Структура проекта описана в [README.md](README.md).

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

## MemoryBank — структурированная память проекта

**MemoryBank** — структурированная память проекта для LLM. Концепты, описывающие что есть в проекте, как принято делать, почему так решили и над чем работаем.

| Компонент | Расположение | Описание |
|-----------|--------------|----------|
| **Patterns** (Паттерны) | `/.claude/instructions/` | Как делать: стандарты, правила |
| **Entities** (Сущности) | `/src/`, `/shared/`, `/platform/` | Что есть: код, контракты, инфраструктура |
| **Entity Docs** (Описания) | `/doc/src/`, `/doc/shared/` | Документация сущностей |
| **Tech Context** (Контекст) | `/specs/services/{service}/architecture.md` | Архитектура сервиса |
| **ADR** (Решения) | `/specs/services/{service}/adr/` | Архитектурные решения |
| **Progress** (Прогресс) | `/specs/services/{service}/plans/` | Планы и roadmap |
| **Active Context** | GitHub Issues | Текущие задачи |
| **Glossary** (Глоссарий) | `/doc/glossary.md` | Термины проекта |
| **Discussions** (Дискуссии) | `/.claude/discussions/` | Обсуждения и заметки |

---

## Инструкции

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md)

**Правило:** При работе с папкой `/X/` — читать `/.claude/instructions/X/README.md`.

### Дерево README.md в /.claude/

```
/.claude/
├── README.md                           # Индекс папки .claude
├── instructions/
│   ├── README.md                       # Главный индекс инструкций (75 файлов)
│   ├── config/                         # (2 файла, README не нужен)
│   ├── doc/
│   │   └── README.md                   # Документация: structure, templates
│   ├── git/
│   │   └── README.md                   # Git: commits, issues, workflow, review, ci
│   ├── platform/
│   │   └── README.md                   # Инфраструктура: docker, deployment, observability
│   ├── shared/
│   │   └── README.md                   # Общий код: contracts, events, libs
│   ├── specs/
│   │   └── README.md                   # Спецификации: discussions, impact, adr, plans
│   ├── src/
│   │   ├── README.md                   # Правила разработки (главный)
│   │   ├── api/README.md               # API: design, versioning, deprecation
│   │   ├── data/README.md              # Данные: errors, logging, pagination
│   │   ├── dev/README.md               # Разработка: local, testing, performance
│   │   ├── runtime/README.md           # Runtime: database, health, resilience
│   │   └── security/README.md          # Безопасность: auth, audit
│   └── tests/
│       └── README.md                   # Тестирование: unit, e2e, claude-testing
├── skills/
│   └── README.md                       # Индекс скиллов
├── templates/
│   ├── specs/                          # Шаблоны спецификаций (5)
│   ├── git/                            # Шаблоны git (4)
│   ├── platform/                       # Шаблоны инфраструктуры (5)
│   ├── doc/                            # Шаблоны документации (4)
│   └── tests/                          # Шаблоны тестов (3)
└── discussions/
    └── README.md                       # Индекс дискуссий
```

## Ключевые файлы

| Файл | Назначение |
|------|------------|
| `/doc/glossary.md` | Глоссарий терминов |
| `/.claude/discussions/` | Активные дискуссии |
| `/specs/services/{service}/adr/` | ADR сервиса |

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

## Полная структура проекта

**Полное описание структуры:** [README.md](README.md)

---

## Граф зависимостей скиллов

**Полный граф:** [/.claude/README.md](/.claude/README.md)

### Оркестраторы (вызывают другие скиллы)

```
skill-create → links-update, skill-update, input-validate, environment-check
instruction-create → links-update, context-update, instruction-update
doc-create/update → links-update, input-validate
doc-delete → issue-create, links-delete
```

### Утилиты (вызываются другими)

| Скилл | Вызывается из |
|-------|---------------|
| `links-update` | 6+ скиллов (самый частый) |
| `environment-check` | 7+ скиллов |
| `input-validate` | 3+ скиллов |
| `context-update` | 3 скилла |

---

## Матрица выбора скиллов

### Когда использовать какой скилл

| Ситуация | Скилл |
|----------|-------|
| Создать новый скилл | `/skill-create` |
| Переименовать/переместить скилл | `/skill-migrate` |
| Проверить все ссылки в проекте | `/links-validate` |
| Переиндексировать документацию | `/doc-reindex` |
| Проверить целостность проекта | `/health-check` |
| Переоткрыть закрытый Issue | `/issue-reopen` |
| Путь изменился | `/links-update` |
| Содержимое изменилось | `/context-update` |

### links-update vs context-update

| Аспект | links-update | context-update |
|--------|--------------|----------------|
| **Что обновляет** | Синтаксис `[text](path)` | Семантический контекст |
| **Глубина** | Прямые ссылки | Транзитивные связи (A→B→C) |
| **Когда** | После создания/переименования | После изменения содержимого |

---

## Запрет архивирования инструкций

**ПРАВИЛО:** Архивирование инструкций ЗАПРЕЩЕНО.

**Причина:** Архивирование создаёт "мёртвый код" в документации, усложняет поиск и поддержку.

**Вместо архивирования:**
1. **Удалить** через `/instruction-delete` — очистит ссылки и статусы
2. **Заменить** — создать новую инструкцию, удалить старую
3. **Объединить** — перенести контент в другую инструкцию

**Если инструкция устарела:**
```
1. /instruction-delete <путь>
2. (скилл автоматически очистит ссылки и обновит README.md)
```

---
