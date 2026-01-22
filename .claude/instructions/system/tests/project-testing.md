---
type: project
description: Индекс инструкций тестирования проекта
related:
  - tests/claude-testing.md
  - src/dev/testing.md
  - git/ci.md
---

# Тестирование проекта

Индекс инструкций для тестирования проекта (`/tests/`).

> **Отличие от [claude-testing.md](./claude-testing.md):** Этот раздел описывает тесты для кода проекта (unit, integration, e2e). Claude-testing описывает тесты для скиллов, инструкций и агентов Claude Code.

> **Шаблоны форматов:** [test-formats.md](/.claude/templates/test-formats.md) — статусы, типы тестов, шаблоны.

## Оглавление

- [Общие правила](#общие-правила)
- [Структура папки /tests/](#структура-папки-tests)
- [Инструкции](#инструкции)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Общие правила

**Правило:** Все тесты запускаются через Makefile.

```bash
make test           # Все тесты
make test-unit      # Только unit
make test-e2e       # Только e2e
make test-smoke     # Smoke-тесты (быстрые)
```

**Правило:** Тесты должны быть идемпотентны — повторный запуск даёт тот же результат.

**Правило:** Тесты не должны зависеть от порядка выполнения.

---

## Структура папки /tests/

```
/tests/
  /unit/           # Юнит-тесты сервисов
  /integration/    # Интеграционные тесты
  /e2e/            # End-to-end тесты
  /smoke/          # Smoke-тесты (быстрая проверка)
  /load/           # Нагрузочные тесты
  /fixtures/       # Тестовые данные
```

---

## Инструкции

| Инструкция | Описание | Тип | Статус |
|------------|----------|-----|:------:|
| [unit.md](../tests/unit.md) | Unit-тесты: изоляция, моки, покрытие | standard | ✅ |
| [integration.md](../tests/integration.md) | Интеграционные тесты: БД, API, сервисы | standard | ✅ |
| [e2e.md](../tests/e2e.md) | End-to-end тесты: сценарии пользователя | standard | ✅ |
| [smoke.md](../tests/smoke.md) | Smoke-тесты: быстрая проверка работоспособности | standard | ✅ |
| [load.md](../tests/load.md) | Нагрузочные тесты: k6, пороги производительности | standard | ✅ |
| [fixtures.md](../tests/fixtures.md) | Тестовые данные: фикстуры, фабрики, seeds | standard | ✅ |

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание | Команда |
|-------|----------|---------|
| [test-create](/.claude/skills/test-create/SKILL.md) | Создание теста с автоопределением scope | `/test-create` |
| [test-execute](/.claude/skills/test-execute/SKILL.md) | Выполнение тестов | `/test-execute` |
| [test-update](/.claude/skills/test-update/SKILL.md) | Изменение существующего теста | `/test-update` |
| [test-review](/.claude/skills/test-review/SKILL.md) | Проверка полноты и качества теста | `/test-review` |
| [test-complete](/.claude/skills/test-complete/SKILL.md) | Отметка теста как пройденного | `/test-complete` |
| [test-delete](/.claude/skills/test-delete/SKILL.md) | Удаление теста | `/test-delete` |

**Автоопределение scope:** При указании пути `src/*`, `tests/*`, `shared/*` скиллы автоматически работают в режиме `project` (тестирование кода проекта).

---

## FAQ / Troubleshooting

### Как отладить падающий тест?

1. Запустить с verbose:
   ```bash
   make test-unit VERBOSE=1
   # или
   npm test -- --verbose
   ```
2. Запустить только падающий тест:
   ```bash
   npm test -- --filter "test name"
   pytest -k "test_name" -v
   ```
3. Проверить тестовые данные (fixtures) — возможно устарели
4. Проверить моки — возможно не соответствуют реальным API

### Как перезапустить только failed тесты?

```bash
# Jest
npm test -- --onlyFailures

# Pytest
pytest --lf  # last failed

# Vitest
npx vitest --changed
```

Или через скилл:
```
/test-execute --scope project --only-failed
```

### Какой минимальный coverage для кода?

| Тип кода | Coverage | Комментарий |
|----------|----------|-------------|
| Бизнес-логика | 80%+ | Критично для стабильности |
| API handlers | 70%+ | Включая error cases |
| Утилиты | 90%+ | Простой код, легко покрыть |
| UI компоненты | 60%+ | Сложно тестировать, меньше требований |

### Тесты проходят локально, падают в CI — что делать?

1. **Проверить окружение:**
   - Версии Node/Python/etc
   - Переменные окружения
   - Доступ к внешним сервисам

2. **Проверить тайминги:**
   - Добавить `await` для async операций
   - Увеличить таймауты для CI

3. **Проверить изоляцию:**
   - Тесты не должны зависеть от порядка
   - Каждый тест очищает за собой данные

### Scope определён неверно — что делать?

**Симптом:** Скилл создал тест в формате markdown вместо `.test.ts` (или наоборот).

**Решение:** Указать scope явно:
```
/test-create src/auth/token.ts --scope project
/test-execute tests/unit/ --scope project
```

**Причины неверного определения:**
- Путь содержит `.claude/` → определяется как `claude`
- Файл вне стандартных папок (`src/`, `tests/`, `shared/`)

### Как управлять тестовыми данными (fixtures)?

1. **Расположение:** `/tests/fixtures/`
2. **Формат:** JSON, YAML или TypeScript factories
3. **Принцип:** Каждый тест использует свои данные или явно указывает shared fixture
4. **Очистка:** После теста удалять созданные данные

Подробнее: [fixtures.md](/.claude/instructions/tests/fixtures.md) *(когда будет создан)*

---

## Связанные инструкции

- [claude-testing.md](/.claude/instructions/tests/claude-testing.md) — тестирование Claude Code (скиллы, инструкции)
- [src/dev/testing.md](/.claude/instructions/src/dev/testing.md) — тесты внутри сервисов (co-located)
- [git/ci.md](/.claude/instructions/git/ci.md) — CI/CD pipeline (запуск тестов)
