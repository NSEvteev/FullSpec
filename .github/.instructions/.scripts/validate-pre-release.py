#!/usr/bin/env python3
"""
validate-pre-release.py — Pre-release валидация перед созданием GitHub Release.

Проверяет: main синхронизирована, нет critical PR, тесты, Milestone, чистый working tree.

Использование:
    python validate-pre-release.py --version v1.0.0
    python validate-pre-release.py --version v1.0.0 --skip-tests
    python validate-pre-release.py --version v1.0.0 --json

Примеры:
    python validate-pre-release.py --version v1.0.0
    python validate-pre-release.py --version v2.0.0-beta.1 --skip-tests

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
    2 — фатальная ошибка (gh не установлен, не git-репозиторий)
"""

import argparse
import json
import subprocess
import sys


# =============================================================================
# Константы
# =============================================================================

ERROR_CODES = {
    "E001": "Main не синхронизирована с remote",
    "E002": "Есть открытые PR с меткой critical",
    "E003": "Тесты не прошли (make test)",
    "E004": "Milestone не найден",
    "E005": "Milestone не закрыт",
    "E006": "В Milestone есть открытые Issues",
    "E007": "Есть незакоммиченные изменения",
    "E008": "Текущая ветка не main",
    "E009": "Есть open Dependabot alerts (critical/high)",
    "E010": "Есть open Issues с меткой security",
}


# =============================================================================
# Helpers
# =============================================================================

def run_cmd(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess:
    """Выполнить команду и вернуть результат."""
    return subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", check=check,
    )


def gh_api(endpoint: str, method: str = "GET") -> dict | list | None:
    """Выполнить запрос к GitHub API через gh CLI."""
    cmd = ["gh", "api", "--method", method, endpoint]
    try:
        result = run_cmd(cmd, check=True)
        return json.loads(result.stdout) if result.stdout.strip() else None
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        print("[FATAL] gh CLI не установлен")
        sys.exit(2)


def get_repo_path() -> str:
    """Получить owner/repo из текущего репозитория."""
    try:
        result = run_cmd(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[FATAL] Не удалось определить репозиторий")
        sys.exit(2)


# =============================================================================
# Проверки
# =============================================================================

def check_current_branch() -> list[str]:
    """Проверить что текущая ветка — main."""
    result = run_cmd(["git", "branch", "--show-current"])
    branch = result.stdout.strip()
    if branch != "main":
        return [f"[E008] Текущая ветка '{branch}', ожидается 'main'"]
    return []


def check_main_synced() -> list[str]:
    """Проверить что main синхронизирована с remote."""
    # Fetch latest
    run_cmd(["git", "fetch", "origin", "main"])

    # Compare local and remote
    local = run_cmd(["git", "rev-parse", "main"]).stdout.strip()
    remote = run_cmd(["git", "rev-parse", "origin/main"]).stdout.strip()

    if local != remote:
        return [f"[E001] main ({local[:7]}) отличается от origin/main ({remote[:7]}). Выполните: git pull origin main"]
    return []


def check_no_critical_prs() -> list[str]:
    """Проверить что нет открытых PR с меткой critical."""
    result = run_cmd(["gh", "pr", "list", "--label", "critical", "--state", "open", "--json", "number,title"])
    if result.returncode != 0:
        return []  # Если gh не может получить PR — пропускаем

    prs = json.loads(result.stdout) if result.stdout.strip() else []
    if prs:
        titles = ", ".join(f"#{pr['number']} {pr['title']}" for pr in prs)
        return [f"[E002] Есть {len(prs)} открытых critical PR: {titles}"]
    return []


def check_tests(skip: bool = False) -> list[str]:
    """Проверить что тесты проходят (make test)."""
    if skip:
        return []

    result = run_cmd(["make", "test"])
    if result.returncode != 0:
        stderr_preview = (result.stderr or "")[:200]
        return [f"[E003] make test провалился: {stderr_preview}"]
    return []


def check_milestone(repo: str, version: str) -> list[str]:
    """Проверить Milestone: существует, закрыт, нет открытых Issues."""
    errors = []

    # Найти Milestone
    milestones = gh_api(f"repos/{repo}/milestones?state=all") or []
    milestone = None
    for ms in milestones:
        if ms.get("title") == version:
            milestone = ms
            break

    if not milestone:
        errors.append(f"[E004] Milestone '{version}' не найден")
        return errors

    # Проверить статус
    if milestone.get("state") != "closed":
        open_issues = milestone.get("open_issues", 0)
        if open_issues > 0:
            errors.append(f"[E006] В Milestone '{version}' есть {open_issues} открытых Issues")
        errors.append(f"[E005] Milestone '{version}' не закрыт (state: {milestone.get('state')})")

    return errors


def check_clean_working_tree() -> list[str]:
    """Проверить что нет незакоммиченных изменений."""
    result = run_cmd(["git", "diff", "--quiet"])
    staged = run_cmd(["git", "diff", "--cached", "--quiet"])

    if result.returncode != 0 or staged.returncode != 0:
        return ["[E007] Есть незакоммиченные изменения. Выполните: git stash или git commit"]
    return []


def check_dependabot_alerts(repo: str) -> list[str]:
    """E009: Проверить Dependabot alerts (critical/high)."""
    result = run_cmd([
        "gh", "api", f"repos/{repo}/dependabot/alerts",
        "--jq", '[.[] | select(.state=="open") | select(.security_advisory.severity=="critical" or .security_advisory.severity=="high")] | length',
    ])
    if result.returncode != 0:
        # API недоступен (нет прав, не настроен) — warning, не ошибка
        return []
    count = int(result.stdout.strip() or "0")
    if count > 0:
        return [f"[E009] {count} open Dependabot alert(s) с severity critical/high"]
    return []


def check_security_issues() -> list[str]:
    """E010: Проверить open Issues с меткой security."""
    result = run_cmd([
        "gh", "issue", "list", "--label", "security",
        "--state", "open", "--json", "number", "--jq", "length",
    ])
    if result.returncode != 0:
        return []
    count = int(result.stdout.strip() or "0")
    if count > 0:
        return [f"[E010] {count} open Issue(s) с меткой security"]
    return []


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Pre-release валидация перед созданием GitHub Release"
    )
    parser.add_argument("--version", required=True, help="Версия релиза (например v1.0.0)")
    parser.add_argument("--skip-tests", action="store_true", help="Пропустить make test")
    parser.add_argument("--json", action="store_true", help="Вывод в формате JSON")

    args = parser.parse_args()

    repo = get_repo_path()
    all_errors: list[str] = []

    # Последовательные проверки (порядок важен)
    checks = [
        ("Текущая ветка", lambda: check_current_branch()),
        ("Main синхронизирована", lambda: check_main_synced()),
        ("Нет critical PR", lambda: check_no_critical_prs()),
        ("Тесты", lambda: check_tests(args.skip_tests)),
        ("Milestone", lambda: check_milestone(repo, args.version)),
        ("Чистый working tree", lambda: check_clean_working_tree()),
        ("Dependabot alerts", lambda: check_dependabot_alerts(repo)),
        ("Security issues", lambda: check_security_issues()),
    ]

    results = []
    for name, check_fn in checks:
        errors = check_fn()
        passed = len(errors) == 0
        results.append({"check": name, "passed": passed, "errors": errors})
        all_errors.extend(errors)

    # Вывод
    if args.json:
        output = {
            "version": args.version,
            "checks": results,
            "total_errors": len(all_errors),
            "ready": len(all_errors) == 0,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"Pre-release валидация: {args.version}\n")
        for r in results:
            status = "✅" if r["passed"] else "❌"
            print(f"  {status} {r['check']}")
            for err in r["errors"]:
                print(f"     {err}")

        print()
        if all_errors:
            print(f"❌ {len(all_errors)} ошибок — Release создавать НЕЛЬЗЯ")
        else:
            print(f"✅ Все проверки пройдены — можно создавать Release {args.version}")

    sys.exit(0 if not all_errors else 1)


if __name__ == "__main__":
    main()
