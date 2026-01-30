#!/usr/bin/env python3
"""
validate-agent.py — Валидация конфигурации агента.

Использование:
    python validate-agent.py <agent-folder>
    python validate-agent.py .claude/agents/
    python validate-agent.py --all

Примеры:
    python validate-agent.py .claude/agents/todo-finder
    python validate-agent.py .claude/agents/
    python validate-agent.py --all

Проверки:
    - Структура папки (AGENT.md существует)
    - YAML frontmatter валиден
    - Обязательные поля (name, description)
    - Официальные поля (model, tools, permissionMode)
    - Именование (kebab-case, латиница)
    - Тип агента (explore, bash, plan, general-purpose)
    - Структура промпта (роль, ограничения, формат вывода)
    - Безопасность (permissionMode, disallowedTools)

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
    "A001": "Невалидный YAML frontmatter",
    "A002": "Отсутствует обязательное поле",
    "A003": "Неверный тип агента",
    "A004": "Неверное именование",
    "A005": "Имя папки не соответствует полю name",
    "A006": "Пустой промпт",
    "A007": "В промпте нет секции 'Ограничения'",
    "A008": "В промпте нет секции 'Формат вывода'",
    "A009": "Небезопасный permissionMode",
    "A010": "Неверное значение поля",
    "A011": "В промпте нет секции 'Роль' или 'Задача'",
    "A012": "Скиллы указаны для не-general-purpose агента",
    "A013": "Файл AGENT.md не найден",
    "A014": "Frontmatter не найден",
    "A015": "Неверный инструмент в tools/disallowedTools",
}

VALID_TYPES = {"explore", "bash", "plan", "general-purpose"}
VALID_MODELS = {"haiku", "sonnet", "opus", "inherit"}
VALID_PERMISSION_MODES = {"default", "acceptEdits", "dontAsk", "bypassPermissions", "plan"}
VALID_TOOLS = {"Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebSearch", "WebFetch", "AskUserQuestion"}

KEBAB_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


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
# Парсинг
# =============================================================================

def parse_agent_md(file_path: Path) -> tuple[dict | None, str, list]:
    """Парсить AGENT.md: frontmatter и тело."""
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        add_error(errors, "A001", str(e))
        return None, "", errors

    # Найти frontmatter
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        add_error(errors, "A014")
        return None, "", errors

    frontmatter_text = match.group(1)
    body = content[match.end():].strip()

    # Парсить YAML
    try:
        import yaml
        data = yaml.safe_load(frontmatter_text)
        return data, body, errors
    except ImportError:
        # Fallback без yaml
        errors.append("WARNING: PyYAML не установлен, пропуск проверки синтаксиса")
        return None, body, errors
    except Exception as e:
        add_error(errors, "A001", str(e))
        return None, body, errors


# =============================================================================
# Валидация
# =============================================================================

def validate_required_fields(data: dict) -> list:
    """Проверить наличие обязательных полей."""
    errors = []
    required = ["name", "description"]

    for field in required:
        if field not in data or not data[field]:
            add_error(errors, "A002", f"'{field}'")

    return errors


def validate_naming(data: dict, agent_dir: Path) -> list:
    """Проверить именование агента."""
    errors = []
    name = data.get("name", "")

    if name:
        # Проверить kebab-case
        if not KEBAB_CASE_PATTERN.match(name):
            add_error(errors, "A004", f"'{name}' не соответствует kebab-case")

        # Проверить соответствие имени папки
        if agent_dir.name != name:
            add_error(errors, "A005", f"папка '{agent_dir.name}', поле name '{name}'")

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


def validate_official_fields(data: dict) -> list:
    """Проверить официальные поля Claude Code."""
    errors = []

    # model
    model = data.get("model", "")
    if model and model not in VALID_MODELS:
        add_error(errors, "A010", f"model '{model}', допустимые: {', '.join(VALID_MODELS)}")

    # permissionMode
    perm_mode = data.get("permissionMode", "")
    if perm_mode and perm_mode not in VALID_PERMISSION_MODES:
        add_error(errors, "A010", f"permissionMode '{perm_mode}', допустимые: {', '.join(VALID_PERMISSION_MODES)}")

    # tools
    tools = data.get("tools", "")
    if tools:
        if isinstance(tools, str):
            tool_list = [t.strip() for t in tools.split(",")]
        else:
            tool_list = tools

        for tool in tool_list:
            if tool and tool not in VALID_TOOLS:
                add_error(errors, "A015", f"tools: '{tool}'")

    # disallowedTools
    disallowed = data.get("disallowedTools", "")
    if disallowed:
        if isinstance(disallowed, str):
            tool_list = [t.strip() for t in disallowed.split(",")]
        else:
            tool_list = disallowed

        for tool in tool_list:
            if tool and tool not in VALID_TOOLS:
                add_error(errors, "A015", f"disallowedTools: '{tool}'")

    return errors


def validate_prompt(body: str) -> tuple[list, list]:
    """Проверить структуру промпта (тело AGENT.md)."""
    errors = []
    warnings = []

    if not body or not body.strip():
        add_error(errors, "A006")
        return errors, warnings

    prompt_lower = body.lower()

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

    # Проверить permissionMode
    perm_mode = data.get("permissionMode", "")
    if perm_mode == "bypassPermissions":
        add_error(errors, "A009", "bypassPermissions опасен для кастомных агентов")

    return errors


def validate_agent(agent_dir: Path) -> dict:
    """Валидировать один агент."""
    result = {
        "name": agent_dir.name,
        "path": str(agent_dir),
        "errors": [],
        "warnings": [],
        "valid": False,
    }

    # Проверить AGENT.md
    agent_file = agent_dir / "AGENT.md"
    if not agent_file.exists():
        add_error(result["errors"], "A013")
        return result

    # Парсить файл
    data, body, parse_errors = parse_agent_md(agent_file)
    result["errors"].extend(parse_errors)

    if data is None:
        return result

    # Все проверки
    result["errors"].extend(validate_required_fields(data))
    result["errors"].extend(validate_naming(data, agent_dir))
    result["errors"].extend(validate_type(data))
    result["errors"].extend(validate_official_fields(data))

    prompt_errors, prompt_warnings = validate_prompt(body)
    result["errors"].extend(prompt_errors)
    result["warnings"].extend(prompt_warnings)

    result["errors"].extend(validate_security(data))

    result["valid"] = len(result["errors"]) == 0
    return result


def validate_directory(dir_path: Path) -> list[dict]:
    """Валидировать все агенты в директории."""
    results = []

    for agent_dir in sorted(dir_path.iterdir()):
        # Пропустить файлы и DELETE_ папки
        if not agent_dir.is_dir():
            continue
        if agent_dir.name.startswith("DELETE_"):
            continue
        if agent_dir.name.startswith("."):
            continue

        # Проверить наличие AGENT.md
        agent_file = agent_dir / "AGENT.md"
        if agent_file.exists():
            results.append(validate_agent(agent_dir))

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
        help="Путь к папке агента или директории с агентами"
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
    if target.is_dir():
        # Проверить, это папка агента или папка со всеми агентами
        agent_file = target / "AGENT.md"
        if agent_file.exists():
            # Это папка одного агента
            results = [validate_agent(target)]
        else:
            # Это папка со всеми агентами
            results = validate_directory(target)
    else:
        print(f"Ожидается папка агента: {target}")
        sys.exit(1)

    if not results:
        print(f"Агенты не найдены в {target}")
        sys.exit(0)

    # Вывод результатов
    has_errors = False

    for result in results:
        if result["valid"]:
            print(f"✅ {result['name']}")
        else:
            has_errors = True
            error_count = len(result["errors"])
            print(f"❌ {result['name']} — {error_count} ошибок:")
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
