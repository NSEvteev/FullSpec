#!/usr/bin/env python3
"""
check-version-drift.py — Проверка расхождения версий стандартов.

Проверяет все стандарты и их зависимые файлы на расхождение версий.
Предназначен для использования в CI/CD.

Использование:
    python check-version-drift.py
    python check-version-drift.py --verbose

Возвращает:
    0 — все версии синхронизированы
    1 — есть расхождения
"""

import argparse
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

VERSION_PATTERN = re.compile(r"^Версия стандарта:\s*(\d+\.\d+)", re.MULTILINE)
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
STANDARD_VERSION_PATTERN = re.compile(r"^standard-version:\s*v?(\d+\.\d+)", re.MULTILINE)


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


def get_standard_version(file_path: Path) -> str | None:
    """Извлечь версию из строки 'Версия стандарта: X.Y'."""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = VERSION_PATTERN.search(content)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None


def get_file_info(file_path: Path) -> tuple[str | None, str | None]:
    """Извлечь standard и standard-version из frontmatter."""
    try:
        content = file_path.read_text(encoding="utf-8")
        fm_match = FRONTMATTER_PATTERN.match(content)
        if fm_match:
            frontmatter = fm_match.group(1)

            standard = None
            match = re.search(r"^standard:\s*(.+)$", frontmatter, re.MULTILINE)
            if match:
                standard = match.group(1).strip()

            version = None
            sv_match = STANDARD_VERSION_PATTERN.search(frontmatter)
            if sv_match:
                version = sv_match.group(1)

            return standard, version
        return None, None
    except Exception:
        return None, None


def find_all_standards(repo_root: Path) -> list[Path]:
    """Найти все файлы standard-*.md."""
    standards = []
    for md_file in repo_root.rglob("standard-*.md"):
        if any(part.startswith(".git") or part == "node_modules" for part in md_file.parts):
            continue
        standards.append(md_file)
    return standards


def find_all_md_files(repo_root: Path) -> list[Path]:
    """Найти все .md файлы."""
    files = []
    for md_file in repo_root.rglob("*.md"):
        if any(part.startswith(".git") or part == "node_modules" for part in md_file.parts):
            continue
        files.append(md_file)
    return files


# =============================================================================
# Main
# =============================================================================

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Проверка расхождения версий стандартов"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Подробный вывод"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Найти все стандарты и их версии
    standards = find_all_standards(repo_root)
    standard_versions = {}

    for std_path in standards:
        version = get_standard_version(std_path)
        rel_path = str(std_path.relative_to(repo_root)).replace("\\", "/")
        if version:
            standard_versions[rel_path] = version
            if args.verbose:
                print(f"Стандарт: {rel_path} = v{version}")

    if args.verbose:
        print()

    # Проверить все файлы
    all_files = find_all_md_files(repo_root)
    drifts = []

    for file_path in all_files:
        standard, file_version = get_file_info(file_path)
        if not standard:
            continue

        # Нормализовать путь
        standard_normalized = standard.replace("\\", "/").lstrip("./")

        # Найти версию стандарта
        expected_version = standard_versions.get(standard_normalized)
        if not expected_version:
            continue

        if file_version != expected_version:
            rel_path = file_path.relative_to(repo_root)
            drifts.append({
                "file": str(rel_path),
                "standard": standard_normalized,
                "current": file_version,
                "expected": expected_version
            })

    # Вывод результатов
    if not drifts:
        print(f"✅ Все версии синхронизированы ({len(all_files)} файлов проверено)")
        sys.exit(0)

    print(f"❌ Обнаружено расхождений: {len(drifts)}")
    print()

    # Группировка по стандартам
    by_standard = {}
    for drift in drifts:
        std = drift["standard"]
        if std not in by_standard:
            by_standard[std] = []
        by_standard[std].append(drift)

    for std, files in by_standard.items():
        expected = files[0]["expected"]
        print(f"## {std} (v{expected})")
        for drift in files:
            current = drift["current"] or "?"
            print(f"   {drift['file']}: v{current}")
        print()

    print("Для синхронизации выполните:")
    for std in by_standard.keys():
        print(f"  python .instructions/.scripts/sync-standard-version.py {std}")

    sys.exit(1)


if __name__ == "__main__":
    main()
