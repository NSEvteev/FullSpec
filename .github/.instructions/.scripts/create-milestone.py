#!/usr/bin/env python3
"""
create-milestone.py — Создание GitHub Milestone по стандарту.

Автоматизирует: определение версии, проверку уникальности, создание, валидацию.

Использование:
    python create-milestone.py --title "v1.0.0" --due 2026-03-15
    python create-milestone.py --title "v0.1.0" --due 2026-03-15 --description "## Цель\n\nMVP"
    python create-milestone.py --next --due 2026-03-15
    python create-milestone.py --next --increment minor --due 2026-03-15

Примеры:
    python create-milestone.py --title "v0.1.0" --due 2026-03-01
    python create-milestone.py --next --increment major --due 2026-06-01
    python create-milestone.py --title "v1.0.0-beta.1" --due 2026-02-28 --dry-run

Возвращает:
    0 — Milestone создан успешно
    1 — ошибка создания
"""

import argparse
import json
import re
import subprocess
import sys


# =============================================================================
# Константы
# =============================================================================

SEMVER_PATTERN = re.compile(
    r"^v(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*))?$"
)

DEFAULT_DESCRIPTION = """## Цель

{goal}

## Критерии готовности

- [ ] {criteria}"""


# =============================================================================
# GitHub API
# =============================================================================

def gh_api(endpoint, method="GET", fields=None):
    """Выполнить запрос к GitHub API через gh CLI."""
    cmd = ["gh", "api", "--method", method, endpoint]
    if fields:
        for key, value in fields.items():
            cmd.extend(["-f", f"{key}={value}"])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=True)
        return json.loads(result.stdout) if result.stdout.strip() else None
    except subprocess.CalledProcessError as e:
        if "422" in (e.stderr or ""):
            print(f"[ERROR] Milestone с таким title уже существует")
        elif "403" in (e.stderr or ""):
            print(f"[ERROR] Нет прав на создание Milestone")
        else:
            print(f"[ERROR] API error: {e.stderr}")
        return None
    except FileNotFoundError:
        print("[FATAL] gh CLI не установлен")
        sys.exit(2)


def get_repo_path():
    """Получить owner/repo."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[FATAL] Не удалось определить репозиторий")
        sys.exit(2)


# =============================================================================
# Версионирование
# =============================================================================

def get_all_versions(repo):
    """Получить все версии Milestones."""
    versions = []
    for state in ("open", "closed"):
        ms = gh_api(f"repos/{repo}/milestones", fields={"state": state})
        if ms:
            for m in ms:
                title = m.get("title", "")
                match = SEMVER_PATTERN.match(title)
                if match:
                    versions.append({
                        "title": title,
                        "major": int(match.group("major")),
                        "minor": int(match.group("minor")),
                        "patch": int(match.group("patch")),
                        "prerelease": match.group("prerelease"),
                    })
    versions.sort(key=lambda v: (v["major"], v["minor"], v["patch"]))
    return versions


def get_next_version(versions, increment="minor"):
    """Определить следующую версию."""
    if not versions:
        return "v0.1.0"

    # Берём последнюю стабильную (без prerelease)
    stable = [v for v in versions if not v["prerelease"]]
    latest = stable[-1] if stable else versions[-1]

    major, minor, patch = latest["major"], latest["minor"], latest["patch"]

    if increment == "major":
        return f"v{major + 1}.0.0"
    elif increment == "minor":
        return f"v{major}.{minor + 1}.0"
    elif increment == "patch":
        return f"v{major}.{minor}.{patch + 1}"
    else:
        return f"v{major}.{minor + 1}.0"


def check_uniqueness(repo, title):
    """Проверить уникальность title."""
    for state in ("open", "closed"):
        ms = gh_api(f"repos/{repo}/milestones", fields={"state": state})
        if ms:
            for m in ms:
                if m.get("title") == title:
                    return False
    return True


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Создание GitHub Milestone по стандарту")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--title", help="Title Milestone (SemVer: vX.Y.Z)")
    group.add_argument("--next", action="store_true", help="Автоматически определить следующую версию")
    parser.add_argument("--increment", choices=["major", "minor", "patch"], default="minor",
                        help="Тип инкремента для --next (по умолчанию: minor)")
    parser.add_argument("--due", required=True, help="Due date (YYYY-MM-DD)")
    parser.add_argument("--description", help="Description (markdown). По умолчанию: шаблон")
    parser.add_argument("--goal", default="Описание цели Milestone", help="Цель для шаблона description")
    parser.add_argument("--criteria", default="Критерий готовности", help="Критерий для шаблона description")
    parser.add_argument("--dry-run", action="store_true", help="Показать план без создания")
    parser.add_argument("--json", action="store_true", help="Вывод в формате JSON")

    args = parser.parse_args()

    repo = get_repo_path()

    # Определить title
    if args.next:
        versions = get_all_versions(repo)
        title = get_next_version(versions, args.increment)
        print(f"📊 Последняя версия: {versions[-1]['title'] if versions else 'нет'}")
        print(f"📌 Следующая версия: {title} (инкремент: {args.increment})")
    else:
        title = args.title

    # Проверить формат
    if not SEMVER_PATTERN.match(title):
        print(f"❌ Title '{title}' не соответствует SemVer (vMAJOR.MINOR.PATCH)")
        sys.exit(1)

    # Проверить уникальность
    if not check_uniqueness(repo, title):
        print(f"❌ Milestone '{title}' уже существует")
        sys.exit(1)
    print(f"✅ Title '{title}' уникален")

    # Подготовить description
    if args.description:
        description = args.description.replace("\\n", "\n")
    else:
        description = DEFAULT_DESCRIPTION.format(goal=args.goal, criteria=args.criteria)

    # Подготовить due date
    due_on = f"{args.due}T23:59:59Z"

    # Dry run
    if args.dry_run:
        print(f"\n🔍 Dry run — Milestone НЕ будет создан:")
        print(f"   Title: {title}")
        print(f"   Due: {due_on}")
        print(f"   Description:\n{description}")
        sys.exit(0)

    # Создать Milestone
    print(f"\n🚀 Создание Milestone '{title}'...")
    result = gh_api(
        f"repos/{repo}/milestones",
        method="POST",
        fields={
            "title": title,
            "description": description,
            "due_on": due_on,
        },
    )

    if not result:
        print("❌ Не удалось создать Milestone")
        sys.exit(1)

    number = result.get("number")
    url = result.get("html_url", "")

    if args.json:
        print(json.dumps({
            "number": number,
            "title": title,
            "due_on": due_on,
            "url": url,
            "status": "created",
        }, ensure_ascii=False, indent=2))
    else:
        print(f"✅ Milestone создан:")
        print(f"   Number: {number}")
        print(f"   Title: {title}")
        print(f"   Due: {due_on}")
        print(f"   URL: {url}")
        print(f"\n💡 Валидация: python .github/.instructions/.scripts/validate-milestone.py --number {number}")


if __name__ == "__main__":
    main()
