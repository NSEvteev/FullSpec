---
description: Валидация per-tech стандартов кодирования — frontmatter, секции, rule, реестр, режим заглушки.
standard: .instructions/standard-instruction.md
standard-version: v1.1
index: specs/.instructions/technologies/README.md
---

# Валидация per-tech стандартов

Рабочая версия стандарта: 1.1

Проверка файлов `specs/.instructions/technologies/standard-{tech}.md` и `validation-{tech}.md` на соответствие [standard-technology.md](./standard-technology.md).

**Полезные ссылки:**
- [Инструкции технологий](./README.md)
- [Технологический реестр](/specs/technologies/README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-technology.md](./standard-technology.md) |
| Валидация | Этот документ |
| Создание | [create-technology.md](./create-technology.md) |
| Модификация | [modify-technology.md](./modify-technology.md) |

## Оглавление

- [Когда валидировать](#когда-валидировать)
- [Шаги](#шаги)
  - [Шаг 0: Автоматическая валидация](#шаг-0-автоматическая-валидация)
  - [Шаг 1: Frontmatter](#шаг-1-frontmatter)
  - [Шаг 2: Обязательные секции](#шаг-2-обязательные-секции)
  - [Шаг 3: Содержание секций](#шаг-3-содержание-секций)
  - [Режим заглушки](#режим-заглушки-если-секции-2-6-содержат-placeholder)
  - [Шаг 4: Rule](#шаг-4-rule)
  - [Шаг 5: Реестр](#шаг-5-реестр)
- [Чек-лист](#чек-лист)
- [Типичные ошибки](#типичные-ошибки)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Когда валидировать

| Момент | Как |
|--------|-----|
| После создания/обновления `standard-{tech}.md` | `python specs/.instructions/.scripts/validate-technology.py {путь}` |
| После создания/обновления `validation-{tech}.md` | Ручная проверка по чек-листу |
| При code review | Проверить чек-лист |

---

## Шаги

### Шаг 0: Автоматическая валидация

```bash
python specs/.instructions/.scripts/validate-technology.py specs/.instructions/technologies/standard-{tech}.md --verbose
```

Скрипт проверяет правила TECH001-TECH010. Автоматически определяет заглушка/полный по наличию placeholder в § 2-6. Если валидация пройдена — **готово**.

**Если скрипт недоступен** — выполнить шаги 1-5 вручную.

### Шаг 1: Frontmatter

Проверить frontmatter файла `standard-{tech}.md`:

| Поле | Правило | Код |
|------|---------|-----|
| `description` | Присутствует, формат "Стандарт кодирования {Technology} — ..." | TECH001 |
| `standard` | `.instructions/standard-instruction.md` | TECH002 |
| `standard-version` | Формат `vX.Y` | TECH002 |
| `index` | `specs/.instructions/technologies/README.md` | TECH002 |
| `technology` | Присутствует, kebab-case | TECH003 |

### Шаг 2: Обязательные секции

Проверить наличие **6 обязательных секций** (заголовки `##`) в `standard-{tech}.md`:

| # | Секция (заголовок `##`) | Код |
|---|------------------------|-----|
| 1 | Версия и источники | TECH004 |
| 2 | Конвенции именования | TECH004 |
| 3 | Структура кода | TECH004 |
| 4 | Паттерны использования | TECH004 |
| 5 | Типичные ошибки | TECH004 |
| 6 | Ссылки | TECH004 |

Секции должны идти **строго в указанном порядке** (TECH005).

### Шаг 3: Содержание секций

**Версия и источники:**
- Таблица с колонками: Параметр, Значение (TECH006)
- Строки: Версия, Документация, Style guide

**Конвенции именования:**
- Таблица с колонками: Элемент, Правило, Пример (TECH006)

**Структура кода:**
- Описание организации модулей (TECH006)

**Паттерны использования:**
- Рекомендуемые паттерны с примерами (TECH006)

**Типичные ошибки:**
- Антипаттерны с примерами правильного кода (TECH006)
- Не противоречит [standard-principles.md](/.instructions/standard-principles.md) (TECH007)

**Ссылки:**
- Ссылки на документацию и style guides (TECH006)

### Режим заглушки (если секции 2-6 содержат placeholder)

При наличии `*Заполняется при ADR → DONE.*` в секциях 2-6 — файл является заглушкой:

| Проверка | Правило |
|----------|---------|
| § 1 (Версия и источники) | Заполнен (версия, документация) |
| § 2-6 | Содержат `*Заполняется при ADR → DONE.*` |
| Frontmatter `technology` | Присутствует, kebab-case |

**Ошибка:** Если § 1 не заполнен, а § 2-6 — placeholder → `TECH008: § 1 обязателен даже для заглушки`.

**Ошибка:** Если часть секций заполнена, а часть — placeholder → `TECH009: смешанное состояние — заполнить все или оставить placeholder`.

### Шаг 4: Rule

| Проверка | Правило | Код |
|----------|---------|-----|
| Файл `.claude/rules/{tech}.md` | Существует | TECH010 |
| Содержит ссылки | На `standard-{tech}.md` и `validation-{tech}.md` | TECH010 |
| Globs | Соответствуют файлам технологии | TECH010 |

### Шаг 5: Реестр

| Проверка | Правило | Код |
|----------|---------|-----|
| `specs/technologies/README.md` | Строка с технологией существует | TECH011 |
| Колонка "Сервисы" | Актуальна | TECH011 |

---

## Чек-лист

### Frontmatter
- [ ] `description` — формат "Стандарт кодирования {Technology} — ..." (TECH001)
- [ ] `technology` — kebab-case (TECH003)
- [ ] `standard`, `standard-version`, `index` — корректны (TECH002)

### Секции
- [ ] Все 6 секций присутствуют (TECH004)
- [ ] Порядок секций соответствует стандарту (TECH005)

### Содержание (полный режим)
- [ ] § 1 — таблица Параметр/Значение (TECH006)
- [ ] § 2 — таблица Элемент/Правило/Пример (TECH006)
- [ ] § 3-4 — описание с примерами (TECH006)
- [ ] § 5 — не противоречит standard-principles.md (TECH007)
- [ ] § 6 — ссылки на документацию (TECH006)

### Содержание (режим заглушки)
- [ ] § 1 — заполнен (версия, документация)
- [ ] § 2-6 — `*Заполняется при ADR → DONE.*` (TECH008)

### Инфраструктура
- [ ] Rule `.claude/rules/{tech}.md` существует (TECH010)
- [ ] Строка в реестре `specs/technologies/README.md` (TECH011)

---

## Типичные ошибки

| Ошибка | Код | Причина | Решение |
|--------|-----|---------|---------|
| Нет frontmatter | TECH001 | Файл создан без `---` блока | Добавить frontmatter по [standard-technology.md § 3](./standard-technology.md#3-frontmatter) |
| Нет поля technology | TECH003 | Пропущено при создании | Добавить `technology: {tech}` в frontmatter |
| Отсутствует секция | TECH004 | Не все 6 секций | Добавить недостающую секцию |
| Секции не по порядку | TECH005 | Порядок нарушен | Переставить по стандарту (§ 5) |
| Некорректное содержание | TECH006 | Таблица/формат не совпадают | Привести к формату из [standard-technology.md § 5](./standard-technology.md#5-секции-per-tech-стандарта) |
| Конфликт с principles | TECH007 | Типичные ошибки противоречат standard-principles.md | Устранить противоречие (§ 5.7) |
| § 1 пуст в заглушке | TECH008 | Версия и источники не заполнены | Заполнить § 1 (Design знает технологию и версию) |
| Смешанное состояние | TECH009 | Часть секций заполнена, часть — placeholder | Заполнить все или оставить все как placeholder |
| Нет rule | TECH010 | Rule не создан | Создать `.claude/rules/{tech}.md` по [standard-technology.md § 7.3](./standard-technology.md#73-шаблон-rule-для-автозагрузки) |
| Нет строки в реестре | TECH011 | Технология не добавлена в реестр | Добавить строку в `specs/technologies/README.md` |

---

## Скрипты

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `validate-technology.py` | Валидация `standard-{tech}.md` — frontmatter, секции, rule, реестр | [specs/.instructions/.scripts/validate-technology.py](../.scripts/validate-technology.py) |

```bash
# Валидация одного файла
python specs/.instructions/.scripts/validate-technology.py specs/.instructions/technologies/standard-python.md

# Валидация всех per-tech стандартов
python specs/.instructions/.scripts/validate-technology.py specs/.instructions/technologies/

# Подробный вывод
python specs/.instructions/.scripts/validate-technology.py specs/.instructions/technologies/ --verbose
```

---

## Скиллы

| Скилл | Назначение | Путь |
|-------|------------|------|
| `/technology-validate` | Валидация per-tech стандарта | [.claude/skills/technology-validate/SKILL.md](/.claude/skills/technology-validate/SKILL.md) |
