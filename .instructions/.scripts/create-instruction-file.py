#!/usr/bin/env python3
"""
create-instruction-file.py — Создание файла инструкции по шаблону.

Создаёт новый файл инструкции в указанной папке .instructions/
с заполненным frontmatter и базовой структурой.

Использование:
    python create-instruction-file.py <name> <type> [--area <path>] [--description <text>]

Аргументы:
    name        Имя инструкции (без префикса и расширения)
    type        Тип: standard, create, modify, validation

Примеры:
    python create-instruction-file.py api-versioning standard
    python create-instruction-file.py script create --area .instructions
    python create-instruction-file.py links validation --area .structure/.instructions --description "Валидация ссылок"

Возвращает:
    0 — файл создан
    1 — ошибка (файл существует, неверные аргументы)
"""

import argparse
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

VALID_TYPES = ("standard", "create", "modify", "validation")
VERSION_PATTERN = re.compile(r"^Версия стандарта:\s*(\d+\.\d+)", re.MULTILINE)

TEMPLATES = {
    "standard": '''---
description: {description}
standard: {standard_path}
standard-version: v{standard_version}
index: {index_path}
---

# Стандарт {title}

Версия стандарта: 1.0

{short_description}

**Полезные ссылки:**
- [Инструкции]({readme_link})

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-{name}.md](./validation-{name}.md) |
| Создание | [create-{name}.md](./create-{name}.md) |
| Модификация | [modify-{name}.md](./modify-{name}.md) |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Правила](#2-правила)
- [3. Примеры](#3-примеры)

---

## 1. Назначение

<!-- Описание: что регламентирует этот стандарт -->

---

## 2. Правила

<!-- Правила и требования -->

---

## 3. Примеры

<!-- Примеры применения -->
''',

    "create": '''---
description: {description}
standard: {standard_path}
standard-version: v{standard_version}
index: {index_path}
---

# Воркфлоу создания

Рабочая версия стандарта: {standard_version}

{short_description}

**Полезные ссылки:**
- [Инструкции]({readme_link})

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-{name}.md](./standard-{name}.md) |
| Валидация | [validation-{name}.md](./validation-{name}.md) |
| Создание | Этот документ |
| Модификация | [modify-{name}.md](./modify-{name}.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

<!-- Ключевые принципы создания -->

---

## Шаги

### Шаг 1: Подготовка

<!-- Описание шага -->

### Шаг 2: Создание

<!-- Описание шага -->

### Шаг 3: Валидация

<!-- Описание шага -->

---

## Чек-лист

- [ ] Шаг 1 выполнен
- [ ] Шаг 2 выполнен
- [ ] Валидация пройдена

---

## Примеры

<!-- Примеры использования -->

---

## Скрипты

*Нет скриптов.*

---

## Скиллы

*Нет скиллов.*
''',

    "modify": '''---
description: {description}
standard: {standard_path}
standard-version: v{standard_version}
index: {index_path}
---

# Воркфлоу изменения

Рабочая версия стандарта: {standard_version}

{short_description}

**Полезные ссылки:**
- [Инструкции]({readme_link})

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-{name}.md](./standard-{name}.md) |
| Валидация | [validation-{name}.md](./validation-{name}.md) |
| Создание | [create-{name}.md](./create-{name}.md) |
| Модификация | Этот документ |

## Оглавление

- [Типы изменений](#типы-изменений)
- [Обновление](#обновление)
- [Удаление](#удаление)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Типы изменений

| Тип | Описание |
|-----|----------|
| Обновление | Изменение содержимого |
| Удаление | Удаление объекта |

---

## Обновление

### Шаг 1: Найти объект

<!-- Описание шага -->

### Шаг 2: Внести изменения

<!-- Описание шага -->

### Шаг 3: Валидация

<!-- Описание шага -->

---

## Удаление

### Шаг 1: Найти зависимости

<!-- Описание шага -->

### Шаг 2: Удалить

<!-- Описание шага -->

---

## Чек-лист

### Обновление
- [ ] Найден объект
- [ ] Внесены изменения
- [ ] Валидация пройдена

### Удаление
- [ ] Найдены зависимости
- [ ] Зависимости обновлены
- [ ] Объект удалён

---

## Примеры

<!-- Примеры использования -->

---

## Скрипты

*Нет скриптов.*

---

## Скиллы

*Нет скиллов.*
''',

    "validation": '''---
description: {description}
standard: {standard_path}
standard-version: v{standard_version}
index: {index_path}
---

# Валидация {title}

Рабочая версия стандарта: {standard_version}

{short_description}

**Полезные ссылки:**
- [Инструкции]({readme_link})

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-{name}.md](./standard-{name}.md) |
| Валидация | Этот документ |
| Создание | [create-{name}.md](./create-{name}.md) |
| Модификация | [modify-{name}.md](./modify-{name}.md) |

## Оглавление

- [Когда валидировать](#когда-валидировать)
- [Шаги](#шаги)
- [Чек-лист](#чек-лист)
- [Типичные ошибки](#типичные-ошибки)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Когда валидировать

**Обязательно:**
- Перед коммитом
- После изменений
- При code review

**Опционально:**
- В CI/CD pipeline

---

## Шаги

### Шаг 1: Проверить структуру

<!-- Описание шага -->

### Шаг 2: Проверить содержимое

<!-- Описание шага -->

---

## Чек-лист

- [ ] Структура проверена
- [ ] Содержимое проверено

---

## Типичные ошибки

| Ошибка | Код | Причина | Решение |
|--------|-----|---------|---------|
| — | — | — | — |

---

## Скрипты

*Нет скриптов.*

---

## Скиллы

*Нет скиллов.*
''',
}


# =============================================================================
# Общие функции
# =============================================================================

def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def get_standard_version(file_path: Path) -> str | None:
    """Извлечь версию из строки 'Версия стандарта: X.Y'."""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = VERSION_PATTERN.search(content)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None


# =============================================================================
# Основные функции
# =============================================================================

def create_instruction_file(
    name: str,
    inst_type: str,
    area: Path,
    repo_root: Path,
    description: str | None = None
) -> Path:
    """Создать файл инструкции."""
    # Убрать префикс из name, если он уже есть
    # Например: если name="standard-rule" и type="standard", то name станет "rule"
    for prefix in VALID_TYPES:
        prefix_with_dash = f"{prefix}-"
        if name.startswith(prefix_with_dash):
            name = name[len(prefix_with_dash):]
            break

    # Полное имя файла
    filename = f"{inst_type}-{name}.md"
    file_path = area / filename

    # Проверить существование
    if file_path.exists():
        raise FileExistsError(f"Файл уже существует: {file_path}")

    # Определить пути для frontmatter
    rel_area = area.relative_to(repo_root)

    # standard — путь к standard-instruction.md (для frontmatter)
    standard_path = ".instructions/standard-instruction.md"

    # Получить версию стандарта
    # Для типа standard — всегда 1.0 (новый стандарт)
    # Для create/modify/validation — из standard-{name}.md в той же папке
    if inst_type == "standard":
        standard_version = "1.0"
    else:
        # Найти standard-{name}.md в той же папке
        object_standard_file = area / f"standard-{name}.md"
        if not object_standard_file.exists():
            raise FileNotFoundError(
                f"Не найден standard-{name}.md в {area}. "
                f"Сначала создайте стандарт: /instruction-create {name} --type standard"
            )
        standard_version = get_standard_version(object_standard_file)
        if not standard_version:
            raise ValueError(f"Не найдена 'Версия стандарта:' в {object_standard_file}")

    # index — README этой папки
    index_path = f"{rel_area}/README.md".replace("\\", "/")

    # readme_link — ссылка на README
    readme_link = "./README.md"

    # Описание по умолчанию
    if not description:
        type_desc = {
            "standard": f"Стандарт формата {name}",
            "create": f"Воркфлоу создания {name}",
            "modify": f"Воркфлоу изменения {name}",
            "validation": f"Валидация формата {name}",
        }
        description = type_desc.get(inst_type, f"Инструкция {name}")

    # Title для заголовка
    title = name.replace("-", " ")

    # Short description
    short_description = description

    # Заполнить шаблон
    template = TEMPLATES[inst_type]
    content = template.format(
        name=name,
        title=title,
        description=description,
        short_description=short_description,
        standard_path=standard_path,
        standard_version=standard_version,
        index_path=index_path,
        readme_link=readme_link,
    )

    # Создать директорию если нужно
    area.mkdir(parents=True, exist_ok=True)

    # Записать файл
    file_path.write_text(content, encoding='utf-8')

    return file_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание файла инструкции по шаблону"
    )
    parser.add_argument("name", help="Имя инструкции (без префикса)")
    parser.add_argument("type", choices=VALID_TYPES, help="Тип инструкции")
    parser.add_argument(
        "--area", default=".instructions",
        help="Папка .instructions (по умолчанию: .instructions)"
    )
    parser.add_argument(
        "--description",
        help="Описание для frontmatter"
    )
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    area = repo_root / args.area

    # Проверить что area — папка .instructions
    if not area.name == ".instructions" and ".instructions" not in str(area):
        print(f"❌ Область должна быть папкой .instructions: {area}", file=sys.stderr)
        sys.exit(1)

    try:
        file_path = create_instruction_file(
            name=args.name,
            inst_type=args.type,
            area=area,
            repo_root=repo_root,
            description=args.description,
        )
        rel_path = file_path.relative_to(repo_root)
        print(f"✅ Создан: {rel_path}")
        sys.exit(0)

    except FileExistsError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
