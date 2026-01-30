#!/usr/bin/env python3
"""
validate-agent.py — Валидация конфигурации агента.

Использование:
    python validate-agent.py <agent.yaml>
    python validate-agent.py .claude/agents/

Примеры:
    python validate-agent.py .claude/agents/todo-finder.yaml
    python validate-agent.py .claude/agents/
    python validate-agent.py --all

Проверки:
    - YAML-синтаксис
    - Обязательные поля (name, description, type, prompt)
    - Именование (kebab-case, латиница)
    - Тип агента (explore, bash, plan, general-purpose)
    - Структура промпта (роль, ограничения, формат вывода)
    - Безопасность (уровни доступа, запрещённые операции)

Возвращает:
    0 — все проверки пройдены
    1 — есть ошибки
"""

import argparse
import re
import sys
from pathlib import Path

# =============================================================================
# Константы
# =============================================================================

ERROR_CODES = {
    "A001": "Невалидный YAML-синтаксис",
    "A002": "Отсутствует обязательное поле",
    "A003": "Неверный тип агента",
    "A004": "Неверное именование",
    "A005": "Имя файла не соответствует полю name",
    "A006": "Пустой промпт",
    "A007": "В промпте нет секции 'Ограничения'",
    "A008": "В промпте нет секции 'Формат вывода'",
    "A009": "Небезопасный уровень доступа",
    "A010": "Разрешены запрещённые операции",
    "A011": "В промпте нет секции 'Роль' или 'Задача'",
    "A012": "Скиллы указаны для не-general-purpose агента",
}

VALID_TYPES = {"explore", "bash", "plan", "general-purpose"}
KEBAB_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
FORBIDDEN_OPERATIONS = {"delete", "rm", "rm -rf", "git push", "git reset"}


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


def add_error(errors: list, code: str, detail: str = "") -> None:
    """Добавить ошибку с кодом из ERROR_CODES."""
    message = ERROR_CODES.get(code, code)
    if detail:
        errors.append(f"{code}: {message}: {detail}")
    else:
        errors.append(f"{code}: {message}")


def add_warning(warnings: list, message: str) -> None:
    """Добавить предупреждение."""
    warnings.append(f"WARNING: {message}")


# =============================================================================
# Валидация
# =============================================================================

def validate_yaml_syntax(file_path: Path) -> tuple[dict | None, list]:
    """Проверить YAML-синтаксис и вернуть данные."""
    errors = []
    try:
        import yaml
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data, errors
    except ImportError:
        # Fallback без yaml библиотеки
        errors.append("WARNING: PyYAML не установлен, пропуск проверки синтаксиса")
        return None, errors
    except Exception as e:
        add_error(errors, "A001", str(e))
        return None, errors


def validate_required_fields(data: dict) -> list:
    """Проверить наличие обязательных полей."""
    errors = []
    required = ["name", "description", "type", "prompt"]

    for field in required:
        if field not in data or not data[field]:
            add_error(errors, "A002", f"'{field}'")

    return errors


def validate_naming(data: dict, file_path: Path) -> list:
    """Проверить именование агента."""
    errors = []
    name = data.get("name", "")

    if name:
        # Проверить kebab-case
        if not KEBAB_CASE_PATTERN.match(name):
            add_error(errors, "A004", f"'{name}' не соответствует kebab-case")

        # Проверить соответствие имени файла
        expected_filename = f"{name}.yaml"
        if file_path.name != expected_filename:
            add_error(errors, "A005", f"файл '{file_path.name}', ожидается '{expected_filename}'")

        # Проверить префикс agent-
        if name.startswith("agent-"):
            add_error(errors, "A004", f"'{name}' не должен начинаться с 'agent-'")

    return errors


def validate_type(data: dict) -> list:
    """Проверить тип агента."""
    errors = []
    agent_type = data.get("type", "")

    if agent_type and agent_type not in VALID_TYPES:
        add_error(errors, "A003", f"'{agent_type}', допустимые: {', '.join(VALID_TYPES)}")

    # Проверить skills для не-general-purpose
    if agent_type != "general-purpose" and data.get("skills"):
        add_error(errors, "A012", f"тип '{agent_type}'")

    return errors


def validate_prompt(data: dict) -> tuple[list, list]:
    """Проверить структуру промпта."""
    errors = []
    warnings = []
    prompt = data.get("prompt", "")

    if not prompt or not prompt.strip():
        add_error(errors, "A006")
        return errors, warnings

    prompt_lower = prompt.lower()

    # Проверить наличие роли или задачи
    has_role = "## роль" in prompt_lower or "## role" in prompt_lower
    has_task = "## задача" in prompt_lower or "## task" in prompt_lower
    if not has_role and not has_task:
        add_error(errors, "A011")

    # Проверить ограничения
    has_constraints = (
        "## ограничения" in prompt_lower or
        "## constraints" in prompt_lower or
        "запрещено" in prompt_lower or
        "не должен" in prompt_lower
    )
    if not has_constraints:
        add_error(errors, "A007")

    # Проверить формат вывода
    has_output = (
        "## формат вывода" in prompt_lower or
        "## output" in prompt_lower or
        "## format" in prompt_lower
    )
    if not has_output:
        add_error(errors, "A008")

    return errors, warnings


def validate_security(data: dict) -> list:
    """Проверить настройки безопасности."""
    errors = []
    settings = data.get("settings", {})

    if not settings:
        return errors

    # Проверить уровень доступа
    access_level = settings.get("access_level", "")
    if access_level == "full":
        add_error(errors, "A009", "full доступ запрещён для агентов")

    # Проверить запрещённые операции
    allowed_ops = settings.get("allowed_operations", [])
    if allowed_ops:
        for op in allowed_ops:
            if op.lower() in FORBIDDEN_OPERATIONS:
                add_error(errors, "A010", f"'{op}'")

    return errors


def validate_agent(file_path: Path) -> dict:
    """Валидировать один файл агента."""
    result = {
        "file": str(file_path),
        "errors": [],
        "warnings": [],
        "valid": False,
    }

    # Проверить расширение
    if file_path.suffix != ".yaml":
        result["errors"].append(f"Неверное расширение: {file_path.suffix}, ожидается .yaml")
        return result

    # Проверить YAML
    data, yaml_errors = validate_yaml_syntax(file_path)
    result["errors"].extend(yaml_errors)

    if data is None:
        return result

    # Все остальные проверки
    result["errors"].extend(validate_required_fields(data))
    result["errors"].extend(validate_naming(data, file_path))
    result["errors"].extend(validate_type(data))

    prompt_errors, prompt_warnings = validate_prompt(data)
    result["errors"].extend(prompt_errors)
    result["warnings"].extend(prompt_warnings)

    result["errors"].extend(validate_security(data))

    result["valid"] = len(result["errors"]) == 0
    return result


def validate_directory(dir_path: Path) -> list[dict]:
    """Валидировать все агенты в директории."""
    results = []

    for yaml_file in dir_path.glob("*.yaml"):
        results.append(validate_agent(yaml_file))

    return results


# =============================================================================
# Main
# =============================================================================

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация конфигурации агента"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Путь к .yaml файлу или директории с агентами"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Проверить все агенты в .claude/agents/"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Определить что валидировать
    if args.all:
        target = repo_root / ".claude" / "agents"
    elif args.path:
        target = Path(args.path)
        if not target.is_absolute():
            target = repo_root / target
    else:
        target = repo_root / ".claude" / "agents"

    if not target.exists():
        print(f"Путь не существует: {target}")
        sys.exit(1)

    # Валидация
    if target.is_file():
        results = [validate_agent(target)]
    else:
        results = validate_directory(target)

    if not results:
        print(f"Агенты не найдены в {target}")
        sys.exit(0)

    # Вывод результатов
    has_errors = False

    for result in results:
        file_name = Path(result["file"]).name

        if result["valid"]:
            print(f"✅ {file_name}")
        else:
            has_errors = True
            error_count = len(result["errors"])
            print(f"❌ {file_name} — {error_count} ошибок:")
            for error in result["errors"]:
                print(f"   {error}")

        for warning in result["warnings"]:
            print(f"   {warning}")

    # Итог
    valid_count = sum(1 for r in results if r["valid"])
    total_count = len(results)

    if total_count > 1:
        print(f"\nИтого: {valid_count}/{total_count} агентов валидны")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
