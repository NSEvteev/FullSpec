#!/usr/bin/env python3
"""
validate-codeowners.py — Валидация синтаксиса и структуры CODEOWNERS.

Проверяет соответствие .github/CODEOWNERS стандарту.

Использование:
    python validate-codeowners.py [path] [--json]

Примеры:
    python validate-codeowners.py
    python validate-codeowners.py .github/CODEOWNERS
    python validate-codeowners.py --json

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

DEFAULT_CODEOWNERS_PATH = ".github/CODEOWNERS"

ERROR_CODES = {
    "CO001": "Файл не найден",
    "CO002": "Неверное расположение (должен быть в .github/)",
    "CO003": "Невалидный синтаксис строки",
    "CO004": "Inline-комментарий (# после владельца)",
    "CO005": "Пользователь не найден (проверьте username)",
    "CO006": "Команда не найдена (проверьте org/team)",
    "CO007": "Нет глобального владельца (* @owner)",
    "CO008": "Невалидный glob-паттерн",
}

# Паттерн для валидной строки CODEOWNERS
# pattern @owner1 @owner2 ...
VALID_LINE_PATTERN = re.compile(
    r'^'
    r'(?P<pattern>[^\s@#]+)'  # Паттерн (не содержит пробелов, @ и #)
    r'\s+'                     # Пробел(ы)
    r'(?P<owners>@[\w\-/]+(?:\s+@[\w\-/]+)*)'  # Один или более @owner
    r'$'
)

# Паттерн для владельца
OWNER_PATTERN = re.compile(r'^@[\w\-]+(/[\w\-]+)?$')

# Паттерн для inline-комментария
INLINE_COMMENT_PATTERN = re.compile(r'@[\w\-/]+.*#')


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

def validate_line(line: str, line_num: int) -> list[tuple[str, str, int]]:
    """Валидация одной строки CODEOWNERS.

    Returns:
        list: [(код ошибки, сообщение, номер строки)]
    """
    errors = []
    stripped = line.strip()

    # Пустая строка или комментарий — OK
    if not stripped or stripped.startswith('#'):
        return errors

    # CO004: Inline-комментарий
    if INLINE_COMMENT_PATTERN.search(stripped):
        errors.append(("CO004", f"Inline-комментарий: '{stripped[:50]}...'", line_num))
        return errors

    # CO003: Проверка формата строки
    match = VALID_LINE_PATTERN.match(stripped)
    if not match:
        errors.append(("CO003", f"Невалидный синтаксис: '{stripped[:50]}...'", line_num))
        return errors

    # Проверка владельцев
    owners_str = match.group('owners')
    owners = owners_str.split()

    for owner in owners:
        if not OWNER_PATTERN.match(owner):
            errors.append(("CO003", f"Невалидный владелец: '{owner}'", line_num))

    # CO008: Проверка паттерна (базовая)
    pattern = match.group('pattern')
    if not is_valid_glob_pattern(pattern):
        errors.append(("CO008", f"Невалидный паттерн: '{pattern}'", line_num))

    return errors


def is_valid_glob_pattern(pattern: str) -> bool:
    """Проверить валидность glob-паттерна.

    Базовая проверка — допустимые символы.
    """
    # Допустимые символы в glob-паттерне
    # Буквы, цифры, /, *, ?, [], {}, -, _, ., \
    if not re.match(r'^[a-zA-Z0-9/*?\[\]{}\-_.\\]+$', pattern):
        return False

    # Проверка на несбалансированные скобки
    if pattern.count('[') != pattern.count(']'):
        return False
    if pattern.count('{') != pattern.count('}'):
        return False

    return True


def validate_codeowners(file_path: Path, repo_root: Path) -> list[tuple[str, str, int | None]]:
    """Валидация CODEOWNERS файла.

    Returns:
        list: [(код ошибки, сообщение, номер строки или None)]
    """
    errors = []

    # CO001: Файл существует
    if not file_path.exists():
        errors.append(("CO001", f"Файл не найден: {file_path}", None))
        return errors

    # CO002: Расположение
    try:
        rel_path = file_path.relative_to(repo_root)
        # Нормализуем путь для сравнения (Windows использует \)
        rel_path_str = str(rel_path).replace("\\", "/")
        if rel_path_str != ".github/CODEOWNERS":
            errors.append(("CO002", f"Файл в {rel_path_str}, должен быть .github/CODEOWNERS", None))
    except ValueError:
        errors.append(("CO002", "Не удалось определить расположение", None))

    # Чтение содержимого
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Валидация каждой строки
    has_global_owner = False

    for i, line in enumerate(lines, 1):
        line_errors = validate_line(line, i)
        errors.extend(line_errors)

        # Проверка на глобальный владелец
        stripped = line.strip()
        if stripped.startswith('* ') or stripped.startswith('*\t'):
            has_global_owner = True

    # CO007: Глобальный владелец
    if not has_global_owner:
        errors.append(("CO007", "Отсутствует глобальный владелец (* @owner)", None))

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
        description="Валидация синтаксиса и структуры CODEOWNERS"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help=f"Путь к файлу (по умолчанию: {DEFAULT_CODEOWNERS_PATH})"
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
        file_path = repo_root / DEFAULT_CODEOWNERS_PATH

    # Валидация
    errors = validate_codeowners(file_path, repo_root)

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
            print(f"❌ CODEOWNERS — {len(errors)} ошибок:")
            for code, msg, line in errors:
                line_info = f" (строка {line})" if line else ""
                print(f"   {code}: {msg}{line_info}")
        else:
            print(f"✅ CODEOWNERS — валидация пройдена")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
