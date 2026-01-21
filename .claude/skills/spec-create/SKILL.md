---
name: spec-create
description: Создание документов /specs/ (Discussion, Impact, ADR, Plan)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
category: specs
triggers:
  commands:
    - /spec-create
  phrases:
    ru:
      - создай спецификацию
      - новая дискуссия
      - создай adr
      - создай план
      - создай импакт
    en:
      - create spec
      - new discussion
      - create adr
      - create plan
      - create impact
---

# Создание документов /specs/

Создание документов спецификаций: Discussion, Impact, ADR, Plan. Тип документа определяется автоматически по первому аргументу.

**Связанные скиллы:**
- [spec-status](/.claude/skills/spec-status/SKILL.md) — изменение статуса документа
- [spec-update](/.claude/skills/spec-update/SKILL.md) — работа с документом
- [specs-health](/.claude/skills/specs-health/SKILL.md) — проверка целостности /specs/
- [specs-index](/.claude/skills/specs-index/SKILL.md) — обновление индексов

**Связанные инструкции:**
- [specs/README.md](/.claude/instructions/specs/README.md) — индекс инструкций /specs/
- [specs/statuses.md](/.claude/instructions/specs/statuses.md) — система статусов
- [specs/workflow.md](/.claude/instructions/specs/workflow.md) — полный workflow
- [specs/discussions.md](/.claude/instructions/specs/discussions.md) — формат дискуссий
- [specs/impact.md](/.claude/instructions/specs/impact.md) — формат импакт-анализа
- [specs/adr.md](/.claude/instructions/specs/adr.md) — формат ADR
- [specs/plans.md](/.claude/instructions/specs/plans.md) — формат планов
- [specs/rules.md](/.claude/instructions/specs/rules.md) — правила и запреты

**Шаблоны:**
- [discussion.md](/.claude/templates/specs/discussion.md) — шаблон дискуссии
- [impact.md](/.claude/templates/specs/impact.md) — шаблон импакт-анализа
- [adr.md](/.claude/templates/specs/adr.md) — шаблон ADR
- [plan.md](/.claude/templates/specs/plan.md) — шаблон плана
- [architecture.md](/.claude/templates/specs/architecture.md) — шаблон архитектуры

**Utility-скиллы:**
- [input-validate](/.claude/skills/input-validate/SKILL.md) — валидация входных данных
- [environment-check](/.claude/skills/environment-check/SKILL.md) — проверка git

## Оглавление

- [Формат вызова](#формат-вызова)
- [Типы документов](#типы-документов)
- [Воркфлоу](#воркфлоу)
- [Создание нового сервиса](#создание-нового-сервиса)
- [Обработка ошибок](#обработка-ошибок)
- [Чек-лист](#чек-лист)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/spec-create <type> [parent] [service] [--dry-run] [--new]
```

| Параметр | Описание | Обязательный |
|----------|----------|:------------:|
| `type` | Тип документа: `discussion`, `impact`, `adr`, `plan` | Да |
| `parent` | ID или тема родительского документа | Для impact/adr/plan |
| `service` | Название сервиса (для adr) | Для adr |
| `--dry-run` | Показать план без создания | Нет |
| `--new` | Создать структуру нового сервиса | Нет |

---

## Типы документов

| Тип | Parent | Результат |
|-----|--------|-----------|
| `discussion` | — | `/specs/discussions/NNN-{topic}.md` |
| `impact` | discussion ID | `/specs/impact/NNN-{topic}.md` |
| `adr` | impact ID + service | `/specs/services/{service}/adr/NNN-{topic}.md` |
| `plan` | adr path | `/specs/services/{service}/plans/{topic}-plan.md` |

**Нумерация:**
- Автоинкремент: следующий номер после последнего в папке
- Формат: `001`, `002`, `003`...

---

## Воркфлоу

### Шаг 1: Определить тип документа

Из первого аргумента: `discussion`, `impact`, `adr`, `plan`.

Если не указан — спросить:
```
Какой тип документа создать?
1. Discussion — исследование идеи
2. Impact — анализ влияния на сервисы
3. ADR — архитектурное решение для сервиса
4. Plan — план реализации ADR
```

### Шаг 2: Получить родительский документ

| Тип | Родитель | Как получить |
|-----|----------|--------------|
| `discussion` | — | Не требуется |
| `impact` | Discussion | `parent` аргумент или спросить ID |
| `adr` | Impact | `parent` аргумент или спросить ID |
| `plan` | ADR | `parent` аргумент или спросить путь |

**Валидация родителя:**
- Родительский документ существует
- Статус родителя позволяет создание дочернего (см. [workflow.md](/.claude/instructions/specs/workflow.md))

### Шаг 3: Получить тему/название

Из аргумента или спросить:
```
Введите тему документа (краткое название, латиница с дефисами):
> auth-strategy
```

**Валидация:**
- Только латиница, цифры, дефис
- Нет пробелов
- Не пустая строка

### Шаг 4: Определить номер

```bash
# Найти последний номер в папке
ls /specs/{type}/ | grep -E "^[0-9]{3}-" | sort | tail -1
```

Если папка пуста — начать с `001`.

### Шаг 5: Для ADR — определить сервис

Из аргумента `service` или спросить:
```
Для какого сервиса создаётся ADR?
Существующие сервисы: auth, gateway, users
Или введите имя нового сервиса:
```

Если сервис новый и указан `--new`:
- Создать структуру сервиса (см. [Создание нового сервиса](#создание-нового-сервиса))

### Шаг 6: Прочитать шаблон

| Тип | Шаблон |
|-----|--------|
| `discussion` | [/.claude/templates/specs/discussion.md](/.claude/templates/specs/discussion.md) |
| `impact` | [/.claude/templates/specs/impact.md](/.claude/templates/specs/impact.md) |
| `adr` | [/.claude/templates/specs/adr.md](/.claude/templates/specs/adr.md) |
| `plan` | [/.claude/templates/specs/plan.md](/.claude/templates/specs/plan.md) |

### Шаг 7: Создать документ

1. Подставить в шаблон:
   - Номер и тему
   - Ссылку на родительский документ
   - Дату создания
   - Начальный статус: `DRAFT`

2. Создать файл:
   ```bash
   write /specs/{path}/{NNN}-{topic}.md
   ```

### Шаг 8: Обновить индекс README.md

Добавить строку в таблицу соответствующего README.md:

| Тип | README |
|-----|--------|
| `discussion` | `/specs/discussions/README.md` |
| `impact` | `/specs/impact/README.md` |
| `adr` | `/specs/services/{service}/adr/README.md` |
| `plan` | `/specs/services/{service}/plans/README.md` |

**Формат строки:**
```markdown
| [NNN](NNN-{topic}.md) | {Тема} | DRAFT | {дата} |
```

### Шаг 9: Добавить backlink в родительский документ

Обновить родительский документ, добавив ссылку на созданный дочерний:

| Создан | Обновить родителя |
|--------|-------------------|
| Impact | Discussion — секция "Связанные документы" |
| ADR | Impact — таблица "Затронутые сервисы" |
| Plan | ADR — секция "План реализации" |

### Шаг 10: Результат

```
✅ Документ создан

Файл: /specs/{path}/{NNN}-{topic}.md
Тип: {type}
Статус: DRAFT
Родитель: {parent path}

Индекс обновлён: /specs/{path}/README.md
Backlink добавлен: {parent path}

Следующий шаг:
- Заполнить документ
- Перевести в REVIEW: /spec-status {path} review
```

---

## Создание нового сервиса

При создании ADR для несуществующего сервиса с флагом `--new`:

### Структура создаваемых папок

```
/src/{service}/                    # Код сервиса
/tests/{service}/                  # Тесты
/specs/services/{service}/         # Спецификации
  ├── README.md                    # Описание сервиса
  ├── architecture.md              # Архитектура (из шаблона)
  ├── adr/
  │   └── README.md                # Индекс ADR
  └── plans/
      └── README.md                # Индекс планов
/doc/src/{service}/
  └── README.md                    # Документация
```

### Workflow создания

```
/spec-create adr 001-auth-strategy payments --new

⚠️ Сервис "payments" не существует.

Создать структуру нового сервиса?
- /src/payments/
- /tests/payments/
- /specs/services/payments/
- /doc/src/payments/

[Y/n]
```

После подтверждения:
1. Создать все папки
2. Создать README.md файлы по шаблонам
3. Создать начальный architecture.md
4. Создать запрошенный ADR

---

## Обработка ошибок

| Ошибка | Действие |
|--------|----------|
| Неверный тип документа | Показать список допустимых типов |
| Родитель не найден | Показать существующие документы для выбора |
| Родитель в неправильном статусе | Показать текущий статус и требуемый |
| Сервис не существует | Предложить `--new` для создания |
| Документ с таким номером существует | Пересчитать номер |

**Откат при ошибке:**

```bash
# Удалить созданный файл
rm /specs/{path}/{file}.md

# Откатить изменения в README.md
git checkout -- /specs/{path}/README.md

# Откатить изменения в родителе
git checkout -- {parent-path}
```

---

## Чек-лист

- [ ] Определён тип документа
- [ ] Получен родительский документ (если нужен)
- [ ] Валидирован статус родителя
- [ ] Получена тема документа
- [ ] Определён номер (автоинкремент)
- [ ] Для ADR: определён сервис
- [ ] Для нового сервиса: создана структура (если `--new`)
- [ ] Прочитан шаблон
- [ ] Создан файл документа
- [ ] Обновлён индекс README.md
- [ ] Добавлен backlink в родительский документ
- [ ] Выведен результат

---

## Примеры использования

### Пример 1: Создание Discussion

**Команда:**
```
/spec-create discussion "Auth Strategy"
```

**Результат:**
```
✅ Discussion создана

Файл: /specs/discussions/001-auth-strategy.md
Статус: DRAFT

Индекс обновлён: /specs/discussions/README.md

Следующий шаг:
- Заполнить секции документа
- Перевести в REVIEW: /spec-status discussions/001 review
```

### Пример 2: Создание ADR для существующего сервиса

**Команда:**
```
/spec-create adr 001-auth-strategy auth
```

**Результат:**
```
✅ ADR создан

Файл: /specs/services/auth/adr/001-jwt-tokens.md
Тип: ADR
Статус: DRAFT
Родитель: /specs/impact/001-auth-strategy.md

Индекс обновлён: /specs/services/auth/adr/README.md
Backlink добавлен: /specs/impact/001-auth-strategy.md

Следующий шаг:
- Заполнить ADR
- Перевести в REVIEW: /spec-status auth/adr/001 review
```

### Пример 3: Создание ADR с новым сервисом

**Команда:**
```
/spec-create adr 001-auth-strategy payments --new
```

**Диалог:**
```
⚠️ Сервис "payments" не существует.

Создать структуру нового сервиса?
- /src/payments/
- /tests/payments/
- /specs/services/payments/
- /doc/src/payments/

[Y/n] Y

✅ Структура сервиса "payments" создана

✅ ADR создан

Файл: /specs/services/payments/adr/001-payment-processing.md
...
```

### Пример 4: Dry-run режим

**Команда:**
```
/spec-create impact 001-auth-strategy --dry-run
```

**Результат:**
```
📋 Предварительный просмотр (--dry-run)

Будет создано:
- /specs/impact/001-auth-strategy.md

Будет обновлено:
- /specs/impact/README.md (добавлена строка)
- /specs/discussions/001-auth-strategy.md (backlink)

ℹ️ Изменения НЕ применены (--dry-run)
```
