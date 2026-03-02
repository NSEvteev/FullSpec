#!/usr/bin/env python3
"""
validate-issue.py — Валидация GitHub Issue по стандарту.

Проверяет: title, body, labels, assignees, milestone, закрытие, зависимости.

Использование:
    python validate-issue.py 42                          # Валидация Issue #42
    python validate-issue.py --all                       # Все открытые Issues
    python validate-issue.py --milestone "v1.0.0"        # Issues milestone v1.0.0
    python validate-issue.py --all --state closed         # Все закрытые Issues

Примеры:
    python validate-issue.py 42
    python validate-issue.py --all --json
    python validate-issue.py --milestone "v1.0.0" --state all

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
"""

import argparse
import json
import re
import subprocess
import sys


# =============================================================================
# Константы
# =============================================================================

ERROR_CODES = {
    "E001": "Title не начинается с глагола",
    "E002": "Title со строчной буквы",
    "E003": "Title с префиксом типа",
    "E004": "Body пустой",
    "E005": "Нет секции 'Документы для изучения'",
    "E006": "Нет секции 'Критерии готовности' с чек-листом",
    "E007": "Нет метки типа",
    "E008": "Нет метки приоритета",
    "E009": "Несколько меток типа",
    "E010": "Milestone не назначен",
    "E011": "Более 3 assignees",
    "E012": "Закрыт вручную (completed) без PR",
    "E013": "Нет комментария при закрытии not planned",
    "E014": "Зависимость не закрыта при закрытии Issue",
    "E015": "Title слишком короткий (< 50 символов)",
    "E016": "Нет секции 'Задание'",
    "E017": "Нет секции 'Практический контекст'",
}

TITLE_MIN_LENGTH = 50
TITLE_MAX_LENGTH = 70
MAX_ASSIGNEES = 3

# Допустимые имена меток по группам (SSOT: labels.yml)
TYPE_LABELS = {"bug", "task", "docs", "refactor", "feature", "infra", "test"}
PRIORITY_LABELS = {"critical", "high", "medium", "low"}

# Префиксы типов, которые не должны быть в title
TYPE_PREFIXES = re.compile(
    r"^\[?(Bug|Task|Docs|Refactor|Fix|Hotfix|Feature|Infra|Test)\]?\s*:?\s*",
    re.IGNORECASE,
)


# =============================================================================
# GitHub API
# =============================================================================

def gh_api(endpoint: str) -> dict | list | None:
    """Выполнить GET-запрос к GitHub API через gh CLI."""
    cmd = ["gh", "api", "--method", "GET", endpoint]
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


def gh_command(args: list[str]) -> str:
    """Выполнить произвольную gh-команду и вернуть stdout."""
    cmd = ["gh"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def get_repo_path() -> str:
    """Получить owner/repo из текущего репозитория."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[FATAL] Не удалось определить репозиторий.")
        sys.exit(2)


def get_issue(repo: str, number: int) -> dict | None:
    """Получить Issue по номеру."""
    return gh_api(f"repos/{repo}/issues/{number}")


def get_issues_by_state(repo: str, state: str = "open") -> list[dict]:
    """Получить Issues по состоянию."""
    issues = gh_api(f"repos/{repo}/issues?state={state}&per_page=100")
    if not issues:
        return []
    # Фильтруем Pull Requests (API issues возвращает и PR)
    return [i for i in issues if "pull_request" not in i]


def get_issues_by_milestone(repo: str, milestone_title: str, state: str = "open") -> list[dict]:
    """Получить Issues по milestone title."""
    # Сначала найти номер milestone
    milestones = gh_api(f"repos/{repo}/milestones?state=all")
    if not milestones:
        return []
    ms_number = None
    for ms in milestones:
        if ms.get("title") == milestone_title:
            ms_number = ms.get("number")
            break
    if not ms_number:
        return []
    issues = gh_api(f"repos/{repo}/issues?milestone={ms_number}&state={state}&per_page=100")
    if not issues:
        return []
    return [i for i in issues if "pull_request" not in i]


def get_issue_comments(repo: str, number: int) -> list[dict]:
    """Получить комментарии Issue."""
    return gh_api(f"repos/{repo}/issues/{number}/comments") or []


def get_issue_events(repo: str, number: int) -> list[dict]:
    """Получить события Issue (для проверки закрытия через PR)."""
    return gh_api(f"repos/{repo}/issues/{number}/events") or []


# =============================================================================
# Валидация
# =============================================================================

def validate_title(issue: dict) -> list[str]:
    """Шаг 1: Проверить title."""
    errors = []
    title = issue.get("title", "")

    # E003: Префикс типа
    if TYPE_PREFIXES.match(title):
        errors.append(f"[E003] #{issue['number']}: title содержит префикс типа '{title}'")

    # E002: Строчная буква
    clean_title = TYPE_PREFIXES.sub("", title).strip()
    if clean_title and clean_title[0].islower():
        errors.append(f"[E002] #{issue['number']}: title начинается со строчной буквы '{title}'")

    # E015: Слишком короткий
    if len(title) < TITLE_MIN_LENGTH:
        errors.append(f"[E015] #{issue['number']}: title '{title}' — {len(title)} символов (мин. {TITLE_MIN_LENGTH})")

    return errors


def validate_body(issue: dict) -> list[str]:
    """Шаг 2: Проверить body."""
    errors = []
    number = issue.get("number", "?")
    body = issue.get("body") or ""

    # E004: Пустой body
    if not body.strip():
        errors.append(f"[E004] #{number}: body пустой")
        return errors

    lines = body.split("\n")
    lower_lines = [line.strip().lower() for line in lines]

    # E005: Секция "Документы для изучения"
    has_documents = any(
        line.startswith("## ") and "документы для изучения" in line
        for line in lower_lines
    )
    # Также проверяем английский вариант (из шаблонов)
    if not has_documents:
        has_documents = any(
            line.startswith("### documents") or line.startswith("## documents")
            for line in lower_lines
        )
    if not has_documents:
        errors.append(f"[E005] #{number}: отсутствует секция 'Документы для изучения'")

    # E016: Секция "Задание"
    has_assignment = any(
        line.startswith("## ") and line.strip() == "## задание"
        for line in lower_lines
    )
    if not has_assignment:
        has_assignment = any(
            line.startswith("## ") and "assignment" in line
            for line in lower_lines
        )
    if not has_assignment:
        errors.append(f"[E016] #{number}: отсутствует секция 'Задание'")

    # E017: Секция "Практический контекст"
    has_practical = any(
        line.startswith("## ") and "практический контекст" in line
        for line in lower_lines
    )
    if not has_practical:
        has_practical = any(
            line.startswith("## ") and "practical context" in line
            for line in lower_lines
        )
    if not has_practical:
        errors.append(f"[E017] #{number}: отсутствует секция 'Практический контекст'")

    # E006: Секция "Критерии готовности"
    has_criteria = False
    in_criteria = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") and "критери" in stripped.lower():
            in_criteria = True
            continue
        if stripped.startswith("## ") and in_criteria:
            break
        if in_criteria and stripped.startswith("- [ ]"):
            has_criteria = True
            break

    if not has_criteria:
        errors.append(f"[E006] #{number}: отсутствует секция 'Критерии готовности' с чек-листом")

    return errors


def validate_labels(issue: dict) -> list[str]:
    """Шаг 3: Проверить labels."""
    errors = []
    number = issue.get("number", "?")
    labels = [label.get("name", "") for label in issue.get("labels", [])]

    type_labels = [l for l in labels if l in TYPE_LABELS]
    priority_labels = [l for l in labels if l in PRIORITY_LABELS]

    # E007: Нет метки типа
    if len(type_labels) == 0:
        errors.append(f"[E007] #{number}: нет метки типа ({', '.join(sorted(TYPE_LABELS))})")

    # E009: Несколько меток типа
    if len(type_labels) > 1:
        errors.append(f"[E009] #{number}: несколько меток типа ({', '.join(type_labels)})")

    # E008: Нет метки приоритета
    if len(priority_labels) == 0:
        errors.append(f"[E008] #{number}: нет метки приоритета ({', '.join(sorted(PRIORITY_LABELS))})")

    return errors


def validate_assignees(issue: dict) -> list[str]:
    """Шаг 4: Проверить assignees."""
    errors = []
    number = issue.get("number", "?")
    assignees = issue.get("assignees", [])

    # E011: Более 3
    if len(assignees) > MAX_ASSIGNEES:
        errors.append(f"[E011] #{number}: {len(assignees)} assignees (макс. {MAX_ASSIGNEES})")

    return errors


def validate_milestone(issue: dict) -> list[str]:
    """Шаг 5: Проверить milestone."""
    errors = []
    number = issue.get("number", "?")

    # E010: Milestone не назначен
    if not issue.get("milestone"):
        errors.append(f"[E010] #{number}: milestone не назначен")

    return errors


def validate_closing(issue: dict, repo: str) -> list[str]:
    """Шаг 6: Проверить закрытие (для closed Issues)."""
    errors = []
    number = issue.get("number", "?")
    state = issue.get("state", "open")

    if state != "closed":
        return errors

    state_reason = issue.get("state_reason", "")

    if state_reason == "completed":
        # E012: Закрыт с completed — должен быть merged PR
        events = get_issue_events(repo, issue["number"])
        closed_by_pr = any(
            event.get("event") == "closed"
            and event.get("commit_id") is not None
            for event in events
        )
        if not closed_by_pr:
            errors.append(f"[E012] #{number}: закрыт с reason 'completed' без PR")

    elif state_reason == "not_planned":
        # E013: Должен быть комментарий
        comments = get_issue_comments(repo, issue["number"])
        if not comments:
            errors.append(f"[E013] #{number}: закрыт 'not planned' без комментария с причиной")

    return errors


def validate_dependencies(issue: dict, repo: str) -> list[str]:
    """Шаг 7: Проверить зависимости."""
    errors = []
    number = issue.get("number", "?")
    state = issue.get("state", "open")
    body = issue.get("body") or ""

    # Ищем строку "**Зависит от:** #N, #M"
    dep_match = re.search(r"\*\*Зависит от:\*\*\s*(.*)", body)
    if not dep_match:
        return errors

    dep_text = dep_match.group(1)
    dep_numbers = [int(n) for n in re.findall(r"#(\d+)", dep_text)]

    if not dep_numbers:
        return errors

    # E014: Для закрытого Issue — зависимости должны быть закрыты
    if state == "closed":
        for dep_num in dep_numbers:
            dep_issue = get_issue(repo, dep_num)
            if dep_issue and dep_issue.get("state") != "closed":
                errors.append(
                    f"[E014] #{number}: зависимость #{dep_num} не закрыта"
                )

    return errors


def validate_issue(issue: dict, repo: str) -> list[str]:
    """Полная валидация одного Issue."""
    errors = []
    errors.extend(validate_title(issue))
    errors.extend(validate_body(issue))
    errors.extend(validate_labels(issue))
    errors.extend(validate_assignees(issue))
    errors.extend(validate_milestone(issue))
    errors.extend(validate_closing(issue, repo))
    errors.extend(validate_dependencies(issue, repo))
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
        description="Валидация GitHub Issue по стандарту"
    )
    parser.add_argument("number", nargs="?", type=int, help="Номер Issue для валидации")
    parser.add_argument("--all", action="store_true", help="Валидация всех Issues")
    parser.add_argument("--milestone", help="Валидация Issues конкретного milestone")
    parser.add_argument(
        "--state", default="open", choices=["open", "closed", "all"],
        help="Состояние Issues (по умолчанию: open)"
    )
    parser.add_argument("--json", action="store_true", help="Вывод в формате JSON")

    args = parser.parse_args()

    if not args.number and not args.all and not args.milestone:
        parser.error("Укажите номер Issue, --all или --milestone")

    repo = get_repo_path()
    all_results: list[dict] = []

    if args.number:
        issue = get_issue(repo, args.number)
        if not issue:
            print(f"[FATAL] Issue #{args.number} не найден")
            sys.exit(2)
        if "pull_request" in issue:
            print(f"[FATAL] #{args.number} — это Pull Request, не Issue")
            sys.exit(2)
        errors = validate_issue(issue, repo)
        all_results.append({"number": args.number, "title": issue.get("title", ""), "errors": errors})

    else:
        if args.milestone:
            issues = get_issues_by_milestone(repo, args.milestone, args.state)
            empty_msg = f"Нет Issues в milestone '{args.milestone}' (state={args.state})"
        else:  # args.all
            issues = get_issues_by_state(repo, args.state)
            empty_msg = f"Нет Issues (state={args.state})"

        if not issues:
            print(empty_msg)
            sys.exit(0)
        for issue in issues:
            errors = validate_issue(issue, repo)
            all_results.append({
                "number": issue["number"],
                "title": issue.get("title", ""),
                "errors": errors,
            })

    # Вывод результатов
    total_errors = sum(len(entry["errors"]) for entry in all_results)

    if args.json:
        result = {
            "issues": [
                {
                    "number": entry["number"],
                    "title": entry["title"],
                    "errors": entry["errors"],
                    "valid": len(entry["errors"]) == 0,
                }
                for entry in all_results
            ],
            "total_errors": total_errors,
            "valid": total_errors == 0,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for entry in all_results:
            num = entry["number"]
            title = entry["title"]
            errors = entry["errors"]
            if errors:
                print(f"❌ #{num} «{title}» — {len(errors)} ошибок:")
                for err in errors:
                    print(f"   {err}")
            else:
                print(f"✅ #{num} «{title}» — валидация пройдена")

        if len(all_results) > 1:
            valid_count = sum(1 for e in all_results if not e["errors"])
            print(f"\nИтого: {total_errors} ошибок в {len(all_results)} Issues ({valid_count} валидных)")

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
