#!/usr/bin/env python3
"""
create-analysis-plan-test-file.py — Создание файла plan-test.md по шаблону.

Создаёт пустой plan-test.md в папке specs/analysis/{branch}/ с заполненным frontmatter
и пустыми per-service секциями (из SVC-N в design.md).

Использование:
    python create-analysis-plan-test-file.py <branch> [--description <desc>] [--repo <dir>]

Аргументы:
    branch      Имя папки analysis chain (формат NNNN-{topic})

Примеры:
    python create-analysis-plan-test-file.py 0001-task-dashboard
    python create-analysis-plan-test-file.py 0001-oauth2-authorization --description "Plan Tests OAuth2"

Возвращает:
    0 — файл создан
    1 — ошибка (файл существует, папка не найдена, нет design.md)

Рефакторинг: утилиты (parse_frontmatter, find_repo_root) делегированы
chain_status.ChainManager (SSOT).
"""

import argparse
import re
import sys
from pathlib import Path

# --- sys.path для импорта chain_status ---
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from chain_status import ChainManager  # noqa: E402


# =============================================================================
# Константы
# =============================================================================

FOLDER_REGEX = re.compile(r'^(\d{4})-(.+)$')
SVC_HEADING_REGEX = re.compile(r'^## (SVC-\d+:\s*.+)$', re.MULTILINE)

FRONTMATTER_TEMPLATE = """\
---
description: {description}
standard: specs/.instructions/analysis/plan-test/standard-plan-test.md
standard-version: v1.3
index: specs/analysis/README.md
parent: design.md
children: []
status: DRAFT
milestone: {milestone}
---

# {nnnn}: {topic_title} — Plan Tests

## Резюме

{{Scope, кол-во сервисов, кол-во TC-N, покрытие STS-N и REQ-N}}

"""

PER_SERVICE_TEMPLATE = """\
## {svc_heading}

### Acceptance-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|

"""

SYSTEM_AND_MATRIX_TEMPLATE = """\
## Системные тест-сценарии

| ID | Описание | Тип | Источник | Данные |
|----|----------|-----|----------|--------|

### Тестовые данные

| Fixture | Описание | Поля |
|---------|----------|------|

## Матрица покрытия

| Источник | TC |
|----------|----|

## Блоки тестирования

| BLOCK | TC | Сервисы | Dev BLOCK |
|-------|----|---------|-----------|
"""


# =============================================================================
# Функции
# =============================================================================

def get_design_info(analysis_dir: Path) -> dict:
    """Извлечь milestone, status и SVC-N из design.md."""
    design_path = analysis_dir / "design.md"
    fm = ChainManager.parse_frontmatter_file(design_path)

    # Извлечь SVC-N заголовки из тела документа
    content = design_path.read_text(encoding='utf-8')
    svc_headings = SVC_HEADING_REGEX.findall(content)

    return {
        "milestone": fm.get("milestone", ""),
        "status": fm.get("status", ""),
        "description": fm.get("description", ""),
        "svc_headings": svc_headings,
    }


def get_discussion_milestone(analysis_dir: Path) -> str:
    """Извлечь milestone из discussion.md (SSOT для milestone)."""
    discussion_path = analysis_dir / "discussion.md"
    if not discussion_path.exists():
        return ""
    fm = ChainManager.parse_frontmatter_file(discussion_path)
    return fm.get("milestone", "")


def create_plan_test_file(
    branch: str,
    description: str,
    repo_root: Path,
) -> Path:
    """Создать plan-test.md по шаблону."""
    folder_match = FOLDER_REGEX.match(branch)
    if not folder_match:
        raise ValueError(f"Папка '{branch}' не соответствует формату NNNN-{{topic}}")

    nnnn = folder_match.group(1)
    topic_slug = folder_match.group(2)
    topic_title = topic_slug.replace("-", " ").capitalize()

    analysis_dir = repo_root / "specs" / "analysis" / branch

    if not analysis_dir.exists():
        raise FileNotFoundError(f"Папка analysis chain не найдена: {analysis_dir}")

    # Проверить наличие design.md
    design_path = analysis_dir / "design.md"
    if not design_path.exists():
        raise FileNotFoundError(f"design.md не найден: {design_path}")

    # Проверить статус design.md
    design_info = get_design_info(analysis_dir)
    if design_info["status"] != "WAITING":
        raise ValueError(
            f"Design не в статусе WAITING (текущий: {design_info['status']}). "
            f"Plan Tests может быть создан только после одобрения Design."
        )

    # Определить milestone (из Discussion — SSOT)
    milestone = get_discussion_milestone(analysis_dir)
    if not milestone:
        milestone = design_info["milestone"]
    if not milestone:
        milestone = "v0.1.0"

    # Определить description
    if not description:
        design_desc = design_info["description"]
        description = f"{design_desc} — план тестов."

    # Проверить существование plan-test.md
    plan_test_path = analysis_dir / "plan-test.md"
    if plan_test_path.exists():
        raise FileExistsError(f"plan-test.md уже существует: {plan_test_path}")

    # Собрать содержимое
    content = FRONTMATTER_TEMPLATE.format(
        description=description,
        milestone=milestone,
        nnnn=nnnn,
        topic_title=topic_title,
    )

    # Per-service секции из SVC-N в Design
    svc_headings = design_info["svc_headings"]
    if not svc_headings:
        content += PER_SERVICE_TEMPLATE.format(svc_heading="SVC-1: {сервис}")
    else:
        for heading in svc_headings:
            content += PER_SERVICE_TEMPLATE.format(svc_heading=heading)

    # Системные тест-сценарии + Матрица покрытия + Блоки тестирования
    content += SYSTEM_AND_MATRIX_TEMPLATE

    plan_test_path.write_text(content, encoding='utf-8')
    return plan_test_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание файла plan-test.md по шаблону"
    )
    parser.add_argument("branch", help="Имя папки analysis chain (формат NNNN-{topic})")
    parser.add_argument(
        "--description", default="",
        help="Описание плана тестов (до 1024 символов). По умолчанию — из design.md"
    )
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = ChainManager.find_repo_root(Path(args.repo))

    try:
        plan_test_path = create_plan_test_file(
            branch=args.branch,
            description=args.description,
            repo_root=repo_root,
        )
        rel_path = plan_test_path.relative_to(repo_root)
        print(f"✅ Создан: {rel_path}")
        sys.exit(0)

    except FileExistsError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    except (FileNotFoundError, ValueError) as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
