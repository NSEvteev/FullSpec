#!/usr/bin/env python3
"""
create-design-file.py — Создание файла проектирования из шаблона.

Извлекает номер NNNN из parent Impact и создаёт файл
design-NNNN-topic.md из шаблона standard-design.md § 7.

Использование:
    python create-design-file.py --parent specs/impact/impact-0002-api-rate-limiting.md
    python create-design-file.py --parent impact/impact-0002-api-rate-limiting.md custom-topic

Примеры:
    python create-design-file.py --parent specs/impact/impact-0001-oauth2-authorization.md
    python create-design-file.py --parent specs/impact/impact-0005-cache-optimization.md cache-design

Возвращает:
    0 — файл создан
    1 — ошибка (parent не существует, status не WAITING, файл существует)
"""

import argparse
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

IMPACT_FILENAME_PATTERN = re.compile(r"^impact-(\d{4})-(.+)\.md$")

TOPIC_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

FRONTMATTER_STATUS_PATTERN = re.compile(r"^status:\s*(.+)$", re.MULTILINE)

FRONTMATTER_MILESTONE_PATTERN = re.compile(r"^milestone:\s*(.+)$", re.MULTILINE)

TEMPLATE = """\
---
description: {{Описание проектирования — до 1024 символов}}
standard: specs/.instructions/design/standard-design.md
standard-version: v1.1
index: specs/design/README.md
parent: {parent}
children: []
status: DRAFT
milestone: {milestone}
---

# design-{number}: {{Тема}}

## 📋 Резюме

{{Краткое описание проектных решений: scope, ключевые решения, изменения vs Impact}}

## SVC-1: {{Сервис}}

**Impact:** SVC-N ({{Тип}}, {{Уверенность}}) | **Решение Design:** {{Подтверждён/Изменён/Отклонён/Добавлен}}

{{Описание ответственности: за что отвечает, чем владеет, что предоставляет, что потребляет — 1-2 абзаца}}

### 📋 Ответственность

- {{Ответственность 1}}
- {{Ответственность 2}}

### 📦 Компоненты

| ID | Компонент | Scope | Решение |
|----|-----------|-------|---------|
| CMP-1 | {{Компонент}} | {{local/shared ({{путь}})}} | {{Подтверждён/Изменён/Добавлен Design}} |

### 🔗 Зависимости

- **Предоставляет:** {{INT-N (описание)}}
- **Потребляет:** {{INT-N (описание)}}

## INT-1: {{Описание взаимодействия}}

**Участники:** {{provider}} (provider) ↔ {{consumer}} (consumer)
**Паттерн:** {{sync/async}} ({{протокол}})
**Источник Impact:** {{DEP-N или —}}

### Контракт

{{Спецификация endpoint/события}}

### Sequence

```mermaid
sequenceDiagram
    {{участники и вызовы}}
```

## 🧪 Системные тест-сценарии

| ID | Сценарий | Участники | Тип | Источник |
|----|----------|-----------|-----|----------|
| STS-1 | {{Описание сценария}} | {{Сервис 1, Сервис 2}} | {{e2e/integration/load}} | {{INT-N}} |
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


def parse_parent_filename(parent_path: str) -> tuple[str, str]:
    """Извлечь номер NNNN и topic из имени parent Impact файла.

    Returns:
        (number_str, topic) — например ("0002", "api-rate-limiting")
    """
    filename = Path(parent_path).name
    m = IMPACT_FILENAME_PATTERN.match(filename)
    if not m:
        raise ValueError(
            f"Не удалось извлечь NNNN из parent: {filename}\n"
            f"Ожидаемый формат: impact-NNNN-topic.md"
        )
    return m.group(1), m.group(2)


def normalize_parent_path(parent_arg: str) -> str:
    """Нормализовать путь parent к формату impact/impact-NNNN-topic.md.

    Принимает как specs/impact/impact-... так и impact/impact-...
    Возвращает путь без префикса specs/ для использования в frontmatter.
    """
    normalized = parent_arg.replace("\\", "/")
    if normalized.startswith("specs/"):
        normalized = normalized[len("specs/"):]
    return normalized


def resolve_parent_absolute(parent_arg: str, repo_root: Path) -> Path:
    """Получить абсолютный путь к parent Impact файлу."""
    normalized = parent_arg.replace("\\", "/")
    if normalized.startswith("specs/"):
        return repo_root / normalized
    return repo_root / "specs" / normalized


def read_parent_frontmatter(parent_path: Path) -> tuple[str, str]:
    """Прочитать status и milestone из frontmatter parent Impact.

    Returns:
        (status, milestone) — например ("WAITING", "v1.1.0")
    """
    content = parent_path.read_text(encoding="utf-8")

    status_match = FRONTMATTER_STATUS_PATTERN.search(content)
    status = status_match.group(1).strip() if status_match else ""

    milestone_match = FRONTMATTER_MILESTONE_PATTERN.search(content)
    milestone = milestone_match.group(1).strip() if milestone_match else ""

    return status, milestone


# =============================================================================
# Основные функции
# =============================================================================

def create_design_file(parent_arg: str, topic_override: str | None, repo_root: Path) -> Path:
    """Создать файл проектирования из шаблона."""
    design_dir = repo_root / "specs" / "design"

    if not design_dir.exists():
        raise FileNotFoundError(
            f"Папка не существует: specs/design/\n"
            f"Используйте /structure-create specs/design"
        )

    # --- Извлечь номер и topic из parent ---
    number_str, parent_topic = parse_parent_filename(parent_arg)

    topic = topic_override if topic_override else parent_topic

    if not TOPIC_PATTERN.match(topic):
        raise ValueError(
            f"Topic должен быть в kebab-case (латиница): {topic}"
        )

    # --- Проверить parent файл ---
    parent_absolute = resolve_parent_absolute(parent_arg, repo_root)

    if not parent_absolute.exists():
        raise FileNotFoundError(
            f"Parent Impact не существует: {parent_arg}"
        )

    status, milestone = read_parent_frontmatter(parent_absolute)

    if status != "WAITING":
        raise ValueError(
            f"Parent Impact status должен быть WAITING, текущий: {status}"
        )

    if not milestone:
        raise ValueError(
            f"Parent Impact не содержит milestone в frontmatter"
        )

    # --- Проверить что design с таким номером не существует ---
    filename = f"design-{number_str}-{topic}.md"
    file_path = design_dir / filename

    existing = list(design_dir.glob(f"design-{number_str}-*.md"))
    if existing:
        raise FileExistsError(
            f"Design с номером {number_str} уже существует: {existing[0].name}"
        )

    # --- Создать файл ---
    parent_frontmatter = normalize_parent_path(parent_arg)

    content = TEMPLATE.format(
        number=number_str,
        parent=parent_frontmatter,
        milestone=milestone,
    )
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
        description="Создание файла проектирования из шаблона"
    )
    parser.add_argument(
        "--parent", required=True,
        help="Путь к parent Impact (например: specs/impact/impact-0001-oauth2-authorization.md)"
    )
    parser.add_argument(
        "topic", nargs="?", default=None,
        help="Тема в kebab-case (латиница). Если не указана — извлекается из parent filename"
    )
    parser.add_argument(
        "--repo", default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    try:
        file_path = create_design_file(args.parent, args.topic, repo_root)
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
