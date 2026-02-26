#!/usr/bin/env python3
"""
check-content-drift.py — Проверка контентного покрытия секций стандарта.

Автоматически строит таблицу покрытия «секция стандарта → шаг workflow →
ERROR_CODE скрипта» и выявляет пробелы.  Дополняет check-version-drift.py,
который проверяет только числовые версии.

Использование:
    python check-content-drift.py <стандарт>
    python check-content-drift.py <стандарт> --json
    python check-content-drift.py <стандарт> --check
    python check-content-drift.py <стандарт> --verbose

Примеры:
    python check-content-drift.py .instructions/standard-instruction.md
    python check-content-drift.py specs/.instructions/docs/standard-technology.md --json
    python check-content-drift.py .instructions/standard-instruction.md --check

Возвращает:
    0 — все секции покрыты
    1 — есть непокрытые секции
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

# Фаза 1: парсинг секций стандарта
H2_NUMBERED = re.compile(r"^##\s+(\d+)\.\s+(.+)$")
H2_UNNUMBERED = re.compile(r"^##\s+([^#\d].+)$")
SKIP_SECTIONS = {"Оглавление", "Скрипты", "Скиллы"}

# Фаза 3: SSOT-ссылки в workflows
SSOT_REF = re.compile(
    r"\*\*SSOT:\*\*\s*\[([^\]]*?§\s*(\d+)[^\]]*)\]\(([^)]+)\)"
)

# Фаза 3: шаги workflow
STEP_HEADER = re.compile(
    r"^###\s+Шаг\s+(\d+)[\s:.]\s*(.+)$", re.IGNORECASE | re.MULTILINE
)

# Фаза 4: ERROR_CODES из скриптов
ERROR_CODES_BLOCK = re.compile(r"ERROR_CODES\s*=\s*\{(.*?)\}", re.DOTALL)
ERROR_CODE_ENTRY = re.compile(r'"([A-Z]+-?[A-Z]*\d+)":\s*"([^"]+)"')

# Минимальный порог fuzzy-совпадения (доля общих ключевых слов)
FUZZY_THRESHOLD = 0.3

# Стоп-слова для fuzzy-сравнения (не несут смысловой нагрузки)
STOP_WORDS = {
    "и", "в", "на", "с", "по", "из", "для", "от", "к", "не", "что", "как",
    "а", "о", "при", "все", "до", "или", "без", "это", "так", "он", "она",
    "the", "a", "an", "and", "or", "of", "in", "to", "for", "is", "are",
    "be", "with", "as", "at", "by", "on", "not", "from", "but",
}


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


def read_file(path: Path) -> str:
    """Прочитать файл, вернуть пустую строку если не удалось."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def get_standard_version(content: str) -> str | None:
    """Извлечь 'Версия стандарта: X.Y'."""
    m = re.search(r"^Версия стандарта:\s*(\d+\.\d+)", content, re.MULTILINE)
    return m.group(1) if m else None


def stem(word: str) -> str:
    """Простой стемминг: усечение русских слов до 5 символов."""
    # Латинские слова — без усечения (короткие технические термины)
    if re.match(r"^[a-z]", word):
        return word
    # Русские слова длиннее 5 символов — усечь
    return word[:5] if len(word) > 5 else word


def keywords(text: str) -> set[str]:
    """Извлечь ключевые слова из текста (lower, stem, без стоп-слов)."""
    words = re.findall(r"[а-яёa-z0-9_-]{3,}", text.lower())
    return {stem(w) for w in words if w not in STOP_WORDS}


def fuzzy_match(section_title: str, text: str) -> float:
    """Доля общих ключевых слов между заголовком секции и текстом."""
    kw_section = keywords(section_title)
    kw_text = keywords(text)
    if not kw_section:
        return 0.0
    return len(kw_section & kw_text) / len(kw_section)


# =============================================================================
# Фаза 1: Извлечение секций стандарта
# =============================================================================

def extract_sections(content: str) -> list[dict]:
    """Парсит h2-заголовки из standard-*.md, пропуская code-блоки."""
    sections = []
    in_code_block = False
    auto_num = 0

    for line_no, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()

        # Переключение code-блоков
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Пронумерованные: ## 1. Название
        m = H2_NUMBERED.match(stripped)
        if m:
            title = m.group(2).strip()
            if title in SKIP_SECTIONS:
                continue
            sections.append({
                "number": int(m.group(1)),
                "title": title,
                "line": line_no,
            })
            continue

        # Ненумерованные: ## Название
        m = H2_UNNUMBERED.match(stripped)
        if m:
            title = m.group(1).strip()
            if title in SKIP_SECTIONS:
                continue
            auto_num += 1
            sections.append({
                "number": auto_num,
                "title": title,
                "line": line_no,
            })

    return sections


# =============================================================================
# Фаза 2: Поиск зависимых файлов
# =============================================================================

def find_workflow_files(std_path: Path) -> dict[str, Path]:
    """Найти validation/create/modify workflow рядом со стандартом."""
    std_dir = std_path.parent
    base_name = std_path.name.replace("standard-", "").replace(".md", "")

    result = {}
    for prefix in ("validation", "create", "modify"):
        candidate = std_dir / f"{prefix}-{base_name}.md"
        if candidate.exists():
            result[prefix] = candidate
    return result


def find_script_files(
    std_path: Path, workflows: dict[str, Path], repo_root: Path
) -> list[Path]:
    """Найти связанные validate-*.py скрипты."""
    scripts: set[Path] = set()

    # Из секций «Скрипты» workflow-файлов — ссылки на .py
    py_ref = re.compile(r"\[([^\]]*\.py)\]\(([^)]+\.py)\)")
    for wf_path in workflows.values():
        wf_content = read_file(wf_path)
        for _label, href in py_ref.findall(wf_content):
            # href может быть абсолютным (/) или относительным
            if href.startswith("/"):
                candidate = repo_root / href.lstrip("/")
            else:
                candidate = (wf_path.parent / href).resolve()
            if candidate.exists() and candidate.suffix == ".py":
                scripts.add(candidate)

    # Паттерн validate-*.py в .scripts/ рядом
    scripts_dir = std_path.parent / ".scripts"
    if scripts_dir.is_dir():
        for py_file in scripts_dir.glob("validate-*.py"):
            scripts.add(py_file)

    # Также проверяем ../.scripts/ (часто .instructions/.scripts/)
    scripts_dir_parent = std_path.parent.parent / ".scripts"
    if scripts_dir_parent.is_dir():
        base_name = std_path.name.replace("standard-", "").replace(".md", "")
        for py_file in scripts_dir_parent.glob(f"validate-*{base_name}*.py"):
            scripts.add(py_file)
        # Также точное совпадение validate-{object}.py
        exact = scripts_dir_parent / f"validate-{base_name}.py"
        if exact.exists():
            scripts.add(exact)

    return sorted(scripts)


# =============================================================================
# Фаза 3: Извлечение покрытия из workflows
# =============================================================================

def extract_workflow_coverage(
    wf_path: Path, std_path: Path, sections: list[dict], repo_root: Path
) -> dict[int, list[str]]:
    """Возвращает {section_number: [описания покрытия]}."""
    content = read_file(wf_path)
    if not content:
        return {}

    coverage: dict[int, list[str]] = {}
    std_rel = str(std_path.relative_to(repo_root)).replace("\\", "/")
    std_name = std_path.name

    # Стратегия A: SSOT-ссылки
    for match in SSOT_REF.finditer(content):
        _label = match.group(1)
        section_num = int(match.group(2))
        href = match.group(3)

        # Фильтр: ссылка должна указывать на наш стандарт
        href_clean = href.split("#")[0]
        if href_clean.startswith("/"):
            href_clean = href_clean.lstrip("/")
        href_name = Path(href_clean).name

        if href_name == std_name or href_clean == std_rel:
            # Найти, в каком шаге находится эта ссылка
            step_desc = _find_enclosing_step(content, match.start())
            desc = step_desc if step_desc else "SSOT §"
            coverage.setdefault(section_num, []).append(desc)

    # Стратегия B: эвристика по названиям шагов
    steps = _extract_steps(content)
    for sec in sections:
        if sec["number"] in coverage:
            continue  # уже покрыто через SSOT
        for step_num, step_title in steps:
            score = fuzzy_match(sec["title"], step_title)
            if score >= FUZZY_THRESHOLD:
                coverage.setdefault(sec["number"], []).append(
                    f"Шаг {step_num} (~)"
                )

    # Стратегия B2: поиск «§ N» в теле шагов
    step_bodies = _extract_step_bodies(content)
    section_ref = re.compile(r"§\s*(\d+)")
    for step_num, body in step_bodies:
        for m in section_ref.finditer(body):
            ref_num = int(m.group(1))
            # Проверить что секция с таким номером существует
            if any(s["number"] == ref_num for s in sections):
                if ref_num not in coverage:
                    coverage.setdefault(ref_num, []).append(
                        f"Шаг {step_num} (§)"
                    )

    return coverage


def _find_enclosing_step(content: str, char_pos: int) -> str | None:
    """Найти ### Шаг N: ... в котором находится позиция char_pos."""
    # Ищем последний ### Шаг перед char_pos
    text_before = content[:char_pos]
    matches = list(STEP_HEADER.finditer(text_before))
    if matches:
        last = matches[-1]
        return f"Шаг {last.group(1)}"
    return None


def _extract_steps(content: str) -> list[tuple[str, str]]:
    """Извлечь все шаги (номер, название)."""
    return [
        (m.group(1), m.group(2).strip())
        for m in STEP_HEADER.finditer(content)
    ]


def _extract_step_bodies(content: str) -> list[tuple[str, str]]:
    """Извлечь тела шагов (номер, текст между заголовками)."""
    matches = list(STEP_HEADER.finditer(content))
    result = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end]
        result.append((m.group(1), body))
    return result


# =============================================================================
# Фаза 4: Извлечение покрытия из скриптов
# =============================================================================

def extract_script_coverage(
    script_path: Path, sections: list[dict]
) -> dict[int, list[str]]:
    """Возвращает {section_number: [ERROR_CODE]}."""
    content = read_file(script_path)
    if not content:
        return {}

    # Извлечь ERROR_CODES
    block_match = ERROR_CODES_BLOCK.search(content)
    if not block_match:
        return {}

    error_codes: list[tuple[str, str]] = ERROR_CODE_ENTRY.findall(
        block_match.group(1)
    )
    if not error_codes:
        return {}

    coverage: dict[int, list[str]] = {}

    for code, description in error_codes:
        best_section = None
        best_score = 0.0

        for sec in sections:
            score = fuzzy_match(sec["title"], description)
            if score > best_score:
                best_score = score
                best_section = sec["number"]

        if best_section is not None and best_score >= FUZZY_THRESHOLD:
            coverage.setdefault(best_section, []).append(code)

    return coverage


# =============================================================================
# Фаза 5: Матрица покрытия
# =============================================================================

def build_matrix(
    sections: list[dict],
    wf_coverage: dict[str, dict[int, list[str]]],
    script_coverage: dict[int, list[str]],
    available_workflows: list[str],
) -> list[dict]:
    """Построить матрицу покрытия для каждой секции."""
    matrix = []

    for sec in sections:
        num = sec["number"]
        row = {
            "number": num,
            "title": sec["title"],
            "line": sec["line"],
        }

        # Покрытие по каждому workflow
        for wf_type in ("validation", "create", "modify"):
            if wf_type in wf_coverage:
                hits = wf_coverage[wf_type].get(num, [])
                row[wf_type] = ", ".join(hits) if hits else None
            else:
                row[wf_type] = None  # workflow не существует

        # Покрытие скриптами
        script_hits = script_coverage.get(num, [])
        row["script"] = ", ".join(script_hits) if script_hits else None

        # Статус
        covered_count = 0
        total_checks = 0

        for wf_type in available_workflows:
            total_checks += 1
            if row.get(wf_type):
                covered_count += 1

        if script_coverage:  # есть скрипты
            total_checks += 1
            if row["script"]:
                covered_count += 1

        if total_checks == 0:
            row["status"] = "uncovered"
        elif covered_count == total_checks:
            row["status"] = "covered"
        elif covered_count > 0:
            row["status"] = "partial"
        else:
            row["status"] = "uncovered"

        matrix.append(row)

    return matrix


# =============================================================================
# Фаза 6: Вывод
# =============================================================================

STATUS_ICON = {
    "covered": "✅",
    "partial": "⚠️",
    "uncovered": "❌",
}


def print_table(
    std_rel: str,
    version: str | None,
    matrix: list[dict],
    available_workflows: list[str],
    has_scripts: bool,
    verbose: bool,
) -> None:
    """Табличный вывод матрицы покрытия."""
    ver_str = f" (v{version})" if version else ""
    print(f"=== Контентное покрытие: {std_rel}{ver_str} ===")
    print()

    # Заголовок таблицы
    cols = ["§", "Секция"]
    for wf in available_workflows:
        cols.append(wf)
    if has_scripts:
        cols.append("script")
    cols.append("Статус")

    # Ширины колонок
    widths = [3, 30]
    for _ in available_workflows:
        widths.append(14)
    if has_scripts:
        widths.append(14)
    widths.append(6)

    # Печать заголовка
    header = "| " + " | ".join(
        c.ljust(w) for c, w in zip(cols, widths)
    ) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    print(header)
    print(sep)

    # Печать строк
    for row in matrix:
        cells = [
            str(row["number"]).ljust(3),
            row["title"][:30].ljust(30),
        ]
        for wf in available_workflows:
            val = row.get(wf) or "❌"
            cells.append(val[:14].ljust(14))
        if has_scripts:
            val = row.get("script") or "❌"
            cells.append(val[:14].ljust(14))
        cells.append(STATUS_ICON.get(row["status"], "?").ljust(6))
        print("| " + " | ".join(cells) + " |")

    print()

    # Итого
    total = len(matrix)
    covered = sum(1 for r in matrix if r["status"] == "covered")
    partial = sum(1 for r in matrix if r["status"] == "partial")
    uncovered = sum(1 for r in matrix if r["status"] == "uncovered")

    print(
        f"Итого: {total} секций, {covered} покрыто, "
        f"{partial} частично, {uncovered} не покрыто"
    )
    print()

    # Непокрытые
    gaps = [r for r in matrix if r["status"] in ("uncovered", "partial")]
    if gaps:
        print("❌ Непокрытые/частично покрытые секции:")
        for r in gaps:
            missing = []
            for wf in available_workflows:
                if not r.get(wf):
                    missing.append(f"нет в {wf}")
            if has_scripts and not r.get("script"):
                missing.append("нет в скрипте")
            details = "; ".join(missing) if missing else ""
            print(
                f"  § {r['number']} {r['title']} — {details}"
            )
        print()

        print("Рекомендации:")
        for i, r in enumerate(gaps, 1):
            missing_wf = [
                wf for wf in available_workflows if not r.get(wf)
            ]
            for wf in missing_wf:
                print(
                    f"  {i}. Добавить шаг в {wf} для § {r['number']} "
                    f"({r['title']})"
                )
            if has_scripts and not r.get("script"):
                print(
                    f"  {i}. Добавить ERROR_CODE в скрипт для § {r['number']} "
                    f"({r['title']})"
                )


def output_json(
    std_rel: str,
    version: str | None,
    matrix: list[dict],
    available_workflows: list[str],
    has_scripts: bool,
) -> dict:
    """Структурированный JSON вывод."""
    total = len(matrix)
    covered = sum(1 for r in matrix if r["status"] == "covered")
    partial = sum(1 for r in matrix if r["status"] == "partial")
    uncovered = sum(1 for r in matrix if r["status"] == "uncovered")

    gaps = []
    for r in matrix:
        if r["status"] in ("uncovered", "partial"):
            missing = []
            for wf in available_workflows:
                if not r.get(wf):
                    missing.append(wf)
            if has_scripts and not r.get("script"):
                missing.append("script")
            gaps.append({
                "section": r["number"],
                "title": r["title"],
                "status": r["status"],
                "missing_in": missing,
            })

    return {
        "standard": std_rel,
        "standard_version": version,
        "sections": matrix,
        "summary": {
            "total": total,
            "covered": covered,
            "partial": partial,
            "uncovered": uncovered,
        },
        "gaps": gaps,
    }


# =============================================================================
# Main
# =============================================================================

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Проверка контентного покрытия секций стандарта"
    )
    parser.add_argument(
        "standard",
        help="Путь к standard-*.md"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Детали маппинга"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Только exit code (0 = покрыто, 1 = пробелы)"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию .)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Нормализовать путь к стандарту
    std_input = args.standard.replace("\\", "/")
    if std_input.startswith("./"):
        std_input = std_input[2:]
    std_path = repo_root / std_input

    if not std_path.exists():
        if not args.check and not args.json:
            print(f"❌ Стандарт не найден: {args.standard}")
        sys.exit(1)

    std_content = read_file(std_path)
    std_rel = str(std_path.relative_to(repo_root)).replace("\\", "/")
    version = get_standard_version(std_content)

    # --- Фаза 1 ---
    sections = extract_sections(std_content)
    if not sections:
        if not args.check and not args.json:
            print(f"⚠️ Не найдено h2-секций в {std_rel}")
        sys.exit(0)

    if args.verbose and not args.json:
        print(f"[Фаза 1] Секции стандарта ({len(sections)}):")
        for s in sections:
            print(f"  § {s['number']} {s['title']} (строка {s['line']})")
        print()

    # --- Фаза 2 ---
    workflows = find_workflow_files(std_path)
    scripts = find_script_files(std_path, workflows, repo_root)

    if args.verbose and not args.json:
        print(f"[Фаза 2] Workflows: {list(workflows.keys())}")
        print(
            f"[Фаза 2] Скрипты: "
            f"{[str(s.relative_to(repo_root)) for s in scripts]}"
        )
        print()

    # --- Фаза 3 ---
    wf_coverage: dict[str, dict[int, list[str]]] = {}
    for wf_type, wf_path in workflows.items():
        cov = extract_workflow_coverage(wf_path, std_path, sections, repo_root)
        wf_coverage[wf_type] = cov

        if args.verbose and not args.json:
            print(f"[Фаза 3] {wf_type}: {cov}")

    if args.verbose and not args.json:
        print()

    # --- Фаза 4 ---
    all_script_coverage: dict[int, list[str]] = {}
    for script_path in scripts:
        cov = extract_script_coverage(script_path, sections)
        for num, codes in cov.items():
            all_script_coverage.setdefault(num, []).extend(codes)

        if args.verbose and not args.json:
            script_rel = str(script_path.relative_to(repo_root))
            print(f"[Фаза 4] {script_rel}: {cov}")

    if args.verbose and not args.json:
        print()

    # --- Фаза 5 ---
    available_workflows = [
        wf for wf in ("validation", "create", "modify") if wf in workflows
    ]
    has_scripts = bool(scripts)

    matrix = build_matrix(
        sections, wf_coverage, all_script_coverage, available_workflows
    )

    # --- Фаза 6 ---
    has_gaps = any(r["status"] != "covered" for r in matrix)

    if args.json:
        result = output_json(
            std_rel, version, matrix, available_workflows, has_scripts
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1 if has_gaps else 0)

    if args.check:
        sys.exit(1 if has_gaps else 0)

    print_table(
        std_rel, version, matrix, available_workflows, has_scripts,
        args.verbose,
    )

    sys.exit(1 if has_gaps else 0)


if __name__ == "__main__":
    main()
