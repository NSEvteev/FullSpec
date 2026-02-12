#!/usr/bin/env python3
"""
validate-links.py — Валидация ссылок в markdown-документах.

Использование:
    python validate-links.py [--repo <корень>] [--json] [--path <файл/папка>]

Примеры:
    python validate-links.py
    python validate-links.py --json
    python validate-links.py --path docs/
    python validate-links.py --path README.md

Проверки:
    E001 — Файл по ссылке не существует
    E002 — Папка по ссылке не существует
    E003 — Якорь не найден в целевом файле
    E004 — Ссылка на папку без trailing slash
    E005 — Квадратные скобки в frontmatter-ссылке
    E006 — Ведущий / в frontmatter-ссылке
    E007 — Файл из frontmatter не существует
    E008 — Неверный формат ссылки в SSOT
    E009 — Ссылка в SSOT не на README.md
    E010 — Папка скилла не существует (ссылка из инструкции)
    E011 — SKILL.md не найден в папке скилла
    E012 — SSOT-инструкция в скилле не существует
    E013 — SSOT-инструкция в скилле помечена DELETE_
    E014 — Неверный формат якоря строки (#L)
    E015 — Якорь строки на markdown-файл
    E016 — Отсутствует обязательная ссылка по графу (§13)

Шаг 13 (§12): Автогенерируемые файлы — все ошибки помечаются генератором
Шаг 14 (§13): Граф зависимостей — проверка обязательных ссылок

Предупреждения:
    W001 — Абсолютный путь для файла в той же папке
    W002 — Относительный путь с длинной цепочкой ../
    W003 — Похожий якорь существует (опечатка?)
    W004 — Имя скилла в тексте не совпадает с папкой
    W005 — Скилл ссылается на переименованную инструкцию
    W006 — Номер строки выходит за пределы файла
    W007 — GitHub-ссылка на main/master (может стать битой)
    W008 — Ссылка на deprecated-файл
    W009 — Документ не имеет входящих ссылок (сирота)

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher


# =============================================================================
# Константы
# =============================================================================

ERROR_CODES = {
    # Ошибки (E0xx)
    "E000": "Не удалось прочитать файл",
    "E001": "Файл по ссылке не существует",
    "E002": "Папка по ссылке не существует",
    "E003": "Якорь не найден в целевом файле",
    "E004": "Ссылка на папку без trailing slash",
    "E005": "Квадратные скобки в frontmatter-ссылке",
    "E006": "Ведущий / в frontmatter-ссылке",
    "E007": "Файл из frontmatter не существует",
    "E008": "Неверный формат ссылки в SSOT",
    "E009": "Ссылка в SSOT не на README.md",
    "E010": "Папка скилла не существует",
    "E011": "SKILL.md не найден в папке скилла",
    "E012": "SSOT-инструкция в скилле не существует",
    "E013": "SSOT-инструкция в скилле помечена DELETE_",
    "E014": "Неверный формат якоря строки (#L)",
    "E015": "Якорь строки на markdown-файл",
    "E016": "Отсутствует обязательная ссылка по графу",
    # Предупреждения (W0xx)
    "W001": "Абсолютный путь для файла в той же папке",
    "W002": "Относительный путь с длинной цепочкой ../",
    "W003": "Похожий якорь существует (опечатка?)",
    "W004": "Имя скилла в тексте не совпадает с папкой",
    "W005": "Скилл ссылается на переименованную инструкцию",
    "W006": "Номер строки выходит за пределы файла",
    "W007": "GitHub-ссылка на main/master (может стать битой)",
    "W008": "Ссылка на deprecated-файл",
    "W009": "Документ не имеет входящих ссылок (сирота)",
}


# =============================================================================
# Хелперы для ошибок
# =============================================================================

def add_error(result: dict, code: str, detail: str = "") -> None:
    """Добавить ошибку с кодом из ERROR_CODES."""
    message = ERROR_CODES.get(code, code)
    if detail:
        message = f"{message}: {detail}"
    result["errors"].append({"code": code, "message": message})


def add_warning(result: dict, code: str, detail: str = "") -> None:
    """Добавить предупреждение с кодом из ERROR_CODES."""
    message = ERROR_CODES.get(code, code)
    if detail:
        message = f"{message}: {detail}"
    result["warnings"].append({"code": code, "message": message})


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


def extract_frontmatter(content: str) -> dict[str, str]:
    """Извлечь frontmatter из markdown-файла."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def extract_headings(content: str) -> list[str]:
    """Извлечь все заголовки из markdown-файла и преобразовать в якоря."""
    headings = []
    for match in re.finditer(r"^#+\s+(.+)$", content, re.MULTILINE):
        heading = match.group(1)
        # Убрать markdown-ссылки: [text](url) → text
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        # Преобразование в якорь: lowercase, пробелы → дефисы, удаление спецсимволов
        anchor = heading.lower()
        anchor = re.sub(r"[^\w\s\-а-яё]", "", anchor, flags=re.IGNORECASE)
        anchor = re.sub(r"\s+", "-", anchor)
        anchor = anchor.strip("-")
        headings.append(anchor)
    return headings


def remove_code_blocks(content: str) -> str:
    """Удалить блоки кода из markdown для корректного парсинга ссылок."""
    # Удаляем fenced code blocks (```...```)
    content = re.sub(r"```[\s\S]*?```", "", content)
    # Удаляем inline code (`...`)
    content = re.sub(r"`[^`]+`", "", content)
    return content


def extract_links(content: str) -> list[dict]:
    """Извлечь все markdown-ссылки из содержимого (игнорируя блоки кода)."""
    # Убираем блоки кода перед парсингом
    clean_content = remove_code_blocks(content)

    links = []
    # Паттерн для [текст](путь) или [текст](путь#якорь)
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", clean_content):
        text = match.group(1)
        href = match.group(2)
        start = match.start()

        links.append({
            "text": text,
            "href": href,
            "position": start,
            "is_external": href.startswith(("http://", "https://", "mailto:")),
        })
    return links


def check_line_anchor(href: str, target_file: Path, result: dict) -> None:
    """Проверить якорь на строку кода (#L42 или #L42-L50)."""
    if "#L" not in href:
        return

    path_part, anchor = href.split("#", 1)

    # E015: Якорь строки на markdown
    if target_file.suffix == ".md":
        add_error(result, "E015", href)
        return

    # E014: Неверный формат
    if not re.match(r"^L\d+(-L\d+)?$", anchor):
        add_error(result, "E014", href)
        return

    # W006: Номер строки за пределами файла
    if target_file.exists():
        try:
            line_count = len(target_file.read_text(encoding="utf-8").split("\n"))
            numbers = re.findall(r"\d+", anchor)
            for num in numbers:
                if int(num) > line_count:
                    add_warning(result, "W006", f"{href} (файл имеет {line_count} строк)")
                    break
        except Exception:
            pass


def check_github_links(links: list[dict], result: dict) -> None:
    """Проверить GitHub-ссылки на привязку к версии (Шаг 11)."""
    for link in links:
        if not link["is_external"]:
            continue
        href = link["href"]
        if "github.com" in href and "/blob/" in href:
            if "/blob/main/" in href or "/blob/master/" in href:
                add_warning(result, "W007", href)


def check_deprecated_links(href: str, target_file: Path, result: dict) -> None:
    """Проверить ссылки на deprecated-файлы (Шаг 12)."""
    if not target_file.exists():
        return
    try:
        content = target_file.read_text(encoding="utf-8")
        # Ищем DEPRECATED в начале файла (после frontmatter), не в примерах
        # Паттерн: > ⚠️ **DEPRECATED:** в первых 50 строках
        lines = content.split("\n")[:50]
        header = "\n".join(lines)
        if "> ⚠️ **DEPRECATED:**" in header or "> **DEPRECATED:**" in header:
            add_warning(result, "W008", href)
    except Exception:
        pass


def resolve_path(base_file: Path, href: str, repo_root: Path) -> Path:
    """Разрешить путь ссылки относительно файла или корня."""
    # Убираем якорь
    path_part = href.split("#")[0] if "#" in href else href

    if not path_part:
        # Только якорь (#section)
        return base_file

    if path_part.startswith("/"):
        # Абсолютный путь от корня
        return repo_root / path_part.lstrip("/")
    else:
        # Относительный путь от файла
        return (base_file.parent / path_part).resolve()


def similar_anchor(anchor: str, headings: list[str], threshold: float = 0.8) -> str | None:
    """Найти похожий якорь (для предупреждения об опечатке)."""
    for heading in headings:
        ratio = SequenceMatcher(None, anchor, heading).ratio()
        if ratio >= threshold and anchor != heading:
            return heading
    return None


def validate_file(file_path: Path, repo_root: Path) -> dict:
    """Валидировать ссылки в одном файле."""
    result = {
        "file": str(file_path.relative_to(repo_root)),
        "errors": [],
        "warnings": [],
    }

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        add_error(result, "E000", str(e))
        return result

    # Проверка frontmatter (Шаг 5)
    frontmatter = extract_frontmatter(content)
    for field in ["standard", "index"]:
        if field in frontmatter:
            value = frontmatter[field]

            # E005: Квадратные скобки
            if "[" in value or "]" in value:
                add_error(result, "E005", f"{field}: {value}")

            # E006: Ведущий /
            if value.startswith("/"):
                add_error(result, "E006", f"{field}: {value}")

            # E007: Файл не существует
            resolved = repo_root / value
            if not resolved.exists():
                add_error(result, "E007", f"{field}: {value}")

    # Проверка ссылок в SSOT (Шаг 6)
    is_ssot = file_path == repo_root / ".structure" / "README.md"
    if is_ssot:
        for match in re.finditer(r"^###\s*🔗\s*\[([^\]]+)\]\(([^)]+)\)", content, re.MULTILINE):
            link_text = match.group(1)
            link_href = match.group(2)

            # E008: Название без trailing slash
            if not link_text.endswith("/"):
                add_error(result, "E008", f"[{link_text}]")

            # E009: Путь не на README.md
            if not link_href.endswith("README.md"):
                add_error(result, "E009", link_href)

    # Проверка всех ссылок
    links = extract_links(content)

    # Шаг 11: GitHub-ссылки
    check_github_links(links, result)

    for link in links:
        # Пропускаем внешние ссылки для внутренних проверок
        if link["is_external"]:
            continue

        href = link["href"]
        anchor = None

        # Разделяем путь и якорь
        if "#" in href:
            path_part, anchor = href.split("#", 1)
        else:
            path_part = href

        # Шаг 1: Существование цели
        if path_part:
            resolved = resolve_path(file_path, href, repo_root)

            if resolved.is_dir():
                # E004: Ссылка на папку без trailing slash
                if not path_part.endswith("/") and not path_part.endswith("README.md"):
                    add_error(result, "E004", href)
            elif not resolved.exists():
                # Проверяем, это папка или файл
                if path_part.endswith("/"):
                    add_error(result, "E002", href)
                else:
                    add_error(result, "E001", href)
                continue  # Не проверяем якорь, если файл не существует

        # Шаг 3: Якорные ссылки
        if anchor:
            target_file = resolve_path(file_path, href, repo_root)
            if target_file.exists() and target_file.is_file():
                # Шаг 9: Якоря на строки кода
                if anchor.startswith("L") and anchor[1:2].isdigit():
                    check_line_anchor(href, target_file, result)
                else:
                    # Обычные якоря на заголовки
                    try:
                        target_content = target_file.read_text(encoding="utf-8")
                        headings = extract_headings(target_content)

                        if anchor not in headings:
                            # E003: Якорь не найден
                            add_error(result, "E003", href)

                            # W003: Похожий якорь
                            similar = similar_anchor(anchor, headings)
                            if similar:
                                add_warning(result, "W003", f"#{similar} (вместо #{anchor})")
                    except Exception:
                        pass

                # Шаг 12: Проверка deprecated
                check_deprecated_links(href, target_file, result)

        # Шаг 2: Формат пути
        if path_part:
            # W001: Абсолютный путь для файла в той же папке
            if path_part.startswith("/"):
                resolved = repo_root / path_part.lstrip("/")
                if resolved.parent == file_path.parent:
                    add_warning(result, "W001", href)

            # W002: Длинная цепочка ../
            parent_count = path_part.count("../")
            if parent_count >= 3:
                add_warning(result, "W002", href)

    # Шаг 7: Проверка ссылок на скиллы (только в .instructions)
    if ".instructions" in str(file_path):
        skill_result = validate_skill_links_in_instructions(file_path, content, repo_root)
        result["errors"].extend(skill_result["errors"])
        result["warnings"].extend(skill_result["warnings"])

    # Шаг 13: Проверка автогенерируемых файлов (§12)
    check_autogenerated_files(file_path, content, result)

    # Шаг 14: Проверка графа зависимостей (§13)
    check_dependency_graph(file_path, content, repo_root, result)

    return result


def validate_skill_links_in_instructions(file_path: Path, content: str, repo_root: Path) -> dict:
    """
    Проверить ссылки на скиллы в инструкциях (Шаг 7).

    Возвращает dict с errors и warnings.
    """
    result = {"errors": [], "warnings": []}

    # Ищем ссылки вида [/skill-name](/.claude/skills/skill-name/SKILL.md)
    pattern = r"\[(/[\w-]+)\]\((/?\.claude/skills/([^/]+)/SKILL\.md)\)"

    for match in re.finditer(pattern, content):
        skill_text = match.group(1)  # /skill-name
        skill_path = match.group(2)  # .claude/skills/skill-name/SKILL.md
        skill_folder = match.group(3)  # skill-name

        # Нормализуем путь
        if skill_path.startswith("/"):
            skill_path = skill_path[1:]

        full_skill_path = repo_root / skill_path
        skill_folder_path = repo_root / ".claude" / "skills" / skill_folder

        # E010: Папка скилла не существует
        if not skill_folder_path.exists():
            add_error(result, "E010", f"{skill_folder}/")
            continue

        # E011: SKILL.md не найден
        if not full_skill_path.exists():
            add_error(result, "E011", skill_path)
            continue

        # W004: Имя скилла в тексте не совпадает с папкой
        expected_name = f"/{skill_folder}"
        if skill_text != expected_name:
            add_warning(result, "W004", f"'{skill_text}' vs '{expected_name}'")

    return result


def validate_ssot_links_in_skills(repo_root: Path) -> list[dict]:
    """
    Проверить SSOT-ссылки в скиллах (Шаг 8).

    Возвращает список результатов по файлам.
    """
    results = []
    skills_dir = repo_root / ".claude" / "skills"

    if not skills_dir.exists():
        return results

    for skill_folder in skills_dir.iterdir():
        if not skill_folder.is_dir():
            continue

        # Пропускаем уже удалённые
        if skill_folder.name.startswith("DELETE_"):
            continue

        skill_md = skill_folder / "SKILL.md"
        if not skill_md.exists():
            continue

        file_result = {
            "file": str(skill_md.relative_to(repo_root)),
            "errors": [],
            "warnings": [],
        }

        try:
            content = skill_md.read_text(encoding="utf-8")
        except Exception:
            continue

        # Ищем SSOT: ссылки
        # Паттерн: **SSOT:** [text](path) или SSOT: [text](path)
        ssot_pattern = r"\*?\*?SSOT:?\*?\*?\s*\[([^\]]+)\]\(([^)]+)\)"

        for match in re.finditer(ssot_pattern, content):
            link_text = match.group(1)
            link_path = match.group(2)

            # Нормализуем путь
            if link_path.startswith("/"):
                resolved = repo_root / link_path[1:]
            else:
                resolved = (skill_md.parent / link_path).resolve()

            # E012: SSOT-инструкция не существует
            if not resolved.exists():
                add_error(file_result, "E012", link_path)
                continue

            # E013: SSOT-инструкция помечена DELETE_
            path_str = str(resolved)
            if "DELETE_" in path_str:
                add_error(file_result, "E013", link_path)

            # W005: Путь содержит старое имя (возможно, переименовано)
            # Это сложно определить автоматически, пропускаем

        if file_result["errors"] or file_result["warnings"]:
            results.append(file_result)

    return results


def check_autogenerated_files(file_path: Path, content: str, result: dict) -> None:
    """Проверить автогенерируемые файлы (Шаг 13, §12)."""
    frontmatter = extract_frontmatter(content)
    if frontmatter.get("autogenerated") == "true":
        generator = frontmatter.get("generator", "unknown")
        # Все ошибки в автогенерируемых файлах помечаем указанием генератора
        for error in result["errors"]:
            error["message"] += f" [autogenerated by: {generator}]"
        for warning in result["warnings"]:
            warning["message"] += f" [autogenerated by: {generator}]"


def check_dependency_graph(file_path: Path, content: str, repo_root: Path, result: dict) -> None:
    """Проверить обязательные ссылки по графу зависимостей (Шаг 14, §13)."""
    frontmatter = extract_frontmatter(content)
    rel_path = str(file_path.relative_to(repo_root)).replace("\\", "/")

    # Инструкция (standard-*) должна иметь standard в frontmatter
    if "/standard-" in rel_path and rel_path.endswith(".md"):
        if "standard" not in frontmatter:
            add_error(result, "E016", "standard-* должен иметь поле 'standard' в frontmatter")

    # Инструкция (create-/modify-/validation-) должна ссылаться на standard-*
    for prefix in ["create-", "modify-", "validation-"]:
        if f"/{prefix}" in rel_path and rel_path.endswith(".md"):
            if "standard" not in frontmatter:
                add_error(result, "E016", f"{prefix}* должен иметь поле 'standard' в frontmatter")
            break

    # Скилл должен иметь SSOT-ссылку
    if "/.claude/skills/" in rel_path and rel_path.endswith("SKILL.md"):
        if "**SSOT:**" not in content and "SSOT:" not in content:
            add_error(result, "E016", "SKILL.md должен иметь SSOT-ссылку")

    # README папки должен ссылаться на README родителя (кроме корневого)
    if rel_path.endswith("README.md") and rel_path != "README.md":
        parent_readme_patterns = ["../README.md", "родител", "Полезные ссылки"]
        has_parent_link = any(p in content for p in parent_readme_patterns)
        if not has_parent_link:
            add_warning(result, "W009", "README не ссылается на README родителя")


def find_orphan_documents(repo_root: Path, all_files: list[Path]) -> list[dict]:
    """Найти документы без входящих ссылок (сироты)."""
    # Собираем все ссылки
    all_links = set()
    for file_path in all_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            links = extract_links(content)
            for link in links:
                if not link["is_external"]:
                    resolved = resolve_path(file_path, link["href"], repo_root)
                    if resolved.exists():
                        all_links.add(str(resolved.relative_to(repo_root)).replace("\\", "/"))
        except Exception:
            continue

    # Проверяем, какие файлы не имеют входящих ссылок
    orphans = []
    excluded_roots = {"README.md", "CLAUDE.md", ".structure/README.md"}
    for file_path in all_files:
        rel_path = str(file_path.relative_to(repo_root)).replace("\\", "/")
        # Пропускаем корневые файлы
        if rel_path in excluded_roots:
            continue
        # Пропускаем стандарты (они — источники, а не цели)
        if "/standard-" in rel_path:
            continue
        if rel_path not in all_links:
            orphans.append({
                "file": rel_path,
                "errors": [],
                "warnings": [{"code": "W009", "message": f"{ERROR_CODES['W009']}: {rel_path}"}]
            })

    return orphans


def validate_links(repo_root: Path, target_path: Path | None = None) -> dict:
    """
    Валидировать ссылки в markdown-файлах.

    Возвращает dict с полями:
        valid: bool
        files_checked: int
        total_errors: int
        total_warnings: int
        results: list[dict] — результаты по файлам
    """
    result = {
        "valid": True,
        "files_checked": 0,
        "total_errors": 0,
        "total_warnings": 0,
        "results": [],
    }

    # Определяем, какие файлы проверять
    if target_path:
        if target_path.is_file():
            md_files = [target_path]
        elif target_path.is_dir():
            md_files = list(target_path.rglob("*.md"))
        else:
            result["results"].append({
                "file": str(target_path),
                "errors": [{"code": "E000", "message": f"{ERROR_CODES['E000']}: путь не существует"}],
                "warnings": [],
            })
            result["valid"] = False
            return result
    else:
        md_files = list(repo_root.rglob("*.md"))

    # Исключаем node_modules и т.п.
    excluded = {"node_modules", ".git", "dist", "build", "__pycache__", "venv", ".venv"}
    md_files = [
        f for f in md_files
        if not any(part in excluded for part in f.parts)
    ]

    for md_file in md_files:
        file_result = validate_file(md_file, repo_root)
        result["files_checked"] += 1

        if file_result["errors"]:
            result["valid"] = False
            result["total_errors"] += len(file_result["errors"])

        result["total_warnings"] += len(file_result["warnings"])

        # Добавляем только файлы с проблемами
        if file_result["errors"] or file_result["warnings"]:
            result["results"].append(file_result)

    # Шаг 8: Проверка SSOT-ссылок в скиллах
    skill_results = validate_ssot_links_in_skills(repo_root)
    for skill_result in skill_results:
        result["results"].append(skill_result)
        if skill_result["errors"]:
            result["valid"] = False
            result["total_errors"] += len(skill_result["errors"])
        result["total_warnings"] += len(skill_result["warnings"])

    # Шаг 14: Проверка сирот (документы без входящих ссылок)
    # Выполняется только при проверке всего проекта
    if not target_path:
        orphan_results = find_orphan_documents(repo_root, md_files)
        for orphan in orphan_results:
            result["results"].append(orphan)
            result["total_warnings"] += len(orphan["warnings"])

    return result


def main():
    """Точка входа."""
    # UTF-8 для Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация ссылок в markdown-документах"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )
    parser.add_argument(
        "--path",
        default=None,
        help="Конкретный файл или папка для проверки"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в JSON формате"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    target_path = Path(args.path).resolve() if args.path else None

    result = validate_links(repo_root, target_path)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["valid"] else 1)

    # Человекочитаемый вывод
    print(f"Проверка ссылок в: {target_path or repo_root}")
    print(f"Файлов проверено: {result['files_checked']}")
    print()

    if result["valid"] and result["total_warnings"] == 0:
        print("✅ Все ссылки валидны")
        sys.exit(0)

    # Группируем по файлам
    for file_result in result["results"]:
        print(f"📄 {file_result['file']}")

        for error in file_result["errors"]:
            print(f"   ❌ [{error['code']}] {error['message']}")

        for warning in file_result["warnings"]:
            print(f"   ⚠️  [{warning['code']}] {warning['message']}")

        print()

    # Итоги
    print("─" * 40)
    if result["total_errors"]:
        print(f"❌ Ошибок: {result['total_errors']}")
    if result["total_warnings"]:
        print(f"⚠️  Предупреждений: {result['total_warnings']}")

    sys.exit(1 if not result["valid"] else 0)


if __name__ == "__main__":
    main()
