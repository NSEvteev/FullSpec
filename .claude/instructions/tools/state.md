---
type: standard
description: Управление состоянием между вызовами скиллов
related:
  - tools/skills.md
  - tools/claude-testing.md
---

# State Management

Правила работы с папкой `/.claude/state/` для хранения состояния между вызовами скиллов.

## Оглавление

- [Назначение](#назначение)
- [Структура папки](#структура-папки)
- [Формат файлов](#формат-файлов)
- [Правила](#правила)
- [Типы состояния](#типы-состояния)
- [Жизненный цикл](#жизненный-цикл)
- [Интеграция со скиллами](#интеграция-со-скиллами)
- [Примеры](#примеры)
- [Автоматизация](#автоматизация)

---

## Назначение

Папка `/.claude/state/` решает проблемы:

| Проблема | Решение через state |
|----------|---------------------|
| Нет истории вызовов скиллов | `skill-history.json` |
| Нельзя откатить изменения | `last-operation.json` |
| Нет кэша между сессиями | `cache/*.json` |
| Нет состояния тестов | `test-results.json` |
| Потеря контекста при перезапуске | Персистентное хранение |

---

## Структура папки

```
/.claude/state/
├── skill-history.json      # История вызовов скиллов
├── last-operation.json     # Последняя операция (для undo)
├── test-results.json       # Результаты последнего запуска тестов
├── locks/                  # Блокировки для concurrent access
│   └── {skill-name}.lock   # Блокировка конкретного скилла
├── cache/                  # Кэш данных
│   ├── skills-index.json   # Кэш индекса скиллов
│   └── references.json     # Кэш перекрёстных ссылок
└── sessions/               # Данные сессий (опционально)
    └── {session-id}.json   # Состояние конкретной сессии
```

---

## Формат файлов

### skill-history.json

История последних N вызовов скиллов.

```json
{
  "version": "1.0",
  "max_entries": 100,
  "entries": [
    {
      "id": "uuid-v4",
      "timestamp": "2026-01-20T14:30:00Z",
      "skill": "skill-create",
      "args": ["my-skill", "--auto"],
      "status": "success",
      "duration_ms": 1250,
      "files_changed": [
        "/.claude/skills/my-skill/SKILL.md",
        "/.claude/instructions/tools/skills.md"
      ]
    }
  ]
}
```

### last-operation.json

Информация для отката последней операции.

```json
{
  "version": "1.0",
  "operation": {
    "id": "uuid-v4",
    "skill": "skill-create",
    "timestamp": "2026-01-20T14:30:00Z",
    "can_undo": true,
    "undo_commands": [
      "rm -rf /.claude/skills/my-skill/",
      "git checkout -- /.claude/instructions/tools/skills.md"
    ],
    "backup_files": {
      "/.claude/instructions/tools/skills.md": "base64-encoded-content"
    }
  }
}
```

### test-results.json

Результаты последнего запуска тестов.

```json
{
  "version": "1.0",
  "last_run": "2026-01-20T14:30:00Z",
  "scope": "claude",
  "summary": {
    "total": 29,
    "passed": 27,
    "failed": 2,
    "skipped": 0
  },
  "failed_tests": [
    {
      "skill": "issue-create",
      "test": "smoke-1",
      "error": "gh: not authenticated"
    }
  ],
  "results": {
    "skill-create": {"status": "passed", "duration_ms": 150},
    "issue-create": {"status": "failed", "duration_ms": 50}
  }
}
```

### locks/{skill-name}.lock

Файл блокировки для предотвращения concurrent access.

```json
{
  "locked_by": "session-id-or-pid",
  "locked_at": "2026-01-20T14:30:00Z",
  "expires_at": "2026-01-20T14:35:00Z",
  "operation": "skill-update"
}
```

---

## Правила

### Правило версионирования

**Правило:** Каждый файл состояния ДОЛЖЕН иметь поле `version` для миграции.

```json
{
  "version": "1.0",
  ...
}
```

### Правило атомарности

**Правило:** Запись в state файлы должна быть атомарной.

**Алгоритм:**
1. Записать во временный файл `{name}.tmp`
2. Проверить валидность JSON
3. Переименовать `{name}.tmp` → `{name}.json`

```bash
# Пример атомарной записи
echo "$json_content" > state/file.tmp
python -m json.tool state/file.tmp > /dev/null && mv state/file.tmp state/file.json
```

### Правило блокировок

**Правило:** Перед изменением общих файлов — проверить и создать lock.

**Алгоритм:**
1. Проверить наличие lock файла
2. Если есть и не истёк — подождать или сообщить об ошибке
3. Создать lock файл
4. Выполнить операцию
5. Удалить lock файл

**Timeout:** 5 минут (по умолчанию)

### Правило очистки

**Правило:** Старые записи удаляются автоматически.

| Файл | Правило очистки |
|------|-----------------|
| skill-history.json | Хранить последние 100 записей |
| cache/*.json | TTL 24 часа |
| locks/*.lock | Удалять истёкшие при каждом доступе |
| sessions/*.json | Удалять старше 7 дней |

### Правило gitignore

**Правило:** Папка `/.claude/state/` добавляется в `.gitignore`.

```gitignore
# Claude state (local, not versioned)
/.claude/state/
```

**Исключение:** Если нужно версионировать состояние — создать отдельную папку `/.claude/state-shared/`.

---

## Типы состояния

### Персистентное (persistent)

Сохраняется между сессиями, не версионируется в git.

| Файл | Назначение |
|------|------------|
| skill-history.json | История вызовов |
| test-results.json | Результаты тестов |
| cache/*.json | Кэш данных |

### Транзиентное (transient)

Существует только во время выполнения операции.

| Файл | Назначение |
|------|------------|
| locks/*.lock | Блокировки |
| last-operation.json | Для undo (перезаписывается) |

### Сессионное (session)

Привязано к конкретной сессии Claude Code.

| Файл | Назначение |
|------|------------|
| sessions/{id}.json | Контекст сессии |

---

## Жизненный цикл

### Создание state файла

```
1. Скилл начинает выполнение
2. Проверка/создание lock (если нужен)
3. Чтение текущего state (если есть)
4. Выполнение операции
5. Обновление state
6. Удаление lock
```

### Чтение state файла

```python
import json
from pathlib import Path

def read_state(filename: str, default: dict = None) -> dict:
    """Безопасное чтение state файла."""
    path = Path(f".claude/state/{filename}")
    if not path.exists():
        return default or {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return default or {}
```

### Запись state файла

```python
import json
from pathlib import Path

def write_state(filename: str, data: dict) -> None:
    """Атомарная запись state файла."""
    path = Path(f".claude/state/{filename}")
    tmp_path = path.with_suffix(".tmp")

    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write to temp file
    tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    # Atomic rename
    tmp_path.rename(path)
```

---

## Интеграция со скиллами

### Как использовать в SKILL.md

В разделе "Воркфлоу" добавить шаг:

```markdown
### Шаг N: Обновить state

1. Прочитать `/.claude/state/skill-history.json`
2. Добавить запись о текущей операции
3. Записать обновлённый файл

> **SSOT:** [state.md](/.claude/instructions/tools/state.md)
```

### Скиллы, использующие state

| Скилл | Файл state | Операция |
|-------|-----------|----------|
| test-execute | test-results.json | Запись результатов |
| test-review | test-results.json | Чтение для --last-failed |
| skill-create | skill-history.json | Запись в историю |
| skill-create | last-operation.json | Для undo |

### Пример интеграции в test-execute

```markdown
### Шаг N: Сохранить результаты

1. Сформировать объект результатов:
   ```json
   {
     "version": "1.0",
     "last_run": "{timestamp}",
     "scope": "{scope}",
     "summary": {...},
     "results": {...}
   }
   ```

2. Записать в `/.claude/state/test-results.json`

3. Вывести summary пользователю
```

---

## Примеры

### Пример 1: Запись в историю после skill-create

```bash
# После успешного создания скилла
cat > .claude/state/skill-history.tmp << 'EOF'
{
  "version": "1.0",
  "max_entries": 100,
  "entries": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2026-01-20T14:30:00Z",
      "skill": "skill-create",
      "args": ["my-skill"],
      "status": "success",
      "duration_ms": 1250,
      "files_changed": [
        "/.claude/skills/my-skill/SKILL.md",
        "/.claude/skills/my-skill/tests.md"
      ]
    }
  ]
}
EOF

mv .claude/state/skill-history.tmp .claude/state/skill-history.json
```

### Пример 2: Чтение результатов для --last-failed

```bash
# test-execute --last-failed читает failed тесты
failed=$(cat .claude/state/test-results.json | python -c "
import sys, json
data = json.load(sys.stdin)
for t in data.get('failed_tests', []):
    print(t['skill'])
")

# Запустить только failed
for skill in $failed; do
    /test-execute $skill
done
```

### Пример 3: Проверка блокировки

```bash
lock_file=".claude/state/locks/skills-index.lock"

if [ -f "$lock_file" ]; then
    expires=$(cat "$lock_file" | python -c "import sys,json; print(json.load(sys.stdin)['expires_at'])")
    if [ "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \< "$expires" ]; then
        echo "❌ skills-index заблокирован другим процессом"
        exit 1
    fi
fi

# Создать блокировку
cat > "$lock_file" << EOF
{
  "locked_by": "$$",
  "locked_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "expires_at": "$(date -u -d '+5 minutes' +%Y-%m-%dT%H:%M:%SZ)",
  "operation": "skill-update"
}
EOF
```

---

## FAQ

### Нужно ли коммитить .claude/state/?

**Нет.** Папка добавляется в `.gitignore`. State специфичен для локальной машины.

### Что делать при corrupted state файле?

Удалить файл — он будет создан заново при следующем использовании:

```bash
rm .claude/state/test-results.json
```

### Как мигрировать при изменении версии формата?

1. Проверить поле `version` при чтении
2. Если версия старая — выполнить миграцию
3. Обновить `version`

```python
def migrate_state(data: dict) -> dict:
    version = data.get("version", "0.0")
    if version == "1.0":
        return data
    if version == "0.9":
        # Миграция с 0.9 на 1.0
        data["new_field"] = "default"
        data["version"] = "1.0"
    return data
```

### Как очистить весь state?

```bash
rm -rf .claude/state/*
```

---

## Автоматизация

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| test-execute | Записывает результаты в test-results.json |
| test-review --last-failed | Читает failed тесты из state |

---

## Связанные инструкции

- [skills.md](skills.md) — индекс скиллов, которые используют state
- [claude-testing.md](claude-testing.md) — тестирование, использует test-results.json
