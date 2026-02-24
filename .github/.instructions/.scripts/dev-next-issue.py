#!/usr/bin/env python3
"""
dev-next-issue.py — Определение следующего незаблокированного Issue.

Из текущей ветки определяет analysis chain, читает plan-dev.md,
извлекает TASK-N с зависимостями, запрашивает Issues через gh CLI
и выводит следующий незаблокированный Issue для работы.
Используется в modify-development.md Шаг 1.

Использование:
    python dev-next-issue.py              # Автоопределение из ветки
    python dev-next-issue.py --json       # JSON вывод

Аргументы:
    --json          JSON вывод
    --repo          Корень репозитория

Примеры:
    python dev-next-issue.py
    python dev-next-issue.py --json

Возвращает:
    0 — найден следующий Issue или все закрыты
    1 — ошибка (нет ветки, нет plan-dev.md, gh недоступен)

Рефакторинг: утилиты (parse_frontmatter, find_repo_root) делегированы
chain_status.ChainManager (SSOT).
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# --- sys.path для импорта chain_status ---
_SPECS_SCRIPTS = Path(__file__).resolve().parent.parent.parent.parent / "specs" / ".instructions" / ".scripts"
if str(_SPECS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SPECS_SCRIPTS))

from chain_status import ChainManager  # noqa: E402


# =============================================================================
# Константы
# =============================================================================

BRANCH_REGEX = re.compile(r'^(\d{4})-.+$')
TASK_HEADING_PATTERN = re.compile(
    r'^####\s+TASK-(\d+):\s+(.+)$', re.MULTILINE
)
DEPS_PATTERN = re.compile(r'\*\*Зависимости:\*\*\s*(.+)')
COMPLEXITY_PATTERN = re.compile(r'\*\*Сложность:\*\*\s*(\d+)/10')
PRIORITY_PATTERN = re.compile(r'\*\*Приоритет:\*\*\s*(high|medium|low)', re.IGNORECASE)
TASK_REF_PATTERN = re.compile(r'TASK-(\d+)')


# =============================================================================
# Утилиты
# =============================================================================

def get_body(content: str) -> str:
    """Получить тело документа без frontmatter."""
    return re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)


def remove_code_blocks(content: str) -> str:
    """Убрать блоки кода из содержимого."""
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', '', content)
    return content


def get_current_branch() -> str:
    """Получить имя текущей ветки."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def gh_issue_list(milestone: str) -> list[dict]:
    """Получить Issues из GitHub через gh CLI."""
    try:
        result = subprocess.run(
            [
                "gh", "issue", "list",
                "--milestone", milestone,
                "--state", "all",
                "--json", "number,title,state,body",
                "--limit", "200",
            ],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка gh issue list: {e.stderr}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("Ошибка: gh CLI не установлен", file=sys.stderr)
        return []


# =============================================================================
# Парсинг TASK-N
# =============================================================================

def extract_tasks(content: str) -> list[dict]:
    """Извлечь все TASK-N из plan-dev.md с зависимостями."""
    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    tasks = []
    task_positions = list(TASK_HEADING_PATTERN.finditer(body_no_code))

    for i, match in enumerate(task_positions):
        task_num = int(match.group(1))
        task_name = match.group(2).strip()
        start = match.end()
        end = (
            task_positions[i + 1].start()
            if i + 1 < len(task_positions)
            else len(body_no_code)
        )
        block = body_no_code[start:end]

        # Извлечь зависимости
        deps_match = DEPS_PATTERN.search(block)
        deps_raw = deps_match.group(1).strip() if deps_match else "—"
        dep_nums = []
        if deps_raw != "—":
            dep_nums = [int(m) for m in TASK_REF_PATTERN.findall(deps_raw)]

        # Извлечь сложность и приоритет
        complexity_match = COMPLEXITY_PATTERN.search(block)
        priority_match = PRIORITY_PATTERN.search(block)

        tasks.append({
            "num": task_num,
            "name": task_name,
            "deps": dep_nums,
            "complexity": complexity_match.group(1) if complexity_match else None,
            "priority": priority_match.group(1).lower() if priority_match else None,
        })

    return tasks


# =============================================================================
# Сопоставление TASK-N → Issue
# =============================================================================

def match_tasks_to_issues(
    tasks: list[dict], issues: list[dict]
) -> dict[int, dict]:
    """Сопоставить TASK-N с Issues по title или body.

    Возвращает dict: task_num → issue dict.
    """
    mapping: dict[int, dict] = {}

    for task in tasks:
        task_ref = f"TASK-{task['num']}"
        task_name_lower = task["name"].lower()

        for issue in issues:
            title = issue.get("title", "")
            body = issue.get("body", "")

            # Ищем TASK-N в title или body
            if task_ref in title or task_ref in body:
                mapping[task["num"]] = issue
                break

            # Fallback: совпадение по имени задачи в title
            if task_name_lower and task_name_lower in title.lower():
                mapping[task["num"]] = issue
                break

    return mapping


# =============================================================================
# Определение следующего Issue
# =============================================================================

def find_next_issue(
    tasks: list[dict], mapping: dict[int, dict]
) -> dict | None:
    """Найти первый незаблокированный открытый Issue по порядку plan-dev.md.

    Возвращает dict с ключами: task, issue или None если все закрыты/заблокированы.
    """
    # Множество закрытых TASK-N
    closed_tasks = set()
    for task in tasks:
        issue = mapping.get(task["num"])
        if issue and issue.get("state") == "CLOSED":
            closed_tasks.add(task["num"])

    # Найти первый открытый незаблокированный
    for task in tasks:
        issue = mapping.get(task["num"])
        if not issue:
            continue
        if issue.get("state") == "CLOSED":
            continue

        # Проверить зависимости
        blocked = False
        blocking_tasks = []
        for dep_num in task["deps"]:
            if dep_num not in closed_tasks:
                blocked = True
                blocking_tasks.append(dep_num)

        if not blocked:
            return {
                "task": task,
                "issue": issue,
                "blocking_tasks": [],
            }

    return None


# =============================================================================
# Форматирование вывода
# =============================================================================

def format_text(
    branch: str,
    milestone: str,
    tasks: list[dict],
    mapping: dict[int, dict],
    next_issue: dict | None,
) -> str:
    """Форматировать результат как текст."""
    total = len(tasks)
    closed = sum(
        1 for t in tasks
        if mapping.get(t["num"], {}).get("state") == "CLOSED"
    )
    unmapped = sum(1 for t in tasks if t["num"] not in mapping)

    lines = [
        f"Ветка: {branch}",
        f"Milestone: {milestone}",
        f"Прогресс: {closed}/{total} Issues закрыты",
    ]

    if unmapped > 0:
        lines.append(f"Внимание: {unmapped} TASK-N без Issue (не сопоставлены)")

    lines.append("")

    if closed == total:
        lines.append("✅ Все Issues закрыты → готово к PR")
    elif next_issue:
        issue = next_issue["issue"]
        task = next_issue["task"]
        number = issue.get("number", "?")
        title = issue.get("title", "?")
        task_num = task["num"]

        deps_str = "— (нет)"
        if task["deps"]:
            deps_str = ", ".join(f"TASK-{d}" for d in task["deps"])

        complexity = task.get("complexity", "?")
        priority = task.get("priority", "?")

        lines.append(f"Следующий: #{number} — {title} (TASK-{task_num})")
        lines.append(f"  Зависимости: {deps_str}")
        lines.append(f"  Сложность: {complexity}/10 | Приоритет: {priority}")
    else:
        lines.append("⚠️ Все открытые Issues заблокированы зависимостями")

    return "\n".join(lines)


def format_json_output(
    branch: str,
    milestone: str,
    tasks: list[dict],
    mapping: dict[int, dict],
    next_issue: dict | None,
) -> str:
    """Форматировать результат как JSON."""
    total = len(tasks)
    closed = sum(
        1 for t in tasks
        if mapping.get(t["num"], {}).get("state") == "CLOSED"
    )

    result = {
        "branch": branch,
        "milestone": milestone,
        "total_tasks": total,
        "closed_tasks": closed,
        "all_done": closed == total,
        "next": None,
    }

    if next_issue:
        issue = next_issue["issue"]
        task = next_issue["task"]
        result["next"] = {
            "issue_number": issue.get("number"),
            "issue_title": issue.get("title"),
            "task_num": task["num"],
            "task_name": task["name"],
            "deps": task["deps"],
            "complexity": task.get("complexity"),
            "priority": task.get("priority"),
        }

    return json.dumps(result, ensure_ascii=False, indent=2)


# =============================================================================
# Точка входа
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Определение следующего незаблокированного Issue"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="JSON вывод"
    )
    parser.add_argument(
        "--repo", default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = ChainManager.find_repo_root(Path(args.repo))

    # 1. Определить ветку
    branch = get_current_branch()
    if not branch:
        print("Ошибка: не удалось определить текущую ветку", file=sys.stderr)
        sys.exit(1)

    branch_match = BRANCH_REGEX.match(branch)
    if not branch_match:
        print(
            f"Ошибка: ветка '{branch}' не соответствует формату NNNN-{{topic}}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 2. Найти plan-dev.md
    chain_dir = repo_root / "specs" / "analysis" / branch
    plan_dev_path = chain_dir / "plan-dev.md"

    if not plan_dev_path.exists():
        print(
            f"Ошибка: {plan_dev_path.relative_to(repo_root)} не найден",
            file=sys.stderr,
        )
        sys.exit(1)

    # 3. Извлечь TASK-N
    plan_dev_content = plan_dev_path.read_text(encoding="utf-8")
    tasks = extract_tasks(plan_dev_content)

    if not tasks:
        print("Ошибка: TASK-N не найдены в plan-dev.md", file=sys.stderr)
        sys.exit(1)

    # 4. Получить milestone
    discussion_path = chain_dir / "discussion.md"
    discussion_fm = ChainManager.parse_frontmatter_file(discussion_path)
    milestone = discussion_fm.get("milestone", "")

    if not milestone:
        # Fallback: из plan-dev.md
        plan_dev_fm = ChainManager.parse_frontmatter_file(plan_dev_path)
        milestone = plan_dev_fm.get("milestone", "")

    if not milestone:
        print("Ошибка: milestone не найден в discussion.md и plan-dev.md",
              file=sys.stderr)
        sys.exit(1)

    # 5. Запросить Issues
    issues = gh_issue_list(milestone)
    if not issues:
        print(
            f"Внимание: Issues для milestone '{milestone}' не найдены",
            file=sys.stderr,
        )

    # 6. Сопоставить TASK-N → Issue
    mapping = match_tasks_to_issues(tasks, issues)

    # 7. Найти следующий
    next_issue = find_next_issue(tasks, mapping)

    # 8. Вывод
    if args.json:
        print(format_json_output(branch, milestone, tasks, mapping, next_issue))
    else:
        print(format_text(branch, milestone, tasks, mapping, next_issue))

    sys.exit(0)


if __name__ == "__main__":
    main()
