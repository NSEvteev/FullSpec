---
description: Стандарт кодирования PostgreSQL — конвенции именования, SQLAlchemy, Alembic, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: postgresql
---

# Стандарт PostgreSQL v1.0

> **Стек:** Этот стандарт описывает доступ к PostgreSQL через Python/SQLAlchemy стек (asyncpg, SQLAlchemy 2.0, Alembic). Для TypeScript-сервисов, использующих Prisma ORM, см. [standard-prisma.md](./standard-prisma.md).

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | PostgreSQL 16 |
| Ключевые библиотеки | asyncpg 0.29 (async-драйвер), psycopg 3.1 (sync/migrations), SQLAlchemy 2.0 (ORM, async engine), Alembic 1.13 (миграции) |
| Конфигурация | `config/{env}/database.yaml`; connection pool: min=5, max=20, timeout=30s |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| Таблица | snake_case, множественное число | `users`, `task_comments`, `audit_logs` |
| Колонка | snake_case | `user_id`, `created_at`, `is_active` |
| Primary Key | `id` (UUID), server-generated | `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` |
| Foreign Key | `{referenced_table_singular}_id` | `user_id`, `task_id` |
| Индекс | `idx_{table}_{columns}` | `idx_tasks_user_id`, `idx_users_email` |
| Unique constraint | `uq_{table}_{columns}` | `uq_users_email`, `uq_tasks_slug` |
| Check constraint | `ck_{table}_{description}` | `ck_tasks_status`, `ck_users_role` |
| Enum type | `{domain}_{name}_enum` | `task_status_enum`, `user_role_enum` |
| SQLAlchemy-модель | PascalCase, singular | `User`, `Task`, `AuditLog` |
| Repository-функция | `{verb}_{entity}[_{qualifier}]` | `get_user_by_id`, `list_tasks_by_user`, `create_task` |
| Миграция (Alembic) | `{NNNN}_{description}.py` | `0001_create_users.py`, `0002_add_task_status_index.py` |

## Паттерны кода

### Подключение и настройка сессии

Async-движок создаётся один раз при старте приложения. Используется `AsyncSession` через dependency injection (FastAPI).

```python
# src/{svc}/database/session.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=15,
    pool_timeout=30,
    echo=False,  # True только для отладки
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_session() -> AsyncSession:
    """FastAPI dependency — возвращает сессию с автоматическим закрытием."""
    async with AsyncSessionFactory() as session:
        yield session
```

### Определение модели (SQLAlchemy 2.0)

Все модели наследуют от общего `Base`. Каждая модель — отдельный класс в `models.py`. UUID генерируется на стороне БД.

```python
# src/{svc}/database/models.py
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import UUID
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    email = Column(String(255), nullable=False, unique=True)
    role = Column(String(20), nullable=False, server_default="user")
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, server_default="pending")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
```

### Запросы с пагинацией

Стандартный паттерн для GET-списков с total count. Используется `select()` + `func.count()`.

```python
# src/{svc}/database/repository.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Task

async def list_tasks(
    session: AsyncSession,
    user_id: str,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Task], int]:
    query = select(Task).where(Task.user_id == user_id)
    if status:
        query = query.where(Task.status == status)

    total = await session.scalar(
        select(func.count()).select_from(query.subquery())
    )
    items = (
        await session.scalars(
            query.order_by(Task.created_at.desc()).limit(limit).offset(offset)
        )
    ).all()

    return list(items), total or 0

async def get_task_by_id(session: AsyncSession, task_id: str) -> Task | None:
    return await session.get(Task, task_id)
```

### Транзакция с обработкой ошибок

При `flush` ловить `IntegrityError` для нарушения constraints (дубли, FK-нарушения). Транзакция управляется сессией.

```python
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Task

class DuplicateError(Exception):
    pass

class NotFoundError(Exception):
    pass

async def create_task(session: AsyncSession, user_id: str, title: str, description: str | None = None) -> Task:
    task = Task(user_id=user_id, title=title, description=description)
    session.add(task)
    try:
        await session.flush()
    except IntegrityError as e:
        await session.rollback()
        raise DuplicateError(f"Task already exists or FK violation: {e}") from e
    return task

async def update_task_status(session: AsyncSession, task_id: str, status: str) -> Task:
    task = await session.get(Task, task_id)
    if task is None:
        raise NotFoundError(f"Task {task_id} not found")
    task.status = status
    await session.flush()
    return task

async def delete_task(session: AsyncSession, task_id: str) -> None:
    task = await session.get(Task, task_id)
    if task is None:
        raise NotFoundError(f"Task {task_id} not found")
    await session.delete(task)
    await session.flush()
```

### Миграция Alembic

Каждая миграция содержит `upgrade()` и `downgrade()`. Автогенерация — для DDL-изменений, ручные — для данных.

```python
# src/{svc}/database/migrations/versions/0001_create_users_and_tasks.py
"""create users and tasks tables"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_users_email", "users", ["email"])
    op.create_unique_constraint("uq_users_email", "users", ["email"])

    op.create_table(
        "tasks",
        sa.Column("id", UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", UUID, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_tasks_user_id", "tasks", ["user_id"])
    op.create_index("idx_tasks_created_at", "tasks", ["created_at"])

def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("users")
```

**Команды Alembic:**

```bash
alembic revision --autogenerate -m "add_task_status_index"   # Автогенерация из diff моделей
alembic revision -m "backfill_user_roles"                    # Пустая (для ручного заполнения данных)
alembic upgrade head                                          # Применить все миграции
alembic downgrade -1                                          # Откатить последнюю
alembic current                                               # Текущая ревизия
alembic history --verbose                                     # История миграций
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| `SELECT *` в запросах | Лишние данные по сети; ломается при добавлении колонок с side-эффектами | Явно перечислять нужные колонки или использовать ORM-модель целиком |
| Строковая интерполяция в SQL (`f"WHERE id = {user_id}"`) | SQL-инъекция — злоумышленник может выполнить произвольный запрос | Параметризованные запросы: SQLAlchemy bind params или `asyncpg` `$1` плейсхолдеры |
| N+1 запросы (загрузка связей в цикле) | Экспоненциальный рост числа запросов; при 100 items — 101 запрос | `joinedload()` или `selectinload()` для eager loading связей |
| Миграции без `downgrade()` | Невозможно откатить миграцию при деплойменте без ручного вмешательства | Всегда писать `downgrade()` с обратным действием |
| `nullable=True` по умолчанию (неявный NULL) | Неявные NULL в данных приводят к `NullPointerException` на уровне приложения | Явно указывать `nullable=False` где поле обязательно; `nullable=True` — только осознанное решение |
| Индекс на каждую колонку | Замедляет INSERT/UPDATE/DELETE на 10–30% за каждый индекс | Индексы только для колонок в частых `WHERE`, `ORDER BY`, `JOIN` условиях |
| Большие транзакции (часы/минуты) | Блокировки таблиц и строк; таймаут; deadlocks | Минимальные транзакции по операции; batch-обработка массовых данных отдельными транзакциями |
| `session.commit()` внутри репозитория | Репозиторий нарушает управление транзакциями — невозможно группировать операции | Только `session.flush()`; commit управляется на уровне use-case или middleware |
| Хардкод `SERIAL` / `INTEGER` для PK | Исчерпание диапазона при масштабировании; проблемы при merge/sharding | Использовать `UUID` с `gen_random_uuid()` |

## Структура файлов

```
src/{svc}/
├── database/
│   ├── models.py           # SQLAlchemy-модели (Base, все таблицы сервиса)
│   ├── repository.py       # Функции CRUD и специфичных запросов
│   ├── session.py          # AsyncSession factory, движок, Base, get_session()
│   └── migrations/
│       ├── env.py          # Alembic config (автоimport моделей)
│       ├── script.py.mako  # Шаблон файла миграции
│       └── versions/       # Файлы миграций (NNNN_description.py)
└── ...
```

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется вручную по чек-листу из [validation-technology.md](/specs/.instructions/docs/technology/validation-technology.md).*

## Тестирование

Все тесты, работающие с PostgreSQL, используют `pytest` с async-поддержкой. Unit-тесты мокируют `AsyncSession`, integration-тесты поднимают реальную БД в Docker (через фикстуру). `factory_boy` генерирует тестовые данные.

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| Фреймворк | `pytest 8.x` | Основной test runner |
| Async | `pytest-asyncio 0.23` | Поддержка `async def` тестов |
| Фабрики | `factory_boy 3.3` | Генерация тестовых объектов моделей |
| Coverage | `pytest-cov` | Измерение покрытия кода |

### Фикстуры

Базовая фикстура создаёт изолированную async-сессию с транзакцией, которая откатывается после каждого теста. Тестовая БД — отдельный Docker-контейнер (порт 5433).

```python
# src/{svc}/tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.database.session import Base

TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5433/test"

@pytest.fixture(scope="session")
async def db_engine():
    """Движок тестовой БД — создаётся один раз на всю сессию."""
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    """Сессия с транзакцией — откатывается после каждого теста."""
    AsyncSessionFactory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionFactory() as session:
        async with session.begin():
            yield session
            await session.rollback()
```

### Мокирование

- **Unit-тесты:** мокируем `AsyncSession` целиком — тестируем логику репозитория без реального SQL.
- **Integration-тесты:** реальная БД в Docker, не мокируем — тестируем запросы и constraints.

```python
# src/{svc}/tests/unit/conftest.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
def mock_session():
    """Мок AsyncSession для unit-тестов (без реальной БД)."""
    session = AsyncMock(spec=AsyncSession)
    session.get = AsyncMock(return_value=None)
    session.scalar = AsyncMock(return_value=0)
    scalars_result = MagicMock()
    scalars_result.all.return_value = []
    session.scalars = AsyncMock(return_value=scalars_result)
    session.add = MagicMock()
    session.delete = AsyncMock()
    session.flush = AsyncMock()
    session.rollback = AsyncMock()
    return session
```

### Паттерны тестов

```python
# --- Factory (src/{svc}/tests/factories.py) ---
import factory
from app.database.models import User, Task

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Faker("uuid4")
    email = factory.Faker("email")
    role = "user"
    is_active = True

class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    id = factory.Faker("uuid4")
    user_id = factory.Faker("uuid4")
    title = factory.Faker("sentence", nb_words=4)
    status = "pending"

# --- Unit-тест (мок сессии) ---
import pytest
from app.database.repository import create_task, NotFoundError, DuplicateError
from sqlalchemy.exc import IntegrityError

async def test_create_task_calls_flush(mock_session):
    """Проверяем, что create_task добавляет модель и вызывает flush."""
    result = await create_task(mock_session, user_id="abc", title="My Task")
    mock_session.add.assert_called_once()
    mock_session.flush.assert_awaited_once()
    assert result.title == "My Task"

async def test_create_task_raises_duplicate_on_integrity_error(mock_session):
    """IntegrityError при flush → DuplicateError."""
    mock_session.flush.side_effect = IntegrityError("", {}, Exception())
    with pytest.raises(DuplicateError):
        await create_task(mock_session, user_id="abc", title="Duplicate")

# --- Integration-тест (реальная БД) ---
async def test_list_tasks_filters_by_status(db_session):
    """Фильтрация по статусу возвращает только matching задачи."""
    user_id = "550e8400-e29b-41d4-a716-446655440000"
    db_session.add(Task(user_id=user_id, title="A", status="pending"))
    db_session.add(Task(user_id=user_id, title="B", status="done"))
    await db_session.flush()

    from app.database.repository import list_tasks
    items, total = await list_tasks(db_session, user_id=user_id, status="pending")
    assert total == 1
    assert items[0].title == "A"
```

## Логирование

SQLAlchemy и asyncpg имеют встроенное логирование через stdlib `logging`. По умолчанию SQL-запросы не логируются (слишком шумно). В production логируются только slow queries и ошибки.

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| Успешный запрос | DEBUG | `db.query_executed query="SELECT ..." duration_ms=8` |
| Slow query (>500ms) | WARNING | `db.slow_query query="SELECT tasks WHERE ..." duration_ms=1340` |
| Pool exhausted | WARNING | `db.pool_exhausted pool_size=20 waiting=3` |
| Миграция применена | INFO | `db.migration_applied revision="0002" description="add_task_status_index"` |
| Ошибка подключения | ERROR | `db.connection_failed host="postgres" port=5432 error="connection refused"` |
| IntegrityError | WARNING | `db.integrity_error table="tasks" constraint="uq_tasks_slug" detail="Key already exists"` |

```python
# src/{svc}/database/session.py (logging setup — добавить при инициализации)
import logging

def configure_db_logging(debug: bool = False) -> None:
    """Настройка логирования SQLAlchemy: DEBUG в dev, WARNING в prod."""
    level = logging.DEBUG if debug else logging.WARNING
    logging.getLogger("sqlalchemy.engine").setLevel(level)
    logging.getLogger("sqlalchemy.pool").setLevel(level)
    # asyncpg логирует через asyncio — WARNING всегда
    logging.getLogger("asyncpg").setLevel(logging.WARNING)
```
