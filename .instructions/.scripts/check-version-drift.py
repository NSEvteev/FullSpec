#!/usr/bin/env python3
"""
check-version-drift.py — Проверка расхождения версий стандартов.

Проверяет все стандарты и их зависимые файлы на расхождение версий.
Предназначен для использования в CI/CD и скиллах миграции.

Использование:
    python check-version-drift.py
    python check-version-drift.py --verbose
    python check-version-drift.py <стандарт> --json
    python check-version-drift.py <стандарт> --check

Примеры:
    python check-version-drift.py
    python check-version-drift.py .instructions/standard-instruction.md --json
    python check-version-drift.py .instructions/standard-instruction.md --check

Возвращает:
    0 — все версии синхронизированы
    1 — есть расхождения
"""

import argparse
import json
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


def get_working_version(file_path: Path) -> str | None:
    """Извлечь версию из строки 'Рабочая версия стандарта: X.Y'."""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = WORKING_VERSION_PATTERN.search(content)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None


def find_workflow_files(std_path: Path) -> list[Path]:
    """Найти связанные Workflow файлы (validation, create, modify)."""
    std_dir = std_path.parent
    std_name = std_path.name  # standard-X.md
    base_name = std_name.replace("standard-", "").replace(".md", "")  # X

    workflow_files = []
    for prefix in ["validation", "create", "modify"]:
        related = std_dir / f"{prefix}-{base_name}.md"
        if related.exists():
            workflow_files.append(related)
    return workflow_files


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
        "standard",
        nargs="?",
        help="Путь к конкретному стандарту (опционально)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Подробный вывод"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Только проверка (exit code без вывода)"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Если указан конкретный стандарт
    if args.standard:
        std_input = args.standard.replace("\\", "/")
        if std_input.startswith("./"):
            std_input = std_input[2:]
        std_path = repo_root / std_input
        if not std_path.exists():
            if not args.check and not args.json:
                print(f"❌ Стандарт не найден: {args.standard}")
            sys.exit(1)
        standards = [std_path]
    else:
        standards = find_all_standards(repo_root)

    # Найти версии стандартов
    standard_versions = {}
    for std_path in standards:
        version = get_standard_version(std_path)
        rel_path = str(std_path.relative_to(repo_root)).replace("\\", "/")
        if version:
            standard_versions[rel_path] = version
            if args.verbose and not args.json:
                print(f"Стандарт: {rel_path} = v{version}")

    if args.verbose and not args.json:
        print()

    # ==========================================================================
    # Workflows: проверить validation/create/modify (Рабочая версия стандарта)
    # ==========================================================================
    workflow_drifts = []
    workflow_ok = []

    for std_path in standards:
        std_version = get_standard_version(std_path)
        if not std_version:
            continue

        rel_std = str(std_path.relative_to(repo_root)).replace("\\", "/")
        workflow_files = find_workflow_files(std_path)

        for wf_file in workflow_files:
            working_version = get_working_version(wf_file)
            rel_wf = str(wf_file.relative_to(repo_root)).replace("\\", "/")

            if working_version != std_version:
                workflow_drifts.append({
                    "file": rel_wf,
                    "standard": rel_std,
                    "version": working_version,
                    "expected": std_version,
                    "type": "workflow"
                })
            else:
                workflow_ok.append({
                    "file": rel_wf,
                    "standard": rel_std,
                    "version": working_version,
                    "type": "workflow"
                })

    # ==========================================================================
    # Экземпляры: проверить (frontmatter standard-version)
    # ==========================================================================
    all_files = find_all_md_files(repo_root)
    drifts = []
    ok_files = []

    for file_path in all_files:
        standard, file_version = get_file_info(file_path)
        if not standard:
            continue

        # Нормализовать путь (removeprefix вместо lstrip чтобы не убрать .claude/)
        standard_normalized = standard.replace("\\", "/")
        if standard_normalized.startswith("./"):
            standard_normalized = standard_normalized[2:]

        # Фильтр по конкретному стандарту
        if args.standard:
            target_std = args.standard.replace("\\", "/")
            if target_std.startswith("./"):
                target_std = target_std[2:]
            if standard_normalized != target_std:
                continue

        # Найти версию стандарта
        expected_version = standard_versions.get(standard_normalized)
        if not expected_version:
            continue

        rel_path = str(file_path.relative_to(repo_root)).replace("\\", "/")

        if file_version != expected_version:
            drifts.append({
                "file": rel_path,
                "standard": standard_normalized,
                "version": file_version,
                "expected": expected_version,
                "status": "outdated"
            })
        else:
            ok_files.append({
                "file": rel_path,
                "standard": standard_normalized,
                "version": file_version,
                "status": "ok"
            })

    # Объединить все расхождения
    all_drifts = workflow_drifts + drifts
    all_ok = workflow_ok + ok_files

    # Вывод результатов
    if args.json:
        # JSON формат
        result = {
            "workflows": {
                "drifts": workflow_drifts,
                "ok": workflow_ok
            },
            "instances": {
                "drifts": drifts,
                "ok": ok_files
            },
            "summary": {
                "workflow_drifts": len(workflow_drifts),
                "instance_drifts": len(drifts),
                "total_drifts": len(all_drifts),
                "total_ok": len(all_ok)
            }
        }
        # Если указан конкретный стандарт, добавить его информацию
        if args.standard:
            target_std = args.standard.replace("\\", "/")
            if target_std.startswith("./"):
                target_std = target_std[2:]
            result["standard"] = target_std
            result["standard_version"] = standard_versions.get(target_std)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1 if all_drifts else 0)

    if args.check:
        # Только exit code
        sys.exit(1 if all_drifts else 0)

    if not all_drifts:
        print(f"✅ Все версии синхронизированы ({len(all_files)} файлов проверено)")
        sys.exit(0)

    # Вывод Workflows
    if workflow_drifts:
        print(f"=== Workflows: validation/create/modify ({len(workflow_drifts)} расхождений) ===")
        print()
        by_standard_wf = {}
        for drift in workflow_drifts:
            std = drift["standard"]
            if std not in by_standard_wf:
                by_standard_wf[std] = []
            by_standard_wf[std].append(drift)

        for std, files in by_standard_wf.items():
            expected = files[0]["expected"]
            print(f"## {std} (v{expected})")
            for drift in files:
                current = drift["version"] or "?"
                print(f"   ❌ {drift['file']}: v{current}")
            print()

    # Вывод Экземпляров
    if drifts:
        print(f"=== Экземпляры ({len(drifts)} расхождений) ===")
        print()
        by_standard_inst = {}
        for drift in drifts:
            std = drift["standard"]
            if std not in by_standard_inst:
                by_standard_inst[std] = []
            by_standard_inst[std].append(drift)

        for std, files in by_standard_inst.items():
            expected = files[0]["expected"]
            print(f"## {std} (v{expected})")
            for drift in files:
                current = drift["version"] or "?"
                print(f"   {drift['file']}: v{current}")
            print()

    # Итого
    print(f"❌ Всего расхождений: {len(all_drifts)} (Workflows: {len(workflow_drifts)}, Экземпляры: {len(drifts)})")
    print()
    print("Для миграции выполните:")
    all_standards = set(d["standard"] for d in all_drifts)
    for std in all_standards:
        print(f"  /migration-create {std}")

    sys.exit(1)


if __name__ == "__main__":
    main()
