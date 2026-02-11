#!/usr/bin/env python3
"""
create-discussion-file.py — Создание файла дискуссии из шаблона.

Определяет следующий номер NNNN в specs/discussion/ и создаёт файл
disc-NNNN-topic.md из шаблона standard-discussion.md § 7.

Использование:
    python create-discussion-file.py <topic>

Примеры:
    python create-discussion-file.py oauth2-authorization
    python create-discussion-file.py cache-race-conditions
    python create-discussion-file.py api-latency-reduction

Возвращает:
    0 — файл создан
    1 — ошибка (невалидный topic, папка не существует, файл существует)
"""

import argparse
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

DISC_PATTERN = re.compile(r"^disc-(\d{4})-.+\.md$")

TOPIC_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

TEMPLATE = """\
---
description: {{Описание дискуссии — до 1024 символов}}
standard: specs/.instructions/discussion/standard-discussion.md
standard-version: v1.0
index: specs/discussion/README.md
children: []
status: DRAFT
milestone: {{vX.Y.Z}}
---

# disc-{number}: {{Тема}}

## Проблема / Контекст

**Текущее состояние (AS IS):**
{{Что сейчас работает и как, какие метрики}}

**Проблема:**
{{Зачем это нужно, что не работает, бизнес-контекст}}

## Фичи

### F-1: {{Название}}
{{Описание функциональности}}

## User Stories

### US-1: {{Название}}
Как **{{роль}}**, я хочу **{{действие}}**, чтобы **{{цель}}**.

## Требования

### REQ-1: {{Название}} (F-N, US-N)
- **GIVEN** {{предусловие}}
- **WHEN** {{действие}}
- **THEN** {{результат}}

## Предложения

### PROP-1: {{Название}}
{{Описание предложения}}
→ Влияет на: {{список затронутых фич/user stories}}

## Критерии успеха

- {{Измеримый критерий 1}}
- {{Измеримый критерий 2}}
"""


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


def find_next_number(discussion_dir: Path) -> int:
    """Определить следующий номер NNNN на основе существующих файлов."""
    max_num = 0
    if discussion_dir.exists():
        for f in discussion_dir.iterdir():
            m = DISC_PATTERN.match(f.name)
            if m:
                num = int(m.group(1))
                if num > max_num:
                    max_num = num
    return max_num + 1


# =============================================================================
# Основные функции
# =============================================================================

def create_discussion_file(topic: str, repo_root: Path) -> Path:
    """Создать файл дискуссии из шаблона."""
    discussion_dir = repo_root / "specs" / "discussion"

    if not discussion_dir.exists():
        raise FileNotFoundError(
            f"Папка не существует: specs/discussion/\n"
            f"Используйте /structure-create specs/discussion"
        )

    if not TOPIC_PATTERN.match(topic):
        raise ValueError(
            f"Topic должен быть в kebab-case (латиница): {topic}"
        )

    number = find_next_number(discussion_dir)
    number_str = f"{number:04d}"
    filename = f"disc-{number_str}-{topic}.md"
    file_path = discussion_dir / filename

    if file_path.exists():
        raise FileExistsError(f"Файл уже существует: {filename}")

    content = TEMPLATE.format(number=number_str)
    file_path.write_text(content, encoding="utf-8")

    return file_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание файла дискуссии из шаблона"
    )
    parser.add_argument(
        "topic",
        help="Тема в kebab-case (латиница), например: oauth2-authorization"
    )
    parser.add_argument(
        "--repo", default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    try:
        file_path = create_discussion_file(args.topic, repo_root)
        rel_path = file_path.relative_to(repo_root)
        print(f"✅ Создан: {rel_path}")
        sys.exit(0)

    except (FileNotFoundError, FileExistsError, ValueError) as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
