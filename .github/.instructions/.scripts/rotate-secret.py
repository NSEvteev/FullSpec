#!/usr/bin/env python3
"""
rotate-secret.py — Автоматизация ротации GitHub Secret.

Обновляет секрет через gh CLI, опционально запускает smoke-test workflow,
записывает результат в лог ротации.

Использование:
    python rotate-secret.py --name DB_POSTGRES_PASSWORD --value "new-password"
    python rotate-secret.py --name DB_POSTGRES_PASSWORD --value "new-password" --env production
    python rotate-secret.py --name DB_POSTGRES_PASSWORD --value "new-password" --workflow ci.yml
    python rotate-secret.py --name DB_POSTGRES_PASSWORD --value "new-password" --workflow ci.yml --timeout 300

Примеры:
    # Обновить секрет без проверки
    python rotate-secret.py --name API_STRIPE_SECRET_KEY --value "sk_live_..."

    # Обновить секрет для среды и проверить workflow
    python rotate-secret.py --name DB_POSTGRES_URL --value "postgresql://..." --env production --workflow deploy.yml

Возвращает:
    0 — ротация завершена успешно
    1 — ошибка при ротации
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

ROTATION_LOG_PATH = ".github/secrets-rotation-log.json"
WORKFLOW_POLL_INTERVAL = 15  # секунд
DEFAULT_TIMEOUT = 300  # 5 минут


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


def run_gh(args: list[str]) -> subprocess.CompletedProcess:
    """Выполнить команду gh CLI."""
    return subprocess.run(
        ["gh"] + args,
        capture_output=True,
        encoding="utf-8",
    )


# =============================================================================
# Шаг 2: Обновление секрета в GitHub
# =============================================================================

def update_secret(name: str, value: str, env: str | None = None) -> bool:
    """Обновить секрет через gh CLI."""
    cmd = ["secret", "set", name, "--body", value]
    if env:
        cmd.extend(["--env", env])

    result = run_gh(cmd)
    if result.returncode != 0:
        print(f"Ошибка обновления секрета: {result.stderr.strip()}", file=sys.stderr)
        return False

    env_label = f" (environment: {env})" if env else ""
    print(f"Секрет {name}{env_label} обновлён")
    return True


# =============================================================================
# Шаг 3: Проверка — запуск smoke-test workflow
# =============================================================================

def run_smoke_test(workflow: str, timeout: int) -> bool:
    """Запустить workflow и дождаться результата."""
    print(f"Запуск workflow: {workflow}")

    result = run_gh(["workflow", "run", workflow])
    if result.returncode != 0:
        print(f"Ошибка запуска workflow: {result.stderr.strip()}", file=sys.stderr)
        return False

    # Подождать немного, пока run появится в API
    time.sleep(5)

    # Получить ID последнего запуска
    result = run_gh([
        "run", "list",
        "--workflow", workflow,
        "--limit", "1",
        "--json", "databaseId,status,conclusion",
    ])
    if result.returncode != 0:
        print(f"Ошибка получения статуса: {result.stderr.strip()}", file=sys.stderr)
        return False

    runs = json.loads(result.stdout)
    if not runs:
        print("Не найден запуск workflow", file=sys.stderr)
        return False

    run_id = runs[0]["databaseId"]
    print(f"Ожидание завершения run #{run_id} (timeout: {timeout}с)")

    elapsed = 0
    while elapsed < timeout:
        result = run_gh([
            "run", "view", str(run_id),
            "--json", "status,conclusion",
        ])
        if result.returncode != 0:
            print(f"Ошибка проверки статуса: {result.stderr.strip()}", file=sys.stderr)
            return False

        run_data = json.loads(result.stdout)
        status = run_data.get("status", "")
        conclusion = run_data.get("conclusion", "")

        if status == "completed":
            if conclusion == "success":
                print(f"Workflow завершён успешно")
                return True
            else:
                print(f"Workflow завершён с результатом: {conclusion}", file=sys.stderr)
                return False

        time.sleep(WORKFLOW_POLL_INTERVAL)
        elapsed += WORKFLOW_POLL_INTERVAL

    print(f"Timeout ({timeout}с) — workflow не завершился", file=sys.stderr)
    return False


# =============================================================================
# Шаг 5: Документирование ротации
# =============================================================================

def log_rotation(repo_root: Path, name: str, env: str | None, success: bool) -> None:
    """Записать результат ротации в лог."""
    log_path = repo_root / ROTATION_LOG_PATH
    log_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    if log_path.exists():
        try:
            entries = json.loads(log_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            entries = []

    entry = {
        "secret": name,
        "environment": env,
        "rotated_at": datetime.now(timezone.utc).isoformat(),
        "success": success,
    }
    entries.append(entry)

    log_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Лог ротации обновлён: {ROTATION_LOG_PATH}")


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Автоматизация ротации GitHub Secret (шаги 2-5)"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Имя секрета (например, DB_POSTGRES_PASSWORD)"
    )
    parser.add_argument(
        "--value",
        required=True,
        help="Новое значение секрета"
    )
    parser.add_argument(
        "--env",
        default=None,
        help="Environment (например, production, staging)"
    )
    parser.add_argument(
        "--workflow",
        default=None,
        help="Workflow для smoke-test (например, ci.yml)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout ожидания workflow в секундах (по умолчанию: {DEFAULT_TIMEOUT})"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    # Шаг 2: Обновить секрет
    if not update_secret(args.name, args.value, args.env):
        log_rotation(repo_root, args.name, args.env, success=False)
        sys.exit(1)

    # Шаг 3: Проверить (если указан workflow)
    smoke_ok = True
    if args.workflow:
        smoke_ok = run_smoke_test(args.workflow, args.timeout)
        if not smoke_ok:
            print(
                "ВНИМАНИЕ: Smoke-test не прошёл. "
                "Секрет уже обновлён — проверьте вручную.",
                file=sys.stderr,
            )

    # Шаг 5: Документировать
    log_rotation(repo_root, args.name, args.env, success=smoke_ok)

    # Шаг 4: Напоминание
    if smoke_ok:
        print()
        print("Ротация завершена. Следующий шаг:")
        print("  → Отзовите старый секрет в провайдере")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
