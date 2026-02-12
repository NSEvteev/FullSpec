---
description: Валидация фиксированных файлов архитектуры — существование, frontmatter, обязательные секции, согласованность services/.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/.instructions/living-docs/architecture/README.md
---

# Валидация фиксированных файлов архитектуры

Версия стандарта: 1.0

Проверка существования, структуры и согласованности фиксированных файлов `specs/architecture/`.

**Полезные ссылки:**
- [Стандарт фиксированных файлов](./standard-architecture.md)
- [Инструкции living-docs](../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-architecture.md](./standard-architecture.md) |
| Валидация | Этот документ |

## Оглавление

- [1. Когда валидировать](#1-когда-валидировать)
- [2. Автоматическая валидация](#2-автоматическая-валидация)
- [3. Коды ошибок](#3-коды-ошибок)
- [4. Чек-лист](#4-чек-лист)
- [5. Скрипты](#5-скрипты)

---

## 1. Когда валидировать

| Момент | Как |
|--------|-----|
| После создания/обновления файлов architecture/ | `python specs/.instructions/.scripts/validate-architecture.py --verbose` |
| При code review | Проверить чек-лист (§ 4) |
| Перед коммитом (автоматически) | Pre-commit хук `architecture-validate` |

---

## 2. Автоматическая валидация

### Pre-commit хук

Хук `architecture-validate` в `.pre-commit-config.yaml` запускается при изменении файлов в `specs/architecture/` или `specs/services/`:

```yaml
- id: architecture-validate
  name: Validate architecture fixed files
  entry: python specs/.instructions/.scripts/validate-architecture.py --check-services
  language: system
  files: ^specs/(architecture/|services/)
  pass_filenames: false
  stages: [pre-commit]
```

### Ручной запуск

```bash
# Структурная валидация (существование, frontmatter, секции)
python specs/.instructions/.scripts/validate-architecture.py --verbose

# С проверкой согласованности services/
python specs/.instructions/.scripts/validate-architecture.py --check-services --verbose
```

---

## 3. Коды ошибок

| Код | Проверка | Severity |
|-----|----------|----------|
| `[AC001]` | Фиксированный файл отсутствует | ERROR |
| `[AC002]` | Отсутствует frontmatter | ERROR |
| `[AC003]` | Отсутствует `description` в frontmatter | ERROR |
| `[AC004]` | Отсутствует обязательная секция | ERROR |
| `[AC005]` | Нет секции "Planned Changes" | ERROR |
| `[AC006]` | Новая папка `specs/services/` без изменений в `architecture/` | ERROR |

### AC001 — Фиксированный файл отсутствует

Один из 4 файлов не найден: `system/overview.md`, `system/data-flows.md`, `system/infrastructure.md`, `domains/context-map.md`.

**Исправление:** Создать файл по шаблону из [standard-architecture.md § 5](./standard-architecture.md#5-шаблоны).

### AC002 — Отсутствует frontmatter

Файл не содержит YAML frontmatter (блок `---`).

**Исправление:** Добавить frontmatter с полем `description`.

### AC003 — Отсутствует description в frontmatter

Frontmatter существует, но поле `description` отсутствует или пустое.

**Исправление:** Добавить `description` с кратким описанием файла.

### AC004 — Отсутствует обязательная секция

Файл не содержит одну из обязательных секций (заголовок `##`).

**Исправление:** Добавить секцию. Список обязательных секций — в [standard-architecture.md § 4](./standard-architecture.md#4-обязательные-секции).

### AC005 — Нет секции "Planned Changes"

Файл не содержит секцию `## Planned Changes`. Обязательна во всех 4 файлах.

**Исправление:** Добавить `## Planned Changes` с текстом `*Нет запланированных изменений.*`.

### AC006 — Новая папка specs/services/ без изменений в architecture/

В staged файлах есть **новые** файлы под `specs/services/{svc}/` (не `.gitkeep`), но ни один файл из `specs/architecture/` не staged. При добавлении нового сервиса необходимо обновить architecture/ файлы.

**Исправление:** Обновить файлы в `specs/architecture/` (overview.md, data-flows.md, context-map.md) и добавить их в коммит.

---

## 4. Чек-лист

- [ ] 4 фиксированных файла существуют (AC001)
- [ ] Каждый файл содержит frontmatter (AC002)
- [ ] Каждый frontmatter содержит `description` (AC003)
- [ ] Обязательные секции присутствуют (AC004)
- [ ] Секция "Planned Changes" в каждом файле (AC005)
- [ ] Новые сервисы сопровождаются обновлением architecture/ (AC006)

---

## 5. Скрипты

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `validate-architecture.py` | Валидация фиксированных файлов + согласованность services/ | [specs/.instructions/.scripts/validate-architecture.py](../../.scripts/validate-architecture.py) |

```bash
# Структурная валидация
python specs/.instructions/.scripts/validate-architecture.py

# С проверкой согласованности services/
python specs/.instructions/.scripts/validate-architecture.py --check-services

# Подробный вывод
python specs/.instructions/.scripts/validate-architecture.py --verbose
```
