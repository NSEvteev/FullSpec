#!/usr/bin/env python3
"""
instruction-readme-update.py — Обновление README.md инструкций.

Использование:
    python instruction-readme-update.py <путь> <описание> [--type standard|project] [--dry-run]

Примеры:
    # Добавить новую инструкцию
    python instruction-readme-update.py specs/statuses.md "Система статусов документов" --type standard

    # Предпросмотр
    python instruction-readme-update.py specs/workflow.md "Workflow документов" --dry-run

    # Отметить как заполненную
    python instruction-readme-update.py specs/statuses.md --filled

Функции:
    - Добавляет новый раздел если папка новая
    - Добавляет строку в таблицу существующего раздела
    - Обновляет статус (✅/⬜) для существующей инструкции
    - Обновляет счётчик в заголовке

Возвращает:
    0 — успех
    1 — ошибка
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


def parse_table_row(line: str) -> dict | None:
    """Парсить строку таблицы markdown."""
    # | [file.md](./path) | Description | type | ✅ | ✅ |
    pattern = r'\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|'
    match = re.match(pattern, line)
    if match:
        return {
            "name": match.group(1),
            "link": match.group(2),
            "description": match.group(3).strip(),
            "type": match.group(4).strip(),
            "created": match.group(5).strip(),
            "filled": match.group(6).strip(),
        }
    return None


def format_table_row(
    file_name: str,
    path: str,
    description: str,
    type_: str,
    created: str = "✅",
    filled: str = "✅"
) -> str:
    """Форматировать строку таблицы."""
    return f"| [{file_name}]({path}) | {description} | {type_} | {created} | {filled} |"


def find_section_for_folder(content: str, folder: str) -> tuple[int, int] | None:
    """
    Найти секцию для папки в README.md.

    Возвращает (start_line, end_line) или None если не найдено.
    """
    lines = content.split("\n")

    # Ищем заголовок секции (## /folder/ или ## /folder — ...)
    section_pattern = re.compile(rf'^##\s+/{folder}/?\s*[—-]', re.IGNORECASE)
    alt_pattern = re.compile(rf'^##\s+.*/{folder}/', re.IGNORECASE)

    start_line = None
    end_line = None

    for i, line in enumerate(lines):
        if section_pattern.match(line) or alt_pattern.match(line):
            start_line = i
            continue

        # Если нашли начало, ищем конец (следующий ## или конец файла)
        if start_line is not None and line.startswith("## "):
            end_line = i
            break

    if start_line is not None and end_line is None:
        end_line = len(lines)

    if start_line is not None:
        return (start_line, end_line)

    return None


def find_table_in_section(lines: list[str], start: int, end: int) -> tuple[int, int] | None:
    """
    Найти таблицу в секции.

    Возвращает (table_start, table_end).
    """
    table_start = None
    table_end = None

    for i in range(start, end):
        line = lines[i]

        # Начало таблицы — строка с | Инструкция | или |---
        if table_start is None:
            if line.strip().startswith("|") and ("Инструкция" in line or "---" in line):
                # Ищем заголовок таблицы (строка перед ---)
                if "---" in line and i > 0:
                    table_start = i - 1
                else:
                    table_start = i
                continue

        # Конец таблицы — пустая строка или не-таблица
        if table_start is not None:
            if not line.strip().startswith("|"):
                table_end = i
                break

    if table_start is not None and table_end is None:
        table_end = end

    if table_start is not None:
        return (table_start, table_end)

    return None


def create_new_section(folder: str, instructions: list[dict]) -> str:
    """Создать новую секцию для папки."""
    # Определяем название секции
    folder_names = {
        "specs": "Правила спецификаций",
        "src": "Правила разработки сервисов",
        "doc": "Правила документации",
        "git": "Правила Git",
        "platform": "Правила инфраструктуры",
        "shared": "Правила общего кода",
        "config": "Правила конфигураций",
        "tests": "Правила тестирования",
        "tools": "Правила инструментов",
    }

    section_name = folder_names.get(folder, f"Правила {folder}")

    lines = [
        f"## /{folder}/ — {section_name}",
        "",
        "| Инструкция | Описание | Тип | Создано | Заполнено |",
        "|------------|----------|-----|:-------:|:---------:|",
    ]

    for instr in instructions:
        lines.append(format_table_row(
            instr["file_name"],
            instr["path"],
            instr["description"],
            instr["type"],
            instr.get("created", "✅"),
            instr.get("filled", "✅"),
        ))

    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def update_readme(
    readme_path: Path,
    instruction_path: str,
    description: str,
    type_: str = "standard",
    mark_filled: bool = False,
    dry_run: bool = False
) -> dict:
    """
    Обновить README.md.

    Возвращает dict с результатом операции.
    """
    result = {
        "success": True,
        "action": "",  # "added", "updated", "section_created"
        "changes": [],
        "errors": [],
    }

    if not readme_path.exists():
        result["success"] = False
        result["errors"].append(f"README.md не найден: {readme_path}")
        return result

    content = readme_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Извлекаем папку и имя файла
    path_parts = instruction_path.replace("\\", "/").strip("/").split("/")
    folder = path_parts[0]
    file_name = path_parts[-1]
    relative_path = f"./{instruction_path}"

    # Ищем секцию для папки
    section_range = find_section_for_folder(content, folder)

    if section_range is None:
        # Нужно создать новую секцию
        new_section = create_new_section(folder, [{
            "file_name": file_name,
            "path": relative_path,
            "description": description,
            "type": type_,
            "created": "✅",
            "filled": "✅" if mark_filled else "✅",
        }])

        # Вставляем перед последним ---
        insert_pos = len(lines) - 1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == "---":
                insert_pos = i
                break

        new_lines = lines[:insert_pos] + new_section.split("\n") + lines[insert_pos:]

        result["action"] = "section_created"
        result["changes"].append(f"Создана новая секция /{folder}/")
        result["changes"].append(f"Добавлена инструкция {file_name}")

    else:
        start, end = section_range
        table_range = find_table_in_section(lines, start, end)

        if table_range is None:
            result["success"] = False
            result["errors"].append(f"Таблица не найдена в секции /{folder}/")
            return result

        table_start, table_end = table_range

        # Проверяем, есть ли уже эта инструкция в таблице
        existing_row = None
        existing_row_idx = None

        for i in range(table_start + 2, table_end):  # +2 чтобы пропустить заголовок и ---
            row = parse_table_row(lines[i])
            if row and (row["name"] == file_name or file_name in row["link"]):
                existing_row = row
                existing_row_idx = i
                break

        if existing_row:
            # Обновляем существующую строку
            new_row = format_table_row(
                file_name,
                relative_path,
                description or existing_row["description"],
                type_ or existing_row["type"],
                "✅",
                "✅" if mark_filled else existing_row["filled"],
            )
            lines[existing_row_idx] = new_row
            result["action"] = "updated"
            result["changes"].append(f"Обновлена инструкция {file_name}")
        else:
            # Добавляем новую строку в конец таблицы
            new_row = format_table_row(
                file_name,
                relative_path,
                description,
                type_,
                "✅",
                "✅" if mark_filled else "✅",
            )
            lines.insert(table_end, new_row)
            result["action"] = "added"
            result["changes"].append(f"Добавлена инструкция {file_name}")

        new_lines = lines

    # Обновляем счётчик в заголовке
    new_content = "\n".join(new_lines)
    new_content = update_stats_counter(new_content)

    if not dry_run:
        readme_path.write_text(new_content, encoding="utf-8")

    return result


def update_stats_counter(content: str) -> str:
    """Обновить счётчик статистики в README."""
    # Считаем ✅ в таблицах
    created_count = content.count("| ✅ |")
    # Это грубая оценка, но работает для простых случаев

    # Паттерн: Создано **X из Y** инструкций
    pattern = r'Создано \*\*\d+ из \d+\*\* инструкций'

    # Считаем общее количество строк таблиц с инструкциями
    total_count = len(re.findall(r'\| \[[^\]]+\.md\]', content))

    replacement = f'Создано **{total_count} из {total_count}** инструкций'
    content = re.sub(pattern, replacement, content)

    return content


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Обновление README.md инструкций."
    )
    parser.add_argument(
        "path",
        help="Путь к инструкции (относительно .claude/.instructions/)"
    )
    parser.add_argument(
        "description",
        nargs="?",
        default="",
        help="Описание инструкции"
    )
    parser.add_argument(
        "--type",
        choices=["standard", "project"],
        default="standard",
        help="Тип инструкции"
    )
    parser.add_argument(
        "--filled",
        action="store_true",
        help="Отметить как заполненную"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать изменения без применения"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    readme_path = repo_root / ".claude" / "instructions" / "README.md"

    result = update_readme(
        readme_path,
        args.path,
        args.description,
        args.type,
        args.filled,
        args.dry_run,
    )

    if result["success"]:
        action_msg = {
            "added": "добавлена",
            "updated": "обновлена",
            "section_created": "создана секция",
        }.get(result["action"], result["action"])

        if args.dry_run:
            print(f"📋 Предпросмотр (--dry-run)")
        else:
            print(f"✅ README.md обновлён")

        print(f"   Действие: {action_msg}")
        for change in result["changes"]:
            print(f"   - {change}")

        if args.dry_run:
            print()
            print("ℹ️  Изменения НЕ применены (--dry-run)")

        sys.exit(0)
    else:
        print(f"❌ Ошибка обновления README.md")
        for error in result["errors"]:
            print(f"   {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
