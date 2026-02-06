#!/usr/bin/env python3
"""
validate-action.py — Валидация GitHub Actions workflow файлов.

Проверяет соответствие .github/workflows/*.yml стандарту standard-action.md.

Использование:
    python validate-action.py <path> [--all] [--json] [--repo <dir>]

Примеры:
    python validate-action.py .github/workflows/ci.yml
    python validate-action.py --all
    python validate-action.py --all --json

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

WORKFLOWS_DIR = ".github/workflows"

ERROR_CODES = {
    "A001": "Отсутствует name: на уровне workflow",
    "A002": "Отсутствует permissions: на уровне workflow",
    "A003": "Отсутствует timeout-minutes: у job",
    "A004": "Action использует ветку вместо версии (@main, @master)",
    "A005": "Секрет используется напрямую в run: (вынести в env:)",
    "A006": "Отсутствует runs-on: у job",
    "A007": "Файл не в .github/workflows/",
}

# Паттерн для uses с веткой вместо версии
BRANCH_REF_PATTERN = re.compile(r"uses:\s+[\w\-./]+@(main|master|develop|HEAD)\b")

# Паттерн для secrets напрямую в run
SECRETS_IN_RUN_PATTERN = re.compile(r"\$\{\{\s*secrets\.\w+\s*\}\}")


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
# Валидация
# =============================================================================

def validate_workflow(file_path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидация одного workflow файла.

    Returns:
        list: [(код ошибки, сообщение)]
    """
    errors = []

    # A007: Расположение
    try:
        rel_path = file_path.relative_to(repo_root)
        rel_str = str(rel_path).replace("\\", "/")
        if not rel_str.startswith(WORKFLOWS_DIR + "/"):
            errors.append(("A007", f"Файл в {rel_str}, должен быть в {WORKFLOWS_DIR}/"))
    except ValueError:
        errors.append(("A007", "Не удалось определить расположение"))

    if not file_path.exists():
        errors.append(("A007", f"Файл не найден: {file_path}"))
        return errors

    # Парсинг YAML
    try:
        content = file_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        errors.append(("A001", f"Невалидный YAML: {e}"))
        return errors

    if not isinstance(data, dict):
        errors.append(("A001", "Файл не содержит YAML mapping"))
        return errors

    # A001: name
    if "name" not in data:
        errors.append(("A001", "Отсутствует name: на уровне workflow"))

    # A002: permissions
    if "permissions" not in data:
        errors.append(("A002", "Отсутствует permissions: (добавьте минимум contents: read)"))

    # Проверка jobs
    jobs = data.get("jobs", {})
    if not isinstance(jobs, dict):
        return errors

    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue

        # A003: timeout-minutes
        if "timeout-minutes" not in job_config:
            errors.append(("A003", f"Job '{job_name}': отсутствует timeout-minutes"))

        # A006: runs-on
        if "runs-on" not in job_config and "uses" not in job_config:
            # reusable workflow jobs use 'uses' instead of 'runs-on'
            errors.append(("A006", f"Job '{job_name}': отсутствует runs-on"))

        # Проверка steps
        steps = job_config.get("steps", [])
        if not isinstance(steps, list):
            continue

        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                continue

            # A004: Action версионирование
            uses = step.get("uses", "")
            if isinstance(uses, str) and uses:
                match = BRANCH_REF_PATTERN.match(f"uses: {uses}")
                if match:
                    errors.append(("A004", f"Job '{job_name}', step {i + 1}: {uses} — используйте @vN вместо @{match.group(1)}"))

            # A005: Secrets в run
            run_cmd = step.get("run", "")
            if isinstance(run_cmd, str) and SECRETS_IN_RUN_PATTERN.search(run_cmd):
                secrets_found = SECRETS_IN_RUN_PATTERN.findall(run_cmd)
                errors.append(("A005", f"Job '{job_name}', step {i + 1}: секрет в run: — вынесите в env: блок"))

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
        description="Валидация GitHub Actions workflow файлов (A001-A007)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Путь к workflow файлу (можно несколько)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help=f"Валидировать все файлы в {WORKFLOWS_DIR}/"
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

    # Собрать список файлов
    files: list[Path] = []

    if args.all:
        workflows_dir = repo_root / WORKFLOWS_DIR
        if workflows_dir.exists():
            files = sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))
        else:
            print(f"❌ Папка {WORKFLOWS_DIR}/ не найдена")
            sys.exit(1)
    elif args.path:
        for p in args.path:
            path = Path(p)
            if not path.is_absolute():
                path = repo_root / path
            files.append(path)
    else:
        parser.print_help()
        sys.exit(1)

    # Фильтровать README.md
    files = [f for f in files if f.name.lower() != "readme.md"]

    if not files:
        print(f"⚠️ Нет workflow файлов в {WORKFLOWS_DIR}/")
        sys.exit(0)

    # Валидация
    all_results = []
    has_errors = False

    for file_path in files:
        errors = validate_workflow(file_path, repo_root)
        rel_path = str(file_path.relative_to(repo_root)).replace("\\", "/")

        result = {
            "file": rel_path,
            "errors": [{"code": code, "message": msg} for code, msg in errors],
            "valid": len(errors) == 0,
        }
        all_results.append(result)

        if errors:
            has_errors = True

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
