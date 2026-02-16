#!/usr/bin/env python3
"""
create-service-file.py — Создание файла-заглушки сервиса из шаблона.

Создаёт specs/architecture/services/{svc}.md по шаблону заглушки
(standard-service.md § 9.1). Извлекает ссылки на Discussion и Design
из frontmatter Design-документа для Planned Changes.

Использование:
    python create-service-file.py --svc auth --design specs/design/design-0001-oauth2.md
    python create-service-file.py --svc billing --design specs/design/design-0001-oauth2.md --description "Биллинг и тарификация"

Примеры:
    python create-service-file.py --svc auth --design specs/design/design-0001-oauth2.md
    python create-service-file.py --svc notification --design specs/design/design-0005-notifications.md

Возвращает:
    0 — файл создан
    1 — ошибка (Design не существует, status не WAITING, файл существует)
"""

import argparse
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

SERVICE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

FRONTMATTER_STATUS_PATTERN = re.compile(r"^status:\s*(.+)$", re.MULTILINE)

FRONTMATTER_PARENT_PATTERN = re.compile(r"^parent:\s*(.+)$", re.MULTILINE)

DESIGN_FILENAME_PATTERN = re.compile(r"^design-(\d{4})-(.+)\.md$")

IMPACT_FILENAME_PATTERN = re.compile(r"^impact-(\d{4})-(.+)\.md$")

DISC_FILENAME_PATTERN = re.compile(r"^disc-(\d{4})-(.+)\.md$")

PLANNED_MARKER = "*Предварительно (Design → WAITING). Финализируется при ADR → DONE.*"

STUB_PLACEHOLDER = "*Заполняется при ADR → DONE.*"

TEMPLATE = """\
---
description: Архитектура сервиса {svc} — {{назначение из Design}}.
service: {svc}
---

# {svc}

## Резюме

{{Назначение из секции сервиса в Design — 1-3 предложения}}

## API контракты

{planned_marker}

| Тип | Endpoint/Event | Метод | Описание |
|-----|---------------|-------|----------|
| {{REST/Event/CLI}} | {{endpoint}} | {{метод}} | {{описание из Impact API-N}} |

## Data Model

{planned_marker}

| Сущность | Хранилище | Назначение |
|----------|-----------|-----------|
| {{Entity}} | {{Storage: table/key}} | {{описание из Impact DATA-N}} |

## Code Map

{stub_placeholder}

## Внешние зависимости

{planned_marker}

| Тип | Путь/Сервис | Что используем | Роль |
|-----|------------|---------------|------|
| {{shared/service}} | {{путь/сервис}} | {{что}} | {{provider/consumer/publisher/subscriber}} |

## Границы автономии LLM

{stub_placeholder}

## Planned Changes

- **[Discussion {disc_number}: {disc_topic}]({disc_path})**
  Статус: WAITING | Затрагивает: {{области из Design}}
  Design: [{design_id}]({design_path})

## Changelog

*Нет записей.*
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


def resolve_path(path_arg: str, repo_root: Path) -> Path:
    """Получить абсолютный путь, добавляя specs/ если нужно."""
    normalized = path_arg.replace("\\", "/")
    if normalized.startswith("specs/"):
        return repo_root / normalized
    return repo_root / "specs" / normalized


def read_frontmatter(file_path: Path) -> dict[str, str]:
    """Прочитать frontmatter из файла.

    Returns:
        Словарь с ключами status, parent.
    """
    content = file_path.read_text(encoding="utf-8")

    status_match = FRONTMATTER_STATUS_PATTERN.search(content)
    parent_match = FRONTMATTER_PARENT_PATTERN.search(content)

    return {
        "status": status_match.group(1).strip() if status_match else "",
        "parent": parent_match.group(1).strip() if parent_match else "",
    }


def extract_disc_info(impact_parent: str, repo_root: Path) -> tuple[str, str, str]:
    """Извлечь номер, topic и путь Discussion из parent Impact.

    Цепочка: Design.parent → Impact.parent → Discussion.

    Returns:
        (disc_number, disc_topic, disc_path) — например ("0001", "oauth2", "specs/discussion/disc-0001-oauth2.md")
    """
    impact_path = resolve_path(impact_parent, repo_root)
    if not impact_path.exists():
        return "", "", ""

    fm = read_frontmatter(impact_path)
    disc_ref = fm["parent"]
    if not disc_ref:
        return "", "", ""

    disc_path = resolve_path(disc_ref, repo_root)
    filename = disc_path.name
    m = DISC_FILENAME_PATTERN.match(filename)
    if not m:
        return "", "", ""

    disc_number = m.group(1)
    disc_topic = m.group(2).replace("-", " ")

    disc_rel = disc_ref if disc_ref.startswith("specs/") else f"specs/{disc_ref}"
    return disc_number, disc_topic, disc_rel


# =============================================================================
# Основные функции
# =============================================================================

def create_service_file(
    svc: str,
    design_arg: str,
    description: str | None,
    repo_root: Path,
) -> Path:
    """Создать файл-заглушку сервиса из шаблона."""
    services_dir = repo_root / "specs" / "architecture" / "services"

    if not services_dir.exists():
        raise FileNotFoundError(
            f"Папка не существует: specs/architecture/services/\n"
            f"Используйте /structure-create specs/architecture/services"
        )

    # --- Валидировать имя сервиса ---
    if not SERVICE_NAME_PATTERN.match(svc):
        raise ValueError(
            f"Имя сервиса должно быть в kebab-case (латиница): {svc}"
        )

    # --- Проверить что файл не существует ---
    file_path = services_dir / f"{svc}.md"
    if file_path.exists():
        raise FileExistsError(
            f"Сервисный документ уже существует: specs/architecture/services/{svc}.md"
        )

    # --- Прочитать Design ---
    design_absolute = resolve_path(design_arg, repo_root)
    if not design_absolute.exists():
        raise FileNotFoundError(
            f"Design не существует: {design_arg}"
        )

    design_fm = read_frontmatter(design_absolute)

    if design_fm["status"] != "WAITING":
        raise ValueError(
            f"Design status должен быть WAITING, текущий: {design_fm['status']}"
        )

    # --- Извлечь design-id и design-path ---
    design_name = design_absolute.name
    m = DESIGN_FILENAME_PATTERN.match(design_name)
    if not m:
        raise ValueError(
            f"Не удалось извлечь ID из Design: {design_name}\n"
            f"Ожидаемый формат: design-NNNN-topic.md"
        )

    design_number = m.group(1)
    design_id = f"design-{design_number}"
    design_rel = design_arg if design_arg.startswith("specs/") else f"specs/{design_arg}"
    design_rel = design_rel.replace("\\", "/")

    # --- Извлечь Discussion через Impact ---
    impact_ref = design_fm["parent"]
    disc_number, disc_topic, disc_path = extract_disc_info(impact_ref, repo_root)

    if not disc_number:
        disc_number = design_number
        disc_topic = "topic"
        disc_path = f"specs/discussion/disc-{design_number}-topic.md"

    # --- Создать файл ---
    content = TEMPLATE.format(
        svc=svc,
        planned_marker=PLANNED_MARKER,
        stub_placeholder=STUB_PLACEHOLDER,
        disc_number=disc_number,
        disc_topic=disc_topic,
        disc_path=disc_path,
        design_id=design_id,
        design_path=design_rel,
    )

    if description:
        content = content.replace(
            "{{назначение из Design}}",
            description,
        )

    file_path.write_text(content, encoding="utf-8")
    return file_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа: парсинг аргументов и создание файла-заглушки сервиса."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание файла-заглушки сервиса из шаблона"
    )
    parser.add_argument(
        "--svc", required=True,
        help="Имя сервиса (kebab-case, например: auth, billing, notification-gateway)"
    )
    parser.add_argument(
        "--design", required=True,
        help="Путь к Design-документу (например: specs/design/design-0001-oauth2.md)"
    )
    parser.add_argument(
        "--description", default=None,
        help="Краткое назначение сервиса (для description в frontmatter)"
    )
    parser.add_argument(
        "--repo", default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    try:
        file_path = create_service_file(args.svc, args.design, args.description, repo_root)
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
