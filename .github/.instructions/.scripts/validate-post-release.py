#!/usr/bin/env python3
"""
validate-post-release.py — Post-release валидация после создания GitHub Release.

Проверяет: объект Release, Release Notes, CHANGELOG.md, деплой.

Использование:
    python validate-post-release.py --version v1.0.0
    python validate-post-release.py --version v1.0.0 --skip-deploy
    python validate-post-release.py --version v1.0.0 --json

Примеры:
    python validate-post-release.py --version v1.0.0
    python validate-post-release.py --version v1.0.0 --skip-deploy --json

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
    2 — фатальная ошибка (gh не установлен, не git-репозиторий)
"""

import argparse
import json
import os
import re
import subprocess
import sys


# =============================================================================
# Константы
# =============================================================================

ERROR_CODES = {
    "E001": "Release не найден",
    "E002": "Tag не соответствует формату vX.Y.Z",
    "E003": "Title не соответствует формату 'Release vX.Y.Z'",
    "E004": "Body пустой",
    "E005": "Release помечен как draft",
    "E006": "Target не main",
    "E007": "Git-тег не существует",
    "E008": "Нет ссылки на Milestone в Release Notes",
    "E009": "Нет changelog в Release Notes",
    "E010": "Placeholder-текст в Release Notes (TODO/WIP/TBD)",
    "E011": "CHANGELOG.md не существует",
    "E012": "Версия не найдена в CHANGELOG.md",
    "E013": "Формат CHANGELOG.md некорректный",
    "E014": "Деплой провалился",
    "E015": "Деплой не запущен",
}

SEMVER_PATTERN = re.compile(
    r"^v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?$"
)

PLACEHOLDER_PATTERNS = re.compile(r"\b(TODO|WIP|TBD|FIXME|HACK)\b", re.IGNORECASE)


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

def check_release_object(repo: str, version: str) -> tuple[list[str], dict | None]:
    """Проверить объект Release: tag, title, body, draft, target."""
    errors = []

    release = gh_api(f"repos/{repo}/releases/tags/{version}")
    if not release:
        errors.append(f"[E001] Release '{version}' не найден")
        return errors, None

    tag = release.get("tag_name", "")
    name = release.get("name", "")
    body = release.get("body") or ""
    draft = release.get("draft", False)
    target = release.get("target_commitish", "")

    # E002: Tag формат
    if not SEMVER_PATTERN.match(tag):
        errors.append(f"[E002] Tag '{tag}' не соответствует формату vX.Y.Z")

    # E003: Title формат
    expected_title = f"Release {version}"
    if name != expected_title:
        errors.append(f"[E003] Title '{name}', ожидается '{expected_title}'")

    # E004: Body не пустой
    if not body.strip():
        errors.append("[E004] Body (Release Notes) пустой")

    # E005: Не draft
    if draft:
        errors.append("[E005] Release помечен как draft (не опубликован)")

    # E006: Target = main
    if target and target != "main":
        errors.append(f"[E006] Target '{target}', ожидается 'main'")

    return errors, release


def check_git_tag(version: str) -> list[str]:
    """Проверить что Git-тег существует."""
    run_cmd(["git", "fetch", "--tags"])
    result = run_cmd(["git", "rev-parse", f"refs/tags/{version}"])
    if result.returncode != 0:
        return [f"[E007] Git-тег '{version}' не существует"]
    return []


def check_release_notes(release: dict | None, version: str) -> list[str]:
    """Проверить содержимое Release Notes."""
    if not release:
        return []

    errors = []
    body = release.get("body") or ""

    # E008: Ссылка на Milestone
    if "milestone" not in body.lower():
        errors.append("[E008] Release Notes не содержит ссылку на Milestone (секция '## Milestone')")

    # E009: Changelog
    has_changelog = (
        "what's changed" in body.lower()
        or "changelog" in body.lower()
        or body.count("- ") >= 2  # Минимум 2 элемента списка
    )
    if not has_changelog:
        errors.append("[E009] Release Notes не содержит changelog (список изменений)")

    # E010: Placeholder-тексты
    placeholders = PLACEHOLDER_PATTERNS.findall(body)
    if placeholders:
        errors.append(f"[E010] Placeholder-тексты в Release Notes: {', '.join(set(placeholders))}")

    return errors


def check_changelog(version: str) -> list[str]:
    """Проверить CHANGELOG.md."""
    errors = []
    changelog_path = "CHANGELOG.md"

    # E011: Файл существует
    if not os.path.isfile(changelog_path):
        errors.append(f"[E011] {changelog_path} не существует")
        return errors

    with open(changelog_path, encoding="utf-8") as f:
        content = f.read()

    # E013: Формат — заголовок
    if not content.startswith("# Changelog"):
        errors.append("[E013] CHANGELOG.md должен начинаться с '# Changelog'")

    # E013: Секция Unreleased
    if "[Unreleased]" not in content and "[unreleased]" not in content.lower():
        errors.append("[E013] CHANGELOG.md не содержит секцию '[Unreleased]'")

    # E012: Версия присутствует
    version_without_v = version.lstrip("v")
    if f"[{version_without_v}]" not in content:
        errors.append(f"[E012] Версия [{version_without_v}] не найдена в CHANGELOG.md")

    return errors


def check_deploy(skip: bool = False) -> list[str]:
    """Проверить статус деплоя."""
    if skip:
        return []

    errors = []

    # Проверить что deploy.yml существует
    if not os.path.isfile(".github/workflows/deploy.yml"):
        errors.append("[E015] deploy.yml не существует (.github/workflows/deploy.yml)")
        return errors

    result = run_cmd(["gh", "run", "list", "--workflow=deploy.yml", "--limit", "1", "--json", "status,conclusion"])

    if result.returncode != 0:
        errors.append("[E015] Не удалось получить статус deploy.yml (workflow не найден?)")
        return errors

    runs = json.loads(result.stdout) if result.stdout.strip() else []
    if not runs:
        errors.append("[E015] Нет запусков deploy.yml")
        return errors

    run = runs[0]
    status = run.get("status", "")
    conclusion = run.get("conclusion", "")

    if status == "completed" and conclusion != "success":
        errors.append(f"[E014] Деплой провалился (conclusion: {conclusion})")
    elif status != "completed":
        errors.append(f"[E015] Деплой ещё не завершён (status: {status})")

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
        description="Post-release валидация после создания GitHub Release"
    )
    parser.add_argument("--version", required=True, help="Версия релиза (например v1.0.0)")
    parser.add_argument("--skip-deploy", action="store_true", help="Пропустить проверку деплоя")
    parser.add_argument("--json", action="store_true", help="Вывод в формате JSON")

    args = parser.parse_args()

    repo = get_repo_path()
    all_errors: list[str] = []

    # Проверки
    release_errors, release = check_release_object(repo, args.version)

    checks = [
        ("Объект Release", release_errors),
        ("Git-тег", check_git_tag(args.version)),
        ("Release Notes", check_release_notes(release, args.version)),
        ("CHANGELOG.md", check_changelog(args.version)),
        ("Деплой", check_deploy(args.skip_deploy)),
    ]

    results = []
    for name, errors in checks:
        passed = len(errors) == 0
        results.append({"check": name, "passed": passed, "errors": errors})
        all_errors.extend(errors)

    # Вывод
    if args.json:
        output = {
            "version": args.version,
            "checks": results,
            "total_errors": len(all_errors),
            "valid": len(all_errors) == 0,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"Post-release валидация: {args.version}\n")
        for r in results:
            status = "✅" if r["passed"] else "❌"
            print(f"  {status} {r['check']}")
            for err in r["errors"]:
                print(f"     {err}")

        print()
        if all_errors:
            print(f"❌ {len(all_errors)} ошибок — Release требует исправлений")
        else:
            print(f"✅ Release {args.version} валиден")

    sys.exit(0 if not all_errors else 1)


if __name__ == "__main__":
    main()
