---
type: project
description: Индекс скиллов, правила создания, параметры
related:
  - /.claude/agents/README.md
  - /.claude/instructions/tests/claude-testing.md
  - /.claude/instructions/tests/project-testing.md
---

# Индекс скиллов

Скиллы — команды для автоматизации повторяющихся задач.

## Правила

### Правило одного действия

Скилл выполняет **1 действие** над объектом:
- `create` — создание
- `update` — обновление
- `delete` — удаление

### Формат названия

```
{объект}-{действие}
```

Примеры: `skill-create`, `agent-update`, `doc-delete`

### Расположение

```
/.claude/skills/{название}/
    SKILL.md
```

---

## Категории

### skill-management

Управление скиллами.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [skill-create](./skill-create/SKILL.md) | Создание нового скилла | `/skill-create`, "создай скилл" |
| [skill-update](./skill-update/SKILL.md) | Обновление скиллов при добавлении нового | `/skill-update`, "обнови скиллы" |
| [skill-delete](./skill-delete/SKILL.md) | Обновление существующих скиллов при удалении скилла | `/skill-delete`, "удали скилл" |
| [skill-migrate](./skill-migrate/SKILL.md) | Переименование скилла с обновлением всех ссылок | `/skill-migrate`, "мигрируй скилл" |

### agent-management

Управление агентами.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [agent-create](./agent-create/SKILL.md) | Создание нового агента по шаблону | `/agent-create`, "создай агента" |

### instruction-management

Управление инструкциями.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [instruction-create](./instruction-create/SKILL.md) | Создание новой инструкции | `/instruction-create`, "создай инструкцию" |
| [instruction-update](./instruction-update/SKILL.md) | Проверка файлов на соответствие инструкции | `/instruction-update`, "проверь инструкцию" |
| [instruction-deactivate](./instruction-deactivate/SKILL.md) | Очистка ссылок при удалении инструкции | `/instruction-deactivate`, "удали инструкцию" |

### documentation

Работа с документацией.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [doc-create](./doc-create/SKILL.md) | Создание документации для файла в /src/ | `/doc-create`, "создай документацию" |
| [doc-update](./doc-update/SKILL.md) | Обновление документации при изменении кода | `/doc-update`, "обнови документацию" |
| [doc-delete](./doc-delete/SKILL.md) | Пометка документации при удалении файла | `/doc-delete`, "удали документацию" |
| [links-create](./links-create/SKILL.md) | Создание ссылок на файлы и папки | `/links-create`, "создай ссылки" |
| [links-update](./links-update/SKILL.md) | Обновление ссылок в связанных документах | `/links-update`, "обнови ссылки" |
| [links-delete](./links-delete/SKILL.md) | Пометка битых ссылок при удалении файлов | `/links-delete`, "удали ссылки" |
| [context-update](./context-update/SKILL.md) | Распространение контекста по графу документов | `/context-update`, "пошарь контекст" |
| [context-delete](./context-delete/SKILL.md) | Очистка контекста при удалении документа | `/context-delete`, "удали контекст" |
| [links-validate](./links-validate/SKILL.md) | Валидация всех ссылок в проекте | `/links-validate`, "проверь ссылки" |
| [doc-reindex](./doc-reindex/SKILL.md) | Полная переиндексация документации | `/doc-reindex`, "переиндексируй документацию" |

### meta

Мета-скиллы для улучшения работы с LLM.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [prompt-update](./prompt-update/SKILL.md) | Улучшение и обогащение промтов | `/prompt`, "улучши промт" |

### utility

Утилитарные микро-скиллы для переиспользования в других скиллах.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [input-validate](./input-validate/SKILL.md) | Валидация входных данных скилла | `/input-validate`, "проверь ввод" |
| [environment-check](./environment-check/SKILL.md) | Проверка окружения (gh, git, python) | `/environment-check`, "проверь окружение" |
| [health-check](./health-check/SKILL.md) | Проверка целостности проекта Claude | `/health-check`, "проверь проект" |

### testing

Тестирование скиллов и кода проекта.

> **SSOT:** Определение scope (claude/project) описано в [scope-detection.md](/.claude/instructions/shared/scope.md).

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [test-create](./test-create/SKILL.md) | Создание теста с автоопределением scope | `/test-create`, "создай тест" |
| [test-update](./test-update/SKILL.md) | Изменение существующего теста | `/test-update`, "обнови тест" |
| [test-review](./test-review/SKILL.md) | Проверка полноты и качества теста | `/test-review`, "проверь тест" |
| [test-execute](./test-execute/SKILL.md) | Выполнение тестов с автоопределением scope | `/test-execute`, "запусти тест" |
| [test-complete](./test-complete/SKILL.md) | Отметка теста как пройденного | `/test-complete`, "тест пройден" |
| [test-delete](./test-delete/SKILL.md) | Удаление теста | `/test-delete`, "удали тест" |
| [test-coverage](./test-coverage/SKILL.md) | Анализ покрытия тестами | `/test-coverage`, "покрытие тестами" |

### git

Git операции.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [issue-create](./issue-create/SKILL.md) | Создание GitHub Issue с правильным форматом | `/issue-create`, "создай задачу" |
| [issue-update](./issue-update/SKILL.md) | Обновление описания и меток Issue | `/issue-update`, "обнови задачу" |
| [issue-execute](./issue-execute/SKILL.md) | Взятие Issue в работу и выполнение | `/issue-execute`, "возьми задачу" |
| [issue-review](./issue-review/SKILL.md) | Ревью решения перед закрытием Issue | `/issue-review`, "проверь решение" |
| [issue-complete](./issue-complete/SKILL.md) | Закрытие Issue как выполненного | `/issue-complete`, "заверши задачу" |
| [issue-delete](./issue-delete/SKILL.md) | Закрытие Issue как неактуального | `/issue-delete`, "удали задачу" |
| [issue-reopen](./issue-reopen/SKILL.md) | Переоткрытие закрытого Issue | `/issue-reopen`, "переоткрой задачу" |

### specs

Работа с документами спецификаций /specs/.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [spec-create](./spec-create/SKILL.md) | Создание документов /specs/ (Discussion, Impact, ADR, Plan) | `/spec-create`, "создай спецификацию" |
| [spec-status](./spec-status/SKILL.md) | Изменение статуса документа /specs/ | `/spec-status`, "статус спецификации" |
| [spec-update](./spec-update/SKILL.md) | Работа с документом /specs/ | `/spec-update`, "обнови спецификацию" |
| [specs-health](./specs-health/SKILL.md) | Проверка целостности /specs/ | `/specs-health`, "проверь спецификации" |
| [specs-sync](./specs-sync/SKILL.md) | Синхронизация каскадных статусов | `/specs-sync`, "синхронизируй статусы" |
| [specs-index](./specs-index/SKILL.md) | Обновление индексов README.md в /specs/ | `/specs-index`, "обнови индексы" |

### glossary

Работа с глоссарием /specs/glossary.md.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [glossary-candidates](./glossary-candidates/SKILL.md) | Поиск терминов-кандидатов в документе | `/glossary-candidates`, "найди термины" |
| [glossary-review](./glossary-review/SKILL.md) | Интерактивная обработка кандидатов | `/glossary-review`, "проверь термины" |
| [glossary-link](./glossary-link/SKILL.md) | Добавление ссылок на глоссарий в документы | `/glossary-link`, "расставь ссылки" |

---

## Справочник allowed-tools

| Инструмент | Описание |
|------------|----------|
| `Bash` | Выполнение команд в терминале |
| `Read` | Чтение файлов |
| `Write` | Создание файлов |
| `Edit` | Редактирование файлов |
| `Glob` | Поиск файлов по паттерну |
| `Grep` | Поиск в содержимом файлов |
| `WebFetch` | HTTP запросы к URL |
| `WebSearch` | Поиск в интернете |
| `Task` | Запуск подзадач (агентов) |

---

## Добавление нового скилла

Используй команду `/skill-create` или скажи "создай скилл".

---

## Стандарт параметров

Единообразие параметров скиллов для предсказуемого поведения.

### Общие флаги

| Флаг | Описание | Тип | Пример |
|------|----------|-----|--------|
| `--dry-run` | Показать план без выполнения | boolean | `--dry-run` |
| `--auto` | Автоматический режим без подтверждений | boolean | `--auto` |
| `--json` | Вывод в JSON формате (для CI/скриптов) | boolean | `--json` |
| `--verbose` | Подробный вывод с деталями | boolean | `--verbose` |
| `--depth N` | Глубина обхода связей (по умолчанию 1) | number | `--depth 2` |
| `--diff` | Показать diff изменений | boolean | `--diff` |
| `--no-issue` | Не создавать/не связывать Issue | boolean | `--no-issue` |

### Правила использования

**Правило:** Все скиллы должны поддерживать `--dry-run` для предварительного просмотра.

**Правило:** Флаги с отрицанием начинаются с `--no-` (например, `--no-issue`).

**Правило:** Числовые параметры указываются после имени через пробел (`--depth 2`).

### Совместимость флагов

| Комбинация | Результат |
|------------|-----------|
| `--dry-run --auto` | Показать план (auto игнорируется) |
| `--depth 0` | Без рекурсивного обхода |
| `--diff --dry-run` | Показать предполагаемые изменения |
| `--json --verbose` | JSON с расширенными полями |
| `--json --dry-run` | JSON с планом изменений |

---

## Автоматизация

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| [/skill-create](./skill-create/SKILL.md) | Создание нового скилла по шаблону |
| [/skill-update](./skill-update/SKILL.md) | Обновление существующих скиллов при добавлении нового |
| [/skill-delete](./skill-delete/SKILL.md) | Удаление скилла и обновление связей |

---

## FAQ / Troubleshooting

### Что делать при конфликте между скиллами?

**Симптом:** Два скилла пытаются изменить один файл, или один скилл отменяет изменения другого.

**Причины:**

| Причина | Пример | Решение |
|---------|--------|---------|
| Перекрытие зон ответственности | `doc-update` и `links-update` оба обновляют README | Вызывать последовательно, а не параллельно |
| Конкурентные изменения | `skill-update` A обновляет skills.md, пока `skill-update` B тоже его меняет | Не запускать одинаковые скиллы параллельно |
| Циклическая зависимость | A вызывает B, B вызывает A | Переструктурировать воркфлоу |

**Решение:**

1. **Определить конфликт:**
   ```
   ⚠️ Конфликт: файл skills.md изменён другим процессом

   Варианты:
   [1] Перезагрузить файл и повторить
   [2] Принудительно записать мои изменения
   [3] Отменить
   ```

2. **Предотвращение:**
   - Вызывать связанные скиллы последовательно через воркфлоу
   - Не запускать один скилл несколько раз параллельно
   - Использовать `--dry-run` для проверки перед выполнением

3. **При обнаружении цикла:**
   ```
   ❌ Обнаружен цикл: skill-update → instruction-update → skill-update

   Решение: Один из скиллов должен НЕ вызывать другой.
   Проверьте воркфлоу обоих скиллов.
   ```

### Как добавить новую категорию скиллов?

**Шаг 1:** Убедиться, что категория действительно нужна

Категория нужна если:
- Есть 2+ скиллов с общей темой
- Скиллы не подходят в существующие категории
- Категория имеет понятное название

**Шаг 2:** Добавить категорию в README.md

1. Открыть этот файл (`/.claude/skills/README.md`)
2. Найти раздел `## Категории`
3. Добавить новую секцию в алфавитном порядке:

```markdown
### {category-name}

{Описание категории — 1 строка.}

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| — | — | — |
```

**Шаг 3:** Обновить связанные скиллы

1. В `/skill-create/SKILL.md` добавить категорию в список доступных
2. В каждом скилле категории указать `category: {category-name}` в frontmatter

**Шаг 4:** Создать скиллы для категории

```
/skill-create {object}-create
/skill-create {object}-update
/skill-create {object}-delete
```

**Пример:**

Добавление категории `ci-management`:

```markdown
### ci-management

Управление CI/CD pipeline.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [ci-check](./ci-check/SKILL.md) | Проверка статуса CI | `/ci-check`, "проверь CI" |
| [ci-fix](./ci-fix/SKILL.md) | Исправление ошибок CI | `/ci-fix`, "исправь CI" |
```

**Именование категорий:**

| Формат | Пример | Описание |
|--------|--------|----------|
| `{object}-management` | `skill-management` | Управление объектами |
| `{domain}` | `git`, `testing` | Доменная область |
| `{action}-{object}` | Не рекомендуется | Лучше использовать `{object}-management` |

---

## Связанные инструкции

- [agents/README.md](/.claude/agents/README.md) — индекс агентов
- [instructions/tests/claude-testing.md](/.claude/instructions/tests/claude-testing.md) — тестирование Claude Code
- [instructions/tests/project-testing.md](/.claude/instructions/tests/project-testing.md) — тестирование проекта
