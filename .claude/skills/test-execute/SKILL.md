---
name: test-execute
description: Выполнение тестов с автоопределением scope по пути или параметру
allowed-tools: Bash, Read, Glob, Grep
category: testing
triggers:
  commands:
    - /test-execute
    - /test-run
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
- [tools/claude-testing.md](/.claude/instructions/tools/claude-testing.md) — тестирование Claude Code
- [tools/project-testing.md](/.claude/instructions/tools/project-testing.md) — тестирование проекта

## Оглавление

- [Формат вызова](#формат-вызова)
- [Автоопределение scope](#автоопределение-scope)
- [Правила](#правила)
- [Воркфлоу](#воркфлоу)
  - [Шаг 1: Определить цель](#шаг-1-определить-цель)
  - [Шаг 2: Определить scope](#шаг-2-определить-scope)
  - [Шаг 3: Найти тесты](#шаг-3-найти-тесты)
  - [Шаг 4: Выполнить тесты](#шаг-4-выполнить-тесты)
  - [Шаг 5: Результат](#шаг-5-результат)
- [Чек-лист](#чек-лист)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/test-execute [target] [--scope claude|project|all] [--type smoke|functional|all]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `target` | Путь к объекту или скиллу | Все тесты scope |
| `--scope` | Область тестов | Авто или спросить |
| `--type` | Тип тестов | `all` |
| `--verbose` | Подробный вывод | — |
| `--dry-run` | Показать план без выполнения | — |

---

## Автоопределение scope

```
                    /test-execute [target] [--scope]
                               │
               ┌───────────────┼───────────────┐
               │               │               │
         target есть?    --scope есть?    ничего нет
               │               │               │
               ▼               ▼               ▼
       Автоопределить     Использовать     Спросить:
       по пути:           указанный        [1] claude
       .claude/* → claude                  [2] project
       src/* → project                     [3] all
       tests/* → project
```

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
   - Прочитать раздел "Тестирование"
   - Выполнить шаги теста
   - Проверить результат
   - Записать статус

2. Формат выполнения smoke test:
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

```bash
# Определить команду запуска
if [ -f "Makefile" ]; then
  make test
elif [ -f "package.json" ]; then
  npm test
elif [ -f "pytest.ini" ]; then
  pytest
fi
```

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
