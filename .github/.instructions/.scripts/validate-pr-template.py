#!/usr/bin/env python3
"""
validate-pr-template.py — Валидация структуры PR template.

Проверяет соответствие .github/PULL_REQUEST_TEMPLATE.md стандарту.

Использование:
    python validate-pr-template.py [path] [--json]

Примеры:
    python validate-pr-template.py
    python validate-pr-template.py .github/PULL_REQUEST_TEMPLATE.md
    python validate-pr-template.py --json

Возвращает:
    0 — валидация пройдена
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

DEFAULT_TEMPLATE_PATH = ".github/PULL_REQUEST_TEMPLATE.md"

REQUIRED_SECTIONS = ["Summary", "Changes", "Test plan", "Related issues"]
OPTIONAL_SECTIONS = ["Breaking changes", "Notes"]

ERROR_CODES = {
    "PRT001": "Отсутствует обязательная секция",
    "PRT002": "Неверный уровень заголовка (должен быть ##)",
    "PRT003": "Пустая опциональная секция (заполнить или удалить)",
    "PRT004": "Неверный формат чек-листа (должен быть '- [ ]')",
    "PRT005": "Неверный формат placeholder (должен быть '[...]')",
    "PRT006": "Файл не найден",
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


# =============================================================================
# Валидация
# =============================================================================

def extract_sections(content: str) -> dict[str, tuple[int, str]]:
    """Извлечь секции из markdown.

    Returns:
        dict: {название секции: (номер строки, содержимое секции)}
    """
    sections = {}
    lines = content.split("\n")
    current_section = None
    current_content = []
    current_line = 0

    for i, line in enumerate(lines, 1):
        # Проверка на заголовок секции (## Name)
        match = re.match(r"^##\s+(.+)$", line)
        if match:
            # Сохранить предыдущую секцию
            if current_section:
                sections[current_section] = (current_line, "\n".join(current_content).strip())

            current_section = match.group(1).strip()
            current_content = []
            current_line = i
        elif current_section:
            current_content.append(line)

    # Сохранить последнюю секцию
    if current_section:
        sections[current_section] = (current_line, "\n".join(current_content).strip())

    return sections


def validate_template(file_path: Path) -> list[tuple[str, str, int | None]]:
    """Валидация PR template.

    Returns:
        list: [(код ошибки, сообщение, номер строки или None)]
    """
    errors = []

    # PRT006: Файл существует
    if not file_path.exists():
        errors.append(("PRT006", f"Файл не найден: {file_path}", None))
        return errors

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    sections = extract_sections(content)

    # PRT001: Обязательные секции
    for section in REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(("PRT001", f"Отсутствует секция: ## {section}", None))

    # PRT002: Проверка уровней заголовков (не должно быть # или ###)
    for i, line in enumerate(lines, 1):
        # Одиночный # (не ##)
        if re.match(r"^#\s+[^#]", line):
            errors.append(("PRT002", f"Заголовок уровня # (должен быть ##): {line.strip()}", i))
        # Тройной ###
        if re.match(r"^###\s+", line):
            errors.append(("PRT002", f"Заголовок уровня ### (должен быть ##): {line.strip()}", i))

    # PRT003: Пустые опциональные секции
    # В шаблоне placeholder допустим. Ошибка только если секция совсем пустая.
    for section in OPTIONAL_SECTIONS:
        if section in sections:
            line_num, section_content = sections[section]
            # Секция считается пустой, если нет текста (только пробелы/переносы)
            if not section_content.strip():
                errors.append(("PRT003", f"Пустая секция: ## {section}", line_num))

    # PRT004: Формат чек-листов
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Неправильные форматы чек-листов
        if re.match(r"^-\s*\[\]", stripped):  # - [] (без пробела)
            errors.append(("PRT004", f"Неверный формат: '{stripped}' (должен быть '- [ ]')", i))
        if re.match(r"^\*\s*\[\s*\]", stripped):  # * [ ] (звёздочка вместо дефиса)
            errors.append(("PRT004", f"Неверный формат: '{stripped}' (должен быть '- [ ]')", i))

    # PRT005: Формат placeholder (проверяем наличие <> или {} вместо [])
    for i, line in enumerate(lines, 1):
        # Placeholder в угловых скобках <...>
        if re.search(r"<[A-Za-zА-Яа-я][^>]*>", line) and not line.strip().startswith("```"):
            # Исключаем HTML теги и код
            if not re.search(r"<(br|hr|img|a|p|div|span|code|pre)\s*/?>", line, re.IGNORECASE):
                errors.append(("PRT005", f"Placeholder в <>: '{line.strip()[:50]}...' (должен быть [...])", i))
        # Placeholder в фигурных скобках {...}
        if re.search(r"\{[A-Za-zА-Яа-я][^}]*\}", line) and not line.strip().startswith("```"):
            errors.append(("PRT005", f"Placeholder в {{}}: '{line.strip()[:50]}...' (должен быть [...])", i))

    return errors


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация структуры PR template"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help=f"Путь к файлу (по умолчанию: {DEFAULT_TEMPLATE_PATH})"
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

    # Определить путь к файлу
    if args.path:
        file_path = Path(args.path)
        if not file_path.is_absolute():
            file_path = repo_root / file_path
    else:
        file_path = repo_root / DEFAULT_TEMPLATE_PATH

    # Валидация
    errors = validate_template(file_path)

    # Вывод результатов
    if args.json:
        result = {
            "file": str(file_path.relative_to(repo_root)),
            "errors": [
                {"code": code, "message": msg, "line": line}
                for code, msg, line in errors
            ],
            "valid": len(errors) == 0
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if errors:
            print(f"❌ {file_path.name} — {len(errors)} ошибок:")
            for code, msg, line in errors:
                line_info = f" (строка {line})" if line else ""
                print(f"   {code}: {msg}{line_info}")
        else:
            print(f"✅ {file_path.name} — валидация пройдена")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
