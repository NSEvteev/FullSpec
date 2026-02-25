---
description: Переименование агентов amy-santiago → meta-agent, captain-holt → meta-reviewer
type: refactoring
status: done
created: 2026-02-25
---

# Переименование агентов: amy-santiago → meta-agent, captain-holt → meta-reviewer

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Изменения](#изменения)
  - [Порядок выполнения](#порядок-выполнения)
  - [Риски](#риски)
  - [Чек-лист готовности](#чек-лист-готовности)

## Контекст

Текущие имена агентов (`amy-santiago`, `captain-holt`) — персонажи Brooklyn Nine-Nine. Не передают назначение без знания контекста. Новые имена (`meta-agent`, `meta-reviewer`) описывают роль: оба работают с мета-слоем проекта (инструкции, скиллы, правила, структура).

**Тип:** рефакторинг (переименование без изменения функциональности).

## Содержание

### Изменения

#### 1. Переименование папок (filesystem)

| Было | Стало |
|------|-------|
| `.claude/agents/amy-santiago/` | `.claude/agents/meta-agent/` |
| `.claude/agents/captain-holt/` | `.claude/agents/meta-reviewer/` |

**Действие:** `/agent-modify` с типом "миграция" для каждого агента.

#### 2. Файлы агентов (AGENT.md)

##### 2.1. meta-agent (бывший amy-santiago)

**Файл:** `.claude/agents/meta-agent/AGENT.md`

| Поле / строка | Было | Стало |
|---------------|------|-------|
| frontmatter `name` | `amy-santiago` | `meta-agent` |
| frontmatter `description` | `Помощник по созданию инструкций (Эми Сантьяго). Используй для работы с документацией, скиллами, правилами и структурой проекта.` | `Помощник по созданию инструкций. Используй для работы с документацией, скиллами, правилами и структурой проекта.` |
| Роль (строка 37) | `Ты — Эми Сантьяго, эксперт по документации и инструкциям.` | `Ты — эксперт по документации и инструкциям.` |
| Роль (строка 39) | `Как и твой прототип из Brooklyn Nine-Nine, ты обожаешь порядок, правила и идеально структурированные документы.` | `Ты следуешь порядку, правилам и создаёшь идеально структурированные документы.` |
| Строка 135 | `Amy Santiago создаёт только` | `meta-agent создаёт только` |
| Строка 302 | `/.claude/agents/amy-santiago/CHANGELOG.md` | `/.claude/agents/meta-agent/CHANGELOG.md` |
| Строка 306 | `# CHANGELOG — Amy Santiago` | `# CHANGELOG — meta-agent` |

##### 2.2. meta-reviewer (бывший captain-holt)

**Файл:** `.claude/agents/meta-reviewer/AGENT.md`

| Поле / строка | Было | Стало |
|---------------|------|-------|
| frontmatter `name` | `captain-holt` | `meta-reviewer` |
| frontmatter `description` | (без изменений — уже описательное) | (без изменений) |
| Роль (строка 18) | `Ты — Капитан Реймонд Холт, педантичный аналитик ясности документации.` | `Ты — педантичный аналитик ясности документации.` |
| Строка 157 | `captain-holt-{timestamp}.json` | `meta-reviewer-{timestamp}.json` |
| Строка 270 | `/.claude/agents/captain-holt/CHANGELOG.md` | `/.claude/agents/meta-reviewer/CHANGELOG.md` |

#### 3. CHANGELOG агентов

##### 3.1. meta-agent/CHANGELOG.md

| Строка | Было | Стало |
|--------|------|-------|
| 1 | `# CHANGELOG — Amy Santiago` | `# CHANGELOG — meta-agent` |
| 3 | `История изменений агента amy-santiago.` | `История изменений агента meta-agent.` |
| 14 | `**Исправления по анализу Captain Holt**` | `**Исправления по анализу meta-reviewer**` |

##### 3.2. meta-reviewer/CHANGELOG.md

| Строка | Было | Стало |
|--------|------|-------|
| 1 | `# CHANGELOG — Captain Holt` | `# CHANGELOG — meta-reviewer` |
| 3 | `История изменений стандартов анализа агента captain-holt.` | `История изменений стандартов анализа агента meta-reviewer.` |

#### 4. Индекс агентов

**Файл:** `.claude/.instructions/agents/README.md`

| Строка | Было | Стало |
|--------|------|-------|
| 139 | `[captain-holt](/.claude/agents/captain-holt/AGENT.md) \| plan \| Семантический анализ...` | `[meta-reviewer](/.claude/agents/meta-reviewer/AGENT.md) \| plan \| Семантический анализ...` |
| 140 | `[amy-santiago](/.claude/agents/amy-santiago/AGENT.md) \| general-purpose \| Помощник по созданию...` | `[meta-agent](/.claude/agents/meta-agent/AGENT.md) \| general-purpose \| Помощник по созданию...` |

#### 5. README .claude/

**Файл:** `.claude/README.md` (строка 60)

| Было | Стало |
|------|-------|
| `captain-holt` (семантический анализ документов), `amy-santiago` (помощник по инструкциям) | `meta-reviewer` (семантический анализ документов), `meta-agent` (помощник по инструкциям) |

#### 6. CHANGELOG .claude/

**Файл:** `.claude/CHANGELOG.md`

| Строка | Было | Стало |
|--------|------|-------|
| 26 | `Агент Captain Holt для семантического анализа` | `Агент meta-reviewer для семантического анализа` |
| 72 | `Агенты Amy Santiago и Captain Holt` | `Агенты meta-agent и meta-reviewer` |

#### 7. Стандарт агентов

**Файл:** `.claude/.instructions/agents/standard-agent.md`

| Строка | Было | Стало |
|--------|------|-------|
| 576 | `amy-santiago` | `meta-agent` |
| 577 | `captain-holt` | `meta-reviewer` |
| 591 | `Task: amy-santiago` | `Task: meta-agent` |
| 599 | `Task: captain-holt` | `Task: meta-reviewer` |
| 609 | `Task: amy-santiago` | `Task: meta-agent` |

#### 8. Валидация агентов

**Файл:** `.claude/.instructions/agents/validation-agent.md` (строка 290)

| Было | Стало |
|------|-------|
| `captain-holt` | `meta-reviewer` |

#### 9. Инструкции по инструкциям

##### 9.1. standard-instruction.md

**Файл:** `.instructions/standard-instruction.md`

| Строка | Было | Стало |
|--------|------|-------|
| 123 | `агент captain-holt` | `агент meta-reviewer` |
| 125 | `анализа captain-holt` | `анализа meta-reviewer` |
| 132 | `captain-holt для анализа` | `meta-reviewer для анализа` |
| 135 | `subagent_type: captain-holt` | `subagent_type: meta-reviewer` |

##### 9.2. create-instruction.md

**Файл:** `.instructions/create-instruction.md`

| Строка | Было | Стало |
|--------|------|-------|
| 238 | `captain-holt` | `meta-reviewer` |
| 241 | `subagent_type: captain-holt` | `subagent_type: meta-reviewer` |
| 255 | `Агент captain-holt` | `Агент meta-reviewer` |
| 263 | `анализа captain-holt` | `анализа meta-reviewer` |
| 277 | `Анализ captain-holt` | `Анализ meta-reviewer` |
| 446 | `captain-holt` | `meta-reviewer` |
| 486 | `captain-holt` | `meta-reviewer` |

##### 9.3. modify-instruction.md

**Файл:** `.instructions/modify-instruction.md`

| Строка | Было | Стало |
|--------|------|-------|
| 133 | `captain-holt` | `meta-reviewer` |
| 136 | `subagent_type: captain-holt` | `subagent_type: meta-reviewer` |

#### 10. Пример в drafts

**Файл:** `.claude/drafts/examples/example-github-platform-research.md`

| Строка | Было | Стало |
|--------|------|-------|
| 1034 | `captain-holt` | `meta-reviewer` |
| 1036 | `Amy Santiago` | `meta-agent` |
| 1041 | `captain-holt` | `meta-reviewer` |
| 1043 | `captain-holt` | `meta-reviewer` |
| 1044 | `Amy` | `meta-agent` |
| 1053 | `Amy ... captain-holt` | `meta-agent ... meta-reviewer` |
| 1114 | `captain-holt` | `meta-reviewer` |

### Порядок выполнения

1. **Миграция captain-holt → meta-reviewer** — `/agent-modify` (тип: миграция)
2. **Миграция amy-santiago → meta-agent** — `/agent-modify` (тип: миграция)
3. **Обновить ссылки** в 8 файлах (секции 4–10 выше)
4. **Валидация** — `/agent-validate` для обоих агентов
5. **Коммит** — один коммит на всё переименование

### Риски

- **Скрипт `find-agent-refs.py`** — проверить, что он корректно находит новые имена
- **Claude Code settings** — `.claude/settings.local.json` может содержать ссылки (проверено — нет)
- **Кэш/state** — файлы `captain-holt-{timestamp}.json` в `.claude/state/` если существуют

### Чек-лист готовности

- [x] Папки переименованы
- [x] AGENT.md обоих агентов обновлены
- [x] CHANGELOG.md обоих агентов обновлены
- [x] Индекс агентов (README.md) обновлён
- [x] `.claude/README.md` обновлён
- [x] `.claude/CHANGELOG.md` обновлён
- [x] `standard-agent.md` обновлён
- [x] `validation-agent.md` обновлён
- [x] `standard-instruction.md` обновлён
- [x] `create-instruction.md` обновлён
- [x] `modify-instruction.md` обновлён
- [x] Пример в drafts обновлён
- [x] `/agent-validate` пройден для meta-agent
- [x] `/agent-validate` пройден для meta-reviewer
- [x] grep по проекту на старые имена — 0 результатов

### Tasklist

Задачи для исполнения через TaskCreate. Зависимости указаны в blockedBy.

```
TASK 1: Миграция captain-holt → meta-reviewer
  description: >
    Драфт: .claude/drafts/2026-02-25-rename-agents-meta.md (секция 2.2, 3.2)
    /agent-modify миграция captain-holt → meta-reviewer.
    Переименовать папку .claude/agents/captain-holt/ → .claude/agents/meta-reviewer/.
    Обновить AGENT.md: frontmatter name, description (убрать персонажа),
    роль (строка 18), state path (строка 157), CHANGELOG path (строка 270).
    Обновить CHANGELOG.md: заголовок, описание.
  activeForm: Мигрирую captain-holt → meta-reviewer

TASK 2: Миграция amy-santiago → meta-agent
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-25-rename-agents-meta.md (секция 2.1, 3.1)
    /agent-modify миграция amy-santiago → meta-agent.
    Переименовать папку .claude/agents/amy-santiago/ → .claude/agents/meta-agent/.
    Обновить AGENT.md: frontmatter name, description (убрать персонажа),
    роль (строки 37, 39), ссылка на Amy Santiago (строка 135),
    CHANGELOG path (строка 302), CHANGELOG format (строка 306).
    Обновить CHANGELOG.md: заголовок, описание, ссылку на Captain Holt → meta-reviewer.
  activeForm: Мигрирую amy-santiago → meta-agent

TASK 3: Обновить индекс и README агентов
  blockedBy: [1, 2]
  description: >
    Драфт: .claude/drafts/2026-02-25-rename-agents-meta.md (секции 4, 5, 6)
    Файлы:
    - .claude/.instructions/agents/README.md (строки 139-140): пути и имена агентов
    - .claude/README.md (строка 60): captain-holt → meta-reviewer, amy-santiago → meta-agent
    - .claude/CHANGELOG.md (строки 26, 72): Captain Holt → meta-reviewer, Amy Santiago → meta-agent
  activeForm: Обновляю индексы и README

TASK 4: Обновить стандарт и валидацию агентов
  blockedBy: [1, 2]
  description: >
    Драфт: .claude/drafts/2026-02-25-rename-agents-meta.md (секции 7, 8)
    Файлы:
    - .claude/.instructions/agents/standard-agent.md (строки 576, 577, 591, 599, 609):
      amy-santiago → meta-agent, captain-holt → meta-reviewer
    - .claude/.instructions/agents/validation-agent.md (строка 290):
      captain-holt → meta-reviewer
  activeForm: Обновляю стандарт агентов

TASK 5: Обновить инструкции по инструкциям
  blockedBy: [1, 2]
  description: >
    Драфт: .claude/drafts/2026-02-25-rename-agents-meta.md (секция 9)
    Файлы:
    - .instructions/standard-instruction.md (строки 123, 125, 132, 135):
      captain-holt → meta-reviewer
    - .instructions/create-instruction.md (строки 238, 241, 255, 263, 277, 446, 486):
      captain-holt → meta-reviewer
    - .instructions/modify-instruction.md (строки 133, 136):
      captain-holt → meta-reviewer
  activeForm: Обновляю инструкции

TASK 6: Обновить пример в drafts
  blockedBy: [1, 2]
  description: >
    Драфт: .claude/drafts/2026-02-25-rename-agents-meta.md (секция 10)
    Файл: .claude/drafts/examples/example-github-platform-research.md
    Строки 1034, 1036, 1041, 1043, 1044, 1053, 1114:
    captain-holt → meta-reviewer, Amy Santiago / Amy → meta-agent
  activeForm: Обновляю пример в drafts

TASK 7: Валидация и финальная проверка
  blockedBy: [3, 4, 5, 6]
  description: >
    Драфт: .claude/drafts/2026-02-25-rename-agents-meta.md (секция "Чек-лист готовности")
    1. /agent-validate для meta-agent
    2. /agent-validate для meta-reviewer
    3. grep -ri "amy-santiago|captain-holt" по проекту — ожидаем 0 результатов
       (исключая .claude/drafts/2026-02-25-rename-agents-meta.md — сам драфт)
    4. Отметить чек-лист готовности в драфте
  activeForm: Валидирую переименование
```
