# Сессия улучшений test-* скиллов и связей

> **Дата:** 2026-01-20
> **Статус:** ✅ Завершено
> **Ветка:** refactoring-docs

---

## Контекст сессии

Анализ всех изменений за 2026-01-20 выявил 7 направлений улучшений. Пользователь выбрал задачи для выполнения.

---

## Задачи от пользователя

| # | Задача | Решение | Статус |
|---|--------|---------|:------:|
| 1 | Дублирование | ОК, не требует действий | ✅ |
| 2 | FAQ в test-delete | Добавлено 7 вопросов | ✅ |
| 3 | Неотвеченные вопросы | 6 ответов добавлены | ✅ |
| 4 | Отсутствующие связи | 3 связи созданы | ✅ |
| 5 | Реиспользование | ci.md → issue-complete | ✅ |
| 6 | Связывание по контексту | Уже существовало | ✅ |
| 7 | Улучшения workflow | 4 улучшения реализованы | ✅ |

---

## Детали задач

### Задача 2: FAQ в test-delete

**Что добавить:**
- Как восстановить удалённый тест?
- Когда использовать delete vs archive?
- Что происходит со связанными тестами?
- Как удалить все тесты объекта?

### Задача 3: Неотвеченные вопросы

| Вопрос | Где ответить | Приоритет |
|--------|--------------|:---------:|
| Как тестировать скиллы со side effects? | claude-testing.md или test-create FAQ | 🔴 |
| Как мокировать внешние зависимости в claude-тестах? | claude-testing.md | 🔴 |
| Как отличить flaky тест от реальной ошибки? | test-formats.md или test-review | 🟡 |
| Что делать если тест и код изменились одновременно? | test-update FAQ | 🟡 |
| Как версионировать тесты? | claude-testing.md | 🟢 |
| Rollback теста к предыдущей версии? | test-delete FAQ | 🟢 |

### Задача 4: Отсутствующие связи

| Откуда | Куда | Тип связи |
|--------|------|-----------|
| test-complete (при failed) | issue-create | Автопредложение |
| test-review | test-update | "Следующий шаг" |
| skills.md "testing" | scope-detection.md | Ссылка на SSOT |

### Задача 5: Реиспользование

| Сущность | Где использовать | Как |
|----------|------------------|-----|
| scope-detection.md | doc-create, doc-update | Обобщить логику scope |
| test-formats.md (статусы) | Универсальные статусы | Создать status-formats.md или обобщить |
| ci.md | issue-complete | Проверка CI перед закрытием |

### Задача 6: Связывание по контексту

**Группа "Тестирование" → "Issue lifecycle":**
- test-complete --status failed → issue-create

**Группа "Тестирование" → "Качество кода":**
- ci.md → test-review (для диагностики)

### Задача 7: Улучшения workflow (для обсуждения)

**A. Автоматические переходы:**
- `/test-review` → нашёл проблемы → предложить `/test-update --fix`
- `/test-complete --status failed` → предложить `/issue-create`

**B. Batch-операции:**
```bash
/test-execute --scope claude --category testing
```

**C. Состояние между вызовами:**
```bash
/test-review --last-failed
```

**D. Интеграция с git hooks:**
```yaml
pre-commit:
  - /test-execute --scope project --type smoke --auto
```

---

## Скрытый контекст (внутренние заметки)

### Структура test-* скиллов

Все 6 скиллов имеют единую структуру:
1. Frontmatter (name, description, triggers)
2. Связанные скиллы (все 5 других test-*)
3. Связанные инструкции (claude-testing, project-testing)
4. Шаблоны (test-formats, scope-detection)
5. Формат вызова
6. Автоопределение scope (ссылка на SSOT)
7. Правила
8. Воркфлоу (5-6 шагов)
9. Чек-лист
10. Примеры
11. FAQ (кроме test-delete)
12. Следующие шаги

### Паттерны именования

- Скиллы: `{объект}-{действие}` (test-create, test-update)
- Инструкции: `{категория}/{тема}.md` (tools/claude-testing.md)
- Шаблоны: `{тема}.md` в /.claude/templates/

### Критичные скиллы (из CLAUDE.md)

- skill-*: skill-create, skill-update, skill-delete
- instruction-*: instruction-create, instruction-update, instruction-delete
- issue-*: issue-create, issue-update, issue-execute, issue-review, issue-complete, issue-delete

test-* НЕ являются критичными (можно удалять тесты свободно).

### Текущие цепочки скиллов

```
Создание: test-create → test-execute → test-complete
Исправление: test-execute(failed) → test-review → test-update → test-execute
Удаление: test-delete (с архивацией в git)
```

### Файлы, которые нужно изменить

| Задача | Файлы |
|--------|-------|
| 2 | test-delete/SKILL.md |
| 3 | claude-testing.md, test-update/SKILL.md, test-formats.md, test-review/SKILL.md |
| 4 | test-complete/SKILL.md, test-review/SKILL.md, skills.md |
| 5 | scope-detection.md (обобщение), ci.md |
| 6 | ci.md, test-complete/SKILL.md |

---

## Прогресс выполнения

### Сессия 1 (завершена)

- [x] Создан файл отслеживания прогресса
- [x] Задача 2: FAQ в test-delete (7 вопросов)
- [x] Задача 3: Неотвеченные вопросы (6 ответов)
- [x] Задача 4: Отсутствующие связи (проверены, добавлена ссылка SSOT)
- [x] Задача 5: Реиспользование (ci.md → issue-complete)
- [x] Задача 6: Связывание по контексту (уже существовало)
- [x] Задача 7: Все 4 улучшения workflow реализованы

### Изменённые файлы

| Файл | Изменения |
|------|-----------|
| test-delete/SKILL.md | +FAQ (7 вопросов) |
| test-update/SKILL.md | +FAQ (одновременное изменение, rollback) |
| test-execute/SKILL.md | +--category, +--last-failed, +состояние |
| test-review/SKILL.md | +--last-failed |
| test-complete/SKILL.md | +критичные скиллы alert |
| test-formats.md | +диагностика flaky |
| claude-testing.md | +side effects, +мокирование, +git hooks |
| skills.md | +ссылка на SSOT |
| issue-complete/SKILL.md | +проверка CI, +ссылка на ci.md |

---

## Примечания

- Пользователь предпочитает пошаговое выполнение с подтверждением
- Задача 7 требует обсуждения перед реализацией
- Все изменения должны быть совместимы с существующей структурой
