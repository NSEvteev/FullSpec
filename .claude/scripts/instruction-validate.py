#!/usr/bin/env python3
"""
instruction-validate.py — Валидация пути инструкции.

Использование:
    python instruction-validate.py <путь> [--repo <корень>]

Примеры:
    python instruction-validate.py src/api/design.md
    python instruction-validate.py specs/statuses.md
    python instruction-validate.py random/invalid.md  # ошибка

Проверки:
    - Путь соответствует допустимым папкам (или папка уже существует)
    - Файл имеет расширение .md
    - Папка .claude/instructions/ существует
    - Файл README.md инструкций существует

Возвращает:
    0 — валидация пройдена
    1 — ошибка валидации (детали в stderr)
"""

import argparse
import json
import sys
from pathlib import Path


# Стандартные допустимые папки
STANDARD_FOLDERS = [
    "src",
    "platform",
    "tests",
    "doc",
    "shared",
    "config",
    "git",
    "tools",
]


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def get_existing_folders(instructions_dir: Path) -> list[str]:
    """Получить список существующих папок в instructions/."""
    folders = []
    if instructions_dir.exists():
        for item in instructions_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                folders.append(item.name)
    return folders


def validate_path(
    path: str,
    repo_root: Path
) -> dict:
    """
    Валидировать путь инструкции.

    Возвращает dict с полями:
        valid: bool
        path: str — нормализованный путь
        folder: str — корневая папка (src, git, specs и т.д.)
        file_name: str — имя файла
        full_path: Path — полный путь к файлу
        exists: bool — файл уже существует
        errors: list[str] — список ошибок (если есть)
        warnings: list[str] — список предупреждений
    """
    result = {
        "valid": True,
        "path": path,
        "folder": "",
        "file_name": "",
        "full_path": None,
        "exists": False,
        "errors": [],
        "warnings": [],
    }

    instructions_dir = repo_root / ".claude" / "instructions"

    # Проверка 1: папка instructions существует
    if not instructions_dir.exists():
        result["errors"].append(
            f"Папка .claude/instructions/ не существует в {repo_root}"
        )
        result["valid"] = False
        return result

    # Проверка 2: README.md существует
    readme_path = instructions_dir / "README.md"
    if not readme_path.exists():
        result["warnings"].append(
            "Файл .claude/instructions/README.md не найден"
        )

    # Нормализация пути
    path = path.replace("\\", "/").strip("/")
    result["path"] = path

    # Проверка 3: расширение .md
    if not path.endswith(".md"):
        result["errors"].append(
            f"Файл должен иметь расширение .md, получено: {path}"
        )
        result["valid"] = False
        return result

    # Извлечение папки и имени файла
    parts = path.split("/")
    result["folder"] = parts[0]
    result["file_name"] = parts[-1]

    # Проверка 4: допустимая папка
    existing_folders = get_existing_folders(instructions_dir)
    allowed_folders = set(STANDARD_FOLDERS + existing_folders)

    if result["folder"] not in allowed_folders:
        # Проверяем, может это новая папка которую нужно создать
        result["warnings"].append(
            f"Папка '{result['folder']}' не существует и будет создана"
        )

    # Полный путь
    full_path = instructions_dir / path
    result["full_path"] = str(full_path)
    result["exists"] = full_path.exists()

    if result["exists"]:
        result["warnings"].append(
            f"Файл уже существует: {full_path}"
        )

    return result


def main():
    # UTF-8 для Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация пути инструкции."
    )
    parser.add_argument(
        "path",
        help="Путь к инструкции (относительно .claude/instructions/)"
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

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    result = validate_path(args.path, repo_root)

    if args.json:
        # JSON вывод для программного использования
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["valid"] else 1)

    # Человекочитаемый вывод
    if result["valid"]:
        print(f"✅ Путь валиден: {result['path']}")
        print(f"   Папка: {result['folder']}")
        print(f"   Файл: {result['file_name']}")
        print(f"   Полный путь: {result['full_path']}")

        if result["exists"]:
            print(f"   ⚠️  Файл уже существует")

        for warning in result["warnings"]:
            print(f"   ⚠️  {warning}")

        sys.exit(0)
    else:
        print(f"❌ Ошибка валидации: {result['path']}")
        for error in result["errors"]:
            print(f"   {error}")

        print()
        print("Допустимые папки:")
        for folder in sorted(STANDARD_FOLDERS):
            print(f"   - {folder}/")

        sys.exit(1)


if __name__ == "__main__":
    main()
