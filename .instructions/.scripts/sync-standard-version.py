#!/usr/bin/env python3
"""
sync-standard-version.py — Синхронизация версий стандартов.

Находит все файлы, зависящие от указанного стандарта, и обновляет их
standard-version до актуальной версии стандарта.

Использование:
    python sync-standard-version.py <standard-file>
    python sync-standard-version.py .instructions/standard-instruction.md
    python sync-standard-version.py --check  # только проверка расхождений

Примеры:
    python sync-standard-version.py .instructions/standard-instruction.md
    python sync-standard-version.py .claude/.instructions/agents/standard-agent.md

Возвращает:
    0 — все файлы синхронизированы
    1 — есть расхождения (при --check) или ошибка
"""

import argparse
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

VERSION_PATTERN = re.compile(r"^Версия стандарта:\s*(\d+\.\d+)", re.MULTILINE)
WORKING_VERSION_PATTERN = re.compile(r"^Рабочая версия стандарта:\s*(\d+\.\d+)", re.MULTILINE)
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


def get_file_standard_version(file_path: Path) -> str | None:
    """Извлечь standard-version из frontmatter файла."""
    try:
        content = file_path.read_text(encoding="utf-8")
        fm_match = FRONTMATTER_PATTERN.match(content)
        if fm_match:
            frontmatter = fm_match.group(1)
            sv_match = STANDARD_VERSION_PATTERN.search(frontmatter)
            if sv_match:
                return sv_match.group(1)
        return None
    except Exception:
        return None


def get_file_standard_path(file_path: Path) -> str | None:
    """Извлечь standard из frontmatter файла."""
    try:
        content = file_path.read_text(encoding="utf-8")
        fm_match = FRONTMATTER_PATTERN.match(content)
        if fm_match:
            frontmatter = fm_match.group(1)
            match = re.search(r"^standard:\s*(.+)$", frontmatter, re.MULTILINE)
            if match:
                return match.group(1).strip()
        return None
    except Exception:
        return None


def find_dependent_files(repo_root: Path, standard_path: str) -> list[Path]:
    """Найти все файлы, зависящие от указанного стандарта."""
    dependent = []

    # Нормализовать путь стандарта
    standard_normalized = standard_path.replace("\\", "/").lstrip("./")

    for md_file in repo_root.rglob("*.md"):
        # Пропустить node_modules, .git и сам стандарт
        if any(part.startswith(".git") or part == "node_modules" for part in md_file.parts):
            continue

        file_standard = get_file_standard_path(md_file)
        if file_standard:
            file_standard_normalized = file_standard.replace("\\", "/").lstrip("./")
            if file_standard_normalized == standard_normalized:
                dependent.append(md_file)

    return dependent


def update_file_version(file_path: Path, new_version: str) -> bool:
    """Обновить standard-version и рабочую версию в файле."""
    try:
        content = file_path.read_text(encoding="utf-8")

        # Обновить standard-version в frontmatter
        def replace_frontmatter_version(match):
            frontmatter = match.group(1)
            updated = re.sub(
                r"^(standard-version:\s*)v?\d+\.\d+",
                f"\\g<1>v{new_version}",
                frontmatter,
                flags=re.MULTILINE
            )
            return f"---\n{updated}\n---"

        content = FRONTMATTER_PATTERN.sub(replace_frontmatter_version, content)

        # Обновить рабочую версию в теле
        content = re.sub(
            r"^(Рабочая версия стандарта:\s*)\d+\.\d+",
            f"\\g<1>{new_version}",
            content,
            flags=re.MULTILINE
        )

        file_path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Ошибка при обновлении {file_path}: {e}", file=sys.stderr)
        return False


# =============================================================================
# Main
# =============================================================================

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Синхронизация версий стандартов"
    )
    parser.add_argument(
        "standard",
        nargs="?",
        help="Путь к файлу стандарта (standard-*.md)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Только проверка расхождений, без изменений"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if not args.standard:
        print("Укажите путь к стандарту", file=sys.stderr)
        sys.exit(1)

    standard_path = Path(args.standard)
    if not standard_path.is_absolute():
        standard_path = repo_root / standard_path

    if not standard_path.exists():
        print(f"Файл не найден: {standard_path}", file=sys.stderr)
        sys.exit(1)

    # Получить версию стандарта
    version = get_standard_version(standard_path)
    if not version:
        print(f"Не найдена 'Версия стандарта:' в {standard_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Стандарт: {standard_path.relative_to(repo_root)}")
    print(f"Версия: {version}")
    print()

    # Найти зависимые файлы
    standard_rel = str(standard_path.relative_to(repo_root)).replace("\\", "/")
    dependent_files = find_dependent_files(repo_root, standard_rel)

    if not dependent_files:
        print("Зависимых файлов не найдено")
        sys.exit(0)

    # Проверить расхождения
    outdated = []
    for dep_file in dependent_files:
        file_version = get_file_standard_version(dep_file)
        if file_version != version:
            outdated.append((dep_file, file_version))

    if not outdated:
        print(f"✅ Все {len(dependent_files)} файлов синхронизированы")
        sys.exit(0)

    # Вывести список устаревших
    print(f"Устаревших файлов: {len(outdated)}/{len(dependent_files)}")
    print()

    for dep_file, file_version in outdated:
        rel_path = dep_file.relative_to(repo_root)
        print(f"  {rel_path}: v{file_version or '?'} → v{version}")

    if args.check:
        sys.exit(1)

    print()

    # Обновить файлы
    updated = 0
    for dep_file, _ in outdated:
        if update_file_version(dep_file, version):
            updated += 1
            rel_path = dep_file.relative_to(repo_root)
            print(f"✅ Обновлён: {rel_path}")

    print()
    print(f"Обновлено: {updated}/{len(outdated)}")

    sys.exit(0 if updated == len(outdated) else 1)


if __name__ == "__main__":
    main()
