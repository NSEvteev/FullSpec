---
name: test-coverage
description: Анализ покрытия тестами скиллов и проекта
allowed-tools: Bash, Read, Glob, Grep
category: testing
triggers:
  commands:
    - /test-coverage
  phrases:
    ru:
      - покрытие тестами
      - анализ покрытия
    en:
      - test coverage
      - coverage report
---

# Анализ покрытия тестами

Команда для анализа покрытия тестами скиллов Claude и кода проекта.

**Связанные скиллы:**
- [test-create](/.claude/skills/test-create/SKILL.md) — создание тестов
- [test-execute](/.claude/skills/test-execute/SKILL.md) — выполнение тестов
- [test-review](/.claude/skills/test-review/SKILL.md) — ревью качества тестов
- [health-check](/.claude/skills/health-check/SKILL.md) — общая проверка проекта

**Связанные инструкции:**
- [tests/claude-testing.md](/.claude/instructions/tests/claude-testing.md) — тестирование Claude скиллов
- [tests/project-testing.md](/.claude/instructions/tests/project-testing.md) — тестирование проекта
- [scope-detection.md](/.claude/instructions/shared/scope.md) — определение scope

## Оглавление

- [Формат вызова](#формат-вызова)
- [Режимы работы](#режимы-работы)
- [Воркфлоу](#воркфлоу)
- [Метрики покрытия](#метрики-покрытия)
- [Формат вывода](#формат-вывода)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/test-coverage [scope] [--json] [--verbose] [--threshold N]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `scope` | `claude` / `project` / `all` | `all` |
| `--json` | Вывод в JSON формате | false |
| `--verbose` | Подробный вывод с деталями | false |
| `--threshold N` | Порог покрытия в % (для CI) | 80 |

---

## Режимы работы

### scope: claude

Анализ покрытия Claude скиллов тестами:
- Проверка наличия `tests.md` для каждого скилла
- Подсчёт тест-кейсов в каждом `tests.md`
- Анализ статусов тестов (pending/passed/failed)

### scope: project

Анализ покрытия кода проекта:
- Запуск команды покрытия из проекта (jest --coverage, pytest --cov, etc.)
- Парсинг отчёта покрытия
- Сводка по файлам и модулям

### scope: all

Комбинация обоих режимов с общей статистикой.

---

## Воркфлоу

### Шаг 1: Определить scope

1. Из аргумента: `/test-coverage claude`
2. Или по умолчанию: `all`

### Шаг 2: Claude coverage (если scope = claude или all)

```bash
# Найти все скиллы
ls .claude/skills/*/SKILL.md

# Для каждого скилла проверить tests.md
ls .claude/skills/{skill}/tests.md
```

**Метрики:**
- Скиллов всего: N
- Скиллов с tests.md: M
- Покрытие скиллов: M/N * 100%
- Тест-кейсов всего: K
- Статусы: passed / failed / pending

### Шаг 3: Project coverage (если scope = project или all)

1. Определить тип проекта (package.json, pyproject.toml, go.mod)
2. Запустить соответствующую команду покрытия
3. Спарсить результат

| Тип проекта | Команда |
|-------------|---------|
| Node.js | `npm run test:coverage` или `jest --coverage --json` |
| Python | `pytest --cov --cov-report=json` |
| Go | `go test -cover -coverprofile=coverage.out` |

### Шаг 4: Сформировать отчёт

Вывести сводку покрытия в выбранном формате.

### Шаг 5: Проверить threshold (если указан)

```
if coverage < threshold:
    exit(1)  # Для CI
```

---

## Метрики покрытия

### Claude скиллы

| Метрика | Описание |
|---------|----------|
| `skills_total` | Общее количество скиллов |
| `skills_with_tests` | Скиллы с файлом tests.md |
| `skills_coverage` | % скиллов с тестами |
| `test_cases_total` | Общее число тест-кейсов |
| `test_cases_passed` | Тесты со статусом passed |
| `test_cases_failed` | Тесты со статусом failed |
| `test_cases_pending` | Тесты со статусом pending |

### Код проекта

| Метрика | Описание |
|---------|----------|
| `lines_total` | Всего строк кода |
| `lines_covered` | Покрытых строк |
| `lines_coverage` | % покрытия строк |
| `branches_total` | Всего веток |
| `branches_covered` | Покрытых веток |
| `branches_coverage` | % покрытия веток |
| `functions_total` | Всего функций |
| `functions_covered` | Покрытых функций |
| `functions_coverage` | % покрытия функций |

---

## Формат вывода

### Стандартный вывод

```
📊 Отчёт о покрытии тестами

═══════════════════════════════════════════════════════
CLAUDE СКИЛЛЫ
═══════════════════════════════════════════════════════

Скиллов всего:        35
С тестами (tests.md): 35
Покрытие:             100% ✅

Тест-кейсы:
  • passed:  42
  • failed:   0
  • pending: 89

Скиллы без тестов: нет

═══════════════════════════════════════════════════════
КОД ПРОЕКТА
═══════════════════════════════════════════════════════

Lines:     78.5% (1245/1586)
Branches:  65.2% (234/359)
Functions: 82.1% (147/179)

Файлы с низким покрытием (<50%):
  • src/utils/parser.ts (23%)
  • src/services/legacy.ts (41%)

═══════════════════════════════════════════════════════
ИТОГО
═══════════════════════════════════════════════════════

Общее покрытие: 85% ✅ (порог: 80%)
```

### JSON вывод (--json)

```json
{
  "claude": {
    "skills_total": 35,
    "skills_with_tests": 35,
    "skills_coverage": 100,
    "test_cases": {
      "total": 131,
      "passed": 42,
      "failed": 0,
      "pending": 89
    },
    "skills_without_tests": []
  },
  "project": {
    "lines": { "total": 1586, "covered": 1245, "coverage": 78.5 },
    "branches": { "total": 359, "covered": 234, "coverage": 65.2 },
    "functions": { "total": 179, "covered": 147, "coverage": 82.1 },
    "low_coverage_files": [
      { "file": "src/utils/parser.ts", "coverage": 23 },
      { "file": "src/services/legacy.ts", "coverage": 41 }
    ]
  },
  "summary": {
    "coverage": 85,
    "threshold": 80,
    "passed": true
  }
}
```

---

## Примеры использования

### Пример 1: Быстрая проверка Claude скиллов

**Вызов:**
```
/test-coverage claude
```

**Результат:**
```
📊 Claude скиллы: покрытие тестами

Скиллов: 35
С tests.md: 35 (100%)
Тест-кейсов: 131 (passed: 42, pending: 89)

✅ Все скиллы имеют тесты
```

### Пример 2: CI проверка с порогом

**Вызов:**
```
/test-coverage all --threshold 80 --json
```

**Использование в CI:**
```yaml
- name: Check test coverage
  run: claude /test-coverage all --threshold 80
```

### Пример 3: Подробный отчёт

**Вызов:**
```
/test-coverage all --verbose
```

**Результат:**
Включает список всех скиллов с количеством тестов и детализацию по каждому файлу проекта.

---

## FAQ

### Как повысить покрытие Claude скиллов?

1. Найти скиллы без тестов: `/test-coverage claude`
2. Создать тесты: `/test-create {skill-name}`

### Как интегрировать в CI?

```yaml
jobs:
  coverage:
    steps:
      - run: /test-coverage all --threshold 80
```

При покрытии ниже порога — выход с кодом 1.

### Почему покрытие проекта 0%?

Проверьте:
1. Есть ли команда `test:coverage` в package.json
2. Настроен ли jest/pytest для генерации отчётов
3. Существуют ли тестовые файлы в проекте
