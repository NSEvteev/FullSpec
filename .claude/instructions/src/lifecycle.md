---
type: standard
description: Lifecycle сервиса — создание, обновление, удаление
governed-by: services/README.md
related:
  - services/structure.md
  - services/dependencies.md
  - specs/impact.md
---

# Lifecycle сервиса

Правила создания, обновления и удаления сервисов.

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [services/README.md](./README.md)

## Оглавление

- [Когда создавать сервис](#когда-создавать-сервис)
- [Что создаётся](#что-создаётся)
- [Workflow создания](#workflow-создания)
- [Удаление/архивирование](#удалениеархивирование)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Когда создавать сервис

### Признаки необходимости нового сервиса

При анализе Impact может быть определено, что для реализации требуется **новый сервис**.

**Создавать новый сервис когда:**
- Функциональность не вписывается в существующие сервисы
- Требуется изоляция по причинам безопасности/производительности
- Новый bounded context в доменной модели
- Независимый lifecycle (деплой, масштабирование)

**НЕ создавать новый сервис когда:**
- Это просто новый модуль существующего сервиса
- Функциональность тесно связана с существующим сервисом
- Нет чёткой границы ответственности

### Точка принятия решения

Решение о создании нового сервиса принимается на этапе **Impact-анализа** (`/specs/impact/`).

> См. [specs/impact.md](../specs/impact.md) для деталей Impact-анализа.

---

## Что создаётся

При создании нового сервиса создаётся следующая структура:

| Папка | Назначение |
|-------|------------|
| `/src/{service}/` | Код сервиса (включая `docs/`) |
| `/tests/{service}/` | Тесты сервиса |
| `/specs/services/{service}/` | Спецификации (ADR, планы, архитектура) |

### Структура /src/{service}/

> **SSOT:** [structure.md](./structure.md)

```
/src/{service}/
├── README.md               # Точка входа
├── Makefile                # Команды сервиса
├── dependencies.yaml       # Зависимости
├── .env.example            # Переменные окружения
├── /backend/               # Серверный код
├── /frontend/              # Клиентский код (опционально)
├── /database/              # Схема и миграции
├── /tests/                 # Unit тесты
└── /docs/                  # Документация сервиса
```

### Структура /specs/services/{service}/

```
/specs/services/{service}/
├── README.md               # Описание и статус сервиса
├── architecture.md         # Архитектура сервиса
├── adr/
│   ├── README.md           # Индекс ADR
│   └── 001-initial.md      # Начальный ADR
└── plans/
    └── README.md           # Индекс планов
```

---

## Workflow создания

### Триггер

Создание сервиса инициируется через скилл `/spec-create adr` с флагом `--new`:

```
/spec-create adr <impact-id> <service-name> --new
```

### Диаграмма

```
Impact определяет: нужен новый сервис
    │
    ▼
/spec-create adr <impact> <new-service> --new
    │
    ├── Создаёт /src/{service}/
    │   ├── README.md (по шаблону)
    │   ├── Makefile
    │   ├── dependencies.yaml
    │   └── .env.example
    │
    ├── Создаёт /tests/{service}/
    │
    └── Создаёт /specs/services/{service}/
        ├── README.md
        ├── architecture.md
        ├── adr/README.md
        ├── adr/001-initial.md
        └── plans/README.md
    │
    ▼
ADR 001-initial.md в статусе DRAFT
```

### После создания

1. **Заполнить ADR** — описать решение по архитектуре сервиса
2. **Обновить architecture.md** — если нужны детали
3. **Создать план** — декомпозиция на задачи (`/spec-create plan`)
4. **Начать реализацию** — после `APPROVED` статуса ADR

---

## Удаление/архивирование

### Когда удалять сервис

- Функциональность полностью перенесена в другой сервис
- Сервис больше не используется
- Слияние сервисов

### Workflow удаления

```
1. Убедиться, что сервис не используется
   - Проверить dependencies.yaml других сервисов
   - Проверить трафик (мониторинг)

2. Создать ADR о удалении
   /spec-create adr <service> deletion-{service}
   - Описать причину удаления
   - План миграции (если есть)

3. После APPROVED:
   - Удалить код (/src/{service}/)
   - Удалить тесты (/tests/{service}/)
   - Архивировать спецификации (пометить как DEPRECATED)
   - Обновить документацию
```

### Архивирование спецификаций

При удалении сервиса его спецификации **не удаляются**, а помечаются:

```yaml
# /specs/services/{service}/README.md
---
status: DEPRECATED
deprecated-at: 2024-01-15
reason: Merged into auth service
migration: See ADR auth/005-merge-users
---
```

---

## Примеры

### Пример 1: Создание сервиса notifications

```bash
# 1. Impact определил необходимость нового сервиса
# /specs/impact/003-notification-system.md

# 2. Создание сервиса
/spec-create adr 003-notification-system notifications --new

# Результат:
# ✅ /src/notifications/ создан (включая docs/)
# ✅ /tests/notifications/ создан
# ✅ /specs/services/notifications/ создан
# ✅ ADR 001-initial.md создан (DRAFT)
```

### Пример 2: Удаление сервиса users (слияние с auth)

```bash
# 1. Создать ADR о слиянии
/spec-create adr auth merge-users-service

# 2. После APPROVED — выполнить миграцию
# 3. Удалить /src/users/, /tests/users/
# 4. Пометить /specs/services/users/ как DEPRECATED
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/spec-create](/.claude/skills/spec-create/SKILL.md) | Создание сервиса через `--new` флаг |

> **TODO:** Создать скилл `/service-create` для прямого создания сервиса.

---

## Связанные инструкции

- [structure.md](./structure.md) — структура папок сервиса
- [dependencies.md](./dependencies.md) — зависимости между сервисами
- [specs/impact.md](../specs/impact.md) — Impact-анализ (определение необходимости сервиса)
- [docs/structure.md](../meta/docs/structure.md) — правила документации
