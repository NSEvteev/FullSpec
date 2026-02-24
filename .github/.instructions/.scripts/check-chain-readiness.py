#!/usr/bin/env python3
"""
check-chain-readiness.py — Проверка готовности analysis chain к разработке.

Читает frontmatter 4 документов цепочки (discussion.md, design.md,
plan-test.md, plan-dev.md), проверяет status=WAITING и отсутствие
маркеров [ТРЕБУЕТ УТОЧНЕНИЯ]. Используется в create-development.md Шаг 1.

Использование:
    python check-chain-readiness.py <NNNN>          # Проверить цепочку
    python check-chain-readiness.py <NNNN> --json   # JSON вывод

Аргументы:
    NNNN            Номер analysis chain (4 цифры)
    --json          JSON вывод
    --repo          Корень репозитория

Примеры:
    python check-chain-readiness.py 0001
    python check-chain-readiness.py 0001 --json

Возвращает:
    0 — цепочка готова (4/4 WAITING, 0 маркеров)
    1 — цепочка НЕ готова
    2 — ошибка аргументов (цепочка не найдена)

Рефакторинг: утилиты (parse_frontmatter, find_repo_root, count_markers,
CHAIN_DOCS) делегированы chain_status.ChainManager (SSOT).
"""

import argparse
import json
import re
import sys
from pathlib import Path


# --- sys.path для импорта chain_status ---
_SPECS_SCRIPTS = Path(__file__).resolve().parent.parent.parent.parent / "specs" / ".instructions" / ".scripts"
if str(_SPECS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SPECS_SCRIPTS))

from chain_status import (  # noqa: E402
    ChainManager, ChainNotFoundError, CHAIN_DOCS,
)


# =============================================================================
# Основная логика
# =============================================================================

def check_readiness(mgr: ChainManager) -> dict:
    """Проверить готовность цепочки через ChainManager.

    Возвращает dict:
        ready: bool — готова ли цепочка
        chain: str — имя папки цепочки
        docs: list[dict] — статус каждого документа
        total_markers: int — общее количество маркеров
    """
    results = {
        "ready": True,
        "chain": mgr.chain_name(),
        "docs": [],
        "total_markers": 0,
    }

    statuses = mgr.status()

    for doc in CHAIN_DOCS:
        doc_path = mgr.chain_dir() / f"{doc}.md"
        doc_info = {
            "name": f"{doc}.md",
            "exists": doc_path.exists(),
            "status": None,
            "status_ok": False,
            "markers": 0,
        }

        if not doc_info["exists"]:
            results["ready"] = False
        else:
            doc_info["status"] = statuses.get(doc, "")
            doc_info["status_ok"] = doc_info["status"] == "WAITING"
            doc_info["markers"] = ChainManager.count_markers(doc_path)
            results["total_markers"] += doc_info["markers"]

            if not doc_info["status_ok"] or doc_info["markers"] > 0:
                results["ready"] = False

        results["docs"].append(doc_info)

    return results


# =============================================================================
# Форматирование вывода
# =============================================================================

def format_text(results: dict) -> str:
    """Форматировать результат как текст."""
    chain = results["chain"]
    waiting_count = sum(1 for d in results["docs"] if d["status_ok"])
    total = len(results["docs"])
    markers = results["total_markers"]

    if results["ready"]:
        return f"✅ {chain} — готова к разработке ({waiting_count}/{total} WAITING, {markers} маркеров)"

    lines = [f"❌ {chain} — НЕ готова:"]
    for doc in results["docs"]:
        name = doc["name"]
        if not doc["exists"]:
            lines.append(f"   {name}: НЕ НАЙДЕН")
        else:
            status = doc["status"] or "—"
            mark = "✓" if doc["status_ok"] else "✗"
            suffix = ""
            if not doc["status_ok"]:
                suffix = f" (ожидается WAITING)"
            if doc["markers"] > 0:
                suffix += f" ({doc['markers']} маркеров [ТРЕБУЕТ УТОЧНЕНИЯ])"
            lines.append(f"   {name}: {status} {mark}{suffix}")

    return "\n".join(lines)


def format_json(results: dict) -> str:
    """Форматировать результат как JSON."""
    return json.dumps(results, ensure_ascii=False, indent=2)


# =============================================================================
# Точка входа
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Проверка готовности analysis chain к разработке"
    )
    parser.add_argument(
        "nnnn",
        help="Номер analysis chain (4 цифры, например 0001)"
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

    # Валидация аргумента
    if not re.match(r'^\d{4}$', args.nnnn):
        print(f"Ошибка: NNNN должен быть 4 цифры, получено: {args.nnnn}",
              file=sys.stderr)
        sys.exit(2)

    repo_root = ChainManager.find_repo_root(Path(args.repo))

    # Найти цепочку через ChainManager
    try:
        mgr = ChainManager(args.nnnn, repo_root=repo_root)
    except ChainNotFoundError:
        print(f"Ошибка: цепочка {args.nnnn} не найдена в specs/analysis/",
              file=sys.stderr)
        sys.exit(2)

    # Проверить готовность
    results = check_readiness(mgr)

    # Вывод
    if args.json:
        print(format_json(results))
    else:
        print(format_text(results))

    sys.exit(0 if results["ready"] else 1)


if __name__ == "__main__":
    main()
