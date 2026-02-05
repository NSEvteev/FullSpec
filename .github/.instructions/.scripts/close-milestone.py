#!/usr/bin/env python3
"""
close-milestone.py — Закрытие GitHub Milestone с проверками.

Автоматизирует: проверку open issues, перенос незавершённых, закрытие, верификацию.

Использование:
    python close-milestone.py --number 3
    python close-milestone.py --title "v1.0.0"
    python close-milestone.py --title "v1.0.0" --transfer "v1.1.0"
    python close-milestone.py --title "v1.0.0" --dry-run

Примеры:
    python close-milestone.py --number 3
    python close-milestone.py --title "v1.0.0" --transfer "v1.1.0" --force
    python close-milestone.py --title "v1.0.0" --dry-run

Возвращает:
    0 — Milestone закрыт успешно
    1 — ошибка (есть открытые Issues или другая проблема)
"""

import argparse
import json
import subprocess
import sys


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
    except subprocess.CalledProcessError:
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


def get_milestone(repo, number=None, title=None):
    """Получить Milestone по номеру или title."""
    if number:
        return gh_api(f"repos/{repo}/milestones/{number}")

    for state in ("open", "closed"):
        ms = gh_api(f"repos/{repo}/milestones", fields={"state": state})
        if ms:
            for m in ms:
                if m.get("title") == title:
                    return m
    return None


def get_open_issues(repo, milestone_title):
    """Получить открытые Issues в Milestone."""
    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--milestone", milestone_title, "--state", "open",
             "--json", "number,title", "-q", ".[] | {number, title}"],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        if not result.stdout.strip():
            return []
        issues = []
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                issues.append(json.loads(line))
        return issues
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return []


def transfer_issue(issue_number, target_milestone):
    """Перенести Issue в другой Milestone."""
    try:
        subprocess.run(
            ["gh", "issue", "edit", str(issue_number), "--milestone", target_milestone],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_target_milestone_number(repo, title):
    """Получить номер целевого Milestone для переноса."""
    ms = gh_api(f"repos/{repo}/milestones", fields={"state": "open"})
    if ms:
        for m in ms:
            if m.get("title") == title:
                return m.get("number")
    return None


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Закрытие GitHub Milestone с проверками")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--number", type=int, help="Номер Milestone")
    group.add_argument("--title", help="Title Milestone")
    parser.add_argument("--transfer", help="Title Milestone для переноса незавершённых Issues")
    parser.add_argument("--force", action="store_true",
                        help="Закрыть даже если есть открытые Issues (требует --transfer)")
    parser.add_argument("--dry-run", action="store_true", help="Показать план без закрытия")
    parser.add_argument("--json", action="store_true", help="Вывод в формате JSON")

    args = parser.parse_args()

    repo = get_repo_path()

    # Найти Milestone
    ms = get_milestone(repo, number=args.number, title=args.title)
    if not ms:
        print(f"❌ Milestone не найден")
        sys.exit(1)

    ms_number = ms["number"]
    ms_title = ms["title"]
    ms_state = ms["state"]
    open_count = ms.get("open_issues", 0)
    closed_count = ms.get("closed_issues", 0)
    total = open_count + closed_count

    print(f"📋 Milestone: {ms_title} (#{ms_number})")
    print(f"   Статус: {ms_state}")
    print(f"   Issues: {closed_count}/{total} закрыто ({open_count} открытых)")

    # Проверка: уже закрыт
    if ms_state == "closed":
        print(f"⚠️  Milestone уже закрыт")
        sys.exit(0)

    # Проверка: есть открытые Issues
    if open_count > 0:
        open_issues = get_open_issues(repo, ms_title)
        print(f"\n⚠️  Открытые Issues ({open_count}):")
        for issue in open_issues:
            print(f"   #{issue['number']}: {issue['title']}")

        if not args.transfer:
            print(f"\n❌ Невозможно закрыть: есть {open_count} открытых Issues")
            print(f"   Используйте --transfer \"vX.Y.Z\" для переноса")
            sys.exit(1)

        if not args.force:
            print(f"\n❌ Используйте --force для подтверждения переноса Issues")
            sys.exit(1)

        # Проверить целевой Milestone
        target_number = get_target_milestone_number(repo, args.transfer)
        if not target_number:
            print(f"❌ Целевой Milestone '{args.transfer}' не найден (должен быть open)")
            sys.exit(1)

        if args.dry_run:
            print(f"\n🔍 Dry run — будут перенесены {len(open_issues)} Issues в '{args.transfer}'")
            print(f"   Milestone '{ms_title}' будет закрыт")
            sys.exit(0)

        # Перенести Issues
        print(f"\n🔄 Перенос Issues в '{args.transfer}'...")
        transferred = 0
        for issue in open_issues:
            if transfer_issue(issue["number"], args.transfer):
                print(f"   ✅ #{issue['number']} перенесён")
                transferred += 1
            else:
                print(f"   ❌ #{issue['number']} не удалось перенести")

        print(f"   Перенесено: {transferred}/{len(open_issues)}")

        if transferred < len(open_issues):
            print(f"❌ Не все Issues перенесены. Закрытие отменено.")
            sys.exit(1)

    elif args.dry_run:
        print(f"\n🔍 Dry run — Milestone '{ms_title}' будет закрыт")
        sys.exit(0)

    # Закрыть Milestone
    print(f"\n🔒 Закрытие Milestone '{ms_title}'...")
    result = gh_api(
        f"repos/{repo}/milestones/{ms_number}",
        method="PATCH",
        fields={"state": "closed"},
    )

    if not result:
        print("❌ Не удалось закрыть Milestone")
        sys.exit(1)

    # Верификация
    verify = gh_api(f"repos/{repo}/milestones/{ms_number}")
    if verify and verify.get("state") == "closed":
        if args.json:
            print(json.dumps({
                "number": ms_number,
                "title": ms_title,
                "state": "closed",
                "open_issues": verify.get("open_issues", 0),
                "closed_issues": verify.get("closed_issues", 0),
            }, ensure_ascii=False, indent=2))
        else:
            print(f"✅ Milestone '{ms_title}' закрыт")
            print(f"\n💡 Следующий шаг: создать Release")
            print(f"   gh release create {ms_title} --title \"{ms_title}\" --notes \"...\"")
    else:
        print("❌ Верификация не пройдена — статус не 'closed'")
        sys.exit(1)


if __name__ == "__main__":
    main()
