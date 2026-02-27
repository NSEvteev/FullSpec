---
description: Воркфлоу создания нового docs/{svc}.md — от заполнения секций до регистрации в README.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу создания

Рабочая версия стандарта: 1.2

Пошаговый процесс создания нового `specs/docs/{svc}.md` — per-service документа. Описывает подготовку, создание файла по шаблону, заполнение 10 секций и регистрацию в `docs/README.md`.

**Полезные ссылки:**
- [Инструкции specs/](../../README.md)
- [Стандарт {svc}.md](./standard-service.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-service.md](./standard-service.md) |
| Валидация | [validation-service.md](./validation-service.md) |
| Создание | Этот документ |
| Модификация | [modify-service.md](./modify-service.md) |

## Оглавление

- [Принципы](#принципы)
- [Когда создавать](#когда-создавать)
- [Шаги](#шаги)
  - [Шаг 1: Определить имя сервиса](#шаг-1-определить-имя-сервиса)
  - [Шаг 2: Проверить существование](#шаг-2-проверить-существование)
  - [Шаг 3: Создать файл из шаблона](#шаг-3-создать-файл-из-шаблона)
  - [Шаг 4: Заполнить frontmatter](#шаг-4-заполнить-frontmatter)
  - [Шаг 5: Заполнить секции](#шаг-5-заполнить-секции)
  - [Шаг 6: Зарегистрировать в README](#шаг-6-зарегистрировать-в-readme)
  - [Шаг 7: Валидация](#шаг-7-валидация)
  - [Шаг 8: Отчёт](#шаг-8-отчёт)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Один сервис — один файл.** Каждый `{svc}.md` описывает ровно один сервис. Имя файла совпадает с именем папки сервиса в `/src/`.

> **Шаблон обязателен.** Файл создаётся из шаблона в [standard-service.md § 5](./standard-service.md#5-шаблон). Запрещено придумывать свой формат.

> **10 секций без исключений.** Все 10 секций обязательны. Если секция неприменима — stub-текст в курсиве. Удалять секцию запрещено.

> **Имплементационный уровень для API и Data Model.** Секции API контракты и Data Model заполняются до уровня, достаточного для написания кода по аналогии.

> **Регистрация в README обязательна.** После создания файла — обновить `docs/README.md`: таблицу Сервисы и дерево.

> **Автоматическое создание.** При работе через analysis chain — `{svc}.md` создаётся автоматически `/docs-sync` (service-agent). Ручной вызов `/service-create` — для сервисов вне analysis chain.

> **Chain-маркер в Planned Changes.** Блок Planned Changes (§ 9) обязательно обёрнут в chain-маркер: `<!-- chain: NNNN-{topic} -->` ... `<!-- /chain: NNNN-{topic} -->`. Маркер обеспечивает идемпотентность и откат.

---

## Когда создавать

**Обязательно:**
- При появлении нового сервиса в overview.md
- Перед началом работы с сервисом, у которого нет `{svc}.md`
- При переносе из `analysis/` в реализацию

**НЕ создавать:**
- Для инфраструктурных компонентов без собственного кода (Docker, nginx конфиг)
- Для shared-пакетов (описываются в `conventions.md`)

---

## Шаги

### Шаг 1: Определить имя сервиса

**Имя файла:** `{svc}.md` — где `{svc}` совпадает с именем папки сервиса в `/src/{svc}/`.

**Правила:**
- Kebab-case: `notification.md`, `user-auth.md`, `api-gateway.md`
- Без суффиксов `-service`, `-svc`

### Шаг 2: Проверить существование

Убедиться, что файл ещё не создан:

```bash
ls specs/docs/{svc}.md
```

Если файл уже существует — использовать [modify-service.md](./modify-service.md) вместо создания.

### Шаг 3: Создать файл из шаблона

Скопировать шаблон из [standard-service.md § 5](./standard-service.md#5-шаблон) в `specs/docs/{svc}.md`.

### Шаг 4: Заполнить frontmatter

```yaml
---
description: {svc} — {назначение сервиса, 10-15 слов}.
standard: specs/.instructions/docs/service/standard-service.md
criticality: critical-high | critical-medium | critical-low
---
```

**Определение уровня критичности:**
1. Оценить бизнес-влияние полной недоступности сервиса: что произойдёт если сервис упадёт?
2. Выбрать уровень по критериям:
   - `critical-high` — бизнес-остановка, revenue = 0 (платёжный шлюз, авторизация, основная БД)
   - `critical-medium` — значительная деградация, бизнес работает ограниченно (поиск, рекомендации, уведомления)
   - `critical-low` — неудобство, есть обходные пути (аналитика, экспорт отчётов, админ-панель логов)
3. Указать обоснование выбранного уровня в секции «Назначение» (см. Шаг 5)

### Шаг 5: Заполнить секции

Заполнить все 10 секций согласно [standard-service.md § 3](./standard-service.md#3-секции). Источники информации для заполнения:

| Секция | Источник данных |
|--------|----------------|
| Назначение | overview.md, README сервиса, analysis/. Включить **обоснование критичности** (почему выбран уровень из frontmatter) |
| API контракты | Исходный код (routes/controllers), OpenAPI, analysis/ |
| Data Model | Миграции БД, models, analysis/ |
| Потоки | Исходный код, analysis/ |
| Code Map | `src/{svc}/`, package.json / pyproject.toml |
| Code Map → Makefile таргеты | Makefile (корневой), src/{svc}/Makefile (если есть) |
| Зависимости | imports, docker-compose, conventions.md |
| Доменная модель | Бизнес-требования, analysis/ |
| Границы автономии LLM | Архитектурные ограничения проекта |
| Planned Changes | Активные analysis/ документы |
| Changelog | Первая запись: `- **Создание сервиса** \| DONE {дата}` |

**Неприменимые секции:** если секция не применима (критерии — в описании каждой секции в стандарте) — stub-текст в курсиве: `*{Название раздела} не применимо — {причина}.*`

**Порядок заполнения (рекомендация):**
1. Назначение — определяет scope документа
2. API контракты + Data Model — имплементационные секции, заполняются первыми
3. Потоки — опираются на API и Data Model
4. Code Map + Зависимости — навигационные секции
5. Доменная модель — архитектурная секция
6. Границы автономии LLM — по итогам заполнения предыдущих секций
7. Planned Changes + Changelog — заключительные

### Шаг 5.1: Создать per-service Makefile таргеты

Добавить в корневой `Makefile` per-service таргеты для тестирования и линтинга:

```makefile
test-{svc}:  ## Unit + integration тесты {svc}
	cd src/{svc} && make test

lint-{svc}:  ## Линтинг {svc}
	cd src/{svc} && make lint
```

Если таргеты уже существуют — проверить соответствие формату `{action}-{svc}` (kebab-case). Если сервис имеет Docker-образ — добавить `build-{svc}`.

### Шаг 6: Зарегистрировать в README

Обновить `specs/docs/README.md` в трёх местах:

**1. Таблица Сервисы:**

```markdown
| {svc} | {назначение, 5-10 слов} | {язык, БД, MQ} | [{svc}.md]({svc}.md) |
```

Строки в таблице — в алфавитном порядке.

**2. Дерево:**

Добавить `├── {svc}.md` в дерево (алфавитный порядок среди per-service файлов).

**3. Проверить overview.md:**

Убедиться, что сервис указан в `overview.md`. Если нет — обновить через [modify-overview.md](../overview/modify-overview.md).

### Шаг 7: Валидация

```bash
# Валидация формата {svc}.md
python specs/.instructions/.scripts/validate-docs-service.py specs/docs/{svc}.md

# Валидация синхронизации README с деревом
python specs/.instructions/.scripts/validate-docs-readme-services.py
```

Оба скрипта должны пройти без ошибок. Если есть ошибки — исправить по кодам из [validation-service.md](./validation-service.md).

### Шаг 8: Отчёт

```
## Отчёт о создании {svc}.md

✅ **Создан:** `specs/docs/{svc}.md`
📝 **Секции:** {N заполненных} / 10 (остальные — stub)

### Заполненные секции
- {список заполненных секций}

### Stub-секции
- {список stub-секций с причинами}

### Обновления
- `specs/docs/README.md` — таблица Сервисы + дерево
- `specs/docs/.system/overview.md` — {обновлён / уже содержал}
```

---

## Чек-лист

- [ ] Имя сервиса определено (совпадает с `/src/{svc}/`)
- [ ] Файл не существовал ранее
- [ ] Файл создан из шаблона standard-service.md § 5
- [ ] Frontmatter заполнен (description, standard, criticality)
- [ ] Все 10 секций присутствуют
- [ ] API контракты и Data Model — имплементационный уровень (или stub)
- [ ] Changelog содержит запись о создании сервиса
- [ ] Stub-секции содержат текст в курсиве с причиной
- [ ] docs/README.md обновлён (таблица + дерево)
- [ ] overview.md содержит сервис
- [ ] Per-service Makefile таргеты созданы (`make test-{svc}`, `make lint-{svc}`)
- [ ] Code Map содержит подсекцию Makefile таргеты
- [ ] Валидация: `validate-docs-service.py` пройдена
- [ ] Валидация: `validate-docs-readme-services.py` пройдена

---

## Примеры

### Создание notification.md

```bash
# Шаг 1: имя = notification (папка /src/notification/)
# Шаг 2: проверить — файл не существует
ls specs/docs/notification.md  # Not found

# Шаг 3: скопировать шаблон из standard-service.md § 5
# Шаг 4: заполнить frontmatter
# Шаг 5: заполнить секции (пример — см. standard-service.md § 6)
# Шаг 6: обновить README
# Шаг 7: валидация
python specs/.instructions/.scripts/validate-docs-service.py specs/docs/notification.md
python specs/.instructions/.scripts/validate-docs-readme-services.py
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-docs-service.py](../../.scripts/validate-docs-service.py) | Валидация формата {svc}.md | [validation-service.md](./validation-service.md) |
| [validate-docs-readme-services.py](../../.scripts/validate-docs-readme-services.py) | Синхронизация README с деревом | [validation-readme.md](../readme/validation-readme.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/service-create](/.claude/skills/service-create/SKILL.md) | Создание {svc}.md | Этот документ |
