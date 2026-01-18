# Инструкция по скиллам Claude Code

**Связанные документы:**
- [llm_instructions.md](llm_instructions.md) — индекс инструкций
- [agents.md](agents.md) — агенты (скиллы можно привязать к агентам)
- [CLAUDE.md](../CLAUDE.md) — краткие инструкции для Claude

---

## Назначение

Папка `.claude/skills/` содержит скиллы — Markdown-файлы с инструкциями для Claude по выполнению конкретных задач.

## Структура

```
.claude/
└── skills/
    └── [имя-скилла]/
        ├── SKILL.md            # Основной файл скилла (обязательно)
        ├── [доп-файлы].md      # Вспомогательные инструкции
        └── scripts/            # Утилиты скилла
```

## Что такое скилл

**[📖 Скилл](../general_docs/glossary.md#скилл)** — набор инструкций, которые учат Claude выполнять конкретную задачу. [📖 Скиллы](../general_docs/glossary.md#скилл) работают в основной беседе и автоматически срабатывают по описанию.

### Отличия от [📖 агентов](../general_docs/glossary.md#агент)

| Аспект | [📖 Скиллы](../general_docs/glossary.md#скилл) | [📖 Агенты](../general_docs/glossary.md#агент) |
|--------|--------|--------|
| Контекст | Основная беседа | Отдельный (изолированный) |
| Срабатывание | Автоматическое по description | Явный вызов |
| Применение | Методологии, стандарты | Сложные многошаговые задачи |

## Формат файла SKILL.md

```yaml
---
name: имя-скилла
description: Описание скилла и когда его использовать.
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Название скилла

## Инструкции

Пошаговые действия для выполнения задачи.

## Примеры

Примеры использования.
```

### Обязательные поля

| Поле | Описание |
|------|----------|
| `name` | Уникальное имя (строчные буквы, дефисы, до 64 символов) |
| `description` | Описание назначения (до 1024 символов) |

### Опциональные поля

| Поле | Описание |
|------|----------|
| `allowed-tools` | Инструменты без подтверждения |
| `model` | Модель: `haiku`, `sonnet`, `opus` |
| `context` | `fork` — запуск в отдельном контексте |
| `agent` | Тип агента при `context: fork` |
| `hooks` | Хуки жизненного цикла |
| `user-invocable` | Показывать в меню (по умолчанию `true`) |

## Расположение скиллов

| Тип | Путь | Применение |
|-----|------|------------|
| Проектный | `.claude/skills/` | Для команды в репозитории |
| Персональный | `~/.claude/skills/` | Для всех проектов пользователя |

## Вызов скилла

```bash
# Автоматически (по description)
Напиши commit-сообщение для изменений

# Явно через [📖 слэш-команду](../general_docs/glossary.md#слэш-команда)
/имя-скилла

# Проверка доступных скиллов
Какие скиллы доступны?
```

## Связь с [📖 агентами](../general_docs/glossary.md#агент)

[📖 Скиллы](../general_docs/glossary.md#скилл) можно привязать к [📖 агенту](../general_docs/glossary.md#агент) через поле `skills` в файле агента:

```yaml
---
name: code-reviewer
skills: coding-standards, security-checklist
---
```

Содержимое [📖 скиллов](../general_docs/glossary.md#скилл) инжектируется в контекст [📖 агента](../general_docs/glossary.md#агент) при запуске.

## Добавление нового [📖 скилла](../general_docs/glossary.md#скилл)

При создании нового [📖 скилла](../general_docs/glossary.md#скилл):

1. Создать папку `.claude/skills/[имя-скилла]/`
2. Создать файл `SKILL.md` с frontmatter
3. Написать инструкции и примеры
4. Указать минимально необходимые `allowed-tools`
5. Добавить вспомогательные файлы (если нужно)
6. Добавить описание скилла в этот файл
7. **Проверить, нужен ли скилл каким-либо агентам** — обновить поле `skills` в конфигурации агента

**ВАЖНО для скиллов документации:**
- Все новые скиллы с префиксом `doc-*` или `glossary-*` **обязательно назначать агенту amy-santiago**
- Обновить файл `.claude/agents/amy-santiago.md` — добавить скилл в поле `skills`
- Обновить таблицу в `agents.md` — добавить скилл в колонку "Скиллы" для amy-santiago
- Обновить таблицу "Скиллы проекта" в этом файле — указать `amy-santiago` в колонке "Используется в агентах"

## Добавление нового [📖 агента](../general_docs/glossary.md#агент)

**ВАЖНО:** При создании нового [📖 агента](../general_docs/glossary.md#агент) **всегда проверяй** доступные скиллы и назначай релевантные:

1. Проанализировать назначение агента
2. Просмотреть список доступных скиллов в `.claude/skills/`
3. Определить, какие скиллы помогут агенту в его задачах
4. Добавить в frontmatter агента поле `skills: skill-1, skill-2, skill-3`
5. Обновить документацию агента (таблицу в `agents.md`)

**Примеры назначения скиллов:**
- **Documentation Manager** → doc-health, doc-claude, doc-project-structure, glossary-*
- **Code Reviewer** → coding-standards, security-checklist
- **Release Manager** → commit-push, changelog-update

## Скиллы проекта

| Имя | Назначение | Инструменты | Используется в агентах |
|-----|------------|-------------|------------------------|
| discussion | Управление дискуссиями — создание, изменение, удаление. ОБЯЗАТЕЛЬНО сверяться с этим скиллом при любых действиях с файлами в general_docs/01_discuss/ | Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion | amy-santiago |
| discussion-review | Ревью выбранного решения в дискуссии. Анализирует, что пользователь СМОЖЕТ и НЕ СМОЖЕТ сделать при выборе варианта. Вызывается после выбора варианта, переводит дискуссию из in_progress в review | Read, Grep, Glob, AskUserQuestion, Edit | amy-santiago |
| summary-doc | Обновление 000_SUMMARY.md дискуссий при переходе в approved. Агрегирует принятые решения для контекста архитектуры | Read, Edit, Grep | amy-santiago |
| summary-arch | Обновление 000_SUMMARY.md архитектуры при переходе в статус approved. Агрегирует архитектурные решения для контекста при создании ADR. Вызывается после ревью архитектуры | Read, Edit, Grep | amy-santiago |
| architect | Создание архитектурного документа из одобренной дискуссии. Читает SUMMARY + дискуссию для полного контекста. Вызывается после /summary-doc, затем переводит дискуссию в final | Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion | amy-santiago |
| architect-review | Ревью архитектуры перед созданием ADR. Анализирует полноту компонентов, зависимости, риски. Вызывается после заполнения архитектуры, переводит из in_progress в review, затем в approved | Read, Edit, Grep, Glob, AskUserQuestion | amy-santiago |
| commit-push | Коммит и пуш с правильным форматированием сообщений | Bash, Read | — |
| doc-claude | Обновление CLAUDE.md и llm_instructions.md при важных изменениях | Read, Edit, Bash | amy-santiago |
| doc-health | Проверка здоровья документации — ссылки, структура, статусы, метаданные | Bash | amy-santiago |
| doc-health-deep | Глубокий смысловой аудит документации с автогенерацией задач на исправление | Read, Edit, Write, Grep, Glob, Bash, AskUserQuestion | amy-santiago |
| doc-review | **Глубокое ревью** — критический анализ, поиск упущений, автоулучшение. При создании документа — улучшения автоматически. При явном вызове — с подтверждением. Триггеры: "уделить внимание", "подумать", "ревью", "ультрасинк" | Read, Grep, Glob, AskUserQuestion, Edit | amy-santiago |
| doc-project-structure | Генерация структуры проекта и обновление в llm_instructions.md и README.md | Glob, Read, Edit, Bash | amy-santiago |
| glossary-candidates | Поиск специфичных терминов в документе и добавление в кандидаты глоссария | Read, Edit, Glob | amy-santiago |
| glossary-link | Добавление ссылок на глоссарий во все .md файлы проекта | Read, Edit, Glob, Grep | amy-santiago |
| glossary-review | Интерактивная обработка кандидатов в глоссарий | Read, Edit, AskUserQuestion, Grep | amy-santiago |
| task-documentation | Автоматическое документирование завершённых задач — обновление связанных документов | Read, Edit, Write, Grep, Glob | amy-santiago |
| decision | Создание ADR (Architecture Decision Record) из одобренной архитектуры. ADR затем создаёт ресурсы и планы реализации | Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion | amy-santiago |
| resource | Создание ресурса (database, backend, frontend, infra) из одобренного ADR. Ресурсы описывают конкретные технические компоненты системы | Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion | amy-santiago |
| imp-plan | Создание плана реализации из одобренного ADR. План содержит фазы, задачи и критерии готовности для реализации решения | Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion | amy-santiago |
| doc-delete | Безопасное удаление документа с созданием задачи на актуализацию связей. Находит зависимые документы и создаёт задачу для их обновления | Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion | amy-santiago |
| feedback | Отслеживание изменений по цепочке зависимостей. При изменении документа определяет, какие связанные документы нужно обновить | Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion | amy-santiago |