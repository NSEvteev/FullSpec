---
description: Мета-стандарт технологических стандартов — как создавать per-tech standard-{tech}.md и validation-{tech}.md, автозагрузка через rules, связь с Code Map.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/.instructions/technologies/README.md
---

# Стандарт технологий

Версия стандарта: 1.1

Как создавать per-tech стандарты кодирования (standard-{tech}.md + validation-{tech}.md), подключать их через rules и связывать с Code Map в architecture/services/. Стандарт создаётся полностью при Design → WAITING — это прескриптивный словарь правил, не зависящий от ADR.

**Полезные ссылки:**
- [Инструкции технологий](./README.md)
- [Технологический реестр](/specs/technologies/README.md)

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
- [4. Триггер создания](#4-триггер-создания)
- [5. Секции per-tech стандарта](#5-секции-per-tech-стандарта)
- [6. Автозагрузка через rules](#6-автозагрузка-через-rules)
- [7. Шаблоны](#7-шаблоны)
- [8. Чек-лист качества](#8-чек-лист-качества)
- [9. Примеры](#9-примеры)
- [10. Миграция при изменении standard-technology.md](#10-миграция-при-изменении-standard-technologymd)

---

## 1. Назначение

**Регулирует:**
- Формат и содержание per-tech стандартов кодирования (`standard-{tech}.md`)
- Формат per-tech валидаций (`validation-{tech}.md`)
- Автозагрузку стандартов через `.claude/rules/`
- Связь с технологическим реестром (`/specs/technologies/README.md`)

**НЕ регулирует:**
- Архитектуру сервисов — [standard-service.md](/specs/.instructions/living-docs/service/standard-service.md)
- SDD-документы (Discussion, Impact, Design, ADR) — [standard-specs.md](/specs/.instructions/standard-specs.md)
- Общие принципы программирования — [standard-principles.md](/.instructions/standard-principles.md)

**Пара standard + validation:**

Каждая технология описывается парой файлов:

| Файл | Назначение |
|------|------------|
| `standard-{tech}.md` | Правила, конвенции, паттерны использования |
| `validation-{tech}.md` | Коды ошибок, чек-лист проверки |

---

## 2. Расположение и именование

**Расположение per-tech стандартов:**
```
specs/technologies/standard-{tech}.md
specs/technologies/validation-{tech}.md
```

**Именование `{tech}`:**
- Kebab-case: `python`, `typescript`, `postgresql`, `tailwind-css`
- Имя технологии, не фреймворка, если технология = фреймворк: `fastapi`, `nextjs`
- Фреймворк выделяется в отдельный стандарт, когда его конвенции **конфликтуют** с базовой технологией (например, структура проекта, паттерны импорта). Если конвенции **дополняют** базовую технологию без конфликтов — использовать стандарт базовой технологии

---

## 3. Frontmatter

```yaml
---
description: Стандарт кодирования {Technology} — конвенции именования, структура, паттерны.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/technologies/README.md
technology: {tech}
---
```

| Поле | Обязательное | Описание |
|------|-------------|----------|
| `description` | Да | Краткое описание |
| `standard` | Да | Ссылка на стандарт инструкций |
| `standard-version` | Да | Версия стандарта |
| `index` | Да | README области |
| `technology` | Да | Kebab-case имя технологии |

---

## 4. Триггер создания

Per-tech стандарт создаётся **полностью** при Design → WAITING (все секции заполнены конвенциями). Технологический стандарт — прескриптивный словарь правил. Конвенции использования технологии известны с момента выбора и не зависят от ADR.

**Каскад Design → WAITING:**

```
Design выбирает технологию в Tech Stack
  → Проверить: существует standard-{tech}.md?
    → Нет (новая технология):
        1. Создать standard-{tech}.md (полный — § 7.1)
        2. Создать validation-{tech}.md (полный — § 7.2)
        3. Создать rule .claude/rules/{tech}.md (§ 7.3)
        4. Добавить строку в specs/technologies/README.md (реестр)
    → Да (существующая технология):
        → Обновить колонку "Сервисы" в реестре (добавить новый сервис)
```

> **Порядок строго последовательный:** standard → validation → rule. Параллельное создание запрещено — см. [standard-instruction.md](/.instructions/standard-instruction.md).

### 4.0.1. Откат

| Уровень | Действие |
|---------|----------|
| Design → ROLLING_BACK | Удалить `standard-{tech}.md`, `validation-{tech}.md`, rule, строку реестра (если технология введена этим Design) |

**Связь с Code Map:**

При наличии per-tech стандарта таблица Tech Stack в `architecture/services/{svc}.md` дополняется колонкой "Стандарт" — см. [standard-service.md § 5.4](/specs/.instructions/living-docs/service/standard-service.md#54-code-map):

| Технология | Версия | Назначение | Стандарт |
|-----------|--------|------------|---------|
| Python | 3.12 | Backend API | [standard-python.md](/specs/technologies/standard-python.md) |

**Реестр технологий:**

При создании стандарта добавить строку в `/specs/technologies/README.md`:

| Технология | Версия | Сервисы | Стандарт | Последний Design |
|-----------|--------|---------|---------|-----------------|
| Python | 3.12 | auth, billing | [standard-python.md](/specs/technologies/standard-python.md) | design-0001 |

### 4.1. Когда НЕ создавать per-tech стандарт

| Ситуация | Причина | Действие |
|----------|---------|----------|
| Технология только для tooling (webpack, prettier) | Не попадает в `src/`, не требует конвенций кодирования | Не создавать standard-{tech}.md |
| Обёртка над другой технологией (TypeORM → PostgreSQL) | Конвенции наследуются от базовой технологии | Ссылаться на standard базовой технологии в ADR |
| Технология deprecated/экспериментальная | Неоправданная поддержка | Дождаться стабилизации |
| Одноразовое использование (скрипт миграции) | Не требует долгосрочной поддержки | Использовать [standard-principles.md](/.instructions/standard-principles.md) |

---

## 5. Секции per-tech стандарта

Каждый `standard-{tech}.md` содержит следующие секции:

### 5.1. Версия и источники

Версия технологии, ссылки на официальную документацию.

### 5.2. Конвенции именования

Правила именования: файлы, модули, классы, функции, переменные, константы.

### 5.3. Структура кода

Организация модулей, импорты, порядок определений.

### 5.4. Паттерны использования

Рекомендуемые паттерны для данной технологии в контексте проекта.

### 5.5. Типичные ошибки

Антипаттерны и частые ошибки с примерами правильного кода.

### 5.6. Ссылки

Ссылки на официальную документацию и style guides.

### 5.7. Скрипт валидации кода (опционально)

Для технологий с автоматизируемыми правилами создаётся скрипт `specs/.instructions/.scripts/validate-{tech}-code.py`:

- Проверяет исходный код на соответствие standard-{tech}.md
- Коды ошибок — из validation-{tech}.md § 2
- Интегрируется в pre-commit через `.pre-commit-config.yaml`
- Не все правила автоматизируемы — семантические проверки остаются для ручного review / Claude
- Все проверки блокируют коммит (exit code 1)

### 5.8. Связь с принципами программирования

Все per-tech стандарты **ДОЛЖНЫ** соответствовать [standard-principles.md](/.instructions/standard-principles.md). При конфликте между per-tech стандартом и универсальными принципами — **приоритет у принципов**.

**Примеры:**
- standard-python.md **НЕ МОЖЕТ** разрешить голый `except:` (запрещено standard-principles.md)
- standard-typescript.md **НЕ МОЖЕТ** разрешить `any` без обоснования
- standard-{tech}.md **МОЖЕТ** дополнить принципы специфичными для технологии правилами (например, PEP 8 для Python)

**Проверка при создании:** При создании standard-{tech}.md проверить, что секция "Типичные ошибки" (§ 5.5) не противоречит standard-principles.md.

---

## 6. Автозагрузка через rules

Каждый per-tech стандарт подключается через rule в `.claude/rules/`. Rule автоматически **включается в контекст** при работе с файлами, соответствующими паттерну `globs`. Rule содержит ссылки на standard-{tech}.md и validation-{tech}.md — LLM **ДОЛЖЕН** прочитать эти файлы перед выполнением задачи.

**Расположение rule:**
```
.claude/rules/{tech}.md
```

**Паттерн paths:**

| Технология | Paths |
|-----------|-------|
| Python | `["src/**/*.py", "tests/**/*.py"]` |
| TypeScript | `["src/**/*.ts", "src/**/*.tsx"]` |
| PostgreSQL | `["src/**/database/**", "**/*.sql"]` |

**Содержимое rule:**

```markdown
При работе с {Technology}-файлами ОБЯЗАТЕЛЬНО следовать:
- [standard-{tech}.md](/specs/technologies/standard-{tech}.md)
- [validation-{tech}.md](/specs/technologies/validation-{tech}.md)
```

---

## 7. Шаблоны

### 7.1. Шаблон standard-{tech}.md

`````markdown
---
description: Стандарт кодирования {Technology} — конвенции именования, структура, паттерны.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/technologies/README.md
technology: {tech}
---

# Стандарт {Technology}

Версия стандарта: 1.0

Правила и конвенции кодирования на {Technology} в проекте.

**Полезные ссылки:**
- [Технологический реестр](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-{tech}.md](./validation-{tech}.md) |

## Оглавление

- [1. Версия и источники](#1-версия-и-источники)
- [2. Конвенции именования](#2-конвенции-именования)
- [3. Структура кода](#3-структура-кода)
- [4. Паттерны использования](#4-паттерны-использования)
- [5. Типичные ошибки](#5-типичные-ошибки)
- [6. Ссылки](#6-ссылки)

---

## 1. Версия и источники

| Параметр | Значение |
|----------|----------|
| Версия | {version} |
| Документация | {url} |
| Style guide | {url} |

---

## 2. Конвенции именования

| Элемент | Правило | Пример |
|---------|---------|--------|
| {элемент} | {правило} | `{пример}` |

---

## 3. Структура кода

{Правила организации кода}

---

## 4. Паттерны использования

{Рекомендуемые паттерны}

---

## 5. Типичные ошибки

{Антипаттерны с примерами}

---

## 6. Ссылки

- [{Technology} Documentation]({url})
- [{Style Guide}]({url})
`````

### 7.2. Шаблон validation-{tech}.md

`````markdown
---
description: Валидация кода на {Technology} — коды ошибок, чек-лист проверки.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/technologies/README.md
technology: {tech}
---

# Валидация {Technology}

Рабочая версия стандарта: 1.0

Проверка соответствия кода стандарту [standard-{tech}.md](./standard-{tech}.md).

**Полезные ссылки:**
- [Технологический реестр](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-{tech}.md](./standard-{tech}.md) |
| Валидация | Этот документ |

## Оглавление

- [1. Когда валидировать](#1-когда-валидировать)
- [2. Коды ошибок](#2-коды-ошибок)
- [3. Чек-лист](#3-чек-лист)

---

## 1. Когда валидировать

- После написания нового кода на {Technology}
- При code review
- Перед коммитом (автоматически через rule)

---

## 2. Коды ошибок

| Код | Описание | Severity |
|-----|----------|----------|
| {TECH}001 | {описание} | error |

---

## 3. Чек-лист

- [ ] Именование соответствует конвенциям
- [ ] Структура кода соответствует стандарту
- [ ] Нет типичных ошибок из антипаттернов
`````

### 7.3. Шаблон rule для автозагрузки

`````markdown
---
description: Автозагрузка стандарта {Technology} при работе с файлами.
globs:
  - {паттерн файлов}
---

При работе с {Technology}-файлами ОБЯЗАТЕЛЬНО следовать:
- [standard-{tech}.md](/specs/technologies/standard-{tech}.md)
- [validation-{tech}.md](/specs/technologies/validation-{tech}.md)
`````

### 7.4. Шаблон validate-{tech}-code.py (опционально)

Каркас скрипта валидации кода (§ 5.7):

```python
#!/usr/bin/env python3
"""
validate-{tech}-code.py — Валидация кода на соответствие standard-{tech}.md.

Использование:
    python validate-{tech}-code.py <файл или папка>
    python validate-{tech}-code.py <файл или папка> --verbose

Проверяет автоматизируемые правила из validation-{tech}.md:
    - {TECH}NNN: {описание}

SSOT:
    - specs/technologies/standard-{tech}.md
    - specs/technologies/validation-{tech}.md

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
"""

import argparse
import re
import sys
from pathlib import Path

ERROR_CODES = {
    "{TECH}001": "{описание}",
}

# ... проверки ...

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация кода на соответствие standard-{tech}.md"
    )
    parser.add_argument("path", nargs="*", help="Файлы или папки")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    # ... валидация ...

if __name__ == "__main__":
    main()
```

*Не все технологии требуют скрипт — шаг опционален (§ 5.7).*

---

## 8. Чек-лист качества

### При создании (Design → WAITING)

- [ ] Design выбрал технологию в Tech Stack
- [ ] `standard-{tech}.md` создан по шаблону (§ 7.1), все 6 секций заполнены конвенциями
- [ ] `validation-{tech}.md` создан по шаблону (§ 7.2), секции заполнены (коды ошибок, чек-лист)
- [ ] Примеры кода — конкретные, не абстрактные
- [ ] Не противоречит [standard-principles.md](/.instructions/standard-principles.md) (§ 5.7)
- [ ] Rule в `.claude/rules/` создан с правильными globs (§ 7.3)
- [ ] `validate-{tech}-code.py` создан (если есть автоматизируемые правила, § 7.4)
- [ ] Pre-commit хук добавлен (если создан скрипт)
- [ ] Строка добавлена в `/specs/technologies/README.md` (реестр)
- [ ] README области (`specs/.instructions/technologies/README.md`) обновлён

---

## 9. Примеры

### Пример: создание стандарта Python

**1. Design design-0001 выбирает Python 3.12 для auth-сервиса → Design переходит в WAITING.**

**2. Создать стандарт (technology-agent):**
```
specs/technologies/standard-python.md  — полный (§ 7.1), все секции заполнены
specs/technologies/validation-python.md — полный (§ 7.2), коды ошибок и чек-лист
```

**3. Создать rule:**
```
.claude/rules/python.md
```

С содержимым:
```markdown
---
description: Автозагрузка стандарта Python при работе с .py файлами.
globs:
  - "src/**/*.py"
  - "tests/**/*.py"
---

При работе с Python-файлами ОБЯЗАТЕЛЬНО следовать:
- [standard-python.md](/specs/technologies/standard-python.md)
- [validation-python.md](/specs/technologies/validation-python.md)
```

**4. Обновить реестр** (`/specs/technologies/README.md`):

| Технология | Версия | Сервисы | Стандарт | Последний Design |
|-----------|--------|---------|---------|-----------------|
| Python | 3.12 | auth | [standard-python.md](/specs/technologies/standard-python.md) | design-0001 |

---

## 10. Миграция при изменении standard-technology.md

**Триггер:** Обновление standard-technology.md с изменением структуры секций (§ 5) или формата (§ 3).

**SSOT миграции:** [standard-migration.md](/.instructions/migration/standard-migration.md)

**Шаги:**
1. Создать миграцию: `/migration-create specs/.instructions/technologies/standard-technology.md`
2. План миграции включает обновление всех существующих `standard-{tech}.md` и `validation-{tech}.md`
3. Выполнить миграцию согласно плану
4. Валидировать обновлённые стандарты
