#!/usr/bin/env python3
"""
ssot.py — Управление SSOT структуры проекта.

Подкоманды:
    add     Добавить папку в SSOT
    rename  Переименовать папку в SSOT
    delete  Удалить папку из SSOT

Использование:
    python ssot.py add <папка> --description "Описание"
    python ssot.py rename <старое_имя> <новое_имя> --description "Описание"
    python ssot.py delete <папка>

Примеры:
    python ssot.py add docs --description "Документация проекта"
    python ssot.py rename utils helpers --description "Хелперы"
    python ssot.py delete legacy

Вывод: изменённый /.structure/README.md
"""

import argparse
import re
import sys
from pathlib import Path


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


def get_folder_name(folder_path: str) -> str:
    """Получить имя папки из пути."""
    return folder_path.strip("/").split("/")[-1]


def sort_key(name: str) -> tuple:
    """Ключ сортировки: папки с точкой первыми, затем алфавитно."""
    starts_with_dot = name.startswith(".")
    clean_name = name.lstrip(".")
    return (not starts_with_dot, clean_name.lower())


def extract_folder_from_toc(line: str) -> str:
    """Извлечь имя папки из строки оглавления."""
    match = re.search(r'\[(\.?[^/]+)/\]', line)
    return match.group(1) if match else ""


def extract_folder_from_section(line: str) -> str:
    """Извлечь имя папки из заголовка секции."""
    match = re.search(r'\[(\.?[^/]+)/\]', line)
    return match.group(1) if match else ""


def extract_folder_from_tree(line: str) -> str:
    """Извлечь имя папки из строки дерева."""
    match = re.search(r'[├└]── (\.?[^/\s]+)/', line)
    return match.group(1) if match else ""


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

def add_to_toc(lines: list, folder_name: str) -> list:
    """Добавить папку в оглавление."""
    toc_start, toc_end = find_toc_range(lines)
    if not toc_start or not toc_end:
        return lines

    toc_line = f"  - [{folder_name}/](#-{folder_name})"
    exists = any(f"[{folder_name}/]" in lines[i] for i in range(toc_start, toc_end))
    if exists:
        return lines

    inserted = False
    new_lines = lines[:toc_start]
    for i in range(toc_start, toc_end):
        existing_folder = extract_folder_from_toc(lines[i])
        if existing_folder and not inserted:
            if sort_key(folder_name) < sort_key(existing_folder):
                new_lines.append(toc_line)
                inserted = True
        new_lines.append(lines[i])
    if not inserted:
        new_lines.append(toc_line)
    new_lines.extend(lines[toc_end:])
    return new_lines


def add_to_sections(lines: list, folder_name: str, description: str) -> list:
    """Добавить секцию папки."""
    sections_start, sections_end = find_sections_range(lines)
    if not sections_start or not sections_end:
        return lines

    exists = any(f"[{folder_name}/]" in lines[i] for i in range(sections_start, sections_end))
    if exists:
        return lines

    new_section = f"""### 🔗 [{folder_name}/](../{folder_name}/README.md)

**{description}.**

{{EXTENDED_DESCRIPTION}}"""

    inserted = False
    new_lines = lines[:sections_start]
    i = sections_start
    while i < sections_end:
        line = lines[i]
        if line.startswith("### 🔗"):
            existing_folder = extract_folder_from_section(line)
            if existing_folder and not inserted:
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


def add_to_tree(lines: list, folder_name: str, description: str) -> list:
    """Добавить папку в дерево."""
    tree_start, tree_end = find_tree_range(lines)
    if not tree_start or not tree_end:
        return lines

    # Проверяем корневую папку
    exists = any(
        re.match(rf'^├── {re.escape(folder_name)}/', lines[i])
        for i in range(tree_start, tree_end)
    )
    if exists:
        return lines

    tree_line = f"├── {folder_name}/                             # {description}"

    # Находим корневые папки
    root_folders = []
    for i in range(tree_start, tree_end):
        line = lines[i]
        match = re.match(r'^├── (\.[a-zA-Z]|[a-zA-Z])[^/]*/\s', line)
        if match:
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
            new_lines.append("│")
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
                    final_lines.append("│")
                    file_section_started = True
            final_lines.append(line)
        if not file_section_started:
            final_lines.append(tree_line)
        new_lines = final_lines

    return lines[:tree_start] + new_lines + lines[tree_end:]


def cmd_add(ssot_path: Path, folder_name: str, description: str) -> str:
    """Добавить папку в SSOT."""
    content = ssot_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    lines = add_to_toc(lines, folder_name)
    lines = add_to_sections(lines, folder_name, description)
    lines = add_to_tree(lines, folder_name, description)

    return "\n".join(lines)


# =============================================================================
# RENAME — Переименование папки
# =============================================================================

def rename_in_toc(lines: list, old_name: str, new_name: str) -> list:
    """Переименовать папку в оглавлении."""
    toc_start, toc_end = find_toc_range(lines)
    if not toc_start or not toc_end:
        return lines

    # Удаляем старую запись
    new_lines = lines[:toc_start]
    for i in range(toc_start, toc_end):
        if f"[{old_name}/]" not in lines[i]:
            new_lines.append(lines[i])
    new_lines.extend(lines[toc_end:])

    # Добавляем новую
    return add_to_toc(new_lines, new_name)


def rename_in_sections(lines: list, old_name: str, new_name: str, description: str) -> list:
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
            if f"[{old_name}/]" in line:
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
    return add_to_sections(new_lines, new_name, description)


def rename_in_tree(lines: list, old_name: str, new_name: str, description: str) -> list:
    """Переименовать папку в дереве."""
    tree_start, tree_end = find_tree_range(lines)
    if not tree_start or not tree_end:
        return lines

    # Удаляем старую запись (только корневую папку, без подпапок)
    new_lines = lines[:tree_start]
    i = tree_start
    while i < tree_end:
        line = lines[i]
        # Пропускаем корневую папку old_name
        if re.match(rf'^├── {re.escape(old_name)}/', line):
            i += 1
            # Пропускаем пустую строку после
            if i < tree_end and lines[i] == "│":
                i += 1
            continue
        new_lines.append(line)
        i += 1

    new_lines.extend(lines[tree_end:])

    # Добавляем новую
    return add_to_tree(new_lines, new_name, description)


def cmd_rename(ssot_path: Path, old_name: str, new_name: str, description: str) -> str:
    """Переименовать папку в SSOT."""
    content = ssot_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    lines = rename_in_toc(lines, old_name, new_name)
    lines = rename_in_sections(lines, old_name, new_name, description)
    lines = rename_in_tree(lines, old_name, new_name, description)

    return "\n".join(lines)


# =============================================================================
# DELETE — Удаление папки
# =============================================================================

def delete_from_toc(lines: list, folder_name: str) -> list:
    """Удалить папку из оглавления."""
    toc_start, toc_end = find_toc_range(lines)
    if not toc_start or not toc_end:
        return lines

    new_lines = lines[:toc_start]
    for i in range(toc_start, toc_end):
        if f"[{folder_name}/]" not in lines[i]:
            new_lines.append(lines[i])
    new_lines.extend(lines[toc_end:])
    return new_lines


def delete_from_sections(lines: list, folder_name: str) -> list:
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
            if f"[{folder_name}/]" in line:
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


def delete_from_tree(lines: list, folder_name: str) -> list:
    """Удалить папку из дерева."""
    tree_start, tree_end = find_tree_range(lines)
    if not tree_start or not tree_end:
        return lines

    new_lines = lines[:tree_start]
    i = tree_start
    while i < tree_end:
        line = lines[i]
        # Пропускаем корневую папку
        if re.match(rf'^├── {re.escape(folder_name)}/', line):
            i += 1
            # Пропускаем пустую строку после
            if i < tree_end and lines[i] == "│":
                i += 1
            continue
        new_lines.append(line)
        i += 1

    new_lines.extend(lines[tree_end:])
    return new_lines


def cmd_delete(ssot_path: Path, folder_name: str) -> str:
    """Удалить папку из SSOT."""
    content = ssot_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    lines = delete_from_toc(lines, folder_name)
    lines = delete_from_sections(lines, folder_name)
    lines = delete_from_tree(lines, folder_name)

    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Управление SSOT структуры проекта",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python ssot.py add docs --description "Документация проекта"
  python ssot.py rename utils helpers --description "Хелперы"
  python ssot.py delete legacy
"""
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # === ADD ===
    add_parser = subparsers.add_parser("add", help="Добавить папку в SSOT")
    add_parser.add_argument("folder", help="Имя папки")
    add_parser.add_argument("--description", "-d", required=True, help="Описание папки")
    add_parser.add_argument("--repo", default=".", help="Корень репозитория")
    add_parser.add_argument("--dry-run", action="store_true", help="Показать без записи")

    # === RENAME ===
    rename_parser = subparsers.add_parser("rename", help="Переименовать папку в SSOT")
    rename_parser.add_argument("old_name", help="Старое имя папки")
    rename_parser.add_argument("new_name", help="Новое имя папки")
    rename_parser.add_argument("--description", "-d", required=True, help="Описание папки")
    rename_parser.add_argument("--repo", default=".", help="Корень репозитория")
    rename_parser.add_argument("--dry-run", action="store_true", help="Показать без записи")

    # === DELETE ===
    delete_parser = subparsers.add_parser("delete", help="Удалить папку из SSOT")
    delete_parser.add_argument("folder", help="Имя папки")
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
        folder_name = get_folder_name(args.folder)
        folder_path = repo_root / folder_name
        if not folder_path.exists():
            print(f"⚠️  Папка не существует: {folder_path}", file=sys.stderr)

        result = cmd_add(ssot_path, folder_name, args.description)
        msg_action = f"Добавлена папка: {folder_name}/"
        msg_extra = "\n⚠️  Замените {EXTENDED_DESCRIPTION} в секции папки!"

    elif args.command == "rename":
        old_name = get_folder_name(args.old_name)
        new_name = get_folder_name(args.new_name)
        result = cmd_rename(ssot_path, old_name, new_name, args.description)
        msg_action = f"Переименована папка: {old_name}/ → {new_name}/"
        msg_extra = "\n⚠️  Обновите ссылки в других файлах!"

    elif args.command == "delete":
        folder_name = get_folder_name(args.folder)
        result = cmd_delete(ssot_path, folder_name)
        msg_action = f"Удалена папка: {folder_name}/"
        msg_extra = "\n⚠️  Удалите папку и обновите ссылки в других файлах!"

    # Вывод
    if args.dry_run:
        print("=== DRY RUN ===")
        print(result)
    else:
        ssot_path.write_text(result, encoding="utf-8")
        print(f"✅ SSOT обновлён: {ssot_path}")
        print(f"   {msg_action}")
        print(msg_extra)


if __name__ == "__main__":
    main()
