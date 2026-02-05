#!/usr/bin/env python3
"""
validate-milestone.py — Валидация GitHub Milestone по стандарту.

Проверяет: title (SemVer), description, due date, Issues, связь с Release.

Использование:
    python validate-milestone.py --number 3           # Валидация Milestone #3
    python validate-milestone.py --title "v1.0.0"     # Валидация по title
    python validate-milestone.py --all                 # Валидация всех открытых
    python validate-milestone.py --all --state closed  # Валидация всех закрытых

Примеры:
    python validate-milestone.py --number 3
    python validate-milestone.py --title "v1.0.0" --json
    python validate-milestone.py --all --state all

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone


# =============================================================================
# Константы
# =============================================================================

ERROR_CODES = {
    "E001": "Title не соответствует SemVer формату vX.Y.Z",
    "E002": "Title без обязательного префикса 'v'",
    "E003": "Дубликат title (Milestone с таким title уже существует)",
    "E004": "Description пустой",
    "E005": "Отсутствует секция 'Критерии готовности' с чек-листом",
    "E006": "Due date не установлен",
    "E007": "Due date просрочен (для открытых Milestones)",
    "E008": "Milestone перегружен (более 20 Issues)",
    "E009": "Milestone пустой (нет Issues)",
    "E010": "Закрыт с открытыми Issues",
    "E011": "Нет Release для закрытого Milestone",
    "E012": "Нет ссылки на Milestone в Release Notes",
}

# SemVer regex: vMAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
SEMVER_PATTERN = re.compile(
    r"^v"
    r"(?P<major>0|[1-9]\d*)"
    r"\."
    r"(?P<minor>0|[1-9]\d*)"
    r"\."
    r"(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*))?"
    r"(?:\+(?P<build>[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*))?"
    r"$"
)

MAX_TITLE_LENGTH = 50
MAX_ISSUES = 20
OVERDUE_GRACE_DAYS = 7


# =============================================================================
# GitHub API
# =============================================================================

def gh_api(endpoint: str, method: str = "GET", fields: dict | None = None) -> dict | list | None:
    """Выполнить запрос к GitHub API через gh CLI."""
    cmd = ["gh", "api", "--method", method, endpoint]
    if fields:
        for key, value in fields.items():
            cmd.extend(["-f", f"{key}={value}"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=True)
        return json.loads(result.stdout) if result.stdout.strip() else None
    except subprocess.CalledProcessError as e:
        if "404" in (e.stderr or ""):
            return None
        return None
    except FileNotFoundError:
        print("[FATAL] gh CLI не установлен")
        sys.exit(2)


def get_repo_path() -> str:
    """Получить owner/repo из текущего репозитория."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[FATAL] Не удалось определить репозиторий. Убедитесь, что вы в git-репозитории с remote.")
        sys.exit(2)


def get_milestone_by_number(repo: str, number: int) -> dict | None:
    """Получить Milestone по номеру."""
    return gh_api(f"repos/{repo}/milestones/{number}")


def get_milestone_by_title(repo: str, title: str) -> dict | None:
    """Получить Milestone по title."""
    for state in ("open", "closed"):
        milestones = gh_api(f"repos/{repo}/milestones", fields={"state": state})
        if milestones:
            for ms in milestones:
                if ms.get("title") == title:
                    return ms
    return None


def get_all_milestones(repo: str, state: str = "open") -> list[dict]:
    """Получить все Milestones."""
    if state == "all":
        result = []
        for s in ("open", "closed"):
            ms = gh_api(f"repos/{repo}/milestones", fields={"state": s})
            if ms:
                result.extend(ms)
        return result
    ms = gh_api(f"repos/{repo}/milestones", fields={"state": state})
    return ms or []


def get_all_milestone_titles(repo: str) -> list[str]:
    """Получить titles всех Milestones для проверки уникальности."""
    titles = []
    for state in ("open", "closed"):
        milestones = gh_api(f"repos/{repo}/milestones", fields={"state": state})
        if milestones:
            for ms in milestones:
                titles.append(ms.get("title", ""))
    return titles


def get_release_by_tag(repo: str, tag: str) -> dict | None:
    """Получить Release по тегу."""
    return gh_api(f"repos/{repo}/releases/tags/{tag}")


# =============================================================================
# Валидация
# =============================================================================

def validate_title(milestone: dict, all_titles: list[str]) -> list[str]:
    """Шаг 1: Проверить title (SemVer)."""
    errors = []
    title = milestone.get("title", "")

    # E002: Префикс v
    if not title.startswith("v"):
        errors.append(f"[E002] '{title}': отсутствует префикс 'v'")
        return errors  # Дальше нет смысла проверять SemVer

    # E001: SemVer формат
    if not SEMVER_PATTERN.match(title):
        errors.append(f"[E001] '{title}': не соответствует формату vMAJOR.MINOR.PATCH[-PRERELEASE]")

    # Длина
    if len(title) > MAX_TITLE_LENGTH:
        errors.append(f"[E001] '{title}': длина {len(title)} > {MAX_TITLE_LENGTH} символов")

    # E003: Уникальность
    count = all_titles.count(title)
    if count > 1:
        errors.append(f"[E003] '{title}': дубликат (найдено {count} Milestones с таким title)")

    return errors


def validate_description(milestone: dict) -> list[str]:
    """Шаг 2: Проверить description."""
    errors = []
    title = milestone.get("title", "")
    desc = milestone.get("description") or ""

    # E004: Пустой description
    if not desc.strip():
        errors.append(f"[E004] '{title}': description пустой")
        return errors

    # E005: Секция "Критерии готовности" с чек-листом
    has_criteria = False
    lines = desc.split("\n")
    in_criteria_section = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") and "критери" in stripped.lower():
            in_criteria_section = True
            continue
        if stripped.startswith("## ") and in_criteria_section:
            break
        if in_criteria_section and stripped.startswith("- [ ]"):
            has_criteria = True
            break

    if not has_criteria:
        errors.append(f"[E005] '{title}': отсутствует секция 'Критерии готовности' с чек-листом '- [ ]'")

    # Проверка секции "Цель"
    has_goal = any(
        line.strip().startswith("## ") and "цель" in line.strip().lower()
        for line in lines
    )
    if not has_goal:
        errors.append(f"[E004] '{title}': отсутствует секция 'Цель'")

    return errors


def validate_due_date(milestone: dict) -> list[str]:
    """Шаг 3: Проверить due date."""
    errors = []
    title = milestone.get("title", "")
    due_on = milestone.get("due_on")
    state = milestone.get("state", "open")

    # E006: Due date не установлен
    if not due_on:
        errors.append(f"[E006] '{title}': due date не установлен")
        return errors

    # E007: Due date просрочен (только для открытых)
    if state == "open":
        try:
            due_date = datetime.fromisoformat(due_on.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            overdue_days = (now - due_date).days

            if overdue_days > OVERDUE_GRACE_DAYS:
                errors.append(
                    f"[E007] '{title}': due date просрочен на {overdue_days} дней "
                    f"(допустимо до {OVERDUE_GRACE_DAYS})"
                )
        except (ValueError, TypeError):
            errors.append(f"[E006] '{title}': невалидный формат due date '{due_on}'")

    return errors


def validate_issues(milestone: dict) -> list[str]:
    """Шаг 4: Проверить Issues."""
    errors = []
    title = milestone.get("title", "")
    open_issues = milestone.get("open_issues", 0)
    closed_issues = milestone.get("closed_issues", 0)
    total = open_issues + closed_issues
    state = milestone.get("state", "open")

    # E009: Milestone пустой
    if total == 0:
        errors.append(f"[E009] '{title}': нет Issues (пустой Milestone)")

    # E008: Перегружен
    if total > MAX_ISSUES:
        errors.append(f"[E008] '{title}': {total} Issues (макс. {MAX_ISSUES})")

    # E010: Закрыт с открытыми Issues
    if state == "closed" and open_issues > 0:
        errors.append(f"[E010] '{title}': закрыт с {open_issues} открытыми Issues")

    return errors


def validate_release(milestone: dict, repo: str) -> list[str]:
    """Шаг 5: Проверить связь с Release (для закрытых)."""
    errors = []
    title = milestone.get("title", "")
    state = milestone.get("state", "open")

    # Только для закрытых Milestones
    if state != "closed":
        return errors

    # E011: Существует ли Release
    release = get_release_by_tag(repo, title)
    if not release:
        errors.append(f"[E011] '{title}': нет GitHub Release с тегом '{title}'")
        return errors

    # E012: Ссылка на Milestone в Release Notes
    body = release.get("body") or ""
    if "milestone" not in body.lower() and "Milestone" not in body:
        errors.append(f"[E012] '{title}': в Release Notes нет ссылки на Milestone")

    return errors


def validate_milestone(milestone: dict, repo: str, all_titles: list[str]) -> list[str]:
    """Полная валидация одного Milestone."""
    errors = []
    errors.extend(validate_title(milestone, all_titles))
    errors.extend(validate_description(milestone))
    errors.extend(validate_due_date(milestone))
    errors.extend(validate_issues(milestone))
    errors.extend(validate_release(milestone, repo))
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
        description="Валидация GitHub Milestone по стандарту"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--number", type=int, help="Номер Milestone для валидации")
    group.add_argument("--title", help="Title Milestone для валидации")
    group.add_argument("--all", action="store_true", help="Валидация всех Milestones")
    parser.add_argument(
        "--state", default="open", choices=["open", "closed", "all"],
        help="Состояние Milestones для --all (по умолчанию: open)"
    )
    parser.add_argument("--json", action="store_true", help="Вывод в формате JSON")

    args = parser.parse_args()

    repo = get_repo_path()
    all_titles = get_all_milestone_titles(repo)
    all_errors: list[dict] = []  # [{milestone: title, errors: [...]}]

    if args.number:
        ms = get_milestone_by_number(repo, args.number)
        if not ms:
            print(f"[FATAL] Milestone #{args.number} не найден")
            sys.exit(2)
        errors = validate_milestone(ms, repo, all_titles)
        all_errors.append({"milestone": ms.get("title", f"#{args.number}"), "errors": errors})

    elif args.title:
        ms = get_milestone_by_title(repo, args.title)
        if not ms:
            print(f"[FATAL] Milestone '{args.title}' не найден")
            sys.exit(2)
        errors = validate_milestone(ms, repo, all_titles)
        all_errors.append({"milestone": args.title, "errors": errors})

    elif args.all:
        milestones = get_all_milestones(repo, args.state)
        if not milestones:
            print(f"Нет Milestones со статусом '{args.state}'")
            sys.exit(0)
        for ms in milestones:
            errors = validate_milestone(ms, repo, all_titles)
            all_errors.append({"milestone": ms.get("title", "?"), "errors": errors})

    # Вывод результатов
    total_errors = sum(len(entry["errors"]) for entry in all_errors)

    if args.json:
        result = {
            "milestones": [
                {"title": entry["milestone"], "errors": entry["errors"], "valid": len(entry["errors"]) == 0}
                for entry in all_errors
            ],
            "total_errors": total_errors,
            "valid": total_errors == 0,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for entry in all_errors:
            title = entry["milestone"]
            errors = entry["errors"]
            if errors:
                print(f"❌ {title} — {len(errors)} ошибок:")
                for err in errors:
                    print(f"   {err}")
            else:
                print(f"✅ {title} — валидация пройдена")

        if len(all_errors) > 1:
            print(f"\nИтого: {total_errors} ошибок в {len(all_errors)} Milestones")

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
