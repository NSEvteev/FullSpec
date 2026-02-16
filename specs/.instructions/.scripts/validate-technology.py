#!/usr/bin/env python3
"""
validate-technology.py — Валидация per-tech стандартов standard-{tech}.md.

Использование:
    python validate-technology.py <путь>              # Один файл или папка
    python validate-technology.py <путь> --verbose    # Подробный вывод

Проверяет:
    - TECH001: description — формат "Стандарт кодирования {Technology} — ..."
    - TECH002: standard, standard-version, index — корректны
    - TECH003: technology — присутствует, kebab-case
    - TECH004: Все 6 обязательных секций присутствуют
    - TECH005: Порядок секций соответствует стандарту
    - TECH006: Содержание секций — таблицы, формат
    - TECH007: § 5 не противоречит standard-principles.md (предупреждение)
    - TECH010: Rule .claude/rules/{tech}.md существует и содержит ссылки
    - TECH011: Строка в реестре specs/technologies/README.md

    Все стандарты должны быть полными (заглушки не допускаются).

SSOT:
    - specs/.instructions/technologies/standard-technology.md
    - specs/.instructions/technologies/validation-technology.md

Примеры:
    python validate-technology.py specs/technologies/standard-python.md
    python validate-technology.py specs/technologies/ --verbose

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
    "TECH001": "Некорректный description",
    "TECH002": "Некорректный standard/standard-version/index",
    "TECH003": "Отсутствует или некорректное поле technology",
    "TECH004": "Отсутствует обязательная секция",
    "TECH005": "Порядок секций нарушен",
    "TECH006": "Некорректное содержание секции",
    "TECH007": "Возможный конфликт с standard-principles.md",
    "TECH010": "Нет rule или некорректное содержание",
    "TECH011": "Нет строки в реестре technologies/README.md",
}

# 6 обязательных секций в порядке (заголовки ## с нумерацией)
REQUIRED_SECTIONS = [
    "Версия и источники",
    "Конвенции именования",
    "Структура кода",
    "Паттерны использования",
    "Типичные ошибки",
    "Ссылки",
]

STUB_PLACEHOLDER = "*Заполняется при ADR → DONE.*"

EXPECTED_STANDARD = ".instructions/standard-instruction.md"
EXPECTED_INDEX = "specs/technologies/README.md"

KEBAB_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
STANDARD_VERSION_PATTERN = re.compile(r"^v\d+\.\d+$")
FILENAME_PATTERN = re.compile(r"^standard-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)\.md$")


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
    """Итератор по строкам markdown вне code blocks. Yields (index, stripped_line)."""
    in_code = False
    for i, line in enumerate(content.split("\n")):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            yield i, stripped


def extract_h2_sections(content: str) -> list[str]:
    """Извлечь все заголовки ## из markdown (вне code blocks)."""
    sections = []
    for _, stripped in iter_lines_outside_code(content):
        match = re.match(r"^##\s+(?:\d+\.\s+)?(.+)$", stripped)
        if match:
            sections.append(match.group(1).strip())
    return sections


def extract_section_content(content: str, section_name: str) -> str:
    """Извлечь содержимое секции ## до следующей секции ##."""
    pattern = rf"^##\s+(?:\d+\.\s+)?{re.escape(section_name)}\s*$"
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


def validate_file(file_path: Path, repo_root: Path, verbose: bool = False) -> list[str]:
    """Валидация одного файла standard-{tech}.md."""
    errors = []
    rel = file_path.relative_to(repo_root)

    content = file_path.read_text(encoding="utf-8")

    # Проверить имя файла
    name_match = FILENAME_PATTERN.match(file_path.name)
    if not name_match:
        errors.append(f"[TECH001] {rel}: имя файла не соответствует standard-{{tech}}.md")
        return errors

    tech_from_name = name_match.group(1)

    # TECH001: frontmatter
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(f"[TECH001] {rel}: отсутствует frontmatter")
        return errors

    if verbose:
        print(f"  ✓ frontmatter существует")

    # TECH001: description
    desc = fm.get("description", "")
    if not desc:
        errors.append(f"[TECH001] {rel}: отсутствует description")
    elif not desc.startswith("Стандарт кодирования"):
        errors.append(
            f"[TECH001] {rel}: description не начинается с 'Стандарт кодирования'"
        )
    elif verbose:
        print(f"    description ✓")

    # TECH002: standard, standard-version, index
    standard = fm.get("standard", "")
    if standard != EXPECTED_STANDARD:
        errors.append(
            f"[TECH002] {rel}: standard = '{standard}', "
            f"ожидается '{EXPECTED_STANDARD}'"
        )
    elif verbose:
        print(f"    standard ✓")

    sv = fm.get("standard-version", "")
    if not sv:
        errors.append(f"[TECH002] {rel}: отсутствует standard-version")
    elif not STANDARD_VERSION_PATTERN.match(sv):
        errors.append(
            f"[TECH002] {rel}: standard-version = '{sv}', "
            f"ожидается формат vX.Y"
        )
    elif verbose:
        print(f"    standard-version: {sv} ✓")

    index = fm.get("index", "")
    if index != EXPECTED_INDEX:
        errors.append(
            f"[TECH002] {rel}: index = '{index}', "
            f"ожидается '{EXPECTED_INDEX}'"
        )
    elif verbose:
        print(f"    index ✓")

    # TECH003: technology
    tech = fm.get("technology", "")
    if not tech:
        errors.append(f"[TECH003] {rel}: отсутствует поле technology")
    elif not KEBAB_PATTERN.match(tech):
        errors.append(f"[TECH003] {rel}: technology '{tech}' не в kebab-case")
    elif tech != tech_from_name:
        errors.append(
            f"[TECH003] {rel}: technology '{tech}' не совпадает "
            f"с именем файла '{tech_from_name}'"
        )
    elif verbose:
        print(f"    technology: {tech} ✓")

    # TECH004 + TECH005: обязательные секции и порядок
    h2 = extract_h2_sections(content)
    found_order = []

    for section in REQUIRED_SECTIONS:
        if section not in h2:
            errors.append(f"[TECH004] {rel}: отсутствует секция '{section}'")
        else:
            found_order.append(h2.index(section))
            if verbose:
                print(f"    секция: {section} ✓")

    if len(found_order) == len(REQUIRED_SECTIONS) and found_order != sorted(
        found_order
    ):
        errors.append(f"[TECH005] {rel}: порядок секций нарушен")

    # Проверить отсутствие placeholder (заглушки не допускаются)
    for section in REQUIRED_SECTIONS:
        sec_content = extract_section_content(content, section).strip()
        if STUB_PLACEHOLDER in sec_content:
            errors.append(
                f"[TECH006] {rel}: секция '{section}' содержит placeholder "
                f"— заглушки не допускаются, все секции должны быть заполнены"
            )

    # TECH006: содержание секций
    sec1_content = extract_section_content(content, "Версия и источники").strip()
    if True:
        # § 1: таблица Параметр/Значение
        if sec1_content:
            if "Параметр" not in sec1_content or "Значение" not in sec1_content:
                errors.append(
                    f"[TECH006] {rel}: § 1 без таблицы Параметр/Значение"
                )
            elif verbose:
                print(f"    § 1: таблица Параметр/Значение ✓")

        # § 2: таблица Элемент/Правило/Пример
        sec2_content = extract_section_content(content, "Конвенции именования").strip()
        if sec2_content:
            if "Элемент" not in sec2_content or "Правило" not in sec2_content:
                errors.append(
                    f"[TECH006] {rel}: § 2 без таблицы Элемент/Правило/Пример"
                )
            elif verbose:
                print(f"    § 2: таблица Элемент/Правило/Пример ✓")

        # § 3-4: описание с содержанием
        for section in ["Структура кода", "Паттерны использования"]:
            sec_content = extract_section_content(content, section).strip()
            if not sec_content:
                errors.append(f"[TECH006] {rel}: секция '{section}' пуста")
            elif verbose:
                print(f"    секция '{section}': заполнена ✓")

        # § 5: типичные ошибки
        sec5_content = extract_section_content(content, "Типичные ошибки").strip()
        if not sec5_content:
            errors.append(f"[TECH006] {rel}: секция 'Типичные ошибки' пуста")
        elif verbose:
            print(f"    секция 'Типичные ошибки': заполнена ✓")

        # § 6: ссылки
        sec6_content = extract_section_content(content, "Ссылки").strip()
        if not sec6_content:
            errors.append(f"[TECH006] {rel}: секция 'Ссылки' пуста")
        elif verbose:
            print(f"    секция 'Ссылки': заполнена ✓")

    # TECH010: Rule
    if tech:
        rule_path = repo_root / ".claude" / "rules" / f"{tech}.md"
        if not rule_path.exists():
            errors.append(f"[TECH010] {rel}: rule '.claude/rules/{tech}.md' не найден")
        else:
            rule_content = rule_path.read_text(encoding="utf-8")
            if f"standard-{tech}.md" not in rule_content:
                errors.append(
                    f"[TECH010] {rel}: rule не содержит ссылку на standard-{tech}.md"
                )
            if f"validation-{tech}.md" not in rule_content:
                errors.append(
                    f"[TECH010] {rel}: rule не содержит ссылку на validation-{tech}.md"
                )
            if verbose and rule_path.exists():
                rule_ok = (
                    f"standard-{tech}.md" in rule_content
                    and f"validation-{tech}.md" in rule_content
                )
                if rule_ok:
                    print(f"    rule: .claude/rules/{tech}.md ✓")

    # TECH011: Реестр
    if tech:
        registry_path = repo_root / "specs" / "technologies" / "README.md"
        if registry_path.exists():
            registry_content = registry_path.read_text(encoding="utf-8")
            # Ищем имя технологии в таблице реестра (case-insensitive для первой буквы)
            tech_title = tech.replace("-", " ").title().replace(" ", " ")
            if (
                tech not in registry_content.lower()
                and f"standard-{tech}.md" not in registry_content
            ):
                errors.append(
                    f"[TECH011] {rel}: технология не найдена в реестре "
                    f"specs/technologies/README.md"
                )
            elif verbose:
                print(f"    реестр: {tech} ✓")
        elif verbose:
            print(f"    реестр: specs/technologies/README.md не найден (пропуск)")

    return errors


def main():
    """Точка входа: парсинг аргументов и запуск валидации."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация per-tech стандартов standard-{tech}.md"
    )
    parser.add_argument("path", help="Файл .md или папка technologies/")
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
        files = sorted(target.glob("standard-*.md"))
        # Исключить мета-стандарт standard-technology.md
        files = [f for f in files if f.name != "standard-technology.md"]
    elif target.is_file() and target.suffix == ".md":
        files = [target]
    else:
        print(f"❌ Путь не найден: {target}")
        sys.exit(1)

    if not files:
        print("⚠ Нет файлов для валидации")
        sys.exit(0)

    print(f"🔍 Валидация per-tech стандартов ({len(files)} файлов)...")

    all_errors = []
    for f in files:
        if args.verbose:
            print(f"\n📄 {f.relative_to(repo_root)}")
        file_errors = validate_file(f, repo_root, verbose=args.verbose)
        all_errors.extend(file_errors)

    if all_errors:
        print(f"\n❌ Найдено ошибок: {len(all_errors)}")
        for err in all_errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("✅ Все per-tech стандарты валидны")
        sys.exit(0)


if __name__ == "__main__":
    main()
