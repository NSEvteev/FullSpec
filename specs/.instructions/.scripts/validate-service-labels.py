#!/usr/bin/env python3
"""
validate-service-labels.py — Валидация соответствия svc:* меток и specs/services/ папок.

Использование:
    python validate-service-labels.py              # Проверить соответствие
    python validate-service-labels.py --verbose    # Подробный вывод

Проверяет:
    - Каждая папка specs/services/{svc}/ имеет метку svc:{svc} в labels.yml (ERROR)
    - Каждая метка svc:{svc} имеет папку specs/services/{svc}/ (WARNING)

SSOT:
    - specs/services/ — папки = сервисы
    - .github/labels.yml — метки svc:*

Примеры:
    python validate-service-labels.py
    # ✅ Все svc:* метки соответствуют specs/services/

    python validate-service-labels.py --verbose
    # 📁 Найдено сервисов (папки): 3
    # 🏷️ Найдено svc:* меток: 3

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
"""

import argparse
import re
import sys
from pathlib import Path

# Коды ошибок
ERROR_CODES = {
    "SL001": "Папка specs/services/{svc}/ существует, но метка svc:{svc} отсутствует в labels.yml",
    "SL002": "(warning) Метка svc:{svc} в labels.yml, но specs/services/{svc}/ не найдена",
}


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def load_svc_labels(repo_root: Path) -> set[str]:
    """Загрузить svc:* метки из labels.yml."""
    labels_path = repo_root / ".github" / "labels.yml"
    if not labels_path.exists():
        return set()

    svc_labels = set()
    with open(labels_path, encoding="utf-8") as f:
        for line in f:
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue
            match = re.search(r'-\s*name:\s*["\']?svc:([a-z0-9-]+)["\']?', stripped)
            if match:
                svc_labels.add(match.group(1))

    return svc_labels


def load_service_dirs(repo_root: Path) -> set[str]:
    """Загрузить имена сервисов из папок specs/services/."""
    services_dir = repo_root / "specs" / "services"
    if not services_dir.exists():
        return set()

    service_dirs = set()
    for item in services_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            service_dirs.add(item.name)

    return service_dirs


def validate(repo_root: Path, verbose: bool = False) -> list[str]:
    """Валидация соответствия svc:* меток и specs/services/ папок."""
    errors = []

    label_services = load_svc_labels(repo_root)
    dir_services = load_service_dirs(repo_root)

    if verbose:
        print(f"📁 Найдено сервисов (папки): {len(dir_services)}")
        for svc in sorted(dir_services):
            print(f"    specs/services/{svc}/")
        print(f"🏷️  Найдено svc:* меток: {len(label_services)}")
        for svc in sorted(label_services):
            print(f"    svc:{svc}")

    # SL001: папка есть, метки нет (ERROR)
    for svc in sorted(dir_services - label_services):
        errors.append(
            f"[SL001] svc:{svc}: папка specs/services/{svc}/ существует, "
            f"но метка svc:{svc} отсутствует в labels.yml"
        )

    # SL002: метка есть, папки нет (WARNING)
    for svc in sorted(label_services - dir_services):
        errors.append(
            f"[SL002] svc:{svc}: метка в labels.yml, "
            f"но specs/services/{svc}/ не найдена (warning)"
        )

    return errors


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация соответствия svc:* меток и specs/services/ папок"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    print("🔍 Валидация svc:* ↔ specs/services/...")

    errors = validate(repo_root, verbose=args.verbose)

    if errors:
        print("\n❌ Найдены ошибки:")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("✅ Все svc:* метки соответствуют specs/services/")
        sys.exit(0)


if __name__ == "__main__":
    main()
