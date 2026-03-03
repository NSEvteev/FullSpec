---
description: Стандарт кодирования FastAPI — конвенции именования, роутеры, Pydantic-модели, антипаттерны.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: fastapi
---

# Стандарт FastAPI v1.0

## Версия и настройка

| Параметр | Значение |
|----------|----------|
| Версия | FastAPI 0.115 |
| Ключевые библиотеки | Uvicorn 0.32 (ASGI-сервер), Pydantic 2.10 (валидация), python-multipart 0.0.18 (формы) |
| Линтер | Ruff (`ruff check`) |
| Конфигурация | `pyproject.toml` — секция `[tool.ruff]`, `[tool.pytest.ini_options]` |

## Конвенции именования

| Объект | Конвенция | Пример |
|--------|----------|--------|
| Файл модуля | snake_case | `user_router.py`, `auth_service.py` |
| Расположение роутеров | `src/{svc}/backend/routers/` | `src/auth/backend/routers/auth.py` |
| Router variable | `router` (единственный на файл) | `router = APIRouter()` |
| Endpoint-функция | snake_case, глагол + существительное | `create_user`, `get_task_list` |
| Path parameter | snake_case в `{}` | `{user_id}`, `{task_id}` |
| Pydantic Request model | PascalCase + `Request` | `CreateUserRequest`, `UpdateTaskRequest` |
| Pydantic Response model | PascalCase + `Response` | `UserResponse`, `TaskListResponse` |
| Dependency | snake_case, имя по назначению | `get_current_user`, `get_db_session` |
| Settings class | `Settings` (единственный) | `class Settings(BaseSettings)` |
| Тег роутера | kebab-case, по домену | `user-management`, `auth` |

## Паттерны кода

### Инициализация приложения

Точка входа — `main.py`. Фабрика приложения создаёт FastAPI instance с метаданными и подключает роутеры.

```python
from fastapi import FastAPI

from app.routers import auth, users

def create_app() -> FastAPI:
    app = FastAPI(
        title="Auth Service API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url=None,
    )
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["user-management"])
    return app

app = create_app()
```

### Роутер с CRUD-операциями

Один файл — один роутер — один домен. Все endpoint-функции async. Pydantic-модели для request/response.

```python
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.dependencies import UserServiceDep
from app.models.user import CreateUserRequest, UserResponse, UpdateUserRequest

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: CreateUserRequest, service: UserServiceDep) -> UserResponse:
    """Создать нового пользователя."""
    return await service.create(body)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, service: UserServiceDep) -> UserResponse:
    """Получить пользователя по ID."""
    user = await service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID, body: UpdateUserRequest, service: UserServiceDep
) -> UserResponse:
    """Обновить пользователя."""
    user = await service.update(user_id, body)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, service: UserServiceDep) -> None:
    """Удалить пользователя."""
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
```

### Pydantic-модели (request / response)

Все модели наследуют от `BaseModel`. Request и Response — отдельные классы. `model_config` вместо внутреннего `Config`.

```python
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, model_validator


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=255)
    role: str = Field(default="user", pattern=r"^(user|admin)$")


class UpdateUserRequest(BaseModel):
    email: EmailStr | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)

    @model_validator(mode="before")
    @classmethod
    def check_at_least_one_field(cls, values: dict) -> dict:
        if not any(v is not None for v in values.values()):
            raise ValueError("At least one field must be provided")
        return values


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
```

### Dependency Injection

Зависимости — через `Depends()`. Каждая зависимость — отдельная async-функция. Вложенные зависимости допустимы. Конвенция: `Annotated`-алиасы для DI-типов используют суффикс `Dep` (`DbSessionDep`, `UserServiceDep`).

```python
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.services.user_service import UserService

DbSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def get_user_service(session: DbSessionDep) -> UserService:
    """Фабрика UserService с внедрённой сессией БД."""
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
```

В роутере импортировать `Dep`-алиасы и использовать в сигнатурах:

```python
from app.dependencies import UserServiceDep

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, service: UserServiceDep) -> UserResponse:
    """Получить пользователя по ID."""
    user = await service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
```

### Обработка ошибок

Единый формат ошибок через exception handler. `HTTPException` для бизнес-ошибок, custom exception handler для неожиданных.

```python
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Обработчик непредвиденных ошибок — единый формат ответа."""
    logger.error("Unhandled exception: %s %s", request.method, request.url, exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"code": "INTERNAL_ERROR", "message": "Internal server error"},
    )


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(Exception, unhandled_exception_handler)
    return app
```

### Пагинация

Стандартный паттерн для GET-списков с `limit`/`offset` и `total`. Generic-модель `PaginatedResponse` переиспользуется для всех list-endpoints.

```python
from typing import Generic, TypeVar

from fastapi import APIRouter, Query
from pydantic import BaseModel

T = TypeVar("T")

router = APIRouter()


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int


@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    service: UserServiceDep,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResponse[UserResponse]:
    """Список пользователей с пагинацией."""
    items, total = await service.list(limit=limit, offset=offset)
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)
```

### Настройки через Pydantic Settings

Конфигурация из переменных окружения. Один класс `Settings`, загрузка из `.env`.

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379"
    jwt_secret: str
    debug: bool = False

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
```

### Связь с SDD процессом

| Момент SDD | Действие с FastAPI |
|------------|-------------------|
| Design (SVC-N) | Определяет роутеры, endpoints, Pydantic-модели. Имена endpoint-функций: глагол из HTTP-метода + существительное из пути (`GET /users/{id}` → `get_user`) |
| Design (INT-N) | Определяет `prefix` роутера и формат контракта. `tags` — из имени домена SVC-N |
| INFRA-блок (wave 0) | Dev-agent создаёт `main.py`, базовую структуру, `dependencies.py` |
| Per-service блок | Dev-agent реализует роутеры, сервисы, Pydantic-модели по SVC-N |
| Design → DONE | Все endpoints реализованы, авто-OpenAPI (`/docs`) соответствует INT-N |

```python
# prefix берётся из INT-N (интеграционный контракт), tags — из имени домена SVC-N
# Пример: INT-1 определяет REST /api/v1/users, SVC-2 = user-management
app.include_router(users.router, prefix="/api/v1/users", tags=["user-management"])
```

## Антипаттерны

| Антипаттерн | Почему плохо | Правильно |
|-------------|-------------|-----------|
| Бизнес-логика в endpoint-функции | Нетестируемо, нарушает SRP | Вынести в service-слой |
| `def` вместо `async def` для IO-операций | Блокирует event loop | `async def` для всех IO |
| Inline Pydantic-модель (`body: BaseModel` с полями в декораторе) | Дублирование схемы при переиспользовании, OpenAPI docs показывает анонимный тип | Отдельный класс в `models/` |
| `response_model=dict` | Секретные поля (пароль, token) попадают в ответ; нет 422 при расхождении схемы; OpenAPI docs пустой | Типизированная Pydantic-модель |
| Глобальное состояние (модульные переменные) | Race conditions, сложность тестирования | Dependency Injection через `Depends()` |
| `except Exception` в endpoint без re-raise | Скрывает ошибки, 200 на невалидные данные | `HTTPException` с конкретным status code |
| Жёстко заданные URL других сервисов | staging/prod используют один адрес → ошибки при деплое, невозможно тестировать локально | `Settings` через env-переменные |
| `sync_to_async` / `run_in_executor` повсеместно | Теряется смысл async | Использовать async-библиотеки (httpx, asyncpg) |

## Структура файлов

```
src/{svc}/
├── backend/
│   ├── main.py              # Точка входа: create_app(), include_router
│   ├── config.py            # Settings (Pydantic BaseSettings)
│   ├── dependencies.py      # Общие зависимости (get_db_session, get_current_user)
│   ├── routers/
│   │   ├── auth.py          # Роутер авторизации
│   │   └── users.py         # Роутер пользователей
│   ├── models/
│   │   ├── auth.py          # Pydantic-модели: request/response для auth
│   │   └── users.py         # Pydantic-модели: request/response для users
│   ├── services/
│   │   ├── auth_service.py  # Бизнес-логика авторизации
│   │   └── user_service.py  # Бизнес-логика пользователей
│   └── middleware/
│       └── logging.py       # Middleware для логирования запросов
└── tests/
    ├── conftest.py           # Фикстуры: TestClient, mock-зависимости
    ├── test_auth.py          # Тесты роутера auth
    └── test_users.py         # Тесты роутера users
```

Правила размещения:
- Один файл роутера на один домен (совпадает с тегом)
- Pydantic-модели рядом с роутером (в `models/`)
- Бизнес-логика — в `services/`, не в роутерах
- Зависимости — в `dependencies.py` (общие) или в файле сервиса (приватные)

## Валидация

*Скрипт валидации кода не создан. Валидация выполняется линтером: `ruff check src/{svc}/backend/`. Pre-commit hook `ruff` запускает проверку для изменённых `.py` файлов.*

## Тестирование

Тесты FastAPI-приложения используют pytest с `httpx.AsyncClient` (async) или `TestClient` (sync). Unit-тесты мокируют зависимости через `app.dependency_overrides`. Integration-тесты используют реальные зависимости.

### Фреймворк и плагины

| Компонент | Пакет | Назначение |
|-----------|-------|-----------|
| Фреймворк | `pytest 8.x` | Основной test runner |
| Async | `pytest-asyncio 0.23` | Поддержка async/await в тестах |
| HTTP client | `httpx 0.28` | AsyncClient для тестирования endpoints |
| Coverage | `pytest-cov` | Покрытие кода |

### Фикстуры

Базовая фикстура создаёт `AsyncClient` с `app.dependency_overrides` для подмены зависимостей.

```python
import pytest
from unittest.mock import AsyncMock
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import create_app
from app.dependencies import get_db_session


@pytest.fixture
def mock_session():
    """Мок AsyncSession для подмены зависимости БД."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def app(mock_session):
    """FastAPI-приложение с подменёнными зависимостями."""
    application = create_app()
    application.dependency_overrides[get_db_session] = lambda: mock_session
    yield application
    application.dependency_overrides.clear()


@pytest.fixture
async def client(app):
    """Async HTTP-клиент для тестирования endpoints."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

### Мокирование

- **Unit-тесты:** подменяем зависимости через `app.dependency_overrides` — тестируем endpoint, не сервис.
- **Integration-тесты:** реальные зависимости (БД в Docker), не мокируем — тестируем полный путь.

```python
from unittest.mock import AsyncMock

from app.services.user_service import UserService


@pytest.fixture
def mock_user_service():
    """Мок UserService для unit-тестов endpoints."""
    service = AsyncMock(spec=UserService)
    service.get_by_id.return_value = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "test@example.com",
        "name": "Test User",
        "role": "user",
    }
    return service
```

### Паттерны тестов

```python
import pytest
from httpx import AsyncClient


async def test_create_user_returns_201(client: AsyncClient):
    """Создание пользователя — успешный сценарий."""
    response = await client.post(
        "/api/v1/users/",
        json={"email": "new@example.com", "name": "New User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data


async def test_get_user_not_found_returns_404(client: AsyncClient):
    """Запрос несуществующего пользователя — 404."""
    response = await client.get("/api/v1/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_create_user_invalid_email_returns_422(client: AsyncClient):
    """Невалидный email — Pydantic отклоняет с 422."""
    response = await client.post(
        "/api/v1/users/",
        json={"email": "not-an-email", "name": "Bad User"},
    )
    assert response.status_code == 422
```

## Логирование

| Событие | Уровень | Пример сообщения |
|---------|---------|-----------------|
| Входящий запрос | INFO | `http.request method="POST" path="/api/v1/users/" status=201 duration_ms=45` |
| Валидация Pydantic провалена | WARNING | `http.validation_error path="/api/v1/users/" errors=2` |
| Зависимость не доступна | ERROR | `app.dependency_failed name="get_db_session" error="connection refused"` |
| Запуск приложения | INFO | `app.started host="0.0.0.0" port=8000` |
| Остановка приложения | INFO | `app.shutdown reason="SIGTERM"` |

```python
import logging
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования HTTP-запросов."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.monotonic()
        response = await call_next(request)
        duration_ms = round((time.monotonic() - start) * 1000)
        logger.info(
            'http.request method="%s" path="%s" status=%d duration_ms=%d',
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
```
