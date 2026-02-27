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

Рефакторинг: утилиты (parse_frontmatter, find_repo_root, count_iterations,
find_all_chains) делегированы chain_status.ChainManager (SSOT).
"""

import argparse
import re
import sys
from pathlib import Path

# --- sys.path для импорта chain_status из той же директории ---
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from chain_status import ChainManager, CHAIN_DOCS  # noqa: E402


# =============================================================================
# Константы (display-only, не дублируют chain_status)
# =============================================================================

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

DOCS_DISPLAY = [
    ("Discussion", "discussion"),
    ("Design", "design"),
    ("Plan Tests", "plan-test"),
    ("Plan Dev", "plan-dev"),
    ("Review", "review"),
]


def count_tasks(file_path: Path) -> int:
    """Подсчитать количество TASK-N в plan-dev.md."""
    if not file_path.exists():
        return 0
    text = file_path.read_text(encoding="utf-8")
    return len(re.findall(r"^### TASK-\d+", text, re.MULTILINE))


# =============================================================================
# Логика
# =============================================================================

def get_chain_info(chain_dir: Path, repo_root: Path) -> dict | None:
    """Получить информацию о цепочке из директории."""
    if not chain_dir.is_dir():
        return None

    info = {
        "nnnn": chain_dir.name[:4],
        "topic": chain_dir.name[5:] if len(chain_dir.name) > 5 else chain_dir.name,
        "full_name": chain_dir.name,
        "docs": {},
    }

    # Статусы через ChainManager.parse_frontmatter_file (SSOT)
    for label, doc_name in DOCS_DISPLAY:
        fm = ChainManager.parse_frontmatter_file(chain_dir / f"{doc_name}.md")
        info["docs"][label] = fm.get("status", "—")

    # Milestone из discussion.md
    disc_fm = ChainManager.parse_frontmatter_file(chain_dir / "discussion.md")
    info["milestone"] = disc_fm.get("milestone", "—")

    # docs-synced из design.md
    design_fm = ChainManager.parse_frontmatter_file(chain_dir / "design.md")
    info["docs_synced"] = design_fm.get("docs-synced", "—")

    # TASK-N count (специфично для этого скрипта)
    info["task_count"] = count_tasks(chain_dir / "plan-dev.md")

    # Iteration count через ChainManager.count_iterations (SSOT)
    info["iteration_count"] = ChainManager.count_iterations(chain_dir / "review.md")

    return info


def get_chain_status(info: dict) -> str:
    """Определить общий статус цепочки (по наименьшему прогрессу 4 основных)."""
    priority = ["DRAFT", "WAITING", "RUNNING", "REVIEW", "DONE",
                "CONFLICT", "ROLLING_BACK", "REJECTED"]
    statuses = [info["docs"].get(label, "—")
                for label, _ in DOCS_DISPLAY[:4]]  # Только 4 основных
    for p in priority:
        if p in statuses:
            return p
    return "—"


def print_single(info: dict) -> None:
    """Вывести статус одной цепочки."""
    width = 55
    name = info["full_name"]

    print(f"+-  {name} " + "-" * (width - len(name) - 5) + "+")
    for label, doc_name in DOCS_DISPLAY:
        status = info["docs"].get(label, "—")
        extra = ""
        if label == "Plan Dev" and info["task_count"] > 0:
            extra = f"  ({info['task_count']} TASK-N)"
        if label == "Review" and info["iteration_count"] > 0:
            extra = f"  (итерация {info['iteration_count']})"
        print(f"| {label:<12} {status:<10} {doc_name}.md{extra}")

    # docs-synced маркер (из design.md frontmatter)
    docs_synced = info.get("docs_synced", "—")
    if docs_synced == "true":
        print(f"| {'Docs Sync':<12} {'done':<10} docs-synced: true")
    elif docs_synced == "—":
        print(f"| {'Docs Sync':<12} {'pending':<10} docs-synced: —")

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


def update_readme(repo_root: Path) -> bool:
    """Обновить dashboard в specs/analysis/README.md через ChainManager."""
    chain_names = ChainManager.find_all_chains(repo_root)
    if not chain_names:
        print("Нет цепочек — dashboard не обновлён")
        return True

    # Создаём ChainManager для первой цепочки — _update_readme_dashboard
    # перегенерирует ВСЮ таблицу (все цепочки), не только текущую
    try:
        mgr = ChainManager(chain_names[0][:4], repo_root=repo_root)
        mgr._update_readme_dashboard()
        print(f"Dashboard обновлён в specs/analysis/README.md")
        return True
    except Exception as e:
        print(f"Ошибка при обновлении dashboard: {e}", file=sys.stderr)
        return False


def find_all_chains_info(repo_root: Path) -> list[dict]:
    """Найти все цепочки и собрать информацию через ChainManager."""
    analysis_dir = repo_root / "specs" / "analysis"
    chain_names = ChainManager.find_all_chains(repo_root)
    chains = []
    for name in chain_names:
        chain_dir = analysis_dir / name
        info = get_chain_info(chain_dir, repo_root)
        if info:
            chains.append(info)
    return chains


# =============================================================================
# Точка входа
# =============================================================================

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
    repo_root = ChainManager.find_repo_root(Path(args.repo))

    if not args.nnnn and not args.all and not args.update:
        parser.error("Укажите NNNN, --all или --update")

    if args.all or args.update:
        if args.update:
            success = update_readme(repo_root)
            sys.exit(0 if success else 1)
        else:
            chains = find_all_chains_info(repo_root)
            print_all(chains)
            sys.exit(0)

    # Одна цепочка
    try:
        mgr = ChainManager(args.nnnn, repo_root=repo_root)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    info = get_chain_info(mgr.chain_dir(), repo_root)
    if info:
        print_single(info)
    sys.exit(0)


if __name__ == "__main__":
    main()
