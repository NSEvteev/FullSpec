#!/usr/bin/env python3
"""
create-analysis-plan-dev-file.py — Создание файла plan-dev.md по шаблону.

Создаёт пустой plan-dev.md в папке specs/analysis/{branch}/ с заполненным frontmatter
и пустыми per-service секциями (из SVC-N в design.md).

Использование:
    python create-analysis-plan-dev-file.py <branch> [--description <desc>] [--repo <dir>]

Аргументы:
    branch      Имя папки analysis chain (формат NNNN-{topic})

Примеры:
    python create-analysis-plan-dev-file.py 0001-task-dashboard
    python create-analysis-plan-dev-file.py 0001-oauth2-authorization --description "Plan Dev OAuth2"

Возвращает:
    0 — файл создан
    1 — ошибка (файл существует, папка не найдена, нет plan-test.md, parent не WAITING)

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
standard: specs/.instructions/analysis/plan-dev/standard-plan-dev.md
standard-version: v1.3
index: specs/analysis/README.md
parent: plan-test.md
status: DRAFT
milestone: {milestone}
---

# {nnnn}: {topic_title} — Plan Dev

## Резюме

{{Scope, кол-во сервисов, кол-во TASK-N, средняя сложность}}

"""

PER_SERVICE_TEMPLATE = """\
## {svc_heading}

### Задачи

"""

SYSTEM_SECTIONS_TEMPLATE = """\
## Кросс-сервисные зависимости

*Кросс-сервисных зависимостей нет.*

## Маппинг GitHub Issues

| Элемент | Маппинг |
|---------|---------|
| TASK-N | → Issue title |
| Подзадачи | → Чек-лист в Issue body |
| Приоритет | → Label `priority/{value}` |
| Зависимости | → "Blocked by #N" в Issue body |
| TC | → Ссылка на TC-N в Issue body |
| Milestone | → Milestone из frontmatter Discussion |

## Блоки выполнения

| BLOCK | Задачи | Сервисы | Зависимости | Wave |
|-------|--------|---------|-------------|------|

## Предложения

_Предложений нет._

## Отвергнутые предложения

_Отвергнутых предложений нет._
"""


# =============================================================================
# Функции
# =============================================================================

def get_design_svc_headings(analysis_dir: Path) -> list:
    """Извлечь SVC-N заголовки из design.md."""
    design_path = analysis_dir / "design.md"
    if not design_path.exists():
        return []
    content = design_path.read_text(encoding='utf-8')
    return SVC_HEADING_REGEX.findall(content)


def get_plan_test_info(analysis_dir: Path) -> dict:
    """Извлечь status из plan-test.md."""
    plan_test_path = analysis_dir / "plan-test.md"
    fm = ChainManager.parse_frontmatter_file(plan_test_path)
    return {
        "status": fm.get("status", ""),
        "description": fm.get("description", ""),
    }


def get_discussion_milestone(analysis_dir: Path) -> str:
    """Извлечь milestone из discussion.md (SSOT для milestone)."""
    discussion_path = analysis_dir / "discussion.md"
    if not discussion_path.exists():
        return ""
    fm = ChainManager.parse_frontmatter_file(discussion_path)
    return fm.get("milestone", "")


def create_plan_dev_file(
    branch: str,
    description: str,
    repo_root: Path,
) -> Path:
    """Создать plan-dev.md по шаблону."""
    folder_match = FOLDER_REGEX.match(branch)
    if not folder_match:
        raise ValueError(f"Папка '{branch}' не соответствует формату NNNN-{{topic}}")

    nnnn = folder_match.group(1)
    topic_slug = folder_match.group(2)
    topic_title = topic_slug.replace("-", " ").capitalize()

    analysis_dir = repo_root / "specs" / "analysis" / branch

    if not analysis_dir.exists():
        raise FileNotFoundError(f"Папка analysis chain не найдена: {analysis_dir}")

    # Проверить наличие plan-test.md
    plan_test_path = analysis_dir / "plan-test.md"
    if not plan_test_path.exists():
        raise FileNotFoundError(f"plan-test.md не найден: {plan_test_path}")

    # Проверить статус plan-test.md
    plan_test_info = get_plan_test_info(analysis_dir)
    if plan_test_info["status"] != "WAITING":
        raise ValueError(
            f"Plan Tests не в статусе WAITING (текущий: {plan_test_info['status']}). "
            f"Plan Dev может быть создан только после одобрения Plan Tests."
        )

    # Определить milestone (из Discussion — SSOT)
    milestone = get_discussion_milestone(analysis_dir)
    if not milestone:
        milestone = "v0.1.0"

    # Определить description
    if not description:
        pt_desc = plan_test_info["description"]
        description = f"{pt_desc} — план разработки."

    # Проверить существование plan-dev.md
    plan_dev_path = analysis_dir / "plan-dev.md"
    if plan_dev_path.exists():
        raise FileExistsError(f"plan-dev.md уже существует: {plan_dev_path}")

    # Собрать содержимое
    content = FRONTMATTER_TEMPLATE.format(
        description=description,
        milestone=milestone,
        nnnn=nnnn,
        topic_title=topic_title,
    )

    # Per-service секции из SVC-N в Design
    svc_headings = get_design_svc_headings(analysis_dir)
    if not svc_headings:
        content += PER_SERVICE_TEMPLATE.format(svc_heading="SVC-1: {сервис}")
    else:
        for heading in svc_headings:
            content += PER_SERVICE_TEMPLATE.format(svc_heading=heading)

    # Системные секции
    content += SYSTEM_SECTIONS_TEMPLATE

    plan_dev_path.write_text(content, encoding='utf-8')
    return plan_dev_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание файла plan-dev.md по шаблону"
    )
    parser.add_argument("branch", help="Имя папки analysis chain (формат NNNN-{topic})")
    parser.add_argument(
        "--description", default="",
        help="Описание плана разработки (до 1024 символов). По умолчанию — из plan-test.md"
    )
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = ChainManager.find_repo_root(Path(args.repo))

    try:
        plan_dev_path = create_plan_dev_file(
            branch=args.branch,
            description=args.description,
            repo_root=repo_root,
        )
        rel_path = plan_dev_path.relative_to(repo_root)
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
