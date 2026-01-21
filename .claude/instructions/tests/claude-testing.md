---
type: standard
description: Тестирование Claude Code: smoke tests, проверка скиллов
related:
  - /.claude/skills/README.md
  - /.claude/agents/README.md
  - /.claude/instructions/tests/project-testing.md
  - /.claude/instructions/tests/claude-functional.md
---

# Тестирование Claude Code

Правила тестирования скиллов, инструкций и воркфлоу Claude Code.

> **Шаблоны форматов:** [test-formats.md](/.claude/templates/test-formats.md) — статусы, типы тестов, шаблоны smoke/functional/integration.

## Оглавление

- [Правила](#правила)
  - [Типы тестов](#типы-тестов)
  - [Smoke tests](#smoke-tests)
  - [Тестирование инструкций](#тестирование-инструкций)
- [Чек-листы](#чек-листы)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Интеграция с Git Hooks](#интеграция-с-git-hooks)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Типы тестов

> **SSOT:** Полное описание типов тестов см. в [scope-detection.md](/.claude/templates/scope-detection.md#формат-тестов-по-scope).

**Для scope `claude`:**

| Тип | Что проверяет | Когда запускать |
|-----|---------------|-----------------|
| `smoke` | Скилл вызывается и отвечает | После создания скилла |
| `functional` | Скилл выполняет задачу корректно | После изменения скилла |
| `integration` | Скиллы работают вместе | После изменения воркфлоу |

### Smoke tests

> **Шаблон:** [/.claude/templates/tests/smoke-test.md](/.claude/templates/tests/smoke-test.md)

**Правило:** Каждый скилл должен проходить базовую проверку.

**Критерии smoke test:**
1. Скилл распознаётся по команде (`/skill-name`)
2. Скилл распознаётся по фразам-триггерам
3. Скилл выводит ожидаемый формат ответа
4. Скилл не падает с ошибкой

**Формат проверки:** см. [Шаблон: Smoke test](/.claude/templates/test-formats.md#шаблон-smoke-test)

> **Functional tests:** [claude-functional.md](./claude-functional.md) — функциональное, интеграционное и регрессионное тестирование скиллов.

### Тестирование инструкций

**Правило:** Инструкции тестируются на применимость к реальному коду.

**Что проверять:**

| Аспект | Проверка |
|--------|----------|
| Понятность | Инструкция понятна без дополнительного контекста |
| Полнота | Все необходимые правила описаны |
| Примеры | Примеры работают и актуальны |
| Связи | Ссылки на связанные инструкции корректны |
| Применимость | Код проекта соответствует инструкции |

**Проверка через `/instruction-update`:**

```bash
/instruction-update {путь-к-инструкции}
```

---

## Чек-листы

> **Базовые чек-листы:** см. [test-formats.md](/.claude/templates/test-formats.md#чек-листы)
> **Чек-листы functional/integration/regression тестов:** см. [claude-functional.md](./claude-functional.md#чек-листы)

### Чек-лист smoke test для скилла (расширенный)

- [ ] Скилл вызывается по команде `/{name}`
- [ ] Скилл вызывается по русской фразе
- [ ] Скилл вызывается по английской фразе
- [ ] Скилл выводит описание при вызове без аргументов
- [ ] Скилл корректно обрабатывает `--help` (если поддерживает)
- [ ] Скилл не падает с ошибкой при базовом вызове

### Чек-лист тестирования инструкции

- [ ] Frontmatter корректен (type, description, related)
- [ ] Все разделы заполнены (Правила, Примеры, Связанные)
- [ ] Примеры актуальны и работают
- [ ] Ссылки на файлы корректны (не битые)
- [ ] Код проекта соответствует инструкции

---

## Примеры

> **Примеры functional/integration/regression тестов:** см. [claude-functional.md](./claude-functional.md#примеры)

### Пример: Smoke test для issue-create

```
📋 Smoke test: issue-create

Команда: /issue-create
Триггер: "создай задачу"

Шаги:
1. Ввести: /issue-create
2. Проверить, что скилл запрашивает параметры

Ожидание:
- Скилл выводит список сервисов для выбора
- Запрашивает заголовок задачи

Результат:
> /issue-create

Для какого сервиса?
[1] auth
[2] notify
...

Статус: ✅ Passed
```

### Пример: Тест инструкции git/commits.md

```
📋 Instruction test: git/commits.md

Проверка применимости к проекту.

Шаги:
1. /instruction-update git/commits.md
2. Проверить последние коммиты на соответствие

Ожидание:
- Все коммиты следуют Conventional Commits
- Есть feat, fix, docs типы
- Сообщения на русском языке

Проверка:
$ git log --oneline -10
a77b538 feat: Обновлены skill-update и instruction-create
d3c0f0e feat: Создан скилл issue-review...

Соответствие: ✅ 100%

Статус: ✅ Passed
```

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

**Автоопределение scope:** При указании пути `.claude/*` скиллы автоматически работают в режиме `claude` (тестирование скиллов и инструкций).

---

## FAQ / Troubleshooting

### Как отладить падающий тест скилла?

1. Запустить тест с `--verbose`:
   ```
   /test-execute .claude/skills/{skill}/SKILL.md --verbose
   ```
2. Проверить, что ожидания в тесте соответствуют текущему поведению скилла
3. Выполнить шаги теста вручную и сравнить результат
4. Проверить, не изменился ли скилл после создания теста

### Как перезапустить только failed тесты?

```
/test-execute --scope claude --only-failed
```

Или указать конкретные скиллы:
```
/test-execute .claude/skills/issue-create/SKILL.md .claude/skills/doc-update/SKILL.md
```

### Какой минимальный coverage для скиллов?

| Уровень | Coverage | Когда достаточно |
|---------|----------|------------------|
| Минимум | 50% | Новый скилл, базовая проверка |
| Норма | 70% | Стабильный скилл |
| Идеал | 90%+ | Критичный скилл (issue-*, skill-*) |

### Как предотвратить flaky тесты?

1. **Избегать зависимости от времени** — не проверять точные даты
2. **Изолировать тесты** — каждый тест независим
3. **Не полагаться на порядок** — тесты могут выполняться в любом порядке
4. **Проверять стабильность** — запустить тест 3 раза подряд перед коммитом

### Scope определён неверно — что делать?

**Симптом:** Скилл запустился в режиме `project` вместо `claude` (или наоборот).

**Решение:** Указать scope явно:
```
/test-create .claude/skills/my-skill/SKILL.md --scope claude
/test-execute .claude/skills/my-skill/SKILL.md --scope claude
```

**Причины неверного определения:**
- Путь не начинается с `.claude/` → определяется как `project`
- Опечатка в пути

### Как версионировать тесты?

Тесты claude-скиллов версионируются вместе со скиллом:
- Тест в SKILL.md — одна версия в git
- Отдельный `tests.md` — отдельный файл в git

**Правило:** При изменении скилла обновлять тест в том же коммите.

```bash
git add .claude/skills/{skill}/SKILL.md
git commit -m "feat: обновлён {skill} + тесты"
```

**Откат к предыдущей версии:**
```bash
git checkout HEAD~1 -- .claude/skills/{skill}/SKILL.md
```

### Как управлять fixture-файлами для claude-тестов?

**Fixture** — это подготовленные данные или состояние для теста.

**Где хранить:**
```
/.claude/skills/{skill}/
  SKILL.md          # Скилл
  tests.md          # Тесты
  fixtures/         # Fixture-файлы
    sample.md       # Пример входных данных
    expected.md     # Ожидаемый результат
```

**Типы fixtures:**

| Тип | Описание | Пример |
|-----|----------|--------|
| Input | Входные данные для скилла | `fixtures/input.md` |
| Expected | Ожидаемый результат | `fixtures/expected.md` |
| State | Начальное состояние | `fixtures/state.json` |
| Mock | Заглушки для зависимостей | `fixtures/mock-api.json` |

**Использование в тесте:**

```markdown
### Input

Загрузить: [input.md](./fixtures/input.md)

### Expected

Сравнить результат с: [expected.md](./fixtures/expected.md)
```

**Правила:**
1. Fixture должен быть детерминированным (одинаковый результат)
2. Не использовать реальные данные (токены, пароли)
3. Fixture версионируется вместе с тестом

### Как мокировать внешние зависимости (API, DB)?

Claude-тесты работают на уровне скиллов, а не на уровне кода. Мокирование выполняется через подмену поведения.

**Принцип:** Тест описывает ОЖИДАЕМОЕ поведение, а не реальные вызовы.

**Вариант 1: Описательное мокирование**

В тесте указывается, что зависимость вернёт:

```markdown
### Setup (Mocks)

- `gh issue list` → возвращает:
  ```
  #1  [AUTH] Add OAuth  open  service:auth
  #2  [PAY] Fix checkout  closed  service:payment
  ```

- `gh issue view 1` → возвращает:
  ```
  title: [AUTH] Add OAuth
  state: OPEN
  labels: service:auth, feature
  ```
```

**Вариант 2: Fixture-файлы для mock**

```
/.claude/skills/{skill}/fixtures/
  mock-gh-issue-list.txt    # Вывод gh issue list
  mock-gh-issue-view.json   # Вывод gh issue view
```

**Вариант 3: Флаг --mock в скилле**

Некоторые скиллы поддерживают `--mock` для тестирования:

```
/issue-create --mock --service auth "Test issue"
# Не создаёт реальный Issue, но проходит весь workflow
```

**Что мокируется:**

| Зависимость | Как мокировать |
|-------------|----------------|
| GitHub API (gh) | Fixture с выводом команды |
| Файловая система | Fixture с файлами |
| Git состояние | Описание состояния в Setup |
| Внешние API | Не тестируется в claude-тестах |

**Важно:**
- Claude-тесты НЕ выполняют реальные команды автоматически
- Тестировщик (человек или CI) выполняет команды и сравнивает результат
- Для реальных интеграционных тестов используйте [project-testing.md](./project-testing.md)

---

## Интеграция с Git Hooks

Тесты можно автоматизировать через git hooks или Claude Code hooks.

### Pre-commit: быстрые проверки

```bash
# .git/hooks/pre-commit (или claude hooks)
#!/bin/bash

# Запустить smoke тесты критичных скиллов
/test-execute --scope claude --category skill-management --category git --type smoke --auto

# При failed — отменить коммит
if [ $? -ne 0 ]; then
  echo "❌ Тесты не прошли. Коммит отменён."
  exit 1
fi
```

### Pre-push: полные проверки

```bash
# .git/hooks/pre-push
#!/bin/bash

# Запустить все тесты проекта
/test-execute --scope project --type smoke --auto

# При failed — отменить push
if [ $? -ne 0 ]; then
  echo "❌ Тесты не прошли. Push отменён."
  echo "Запустите /test-execute --scope project для деталей."
  exit 1
fi
```

### Claude Code hooks (settings.json)

```json
{
  "hooks": {
    "pre-commit": [
      {
        "command": "/test-execute --scope claude --category skill-management --type smoke --auto",
        "on_failure": "block"
      }
    ]
  }
}
```

### Рекомендации по hooks

| Hook | Что запускать | Время |
|------|---------------|-------|
| `pre-commit` | Smoke тесты критичных скиллов | < 30 сек |
| `pre-push` | Smoke тесты проекта | < 2 мин |
| `post-merge` | Полные тесты (фоном) | Async |

**Важно:**
- Используйте `--auto` чтобы не ждать подтверждений
- Не запускайте полные тесты в pre-commit — это замедлит работу
- Для CI используйте [ci.md](/.claude/instructions/git/ci.md) вместо hooks

---

## Связанные инструкции

- [claude-functional.md](./claude-functional.md) — Функциональное, интеграционное и регрессионное тестирование
- [skills/README.md](/.claude/skills/README.md) — Индекс скиллов, категории
- [agents/README.md](/.claude/agents/README.md) — Индекс агентов
- [project-testing.md](./project-testing.md) — Тестирование проекта (unit, e2e, load)
- [ci.md](/.claude/instructions/git/ci.md) — CI/CD pipeline
