# Per-tech скрипты валидации + pre-commit интеграция

Добавление автоматических скриптов валидации кода для каждой технологии (`validate-{tech}-code.py`) и интеграция в pre-commit хуки.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблема](#1-проблема)
  - [2. Решение](#2-решение)
  - [3. Архитектура скриптов](#3-архитектура-скриптов)
  - [4. Именование и расположение](#4-именование-и-расположение)
  - [5. Скрипт validate-postgresql-code.py](#5-скрипт-validate-postgresql-codepy)
  - [6. Скрипт validate-redis-code.py](#6-скрипт-validate-redis-codepy)
  - [7. Pre-commit интеграция](#7-pre-commit-интеграция)
  - [8. Обновление воркфлоу create-technology.md](#8-обновление-воркфлоу-create-technologymd)
  - [9. Обновление standard-technology.md](#9-обновление-standard-technologymd)
  - [10. Обновление technology-agent AGENT.md](#10-обновление-technology-agent-agentmd)
  - [11. Обновление pre-commit.md](#11-обновление-pre-commitmd)
  - [12. Обновление .pre-commit-config.yaml](#12-обновление-pre-commit-configyaml)
  - [13. Затронутые файлы](#13-затронутые-файлы)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** Автоматизация проверки кода на соответствие per-tech стандартам (standard-redis.md, standard-postgresql.md).
**Почему создан:** Файлы validation-{tech}.md определяют коды ошибок (PG001-PG010, RDS001-RDS008) и чек-листы, но никакой скрипт их не enforce-ит. Без автоматизации validation-{tech}.md — мёртвый справочник.
**Связанные файлы:**
- `specs/technologies/validation-redis.md`
- `specs/technologies/validation-postgresql.md`
- `specs/.instructions/technologies/create-technology.md`
- `specs/.instructions/technologies/standard-technology.md`
- `.claude/agents/technology-agent/AGENT.md`
- `.pre-commit-config.yaml`
- `.structure/pre-commit.md`

---

## Содержание

### 1. Проблема

Текущее состояние:

| Артефакт | Статус | Автоматизация |
|----------|--------|---------------|
| `standard-{tech}.md` | Заполнен конвенциями | Rule загружает в Claude |
| `validation-{tech}.md` | Коды ошибок + чек-лист | **Нет скрипта** |
| `validate-technology.py` | Проверяет **формат** standard-{tech}.md | Не проверяет код |

Validation-{tech}.md определяет правила (PG001-PG010, RDS001-RDS008), но:
- Никакой скрипт не проверяет исходный код по этим правилам
- Pre-commit не запускает per-tech валидации
- Ошибки ловятся только при ручном code review

### 2. Решение

Создать per-tech скрипты валидации **кода** и подключить к pre-commit:

```
specs/.instructions/.scripts/
├── validate-technology.py          # Существует: проверяет формат standard-{tech}.md
├── validate-postgresql-code.py     # НОВЫЙ: проверяет .sql файлы по PG001-PG010
└── validate-redis-code.py          # НОВЫЙ: проверяет код по RDS001-RDS008
```

**Принцип:** Один скрипт на одну технологию. Скрипт проверяет **автоматизируемые** правила из validation-{tech}.md. Правила, требующие понимания семантики (PG006 N+1, RDS007 гарантированная доставка), остаются для ручного review / Claude.

### 3. Архитектура скриптов

Каждый `validate-{tech}-code.py`:

```python
#!/usr/bin/env python3
"""
validate-{tech}-code.py — Валидация кода на соответствие standard-{tech}.md.

Использование:
    python validate-{tech}-code.py <файл или папка>
    python validate-{tech}-code.py <файл или папка> --verbose

Проверяет автоматизируемые правила из validation-{tech}.md.
Коды ошибок: {TECH}001-{TECH}NNN (см. validation-{tech}.md).

SSOT:
    - specs/technologies/standard-{tech}.md
    - specs/technologies/validation-{tech}.md
"""
```

**Интерфейс (единый для всех per-tech скриптов):**

| Параметр | Описание |
|----------|----------|
| `path` | Файл .sql/.py или папка |
| `--verbose` | Подробный вывод |
| `--repo` | Корень репозитория (по умолчанию `.`) |

**Возвращает:**
- `0` — все проверки пройдены
- `1` — ошибки валидации

**Паттерн:** Аналогичен `validate-technology.py` — тот же стиль кода, encoding, argparse.

### 4. Именование и расположение

| Артефакт | Путь | Проверяет |
|----------|------|-----------|
| `validate-technology.py` | `specs/.instructions/.scripts/` | Формат standard-{tech}.md (мета) |
| `validate-{tech}-code.py` | `specs/.instructions/.scripts/` | Исходный код на соответствие стандарту |

Суффикс `-code` отделяет валидацию **кода** от валидации **документов**.

### 5. Скрипт validate-postgresql-code.py

**Файлы:** `**/*.sql`, `src/**/database/**`

**Автоматизируемые проверки:**

| Код | Правило | Как проверять |
|-----|---------|---------------|
| PG001 | Таблицы snake_case, множественное число | Regex на CREATE TABLE: имя таблицы snake_case |
| PG002 | Колонки snake_case | Regex на определения колонок |
| PG003 | FK без индекса | Найти FOREIGN KEY, проверить наличие CREATE INDEX на ту же колонку |
| PG004 | TIMESTAMP вместо TIMESTAMPTZ | Regex: `TIMESTAMP` без `TZ` |
| PG005 | SELECT * | Regex: `SELECT\s+\*\s+FROM` |
| PG007 | Формат миграций | Regex на имя файла: `^\d{3}_[a-z0-9_]+\.sql$` |
| PG009 | SQL keywords UPPER CASE | Проверить основные: SELECT, INSERT, UPDATE, DELETE, FROM, WHERE, JOIN, CREATE, ALTER, DROP |

**НЕ автоматизируемые (ручной review):**

| Код | Причина |
|-----|---------|
| PG006 | N+1 требует анализа цикла вокруг запроса |
| PG008 | created_at/updated_at — нужен контекст (не все таблицы требуют) |
| PG010 | Offset vs cursor — зависит от use case |

### 6. Скрипт validate-redis-code.py

**Файлы:** `src/**/redis/**`, `src/**/*.py`, `src/**/*.ts` (файлы, содержащие Redis-операции)

**Автоматизируемые проверки:**

| Код | Правило | Как проверять |
|-----|---------|---------------|
| RDS001 | Формат ключей `{service}:{entity}:{id}` | Regex на строковые литералы с Redis-ключами (паттерн коротких ключей без `:`) |
| RDS002 | Inline-конструирование ключей | Regex: f-string/template с `redis.get/set/del` и строковой конкатенацией |
| RDS004 | KEYS вместо SCAN | Regex: вызов `.keys(` или `KEYS ` |
| RDS008 | Отсутствует сервис-префикс | Строковые литералы без `:` в Redis-операциях |

**НЕ автоматизируемые (ручной review):**

| Код | Причина |
|-----|---------|
| RDS003 | TTL — нужен контекст (SET может быть в wrapper с TTL) |
| RDS005 | snake_case хэш-полей — сложно отделить от других строк |
| RDS006 | Большие значения — нужен runtime анализ |
| RDS007 | Pub/Sub для гарантированной доставки — семантика |

### 7. Pre-commit интеграция

Добавить в `.pre-commit-config.yaml`:

```yaml
# 15. Валидация PostgreSQL-кода
- id: postgresql-code-validate
  name: Validate PostgreSQL code
  entry: python specs/.instructions/.scripts/validate-postgresql-code.py
  language: system
  files: \.(sql)$
  pass_filenames: true
  require_serial: true
  stages: [pre-commit]

# 16. Валидация Redis-кода
- id: redis-code-validate
  name: Validate Redis code
  entry: python specs/.instructions/.scripts/validate-redis-code.py
  language: system
  files: (src/.*/redis/|\.py$|\.ts$)
  pass_filenames: true
  require_serial: true
  stages: [pre-commit]
```

**Важно:** Redis-хук срабатывает на `.py`/`.ts` файлы — нужна предварительная фильтрация внутри скрипта (проверять только файлы с Redis-импортами/операциями).

### 8. Обновление воркфлоу create-technology.md

Добавить **Шаг 3.5** между validation-{tech}.md и rule:

```
### Шаг 3.5: Создать validate-{tech}-code.py (опционально)

Если технология имеет автоматизируемые проверки из validation-{tech}.md:

1. Создать `specs/.instructions/.scripts/validate-{tech}-code.py`
2. Реализовать автоматизируемые правила из § 2 validation-{tech}.md
3. Добавить хук в `.pre-commit-config.yaml`
4. Обновить `.structure/pre-commit.md` (таблица хуков)
```

**Принцип:** Шаг опционален. Не все технологии имеют автоматизируемые проверки (например, для CSS конвенций автоматизация нецелесообразна — stylelint/eslint лучше).

### 9. Обновление standard-technology.md

В § 5 добавить подсекцию **5.7. Скрипт валидации кода**:

```markdown
### 5.7. Скрипт валидации кода (опционально)

Для технологий с автоматизируемыми правилами создаётся скрипт
`specs/.instructions/.scripts/validate-{tech}-code.py`:

- Проверяет исходный код на соответствие standard-{tech}.md
- Коды ошибок — из validation-{tech}.md § 2
- Интегрируется в pre-commit через `.pre-commit-config.yaml`
- Не все правила автоматизируемы — семантические проверки остаются для ручного review
```

В § 7 добавить **7.4. Шаблон validate-{tech}-code.py** — каркас скрипта.

В § 8 (чек-лист) добавить опциональный пункт:
```
- [ ] validate-{tech}-code.py создан (если есть автоматизируемые правила)
- [ ] Pre-commit хук добавлен
```

### 10. Обновление technology-agent AGENT.md

В алгоритм режима `create` добавить шаг между rule и реестром:

```markdown
6.5. **Создать validate-{tech}-code.py** (если есть автоматизируемые проверки):
   - Скрипт в `specs/.instructions/.scripts/validate-{tech}-code.py`
   - Реализовать автоматизируемые правила из validation-{tech}.md
   - Добавить хук в `.pre-commit-config.yaml`
```

Обновить секцию "Область работы":
```
- Запись: ..., specs/.instructions/.scripts/validate-{tech}-code.py, .pre-commit-config.yaml, .structure/pre-commit.md
```

### 11. Обновление pre-commit.md

Добавить строки в таблицу "Активные хуки":

```markdown
| `postgresql-code-validate` | PostgreSQL: naming, timestamps, SELECT * | `**/*.sql` |
| `redis-code-validate` | Redis: ключи, KEYS vs SCAN, inline | `src/**/redis/**`, `*.py`, `*.ts` |
```

### 12. Обновление .pre-commit-config.yaml

Добавить 2 новых хука (§ 7 выше).

### 13. Затронутые файлы

| # | Файл | Действие |
|---|------|----------|
| 1 | `specs/.instructions/.scripts/validate-postgresql-code.py` | **Создать** |
| 2 | `specs/.instructions/.scripts/validate-redis-code.py` | **Создать** |
| 3 | `specs/.instructions/technologies/create-technology.md` | Добавить шаг 3.5 |
| 4 | `specs/.instructions/technologies/standard-technology.md` | Добавить § 5.7, § 7.4, обновить § 8 |
| 5 | `.claude/agents/technology-agent/AGENT.md` | Добавить шаг 6.5, обновить scope |
| 6 | `.pre-commit-config.yaml` | Добавить 2 хука |
| 7 | `.structure/pre-commit.md` | Добавить 2 строки в таблицу |
| 8 | `specs/technologies/validation-postgresql.md` | Добавить секцию "Скрипты" (ссылка на validate-postgresql-code.py) |
| 9 | `specs/technologies/validation-redis.md` | Добавить секцию "Скрипты" (ссылка на validate-redis-code.py) |

---

## Решения

- **Суффикс `-code`:** Разделяет `validate-technology.py` (формат документа) и `validate-{tech}-code.py` (код) — избегает путаницы.
- **Опциональность:** Не все технологии нуждаются в скрипте (CSS — используй stylelint, Go — используй golint). Шаг создания скрипта опционален.
- **Pre-фильтрация Redis:** Хук триггерится на `.py`/`.ts`, но скрипт внутри проверяет наличие Redis-импортов, чтобы не шуметь на каждом Python-файле.
- **Расположение:** `specs/.instructions/.scripts/` — единообразно с остальными скриптами валидации.

## Открытые вопросы

*Все вопросы решены.*

- ~~**Generic runner?**~~ **Решение:** Отдельные скрипты на технологию. Каждая технология проверяет разные файлы разными правилами — общий runner усложнит без пользы.
- ~~**Severity?**~~ **Решение:** Все проверки блокируют коммит (exit code 1). Warning из validation-{tech}.md в скрипте тоже ошибка — если правило стоит проверять автоматически, значит оно обязательно.
