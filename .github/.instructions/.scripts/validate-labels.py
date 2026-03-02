#!/usr/bin/env python3
"""
validate-labels.py — Валидация labels.yml и меток на Issues/PR.

Использование:
    python validate-labels.py --file              # Валидация структуры labels.yml
    python validate-labels.py --sync              # Проверка синхронизации с GitHub
    python validate-labels.py --issue 123         # Валидация меток на Issue
    python validate-labels.py --pr 456            # Валидация меток на PR
    python validate-labels.py --all               # Валидация всех открытых Issues/PR

Примеры:
    python validate-labels.py --file --sync
    python validate-labels.py --issue 123 --issue 456
    python validate-labels.py --all

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Допустимые имена меток по группам (SSOT: labels.yml)
TYPE_LABELS = {"bug", "task", "docs", "refactor"}
PRIORITY_LABELS = {"critical", "high", "medium", "low"}
AREA_LABELS = {"backend", "frontend", "database", "platform", "api", "tests", "specs"}
ENV_LABELS = {"production", "staging", "local"}

# Коды ошибок для валидатора
ERROR_CODES = {
    "E001": "Некорректный формат имени метки",
    "E002": "Имя метки не в lowercase",
    "E003": "Имя метки не в kebab-case",
    "E004": "HEX цвета некорректен (должен быть 6 символов без #)",
    "E005": "Дубликат имени метки",
    "E006": "Description не начинается с emoji",
    "E007": "Description превышает 50 символов",
    "E008": "Метка отсутствует в GitHub",
    "E009": "Лишняя метка в GitHub (нет в labels.yml)",
    "E010": "Расхождение description/color с GitHub",
    "E011": "Отсутствует обязательная метка типа",
    "E012": "Отсутствует обязательная метка приоритета",
    "E013": "Несколько меток типа",
    "E014": "Несколько меток приоритета",
    "E015": "Метка env на не-баге",
    "E016": "Более 3 меток area",
    "E017": "Метка не существует в labels.yml",
}


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def load_labels_yml(repo_root: Path) -> list[dict]:
    """Загрузить метки из labels.yml."""
    labels_path = repo_root / ".github" / "labels.yml"
    if not labels_path.exists():
        print(f"[E001] Файл не найден: {labels_path}")
        return []

    try:
        import yaml
    except ImportError:
        print("[WARN] PyYAML не установлен, используем простой парсер")
        return parse_labels_yml_simple(labels_path)

    with open(labels_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def parse_labels_yml_simple(path: Path) -> list[dict]:
    """Простой парсер labels.yml без PyYAML."""
    labels = []
    current: dict = {}

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- name:"):
                if current:
                    labels.append(current)
                current = {"name": line.split(":", 1)[1].strip().strip('"')}
            elif line.startswith("description:") and current:
                current["description"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("color:") and current:
                current["color"] = line.split(":", 1)[1].strip().strip('"')

    if current:
        labels.append(current)

    return labels


def validate_label_format(label: dict) -> list[str]:
    """Проверить формат одной метки."""
    errors = []
    name = label.get("name", "")
    desc = label.get("description", "")
    color = label.get("color", "")

    # E002: lowercase
    if name != name.lower():
        errors.append(f"[E002] {name}: должен быть lowercase")

    # E003: kebab-case (буквы, цифры, дефис; допускается префикс с двоеточием для svc:)
    if not re.match(r"^[a-z0-9-]+(:[a-z0-9-]+)?$", name):
        errors.append(f"[E003] {name}: должен быть kebab-case")

    # E004: HEX цвета
    if not re.match(r"^[0-9a-fA-F]{6}$", color):
        errors.append(f"[E004] {name}: color '{color}' некорректен")

    # E006: emoji в начале description
    if desc and not has_emoji(desc):
        errors.append(f"[E006] {name}: description не начинается с emoji")

    # E007: длина description
    if len(desc) > 50:
        errors.append(f"[E007] {name}: description > 50 символов ({len(desc)})")

    return errors


def has_emoji(text: str) -> bool:
    """Проверить наличие emoji в начале текста."""
    if not text:
        return False
    # Простая проверка: первый символ имеет высокий код (emoji обычно > 127)
    return ord(text[0]) > 127


def validate_file(repo_root: Path) -> list[str]:
    """Валидация структуры labels.yml."""
    errors = []
    labels = load_labels_yml(repo_root)

    if not labels:
        errors.append("[E001] labels.yml пуст или не найден")
        return errors

    names = set()
    for label in labels:
        # Проверка формата
        errors.extend(validate_label_format(label))

        # E005: дубликаты
        name = label.get("name", "")
        if name in names:
            errors.append(f"[E005] {name}: дубликат")
        names.add(name)

    return errors


def get_github_labels() -> list[dict]:
    """Получить метки из GitHub через gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "label", "list", "--json", "name,description,color", "--limit", "200"],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[WARN] Не удалось получить метки из GitHub: {e}")
        return []
    except FileNotFoundError:
        print("[WARN] gh CLI не установлен")
        return []


def validate_sync(repo_root: Path) -> list[str]:
    """Проверка синхронизации labels.yml с GitHub."""
    errors = []
    yml_labels = load_labels_yml(repo_root)
    gh_labels = get_github_labels()

    if not gh_labels:
        errors.append("[WARN] Не удалось получить метки из GitHub")
        return errors

    yml_names = {l["name"] for l in yml_labels}
    gh_names = {l["name"] for l in gh_labels}
    gh_by_name = {l["name"]: l for l in gh_labels}

    # E008: метки в yml, но нет в GitHub
    for name in yml_names - gh_names:
        errors.append(f"[E008] {name}: отсутствует в GitHub")

    # E009: метки в GitHub, но нет в yml
    for name in gh_names - yml_names:
        errors.append(f"[E009] {name}: лишняя в GitHub (нет в labels.yml)")

    # E010: расхождения description/color
    for label in yml_labels:
        name = label["name"]
        if name in gh_by_name:
            gh = gh_by_name[name]
            if label.get("description", "") != gh.get("description", ""):
                errors.append(f"[E010] {name}: расхождение description")
            if label.get("color", "").lower() != gh.get("color", "").lower():
                errors.append(f"[E010] {name}: расхождение color")

    return errors


def get_issue_labels(number: int) -> list[str]:
    """Получить метки Issue через gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(number), "--json", "labels", "-q", ".labels[].name"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
    except subprocess.CalledProcessError:
        return []


def get_pr_labels(number: int) -> list[str]:
    """Получить метки PR через gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "pr", "view", str(number), "--json", "labels", "-q", ".labels[].name"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
    except subprocess.CalledProcessError:
        return []


def validate_labels_on_item(
    labels: list[str], item_type: str, number: int, valid_names: set[str]
) -> list[str]:
    """Валидация меток на Issue/PR."""
    errors = []
    prefix = f"{item_type} #{number}"

    # Фильтруем по категориям (по именам, без префиксов)
    type_labels = [l for l in labels if l in TYPE_LABELS]
    priority_labels = [l for l in labels if l in PRIORITY_LABELS]
    area_labels = [l for l in labels if l in AREA_LABELS]
    env_labels = [l for l in labels if l in ENV_LABELS]

    # E011: нет метки типа
    if not type_labels:
        errors.append(f"[E011] {prefix}: отсутствует метка типа ({', '.join(sorted(TYPE_LABELS))})")

    # E012: нет метки приоритета
    if not priority_labels:
        errors.append(f"[E012] {prefix}: отсутствует метка приоритета ({', '.join(sorted(PRIORITY_LABELS))})")

    # E013: несколько меток типа
    if len(type_labels) > 1:
        errors.append(f"[E013] {prefix}: несколько меток типа ({', '.join(type_labels)})")

    # E014: несколько меток приоритета
    if len(priority_labels) > 1:
        errors.append(f"[E014] {prefix}: несколько меток приоритета ({', '.join(priority_labels)})")

    # E015: env на не-баге
    if env_labels and "bug" not in labels:
        errors.append(f"[E015] {prefix}: env-метка без bug ({', '.join(env_labels)})")

    # E016: более 3 меток area
    if len(area_labels) > 3:
        errors.append(f"[E016] {prefix}: более 3 меток area ({len(area_labels)})")

    # E017: метка не в labels.yml
    for label in labels:
        if label not in valid_names:
            errors.append(f"[E017] {prefix}: метка '{label}' не в labels.yml")

    return errors


def validate_issue(number: int, valid_names: set[str]) -> list[str]:
    """Валидация меток на Issue."""
    labels = get_issue_labels(number)
    if not labels:
        return [f"[WARN] Issue #{number}: не удалось получить метки"]
    return validate_labels_on_item(labels, "Issue", number, valid_names)


def validate_pr(number: int, valid_names: set[str]) -> list[str]:
    """Валидация меток на PR."""
    labels = get_pr_labels(number)
    if not labels:
        return [f"[WARN] PR #{number}: не удалось получить метки"]
    return validate_labels_on_item(labels, "PR", number, valid_names)


def get_all_open_issues() -> list[int]:
    """Получить номера всех открытых Issues."""
    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--state", "open", "--json", "number", "-q", ".[].number"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [int(n) for n in result.stdout.strip().split("\n") if n.strip()]
    except subprocess.CalledProcessError:
        return []


def get_all_open_prs() -> list[int]:
    """Получить номера всех открытых PR."""
    try:
        result = subprocess.run(
            ["gh", "pr", "list", "--state", "open", "--json", "number", "-q", ".[].number"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [int(n) for n in result.stdout.strip().split("\n") if n.strip()]
    except subprocess.CalledProcessError:
        return []


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация labels.yml и меток на Issues/PR"
    )
    parser.add_argument("--file", action="store_true", help="Валидация структуры labels.yml")
    parser.add_argument("--sync", action="store_true", help="Проверка синхронизации с GitHub")
    parser.add_argument("--issue", type=int, action="append", help="Номер Issue для проверки")
    parser.add_argument("--pr", type=int, action="append", help="Номер PR для проверки")
    parser.add_argument("--all", action="store_true", help="Проверить все открытые Issues/PR")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    # Если ничего не указано — проверяем файл
    if not any([args.file, args.sync, args.issue, args.pr, args.all]):
        args.file = True

    repo_root = find_repo_root(Path(args.repo))
    all_errors: list[str] = []

    # Загружаем валидные имена меток
    labels = load_labels_yml(repo_root)
    valid_names = {l["name"] for l in labels}

    # Валидация файла
    if args.file:
        print("📋 Валидация labels.yml...")
        errors = validate_file(repo_root)
        all_errors.extend(errors)
        if not errors:
            print("  ✅ Структура корректна")

    # Синхронизация
    if args.sync:
        print("🔄 Проверка синхронизации с GitHub...")
        errors = validate_sync(repo_root)
        all_errors.extend(errors)
        if not errors:
            print("  ✅ Синхронизировано")

    # Проверка Issues
    issues = args.issue or []
    if args.all:
        issues.extend(get_all_open_issues())

    for num in issues:
        print(f"🔍 Проверка Issue #{num}...")
        errors = validate_issue(num, valid_names)
        all_errors.extend(errors)
        if not errors:
            print(f"  ✅ Issue #{num} OK")

    # Проверка PR
    prs = args.pr or []
    if args.all:
        prs.extend(get_all_open_prs())

    for num in prs:
        print(f"🔍 Проверка PR #{num}...")
        errors = validate_pr(num, valid_names)
        all_errors.extend(errors)
        if not errors:
            print(f"  ✅ PR #{num} OK")

    # Вывод ошибок
    if all_errors:
        print("\n❌ Найдены ошибки:")
        for err in all_errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("\n✅ Все проверки пройдены")
        sys.exit(0)


if __name__ == "__main__":
    main()
