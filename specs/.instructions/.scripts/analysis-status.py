#!/usr/bin/env python3
"""
analysis-status.py — Отображение статусов analysis chain цепочек.

Читает frontmatter из 4 документов цепочки (discussion.md, design.md,
plan-test.md, plan-dev.md) и review.md. Выводит сводку по одной цепочке
или по всем. Может обновлять dashboard в specs/analysis/README.md.

Использование:
    python analysis-status.py <NNNN>          # Статус одной цепочки
    python analysis-status.py --all           # Статус всех цепочек
    python analysis-status.py --update        # Обновить dashboard в README

Аргументы:
    NNNN            Номер analysis chain (4 цифры)
    --all           Показать все цепочки
    --update        Обновить dashboard в specs/analysis/README.md

Примеры:
    python analysis-status.py 0001
    python analysis-status.py --all
    python analysis-status.py --update

Возвращает:
    0 — успех
    1 — ошибка (цепочка не найдена, неверный формат)
"""

import argparse
import re
import sys
from pathlib import Path


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def parse_frontmatter(file_path: Path) -> dict:
    """Извлечь frontmatter из markdown-файла."""
    if not file_path.exists():
        return {}
    text = file_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def count_iterations(file_path: Path) -> int:
    """Подсчитать количество итераций в review.md."""
    if not file_path.exists():
        return 0
    text = file_path.read_text(encoding="utf-8")
    return len(re.findall(r"^## Итерация \d+", text, re.MULTILINE))


def count_tasks(file_path: Path) -> int:
    """Подсчитать количество TASK-N в plan-dev.md."""
    if not file_path.exists():
        return 0
    text = file_path.read_text(encoding="utf-8")
    return len(re.findall(r"^### TASK-\d+", text, re.MULTILINE))


STATUS_SHORT = {
    "DRAFT": "D",
    "WAITING": "W",
    "RUNNING": "R",
    "REVIEW": "RV",
    "DONE": "DN",
    "CONFLICT": "C",
    "ROLLING_BACK": "RB",
    "REJECTED": "RJ",
    "OPEN": "OP",
    "RESOLVED": "RS",
}

DOCS = [
    ("Discussion", "discussion.md"),
    ("Design", "design.md"),
    ("Plan Tests", "plan-test.md"),
    ("Plan Dev", "plan-dev.md"),
    ("Review", "review.md"),
]


def get_chain_info(chain_dir: Path) -> dict | None:
    """Получить информацию о цепочке из директории."""
    if not chain_dir.is_dir():
        return None

    info = {
        "nnnn": chain_dir.name[:4],
        "topic": chain_dir.name[5:] if len(chain_dir.name) > 5 else chain_dir.name,
        "full_name": chain_dir.name,
        "docs": {},
    }

    for label, filename in DOCS:
        file_path = chain_dir / filename
        fm = parse_frontmatter(file_path)
        status = fm.get("status", "—")
        info["docs"][label] = status

    # Milestone из discussion.md
    disc_fm = parse_frontmatter(chain_dir / "discussion.md")
    info["milestone"] = disc_fm.get("milestone", "—")

    # TASK-N count
    info["task_count"] = count_tasks(chain_dir / "plan-dev.md")

    # Iteration count for review.md
    info["iteration_count"] = count_iterations(chain_dir / "review.md")

    return info


def get_chain_status(info: dict) -> str:
    """Определить общий статус цепочки (по наименьшему прогрессу 4 основных)."""
    priority = ["DRAFT", "WAITING", "RUNNING", "REVIEW", "DONE",
                "CONFLICT", "ROLLING_BACK", "REJECTED"]
    statuses = [info["docs"].get(label, "—")
                for label, _ in DOCS[:4]]  # Только 4 основных
    for p in priority:
        if p in statuses:
            return p
    return "—"


def print_single(info: dict) -> None:
    """Вывести статус одной цепочки."""
    width = 55
    name = info["full_name"]

    print(f"+-  {name} " + "-" * (width - len(name) - 5) + "+")
    for label, _ in DOCS:
        status = info["docs"].get(label, "—")
        extra = ""
        if label == "Plan Dev" and info["task_count"] > 0:
            extra = f"  ({info['task_count']} TASK-N)"
        if label == "Review" and info["iteration_count"] > 0:
            extra = f"  (итерация {info['iteration_count']})"
        print(f"| {label:<12} {status:<10} {label.lower().replace(' ', '-')}.md{extra}")

    print(f"|")
    print(f"| Milestone:  {info['milestone']}")
    print(f"+" + "-" * (width - 1) + "+")


def print_all(chains: list[dict]) -> None:
    """Вывести сводку по всем цепочкам."""
    if not chains:
        print("Цепочки не найдены в specs/analysis/")
        return

    header = "| NNNN | Тема              | Статус  | D  | DE | PT | PD | Rev | Milestone |"
    sep = "|------|-------------------|---------|----|----|----|----|-----|-----------|"
    print(header)
    print(sep)

    for info in chains:
        nnnn = info["nnnn"]
        topic = info["topic"][:17]
        overall = get_chain_status(info)
        d = STATUS_SHORT.get(info["docs"].get("Discussion", "—"), "—")
        de = STATUS_SHORT.get(info["docs"].get("Design", "—"), "—")
        pt = STATUS_SHORT.get(info["docs"].get("Plan Tests", "—"), "—")
        pd = STATUS_SHORT.get(info["docs"].get("Plan Dev", "—"), "—")
        rev = STATUS_SHORT.get(info["docs"].get("Review", "—"), "—")
        ms = info["milestone"]
        print(f"| {nnnn} | {topic:<17} | {overall:<7} | {d:<2} | {de:<2} | {pt:<2} | {pd:<2} | {rev:<3} | {ms:<9} |")

    print()
    print("Легенда: D=DRAFT, W=WAITING, R=RUNNING, RV=REVIEW, DN=DONE, "
          "C=CONFLICT, RB=ROLLING_BACK, RJ=REJECTED")
    print("         OP=OPEN, RS=RESOLVED")


def update_readme(repo_root: Path, chains: list[dict]) -> bool:
    """Обновить dashboard в specs/analysis/README.md."""
    readme_path = repo_root / "specs" / "analysis" / "README.md"
    if not readme_path.exists():
        print(f"Ошибка: {readme_path} не найден", file=sys.stderr)
        return False

    text = readme_path.read_text(encoding="utf-8")

    begin = "<!-- BEGIN:analysis-status -->"
    end = "<!-- END:analysis-status -->"

    if begin not in text or end not in text:
        print(f"Ошибка: маркеры {begin} / {end} не найдены в README.md",
              file=sys.stderr)
        return False

    # Формируем таблицу
    lines = []
    lines.append("| NNNN | Тема | Disc | Design | P.Test | P.Dev | Review | Branch | Milestone |")
    lines.append("|------|------|------|--------|--------|-------|--------|--------|-----------|")
    for info in chains:
        nnnn = info["nnnn"]
        topic = info["topic"]
        d = STATUS_SHORT.get(info["docs"].get("Discussion", "—"), "—")
        de = STATUS_SHORT.get(info["docs"].get("Design", "—"), "—")
        pt = STATUS_SHORT.get(info["docs"].get("Plan Tests", "—"), "—")
        pd = STATUS_SHORT.get(info["docs"].get("Plan Dev", "—"), "—")
        rev = STATUS_SHORT.get(info["docs"].get("Review", "—"), "—")
        branch = info["full_name"]
        ms = info["milestone"]
        lines.append(f"| {nnnn} | {topic} | {d} | {de} | {pt} | {pd} | {rev} | {branch} | {ms} |")

    table = "\n".join(lines)
    new_block = f"{begin}\n{table}\n{end}"

    pattern = re.compile(
        re.escape(begin) + r".*?" + re.escape(end),
        re.DOTALL,
    )
    new_text = pattern.sub(new_block, text)
    readme_path.write_text(new_text, encoding="utf-8")
    print(f"Dashboard обновлён в {readme_path}")
    return True


def find_all_chains(repo_root: Path) -> list[dict]:
    """Найти все цепочки в specs/analysis/."""
    analysis_dir = repo_root / "specs" / "analysis"
    if not analysis_dir.exists():
        return []

    chains = []
    for d in sorted(analysis_dir.iterdir()):
        if not d.is_dir():
            continue
        if not re.match(r"\d{4}-", d.name):
            continue
        info = get_chain_info(d)
        if info:
            chains.append(info)
    return chains


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Отображение статусов analysis chain цепочек"
    )
    parser.add_argument(
        "nnnn", nargs="?",
        help="Номер analysis chain (4 цифры)"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Показать все цепочки"
    )
    parser.add_argument(
        "--update", action="store_true",
        help="Обновить dashboard в specs/analysis/README.md"
    )
    parser.add_argument(
        "--repo", default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    if not args.nnnn and not args.all and not args.update:
        parser.error("Укажите NNNN, --all или --update")

    if args.all or args.update:
        chains = find_all_chains(repo_root)
        if args.update:
            success = update_readme(repo_root, chains)
            sys.exit(0 if success else 1)
        else:
            print_all(chains)
            sys.exit(0)

    # Одна цепочка
    nnnn = args.nnnn
    analysis_dir = repo_root / "specs" / "analysis"
    matching = [d for d in analysis_dir.iterdir()
                if d.is_dir() and d.name.startswith(nnnn)]

    if not matching:
        print(f"Ошибка: цепочка {nnnn} не найдена в {analysis_dir}",
              file=sys.stderr)
        sys.exit(1)

    if len(matching) > 1:
        print(f"Ошибка: найдено несколько цепочек для {nnnn}: "
              f"{[d.name for d in matching]}", file=sys.stderr)
        sys.exit(1)

    info = get_chain_info(matching[0])
    if info:
        print_single(info)
    sys.exit(0)


if __name__ == "__main__":
    main()
