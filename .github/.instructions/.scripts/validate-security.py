#!/usr/bin/env python3
"""
validate-security.py — Валидация файлов безопасности GitHub.

Проверяет соответствие dependabot.yml, SECURITY.md и codeql.yml
стандарту standard-security.md.

Использование:
    python validate-security.py [--json] [--repo <dir>]

Примеры:
    python validate-security.py
    python validate-security.py --json
    python validate-security.py --repo /path/to/repo

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


# =============================================================================
# Константы
# =============================================================================

DEPENDABOT_PATH = ".github/dependabot.yml"
SECURITY_MD_PATH = ".github/SECURITY.md"
CODEQL_PATH = ".github/workflows/codeql.yml"

ERROR_CODES = {
    "SEC001": "Отсутствует dependabot.yml",
    "SEC002": "dependabot.yml: отсутствует version: 2",
    "SEC003": "dependabot.yml: отсутствуют updates",
    "SEC004": "dependabot.yml: ecosystem без обязательных полей",
    "SEC005": "Отсутствует SECURITY.md",
    "SEC006": "SECURITY.md: отсутствует секция Reporting",
    "SEC007": "SECURITY.md: отсутствует секция Response timeline",
    "SEC008": "Отсутствует codeql.yml",
    "SEC009": "codeql.yml: нет matrix.language (не Advanced Setup)",
    "SEC010": "codeql.yml: отсутствует permissions",
}


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


# =============================================================================
# Валидация dependabot.yml
# =============================================================================

def validate_dependabot(repo_root: Path) -> list[tuple[str, str]]:
    """Валидация dependabot.yml."""
    errors = []
    file_path = repo_root / DEPENDABOT_PATH

    if not file_path.exists():
        errors.append(("SEC001", f"Файл не найден: {DEPENDABOT_PATH}"))
        return errors

    try:
        content = file_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        errors.append(("SEC002", f"Невалидный YAML: {e}"))
        return errors

    if not isinstance(data, dict):
        errors.append(("SEC002", "Файл не содержит YAML mapping"))
        return errors

    # SEC002: version
    if data.get("version") != 2:
        errors.append(("SEC002", f"version: {data.get('version')}, ожидается 2"))

    # SEC003: updates
    updates = data.get("updates")
    if not isinstance(updates, list) or len(updates) == 0:
        errors.append(("SEC003", "Отсутствует или пустой массив updates"))
        return errors

    # SEC004: обязательные поля каждого ecosystem
    for i, entry in enumerate(updates):
        if not isinstance(entry, dict):
            continue
        missing = []
        if "package-ecosystem" not in entry:
            missing.append("package-ecosystem")
        if "directory" not in entry:
            missing.append("directory")
        if "schedule" not in entry:
            missing.append("schedule")
        if missing:
            ecosystem = entry.get("package-ecosystem", f"entry[{i}]")
            errors.append(("SEC004", f"'{ecosystem}': отсутствуют {', '.join(missing)}"))

    return errors


# =============================================================================
# Валидация SECURITY.md
# =============================================================================

def validate_security_md(repo_root: Path) -> list[tuple[str, str]]:
    """Валидация SECURITY.md."""
    errors = []
    file_path = repo_root / SECURITY_MD_PATH

    if not file_path.exists():
        errors.append(("SEC005", f"Файл не найден: {SECURITY_MD_PATH}"))
        return errors

    content = file_path.read_text(encoding="utf-8")

    # SEC006: секция Reporting
    if not re.search(r"#+\s+Reporting", content, re.IGNORECASE):
        errors.append(("SEC006", "Отсутствует секция 'Reporting a Vulnerability'"))

    # SEC007: секция Response timeline
    if not re.search(r"#+\s+Response\s+timeline", content, re.IGNORECASE):
        errors.append(("SEC007", "Отсутствует секция 'Response timeline'"))

    return errors


# =============================================================================
# Валидация codeql.yml
# =============================================================================

def validate_codeql(repo_root: Path) -> list[tuple[str, str]]:
    """Валидация codeql.yml (Advanced Setup)."""
    errors = []
    file_path = repo_root / CODEQL_PATH

    if not file_path.exists():
        return errors  # codeql.yml опционален (требует GitHub Team или публичного репо)

    try:
        content = file_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        errors.append(("SEC008", f"Невалидный YAML: {e}"))
        return errors

    if not isinstance(data, dict):
        errors.append(("SEC008", "Файл не содержит YAML mapping"))
        return errors

    # SEC010: permissions
    if "permissions" not in data:
        errors.append(("SEC010", "Отсутствует permissions: (нужен security-events: write)"))

    # SEC009: matrix.language (признак Advanced Setup)
    jobs = data.get("jobs", {})
    has_matrix_language = False

    if isinstance(jobs, dict):
        for job_name, job_config in jobs.items():
            if not isinstance(job_config, dict):
                continue
            strategy = job_config.get("strategy", {})
            if isinstance(strategy, dict):
                matrix = strategy.get("matrix", {})
                if isinstance(matrix, dict) and "language" in matrix:
                    has_matrix_language = True
                    break

    if not has_matrix_language:
        errors.append(("SEC009", "Нет strategy.matrix.language — возможно используется Default Setup вместо Advanced"))

    return errors


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация файлов безопасности GitHub (SEC001-SEC010)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Пути к файлам (игнорируются, проверяются все 3 файла)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    # Валидация всех файлов
    all_results = []

    # dependabot.yml
    errors = validate_dependabot(repo_root)
    all_results.append({
        "file": DEPENDABOT_PATH,
        "errors": [{"code": code, "message": msg} for code, msg in errors],
        "valid": len(errors) == 0,
    })

    # SECURITY.md
    errors = validate_security_md(repo_root)
    all_results.append({
        "file": SECURITY_MD_PATH,
        "errors": [{"code": code, "message": msg} for code, msg in errors],
        "valid": len(errors) == 0,
    })

    # codeql.yml
    errors = validate_codeql(repo_root)
    all_results.append({
        "file": CODEQL_PATH,
        "errors": [{"code": code, "message": msg} for code, msg in errors],
        "valid": len(errors) == 0,
    })

    has_errors = any(not r["valid"] for r in all_results)

    # Вывод
    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    else:
        for result in all_results:
            name = Path(result["file"]).name
            if result["valid"]:
                print(f"✅ {name} — валидация пройдена")
            else:
                error_count = len(result["errors"])
                print(f"❌ {name} — {error_count} ошибок:")
                for err in result["errors"]:
                    print(f"   {err['code']}: {err['message']}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
