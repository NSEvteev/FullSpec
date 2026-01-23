---
name: test-create
description: Создание теста с автоопределением scope (claude/project) по пути
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
category: testing
triggers:
  commands:
    - /test-create
  phrases:
    ru:
      - создай тест
      - новый тест
    en:
      - create test
      - new test
---

# Создание теста

Команда для создания теста с автоматическим определением scope по пути.

**Связанные скиллы:**
- [test-update](/.claude/skills/test-update/SKILL.md) — изменение теста
- [test-review](/.claude/skills/test-review/SKILL.md) — проверка полноты теста
- [test-execute](/.claude/skills/test-execute/SKILL.md) — выполнение тестов
- [test-complete](/.claude/skills/test-complete/SKILL.md) — отметка о прохождении
- [test-delete](/.claude/skills/test-delete/SKILL.md) — удаление теста

**Связанные инструкции:**
- [tests/claude-testing.md](/.claude/.instructions/system/tests/claude-testing.md) — тестирование Claude Code
- [tests/project-testing.md](/.claude/.instructions/system/tests/project-testing.md) — тестирование проекта

**Шаблоны:**
- [test-formats.md](/.claude/.instructions/system/tests/formats.md) — форматы тестов, статусы, чек-листы
- [scope-detection.md](/.claude/.instructions/system/shared/scope.md) — определение scope (SSOT)
- [output-formats.md](/.claude/.instructions/.claude/skills/output.md) — форматы вывода (SSOT)
- [workflow-template.md](/.claude/.instructions/.claude/skills/workflow.md) — SSOT структуры воркфлоу

**Utility-скиллы:**
- [environment-check](/.claude/skills/environment-check/SKILL.md) — проверка gh/git перед выполнением
- [input-validate](/.claude/skills/input-validate/SKILL.md) — валидация входных данных

## Оглавление

- [Формат вызова](#формат-вызова)
- [Автоопределение scope](#автоопределение-scope)
- [Правила](#правила)
- [Воркфлоу](#воркфлоу)
  - [Шаг 1: Определить цель теста](#шаг-1-определить-цель-теста)
  - [Шаг 2: Автоопределить scope](#шаг-2-автоопределить-scope)
  - [Шаг 3: Сгенерировать тест](#шаг-3-сгенерировать-тест)
  - [Шаг 4: Создать файл теста](#шаг-4-создать-файл-теста)
  - [Шаг 5: Ревью теста](#шаг-5-ревью-теста)
  - [Шаг 6: Результат](#шаг-6-результат)
- [Чек-лист](#чек-лист)
- [Примеры использования](#примеры-использования)
- [FAQ / Troubleshooting](#faq--troubleshooting)

---

## Формат вызова

```
/test-create [путь-к-объекту] [--scope claude|project] [--type smoke|functional|integration]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь-к-объекту` | Файл или скилл для тестирования | Спросить |
| `--scope` | Принудительно указать scope | Авто по пути |
| `--type` | Тип теста | `smoke` |
| `--dry-run` | Показать план без создания | — |

---

## Автоопределение scope

> **SSOT:** Полная логика определения scope описана в [scope-detection.md](/.claude/.instructions/system/shared/scope.md).

**Принцип:** Один набор скиллов test-* для всех типов тестов. Scope определяется **автоматически по пути**.

**Краткая таблица:**

| Путь начинается с | Scope | Описание |
|-------------------|-------|----------|
| `.claude/*` | `claude` | Тесты скиллов, инструкций, агентов |
| `src/*` | `project` | Тесты кода проекта |
| `tests/*` | `project` | Тесты в папке тестов |
| `shared/*` | `project` | Тесты общего кода |

---

## Правила

### Правило scope

**Правило:** Если путь начинается с `.claude/` — scope автоматически `claude`.

**Правило:** Если путь начинается с `src/`, `tests/`, `shared/` — scope автоматически `project`.

### Правило типа теста

**Правило:** По умолчанию создаётся `smoke` тест — быстрая проверка работоспособности.

| Тип | Назначение | Когда использовать |
|-----|------------|-------------------|
| `smoke` | Базовая проверка работоспособности | После создания, быстрая проверка |
| `functional` | Полная проверка функционала | После изменений, перед релизом |
| `integration` | Проверка взаимодействия | При интеграции компонентов |

### Правило именования файлов тестов

**Scope claude:**
- Раздел в SKILL.md: `## Тестирование`
- Отдельный файл: `{skill}/tests.md`

**Scope project:**
- Формат: `{name}.test.ts` или `{name}.spec.ts`
- Соответствие исходному файлу: `token.ts` → `token.test.ts`

### Правило расположения тестов

**Scope claude:**
- **ВАЖНО:** Каждая папка скилла уже содержит файл `tests.md` с описанием тестов
- Файл: `/.claude/skills/{skill}/tests.md`
- Структура tests.md:
  - Smoke test — базовая проверка
  - Functional tests — детальные сценарии
  - Integration test — взаимодействие с другими скиллами
  - Чек-лист smoke test — быстрые проверки
  - История запусков — результаты выполнения
- При создании теста проверить существующий tests.md:
  - Если тест существует → предложить обновить через `/test-update`
  - Если тест не существует → добавить в tests.md

**Scope project:**
- Unit/integration: рядом с кодом `/src/{service}/tests/`
- E2E: `/tests/e2e/`
- Load: `/tests/load/`

---

## Воркфлоу

### Шаг 1: Определить цель теста

1. Из аргумента: `/test-create .claude/skills/issue-create/SKILL.md`
2. Или спросить: "Что нужно протестировать?"

**Валидация:**
- Путь существует
- Объект тестируемый (скилл, инструкция, код)

### Шаг 2: Автоопределить scope

1. Проверить путь:
   - Начинается с `.claude/` → scope = `claude`
   - Начинается с `src/`, `tests/`, `shared/` → scope = `project`
   - Иначе → спросить пользователя

2. Если указан `--scope` — использовать его

3. Вывести подтверждение:
   ```
   📋 Определён scope

   Объект: .claude/skills/issue-create/SKILL.md
   Scope: claude (авто)
   Тип: smoke

   Продолжить? [Y/n]
   ```

### Шаг 3: Сгенерировать тест

**Для scope = claude (скилл):**

1. Прочитать SKILL.md
2. Извлечь:
   - Триггеры (commands, phrases)
   - Воркфлоу (шаги)
   - Ожидаемые результаты
3. Сгенерировать smoke test:
   - Проверка вызова по команде
   - Проверка вызова по фразе
   - Проверка базового ответа

**Для scope = project (код):**

1. Прочитать файл кода
2. Извлечь:
   - Экспортируемые функции
   - Публичные методы
   - Зависимости
3. Сгенерировать тест:
   - Импорты
   - Тестовые случаи
   - Моки (если нужны)

### Шаг 4: Создать файл теста

**Scope claude:**

1. **Проверить существующий tests.md:**
   ```bash
   ls .claude/skills/{skill}/tests.md
   ```

2. **Если tests.md существует:**
   - Прочитать текущее содержимое
   - Проверить, есть ли нужный тест
   - Если тест есть → предложить `/test-update`
   - Если теста нет → добавить в существующий файл

3. **Если tests.md не существует:**
   - Создать новый файл по шаблону:

```markdown
# Тесты: {skill-name}

> **Scope:** claude
> **Категория:** {category}
> **Критичность:** 🟡 Medium

---

## Smoke test

📋 **Smoke test: {skill-name}**

**Команда:** `/{skill-name}`
**Триггер:** "{фраза}"

**Ожидание:**
- [ ] Скилл запускается без ошибок
- [ ] Запрашивает необходимые параметры
- [ ] Выводит ожидаемый результат

**Результат:** ⬜ Не выполнен
```

**Scope project:**

```typescript
// {path}/tests/{name}.test.ts
import { describe, it, expect } from 'vitest';
import { функция } from '../{file}';

describe('{name}', () => {
  it('should work correctly', () => {
    // arrange
    // act
    // assert
  });
});
```

### Шаг 5: Ревью теста

```
📋 Ревью теста

✅ Покрытие:
- Основной сценарий: ✅
- Граничные случаи: ⬜
- Ошибки: ⬜

💡 Предложения (по приоритету):

🔴 Критично (блокирует качество):
1. Добавить тест на ошибки (обязательно для production)

🟡 Рекомендуется (улучшает покрытие):
2. Добавить тест на невалидные данные
3. Добавить тест на пустой ввод

🟢 По желанию (nice to have):
4. Добавить параметризованные тесты

Применить? [все/критичные/выборочно/пропустить]
```

**Приоритеты предложений:**

| Приоритет | Когда использовать | Пример |
|-----------|-------------------|--------|
| 🔴 Критично | Отсутствует тест ошибок, пропущен критичный сценарий | Нет теста на exception |
| 🟡 Рекомендуется | Улучшает покрытие, edge cases | Тест на граничные значения |
| 🟢 По желанию | Оптимизация, параметризация, стиль | Объединить похожие тесты |

### Шаг 6: Результат

```
✅ Тест создан

Объект: {путь}
Scope: {claude|project}
Тип: {smoke|functional|integration}

Файл теста:
- {путь к тесту}

Следующие шаги:
- Выполнить тест: /test-execute {путь}
- Добавить больше сценариев

Запустить тест сейчас? [Y/n]
```

---

## Чек-лист

- [ ] **Шаг 1:** Получил путь к объекту тестирования
- [ ] **Шаг 2:** Определил scope (claude/project)
- [ ] **Шаг 2:** Определил тип теста (smoke/functional/integration)
- [ ] **Шаг 3:** Прочитал объект тестирования
- [ ] **Шаг 3:** Сгенерировал содержимое теста
- [ ] **Шаг 4:** Создал файл теста
- [ ] **Шаг 5:** Провёл ревью, применил улучшения
- [ ] **Шаг 6:** Вывел результат

---

## Примеры использования

### Пример 1: Smoke test для скилла

**Вызов:**
```
/test-create .claude/skills/issue-create/SKILL.md
```

**Диалог:**
```
📋 Определён scope

Объект: .claude/skills/issue-create/SKILL.md
Scope: claude (авто)
Тип: smoke

Продолжить? [Y/n]
> Y

Генерирую smoke test...

Добавлен раздел "Тестирование" в SKILL.md:

## Тестирование

### Smoke test

📋 Smoke test: issue-create

Команда: /issue-create
Триггер: "создай задачу"

Ожидание:
- Скилл запускается
- Выводит список сервисов для выбора
- Запрашивает заголовок задачи

Результат: ⬜ Не выполнен

✅ Тест создан
```

### Пример 2: Unit test для кода

**Вызов:**
```
/test-create src/auth/services/token.ts --type functional
```

**Диалог:**
```
📋 Определён scope

Объект: src/auth/services/token.ts
Scope: project (авто)
Тип: functional

Продолжить? [Y/n]
> Y

Генерирую functional test...

Создан файл: src/auth/services/tests/token.test.ts

import { describe, it, expect, vi } from 'vitest';
import { generateToken, validateToken } from '../token';

describe('Token Service', () => {
  describe('generateToken', () => {
    it('should generate valid JWT token', () => {
      const payload = { userId: '123' };
      const token = generateToken(payload);
      expect(token).toBeDefined();
      expect(typeof token).toBe('string');
    });
  });

  describe('validateToken', () => {
    it('should validate correct token', () => {
      const token = generateToken({ userId: '123' });
      const result = validateToken(token);
      expect(result.valid).toBe(true);
    });

    it('should reject invalid token', () => {
      const result = validateToken('invalid-token');
      expect(result.valid).toBe(false);
    });
  });
});

✅ Тест создан
```

### Пример 3: Принудительный scope

**Вызов:**
```
/test-create shared/utils/format.ts --scope project --type integration
```

**Результат:**
```
📋 Определён scope

Объект: shared/utils/format.ts
Scope: project (указан явно)
Тип: integration

Создан файл: tests/integration/shared/format.test.ts

✅ Тест создан
```

### Пример 4: Dry-run

**Вызов:**
```
/test-create .claude/skills/doc-create/SKILL.md --dry-run
```

**Результат:**
```
📋 План создания теста (dry-run)

Объект: .claude/skills/doc-create/SKILL.md
Scope: claude
Тип: smoke

Будет создано:
- Раздел "Тестирование" в SKILL.md
- Smoke test с проверками:
  - Вызов по команде /doc-create
  - Вызов по фразе "создай документацию"
  - Проверка запроса пути к файлу

Изменений не внесено (dry-run).
```

---

## FAQ / Troubleshooting

### Scope определён неверно — что делать?

**Симптом:** Скилл создал тест в формате markdown (для claude) вместо `.test.ts` (для project), или наоборот.

**Решение:** Указать scope явно:
```
/test-create .claude/skills/my-skill/SKILL.md --scope claude
/test-create src/auth/token.ts --scope project
```

**Причины неверного определения:**

| Ситуация | Причина | Решение |
|----------|---------|---------|
| Путь не начинается с `.claude/` | Определяется как `project` | Добавить `--scope claude` |
| Путь вне стандартных папок | Неизвестный scope | Явно указать `--scope` |
| Опечатка в пути | Автоопределение не работает | Проверить путь |
| Файл в нестандартной папке | Алгоритм не распознаёт | Явно указать `--scope` |

### Scope claude: Как исправить неверно созданный тест?

**Если создан `.test.ts` вместо раздела в SKILL.md:**

1. Удалить созданный файл:
   ```bash
   rm .claude/skills/{skill}/tests.test.ts
   ```

2. Пересоздать с правильным scope:
   ```
   /test-create .claude/skills/{skill}/SKILL.md --scope claude
   ```

**Если создан раздел, но в неверном формате:**

1. Удалить через `/test-delete`
2. Пересоздать с явными параметрами

### Scope project: Как исправить неверно созданный тест?

**Если создан markdown вместо `.test.ts`:**

1. Удалить созданный markdown:
   ```bash
   rm src/{path}/tests/{name}.md
   ```

2. Пересоздать с правильным scope:
   ```
   /test-create src/{path}/{file}.ts --scope project
   ```

**Если тест создан в неправильной папке:**

1. Переместить файл:
   ```bash
   mv src/{wrong}/tests/{name}.test.ts src/{correct}/tests/
   ```

2. Обновить импорты в тесте

### Как узнать, какой scope будет определён?

Используйте `--dry-run`:
```
/test-create {путь} --dry-run
```

Вывод покажет:
```
📋 План создания теста (dry-run)

Объект: {путь}
Scope: {определённый scope}  ← проверить здесь
Тип: smoke
```

### Когда использовать явный --scope?

| Ситуация | Рекомендация |
|----------|--------------|
| Путь `.claude/*` | Не нужен (авто = claude) |
| Путь `src/*`, `tests/*`, `shared/*` | Не нужен (авто = project) |
| Файл в корне проекта | Указать явно |
| Нестандартная структура | Указать явно |
| Сомнения в определении | Использовать `--dry-run` или указать явно |

---

## Следующие шаги

После создания теста рекомендуется:

```bash
# 1. Проверить, что тест работает
/test-execute {путь-к-тесту}

# 2. Проверить покрытие (опционально)
/test-review {путь-к-тесту}
```

**Типичная цепочка:**
```
/test-create → /test-execute → /test-review → /test-complete
```
