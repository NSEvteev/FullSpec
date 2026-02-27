#!/usr/bin/env python3
"""
create-analysis-design-file.py — Создание файла design.md по шаблону.

Создаёт пустой design.md в папке specs/analysis/{branch}/ с заполненным frontmatter
и базовой структурой секций (Резюме, SVC-N, INT-N, STS-N).

Использование:
    python create-analysis-design-file.py <branch> [--description <desc>] [--repo <dir>]

Аргументы:
    branch      Имя папки analysis chain (формат NNNN-{topic})

Примеры:
    python create-analysis-design-file.py 0001-task-dashboard
    python create-analysis-design-file.py 0001-oauth2-authorization --description "OAuth2 авторизация — Design"

Возвращает:
    0 — файл создан
    1 — ошибка (файл существует, папка не найдена, нет discussion.md)

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

TEMPLATE = """\
---
description: {description}
standard: specs/.instructions/analysis/design/standard-design.md
standard-version: v2.1
index: specs/analysis/README.md
parent: discussion.md
children: []
status: DRAFT
milestone: {milestone}
---

# {nnnn}: {topic_title} — Design

## Резюме

{{Scope, ключевые решения, кол-во INT-N и STS-N}}

## Выбор технологий

{{Сравнительные таблицы по категориям, 7 критериев, "Выбрано"}}

## SVC-1: {{Сервис}}

{{Описание: что делает в контексте изменения — 1-2 абзаца}}

### 1. Назначение

{{Delta к § 1 — как меняется зона ответственности}}

### 2. API контракты

{{ADDED/MODIFIED/REMOVED endpoints}}

### 3. Data Model

{{ADDED/MODIFIED/REMOVED таблицы, колонки, индексы}}

### 4. Потоки

{{ADDED/MODIFIED runtime-сценарии}}

### 5. Code Map

{{ADDED/MODIFIED/REMOVED пакеты, модули}}

### 6. Зависимости

{{ADDED/MODIFIED — ссылки на INT-N, shared-код}}

### 7. Доменная модель

{{ADDED/MODIFIED/REMOVED агрегаты, события}}

### 8. Границы автономии LLM

{{ADDED/MODIFIED — Свободно/Флаг/CONFLICT}}

### 9. Решения по реализации

{{WHY: trade-offs, алгоритмы, библиотеки}}

## INT-1: {{Описание взаимодействия}}

**Участники:** {{provider}} ({{role}}) ↔ {{consumer}} ({{role}})
**Паттерн:** {{sync/async}} ({{протокол}})

### Контракт

{{Спецификация endpoint/события}}

### Sequence

```mermaid
sequenceDiagram
    {{участники и вызовы}}
```

## Системные тест-сценарии

| ID | Сценарий | Участники | Тип | Источник |
|----|----------|-----------|-----|----------|
| STS-1 | {{Описание}} | {{Сервисы}} | {{e2e/integration/load}} | {{INT-N}} |
"""


# =============================================================================
# Функции
# =============================================================================

def get_discussion_info(analysis_dir: Path) -> dict:
    """Извлечь milestone и description из discussion.md через ChainManager (SSOT)."""
    discussion_path = analysis_dir / "discussion.md"
    fm = ChainManager.parse_frontmatter_file(discussion_path)
    return {
        "milestone": fm.get("milestone", ""),
        "status": fm.get("status", ""),
        "description": fm.get("description", ""),
    }


def create_design_file(
    branch: str,
    description: str,
    repo_root: Path,
) -> Path:
    """Создать design.md по шаблону."""
    folder_match = FOLDER_REGEX.match(branch)
    if not folder_match:
        raise ValueError(f"Папка '{branch}' не соответствует формату NNNN-{{topic}}")

    nnnn = folder_match.group(1)
    topic_slug = folder_match.group(2)
    topic_title = topic_slug.replace("-", " ").capitalize()

    analysis_dir = repo_root / "specs" / "analysis" / branch

    if not analysis_dir.exists():
        raise FileNotFoundError(f"Папка analysis chain не найдена: {analysis_dir}")

    # Проверить наличие discussion.md
    discussion_path = analysis_dir / "discussion.md"
    if not discussion_path.exists():
        raise FileNotFoundError(f"discussion.md не найден: {discussion_path}")

    # Проверить статус discussion.md
    disc_info = get_discussion_info(analysis_dir)
    if disc_info["status"] != "WAITING":
        raise ValueError(
            f"Discussion не в статусе WAITING (текущий: {disc_info['status']}). "
            f"Design может быть создан только после одобрения Discussion."
        )

    # Определить milestone
    milestone = disc_info["milestone"]
    if not milestone:
        milestone = "v0.1.0"

    # Определить description
    if not description:
        disc_desc = disc_info["description"]
        description = f"{disc_desc} — проектирование распределения ответственностей между сервисами."

    # Проверить существование design.md
    design_path = analysis_dir / "design.md"
    if design_path.exists():
        raise FileExistsError(f"design.md уже существует: {design_path}")

    # Заполнить шаблон
    content = TEMPLATE.format(
        description=description,
        milestone=milestone,
        nnnn=nnnn,
        topic_title=topic_title,
    )

    design_path.write_text(content, encoding='utf-8')
    return design_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание файла design.md по шаблону"
    )
    parser.add_argument("branch", help="Имя папки analysis chain (формат NNNN-{topic})")
    parser.add_argument(
        "--description", default="",
        help="Описание проектирования (до 1024 символов). По умолчанию — из discussion.md"
    )
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = ChainManager.find_repo_root(Path(args.repo))

    try:
        design_path = create_design_file(
            branch=args.branch,
            description=args.description,
            repo_root=repo_root,
        )
        rel_path = design_path.relative_to(repo_root)
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
