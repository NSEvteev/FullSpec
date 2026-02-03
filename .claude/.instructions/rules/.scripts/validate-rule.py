#!/usr/bin/env python3
"""
validate-rule.py — Валидация формата rule-файлов.

Проверяет соответствие rule стандарту standard-rule.md.

Использование:
    python validate-rule.py <name-or-path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-rule.py ssot
    python validate-rule.py .claude/rules/core.md
    python validate-rule.py --all
    python validate-rule.py --json ssot

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

ERROR_CODES = {
    "R001": "Неверное расположение (не в /.claude/rules/)",
    "R002": "Неверное расширение (не .md)",
    "R010": "Невалидный frontmatter",
    "R011": "Отсутствует description",
    "R012": "Отсутствует standard",
    "R013": "Отсутствует index",
    "R014": "paths не массив строк",
    "R015": "Невалидный glob-паттерн в paths",
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


def parse_frontmatter(content: str) -> dict:
    """Извлечь frontmatter из markdown."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    result = {}
    current_key = None
    current_value = []

    for line in match.group(1).split('\n'):
        # Проверка на новый ключ
        if ':' in line and not line.startswith(' ') and not line.startswith('-'):
            # Сохранить предыдущий ключ
            if current_key:
                result[current_key] = '\n'.join(current_value).strip()

            key, value = line.split(':', 1)
            current_key = key.strip()
            current_value = [value.strip()] if value.strip() else []
        elif current_key:
            # Продолжение значения (массив или многострочное)
            current_value.append(line.strip())

    # Сохранить последний ключ
    if current_key:
        result[current_key] = '\n'.join(current_value).strip()

    return result


def parse_paths_array(value: str) -> list[str] | None:
    """Распарсить массив paths из frontmatter."""
    if not value:
        return None

    # Убрать пробелы и переносы
    value = value.replace('\n', ' ')

    # Паттерн для массива YAML
    # Формат: - "pattern" или - pattern
    patterns = re.findall(r'-\s*["\']?([^"\'\n]+)["\']?', value)

    if patterns:
        return [p.strip() for p in patterns]

    return None


def is_valid_glob(pattern: str) -> bool:
    """Проверить валидность glob-паттерна."""
    # Базовая проверка: glob должен содержать допустимые символы
    # Допустимые: буквы, цифры, /, *, ?, [], {}, -, _, .
    if not re.match(r'^[a-zA-Z0-9/*?\[\]{}\-_.]+$', pattern):
        return False

    # Проверка на базовые ошибки
    if pattern.startswith('/') and not pattern.startswith('/**'):
        # Абсолютные пути не рекомендуются
        return False

    return True


# =============================================================================
# Проверки
# =============================================================================

def check_file(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Проверить файл: расположение, расширение."""
    errors = []

    # R002: расширение
    if path.suffix != ".md":
        errors.append(("R002", f"Расширение {path.suffix}, ожидается .md"))

    # R001: расположение в /.claude/rules/
    try:
        rel_path = path.resolve().relative_to(repo_root)
        expected_dir = Path(".claude") / "rules"

        if rel_path.parent != expected_dir:
            errors.append(("R001", f"Файл в {rel_path.parent}, ожидается /.claude/rules/"))
    except ValueError:
        errors.append(("R001", "Не удалось определить расположение"))

    return errors


def check_frontmatter(content: str) -> list[tuple[str, str]]:
    """Проверить frontmatter."""
    errors = []

    # R010: наличие frontmatter
    if not content.startswith("---\n"):
        errors.append(("R010", "Отсутствует frontmatter"))
        return errors

    fm = parse_frontmatter(content)

    # R011: description
    if not fm.get("description"):
        errors.append(("R011", "Отсутствует поле description"))

    # R012: standard
    if not fm.get("standard"):
        errors.append(("R012", "Отсутствует поле standard"))

    # R013: index
    if not fm.get("index"):
        errors.append(("R013", "Отсутствует поле index"))

    # R014 и R015: paths (опционально)
    if "paths" in fm:
        paths_value = fm.get("paths", "")
        paths = parse_paths_array(paths_value)

        if paths is None:
            errors.append(("R014", "Поле paths указано, но не является массивом строк"))
        else:
            # R015: валидность glob-паттернов
            for pattern in paths:
                if not is_valid_glob(pattern):
                    errors.append(("R015", f"Невалидный glob-паттерн: {pattern}"))

    return errors


def check_structure(content: str) -> list[tuple[str, str]]:
    """Проверить структуру rule."""
    errors = []
    # Проверки структуры отключены (H1 больше не требуется)
    return errors


def validate_rule(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Полная валидация rule."""
    errors = []

    # Проверка файла
    errors.extend(check_file(path, repo_root))

    # Чтение содержимого
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(("R010", f"Ошибка чтения файла: {e}"))
        return errors

    # Проверка frontmatter
    errors.extend(check_frontmatter(content))

    # Проверка структуры
    errors.extend(check_structure(content))

    return errors


# =============================================================================
# Основная логика
# =============================================================================

def validate_single(name_or_path: str, repo_root: Path, json_output: bool = False) -> bool:
    """Валидировать один rule.

    Args:
        name_or_path: Имя rule (без .md) или путь к файлу
        repo_root: Корень репозитория
        json_output: Выводить JSON
    """
    # Определить: путь или имя
    if '/' in name_or_path or '\\' in name_or_path or name_or_path.endswith('.md'):
        # Это путь к файлу
        rule_path = Path(name_or_path)
        if not rule_path.is_absolute():
            rule_path = repo_root / rule_path
        name = rule_path.stem
    else:
        # Это имя rule
        name = name_or_path
        rule_path = repo_root / ".claude" / "rules" / f"{name}.md"

    if not rule_path.exists():
        if json_output:
            print(json.dumps({"file": name, "errors": [{"code": "R001", "message": "Файл не найден"}]}))
        else:
            print(f"❌ {name}.md — файл не найден")
        return False

    errors = validate_rule(rule_path, repo_root)

    if json_output:
        error_list = [{"code": code, "message": msg} for code, msg in errors]
        print(json.dumps({"file": name, "errors": error_list}))
    else:
        if errors:
            print(f"❌ {name}.md — {len(errors)} ошибок:")
            for code, msg in errors:
                print(f"   {code}: {msg}")
        else:
            print(f"✅ {name}.md — валидация пройдена")

    return len(errors) == 0


def validate_all(repo_root: Path, json_output: bool = False) -> bool:
    """Валидировать все rules."""
    rules_dir = repo_root / ".claude" / "rules"

    if not rules_dir.exists():
        if json_output:
            print(json.dumps({"error": "Директория /.claude/rules/ не найдена"}))
        else:
            print("❌ Директория /.claude/rules/ не найдена")
        return False

    rule_files = list(rules_dir.glob("*.md"))

    if not rule_files:
        if json_output:
            print(json.dumps({"message": "Rules не найдены"}))
        else:
            print("ℹ️  Rules не найдены в /.claude/rules/")
        return True

    all_valid = True
    results = []

    for rule_file in rule_files:
        name = rule_file.stem
        errors = validate_rule(rule_file, repo_root)

        if json_output:
            error_list = [{"code": code, "message": msg} for code, msg in errors]
            results.append({"file": name, "errors": error_list})
        else:
            if errors:
                print(f"❌ {name}.md — {len(errors)} ошибок:")
                for code, msg in errors:
                    print(f"   {code}: {msg}")
                all_valid = False
            else:
                print(f"✅ {name}.md")

    if json_output:
        print(json.dumps({"rules": results}))

    return all_valid


def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация формата rule-файлов"
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Имя rule (ssot) или путь к файлу (.claude/rules/core.md)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Валидировать все rules в /.claude/rules/"
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

    if args.all:
        success = validate_all(repo_root, args.json)
    elif args.name:
        success = validate_single(args.name, repo_root, args.json)
    else:
        parser.print_help()
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
