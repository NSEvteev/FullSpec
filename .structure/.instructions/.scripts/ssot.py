#!/usr/bin/env python3
"""
ssot.py — Управление SSOT структуры проекта.

Подкоманды:
    add     Добавить папку в SSOT
    rename  Переименовать папку в SSOT
    delete  Удалить папку из SSOT

Использование:
    python ssot.py add <папка> --description "Описание"
    python ssot.py add <родитель/папка> --description "Описание"
    python ssot.py rename <старое_имя> <новое_имя> --description "Описание"
    python ssot.py delete <папка>

Примеры:
    python ssot.py add docs --description "Документация проекта"
    python ssot.py add test/subtest --description "Тестовая подпапка"
    python ssot.py rename utils helpers --description "Хелперы"
    python ssot.py delete legacy

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

COMMENT_COLUMN = 41  # Позиция начала комментария в дереве
SUBCOMMENT_PREFIX = "  "  # Отступ для комментариев подпапок


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
        (full_path, parent_path, folder_name, depth)

    Примеры:
        "test" -> ("test", None, "test", 0)
        "test/subtest" -> ("test/subtest", "test", "subtest", 1)
        "test/sub/deep" -> ("test/sub/deep", "test/sub", "deep", 2)
    """
    parts = folder_path.strip("/").split("/")
    full_path = "/".join(parts)
    folder_name = parts[-1]
    depth = len(parts) - 1
    parent_path = "/".join(parts[:-1]) if depth > 0 else None
    return full_path, parent_path, folder_name, depth


def sort_key(name: str) -> tuple:
    """Ключ сортировки: папки с точкой первыми, затем алфавитно."""
    starts_with_dot = name.startswith(".")
    clean_name = name.lstrip(".")
    return (not starts_with_dot, clean_name.lower())


def format_tree_line(folder_name: str, description: str, depth: int = 0, is_last: bool = False) -> str:
    """
    Форматировать строку дерева с выровненным комментарием.

    Args:
        folder_name: Имя папки
        description: Описание
        depth: Глубина вложенности (0 = корневая)
        is_last: Последний элемент на уровне (└── вместо ├──)
    """
    indent = "│   " * depth
    connector = "└── " if is_last else "├── "
    prefix = f"{indent}{connector}{folder_name}/"

    # Отступ комментария для подпапок
    comment_prefix = "#" + SUBCOMMENT_PREFIX * depth if depth > 0 else "#"

    padding = max(1, COMMENT_COLUMN - len(prefix))
    return f"{prefix}{' ' * padding}{comment_prefix} {description}"


# =============================================================================
# Исправление коннекторов дерева
# =============================================================================

def fix_tree_connectors(tree_lines: list) -> list:
    """
    Исправить коннекторы в дереве (├── vs └──) и разделители (│).

    Правила:
    - Последняя папка на каждом уровне использует └──
    - Остальные папки используют ├──
    - │ ставится между папками одного уровня (не после последней)
    """
    if not tree_lines:
        return tree_lines

    # Парсим дерево в структуру
    entries = []  # [(line_idx, depth, folder_name, comment, is_folder)]

    for i, line in enumerate(tree_lines):
        # Пропускаем разделители │
        if line.strip() == "│" or line == "│":
            continue

        # Определяем глубину
        depth = 0
        pos = 0
        while line[pos:pos+4] == "│   ":
            depth += 1
            pos += 4

        # Ищем папку или файл
        match = re.match(r'^(│   )*[├└]── ([^/\s]+)(/)?(.*)$', line)
        if match:
            name = match.group(2)
            is_folder = match.group(3) == "/"
            rest = match.group(4) or ""
            entries.append({
                'idx': i,
                'depth': depth,
                'name': name,
                'is_folder': is_folder,
                'rest': rest,
                'line': line
            })

    if not entries:
        return tree_lines

    # Группируем по глубине и определяем последние элементы
    # Для каждой глубины находим последний элемент
    result = []

    # Определяем, какие элементы последние на своём уровне
    # Элемент последний если после него нет элементов той же глубины
    # (пока не встретится элемент меньшей глубины)

    for i, entry in enumerate(entries):
        is_last = True
        # Проверяем, есть ли после этого элемента другие элементы той же глубины
        for j in range(i + 1, len(entries)):
            if entries[j]['depth'] < entry['depth']:
                # Вышли из родителя — этот элемент последний
                break
            if entries[j]['depth'] == entry['depth']:
                # Есть ещё элемент на том же уровне — не последний
                is_last = False
                break
        entry['is_last'] = is_last

    # Собираем новое дерево
    for i, entry in enumerate(entries):
        depth = entry['depth']
        name = entry['name']
        is_folder = entry['is_folder']
        is_last = entry['is_last']
        rest = entry['rest']

        # Формируем строку
        indent = "│   " * depth
        connector = "└── " if is_last else "├── "
        suffix = "/" if is_folder else ""

        new_line = f"{indent}{connector}{name}{suffix}{rest}"
        result.append(new_line)

        # Добавляем │ ПОСЛЕ последнего ребёнка корневой папки (перед следующей корневой)
        # Проверяем: текущий элемент — последний ребёнок (любой глубины) перед следующей корневой папкой?
        if depth > 0 and i + 1 < len(entries):
            next_entry = entries[i + 1]
            # Следующий элемент на корневом уровне — добавляем разделитель
            if next_entry['depth'] == 0:
                result.append("│")
        # Корневая папка без детей перед следующей корневой
        elif depth == 0 and is_folder and not is_last:
            # Проверяем, есть ли дети у этой папки
            has_children = False
            if i + 1 < len(entries) and entries[i + 1]['depth'] > 0:
                has_children = True
            if not has_children:
                result.append("│")

    return result


# =============================================================================
# Функции поиска диапазонов
# =============================================================================

def extract_folder_from_toc(line: str) -> str:
    """Извлечь путь папки из строки оглавления."""
    match = re.search(r'\[([^\]]+)/\]', line)
    return match.group(1) if match else ""


def extract_folder_from_section(line: str) -> str:
    """Извлечь путь папки из заголовка секции."""
    match = re.search(r'\[([^\]]+)/\]', line)
    return match.group(1) if match else ""


def extract_folder_from_tree(line: str) -> str:
    """Извлечь имя папки из строки дерева (только имя, не путь)."""
    match = re.search(r'[├└]── ([^/\s]+)/', line)
    return match.group(1) if match else ""


def get_tree_line_depth(line: str) -> int:
    """Получить глубину строки в дереве."""
    # Считаем количество "│   " в начале
    depth = 0
    pos = 0
    while line[pos:pos+4] == "│   ":
        depth += 1
        pos += 4
    return depth


def find_toc_range(lines: list) -> tuple:
    """Найти диапазон оглавления корневых папок."""
    toc_start = toc_end = None
    for i, line in enumerate(lines):
        if "- [1. Корневые папки]" in line:
            toc_start = i + 1
        if toc_start and "- [2. Корневые файлы]" in line:
            toc_end = i
            break
    return toc_start, toc_end


def find_sections_range(lines: list) -> tuple:
    """Найти диапазон секций корневых папок."""
    sections_start = sections_end = None
    for i, line in enumerate(lines):
        if line.strip() == "## 1. Корневые папки":
            sections_start = i + 1
        if sections_start and line.strip() == "## 2. Корневые файлы":
            sections_end = i - 1
            break
    return sections_start, sections_end


def find_tree_range(lines: list) -> tuple:
    """Найти диапазон дерева."""
    tree_start = tree_end = None
    for i, line in enumerate(lines):
        if "## 3. Дерево" in line:
            for j in range(i, min(i + 5, len(lines))):
                if lines[j].strip() == "```":
                    tree_start = j + 2
                    break
        if tree_start and line.strip() == "```" and i > tree_start:
            tree_end = i
            break
    return tree_start, tree_end


# =============================================================================
# ADD — Добавление папки
# =============================================================================

def add_to_toc(lines: list, full_path: str, parent_path: str, depth: int) -> list:
    """Добавить папку в оглавление. Только для корневых папок (depth=0)."""
    # Оглавление только для корневых папок
    if depth > 0:
        return lines

    toc_start, toc_end = find_toc_range(lines)
    if not toc_start or not toc_end:
        return lines

    folder_name = full_path.split("/")[-1]
    anchor = full_path.replace("/", "")
    indent = "  " * (depth + 1)
    toc_line = f"{indent}- [{full_path}/](#-{anchor})"

    # Проверяем существование
    exists = any(f"[{full_path}/]" in lines[i] for i in range(toc_start, toc_end))
    if exists:
        return lines

    if depth == 0:
        # Корневая папка — сортируем среди корневых
        inserted = False
        new_lines = lines[:toc_start]
        for i in range(toc_start, toc_end):
            line = lines[i]
            # Только корневые записи (2 пробела отступа)
            if line.startswith("  - [") and not line.startswith("    "):
                existing_folder = extract_folder_from_toc(line)
                if existing_folder and not inserted:
                    if sort_key(folder_name) < sort_key(existing_folder):
                        new_lines.append(toc_line)
                        inserted = True
            new_lines.append(line)
        if not inserted:
            new_lines.append(toc_line)
        new_lines.extend(lines[toc_end:])
        return new_lines
    else:
        # Вложенная папка — вставляем после родителя
        new_lines = []
        inserted = False
        for i, line in enumerate(lines):
            new_lines.append(line)
            if not inserted and i >= toc_start and i < toc_end:
                if f"[{parent_path}/]" in line:
                    # Пропускаем существующие дочерние элементы
                    j = i + 1
                    while j < toc_end and lines[j].startswith("    "):
                        j += 1
                    # Вставляем в конец дочерних
                    insert_pos = len(new_lines)
                    # Найти правильную позицию среди siblings
                    siblings = []
                    k = i + 1
                    while k < toc_end and lines[k].startswith("    - ["):
                        sib_folder = extract_folder_from_toc(lines[k])
                        siblings.append((k, sib_folder))
                        k += 1

                    # Сортировка среди siblings
                    inserted_among_siblings = False
                    for sib_idx, (sib_line_idx, sib_name) in enumerate(siblings):
                        if sort_key(folder_name) < sort_key(sib_name.split("/")[-1]):
                            # Вставить перед этим sibling
                            # new_lines уже содержит parent, нужно вставить после
                            pos = len(new_lines) - 1 + sib_idx + 1
                            new_lines.insert(pos, toc_line)
                            inserted_among_siblings = True
                            break

                    if not inserted_among_siblings:
                        # Вставить после всех siblings (или сразу после родителя)
                        new_lines.append(toc_line)

                    inserted = True

        if not inserted:
            # Родитель не найден — добавляем как корневую
            return add_to_toc(lines, full_path, None, 0)

        return new_lines


def add_to_sections(lines: list, full_path: str, parent_path: str, description: str, depth: int) -> list:
    """Добавить секцию папки. Только для корневых папок (depth=0)."""
    # Секции только для корневых папок
    if depth > 0:
        return lines

    sections_start, sections_end = find_sections_range(lines)
    if not sections_start or not sections_end:
        return lines

    # Проверяем существование
    exists = any(f"[{full_path}/]" in lines[i] for i in range(sections_start, sections_end))
    if exists:
        return lines

    new_section = f"""### 🔗 [{full_path}/](../{full_path}/README.md)

**{description}.**

{{EXTENDED_DESCRIPTION}}"""

    if depth == 0:
        # Корневая папка — сортируем среди корневых
        folder_name = full_path
        inserted = False
        new_lines = lines[:sections_start]
        i = sections_start
        while i < sections_end:
            line = lines[i]
            if line.startswith("### 🔗"):
                existing_folder = extract_folder_from_section(line)
                if existing_folder and not inserted:
                    # Сравниваем только корневые (без /)
                    if "/" not in existing_folder:
                        if sort_key(folder_name) < sort_key(existing_folder):
                            new_lines.append(new_section)
                            new_lines.append("")
                            inserted = True
            new_lines.append(line)
            i += 1

        if not inserted:
            new_lines.append("")
            new_lines.append(new_section)

        new_lines.extend(lines[sections_end:])
        return new_lines
    else:
        # Вложенная папка — вставляем после родительской секции
        new_lines = []
        inserted = False
        i = 0
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)

            if not inserted and i >= sections_start and i < sections_end:
                if line.startswith("### 🔗") and f"[{parent_path}/]" in line:
                    # Нашли родительскую секцию, ищем её конец
                    i += 1
                    while i < sections_end and not lines[i].startswith("### 🔗"):
                        new_lines.append(lines[i])
                        i += 1
                    # Вставляем новую секцию
                    new_lines.append("")
                    new_lines.append(new_section)
                    inserted = True
                    continue
            i += 1

        if not inserted:
            # Родитель не найден — добавляем как обычно
            return add_to_sections(lines, full_path, None, description, 0)

        return new_lines


def add_to_tree(lines: list, full_path: str, parent_path: str, description: str, depth: int) -> list:
    """Добавить папку в дерево."""
    tree_start, tree_end = find_tree_range(lines)
    if not tree_start or not tree_end:
        return lines

    folder_name = full_path.split("/")[-1]

    # Проверяем существование (ищем полный путь через контекст)
    # Для простоты проверяем только имя на нужной глубине
    # TODO: более точная проверка

    if depth == 0:
        # Корневая папка
        exists = any(
            re.match(rf'^[├└]── {re.escape(folder_name)}/', lines[i])
            for i in range(tree_start, tree_end)
        )
        if exists:
            return lines

        tree_line = format_tree_line(folder_name, description, depth=0)

        # Находим корневые папки
        root_folders = []
        for i in range(tree_start, tree_end):
            line = lines[i]
            if re.match(r'^├── [^/]+/', line):
                existing_folder = extract_folder_from_tree(line)
                if existing_folder:
                    root_folders.append((i, existing_folder))

        # Находим позицию для вставки
        insert_idx = None
        for idx, existing_folder in root_folders:
            if sort_key(folder_name) < sort_key(existing_folder):
                insert_idx = idx
                break

        # Собираем результат
        new_lines = []
        inserted = False

        for i in range(tree_start, tree_end):
            if insert_idx is not None and i == insert_idx and not inserted:
                new_lines.append(tree_line)
                inserted = True
            new_lines.append(lines[i])

        # Если не вставили — перед файлами
        if not inserted:
            final_lines = []
            file_section_started = False
            for line in new_lines:
                if re.match(r'^[├└]── [^/\s]+$', line.rstrip()):
                    if not file_section_started:
                        final_lines.append(tree_line)
                        file_section_started = True
                final_lines.append(line)
            if not file_section_started:
                final_lines.append(tree_line)
            new_lines = final_lines

        # Исправляем коннекторы
        new_lines = fix_tree_connectors(new_lines)
        return lines[:tree_start] + new_lines + lines[tree_end:]

    else:
        # Вложенная папка — найти родителя и вставить внутрь
        # Нужно найти родителя по полному пути, а не только по имени
        parent_parts = parent_path.split("/") if parent_path else []
        parent_depth = depth - 1

        tree_line = format_tree_line(folder_name, description, depth=depth)

        new_lines = lines[:tree_start]
        inserted = False
        i = tree_start

        # Отслеживаем текущий путь в дереве (стек предков)
        path_stack = []  # [(depth, folder_name), ...]

        while i < tree_end:
            line = lines[i]
            new_lines.append(line)

            if not inserted:
                # Ищем родительскую папку на нужной глубине
                line_depth = get_tree_line_depth(line)
                line_folder = extract_folder_from_tree(line)

                # Обновляем стек пути
                if line_folder:
                    # Убираем из стека папки с глубиной >= текущей
                    while path_stack and path_stack[-1][0] >= line_depth:
                        path_stack.pop()
                    path_stack.append((line_depth, line_folder))

                # Проверяем полный путь до текущей папки
                current_path = [name for _, name in path_stack]
                is_correct_parent = (
                    parent_parts and
                    line_depth == parent_depth and
                    line_folder == parent_parts[-1] and
                    current_path == parent_parts
                )

                if is_correct_parent:
                    # Нашли родителя, ищем место для вставки среди его детей
                    i += 1
                    children = []

                    # Проверяем, есть ли уже эта папка среди детей
                    already_exists = False
                    j = i
                    while j < tree_end:
                        check_line = lines[j]
                        if check_line.strip() == "│" or check_line == "│":
                            j += 1
                            continue
                        check_depth = get_tree_line_depth(check_line)
                        if check_depth <= parent_depth:
                            break
                        if check_depth == depth:
                            check_folder = extract_folder_from_tree(check_line)
                            if check_folder == folder_name:
                                already_exists = True
                                break
                        j += 1

                    if already_exists:
                        # Папка уже существует — пропускаем добавление
                        new_lines.extend(lines[i:])
                        return lines[:tree_start] + new_lines[len(lines[:tree_start]):tree_end - tree_start + len(lines[:tree_start])] + lines[tree_end:]

                    # Собираем детей родителя
                    while i < tree_end:
                        child_line = lines[i]

                        # Пропускаем разделители │
                        if child_line.strip() == "│" or child_line == "│":
                            new_lines.append(child_line)
                            i += 1
                            continue

                        child_depth = get_tree_line_depth(child_line)

                        if child_depth <= parent_depth:
                            # Вышли из родителя
                            break

                        if child_depth == depth:
                            child_folder = extract_folder_from_tree(child_line)
                            if child_folder:
                                children.append((len(new_lines), child_folder, child_line))

                        new_lines.append(child_line)
                        i += 1

                    # Определяем позицию вставки среди children
                    insert_pos = None
                    for pos, (idx, child_name, _) in enumerate(children):
                        if sort_key(folder_name) < sort_key(child_name):
                            insert_pos = children[pos][0]
                            break

                    if insert_pos is not None:
                        new_lines.insert(insert_pos, tree_line)
                    else:
                        # Вставляем в конец детей (перед выходом из родителя)
                        # Найти позицию последнего ребенка или сразу после родителя
                        if children:
                            # После последнего ребенка
                            new_lines.append(tree_line)
                        else:
                            # Сразу после родителя (перед разделителем │)
                            # Проверяем есть ли пустая строка │
                            if new_lines and new_lines[-1].strip() == "│":
                                new_lines.insert(-1, tree_line)
                            else:
                                new_lines.append(tree_line)

                    inserted = True
                    continue

            i += 1

        new_lines.extend(lines[tree_end:])

        if not inserted:
            # Родитель не найден — ошибка
            print(f"⚠️  Родительская папка '{parent_path}' не найдена в дереве", file=sys.stderr)

        # Исправляем коннекторы в дереве
        new_tree_start, new_tree_end = find_tree_range(new_lines)
        if new_tree_start and new_tree_end:
            tree_portion = new_lines[new_tree_start:new_tree_end]
            tree_portion = fix_tree_connectors(tree_portion)
            new_lines = new_lines[:new_tree_start] + tree_portion + new_lines[new_tree_end:]

        return new_lines


def cmd_add(ssot_path: Path, folder_path: str, description: str, repo_root: Path = None) -> str:
    """Добавить папку в SSOT."""
    content = ssot_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    full_path, parent_path, folder_name, depth = parse_folder_path(folder_path)

    lines = add_to_toc(lines, full_path, parent_path, depth)
    lines = add_to_sections(lines, full_path, parent_path, description, depth)
    lines = add_to_tree(lines, full_path, parent_path, description, depth)

    # Автоматически добавляем .instructions/ если существует
    if repo_root:
        # 1. Собственная .instructions/ папки (для корневых папок)
        instructions_path = repo_root / full_path / ".instructions"
        if instructions_path.exists() and instructions_path.is_dir():
            instr_full_path = f"{full_path}/.instructions"
            instr_description = f"Инструкции для {folder_name}/"
            lines = add_to_tree(lines, instr_full_path, full_path, instr_description, depth + 1)

        # 2. Зеркало в родительском .instructions/ (для вложенных папок)
        # test/subtest/ → зеркало test/.instructions/subtest/
        if parent_path:
            # Находим корневую папку (первый элемент пути)
            parts = full_path.split("/")
            root_folder = parts[0]
            # Путь зеркала: root/.instructions/остаток_пути
            mirror_path = repo_root / root_folder / ".instructions" / "/".join(parts[1:])
            if mirror_path.exists() and mirror_path.is_dir():
                # Путь в SSOT: root/.instructions/subpath
                mirror_ssot_path = f"{root_folder}/.instructions/{'/'.join(parts[1:])}"
                # Родитель: root/.instructions или root/.instructions/parent
                if len(parts) == 2:
                    mirror_parent = f"{root_folder}/.instructions"
                else:
                    mirror_parent = f"{root_folder}/.instructions/{'/'.join(parts[1:-1])}"
                mirror_depth = len(parts)  # depth в дереве
                mirror_description = f"Инструкции для {folder_name}/"
                lines = add_to_tree(lines, mirror_ssot_path, mirror_parent, mirror_description, mirror_depth)

    return "\n".join(lines)


# =============================================================================
# Обновление README родительской папки
# =============================================================================

def update_parent_readme(repo_root: Path, folder_path: str, description: str) -> bool:
    """
    Обновить README родительской папки при добавлении подпапки.

    Добавляет:
    - Секцию в "## 1. Папки"
    - Запись в дерево "## 3. Дерево"

    Returns:
        True если обновлено, False если не требуется (корневая папка)
    """
    full_path, parent_path, folder_name, depth = parse_folder_path(folder_path)

    # Корневые папки не имеют родителя для обновления
    if not parent_path:
        return False

    parent_readme = repo_root / parent_path / "README.md"
    if not parent_readme.exists():
        print(f"⚠️  README родителя не найден: {parent_readme}", file=sys.stderr)
        return False

    content = parent_readme.read_text(encoding="utf-8")
    lines = content.split("\n")

    # 1. Добавляем в секцию "Папки"
    lines = add_subfolder_to_folders_section(lines, folder_name, description)

    # 2. Добавляем в дерево
    lines = add_subfolder_to_tree_section(lines, folder_name, description)

    # Записываем
    parent_readme.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Обновлён README родителя: {parent_readme}")
    return True


def add_subfolder_to_folders_section(lines: list, folder_name: str, description: str) -> list:
    """Добавить подпапку в секцию '## 1. Папки'."""
    # Ищем секцию "## 1. Папки" и "---" после неё
    folders_idx = None
    section_end_idx = None

    for i, line in enumerate(lines):
        if "## 1. Папки" in line:
            folders_idx = i
        elif folders_idx is not None and line.strip() == "---":
            section_end_idx = i
            break

    if folders_idx is None:
        return lines

    if section_end_idx is None:
        section_end_idx = len(lines)

    # Проверяем, есть ли уже эта подпапка
    for i in range(folders_idx, section_end_idx):
        if f"[{folder_name}/]" in lines[i]:
            return lines  # Уже есть

    # Формируем новую секцию
    new_section_lines = [
        f"### 🔗 [{folder_name}/](./{folder_name}/README.md)",
        "",
        f"**{description}.**",
        ""
    ]

    # Убираем "*Подпапки отсутствуют.*" если есть и собираем результат
    result = []
    inserted = False

    for i, line in enumerate(lines):
        # Пропускаем placeholder
        if folders_idx < i < section_end_idx:
            if "*Подпапки отсутствуют.*" in line or "*Нет подпапок.*" in line:
                continue

        result.append(line)

        # Вставляем после "## 1. Папки"
        if not inserted and i == folders_idx:
            result.append("")  # Пустая строка после заголовка
            result.extend(new_section_lines)
            inserted = True

    return result


def add_subfolder_to_tree_section(lines: list, folder_name: str, description: str) -> list:
    """Добавить подпапку в секцию '## 3. Дерево'."""
    # Ищем секцию "## 3. Дерево" и блок ```
    tree_start = None
    tree_end = None

    for i, line in enumerate(lines):
        if "## 3. Дерево" in line:
            # Ищем начало блока кода
            for j in range(i, min(i + 5, len(lines))):
                if lines[j].strip() == "```":
                    tree_start = j + 2  # После ``` и строки с путём
                    break
        if tree_start and line.strip() == "```" and i > tree_start:
            tree_end = i
            break

    if not tree_start or not tree_end:
        return lines

    # Проверяем, есть ли уже эта подпапка
    for i in range(tree_start, tree_end):
        if f"── {folder_name}/" in lines[i]:
            return lines  # Уже есть

    # Формируем строку дерева
    tree_line = f"├── {folder_name}/"
    padding = max(1, COMMENT_COLUMN - len(tree_line) - 4)  # -4 для отступа
    tree_line = f"├── {folder_name}/{' ' * padding}# {description}"

    # Ищем место для вставки (перед README.md)
    readme_idx = None
    existing_entries = []

    for i in range(tree_start, tree_end):
        line = lines[i]
        if "── README.md" in line:
            readme_idx = i
        match = re.search(r'[├└]── ([^/\s]+)/', line)
        if match:
            existing_entries.append((i, match.group(1)))

    # Находим позицию для вставки (алфавитный порядок среди папок)
    insert_idx = readme_idx if readme_idx else tree_end
    for idx, existing_name in existing_entries:
        if sort_key(folder_name) < sort_key(existing_name):
            insert_idx = idx
            break

    # Вставляем
    result = lines[:insert_idx]
    result.append(tree_line)
    result.extend(lines[insert_idx:])

    # Исправляем коннекторы (├── vs └──)
    # Находим новый диапазон дерева
    new_tree_start = None
    new_tree_end = None
    for i, line in enumerate(result):
        if "## 3. Дерево" in line:
            for j in range(i, min(i + 5, len(result))):
                if result[j].strip() == "```":
                    new_tree_start = j + 2
                    break
        if new_tree_start and line.strip() == "```" and i > new_tree_start:
            new_tree_end = i
            break

    if new_tree_start and new_tree_end:
        # Последний элемент должен использовать └──
        for i in range(new_tree_start, new_tree_end):
            line = result[i]
            if i == new_tree_end - 1:
                result[i] = line.replace("├── ", "└── ")
            else:
                result[i] = line.replace("└── ", "├── ")

    return result


# =============================================================================
# RENAME — Переименование папки
# =============================================================================

def rename_in_toc(lines: list, old_path: str, new_path: str) -> list:
    """Переименовать папку в оглавлении."""
    toc_start, toc_end = find_toc_range(lines)
    if not toc_start or not toc_end:
        return lines

    old_anchor = old_path.replace("/", "")
    new_anchor = new_path.replace("/", "")
    _, _, new_name, new_depth = parse_folder_path(new_path)

    new_indent = "  " * (new_depth + 1)
    new_toc_line = f"{new_indent}- [{new_path}/](#-{new_anchor})"

    # Удаляем старую запись
    new_lines = lines[:toc_start]
    for i in range(toc_start, toc_end):
        if f"[{old_path}/]" not in lines[i]:
            new_lines.append(lines[i])
    new_lines.extend(lines[toc_end:])

    # Добавляем новую
    _, parent_path, _, depth = parse_folder_path(new_path)
    return add_to_toc(new_lines, new_path, parent_path, depth)


def rename_in_sections(lines: list, old_path: str, new_path: str, description: str) -> list:
    """Переименовать секцию папки."""
    sections_start, sections_end = find_sections_range(lines)
    if not sections_start or not sections_end:
        return lines

    # Находим и удаляем старую секцию
    new_lines = lines[:sections_start]
    i = sections_start
    skip_until_next_section = False

    while i < sections_end:
        line = lines[i]

        if line.startswith("### 🔗"):
            if f"[{old_path}/]" in line:
                # Пропускаем эту секцию
                skip_until_next_section = True
                i += 1
                continue
            else:
                skip_until_next_section = False

        if not skip_until_next_section:
            new_lines.append(line)
        elif line.startswith("### 🔗"):
            skip_until_next_section = False
            new_lines.append(line)

        i += 1

    new_lines.extend(lines[sections_end:])

    # Добавляем новую секцию
    _, parent_path, _, depth = parse_folder_path(new_path)
    return add_to_sections(new_lines, new_path, parent_path, description, depth)


def rename_in_tree(lines: list, old_path: str, new_path: str, description: str) -> list:
    """Переименовать папку в дереве."""
    tree_start, tree_end = find_tree_range(lines)
    if not tree_start or not tree_end:
        return lines

    _, _, old_name, old_depth = parse_folder_path(old_path)
    _, parent_path, new_name, new_depth = parse_folder_path(new_path)

    # Удаляем старую запись и её детей
    new_lines = lines[:tree_start]
    i = tree_start
    skip_children = False
    skip_depth = 0

    while i < tree_end:
        line = lines[i]
        line_depth = get_tree_line_depth(line)
        line_folder = extract_folder_from_tree(line)

        # Если пропускаем детей, проверяем глубину
        if skip_children:
            # Пропускаем разделители │
            if line.strip() == "│" or line == "│":
                i += 1
                continue
            # Если вернулись на уровень родителя или выше — прекращаем пропуск
            if line_depth <= skip_depth:
                skip_children = False
            else:
                # Пропускаем ребёнка
                i += 1
                continue

        # Пропускаем папку на нужной глубине с нужным именем
        if line_depth == old_depth and line_folder == old_name:
            # Начинаем пропускать детей
            skip_children = True
            skip_depth = old_depth
            i += 1
            # Пропускаем пустую строку после (│)
            if i < tree_end and lines[i] == "│":
                i += 1
            continue
        new_lines.append(line)
        i += 1

    new_lines.extend(lines[tree_end:])

    # Добавляем новую
    return add_to_tree(new_lines, new_path, parent_path, description, new_depth)


def cmd_rename(ssot_path: Path, old_path: str, new_path: str, description: str, repo_root: Path = None) -> str:
    """Переименовать папку в SSOT."""
    content = ssot_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    lines = rename_in_toc(lines, old_path, new_path)
    lines = rename_in_sections(lines, old_path, new_path, description)
    lines = rename_in_tree(lines, old_path, new_path, description)

    # Обновляем зеркало .instructions в дереве
    if repo_root:
        _, _, new_name, new_depth = parse_folder_path(new_path)
        _, old_parent, old_name, old_depth = parse_folder_path(old_path)

        # Для вложенных папок: зеркало в родительском .instructions/
        # test/subtest → test/.instructions/subtest
        if old_parent:
            parts = new_path.split("/")
            root_folder = parts[0]

            # Старое зеркало
            old_mirror_ssot = f"{root_folder}/.instructions/{'/'.join(old_path.split('/')[1:])}"
            # Новое зеркало
            new_mirror_ssot = f"{root_folder}/.instructions/{'/'.join(parts[1:])}"

            # Удаляем старое зеркало из дерева
            lines = delete_from_tree(lines, old_mirror_ssot)

            # Проверяем существование нового зеркала
            new_mirror_path = repo_root / root_folder / ".instructions" / "/".join(parts[1:])
            if new_mirror_path.exists() and new_mirror_path.is_dir():
                # Родитель зеркала
                if len(parts) == 2:
                    mirror_parent = f"{root_folder}/.instructions"
                else:
                    mirror_parent = f"{root_folder}/.instructions/{'/'.join(parts[1:-1])}"
                mirror_depth = len(parts)
                mirror_description = f"Инструкции для {new_name}/"
                lines = add_to_tree(lines, new_mirror_ssot, mirror_parent, mirror_description, mirror_depth)

    return "\n".join(lines)


# =============================================================================
# DELETE — Удаление папки
# =============================================================================

def delete_from_toc(lines: list, folder_path: str) -> list:
    """Удалить папку из оглавления."""
    toc_start, toc_end = find_toc_range(lines)
    if not toc_start or not toc_end:
        return lines

    new_lines = lines[:toc_start]
    for i in range(toc_start, toc_end):
        if f"[{folder_path}/]" not in lines[i]:
            new_lines.append(lines[i])
    new_lines.extend(lines[toc_end:])
    return new_lines


def delete_from_sections(lines: list, folder_path: str) -> list:
    """Удалить секцию папки."""
    sections_start, sections_end = find_sections_range(lines)
    if not sections_start or not sections_end:
        return lines

    new_lines = lines[:sections_start]
    i = sections_start
    skip_until_next_section = False
    prev_was_empty = False

    while i < sections_end:
        line = lines[i]

        if line.startswith("### 🔗"):
            if f"[{folder_path}/]" in line:
                skip_until_next_section = True
                i += 1
                continue
            else:
                skip_until_next_section = False

        if not skip_until_next_section:
            # Избегаем двойных пустых строк
            if line == "" and prev_was_empty:
                i += 1
                continue
            new_lines.append(line)
            prev_was_empty = (line == "")
        elif line.startswith("### 🔗"):
            skip_until_next_section = False
            new_lines.append(line)
            prev_was_empty = False

        i += 1

    new_lines.extend(lines[sections_end:])
    return new_lines


def delete_from_tree(lines: list, folder_path: str) -> list:
    """Удалить папку из дерева."""
    tree_start, tree_end = find_tree_range(lines)
    if not tree_start or not tree_end:
        return lines

    _, _, folder_name, depth = parse_folder_path(folder_path)

    new_lines = lines[:tree_start]
    i = tree_start
    skip_children = False
    skip_depth = 0

    while i < tree_end:
        line = lines[i]
        line_depth = get_tree_line_depth(line)
        line_folder = extract_folder_from_tree(line)

        # Если пропускаем детей, проверяем глубину
        if skip_children:
            # Пропускаем разделители │
            if line.strip() == "│" or line == "│":
                i += 1
                continue
            # Если вернулись на уровень родителя или выше — прекращаем пропуск
            if line_depth <= skip_depth:
                skip_children = False
            else:
                # Пропускаем ребёнка
                i += 1
                continue

        # Пропускаем папку на нужной глубине с нужным именем
        if line_depth == depth and line_folder == folder_name:
            # Начинаем пропускать детей
            skip_children = True
            skip_depth = depth
            i += 1
            # Пропускаем пустую строку после (│)
            if i < tree_end and lines[i] == "│":
                i += 1
            continue
        new_lines.append(line)
        i += 1

    new_lines.extend(lines[tree_end:])

    # Исправляем коннекторы в дереве
    new_tree_start, new_tree_end = find_tree_range(new_lines)
    if new_tree_start and new_tree_end:
        tree_portion = new_lines[new_tree_start:new_tree_end]
        tree_portion = fix_tree_connectors(tree_portion)
        new_lines = new_lines[:new_tree_start] + tree_portion + new_lines[new_tree_end:]

    return new_lines


def cmd_delete(ssot_path: Path, folder_path: str, repo_root: Path = None) -> str:
    """Удалить папку из SSOT."""
    content = ssot_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    lines = delete_from_toc(lines, folder_path)
    lines = delete_from_sections(lines, folder_path)
    lines = delete_from_tree(lines, folder_path)

    # Удаляем зеркало .instructions из дерева для вложенных папок
    _, parent_path, folder_name, depth = parse_folder_path(folder_path)
    if parent_path:
        # Для вложенной папки test/demo зеркало: test/.instructions/demo
        parts = folder_path.split("/")
        root_folder = parts[0]
        mirror_ssot_path = f"{root_folder}/.instructions/{'/'.join(parts[1:])}"
        lines = delete_from_tree(lines, mirror_ssot_path)

    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Управление SSOT структуры проекта",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python ssot.py add docs --description "Документация проекта"
  python ssot.py add test/subtest --description "Тестовая подпапка"
  python ssot.py rename utils helpers --description "Хелперы"
  python ssot.py delete legacy
"""
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # === ADD ===
    add_parser = subparsers.add_parser("add", help="Добавить папку в SSOT")
    add_parser.add_argument("folder", help="Путь к папке (например: docs или test/subtest)")
    add_parser.add_argument("--description", "-d", required=True, help="Описание папки")
    add_parser.add_argument("--extended", "-e", help="Расширенное описание (заменяет {EXTENDED_DESCRIPTION})")
    add_parser.add_argument("--repo", default=".", help="Корень репозитория")
    add_parser.add_argument("--dry-run", action="store_true", help="Показать без записи")

    # === RENAME ===
    rename_parser = subparsers.add_parser("rename", help="Переименовать папку в SSOT")
    rename_parser.add_argument("old_path", help="Старый путь папки")
    rename_parser.add_argument("new_path", help="Новый путь папки")
    rename_parser.add_argument("--description", "-d", required=True, help="Описание папки")
    rename_parser.add_argument("--repo", default=".", help="Корень репозитория")
    rename_parser.add_argument("--dry-run", action="store_true", help="Показать без записи")

    # === DELETE ===
    delete_parser = subparsers.add_parser("delete", help="Удалить папку из SSOT")
    delete_parser.add_argument("folder", help="Путь к папке")
    delete_parser.add_argument("--repo", default=".", help="Корень репозитория")
    delete_parser.add_argument("--dry-run", action="store_true", help="Показать без записи")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    ssot_path = repo_root / ".structure" / "README.md"

    if not ssot_path.exists():
        print(f"❌ SSOT не найден: {ssot_path}", file=sys.stderr)
        sys.exit(1)

    # Выполняем команду
    if args.command == "add":
        folder_path = args.folder.strip("/")
        full_path, parent_path, folder_name, depth = parse_folder_path(folder_path)

        # Проверяем существование папки
        check_path = repo_root / full_path
        if not check_path.exists():
            print(f"⚠️  Папка не существует: {check_path}", file=sys.stderr)

        # Для вложенных — проверяем родителя в SSOT
        if parent_path:
            content = ssot_path.read_text(encoding="utf-8")
            if f"[{parent_path}/]" not in content:
                print(f"⚠️  Родительская папка '{parent_path}/' не найдена в SSOT", file=sys.stderr)
                print(f"   Сначала добавьте родителя: python ssot.py add {parent_path} --description \"...\"", file=sys.stderr)

        result = cmd_add(ssot_path, folder_path, args.description, repo_root)

        # Заменяем {EXTENDED_DESCRIPTION} если указан --extended
        if args.extended:
            result = result.replace("{EXTENDED_DESCRIPTION}", args.extended)
            msg_extra = ""
        else:
            msg_extra = "\n⚠️  Замените {EXTENDED_DESCRIPTION} в секции папки!"

        msg_action = f"Добавлена папка: {full_path}/"

    elif args.command == "rename":
        old_path = args.old_path.strip("/")
        new_path = args.new_path.strip("/")
        result = cmd_rename(ssot_path, old_path, new_path, args.description, repo_root)
        msg_action = f"Переименована папка: {old_path}/ → {new_path}/"
        msg_extra = "\n⚠️  Обновите ссылки в других файлах!"

    elif args.command == "delete":
        folder_path = args.folder.strip("/")
        result = cmd_delete(ssot_path, folder_path)
        msg_action = f"Удалена папка: {folder_path}/"
        msg_extra = "\n⚠️  Удалите папку и обновите ссылки в других файлах!"

    # Вывод
    if args.dry_run:
        print("=== DRY RUN ===")
        print(result)
    else:
        ssot_path.write_text(result, encoding="utf-8")
        print(f"✅ SSOT обновлён: {ssot_path}")
        print(f"   {msg_action}")

        # Обновляем README родительской папки (для подпапок)
        if args.command == "add":
            folder_path = args.folder.strip("/")
            _, parent_path, _, _ = parse_folder_path(folder_path)
            if parent_path:
                update_parent_readme(repo_root, folder_path, args.description)

        if msg_extra:
            print(msg_extra)

    sys.exit(0)


if __name__ == "__main__":
    main()
