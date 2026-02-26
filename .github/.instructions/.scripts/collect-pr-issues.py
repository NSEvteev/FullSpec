#!/usr/bin/env python3
"""
collect-pr-issues.py — Сбор Issues из analysis chain для создания PR.

Парсит plan-dev.md (маппинг TASK-N → Issue), discussion.md (metadata),
проверяет статус Issues через gh CLI, определяет suggested_type из TYPE-меток.

Использование:
    python collect-pr-issues.py <NNNN>
    python collect-pr-issues.py <NNNN> --repo /path/to/repo

Примеры:
    python collect-pr-issues.py 0001
    python collect-pr-issues.py 0042 --repo .

Возвращает:
    JSON на stdout с полями: chain, topic, milestone, branch, description,
    issues, suggested_type, suggested_priority, suggested_title, existing_pr, errors.

    Exit code 0 — всегда (ошибки в поле errors JSON).
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


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


def run_gh(args: list[str]) -> tuple[str, bool]:
    """Выполнить gh CLI команду. Возвращает (stdout, success)."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True, text=True, encoding="utf-8", timeout=30
        )
        return result.stdout.strip(), result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "", False


def parse_frontmatter(text: str) -> dict[str, str]:
    """Извлечь frontmatter из markdown-файла."""
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm


# =============================================================================
# Поиск chain
# =============================================================================

def find_chain_dir(repo_root: Path, chain: str) -> Path | None:
    """Найти папку chain в specs/analysis/."""
    analysis_dir = repo_root / "specs" / "analysis"
    if not analysis_dir.exists():
        return None
    for d in analysis_dir.iterdir():
        if d.is_dir() and d.name.startswith(f"{chain}-"):
            return d
    return None


def extract_topic_from_dir(chain_dir: Path) -> str:
    """Извлечь topic из имени папки chain."""
    name = chain_dir.name
    # Формат: NNNN-topic
    parts = name.split("-", 1)
    return parts[1] if len(parts) > 1 else ""


# =============================================================================
# Парсинг plan-dev.md
# =============================================================================

def parse_plan_dev_issues(plan_dev_path: Path) -> list[dict]:
    """Парсить таблицу маппинга TASK-N → Issue из plan-dev.md."""
    if not plan_dev_path.exists():
        return []
    text = plan_dev_path.read_text(encoding="utf-8")

    # Ищем секцию "Маппинг GitHub Issues"
    mapping_match = re.search(
        r"##\s+Маппинг GitHub Issues\s*\n(.*?)(?=\n##\s|\Z)",
        text, re.DOTALL
    )
    if not mapping_match:
        return []

    section = mapping_match.group(1)
    issues = []

    # Ищем строки таблицы с Issue номерами: | TASK-N | #NN |
    for match in re.finditer(
        r"\|\s*(TASK-\d+)\s*\|\s*#(\d+)\s*\|", section
    ):
        issues.append({
            "task": match.group(1),
            "number": int(match.group(2))
        })

    # Также ищем формат | TASK-N | Отдельный Issue ... #NN |
    if not issues:
        for match in re.finditer(r"#(\d+)", section):
            num = int(match.group(1))
            if num > 0:
                issues.append({"task": "", "number": num})

    return issues


# =============================================================================
# Парсинг discussion.md
# =============================================================================

def parse_discussion_metadata(chain_dir: Path) -> dict[str, str]:
    """Парсить frontmatter discussion.md → milestone, description."""
    discussion_path = chain_dir / "discussion.md"
    if not discussion_path.exists():
        return {}
    text = discussion_path.read_text(encoding="utf-8")
    return parse_frontmatter(text)


# =============================================================================
# GitHub API
# =============================================================================

def get_issue_details(issue_numbers: list[int]) -> list[dict]:
    """Получить детали Issues через gh CLI."""
    details = []
    for num in issue_numbers:
        stdout, ok = run_gh([
            "issue", "view", str(num),
            "--json", "number,title,state,labels"
        ])
        if ok and stdout:
            try:
                data = json.loads(stdout)
                details.append(data)
            except json.JSONDecodeError:
                pass
    return details


def check_existing_pr(branch: str) -> int | None:
    """Проверить существующий PR для ветки."""
    stdout, ok = run_gh([
        "pr", "list", "--head", branch,
        "--json", "number", "--limit", "1"
    ])
    if ok and stdout:
        try:
            prs = json.loads(stdout)
            if prs:
                return prs[0]["number"]
        except json.JSONDecodeError:
            pass
    return None


def determine_suggested_type(issue_details: list[dict]) -> str:
    """Определить suggested_type из TYPE-меток Issues."""
    type_labels = {"bug", "task", "docs", "refactor"}
    type_counts: dict[str, int] = {}

    for issue in issue_details:
        for label in issue.get("labels", []):
            name = label.get("name", "")
            if name in type_labels:
                type_counts[name] = type_counts.get(name, 0) + 1

    if not type_counts:
        return "task"  # Default
    return max(type_counts, key=type_counts.get)


def determine_suggested_priority(issue_details: list[dict]) -> str:
    """Определить suggested_priority из PRIORITY-меток Issues."""
    priority_labels = {"critical", "high", "medium", "low"}
    priority_order = ["critical", "high", "medium", "low"]
    found = set()

    for issue in issue_details:
        for label in issue.get("labels", []):
            name = label.get("name", "")
            if name in priority_labels:
                found.add(name)

    # Наивысший приоритет
    for p in priority_order:
        if p in found:
            return p
    return "medium"  # Default


# =============================================================================
# Main
# =============================================================================

def collect(chain: str, repo_root: Path) -> dict:
    """Основная логика сбора данных."""
    result = {
        "chain": chain,
        "topic": "",
        "milestone": "",
        "branch": "",
        "description": "",
        "issues": [],
        "suggested_type": "task",
        "suggested_priority": "medium",
        "suggested_title": "",
        "existing_pr": None,
        "errors": []
    }

    # Найти папку chain
    chain_dir = find_chain_dir(repo_root, chain)
    if not chain_dir:
        result["errors"].append("no_chain")
        return result

    topic = extract_topic_from_dir(chain_dir)
    result["topic"] = topic
    result["branch"] = f"{chain}-{topic}"

    # Парсить discussion.md
    metadata = parse_discussion_metadata(chain_dir)
    result["milestone"] = metadata.get("milestone", "")
    result["description"] = metadata.get("description", "")

    # Парсить plan-dev.md
    plan_dev_path = chain_dir / "plan-dev.md"
    if not plan_dev_path.exists():
        result["errors"].append("no_plan_dev")
        return result

    parsed_issues = parse_plan_dev_issues(plan_dev_path)
    if not parsed_issues:
        result["errors"].append("no_issues")
        return result

    issue_numbers = [i["number"] for i in parsed_issues]
    task_map = {i["number"]: i["task"] for i in parsed_issues}

    # Получить детали Issues через gh CLI
    issue_details = get_issue_details(issue_numbers)

    # Проверить: все закрыты?
    all_closed = all(
        d.get("state") == "CLOSED" for d in issue_details
    ) if issue_details else False
    if all_closed and issue_details:
        result["errors"].append("all_closed")

    # Заполнить issues
    for detail in issue_details:
        num = detail.get("number", 0)
        result["issues"].append({
            "number": num,
            "title": detail.get("title", ""),
            "state": detail.get("state", "").lower(),
            "task": task_map.get(num, "")
        })

    # Определить type и priority
    result["suggested_type"] = determine_suggested_type(issue_details)
    result["suggested_priority"] = determine_suggested_priority(issue_details)

    # Suggested title
    desc = result["description"]
    stype = result["suggested_type"]
    max_desc_len = 70 - len(stype) - 2  # "{type}: {desc}"
    if desc and len(desc) > max_desc_len:
        desc = desc[:max_desc_len - 3] + "..."
    result["suggested_title"] = f"{stype}: {desc.lower()}" if desc else ""

    # Проверить существующий PR
    branch = result["branch"]
    existing = check_existing_pr(branch)
    if existing:
        result["existing_pr"] = existing
        result["errors"].append("pr_exists")

    return result


def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Сбор Issues из analysis chain для создания PR"
    )
    parser.add_argument(
        "chain",
        help="Номер chain (NNNN), например 0001"
    )
    parser.add_argument(
        "--repo", default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    result = collect(args.chain, repo_root)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
