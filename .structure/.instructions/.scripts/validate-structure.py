#!/usr/bin/env python3
"""
validate-structure.py — Валидация согласованности /.structure/README.md.

Использование:
    python validate-structure.py [--repo <корень>] [--json] [--check-instructions]

Примеры:
    python validate-structure.py
    python validate-structure.py --json
    python validate-structure.py --check-instructions
    python validate-structure.py --repo /path/to/project

Проверки:
    T001 — SSOT файл не найден
    T002 — Папка в ФС, но отсутствует в дереве
    T003 — Папка в дереве, но не существует в ФС
    T004 — Комментарий не соответствует описанию в секции
    T005 — Папка без зеркала .instructions

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

ERROR_CODES = {
    "T001": "SSOT файл не найден",
    "T002": "Папка в ФС, но отсутствует в дереве",
    "T003": "Папка в дереве, но не существует в ФС",
    "T004": "Комментарий не соответствует описанию в секции",
    "T005": "Папка без зеркала .instructions",
    "S010": "Подпапка не указана в 'Вложенные области'",
    "S011": "Битая ссылка на README подпапки",
    "S012": "Секция 'Вложенные области' отсутствует при наличии подпапок",
}

# Папки, которые исключаются из проверки
EXCLUDED_FOLDERS = {
    "node_modules",
    ".git",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "venv",
    ".venv",
    "env",
}


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def get_filesystem_folders(repo_root: Path) -> set[str]:
    """Получить список корневых папок из файловой системы."""
    folders = set()
    for item in repo_root.iterdir():
        if item.is_dir() and item.name not in EXCLUDED_FOLDERS:
            folders.add(item.name)
    return folders


def parse_tree_from_readme(readme_path: Path) -> dict[str, str]:
    """
    Парсить дерево папок из README.md.

    Возвращает dict: имя_папки -> комментарий
    """
    if not readme_path.exists():
        return {}

    content = readme_path.read_text(encoding="utf-8")

    # Ищем секцию "Дерево" (может быть "Дерево", "Дерево папок", "3. Дерево")
    tree_match = re.search(
        r"##\s*\d*\.?\s*Дерево.*?```(.*?)```",
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not tree_match:
        return {}

    tree_content = tree_match.group(1)
    folders = {}

    # Паттерн для корневой папки в дереве:
    # ├── .claude/                             # Комментарий
    # Корневые папки — строки без │ в начале (не вложенные)
    pattern = r"^[├└]──\s+([^/\s]+)/\s+#\s*(.*)$"

    for line in tree_content.split("\n"):
        # Пропускаем вложенные папки (начинаются с │)
        stripped = line.lstrip()
        if stripped.startswith("│"):
            continue

        match = re.match(pattern, stripped)
        if match:
            folder_name = match.group(1)
            comment = match.group(2).strip()
            folders[folder_name] = comment

    return folders


def parse_sections_from_readme(readme_path: Path) -> dict[str, str]:
    """
    Парсить описания папок из секций README.md.

    Возвращает dict: имя_папки -> краткое описание
    """
    if not readme_path.exists():
        return {}

    content = readme_path.read_text(encoding="utf-8")
    sections = {}

    # Паттерн для секции папки: ### 🔗 [folder/](path) \n\n **Описание.**
    pattern = r"###\s*🔗\s*\[([^/]+)/\]\([^)]+\)\s*\n\n\*\*([^*]+)\.\*\*"

    for match in re.finditer(pattern, content):
        folder_name = match.group(1)
        description = match.group(2).strip()
        sections[folder_name] = description

    return sections


def validate_structure(repo_root: Path) -> dict:
    """
    Валидировать структуру проекта.

    Возвращает dict с полями:
        valid: bool
        fs_folders: list — папки в файловой системе
        tree_folders: list — папки в дереве
        missing_in_tree: list — папки есть в ФС, но нет в дереве
        missing_in_fs: list — папки есть в дереве, но нет в ФС
        comment_mismatches: list — несоответствия комментариев
        errors: list[str]
        warnings: list[str]
    """
    result = {
        "valid": True,
        "fs_folders": [],
        "tree_folders": [],
        "missing_in_tree": [],
        "missing_in_fs": [],
        "comment_mismatches": [],
        "errors": [],
        "warnings": [],
    }

    structure_readme = repo_root / ".structure" / "README.md"

    # Проверка: файл существует
    if not structure_readme.exists():
        result["errors"].append(f"T001: {ERROR_CODES['T001']}")
        result["valid"] = False
        return result

    # Получаем данные
    fs_folders = get_filesystem_folders(repo_root)
    tree_folders = parse_tree_from_readme(structure_readme)
    section_descriptions = parse_sections_from_readme(structure_readme)

    result["fs_folders"] = sorted(fs_folders)
    result["tree_folders"] = sorted(tree_folders.keys())

    # Проверка 1: папки из ФС есть в дереве
    for folder in fs_folders:
        if folder not in tree_folders:
            result["missing_in_tree"].append(folder)
            result["errors"].append(f"T002: {ERROR_CODES['T002']}: {folder}/")
            result["valid"] = False

    # Проверка 2: папки из дерева есть в ФС
    for folder in tree_folders:
        if folder not in fs_folders:
            result["missing_in_fs"].append(folder)
            result["errors"].append(f"T003: {ERROR_CODES['T003']}: {folder}/")
            result["valid"] = False

    # Проверка 3: комментарии соответствуют секциям
    for folder, tree_comment in tree_folders.items():
        if folder in section_descriptions:
            section_desc = section_descriptions[folder]
            # Сравниваем начало (комментарий может быть сокращённым)
            if not tree_comment.lower().startswith(section_desc.lower()[:20]):
                # Нестрогая проверка — только предупреждение
                result["comment_mismatches"].append({
                    "folder": folder,
                    "tree_comment": tree_comment,
                    "section_description": section_desc,
                })
                result["warnings"].append(f"T004: {ERROR_CODES['T004']}: {folder}/")

    return result


def check_nested_areas(instructions_path: Path) -> list[dict]:
    """
    Проверить секцию 'Вложенные области' в README инструкций.

    Возвращает список ошибок с полями: code, message, path
    """
    errors = []
    readme_path = instructions_path / "README.md"

    if not readme_path.exists():
        return errors

    # Найти подпапки (кроме .scripts)
    subfolders = [
        d for d in instructions_path.iterdir()
        if d.is_dir() and d.name != ".scripts" and not d.name.startswith("DELETE_")
    ]

    if not subfolders:
        return errors  # Нет подпапок — проверка не нужна

    content = readme_path.read_text(encoding="utf-8")

    # Проверить наличие секции "Вложенные области"
    if "## Вложенные области" not in content:
        errors.append({
            "code": "S012",
            "message": f"{ERROR_CODES['S012']}: {readme_path}",
            "path": str(readme_path),
        })
        return errors

    # Проверить что все подпапки указаны
    for subfolder in subfolders:
        folder_name = subfolder.name

        # Проверка: подпапка указана в секции
        if f"[{folder_name}/]" not in content:
            errors.append({
                "code": "S010",
                "message": f"{ERROR_CODES['S010']}: {folder_name}/ в {readme_path}",
                "path": str(readme_path),
            })

        # Проверка: README подпапки существует
        subfolder_readme = subfolder / "README.md"
        if f"[README](./{folder_name}/README.md)" in content and not subfolder_readme.exists():
            errors.append({
                "code": "S011",
                "message": f"{ERROR_CODES['S011']}: {subfolder_readme}",
                "path": str(subfolder_readme),
            })

    return errors


def check_all_nested_areas(repo_root: Path, tree_folders: list[str]) -> dict:
    """
    Проверить секции 'Вложенные области' во всех папках .instructions.

    Возвращает dict с полями:
        nested_errors: list — ошибки вложенных областей
        errors: list[str]
    """
    result = {
        "nested_errors": [],
        "errors": [],
    }

    for folder in tree_folders:
        # Пропускаем .structure
        if folder == ".structure":
            continue

        instructions_path = repo_root / folder / ".instructions"
        if not instructions_path.exists():
            continue

        folder_errors = check_nested_areas(instructions_path)
        result["nested_errors"].extend(folder_errors)

        for err in folder_errors:
            result["errors"].append(f"{err['code']}: {err['message']}")

    return result


def fix_structure_errors(repo_root: Path, missing_in_tree: list[str], missing_in_fs: list[str]) -> dict:
    """
    Автоматически исправить расхождения структуры.

    - T002 (папка в ФС, нет в дереве) → ssot.py add
    - T003 (папка в дереве, нет в ФС) → ssot.py delete

    Возвращает dict с полями:
        fixed: list — исправленные папки
        failed: list — папки с ошибками
    """
    import subprocess

    result = {
        "fixed": [],
        "failed": [],
    }

    scripts_dir = repo_root / ".structure" / ".instructions" / ".scripts"
    ssot_script = scripts_dir / "ssot.py"

    if not ssot_script.exists():
        result["failed"].append(f"ssot.py не найден: {ssot_script}")
        return result

    # T002: добавить папки в SSOT
    for folder in missing_in_tree:
        try:
            cmd = [
                sys.executable,
                str(ssot_script),
                "add",
                folder,
                "--description", "TODO: добавить описание",
                "--repo", str(repo_root),
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            result["fixed"].append(f"T002 fixed: {folder}/ добавлена в SSOT")
        except subprocess.CalledProcessError as e:
            result["failed"].append(f"T002 failed: {folder}/ — {e.stderr}")

    # T003: удалить папки из SSOT
    for folder in missing_in_fs:
        try:
            cmd = [
                sys.executable,
                str(ssot_script),
                "delete",
                folder,
                "--repo", str(repo_root),
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            result["fixed"].append(f"T003 fixed: {folder}/ удалена из SSOT")
        except subprocess.CalledProcessError as e:
            result["failed"].append(f"T003 failed: {folder}/ — {e.stderr}")

    return result


def check_instructions_mirrors(repo_root: Path, tree_folders: list[str]) -> dict:
    """
    Проверить наличие зеркал .instructions для всех папок в SSOT.

    Возвращает dict с полями:
        missing_instructions: list — папки без зеркала .instructions
        errors: list[str]
    """
    result = {
        "missing_instructions": [],
        "errors": [],
    }

    for folder in tree_folders:
        # Пропускаем .structure (сама содержит инструкции)
        if folder == ".structure":
            continue

        # Пропускаем папки с DELETE_
        if folder.startswith("DELETE_"):
            continue

        instructions_path = repo_root / folder / ".instructions"
        instructions_readme = instructions_path / "README.md"

        if not instructions_path.exists():
            result["missing_instructions"].append(folder)
            result["errors"].append(f"T005: {ERROR_CODES['T005']}: {folder}/")
        elif not instructions_readme.exists():
            result["missing_instructions"].append(folder)
            result["errors"].append(f"T005: {ERROR_CODES['T005']}: {folder}/.instructions/")

    return result


def main():
    """Точка входа."""
    # UTF-8 для Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация согласованности /.structure/README.md"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в JSON формате"
    )
    parser.add_argument(
        "--check-instructions",
        action="store_true",
        help="Проверить наличие зеркал .instructions"
    )
    parser.add_argument(
        "--check-nested",
        action="store_true",
        help="Проверить секции 'Вложенные области' в .instructions"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Автоматически исправить расхождения (T002, T003)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    result = validate_structure(repo_root)

    # Проверка зеркал .instructions
    if args.check_instructions and result["tree_folders"]:
        instr_result = check_instructions_mirrors(repo_root, result["tree_folders"])
        result["missing_instructions"] = instr_result["missing_instructions"]
        result["errors"].extend(instr_result["errors"])
        if instr_result["errors"]:
            result["valid"] = False

    # Проверка секций "Вложенные области"
    if args.check_nested and result["tree_folders"]:
        nested_result = check_all_nested_areas(repo_root, result["tree_folders"])
        result["nested_errors"] = nested_result["nested_errors"]
        result["errors"].extend(nested_result["errors"])
        if nested_result["errors"]:
            result["valid"] = False

    # Автоматическое исправление
    if args.fix and (result["missing_in_tree"] or result["missing_in_fs"]):
        fix_result = fix_structure_errors(
            repo_root,
            result["missing_in_tree"],
            result["missing_in_fs"]
        )
        result["fix_result"] = fix_result

        if not args.json:
            if fix_result["fixed"]:
                print("🔧 Исправлено:")
                for msg in fix_result["fixed"]:
                    print(f"   • {msg}")
                print()

            if fix_result["failed"]:
                print("❌ Не удалось исправить:")
                for msg in fix_result["failed"]:
                    print(f"   • {msg}")
                print()

            # После исправлений — повторная проверка
            print("Повторная проверка...")
            result = validate_structure(repo_root)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["valid"] else 1)

    # Человекочитаемый вывод
    print(f"Проверка: {repo_root / '.structure' / 'README.md'}")
    print()

    if result["valid"] and not result["warnings"]:
        print("✅ Структура валидна")
        print()
        print(f"   Папок в ФС: {len(result['fs_folders'])}")
        print(f"   Папок в дереве: {len(result['tree_folders'])}")
        sys.exit(0)

    if result["errors"]:
        print("❌ Ошибки:")
        for error in result["errors"]:
            print(f"   • {error}")
        print()

    if result["warnings"]:
        print("⚠️  Предупреждения:")
        for warning in result["warnings"]:
            print(f"   • {warning}")
        print()

    if result["missing_in_tree"]:
        print("📁 Добавить в дерево:")
        for folder in sorted(result["missing_in_tree"]):
            print(f"   ├── {folder}/")
        print()

    if result["missing_in_fs"]:
        print("🗑️  Удалить из дерева (или создать папку):")
        for folder in sorted(result["missing_in_fs"]):
            print(f"   ├── {folder}/")
        print()

    if result.get("missing_instructions"):
        print("📋 Создать зеркало .instructions:")
        for folder in sorted(result["missing_instructions"]):
            print(f"   python mirror-instructions.py create {folder}")
        print()

    if result.get("nested_errors"):
        print("📂 Ошибки секций 'Вложенные области':")
        for err in result["nested_errors"]:
            print(f"   • {err['code']}: {err['message']}")
        print()

    sys.exit(1 if not result["valid"] else 0)


if __name__ == "__main__":
    main()
