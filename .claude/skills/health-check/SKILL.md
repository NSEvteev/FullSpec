---
name: health-check
category: utility
trigger: /health-check
description: Проверка целостности проекта Claude
critical: false
---

# /health-check

Комплексная проверка целостности проекта: скиллы, инструкции, ссылки, конфигурация.

## Триггеры

- `/health-check` — полная проверка
- `/health-check --quick` — быстрая проверка (без тестов)
- `/health-check --fix` — исправить найденные проблемы

## Параметры

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--quick` | Быстрая проверка без тестов | false |
| `--fix` | Автоматическое исправление | false |
| `--dry-run` | Показать без изменений | false |
| `--json` | JSON формат вывода | false |
| `--verbose` | Подробный вывод | false |

## Воркфлоу

### Шаг 1: Проверка структуры

1. **Обязательные папки:**
   - `/.claude/skills/` — существует
   - `/.claude/.instructions/` — существует
   - `/.claude/templates/` — существует

2. **Обязательные файлы:**
   - `CLAUDE.md` — существует
   - `/.claude/.instructions/README.md` — существует
   - `/.claude/skills/README.md` — существует

### Шаг 2: Проверка скиллов

Для каждого скилла в `/.claude/skills/*/`:

1. **Структура:**
   - [ ] SKILL.md существует
   - [ ] tests.md существует

2. **SKILL.md валидность:**
   - [ ] Frontmatter корректный (YAML)
   - [ ] Поля name, category, trigger заполнены
   - [ ] Trigger соответствует имени папки

3. **Регистрация:**
   - [ ] Скилл есть в skills.md

### Шаг 3: Проверка инструкций

Для каждой инструкции в `/.claude/.instructions/**/*.md`:

1. **Frontmatter:**
   - [ ] type указан (standard/project)
   - [ ] description заполнен
   - [ ] related — массив

2. **Регистрация:**
   - [ ] Инструкция есть в README.md

### Шаг 4: Проверка ссылок

Вызвать `/links-validate --json` и проанализировать результат.

### Шаг 5: Проверка SSOT

1. **Шаблоны существуют:**
   - [ ] output-formats.md
   - [ ] error-handling.md
   - [ ] scope-detection.md

2. **Ссылки на SSOT:**
   - [ ] Скиллы ссылаются на SSOT

### Шаг 6: Формирование отчёта

```
📋 Health Check Report

┌─────────────────────────────────────────────┐
│ Компонент          │ Статус │ Проблем │
├─────────────────────────────────────────────┤
│ Структура          │ ✅     │ 0       │
│ Скиллы (29)        │ ✅     │ 0       │
│ Инструкции (53)    │ ⚠️     │ 2       │
│ Ссылки (342)       │ ❌     │ 5       │
│ SSOT               │ ✅     │ 0       │
└─────────────────────────────────────────────┘

Общий статус: ⚠️ Требует внимания

Проблемы:
1. [WARN] Инструкция не в README: /tests/new.md
2. [WARN] Инструкция без раздела "Скиллы": /src/api/design.md
3. [ERROR] Битая ссылка: /doc/api.md:42
...

Используйте /health-check --fix для исправления
```

### Шаг 7: Исправление (--fix)

Если `--fix`:

1. Для каждой исправимой проблемы:
   - Предложить решение
   - Применить или запросить подтверждение

2. Типы автоисправлений:
   - Добавить скилл в skills.md
   - Добавить инструкцию в README.md
   - Исправить битые ссылки (через /links-validate --fix)

### Шаг 8: Результат

**Всё в порядке:**
```
✅ Health Check: OK

Проверено:
- Скиллов: 29
- Инструкций: 53
- Ссылок: 342

Все проверки пройдены.
```

**Есть проблемы:**
```
⚠️ Health Check: {N} проблем

Критичных: {K}
Предупреждений: {M}

Используйте /health-check --verbose для деталей
Используйте /health-check --fix для исправления
```

---

## Примеры использования

### Полная проверка

```
/health-check
```

### Быстрая проверка (CI)

```
/health-check --quick
```

### Исправление проблем

```
/health-check --fix
```

### JSON для CI

```
/health-check --json
```

**Результат:**
```json
{
  "status": "warning",
  "components": {
    "structure": {"status": "ok", "issues": 0},
    "skills": {"status": "ok", "issues": 0, "count": 29},
    "instructions": {"status": "warning", "issues": 2, "count": 53},
    "links": {"status": "error", "issues": 5, "count": 342},
    "ssot": {"status": "ok", "issues": 0}
  },
  "issues": [
    {"level": "error", "component": "links", "message": "..."}
  ]
}
```

---

## Интеграция с CI

```yaml
# .github/workflows/health-check.yml
jobs:
  health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Health Check
        run: claude /health-check --quick --json > health.json
      - name: Check status
        run: |
          status=$(cat health.json | jq -r '.status')
          if [ "$status" = "error" ]; then
            exit 1
          fi
```

---

## Связи с другими скиллами

| Скилл | Связь |
|-------|-------|
| `/links-validate` | Вызывается для проверки ссылок |
| `/doc-reindex` | Может исправить проблемы с README |
| `/test-execute` | Опционально запускает тесты |

---

## FAQ

### Как часто запускать?

- В CI — при каждом PR (--quick)
- Локально — после больших изменений
- Периодически — раз в неделю полная проверка

### Что значит "критичная" проблема?

Проблема, которая может привести к некорректной работе скиллов:
- Отсутствующий SKILL.md
- Битая ссылка в CLAUDE.md
- Невалидный frontmatter

### Можно ли игнорировать предупреждения?

Да, но не рекомендуется. Предупреждения указывают на потенциальные проблемы.

---

## SSOT

- [output-formats.md](/.claude/.instructions/.claude/skills/output.md) — формат вывода
- [error-handling.md](/.claude/.instructions/.claude/skills/errors.md) — обработка ошибок
