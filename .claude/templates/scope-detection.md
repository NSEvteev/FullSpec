# Scope Detection — единый источник истины

> **SSOT:** Этот файл — единственный источник правил определения scope.
> Все test-* скиллы ДОЛЖНЫ ссылаться на этот файл.

---

## Принцип

Один набор скиллов `test-*` для всех типов тестов. Scope определяется **автоматически по пути**.

---

## Алгоритм определения scope

```
                     /test-* [target]
                            │
            ┌───────────────┼───────────────┐
            │               │               │
      target есть?    --scope указан?   ничего нет
            │               │               │
            ▼               ▼               ▼
     Определить по    Использовать      Спросить:
     ПУТИ target      указанный         [1] claude
                                        [2] project
                                        [3] all
```

---

## Правила определения по пути

### Таблица маппинга путь → scope

| Путь начинается с | Scope | Описание |
|-------------------|-------|----------|
| `.claude/skills/*` | `claude` | Тесты скиллов |
| `.claude/instructions/*` | `claude` | Тесты инструкций |
| `.claude/agents/*` | `claude` | Тесты агентов |
| `.claude/templates/*` | `claude` | Тесты шаблонов |
| `src/*` | `project` | Код проекта |
| `tests/*` | `project` | Папка тестов проекта |
| `shared/*` | `project` | Общий код |
| `config/*` | `project` | Конфигурации |
| `platform/*` | `project` | Инфраструктура |

### Правило по умолчанию

**Если путь не соответствует ни одному паттерну:**
1. Если путь внутри репозитория → `project`
2. Если путь вне репозитория → ошибка

---

## Формат тестов по scope

### Scope: claude

| Объект | Где хранить тест | Формат |
|--------|-----------------|--------|
| Скилл | `{skill}/SKILL.md` раздел "Тестирование" | Markdown |
| Скилл (много тестов) | `{skill}/tests.md` | Markdown |
| Инструкция | `{instruction}.test.md` | Markdown |
| Агент | `{agent}.test.md` | Markdown |

**Типы тестов claude:**
- `smoke` — базовая проверка (вызов скилла, проверка выхода)
- `functional` — полная проверка всех сценариев
- `integration` — проверка цепочек скиллов

### Scope: project

| Объект | Где хранить тест | Формат |
|--------|-----------------|--------|
| Модуль `src/X/Y.ts` | `src/X/Y.test.ts` или `tests/X/Y.test.ts` | TypeScript/Jest |
| Сервис | `tests/integration/*.test.ts` | TypeScript/Jest |
| API | `tests/e2e/*.test.ts` | TypeScript/Jest |

**Типы тестов project:**
- `unit` — изолированные тесты функций
- `integration` — тесты взаимодействия компонентов
- `e2e` — сквозные тесты API
- `smoke` — быстрая проверка после деплоя
- `load` — нагрузочное тестирование

---

## Примеры определения scope

```bash
# Claude scope (автоопределение)
/test-create .claude/skills/test-create
# → scope: claude

/test-execute .claude/instructions/tools/skills.md
# → scope: claude

# Project scope (автоопределение)
/test-create src/auth/validator.ts
# → scope: project

/test-execute tests/integration/
# → scope: project

# Явное указание scope
/test-execute --scope all
# → запустить все тесты обоих scopes

# Без параметров — спросить
/test-execute
# → "Какой scope запустить? [1] claude [2] project [3] all"
```

---

## Связанные скиллы

Все скиллы, использующие scope-detection:

| Скилл | Использует scope |
|-------|-----------------|
| [test-create](/.claude/skills/test-create/SKILL.md) | ✅ При создании теста |
| [test-update](/.claude/skills/test-update/SKILL.md) | ✅ При поиске теста |
| [test-review](/.claude/skills/test-review/SKILL.md) | ✅ При анализе покрытия |
| [test-execute](/.claude/skills/test-execute/SKILL.md) | ✅ При выборе тестов |
| [test-complete](/.claude/skills/test-complete/SKILL.md) | ✅ При обновлении статуса |
| [test-delete](/.claude/skills/test-delete/SKILL.md) | ✅ При поиске теста |

---

## FAQ

### Что делать, если путь неоднозначен?

Если файл может относиться к обоим scopes (например, `.claude/scripts/build.ts`):
1. Приоритет отдаётся **явному указанию** `--scope`
2. Если не указано — **спросить у пользователя**

### Можно ли переопределить scope?

Да, флаг `--scope` имеет приоритет над автоопределением:
```bash
/test-execute .claude/skills/test-create --scope project
# Выполнит project-тесты, несмотря на путь .claude/
```

### Как добавить новый путь в маппинг?

1. Обновить этот файл (scope-detection.md)
2. Все скиллы автоматически получат обновление через ссылку
