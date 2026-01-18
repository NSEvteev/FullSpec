# Инструкции для LLM

Индекс всех инструкций проекта.

**Полное описание структуры:** [refactoring.md](/refactoring.md) — раздел «Папка .claude»

## Паттерн

Инструкции для папки `/X/` находятся в `/.claude/instructions/X/`.

| Папка проекта | Инструкции |
|---------------|------------|
| `/src/` | `/.claude/instructions/src/` |
| `/doc/` | `/.claude/instructions/doc/` |
| `/shared/` | `/.claude/instructions/shared/` |
| `/config/` | `/.claude/instructions/config/` |
| `/platform/` | `/.claude/instructions/platform/` |
| `/tests/` | `/.claude/instructions/tests/` |

**Внутренние инструкции** (не зеркалируют корневые папки):
- `/.claude/instructions/git/` — Git workflow, коммиты, issues
- `/.claude/instructions/tools/` — агенты и скиллы

## Структура инструкций

| Папка | Назначение | Статус |
|-------|------------|--------|
| [/src/](./src/) | Правила разработки сервисов | ✓ README |
| [/platform/](./platform/) | Правила инфраструктуры | ✓ README |
| [/tests/](./tests/) | Правила тестирования | ✓ README |
| [/doc/](./doc/) | Правила документации | ✓ README |
| [/shared/](./shared/) | Правила общего кода | ✓ README |
| [/config/](./config/) | Правила конфигураций | ✓ README |
| [/git/](./git/) | Правила Git | ✓ README |
| [/tools/](./tools/) | Инструменты Claude | ✅ |

## Правило использования

При работе с папкой `/X/` — читать `/.claude/instructions/X/README.md`.

**README.md в каждой папке инструкций** — обязательная точка входа при работе с ресурсом.

## Содержимое папок

### /src/ — Правила разработки сервисов

```
/src/
  README.md
  documentation.md              ← правила документирования кода
  /api/                         ← проектирование API
  /data/                        ← форматы данных
  /runtime/                     ← поведение в runtime
  /dev/                         ← разработка
  /security/                    ← безопасность
```

### /platform/ — Правила инфраструктуры

```
/platform/
  README.md
  docker.md                     ← работа с Docker
  caching.md                    ← кэширование
  deployment.md                 ← деплой
  security.md                   ← безопасность инфраструктуры
  /observability/               ← наблюдаемость
```

### /tests/ — Правила тестирования

```
/tests/
  README.md
  e2e.md                        ← e2e тесты
  load.md                       ← нагрузочные тесты
  fixtures.md                   ← тестовые данные
```

### /doc/ — Правила документации

```
/doc/
  README.md
  structure.md                  ← структура документации
```

### /shared/ — Правила общего кода

```
/shared/
  README.md
  contracts.md                  ← контракты
  events.md                     ← события
  libs.md                       ← общие библиотеки
  assets.md                     ← статика
  i18n.md                       ← локализация
```

### /config/ — Правила конфигураций

```
/config/
  README.md
  environments.md               ← окружения
  feature-flags.md              ← флаги функций
```

### /git/ — Правила Git

```
/git/
  README.md
  workflow.md                   ← рабочий процесс
  commits.md                    ← коммиты
  issues.md                     ← задачи
```

### /tools/ — Инструменты Claude

```
/tools/
  skills.md                     ← индекс скиллов
  agents.md                     ← индекс агентов
```
