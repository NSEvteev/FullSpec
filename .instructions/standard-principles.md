---
description: Принципы программирования (примеры на Python)
standard: .instructions/standard-instruction.md
index: .instructions/README.md
---

# Стандарт принципов программирования

Универсальные принципы написания кода. Примеры приведены на Python, но применимы к любому языку.

**Полезные ссылки:**
- [Инструкции](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-principles.md](./validation-principles.md) |

## Оглавление

- [1. KISS](#1-kiss)
- [2. DRY](#2-dry)
- [3. YAGNI](#3-yagni)
- [4. Принцип наименьшего удивления](#4-принцип-наименьшего-удивления)
- [5. SOLID](#5-solid)
- [6. Читаемость и документация](#6-читаемость-и-документация)
- [7. Обработка ошибок](#7-обработка-ошибок)
- [8. Минимизация зависимостей](#8-минимизация-зависимостей)

---

> **Шаблоны — из примеров SSOT.** При создании файлов использовать шаблоны из секции "Примеры". Запрещено придумывать свой формат.

---

## 1. KISS

**Keep It Simple, Stupid** — код должен быть максимально простым.

### Правило

Выбирать простое решение вместо сложного, даже если сложное кажется "элегантнее".

### Пример

```python
# ❌ Плохо: переусложнённо
def process_files(files):
    return list(filter(lambda x: x.suffix == '.md',
                      map(lambda x: Path(x), files)))

# ✅ Хорошо: просто и понятно
def process_files(files):
    result = []
    for f in files:
        path = Path(f)
        if path.suffix == '.md':
            result.append(path)
    return result
```

### Признаки нарушения

- Вложенные lambda-выражения
- Цепочки map/filter/reduce без необходимости
- Однострочники, которые сложно читать
- Преждевременные оптимизации

---

## 2. DRY

**Don't Repeat Yourself** — избегать дублирования кода.

### Правило

Каждая часть знания должна иметь единственное, непротиворечивое представление в системе.

### Пример

```python
# ❌ Плохо: дублирование
def validate_instruction(path):
    if not path.exists():
        print(f"❌ Файл не найден: {path}")
        return False
    # ...

def validate_script(path):
    if not path.exists():
        print(f"❌ Файл не найден: {path}")
        return False
    # ...

# ✅ Хорошо: общая функция
def check_file_exists(path, entity_type="Файл"):
    if not path.exists():
        print(f"❌ {entity_type} не найден: {path}")
        return False
    return True

def validate_instruction(path):
    if not check_file_exists(path, "Инструкция"):
        return False
    # ...

def validate_script(path):
    if not check_file_exists(path, "Скрипт"):
        return False
    # ...
```

### Признаки нарушения

- Копирование блоков кода между функциями
- Одинаковые сообщения об ошибках в разных местах
- Повторяющиеся паттерны валидации

---

## 3. YAGNI

**You Aren't Gonna Need It** — не добавлять функционал "на будущее".

### Правило

Реализовывать только то, что нужно сейчас. Не пытаться предугадать будущие требования.

### Пример

```python
# ❌ Плохо: функционал "про запас"
def validate(path, format='text', verbose=False,
             strict=False, cache=True, parallel=False,
             output_file=None, log_level='INFO'):
    # ...

# ✅ Хорошо: только то, что нужно сейчас
def validate(path):
    # ...
```

### Признаки нарушения

- Неиспользуемые аргументы функций
- Пустые методы "для будущего расширения"
- Абстракции без конкретного применения
- Конфигурационные параметры, которые никто не меняет

---

## 4. Принцип наименьшего удивления

**Principle of Least Astonishment** — код должен делать то, что ожидает пользователь.

### Правило

Поведение функции должно соответствовать её имени и документации. Никаких скрытых побочных эффектов.

### Пример

```python
# ❌ Плохо: неожиданное поведение
def delete_file(path):
    """Удаляет файл."""
    shutil.rmtree(path)  # Удаляет папку!

# ✅ Хорошо: предсказуемое поведение
def delete_file(path):
    """Удаляет файл."""
    Path(path).unlink()

def delete_directory(path):
    """Удаляет папку со всем содержимым."""
    shutil.rmtree(path)
```

### Правила

| Аспект | Правило |
|--------|---------|
| Имена функций | Точно отражают действие |
| Аргументы | Очевидные значения по умолчанию |
| Побочные эффекты | Документированы явно |
| Возвращаемые значения | Консистентные типы |

### Признаки нарушения

- Функция делает больше, чем говорит имя
- Неочевидные значения по умолчанию
- Скрытые изменения глобального состояния
- Разные типы возвращаемых значений в разных ветках

---

## 5. SOLID

**Применимые принципы:**

### S — Single Responsibility

**Один модуль/функция = одна задача.**

```python
# ❌ Плохо: функция делает всё
def main():
    validate_structure()
    validate_links()
    generate_report()
    send_email()

# ✅ Хорошо: разделение ответственности
# validate_structure() — валидация структуры
# validate_links() — валидация ссылок
# main() — координация, вызов других функций
```

### O — Open/Closed

**Расширение через аргументы, не изменение кода.**

```python
# ❌ Плохо: изменение кода для нового формата
def output_result(data):
    print(json.dumps(data))

# ✅ Хорошо: расширение через аргументы
def output_result(data, format='text'):
    if format == 'json':
        print(json.dumps(data))
    else:
        print(data)
```

### D — Dependency Inversion

**Зависимость от абстракций.**

```python
# ❌ Плохо: зависимость от конкретики
def process(file_path: str):
    with open(file_path) as f:
        return f.read()

# ✅ Хорошо: зависимость от абстракции
def process(file_path: Path):
    return file_path.read_text()
```

---

## 6. Читаемость и документация

### Правило

Код читается чаще, чем пишется. Приоритет — понятность для будущего читателя.

### Docstring для функций

```python
# ❌ Плохо: нет документации
def f(x, y):
    return [i for i in x if i.n in y]

# ✅ Хорошо: понятный код с документацией
def filter_files_by_names(files: list[Path], names: set[str]) -> list[Path]:
    """
    Фильтрует файлы по именам.

    Args:
        files: Список путей к файлам
        names: Множество допустимых имён

    Returns:
        Файлы, имена которых есть в names
    """
    return [f for f in files if f.name in names]
```

### Правила

| Элемент | Требование |
|---------|------------|
| Функции | Docstring обязателен |
| Аргументы | Типизация (type hints) |
| Переменные | Осмысленные имена |
| Константы | UPPER_CASE с комментарием |

### Признаки нарушения

- Однобуквенные имена переменных (кроме итераторов)
- Функции без docstring
- Магические числа без объяснения
- Аббревиатуры без расшифровки

---

## 7. Обработка ошибок

### Правило

Ошибки должны обрабатываться явно. Никогда не игнорировать исключения.

### Пример

```python
# ❌ Плохо: игнорирование ошибок
def read_frontmatter(path):
    try:
        content = path.read_text()
        return parse_yaml(content)
    except:
        return {}

# ✅ Хорошо: явная обработка
def read_frontmatter(path: Path) -> dict | None:
    """Читает frontmatter из файла."""
    if not path.exists():
        print(f"⚠️ Файл не найден: {path}", file=sys.stderr)
        return None

    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        print(f"⚠️ Ошибка кодировки {path}: {e}", file=sys.stderr)
        return None

    return parse_yaml(content)
```

### Правила

| Правило | Описание |
|---------|----------|
| Нет голого `except:` | Указывать конкретный тип исключения |
| Логирование | Ошибки выводить в stderr |
| Возвращаемые значения | None или пустая структура при ошибке |
| Ранний выход | Проверять условия в начале функции |

### Признаки нарушения

- `except:` без указания типа исключения
- `pass` в блоке except
- Ошибки в stdout вместо stderr
- Возврат разных типов при ошибке и успехе

---

## 8. Минимизация зависимостей

### Правило

> **Не подключать библиотеку ради одной функции.**

### Пример

```python
# ❌ Плохо: тяжёлая зависимость для простой задачи
import pandas as pd

def count_lines(path):
    return len(pd.read_csv(path))

# ✅ Хорошо: стандартная библиотека
def count_lines(path):
    with open(path) as f:
        return sum(1 for _ in f)
```

### Допустимые зависимости

| Зависимость | Когда использовать |
|-------------|-------------------|
| Стандартная библиотека | Всегда |
| PyYAML | Работа с frontmatter |
| argparse | CLI (встроен) |

### Недопустимые зависимости

| Библиотека | Замена |
|------------|--------|
| requests | urllib.request |
| pandas | csv модуль |
| click | argparse |
| colorama | ANSI-коды напрямую |

### Признаки нарушения

- import тяжёлой библиотеки для одной функции
- Зависимость, которую нужно устанавливать через pip
- Использование библиотеки вместо стандартной функции
