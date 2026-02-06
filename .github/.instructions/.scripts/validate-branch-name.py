#!/usr/bin/env python3
"""
validate-branch-name.py — Валидация имени ветки по стандарту ветвления.

Проверяет формат имени ветки, порядок номеров Issues.
Опционально: существование Issues и соответствие TYPE-меток.

Использование:
    python validate-branch-name.py [branch-name] [--check-issues] [--check-labels] [--json]

Примеры:
    python validate-branch-name.py feature/auth-42-43
    python validate-branch-name.py --check-issues --check-labels
    python validate-branch-name.py fix/upload-50 --json

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

ALLOWED_PREFIXES = ("feature", "fix", "docs", "task", "refactor")

# Regex: {type}/{description}-{issue-numbers}
# - type: одно из ALLOWED_PREFIXES
# - description: kebab-case, каждая часть начинается с буквы
# - issue-numbers: одно или более чисел через дефис
BRANCH_PATTERN = re.compile(
    r'^(?P<type>' + '|'.join(ALLOWED_PREFIXES) + r')'
    r'/(?P<description>[a-z][a-z0-9]*(?:-[a-z][a-z0-9]*)*)'
    r'-(?P<numbers>\d+(?:-\d+)*)$'
)

# TYPE-метка Issue → ожидаемый префикс ветки
LABEL_TO_PREFIX = {
    "feature": "feature",
    "bug": "fix",
    "task": "task",
    "docs": "docs",
    "refactor": "refactor",
}

SKIP_BRANCHES = ("main", "master", "develop", "release", "hotfix")

ERROR_CODES = {
    "BR001": "Нет префикса типа",
    "BR002": "Неизвестный префикс",
    "BR003": "Нет номера Issue",
    "BR004": "Подчёркивание в имени",
    "BR005": "Верхний регистр",
    "BR006": "Issue не существует",
    "BR007": "Issue закрыт",
    "BR008": "Несоответствие TYPE-метки",
    "BR009": "Номера не по возрастанию",
    "BR010": "Невалидный формат имени",
    "BR011": "Прямой push в main",
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
    """Получить имя текущей ветки через git."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, encoding="utf-8", timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def run_gh_command(args: list[str]) -> dict | None:
    """Выполнить gh api команду и вернуть JSON."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True, encoding="utf-8", timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
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

    # BR011: Прямой push в main
    if branch_name == "main":
        errors.append(("BR011", "Прямой push в main запрещён"))
        return errors

    # BR005: Верхний регистр
    if branch_name != branch_name.lower():
        errors.append(("BR005", f"Верхний регистр в '{branch_name}'"))

    # BR004: Подчёркивание
    if "_" in branch_name:
        errors.append(("BR004", f"Подчёркивание в '{branch_name}' — используйте дефис"))

    # BR001: Нет слэша (нет префикса)
    if "/" not in branch_name:
        errors.append(("BR001", f"Нет префикса типа в '{branch_name}'"))
        return errors

    prefix = branch_name.split("/")[0]

    # BR002: Неизвестный префикс
    if prefix not in ALLOWED_PREFIXES:
        errors.append(("BR002", f"Неизвестный префикс '{prefix}' — допустимые: {', '.join(ALLOWED_PREFIXES)}"))
        return errors

    # BR010: Полный regex
    match = BRANCH_PATTERN.match(branch_name.lower())
    if not match:
        # BR003: Нет номера Issue
        if not re.search(r'-\d+', branch_name):
            errors.append(("BR003", f"Нет номера Issue в '{branch_name}'"))
        else:
            errors.append(("BR010", f"Невалидный формат: '{branch_name}'"))
        return errors

    # BR009: Порядок номеров
    numbers_str = match.group("numbers")
    numbers = [int(n) for n in numbers_str.split("-")]
    if numbers != sorted(numbers):
        errors.append(("BR009", f"Номера не по возрастанию: {numbers_str} → ожидается {'-'.join(str(n) for n in sorted(numbers))}"))

    return errors


def extract_issue_numbers(branch_name: str) -> list[int]:
    """Извлечь номера Issues из имени ветки."""
    match = BRANCH_PATTERN.match(branch_name)
    if not match:
        return []
    return [int(n) for n in match.group("numbers").split("-")]


def validate_issues(branch_name: str) -> list[tuple[str, str]]:
    """Проверить существование и статус Issues через gh api.

    Returns:
        list: [(код ошибки, сообщение)]
    """
    errors = []
    numbers = extract_issue_numbers(branch_name)

    for num in numbers:
        data = run_gh_command(["issue", "view", str(num), "--json", "state,title"])
        if data is None:
            errors.append(("BR006", f"Issue #{num} не существует или недоступен"))
            continue
        if data.get("state") != "OPEN":
            errors.append(("BR007", f"Issue #{num} закрыт (state={data.get('state')})"))

    return errors


def validate_labels(branch_name: str) -> list[tuple[str, str]]:
    """Проверить соответствие TYPE-метки Issue и префикса ветки.

    Returns:
        list: [(код ошибки, сообщение)]
    """
    errors = []
    match = BRANCH_PATTERN.match(branch_name)
    if not match:
        return errors

    prefix = match.group("type")
    numbers = extract_issue_numbers(branch_name)
    if not numbers:
        return errors

    min_issue = min(numbers)
    data = run_gh_command(["issue", "view", str(min_issue), "--json", "labels"])
    if data is None:
        return errors  # Уже проверено в validate_issues

    labels = [lbl["name"] for lbl in data.get("labels", [])]
    type_labels = [lbl for lbl in labels if lbl in LABEL_TO_PREFIX]

    if not type_labels:
        return errors  # Нет TYPE-метки — не блокируем

    expected_prefix = LABEL_TO_PREFIX.get(type_labels[0])
    if expected_prefix and expected_prefix != prefix:
        errors.append((
            "BR008",
            f"Префикс '{prefix}/' не соответствует TYPE-метке '{type_labels[0]}' "
            f"Issue #{min_issue} → ожидается '{expected_prefix}/'"
        ))

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
        "--check-issues",
        action="store_true",
        help="Проверить существование Issues через gh api"
    )
    parser.add_argument(
        "--check-labels",
        action="store_true",
        help="Проверить соответствие TYPE-меток через gh api"
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

    if not errors and args.check_issues:
        errors.extend(validate_issues(branch_name))

    if not errors and args.check_labels:
        errors.extend(validate_labels(branch_name))

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

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
