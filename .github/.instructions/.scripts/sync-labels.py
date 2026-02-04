#!/usr/bin/env python3
"""
sync-labels.py — Синхронизация labels.yml с GitHub.

Создаёт недостающие метки, удаляет лишние, обновляет расхождения.

Использование:
    python sync-labels.py                    # Показать план (dry-run)
    python sync-labels.py --apply            # Применить изменения
    python sync-labels.py --apply --force    # Применить без подтверждения

Примеры:
    python sync-labels.py                    # Посмотреть что будет сделано
    python sync-labels.py --apply            # Синхронизировать с подтверждением
    python sync-labels.py --apply --force    # Синхронизировать без вопросов

Возвращает:
    0 — синхронизация выполнена / нет изменений
    1 — ошибка
"""

import argparse
import json
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


def load_labels_yml(repo_root: Path) -> list[dict]:
    """Загрузить метки из labels.yml."""
    labels_path = repo_root / ".github" / "labels.yml"
    if not labels_path.exists():
        print(f"[ERROR] Файл не найден: {labels_path}")
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
        print(f"[ERROR] Не удалось получить метки из GitHub: {e}")
        return []
    except FileNotFoundError:
        print("[ERROR] gh CLI не установлен")
        return []


def create_label(name: str, description: str, color: str) -> bool:
    """Создать метку в GitHub."""
    try:
        subprocess.run(
            ["gh", "label", "create", name, "--description", description, "--color", color],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Не удалось создать {name}: {e.stderr.decode()}")
        return False


def delete_label(name: str) -> bool:
    """Удалить метку из GitHub."""
    try:
        subprocess.run(
            ["gh", "label", "delete", name, "--yes"],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Не удалось удалить {name}: {e.stderr.decode()}")
        return False


def edit_label(name: str, description: str | None = None, color: str | None = None) -> bool:
    """Обновить метку в GitHub."""
    cmd = ["gh", "label", "edit", name]
    if description is not None:
        cmd.extend(["--description", description])
    if color is not None:
        cmd.extend(["--color", color])

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Не удалось обновить {name}: {e.stderr.decode()}")
        return False


def compute_diff(yml_labels: list[dict], gh_labels: list[dict]) -> dict:
    """Вычислить разницу между labels.yml и GitHub."""
    yml_by_name = {l["name"]: l for l in yml_labels}
    gh_by_name = {l["name"]: l for l in gh_labels}

    yml_names = set(yml_by_name.keys())
    gh_names = set(gh_by_name.keys())

    diff = {
        "create": [],  # Метки для создания
        "delete": [],  # Метки для удаления
        "update": [],  # Метки для обновления
    }

    # Метки для создания (есть в yml, нет в GitHub)
    for name in yml_names - gh_names:
        diff["create"].append(yml_by_name[name])

    # Метки для удаления (есть в GitHub, нет в yml)
    for name in gh_names - yml_names:
        diff["delete"].append(gh_by_name[name])

    # Метки для обновления (есть в обоих, но расхождения)
    for name in yml_names & gh_names:
        yml = yml_by_name[name]
        gh = gh_by_name[name]

        changes = {}
        if yml.get("description", "") != gh.get("description", ""):
            changes["description"] = yml.get("description", "")
        if yml.get("color", "").lower() != gh.get("color", "").lower():
            changes["color"] = yml.get("color", "")

        if changes:
            diff["update"].append({"name": name, "changes": changes})

    return diff


def print_plan(diff: dict) -> None:
    """Вывести план изменений."""
    total = len(diff["create"]) + len(diff["delete"]) + len(diff["update"])

    if total == 0:
        print("✅ Метки синхронизированы, изменений нет")
        return

    print(f"📋 План синхронизации ({total} изменений):\n")

    if diff["create"]:
        print(f"  🆕 Создать ({len(diff['create'])}):")
        for label in sorted(diff["create"], key=lambda x: x["name"]):
            print(f"     + {label['name']}")

    if diff["delete"]:
        print(f"\n  🗑️  Удалить ({len(diff['delete'])}):")
        for label in sorted(diff["delete"], key=lambda x: x["name"]):
            print(f"     - {label['name']}")

    if diff["update"]:
        print(f"\n  ✏️  Обновить ({len(diff['update'])}):")
        for item in sorted(diff["update"], key=lambda x: x["name"]):
            changes = ", ".join(item["changes"].keys())
            print(f"     ~ {item['name']} ({changes})")

    print()


def apply_changes(diff: dict, force: bool = False) -> bool:
    """Применить изменения."""
    total = len(diff["create"]) + len(diff["delete"]) + len(diff["update"])

    if total == 0:
        return True

    if not force:
        print_plan(diff)
        answer = input("Применить изменения? [y/N]: ").strip().lower()
        if answer not in ("y", "yes", "д", "да"):
            print("Отменено")
            return False

    success = True
    applied = 0

    # Создание
    for label in diff["create"]:
        name = label["name"]
        desc = label.get("description", "")
        color = label.get("color", "CCCCCC")
        print(f"  🆕 Создание {name}...", end=" ")
        if create_label(name, desc, color):
            print("✅")
            applied += 1
        else:
            success = False

    # Удаление
    for label in diff["delete"]:
        name = label["name"]
        print(f"  🗑️  Удаление {name}...", end=" ")
        if delete_label(name):
            print("✅")
            applied += 1
        else:
            success = False

    # Обновление
    for item in diff["update"]:
        name = item["name"]
        changes = item["changes"]
        print(f"  ✏️  Обновление {name}...", end=" ")
        if edit_label(name, changes.get("description"), changes.get("color")):
            print("✅")
            applied += 1
        else:
            success = False

    print(f"\n{'✅' if success else '⚠️'} Применено {applied}/{total} изменений")
    return success


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Синхронизация labels.yml с GitHub"
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Применить изменения (без флага — только показать план)"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Применить без подтверждения"
    )
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Загрузка данных
    print("📥 Загрузка labels.yml...")
    yml_labels = load_labels_yml(repo_root)
    if not yml_labels:
        print("[ERROR] labels.yml пуст или не найден")
        sys.exit(1)

    print("📥 Загрузка меток из GitHub...")
    gh_labels = get_github_labels()
    if gh_labels is None:
        sys.exit(1)

    # Вычисление разницы
    diff = compute_diff(yml_labels, gh_labels)

    if args.apply:
        success = apply_changes(diff, args.force)
        sys.exit(0 if success else 1)
    else:
        print_plan(diff)
        total = len(diff["create"]) + len(diff["delete"]) + len(diff["update"])
        if total > 0:
            print("Для применения запустите: python sync-labels.py --apply")
        sys.exit(0)


if __name__ == "__main__":
    main()
