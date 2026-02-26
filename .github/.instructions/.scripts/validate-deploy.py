#!/usr/bin/env python3
"""
validate-deploy.py — Валидация deploy.yml на соответствие standard-deploy.md.

Проверяет: триггер, discover job, matrix strategy, environments, rollback, permissions.

Использование:
    python validate-deploy.py [--json] [--repo <dir>]

Примеры:
    python validate-deploy.py
    python validate-deploy.py --json
    python validate-deploy.py --repo /path/to/repo

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


# =============================================================================
# Константы
# =============================================================================

DEPLOY_FILE = ".github/workflows/deploy.yml"

ERROR_CODES = {
    "D001": "deploy.yml не найден",
    "D002": "Триггер не release: [published]",
    "D003": "Нет discover job (dynamic service discovery)",
    "D004": "Нет matrix strategy из discover outputs",
    "D005": "Нет environment staging",
    "D006": "Нет environment production",
    "D007": "Нет rollback job с if: failure()",
    "D008": "Нет permissions packages: write",
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
# Валидация
# =============================================================================

def validate_deploy(file_path: Path) -> list[tuple[str, str]]:
    """Валидация deploy.yml.

    Returns:
        list: [(код ошибки, сообщение)]
    """
    errors = []

    # D001: Файл существует
    if not file_path.exists():
        errors.append(("D001", f"{DEPLOY_FILE} не найден"))
        return errors

    # Парсинг YAML
    try:
        content = file_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        errors.append(("D001", f"Невалидный YAML: {e}"))
        return errors

    if not isinstance(data, dict):
        errors.append(("D001", "Файл не содержит YAML mapping"))
        return errors

    # D002: Триггер release: [published]
    on = data.get("on") or data.get(True)  # YAML парсит 'on' как True
    has_release_trigger = False
    if isinstance(on, dict):
        release = on.get("release", {})
        if isinstance(release, dict):
            types = release.get("types", [])
            if "published" in types:
                has_release_trigger = True
    if not has_release_trigger:
        errors.append(("D002", "Триггер должен быть release: types: [published]"))

    # D008: Permissions packages: write
    permissions = data.get("permissions", {})
    if isinstance(permissions, dict):
        if permissions.get("packages") != "write":
            errors.append(("D008", "Отсутствует permissions: packages: write"))
    else:
        errors.append(("D008", "permissions не определён как mapping"))

    # Проверка jobs
    jobs = data.get("jobs", {})
    if not isinstance(jobs, dict):
        errors.append(("D003", "Нет jobs в workflow"))
        return errors

    # D003: Discover job
    discover_job = None
    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue
        outputs = job_config.get("outputs", {})
        if isinstance(outputs, dict) and "services" in outputs:
            discover_job = job_name
            break
    if not discover_job:
        errors.append(("D003", "Нет job с outputs.services (dynamic service discovery)"))

    # D004: Matrix strategy из discover outputs
    has_matrix_from_discover = False
    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue
        strategy = job_config.get("strategy", {})
        if isinstance(strategy, dict):
            matrix = strategy.get("matrix", {})
            if isinstance(matrix, dict):
                service = matrix.get("service", "")
                if isinstance(service, str) and "fromJson" in service:
                    has_matrix_from_discover = True
                    break
    if not has_matrix_from_discover:
        errors.append(("D004", "Нет matrix.service с fromJson() из discover outputs"))

    # D005, D006: Environments
    envs_found = set()
    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue
        env = job_config.get("environment", "")
        if isinstance(env, str) and env:
            envs_found.add(env)
        elif isinstance(env, dict):
            envs_found.add(env.get("name", ""))

    if "staging" not in envs_found:
        errors.append(("D005", "Нет job с environment: staging"))
    if "production" not in envs_found:
        errors.append(("D006", "Нет job с environment: production"))

    # D007: Rollback job с if: failure()
    has_rollback = False
    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue
        condition = job_config.get("if", "")
        if isinstance(condition, str) and "failure()" in condition:
            has_rollback = True
            break
    if not has_rollback:
        errors.append(("D007", "Нет rollback job с if: failure()"))

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
        description="Валидация deploy.yml на соответствие standard-deploy.md (D001-D008)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="Корень репозитория (по умолчанию — текущая директория)"
    )

    args = parser.parse_args()

    if args.repo:
        repo_root = Path(args.repo).resolve()
    else:
        repo_root = find_repo_root(Path.cwd())

    file_path = repo_root / DEPLOY_FILE
    errors = validate_deploy(file_path)

    if args.json:
        output = {
            "file": str(file_path),
            "errors": [{"code": code, "message": msg} for code, msg in errors],
            "total_errors": len(errors),
            "valid": len(errors) == 0,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if errors:
            print(f"❌ deploy.yml — {len(errors)} ошибок:")
            for code, msg in errors:
                print(f"   {code}: {msg}")
        else:
            print("✅ deploy.yml — валидация пройдена")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
