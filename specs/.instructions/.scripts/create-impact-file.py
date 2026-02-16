#!/usr/bin/env python3
"""
create-impact-file.py — Создание файла импакт-анализа из шаблона.

Извлекает номер NNNN из parent Discussion и создаёт файл
impact-NNNN-topic.md из шаблона standard-impact.md § 7.

Использование:
    python create-impact-file.py --parent specs/discussion/disc-0002-api-rate-limiting.md
    python create-impact-file.py --parent discussion/disc-0002-api-rate-limiting.md custom-topic

Примеры:
    python create-impact-file.py --parent specs/discussion/disc-0002-api-rate-limiting.md
    python create-impact-file.py --parent specs/discussion/disc-0003-email-notification-system.md email-alerts

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

DISC_FILENAME_PATTERN = re.compile(r"^disc-(\d{4})-(.+)\.md$")

TOPIC_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

FRONTMATTER_STATUS_PATTERN = re.compile(r"^status:\s*(.+)$", re.MULTILINE)

FRONTMATTER_MILESTONE_PATTERN = re.compile(r"^milestone:\s*(.+)$", re.MULTILINE)

TEMPLATE = """\
---
description: {{Описание импакт-анализа — до 1024 символов}}
standard: specs/.instructions/impact/standard-impact.md
standard-version: v1.0
index: specs/impact/README.md
parent: {parent}
children: []
status: DRAFT
milestone: {milestone}
---

# impact-{number}: {{Тема}}

## 📋 Резюме

{{Краткое описание влияния: scope, характер изменений, ключевые risk areas}}

## SVC-1: {{Сервис}}

**Тип влияния:** {{Основной/Вторичный/Косвенный/Новый (план создания)}} | **Уверенность:** {{Высокая/Средняя/Предположительно}}

{{Флоу сервиса: что делает, при каких действиях, что порождает, что потребляет — 1-2 абзаца}}

### 📦 Компоненты

| ID | Компонент | Scope | Изменение |
|----|-----------|-------|-----------|
| CMP-1 | {{Компонент}} | {{local/shared ({{сервисы}})}} | {{Новый/Модификация/Удалён — описание}} |

### 💾 Данные и хранение

| ID | Хранилище | Изменение |
|----|-----------|-----------|
| DATA-1 | {{БД/Кэш/Файлы}} | {{Описание изменений}} |

### 🔌 API

| ID | Эндпоинт | Изменение | Совместимость |
|----|----------|-----------|---------------|
| API-1 | {{Метод /path}} | {{Новый/Изменён/Удалён — описание}} | {{N/A/Backward-compatible/Breaking}} |

## 🔗 Зависимости

| ID | От сервиса | К сервису | Тип | Описание | Версия контракта |
|----|-----------|----------|-----|----------|------------------|
| DEP-1 | {{Сервис A}} | {{Сервис B}} | {{sync/async}} | {{Описание зависимости}} | {{/vN или пусто}} |

## ⚠️ Риски

| ID | Риск | Вероятность | Влияние | Mitigation |
|----|------|-------------|---------|------------|
| RISK-1 | {{Описание риска}} | {{Высокая/Средняя/Низкая}} | {{Высокое/Среднее/Низкое}} | {{Стратегия снижения}} |
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
    """Извлечь номер NNNN и topic из имени parent Discussion файла.

    Returns:
        (number_str, topic) — например ("0002", "api-rate-limiting")
    """
    filename = Path(parent_path).name
    m = DISC_FILENAME_PATTERN.match(filename)
    if not m:
        raise ValueError(
            f"Не удалось извлечь NNNN из parent: {filename}\n"
            f"Ожидаемый формат: disc-NNNN-topic.md"
        )
    return m.group(1), m.group(2)


def normalize_parent_path(parent_arg: str) -> str:
    """Нормализовать путь parent к формату discussion/disc-NNNN-topic.md.

    Принимает как specs/discussion/disc-... так и discussion/disc-...
    Возвращает путь без префикса specs/ для использования в frontmatter.
    """
    normalized = parent_arg.replace("\\", "/")
    if normalized.startswith("specs/"):
        normalized = normalized[len("specs/"):]
    return normalized


def resolve_parent_absolute(parent_arg: str, repo_root: Path) -> Path:
    """Получить абсолютный путь к parent Discussion файлу."""
    normalized = parent_arg.replace("\\", "/")
    if normalized.startswith("specs/"):
        return repo_root / normalized
    return repo_root / "specs" / normalized


def read_parent_frontmatter(parent_path: Path) -> tuple[str, str]:
    """Прочитать status и milestone из frontmatter parent Discussion.

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

def create_impact_file(parent_arg: str, topic_override: str | None, repo_root: Path) -> Path:
    """Создать файл импакт-анализа из шаблона."""
    impact_dir = repo_root / "specs" / "impact"

    if not impact_dir.exists():
        raise FileNotFoundError(
            f"Папка не существует: specs/impact/\n"
            f"Используйте /structure-create specs/impact"
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
            f"Parent Discussion не существует: {parent_arg}"
        )

    status, milestone = read_parent_frontmatter(parent_absolute)

    if status != "WAITING":
        raise ValueError(
            f"Parent Discussion status должен быть WAITING, текущий: {status}"
        )

    if not milestone:
        raise ValueError(
            f"Parent Discussion не содержит milestone в frontmatter"
        )

    # --- Проверить что impact с таким номером не существует ---
    filename = f"impact-{number_str}-{topic}.md"
    file_path = impact_dir / filename

    existing = list(impact_dir.glob(f"impact-{number_str}-*.md"))
    if existing:
        raise FileExistsError(
            f"Impact с номером {number_str} уже существует: {existing[0].name}"
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
        description="Создание файла импакт-анализа из шаблона"
    )
    parser.add_argument(
        "--parent", required=True,
        help="Путь к parent Discussion (например: specs/discussion/disc-0002-api-rate-limiting.md)"
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
        file_path = create_impact_file(args.parent, args.topic, repo_root)
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
