---
description: Скилл /release-create — обогащение create-release.md (Шаг 0 analysis chains) + release.yml + скилл-обёртка
type: feature
status: draft
created: 2026-02-24
---

# Скилл /release-create — обогащение инструкции + скилл

Добавить проверку analysis chains (Шаг 0) в create-release.md, создать `.github/release.yml` для группировки PR в Release Notes, создать скилл `/release-create` как обёртку.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Закрытые вопросы](#закрытые-вопросы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** G3 из standard-process.md — нет `/release-create` скилла
**Почему создан:** Инструкция create-release.md (7 шагов, 2 скрипта, 3 примера) полная, но: 1) нет проверки analysis chains перед релизом, 2) `--generate-notes` создаёт плоский список PR без группировки (нет release.yml), 3) нет скилла для интеграции с `/chain` (Task 12).
**Связанные файлы:**
- `/.github/.instructions/releases/create-release.md` — SSOT инструкция (7 шагов)
- `/.github/.instructions/releases/standard-release.md` — стандарт Release (20 секций)
- `/.github/.instructions/releases/validation-release.md` — валидация Release
- `/.github/.instructions/.scripts/validate-pre-release.py` — pre-release скрипт (236 строк)
- `/.github/.instructions/.scripts/validate-post-release.py` — post-release скрипт (303 строк)
- `/.github/labels.yml` — SSOT меток (task, bug, docs, refactor — нет feature)
- `/specs/.instructions/standard-process.md` — § 5 Фаза 6, § 8, § 10 G3

**Предшественник:** Исходный черновик содержал оценку инструкции и best practices. Вывод: инструкция достаточно полная. Этот черновик — план реализации.

---

## Содержание

### Почему скилл, а не агент

| Критерий | Скилл `/release-create` | Агент |
|----------|------------------------|-------|
| Частота вызова | Редко (раз в milestone) | — |
| Интерактивность | Высокая (Release Freeze, подтверждения) | Агенту сложнее взаимодействовать |
| Тяжёлая работа | Нет — скрипты делают валидацию, `gh` делает Release | — |
| Контекст основного LLM | Тратит, но для разовой операции допустимо | Экономит, но overkill для простого workflow |

Релиз — редкая операция с обязательным участием пользователя (Release Freeze, подтверждение версии). Скрипты `validate-pre-release.py` и `validate-post-release.py` выполняют тяжёлую работу. Агент не оправдан — скилл достаточен.

### Архитектура

```
standard-release.md              (правила — что)
       ↓ ссылается
create-release.md                (инструкция — как, 7+1 шагов)
       ↓ SSOT для
/release-create (SKILL.md)       (точка входа — вызывает)
```

### Артефакт 1: Обогащение `create-release.md`

**Путь:** `/.github/.instructions/releases/create-release.md`
**Действие:** Добавить Шаг 0 перед Шагом 1.

#### 1.1. Новый Шаг 0: Проверить analysis chains

Мотивация: сейчас create-release.md начинается с определения версии, но не проверяет готовность analysis chains. Если цепочка в RUNNING — релиз создастся с незавершённой работой.

**Содержание шага:**

```markdown
### Шаг 0: Проверить готовность

**SSOT:** [standard-process.md § 5](../../specs/.instructions/standard-process.md#5-путь-a-happy-path) Фаза 5

Убедиться что все analysis chains для этого Milestone завершены:

1. Получить dashboard:

\```bash
python specs/.instructions/.scripts/chain_status.py dashboard
\```

2. **Все цепочки** привязанные к Milestone должны быть в статусе **DONE**.
3. Если есть цепочки НЕ в DONE → **СТОП**.
   - RUNNING → завершить разработку
   - REVIEW → завершить ревью (`/chain-done`)
   - CONFLICT → разрешить конфликт
   - DRAFT/WAITING → цепочка не запущена

> **Исключение:** Hotfix (`--skip-chains`). При hotfix цепочка может быть в RUNNING — релиз критического фикса не ждёт завершения цепочки.
```

#### 1.2. Обновление TOC и нумерации

- Добавить "Шаг 0: Проверить готовность" в оглавление (перед "Шаг 1: Определить версию")
- Добавить пункт в чек-лист: `- [ ] Analysis chains проверены (все DONE или --skip-chains)`

#### 1.3. Обновление секции "Скиллы"

Заменить `*Нет скиллов.*` на:

```markdown
| Скилл | Назначение |
|-------|------------|
| [/release-create](/.claude/skills/release-create/SKILL.md) | Обёртка этой инструкции |
```

### Артефакт 2: `.github/release.yml`

**Путь:** `.github/release.yml`
**Действие:** Создать.

Кастомизация auto-generated Release Notes (`--generate-notes`). Группировка PR по категориям на основе существующих меток из `labels.yml`.

```yaml
changelog:
  categories:
    - title: "🔧 Tasks"
      labels: [task]
    - title: "🐛 Bug Fixes"
      labels: [bug]
    - title: "📚 Documentation"
      labels: [docs]
    - title: "♻️ Refactoring"
      labels: [refactor]
    - title: "Other Changes"
      labels: ["*"]
```

**Почему эти категории:**
- Метки `task`, `bug`, `docs`, `refactor` — единственные TYPE-метки в `labels.yml`
- Нет метки `feature` — задачи на новую функциональность используют `task`
- Нет метки `breaking-change` — BREAKING CHANGE описывается в footer коммита и Release Notes body
- `"*"` — catch-all для PR без TYPE-метки (не должно быть по стандарту, но safety net)

### Артефакт 3: Скилл `/release-create`

**Путь:** `.claude/skills/release-create/SKILL.md`
**Действие:** Создать через `/skill-create`.

**Конфигурация:**

```yaml
---
name: release-create
description: Создание GitHub Release — проверка chains, pre-release валидация, Release Notes, публикация, CHANGELOG.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.0
index: .claude/.instructions/skills/README.md
ssot: .github/.instructions/releases/create-release.md
version: v1.0
argument-hint: "[--draft] [--skip-tests] [--skip-chains]"
---
```

**Формат вызова:**

```
/release-create              — стандартный Release
/release-create --draft      — Draft Release (публикация позже)
/release-create --skip-tests — Hotfix (пропустить make test)
/release-create --skip-chains — Hotfix (пропустить проверку analysis chains)
```

**Воркфлоу скилла:**

1. Прочитать SSOT: `create-release.md`
2. Выполнить Шаг 0–7 по инструкции
3. Передать параметры: `--draft` → шаг 5, `--skip-tests` → шаг 3, `--skip-chains` → шаг 0

### Интеграция с `/chain` (user-process-guide)

Черновик `2026-02-24-user-process-guide.md` определяет Task 12 (Релиз, опциональный) в TaskList. После создания скилла `/release-create`:

- Task 12 description обновляется: `"Если да → /release-create. SSOT: create-release.md"`
- Скилл уже интегрирован в chain через TaskList — дополнительных изменений не нужно

**Примечание:** user-process-guide ещё не реализован. При его реализации Task 12 будет ссылаться на `/release-create`.

### Порядок создания

| # | Артефакт | Инструмент | Зависимости |
|---|---------|------------|-------------|
| 1 | Обогащение `create-release.md` | Ручное редактирование | — |
| 2 | `.github/release.yml` | Write | — |
| 3 | Скилл `/release-create` | `/skill-create` | ← 1 |
| 4 | Обновление `releases/README.md` | Автоматически (шаг 3) | ← 3 |
| 5 | Обновление `standard-process.md` §8/§10 | Ручное | ← 3 |

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| R1 | Скилл, не агент | Release — редкая интерактивная операция (Release Freeze, подтверждения). Тяжёлую работу делают скрипты. Агент — overkill |
| R2 | Шаг 0 в create-release.md | Проверка analysis chains до релиза. Без этого — риск релиза с незавершённой работой |
| R3 | `--skip-chains` для hotfix | Hotfix не ждёт завершения цепочек — критический фикс важнее |
| R4 | Метка `task` в release.yml, не `feature` | В labels.yml нет метки `feature`. Все задачи типа "новая функциональность" используют `task` |
| R5 | Не создаём `breaking-change` метку | BREAKING CHANGE — в footer коммита и body Release Notes. Для шаблона проекта дополнительная метка — over-engineering |
| R6 | user-process-guide Task 12 → `/release-create` | При реализации `/chain` Task 12 будет вызывать скилл. Пока user-process-guide не реализован — совместимость через SSOT (create-release.md) |

---

## Закрытые вопросы

### Q1. Достаточна ли инструкция create-release.md?

**Ответ: да.** 7 шагов, 2 скрипта валидации, 3 примера, чек-лист из 9 пунктов. Единственный пробел — Шаг 0 (проверка analysis chains). Всё остальное покрыто.

### Q2. Нужен ли Milestone validate перед шагом 1?

**Ответ: нет отдельного вызова.** `validate-pre-release.py` уже проверяет Milestone (E004-E006: существует, закрыт, нет open Issues). Дублирование `/milestone-validate` не даёт пользы.

→ Решение из исходного анализа

### Q3. Нужны ли скрипты validate-pre/post-release.py?

**Ответ: уже существуют.** `validate-pre-release.py` (236 строк, E001-E008) и `validate-post-release.py` (303 строки, E001-E015) реализованы и покрывают все проверки из `validation-release.md`. Создавать не нужно.

### Q4. Как release.yml взаимодействует с --generate-notes?

**Ответ:** GitHub использует `.github/release.yml` автоматически при `--generate-notes`. Если файл есть — PR группируются по категориям из `changelog.categories`. Без файла — плоский список PR.

### Q5. Нужно ли обновлять user-process-guide.md?

**Ответ: нет.** user-process-guide ещё не реализован. При его реализации Task 12 будет ссылаться на `/release-create`. Черновик user-process-guide уже содержит `SSOT: standard-release.md, create-release.md` — совместимость обеспечена.

---

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Обогатить create-release.md — Шаг 0
  description: >
    Драфт: .claude/drafts/2026-02-24-release-create.md (секция "Артефакт 1")
    Добавить в .github/.instructions/releases/create-release.md:
    - Новый Шаг 0 "Проверить готовность" перед Шагом 1:
      chain_status.py dashboard, все цепочки DONE, исключение --skip-chains для hotfix
    - Обновить оглавление: добавить "Шаг 0: Проверить готовность"
    - Обновить чек-лист: добавить пункт "Analysis chains проверены"
    - Обновить секцию "Скиллы": ссылка на /release-create
  activeForm: Обогащаю create-release.md

TASK 2: Создать .github/release.yml
  description: >
    Драфт: .claude/drafts/2026-02-24-release-create.md (секция "Артефакт 2")
    Создать .github/release.yml для кастомизации auto-generated Release Notes.
    Категории из labels.yml: task (Tasks), bug (Bug Fixes), docs (Documentation),
    refactor (Refactoring), * (Other Changes).
  activeForm: Создаю release.yml

TASK 3: Создать скилл /release-create
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-release-create.md (секция "Артефакт 3")
    /skill-create для .claude/skills/release-create/SKILL.md.
    SSOT: .github/.instructions/releases/create-release.md.
    Параметры: --draft, --skip-tests, --skip-chains.
    Воркфлоу: прочитать create-release.md → выполнить шаги 0-7.
  activeForm: Создаю /release-create

TASK 4: Обновить releases/README.md
  blockedBy: [3]
  description: >
    Обновить .github/.instructions/releases/README.md:
    - Добавить ссылку на скилл /release-create
    README обновляется автоматически при создании артефактов, но проверить полноту.
  activeForm: Обновляю releases/README.md

TASK 5: Обновить standard-process.md §8/§10
  blockedBy: [3]
  description: >
    Драфт: .claude/drafts/2026-02-24-release-create.md (секция "Порядок создания", шаг 5)
    Обновить specs/.instructions/standard-process.md:
    - § 8 строка 6.1 Release: добавить /release-create в колонку "Скилл"
    - § 9 Quick Reference Фаза 6: заменить `gh release create` на `/release-create`
    - § 10 G3: отметить как закрытый gap
  activeForm: Обновляю standard-process.md

TASK 6: Обновить CLAUDE.md — отметка выполнения
  blockedBy: [5]
  description: >
    В CLAUDE.md отметить release-create (G3) как [x] выполненный.
  activeForm: Обновляю CLAUDE.md
```
