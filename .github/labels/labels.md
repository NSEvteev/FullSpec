# Метки проекта

**SSOT:** Этот файл — единственный источник истины для меток проекта.

**Инструкции:** [.instructions/labels/standard-labels.md](../.instructions/labels/standard-labels.md)

---

## Категории

| Категория | Префикс | Цвет (HEX) | Назначение |
|-----------|---------|------------|------------|
| **type** | `type:` | `0075ca` | Тип задачи |
| **priority** | `priority:` | градиент | Приоритет (critical → low) |
| **status** | `status:` | `8B5CF6` | Статус работы |
| **area** | `area:` | `10B981` | Область кода |
| **effort** | `effort:` | `6B7280` | Оценка трудозатрат |
| **env** | `env:` | `F59E0B` | Окружение (только для багов) |

---

## Метки

### type (Тип задачи)

| Метка | Цвет | Описание |
|-------|------|----------|
| `type:bug` | `0075ca` | Баг — нечто работает не так, как ожидалось |
| `type:feature` | `0075ca` | Новая функциональность |
| `type:task` | `0075ca` | Техническая задача (рефакторинг, настройка CI) |
| `type:docs` | `0075ca` | Документация |
| `type:refactor` | `0075ca` | Рефакторинг без изменения функциональности |

### priority (Приоритет)

| Метка | Цвет | Описание | Критерии |
|-------|------|----------|----------|
| `priority:critical` | `d73a4a` | Блокирует релиз | Production down, security issue, data loss |
| `priority:high` | `FF6B6B` | Высокий приоритет | Фичи текущего спринта, баги с влиянием >30% пользователей |
| `priority:medium` | `FFA500` | Средний приоритет | Стандартные задачи |
| `priority:low` | `FFD700` | Низкий приоритет | Nice-to-have, технический долг |

### status (Статус)

| Метка | Цвет | Описание |
|-------|------|----------|
| `status:blocked` | `8B5CF6` | Заблокировано (ожидает зависимости) |
| `status:in-review` | `8B5CF6` | На code review |
| `status:ready` | `8B5CF6` | Готово к работе |
| `status:wip` | `8B5CF6` | Work in Progress |

### area (Область кода)

| Метка | Цвет | Описание | Пути |
|-------|------|----------|------|
| `area:backend` | `10B981` | Бэкенд (API, БД, бизнес-логика) | `/src/*/backend/` |
| `area:frontend` | `10B981` | Фронтенд (UI, UX) | `/src/*/frontend/` |
| `area:infra` | `10B981` | Инфраструктура (Docker, CI/CD) | `/platform/`, `.github/workflows/` |
| `area:api` | `10B981` | API (контракты, эндпоинты) | `/shared/contracts/` |
| `area:database` | `10B981` | База данных (миграции, схема) | `/src/*/database/` |
| `area:tests` | `10B981` | Тесты (unit, integration, e2e) | `/tests/`, `*/tests/` |
| `area:docs` | `10B981` | Документация | README, инструкции |

### effort (Трудозатраты)

| Метка | Цвет | Описание | Оценка |
|-------|------|----------|--------|
| `effort:xs` | `6B7280` | Очень маленькая задача | < 1 час |
| `effort:s` | `6B7280` | Маленькая задача | 1-4 часа |
| `effort:m` | `6B7280` | Средняя задача | 0.5-1 день |
| `effort:l` | `6B7280` | Большая задача | 1-3 дня |
| `effort:xl` | `6B7280` | Очень большая задача | > 3 дней (разбить!) |

### env (Окружение)

| Метка | Цвет | Описание | Ограничение |
|-------|------|----------|-------------|
| `env:production` | `F59E0B` | Проблема на production | Только для `type:bug` |
| `env:local` | `F59E0B` | Проблема в локальной разработке | Только для `type:bug` |

---

## labels.yml

Для синхронизации с GitHub используется `labels.yml`:

```yaml
labels:
  # === TYPE ===
  - name: "type:bug"
    description: "Баг — нечто работает не так, как ожидалось"
    color: "0075ca"
  - name: "type:feature"
    description: "Новая функциональность"
    color: "0075ca"
  - name: "type:task"
    description: "Техническая задача"
    color: "0075ca"
  - name: "type:docs"
    description: "Документация"
    color: "0075ca"
  - name: "type:refactor"
    description: "Рефакторинг"
    color: "0075ca"

  # === PRIORITY ===
  - name: "priority:critical"
    description: "Блокирует релиз"
    color: "d73a4a"
  - name: "priority:high"
    description: "Высокий приоритет"
    color: "FF6B6B"
  - name: "priority:medium"
    description: "Средний приоритет"
    color: "FFA500"
  - name: "priority:low"
    description: "Низкий приоритет"
    color: "FFD700"

  # === STATUS ===
  - name: "status:blocked"
    description: "Заблокировано"
    color: "8B5CF6"
  - name: "status:in-review"
    description: "На code review"
    color: "8B5CF6"
  - name: "status:ready"
    description: "Готово к работе"
    color: "8B5CF6"
  - name: "status:wip"
    description: "Work in Progress"
    color: "8B5CF6"

  # === AREA ===
  - name: "area:backend"
    description: "Бэкенд"
    color: "10B981"
  - name: "area:frontend"
    description: "Фронтенд"
    color: "10B981"
  - name: "area:infra"
    description: "Инфраструктура"
    color: "10B981"
  - name: "area:api"
    description: "API контракты"
    color: "10B981"
  - name: "area:database"
    description: "База данных"
    color: "10B981"
  - name: "area:tests"
    description: "Тесты"
    color: "10B981"
  - name: "area:docs"
    description: "Документация"
    color: "10B981"

  # === EFFORT ===
  - name: "effort:xs"
    description: "< 1 час"
    color: "6B7280"
  - name: "effort:s"
    description: "1-4 часа"
    color: "6B7280"
  - name: "effort:m"
    description: "0.5-1 день"
    color: "6B7280"
  - name: "effort:l"
    description: "1-3 дня"
    color: "6B7280"
  - name: "effort:xl"
    description: "> 3 дней"
    color: "6B7280"

  # === ENV ===
  - name: "env:production"
    description: "Проблема на production"
    color: "F59E0B"
  - name: "env:local"
    description: "Проблема в локальной разработке"
    color: "F59E0B"
```
