#!/usr/bin/env python3
"""
migrate-label.py — Миграция меток на Issues/PR.

Заменяет одну метку на другую (или удаляет) на всех Issues и PR.

Использование:
    python migrate-label.py <old-label> <new-label>     # Заменить метку
    python migrate-label.py <old-label> --delete        # Удалить метку
    python migrate-label.py <old-label> <new-label> --apply  # Применить

Примеры:
    python migrate-label.py area:infra area:platform           # Показать план
    python migrate-label.py area:infra area:platform --apply   # Применить
    python migrate-label.py area:legacy --delete --apply       # Удалить с Issues/PR

Возвращает:
    0 — миграция выполнена / нет изменений
    1 — ошибка
"""

import argparse
import json
import subprocess
import sys


def get_issues_with_label(label: str) -> list[dict]:
    """Получить все Issues с указанной меткой."""
    try:
        result = subprocess.run(
            [
                "gh", "issue", "list",
                "--label", label,
                "--state", "all",
                "--json", "number,title,state",
                "--limit", "500"
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        return []
    except FileNotFoundError:
        print("[ERROR] gh CLI не установлен")
        return []


def get_prs_with_label(label: str) -> list[dict]:
    """Получить все PR с указанной меткой."""
    try:
        result = subprocess.run(
            [
                "gh", "pr", "list",
                "--label", label,
                "--state", "all",
                "--json", "number,title,state",
                "--limit", "500"
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        return []
    except FileNotFoundError:
        print("[ERROR] gh CLI не установлен")
        return []


def migrate_issue(number: int, old_label: str, new_label: str | None) -> bool:
    """Мигрировать метку на Issue."""
    cmd = ["gh", "issue", "edit", str(number), "--remove-label", old_label]
    if new_label:
        cmd.extend(["--add-label", new_label])

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Issue #{number}: {e.stderr.decode().strip()}")
        return False


def migrate_pr(number: int, old_label: str, new_label: str | None) -> bool:
    """Мигрировать метку на PR."""
    cmd = ["gh", "pr", "edit", str(number), "--remove-label", old_label]
    if new_label:
        cmd.extend(["--add-label", new_label])

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] PR #{number}: {e.stderr.decode().strip()}")
        return False


def print_plan(
    old_label: str,
    new_label: str | None,
    issues: list[dict],
    prs: list[dict]
) -> None:
    """Вывести план миграции."""
    total = len(issues) + len(prs)

    if total == 0:
        print(f"✅ Метка '{old_label}' не используется на Issues/PR")
        return

    action = f"'{old_label}' → '{new_label}'" if new_label else f"удалить '{old_label}'"
    print(f"📋 План миграции: {action} ({total} элементов)\n")

    if issues:
        print(f"  📝 Issues ({len(issues)}):")
        for issue in issues[:10]:
            state = "🟢" if issue["state"] == "OPEN" else "🟣"
            print(f"     {state} #{issue['number']}: {issue['title'][:50]}")
        if len(issues) > 10:
            print(f"     ... и ещё {len(issues) - 10}")

    if prs:
        print(f"\n  🔀 Pull Requests ({len(prs)}):")
        for pr in prs[:10]:
            state = "🟢" if pr["state"] == "OPEN" else "🟣"
            print(f"     {state} #{pr['number']}: {pr['title'][:50]}")
        if len(prs) > 10:
            print(f"     ... и ещё {len(prs) - 10}")

    print()


def apply_migration(
    old_label: str,
    new_label: str | None,
    issues: list[dict],
    prs: list[dict],
    force: bool = False
) -> bool:
    """Применить миграцию."""
    total = len(issues) + len(prs)

    if total == 0:
        return True

    if not force:
        print_plan(old_label, new_label, issues, prs)
        answer = input("Применить миграцию? [y/N]: ").strip().lower()
        if answer not in ("y", "yes", "д", "да"):
            print("Отменено")
            return False

    success = True
    applied = 0

    # Миграция Issues
    for issue in issues:
        num = issue["number"]
        action = f"→ {new_label}" if new_label else "(удаление)"
        print(f"  📝 Issue #{num} {action}...", end=" ")
        if migrate_issue(num, old_label, new_label):
            print("✅")
            applied += 1
        else:
            success = False

    # Миграция PR
    for pr in prs:
        num = pr["number"]
        action = f"→ {new_label}" if new_label else "(удаление)"
        print(f"  🔀 PR #{num} {action}...", end=" ")
        if migrate_pr(num, old_label, new_label):
            print("✅")
            applied += 1
        else:
            success = False

    print(f"\n{'✅' if success else '⚠️'} Мигрировано {applied}/{total}")
    return success


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Миграция меток на Issues/PR"
    )
    parser.add_argument(
        "old_label",
        help="Метка для замены/удаления"
    )
    parser.add_argument(
        "new_label",
        nargs="?",
        help="Новая метка (если не указана с --delete — удаление)"
    )
    parser.add_argument(
        "--delete", action="store_true",
        help="Удалить метку (без замены)"
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Применить миграцию (без флага — только показать план)"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Применить без подтверждения"
    )

    args = parser.parse_args()

    # Проверка аргументов
    if not args.new_label and not args.delete:
        print("[ERROR] Укажите новую метку или --delete")
        print("Использование:")
        print("  migrate-label.py area:old area:new      # Заменить")
        print("  migrate-label.py area:old --delete      # Удалить")
        sys.exit(1)

    if args.new_label and args.delete:
        print("[ERROR] Нельзя указать и новую метку, и --delete")
        sys.exit(1)

    old_label = args.old_label
    new_label = args.new_label if not args.delete else None

    # Получение данных
    print(f"🔍 Поиск Issues/PR с меткой '{old_label}'...")
    issues = get_issues_with_label(old_label)
    prs = get_prs_with_label(old_label)

    if args.apply:
        success = apply_migration(old_label, new_label, issues, prs, args.force)
        sys.exit(0 if success else 1)
    else:
        print_plan(old_label, new_label, issues, prs)
        total = len(issues) + len(prs)
        if total > 0:
            print("Для применения запустите с флагом --apply")
        sys.exit(0)


if __name__ == "__main__":
    main()
