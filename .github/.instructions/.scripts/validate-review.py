#!/usr/bin/env python3
"""
validate-review.py — Pre-commit хук: проверка завершённости ревью кода.

Проверяет наличие review.md для текущей ветки, статус RESOLVED и вердикт READY
в последней итерации. Блокирует коммит если ревью не завершено.

Использование:
    python validate-review.py [--branch <name>] [--review-path <path>]

Примеры:
    python validate-review.py
    python validate-review.py --branch 0001-oauth2-authorization
    python validate-review.py --review-path specs/analysis/0001-oauth2/review.md

Возвращает:
    0 — ревью завершено (или analysis chain не найдена для ветки)
    1 — ревью не завершено или не найдено
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

FOLDER_REGEX = re.compile(r'^\d{4}-.+$')
ITERATION_HEADING_REGEX = re.compile(r'^## Итерация (\d+)', re.MULTILINE)
VERDICT_REGEX = re.compile(r'^\*\*Вердикт:\*\*\s*(READY|NOT READY|CONFLICT)', re.MULTILINE)
FRONTMATTER_STATUS_REGEX = re.compile(r'^status:\s*(.+)$', re.MULTILINE)

ERROR_CODES = {
    "RHK001": "review.md не найден при наличии analysis chain",
    "RHK002": "status не RESOLVED",
    "RHK003": "Нет ни одной секции ## Итерация N",
    "RHK004": "Вердикт последней итерации не READY",
}


# =============================================================================
# Функции
# =============================================================================

def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def get_current_branch() -> str:
    """Получить имя текущей ветки."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def get_review_status(content: str) -> str:
    """Извлечь status из frontmatter."""
    match = FRONTMATTER_STATUS_REGEX.search(content)
    if not match:
        return ""
    return match.group(1).strip()


def get_last_verdict(content: str) -> str:
    """Найти вердикт последней итерации."""
    iterations = ITERATION_HEADING_REGEX.findall(content)
    if not iterations:
        return ""

    # Разделить по заголовкам итераций
    blocks = re.split(r'^## Итерация \d+', content, flags=re.MULTILINE)
    blocks = blocks[1:]  # Пропустить содержимое до первой итерации

    if not blocks:
        return ""

    last_block = blocks[-1]
    verdict_match = VERDICT_REGEX.search(last_block)
    if not verdict_match:
        return ""
    return verdict_match.group(1)


def validate_review(review_path: Path) -> list[tuple[str, str]]:
    """Проверить review.md на завершённость ревью."""
    errors = []

    try:
        content = review_path.read_text(encoding='utf-8')
    except Exception as e:
        return [("RHK001", f"Ошибка чтения {review_path}: {e}")]

    # RHK002: status = RESOLVED
    status = get_review_status(content)
    if status != "RESOLVED":
        errors.append(("RHK002", f"status = '{status}', требуется RESOLVED"))

    # RHK003: хотя бы одна секция ## Итерация N
    iterations = ITERATION_HEADING_REGEX.findall(content)
    if not iterations:
        errors.append(("RHK003", "Нет ни одной секции '## Итерация N' — /review не запускался"))

    # RHK004: вердикт последней итерации = READY
    if iterations:
        last_verdict = get_last_verdict(content)
        if last_verdict != "READY":
            verdict_info = f"'{last_verdict}'" if last_verdict else "(не найден)"
            errors.append(("RHK004", f"Вердикт последней итерации = {verdict_info}, требуется READY"))

    return errors


def run(branch: str, review_path_override: str | None, repo_root: Path) -> bool:
    """Основная логика хука. Возвращает True если всё в порядке."""
    if review_path_override:
        review_path = Path(review_path_override)
        if not review_path.is_absolute():
            review_path = repo_root / review_path

        if not review_path.exists():
            print(f"❌ RHK001: review.md не найден: {review_path}", file=sys.stderr)
            return False

        errors = validate_review(review_path)
        if errors:
            print(f"❌ Ревью не завершено ({review_path}):", file=sys.stderr)
            for code, msg in errors:
                print(f"   {code}: {msg}", file=sys.stderr)
            return False

        print(f"✅ Ревью завершено: {review_path}")
        return True

    # Определить путь по имени ветки
    if not branch:
        branch = get_current_branch()

    if not branch or branch in ("HEAD", "main", "master", "develop"):
        return True  # Служебные ветки — пропустить

    # Проверить наличие analysis chain
    analysis_dir = repo_root / "specs" / "analysis" / branch
    if not analysis_dir.exists() or not FOLDER_REGEX.match(branch):
        return True  # Нет analysis chain — пропустить

    # Ищем review.md
    review_path = analysis_dir / "review.md"
    if not review_path.exists():
        print(
            f"❌ RHK001: review.md не найден для ветки '{branch}'\n"
            f"   Ожидается: {review_path}\n"
            f"   Запустите /review-create для создания документа ревью",
            file=sys.stderr
        )
        return False

    errors = validate_review(review_path)
    if errors:
        print(f"❌ Ревью не завершено для ветки '{branch}':", file=sys.stderr)
        for code, msg in errors:
            print(f"   {code}: {msg}", file=sys.stderr)
        print(f"   Запустите /review для проведения ревью", file=sys.stderr)
        return False

    print(f"✅ Ревью завершено: {review_path}")
    return True


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Pre-commit хук: проверка завершённости ревью кода"
    )
    parser.add_argument("--branch", default="", help="Имя ветки (по умолчанию: текущая)")
    parser.add_argument("--review-path", help="Прямой путь к review.md (для тестов)")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    success = run(args.branch, args.review_path, repo_root)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
