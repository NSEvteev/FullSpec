#!/usr/bin/env python3
"""
validate.py — Единый скрипт валидации проекта.

Использование:
    python validate.py [--repo <корень>] [--path <папка>]
    python validate.py --structure  # Только структура
    python validate.py --links      # Только ссылки

Примеры:
    python validate.py              # Обе проверки
    python validate.py --path test/ # Проверки только для test/

Запускает:
    - validate-structure.py — согласованность SSOT
    - validate-links.py — валидность ссылок

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

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Определяем что запускать
    run_struct = not args.links or args.structure
    run_links = not args.structure or args.links

    # Если ничего не указано — запускаем обе
    if not args.structure and not args.links:
        run_struct = True
        run_links = True

    all_valid = True
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

    # Итог
    print("─" * 40)
    if all_valid:
        print("✅ Валидация пройдена")
    else:
        print("❌ Валидация не пройдена")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
