#!/usr/bin/env python3
"""
pre-commit-structure.py — Оркестратор проверок структуры для pre-commit.

Использование:
    python pre-commit-structure.py

Примеры:
    python pre-commit-structure.py

Логика:
    1. Получить staged файлы: git diff --cached --name-only
    2. Определить затронутые папки
    3. Если создана/удалена корневая папка → validate-structure.py --check
    4. Для каждой затронутой папки с README → sync-readme.py <папка> --check

Возвращает:
    0 — всё синхронизировано
    1 — есть расхождения (блокирует коммит)
"""

import subprocess
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

# Папки, исключённые из проверки
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


# =============================================================================
# Вспомогательные функции
# =============================================================================

def find_repo_root() -> Path:
    """Найти корень репозитория."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        return Path.cwd()


def get_staged_files() -> list:
    """Получить список staged файлов."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRD"],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().split("\n")
        return [f for f in files if f]  # Убираем пустые строки
    except subprocess.CalledProcessError:
        return []


def get_affected_folders(staged_files: list, repo_root: Path) -> dict:
    """
    Определить затронутые папки.

    Возвращает dict:
        root_folders: set — корневые папки (для validate-structure)
        folders_with_readme: set — папки с README (для sync-readme)
    """
    result = {
        "root_folders": set(),
        "folders_with_readme": set(),
    }

    for file_path in staged_files:
        parts = Path(file_path).parts

        if not parts:
            continue

        # Корневая папка
        root_folder = parts[0]
        if root_folder not in EXCLUDED_FOLDERS:
            result["root_folders"].add(root_folder)

        # Папка файла
        folder = Path(file_path).parent
        full_folder_path = repo_root / folder

        # Проверяем README в папке и родительских
        check_path = full_folder_path
        while check_path != repo_root and check_path != check_path.parent:
            # Проверяем, не исключена ли папка
            if any(part in EXCLUDED_FOLDERS for part in check_path.relative_to(repo_root).parts):
                break

            readme_path = check_path / "README.md"
            if readme_path.exists():
                result["folders_with_readme"].add(check_path)

            check_path = check_path.parent

    return result


def run_validate_structure(repo_root: Path) -> bool:
    """
    Запустить validate-structure.py --check.

    Returns:
        True если проверка пройдена, False если есть ошибки
    """
    scripts_dir = repo_root / ".structure" / ".instructions" / ".scripts"
    script_path = scripts_dir / "validate-structure.py"

    if not script_path.exists():
        print(f"⚠️  validate-structure.py не найден: {script_path}", file=sys.stderr)
        return True  # Не блокируем если скрипт не найден

    try:
        result = subprocess.run(
            [sys.executable, str(script_path), "--repo", str(repo_root)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("\n🔍 validate-structure.py:")
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            return False

        return True

    except Exception as e:
        print(f"⚠️  Ошибка при запуске validate-structure.py: {e}", file=sys.stderr)
        return True


def run_sync_readme(folder_path: Path, repo_root: Path) -> bool:
    """
    Запустить sync-readme.py --check для папки.

    Returns:
        True если проверка пройдена, False если есть ошибки
    """
    scripts_dir = repo_root / ".structure" / ".instructions" / ".scripts"
    script_path = scripts_dir / "sync-readme.py"

    if not script_path.exists():
        print(f"⚠️  sync-readme.py не найден: {script_path}", file=sys.stderr)
        return True  # Не блокируем если скрипт не найден

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                str(folder_path),
                "--check",
                "--repo", str(repo_root)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"\n🔍 sync-readme.py: {folder_path}")
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            return False

        return True

    except Exception as e:
        print(f"⚠️  Ошибка при запуске sync-readme.py: {e}", file=sys.stderr)
        return True


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    repo_root = find_repo_root()

    # 1. Получаем staged файлы
    staged_files = get_staged_files()

    if not staged_files:
        # Нет staged файлов — ничего проверять
        sys.exit(0)

    # 2. Определяем затронутые папки
    affected = get_affected_folders(staged_files, repo_root)

    all_passed = True

    # 3. Проверяем корневую структуру если затронуты корневые папки
    if affected["root_folders"]:
        print(f"📁 Проверка корневой структуры (затронуты: {', '.join(sorted(affected['root_folders']))})")

        if not run_validate_structure(repo_root):
            all_passed = False
            print("\n❌ Корневая структура не синхронизирована!")
            print("   Запустите: make sync-structure")
            print()

    # 4. Проверяем README в затронутых папках
    if affected["folders_with_readme"]:
        print(f"📄 Проверка README ({len(affected['folders_with_readme'])} папок)")

        for folder_path in sorted(affected["folders_with_readme"]):
            if not run_sync_readme(folder_path, repo_root):
                all_passed = False

        if not all_passed:
            print("\n❌ README не синхронизированы!")
            print("   Запустите: make sync-structure")
            print()

    # 5. Результат
    if all_passed:
        if affected["root_folders"] or affected["folders_with_readme"]:
            print("✅ Структура синхронизирована")
        sys.exit(0)
    else:
        print("=" * 50)
        print("Коммит заблокирован. Исправьте расхождения:")
        print("  make sync-structure")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
