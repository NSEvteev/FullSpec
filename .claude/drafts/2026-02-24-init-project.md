# Воркфлоу инициализации проекта — инструкция + скилл

Единый процесс инициализации нового проекта, объединяющий три разрозненных процесса в один.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G1 из standard-process.md — Фаза 0 разрозненна, три процесса без оркестратора
**Почему создан:** Определить формат инструкции и скилла `/init-project` перед реализацией
**Связанные файлы:**
- `specs/.instructions/standard-process.md` — §4 Фаза 0
- `/.github/.instructions/standard-github-workflow.md` — §2 Фаза 0: Подготовка инфраструктуры
- `specs/.instructions/docs/standard-docs.md` — §7 Жизненный цикл (минимальный стартовый набор)
- `/.structure/initialization.md` — make setup

## Содержание

### Проблема

Фаза 0 состоит из трёх независимых шагов, каждый со своим SSOT:

| # | Шаг | SSOT | Текущий способ |
|---|-----|------|----------------|
| 0.1 | Настройка GitHub | standard-github-workflow.md §2 | Ручной: labels, issue templates, PR template, CODEOWNERS, Actions, Security — всё по отдельности |
| 0.2 | Настройка docs/ | standard-docs.md §7 | Ручной: создание README, .system/, .technologies/, примеров |
| 0.3 | Настройка среды | initialization.md | `make setup` |

Нет единой точки входа. Пользователь должен знать о трёх процессах и выполнять их вручную.

### Артефакты

По архитектуре проекта: **инструкция (SSOT) → скилл (обёртка)**. Скилл без SSOT-инструкции запрещён.

| # | Артефакт | Путь | Назначение |
|---|---------|------|------------|
| 1 | **Воркфлоу-инструкция** (SSOT) | `/.structure/.instructions/create-initialization.md` | Пошаговый процесс инициализации — шаги, чек-лист, примеры |
| 2 | **Скилл** (обёртка) | `/.claude/skills/init-project/SKILL.md` | Ссылка на SSOT, формат вызова `/init-project` |

Инструкция регистрируется в `/.structure/.instructions/README.md`.

> **Расположение:** `.structure/.instructions/` — потому что инициализация относится к структуре проекта, а не к GitHub или specs.

### Порядок создания

1. `/instruction-create create-initialization --path .structure/.instructions/` — инструкция
2. `/skill-create init-project` — скилл, SSOT → create-initialization.md

### Предлагаемая связка

**Инструкция:** `create-initialization.md` (SSOT — шаги, чек-лист, примеры)
**Скилл:** `/init-project` (обёртка — ссылка на SSOT, формат вызова)
**Тип:** Оркестратор (вызывает существующие скиллы и команды)

### Шаги инструкции (create-initialization.md)

```
/init-project [--skip-github] [--skip-docs] [--skip-setup]
```

| Шаг | Действие | Детали | Скилл/Команда |
|-----|---------|--------|---------------|
| 1 | Проверить prerequisites | Python 3.8+, pre-commit, gh, git | `python --version`, `pre-commit --version`, `gh --version` |
| 2 | Проверить gh auth | `gh auth status` | Если не авторизован — стоп с инструкцией |
| 3 | Настройка GitHub Labels | Создать/синхронизировать labels по labels.yml | `/labels-modify` |
| 4 | Настройка GitHub Security | Напомнить включить Dependabot, Secret Scanning (Settings не автоматизируются) | Вывод инструкции |
| 5 | Настройка Branch Protection | Предложить настроить через gh api | Вывод инструкции или `gh api` |
| 6 | Настройка docs/ | Стартовый набор: README, .system/, .technologies/ | Проверить наличие, создать недостающие |
| 7 | make setup | Pre-commit hooks, зависимости | `make setup` |
| 8 | Проверка | `pre-commit run --all-files` | Должно пройти |
| 9 | Отчёт | Что настроено, что нужно настроить вручную (Security Settings) | Вывод |

### Поведение при частичном выполнении

Скилл должен быть **идемпотентным**: если что-то уже настроено — пропустить с сообщением. Это позволяет запускать повторно для проверки.

### Зависимости от существующих скиллов

| Скилл | Для чего |
|-------|---------|
| `/labels-modify` | Шаг 3: создание labels |
| `/milestone-create` | Опционально: создание первого milestone |

### Что НЕ входит в скилл

- Создание сервисов (`/service-create`) — это Фаза 1, шаг 1.2 (Design → WAITING)
- Создание per-tech стандартов (`/technology-create`) — это Фаза 1, шаг 1.2
- Создание analysis chain — это `/discussion-create` (после инициализации)

## Решения

- **Инструкция → скилл:** create-initialization.md (SSOT) → /init-project (обёртка), по архитектуре проекта
- Скилл является оркестратором — не дублирует логику, вызывает существующие инструменты
- Шаги 4-5 (Security, Branch Protection) не полностью автоматизируемы — скилл выводит инструкции
- Issue Templates, PR Template, CODEOWNERS, Actions — уже в template, скилл проверяет наличие

## Открытые вопросы

- Нужно ли создавать первый Milestone в рамках инициализации?
- Как обрабатывать случай когда GitHub repo ещё не создан (только локальный git)?
- Нужен ли `--interactive` режим с пошаговым подтверждением каждого шага?
