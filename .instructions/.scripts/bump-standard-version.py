#!/usr/bin/env python3
"""
bump-standard-version.py — Увеличение версии стандарта.

Увеличивает версию стандарта (minor или major) с учётом git staging.
Если файл уже изменён в staging — версия не увеличивается повторно.

Использование:
    python bump-standard-version.py <standard-file> [--major] [--check]
    python bump-standard-version.py .instructions/standard-instruction.md
    python bump-standard-version.py .instructions/standard-instruction.md --major
    python bump-standard-version.py .instructions/standard-instruction.md --check

Примеры:
    python bump-standard-version.py .instructions/standard-instruction.md
    # 1.0 → 1.1

    python bump-standard-version.py .instructions/standard-instruction.md --major
    # 1.5 → 2.0

    python bump-standard-version.py .instructions/standard-instruction.md --check
    # Показывает текущую версию без изменения

Возвращает:
    0 — версия увеличена (или --check успешно)
    1 — ошибка или файл уже в staging
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

VERSION_PATTERN = re.compile(r"^(Версия стандарта:\s*)(\d+)\.(\d+)", re.MULTILINE)


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


def is_file_staged(file_path: Path, repo_root: Path) -> bool:
    """Проверить, есть ли файл в git staging."""
    try:
        rel_path = file_path.relative_to(repo_root)
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        staged_files = result.stdout.strip().split("\n")
        rel_str = str(rel_path).replace("\\", "/")
        return rel_str in staged_files
    except Exception:
        return False


def get_current_version(file_path: Path) -> tuple[int, int] | None:
    """Получить текущую версию (major, minor)."""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = VERSION_PATTERN.search(content)
        if match:
            return int(match.group(2)), int(match.group(3))
        return None
    except Exception:
        return None


def update_version(file_path: Path, major: int, minor: int) -> bool:
    """Обновить версию в файле."""
    try:
        content = file_path.read_text(encoding="utf-8")

        def replace_version(match):
            return f"{match.group(1)}{major}.{minor}"

        new_content = VERSION_PATTERN.sub(replace_version, content)
        file_path.write_text(new_content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Ошибка при обновлении: {e}", file=sys.stderr)
        return False


# =============================================================================
# Main
# =============================================================================

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Увеличение версии стандарта"
    )
    parser.add_argument(
        "standard",
        help="Путь к файлу стандарта (standard-*.md)"
    )
    parser.add_argument(
        "--major",
        action="store_true",
        help="Увеличить major версию (X.0)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Только показать текущую версию (без изменения)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Игнорировать проверку git staging"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    standard_path = Path(args.standard)
    if not standard_path.is_absolute():
        standard_path = repo_root / standard_path

    if not standard_path.exists():
        print(f"Файл не найден: {standard_path}", file=sys.stderr)
        sys.exit(1)

    # Проверить staging
    if not args.force and is_file_staged(standard_path, repo_root):
        rel_path = standard_path.relative_to(repo_root)
        print(f"⚠️  Файл уже в staging: {rel_path}")
        print("   Версия не увеличена (один раз за коммит)")
        print("   Используйте --force для принудительного увеличения")
        sys.exit(1)

    # Получить текущую версию
    current = get_current_version(standard_path)
    if not current:
        print(f"Не найдена 'Версия стандарта:' в {standard_path}", file=sys.stderr)
        sys.exit(1)

    major, minor = current
    rel_path = standard_path.relative_to(repo_root)

    # Режим --check: только показать версию
    if args.check:
        print(f"{rel_path}: v{major}.{minor}")
        sys.exit(0)

    # Вычислить новую версию
    if args.major:
        new_major = major + 1
        new_minor = 0
    else:
        new_major = major
        new_minor = minor + 1

    # Обновить
    if update_version(standard_path, new_major, new_minor):
        print(f"✅ {rel_path}: {major}.{minor} → {new_major}.{new_minor}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
