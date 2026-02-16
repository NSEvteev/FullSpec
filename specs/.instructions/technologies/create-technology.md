---
description: Воркфлоу создания per-tech стандарта кодирования — заглушка при Design → WAITING, заполнение при ADR → DONE.
standard: .instructions/standard-instruction.md
standard-version: v1.1
index: specs/.instructions/technologies/README.md
---

# Воркфлоу создания per-tech стандарта

Рабочая версия стандарта: 1.1

Пошаговый процесс создания `standard-{tech}.md` + `validation-{tech}.md` + rule + строки реестра. Двухфазная модель: заглушка при Design → WAITING, заполнение конвенциями при ADR → DONE.

**Полезные ссылки:**
- [Инструкции технологий](./README.md)
- [Стандарт технологий](./standard-technology.md)
- [Технологический реестр](/specs/technologies/README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-technology.md](./standard-technology.md) |
| Валидация | [validation-technology.md](./validation-technology.md) |
| Создание | Этот документ |
| Модификация | [modify-technology.md](./modify-technology.md) |

## Оглавление

- [Принципы](#принципы)
- [Когда создавать](#когда-создавать)
- [Фаза 1: Заглушка (Design → WAITING)](#фаза-1-заглушка-design--waiting)
  - [Шаг 1: Проверить существование](#шаг-1-проверить-существование)
  - [Шаг 2: Создать standard-{tech}.md (заглушка)](#шаг-2-создать-standard-techmd-заглушка)
  - [Шаг 3: Создать validation-{tech}.md (заглушка)](#шаг-3-создать-validation-techmd-заглушка)
  - [Шаг 4: Создать rule](#шаг-4-создать-rule)
  - [Шаг 5: Обновить реестр](#шаг-5-обновить-реестр)
  - [Шаг 6: Валидация](#шаг-6-валидация)
- [Фаза 2: Заполнение (ADR → DONE)](#фаза-2-заполнение-adr--done)
  - [Шаг 7: Заполнить standard-{tech}.md](#шаг-7-заполнить-standard-techmd)
  - [Шаг 8: Заполнить validation-{tech}.md](#шаг-8-заполнить-validation-techmd)
  - [Шаг 9: Обновить Code Map](#шаг-9-обновить-code-map)
  - [Шаг 10: Валидация](#шаг-10-валидация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Двухфазная модель.** Заглушка создаётся при Design → WAITING (декларация выбора технологии). Заполнение конвенциями — при ADR → DONE. Между фазами стандарт существует, rule подключён, но секции § 2-6 — placeholder.

> **Параллельный запуск.** При множестве технологий оркестратор запускает N technology-agent параллельно — по одному на технологию. Каждый агент создаёт полный комплект (standard + validation + rule + реестр).

> **Шаблон — из стандарта.** Использовать шаблоны заглушки из [standard-technology.md § 7.4-7.5](./standard-technology.md#74-шаблон-заглушки-standard-techmd-design--waiting). Запрещено придумывать свой формат.

> **Порядок строго последовательный.** standard → validation → rule. Параллельное создание файлов одной технологии запрещено.

---

## Когда создавать

| Событие | Действие |
|---------|----------|
| Design → WAITING (новая технология в Tech Stack) | Фаза 1: создать заглушки + rule + реестр |
| ADR → DONE (технология финализирована) | Фаза 2: заполнить конвенциями |

**НЕ создавать когда:**
- Технология только для tooling ([standard-technology.md § 4.1](./standard-technology.md#41-когда-не-создавать-per-tech-стандарт))
- Стандарт уже существует (→ [modify-technology.md](./modify-technology.md))
- Design ещё в DRAFT

---

## Фаза 1: Заглушка (Design → WAITING)

### Шаг 1: Проверить существование

Проверить: существует ли `standard-{tech}.md`?

```bash
ls specs/.instructions/technologies/standard-{tech}.md
```

| Результат | Действие |
|-----------|----------|
| Не существует | Продолжить с Шагом 2 |
| Существует | → [modify-technology.md](./modify-technology.md) (обновить колонку "Сервисы" в реестре) |

### Шаг 2: Создать standard-{tech}.md (заглушка)

Создать файл по шаблону заглушки из [standard-technology.md § 7.4](./standard-technology.md#74-шаблон-заглушки-standard-techmd-design--waiting).

**Путь:** `specs/.instructions/technologies/standard-{tech}.md`

**Заполнить:**
- Frontmatter: `description`, `standard`, `standard-version`, `index`, `technology`
- § 1 (Версия и источники): технология, версия, ссылки на документацию (Design знает эти данные)
- § 2-6: placeholder `*Заполняется при ADR → DONE.*`

### Шаг 3: Создать validation-{tech}.md (заглушка)

Создать файл по шаблону заглушки из [standard-technology.md § 7.5](./standard-technology.md#75-шаблон-заглушки-validation-techmd-design--waiting).

**Путь:** `specs/.instructions/technologies/validation-{tech}.md`

**Заполнить:**
- Frontmatter: `description`, `standard`, `standard-version`, `index`, `technology`
- Все секции: placeholder `*Заполняется при ADR → DONE.*`

### Шаг 4: Создать rule

Создать rule по шаблону из [standard-technology.md § 7.3](./standard-technology.md#73-шаблон-rule-для-автозагрузки).

**Путь:** `.claude/rules/{tech}.md`

**Содержимое:**
```markdown
---
description: Автозагрузка стандарта {Technology} при работе с файлами.
globs:
  - {паттерн файлов технологии}
---

При работе с {Technology}-файлами ОБЯЗАТЕЛЬНО следовать:
- [standard-{tech}.md](/specs/.instructions/technologies/standard-{tech}.md)
- [validation-{tech}.md](/specs/.instructions/technologies/validation-{tech}.md)
```

**Определение globs:** Зависит от технологии. Примеры в [standard-technology.md § 6](./standard-technology.md#6-автозагрузка-через-rules).

### Шаг 5: Обновить реестр

Добавить строку в `specs/technologies/README.md`:

```markdown
| {Technology} | {version} | {service} | [standard-{tech}.md](/specs/.instructions/technologies/standard-{tech}.md) | {design-id} |
```

### Шаг 6: Валидация

```bash
python specs/.instructions/.scripts/validate-technology.py specs/.instructions/technologies/standard-{tech}.md --verbose
```

---

## Фаза 2: Заполнение (ADR → DONE)

### Шаг 7: Заполнить standard-{tech}.md

Заменить placeholder в секциях § 2-6 конвенциями кодирования:

| Секция | Содержание |
|--------|-----------|
| § 2 Конвенции именования | Таблица: Элемент, Правило, Пример |
| § 3 Структура кода | Организация модулей, импорты, порядок |
| § 4 Паттерны использования | Рекомендуемые паттерны с примерами |
| § 5 Типичные ошибки | Антипаттерны с примерами правильного кода |
| § 6 Ссылки | Документация, style guides |

**Источники:** ADR содержит технические решения. Официальная документация технологии. [standard-principles.md](/.instructions/standard-principles.md) — не противоречить.

### Шаг 8: Заполнить validation-{tech}.md

Заменить placeholder конкретными правилами:

| Секция | Содержание |
|--------|-----------|
| § 1 Когда валидировать | Условия запуска |
| § 2 Коды ошибок | Таблица: Код, Описание, Severity |
| § 3 Чек-лист | Конкретные проверки |

### Шаг 9: Обновить Code Map

В `architecture/services/{svc}.md` (секция Tech Stack) добавить ссылку на стандарт:

| Технология | Версия | Назначение | Стандарт |
|-----------|--------|------------|---------|
| {Technology} | {version} | {назначение} | [standard-{tech}.md](/specs/.instructions/technologies/standard-{tech}.md) |

### Шаг 10: Валидация

```bash
python specs/.instructions/.scripts/validate-technology.py specs/.instructions/technologies/standard-{tech}.md --verbose
```

---

## Чек-лист

### Фаза 1: Заглушка (Design → WAITING)

- [ ] Проверено: `standard-{tech}.md` не существует
- [ ] `standard-{tech}.md` создан по шаблону заглушки (§ 7.4)
- [ ] § 1 (Версия и источники) заполнен
- [ ] § 2-6 содержат placeholder `*Заполняется при ADR → DONE.*`
- [ ] `validation-{tech}.md` создан по шаблону заглушки (§ 7.5)
- [ ] Rule `.claude/rules/{tech}.md` создан с правильными globs
- [ ] Строка добавлена в `specs/technologies/README.md`
- [ ] Валидация пройдена

### Фаза 2: Заполнение (ADR → DONE)

- [ ] § 2-6 заполнены конвенциями (placeholder заменены)
- [ ] Примеры кода — конкретные, не абстрактные
- [ ] § 5 не противоречит standard-principles.md
- [ ] `validation-{tech}.md` заполнен (коды ошибок, чек-лист)
- [ ] Tech Stack в `architecture/services/{svc}.md` обновлён
- [ ] Валидация пройдена

---

## Примеры

### Фаза 1: Заглушка Python (Design → WAITING)

```bash
# 1. Design design-0001 → WAITING (auth: Python 3.12)

# 2. technology-agent создаёт заглушку
# specs/.instructions/technologies/standard-python.md — по шаблону § 7.4
# specs/.instructions/technologies/validation-python.md — по шаблону § 7.5

# 3. Создать rule
# .claude/rules/python.md — globs: ["src/**/*.py", "tests/**/*.py"]

# 4. Обновить реестр
# specs/technologies/README.md — строка Python

# 5. Валидация
python specs/.instructions/.scripts/validate-technology.py specs/.instructions/technologies/standard-python.md --verbose
```

### Фаза 2: Заполнение Python (ADR → DONE)

```bash
# 1. ADR-0001 → DONE (auth: Python 3.12)

# 2. technology-agent заполняет standard-python.md
# § 2: snake_case для функций, PascalCase для классов...
# § 3: организация пакетов, __init__.py...
# § 4: dataclasses, type hints, async/await...
# § 5: голый except, mutable defaults...
# § 6: PEP 8, PEP 484...

# 3. Заполнить validation-python.md
# Коды ошибок PY001-PY010, чек-лист

# 4. Обновить Code Map
# architecture/services/auth.md → Tech Stack → ссылка на standard-python.md

# 5. Валидация
python specs/.instructions/.scripts/validate-technology.py specs/.instructions/technologies/standard-python.md --verbose
```

---

## Скрипты

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `validate-technology.py` | Валидация per-tech стандарта (шаги 6, 10) | [specs/.instructions/.scripts/validate-technology.py](../../.scripts/validate-technology.py) |

---

## Скиллы

| Скилл | Назначение | Путь |
|-------|------------|------|
| `/technology-create` | Создание per-tech стандарта | [.claude/skills/technology-create/SKILL.md](/.claude/skills/technology-create/SKILL.md) |
