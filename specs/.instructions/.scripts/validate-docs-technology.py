#!/usr/bin/env python3
"""
validate-docs-technology.py — Валидация формата specs/docs/.technologies/standard-{tech}.md.

Проверяет каждый standard-*.md файл (кроме standard-example.md) в
specs/docs/.technologies/ на соответствие standard-technology.md:
frontmatter, заголовок с версией, 8 обязательных секций в правильном порядке,
таблицы, подсекции Паттерны кода и Тестирование, stub-текст, code-блоки.

Использование:
    python validate-docs-technology.py [--json] [--repo <dir>]
    python validate-docs-technology.py path1.md path2.md

Примеры:
    python validate-docs-technology.py
    python validate-docs-technology.py --json
    python validate-docs-technology.py specs/docs/.technologies/standard-postgresql.md

Возвращает:
    0 — валидация пройдена (все файлы корректны)
    1 — есть ошибки
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

TECH_DIR = "specs/docs/.technologies"

REQUIRED_SECTIONS = [
    "Версия и настройка",
    "Конвенции именования",
    "Паттерны кода",
    "Антипаттерны",
    "Структура файлов",
    "Валидация",
    "Тестирование",
    "Логирование",
]

# Секции, которые НЕ допускают stub (у любой технологии есть)
NO_STUB_SECTIONS = {"Версия и настройка", "Конвенции именования"}

# Обязательные колонки в таблицах
TABLE_COLUMNS = {
    "Версия и настройка": ["Параметр", "Значение"],
    "Конвенции именования": ["Объект", "Конвенция", "Пример"],
    "Антипаттерны": ["Антипаттерн", "Почему плохо", "Правильно"],
    "Логирование": ["Событие", "Уровень", "Пример сообщения"],
}

# Обязательные строки в таблице "Версия и настройка"
VERSION_TABLE_ROWS = ["Версия", "Ключевые библиотеки", "Конфигурация"]

# Обязательные подсекции Тестирования
TESTING_SUBSECTIONS = [
    "Фреймворк и плагины",
    "Фикстуры",
    "Мокирование",
    "Паттерны тестов",
]

# Секции, где code-блок обязателен (если не stub)
CODE_BLOCK_REQUIRED = {
    "Структура файлов",
    "Логирование",
}

EXPECTED_STANDARD = "specs/.instructions/docs/technology/standard-technology.md"
KEBAB_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
FILENAME_PATTERN = re.compile(r"^standard-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)\.md$")
SECURITY_FILENAME_PATTERN = re.compile(r"^security-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)\.md$")
H1_VERSION_PATTERN = re.compile(r"^#\s+Стандарт\s+.+\s+v(\d+\.\d+)\s*$")

SECURITY_REQUIRED_SECTIONS = [
    "Инструменты",
    "Dependency Audit",
    "SAST",
    "CI Integration",
    "Known Exceptions",
]

ERROR_CODES = {
    "TECH001": "Отсутствует или некорректный frontmatter",
    "TECH002": "Некорректный заголовок h1 или формат версии",
    "TECH003": "Отсутствует обязательная секция",
    "TECH004": "Секции в неправильном порядке",
    "TECH005": "Таблица не содержит обязательных колонок",
    "TECH006": "Отсутствует обязательная подсекция Паттерны кода",
    "TECH007": "Отсутствует обязательная подсекция Тестирование",
    "TECH008": "Пустая секция без stub-текста",
    "TECH009": "Code-блок отсутствует в секции, где обязателен",
    "TECH-SEC001": "security-{tech}.md: frontmatter не содержит type: security",
    "TECH-SEC002": "security-{tech}.md: не содержит 5 обязательных h2-секций",
    "TECH-SEC003": "security-{tech}.md: неправильное именование файла",
}


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


def parse_frontmatter(content: str) -> dict | None:
    """Извлечь frontmatter из markdown."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    result = {}
    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def get_h2_sections(content: str) -> list[str]:
    """Извлечь все h2-секции из markdown (вне code-блоков)."""
    sections = []
    in_code = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            match = re.match(r"^##\s+(.+)$", stripped)
            if match:
                sections.append(match.group(1).strip())
    return sections


def get_h3_sections_in(section_text: str) -> list[str]:
    """Извлечь все h3-подсекции из текста секции (вне code-блоков)."""
    sections = []
    in_code = False
    for line in section_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            match = re.match(r"^###\s+(.+)$", stripped)
            if match:
                sections.append(match.group(1).strip())
    return sections


def get_section_content(content: str, section_name: str) -> str:
    """Извлечь содержимое h2-секции (от ## до следующего ## или конца)."""
    pattern = rf"^## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    if not match:
        return ""
    return match.group(1)


def extract_table_header(section_text: str) -> list[str]:
    """Извлечь заголовки колонок из первой таблицы в тексте."""
    for line in section_text.strip().split("\n"):
        stripped = line.strip()
        if stripped.startswith("|") and "---" not in stripped:
            cols = [c.strip() for c in stripped.strip().strip("|").split("|")]
            return cols
    return []


def is_stub(section_text: str) -> bool:
    """Проверить, является ли секция stub-текстом (курсив)."""
    stripped = section_text.strip()
    if not stripped:
        return False
    lines = [line.strip() for line in stripped.split("\n") if line.strip()]
    if len(lines) == 1 and lines[0].startswith("*") and lines[0].endswith("*"):
        return True
    return False


def has_code_block(text: str) -> bool:
    """Проверить наличие code-блока в тексте."""
    return "```" in text


def has_content(section_text: str) -> bool:
    """Проверить, содержит ли секция таблицы, code-блоки, h3 или обычный текст."""
    stripped = section_text.strip()
    has_table = "|" in stripped and "---" in stripped
    has_h3 = "### " in stripped
    has_code = "```" in stripped
    # Обычный текст (не HTML-комментарий, не пустые строки)
    text_lines = [
        line for line in stripped.split("\n")
        if line.strip()
        and not line.strip().startswith("<!--")
        and not line.strip().startswith("-->")
        and not line.strip().startswith("---")
    ]
    return has_table or has_h3 or has_code or len(text_lines) > 0


# =============================================================================
# Валидация
# =============================================================================

def validate_frontmatter(content: str, filename: str) -> list[tuple[str, str]]:
    """TECH001: Проверка frontmatter."""
    errors = []
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(("TECH001", "Frontmatter отсутствует"))
        return errors

    # description
    desc = fm.get("description", "")
    if not desc:
        errors.append(("TECH001", "Frontmatter: отсутствует поле description"))
    elif not desc.startswith("Стандарт кодирования"):
        errors.append(("TECH001", f"Frontmatter: description не начинается с 'Стандарт кодирования'"))

    # standard
    standard = fm.get("standard", "")
    if not standard:
        errors.append(("TECH001", "Frontmatter: отсутствует поле standard"))
    elif standard != EXPECTED_STANDARD:
        errors.append(("TECH001", f"Frontmatter: standard = '{standard}', ожидается '{EXPECTED_STANDARD}'"))

    # technology
    tech = fm.get("technology", "")
    if not tech:
        errors.append(("TECH001", "Frontmatter: отсутствует поле technology"))
    elif not KEBAB_PATTERN.match(tech):
        errors.append(("TECH001", f"Frontmatter: technology '{tech}' не в kebab-case"))
    else:
        # Должно совпадать с {tech} из имени файла
        name_match = FILENAME_PATTERN.match(filename)
        if name_match and name_match.group(1) != tech:
            errors.append(("TECH001", f"Frontmatter: technology '{tech}' не совпадает с именем файла '{name_match.group(1)}'"))

    # standard-version НЕ должен присутствовать
    if "standard-version" in fm:
        errors.append(("TECH001", "Frontmatter: поле standard-version не должно присутствовать (версия — в заголовке h1)"))

    return errors


def validate_h1_version(content: str) -> list[tuple[str, str]]:
    """TECH002: Проверка заголовка h1 с версией."""
    errors = []
    h1_match = re.search(r"^# .+$", content, re.MULTILINE)
    if not h1_match:
        errors.append(("TECH002", "Отсутствует заголовок h1"))
        return errors

    h1_line = h1_match.group(0)
    if not H1_VERSION_PATTERN.match(h1_line):
        errors.append(("TECH002", f"Заголовок h1 не соответствует формату '# Стандарт {{Technology}} v{{X.Y}}': {h1_line}"))

    return errors


def validate_sections(content: str) -> list[tuple[str, str]]:
    """TECH003, TECH004: Проверка обязательных секций и порядка."""
    errors = []
    sections = get_h2_sections(content)

    # TECH003: Check presence
    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(("TECH003", f"Отсутствует секция: ## {required}"))

    # TECH004: Check order
    found_order = [s for s in sections if s in REQUIRED_SECTIONS]
    expected_order = [s for s in REQUIRED_SECTIONS if s in found_order]
    if found_order != expected_order:
        errors.append(("TECH004", f"Секции в неправильном порядке. Ожидается: {', '.join(REQUIRED_SECTIONS)}"))

    # TECH004: No extra h2 sections
    extra = [s for s in sections if s not in REQUIRED_SECTIONS]
    if extra:
        errors.append(("TECH004", f"Дополнительные h2-секции не допускаются: {', '.join(extra)}"))

    return errors


def validate_tables(content: str) -> list[tuple[str, str]]:
    """TECH005: Проверка таблиц с обязательными колонками."""
    errors = []

    for section_name, expected_cols in TABLE_COLUMNS.items():
        section_text = get_section_content(content, section_name)
        if not section_text or is_stub(section_text):
            continue

        # Для Логирования — ищем первую таблицу в основном тексте (до code-блока)
        if section_name == "Логирование":
            # Берём текст до первого ```
            text_before_code = section_text.split("```")[0] if "```" in section_text else section_text
            header = extract_table_header(text_before_code)
        elif section_name == "Тестирование → Фреймворк и плагины":
            continue  # Handled in validate_testing_subsections
        else:
            header = extract_table_header(section_text)

        if not header:
            errors.append(("TECH005", f"{section_name}: таблица не найдена"))
            continue

        for col in expected_cols:
            if col not in header:
                errors.append(("TECH005", f"{section_name}: отсутствует колонка «{col}»"))

    # Проверить обязательные строки в "Версия и настройка"
    version_text = get_section_content(content, "Версия и настройка")
    if version_text and not is_stub(version_text):
        for row_name in VERSION_TABLE_ROWS:
            if row_name not in version_text:
                errors.append(("TECH005", f"Версия и настройка: отсутствует строка «{row_name}»"))

    # Проверить таблицу в Тестирование → Фреймворк и плагины
    testing_text = get_section_content(content, "Тестирование")
    if testing_text and not is_stub(testing_text):
        # Найти подсекцию "Фреймворк и плагины"
        fw_pattern = r"^### Фреймворк и плагины\s*\n(.*?)(?=\n### |\n## |\Z)"
        fw_match = re.search(fw_pattern, testing_text, re.DOTALL | re.MULTILINE)
        if fw_match:
            fw_text = fw_match.group(1)
            header = extract_table_header(fw_text)
            if header:
                for col in ["Компонент", "Пакет", "Назначение"]:
                    if col not in header:
                        errors.append(("TECH005", f"Тестирование → Фреймворк и плагины: отсутствует колонка «{col}»"))

    return errors


def validate_patterns_subsections(content: str) -> list[tuple[str, str]]:
    """TECH006: Проверка подсекций Паттерны кода."""
    errors = []
    section_text = get_section_content(content, "Паттерны кода")
    if not section_text or is_stub(section_text):
        return errors

    h3_sections = get_h3_sections_in(section_text)
    if not h3_sections:
        errors.append(("TECH006", "Паттерны кода: нет ни одной h3-подсекции"))
        return errors

    # Каждая h3-подсекция должна содержать code-блок
    for h3_name in h3_sections:
        h3_pattern = rf"^### {re.escape(h3_name)}\s*\n(.*?)(?=\n### |\n## |\Z)"
        h3_match = re.search(h3_pattern, section_text, re.DOTALL | re.MULTILINE)
        if h3_match and not has_code_block(h3_match.group(1)):
            errors.append(("TECH006", f"Паттерны кода → {h3_name}: отсутствует code-блок"))

    return errors


def validate_testing_subsections(content: str) -> list[tuple[str, str]]:
    """TECH007: Проверка подсекций Тестирование."""
    errors = []
    section_text = get_section_content(content, "Тестирование")
    if not section_text or is_stub(section_text):
        return errors

    h3_sections = get_h3_sections_in(section_text)

    for required_sub in TESTING_SUBSECTIONS:
        if required_sub not in h3_sections:
            errors.append(("TECH007", f"Тестирование: отсутствует подсекция «{required_sub}»"))
        else:
            # Подсекции Фикстуры, Мокирование, Паттерны тестов — должны иметь code-блок
            if required_sub != "Фреймворк и плагины":
                sub_pattern = rf"^### {re.escape(required_sub)}\s*\n(.*?)(?=\n### |\n## |\Z)"
                sub_match = re.search(sub_pattern, section_text, re.DOTALL | re.MULTILINE)
                if sub_match and not has_code_block(sub_match.group(1)):
                    errors.append(("TECH007", f"Тестирование → {required_sub}: отсутствует code-блок"))

    return errors


def validate_stub_text(content: str) -> list[tuple[str, str]]:
    """TECH008: Проверка пустых секций на наличие stub-текста."""
    errors = []

    for section_name in REQUIRED_SECTIONS:
        section_text = get_section_content(content, section_name)
        if not section_text:
            continue

        stripped = section_text.strip()
        if not stripped:
            if section_name in NO_STUB_SECTIONS:
                errors.append(("TECH008", f"Секция «{section_name}» пуста — stub не допускается, заполнить обязательно"))
            else:
                errors.append(("TECH008", f"Секция «{section_name}» пуста: нужно содержание или stub-текст"))
            continue

        # Если не stub и нет реального контента
        if not has_content(stripped) and not is_stub(stripped):
            errors.append(("TECH008", f"Секция «{section_name}» не содержит ни контента, ни stub-текста"))

    return errors


def validate_code_blocks(content: str) -> list[tuple[str, str]]:
    """TECH009: Проверка наличия code-блоков в обязательных секциях."""
    errors = []

    for section_name in CODE_BLOCK_REQUIRED:
        section_text = get_section_content(content, section_name)
        if not section_text or is_stub(section_text):
            continue
        if not has_code_block(section_text):
            errors.append(("TECH009", f"Секция «{section_name}»: отсутствует обязательный code-блок"))

    # Логирование — проверяем code-блок для настройки логгера
    log_text = get_section_content(content, "Логирование")
    if log_text and not is_stub(log_text):
        if not has_code_block(log_text):
            errors.append(("TECH009", "Секция «Логирование»: отсутствует code-блок настройки логгера"))

    return errors


# =============================================================================
# Валидация security-{tech}.md
# =============================================================================

def validate_security_file(file_path: Path) -> list[tuple[str, str]]:
    """Валидировать один security-{tech}.md файл. Возвращает список ошибок."""
    errors = []
    content = file_path.read_text(encoding="utf-8")

    # TECH-SEC003: Проверка именования файла
    if not SECURITY_FILENAME_PATTERN.match(file_path.name):
        errors.append(("TECH-SEC003", f"Файл '{file_path.name}' не соответствует паттерну security-{{tech}}.md"))

    # TECH-SEC001: Frontmatter с type: security
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(("TECH-SEC001", "Frontmatter отсутствует"))
    else:
        file_type = fm.get("type", "")
        if file_type != "security":
            errors.append(("TECH-SEC001", f"Frontmatter: type = '{file_type}', ожидается 'security'"))

        # Проверить technology поле
        tech = fm.get("technology", "")
        if not tech:
            errors.append(("TECH-SEC001", "Frontmatter: отсутствует поле technology"))
        elif not KEBAB_PATTERN.match(tech):
            errors.append(("TECH-SEC001", f"Frontmatter: technology '{tech}' не в kebab-case"))
        else:
            name_match = SECURITY_FILENAME_PATTERN.match(file_path.name)
            if name_match and name_match.group(1) != tech:
                errors.append(("TECH-SEC001", f"Frontmatter: technology '{tech}' не совпадает с именем файла '{name_match.group(1)}'"))

    # TECH-SEC002: 5 обязательных h2-секций
    sections = get_h2_sections(content)
    for required in SECURITY_REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(("TECH-SEC002", f"Отсутствует секция: ## {required}"))

    return errors


# =============================================================================
# Поиск файлов
# =============================================================================

def find_tech_files(repo_root: Path) -> list[Path]:
    """Найти все standard-{tech}.md файлы в specs/docs/.technologies/."""
    tech_dir = repo_root / TECH_DIR
    if not tech_dir.is_dir():
        return []

    files = []
    for item in sorted(tech_dir.iterdir()):
        if (
            item.is_file()
            and item.suffix == ".md"
            and item.name.startswith("standard-")
            and item.name != "standard-example.md"
        ):
            files.append(item)
    return files


def find_security_files(repo_root: Path) -> list[Path]:
    """Найти все security-{tech}.md файлы в specs/docs/.technologies/."""
    tech_dir = repo_root / TECH_DIR
    if not tech_dir.is_dir():
        return []

    files = []
    for item in sorted(tech_dir.iterdir()):
        if (
            item.is_file()
            and item.suffix == ".md"
            and item.name.startswith("security-")
        ):
            files.append(item)
    return files


# =============================================================================
# Main
# =============================================================================

def validate_file(file_path: Path) -> list[tuple[str, str]]:
    """Валидировать один standard-{tech}.md файл. Возвращает список ошибок."""
    content = file_path.read_text(encoding="utf-8")

    all_errors = []
    all_errors.extend(validate_frontmatter(content, file_path.name))
    all_errors.extend(validate_h1_version(content))
    all_errors.extend(validate_sections(content))
    all_errors.extend(validate_tables(content))
    all_errors.extend(validate_patterns_subsections(content))
    all_errors.extend(validate_testing_subsections(content))
    all_errors.extend(validate_stub_text(content))
    all_errors.extend(validate_code_blocks(content))

    return all_errors


def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация specs/docs/.technologies/standard-{tech}.md (TECH001-TECH009) и security-{tech}.md (TECH-SEC001-003)"
    )
    parser.add_argument(
        "path",
        nargs="*",
        help="Пути к файлам (если указаны — проверяются только они, иначе все specs/docs/.technologies/standard-*.md)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()
    repo_root = find_repo_root(Path(args.repo))

    # Determine files to validate
    standard_files = []
    security_files = []

    if args.path:
        for p in args.path:
            fp = Path(p)
            if not fp.is_absolute():
                fp = repo_root / fp
            if fp.is_file() and fp.suffix == ".md":
                try:
                    rel = fp.relative_to(repo_root / TECH_DIR)
                    if "/" not in str(rel).replace("\\", "/"):
                        if rel.name.startswith("standard-") and rel.name != "standard-example.md":
                            standard_files.append(fp)
                        elif rel.name.startswith("security-"):
                            security_files.append(fp)
                except ValueError:
                    pass
        if not standard_files and not security_files:
            if args.json:
                print(json.dumps({"files": [], "errors": [], "valid": True}, ensure_ascii=False, indent=2))
            else:
                print("✅ technology — нет файлов для проверки")
            sys.exit(0)
    else:
        standard_files = find_tech_files(repo_root)
        security_files = find_security_files(repo_root)
        if not standard_files and not security_files:
            if args.json:
                print(json.dumps({"files": [], "errors": [], "valid": True}, ensure_ascii=False, indent=2))
            else:
                print("✅ technology — нет файлов для проверки")
            sys.exit(0)

    # Validate all files
    all_results = []
    total_errors = 0

    for file_path in standard_files:
        rel_path = file_path.relative_to(repo_root)
        errors = validate_file(file_path)
        total_errors += len(errors)
        all_results.append({
            "file": str(rel_path).replace("\\", "/"),
            "errors": [{"code": code, "message": msg} for code, msg in errors],
            "valid": len(errors) == 0,
        })

    for file_path in security_files:
        rel_path = file_path.relative_to(repo_root)
        errors = validate_security_file(file_path)
        total_errors += len(errors)
        all_results.append({
            "file": str(rel_path).replace("\\", "/"),
            "errors": [{"code": code, "message": msg} for code, msg in errors],
            "valid": len(errors) == 0,
        })

    has_errors = total_errors > 0

    # Output
    if args.json:
        result = {
            "files": all_results,
            "total_errors": total_errors,
            "valid": not has_errors,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for r in all_results:
            if r["valid"]:
                print(f"✅ {r['file']} — валидация пройдена")
            else:
                print(f"❌ {r['file']} — {len(r['errors'])} ошибок:")
                for err in r["errors"]:
                    print(f"   {err['code']}: {err['message']}")

        if has_errors:
            print(f"\nИтого: {total_errors} ошибок в {sum(1 for r in all_results if not r['valid'])} файлах")
        else:
            print(f"\n✅ Все {len(all_results)} файлов прошли валидацию")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
