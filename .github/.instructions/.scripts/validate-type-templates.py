#!/usr/bin/env python3
"""
validate-type-templates.py — Валидация соответствия type:* меток и Issue Templates.

Использование:
    python validate-type-templates.py              # Проверить соответствие
    python validate-type-templates.py --verbose    # Подробный вывод

Проверяет:
    - Для каждой метки type:* в labels.yml существует Issue Template
    - Каждый Issue Template содержит labels: [type:{value}]

Примеры:
    python validate-type-templates.py
    # ✅ Все метки type:* имеют соответствующие Issue Templates

    python validate-type-templates.py --verbose
    # 📋 Найдено меток type:*: 6
    # 📄 Найдено шаблонов: 6

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
    "TT001": "Метка type:* без соответствующего Issue Template",
    "TT002": "Issue Template без метки type:* в labels",
    "TT003": "Issue Template с неизвестной меткой type:*",
    "TT004": "Файл labels.yml не найден",
    "TT005": "Папка ISSUE_TEMPLATE не найдена",
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
    """Загрузить метки type:* из labels.yml."""
    labels_path = repo_root / ".github" / "labels.yml"
    if not labels_path.exists():
        return set()

    type_labels = set()
    with open(labels_path, encoding="utf-8") as f:
        for line in f:
            # Ищем строки вида: - name: "type:value" или - name: type:value
            match = re.search(r'-\s*name:\s*["\']?(type:[a-z0-9-]+)["\']?', line)
            if match:
                type_labels.add(match.group(1))

    return type_labels


def load_templates(repo_root: Path) -> dict[str, set[str]]:
    """
    Загрузить Issue Templates и их метки type:*.

    Returns:
        dict: {filename: set of type:* labels in template}
    """
    templates_dir = repo_root / ".github" / "ISSUE_TEMPLATE"
    if not templates_dir.exists():
        return {}

    templates = {}
    for template_file in templates_dir.glob("*.yml"):
        if template_file.name == "config.yml":
            continue

        type_labels = set()
        with open(template_file, encoding="utf-8") as f:
            content = f.read()
            # Ищем labels: [...] и извлекаем type:*
            # Поддерживаем форматы:
            # labels: [type:bug, priority:high]
            # labels:
            #   - type:bug
            #   - priority:high

            # Формат 1: однострочный
            match = re.search(r'labels:\s*\[(.*?)\]', content)
            if match:
                labels_str = match.group(1)
                for label in re.findall(r'type:[a-z0-9-]+', labels_str):
                    type_labels.add(label)

            # Формат 2: многострочный
            for match in re.finditer(r'^\s*-\s*(type:[a-z0-9-]+)\s*$', content, re.MULTILINE):
                type_labels.add(match.group(1))

        templates[template_file.name] = type_labels

    return templates


def validate(repo_root: Path, verbose: bool = False) -> list[str]:
    """Валидация соответствия type:* и Issue Templates."""
    errors = []

    # Проверяем наличие файлов
    labels_path = repo_root / ".github" / "labels.yml"
    templates_dir = repo_root / ".github" / "ISSUE_TEMPLATE"

    if not labels_path.exists():
        errors.append(f"[TT004] {labels_path.relative_to(repo_root)}: файл не найден")
        return errors

    # Загружаем данные
    type_labels = load_type_labels(repo_root)
    templates = load_templates(repo_root)

    if verbose:
        print(f"📋 Найдено меток type:*: {len(type_labels)}")
        for label in sorted(type_labels):
            print(f"    {label}")
        print(f"📄 Найдено шаблонов: {len(templates)}")
        for name, labels in sorted(templates.items()):
            print(f"    {name}: {labels or '(нет type:*)'}")

    # Если нет папки ISSUE_TEMPLATE и есть метки type:* — предупреждение
    if not templates_dir.exists() and type_labels:
        errors.append(f"[TT005] {templates_dir.relative_to(repo_root)}: папка не найдена, но есть метки type:*")
        for label in sorted(type_labels):
            errors.append(f"[TT001] {label}: нет Issue Template")
        return errors

    # Собираем все type:* из шаблонов
    templates_type_labels = set()
    for labels in templates.values():
        templates_type_labels.update(labels)

    # TT001: метка type:* без шаблона
    for label in sorted(type_labels - templates_type_labels):
        errors.append(f"[TT001] {label}: нет Issue Template с этой меткой в labels:")

    # TT002: шаблон без type:* в labels
    for name, labels in sorted(templates.items()):
        if not labels:
            errors.append(f"[TT002] {name}: шаблон не содержит метку type:* в labels")

    # TT003: шаблон с неизвестной меткой type:*
    for name, labels in sorted(templates.items()):
        for label in labels:
            if label not in type_labels:
                errors.append(f"[TT003] {name}: метка '{label}' не найдена в labels.yml")

    return errors


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация соответствия type:* меток и Issue Templates"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    print(f"🔍 Валидация type:* ↔ Issue Templates...")

    errors = validate(repo_root, verbose=args.verbose)

    if errors:
        print("\n❌ Найдены ошибки:")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("✅ Все метки type:* имеют соответствующие Issue Templates")
        sys.exit(0)


if __name__ == "__main__":
    main()
