# Интеграция state в агентов

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Архитектура](#архитектура)
  - [План действий](#план-действий)
  - [Что автоматизируют хуки](#что-автоматизируют-хуки)
  - [Что остаётся на агенте](#что-остаётся-на-агенте)
- [Статус](#статус)

---

## Контекст

Стандарт `standard-state.md` завершён. Необходимо интегрировать правила работы со state в агентов.

**Ключевое решение:** Использовать хуки `SubagentStart` и `SubagentStop` для автоматизации.

**SSOT:** [standard-state.md](/.claude/.instructions/state/standard-state.md)

---

## Содержание

### Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code                             │
├─────────────────────────────────────────────────────────────┤
│  SubagentStart hook                                          │
│  └─> record-agent-start.py                                   │
│      └─> Пишет в agents-status.json (status: running)        │
├─────────────────────────────────────────────────────────────┤
│  Агент работает                                              │
│  └─> Rule core.md секция "State" (автозагрузка)              │
│      └─> Проверяет locks.json перед записью                  │
│      └─> Добавляет блокировки                                │
│      └─> Ведёт лог в agent-{name}-operation.json             │
├─────────────────────────────────────────────────────────────┤
│  SubagentStop hook                                           │
│  └─> cleanup-agent.py                                        │
│      └─> Обновляет agents-status.json (status: completed)    │
│      └─> Удаляет блокировки агента (fallback/страховка)      │
└─────────────────────────────────────────────────────────────┘
```

---

### План действий

#### 1. Создать хуки для субагентов

**Файл:** `.claude/settings.json`

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python ./.claude/hooks/record-agent-start.py"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ./.claude/hooks/cleanup-agent.py"
          }
        ]
      }
    ]
  }
}
```

**Входные данные хуков:**
- `agent_id` — уникальный ID субагента
- `agent_type` — тип агента (Explore, Bash, кастомный)
- `agent_transcript_path` — путь к транскрипту

#### 2. Создать скрипты хуков

**Файл:** `.claude/hooks/record-agent-start.py`
```python
#!/usr/bin/env python3
# Читает stdin JSON с agent_id, agent_type
# Добавляет запись в agents-status.json
```

**Файл:** `.claude/hooks/cleanup-agent.py`
```python
#!/usr/bin/env python3
# Читает stdin JSON с agent_id, agent_type
# Обновляет статус в agents-status.json
# Удаляет блокировки агента из locks.json (fallback — на случай падения/прерывания)
```

#### 3. Добавить правило state в core.md

**Файл:** `.claude/rules/core.md` — добавить секцию "State":

```markdown
**State (для агентов с Edit/Write):** Перед записью — проверить блокировку в `/.claude/state/locks.json`, добавить свою, снять сразу после операции. Вести лог в `agent-{name}-operation.json`. См. [standard-state.md](/.claude/.instructions/state/standard-state.md).
```

> **Решение:** Правило добавлено в core.md вместо отдельного файла — глобальные правила в одном месте.

#### 4. Обновить standard-agent.md

Добавить раздел "Работа со state":
- Ссылка на `standard-state.md`
- Описание хуков (автоматизация)
- Ссылка на rule `core.md` секция "State"

#### 5. Обновить воркфлоу агентов

| Файл | Изменение |
|------|-----------|
| `create-agent.md` | Упомянуть что хуки работают автоматически |
| `validation-agent.md` | Проверка что агент ведёт лог операций |

---

### Что автоматизируют хуки

| Задача | Хук | Скрипт |
|--------|-----|--------|
| Запись статуса "running" | `SubagentStart` | `record-agent-start.py` |
| Запись статуса "completed/failed" | `SubagentStop` | `cleanup-agent.py` |
| Cleanup "забытых" блокировок | `SubagentStop` | `cleanup-agent.py` |

**Важно о блокировках:**
- **Основной механизм:** Агент снимает блокировку **сразу после завершения операции** с файлом (не держит до конца работы)
- **Fallback:** `cleanup-agent.py` — страховка на случай падения/прерывания агента, удаляет "мёртвые" блокировки

**Преимущество:** Гарантированное выполнение cleanup, даже если агент упал.

---

### Что остаётся на агенте

| Задача | Как обеспечить |
|--------|----------------|
| Проверка locks.json перед записью | Rule `core.md` |
| Добавление блокировок | Rule `core.md` |
| **Снятие блокировок сразу после операции** | Rule `core.md` |
| Ведение лога операций | Rule `core.md` |

**Почему нельзя автоматизировать:**
- Хуки не знают, какие файлы агент собирается редактировать
- Хуки не знают, когда агент закончил работу с конкретным файлом
- Лог операций требует контекста (reason)

**Цикл блокировки файла:**
```
1. Проверить locks.json → файл свободен?
2. Добавить блокировку
3. Выполнить операцию (edit/write/delete)
4. Снять блокировку ← СРАЗУ, не ждать конца работы агента
```

---

## Статус

- [x] Завершить `standard-state.md`
- [x] Создать `agents-status.json` и `locks.json`
- [x] Создать `.claude/hooks/record-agent-start.py`
- [x] Создать `.claude/hooks/cleanup-agent.py`
- [x] Добавить хуки в `.claude/settings.json`
- [x] Добавить правило state в `core.md`
- [x] Обновить `standard-agent.md` — раздел "Работа со state"
- [x] Обновить `create-agent.md` — упомянуть хуки
- [x] Обновить `validation-agent.md` — проверка лога операций

**Интеграция завершена: 2026-02-01**
