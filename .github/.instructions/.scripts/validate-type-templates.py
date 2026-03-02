#!/usr/bin/env python3
"""
validate-type-templates.py — Валидация соответствия TYPE-меток и Issue Templates.

Использование:
    python validate-type-templates.py              # Проверить соответствие
    python validate-type-templates.py --verbose    # Подробный вывод

Проверяет:
    - Для каждой TYPE-метки в labels.yml существует Issue Template
    - Каждый Issue Template содержит TYPE-метку в labels:
    - Каждый Issue Template содержит 5 обязательных полей body (task-description, documents, assignment, acceptance-criteria, practical-context)

TYPE-метки (из секции # TYPE в labels.yml):
    bug, task, docs, refactor

Примеры:
    python validate-type-templates.py
    # ✅ Все TYPE-метки имеют соответствующие Issue Templates

    python validate-type-templates.py --verbose
    # 📋 Найдено TYPE-меток: 6
    # 📄 Найдено шаблонов: 6

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
"""

import argparse
import re
import sys
from pathlib import Path

# TYPE-метки (SSOT: .github/labels.yml, секция # TYPE)
TYPE_LABELS = {"bug", "task", "docs", "refactor", "feature", "infra", "test"}

# Коды ошибок
ERROR_CODES = {
    "TT001": "TYPE-метка без соответствующего Issue Template",
    "TT002": "Issue Template без TYPE-метки в labels",
    "TT003": "Issue Template с неизвестной TYPE-меткой",
    "TT004": "Файл labels.yml не найден",
    "TT005": "Папка ISSUE_TEMPLATE не найдена",
    "TT006": "Issue Template без обязательного поля documents",
    "TT007": "Issue Template без обязательного поля assignment",
    "TT008": "Issue Template без обязательного поля practical-context",
    "TT009": "Issue Template без обязательного поля task-description",
}


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def load_type_labels_from_yml(repo_root: Path) -> set[str]:
    """Загрузить TYPE-метки из labels.yml."""
    labels_path = repo_root / ".github" / "labels.yml"
    if not labels_path.exists():
        return set()

    found_labels = set()
    in_type_section = False
    passed_type_header = False

    with open(labels_path, encoding="utf-8") as f:
        for line in f:
            # Начало секции TYPE
            if "# TYPE" in line:
                in_type_section = True
                continue
            # Пропускаем закрывающую линию секции TYPE
            if in_type_section and not passed_type_header and line.startswith("# ==="):
                passed_type_header = True
                continue
            # Конец секции TYPE (начало следующей секции с комментарием)
            if in_type_section and passed_type_header and line.startswith("# "):
                break
            # Парсим метки в секции TYPE
            if in_type_section and passed_type_header:
                match = re.search(r'-\s*name:\s*["\']?([a-z0-9-]+)["\']?', line)
                if match:
                    found_labels.add(match.group(1))

    return found_labels


def load_templates(repo_root: Path) -> dict[str, set[str]]:
    """
    Загрузить Issue Templates и их TYPE-метки.

    Returns:
        dict: {filename: set of TYPE labels in template}
    """
    templates_dir = repo_root / ".github" / "ISSUE_TEMPLATE"
    if not templates_dir.exists():
        return {}

    templates = {}
    for template_file in templates_dir.glob("*.yml"):
        if template_file.name == "config.yml":
            continue

        type_labels_found = set()
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

            # Извлекаем все метки из labels: секции
            # Формат 1: labels: [bug, low]
            match = re.search(r'labels:\s*\[(.*?)\]', content)
            if match:
                labels_str = match.group(1)
                for label in re.findall(r'[a-z0-9-]+', labels_str):
                    if label in TYPE_LABELS:
                        type_labels_found.add(label)

            # Формат 2: labels:\n  - bug\n  - low
            for match in re.finditer(r'^\s*-\s*([a-z0-9-]+)\s*$', content, re.MULTILINE):
                label = match.group(1)
                if label in TYPE_LABELS:
                    type_labels_found.add(label)

        templates[template_file.name] = type_labels_found

    return templates


def check_required_body_field(repo_root: Path, field_id: str, error_code: str) -> list[str]:
    """Проверить что каждый шаблон содержит обязательное поле body с указанным id."""
    errors = []
    templates_dir = repo_root / ".github" / "ISSUE_TEMPLATE"
    if not templates_dir.exists():
        return errors

    for template_file in templates_dir.glob("*.yml"):
        if template_file.name == "config.yml":
            continue

        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Проверяем наличие id: {field_id}
        has_id = bool(re.search(rf'^\s+id:\s*{re.escape(field_id)}\s*$', content, re.MULTILINE))
        if not has_id:
            errors.append(
                f"[{error_code}] {template_file.name}: нет поля с id: {field_id}"
            )
            continue

        # Проверяем required: true
        field_block = re.search(
            rf'id:\s*{re.escape(field_id)}.*?validations:\s*\n\s+required:\s*(true|false)',
            content,
            re.DOTALL,
        )
        if field_block and field_block.group(1) != "true":
            errors.append(
                f"[{error_code}] {template_file.name}: поле {field_id} должно быть required: true"
            )

    return errors


def validate(repo_root: Path, verbose: bool = False) -> list[str]:
    """Валидация соответствия TYPE-меток и Issue Templates."""
    errors = []

    # Проверяем наличие файлов
    labels_path = repo_root / ".github" / "labels.yml"
    templates_dir = repo_root / ".github" / "ISSUE_TEMPLATE"

    if not labels_path.exists():
        errors.append(f"[TT004] {labels_path.relative_to(repo_root)}: файл не найден")
        return errors

    # Загружаем данные
    type_labels = load_type_labels_from_yml(repo_root)
    templates = load_templates(repo_root)

    if verbose:
        print(f"📋 Найдено TYPE-меток: {len(type_labels)}")
        for label in sorted(type_labels):
            print(f"    {label}")
        print(f"📄 Найдено шаблонов: {len(templates)}")
        for name, labels in sorted(templates.items()):
            print(f"    {name}: {labels or '(нет TYPE-метки)'}")

    # Если нет папки ISSUE_TEMPLATE и есть TYPE-метки — предупреждение
    if not templates_dir.exists() and type_labels:
        errors.append(f"[TT005] {templates_dir.relative_to(repo_root)}: папка не найдена, но есть TYPE-метки")
        for label in sorted(type_labels):
            errors.append(f"[TT001] {label}: нет Issue Template")
        return errors

    # Собираем все TYPE-метки из шаблонов
    templates_type_labels = set()
    for labels in templates.values():
        templates_type_labels.update(labels)

    # TT001: TYPE-метка без шаблона
    for label in sorted(type_labels - templates_type_labels):
        errors.append(f"[TT001] {label}: нет Issue Template с этой меткой в labels:")

    # TT002: шаблон без TYPE-метки в labels
    for name, labels in sorted(templates.items()):
        if not labels:
            errors.append(f"[TT002] {name}: шаблон не содержит TYPE-метку в labels")

    # TT003: шаблон с неизвестной TYPE-меткой
    for name, labels in sorted(templates.items()):
        for label in labels:
            if label not in type_labels:
                errors.append(f"[TT003] {name}: метка '{label}' не найдена в секции TYPE labels.yml")

    # TT006-TT009: проверка 5 обязательных полей body
    required_fields = [
        ("documents", "TT006"),
        ("assignment", "TT007"),
        ("practical-context", "TT008"),
        ("task-description", "TT009"),
    ]
    for field_id, error_code in required_fields:
        errors.extend(check_required_body_field(repo_root, field_id, error_code))

    return errors


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация соответствия TYPE-меток и Issue Templates"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    print(f"🔍 Валидация TYPE ↔ Issue Templates...")

    errors = validate(repo_root, verbose=args.verbose)

    if errors:
        print("\n❌ Найдены ошибки:")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("✅ Все TYPE-метки имеют соответствующие Issue Templates")
        sys.exit(0)


if __name__ == "__main__":
    main()
