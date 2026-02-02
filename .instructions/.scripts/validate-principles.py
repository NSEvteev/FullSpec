#!/usr/bin/env python3
"""
validate-principles.py — Валидация принципов программирования в Python-коде.

Проверяет соблюдение принципов KISS, DRY, YAGNI и других в любых .py файлах проекта.
В отличие от validate-script.py, не требует расположения в .scripts/ и не проверяет
структуру скрипта (shebang, docstring модуля, main()).

Использование:
    python validate-principles.py <path> [--all] [--json] [--repo <dir>]

Примеры:
    python validate-principles.py src/api/handlers.py
    python validate-principles.py src/ --all
    python validate-principles.py --all --json

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import ast
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

FORBIDDEN_IMPORTS = {
    "pandas", "numpy", "requests", "click", "typer",
    "flask", "django", "fastapi", "sqlalchemy"
}

ERROR_CODES = {
    "P001": "Переусложнённый код (KISS)",
    "P002": "Дублирование кода (DRY)",
    "P003": "Неиспользуемый код (YAGNI)",
    "P004": "Тяжёлая зависимость",
    "P005": "Bare except без типа исключения",
    "P006": "Функция без docstring",
    "P007": "Неочевидное поведение (ручная проверка)",
    "P008": "Модуль делает много (ручная проверка)",
}

# Папки, которые исключаются из проверки
EXCLUDED_DIRS = {
    "node_modules", ".git", ".idea", ".vscode", "dist", "build",
    "__pycache__", ".pytest_cache", ".mypy_cache", "venv", ".venv", "env",
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


def should_skip_path(path: Path) -> bool:
    """Проверить, нужно ли пропустить путь."""
    for part in path.parts:
        if part in EXCLUDED_DIRS:
            return True
    return False


# =============================================================================
# Проверки принципов (P0xx)
# =============================================================================

def check_kiss(content: str) -> list[tuple[str, str]]:
    """Проверить KISS — вложенные lambda и длинные цепочки."""
    errors = []

    for i, line in enumerate(content.split('\n'), 1):
        stripped = line.strip()

        # Пропускаем комментарии
        if stripped.startswith('#'):
            continue

        # Пропускаем строки (могут содержать примеры кода)
        if '"""' in line or "'''" in line:
            continue

        # Пропускаем строки со строковыми литералами, содержащими паттерны
        if "'.map(" in line or '".map(' in line:
            continue
        if "'.filter(" in line or '".filter(' in line:
            continue

        # Вложенные lambda: два или более lambda в одной строке
        if line.count('lambda ') >= 2:
            errors.append(("P001", f"Вложенные lambda в строке {i}"))

        # Длинные цепочки map/filter (реальные вызовы)
        if '.map(' in line and '.filter(' in line:
            errors.append(("P001", f"Длинные цепочки map/filter в строке {i}"))

    return errors


def check_imports(content: str) -> list[tuple[str, str]]:
    """Проверить тяжёлые зависимости."""
    errors = []

    for forbidden in FORBIDDEN_IMPORTS:
        if re.search(rf'^import {forbidden}\b|^from {forbidden}\b', content, re.MULTILINE):
            errors.append(("P004", f"Тяжёлая зависимость: {forbidden}"))

    return errors


def check_bare_except(content: str) -> list[tuple[str, str]]:
    """Проверить bare except без типа исключения."""
    errors = []

    for i, line in enumerate(content.split('\n'), 1):
        stripped = line.strip()

        # Пропускаем комментарии и строки
        if stripped.startswith('#'):
            continue
        if stripped.startswith('"') or stripped.startswith("'"):
            continue

        # Ищем except: без типа
        if re.match(r'^\s*except\s*:\s*(#.*)?$', line):
            errors.append(("P005", f"Bare except без типа в строке {i}"))

    return errors


def parse_functions(content: str) -> list[ast.FunctionDef]:
    """Извлечь все функции из Python кода."""
    try:
        tree = ast.parse(content)
        return [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    except SyntaxError:
        return []


def check_docstrings(content: str) -> list[tuple[str, str]]:
    """Проверить наличие docstring у функций."""
    errors = []
    for node in parse_functions(content):
        # Пропускаем приватные методы и __dunder__
        if node.name.startswith('_'):
            continue
        if not ast.get_docstring(node):
            errors.append(("P006", f"Функция {node.name}() без docstring"))
    return errors


def check_yagni(content: str) -> list[tuple[str, str]]:
    """Проверить YAGNI — неиспользуемые аргументы и переменные."""
    errors = []
    for node in parse_functions(content):
        # Собираем имена аргументов
        arg_names = {arg.arg for arg in node.args.args if arg.arg not in ('self', 'cls')}

        # Собираем все используемые имена в теле функции
        used_names = {child.id for child in ast.walk(node) if isinstance(child, ast.Name)}

        # Находим неиспользуемые аргументы (без _ префикса)
        for arg in arg_names - used_names:
            if not arg.startswith('_'):
                errors.append(("P003", f"Неиспользуемый аргумент '{arg}' в {node.name}()"))
    return errors


def check_dry(content: str) -> list[tuple[str, str]]:
    """Проверить DRY — дублирование блоков кода."""
    errors = []
    lines = content.split('\n')

    # Ищем повторяющиеся блоки из 5+ строк
    block_size = 5
    seen_blocks = {}

    for i in range(len(lines) - block_size + 1):
        # Пропускаем пустые строки и комментарии
        block_lines = []
        for j in range(i, min(i + block_size + 2, len(lines))):
            line = lines[j].strip()
            if line and not line.startswith('#'):
                block_lines.append(line)
            if len(block_lines) >= block_size:
                break

        if len(block_lines) < block_size:
            continue

        block = '\n'.join(block_lines[:block_size])

        # Пропускаем тривиальные блоки (только импорты, пустые строки)
        if all(l.startswith('import ') or l.startswith('from ') for l in block_lines[:block_size]):
            continue

        if block in seen_blocks:
            first_line = seen_blocks[block]
            if abs(i - first_line) > block_size:  # Не соседние блоки
                errors.append(("P002", f"Дублирование кода: строки {first_line + 1} и {i + 1}"))
        else:
            seen_blocks[block] = i

    return errors


def check_principles(content: str) -> list[tuple[str, str]]:
    """Проверить все принципы программирования."""
    errors = []

    errors.extend(check_kiss(content))       # P001
    errors.extend(check_dry(content))        # P002
    errors.extend(check_yagni(content))      # P003
    errors.extend(check_imports(content))    # P004
    errors.extend(check_bare_except(content))  # P005
    errors.extend(check_docstrings(content))   # P006
    # P007, P008 — требуют ручной проверки

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_file(path: Path) -> list[tuple[str, str]]:
    """Валидировать один файл."""
    if not path.exists():
        return [("P000", f"Файл не найден: {path}")]

    if path.suffix != ".py":
        return [("P000", f"Неверное расширение: {path.suffix}")]

    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding='cp1251')
        except Exception as e:
            return [("P000", f"Ошибка чтения файла: {e}")]
    except Exception as e:
        return [("P000", f"Ошибка чтения файла: {e}")]

    return check_principles(content)


def find_python_files(path: Path) -> list[Path]:
    """Найти все Python файлы в директории."""
    files = []

    if path.is_file():
        if path.suffix == ".py" and not should_skip_path(path):
            files.append(path)
    elif path.is_dir():
        for py_file in path.rglob("*.py"):
            if not should_skip_path(py_file):
                files.append(py_file)

    return sorted(files)


def format_output(path: Path, errors: list[tuple[str, str]], as_json: bool) -> str:
    """Форматировать вывод."""
    if as_json:
        return json.dumps({
            "file": str(path),
            "valid": len(errors) == 0,
            "errors": [{"code": code, "message": msg} for code, msg in errors]
        }, ensure_ascii=False, indent=2)

    if not errors:
        return f"  {path.name}"

    lines = [f"  {path.name} — {len(errors)} ошибок:"]
    for code, msg in errors:
        lines.append(f"     {code}: {msg}")
    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация принципов программирования в Python-коде"
    )
    parser.add_argument("path", nargs="?", help="Путь к файлу или директории")
    parser.add_argument("--all", action="store_true", help="Проверить все .py файлы в репозитории")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if args.all:
        files = find_python_files(repo_root)
    elif args.path:
        target = Path(args.path)
        if not target.is_absolute():
            target = repo_root / target
        files = find_python_files(target)
    else:
        parser.print_help()
        sys.exit(2)

    if not files:
        print("Python файлы не найдены")
        sys.exit(1)

    all_valid = True
    results = []
    valid_count = 0
    error_count = 0

    for path in files:
        errors = validate_file(path)
        if errors:
            all_valid = False
            error_count += 1
        else:
            valid_count += 1

        if args.json or errors:  # В текстовом режиме показываем только ошибки
            output = format_output(path, errors, args.json)
            results.append(output)

    if args.json:
        print("[" + ",\n".join(results) + "]")
    else:
        if all_valid:
            print(f"✅ Все файлы ({valid_count}) соответствуют принципам")
        else:
            print(f"❌ Найдены нарушения принципов ({error_count} файлов):\n")
            print("\n".join(results))
            print(f"\n✅ Файлов без нарушений: {valid_count}")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
