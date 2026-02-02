---
description: Стандарт формата скриптов автоматизации
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: .instructions/README.md
---

# Стандарт скриптов

Формат и структура скриптов автоматизации в папках `.scripts/`.

**Полезные ссылки:**
- [Инструкции](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-script.md](./validation-script.md) |
| Создание | [create-script.md](./create-script.md) |
| Модификация | [modify-script.md](./modify-script.md) |

## Оглавление

- [1. Назначение](#1-назначение)
  - [Автоматизация шагов инструкций](#автоматизация-шагов-инструкций)
  - [Когда создавать скрипт](#когда-создавать-скрипт)
- [2. Принципы программирования](#2-принципы-программирования)
- [3. Расположение](#3-расположение)
  - [Правила именования](#правила-именования)
  - [Связь с инструкциями](#связь-с-инструкциями)
- [4. Формат файла](#4-формат-файла)
  - [Shebang](#shebang)
  - [UTF-8 для Windows](#utf-8-для-windows)
  - [Exit codes](#exit-codes)
- [5. Docstring](#5-docstring)
  - [Обязательная структура](#обязательная-структура)
  - [Обязательные секции docstring](#обязательные-секции-docstring)
  - [Опциональные секции docstring](#опциональные-секции-docstring)
- [6. Структура кода](#6-структура-кода)
  - [Порядок секций](#порядок-секций)
  - [Разделители секций](#разделители-секций)
  - [Общие функции](#общие-функции)
  - [Argparse шаблон](#argparse-шаблон)
  - [ERROR_CODES для валидаторов](#error_codes-для-валидаторов)
- [7. Отображение в инструкциях](#7-отображение-в-инструкциях)
- [8. Примеры](#8-примеры)
- [9. Правила для create/modify скриптов](#9-правила-для-createmodify-скриптов)
  - [Проверка существующих скриптов](#проверка-существующих-скриптов)
  - [Циклы подтверждения](#циклы-подтверждения)
  - [Отчёт о проделанной работе](#отчёт-о-проделанной-работе)
  - [Связь со скиллом](#связь-со-скиллом)

---

> **Шаблоны — из примеров SSOT.** При создании файлов использовать шаблоны из секции "Примеры". Запрещено придумывать свой формат.

---

## 1. Назначение

Скрипты — исполняемый код для автоматизации рутинных операций в инструкциях.

### Автоматизация шагов инструкций

> **Скрипты автоматизируют шаги в инструкциях.** Если шаг инструкции требует поиска, фильтрации или трансформации данных — он должен быть реализован скриптом.

**Примеры шагов, требующих скрипта:**

| Шаг в инструкции | Скрипт |
|------------------|--------|
| "Найти все файлы с `standard: X`" | `find-by-frontmatter.py` |
| "Проверить все ссылки в документе" | `validate-links.py` |
| "Сгенерировать README по шаблону" | `generate-readme.py` |
| "Обновить SSOT при переименовании" | `ssot.py rename` |

**Почему:**
- LLM использует скрипты вместо ручного поиска
- Результаты детерминированы и воспроизводимы
- Снижается вероятность ошибки

### Когда создавать скрипт

**Создавать скрипт когда:**
- Шаг инструкции требует поиска/фильтрации/трансформации
- Операция повторяется более 2 раз
- Операция содержит более 3 шагов
- Требуется валидация данных

**НЕ создавать скрипт когда:**
- Разовая операция
- Простое действие (1-2 команды)
- Логика уже есть в существующем скрипте

---

## 2. Принципы программирования

**SSOT:** [standard-principles.md](./standard-principles.md)

Все скрипты должны соблюдать принципы программирования:

| Принцип | Описание |
|---------|----------|
| **KISS** | Максимально простой код |
| **DRY** | Не дублировать код |
| **YAGNI** | Не добавлять функционал "на будущее" |
| **Наименьшее удивление** | Код делает то, что ожидает пользователь |
| **SOLID** | Один скрипт = одна задача |
| **Читаемость** | Docstring, типизация, понятные имена |
| **Обработка ошибок** | Явная, не голый `except:` |
| **Минимум зависимостей** | Только stdlib + PyYAML |

**Валидация:** [validation-principles.md](./validation-principles.md)

---

## 3. Расположение

```
{папка}/.instructions/.scripts/{script-name}.py
```

### Правила именования

| Паттерн | Назначение | Пример |
|---------|------------|--------|
| `validate-{object}.py` | Валидация объекта | `validate-instruction.py` |
| `{action}-{object}.py` | Действие над объектом | `generate-readme.py` |
| `{object}.py` | Управление объектом (CRUD) | `ssot.py` |
| `parse-{object}.py` | Парсинг/анализ объекта | `parse-docstrings.py` |
| `find-{criteria}.py` | Поиск по критерию | `find-by-frontmatter.py` |

### Связь с инструкциями

Скрипты создаются **только** для инструкций типов create, modify и validation.

| Тип инструкции | Типичный скрипт |
|----------------|-----------------|
| `validation-{object}.md` | `validate-{object}.py` |
| `create-{object}.md` | `create-{object}.py`, `generate-{object}.py` |
| `modify-{object}.md` | вспомогательные скрипты |

---

## 4. Формат файла

### Shebang

```python
#!/usr/bin/env python3
```

**Обязательно** для всех Python скриптов.

### UTF-8 для Windows

```python
# UTF-8 для Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
```

**Обязательно** в начале `main()`.

### Exit codes

| Код | Значение |
|-----|----------|
| `0` | Успех |
| `1` | Ошибка валидации / выполнения |
| `2` | Ошибка аргументов (argparse default) |

---

## 5. Docstring

Docstring — **единственное место** для документации скрипта (замена frontmatter).

### Обязательная структура

```python
"""
{script-name}.py — {Краткое описание}.

Использование:
    python {script-name}.py <обязательный> [--опция <значение>]

Примеры:
    python {script-name}.py input.txt
    python {script-name}.py --repo /path/to/repo

Возвращает:
    0 — успех
    1 — ошибка
"""
```

### Обязательные секции docstring

| Секция | Описание |
|--------|----------|
| **Первая строка** | `{name}.py — {описание}.` |
| **Использование** | Синтаксис вызова |
| **Примеры** | 2-3 примера вызова |
| **Возвращает** | Exit codes |

### Опциональные секции docstring

| Секция | Когда добавлять |
|--------|-----------------|
| **Подкоманды** | Скрипт с субкомандами (add, delete) |
| **Проверки** | Скрипт валидации |
| **Запускает** | Скрипт-обёртка |
| **Вывод** | Особый формат вывода |

---

## 6. Структура кода

### Порядок секций

```python
#!/usr/bin/env python3
"""Docstring."""

import ...                    # 1. Импорты (stdlib → third-party → local)

# =============================================================================
# Константы
# =============================================================================

CONSTANT = "value"            # 2. Константы

# =============================================================================
# Общие функции
# =============================================================================

def find_repo_root(): ...     # 3. Общие/утилитные функции

# =============================================================================
# Основные функции
# =============================================================================

def do_something(): ...       # 4. Основная логика

# =============================================================================
# Main
# =============================================================================

def main(): ...               # 5. Точка входа

if __name__ == "__main__":
    main()
```

### Разделители секций

```python
# =============================================================================
# Название секции
# =============================================================================
```

**Когда использовать:** файл > 100 строк или > 3 логических блоков.

### Общие функции

```python
def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()
```

### Argparse шаблон

```python
def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Описание скрипта"
    )
    parser.add_argument("positional", help="Описание")
    parser.add_argument("--option", "-o", default=".", help="Описание")
    parser.add_argument("--flag", action="store_true", help="Описание")

    args = parser.parse_args()

    # Логика...

    sys.exit(0 if success else 1)
```

### ERROR_CODES для валидаторов

> **Только для скриптов валидации** (`validate-*.py`). Остальные скрипты НЕ используют `ERROR_CODES`.

Скрипты валидации **обязаны** иметь константу `ERROR_CODES` — словарь с кодами и описаниями ошибок.

**Формат:**

```python
ERROR_CODES = {
    "X001": "Описание ошибки",
    "X002": "Описание другой ошибки",
    # ...
}
```

**Префиксы кодов:**

| Префикс | Область | Пример |
|---------|---------|--------|
| `S0xx` | Структура скриптов | `S001: Отсутствует shebang` |
| `P0xx` | Принципы программирования | `P001: Переусложнённый код` |
| `I0xx` | Инструкции | `I001: Неверный frontmatter` |
| `K0xx` | Скиллы | `K001: Отсутствует SSOT-ссылка` |
| `E0xx` | Ссылки (ошибки) | `E001: Файл не существует` |
| `W0xx` | Ссылки (предупреждения) | `W001: Абсолютный путь` |
| `T0xx` | Структура проекта | `T001: SSOT файл не найден` |

**Использование в коде:**

```python
# Вариант 1: прямое добавление
result["errors"].append(f"X001: {ERROR_CODES['X001']}: {detail}")

# Вариант 2: helper-функции (рекомендуется для DRY)
def add_error(result: dict, code: str, detail: str = "") -> None:
    """Добавить ошибку с кодом из ERROR_CODES."""
    message = ERROR_CODES.get(code, code)
    if detail:
        message = f"{message}: {detail}"
    result["errors"].append({"code": code, "message": message})
```

**Почему только валидаторы:**

| Тип скрипта | ERROR_CODES | Причина |
|-------------|:-----------:|---------|
| `validate-*.py` | ✅ | Выдают структурированные ошибки с кодами |
| `create-*.py` | ❌ | Создают объекты, не валидируют |
| `find-*.py` | ❌ | Ищут данные, не проверяют |
| `parse-*.py` | ❌ | Парсят данные, не валидируют |
| `*.py` (остальные) | ❌ | Выполняют действия, не валидируют |

---

## 7. Отображение в инструкциях

Каждая инструкция типа create, modify или validation содержит секцию "Скрипты" с таблицей:

```markdown
## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [{script}.py](./.scripts/{script}.py) | {описание} | {ссылка на инструкцию} |
```

**Формат строки:**
- **Скрипт** — ссылка на файл: `[name.py](./.scripts/name.py)`
- **Назначение** — краткое описание (из первой строки docstring)
- **Инструкция** — ссылка на инструкцию, использующую скрипт

Если скриптов нет — `*Нет скриптов.*`

**Скиллы для работы с инструкциями:**
- [/instruction-create](/.claude/skills/instruction-create/SKILL.md) — создание инструкции
- [/instruction-modify](/.claude/skills/instruction-modify/SKILL.md) — обновление инструкции
- [/instruction-validate](/.claude/skills/instruction-validate/SKILL.md) — валидация инструкции

---

## 8. Примеры

### Минимальный скрипт

```python
#!/usr/bin/env python3
"""
example.py — Пример минимального скрипта.

Использование:
    python example.py <input>

Примеры:
    python example.py file.txt

Возвращает:
    0 — успех
    1 — ошибка
"""

import sys
from pathlib import Path


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print("Использование: python example.py <input>", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    print(f"✅ Обработан: {input_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

### Скрипт поиска по frontmatter

```python
#!/usr/bin/env python3
"""
find-by-frontmatter.py — Поиск файлов по полю frontmatter.

Использование:
    python find-by-frontmatter.py <field> <value> [--path <папка>]

Примеры:
    python find-by-frontmatter.py standard instruction-standard.md
    python find-by-frontmatter.py index README.md --path docs/

Возвращает:
    0 — найдены файлы
    1 — файлы не найдены
"""

import argparse
import re
import sys
from pathlib import Path


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def parse_frontmatter(content: str) -> dict:
    """Извлечь frontmatter из markdown."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    result = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    return result


def find_files(root: Path, field: str, value: str) -> list[Path]:
    """Найти файлы с указанным полем frontmatter."""
    found = []
    for md_file in root.rglob('*.md'):
        try:
            content = md_file.read_text(encoding='utf-8')
            fm = parse_frontmatter(content)
            if fm.get(field) == value:
                found.append(md_file)
        except Exception:
            continue
    return found


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Поиск файлов по полю frontmatter"
    )
    parser.add_argument("field", help="Имя поля frontmatter")
    parser.add_argument("value", help="Значение поля")
    parser.add_argument("--path", default=".", help="Папка для поиска")

    args = parser.parse_args()

    root = find_repo_root(Path(args.path))
    search_path = root / args.path if args.path != "." else root

    files = find_files(search_path, args.field, args.value)

    if not files:
        print(f"Файлы с {args.field}: {args.value} не найдены")
        sys.exit(1)

    for f in sorted(files):
        print(f.relative_to(root))

    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## 9. Правила для create/modify скриптов

Инструкции create-script.md и modify-script.md следуют дополнительным правилам.

### Проверка существующих скриптов

> **Перед созданием — проверить существующие (DRY).**

Воркфлоу создания скрипта ДОЛЖЕН содержать шаг проверки:

1. Получить список существующих скриптов (`parse-docstrings.py`)
2. LLM анализирует на совпадения
3. Если найден похожий — AskUserQuestion:
   - Переиспользовать существующий
   - Доработать существующий → `/script-modify`
   - Создать новый

**Принцип:** Не создавать дубликаты. Сначала проверить, потом создавать.

### Циклы подтверждения

> **При отклонении — исправить и повторить.**

Воркфлоу МОЖЕТ содержать цикл подтверждения для шагов, требующих ревью кода.

**Применение:** Автор инструкции решает, нужен ли цикл для конкретного шага.

### Отчёт о проделанной работе

> **Каждый воркфлоу завершается отчётом.**

**Шаблон для создания:**

```
## Отчёт о создании скрипта

**Создан скрипт:** `{путь}`

**Назначение:** {description из docstring}

**Связанная инструкция:** `{путь к инструкции}`

**Автоматизирует шаг:** {номер и название шага}

**Валидация:** пройдена ✅
```

**Шаблон для изменения:**

```
## Отчёт об изменении скрипта

**Изменён скрипт:** `{путь}`

**Тип изменения:** {Обновление/Рефакторинг}

**Что изменено:**
- {список изменений}

**Проверка совместимости:**
- Ссылающиеся страницы: {количество}
- Статус: совместимо ✅ / обновлены ссылки ✅

**Связанные инструкции обновлены:** {список или "не требовалось"}

**Валидация:** пройдена ✅
```

### Связь со скиллом

> **Воркфлоу create/modify/validation скриптов ДОЛЖЕН иметь связанный скилл.**

| Инструкция | Скилл |
|------------|-------|
| `create-script.md` | `/script-create` |
| `modify-script.md` | `/script-modify` |
| `validation-script.md` | `/script-validate`
