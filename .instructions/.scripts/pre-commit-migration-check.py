#!/usr/bin/env python3
"""
pre-commit-migration-check.py — Проверка миграции перед коммитом.

Проверяет, что при изменении standard-*.md файла выполнена миграция
зависимых файлов. Предназначен для использования в git pre-commit hook.

Использование:
    python pre-commit-migration-check.py
    python pre-commit-migration-check.py --verbose

Примеры:
    python pre-commit-migration-check.py
    python pre-commit-migration-check.py --verbose

Возвращает:
    0 — миграция не требуется или выполнена
    1 — есть несинхронизированные файлы
"""

import argparse
import re
import subprocess
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


def get_staged_files() -> list[str]:
    """Получить список staged файлов."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
    except subprocess.CalledProcessError:
        return []


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


def find_all_md_files(repo_root: Path) -> list[Path]:
    """Найти все .md файлы."""
    files = []
    for md_file in repo_root.rglob("*.md"):
        if any(part.startswith(".git") or part == "node_modules" for part in md_file.parts):
            continue
        files.append(md_file)
    return files


def check_migration_for_standard(
    standard_path: str,
    standard_version: str,
    repo_root: Path,
    verbose: bool = False
) -> list[dict]:
    """Проверить миграцию для конкретного стандарта."""
    drifts = []
    all_files = find_all_md_files(repo_root)

    for file_path in all_files:
        standard, file_version = get_file_info(file_path)
        if not standard:
            continue

        # Нормализовать путь
        standard_normalized = standard.replace("\\", "/").lstrip("./")

        if standard_normalized != standard_path:
            continue

        rel_path = str(file_path.relative_to(repo_root)).replace("\\", "/")

        if file_version != standard_version:
            drifts.append({
                "file": rel_path,
                "version": file_version,
                "expected": standard_version
            })
            if verbose:
                print(f"  ❌ {rel_path}: v{file_version or '?'} → v{standard_version}")
        elif verbose:
            print(f"  ✅ {rel_path}: v{file_version}")

    return drifts


# =============================================================================
# Main
# =============================================================================

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Проверка миграции перед коммитом"
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

    # Получить staged файлы
    staged = get_staged_files()
    if not staged:
        if args.verbose:
            print("Нет staged файлов")
        sys.exit(0)

    # Найти изменённые стандарты
    changed_standards = []
    for file in staged:
        file_normalized = file.replace("\\", "/")
        if "/standard-" in file_normalized and file_normalized.endswith(".md"):
            changed_standards.append(file_normalized)

    if not changed_standards:
        if args.verbose:
            print("Стандарты не изменены")
        sys.exit(0)

    # Проверить миграцию для каждого изменённого стандарта
    all_drifts = []

    for std_path in changed_standards:
        full_path = repo_root / std_path
        if not full_path.exists():
            continue

        version = get_standard_version(full_path)
        if not version:
            continue

        if args.verbose:
            print(f"\n## {std_path} (v{version})")

        drifts = check_migration_for_standard(
            std_path,
            version,
            repo_root,
            verbose=args.verbose
        )
        all_drifts.extend(drifts)

    if not all_drifts:
        print("✅ Миграция выполнена корректно")
        sys.exit(0)

    print(f"\n❌ Обнаружено несинхронизированных файлов: {len(all_drifts)}")
    print("\nДля синхронизации выполните:")
    for std_path in changed_standards:
        print(f"  /migration-create {std_path}")
    print("\nИли отключите проверку: git commit --no-verify")

    sys.exit(1)


if __name__ == "__main__":
    main()
