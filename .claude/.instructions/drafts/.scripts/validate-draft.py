#!/usr/bin/env python3
"""
validate-draft.py — Валидация черновиков по стандарту.

Использование:
    python validate-draft.py <путь к черновику>
    python validate-draft.py --all

Примеры:
    python validate-draft.py ../../drafts/2024-01-23-auth.md
    python validate-draft.py --all

Возвращает:
    0 — успех (все проверки пройдены)
    1 — ошибка валидации
"""

import argparse
import re
import sys
from pathlib import Path

# =============================================================================
# Константы
# =============================================================================

ERROR_CODES = {
    "D001": "Неверный формат имени файла (ожидается YYYY-MM-DD-<topic>.md)",
    "D002": "Неверный формат даты (ожидается YYYY-MM-DD)",
    "D003": "Topic не в kebab-case",
    "D004": "Файл не находится в /.claude/drafts/",
    "D005": "Отсутствует заголовок H1",
    "D006": "Отсутствует оглавление",
    "D007": "Отсутствует секция 'Контекст'",
    "D008": "Отсутствует секция 'Содержание'",
    "D009": "Тип 'План' — отсутствует секция 'Tasklist' с TASK N записями",
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


def add_error(result: dict, code: str, detail: str = "") -> None:
    """Добавить ошибку с кодом из ERROR_CODES."""
    message = ERROR_CODES.get(code, code)
    if detail:
        message = f"{message}: {detail}"
    result["errors"].append(f"{code}: {message}")


# =============================================================================
# Основные функции
# =============================================================================

def validate_filename(file_path: Path, result: dict) -> None:
    """Проверка именования файла."""
    filename = file_path.name

    # Паттерн: YYYY-MM-DD-<topic>.md
    pattern = r'^(\d{4})-(\d{2})-(\d{2})-([a-z0-9-]+)\.md$'
    match = re.match(pattern, filename)

    if not match:
        add_error(result, "D001", filename)
        return

    year, month, day, topic = match.groups()

    # Проверка валидности даты
    try:
        from datetime import datetime
        datetime(int(year), int(month), int(day))
    except ValueError:
        add_error(result, "D002", f"{year}-{month}-{day}")

    # Проверка kebab-case в topic
    if "_" in topic or topic.upper() == topic:
        add_error(result, "D003", topic)


def validate_location(file_path: Path, repo_root: Path, result: dict) -> None:
    """Проверка расположения файла."""
    expected_parent = repo_root / ".claude" / "drafts"

    if file_path.parent != expected_parent:
        add_error(result, "D004", str(file_path.relative_to(repo_root)))


def validate_structure(file_path: Path, result: dict) -> None:
    """Проверка структуры файла."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        result["errors"].append(f"Ошибка чтения файла: {e}")
        return

    lines = content.split("\n")

    # Проверка заголовка H1
    has_h1 = False
    for line in lines[:20]:  # Проверяем первые 20 строк
        if line.startswith("# "):
            has_h1 = True
            break

    if not has_h1:
        add_error(result, "D005")

    # Проверка оглавления
    has_toc = any("## Оглавление" in line or "## оглавление" in line.lower() for line in lines)
    if not has_toc:
        add_error(result, "D006")

    # Проверка секции "Контекст"
    has_context = any("## Контекст" in line or "## контекст" in line.lower() for line in lines)
    if not has_context:
        add_error(result, "D007")

    # Проверка секции "Содержание"
    has_content = any("## Содержание" in line or "## содержание" in line.lower() for line in lines)
    if not has_content:
        add_error(result, "D008")

    # Проверка секции "Tasklist" для типа "План"
    # Определяем тип из frontmatter (type: feature/plan) или по наличию blockedBy/TASK N
    is_plan = False
    for line in lines:
        if re.match(r'^type:\s*(feature|plan)', line):
            is_plan = True
            break

    if is_plan:
        has_tasklist = any("## Tasklist" in line for line in lines)
        has_tasks = any(re.match(r'\s*TASK\s+\d+:', line) for line in lines)
        if not has_tasklist or not has_tasks:
            add_error(result, "D009")


def validate_draft(file_path: Path, repo_root: Path) -> dict:
    """Валидация одного черновика."""
    result = {
        "file": str(file_path.relative_to(repo_root)),
        "errors": [],
        "valid": True
    }

    validate_filename(file_path, result)
    validate_location(file_path, repo_root, result)
    validate_structure(file_path, result)

    result["valid"] = len(result["errors"]) == 0
    return result


def find_all_drafts(repo_root: Path) -> list[Path]:
    """Найти все черновики в /.claude/drafts/."""
    drafts_dir = repo_root / ".claude" / "drafts"

    if not drafts_dir.exists():
        return []

    return [f for f in drafts_dir.glob("*.md") if f.name != "README.md"]


# =============================================================================
# Main
# =============================================================================

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация черновиков по стандарту"
    )
    parser.add_argument("path", nargs="?", help="Путь к черновику")
    parser.add_argument("--all", action="store_true", help="Проверить все черновики")

    args = parser.parse_args()

    if not args.all and not args.path:
        parser.print_help()
        sys.exit(2)

    repo_root = find_repo_root(Path.cwd())

    # Проверка всех черновиков
    if args.all:
        drafts = find_all_drafts(repo_root)

        if not drafts:
            print("Черновики не найдены в /.claude/drafts/")
            sys.exit(0)

        all_valid = True

        for draft in sorted(drafts):
            result = validate_draft(draft, repo_root)

            if result["valid"]:
                print(f"✅ {result['file']}")
            else:
                print(f"❌ {result['file']}")
                for error in result["errors"]:
                    print(f"   {error}")
                all_valid = False

        sys.exit(0 if all_valid else 1)

    # Проверка одного черновика
    file_path = Path(args.path).resolve()

    if not file_path.exists():
        print(f"Файл не найден: {args.path}", file=sys.stderr)
        sys.exit(1)

    result = validate_draft(file_path, repo_root)

    if result["valid"]:
        print(f"✅ {result['file']} — валидация пройдена")
        sys.exit(0)
    else:
        print(f"❌ {result['file']} — обнаружены ошибки:")
        for error in result["errors"]:
            print(f"   {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
