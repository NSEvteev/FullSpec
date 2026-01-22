# Инструкции /services/

Индекс инструкций для управления сервисами проекта.

**Содержание:** создание сервисов, структура `/src/{service}/`, lifecycle, зависимости.

> **Область ответственности:** Управление сервисами как сущностями — создание, структура, зависимости.
> Спецификации сервиса (ADR, Plans, Architecture) — в [specs/README.md](../specs/README.md).
> Документация кода сервиса — в [docs/README.md](../docs/README.md).

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Создание](#1-создание) | [lifecycle.md](./lifecycle.md) | Создание, обновление, удаление сервиса |
| [2. Структура](#2-структура) | [structure.md](./structure.md) | Структура папок /src/{service}/ |
| [3. Зависимости](#3-зависимости) | [dependencies.md](./dependencies.md) | dependencies.yaml, межсервисные связи |
| [4. Шаблоны](#4-шаблоны) | — | Шаблоны для сервисов |
| [5. Скиллы](#5-скиллы) | — | Скиллы для работы с сервисами |

```
/.claude/instructions/services/
├── README.md           # Этот файл (индекс)
├── lifecycle.md        # Создание, обновление, удаление сервиса
├── structure.md        # Структура папок /src/{service}/
└── dependencies.md     # Зависимости между сервисами
```

---

# 1. Создание

Lifecycle сервиса: создание, обновление, удаление/архивирование.

**Оглавление:**
- [Когда создавать сервис](./lifecycle.md#когда-создавать-сервис)
- [Что создаётся](./lifecycle.md#что-создаётся)
- [Workflow создания](./lifecycle.md#workflow-создания)
- [Удаление/архивирование](./lifecycle.md#удалениеархивирование)

**Инструкция:** [lifecycle.md](./lifecycle.md)

---

# 2. Структура

Стандартная структура папок сервиса в `/src/{service}/`.

**Оглавление:**
- [Дерево файлов](./structure.md#дерево-файлов)
- [Обязательные файлы](./structure.md#обязательные-файлы)
- [README.md сервиса](./structure.md#readmemd-сервиса)
- [Примеры](./structure.md#примеры)

**Инструкция:** [structure.md](./structure.md)

---

# 3. Зависимости

Управление зависимостями между сервисами через `dependencies.yaml`.

**Оглавление:**
- [Формат dependencies.yaml](./dependencies.md#формат-dependenciesyaml)
- [Типы зависимостей](./dependencies.md#типы-зависимостей)
- [Визуализация графа](./dependencies.md#визуализация-графа)

**Инструкция:** [dependencies.md](./dependencies.md)

---

# 4. Шаблоны

Шаблоны для создания сервисов.

| Шаблон | Назначение |
|--------|------------|
| [service-readme.md](/.claude/templates/services/service-readme.md) | README.md сервиса |
| [dependencies.yaml](/.claude/templates/services/dependencies.yaml) | Шаблон зависимостей |

---

# 5. Скиллы

**Скиллы для этой области пока отсутствуют.**

> **TODO:** Создать скилл `/service-create` для автоматизации создания сервиса.

---

## Связанные инструкции

- [specs/README.md](../specs/README.md) — спецификации сервиса (ADR, Plans)
- [docs/README.md](../docs/README.md) — документация кода сервиса
- [specs/impact.md](../specs/impact.md) — определение необходимости нового сервиса
- [shared/contracts.md](../shared/contracts.md) — контракты между сервисами
