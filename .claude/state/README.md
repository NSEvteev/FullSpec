---
description: Управление состоянием между вызовами скиллов и агентов
standard: .claude/.instructions/state/standard-state.md
index: .claude/.instructions/state/README.md
---

# /.claude/state/

Папка для хранения состояния между вызовами скиллов и агентов.

**Полезные ссылки:**
- [Стандарт state](/.claude/.instructions/state/standard-state.md)
- [Инструкции state](/.claude/.instructions/state/README.md)
- [.claude/](/.claude/README.md)

---

## Назначение

| Проблема | Решение через state |
|----------|---------------------|
| Нет истории вызовов скиллов | `skill-history.json` |
| Нельзя откатить изменения | `last-operation.json` |
| Нет кэша между сессиями | `cache/*.json` |
| Нет состояния тестов | `test-results.json` |
| Потеря контекста при перезапуске | Персистентное хранение |

---

## Структура

```
/.claude/state/
├── skill-history.json      # История вызовов скиллов
├── last-operation.json     # Последняя операция (для undo)
├── test-results.json       # Результаты тестов
├── locks/                  # Блокировки
├── cache/                  # Кэш данных
└── sessions/               # Данные сессий
```

---

## Правила

**Полные правила:** см. [standard-state.md](/.claude/.instructions/state/standard-state.md)

Краткий список:
- **Версионирование:** каждый файл имеет поле `version`
- **Атомарность:** запись через временный файл
- **Блокировки:** lock-файлы для concurrent access
- **Очистка:** автоматическое удаление старых данных
- **gitignore:** папка не версионируется

---

## FAQ

### Нужно ли коммитить .claude/state/?

**Нет.** Папка добавляется в `.gitignore`. State специфичен для локальной машины.

### Что делать при corrupted state файле?

Удалить файл — он будет создан заново:

```bash
rm .claude/state/test-results.json
```

### Как очистить весь state?

```bash
rm -rf .claude/state/*
```
