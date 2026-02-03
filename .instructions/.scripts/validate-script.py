#!/usr/bin/env python3
"""
validate-script.py — Валидация формата скриптов.

Проверяет соответствие скрипта стандарту standard-script.md.

Использование:
    python validate-script.py <path>... [--json] [--all] [--principles] [--repo <dir>]

Примеры:
    python validate-script.py .instructions/.scripts/parse-docstrings.py
    python validate-script.py file1.py file2.py file3.py
    python validate-script.py --all
    python validate-script.py --json --principles path/to/script.py

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

VALID_SHEBANG = "#!/usr/bin/env python3"

FORBIDDEN_IMPORTS = {
    "pandas", "numpy", "requests", "click", "typer",
    "flask", "django", "fastapi", "sqlalchemy"
}

ERROR_CODES = {
    # Структура (S0xx)
    "S001": "Отсутствует shebang",
    "S002": "Неверный shebang",
    "S003": "Неверное расположение (не в .scripts/)",
    "S010": "Отсутствует docstring",
    "S011": "Отсутствует первая строка описания",
    "S012": "Неверный формат первой строки",
    "S013": "Отсутствует секция Использование",
    "S014": "Отсутствует секция Примеры",
    "S015": "Отсутствует секция Возвращает",
    "S020": "Отсутствует if __name__",
    "S021": "Отсутствует функция main()",
    "S030": "Отсутствует UTF-8 настройка для Windows",
    "S031": "Отсутствует sys.exit()",
    "S032": "Отсутствует ERROR_CODES (обязательно для validate-*.py)",
    # Принципы (P0xx)
    "P001": "Переусложнённый код (KISS)",
    "P002": "Дублирование кода (DRY)",
    "P003": "Неиспользуемый код (YAGNI)",
    "P004": "Тяжёлая зависимость",
    "P005": "Bare except без типа исключения",
    "P006": "Функция без docstring",
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
# Проверки структуры (S0xx)
# =============================================================================

def check_location(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Проверить расположение скрипта в папке .scripts/."""
    errors = []

    try:
        rel_path = path.resolve().relative_to(repo_root)
        parts = rel_path.parts
        if ".scripts" not in parts:
            errors.append(("S003", "Файл не в папке .scripts/"))
    except ValueError:
        errors.append(("S003", "Не удалось определить расположение"))

    return errors


def check_shebang(content: str) -> list[tuple[str, str]]:
    """Проверить shebang."""
    errors = []
    lines = content.split('\n')

    if not lines:
        errors.append(("S001", "Файл пустой"))
        return errors

    first_line = lines[0].strip()

    if not first_line.startswith("#!"):
        errors.append(("S001", "Отсутствует shebang"))
    elif first_line != VALID_SHEBANG:
        errors.append(("S002", f"Ожидается '{VALID_SHEBANG}', найдено '{first_line}'"))

    return errors


def check_docstring(content: str, filename: str) -> list[tuple[str, str]]:
    """Проверить docstring модуля."""
    errors = []

    # Найти docstring
    match = re.search(r'^"""(.*?)"""', content, re.DOTALL | re.MULTILINE)
    if not match:
        match = re.search(r"^'''(.*?)'''", content, re.DOTALL | re.MULTILINE)

    if not match:
        errors.append(("S010", "Отсутствует docstring модуля"))
        return errors

    docstring = match.group(1)

    # S011, S012: первая строка
    first_line = docstring.strip().split('\n')[0]
    expected_pattern = f"{filename} —"

    if not first_line:
        errors.append(("S011", "Отсутствует первая строка описания"))
    elif not first_line.startswith(expected_pattern):
        errors.append(("S012", f"Ожидается '{expected_pattern} ...', найдено '{first_line[:50]}...'"))

    # S013: Использование
    if "Использование:" not in docstring:
        errors.append(("S013", "Отсутствует секция Использование"))

    # S014: Примеры
    if "Примеры:" not in docstring and "Пример:" not in docstring:
        errors.append(("S014", "Отсутствует секция Примеры"))

    # S015: Возвращает
    if "Возвращает:" not in docstring:
        errors.append(("S015", "Отсутствует секция Возвращает"))

    return errors


def check_code_structure(content: str, filename: str) -> list[tuple[str, str]]:
    """Проверить структуру кода."""
    errors = []

    # S020: if __name__
    if 'if __name__' not in content:
        errors.append(("S020", "Отсутствует блок if __name__ == \"__main__\""))

    # S021: main()
    if 'def main(' not in content and 'def main()' not in content:
        errors.append(("S021", "Отсутствует функция main()"))

    # S030: UTF-8 для Windows
    if 'reconfigure(encoding' not in content and 'sys.platform' not in content:
        errors.append(("S030", "Отсутствует UTF-8 настройка для Windows"))

    # S031: sys.exit()
    if 'sys.exit(' not in content:
        errors.append(("S031", "Отсутствует sys.exit() для кода возврата"))

    # S032: ERROR_CODES для validate-*.py
    if filename.startswith("validate-") and filename.endswith(".py"):
        if 'ERROR_CODES' not in content:
            errors.append(("S032", "Отсутствует ERROR_CODES (обязательно для validate-*.py)"))

    return errors


# =============================================================================
# Проверки принципов (P0xx)
# =============================================================================

# Импортируем check_principles из validate-principles.py (DRY)
# Если импорт не удался — используем локальную версию
try:
    from importlib.util import spec_from_file_location, module_from_spec
    _spec = spec_from_file_location(
        "validate_principles",
        Path(__file__).parent / "validate-principles.py"
    )
    _module = module_from_spec(_spec)
    _spec.loader.exec_module(_module)
    _check_principles_impl = _module.check_principles
except Exception:
    _check_principles_impl = None


def check_principles(content: str, _path: Path) -> list[tuple[str, str]]:
    """Проверить соблюдение принципов программирования."""
    if _check_principles_impl:
        return _check_principles_impl(content)

    # Fallback: базовые проверки если импорт не удался
    errors = []

    # P001: KISS — вложенные lambda
    for i, line in enumerate(content.split('\n'), 1):
        if line.strip().startswith('#'):
            continue
        if line.count('lambda ') >= 2:
            errors.append(("P001", f"Вложенные lambda в строке {i}"))

    # P004: Тяжёлые зависимости
    for forbidden in FORBIDDEN_IMPORTS:
        if re.search(rf'^import {forbidden}|^from {forbidden}', content, re.MULTILINE):
            errors.append(("P004", f"Тяжёлая зависимость: {forbidden}"))

    # P005: Bare except
    for i, line in enumerate(content.split('\n'), 1):
        if re.match(r'^\s*except\s*:\s*(#.*)?$', line):
            errors.append(("P005", f"Bare except в строке {i}"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_script(path: Path, repo_root: Path, check_principles_flag: bool) -> list[tuple[str, str]]:
    """Валидировать один скрипт."""
    errors = []

    if not path.exists():
        return [("S001", f"Файл не найден: {path}")]

    if path.suffix != ".py":
        return [("S001", f"Неверное расширение: {path.suffix}")]

    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [("S001", f"Ошибка чтения файла: {e}")]

    # Проверка расположения
    errors.extend(check_location(path, repo_root))

    # Проверки структуры
    errors.extend(check_shebang(content))
    errors.extend(check_docstring(content, path.name))
    errors.extend(check_code_structure(content, path.name))

    # Проверки принципов (опционально)
    if check_principles_flag:
        errors.extend(check_principles(content, path))

    return errors


def find_all_scripts(repo_root: Path) -> list[Path]:
    """Найти все скрипты в папках .scripts/."""
    scripts = []
    for scripts_dir in repo_root.rglob(".scripts"):
        if scripts_dir.is_dir():
            for py_file in scripts_dir.glob("*.py"):
                scripts.append(py_file)
    return sorted(scripts)


def format_output(path: Path, errors: list[tuple[str, str]], as_json: bool) -> str:
    """Форматировать вывод."""
    if as_json:
        return json.dumps({
            "file": str(path),
            "valid": len(errors) == 0,
            "errors": [{"code": code, "message": msg} for code, msg in errors]
        }, ensure_ascii=False, indent=2)

    if not errors:
        return f"✅ {path.name} — валидация пройдена"

    lines = [f"❌ {path.name} — {len(errors)} ошибок:"]
    for code, msg in errors:
        lines.append(f"   {code}: {msg}")
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
        description="Валидация формата скриптов"
    )
    parser.add_argument("path", nargs="*", help="Путь к скрипту (можно несколько)")
    parser.add_argument("--all", action="store_true", help="Проверить все скрипты")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--principles", action="store_true", help="Проверять принципы (KISS, DRY, etc.)")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if args.all:
        scripts = find_all_scripts(repo_root)
        if not scripts:
            print("Скрипты не найдены")
            sys.exit(1)
    elif args.path:
        scripts = [Path(p) for p in args.path]
    else:
        parser.print_help()
        sys.exit(2)

    all_valid = True
    results = []

    for path in scripts:
        errors = validate_script(path, repo_root, args.principles)
        if errors:
            all_valid = False

        output = format_output(path, errors, args.json)
        results.append(output)

    if args.json:
        print("[" + ",\n".join(results) + "]")
    else:
        print("\n".join(results))

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
