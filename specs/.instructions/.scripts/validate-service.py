#!/usr/bin/env python3
"""
validate-service.py — Валидация сервисных документов services/{svc}.md.

Использование:
    python validate-service.py <путь>              # Один файл или папка
    python validate-service.py <путь> --verbose    # Подробный вывод

Проверяет:
    - SVC001: Frontmatter существует
    - SVC002: description — формат "Архитектура сервиса X — ..." и длина ≤ 1024
    - SVC003: Поле service присутствует и kebab-case
    - SVC004: created-by — заглушка: отсутствует; полный: формат adr-NNNN
    - SVC005: last-updated-by — заглушка: отсутствует; полный: формат adr-NNNN
    - SVC006: Все 8 обязательных секций присутствуют
    - SVC007: Порядок секций соответствует стандарту
    - SVC008: Таблицы содержат обязательные колонки
    - SVC009: Code Map содержит 4 подсекции (full-режим)
    - SVC010: Роли во Внешних зависимостях корректны (full-режим)
    - SVC011: Границы автономии LLM — три уровня (full-режим)
    - SVC012: Строка сервиса в services/README.md
    - SVC013: Метка svc:{service} в labels.yml
    - SVC014: Секция Changelog — формат и содержание

    Режим заглушки: секции 2, 3, 5 — placeholder ИЛИ предварительные данные с маркером Planned.
    Режим заглушки: секции 4, 6 — только placeholder.
    Автоматически определяет заглушка/полный по отсутствию created-by.

SSOT:
    - specs/.instructions/living-docs/service/standard-service.md
    - specs/.instructions/living-docs/service/validation-service.md

Примеры:
    python validate-service.py specs/architecture/services/auth.md
    python validate-service.py specs/architecture/services/ --verbose

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
"""

import argparse
import re
import sys
from pathlib import Path

# Коды ошибок
ERROR_CODES = {
    "SVC001": "Отсутствует frontmatter",
    "SVC002": "Некорректный description",
    "SVC003": "Отсутствует или некорректное поле service",
    "SVC004": "Некорректный created-by",
    "SVC005": "Некорректный last-updated-by",
    "SVC006": "Отсутствует обязательная секция",
    "SVC007": "Порядок секций нарушен",
    "SVC008": "Некорректная таблица",
    "SVC009": "Code Map без обязательных подсекций",
    "SVC010": "Некорректная роль во Внешних зависимостях",
    "SVC011": "Нет трёх уровней автономии LLM",
    "SVC012": "Нет строки в services/README.md",
    "SVC013": "Нет метки svc: в labels.yml",
    "SVC014": "Некорректная секция Changelog",
}

# 8 обязательных секций в порядке
REQUIRED_SECTIONS = [
    "Резюме",
    "API контракты",
    "Data Model",
    "Code Map",
    "Внешние зависимости",
    "Границы автономии LLM",
    "Planned Changes",
    "Changelog",
]

# Секции 4, 6 — в заглушке содержат только placeholder
STUB_PLACEHOLDER_ONLY_SECTIONS = [
    "Code Map",
    "Границы автономии LLM",
]

# Секции 2, 3, 5 — в заглушке могут содержать placeholder ИЛИ предварительные данные с маркером
STUB_PLANNED_OR_PLACEHOLDER_SECTIONS = [
    "API контракты",
    "Data Model",
    "Внешние зависимости",
]

# Все секции 2-6 (для полного режима проверки)
STUB_PLACEHOLDER_SECTIONS = (
    STUB_PLANNED_OR_PLACEHOLDER_SECTIONS + STUB_PLACEHOLDER_ONLY_SECTIONS
)

STUB_PLACEHOLDER = "*Заполняется при ADR → DONE.*"
PLANNED_MARKER = "*Предварительно (Design → WAITING). Финализируется при ADR → DONE.*"

# 4 обязательные подсекции Code Map
CODE_MAP_SUBSECTIONS = [
    "Tech Stack",
    "Пакеты",
    "Точки входа",
    "Внутренние зависимости",
]

VALID_ROLES = {"provider", "consumer", "publisher", "subscriber"}

ADR_PATTERN = re.compile(r"^adr-\d{4}$")
KEBAB_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def parse_frontmatter(content: str) -> dict | None:
    """Извлечь frontmatter из markdown-файла."""
    if not content.startswith("---"):
        return None

    end = content.find("---", 3)
    if end == -1:
        return None

    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.split("\n"):
        match = re.match(r"^([\w][\w-]*):\s*(.+)$", line.strip())
        if match:
            result[match.group(1)] = match.group(2).strip()

    return result


def extract_h2_sections(content: str) -> list[str]:
    """Извлечь все заголовки ## из markdown (вне code blocks)."""
    sections = []
    in_code = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = re.match(r"^##\s+(.+)$", stripped)
        if match:
            sections.append(match.group(1).strip())
    return sections


def extract_h3_sections(content: str) -> list[str]:
    """Извлечь все заголовки ### из markdown (вне code blocks)."""
    sections = []
    in_code = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = re.match(r"^###\s+(.+)$", stripped)
        if match:
            sections.append(match.group(1).strip())
    return sections


def extract_section_content(content: str, section_name: str) -> str:
    """Извлечь содержимое секции ## до следующей секции ##."""
    pattern = rf"^##\s+{re.escape(section_name)}\s*$"
    lines = content.split("\n")
    start = None
    end = None
    in_code = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(pattern, stripped) and start is None:
            start = i + 1
        elif start is not None and re.match(r"^##\s+", stripped):
            end = i
            break

    if start is None:
        return ""
    if end is None:
        end = len(lines)
    return "\n".join(lines[start:end])


def validate_file(file_path: Path, repo_root: Path, verbose: bool = False) -> list[str]:
    """Валидация одного файла services/{svc}.md."""
    errors = []
    rel = file_path.relative_to(repo_root)

    content = file_path.read_text(encoding="utf-8")

    # SVC001: frontmatter
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(f"[SVC001] {rel}: отсутствует frontmatter")
        return errors  # без frontmatter дальше проверять нечего

    if verbose:
        print(f"  ✓ frontmatter существует")

    # SVC002: description
    desc = fm.get("description", "")
    if not desc:
        errors.append(f"[SVC002] {rel}: отсутствует description")
    elif len(desc) > 1024:
        errors.append(f"[SVC002] {rel}: description длиннее 1024 символов ({len(desc)})")
    elif not desc.startswith("Архитектура сервиса"):
        errors.append(f"[SVC002] {rel}: description не начинается с 'Архитектура сервиса'")
    elif verbose:
        print(f"    description ✓")

    # SVC003: service
    svc = fm.get("service", "")
    if not svc:
        errors.append(f"[SVC003] {rel}: отсутствует поле service")
    elif not KEBAB_PATTERN.match(svc):
        errors.append(f"[SVC003] {rel}: service '{svc}' не в kebab-case")
    elif verbose:
        print(f"    service: {svc} ✓")

    # Детекция заглушка vs полный: отсутствие created-by = заглушка
    created = fm.get("created-by", "")
    updated_by = fm.get("last-updated-by", "")
    is_stub = not created

    if verbose:
        mode = "заглушка" if is_stub else "полный"
        print(f"  Режим: {mode}")

    # SVC004: created-by
    if is_stub:
        # Заглушка: created-by отсутствует — ОК, но проверим секции на согласованность
        if verbose:
            print(f"    created-by: отсутствует (заглушка) ✓")
    else:
        if not ADR_PATTERN.match(created):
            errors.append(f"[SVC004] {rel}: created-by '{created}' не в формате adr-NNNN")
        elif verbose:
            print(f"    created-by: {created} ✓")

    # SVC005: last-updated-by
    if is_stub:
        if updated_by:
            errors.append(f"[SVC005] {rel}: last-updated-by присутствует в заглушке (должен отсутствовать)")
        elif verbose:
            print(f"    last-updated-by: отсутствует (заглушка) ✓")
    else:
        if not updated_by:
            errors.append(f"[SVC005] {rel}: отсутствует поле last-updated-by")
        elif not ADR_PATTERN.match(updated_by):
            errors.append(f"[SVC005] {rel}: last-updated-by '{updated_by}' не в формате adr-NNNN")
        elif verbose:
            print(f"    last-updated-by: {updated_by} ✓")

    # SVC006 + SVC007: обязательные секции и порядок
    h2 = extract_h2_sections(content)
    found_order = []

    for section in REQUIRED_SECTIONS:
        if section not in h2:
            errors.append(f"[SVC006] {rel}: отсутствует секция '{section}'")
        else:
            found_order.append(h2.index(section))
            if verbose:
                print(f"    секция: {section} ✓")

    if len(found_order) == len(REQUIRED_SECTIONS) and found_order != sorted(found_order):
        errors.append(f"[SVC007] {rel}: порядок секций нарушен")

    # Режим заглушки: проверить placeholder/planned в секциях 2-6
    if is_stub:
        # Секции 4, 6 — только placeholder
        for section in STUB_PLACEHOLDER_ONLY_SECTIONS:
            sec_content = extract_section_content(content, section).strip()
            if sec_content and STUB_PLACEHOLDER not in sec_content:
                errors.append(
                    f"[SVC004] {rel}: секция '{section}' заполнена, "
                    f"но created-by отсутствует (режим заглушки)"
                )
            elif verbose:
                print(f"    секция '{section}': placeholder ✓")

        # Секции 2, 3, 5 — placeholder ИЛИ предварительные данные с маркером
        for section in STUB_PLANNED_OR_PLACEHOLDER_SECTIONS:
            sec_content = extract_section_content(content, section).strip()
            if sec_content and STUB_PLACEHOLDER not in sec_content and PLANNED_MARKER not in sec_content:
                errors.append(
                    f"[SVC004] {rel}: секция '{section}' заполнена без маркера, "
                    f"но created-by отсутствует (режим заглушки). "
                    f"Ожидается placeholder или предварительные данные с маркером Planned"
                )
            elif verbose:
                if PLANNED_MARKER in (sec_content or ""):
                    print(f"    секция '{section}': planned ✓")
                else:
                    print(f"    секция '{section}': placeholder ✓")

        # Changelog в заглушке = *Нет записей.*
        changelog_content = extract_section_content(content, "Changelog").strip()
        if changelog_content and "*Нет записей.*" not in changelog_content:
            errors.append(f"[SVC014] {rel}: Changelog в заглушке должен быть '*Нет записей.*'")
        elif verbose:
            print(f"    Changelog: заглушка ✓")

    # Полный режим: проверить что нет placeholder и planned маркеров
    if not is_stub:
        for section in STUB_PLACEHOLDER_SECTIONS:
            sec_content = extract_section_content(content, section).strip()
            if STUB_PLACEHOLDER in sec_content:
                errors.append(
                    f"[SVC008] {rel}: секция '{section}' содержит placeholder заглушки "
                    f"в полном документе"
                )
            if PLANNED_MARKER in sec_content:
                errors.append(
                    f"[SVC008] {rel}: секция '{section}' содержит маркер Planned "
                    f"в полном документе (должен быть убран при ADR → DONE)"
                )

        # SVC008: проверка колонок таблиц
        table_checks = {
            "API контракты": ["Тип", "Endpoint/Event", "Метод", "Описание"],
            "Data Model": ["Сущность", "Хранилище", "Назначение"],
            "Внешние зависимости": ["Тип", "Путь/Сервис", "Что используем", "Роль"],
        }
        for section_name, expected_cols in table_checks.items():
            sec_content = extract_section_content(content, section_name)
            if not sec_content.strip():
                continue
            # Ищем первую строку таблицы (заголовок) с |
            for line in sec_content.split("\n"):
                cells = [c.strip() for c in line.split("|") if c.strip()]
                if len(cells) >= 2 and cells[0] not in ("---", "-"):
                    # Первая непустая строка с | — заголовок таблицы
                    missing = [col for col in expected_cols if col not in cells]
                    if missing:
                        errors.append(
                            f"[SVC008] {rel}: таблица '{section_name}' "
                            f"без колонок: {', '.join(missing)}"
                        )
                    elif verbose:
                        print(f"    таблица '{section_name}': колонки ✓")
                    break

        # SVC009: Code Map подсекции
        h3 = extract_h3_sections(content)
        for sub in CODE_MAP_SUBSECTIONS:
            if sub not in h3:
                errors.append(f"[SVC009] {rel}: Code Map без подсекции '{sub}'")
            elif verbose:
                print(f"    подсекция: {sub} ✓")

        # SVC010: роли во Внешних зависимостях
        deps_content = extract_section_content(content, "Внешние зависимости")
        if deps_content:
            for line in deps_content.split("\n"):
                # Ищем строки таблицы с ролью в последней колонке
                cells = [c.strip() for c in line.split("|") if c.strip()]
                if len(cells) >= 4 and cells[0] not in ("Тип", "---", "-"):
                    role = cells[-1].strip()
                    if role and role not in VALID_ROLES and not role.startswith("-"):
                        errors.append(f"[SVC010] {rel}: некорректная роль '{role}'")

        # SVC011: Границы автономии LLM
        bounds_content = extract_section_content(content, "Границы автономии LLM")
        levels_found = {
            "Свободно": "**Свободно:**" in bounds_content or "**Свободно**" in bounds_content,
            "Флаг": "**Флаг:**" in bounds_content or "**Флаг**" in bounds_content,
            "CONFLICT": "**CONFLICT:**" in bounds_content or "**CONFLICT**" in bounds_content,
        }
        for level, found in levels_found.items():
            if not found:
                errors.append(f"[SVC011] {rel}: нет уровня автономии '{level}'")
            elif verbose:
                print(f"    уровень: {level} ✓")

        # SVC014: Changelog (full-режим)
        changelog_content = extract_section_content(content, "Changelog").strip()
        if not changelog_content:
            errors.append(f"[SVC014] {rel}: секция Changelog пуста")
        elif changelog_content == "*Нет записей.*":
            # Допустимо для full-документа, если Design ещё не DONE
            if verbose:
                print(f"    Changelog: пуст (нет записей) ✓")
        else:
            # Проверить формат записей: маркеры DONE/REJECTED/CONFLICT-RESOLVED
            has_entries = False
            for line in changelog_content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("- **["):
                    has_entries = True
                    if "| DONE" not in stripped and "| REJECTED" not in stripped:
                        errors.append(
                            f"[SVC014] {rel}: запись Changelog без маркера "
                            f"DONE или REJECTED"
                        )
            if has_entries and verbose:
                print(f"    Changelog: формат ✓")

    # SVC012: строка в services/README.md
    if svc:
        readme_path = repo_root / "specs" / "architecture" / "services" / "README.md"
        if readme_path.exists():
            readme_content = readme_path.read_text(encoding="utf-8")
            if f"`{svc}`" not in readme_content and f"| {svc} " not in readme_content:
                errors.append(f"[SVC012] {rel}: сервис '{svc}' не найден в services/README.md")
            elif verbose:
                print(f"    README.md: {svc} ✓")

    # SVC013: метка svc:{service} в labels.yml
    if svc:
        labels_path = repo_root / ".github" / "labels.yml"
        if labels_path.exists():
            labels_content = labels_path.read_text(encoding="utf-8")
            if f"svc:{svc}" not in labels_content:
                errors.append(f"[SVC013] {rel}: метка 'svc:{svc}' не найдена в labels.yml")
            elif verbose:
                print(f"    labels.yml: svc:{svc} ✓")

    return errors


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация сервисных документов services/{svc}.md"
    )
    parser.add_argument("path", help="Файл .md или папка services/")
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    target = Path(args.path)

    # Абсолютный путь
    if not target.is_absolute():
        target = repo_root / target

    # Собрать файлы
    files = []
    if target.is_dir():
        files = sorted(target.glob("*.md"))
        # Исключить README.md
        files = [f for f in files if f.name != "README.md"]
    elif target.is_file() and target.suffix == ".md":
        files = [target]
    else:
        print(f"❌ Путь не найден: {target}")
        sys.exit(1)

    if not files:
        print("⚠ Нет файлов для валидации")
        sys.exit(0)

    print(f"🔍 Валидация сервисных документов ({len(files)} файлов)...")

    all_errors = []
    for f in files:
        if args.verbose:
            print(f"\n📄 {f.relative_to(repo_root)}")
        errors = validate_file(f, repo_root, verbose=args.verbose)
        all_errors.extend(errors)

    if all_errors:
        print(f"\n❌ Найдено ошибок: {len(all_errors)}")
        for err in all_errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("✅ Все сервисные документы валидны")
        sys.exit(0)


if __name__ == "__main__":
    main()
