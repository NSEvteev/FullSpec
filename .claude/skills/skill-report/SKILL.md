---
name: skill-report
description: Генерация отчёта по скиллам проекта
allowed-tools: Read, Glob, Grep
category: skill-management
triggers:
  commands:
    - /skill-report
  phrases:
    ru:
      - отчёт по скиллам
      - статистика скиллов
    en:
      - skill report
      - skills statistics
---

# Отчёт по скиллам

Команда для генерации аналитического отчёта по всем скиллам проекта.

**Связанные скиллы:**
- [skill-create](/.claude/skills/skill-create/SKILL.md) — создание скиллов
- [test-coverage](/.claude/skills/test-coverage/SKILL.md) — покрытие тестами
- [health-check](/.claude/skills/health-check/SKILL.md) — проверка проекта

**Связанные инструкции:**
- [skills/README.md](/.claude/skills/README.md) — индекс скиллов

## Оглавление

- [Формат вызова](#формат-вызова)
- [Метрики отчёта](#метрики-отчёта)
- [Воркфлоу](#воркфлоу)
- [Формат вывода](#формат-вывода)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/skill-report [--json] [--verbose] [--category <name>]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--json` | Вывод в JSON формате | false |
| `--verbose` | Подробный вывод по каждому скиллу | false |
| `--category` | Фильтр по категории | все |

---

## Метрики отчёта

### Общие метрики

| Метрика | Описание |
|---------|----------|
| `total_skills` | Общее количество скиллов |
| `categories_count` | Количество категорий |
| `skills_with_tests` | Скиллы с файлом tests.md |
| `avg_tests_per_skill` | Среднее число тестов на скилл |

### По категориям

| Метрика | Описание |
|---------|----------|
| `category_name` | Название категории |
| `skills_count` | Количество скиллов в категории |
| `skills_list` | Список скиллов |

### По скиллам (--verbose)

| Метрика | Описание |
|---------|----------|
| `name` | Название скилла |
| `category` | Категория |
| `has_tests` | Есть ли tests.md |
| `test_cases_count` | Количество тест-кейсов |
| `triggers_count` | Количество триггеров |
| `dependencies` | Связанные скиллы |

---

## Воркфлоу

### Шаг 1: Сбор данных

```bash
# Найти все скиллы
ls .claude/skills/*/SKILL.md
```

### Шаг 2: Парсинг frontmatter

Для каждого скилла извлечь:
- `name`
- `description`
- `category`
- `triggers`

### Шаг 3: Анализ тестов

```bash
# Для каждого скилла
ls .claude/skills/{skill}/tests.md

# Подсчитать тест-кейсы (паттерн "## TC-")
grep -c "^## TC-" .claude/skills/{skill}/tests.md
```

### Шаг 4: Анализ связей

Найти упоминания скиллов друг в друге:
- Раздел "Связанные скиллы"
- Вызовы в воркфлоу

### Шаг 5: Формирование отчёта

Сгруппировать по категориям, вычислить метрики.

---

## Формат вывода

### Стандартный вывод

```
📊 Отчёт по скиллам

═══════════════════════════════════════════════════════
ОБЩАЯ СТАТИСТИКА
═══════════════════════════════════════════════════════

Скиллов всего:        37
Категорий:            8
С тестами:            37 (100%)
Тест-кейсов:          148
Среднее тестов/скилл: 4.0

═══════════════════════════════════════════════════════
ПО КАТЕГОРИЯМ
═══════════════════════════════════════════════════════

skill-management (4):
  • skill-create, skill-update, skill-delete, skill-migrate

agent-management (1):
  • agent-create

instruction-management (3):
  • instruction-create, instruction-update, instruction-delete

documentation (10):
  • doc-create, doc-update, doc-delete, links-create,
    links-update, links-delete, context-update,
    context-delete, links-validate, doc-reindex

testing (7):
  • test-create, test-update, test-review, test-execute,
    test-complete, test-delete, test-coverage

git (7):
  • issue-create, issue-update, issue-execute, issue-review,
    issue-complete, issue-delete, issue-reopen

utility (3):
  • input-validate, environment-check, health-check

meta (1):
  • prompt-update

═══════════════════════════════════════════════════════
РЕКОМЕНДАЦИИ
═══════════════════════════════════════════════════════

✅ Все скиллы имеют тесты
⚠️ Категория agent-management: только 1 скилл (рассмотреть agent-update, agent-delete)
```

### JSON вывод (--json)

```json
{
  "summary": {
    "total_skills": 37,
    "categories_count": 8,
    "skills_with_tests": 37,
    "test_cases_total": 148,
    "avg_tests_per_skill": 4.0
  },
  "categories": [
    {
      "name": "skill-management",
      "count": 4,
      "skills": ["skill-create", "skill-update", "skill-delete", "skill-migrate"]
    },
    {
      "name": "agent-management",
      "count": 1,
      "skills": ["agent-create"]
    }
  ],
  "recommendations": [
    {
      "type": "warning",
      "message": "Категория agent-management: только 1 скилл"
    }
  ]
}
```

### Verbose вывод (--verbose)

Добавляет детализацию по каждому скиллу:

```
📋 skill-create
   Категория: skill-management
   Описание: Создание нового скилла по шаблону
   Тесты: 6 тест-кейсов
   Триггеры: /skill-create, "создай скилл"
   Связи: skill-update, skill-delete, links-update
```

---

## Примеры использования

### Пример 1: Быстрый обзор

**Вызов:**
```
/skill-report
```

**Результат:**
Общая статистика и группировка по категориям.

### Пример 2: Фильтр по категории

**Вызов:**
```
/skill-report --category git
```

**Результат:**
```
📊 Категория: git

Скиллов: 7
  • issue-create (6 тестов)
  • issue-update (5 тестов)
  • issue-execute (6 тестов)
  • issue-review (5 тестов)
  • issue-complete (6 тестов)
  • issue-delete (5 тестов)
  • issue-reopen (5 тестов)

Всего тестов: 38
```

### Пример 3: JSON для CI/скриптов

**Вызов:**
```
/skill-report --json
```

**Использование:**
```bash
# Получить количество скиллов
/skill-report --json | jq '.summary.total_skills'
```

### Пример 4: Детальный анализ

**Вызов:**
```
/skill-report --verbose --category testing
```

**Результат:**
Подробная информация по каждому скиллу категории testing.

---

## FAQ

### Как найти скиллы без тестов?

```
/skill-report --verbose | grep "Тесты: 0"
```

Или используйте `/test-coverage claude`.

### Как узнать самые используемые скиллы?

В `--verbose` режиме показаны связи. Скиллы с большим количеством связей — наиболее используемые (например, `links-update`).

### Как добавить новую категорию в отчёт?

Категории определяются автоматически из frontmatter скиллов. Добавьте скилл с новой категорией — она появится в отчёте.
