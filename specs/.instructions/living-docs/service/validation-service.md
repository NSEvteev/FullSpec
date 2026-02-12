---
description: Валидация сервисных документов services/{svc}.md — frontmatter, секции, формат таблиц, согласованность с README и labels.
standard: .instructions/standard-instruction.md
standard-version: v2.0
index: specs/.instructions/living-docs/service/README.md
---

# Валидация сервисной документации

Рабочая версия стандарта: 2.0

Проверка файлов `specs/architecture/services/{svc}.md` на соответствие [standard-service.md](./standard-service.md).

**Полезные ссылки:**
- [Стандарт сервисной документации](./standard-service.md)
- [Инструкции living-docs](../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-service.md](./standard-service.md) |
| Валидация | Этот документ |
| Создание | [create-service.md](./create-service.md) |
| Модификация | [modify-service.md](./modify-service.md) |

## Оглавление

- [Когда валидировать](#когда-валидировать)
- [Шаги](#шаги)
  - [Шаг 0: Автоматическая валидация](#шаг-0-автоматическая-валидация)
  - [Шаг 1: Frontmatter](#шаг-1-frontmatter)
  - [Шаг 2: Обязательные секции](#шаг-2-обязательные-секции)
  - [Шаг 3: Содержание секций](#шаг-3-содержание-секций)
  - [Stub-режим (если нет `created-by`)](#stub-режим-если-нет-created-by)
  - [Шаг 4: Согласованность с README и labels](#шаг-4-согласованность-с-readme-и-labels)
  - [Шаг 5: Валидация архитектурных документов](#шаг-5-валидация-архитектурных-документов)
- [Чек-лист](#чек-лист)
- [Типичные ошибки](#типичные-ошибки)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Когда валидировать

| Момент | Как |
|--------|-----|
| После создания/обновления `services/{svc}.md` | `python specs/.instructions/.scripts/validate-service.py {путь}` |
| При code review | Проверить чек-лист |
| Перед коммитом (автоматически) | Pre-commit хук (будет настроен) |

---

## Шаги

### Шаг 0: Автоматическая валидация

```bash
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/{svc}.md --verbose
```

Скрипт проверяет правила SVC001-SVC014. Автоматически определяет stub/full по отсутствию `created-by`. Если валидация пройдена — переходить к **Шагу 5** (архитектурные документы).

**Если скрипт недоступен** — выполнить шаги 1-4 вручную, затем Шаг 5.

### Шаг 1: Frontmatter

Проверить frontmatter файла `services/{svc}.md`:

| Поле | Правило | Код |
|------|---------|-----|
| `description` | Присутствует, до 1024 символов, формат "Архитектура сервиса {service} — {назначение}" | SVC001, SVC002 |
| `service` | Присутствует, kebab-case | SVC003 |
| `created-by` | **Stub:** отсутствует. **Full:** присутствует, формат `adr-NNNN` | SVC004 |
| `last-updated-by` | **Stub:** отсутствует. **Full:** присутствует, формат `adr-NNNN` | SVC005 |

**Детекция stub vs full:** Отсутствие `created-by` = stub-режим. Подробности: [standard-frontmatter.md § 5](/.structure/.instructions/standard-frontmatter.md#5-дополнительные-поля-для-живых-документов-архитектуры).

### Шаг 2: Обязательные секции

Проверить наличие и порядок **8 обязательных секций** (заголовки `##`):

| # | Секция (заголовок `##`) | Код |
|---|------------------------|-----|
| 1 | Резюме | SVC006 |
| 2 | API контракты | SVC006 |
| 3 | Data Model | SVC006 |
| 4 | Code Map | SVC006 |
| 5 | Внешние зависимости | SVC006 |
| 6 | Границы автономии LLM | SVC006 |
| 7 | Planned Changes | SVC006 |
| 8 | Changelog | SVC006 |

Секции должны идти **строго в указанном порядке** (SVC007).

### Шаг 3: Содержание секций

**Резюме:**
- 1-3 предложения, без технических деталей реализации (SVC008)

**API контракты:**
- Таблица с колонками: Тип, Endpoint/Event, Метод, Описание (SVC008)

**Data Model:**
- Таблица с колонками: Сущность, Хранилище, Назначение (SVC008)

**Code Map:**
- Подсекции `### Tech Stack`, `### Пакеты`, `### Точки входа`, `### Внутренние зависимости` (SVC009)
- Tech Stack — таблица: Технология, Назначение
- Пакеты — таблица: Пакет, Назначение, Ключевые модули
- Описание на уровне пакетов/модулей, не файлов

**Внешние зависимости:**
- Таблица с колонками: Тип, Путь/Сервис, Что используем, Роль (SVC008)
- Роли: `provider`, `consumer`, `publisher`, `subscriber` (SVC010)

**Границы автономии LLM:**
- Три уровня: **Свободно**, **Флаг**, **CONFLICT** (SVC011)

**Planned Changes:**
- Формат: ссылки на Discussion + Design + ADR
- Не содержит дублирования дельт из ADR

**Changelog:**
- Записи в обратном хронологическом порядке (SVC014)
- Каждая запись — навигационный указатель (ссылки на Discussion, Design, ADR)
- Маркер статуса: `DONE`, `REJECTED` или `CONFLICT-RESOLVED`
- Stub-режим: `*Нет записей.*`

### Stub-режим (если нет `created-by`)

При отсутствии `created-by` в frontmatter — файл является stub-заглушкой:

| Проверка | Правило |
|----------|---------|
| Секции 2-6 (API контракты — Границы автономии LLM) | Содержат `*Заполняется при ADR → DONE.*` |
| Резюме | Заполнено (1-3 предложения) |
| Planned Changes | Заполнены (ссылка на Discussion + Design) |
| Changelog | `*Нет записей.*` |
| `created-by` / `last-updated-by` | Отсутствуют |

**Ошибка:** Если `created-by` отсутствует, но секции 2-6 заполнены — `SVC004: created-by обязателен для заполненного документа`.

**Ошибка:** Если `created-by` присутствует, но секции содержат `*Заполняется при ADR → DONE.*` — `stub-placeholder в полном документе`.

### Шаг 4: Согласованность с README и labels

| Проверка | Правило | Код |
|----------|---------|-----|
| `services/README.md` | Строка с данными сервиса существует в таблице | SVC012 |
| `labels.yml` | Метка `svc:{service}` существует | SVC013 |

### Шаг 5: Валидация архитектурных документов

Создание или обновление `services/{svc}.md` обычно сопровождается изменениями в файлах `system/` и `domains/`. Запустить валидацию фиксированных файлов архитектуры:

```bash
python specs/.instructions/.scripts/validate-architecture.py --check-services --verbose
```

Скрипт проверяет (AC001-AC006):
- 4 фиксированных файла существуют и содержат обязательные секции
- Новые файлы в `specs/services/` сопровождаются обновлением `specs/architecture/`

**SSOT:** [validation-architecture.md](../architecture/validation-architecture.md)

---

## Чек-лист

### Frontmatter
- [ ] `description` — до 1024 символов, формат "Архитектура сервиса X — назначение" (SVC001, SVC002)
- [ ] `service` — kebab-case (SVC003)
- [ ] **Full:** `created-by` — формат `adr-NNNN` (SVC004). **Stub:** отсутствует
- [ ] **Full:** `last-updated-by` — формат `adr-NNNN` (SVC005). **Stub:** отсутствует

### Секции
- [ ] Все 8 секций присутствуют (SVC006)
- [ ] Порядок секций соответствует стандарту (SVC007)

### Содержание (Full-режим)
- [ ] Резюме — 1-3 предложения (SVC008)
- [ ] API контракты — таблица Тип, Endpoint/Event, Метод, Описание (SVC008)
- [ ] Data Model — таблица Сущность, Хранилище, Назначение (SVC008)
- [ ] Code Map — 4 подсекции: Tech Stack, Пакеты, Точки входа, Внутренние зависимости (SVC009)
- [ ] Внешние зависимости — роли корректны (SVC010)
- [ ] Границы автономии LLM — три уровня (SVC011)
- [ ] Planned Changes — формат, без дублирования дельт
- [ ] Changelog — обратный хронологический порядок, маркеры DONE/REJECTED (SVC014)

### Содержание (Stub-режим)
- [ ] Резюме — 1-3 предложения (SVC008)
- [ ] Секции 2-6 — `*Заполняется при ADR → DONE.*`
- [ ] Planned Changes — ссылка на Discussion + Design
- [ ] Changelog — `*Нет записей.*` (SVC014)

### Согласованность
- [ ] Строка в `services/README.md` актуальна (SVC012)
- [ ] Метка `svc:{service}` в `labels.yml` (SVC013)

### Архитектурные документы
- [ ] `validate-architecture.py --check-services` пройден (AC001-AC006)
- [ ] Фиксированные файлы обновлены при изменении сервиса

---

## Типичные ошибки

| Ошибка | Код | Причина | Решение |
|--------|-----|---------|---------|
| Нет frontmatter | SVC001 | Файл создан без `---` блока | Добавить frontmatter по [standard-service.md § 3](./standard-service.md#3-frontmatter) |
| Некорректный description | SVC002 | Формат не "Архитектура сервиса X — назначение" | Исправить формат, проверить длину ≤ 1024 |
| Нет поля service | SVC003 | Пропущено при создании | Добавить `service: {name}` в frontmatter |
| Некорректный created-by | SVC004 | Формат не `adr-NNNN` | Исправить на `adr-NNNN` (4 цифры, ведущие нули) |
| Некорректный last-updated-by | SVC005 | Формат не `adr-NNNN` | Исправить на ID последнего ADR |
| Отсутствует секция | SVC006 | Не все 8 секций | Добавить недостающую секцию |
| Секции не по порядку | SVC007 | Порядок нарушен | Переставить секции по стандарту (§ 5) |
| Некорректная таблица | SVC008 | Колонки не совпадают со стандартом | Привести к формату из [standard-service.md § 5](./standard-service.md#5-секции-документа-сервиса) |
| Code Map без подсекций | SVC009 | Нет Tech Stack/Пакеты/Точки входа/Внутренние зависимости | Добавить подсекции по [standard-service.md § 5.4](./standard-service.md#54-code-map) |
| Некорректная роль | SVC010 | Роль не из набора provider/consumer/publisher/subscriber | Исправить на допустимое значение |
| Нет трёх уровней автономии | SVC011 | Не указаны Свободно/Флаг/CONFLICT | Добавить по [standard-service.md § 5.6](./standard-service.md#56-границы-автономии-llm) |
| Нет строки в README | SVC012 | Сервис не добавлен в `services/README.md` | Добавить строку в таблицу |
| Нет метки svc: | SVC013 | Метка не создана в `labels.yml` | Создать через `/labels-modify` |
| Нет секции Changelog | SVC014 | Секция `## Changelog` отсутствует | Добавить Changelog по [standard-service.md § 5.8](./standard-service.md#58-changelog) |
| Stub-placeholder в full | — | `*Заполняется при ADR → DONE.*` в документе с `created-by` | Заполнить секции или убрать `created-by` |
| Нет `created-by` в full | SVC004 | Секции заполнены, но `created-by` отсутствует | Добавить `created-by: adr-NNNN` |

---

## Скрипты

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `validate-service.py` | Валидация `services/{svc}.md` — frontmatter, секции, таблицы, согласованность | [specs/.instructions/.scripts/validate-service.py](../../.scripts/validate-service.py) |

```bash
# Валидация одного файла
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/auth.md

# Валидация всех файлов в services/
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/

# Подробный вывод
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/ --verbose
```

---

## Скиллы

*Нет скиллов.*
