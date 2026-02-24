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
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

CHAIN_DOCS = ["discussion.md", "design.md", "plan-test.md", "plan-dev.md"]
MARKER_PATTERN = re.compile(r'\[ТРЕБУЕТ УТОЧНЕНИЯ\]')
FOLDER_REGEX = re.compile(r'^\d{4}-.+$')


# =============================================================================
# Утилиты
# =============================================================================

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


def count_markers(file_path: Path) -> int:
    """Посчитать маркеры [ТРЕБУЕТ УТОЧНЕНИЯ] в файле."""
    if not file_path.exists():
        return 0
    text = file_path.read_text(encoding="utf-8")
    return len(MARKER_PATTERN.findall(text))


def find_chain_folder(repo_root: Path, nnnn: str) -> Path | None:
    """Найти папку цепочки по номеру NNNN."""
    analysis_dir = repo_root / "specs" / "analysis"
    if not analysis_dir.exists():
        return None
    matching = [
        d for d in analysis_dir.iterdir()
        if d.is_dir() and d.name.startswith(f"{nnnn}-")
    ]
    if len(matching) == 1:
        return matching[0]
    return None


# =============================================================================
# Основная логика
# =============================================================================

def check_readiness(chain_dir: Path) -> dict:
    """Проверить готовность цепочки.

    Возвращает dict:
        ready: bool — готова ли цепочка
        chain: str — имя папки цепочки
        docs: list[dict] — статус каждого документа
        total_markers: int — общее количество маркеров
    """
    results = {
        "ready": True,
        "chain": chain_dir.name,
        "docs": [],
        "total_markers": 0,
    }

    for doc_name in CHAIN_DOCS:
        doc_path = chain_dir / doc_name
        doc_info = {
            "name": doc_name,
            "exists": doc_path.exists(),
            "status": None,
            "status_ok": False,
            "markers": 0,
        }

        if not doc_info["exists"]:
            doc_info["status_ok"] = False
            results["ready"] = False
        else:
            fm = parse_frontmatter(doc_path)
            doc_info["status"] = fm.get("status", "")
            doc_info["status_ok"] = doc_info["status"] == "WAITING"
            doc_info["markers"] = count_markers(doc_path)
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
    repo_root = find_repo_root(Path(args.repo))

    # Валидация аргумента
    if not re.match(r'^\d{4}$', args.nnnn):
        print(f"Ошибка: NNNN должен быть 4 цифры, получено: {args.nnnn}",
              file=sys.stderr)
        sys.exit(2)

    # Найти папку цепочки
    chain_dir = find_chain_folder(repo_root, args.nnnn)
    if chain_dir is None:
        print(f"Ошибка: цепочка {args.nnnn} не найдена в specs/analysis/",
              file=sys.stderr)
        sys.exit(2)

    # Проверить готовность
    results = check_readiness(chain_dir)

    # Вывод
    if args.json:
        print(format_json(results))
    else:
        print(format_text(results))

    sys.exit(0 if results["ready"] else 1)


if __name__ == "__main__":
    main()
