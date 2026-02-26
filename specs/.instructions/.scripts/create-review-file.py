#!/usr/bin/env python3
"""
create-review-file.py — Создание файла review.md по шаблону.

Создаёт пустой review.md в папке specs/analysis/{branch}/ с заполненным frontmatter
и базовой структурой секций (Контекст ревью, шаблонные подразделы).

Использование:
    python create-review-file.py <branch> [--milestone <v1.0>] [--base <main>] [--repo <dir>]

Аргументы:
    branch      Имя ветки (= имя папки analysis chain), формат NNNN-{topic}

Примеры:
    python create-review-file.py 0001-oauth2-authorization
    python create-review-file.py 0001-oauth2-authorization --milestone v1.2 --base main

Возвращает:
    0 — файл создан
    1 — ошибка (файл существует, папка не найдена, нет plan-dev.md)

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
MILESTONE_REGEX = re.compile(r'^v\d+\.\d+')

REQUIRED_STANDARD = "specs/.instructions/analysis/review/standard-review.md"
REQUIRED_INDEX = "specs/analysis/README.md"

TEMPLATE = """\
---
description: Ревью кода для {branch}.
standard: specs/.instructions/analysis/review/standard-review.md
standard-version: v1.2
parent: specs/analysis/{branch}/plan-dev.md
index: specs/analysis/README.md
milestone: {milestone}
status: OPEN
---

# review: {nnnn} {topic_title}

**Ветка:** {branch}
**Base:** {base}

## Контекст ревью

> Секция заполняется при /review-create (до начала разработки).
> Содержит все ссылки, необходимые code-reviewer при запуске /review.

### Постановка

| Документ | Путь |
|----------|------|
| Discussion | `specs/analysis/{branch}/discussion.md` |
| Design | `specs/analysis/{branch}/design.md` |
| Plan Tests | `specs/analysis/{branch}/plan-test.md` |
| Plan Dev | `specs/analysis/{branch}/plan-dev.md` |

### {svc_placeholder} (critical-{level_placeholder})

> Блок добавляется на каждый затронутый сервис при /review-create.
> Секции — только те, которые реально меняются (есть в SVC-N design.md).

| Секция | Путь | Что проверяем |
|--------|------|----------------|
| § 8 Автономия | `specs/docs/{svc_placeholder}.md#границы-автономии-llm` | Что можно без флага, что требует CONFLICT |
| § 9 Planned Changes | `specs/docs/{svc_placeholder}.md#planned-changes` | **Эталон для P1-сверки** |

*Незатронутые секции не включаются.*

### Системная документация

- `specs/docs/.system/overview.md`
- `specs/docs/.system/conventions.md`
- `specs/docs/.system/testing.md`
- `specs/docs/.system/infrastructure.md` *(при изменениях в platform/)*

### Tech-стандарты

| Технология | Стандарт |
|------------|----------|
| {tech_placeholder} | `specs/docs/.technologies/standard-{tech_placeholder}.md` |
"""


# =============================================================================
# Функции
# =============================================================================

def get_milestone_from_discussion(analysis_dir: Path) -> str:
    """Извлечь milestone из discussion.md через ChainManager (SSOT)."""
    discussion_path = analysis_dir / "discussion.md"
    fm = ChainManager.parse_frontmatter_file(discussion_path)
    return fm.get("milestone", "")


def create_review_file(
    branch: str,
    milestone: str,
    base: str,
    repo_root: Path,
) -> Path:
    """Создать review.md по шаблону."""
    folder_match = FOLDER_REGEX.match(branch)
    if not folder_match:
        raise ValueError(f"Ветка '{branch}' не соответствует формату NNNN-{{topic}}")

    nnnn = folder_match.group(1)
    topic_slug = folder_match.group(2)
    topic_title = topic_slug.replace("-", " ").capitalize()

    analysis_dir = repo_root / "specs" / "analysis" / branch

    if not analysis_dir.exists():
        raise FileNotFoundError(f"Папка analysis chain не найдена: {analysis_dir}")

    # Проверить наличие plan-dev.md
    plan_dev_path = analysis_dir / "plan-dev.md"
    if not plan_dev_path.exists():
        raise FileNotFoundError(f"plan-dev.md не найден: {plan_dev_path}")

    # Определить milestone
    if not milestone:
        milestone = get_milestone_from_discussion(analysis_dir)
    if not milestone:
        milestone = "v0.1"

    # Проверить существование review.md
    review_path = analysis_dir / "review.md"
    if review_path.exists():
        raise FileExistsError(f"review.md уже существует: {review_path}")

    # Заполнить шаблон
    content = TEMPLATE.format(
        branch=branch,
        nnnn=nnnn,
        topic_title=topic_title,
        milestone=milestone,
        base=base,
        svc_placeholder="{svc}",
        level_placeholder="{level}",
        tech_placeholder="{tech}",
    )

    review_path.write_text(content, encoding='utf-8')
    return review_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание файла review.md по шаблону"
    )
    parser.add_argument("branch", help="Имя ветки (формат NNNN-{topic})")
    parser.add_argument(
        "--milestone", default="",
        help="Milestone (vX.Y). По умолчанию — из discussion.md или v0.1"
    )
    parser.add_argument(
        "--base", default="main",
        help="Базовая ветка (по умолчанию: main)"
    )
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = ChainManager.find_repo_root(Path(args.repo))

    try:
        review_path = create_review_file(
            branch=args.branch,
            milestone=args.milestone,
            base=args.base,
            repo_root=repo_root,
        )
        rel_path = review_path.relative_to(repo_root)
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
