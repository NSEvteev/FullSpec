#!/usr/bin/env python3
"""
create-script-file.py — Создание файла скрипта по шаблону.

Создаёт новый файл скрипта в указанной папке .scripts/
с заполненным docstring и базовой структурой.

Использование:
    python create-script-file.py <name> [--area <path>] [--description <text>]

Аргументы:
    name        Имя скрипта (без расширения)

Примеры:
    python create-script-file.py validate-api
    python create-script-file.py parse-config --area src/.instructions
    python create-script-file.py find-broken-links --description "Поиск битых ссылок"

Возвращает:
    0 — файл создан
    1 — ошибка (файл существует, неверные аргументы)
"""

import argparse
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""
{name}.py — {description}.

{detailed_description}

Использование:
    python {name}.py <input> [--option <value>]

Примеры:
    python {name}.py file.txt
    python {name}.py data.json --output result.json

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
import sys
from pathlib import Path


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
# Основные функции
# =============================================================================

def process(input_path: Path) -> bool:
    """Основная логика скрипта."""
    # TODO: Реализовать логику
    print(f"✅ Обработан: {{input_path}}")
    return True


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="{description}"
    )
    parser.add_argument("input", help="Входной файл")
    parser.add_argument(
        "--repo", default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    input_path = Path(args.input)

    success = process(input_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
'''


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
# Основные функции
# =============================================================================

def create_script_file(
    name: str,
    area: Path,
    description: str | None = None
) -> Path:
    """Создать файл скрипта."""
    # Полное имя файла
    filename = f"{name}.py"
    scripts_dir = area / ".scripts"
    file_path = scripts_dir / filename

    # Проверить существование
    if file_path.exists():
        raise FileExistsError(f"Файл уже существует: {file_path}")

    # Описание по умолчанию
    if not description:
        description = f"Скрипт {name}"

    # Детальное описание
    detailed_description = f"Автоматизация для шагов инструкций в {area.name}/."

    # Заполнить шаблон
    content = SCRIPT_TEMPLATE.format(
        name=name,
        description=description,
        detailed_description=detailed_description,
    )

    # Создать директорию если нужно
    scripts_dir.mkdir(parents=True, exist_ok=True)

    # Записать файл
    file_path.write_text(content, encoding='utf-8')

    return file_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Создание файла скрипта по шаблону"
    )
    parser.add_argument("name", help="Имя скрипта (без расширения)")
    parser.add_argument(
        "--area", default=".instructions",
        help="Папка .instructions (по умолчанию: .instructions)"
    )
    parser.add_argument(
        "--description",
        help="Описание для docstring"
    )
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    area = repo_root / args.area

    # Проверить что area — папка .instructions
    if not area.name == ".instructions" and ".instructions" not in str(area):
        print(f"❌ Область должна быть папкой .instructions: {area}", file=sys.stderr)
        sys.exit(1)

    try:
        file_path = create_script_file(
            name=args.name,
            area=area,
            description=args.description,
        )
        rel_path = file_path.relative_to(repo_root)
        print(f"✅ Создан: {rel_path}")
        sys.exit(0)

    except FileExistsError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
