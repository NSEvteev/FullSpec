#!/usr/bin/env python3
"""
validate.py — Единый скрипт валидации проекта.

Использование:
    python validate.py [--repo <корень>] [--path <папка>]
    python validate.py --structure           # Только структура
    python validate.py --links               # Только ссылки
    python validate.py --check-instructions  # Проверка зеркал .instructions

Примеры:
    python validate.py                       # Все проверки
    python validate.py --path test/          # Проверки только для test/
    python validate.py --check-instructions  # Папки без .instructions

Запускает:
    - validate-structure.py — согласованность SSOT
    - validate-links.py — валидность ссылок
    - check_instructions_mirrors() — наличие зеркал .instructions

Возвращает:
    0 — всё валидно
    1 — есть ошибки
"""

import argparse
import subprocess
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


def get_project_folders(repo_root: Path) -> list[Path]:
    """Получить список папок проекта, которые должны иметь .instructions."""
    # Папки, которые пропускаем
    skip_names = {
        ".git", ".venv", "venv", "node_modules", "__pycache__",
        ".instructions", ".scripts", "DELETE_.instructions",
    }
    skip_prefixes = (".", "DELETE_")

    folders = []

    for item in repo_root.iterdir():
        if not item.is_dir():
            continue
        name = item.name

        # Пропускаем системные и скрытые
        if name in skip_names:
            continue
        if name.startswith(skip_prefixes):
            continue

        folders.append(item)

    return sorted(folders, key=lambda p: p.name)


def check_instructions_mirrors(repo_root: Path, json_output: bool = False) -> tuple[bool, str]:
    """
    Проверить наличие .instructions зеркал для папок проекта.

    Возвращает (all_valid, output_text).
    """
    folders = get_project_folders(repo_root)
    missing = []

    for folder in folders:
        instructions_path = folder / ".instructions"
        readme_path = instructions_path / "README.md"

        if not instructions_path.exists() or not readme_path.exists():
            missing.append(folder)

    if json_output:
        import json
        result = {
            "total_folders": len(folders),
            "missing_instructions": [str(f.relative_to(repo_root)) for f in missing],
            "valid": len(missing) == 0,
        }
        return len(missing) == 0, json.dumps(result, indent=2, ensure_ascii=False)

    # Текстовый вывод
    lines = ["📁 Проверка зеркал .instructions"]
    lines.append(f"   Папок проверено: {len(folders)}")

    if not missing:
        lines.append("   ✅ Все папки имеют .instructions")
    else:
        lines.append(f"   ❌ Папок без .instructions: {len(missing)}")
        lines.append("")
        lines.append("   Недостающие зеркала:")
        for folder in missing:
            rel_path = folder.relative_to(repo_root)
            lines.append(f"   • {rel_path}/")

        lines.append("")
        lines.append("   Команды для создания:")
        for folder in missing:
            rel_path = str(folder.relative_to(repo_root)).replace("\\", "/")
            lines.append(f"   python .structure/.instructions/.scripts/mirror-instructions.py create {rel_path}")

    return len(missing) == 0, "\n".join(lines)


def run_script(script_name: str, repo_root: Path, extra_args: list = None) -> tuple[bool, str]:
    """Запустить скрипт и вернуть (success, output)."""
    script_dir = Path(__file__).parent
    script_path = script_dir / script_name

    cmd = [sys.executable, str(script_path), "--repo", str(repo_root)]
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        output = result.stdout + result.stderr
        return result.returncode == 0, output.strip()
    except Exception as e:
        return False, f"Ошибка запуска {script_name}: {e}"


def main():
    """Точка входа."""
    # UTF-8 для Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Единый скрипт валидации проекта"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )
    parser.add_argument(
        "--path",
        default=None,
        help="Конкретная папка для проверки ссылок"
    )
    parser.add_argument(
        "--structure",
        action="store_true",
        help="Только проверка структуры"
    )
    parser.add_argument(
        "--links",
        action="store_true",
        help="Только проверка ссылок"
    )
    parser.add_argument(
        "--check-instructions",
        action="store_true",
        dest="check_instructions",
        help="Проверка зеркал .instructions для папок проекта"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON (для --check-instructions)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Определяем что запускать
    has_specific = args.structure or args.links or args.check_instructions

    run_struct = args.structure or not has_specific
    run_links = args.links or not has_specific
    run_instructions = args.check_instructions

    all_valid = True

    if not args.json:
        print(f"Проверка: {repo_root}")
        print()

    # === Структура ===
    if run_struct:
        success, output = run_script("validate-structure.py", repo_root)
        if not success:
            all_valid = False
        if output:
            print(output)
        print()

    # === Ссылки ===
    if run_links:
        extra_args = ["--path", args.path] if args.path else None
        success, output = run_script("validate-links.py", repo_root, extra_args)
        if not success:
            all_valid = False
        if output:
            print(output)
        print()

    # === Зеркала .instructions ===
    if run_instructions:
        success, output = check_instructions_mirrors(repo_root, json_output=args.json)
        if not success:
            all_valid = False
        if output:
            print(output)
        if not args.json:
            print()

    # Итог
    if not args.json:
        print("─" * 40)
        if all_valid:
            print("✅ Валидация пройдена")
        else:
            print("❌ Валидация не пройдена")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
