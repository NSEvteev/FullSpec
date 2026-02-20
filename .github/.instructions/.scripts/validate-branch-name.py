#!/usr/bin/env python3
"""
validate-branch-name.py — Валидация имени ветки по стандарту ветвления.

Проверяет формат имени ветки: {NNNN}-{description}.

Использование:
    python validate-branch-name.py [branch-name] [--json]

Примеры:
    python validate-branch-name.py 0001-oauth2-auth
    python validate-branch-name.py
    python validate-branch-name.py 0042-cache-optimization --json

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

# Regex: {NNNN}-{description}
# - NNNN: ровно 4 цифры (номер анализа)
# - description: kebab-case, каждая часть начинается с буквы
BRANCH_PATTERN = re.compile(
    r'^\d{4}-[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*$'
)

SKIP_BRANCHES = ("main", "master", "develop", "release", "hotfix")

ERROR_CODES = {
    "BR001": "Нет NNNN-префикса",
    "BR002": "Невалидный формат",
    "BR003": "Description не в kebab-case",
    "BR004": "Подчёркивание в имени",
    "BR005": "Верхний регистр",
    "BR006": "Прямой push в main",
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


def get_current_branch() -> str | None:
    """Получить имя текущей ветки через git или CI-переменные."""
    import os

    # CI: GitHub Actions (detached HEAD — git branch --show-current пуст)
    branch = os.environ.get("GITHUB_HEAD_REF") or os.environ.get("GITHUB_REF_NAME")
    if branch:
        return branch

    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, encoding="utf-8", timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


# =============================================================================
# Валидация
# =============================================================================

def validate_format(branch_name: str) -> list[tuple[str, str]]:
    """Валидация формата имени ветки.

    Returns:
        list: [(код ошибки, сообщение)]
    """
    errors = []

    # Пропуск системных веток
    if branch_name in SKIP_BRANCHES:
        return errors

    # BR006: Прямой push в main
    if branch_name == "main":
        errors.append(("BR006", "Прямой push в main запрещён"))
        return errors

    # BR005: Верхний регистр
    if branch_name != branch_name.lower():
        errors.append(("BR005", f"Верхний регистр в '{branch_name}'"))

    # BR004: Подчёркивание
    if "_" in branch_name:
        errors.append(("BR004", f"Подчёркивание в '{branch_name}' — используйте дефис"))

    # BR001: Нет NNNN-префикса (не начинается с 4 цифр)
    if not re.match(r'^\d{4}-', branch_name):
        errors.append(("BR001", f"Нет NNNN-префикса в '{branch_name}' — ожидается 4-значный номер анализа"))
        return errors

    # BR002: Полный regex
    if not BRANCH_PATTERN.match(branch_name):
        # BR003: Description не в kebab-case
        desc_part = branch_name[5:]  # после NNNN-
        if desc_part != desc_part.lower() or not re.match(r'^[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*$', desc_part):
            errors.append(("BR003", f"Description не в kebab-case: '{desc_part}'"))
        else:
            errors.append(("BR002", f"Невалидный формат: '{branch_name}'"))

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
        description="Валидация имени ветки по стандарту ветвления"
    )
    parser.add_argument(
        "branch",
        nargs="?",
        help="Имя ветки (по умолчанию: текущая ветка)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )

    args = parser.parse_args()

    # Определить имя ветки
    branch_name = args.branch or get_current_branch()
    if not branch_name:
        print("❌ Не удалось определить имя ветки", file=sys.stderr)
        sys.exit(2)

    # Пропуск системных веток
    if branch_name in SKIP_BRANCHES:
        if not args.json:
            print(f"⏭️  Системная ветка '{branch_name}' — пропуск валидации")
        sys.exit(0)

    # Валидация
    errors = validate_format(branch_name)

    # Вывод результатов
    if args.json:
        result = {
            "branch": branch_name,
            "errors": [
                {"code": code, "message": msg}
                for code, msg in errors
            ],
            "valid": len(errors) == 0
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if errors:
            print(f"❌ Ветка '{branch_name}' — {len(errors)} ошибок:")
            for code, msg in errors:
                print(f"   {code}: {msg}")
        else:
            print(f"✅ Ветка '{branch_name}' — валидация пройдена")
            print(f"   ℹ️  Push в remote после первого коммита: git push -u origin {branch_name}")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
