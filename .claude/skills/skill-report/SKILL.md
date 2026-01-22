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
      - покажи скиллы
      - сколько скиллов
    en:
      - skill report
      - skills statistics
      - show skills
      - list skills
---

# Отчёт по скиллам

Команда для генерации аналитического отчёта по всем скиллам проекта. Собирает статистику, группирует по категориям, анализирует покрытие тестами и выдаёт рекомендации.

**Связанные скиллы:**
- [skill-create](/.claude/skills/skill-create/SKILL.md) — создание скиллов
- [skill-update](/.claude/skills/skill-update/SKILL.md) — обновление скиллов
- [skill-delete](/.claude/skills/skill-delete/SKILL.md) — удаление скиллов
- [skill-migrate](/.claude/skills/skill-migrate/SKILL.md) — переименование скиллов
- [test-coverage](/.claude/skills/test-coverage/SKILL.md) — покрытие тестами
- [health-check](/.claude/skills/health-check/SKILL.md) — проверка проекта

**Связанные инструкции:**
- [skills/README.md](/.claude/skills/README.md) — индекс скиллов

**Шаблоны:**
- [output-formats.md](/.claude/instructions/skills/output.md) — форматы вывода (SSOT)

## Оглавление

- [Формат вызова](#формат-вызова)
- [Метрики отчёта](#метрики-отчёта)
- [Воркфлоу](#воркфлоу)
  - [Шаг 0: Проверка окружения](#шаг-0-проверка-окружения)
  - [Шаг 1: Сбор данных](#шаг-1-сбор-данных)
  - [Шаг 2: Парсинг frontmatter](#шаг-2-парсинг-frontmatter)
  - [Шаг 3: Анализ тестов](#шаг-3-анализ-тестов)
  - [Шаг 4: Анализ связей](#шаг-4-анализ-связей)
  - [Шаг 5: Формирование рекомендаций](#шаг-5-формирование-рекомендаций)
  - [Шаг 6: Проверка по чек-листу](#шаг-6-проверка-по-чек-листу)
  - [Шаг 7: Вывод отчёта](#шаг-7-вывод-отчёта)
- [Формат вывода](#формат-вывода)
- [Обработка ошибок](#обработка-ошибок)
- [Чек-лист](#чек-лист)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Следующие шаги](#следующие-шаги)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/skill-report [--json] [--verbose] [--category <name>] [--no-recommendations]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--json` | Вывод в JSON формате | false |
| `--verbose` | Подробный вывод по каждому скиллу | false |
| `--category` | Фильтр по категории | все |
| `--no-recommendations` | Скрыть раздел рекомендаций | false |

**Примеры:**
- `/skill-report` — стандартный отчёт
- `/skill-report --verbose` — с деталями по каждому скиллу
- `/skill-report --category git` — только git-скиллы
- `/skill-report --json` — для CI/скриптов

---

## Метрики отчёта

### Общие метрики

| Метрика | Описание | Как вычисляется |
|---------|----------|-----------------|
| `total_skills` | Общее количество скиллов | Подсчёт папок в `/.claude/skills/` |
| `categories_count` | Количество категорий | Уникальные значения `category` из frontmatter |
| `skills_with_tests` | Скиллы с файлом tests.md | Проверка наличия `tests.md` в папке скилла |
| `test_coverage_percent` | Процент покрытия тестами | `skills_with_tests / total_skills * 100` |
| `avg_tests_per_skill` | Среднее число тестов на скилл | Сумма тест-кейсов / кол-во скиллов с тестами |
| `critical_skills` | Количество критичных скиллов | Скиллы с `critical: true` в frontmatter |

### По категориям

| Метрика | Описание |
|---------|----------|
| `category_name` | Название категории |
| `skills_count` | Количество скиллов в категории |
| `skills_list` | Список скиллов |
| `test_coverage` | Процент покрытия тестами в категории |

### По скиллам (--verbose)

| Метрика | Описание |
|---------|----------|
| `name` | Название скилла |
| `category` | Категория |
| `description` | Описание скилла |
| `critical` | Критичность (true/false) |
| `has_tests` | Есть ли tests.md |
| `test_cases_count` | Количество тест-кейсов |
| `triggers_count` | Количество триггеров |
| `dependencies` | Связанные скиллы |
| `file_size` | Размер SKILL.md в строках |

---

## Воркфлоу

### Шаг 0: Проверка окружения

1. Проверить наличие папки `/.claude/skills/`
2. Проверить наличие индекса [skills/README.md](/.claude/skills/README.md)

**Если папка не существует:**
```
❌ Папка /.claude/skills/ не найдена

Создайте структуру скиллов:
mkdir -p .claude/skills
```

### Шаг 1: Сбор данных

**Найти все скиллы:**
```
Glob: /.claude/skills/*/SKILL.md
```

**Результат:** список путей к SKILL.md файлам

**Пример:**
```
Найдено 37 скиллов:
/.claude/skills/skill-create/SKILL.md
/.claude/skills/skill-update/SKILL.md
...
```

### Шаг 2: Парсинг frontmatter

Для каждого скилла извлечь из frontmatter:

| Поле | Обязательное | По умолчанию |
|------|--------------|--------------|
| `name` | Да | — |
| `description` | Да | — |
| `category` | Да | — |
| `critical` | Нет | false |
| `triggers.commands` | Да | — |
| `triggers.phrases` | Нет | [] |
| `allowed-tools` | Нет | [] |

**Алгоритм:**
1. Прочитать SKILL.md
2. Извлечь YAML между `---` и `---`
3. Распарсить поля
4. Валидировать обязательные поля

**При ошибке парсинга:**
```
⚠️ Ошибка парсинга: /.claude/skills/broken-skill/SKILL.md
   Причина: Некорректный YAML на строке 5
   Скилл пропущен в отчёте
```

### Шаг 3: Анализ тестов

Для каждого скилла:

1. Проверить наличие `tests.md`:
   ```
   Glob: /.claude/skills/{skill}/tests.md
   ```

2. Если файл существует — подсчитать тест-кейсы:
   ```
   Grep: "^## TC-" в tests.md
   ```

**Структура результата:**
```json
{
  "skill-create": {
    "has_tests": true,
    "test_cases": 6
  },
  "skill-update": {
    "has_tests": true,
    "test_cases": 5
  }
}
```

### Шаг 4: Анализ связей

Найти связи между скиллами:

1. **Явные связи** — раздел "Связанные скиллы" в SKILL.md:
   ```
   Grep: "\[.*\]\(/.claude/skills/.*/SKILL.md\)" в SKILL.md
   ```

2. **Вызовы в воркфлоу** — упоминания других скиллов:
   ```
   Grep: "/[a-z]+-[a-z]+" в SKILL.md
   ```

**Результат:**
```json
{
  "skill-create": {
    "depends_on": ["skill-update", "links-update"],
    "used_by": ["agent-create", "instruction-create"]
  }
}
```

### Шаг 5: Формирование рекомендаций

На основе собранных данных сформировать рекомендации:

**Типы рекомендаций:**

| Тип | Условие | Рекомендация |
|-----|---------|--------------|
| 🔴 Критично | Скилл без тестов + `critical: true` | Добавить тесты |
| 🔴 Критично | Категория с 1 скиллом типа `*-create` | Создать `*-update`, `*-delete` |
| 🟡 Рекомендуется | Скилл без тестов | Добавить тесты |
| 🟡 Рекомендуется | Много скиллов без явных связей | Добавить связи |
| 🟢 Info | Категория с > 10 скиллами | Рассмотреть разделение |

**Алгоритм:**
```
1. Для каждой категории:
   - Проверить полноту (create/update/delete)
   - Проверить покрытие тестами

2. Для каждого скилла:
   - Проверить наличие тестов
   - Проверить количество связей
   - Если critical — приоритет выше
```

### Шаг 6: Проверка по чек-листу

Перед выводом проверить:

```
✅ Шаг 1: Собраны данные о скиллах
✅ Шаг 2: Распарсены frontmatter всех скиллов
✅ Шаг 3: Проанализированы тесты
✅ Шаг 4: Проанализированы связи
✅ Шаг 5: Сформированы рекомендации
```

### Шаг 7: Вывод отчёта

В зависимости от флагов вывести отчёт в нужном формате.

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
Критичных:            12
Тест-кейсов:          148
Среднее тестов/скилл: 4.0

═══════════════════════════════════════════════════════
ПО КАТЕГОРИЯМ
═══════════════════════════════════════════════════════

skill-management (4):
  • skill-create, skill-update, skill-delete, skill-migrate
  • Тесты: 4/4 (100%)

agent-management (1):
  • agent-create
  • Тесты: 1/1 (100%)
  ⚠️ Нет agent-update, agent-delete

instruction-management (3):
  • instruction-create, instruction-update, instruction-deactivate
  • Тесты: 3/3 (100%)

documentation (10):
  • doc-create, doc-update, doc-delete, links-create,
    links-update, links-delete, context-update,
    context-delete, links-validate, doc-reindex
  • Тесты: 10/10 (100%)

testing (7):
  • test-create, test-update, test-review, test-execute,
    test-complete, test-delete, test-coverage
  • Тесты: 7/7 (100%)

git (7):
  • issue-create, issue-update, issue-execute, issue-review,
    issue-complete, issue-delete, issue-reopen
  • Тесты: 7/7 (100%)

utility (3):
  • input-validate, environment-check, health-check
  • Тесты: 3/3 (100%)

meta (1):
  • prompt-update
  • Тесты: 1/1 (100%)

═══════════════════════════════════════════════════════
РЕКОМЕНДАЦИИ
═══════════════════════════════════════════════════════

🟡 Рекомендуется:
1. agent-management: создать agent-update, agent-delete для полноты

🟢 Информация:
2. documentation: 10 скиллов — крупнейшая категория
```

### JSON вывод (--json)

```json
{
  "generated_at": "2026-01-20T10:30:00Z",
  "summary": {
    "total_skills": 37,
    "categories_count": 8,
    "skills_with_tests": 37,
    "test_coverage_percent": 100,
    "test_cases_total": 148,
    "avg_tests_per_skill": 4.0,
    "critical_skills": 12
  },
  "categories": [
    {
      "name": "skill-management",
      "count": 4,
      "skills": ["skill-create", "skill-update", "skill-delete", "skill-migrate"],
      "test_coverage": 100,
      "completeness": "full"
    },
    {
      "name": "agent-management",
      "count": 1,
      "skills": ["agent-create"],
      "test_coverage": 100,
      "completeness": "partial",
      "missing": ["agent-update", "agent-delete"]
    }
  ],
  "skills": [
    {
      "name": "skill-create",
      "category": "skill-management",
      "description": "Создание нового скилла по шаблону",
      "critical": false,
      "has_tests": true,
      "test_cases": 6,
      "triggers_count": 7,
      "dependencies": ["skill-update", "links-update"]
    }
  ],
  "recommendations": [
    {
      "type": "warning",
      "category": "agent-management",
      "message": "Создать agent-update, agent-delete для полноты"
    }
  ]
}
```

### Verbose вывод (--verbose)

Добавляет детализацию по каждому скиллу:

```
═══════════════════════════════════════════════════════
ДЕТАЛИ ПО СКИЛЛАМ
═══════════════════════════════════════════════════════

📋 skill-create
   Категория:   skill-management
   Описание:    Создание нового скилла по шаблону
   Критичный:   Нет
   Тесты:       6 тест-кейсов
   Триггеры:    /skill-create, "создай скилл", "новый скилл"
   Зависит от:  skill-update, links-update, context-update
   Используют:  agent-create, instruction-create
   Размер:      841 строка

📋 skill-update
   Категория:   skill-management
   Описание:    Обновление существующих скиллов
   Критичный:   Нет
   Тесты:       5 тест-кейсов
   Триггеры:    /skill-update, "обнови скилл"
   Зависит от:  links-update
   Используют:  skill-create
   Размер:      320 строк
```

### Фильтр по категории (--category)

```
/skill-report --category git
```

```
📊 Категория: git

Скиллов: 7
Тест-кейсов: 38
Покрытие: 100%

Скиллы:
  • issue-create (6 тестов) — Создание GitHub Issue
  • issue-update (5 тестов) — Обновление GitHub Issue
  • issue-execute (6 тестов) — Взятие Issue в работу
  • issue-review (5 тестов) — Ревью решения перед закрытием
  • issue-complete (6 тестов) — Закрытие Issue как выполненного
  • issue-delete (5 тестов) — Закрытие Issue как неактуального
  • issue-reopen (5 тестов) — Переоткрытие закрытого Issue

Связи внутри категории:
  issue-create → issue-execute → issue-review → issue-complete
                              ↘ issue-update
                                issue-delete
                                issue-reopen
```

---

## Обработка ошибок

> **SSOT:** [error-handling.md](/.claude/instructions/skills/errors.md)

| Ошибка | Действие |
|--------|----------|
| Папка skills/ не найдена | Сообщить, предложить создать |
| Нет ни одного скилла | Сообщить: "Скиллы не найдены" |
| Ошибка парсинга frontmatter | Предупредить, пропустить скилл |
| Категория не найдена (--category) | Показать список доступных категорий |
| Ошибка записи JSON | Вывести в текстовом формате |

**Формат сообщения об ошибке:**

```
❌ Ошибка генерации отчёта

Причина: {описание}
Решение: {рекомендация}

Частичные данные:
- Найдено скиллов: {N}
- Успешно проанализировано: {M}
- С ошибками: {K}
```

---

## Чек-лист

- [ ] **Шаг 0:** Проверил наличие папки `/.claude/skills/`
- [ ] **Шаг 1:** Собрал список всех SKILL.md файлов
- [ ] **Шаг 2:** Распарсил frontmatter каждого скилла
- [ ] **Шаг 2:** Обработал ошибки парсинга (если есть)
- [ ] **Шаг 3:** Проверил наличие tests.md для каждого скилла
- [ ] **Шаг 3:** Подсчитал тест-кейсы
- [ ] **Шаг 4:** Проанализировал связи между скиллами
- [ ] **Шаг 5:** Сформировал рекомендации
- [ ] **Шаг 6:** Проверил выполнение всех шагов
- [ ] **Шаг 7:** Вывел отчёт в запрошенном формате

---

## FAQ / Troubleshooting

### Как найти скиллы без тестов?

**Вариант 1 — через skill-report:**
```
/skill-report --verbose | grep "Тесты: 0"
```

**Вариант 2 — через test-coverage:**
```
/test-coverage claude
```

### Как узнать самые используемые скиллы?

В `--verbose` режиме показаны связи. Скиллы с большим количеством "Используют" — наиболее востребованные.

**Типичные лидеры:**
- `links-update` — вызывается из 10+ скиллов
- `environment-check` — вызывается из 7+ скиллов
- `input-validate` — вызывается из 3+ скиллов

### Как добавить новую категорию в отчёт?

Категории определяются автоматически из frontmatter скиллов. Добавьте скилл с новой категорией — она появится в отчёте.

### Почему скилл не отображается в отчёте?

**Возможные причины:**

| Причина | Решение |
|---------|---------|
| Нет SKILL.md в папке | Создать SKILL.md |
| Ошибка в frontmatter | Исправить YAML-синтаксис |
| Нет обязательного поля | Добавить `name`, `description`, `category` |

### Как сравнить отчёты за разные периоды?

Сохраните JSON-отчёты:
```bash
/skill-report --json > report-2026-01-01.json
# ... позже ...
/skill-report --json > report-2026-01-20.json

# Сравнение
diff report-2026-01-01.json report-2026-01-20.json
```

### Почему рекомендации не отображаются?

Рекомендации формируются только при наличии проблем:
- Скиллы без тестов
- Неполные категории (только create без update/delete)
- Критичные скиллы без тестов

Если всё в порядке — раздел рекомендаций будет минимальным.

### Как интегрировать отчёт в CI?

```yaml
# .github/workflows/skill-report.yml
- name: Generate skill report
  run: claude "/skill-report --json" > skill-report.json

- name: Check test coverage
  run: |
    coverage=$(jq '.summary.test_coverage_percent' skill-report.json)
    if [ "$coverage" -lt 100 ]; then
      echo "Test coverage below 100%: $coverage%"
      exit 1
    fi
```

---

## Следующие шаги

После генерации отчёта:

1. **Если найдены скиллы без тестов:**
   ```
   /test-create /.claude/skills/{skill}/tests.md
   ```

2. **Если категория неполная:**
   ```
   /skill-create {объект}-update
   /skill-create {объект}-delete
   ```

3. **Если нужен детальный анализ:**
   ```
   /health-check
   ```

4. **Если нужно проверить покрытие:**
   ```
   /test-coverage claude
   ```

**Типичная цепочка:**
```
/skill-report
→ Найдены проблемы
→ /test-create или /skill-create
→ /skill-report (проверка)
```

---

## Примеры использования

### Пример 1: Быстрый обзор

**Вызов:**
```
/skill-report
```

**Результат:**
Общая статистика и группировка по категориям с рекомендациями.

### Пример 2: Фильтр по категории

**Вызов:**
```
/skill-report --category testing
```

**Результат:**
```
📊 Категория: testing

Скиллов: 7
  • test-create (5 тестов) — Создание теста
  • test-update (4 тестов) — Изменение теста
  • test-review (5 тестов) — Проверка полноты теста
  • test-execute (6 тестов) — Выполнение тестов
  • test-complete (4 тестов) — Отметка теста как пройденного
  • test-delete (4 тестов) — Удаление теста
  • test-coverage (5 тестов) — Анализ покрытия

Всего тестов: 33
Покрытие: 100%
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

# Проверить покрытие тестами
/skill-report --json | jq '.summary.test_coverage_percent'

# Список скиллов без тестов
/skill-report --json | jq '[.skills[] | select(.has_tests == false) | .name]'
```

### Пример 4: Детальный анализ

**Вызов:**
```
/skill-report --verbose --category skill-management
```

**Результат:**
```
📊 Категория: skill-management (подробно)

📋 skill-create
   Описание:    Создание нового скилла по шаблону
   Критичный:   Нет
   Тесты:       6 тест-кейсов
   Триггеры:    7 (команда + 6 фраз)
   Зависит от:  skill-update, links-update, context-update, prompt-update
   Используют:  agent-create, instruction-create
   Размер:      841 строка

📋 skill-update
   Описание:    Обновление существующих скиллов
   Критичный:   Нет
   Тесты:       5 тест-кейсов
   Триггеры:    4 (команда + 3 фразы)
   Зависит от:  links-update
   Используют:  skill-create
   Размер:      320 строк

📋 skill-delete
   Описание:    Удаление скилла с очисткой связей
   Критичный:   Нет
   Тесты:       5 тест-кейсов
   Триггеры:    4 (команда + 3 фразы)
   Зависит от:  links-delete, context-delete
   Используют:  —
   Размер:      280 строк

📋 skill-migrate
   Описание:    Переименование скилла с обновлением ссылок
   Критичный:   Нет
   Тесты:       5 тест-кейсов
   Триггеры:    3 (команда + 2 фразы)
   Зависит от:  links-update, skill-update
   Используют:  —
   Размер:      350 строк
```

### Пример 5: Проверка после изменений

**Вызов:**
```
/skill-report --no-recommendations
```

**Результат:**
Отчёт без раздела рекомендаций — для быстрой проверки статистики.

### Пример 6: Нет скиллов

**Вызов:**
```
/skill-report
```

**Результат:**
```
📊 Отчёт по скиллам

Скиллы не найдены в /.claude/skills/

Для создания первого скилла используйте:
/skill-create {название}
```

### Пример 7: Категория не найдена

**Вызов:**
```
/skill-report --category unknown
```

**Результат:**
```
❌ Категория "unknown" не найдена

Доступные категории:
- skill-management (4 скилла)
- agent-management (1 скилл)
- instruction-management (3 скилла)
- documentation (10 скиллов)
- testing (7 скиллов)
- git (7 скиллов)
- utility (3 скилла)
- meta (1 скилл)
```
