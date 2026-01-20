---
name: test-execute
description: Выполнение тестов с автоопределением scope по пути или параметру
allowed-tools: Bash, Read, Glob, Grep
category: testing
triggers:
  commands:
    - /test-execute
  phrases:
    ru:
      - запусти тест
      - выполни тест
      - проверь тесты
    en:
      - run test
      - execute test
---

# Выполнение тестов

Команда для запуска тестов с автоматическим определением scope.

**Связанные скиллы:**
- [test-create](/.claude/skills/test-create/SKILL.md) — создание теста
- [test-update](/.claude/skills/test-update/SKILL.md) — изменение теста
- [test-review](/.claude/skills/test-review/SKILL.md) — проверка полноты теста
- [test-complete](/.claude/skills/test-complete/SKILL.md) — отметка о прохождении
- [test-delete](/.claude/skills/test-delete/SKILL.md) — удаление теста

**Связанные инструкции:**
- [tests/claude-testing.md](/.claude/instructions/tests/claude-testing.md) — тестирование Claude Code
- [tests/project-testing.md](/.claude/instructions/tests/project-testing.md) — тестирование проекта

**Шаблоны:**
- [test-formats.md](/.claude/templates/test-formats.md) — форматы отчётов, статусы тестов
- [scope-detection.md](/.claude/templates/scope-detection.md) — определение scope (SSOT)
- [output-formats.md](/.claude/templates/output-formats.md) — форматы вывода (SSOT)

## Оглавление

- [Формат вызова](#формат-вызова)
- [Автоопределение scope](#автоопределение-scope)
- [Состояние между запусками](#состояние-между-запусками)
- [Правила](#правила)
- [Воркфлоу](#воркфлоу)
  - [Шаг 1: Определить цель](#шаг-1-определить-цель)
  - [Шаг 2: Определить scope](#шаг-2-определить-scope)
  - [Шаг 3: Найти тесты](#шаг-3-найти-тесты)
  - [Шаг 4: Выполнить тесты](#шаг-4-выполнить-тесты)
  - [Шаг 5: Результат](#шаг-5-результат)
- [Чек-лист](#чек-лист)
- [Примеры использования](#примеры-использования)
- [FAQ / Troubleshooting](#faq--troubleshooting)

---

## Формат вызова

```
/test-execute [target] [--scope claude|project|all] [--type smoke|functional|all] [--category <name>]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `target` | Путь к объекту или скиллу | Все тесты scope |
| `--scope` | Область тестов | Авто или спросить |
| `--type` | Тип тестов | `all` |
| `--category` | Фильтр по категории (только для scope claude) | Все категории |
| `--last-failed` | Запустить только failed тесты из последнего запуска | — |
| `--only-failed` | Алиас для `--last-failed` | — |
| `--verbose` | Подробный вывод | — |
| `--dry-run` | Показать план без выполнения | — |
| `--watch` | Режим наблюдения (перезапуск при изменениях) | — |
| `--report` | Генерировать отчёт в формате markdown | — |

### Режим --watch

Запуск тестов в режиме наблюдения. При изменении файлов тесты перезапускаются автоматически.

```
/test-execute --scope claude --watch

👁️ Watch mode включён

Отслеживаемые файлы:
- /.claude/skills/**/*.md
- /.claude/instructions/**/*.md

[10:30:15] Запуск тестов... ✅ 15/15 passed
[10:32:45] Изменён: skill-create/SKILL.md
[10:32:46] Перезапуск... ✅ 15/15 passed
[10:35:12] Изменён: test-formats.md
[10:35:13] Перезапуск... ✅ 15/15 passed

Ctrl+C для выхода
```

**Отслеживаемые пути по scope:**

| Scope | Отслеживаемые пути |
|-------|-------------------|
| `claude` | `/.claude/skills/**`, `/.claude/instructions/**`, `/.claude/templates/**` |
| `project` | `/src/**`, `/tests/**`, `/config/**` |
| `all` | Все вышеперечисленные |

### Режим --report

Генерация отчёта в формате markdown.

```
/test-execute --scope all --report

[Выполнение тестов...]

📊 Отчёт сохранён: .claude/reports/test-report-2026-01-20.md
```

**Формат отчёта:**

```markdown
# Test Report — 2026-01-20

## Summary
- Total: 25
- Passed: 23
- Failed: 2
- Duration: 45s

## Failed Tests
| Test | Error |
|------|-------|
| test-create smoke | Expected skill to exist |
| issue-review functional | Timeout |

## Coverage
...
```

**Категории для `--category`** (из [skills.md](/.claude/skills/README.md)):
- `skill-management` — skill-create, skill-update, skill-delete
- `instruction-management` — instruction-*, критичные
- `documentation` — doc-*, links-*, context-*
- `testing` — test-*
- `git` — issue-*, критичные
- `meta` — prompt-update

---

## Автоопределение scope

> **SSOT:** Полная логика определения scope описана в [scope-detection.md](/.claude/templates/scope-detection.md).

```
                    /test-execute [target] [--scope]
                               │
               ┌───────────────┼───────────────┐
               │               │               │
         target есть?    --scope есть?    ничего нет
               │               │               │
               ▼               ▼               ▼
       Автоопределить     Использовать     Спросить:
       по пути            указанный        [1] claude
       (см. SSOT)                          [2] project
                                           [3] all
```

---

## Состояние между запусками

**Механизм:** После каждого запуска `/test-execute` результаты сохраняются для использования `--last-failed`.

**Файл состояния:** `.claude/state/last-test-run.json`

```json
{
  "timestamp": "2026-01-20T16:00:00Z",
  "scope": "claude",
  "category": null,
  "results": {
    "passed": [
      ".claude/skills/test-create/SKILL.md",
      ".claude/skills/test-delete/SKILL.md"
    ],
    "failed": [
      ".claude/skills/test-update/SKILL.md",
      ".claude/skills/test-review/SKILL.md"
    ],
    "not_run": [
      ".claude/skills/issue-create/SKILL.md"
    ]
  }
}
```

**Использование `--last-failed`:**

```bash
# Первый запуск — полный
/test-execute --scope claude
# Результат: 2 failed (test-update, test-review)
# Состояние сохранено в .claude/state/last-test-run.json

# Второй запуск — только failed
/test-execute --last-failed
# Автоматически запустит: test-update, test-review
```

**Правило:** Файл состояния перезаписывается при каждом запуске (кроме `--last-failed`).

---

## Правила

### Правило scope

**Правило:** Без параметров — спросить у пользователя какой scope запустить.

**Правило:** С target — определить scope автоматически по пути.

### Правило выполнения

**Scope claude:**
- Выполнение через LLM: прочитать SKILL.md, выполнить шаги теста
- Интерактивный режим: запуск команд, проверка результатов

**Scope project:**
- Выполнение через CLI: `make test`, `npm test`, `pytest`
- Автоматический режим: запуск и сбор результатов

### Правило отчёта

**Правило:** Всегда выводить итоговый отчёт с результатами.

---

## Воркфлоу

### Шаг 1: Определить цель

1. Из аргумента: `/test-execute .claude/skills/issue-create/SKILL.md`
2. Или из scope: `/test-execute --scope claude`
3. Или спросить: "Что тестировать?"

### Шаг 2: Определить scope

**Если указан target:**
- `.claude/*` → scope = claude
- `src/*`, `tests/*` → scope = project

**Если указан --scope:**
- Использовать указанный

**Если ничего не указано:**
```
Выберите scope для тестирования:
[1] claude — тесты скиллов и инструкций
[2] project — тесты кода проекта
[3] all — все тесты
```

### Шаг 3: Найти тесты

**Scope claude:**

```bash
# Найти все скиллы с разделом "Тестирование"
grep -l "## Тестирование" .claude/skills/*/SKILL.md
```

**Scope project:**

```bash
# Найти все тестовые файлы
find . -name "*.test.ts" -o -name "*.spec.ts" -o -name "*_test.py"
```

### Шаг 4: Выполнить тесты

**Scope claude (интерактивно):**

1. Для каждого скилла с тестами:
   - Прочитать раздел "Тестирование" в SKILL.md
   - Извлечь ожидания из теста
   - Выполнить шаги теста последовательно
   - Сравнить результат с ожиданиями
   - Записать статус (passed/failed)

2. **Алгоритм выполнения шага теста:**
   ```
   a. Прочитать описание шага
   b. Выполнить действие (вызов команды, проверка вывода)
   c. Сравнить результат с ожиданием:
      - Совпадает → ✅ Passed
      - Не совпадает → ❌ Failed + записать причину
      - Ошибка/таймаут → ❌ Failed + записать ошибку
   d. Перейти к следующему шагу или завершить
   ```

3. **Обработка ошибок:**
   - Если шаг failed → продолжить выполнение остальных шагов
   - Если критическая ошибка → остановить тест, пометить как failed
   - Записать все ошибки в отчёт

4. Формат выполнения smoke test:
   ```
   📋 Выполняю: Smoke test issue-create

   Шаг 1: Вызов по команде /issue-create
   → Ожидание: Скилл запускается
   → Результат: ✅ Passed

   Шаг 2: Проверка вывода
   → Ожидание: Выводит список сервисов
   → Результат: ✅ Passed

   Итог: ✅ PASSED (2/2)
   ```

**Scope project (автоматически):**

1. **Определить команду запуска:**
   ```bash
   if [ -f "Makefile" ]; then
     make test
   elif [ -f "package.json" ]; then
     npm test
   elif [ -f "pytest.ini" ]; then
     pytest
   fi
   ```

2. **Параметры запуска:**
   - `--verbose` → передать флаг verbose в тест-раннер
   - `--filter {pattern}` → запустить только тесты по паттерну
   - `--timeout {ms}` → ограничить время выполнения

3. **Сбор результатов:**
   - Парсить вывод тест-раннера
   - Извлечь количество passed/failed/skipped
   - Извлечь coverage (если доступен)
   - Записать в отчёт

4. **Обработка ошибок:**
   - Тест-раннер не найден → предложить установить
   - Таймаут → пометить как failed, показать последний вывод
   - Exit code != 0 → пометить как failed

### Шаг 5: Результат

```
📊 Результаты тестирования

Scope: {claude|project|all}
Тип: {smoke|functional|all}

┌─────────────────────────────────────────────────────────┐
│ Scope: claude                                           │
├─────────────────────────────────────────────────────────┤
│ ✅ issue-create      smoke    PASSED  (3/3)             │
│ ✅ issue-update      smoke    PASSED  (2/2)             │
│ ❌ issue-review      smoke    FAILED  (1/3)             │
│    └─ Шаг 2: ожидался чек-лист, получен текст          │
│ ⬜ doc-create        smoke    NOT RUN                   │
├─────────────────────────────────────────────────────────┤
│ Итого: 2 passed, 1 failed, 1 not run                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Scope: project                                          │
├─────────────────────────────────────────────────────────┤
│ ✅ src/auth/tests    unit     PASSED  (15/15)          │
│ ✅ src/notify/tests  unit     PASSED  (8/8)            │
│ ✅ tests/e2e         e2e      PASSED  (5/5)            │
├─────────────────────────────────────────────────────────┤
│ Итого: 28 passed, 0 failed                             │
└─────────────────────────────────────────────────────────┘

Общий результат: ⚠️ 1 failed
```

---

## Чек-лист

- [ ] **Шаг 1:** Получил цель тестирования (target или scope)
- [ ] **Шаг 2:** Определил scope (claude/project/all)
- [ ] **Шаг 3:** Нашёл все тесты в scope
- [ ] **Шаг 4:** Выполнил тесты
- [ ] **Шаг 4:** Собрал результаты
- [ ] **Шаг 5:** Вывел итоговый отчёт

---

## Примеры использования

### Пример 1: Тест конкретного скилла

**Вызов:**
```
/test-execute .claude/skills/issue-create/SKILL.md
```

**Результат:**
```
📋 Выполняю: Smoke test issue-create

Шаг 1: Вызов по команде /issue-create
→ Результат: ✅ Passed

Шаг 2: Проверка списка сервисов
→ Результат: ✅ Passed

Шаг 3: Проверка запроса заголовка
→ Результат: ✅ Passed

📊 Результат: ✅ PASSED (3/3)
```

### Пример 2: Все тесты Claude Code

**Вызов:**
```
/test-execute --scope claude
```

**Результат:**
```
📊 Результаты тестирования

Scope: claude
Найдено тестов: 5

✅ issue-create    PASSED (3/3)
✅ issue-update    PASSED (2/2)
✅ doc-create      PASSED (2/2)
⬜ skill-create    NOT RUN (нет тестов)
⬜ links-update    NOT RUN (нет тестов)

Итого: 3 passed, 0 failed, 2 without tests
```

### Пример 3: Тесты проекта

**Вызов:**
```
/test-execute --scope project
```

**Результат:**
```
📊 Результаты тестирования

Scope: project
Команда: make test

Running tests...

✅ Unit tests:      15/15 passed
✅ Integration:     8/8 passed
✅ E2E:             5/5 passed

Итого: 28 passed, 0 failed
Coverage: 78%
```

### Пример 4: Dry-run

**Вызов:**
```
/test-execute --scope all --dry-run
```

**Результат:**
```
📋 План тестирования (dry-run)

Scope: all

Claude (5 скиллов с тестами):
- issue-create: smoke test
- issue-update: smoke test
- doc-create: smoke test
- skill-create: smoke test
- links-update: functional test

Project:
- Команда: make test
- Файлов: 28 (*.test.ts, *.spec.ts)

Тесты не запущены (dry-run).
```

### Пример 5: Интерактивный выбор

**Вызов:**
```
/test-execute
```

**Диалог:**
```
Выберите scope для тестирования:
[1] claude — тесты скиллов и инструкций
[2] project — тесты кода проекта
[3] all — все тесты

> 1

Выполняю тесты scope: claude...
```

### Пример 6: Фильтрация по категории

**Вызов:**
```
/test-execute --scope claude --category testing
```

**Результат:**
```
📊 Результаты тестирования

Scope: claude
Категория: testing
Найдено скиллов: 6

┌────────────────────────┬──────────┬─────────────┐
│ Скилл                  │ Тип      │ Результат   │
├────────────────────────┼──────────┼─────────────┤
│ test-create            │ smoke    │ ✅ PASSED   │
│ test-update            │ smoke    │ ✅ PASSED   │
│ test-review            │ smoke    │ ✅ PASSED   │
│ test-execute           │ smoke    │ ✅ PASSED   │
│ test-complete          │ smoke    │ ✅ PASSED   │
│ test-delete            │ smoke    │ ✅ PASSED   │
├────────────────────────┴──────────┴─────────────┤
│ Итого: 6 passed, 0 failed                       │
└─────────────────────────────────────────────────┘
```

### Пример 7: Только критичные скиллы

**Вызов:**
```
/test-execute --scope claude --category git --category skill-management
```

**Результат:**
```
📊 Результаты тестирования

Scope: claude
Категории: git, skill-management (критичные)
Найдено скиллов: 9

issue-*:       6 скиллов (3 с тестами)
skill-*:       3 скилла (2 с тестами)

✅ issue-create      PASSED
✅ issue-execute     PASSED
⬜ issue-update      NOT RUN (нет тестов)
...

Итого: 5 passed, 0 failed, 4 without tests
```

---

## CI интеграция

> Связь с CI pipeline описана в [ci.md](/.claude/instructions/git/ci.md#интеграция-с-тестированием).

### Маппинг на CI

| /test-execute | CI эквивалент |
|---------------|---------------|
| `--scope project` | `make test` |
| `--scope claude` | Manual (Claude Code) |
| `--type smoke` | Быстрые тесты перед push |
| `--type all` | Полные тесты перед merge |

### Рекомендации

**Перед push:**
```bash
/test-execute --scope project --type smoke
```

**При failed CI:**
```bash
# 1. Посмотреть логи
gh run view <run-id> --log-failed

# 2. Найти проблему локально
/test-execute путь-к-failed-тесту --verbose

# 3. Если тест некорректен
/test-update путь --reason fix

# 4. Если баг в коде
/issue-create --type bug
```

---

## FAQ / Troubleshooting

### Scope определён неверно — что делать?

**Симптом:** Скилл запустился в режиме `project` вместо `claude` (или наоборот).

**Решение:** Указать scope явно:
```
/test-execute .claude/skills/my-skill/SKILL.md --scope claude
/test-execute tests/unit/ --scope project
```

**Причины неверного определения:**

| Ситуация | Причина | Решение |
|----------|---------|---------|
| Путь не начинается с `.claude/` | Определяется как `project` | Добавить `--scope claude` |
| Опечатка в пути `.claud/` | Не распознаётся | Исправить путь |
| Относительный путь `skills/...` | Нет `.claude/` | Использовать полный путь |
| Нестандартная структура | Автоопределение не работает | Явно указать `--scope` |

### Scope claude: Тесты не найдены

**Симптом:**
```
📊 Результаты тестирования
Scope: claude
Найдено тестов: 0
```

**Причины:**
1. В скиллах нет раздела "## Тестирование"
2. Указан неверный путь к скиллу
3. Файлы `tests.md` отсутствуют

**Решение:**
1. Создать тесты через `/test-create`:
   ```
   /test-create .claude/skills/{skill}/SKILL.md
   ```
2. Проверить путь существует:
   ```bash
   ls .claude/skills/{skill}/SKILL.md
   ```

### Scope project: Тесты не найдены

**Симптом:**
```
📊 Результаты тестирования
Scope: project
Команда: make test
Exit code: 1 (no tests found)
```

**Причины:**
1. Нет файлов `*.test.ts` / `*.spec.ts`
2. Неверная конфигурация test runner
3. Makefile не настроен

**Решение:**
1. Создать тесты через `/test-create`:
   ```
   /test-create src/{path}/{file}.ts
   ```
2. Проверить наличие тестовых файлов:
   ```bash
   find . -name "*.test.ts" -o -name "*.spec.ts"
   ```
3. Проверить Makefile:
   ```bash
   grep -A5 "test:" Makefile
   ```

### Тесты падают только при выполнении через скилл

**Scope claude:**

Возможные причины:
1. Тест зависит от контекста предыдущего разговора
2. Скилл изменился после создания теста
3. Ожидания в тесте устарели

Решение:
```
/test-update .claude/skills/{skill}/SKILL.md
```

**Scope project:**

Возможные причины:
1. Переменные окружения не загружены
2. Зависимости не установлены
3. База данных недоступна

Решение:
```bash
# Проверить переменные
env | grep -i test

# Установить зависимости
npm install  # или make deps

# Проверить доступность сервисов
docker-compose ps
```

### Как выполнить только failed тесты?

```
/test-execute --scope {claude|project} --only-failed
```

**Или через test runner напрямую:**

**Scope project:**
```bash
# Jest
npm test -- --onlyFailures

# Pytest
pytest --lf

# Vitest
npx vitest --changed
```

### Как получить подробный вывод?

```
/test-execute {target} --verbose
```

**Scope claude:**
- Показывает каждый шаг теста
- Показывает сравнение ожидание vs результат

**Scope project:**
- Передаёт `--verbose` в test runner
- Показывает полные логи тестов

### Как проверить plan без выполнения?

```
/test-execute --scope all --dry-run
```

Покажет:
- Какие тесты будут запущены
- Какие команды будут выполнены
- Какие файлы задействованы

---

## Следующие шаги

После выполнения тестов:

**При passed:**
```bash
/test-complete {путь} --status passed
```

**При failed:**
```bash
# 1. Понять причину
/test-review {путь}

# 2a. Если тест некорректен
/test-update {путь} --reason fix

# 2b. Если баг в коде
/issue-create --type bug --title "Test failed: {название}"
```

**Типичные цепочки:**
```
passed:  /test-execute → /test-complete
failed:  /test-execute → /test-review → /test-update или /issue-create
```
