# docs/.technologies/standard-{tech}.md — стандарт кодирования технологии

Спецификация per-tech стандарта: секции, шаблон, пример standard-postgresql.md. Конвенции и паттерны для LLM-разработчика при написании кода с конкретной технологией.

## Контекст

**Задача:** Определить формат docs/.technologies/standard-{tech}.md — per-tech стандарта кодирования, самодостаточного документа для написания кода.

**Источник:** `.claude/drafts/2026-02-19-sdd-chain-rethink.md` (строки 2014-2451)

**Связанные файлы:**
- `2026-02-19-sdd-structure.md` — общая структура и решения
- `2026-02-19-sdd-docs-service.md` — {svc}.md ссылается на standard-{tech}.md из секции Code Map / Tech Stack
- `2026-02-19-sdd-docs-testing.md` — testing.md задаёт стратегию, standard-{tech}.md содержит per-tech тестовые паттерны
- `2026-02-19-sdd-docs-conventions.md` — conventions.md содержит кросс-сервисные конвенции, standard-{tech}.md — per-tech

---

## Содержание

Конвенции и паттерны, которые LLM-разработчик применяет при написании кода с данной технологией. Каждый стандарт самодостаточен: прочитал — можешь писать код.

### Секции docs/.technologies/standard-{tech}.md

| # | Секция | Содержание | Зачем LLM-разработчику |
|---|--------|-----------|----------------------|
| 1 | **Версия и настройка** | Версия технологии, ключевые библиотеки, конфигурация | Знать какую версию использовать и как настроить |
| 2 | **Конвенции именования** | Таблицы, колонки, индексы (для DB) / функции, переменные, файлы (для языков) | Писать код в едином стиле без угадывания |
| 3 | **Паттерны кода** | Типовые операции с примерами: подключение, запрос, обработка ошибок, транзакции | Копировать рабочий паттерн вместо изобретения своего |
| 4 | **Антипаттерны** | Что НЕ делать — с объяснением почему | Не наступать на грабли |
| 5 | **Структура файлов** | Где размещать код, как организовать модули | Положить файл в правильное место |
| 6 | **Валидация** | Ссылка на скрипт валидации, команда запуска | Проверить свой код перед коммитом |
| 7 | **Тестирование** | Фреймворк, фикстуры, мокирование для данной технологии, паттерны тестов | Писать тесты по конвенции проекта, правильно мокировать технологию |
| 8 | **Логирование** | Что логировать при работе с этой технологией, уровни для типовых операций | Логировать правильные события на правильном уровне |

### Шаблон: docs/.technologies/standard-{tech}.md

`````markdown
# Стандарт {Technology} v{X.Y}

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

### {Операция 1: подключение / запрос / транзакция / ...}

{Когда использовать.}

```{lang}
{код — рабочий пример, готовый к копированию}
```

### {Операция 2}

...

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| {что делают неправильно} | {последствия} | {как правильно} |

## Структура файлов

```
src/{svc}/
├── {dir}/          # {назначение}
│   └── {file}      # {назначение}
└── {dir}/          # {назначение}
```

## Валидация

```bash
python .scripts/validate-{tech}.py [путь]    # Проверить файлы
```

Скрипт проверяет: {что именно проверяет — именование, паттерны, антипаттерны}.
Включён в pre-commit hook: запускается автоматически при коммите файлов `{glob-паттерн}`.

## Тестирование

{Какой фреймворк и плагины использовать для тестирования кода с этой технологией. Как настроить фикстуры, как мокировать — с готовыми к копированию примерами.}

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| {фреймворк} | `{package}` | {зачем} |
| {плагин} | `{package}` | {зачем} |

### Фикстуры

{Базовые фикстуры для тестов с этой технологией — подключение, очистка, seed-данные.}

```{lang}
{код фикстуры — готовый к копированию}
```

### Мокирование

{Когда и как мокировать эту технологию. В каких типах тестов мокируем, в каких — используем реальный экземпляр.}

```{lang}
{код мока — готовый к копированию}
```

### Паттерны тестов

{Типовые тестовые сценарии для этой технологии — CRUD, ошибки, edge cases.}

```{lang}
{код теста — готовый к копированию}
```

## Логирование

{Что логировать при работе с этой технологией. Какие события на каком уровне. Специфичные для технологии настройки логирования.}

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| {событие} | {INFO/WARNING/ERROR} | `{пример}` |

**Настройка логирования {tech}:**

```{lang}
{код — настройка логгера для этой технологии}
```
`````

### Пример: docs/.technologies/standard-postgresql.md

`````markdown
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

**Команды Alembic** (прямые вызовы, make-таргеты — в [Makefile](/Makefile)):

```bash
# Создать миграцию (автогенерация из diff моделей vs БД)
alembic revision --autogenerate -m "add_status_index"

# Создать пустую миграцию (для ручного заполнения)
alembic revision -m "backfill_notification_channels"

# Применить все непримененные
alembic upgrade head

# Откатить последнюю
alembic downgrade -1

# Проверить текущую ревизию
alembic current

# История миграций
alembic history --verbose
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
python .scripts/validate-postgresql.py [путь]    # Проверить SQL/модели
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

Базовая фикстура создаёт изолированную async-сессию с транзакцией, которая откатывается после каждого теста. Это быстрее пересоздания схемы и гарантирует изоляцию.

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
    # scalar() возвращает значение напрямую
    session.scalar = AsyncMock(return_value=None)
    # scalars() возвращает объект с .all()
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
import structlog

# Уровень для SQLAlchemy engine (SQL-запросы)
# DEBUG = все запросы, WARNING = только ошибки (production)
logging.getLogger("sqlalchemy.engine").setLevel(
    logging.DEBUG if settings.debug else logging.WARNING
)

# Slow query middleware (добавить в session events)
from sqlalchemy import event

@event.listens_for(AsyncSession, "after_execute")
def log_slow_queries(conn, clauseelement, multiparams, params, execution_options, result):
    duration = execution_options.get("duration_ms", 0)
    if duration > 500:
        logger.warning("db.slow_query", query=str(clauseelement)[:200], duration_ms=duration)
```
`````

---

## Аудит старых документов

| Старый документ | Что переиспользовать |
|-----------------|---------------------|
| `specs/.instructions/technologies/standard-technology.md` | Мета-стандарт: именование (kebab-case), frontmatter (technology поле), триггер Design→WAITING, автозагрузка через rules, связь с Code Map |
| `specs/.instructions/technologies/validation-technology.md` | Коды TECH001-TECH011, проверка конфликтов с standard-principles.md (TECH007), rule как обязательный артефакт (TECH010), реестр (TECH011) |
| `specs/.instructions/technologies/create-technology.md` | Воркфлоу создания |
| `specs/.instructions/technologies/modify-technology.md` | Воркфлоу обновления |
| `specs/technologies/standard-postgresql.md` | Текущий per-tech стандарт (сравнить с новым шаблоном) |
| `specs/technologies/standard-redis.md` | Ещё один пример per-tech стандарта |
| `specs/.instructions/.scripts/validate-technology.py` | Скрипт валидации (основа для нового) |
| `specs/.instructions/.scripts/validate-postgresql-code.py` | Per-tech скрипт валидации |
| `specs/.instructions/.scripts/validate-redis-code.py` | Per-tech скрипт валидации |
