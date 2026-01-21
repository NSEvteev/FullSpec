---
name: skill-migrate
category: skill-management
trigger: /skill-migrate
description: Переименование скилла с обновлением всех ссылок
critical: true
---

# /skill-migrate

Безопасное переименование или перемещение скилла в другую категорию с автоматическим обновлением всех ссылок и зависимостей.

## Триггеры

- `/skill-migrate <old-name> <new-name>` — переименовать скилл
- `/skill-migrate <old-name> --category <new-category>` — переместить в другую категорию

## Параметры

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<old-name>` | Текущее имя скилла | Да |
| `<new-name>` | Новое имя скилла | Да (если не --category) |
| `--category` | Новая категория | Нет |
| `--dry-run` | Показать план без изменений | Нет |
| `--json` | JSON формат вывода | Нет |
| `--verbose` | Подробный вывод | Нет |

## Воркфлоу

### Шаг 0: Проверки

1. **input-validate:**
   - `old-name` — существующий скилл
   - `new-name` — валидное имя (kebab-case, не занято)

2. **Проверка критичности:**
   - Если скилл критичный — предупреждение

### Шаг 1: Анализ зависимостей

1. Найти все файлы, ссылающиеся на скилл:
   ```
   Grep: /old-name
   Grep: old-name
   Grep: /.claude/skills/old-name/
   ```

2. Вывести список зависимостей:
   ```
   📋 Зависимости скилла old-name

   Ссылки на скилл:
   - /.claude/skills/README.md:42
   - /.claude/skills/other-skill/SKILL.md:15
   - /CLAUDE.md:123

   Всего: {N} файлов
   ```

### Шаг 2: Подтверждение (--dry-run или интерактив)

```
⚠️ Миграция скилла

Было: /old-name
Станет: /new-name

Будет изменено:
- /.claude/skills/old-name/ → /.claude/skills/new-name/
- {N} файлов с ссылками

Продолжить? [Y/n]
```

### Шаг 3: Переименование папки

1. Создать новую папку:
   ```bash
   mkdir /.claude/skills/new-name/
   ```

2. Скопировать файлы с обновлением:
   - SKILL.md — обновить name, trigger
   - tests.md — скопировать

3. Проверить корректность

4. Удалить старую папку

### Шаг 4: Обновление ссылок

1. Вызвать `/links-update --old-name old-name --new-name new-name`

2. Обновить:
   - `/.claude/skills/README.md`
   - Все скиллы, вызывающие old-name
   - CLAUDE.md если есть ссылки

### Шаг 5: Обновление категории (если --category)

1. Обновить поле `category` в SKILL.md
2. Обновить группировку в skills.md

### Шаг 6: Валидация

1. Проверить новый скилл:
   - Файлы существуют
   - SKILL.md валиден
   - tests.md существует

2. Запустить `/links-validate /.claude/skills/new-name/`

### Шаг 7: Результат

**Успех:**
```
✅ Скилл мигрирован успешно

Было: /old-name (category: old-category)
Стало: /new-name (category: new-category)

Обновлено файлов: {N}

Следующие шаги:
- Проверить работу скилла: /new-name --help
- Запустить тесты: /test-execute new-name
```

**Ошибка:**
```
❌ Ошибка миграции

Причина: {описание}
Состояние: Откат выполнен, изменения отменены

Решение: {рекомендация}
```

---

## Примеры использования

### Переименование скилла

```
/skill-migrate my-old-skill my-new-skill
```

### Перемещение в другую категорию

```
/skill-migrate utility-skill --category documentation
```

### Предварительный просмотр

```
/skill-migrate my-skill new-name --dry-run
```

**Результат:**
```
📋 Предварительный просмотр (--dry-run)

Будет переименовано:
- /.claude/skills/my-skill/ → /.claude/skills/new-name/

Будет обновлено:
- /.claude/skills/README.md
- /.claude/skills/other-skill/SKILL.md

ℹ️ Изменения НЕ применены (--dry-run)
```

---

## Связи с другими скиллами

| Скилл | Связь |
|-------|-------|
| `/skill-create` | Создание нового скилла |
| `/skill-delete` | Удаление скилла |
| `/skill-update` | Обновление существующих скиллов |
| `/links-update` | Вызывается для обновления ссылок |
| `/links-validate` | Вызывается для проверки |

---

## FAQ

### Можно ли откатить миграцию?

Да, используйте `/skill-migrate new-name old-name` — обратная миграция.

### Что если скилл критичный?

Миграция критичных скиллов требует дополнительного подтверждения и автоматически создаёт Issue для отслеживания.

### Обновляются ли тесты?

Да, tests.md копируется и проверяется после миграции.

---

## SSOT

- [output-formats.md](/.claude/instructions/skills/output.md) — формат вывода
- [error-handling.md](/.claude/instructions/skills/errors.md) — обработка ошибок
