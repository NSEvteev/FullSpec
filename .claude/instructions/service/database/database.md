---
type: standard
description: Работа с базой данных — connection pooling, миграции, транзакции, saga pattern
related:
  - src/runtime/health.md
  - src/runtime/resilience.md
  - src/data/storage.md
---

# Database

Стандарт работы с базой данных: подключения, миграции, транзакции.

## Оглавление

- [Connection Pooling](#connection-pooling)
- [Миграции](#миграции)
- [Транзакции](#транзакции)
- [Saga Pattern](#saga-pattern)
- [Именование (snake_case)](#именование-snake_case)
- [Чек-лист](#чек-лист)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

## Connection Pooling

### Конфигурация пула

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Параметры пула
POOL_CONFIG = {
    "pool_size": 10,           # Базовый размер пула
    "max_overflow": 20,        # Дополнительные подключения
    "pool_timeout": 30,        # Таймаут получения соединения
    "pool_recycle": 1800,      # Переподключение каждые 30 мин
    "pool_pre_ping": True,     # Проверка соединения перед использованием
}

engine = create_async_engine(
    DATABASE_URL,
    **POOL_CONFIG,
    echo=False,  # True только для отладки
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

### Использование сессий

```python
# Dependency Injection для FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Использование
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

### Мониторинг пула

```python
def get_pool_stats():
    """Статистика пула подключений."""
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "invalid": pool.invalidatedcount(),
    }
```

## Миграции

### Структура

```
/migrations/
  /versions/
    001_initial.py
    002_add_users_table.py
    003_add_orders_table.py
  alembic.ini
  env.py
```

### Именование миграций

```bash
# Формат: NNN_описание_snake_case.py
001_initial.py
002_create_users_table.py
003_add_email_to_users.py
004_create_orders_table.py
```

### Пример миграции

```python
"""Создание таблицы users.

Revision ID: 002
Revises: 001
Create Date: 2024-01-15 10:30:00
"""
from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])


def downgrade():
    op.drop_index("ix_users_email")
    op.drop_table("users")
```

### Команды

```bash
# Создать миграцию
alembic revision -m "add_orders_table"

# Применить все миграции
alembic upgrade head

# Откатить последнюю
alembic downgrade -1

# Проверить текущую версию
alembic current
```

## Транзакции

### Базовая транзакция

```python
async def create_order(db: AsyncSession, order_data: OrderCreate) -> Order:
    """Создание заказа в транзакции."""
    async with db.begin():
        # Всё внутри автоматически в транзакции
        order = Order(**order_data.dict())
        db.add(order)

        # Обновляем баланс
        await db.execute(
            update(User)
            .where(User.id == order_data.user_id)
            .values(balance=User.balance - order_data.total)
        )

        await db.flush()  # Получаем ID без коммита
        return order
    # Автоматический commit при выходе
```

### Вложенные транзакции (Savepoints)

```python
async def process_with_savepoint(db: AsyncSession):
    """Использование savepoints для частичного отката."""
    async with db.begin():
        # Основная операция
        await db.execute(insert(Log).values(message="started"))

        try:
            async with db.begin_nested():  # Savepoint
                await risky_operation(db)
        except Exception as e:
            # Откат только до savepoint
            logger.warning(f"Risky operation failed: {e}")
            await db.execute(insert(Log).values(message="risky_failed"))

        # Это сохранится в любом случае
        await db.execute(insert(Log).values(message="completed"))
```

### Уровни изоляции

```python
from sqlalchemy import text

async def read_committed_query(db: AsyncSession):
    """Запрос с конкретным уровнем изоляции."""
    await db.execute(text("SET TRANSACTION ISOLATION LEVEL READ COMMITTED"))
    # ... запросы


async def serializable_transaction(db: AsyncSession):
    """Сериализуемая транзакция для критичных операций."""
    await db.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
    async with db.begin():
        # Полная изоляция от других транзакций
        pass
```

## Saga Pattern

Для распределённых транзакций между сервисами.

### Архитектура

```
┌──────────────────────────────────────────────────────────────┐
│                        Saga Orchestrator                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   Step 1         Step 2          Step 3          Step 4      │
│  ┌───────┐     ┌───────┐       ┌───────┐       ┌───────┐    │
│  │Reserve│     │Charge │       │ Ship  │       │Notify │    │
│  │ Stock │────►│Payment│──────►│ Order │──────►│ User  │    │
│  └───┬───┘     └───┬───┘       └───┬───┘       └───────┘    │
│      │             │               │                         │
│      ▼             ▼               ▼                         │
│  Compensate    Compensate     Compensate                     │
│  (Release)     (Refund)       (Cancel)                       │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Реализация

```python
from dataclasses import dataclass
from typing import Callable, Awaitable, List
from enum import Enum


class SagaStepStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    COMPENSATED = "compensated"
    FAILED = "failed"


@dataclass
class SagaStep:
    name: str
    execute: Callable[..., Awaitable[None]]
    compensate: Callable[..., Awaitable[None]]
    status: SagaStepStatus = SagaStepStatus.PENDING


class Saga:
    """Оркестратор саги."""

    def __init__(self, name: str):
        self.name = name
        self.steps: List[SagaStep] = []
        self.completed_steps: List[SagaStep] = []

    def add_step(
        self,
        name: str,
        execute: Callable,
        compensate: Callable,
    ):
        self.steps.append(SagaStep(name, execute, compensate))

    async def execute(self, context: dict) -> bool:
        """Выполнение саги с автоматической компенсацией при ошибке."""
        for step in self.steps:
            try:
                logger.info(f"Saga {self.name}: executing {step.name}")
                await step.execute(context)
                step.status = SagaStepStatus.COMPLETED
                self.completed_steps.append(step)
            except Exception as e:
                logger.error(f"Saga {self.name}: {step.name} failed: {e}")
                step.status = SagaStepStatus.FAILED
                await self._compensate(context)
                return False
        return True

    async def _compensate(self, context: dict):
        """Откат выполненных шагов в обратном порядке."""
        for step in reversed(self.completed_steps):
            try:
                logger.info(f"Saga {self.name}: compensating {step.name}")
                await step.compensate(context)
                step.status = SagaStepStatus.COMPENSATED
            except Exception as e:
                logger.critical(
                    f"Saga {self.name}: compensation failed for {step.name}: {e}"
                )
                # Требуется ручное вмешательство
                raise SagaCompensationError(step.name, e)
```

### Пример использования

```python
async def create_order_saga(order_data: dict) -> bool:
    """Сага создания заказа."""
    saga = Saga("create_order")

    # Шаг 1: Резервирование товара
    saga.add_step(
        "reserve_stock",
        execute=lambda ctx: stock_service.reserve(ctx["items"]),
        compensate=lambda ctx: stock_service.release(ctx["reservation_id"]),
    )

    # Шаг 2: Списание оплаты
    saga.add_step(
        "charge_payment",
        execute=lambda ctx: payment_service.charge(ctx["user_id"], ctx["total"]),
        compensate=lambda ctx: payment_service.refund(ctx["payment_id"]),
    )

    # Шаг 3: Создание доставки
    saga.add_step(
        "create_shipment",
        execute=lambda ctx: shipping_service.create(ctx["address"]),
        compensate=lambda ctx: shipping_service.cancel(ctx["shipment_id"]),
    )

    # Шаг 4: Уведомление (без компенсации)
    saga.add_step(
        "notify_user",
        execute=lambda ctx: notification_service.send(ctx["user_id"], "order_created"),
        compensate=lambda ctx: None,  # Уведомление не откатывается
    )

    return await saga.execute(order_data)
```

## Именование (snake_case)

### Таблицы и колонки

```python
# Правильно: snake_case
class UserOrder(Base):
    __tablename__ = "user_orders"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    total_amount = Column(Numeric(10, 2))
    created_at = Column(DateTime(timezone=True))
    shipping_address_id = Column(BigInteger)


# Неправильно
class UserOrder(Base):
    __tablename__ = "UserOrders"  # PascalCase

    userId = Column(...)  # camelCase
    TotalAmount = Column(...)  # PascalCase
```

### Индексы и constraints

```python
# Формат: {тип}_{таблица}_{колонки}
Index("ix_users_email", User.email)
Index("ix_orders_user_id_created_at", Order.user_id, Order.created_at)

UniqueConstraint("email", name="uq_users_email")
ForeignKeyConstraint(
    ["user_id"],
    ["users.id"],
    name="fk_orders_user_id",
)
```

## Чек-лист

- [ ] Connection pool настроен (pool_size, overflow, recycle)
- [ ] `pool_pre_ping=True` для проверки соединений
- [ ] Миграции пронумерованы и названы в snake_case
- [ ] Транзакции используют `async with db.begin()`
- [ ] Savepoints для частичного отката
- [ ] Saga pattern для распределённых транзакций
- [ ] Все имена в БД — snake_case
- [ ] Индексы и constraints именованы по шаблону

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование схемы БД |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при миграциях |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |

---

## Связанные инструкции

- [health.md](health.md) — проверка подключения к БД
- [resilience.md](resilience.md) — повторы при ошибках БД
- [src/data/storage.md](../data/storage.md) — хранение данных
