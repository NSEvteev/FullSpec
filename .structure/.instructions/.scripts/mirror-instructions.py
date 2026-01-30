#!/usr/bin/env python3
"""
mirror-instructions.py — Зеркалирование структуры в .instructions.

Подкоманды:
    create  Создать зеркало .instructions для папки
    rename  Переименовать зеркало при переименовании папки
    move    Переместить зеркало при перемещении папки

Использование:
    python mirror-instructions.py create <папка>
    python mirror-instructions.py rename <старый_путь> <новый_путь>
    python mirror-instructions.py move <старый_путь> <новый_путь>

Примеры:
    python mirror-instructions.py create docs
    python mirror-instructions.py create docs/api
    python mirror-instructions.py rename docs/api docs/endpoints
    python mirror-instructions.py move src/utils shared/utils

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

INSTRUCTIONS_DIR = ".instructions"

README_TEMPLATE = """---
description: Индекс инструкций для {folder_name}/
standard: .structure/.instructions/standard-readme.md
index: {index_path}
---

# Инструкции /{full_path}/

Индекс инструкций для папки {folder_name}/.

**Полезные ссылки:**
{useful_links}

**Содержание:** *добавить темы через запятую.*

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/{instructions_tree_path}/
└── README.md                # Этот файл (индекс)
```

---

# 1. Стандарты

*Нет стандартов.*

---

# 2. Воркфлоу

*Нет воркфлоу.*

---

# 3. Валидация

*Нет валидаций.*

---

# 4. Скрипты

*Нет скриптов.*

---

# 5. Скиллы

*Нет скиллов.*
"""


README_TEMPLATE_WITH_NESTED = """---
description: Индекс инструкций для {folder_name}/
standard: .structure/.instructions/standard-readme.md
index: {index_path}
---

# Инструкции /{full_path}/

Индекс инструкций для папки {folder_name}/.

**Полезные ссылки:**
{useful_links}

**Содержание:** *добавить темы через запятую.*

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [Вложенные области](#вложенные-области) | — | Подобласти инструкций |
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/{instructions_tree_path}/
├── README.md                # Этот файл (индекс)
{nested_tree}
```

---

## Вложенные области

Инструкции разделены на подобласти:

| Область | Описание | Индекс |
|---------|----------|--------|
{nested_table}

---

# 1. Стандарты

*Нет стандартов в корне — см. вложенные области.*

---

# 2. Воркфлоу

*Нет воркфлоу в корне — см. вложенные области.*

---

# 3. Валидация

*Нет валидаций в корне — см. вложенные области.*

---

# 4. Скрипты

*Нет скриптов.*

---

# 5. Скиллы

*См. скиллы во вложенных областях.*
"""


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


def parse_folder_path(folder_path: str) -> tuple:
    """
    Парсить путь папки.

    Returns:
        (full_path, root_folder, subpath, depth)

    Примеры:
        "docs" -> ("docs", "docs", None, 0)
        "docs/api" -> ("docs/api", "docs", "api", 1)
        "docs/api/v1" -> ("docs/api/v1", "docs", "api/v1", 2)
    """
    parts = folder_path.strip("/").split("/")
    full_path = "/".join(parts)
    root_folder = parts[0]
    subpath = "/".join(parts[1:]) if len(parts) > 1 else None
    depth = len(parts) - 1
    return full_path, root_folder, subpath, depth


def get_instructions_path(repo_root: Path, folder_path: str) -> Path:
    """
    Получить путь к зеркалу .instructions для папки.

    Примеры:
        "docs" -> repo_root/docs/.instructions/
        "docs/api" -> repo_root/docs/.instructions/api/
    """
    full_path, root_folder, subpath, depth = parse_folder_path(folder_path)

    if depth == 0:
        # Корневая папка: docs/.instructions/
        return repo_root / root_folder / INSTRUCTIONS_DIR
    else:
        # Подпапка: docs/.instructions/api/
        return repo_root / root_folder / INSTRUCTIONS_DIR / subpath


def generate_readme_content(folder_path: str, repo_root: Path) -> str:
    """Сгенерировать содержимое README.md для .instructions по стандарту."""
    full_path, root_folder, subpath, depth = parse_folder_path(folder_path)

    folder_name = full_path.split("/")[-1]

    # Путь к index
    if depth == 0:
        # docs/.instructions/README.md
        index_path = f"{root_folder}/.instructions/README.md"
        instructions_tree_path = f"{root_folder}/.instructions"
    else:
        # docs/.instructions/api/README.md
        index_path = f"{root_folder}/.instructions/{subpath}/README.md"
        instructions_tree_path = f"{root_folder}/.instructions/{subpath}"

    # Генерация "Полезные ссылки" по стандарту раздела 3
    # Цепочка до README родительской папки (не до структуры проекта)
    useful_links = generate_useful_links(folder_path, depth)

    return README_TEMPLATE.format(
        folder_name=folder_name,
        full_path=full_path,
        index_path=index_path,
        useful_links=useful_links,
        instructions_tree_path=instructions_tree_path,
    )


def generate_useful_links(folder_path: str, depth: int) -> str:
    """
    Сгенерировать блок "Полезные ссылки" для README инструкций.

    По стандарту standard-readme.md#3:
    - README инструкций → ../README.md (README родительской папки проекта)
    - README подпапки инструкций → ../README.md → ../../README.md (цепочка)
    """
    parts = folder_path.split("/")
    lines = []

    if depth == 0:
        # docs/.instructions/README.md → ссылка на docs/README.md
        folder_name = parts[0]
        lines.append(f"- [{folder_name}/](../README.md)")
    else:
        # docs/.instructions/api/README.md → цепочка
        # Первая ссылка — на README родительской .instructions
        lines.append(f"- [Инструкции {parts[0]}/](../README.md)")
        # Вторая ссылка — на README папки проекта
        ups = "../" * 2
        lines.append(f"- [{parts[0]}/]({ups}README.md)")

    return "\n".join(lines)


# =============================================================================
# CREATE — Создание зеркала
# =============================================================================

def cmd_create(repo_root: Path, folder_path: str, dry_run: bool = False) -> bool:
    """Создать зеркало .instructions для папки."""
    full_path, root_folder, subpath, depth = parse_folder_path(folder_path)

    # Проверяем существование папки
    target_folder = repo_root / full_path
    if not target_folder.exists():
        print(f"❌ Папка не существует: {target_folder}", file=sys.stderr)
        return False

    # Путь к зеркалу
    instructions_path = get_instructions_path(repo_root, folder_path)
    readme_path = instructions_path / "README.md"

    if readme_path.exists():
        print(f"⚠️  Зеркало уже существует: {readme_path}", file=sys.stderr)
        return True

    # Генерируем содержимое
    content = generate_readme_content(folder_path, repo_root)

    if dry_run:
        print(f"=== DRY RUN: {readme_path} ===")
        print(content)
        return True

    # Создаём папку и файл
    instructions_path.mkdir(parents=True, exist_ok=True)
    readme_path.write_text(content, encoding="utf-8")

    print(f"✅ Зеркало создано: {readme_path}")
    print(f"ℹ️  .instructions/ будет добавлена в SSOT при добавлении родительской папки")

    # Обновляем README родительских инструкций (для подпапок)
    if depth > 0:
        update_parent_instructions_readme(repo_root, folder_path)

    return True


def update_parent_instructions_readme(repo_root: Path, folder_path: str, description: str = None) -> bool:
    """
    Обновить README родительских инструкций при создании подпапки.

    При создании test/.instructions/subtest/ обновляет test/.instructions/README.md:
    - Добавляет в таблицу оглавления
    - Добавляет в дерево
    - Добавляет в секцию "Вложенные области" (если есть)
    """
    full_path, root_folder, subpath, depth = parse_folder_path(folder_path)

    if depth == 0:
        return False  # Корневая папка — нет родителя

    # README родительских инструкций
    parent_readme = repo_root / root_folder / INSTRUCTIONS_DIR / "README.md"
    if not parent_readme.exists():
        return False

    folder_name = full_path.split("/")[-1]
    content = parent_readme.read_text(encoding="utf-8")
    lines = content.split("\n")

    # 1. Добавляем в секцию "Вложенные области" (также добавит ссылку в оглавление если нужно)
    lines = add_to_nested_areas(lines, folder_name, description)

    # 2. Добавляем в дерево
    lines = add_to_instructions_tree(lines, folder_name)

    parent_readme.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Обновлён README инструкций: {parent_readme}")
    return True


def add_to_nested_areas(lines: list, folder_name: str, description: str = None) -> list:
    """
    Добавить подпапку в секцию "Вложенные области".

    Если секции нет — создаёт её.
    """
    content = "\n".join(lines)

    # Описание по умолчанию
    if not description:
        description = f"Инструкции для {folder_name}/"

    # Проверяем, есть ли уже эта подпапка в секции
    if f"[{folder_name}/]" in content and "## Вложенные области" in content:
        return lines

    # Ищем секцию "Вложенные области"
    nested_start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Вложенные области":
            nested_start = i
            break

    if nested_start is not None:
        # Секция существует — добавляем строку в таблицу
        # Ищем конец таблицы (пустая строка после таблицы или ---)
        table_end = None
        for i in range(nested_start + 1, len(lines)):
            line = lines[i].strip()
            if line.startswith("|") and "|" in line[1:]:
                table_end = i + 1
            elif table_end and (line == "" or line == "---"):
                break

        if table_end:
            new_row = f"| [{folder_name}/](./{folder_name}/) | {description} | [README](./{folder_name}/README.md) |"
            result = lines[:table_end]
            result.append(new_row)
            result.extend(lines[table_end:])
            return result
    else:
        # Секции нет — создаём её перед "# 1. Стандарты"
        insert_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "# 1. Стандарты":
                insert_idx = i
                break

        if insert_idx is None:
            return lines

        nested_section = [
            "## Вложенные области",
            "",
            "Инструкции разделены на подобласти:",
            "",
            "| Область | Описание | Индекс |",
            "|---------|----------|--------|",
            f"| [{folder_name}/](./{folder_name}/) | {description} | [README](./{folder_name}/README.md) |",
            "",
            "---",
            "",
        ]

        result = lines[:insert_idx]
        result.extend(nested_section)
        result.extend(lines[insert_idx:])

        # Также нужно добавить в оглавление ссылку на "Вложенные области"
        result = add_nested_to_toc(result)

        return result

    return lines


def add_nested_to_toc(lines: list) -> list:
    """Добавить ссылку на 'Вложенные области' в оглавление (если её нет)."""
    content = "\n".join(lines)

    # Проверяем, есть ли уже ссылка
    if "[Вложенные области]" in content:
        return lines

    # Ищем таблицу оглавления
    for i, line in enumerate(lines):
        if "| [1. Стандарты]" in line:
            # Вставляем строку перед "1. Стандарты"
            new_row = "| [Вложенные области](#вложенные-области) | — | Подобласти инструкций |"
            result = lines[:i]
            result.append(new_row)
            result.extend(lines[i:])
            return result

    return lines


def add_to_instructions_toc(lines: list, folder_name: str) -> list:
    """Добавить подпапку в таблицу оглавления инструкций."""
    import re

    # Ищем таблицу оглавления (после "## Оглавление")
    toc_start = None
    toc_end = None

    for i, line in enumerate(lines):
        if line.strip() == "## Оглавление":
            toc_start = i + 1
        elif toc_start and line.startswith("```"):
            toc_end = i
            break

    if toc_start is None or toc_end is None:
        return lines

    # Проверяем, есть ли уже эта подпапка
    for i in range(toc_start, toc_end):
        if f"[{folder_name}/]" in lines[i]:
            return lines

    # Ищем позицию для вставки — после заголовка таблицы, но ДО секций (| [N. ...)
    # Заголовок таблицы: | Секция | Инструкция | Описание |
    # Разделитель: |--------|------------|----------|
    insert_idx = None
    for i in range(toc_start, toc_end):
        line = lines[i]
        if line.startswith("|") and "---" in line:
            # Нашли разделитель таблицы, вставляем после него
            insert_idx = i + 1
            break

    if insert_idx is None:
        return lines

    # Добавляем новую строку в таблицу
    new_row = f"| [{folder_name}/](./{folder_name}/README.md) | — | Инструкции для {folder_name}/ |"

    result = lines[:insert_idx]
    result.append(new_row)
    result.extend(lines[insert_idx:])

    return result


def add_to_instructions_tree(lines: list, folder_name: str) -> list:
    """Добавить подпапку в дерево инструкций."""
    import re

    # Ищем блок дерева (``` ... ```)
    tree_start = None
    tree_end = None

    for i, line in enumerate(lines):
        if line.strip().startswith("```") and tree_start is None:
            # Проверяем что это дерево (следующая строка начинается с /)
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("/"):
                tree_start = i + 1
        elif tree_start and line.strip() == "```":
            tree_end = i
            break

    if tree_start is None or tree_end is None:
        return lines

    # Проверяем, есть ли уже эта подпапка
    for i in range(tree_start, tree_end):
        if f"── {folder_name}/" in lines[i]:
            return lines

    # Собираем все элементы дерева (папки и файлы)
    tree_header = lines[tree_start]  # Строка с путём (например: /.claude/.instructions/)
    folders = []  # [(index, name, comment)]
    files = []    # [(index, name, comment)]

    for i in range(tree_start + 1, tree_end):
        line = lines[i]
        # Папка: ├── folder/ или └── folder/
        folder_match = re.match(r'^[├└]── ([^/\s]+)/\s*(#.*)?$', line)
        if folder_match:
            name = folder_match.group(1)
            comment = folder_match.group(2) or ""
            folders.append((i, name, comment.strip()))
            continue
        # Файл: ├── file или └── file
        file_match = re.match(r'^[├└]── ([^/\s]+)\s*(#.*)?$', line)
        if file_match:
            name = file_match.group(1)
            comment = file_match.group(2) or ""
            files.append((i, name, comment.strip()))

    # Добавляем новую папку
    new_comment = f"# Инструкции для {folder_name}/"
    folders.append((None, folder_name, new_comment))

    # Сортируем папки по алфавиту (с учётом точки в начале)
    def sort_key(item):
        name = item[1]
        starts_with_dot = name.startswith(".")
        clean_name = name.lstrip(".")
        return (not starts_with_dot, clean_name.lower())

    folders.sort(key=sort_key)

    # Формируем новое дерево
    result = lines[:tree_start]
    result.append(tree_header)

    # Вычисляем максимальную длину для выравнивания комментариев
    max_prefix_len = max(len(f"├── {f[1]}/") for f in folders) if folders else 20
    max_prefix_len = max(max_prefix_len, max(len(f"├── {f[1]}") for f in files) if files else 20)

    # Добавляем папки
    for idx, (_, name, comment) in enumerate(folders):
        is_last = (idx == len(folders) - 1) and len(files) == 0
        connector = "└── " if is_last else "├── "
        prefix = f"{connector}{name}/"
        padding = max(1, max_prefix_len - len(prefix) + 4)
        line = f"{prefix}{' ' * padding}{comment}" if comment else prefix
        result.append(line)

    # Добавляем файлы
    for idx, (_, name, comment) in enumerate(files):
        is_last = idx == len(files) - 1
        connector = "└── " if is_last else "├── "
        prefix = f"{connector}{name}"
        padding = max(1, max_prefix_len - len(prefix) + 4)
        line = f"{prefix}{' ' * padding}{comment}" if comment else prefix
        result.append(line)

    result.extend(lines[tree_end:])

    return result


# =============================================================================
# RENAME — Переименование зеркала
# =============================================================================

def cmd_rename(repo_root: Path, old_path: str, new_path: str, dry_run: bool = False) -> bool:
    """Переименовать зеркало .instructions."""
    old_full, old_root, old_subpath, old_depth = parse_folder_path(old_path)
    new_full, new_root, new_subpath, new_depth = parse_folder_path(new_path)

    # Проверяем, что корневая папка та же
    if old_root != new_root:
        print(f"❌ Переименование между разными корнями — используйте 'move'", file=sys.stderr)
        return False

    # Пути к зеркалам
    old_instructions = get_instructions_path(repo_root, old_path)
    new_instructions = get_instructions_path(repo_root, new_path)

    if not old_instructions.exists():
        print(f"⚠️  Старое зеркало не существует: {old_instructions}", file=sys.stderr)
        # Создаём новое
        return cmd_create(repo_root, new_path, dry_run)

    if new_instructions.exists():
        print(f"❌ Новое зеркало уже существует: {new_instructions}", file=sys.stderr)
        return False

    if dry_run:
        print(f"=== DRY RUN ===")
        print(f"Переименование: {old_instructions} -> {new_instructions}")
        return True

    # Переименовываем
    new_instructions.parent.mkdir(parents=True, exist_ok=True)
    old_instructions.rename(new_instructions)

    # Обновляем README внутри
    readme_path = new_instructions / "README.md"
    if readme_path.exists():
        content = generate_readme_content(new_path, repo_root)
        readme_path.write_text(content, encoding="utf-8")

    print(f"✅ Зеркало переименовано: {old_instructions.relative_to(repo_root)} -> {new_instructions.relative_to(repo_root)}")
    return True


# =============================================================================
# MOVE — Перемещение зеркала
# =============================================================================

def cmd_move(repo_root: Path, old_path: str, new_path: str, dry_run: bool = False) -> bool:
    """Переместить зеркало .instructions между корневыми папками."""
    old_full, old_root, old_subpath, old_depth = parse_folder_path(old_path)
    new_full, new_root, new_subpath, new_depth = parse_folder_path(new_path)

    # Пути к зеркалам
    old_instructions = get_instructions_path(repo_root, old_path)
    new_instructions = get_instructions_path(repo_root, new_path)

    if not old_instructions.exists():
        print(f"⚠️  Старое зеркало не существует: {old_instructions}", file=sys.stderr)
        # Создаём новое
        return cmd_create(repo_root, new_path, dry_run)

    if new_instructions.exists():
        print(f"❌ Новое зеркало уже существует: {new_instructions}", file=sys.stderr)
        return False

    if dry_run:
        print(f"=== DRY RUN ===")
        print(f"Перемещение: {old_instructions} -> {new_instructions}")
        return True

    # Перемещаем
    new_instructions.parent.mkdir(parents=True, exist_ok=True)

    # Используем shutil для перемещения между разными директориями
    import shutil
    shutil.move(str(old_instructions), str(new_instructions))

    # Обновляем README внутри
    readme_path = new_instructions / "README.md"
    if readme_path.exists():
        content = generate_readme_content(new_path, repo_root)
        readme_path.write_text(content, encoding="utf-8")

    print(f"✅ Зеркало перемещено: {old_instructions.relative_to(repo_root)} -> {new_instructions.relative_to(repo_root)}")
    return True


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Зеркалирование структуры в .instructions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python mirror-instructions.py create docs
  python mirror-instructions.py create docs/api
  python mirror-instructions.py rename docs/api docs/endpoints
  python mirror-instructions.py move src/utils shared/utils
"""
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # === CREATE ===
    create_parser = subparsers.add_parser("create", help="Создать зеркало .instructions")
    create_parser.add_argument("folder", help="Путь к папке")
    create_parser.add_argument("--repo", default=".", help="Корень репозитория")
    create_parser.add_argument("--dry-run", action="store_true", help="Показать без создания")

    # === RENAME ===
    rename_parser = subparsers.add_parser("rename", help="Переименовать зеркало")
    rename_parser.add_argument("old_path", help="Старый путь папки")
    rename_parser.add_argument("new_path", help="Новый путь папки")
    rename_parser.add_argument("--repo", default=".", help="Корень репозитория")
    rename_parser.add_argument("--dry-run", action="store_true", help="Показать без изменения")

    # === MOVE ===
    move_parser = subparsers.add_parser("move", help="Переместить зеркало")
    move_parser.add_argument("old_path", help="Старый путь папки")
    move_parser.add_argument("new_path", help="Новый путь папки")
    move_parser.add_argument("--repo", default=".", help="Корень репозитория")
    move_parser.add_argument("--dry-run", action="store_true", help="Показать без изменения")

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    if args.command == "create":
        success = cmd_create(repo_root, args.folder.strip("/"), args.dry_run)
    elif args.command == "rename":
        success = cmd_rename(repo_root, args.old_path.strip("/"), args.new_path.strip("/"), args.dry_run)
    elif args.command == "move":
        success = cmd_move(repo_root, args.old_path.strip("/"), args.new_path.strip("/"), args.dry_run)
    else:
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
