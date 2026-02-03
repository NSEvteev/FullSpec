#!/usr/bin/env python3
"""
generate-readme.py — Генерация шаблона README.md для папки.

Использование:
    python generate-readme.py <путь_к_папке>

Примеры:
    python generate-readme.py src/api
    python generate-readme.py .claude/.instructions/agents

Логика:
    1. Определяет тип папки (проект vs инструкции)
    2. Вычисляет frontmatter (standard, index)
    3. Генерирует цепочку "Полезные ссылки"
    4. Создаёт шаблон с плейсхолдерами {PLACEHOLDER}

Плейсхолдеры для LLM:
    {DESCRIPTION} — краткое описание папки
    {EXTENDED_DESCRIPTION} — расширенное описание
    {TOPICS} — темы через запятую (для инструкций)
    {FOLDER_PURPOSE} — назначение папки

Возвращает:
    0 — успех
    1 — ошибка (папка не существует и не указан --create)
"""

import argparse
import sys
from pathlib import Path


def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def get_relative_path(folder_path: Path, repo_root: Path) -> str:
    """Получить относительный путь от корня репозитория."""
    try:
        rel = folder_path.resolve().relative_to(repo_root)
        return str(rel).replace("\\", "/")
    except ValueError:
        return str(folder_path).replace("\\", "/")


def is_instructions_folder(rel_path: str) -> bool:
    """Определить, является ли папка папкой инструкций."""
    return ".instructions" in rel_path


def get_nesting_level(rel_path: str) -> int:
    """Вычислить уровень вложенности папки."""
    parts = [p for p in rel_path.split("/") if p and p != "."]
    return len(parts)


def get_standard_version(repo_root: Path) -> str:
    """Получить версию стандарта из standard-readme.md."""
    standard_path = repo_root / ".structure/.instructions/standard-readme.md"
    if standard_path.exists():
        try:
            content = standard_path.read_text(encoding="utf-8")
            import re
            match = re.search(r"^standard-version:\s*(.+)$", content, re.MULTILINE)
            if match:
                return match.group(1).strip()
        except Exception:
            pass
    return "v1.2"  # fallback


def compute_frontmatter(rel_path: str, is_instructions: bool, repo_root: Path) -> dict:
    """Вычислить frontmatter для README."""
    if is_instructions:
        standard = ".structure/.instructions/standard-readme.md"
    else:
        standard = ".structure/.instructions/standard-readme.md"

    # index — путь к самому README
    index = f"{rel_path}/README.md" if rel_path else "README.md"

    # Получаем версию стандарта
    standard_version = get_standard_version(repo_root)

    return {
        "description": "{DESCRIPTION}",
        "standard": standard,
        "standard_version": standard_version,
        "index": index,
    }


def generate_useful_links_project(rel_path: str, repo_root: Path) -> str:
    """Сгенерировать блок 'Полезные ссылки' для папки проекта."""
    level = get_nesting_level(rel_path)
    links = []

    # Собираем цепочку родителей
    parts = [p for p in rel_path.split("/") if p]

    if level == 1:
        # Уровень 1: только ссылка на структуру
        links.append("- [Структура проекта](/.structure/README.md)")
    else:
        # Уровень 2+: цепочка родителей до структуры
        # Идём от непосредственного родителя к корню
        for i in range(level - 1, 0, -1):
            parent_path = "/".join(parts[:i])
            parent_readme = repo_root / parent_path / "README.md"

            # Определяем текст ссылки
            if parent_readme.exists():
                # Читаем заголовок из существующего README
                try:
                    content = parent_readme.read_text(encoding="utf-8")
                    # Ищем заголовок # /path/ — Название
                    import re
                    match = re.search(r"^#\s+/[^/]+/\s*—\s*(.+)$", content, re.MULTILINE)
                    if match:
                        link_text = match.group(1).strip()
                    else:
                        link_text = f"{parts[i-1]}/"
                except Exception:
                    link_text = f"{parts[i-1]}/"
            else:
                link_text = f"{parts[i-1]}/"

            # Вычисляем относительный путь
            dots = "../" * (level - i)
            links.append(f"- [{link_text}]({dots}README.md)")

        links.append("- [Структура проекта](/.structure/README.md)")

    return "**Полезные ссылки:**\n" + "\n".join(links)


def generate_useful_links_instructions(rel_path: str, repo_root: Path) -> str:
    """Сгенерировать блок 'Полезные ссылки' для папки инструкций."""
    # Для инструкций: цепочка до README родительской папки проекта
    parts = [p for p in rel_path.split("/") if p]

    # Находим индекс .instructions в пути
    try:
        instr_idx = parts.index(".instructions")
    except ValueError:
        # Не нашли .instructions — fallback
        return "**Полезные ссылки:**\n- [Родительская папка](../README.md)"

    links = []

    # Уровень внутри .instructions
    level_in_instructions = len(parts) - instr_idx - 1

    if level_in_instructions == 0:
        # README самой папки .instructions — ссылка на README родителя проекта
        parent_project = "/".join(parts[:instr_idx])
        if parent_project:
            # Пытаемся получить название родителя
            parent_readme = repo_root / parent_project / "README.md"
            if parent_readme.exists():
                try:
                    content = parent_readme.read_text(encoding="utf-8")
                    import re
                    # Ищем "описание папки" или заголовок
                    match = re.search(r"^#\s+/\.?([^/]+)/", content, re.MULTILINE)
                    if match:
                        link_text = f"{match.group(1).capitalize()}"
                    else:
                        link_text = parts[instr_idx - 1] if instr_idx > 0 else "Проект"
                except Exception:
                    link_text = parts[instr_idx - 1] if instr_idx > 0 else "Проект"
            else:
                link_text = parts[instr_idx - 1] if instr_idx > 0 else "Проект"
            links.append(f"- [{link_text}](../README.md)")
        else:
            links.append("- [SSOT структуры проекта](../README.md)")
    else:
        # Файл или подпапка внутри .instructions
        # Цепочка: ./README.md → ../README.md → ...
        current_depth = level_in_instructions

        # Сначала ссылка на README текущей папки инструкций
        if current_depth >= 1:
            instr_folder_name = parts[instr_idx + current_depth - 1] if current_depth > 1 else ".instructions"
            links.append(f"- [Инструкции {instr_folder_name}](./README.md)")

        # Затем вверх по цепочке
        for i in range(current_depth - 1, 0, -1):
            dots = "../" * (current_depth - i)
            folder_name = parts[instr_idx + i - 1] if i > 0 else parts[instr_idx - 1]
            links.append(f"- [Инструкции {folder_name}]({dots}README.md)")

        # Последняя — README родителя проекта
        dots = "../" * (current_depth + 1)
        parent_name = parts[instr_idx - 1] if instr_idx > 0 else "проекта"
        links.append(f"- [SSOT {parent_name}]({dots}README.md)")

    return "**Полезные ссылки:**\n" + "\n".join(links)


def generate_project_readme(rel_path: str, frontmatter: dict, useful_links: str) -> str:
    """Сгенерировать шаблон README для папки проекта."""
    folder_name = rel_path.split("/")[-1] if rel_path else "root"

    template = f'''---
description: {{DESCRIPTION}}
standard: {frontmatter["standard"]}
standard-version: {frontmatter["standard_version"]}
index: {frontmatter["index"]}
---

# /{rel_path}/ — {{FOLDER_PURPOSE}}

{{EXTENDED_DESCRIPTION}}

{useful_links}

## Оглавление

- [1. Папки](#1-папки)
- [2. Файлы](#2-файлы)
- [3. Дерево](#3-дерево)

---

## 1. Папки

<!-- Для каждой подпапки: -->
<!-- ### 🔗 [subfolder/](./subfolder/README.md) -->
<!-- **Краткое описание.** -->
<!-- Расширенное описание. -->

{{FOLDERS_CONTENT}}

---

## 2. Файлы

<!-- Для каждого файла: -->
<!-- ### 🔗 [file.ext](./file.ext) -->
<!-- **Краткое описание.** -->
<!-- Расширенное описание. -->

{{FILES_CONTENT}}

---

## 3. Дерево

```
/{rel_path}/
├── {{TREE_CONTENT}}
└── README.md                # Этот файл
```
'''
    return template


def generate_instructions_readme(rel_path: str, frontmatter: dict, useful_links: str) -> str:
    """Сгенерировать шаблон README для папки инструкций по стандарту."""
    # Определяем область инструкций
    parts = [p for p in rel_path.split("/") if p]
    try:
        instr_idx = parts.index(".instructions")
        area = parts[instr_idx - 1] if instr_idx > 0 else "проекта"
    except ValueError:
        area = "проекта"

    template = f'''---
description: {{DESCRIPTION}}
standard: {frontmatter["standard"]}
standard-version: {frontmatter["standard_version"]}
index: {frontmatter["index"]}
---

# Инструкции /{rel_path}/

{{DESCRIPTION}}

{useful_links}

**Содержание:** {{TOPICS}}.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/{rel_path}/
├── README.md            # Этот файл (индекс)
└── {{TREE_CONTENT}}
```

---

# 1. Стандарты

*Нет стандартов.*

<!-- Шаблон для добавления стандарта:
## 1.1. Стандарт {{объекта}}

{{Описание — одно предложение.}}

**Оглавление:**
- [{{Раздел}}](./standard-{{object}}.md#раздел)

**Инструкция:** [standard-{{object}}.md](./standard-{{object}}.md)
-->

---

# 2. Воркфлоу

*Нет воркфлоу.*

<!-- Шаблон для добавления воркфлоу:
## 2.1. Создание {{объекта}}

{{Описание — одно предложение.}}

**Оглавление:**
- [{{Раздел}}](./create-{{object}}.md#раздел)

**Инструкция:** [create-{{object}}.md](./create-{{object}}.md)
-->

---

# 3. Валидация

*Нет валидаций.*

<!-- Шаблон для добавления валидации:
## 3.1. Валидация {{объекта}}

{{Описание — одно предложение.}}

**Оглавление:**
- [{{Раздел}}](./validation-{{object}}.md#раздел)

**Инструкция:** [validation-{{object}}.md](./validation-{{object}}.md)
-->

---

# 4. Скрипты

*Нет скриптов.*

<!-- Шаблон для добавления скриптов:
| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [{{script}}.py](./.scripts/{{script}}.py) | {{описание}} | [{{инструкция}}.md](./{{инструкция}}.md) |
-->

---

# 5. Скиллы

*Нет скиллов.*

<!-- Шаблон для добавления скиллов:
| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/{{skill}}](/.claude/skills/{{skill}}/SKILL.md) | {{описание}} | [{{инструкция}}.md](./{{инструкция}}.md) |
-->
'''
    return template


def generate_readme(folder_path: str, repo_root: Path) -> str:
    """Сгенерировать README для указанной папки."""
    # Нормализуем путь
    folder_path = folder_path.strip("/").replace("\\", "/")

    # Определяем тип папки
    is_instructions = is_instructions_folder(folder_path)

    # Вычисляем frontmatter
    frontmatter = compute_frontmatter(folder_path, is_instructions, repo_root)

    # Генерируем "Полезные ссылки"
    if is_instructions:
        useful_links = generate_useful_links_instructions(folder_path, repo_root)
    else:
        useful_links = generate_useful_links_project(folder_path, repo_root)

    # Генерируем шаблон
    if is_instructions:
        return generate_instructions_readme(folder_path, frontmatter, useful_links)
    else:
        return generate_project_readme(folder_path, frontmatter, useful_links)


def main():
    """Точка входа."""
    # UTF-8 для Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Генерация шаблона README.md для папки"
    )
    parser.add_argument(
        "folder",
        help="Путь к папке (относительный от корня репозитория)"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Создать папку если не существует"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    # Проверяем/создаём папку
    folder_path = args.folder.strip("/").replace("\\", "/")
    full_path = repo_root / folder_path

    if not full_path.exists():
        if args.create:
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Папка создана: {full_path}", file=sys.stderr)
        else:
            print(f"⚠️  Папка не существует: {full_path}", file=sys.stderr)
            print(f"   Используйте --create для автоматического создания", file=sys.stderr)
            sys.exit(1)

    # Генерируем и выводим README
    readme_content = generate_readme(args.folder, repo_root)
    print(readme_content)
    sys.exit(0)


if __name__ == "__main__":
    main()
