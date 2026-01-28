---
description: Стандарт формата скриптов автоматизации
standard: .instructions/standard-instruction.md
index: .instructions/README.md
---

# Стандарт скриптов

Формат и структура скриптов автоматизации в папках `.scripts/`.

**Полезные ссылки:**
- [Инструкции](./README.md)

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Расположение](#2-расположение)
- [3. Формат файла](#3-формат-файла)
- [4. Docstring](#4-docstring)
- [5. Структура кода](#5-структура-кода)
- [6. Примеры](#6-примеры)

---

## 1. Назначение

Скрипты — исполняемый код для автоматизации рутинных операций.

**Когда создавать скрипт:**
- Операция повторяется более 2 раз
- Операция содержит более 3 шагов
- Требуется валидация данных
- Требуется трансформация данных

**Когда НЕ создавать скрипт:**
- Разовая операция
- Простое действие (1-2 команды)
- Логика уже есть в скилле

---

## 2. Расположение

```
{папка}/.instructions/.scripts/{script-name}.py
```

### Правила именования

| Паттерн | Назначение | Пример |
|---------|------------|--------|
| `validate-{object}.py` | Валидация объекта | `validate-instruction.py` |
| `{object}-validate.py` | Альтернатива | `instruction-validate.py` |
| `{action}-{object}.py` | Действие над объектом | `generate-readme.py` |
| `{object}.py` | Управление объектом (CRUD) | `ssot.py` |

### Связь с инструкциями

| Скрипт | Инструкция |
|--------|------------|
| `validate-*.py` | `validation-*.md` |
| `create-*.py` | `create-*.md` |
| `*-update.py` | `modify-*.md` |

---

## 3. Формат файла

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

## 4. Docstring

Docstring — **единственное место** для документации скрипта (замена frontmatter).

### Обязательная структура

```python
"""
{script-name}.py — {Краткое описание}.

Использование:
    python {script-name}.py <обязательный> [--опция <значение>]
    python {script-name}.py --флаг

Примеры:
    python {script-name}.py input.txt
    python {script-name}.py --repo /path/to/repo

{Дополнительные секции — опционально}

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

### Пример полного docstring

```python
"""
validate.py — Единый скрипт валидации проекта.

Использование:
    python validate.py [--repo <корень>] [--path <папка>]
    python validate.py --structure           # Только структура
    python validate.py --links               # Только ссылки

Примеры:
    python validate.py                       # Все проверки
    python validate.py --path test/          # Проверки только для test/

Запускает:
    - validate-structure.py — согласованность SSOT
    - validate-links.py — валидность ссылок

Возвращает:
    0 — всё валидно
    1 — есть ошибки
"""
```

---

## 5. Структура кода

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

### Общие функции (копируемые)

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

---

## 6. Примеры

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

### Скрипт с субкомандами

```python
#!/usr/bin/env python3
"""
crud.py — Управление объектами.

Подкоманды:
    add     Добавить объект
    delete  Удалить объект

Использование:
    python crud.py add <name> --description "Desc"
    python crud.py delete <name>

Примеры:
    python crud.py add item --description "New item"
    python crud.py delete old-item

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
import sys


def cmd_add(name: str, description: str) -> bool:
    print(f"✅ Добавлен: {name}")
    return True


def cmd_delete(name: str) -> bool:
    print(f"✅ Удалён: {name}")
    return True


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Управление объектами")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_p = subparsers.add_parser("add", help="Добавить объект")
    add_p.add_argument("name", help="Имя объекта")
    add_p.add_argument("--description", "-d", required=True)

    # delete
    del_p = subparsers.add_parser("delete", help="Удалить объект")
    del_p.add_argument("name", help="Имя объекта")

    args = parser.parse_args()

    if args.command == "add":
        success = cmd_add(args.name, args.description)
    elif args.command == "delete":
        success = cmd_delete(args.name)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

---

## Связанные инструкции

- [validation-script.md](./validation-script.md) — валидация скриптов
- [create-script.md](./create-script.md) — создание скрипта
- [modify-script.md](./modify-script.md) — изменение скрипта
