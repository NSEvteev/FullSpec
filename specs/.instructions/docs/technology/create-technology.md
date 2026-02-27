---
description: Воркфлоу создания per-tech стандарта кодирования standard-{tech}.md — полный стандарт при Design → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу создания

Рабочая версия стандарта: 1.0

Пошаговый процесс создания нового `specs/docs/.technologies/standard-{tech}.md` — per-tech стандарта кодирования. Описывает подготовку, создание файла по шаблону, заполнение 8 секций, создание rule и регистрацию в `docs/README.md`.

**Полезные ссылки:**
- [Инструкции specs/](../../README.md)
- [Стандарт standard-{tech}.md](./standard-technology.md)

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
  - [Шаг 1: Определить имя технологии](#шаг-1-определить-имя-технологии)
  - [Шаг 2: Проверить существование](#шаг-2-проверить-существование)
  - [Шаг 3: Создать файл из шаблона](#шаг-3-создать-файл-из-шаблона)
  - [Шаг 4: Заполнить frontmatter](#шаг-4-заполнить-frontmatter)
  - [Шаг 5: Заполнить секции](#шаг-5-заполнить-секции)
  - [Шаг 6: Создать rule](#шаг-6-создать-rule)
  - [Шаг 7: Зарегистрировать в README](#шаг-7-зарегистрировать-в-readme)
  - [Шаг 8: Валидация](#шаг-8-валидация)
  - [Шаг 8.5: Ревью содержания](#шаг-85-ревью-содержания-если-вне-контекста-design)
  - [Шаг 9: Отчёт](#шаг-9-отчёт)
  - [Шаг 10: Создать security-{tech}.md (если применимо)](#шаг-10-создать-security-techmd-если-применимо)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Однофазная модель.** Стандарт создаётся полностью за один проход. Конвенции использования технологии известны с момента её выбора и не зависят от ADR.

> **Параллельный запуск.** При множестве технологий оркестратор запускает N technology-agent параллельно — по одному на технологию. Каждый агент создаёт полный комплект (standard + rule + README).

> **Шаблон обязателен.** Файл создаётся из шаблона в [standard-technology.md § 9](./standard-technology.md#9-шаблон). Запрещено придумывать свой формат.

> **8 секций без исключений.** Все 8 секций обязательны. Если секция неприменима — stub-текст в курсиве. Удалять секцию запрещено.

> **Готовые к копированию примеры.** Code-блоки ДОЛЖНЫ содержать рабочий код с реальными импортами и корректным синтаксисом. Псевдокод запрещён.

---

## Когда создавать

**Обязательно:**
- При появлении новой технологии в Tech Stack любого `{svc}.md`
- При Design → WAITING (новая технология)
- Перед началом работы с технологией, у которой нет стандарта

**НЕ создавать:**
- Технология только для tooling (webpack, prettier) — не попадает в `src/`
- Обёртка над другой технологией (TypeORM → PostgreSQL) — конвенции наследуются
- Одноразовое использование вне `src/` (см. [standard-technology.md § 2](./standard-technology.md#2-расположение-и-именование))
- Стандарт уже существует (→ [modify-technology.md](./modify-technology.md))

---

## Шаги

### Шаг 1: Определить имя технологии

**Имя файла:** `standard-{tech}.md` — где `{tech}` в kebab-case.

**Правила:**
- Имя технологии, не продукта: `postgresql` (не `postgres`), `redis` (не `redis-stack`)
- Фреймворк выделяется в отдельный стандарт при конфликте конвенций с базовой технологией (см. [standard-technology.md § 2](./standard-technology.md#2-расположение-и-именование))

### Шаг 2: Проверить существование

Убедиться, что стандарт ещё не создан:

```bash
ls specs/docs/.technologies/standard-{tech}.md
```

| Результат | Действие |
|-----------|----------|
| Не существует | Продолжить с Шагом 3 |
| Существует | → [modify-technology.md](./modify-technology.md) |

### Шаг 3: Создать файл из шаблона

Скопировать шаблон из [standard-technology.md § 9](./standard-technology.md#9-шаблон) в `specs/docs/.technologies/standard-{tech}.md`.

### Шаг 4: Заполнить frontmatter

```yaml
---
description: Стандарт кодирования {Technology} — конвенции именования, паттерны, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: {tech}
---
```

Поле `standard-version` НЕ используется — версия указывается в заголовке h1.

### Шаг 5: Заполнить секции

Заполнить все 8 секций согласно [standard-technology.md § 4](./standard-technology.md#4-секции). Источники информации для заполнения:

| Секция | Источник данных |
|--------|----------------|
| Версия и настройка | Официальная документация технологии, package.json / pyproject.toml |
| Конвенции именования | Официальный style guide, общепринятые конвенции |
| Паттерны кода | Исходный код проекта, best practices документации |
| Антипаттерны | Документация (common pitfalls), опыт проекта |
| Структура файлов | Текущая структура `/src/{svc}/`, конвенции проекта |
| Валидация | Наличие линтеров, статических анализаторов |
| Тестирование | Test framework, фикстуры, конвенции мокирования |
| Логирование | Logging framework, конвенции уровней |

**Принцип:** Стандарт ДОЛЖЕН соответствовать [standard-principles.md](/.instructions/standard-principles.md). При конфликте — добавить явное примечание: `> **Исключение из standard-principles.md:** {описание}`.

**Неприменимые секции:** stub-текст в курсиве: `*{Название секции} не применимо — {причина}.*`

### Шаг 6: Создать rule

Создать rule для автозагрузки стандарта при работе с файлами технологии.

**Путь:** `.claude/rules/{tech}.md`

**Содержимое:** см. [standard-technology.md § 6](./standard-technology.md#6-автозагрузка-через-rules).

**Определение globs:** Зависит от технологии (примеры — в стандарте § 6).

### Шаг 7: Зарегистрировать в README

Обновить `specs/docs/README.md` в двух местах:

**1. Таблица «Стандарты технологий»:**

```markdown
| {Technology} | [standard-{tech}.md](.technologies/standard-{tech}.md) |
```

Строки — в алфавитном порядке по `{tech}`.

**2. Дерево:**

Добавить `├── standard-{tech}.md` в дерево `.technologies/` (алфавитный порядок).

### Шаг 8: Валидация

```bash
# Валидация формата standard-{tech}.md
python specs/.instructions/.scripts/validate-docs-technology.py specs/docs/.technologies/standard-{tech}.md
```

Скрипт должен пройти без ошибок. Если есть ошибки — исправить по кодам из [validation-technology.md](./validation-technology.md).

### Шаг 8.5: Ревью содержания (если вне контекста Design)

> **Условие:** `/technology-create` вызван **вне** create-design.md (например, ручной вызов, `/technology-modify`).

Если вызван из `/docs-sync` — ревью выполняется на уровне оркестратора ([create-docs-sync.md](/specs/.instructions/create-docs-sync.md)), а не здесь.

1. Запустить **одного** technology-reviewer на все созданные стандарты
2. Если вердикт **REVISE** — исправить стандарты по замечаниям → повторить Шаг 8 + 8.5
3. Если вердикт **ACCEPT** — продолжить к Шагу 9

**Агент:** [technology-reviewer](/.claude/agents/technology-reviewer/AGENT.md) (Task tool, subagent_type=`technology-reviewer`)

### Шаг 9: Отчёт

```
## Отчёт о создании standard-{tech}.md

✅ **Создан:** `specs/docs/.technologies/standard-{tech}.md`
📝 **Секции:** {N заполненных} / 8 (остальные — stub)

### Заполненные секции
- {список заполненных секций}

### Stub-секции
- {список stub-секций с причинами}

### Артефакты
- `.claude/rules/{tech}.md` — rule для автозагрузки
- `specs/docs/README.md` — таблица + дерево

### Security
- 📎 `security-{tech}.md`: {создан / не создан — причина}
- Инструменты: {список}
```

### Шаг 10: Создать security-{tech}.md (если применимо)

Определить, нужен ли security-файл для технологии:

| Условие | Пример | Создавать |
|---------|--------|-----------|
| Язык/runtime с package manager | Python, JavaScript, Go, Java | Да |
| Контейнерная технология | Docker | Да |
| СУБД, кэш, очередь | PostgreSQL, Redis, RabbitMQ | Нет |
| CSS/UI framework | Tailwind CSS, Bootstrap | Нет |
| Инфраструктурная утилита | Nginx | Нет |
| IaC с provider registry | Terraform | Да |

**Если Да:**
1. Скопировать шаблон security-{tech}.md (см. standard-technology.md § 11)
2. Заполнить frontmatter (`type: security`)
3. Заполнить 5 секций:

| Секция | Источник данных |
|--------|----------------|
| Инструменты | Официальные security-инструменты технологии |
| Dependency Audit | Package manager audit command |
| SAST | Официальный или de-facto SAST для языка |
| CI Integration | GitHub Actions steps для инструментов выше |
| Known Exceptions | Пусто при создании |

4. Зарегистрировать в `specs/docs/README.md` (таблица + дерево)

**Если Нет:** Шаг пропускается. В отчёте указать: `📎 security-{tech}.md: не создан — {причина}`.

---

## Чек-лист

- [ ] Имя технологии определено (kebab-case)
- [ ] Файл не существовал ранее
- [ ] Файл создан из шаблона standard-technology.md § 9
- [ ] Frontmatter заполнен (description, standard, technology; нет standard-version)
- [ ] Заголовок h1 содержит версию: `# Стандарт {Technology} v1.0`
- [ ] Все 8 секций присутствуют
- [ ] Паттерны кода — рабочий код с реальными импортами
- [ ] Не противоречит standard-principles.md (исключения документированы)
- [ ] Stub-секции содержат текст в курсиве с причиной
- [ ] Rule `.claude/rules/{tech}.md` создан с правильными globs
- [ ] docs/README.md обновлён (таблица + дерево)
- [ ] Валидация: `validate-docs-technology.py` пройдена
- [ ] Ревью содержания: technology-reviewer вердикт ACCEPT (если вне create-design.md)
- [ ] security-{tech}.md создан (если технология имеет package manager / SAST)
- [ ] security-{tech}.md: frontmatter содержит `type: security`
- [ ] security-{tech}.md: 5 секций заполнены / stub
- [ ] security-{tech}.md зарегистрирован в docs/README.md

---

## Примеры

### Создание стандарта PostgreSQL

```bash
# Шаг 1: имя = postgresql
# Шаг 2: проверить — файл не существует
ls specs/docs/.technologies/standard-postgresql.md  # Not found

# Шаг 3: скопировать шаблон из standard-technology.md § 9
# Шаг 4: заполнить frontmatter (technology: postgresql)
# Шаг 5: заполнить 8 секций (пример — см. standard-technology.md § 10)
# Шаг 6: создать rule .claude/rules/postgresql.md
# Шаг 7: обновить docs/README.md
# Шаг 8: валидация
python specs/.instructions/.scripts/validate-docs-technology.py specs/docs/.technologies/standard-postgresql.md
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-docs-technology.py](../../.scripts/validate-docs-technology.py) | Валидация формата standard-{tech}.md | [validation-technology.md](./validation-technology.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/technology-create](/.claude/skills/technology-create/SKILL.md) | Создание per-tech стандарта | Этот документ |
