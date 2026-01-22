# .claude/ — Инструменты Claude Code

Хаб навигации по инструментам Claude Code для проекта.

## Быстрый старт

| Задача | Что делать |
|--------|------------|
| Создать скилл | `/skill-create` |
| Создать инструкцию | `/instruction-create` |
| Создать документацию | `/doc-create` |
| Создать Issue | `/issue-create` |
| Найти правила для /src/ | [instructions/src/](./instructions/src/) |
| Найти правила для /platform/ | [instructions/platform/](./instructions/platform/) |
| Проверить целостность | `/health-check` |

---

## Структура

| Папка | Назначение | Индекс |
|-------|------------|--------|
| [instructions/](./instructions/) | Правила и стандарты | [README.md](./instructions/README.md) |
| [skills/](./skills/) | Автоматизация (37 скиллов) | [README.md](./skills/README.md) |
| [templates/](./templates/) | SSOT шаблоны | [README.md](./templates/README.md) |
| [agents/](./agents/) | Помощники | [README.md](./agents/README.md) |
| [state/](./state/) | Состояние между вызовами | [README.md](./state/README.md) |
| [discussions/](./discussions/) | Дискуссии и заметки | [README.md](./discussions/README.md) |
| [scripts/](./scripts/) | Python скрипты | [README.md](./scripts/README.md) |

---

## Граф зависимостей

### Обзор архитектуры

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLAUDE.md                                  │
│                      (точка входа)                                   │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    /.claude/instructions/                            │
│                                                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │  git/   │  │  tools/ │  │  src/   │  │  doc/   │  │ tests/  │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
└───────┼────────────┼────────────┼────────────┼────────────┼────────┘
        │            │            │            │            │
        ▼            ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      /.claude/skills/                                │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ issue-*  │  │ skill-*  │  │  doc-*   │  │  test-*  │   ...      │
│  │ (7)      │  │ (5)      │  │ (10)     │  │ (7)      │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼─────────────┼─────────────┼──────────────────┘
        │             │             │             │
        └──────────────────┬──────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     /.claude/templates/                              │
│                        (SSOT)                                        │
│                                                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │
│  │ output-formats │  │ error-handling │  │ scope-detection│        │
│  └────────────────┘  └────────────────┘  └────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
```

### Граф скиллов

```
                          ┌─────────────────────────────────────┐
                          │          prompt-update              │
                          │   (мета-скилл, улучшает промты)     │
                          └─────────────┬───────────────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
          ▼                             ▼                             ▼
    skill-* ◄──────────────► instruction-* ◄──────────────► test-*
          │                             │                             │
          │                             │                             │
          ▼                             ▼                             ▼
    links-* ◄────────────────► context-* ◄────────────────► doc-*
          │                             │                             │
          └─────────────────────────────┼─────────────────────────────┘
                                        │
                          ┌─────────────┴─────────────────────────────┐
                          │                                           │
                          ▼                                           ▼
                ┌───────────────────┐                    ┌───────────────────┐
                │    issue-*        │                    │  Utility-скиллы   │
                │ (7 скиллов)       │                    │  input-validate   │
                │                   │                    │  environment-check│
                └───────────────────┘                    └───────────────────┘
```

### Utility-скиллы (используются другими)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        input-validate                                │
│                    (валидация входных данных)                        │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   skill-create      instruction-create       doc-create


┌─────────────────────────────────────────────────────────────────────┐
│                      environment-check                               │
│                   (проверка gh, git, python)                         │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
    ┌─────────────────────────┼─────────────────────────────┐
    │         │         │         │         │         │     │
    ▼         ▼         ▼         ▼         ▼         ▼     ▼
issue-    issue-    issue-    issue-    issue-    issue-  test-
create    update    delete    execute   review    complete execute
```

---

## Цепочки вызовов

### Создание скилла

```
/skill-create
    │
    ├── [Шаг 0] input-validate (название)
    ├── [Шаг 0] environment-check (git)
    │
    ├── [Шаг 4] Write (SKILL.md)
    ├── [Шаг 4] Write (tests.md)
    │
    ├── [Шаг 7] /links-create
    │               │
    │               └── ищет файлы/папки → создаёт ссылки
    │
    ├── [Шаг 9a] /links-update (параллельно)
    │               │
    │               └── обновляет связанные документы
    │
    ├── [Шаг 9b] /skill-update (параллельно)
    │               │
    │               └── обновляет skills/README.md, другие скиллы
    │
    └── [Шаг 11] Результат
```

### Выполнение Issue

```
/issue-execute #123
    │
    ├── [Шаг 0] environment-check (gh, git)
    │
    ├── [Шаг 1] gh issue view #123
    │
    ├── [Шаг 3] git checkout -b feature/123-...
    │
    ├── [Шаг 5] Реализация задачи
    │               │
    │               ├── (опционально) /doc-create
    │               ├── (опционально) /test-create
    │               └── (опционально) /links-update
    │
    ├── [Шаг 6] git commit
    │
    └── [Шаг 7] /issue-review (рекомендуется)
                    │
                    └── /issue-complete
```

### Удаление файла

```
Удаление файла из проекта
    │
    ├── [До удаления] /context-delete
    │                     │
    │                     └── анализирует контекст
    │                         предлагает изменения
    │
    ├── [Удаление] rm файл
    │
    └── [После] /links-delete
                    │
                    └── помечает битые ссылки
                        вызывает /context-update
```

---

## SSOT шаблоны

### Связи шаблонов со скиллами

| Шаблон | Используется в |
|--------|----------------|
| [output-formats.md](./templates/output-formats.md) | ВСЕ 37 скиллов (форматы вывода) |
| [error-handling.md](./templates/error-handling.md) | ВСЕ 37 скиллов (обработка ошибок) |
| [scope-detection.md](./templates/scope-detection.md) | test-*, doc-* (определение scope) |
| [workflow-template.md](./templates/workflow-template.md) | skill-create, instruction-create |

---

## Матрица зависимостей

### Скилл → Вызывает

| Скилл | Вызывает скиллы |
|-------|-----------------|
| skill-create | links-create, skill-update, links-update |
| skill-update | links-update |
| skill-delete | skill-update, links-delete |
| instruction-create | links-create, context-update, instruction-update |
| instruction-update | context-update, links-update, test-update |
| instruction-deactivate | links-delete, context-delete |
| doc-create | links-create |
| doc-update | links-update, context-update |
| doc-delete | links-delete, context-delete |
| links-update | context-update |
| links-delete | context-update |
| issue-review | test-execute (опционально) |
| issue-complete | test-execute (CI check) |

### Скилл → Использует utility

| Скилл | input-validate | environment-check |
|-------|:--------------:|:-----------------:|
| skill-create | ✅ | ✅ |
| instruction-create | ✅ | ✅ |
| doc-create | ✅ | — |
| test-create | ✅ | — |
| issue-create | — | ✅ |
| issue-update | — | ✅ |
| issue-delete | — | ✅ |
| issue-execute | — | ✅ |
| issue-review | — | ✅ |
| issue-complete | — | ✅ |

---

## Категории скиллов

### По объекту управления

| Категория | Скиллы | Количество |
|-----------|--------|------------|
| skill-management | skill-create, skill-update, skill-delete, skill-migrate, skill-report | 5 |
| instruction-management | instruction-create, instruction-update, instruction-deactivate | 3 |
| documentation | doc-create, doc-update, doc-delete, links-create, links-update, links-delete, links-validate, context-update, context-delete, doc-reindex | 10 |
| testing | test-create, test-update, test-review, test-execute, test-complete, test-delete, test-coverage | 7 |
| git | issue-create, issue-update, issue-execute, issue-review, issue-complete, issue-delete, issue-reopen | 7 |
| utility | input-validate, environment-check, health-check | 3 |
| meta | prompt-update | 1 |
| agent-management | agent-create | 1 |

**Всего:** 37 скиллов

---

## Автоматизация

Этот файл обновляется при:
- Создании нового скилла (`/skill-create`)
- Добавлении связей между скиллами
- Изменении структуры `.claude/`

---

## Связанные документы

- [/CLAUDE.md](/CLAUDE.md) — точка входа для Claude Code
- [/README.md](/README.md) — описание проекта
