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
- [tools/claude-testing.md](/.claude/instructions/tools/claude-testing.md) — тестирование Claude Code
- [tools/project-testing.md](/.claude/instructions/tools/project-testing.md) — тестирование проекта

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

**Принцип:** Один набор скиллов test-* для всех типов тестов. Scope определяется автоматически по пути.

```
                    /test-create [target]
                               │
               ┌───────────────┼───────────────┐
               │               │               │
         .claude/*        src/*           tests/*
               │               │               │
               ▼               ▼               ▼
         scope: claude    scope: project  scope: project
```

| Путь | Scope | Описание |
|------|-------|----------|
| `.claude/skills/*` | claude | Тест скилла |
| `.claude/instructions/*` | claude | Тест инструкции |
| `.claude/agents/*` | claude | Тест агента |
| `src/*` | project | Тест кода проекта |
| `tests/*` | project | Тест в папке тестов |
| `shared/*` | project | Тест общего кода |

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
- Тесты описываются в самом SKILL.md в разделе "Тестирование"
- Или в отдельном файле `/.claude/skills/{skill}/tests.md`

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

```markdown
## Тестирование

### Smoke test

```
📋 Smoke test: {skill-name}

Команда: /{skill-name}
Триггер: "{фраза}"

Ожидание:
- Скилл запускается
- Выводит приветствие/описание
- Запрашивает параметры (если нужны)

Результат: ⬜ Не выполнен
```
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

💡 Предложения:
1. Добавить тест на невалидные данные
2. Добавить тест на пустой ввод

Применить? [Y/n/выборочно]
```

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
