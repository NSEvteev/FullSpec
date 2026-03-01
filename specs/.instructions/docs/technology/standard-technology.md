---
description: Стандарт формата docs/.technologies/standard-{tech}.md — версия, конвенции, паттерны, антипаттерны, тестирование, логирование.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Стандарт standard-{tech}.md

Версия стандарта: 1.1

Формат и правила для `specs/docs/.technologies/standard-{tech}.md` — per-tech стандарта кодирования. Каждый стандарт самодостаточен: прочитал — можешь писать код с этой технологией по конвенциям проекта.

**Полезные ссылки:**
- [Инструкции specs/](../../README.md)
- [Мета-стандарт docs/](../standard-docs.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-technology.md](./validation-technology.md) |
| Создание | [create-technology.md](./create-technology.md) |
| Модификация | [modify-technology.md](./modify-technology.md) |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Расположение и именование](#2-расположение-и-именование)
- [3. Frontmatter](#3-frontmatter)
- [4. Секции](#4-секции)
  - [Версия и настройка](#версия-и-настройка)
  - [Конвенции именования](#конвенции-именования)
  - [Паттерны кода](#паттерны-кода)
  - [Антипаттерны](#антипаттерны)
  - [Структура файлов](#структура-файлов)
  - [Валидация](#валидация)
  - [Тестирование](#тестирование)
  - [Логирование](#логирование)
- [5. Принципы](#5-принципы)
- [6. Автозагрузка через rules](#6-автозагрузка-через-rules)
- [7. Регистрация в README](#7-регистрация-в-readme)
- [8. Версионирование](#8-версионирование)
- [9. Шаблон](#9-шаблон)
- [10. Пример](#10-пример)
- [11. Companion: security-{tech}.md](#11-companion-security-techmd)

---

## 1. Назначение

`docs/.technologies/standard-{tech}.md` — per-tech стандарт кодирования. Содержит конвенции, паттерны и антипаттерны использования конкретной технологии в проекте. LLM-разработчик читает этот файл перед работой с кодом на данной технологии.

**Регулирует:**
- Формат и содержание per-tech стандартов кодирования
- 8 обязательных секций стандарта
- Связь с `{svc}.md` через таблицу Tech Stack (секция Code Map)
- Автозагрузку через rules

**НЕ регулирует:**
- Архитектуру сервисов — [standard-service.md](../service/standard-service.md)
- Кросс-сервисные конвенции (формат ошибок, пагинация, auth) — [standard-conventions.md](../conventions/standard-conventions.md)
- Общие принципы программирования — [standard-principles.md](/.instructions/standard-principles.md)
- Деактивацию и миграцию per-tech стандартов — [modify-technology.md](./modify-technology.md)

**Один файл — одна технология.** Для каждой технологии из Tech Stack любого `{svc}.md` ДОЛЖЕН существовать `standard-{tech}.md`. Если стандарт отсутствует — создать через [create-technology.md](./create-technology.md). Per-tech стандарты создаются на основе технологий, отмеченных как "Выбрано" в секции "Выбор технологий" Design-документа (артефакт Step 7 create-design.md).

---

## 2. Расположение и именование

**Расположение:**
```
specs/docs/.technologies/standard-{tech}.md
```

**Именование `{tech}`:**
- Kebab-case: `python`, `typescript`, `postgresql`, `tailwind-css`
- Имя технологии, не продукта: `postgresql` (не `postgres`), `redis` (не `redis-stack`)
- Фреймворк выделяется в отдельный стандарт, если для работы с ним в проекте действуют конвенции, которые **противоречат** конвенциям базовой технологии (разные требования к структуре папок, несовместимые паттерны импорта, другие соглашения именования). Пример: Django — отдельный стандарт (собственная структура apps/, своё именование моделей). FastAPI — описывается в standard-python.md (только декораторы поверх стандартного Python). При сомнении — создать отдельный стандарт.

**Когда НЕ создавать per-tech стандарт:**

| Ситуация | Причина |
|----------|---------|
| Технология только для tooling (webpack, prettier) | Не попадает в `src/`, не требует конвенций кодирования |
| Обёртка над другой технологией (TypeORM → PostgreSQL) | Конвенции наследуются от базовой технологии |
| Одноразовое использование — технология применяется ровно в одном скрипте/файле вне `src/`, не планируется к повторному использованию (например, скрипт разовой миграции данных) | Не требует долгосрочной поддержки. Если та же технология появляется в `src/` хотя бы одного сервиса — стандарт обязателен. |

---

## 3. Frontmatter

```yaml
---
description: Стандарт кодирования {Technology} — конвенции именования, паттерны, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: {tech}
---
```

| Поле | Обязательное | Описание |
|------|-------------|----------|
| `description` | Да | Краткое описание, 10-15 слов |
| `standard` | Да | Путь к этому мета-стандарту |
| `technology` | Да | Kebab-case имя технологии (совпадает с `{tech}` в имени файла) |

**Версия:** Версия per-tech стандарта указывается в заголовке файла (`# Стандарт {Technology} v1.0`), а НЕ в frontmatter. Поле `standard-version` во frontmatter per-tech стандартов НЕ используется. Подробнее — [§ 8. Версионирование](#8-версионирование).

---

## 4. Секции

Каждый `standard-{tech}.md` содержит **8 обязательных h2-секций** в следующем порядке. Дополнительные h2-секции запрещены. Порядок секций фиксирован.

### Версия и настройка

**Содержание:** Версия технологии, ключевые библиотеки/драйверы с версиями, расположение конфигурации.

**Формат:** Таблица «Параметр / Значение».

| Обязательные строки | Описание |
|---------------------|----------|
| Версия | Мажорная версия технологии |
| Ключевые библиотеки | Пакеты/драйверы с версиями. Если сторонних библиотек нет — указать `—` |
| Конфигурация | Путь к конфигу и ключевые параметры |

**Когда stub:** Не бывает stub — у любой технологии есть версия.

---

### Конвенции именования

**Содержание:** Правила именования объектов технологии: файлы, модули, классы, функции, переменные (для языков); таблицы, колонки, индексы (для БД); компоненты, пропсы (для UI-фреймворков).

**Формат:** Таблица «Объект / Конвенция / Пример».

| Колонка | Описание |
|---------|----------|
| Объект | Тип именуемой сущности |
| Конвенция | Правило (camelCase, snake_case, PascalCase и т.д.) |
| Пример | Конкретный пример с backticks |

**Когда stub:** Не бывает stub — у любой технологии есть конвенции.

---

### Паттерны кода

**Содержание:** Типовые операции с готовыми к копированию примерами кода. Каждый паттерн — h3-подсекция с описанием «когда использовать» и code-блоком.

**Формат:** h3-подсекции, каждая содержит:
1. Описание (1-2 предложения: когда использовать этот паттерн)
2. Code-блок с рабочим кодом (готов к копированию)

**Обязательные паттерны:**
- Подключение / инициализация
- Основной запрос / операция
- Обработка ошибок
- Транзакция / batch (если технология поддерживает транзакции)

Секция считается достаточной, если по ней можно написать новый файл с этой технологией без чтения внешней документации технологии.

**Когда stub:** *Паттерны кода не применимо — {причина}.*

---

### Антипаттерны

**Содержание:** Что НЕ делать — конкретные ошибки с объяснением последствий и правильной альтернативой.

**Формат:** Таблица «Антипаттерн / Почему плохо / Правильно».

| Колонка | Описание |
|---------|----------|
| Антипаттерн | Конкретное действие, которое запрещено |
| Почему плохо | Последствия (производительность, безопасность, поддерживаемость) |
| Правильно | Конкретная альтернатива |

**Когда stub:** *Антипаттерны не применимо — {причина}.*

---

### Структура файлов

**Содержание:** Где размещать код, связанный с этой технологией. Дерево папок с комментариями.

**Формат:** Code-блок с деревом + комментарии к каждому элементу.

```
src/{svc}/
├── {dir}/          # {назначение}
│   └── {file}      # {назначение}
└── {dir}/          # {назначение}
```

**Когда stub:** *Структура файлов не применимо — {причина}.* (Например, для технологий без собственной структуры.)

---

### Валидация

**Содержание:** Как проверить код на соответствие этому стандарту. Ссылка на скрипт валидации, команда запуска, что именно проверяется.

**Формат (когда скрипт создан):**
1. Команда запуска скрипта (code-блок)
2. Описание: что проверяет скрипт (перечень)
3. Интеграция в pre-commit hook (если есть)

**Формат (когда скрипт не создан):**
stub-текст: *Скрипт валидации кода не создан. Валидация выполняется вручную по чек-листу из [validation-technology.md](./validation-technology.md).*

---

### Тестирование

**Содержание:** Как тестировать код с этой технологией: фреймворк, фикстуры, мокирование, паттерны тестов — с готовыми к копированию примерами.

**SSOT-зависимость:** Кросс-технологическая стратегия тестирования (типы тестов, структура файлов, мокирование по уровням) — в [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md). Эта секция описывает только per-tech паттерны: конкретный фреймворк, фикстуры и примеры кода для данной технологии.

**Формат:** h3-подсекции:

| Подсекция | Содержание |
|-----------|-----------|
| Фреймворк и плагины | Таблица «Компонент / Пакет / Назначение» |
| Фикстуры | Базовые фикстуры с code-блоком |
| Мокирование | Когда мокировать, когда нет + code-блок мока |
| Паттерны тестов | Типовые тесты (unit + integration) с code-блоками |

Секция считается достаточной, если по ней можно написать тест для этой технологии без чтения внешней документации тестового фреймворка.

**Когда stub:** *Тестирование не применимо — {причина}.*

---

### Логирование

**Содержание:** Что логировать при работе с этой технологией, на каком уровне. Техно-специфичные настройки логгера (кросс-сервисные конвенции логирования — формат, уровни, структура сообщений — в [standard-conventions.md](/specs/.instructions/docs/conventions/standard-conventions.md)).

**Формат:**
1. Таблица «Событие / Уровень / Пример сообщения»
2. Code-блок: настройка логирования для технологии

| Колонка | Описание |
|---------|----------|
| Событие | Что произошло (короткое описание) |
| Уровень | DEBUG / INFO / WARNING / ERROR |
| Пример сообщения | Конкретная строка лога |

**Когда stub:** *Логирование не применимо — технология не генерирует событий, требующих логирования.*

---

## 5. Принципы

> **Самодостаточность.** Прочитав `standard-{tech}.md`, разработчик может писать код на этой технологии без дополнительных источников. Все конвенции, паттерны и примеры — в одном файле.

> **Готовые к копированию примеры.** Code-блоки в секциях «Паттерны кода», «Тестирование», «Логирование» ДОЛЖНЫ содержать рабочий код с реальными импортами и корректным синтаксисом. Плейсхолдеры типа `{value}` допустимы только для конфигурационных значений (хосты, пароли). Псевдокод и абстрактные описания запрещены.

> **Соответствие принципам проекта.** Все per-tech стандарты ДОЛЖНЫ соответствовать [standard-principles.md](/.instructions/standard-principles.md). При конфликте — приоритет у принципов. Per-tech стандарт МОЖЕТ дополнять принципы специфичными для технологии правилами (например, PEP 8 для Python). Если правило в `standard-{tech}.md` расходится с `standard-principles.md` — добавить явное примечание: `> **Исключение из standard-principles.md:** {принцип} не применяется для {tech} по причине {причина}.`

> **8 секций без исключений.** Все 8 секций обязательны. Если секция неприменима — stub-текст в курсиве. Удалять секцию запрещено.

---

## 6. Автозагрузка через rules

Каждый per-tech стандарт подключается через rule в `.claude/rules/`. Rule автоматически включается в контекст при работе с файлами, соответствующими паттерну `globs`.

**Расположение rule:**
```
.claude/rules/{tech}.md
```

**Содержимое rule:**

```markdown
---
description: Автозагрузка стандарта {Technology} при работе с файлами.
standard: .claude/.instructions/rules/standard-rule.md
standard-version: v1.1
index: .claude/.instructions/rules/README.md
globs:
  - {паттерн файлов}
---

При работе с {Technology}-файлами ОБЯЗАТЕЛЬНО следовать:
- [standard-{tech}.md](/specs/docs/.technologies/standard-{tech}.md)
```

**Паттерны globs (примеры):**

| Технология | Globs |
|-----------|-------|
| Python | `src/**/*.py`, `tests/**/*.py` |
| TypeScript | `src/**/*.ts`, `src/**/*.tsx` |
| PostgreSQL | `src/**/database/**`, `**/*.sql` |
| Redis | `src/**/cache/**`, `src/**/redis/**` |

Rule создаётся вместе с per-tech стандартом (см. [create-technology.md](./create-technology.md)).

---

## 7. Регистрация в README

При создании per-tech стандарта обновить `specs/docs/README.md` в двух местах:

**1. Таблица «Стандарты технологий»:**

```markdown
| {Technology} | [standard-{tech}.md](.technologies/standard-{tech}.md) |
```

Строки сортируются по имени технологии `{tech}` (kebab-case, по первому символу): a, b, c... Пример: `fastapi` перед `postgresql`.

**2. Дерево:**

Добавить `├── standard-{tech}.md` в дерево `.technologies/` (алфавитный порядок по `{tech}`).

---

## 8. Версионирование

Версия per-tech стандарта указывается в заголовке h1: `# Стандарт {Technology} v{X.Y}`.

**Правила обновления версии:**

| Изменение | Действие |
|-----------|----------|
| Добавлен паттерн, уточнена конвенция | Минорная: v1.0 → v1.1 |
| Изменена мажорная версия технологии (PostgreSQL 16 → 17) | Мажорная: v1.x → v2.0 |
| Исправлена опечатка, перефразирование | Без изменения версии |

При изменении мажорной версии технологии — обновить per-tech стандарт через [modify-technology.md](./modify-technology.md).

---

## 9. Шаблон

`````markdown
---
description: Стандарт кодирования {Technology} — конвенции именования, паттерны, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: {tech}
---

# Стандарт {Technology} v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | {version} |
| Ключевые библиотеки | {lib1} {ver}, {lib2} {ver} |
| Конфигурация | {где лежит конфиг, ключевые параметры} |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| {объект} | {правило} | `{пример}` |

## Паттерны кода

<!-- Если паттерны применимы: -->

### {Операция 1: подключение / запрос / транзакция / ...}

{Когда использовать.}

```{lang}
{код — рабочий пример, готовый к копированию}
```

### {Операция 2}

...

<!-- Если паттерны не применимы: -->
<!-- *Паттерны кода не применимо — {причина}.* -->

## Антипаттерны

<!-- Если антипаттерны применимы: -->

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| {что делают неправильно} | {последствия} | {как правильно} |

<!-- Если антипаттерны не применимы: -->
<!-- *Антипаттерны не применимо — {причина}.* -->

## Структура файлов

<!-- Если структура применима: -->

```
src/{svc}/
├── {dir}/          # {назначение}
│   └── {file}      # {назначение}
└── {dir}/          # {назначение}
```

<!-- Если структура не применима: -->
<!-- *Структура файлов не применимо — {причина}.* -->

## Валидация

<!-- Вариант А — скрипт создан: -->
```bash
python specs/.instructions/.scripts/validate-{tech}-code.py [путь]
```

Скрипт проверяет: {перечень проверок}.
Включён в pre-commit hook: запускается автоматически при коммите файлов `{glob-паттерн}`.

<!-- Вариант Б — скрипт не создан: -->
<!-- *Скрипт валидации кода не создан. Валидация выполняется вручную по чек-листу из [validation-technology.md](./validation-technology.md).* -->

## Тестирование

<!-- Если тестирование применимо: -->

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| {фреймворк} | `{package}` | {зачем} |

### Фикстуры

```{lang}
{код фикстуры — готовый к копированию}
```

### Мокирование

{Когда мокировать, когда нет.}

```{lang}
{код мока — готовый к копированию}
```

### Паттерны тестов

```{lang}
{код теста — готовый к копированию}
```

<!-- Если тестирование не применимо: -->
<!-- *Тестирование не применимо — {причина}.* -->

## Логирование

<!-- Если логирование применимо: -->

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| {событие} | {INFO/WARNING/ERROR} | `{пример}` |

```{lang}
{код — настройка логгера для этой технологии}
```

<!-- Если логирование не применимо: -->
<!-- *Логирование не применимо — технология не генерирует событий, требующих логирования.* -->
`````

---

## 10. Пример

### standard-postgresql.md

`````markdown
---
description: Стандарт кодирования PostgreSQL — конвенции именования, SQLAlchemy, Alembic, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: postgresql
---

# Стандарт PostgreSQL v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | PostgreSQL 16 |
| Драйвер | asyncpg 0.29 (async), psycopg 3.1 (sync/migrations) |
| ORM | SQLAlchemy 2.0 (declarative, async engine) |
| Миграции | Alembic 1.13 |
| Конфигурация | `config/{env}/database.yaml`, connection pool: 5-20 |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| Таблица | snake_case, множественное число | `notifications`, `audit_logs` |
| Колонка | snake_case | `user_id`, `created_at` |
| Primary Key | `id` (UUID) | `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` |
| Foreign Key | `{referenced_table_singular}_id` | `user_id`, `project_id` |
| Индекс | `idx_{table}_{columns}` | `idx_notifications_user_id` |
| Unique constraint | `uq_{table}_{columns}` | `uq_users_email` |
| Check constraint | `ck_{table}_{description}` | `ck_notifications_status` |
| Enum type | `{domain}_{name}_enum` | `notification_status_enum` |
| Миграция (Alembic) | `{NNNN}_{description}.py` | `0001_create_notifications.py` |

## Паттерны кода

### Определение модели (SQLAlchemy 2.0)

Все модели наследуют от общего Base. Каждая модель — отдельный класс в `models.py`.

```python
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID, nullable=False, index=True)
    type = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(10), nullable=False, server_default="unread")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
```

### Async-запрос с пагинацией

Стандартный паттерн для GET-списков с total count.

```python
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

async def get_notifications(
    session: AsyncSession,
    user_id: str,
    limit: int = 20,
    offset: int = 0,
    status: str | None = None,
) -> tuple[list[Notification], int]:
    query = select(Notification).where(Notification.user_id == user_id)
    if status:
        query = query.where(Notification.status == status)

    total = await session.scalar(select(func.count()).select_from(query.subquery()))
    items = (await session.scalars(
        query.order_by(Notification.created_at.desc()).limit(limit).offset(offset)
    )).all()

    return items, total
```

### Транзакция с обработкой ошибок

При flush — ловить IntegrityError для дублей/нарушения constraints.

```python
from sqlalchemy.exc import IntegrityError

async def create_notification(session: AsyncSession, data: dict) -> Notification:
    notification = Notification(**data)
    session.add(notification)
    try:
        await session.flush()
    except IntegrityError as e:
        await session.rollback()
        raise DuplicateError(f"Notification already exists: {e}") from e
    return notification
```

### Миграция Alembic

Каждая миграция содержит `upgrade()` и `downgrade()`. Автогенерация — для простых случаев, ручные — для данных.

```python
"""create notifications table"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", UUID, nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("status", sa.String(10), nullable=False, server_default="unread"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_notifications_user_id", "notifications", ["user_id"])
    op.create_index("idx_notifications_created_at", "notifications", ["created_at"])

def downgrade() -> None:
    op.drop_table("notifications")
```

**Команды Alembic:**

```bash
alembic revision --autogenerate -m "add_status_index"   # Автогенерация из diff
alembic revision -m "backfill_notification_channels"     # Пустая (для ручного заполнения)
alembic upgrade head                                      # Применить все
alembic downgrade -1                                      # Откатить последнюю
alembic current                                           # Текущая ревизия
alembic history --verbose                                 # История
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| `SELECT *` | Лишние данные, ломается при добавлении колонок | Явно перечислять колонки или использовать ORM-модель |
| Строковая интерполяция в SQL | SQL-инъекция | Параметризованные запросы (SQLAlchemy bind params) |
| N+1 запросы | Экспоненциальный рост запросов | `joinedload()` / `selectinload()` для связей |
| Миграции без downgrade | Невозможно откатить | Всегда писать `downgrade()` |
| `nullable=True` по умолчанию | Неявные NULL в данных | Явно указывать `nullable=False` где возможно |
| Индексы на каждую колонку | Замедляет INSERT/UPDATE | Индексы только для частых WHERE / ORDER BY / JOIN |
| Большие транзакции | Блокировки, таймауты | Минимальные транзакции, batch-обработка для массовых операций |

## Структура файлов

```
src/{svc}/
├── database/
│   ├── models.py       # SQLAlchemy модели (Base, таблицы)
│   ├── repository.py   # Функции запросов (CRUD, специфичные)
│   ├── session.py      # AsyncSession factory, connection pool
│   └── migrations/
│       ├── env.py      # Alembic config
│       └── versions/   # Файлы миграций
└── ...
```

## Валидация

```bash
python specs/.instructions/.scripts/validate-postgresql-code.py [путь]
```

Скрипт проверяет: именование таблиц/колонок/индексов, наличие downgrade в миграциях, отсутствие `SELECT *` и строковой интерполяции.
Включён в pre-commit hook: запускается автоматически при коммите файлов `*.py` в `*/database/*` и `*/migrations/*`.

## Тестирование

Все тесты работающие с PostgreSQL используют pytest с async-поддержкой. Unit-тесты мокируют `AsyncSession`, integration-тесты поднимают реальную БД в Docker (через фикстуру). Factory Boy генерирует тестовые данные.

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| Фреймворк | `pytest 8.x` | Основной test runner |
| Async | `pytest-asyncio 0.23` | Поддержка async/await в тестах |
| Фабрики | `factory_boy 3.3` | Генерация тестовых моделей |
| Coverage | `pytest-cov` | Покрытие кода |

### Фикстуры

Базовая фикстура создаёт изолированную async-сессию с транзакцией, которая откатывается после каждого теста.

```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base

@pytest.fixture
async def db_engine():
    """Движок для тестовой БД (Docker: postgres://test:test@localhost:5433/test)."""
    engine = create_async_engine("postgresql+asyncpg://test:test@localhost:5433/test")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    """Сессия с транзакцией — откатывается после каждого теста."""
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()
```

### Мокирование

- **Unit-тесты:** мокируем `AsyncSession` целиком — тестируем логику, не SQL.
- **Integration-тесты:** реальная БД (Docker), не мокируем — тестируем запросы.

```python
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_session():
    """Мок AsyncSession для unit-тестов (без реальной БД)."""
    session = AsyncMock(spec=AsyncSession)
    session.scalar = AsyncMock(return_value=None)
    scalars_result = MagicMock()
    scalars_result.all.return_value = []
    session.scalars = AsyncMock(return_value=scalars_result)
    return session
```

### Паттерны тестов

```python
# --- Factory ---
import factory
from app.database.models import Notification

class NotificationFactory(factory.Factory):
    class Meta:
        model = Notification

    id = factory.Faker("uuid4")
    user_id = factory.Faker("uuid4")
    type = "info"
    title = factory.Faker("sentence")
    status = "unread"

# --- Unit-тест (мок) ---
async def test_create_notification_returns_model(mock_session):
    """Логика создания — без реальной БД."""
    data = {"user_id": "abc", "type": "info", "title": "Test"}
    result = await create_notification(mock_session, data)
    mock_session.add.assert_called_once()
    mock_session.flush.assert_awaited_once()

# --- Integration-тест (реальная БД) ---
async def test_get_notifications_filters_by_status(db_session):
    """Запрос с фильтром — реальная БД в Docker."""
    user_id = "550e8400-e29b-41d4-a716-446655440000"
    db_session.add(Notification(user_id=user_id, type="info", title="A", status="unread"))
    db_session.add(Notification(user_id=user_id, type="info", title="B", status="read"))
    await db_session.flush()

    items, total = await get_notifications(db_session, user_id, status="unread")
    assert total == 1
    assert items[0].title == "A"
```

## Логирование

SQLAlchemy и asyncpg имеют встроенное логирование через stdlib logging. По умолчанию SQL-запросы не логируются (шумно). В development можно включить echo, в production — только slow queries и ошибки.

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| Успешный запрос | DEBUG | `db.query_executed query="SELECT ..." duration_ms=12` |
| Slow query (>500ms) | WARNING | `db.slow_query query="SELECT ..." duration_ms=1250` |
| Connection pool exhausted | WARNING | `db.pool_exhausted pool_size=20 waiting=5` |
| Миграция применена | INFO | `db.migration_applied revision="0003" description="add_status_index"` |
| Ошибка подключения | ERROR | `db.connection_failed host="postgres" error="connection refused"` |
| IntegrityError | WARNING | `db.integrity_error table="notifications" constraint="uq_users_email"` |

**Настройка логирования SQLAlchemy:**

```python
import logging

# DEBUG = все запросы (dev), WARNING = только ошибки (prod)
logging.getLogger("sqlalchemy.engine").setLevel(
    logging.DEBUG if settings.debug else logging.WARNING
)
```
`````

---

## 11. Companion: security-{tech}.md

Для технологий с package manager или SAST-инструментами создаётся companion-файл
`security-{tech}.md` — описание инструментов безопасности.

**Расположение:**

    specs/docs/.technologies/security-{tech}.md

**Формат:** 5 обязательных h2-секций:

| # | Секция | Содержание |
|---|--------|-----------|
| 1 | Инструменты | Таблица инструментов |
| 2 | Dependency Audit | Команда + severity-модель |
| 3 | SAST | Конфигурация + правила |
| 4 | CI Integration | GitHub Actions job fragment |
| 5 | Known Exceptions | Suppressed правила |

**Frontmatter:** Содержит `type: security` (отличает от `standard-{tech}.md`).

**Шаблон:** См. [standard-security.md § 11](/.github/.instructions/actions/security/standard-security.md#11-per-tech-security-scanning).

**Когда создавать:** Вместе с `standard-{tech}.md` при /technology-create.
Критерий: технология имеет package manager (pip, npm, go mod) или SAST-инструмент.
