#!/usr/bin/env python3
"""
check-github-required.py — Проверка наличия обязательных файлов GitHub.

Использование:
    python check-github-required.py

Проверяет:
    - .github/CODEOWNERS
    - .github/labels.yml
    - .github/PULL_REQUEST_TEMPLATE.md
    - .github/ISSUE_TEMPLATE/ (+ соответствие меток типа)

Примеры:
    python check-github-required.py
    # ✅ Все обязательные файлы GitHub на месте

Возвращает:
    0 — все файлы на месте
    1 — отсутствуют обязательные файлы
"""

import re
import sys
from pathlib import Path

# Допустимые имена меток типа (SSOT: labels.yml)
TYPE_LABELS = {"bug", "task", "docs", "refactor"}

# Коды ошибок
ERROR_CODES = {
    "GH001": "Отсутствует .github/CODEOWNERS",
    "GH002": "Отсутствует .github/labels.yml",
    "GH003": "Отсутствует .github/PULL_REQUEST_TEMPLATE.md",
    "GH004": "Отсутствует папка .github/ISSUE_TEMPLATE/",
    "GH005": "Метка типа без Issue Template",
}


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def load_type_labels(repo_root: Path) -> set[str]:
    """Загрузить метки типа из labels.yml."""
    labels_path = repo_root / ".github" / "labels.yml"
    if not labels_path.exists():
        return set()

    type_labels = set()
    with open(labels_path, encoding="utf-8") as f:
        for line in f:
            match = re.search(r'-\s*name:\s*["\']?([a-z0-9-]+)["\']?', line)
            if match and match.group(1) in TYPE_LABELS:
                type_labels.add(match.group(1))

    return type_labels


def get_templates_type_labels(repo_root: Path) -> set[str]:
    """Получить все метки типа из Issue Templates."""
    templates_dir = repo_root / ".github" / "ISSUE_TEMPLATE"
    if not templates_dir.exists():
        return set()

    type_labels = set()
    for template_file in templates_dir.glob("*.yml"):
        if template_file.name == "config.yml":
            continue

        with open(template_file, encoding="utf-8") as f:
            content = f.read()
            # Формат 1: labels: [bug, ...]
            match = re.search(r'labels:\s*\[(.*?)\]', content)
            if match:
                for label in re.findall(r'[a-z0-9-]+', match.group(1)):
                    if label in TYPE_LABELS:
                        type_labels.add(label)
            # Формат 2: labels:\n  - bug
            for label_match in re.finditer(r'^\s*-\s*([a-z0-9-]+)\s*$', content, re.MULTILINE):
                if label_match.group(1) in TYPE_LABELS:
                    type_labels.add(label_match.group(1))

    return type_labels


def check_required_files(repo_root: Path) -> list[str]:
    """Проверить наличие обязательных файлов."""
    errors = []
    github_dir = repo_root / ".github"

    # GH001: CODEOWNERS
    if not (github_dir / "CODEOWNERS").exists():
        errors.append("[GH001] Отсутствует .github/CODEOWNERS")

    # GH002: labels.yml
    if not (github_dir / "labels.yml").exists():
        errors.append("[GH002] Отсутствует .github/labels.yml")

    # GH003: PULL_REQUEST_TEMPLATE.md
    if not (github_dir / "PULL_REQUEST_TEMPLATE.md").exists():
        errors.append("[GH003] Отсутствует .github/PULL_REQUEST_TEMPLATE.md")

    # GH004: ISSUE_TEMPLATE/
    templates_dir = github_dir / "ISSUE_TEMPLATE"
    if not templates_dir.exists():
        errors.append("[GH004] Отсутствует папка .github/ISSUE_TEMPLATE/")
    else:
        # GH005: Проверить соответствие меток типа и шаблонов
        type_labels = load_type_labels(repo_root)
        templates_labels = get_templates_type_labels(repo_root)

        missing = type_labels - templates_labels
        for label in sorted(missing):
            errors.append(f"[GH005] {label}: нет Issue Template")

    return errors


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    repo_root = find_repo_root(Path.cwd())

    print("🔍 Проверка обязательных файлов GitHub...")
    errors = check_required_files(repo_root)

    if errors:
        print("\n❌ Отсутствуют обязательные файлы:")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("✅ Все обязательные файлы GitHub на месте")
        sys.exit(0)


if __name__ == "__main__":
    main()
