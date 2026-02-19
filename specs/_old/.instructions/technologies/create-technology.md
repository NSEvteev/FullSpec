---
description: Воркфлоу создания per-tech стандарта кодирования — полный стандарт при Design → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.1
index: specs/.instructions/technologies/README.md
---

# Воркфлоу создания per-tech стандарта

Рабочая версия стандарта: 1.1

Пошаговый процесс создания `standard-{tech}.md` + `validation-{tech}.md` + rule + строки реестра. Стандарт создаётся полностью за один проход при Design → WAITING — это прескриптивный словарь правил, конвенции известны с момента выбора технологии.

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
- [Шаги](#шаги)
  - [Шаг 1: Проверить существование](#шаг-1-проверить-существование)
  - [Шаг 2: Создать standard-{tech}.md](#шаг-2-создать-standard-techmd)
  - [Шаг 3: Создать validation-{tech}.md](#шаг-3-создать-validation-techmd)
  - [Шаг 4: Создать rule](#шаг-4-создать-rule)
  - [Шаг 5: Обновить реестр](#шаг-5-обновить-реестр)
  - [Шаг 6: Валидация](#шаг-6-валидация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Однофазная модель.** Стандарт создаётся полностью при Design → WAITING. Технологический стандарт — словарь правил (naming conventions, patterns, antipatterns). Конвенции использования технологии известны с момента её выбора и не зависят от ADR.

> **Параллельный запуск.** При множестве технологий оркестратор запускает N technology-agent параллельно — по одному на технологию. Каждый агент создаёт полный комплект (standard + validation + rule + реестр).

> **Шаблон — из стандарта.** Использовать шаблоны из [standard-technology.md § 7.1-7.2](./standard-technology.md#71-шаблон-standard-techmd). Запрещено придумывать свой формат.

> **Порядок строго последовательный.** standard → validation → rule. Параллельное создание файлов одной технологии запрещено.

---

## Когда создавать

| Событие | Действие |
|---------|----------|
| Design → WAITING (новая технология в Tech Stack) | Создать полный стандарт + rule + реестр |

**НЕ создавать когда:**
- Технология только для tooling ([standard-technology.md § 4.1](./standard-technology.md#41-когда-не-создавать-per-tech-стандарт))
- Стандарт уже существует (→ [modify-technology.md](./modify-technology.md))
- Design ещё в DRAFT

---

## Шаги

### Шаг 1: Проверить существование

Проверить: существует ли `standard-{tech}.md`?

```bash
ls specs/technologies/standard-{tech}.md
```

| Результат | Действие |
|-----------|----------|
| Не существует | Продолжить с Шагом 2 |
| Существует | → [modify-technology.md](./modify-technology.md) (обновить колонку "Сервисы" в реестре) |

### Шаг 2: Создать standard-{tech}.md

Создать файл по шаблону из [standard-technology.md § 7.1](./standard-technology.md#71-шаблон-standard-techmd).

**Путь:** `specs/technologies/standard-{tech}.md`

**Заполнить все секции:**

| Секция | Содержание |
|--------|-----------|
| § 1 Версия и источники | Технология, версия, ссылки на документацию |
| § 2 Конвенции именования | Таблица: Элемент, Правило, Пример |
| § 3 Структура кода | Организация модулей, импорты, порядок |
| § 4 Паттерны использования | Рекомендуемые паттерны с примерами |
| § 5 Типичные ошибки | Антипаттерны с примерами правильного кода |
| § 6 Ссылки | Документация, style guides |

**Источники:** Официальная документация технологии. Общепринятые best practices. [standard-principles.md](/.instructions/standard-principles.md) — не противоречить.

### Шаг 3: Создать validation-{tech}.md

Создать файл по шаблону из [standard-technology.md § 7.2](./standard-technology.md#72-шаблон-validation-techmd).

**Путь:** `specs/technologies/validation-{tech}.md`

**Заполнить все секции:**

| Секция | Содержание |
|--------|-----------|
| § 1 Когда валидировать | Условия запуска |
| § 2 Коды ошибок | Таблица: Код, Описание, Severity |
| § 3 Чек-лист | Конкретные проверки |

### Шаг 3.5: Создать validate-{tech}-code.py (опционально)

Если технология имеет автоматизируемые проверки из validation-{tech}.md:

1. Создать `specs/.instructions/.scripts/validate-{tech}-code.py`
2. Реализовать автоматизируемые правила из § 2 validation-{tech}.md
3. Добавить хук в `.pre-commit-config.yaml`
4. Обновить `.structure/pre-commit.md` (таблица хуков)

**Принцип:** Шаг опционален. Не все технологии имеют автоматизируемые проверки (CSS — используй stylelint, Go — используй golint). Скрипт проверяет только правила, реализуемые статическим анализом. Семантические проверки остаются для ручного review / Claude.

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
- [standard-{tech}.md](/specs/technologies/standard-{tech}.md)
- [validation-{tech}.md](/specs/technologies/validation-{tech}.md)
```

**Определение globs:** Зависит от технологии. Примеры в [standard-technology.md § 6](./standard-technology.md#6-автозагрузка-через-rules).

### Шаг 5: Обновить реестр

Добавить строку в `specs/technologies/README.md`:

```markdown
| {Technology} | {version} | {service} | [standard-{tech}.md](/specs/technologies/standard-{tech}.md) | {design-id} |
```

### Шаг 6: Валидация

```bash
python specs/.instructions/.scripts/validate-technology.py specs/technologies/standard-{tech}.md --verbose
```

---

## Чек-лист

- [ ] Проверено: `standard-{tech}.md` не существует
- [ ] `standard-{tech}.md` создан, все 6 секций заполнены конвенциями
- [ ] Примеры кода — конкретные, не абстрактные
- [ ] § 5 не противоречит standard-principles.md
- [ ] `validation-{tech}.md` создан (коды ошибок, чек-лист)
- [ ] Rule `.claude/rules/{tech}.md` создан с правильными globs
- [ ] `validate-{tech}-code.py` создан (если есть автоматизируемые правила)
- [ ] Pre-commit хук добавлен (если создан скрипт)
- [ ] Строка добавлена в `specs/technologies/README.md`
- [ ] Валидация пройдена

---

## Примеры

### Создание стандарта Python (Design → WAITING)

```bash
# 1. Design design-0001 → WAITING (auth: Python 3.12)

# 2. technology-agent создаёт полный стандарт
# specs/technologies/standard-python.md — все секции заполнены конвенциями
# specs/technologies/validation-python.md — коды ошибок, чек-лист

# 3. Создать rule
# .claude/rules/python.md — globs: ["src/**/*.py", "tests/**/*.py"]

# 4. Обновить реестр
# specs/technologies/README.md — строка Python

# 5. Валидация
python specs/.instructions/.scripts/validate-technology.py specs/technologies/standard-python.md --verbose
```

---

## Скрипты

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `validate-technology.py` | Валидация per-tech стандарта (шаг 6) | [specs/.instructions/.scripts/validate-technology.py](../.scripts/validate-technology.py) |
| `validate-{tech}-code.py` | Валидация кода на соответствие стандарту (шаг 3.5) | `specs/.instructions/.scripts/validate-{tech}-code.py` |

---

## Скиллы

| Скилл | Назначение | Путь |
|-------|------------|------|
| `/technology-create` | Создание per-tech стандарта | [.claude/skills/technology-create/SKILL.md](/.claude/skills/technology-create/SKILL.md) |
