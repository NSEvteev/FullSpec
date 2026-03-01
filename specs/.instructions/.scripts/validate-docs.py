#!/usr/bin/env python3
"""
validate-docs.py — Валидация структуры specs/docs/.

Проверяет наличие обязательных директорий, системных документов,
индекса и файлов-примеров в specs/docs/.

Использование:
    python validate-docs.py [--json] [--repo <dir>]

Примеры:
    python validate-docs.py
    python validate-docs.py --json
    python validate-docs.py --repo /path/to/repo

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

DOCS_ROOT = "specs/docs"

REQUIRED_DIRS = [
    "specs/docs",
    "specs/docs/.system",
    "specs/docs/.technologies",
]

REQUIRED_SYSTEM_FILES = [
    "specs/docs/.system/overview.md",
    "specs/docs/.system/conventions.md",
    "specs/docs/.system/infrastructure.md",
    "specs/docs/.system/testing.md",
]

REQUIRED_INDEX = "specs/docs/README.md"

REQUIRED_EXAMPLES = [
    "specs/docs/example.md",
]

REQUIRED_TEMPLATES = [
    "specs/docs/.technologies/standard-openapi.md",
    "specs/docs/.technologies/standard-protobuf.md",
    "specs/docs/.technologies/standard-asyncapi.md",
]

ERROR_CODES = {
    "DOC001": "Отсутствует обязательная директория docs/",
    "DOC002": "Отсутствует обязательная поддиректория",
    "DOC003": "Отсутствует обязательный системный документ",
    "DOC004": "Отсутствует README.md (индекс)",
    "DOC005": "Отсутствует файл-пример",
    "DOC006": "Отсутствует шаблонный per-tech стандарт",
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


# =============================================================================
# Валидация
# =============================================================================

def validate_directories(repo_root: Path) -> list[tuple[str, str]]:
    """Проверка обязательных директорий."""
    errors = []
    for dir_path in REQUIRED_DIRS:
        full_path = repo_root / dir_path
        if not full_path.is_dir():
            code = "DOC001" if dir_path == DOCS_ROOT else "DOC002"
            errors.append((code, f"Директория не найдена: {dir_path}"))
    return errors


def validate_system_files(repo_root: Path) -> list[tuple[str, str]]:
    """Проверка обязательных системных документов."""
    errors = []
    for file_path in REQUIRED_SYSTEM_FILES:
        full_path = repo_root / file_path
        if not full_path.is_file():
            errors.append(("DOC003", f"Файл не найден: {file_path}"))
    return errors


def validate_index(repo_root: Path) -> list[tuple[str, str]]:
    """Проверка индекса docs/README.md."""
    errors = []
    full_path = repo_root / REQUIRED_INDEX
    if not full_path.is_file():
        errors.append(("DOC004", f"Файл не найден: {REQUIRED_INDEX}"))
    return errors


def validate_examples(repo_root: Path) -> list[tuple[str, str]]:
    """Проверка файлов-примеров."""
    errors = []
    for file_path in REQUIRED_EXAMPLES:
        full_path = repo_root / file_path
        if not full_path.is_file():
            errors.append(("DOC005", f"Файл не найден: {file_path}"))
    return errors


def validate_templates(repo_root: Path) -> list[tuple[str, str]]:
    """Проверка шаблонных per-tech стандартов."""
    errors = []
    for file_path in REQUIRED_TEMPLATES:
        full_path = repo_root / file_path
        if not full_path.is_file():
            errors.append(("DOC006", f"Файл не найден: {file_path}"))
    return errors


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация структуры specs/docs/ (DOC001-DOC006)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Пути к файлам (игнорируются, проверяется вся структура docs/)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    # Собираем все ошибки
    all_errors = []
    all_errors.extend(validate_directories(repo_root))
    all_errors.extend(validate_index(repo_root))
    all_errors.extend(validate_system_files(repo_root))
    all_errors.extend(validate_examples(repo_root))
    all_errors.extend(validate_templates(repo_root))

    has_errors = len(all_errors) > 0

    # Вывод
    if args.json:
        result = {
            "file": DOCS_ROOT,
            "errors": [{"code": code, "message": msg} for code, msg in all_errors],
            "valid": not has_errors,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not has_errors:
            print(f"✅ docs/ — валидация пройдена ({len(REQUIRED_DIRS)} директорий, "
                  f"{len(REQUIRED_SYSTEM_FILES)} системных файлов, "
                  f"{len(REQUIRED_EXAMPLES)} примеров, "
                  f"{len(REQUIRED_TEMPLATES)} шаблонов)")
        else:
            print(f"❌ docs/ — {len(all_errors)} ошибок:")
            for code, msg in all_errors:
                print(f"   {code}: {msg}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
