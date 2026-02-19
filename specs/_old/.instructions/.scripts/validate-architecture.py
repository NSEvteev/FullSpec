#!/usr/bin/env python3
"""
validate-architecture.py — Валидация фиксированных файлов архитектуры.

Использование:
    python validate-architecture.py              # Структурная валидация
    python validate-architecture.py --verbose    # Подробный вывод
    python validate-architecture.py --check-services  # + проверка согласованности services/

Проверяет:
    - AC001: 4 фиксированных файла существуют
    - AC002: Каждый файл содержит frontmatter
    - AC003: Frontmatter содержит description
    - AC004: Обязательные секции присутствуют
    - AC005: Секция "Planned Changes" присутствует
    - AC006: Новые файлы в specs/services/ сопровождаются изменениями в architecture/ (--check-services)

SSOT:
    - specs/.instructions/living-docs/architecture/standard-architecture.md
    - specs/.instructions/living-docs/architecture/validation-architecture.md

Примеры:
    python validate-architecture.py
    # ✅ Все фиксированные файлы архитектуры валидны

    python validate-architecture.py --check-services --verbose
    # 📁 Проверка 4 фиксированных файлов...
    # 🔗 Проверка согласованности services/...

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Коды ошибок
ERROR_CODES = {
    "AC001": "Фиксированный файл отсутствует",
    "AC002": "Отсутствует frontmatter",
    "AC003": "Отсутствует description в frontmatter",
    "AC004": "Отсутствует обязательная секция",
    "AC005": "Нет секции 'Planned Changes'",
    "AC006": "Новая папка specs/services/ без изменений в architecture/",
}

# Фиксированные файлы и их обязательные секции (заголовки ##)
FIXED_FILES = {
    "system/overview.md": ["Домены и сервисы", "Потоки данных", "Инфраструктура", "Planned Changes"],
    "system/data-flows.md": ["Planned Changes"],
    "system/infrastructure.md": ["Deployment", "Networking", "Мониторинг", "Planned Changes"],
    "domains/context-map.md": ["Домены", "Связи между контекстами", "Planned Changes"],
}


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def parse_frontmatter(content: str) -> dict | None:
    """Извлечь frontmatter из markdown-файла."""
    if not content.startswith("---"):
        return None

    end = content.find("---", 3)
    if end == -1:
        return None

    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.split("\n"):
        match = re.match(r"^(\w[\w-]*):\s*(.+)$", line.strip())
        if match:
            result[match.group(1)] = match.group(2).strip()

    return result


def extract_h2_sections(content: str) -> list[str]:
    """Извлечь все заголовки ## из markdown-файла."""
    sections = []
    for line in content.split("\n"):
        match = re.match(r"^##\s+(.+)$", line.strip())
        if match:
            sections.append(match.group(1).strip())
    return sections


def validate_structure(repo_root: Path, verbose: bool = False) -> list[str]:
    """Структурная валидация фиксированных файлов (AC001-AC005)."""
    errors = []
    arch_dir = repo_root / "specs" / "architecture"

    if verbose:
        print(f"📁 Проверка {len(FIXED_FILES)} фиксированных файлов...")

    for rel_path, required_sections in FIXED_FILES.items():
        file_path = arch_dir / rel_path

        # AC001: файл существует
        if not file_path.exists():
            errors.append(
                f"[AC001] {rel_path}: фиксированный файл отсутствует"
            )
            continue

        content = file_path.read_text(encoding="utf-8")

        if verbose:
            print(f"  ✓ {rel_path} — существует")

        # AC002: frontmatter существует
        fm = parse_frontmatter(content)
        if fm is None:
            errors.append(
                f"[AC002] {rel_path}: отсутствует frontmatter"
            )
        else:
            # AC003: description в frontmatter
            if "description" not in fm or not fm["description"]:
                errors.append(
                    f"[AC003] {rel_path}: отсутствует description в frontmatter"
                )
            elif verbose:
                print(f"    frontmatter: description ✓")

        # AC004/AC005: обязательные секции
        h2_sections = extract_h2_sections(content)

        for section in required_sections:
            if section == "Planned Changes":
                # AC005: специальный код для Planned Changes
                if not any(s == "Planned Changes" for s in h2_sections):
                    errors.append(
                        f"[AC005] {rel_path}: нет секции 'Planned Changes'"
                    )
                elif verbose:
                    print(f"    секция: Planned Changes ✓")
            else:
                # AC004: обязательная секция
                if not any(s == section for s in h2_sections):
                    errors.append(
                        f"[AC004] {rel_path}: отсутствует обязательная секция '{section}'"
                    )
                elif verbose:
                    print(f"    секция: {section} ✓")

    return errors


def validate_services_consistency(repo_root: Path, verbose: bool = False) -> list[str]:
    """Проверка согласованности: новые файлы в services/ сопровождаются изменениями в architecture/ (AC006)."""
    errors = []

    if verbose:
        print("🔗 Проверка согласованности services/...")

    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
            capture_output=True,
            encoding="utf-8",
            cwd=repo_root,
        )
        if result.returncode != 0:
            if verbose:
                print("  ⚠ git diff не удался, пропускаем проверку AC006")
            return errors

        staged_new = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except FileNotFoundError:
        if verbose:
            print("  ⚠ git не найден, пропускаем проверку AC006")
        return errors

    # Найти новые файлы в specs/services/ (не .gitkeep)
    new_service_files = [
        f for f in staged_new
        if f.startswith("specs/services/")
        and not f.endswith(".gitkeep")
        and "/" in f[len("specs/services/"):]  # есть подпапка (svc/файл)
    ]

    if not new_service_files:
        if verbose:
            print("  Нет новых файлов в specs/services/")
        return errors

    # Проверить что хотя бы один файл architecture/ тоже staged
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            encoding="utf-8",
            cwd=repo_root,
        )
        staged_all = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except FileNotFoundError:
        return errors

    arch_staged = [f for f in staged_all if f.startswith("specs/architecture/")]

    if not arch_staged:
        # Извлечь имена сервисов
        service_names = set()
        for f in new_service_files:
            parts = f[len("specs/services/"):].split("/")
            if parts:
                service_names.add(parts[0])

        for svc in sorted(service_names):
            errors.append(
                f"[AC006] specs/services/{svc}/: новые файлы добавлены, "
                f"но specs/architecture/ не обновлён"
            )
    elif verbose:
        print(f"  ✓ architecture/ обновлён ({len(arch_staged)} файлов staged)")

    return errors


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация фиксированных файлов архитектуры"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    parser.add_argument(
        "--check-services", action="store_true",
        help="Проверить согласованность с specs/services/ (AC006)"
    )
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    print("🔍 Валидация фиксированных файлов архитектуры...")

    errors = validate_structure(repo_root, verbose=args.verbose)

    if args.check_services:
        errors.extend(validate_services_consistency(repo_root, verbose=args.verbose))

    if errors:
        print(f"\n❌ Найдено ошибок: {len(errors)}")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("✅ Все фиксированные файлы архитектуры валидны")
        sys.exit(0)


if __name__ == "__main__":
    main()
