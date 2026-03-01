#!/usr/bin/env python3
"""
validate-analysis-review.py — Валидация документов ревью кода SDD.

Проверяет соответствие документа review.md стандарту standard-review.md.

Использование:
    python validate-analysis-review.py <path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-analysis-review.py specs/analysis/0001-oauth2-authorization/review.md
    python validate-analysis-review.py --all
    python validate-analysis-review.py --json specs/analysis/0001-oauth2-authorization/review.md

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

FOLDER_REGEX = re.compile(r'^(\d{4})-.+$')
HEADING_REGEX = re.compile(r'^# review:\s+(\d{4})\s+(.+)$', re.MULTILINE)

VALID_STATUSES = {"OPEN", "RESOLVED"}

REQUIRED_STANDARD = "specs/.instructions/analysis/review/standard-review.md"
REQUIRED_INDEX = "specs/analysis/README.md"
STANDARD_VERSION_REGEX = re.compile(r'^v\d+\.\d+$')
MILESTONE_REGEX = re.compile(r'^v\d+\.\d+(\.\d+)?$')

ITERATION_HEADING_REGEX = re.compile(r'^## Итерация (\d+)', re.MULTILINE)
VERDICT_REGEX = re.compile(r'^\*\*Вердикт:\*\*\s*(READY|NOT READY|CONFLICT)', re.MULTILINE)
SVC_BLOCK_REGEX = re.compile(r'^### .+ \(critical-(?:high|medium|low)\)', re.MULTILINE)

ERROR_CODES = {
    "RV001": "Неверное расположение файла",
    "RV002": "Отсутствует description",
    "RV003": "Неверный standard",
    "RV004": "Невалидный status",
    "RV005": "Отсутствует parent",
    "RV006": "Присутствует запрещённое поле children",
    "RV007": "Отсутствует раздел ## Контекст ревью",
    "RV008": "Отсутствует подраздел ### Постановка",
    "RV009": "Нет ни одного сервисного блока ### {svc} (critical-{level})",
    "RV010": "Нет ## Итерация N при status RESOLVED",
    "RV011": "Дублирующийся номер итерации",
    "RV012": "Нет **Вердикт:** в итерации",
    "RV013": "Рассинхрон статуса и вердикта",
    "RV014": "Отсутствует milestone",
    "RV015": "Description слишком длинное (> 1024 символов)",
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


def parse_frontmatter(content: str) -> dict:
    """Извлечь frontmatter из markdown."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    result = {}
    current_key = None
    list_values = []

    for line in match.group(1).split('\n'):
        if line.strip().startswith('- ') and current_key:
            list_values.append(line.strip()[2:])
            result[current_key] = list_values
            continue

        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if value == '[]':
                result[key] = []
                current_key = key
                list_values = []
            elif value == '' or value is None:
                current_key = key
                list_values = []
                result[key] = value
            else:
                result[key] = value
                current_key = key
                list_values = []

    return result


def get_body(content: str) -> str:
    """Получить тело документа без frontmatter."""
    return re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)


# =============================================================================
# Проверки
# =============================================================================

def check_location(path: Path) -> list[tuple[str, str]]:
    """RV001: Проверить расположение файла."""
    errors = []

    if path.name != "review.md":
        errors.append(("RV001", f"Имя файла '{path.name}', ожидается 'review.md'"))
        return errors

    parent_name = path.parent.name
    if not FOLDER_REGEX.match(parent_name):
        errors.append(("RV001", f"Папка '{parent_name}' не соответствует формату NNNN-{{topic}}"))

    return errors


def check_frontmatter(content: str) -> list[tuple[str, str]]:
    """RV002-RV006, RV014-RV015: Проверить frontmatter."""
    errors = []

    if not content.startswith("---\n"):
        errors.append(("RV002", "Отсутствует frontmatter"))
        return errors

    fm = parse_frontmatter(content)

    # RV002, RV015: description
    desc = fm.get("description", "")
    if not desc:
        errors.append(("RV002", "Отсутствует поле description"))
    elif len(desc) > 1024:
        errors.append(("RV015", f"Description {len(desc)} символов (макс. 1024)"))

    # RV003: standard
    standard = fm.get("standard", "")
    if standard != REQUIRED_STANDARD:
        errors.append(("RV003", f"standard = '{standard}', ожидается '{REQUIRED_STANDARD}'"))

    # Проверить standard-version
    sv = fm.get("standard-version", "")
    if not sv or not STANDARD_VERSION_REGEX.match(sv):
        errors.append(("RV003", f"standard-version = '{sv}', ожидается формат vX.Y"))

    # RV004: status
    status = fm.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(("RV004", f"status = '{status}', допустимые: OPEN, RESOLVED"))

    # RV005: parent обязателен
    if not fm.get("parent"):
        errors.append(("RV005", "Отсутствует поле parent (путь к plan-dev.md)"))

    # RV006: children запрещён
    if "children" in fm:
        errors.append(("RV006", "Поле children присутствует (review.md не имеет дочерних документов)"))

    # RV014: milestone
    milestone = fm.get("milestone", "")
    if not milestone:
        errors.append(("RV014", "Отсутствует поле milestone"))
    elif not MILESTONE_REGEX.match(milestone):
        errors.append(("RV014", f"milestone = '{milestone}', ожидается формат vX.Y"))

    # index
    index = fm.get("index", "")
    if index != REQUIRED_INDEX:
        errors.append(("RV003", f"index = '{index}', ожидается '{REQUIRED_INDEX}'"))

    return errors


def check_heading(content: str, path: Path) -> list[tuple[str, str]]:
    """Проверить совпадение NNNN в папке и заголовке."""
    errors = []

    folder_match = FOLDER_REGEX.match(path.parent.name)
    if not folder_match:
        return errors  # RV001 уже покрыто

    folder_nnnn = folder_match.group(1)

    body = get_body(content)
    heading_match = HEADING_REGEX.search(body)

    if not heading_match:
        errors.append(("RV001", "Заголовок '# review: NNNN Тема' не найден"))
        return errors

    heading_nnnn = heading_match.group(1)
    if folder_nnnn != heading_nnnn:
        errors.append(("RV001", f"NNNN в папке ({folder_nnnn}) ≠ NNNN в заголовке ({heading_nnnn})"))

    # Проверить наличие строк Ветка и Base
    if not re.search(r'^\*\*Ветка:\*\*', body, re.MULTILINE):
        errors.append(("RV001", "Отсутствует строка **Ветка:**"))
    if not re.search(r'^\*\*Base:\*\*', body, re.MULTILINE):
        errors.append(("RV001", "Отсутствует строка **Base:**"))

    return errors


def check_context_section(content: str) -> list[tuple[str, str]]:
    """RV007-RV009: Проверить секцию Контекст ревью."""
    errors = []

    body = get_body(content)

    # RV007: ## Контекст ревью
    if not re.search(r'^## Контекст ревью', body, re.MULTILINE):
        errors.append(("RV007", "Отсутствует раздел '## Контекст ревью'"))
        return errors

    # Извлечь содержимое секции Контекст ревью
    context_match = re.search(
        r'^## Контекст ревью\s*\n(.*?)(?=^## |\Z)',
        body, re.MULTILINE | re.DOTALL
    )
    if not context_match:
        errors.append(("RV007", "Раздел '## Контекст ревью' пустой"))
        return errors

    context_text = context_match.group(1)

    # RV008: ### Постановка
    if not re.search(r'^### Постановка', context_text, re.MULTILINE):
        errors.append(("RV008", "Отсутствует подраздел '### Постановка' в Контексте ревью"))

    # RV009: хотя бы один сервисный блок
    if not SVC_BLOCK_REGEX.search(context_text):
        errors.append(("RV009", "Нет ни одного сервисного блока '### {svc} (critical-{level})'"))

    # Проверить ### Системная документация
    if not re.search(r'^### Системная документация', context_text, re.MULTILINE):
        errors.append(("RV007", "Отсутствует подраздел '### Системная документация'"))

    # Проверить ### Tech-стандарты
    if not re.search(r'^### Tech-стандарты', context_text, re.MULTILINE):
        errors.append(("RV007", "Отсутствует подраздел '### Tech-стандарты'"))

    return errors


def check_iterations(content: str) -> list[tuple[str, str]]:
    """RV010-RV013: Проверить итерации."""
    errors = []

    fm = parse_frontmatter(content)
    status = fm.get("status", "")
    body = get_body(content)

    iterations = ITERATION_HEADING_REGEX.findall(body)

    # RV010: при RESOLVED должна быть хотя бы одна итерация
    if status == "RESOLVED" and not iterations:
        errors.append(("RV010", "status=RESOLVED, но нет ни одной секции '## Итерация N'"))

    if not iterations:
        return errors

    # RV011: нумерация без дублей
    seen = set()
    for num in iterations:
        if num in seen:
            errors.append(("RV011", f"Дублирующийся номер итерации: ## Итерация {num}"))
        seen.add(num)

    # Проверить каждую итерацию на вердикт (RV012)
    iteration_blocks = re.split(r'^## Итерация \d+', body, flags=re.MULTILINE)
    # Первый элемент — до первой итерации
    iteration_blocks = iteration_blocks[1:]

    for i, block in enumerate(iteration_blocks, start=1):
        # Граница блока — следующая ## Итерация N (уже разделено) или конец
        verdict_match = VERDICT_REGEX.search(block)
        if not verdict_match:
            errors.append(("RV012", f"Нет строки '**Вердикт:**' в ## Итерация {iterations[i-1]}"))

    # RV013: синхронизация status и вердикта последней итерации
    if iterations:
        last_block = iteration_blocks[-1]
        verdict_match = VERDICT_REGEX.search(last_block)
        if verdict_match:
            last_verdict = verdict_match.group(1)
            if status == "RESOLVED" and last_verdict != "READY":
                errors.append(("RV013", f"status=RESOLVED, но вердикт последней итерации = '{last_verdict}' (ожидается READY)"))
            elif status == "OPEN" and last_verdict == "READY":
                errors.append(("RV013", f"status=OPEN, но вердикт последней итерации = 'READY' (ожидается RESOLVED)"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_review(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать один документ ревью."""
    errors = []

    if not path.exists():
        return [("RV001", f"Файл не найден: {path}")]

    errors.extend(check_location(path))

    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [("RV001", f"Ошибка чтения файла: {e}")]

    errors.extend(check_frontmatter(content))
    errors.extend(check_heading(content, path))
    errors.extend(check_context_section(content))
    errors.extend(check_iterations(content))

    return errors


def find_all_reviews(repo_root: Path) -> list[Path]:
    """Найти все документы ревью."""
    analysis_dir = repo_root / "specs" / "analysis"
    if not analysis_dir.exists():
        return []

    results = []
    for folder in sorted(analysis_dir.iterdir()):
        if folder.is_dir() and FOLDER_REGEX.match(folder.name):
            review_file = folder / "review.md"
            if review_file.exists():
                results.append(review_file)
    return results


def format_output(path: Path, errors: list[tuple[str, str]], as_json: bool) -> str:
    """Форматировать вывод."""
    if as_json:
        return json.dumps({
            "file": str(path),
            "valid": len(errors) == 0,
            "errors": [{"code": code, "message": msg} for code, msg in errors]
        }, ensure_ascii=False, indent=2)

    display_name = f"{path.parent.name}/{path.name}"
    if not errors:
        return f"✅ {display_name} — валидация пройдена"

    lines = [f"❌ {display_name} — {len(errors)} ошибок:"]
    for code, msg in errors:
        lines.append(f"   {code}: {msg}")
    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация документов ревью кода SDD"
    )
    parser.add_argument("path", nargs="?", help="Путь к документу ревью")
    parser.add_argument("--all", action="store_true", help="Проверить все документы ревью")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if args.all:
        reviews = find_all_reviews(repo_root)
        if not reviews:
            print("Документы ревью не найдены")
            sys.exit(0)
    elif args.path:
        reviews = [Path(args.path)]
    else:
        parser.print_help()
        sys.exit(2)

    all_valid = True
    results = []

    for path in reviews:
        errors = validate_review(path, repo_root)
        if errors:
            all_valid = False

        output = format_output(path, errors, args.json)
        results.append(output)

    if args.json:
        print("[" + ",\n".join(results) + "]")
    else:
        print("\n".join(results))

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
