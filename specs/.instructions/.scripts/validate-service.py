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
    - SVC015: Оглавление присутствует
    - SVC016: Planned Changes — блоки Design с ADDED/MODIFIED/REMOVED

    Двухслойная модель:
    - Заглушка: AS IS секции (1-6) содержат *Нет.* или *Сервис ещё не реализован.*
    - Заглушка: Planned Changes содержит блоки Design с ADDED/MODIFIED/REMOVED
    - Полный: AS IS секции заполнены, нет *Нет.* placeholder'ов
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
    "SVC015": "Отсутствует оглавление",
    "SVC016": "Planned Changes без структуры ADDED/MODIFIED/REMOVED",
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

# AS IS секции (1-6) — в заглушке пусты, в полном заполнены
AS_IS_SECTIONS = [
    "Резюме",
    "API контракты",
    "Data Model",
    "Code Map",
    "Внешние зависимости",
    "Границы автономии LLM",
]

# Допустимые placeholder'ы для пустых AS IS секций в заглушке
STUB_EMPTY_MARKERS = [
    "*Нет.*",
    "*Сервис ещё не реализован.*",
]

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


def iter_lines_outside_code(content: str):
    """Итерировать строки markdown вне code blocks. Yields (index, stripped_line)."""
    in_code = False
    for i, line in enumerate(content.split("\n")):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            yield i, stripped


def extract_headings(content: str, level: int) -> list[str]:
    """Извлечь заголовки указанного уровня из markdown (вне code blocks)."""
    prefix = "#" * level
    pattern = re.compile(rf"^{prefix}\s+(.+)$")
    return [
        m.group(1).strip()
        for _, line in iter_lines_outside_code(content)
        if (m := pattern.match(line))
    ]


def extract_h2_sections(content: str) -> list[str]:
    """Извлечь все заголовки ## из markdown (вне code blocks)."""
    return extract_headings(content, 2)


def extract_h3_sections(content: str) -> list[str]:
    """Извлечь все заголовки ### из markdown (вне code blocks)."""
    return extract_headings(content, 3)


def extract_h4_sections(content: str) -> list[str]:
    """Извлечь все заголовки #### из markdown (вне code blocks)."""
    return extract_headings(content, 4)


def extract_section_content(content: str, section_name: str) -> str:
    """Извлечь содержимое секции ## до следующей секции ##."""
    pattern = rf"^##\s+{re.escape(section_name)}\s*$"
    lines = content.split("\n")
    start = None
    end = None

    for i, stripped in iter_lines_outside_code(content):
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


def has_toc(content: str) -> bool:
    """Проверить наличие оглавления (## Оглавление) в документе."""
    h2 = extract_h2_sections(content)
    return "Оглавление" in h2


def check_planned_changes_structure(content: str) -> tuple[bool, list[str]]:
    """Проверить структуру Planned Changes: блоки Design с ADDED/MODIFIED/REMOVED.

    Returns:
        (has_blocks, issues): has_blocks — найдены ли блоки Design, issues — список проблем.
    """
    pc_content = extract_section_content(content, "Planned Changes")
    if not pc_content.strip():
        return False, []

    # Если пустая секция — допустимо для полного документа
    if "*Нет активных Design.*" in pc_content:
        return False, []

    # Ищем h3 блоки (design-NNNN: ...)
    h3_in_pc = []
    h4_in_pc = []
    for _, line in iter_lines_outside_code(pc_content):
        h3_match = re.match(r"^###\s+(.+)$", line)
        if h3_match:
            h3_in_pc.append(h3_match.group(1).strip())
        h4_match = re.match(r"^####\s+(.+)$", line)
        if h4_match:
            h4_in_pc.append(h4_match.group(1).strip())

    if not h3_in_pc:
        return False, ["нет блоков Design (h3)"]

    issues = []
    required_h4 = {"ADDED", "MODIFIED", "REMOVED"}
    found_h4 = {h.strip() for h in h4_in_pc}
    missing = required_h4 - found_h4
    if missing:
        issues.append(f"отсутствуют подсекции: {', '.join(sorted(missing))}")

    return True, issues


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

    # SVC015: оглавление
    if not has_toc(content):
        errors.append(f"[SVC015] {rel}: отсутствует оглавление (## Оглавление)")
    elif verbose:
        print(f"    оглавление ✓")

    # SVC006 + SVC007: обязательные секции и порядок
    h2 = extract_h2_sections(content)
    # Исключаем "Оглавление" из проверки порядка 8 секций
    h2_without_toc = [h for h in h2 if h != "Оглавление"]
    found_order = []

    for section in REQUIRED_SECTIONS:
        if section not in h2_without_toc:
            errors.append(f"[SVC006] {rel}: отсутствует секция '{section}'")
        else:
            found_order.append(h2_without_toc.index(section))
            if verbose:
                print(f"    секция: {section} ✓")

    if len(found_order) == len(REQUIRED_SECTIONS) and found_order != sorted(found_order):
        errors.append(f"[SVC007] {rel}: порядок секций нарушен")

    # --- Режим заглушки ---
    if is_stub:
        # AS IS секции (1-6) должны быть пусты
        for section in AS_IS_SECTIONS:
            sec_content = extract_section_content(content, section).strip()
            if not sec_content:
                continue
            # Проверяем что содержимое — один из допустимых placeholder'ов
            is_empty_marker = any(marker in sec_content for marker in STUB_EMPTY_MARKERS)
            if not is_empty_marker:
                errors.append(
                    f"[SVC004] {rel}: AS IS секция '{section}' содержит данные в заглушке. "
                    f"Данные должны быть в Planned Changes → ADDED, а не в AS IS"
                )
            elif verbose:
                print(f"    AS IS '{section}': пусто ✓")

        # SVC016: Planned Changes должны содержать блоки Design с ADDED/MODIFIED/REMOVED
        has_blocks, pc_issues = check_planned_changes_structure(content)
        if not has_blocks:
            pc_content = extract_section_content(content, "Planned Changes").strip()
            if pc_content and "*Нет активных Design.*" not in pc_content:
                errors.append(
                    f"[SVC016] {rel}: Planned Changes в заглушке должны содержать "
                    f"блоки Design с ADDED/MODIFIED/REMOVED"
                )
        elif pc_issues:
            for issue in pc_issues:
                errors.append(f"[SVC016] {rel}: Planned Changes: {issue}")
        elif verbose:
            print(f"    Planned Changes: структура ✓")

        # Changelog в заглушке = *Нет записей.*
        changelog_content = extract_section_content(content, "Changelog").strip()
        if changelog_content and "*Нет записей.*" not in changelog_content:
            errors.append(f"[SVC014] {rel}: Changelog в заглушке должен быть '*Нет записей.*'")
        elif verbose:
            print(f"    Changelog: заглушка ✓")

    # --- Полный режим ---
    if not is_stub:
        # AS IS секции не должны содержать stub placeholder'ы
        for section in AS_IS_SECTIONS:
            sec_content = extract_section_content(content, section).strip()
            for marker in STUB_EMPTY_MARKERS:
                if sec_content == marker:
                    errors.append(
                        f"[SVC008] {rel}: AS IS секция '{section}' содержит placeholder "
                        f"'{marker}' в полном документе"
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

        # SVC016: Planned Changes структура (полный режим — допустимо *Нет активных Design.*)
        has_blocks, pc_issues = check_planned_changes_structure(content)
        if has_blocks and pc_issues:
            for issue in pc_issues:
                errors.append(f"[SVC016] {rel}: Planned Changes: {issue}")
        elif verbose:
            if has_blocks:
                print(f"    Planned Changes: структура ✓")
            else:
                print(f"    Planned Changes: нет активных Design ✓")

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
    """Точка входа: парсинг аргументов и запуск валидации сервисных документов."""
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
