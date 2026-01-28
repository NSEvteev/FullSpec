---
description: Воркфлоу создания нового скрипта
standard: .instructions/standard-instruction.md
index: .instructions/README.md
---

# Создание скрипта

Пошаговый процесс создания нового скрипта автоматизации.

**Полезные ссылки:**
- [Инструкции](./README.md)

## Оглавление

- [1. Когда создавать](#1-когда-создавать)
- [2. Подготовка](#2-подготовка)
- [3. Шаги создания](#3-шаги-создания)
- [4. Шаблон](#4-шаблон)
- [5. Чек-лист](#5-чек-лист)

---

## 1. Когда создавать

**Создавать скрипт когда:**

| Критерий | Порог |
|----------|-------|
| Повторяемость | > 2 раз |
| Количество шагов | > 3 шагов |
| Валидация данных | Требуется |
| Трансформация данных | Требуется |

**НЕ создавать скрипт когда:**

- Разовая операция
- Простое действие (1-2 команды)
- Логика уже реализована в скилле
- Существует аналогичный скрипт

---

## 2. Подготовка

### 2.1. Определить назначение

```
Вопросы:
1. Что делает скрипт? (одно предложение)
2. Какие входные данные?
3. Какой выход?
4. Есть ли побочные эффекты?
```

### 2.2. Выбрать имя

| Паттерн | Когда использовать |
|---------|-------------------|
| `validate-{object}.py` | Валидация |
| `create-{object}.py` | Создание |
| `{action}-{object}.py` | Действие над объектом |
| `{object}.py` | CRUD операции |

### 2.3. Определить расположение

```
{область}/.instructions/.scripts/{script-name}.py
```

Примеры:
- `/.instructions/.scripts/validate-instruction.py`
- `/.structure/.instructions/.scripts/ssot.py`
- `/specs/.instructions/.scripts/check-status.py`

---

## 3. Шаги создания

```
1. Создать файл
   └── Расположение: {область}/.instructions/.scripts/{name}.py

2. Добавить shebang
   └── #!/usr/bin/env python3

3. Написать docstring
   ├── Первая строка: {name}.py — {описание}.
   ├── Секция: Использование
   ├── Секция: Примеры
   └── Секция: Возвращает

4. Добавить импорты
   └── stdlib → third-party → local

5. Реализовать логику
   ├── Константы (если нужны)
   ├── Вспомогательные функции
   └── Основные функции

6. Добавить main()
   ├── UTF-8 для Windows
   ├── argparse
   └── sys.exit()

7. Добавить if __name__
   └── if __name__ == "__main__": main()

8. Протестировать
   ├── Позитивные сценарии
   └── Негативные сценарии

9. Валидировать
   └── python validate-script.py {name}.py

10. Обновить README
    └── Добавить скрипт в секцию "Скрипты"
```

---

## 4. Шаблон

```python
#!/usr/bin/env python3
"""
{script-name}.py — {Краткое описание}.

Использование:
    python {script-name}.py <input> [--option <value>]

Примеры:
    python {script-name}.py file.txt
    python {script-name}.py data.json --output result.json

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
import sys
from pathlib import Path


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def process(input_path: Path) -> bool:
    """
    Основная логика скрипта.

    Args:
        input_path: Путь к входному файлу

    Returns:
        True если успех, False если ошибка
    """
    # TODO: реализовать
    print(f"✅ Обработан: {input_path}")
    return True


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="{Краткое описание}"
    )
    parser.add_argument(
        "input",
        help="Входной файл"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    input_path = Path(args.input)

    success = process(input_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

---

## 5. Чек-лист

```markdown
## Чек-лист создания скрипта

### Подготовка
- [ ] Определено назначение (одно предложение)
- [ ] Выбрано имя по паттерну
- [ ] Определено расположение

### Реализация
- [ ] Создан файл .py
- [ ] Добавлен shebang
- [ ] Написан docstring со всеми секциями
- [ ] Реализована логика
- [ ] Добавлена функция main() с UTF-8 и argparse
- [ ] Добавлен if __name__

### Проверка
- [ ] Протестированы позитивные сценарии
- [ ] Протестированы негативные сценарии
- [ ] Пройдена валидация формата

### Документация
- [ ] Скрипт добавлен в README секцию "Скрипты"
```

---

## Связанные инструкции

- [standard-script.md](./standard-script.md) — стандарт формата
- [validation-script.md](./validation-script.md) — валидация скриптов
- [modify-script.md](./modify-script.md) — изменение скрипта
