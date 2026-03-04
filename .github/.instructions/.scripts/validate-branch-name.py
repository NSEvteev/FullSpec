#!/usr/bin/env python3
"""
validate-branch-name.py — Валидация имени ветки по стандарту ветвления.

Проверяет что имя ветки = имя папки analysis chain (specs/analysis/{branch-name}/).

Использование:
    python validate-branch-name.py [branch-name] [--json]

Примеры:
    python validate-branch-name.py 0001-oauth2-authorization
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


# =============================================================================
# Константы
# =============================================================================

# Regex: {NNNN}-{topic} — имя ветки = имя папки analysis chain
# - NNNN: ровно 4 цифры (номер анализа)
# - topic: kebab-case, каждая часть начинается с буквы
BRANCH_PATTERN = re.compile(
    r'^\d{4}-[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*$'
)

SKIP_BRANCHES = ("main", "master", "develop", "release", "hotfix")
SKIP_PREFIXES = ("backport/", "chore/")

ERROR_CODES = {
    "BR001": "Нет NNNN-префикса",
    "BR002": "Невалидный формат",
    "BR003": "Topic не в kebab-case",
    "BR004": "Подчёркивание в имени",
    "BR005": "Верхний регистр",
    "BR006": "Прямой push в main",
    "BR007": "Папка analysis не найдена",
}


# =============================================================================
# Общие функции
# =============================================================================


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


def find_repo_root() -> str | None:
    """Найти корень git-репозитория."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, encoding="utf-8", timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def validate_analysis_folder(branch_name: str) -> list[tuple[str, str]]:
    """Проверить существование папки specs/analysis/{branch-name}/.

    Returns:
        list: [(код ошибки, сообщение)]
    """
    import os

    repo_root = find_repo_root()
    if not repo_root:
        return []  # не можем проверить — не блокируем

    analysis_path = os.path.join(repo_root, "specs", "analysis", branch_name)
    if not os.path.isdir(analysis_path):
        return [("BR007", ERROR_CODES["BR007"] + f": specs/analysis/{branch_name}/")]

    return []


# =============================================================================
# Валидация
# =============================================================================

def validate_format(branch_name: str) -> list[tuple[str, str]]:
    """Валидация формата имени ветки.

    Проверяет все правила BR001-BR005 без раннего выхода,
    чтобы накопить все ошибки за один запуск.

    Returns:
        list: [(код ошибки, сообщение)]
    """
    errors = []

    # BR005: Верхний регистр
    if branch_name != branch_name.lower():
        errors.append(("BR005", ERROR_CODES["BR005"] + f": '{branch_name}'"))

    # BR004: Подчёркивание
    if "_" in branch_name:
        errors.append(("BR004", ERROR_CODES["BR004"] + f": '{branch_name}' — используйте дефис"))

    # BR001: Нет NNNN-префикса (не начинается с 4 цифр)
    if not re.match(r'^\d{4}-', branch_name):
        errors.append(("BR001", ERROR_CODES["BR001"] + f": '{branch_name}' — ожидается 4-значный номер анализа"))
    elif not BRANCH_PATTERN.match(branch_name):
        # BR002/BR003: Полный regex не прошёл (проверяем только если NNNN-префикс есть)
        desc_part = branch_name[5:]  # после NNNN-
        if desc_part != desc_part.lower() or not re.match(r'^[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*$', desc_part):
            errors.append(("BR003", ERROR_CODES["BR003"] + f": '{desc_part}'"))
        else:
            errors.append(("BR002", ERROR_CODES["BR002"] + f": '{branch_name}'"))

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
    if branch_name in SKIP_BRANCHES or any(branch_name.startswith(p) for p in SKIP_PREFIXES):
        if not args.json:
            print(f"⏭️  Системная ветка '{branch_name}' — пропуск валидации")
        sys.exit(0)

    # Валидация формата + существования папки analysis
    errors = validate_format(branch_name)
    errors.extend(validate_analysis_folder(branch_name))

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
