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

Предупреждения:
    W001 — Абсолютный путь для файла в той же папке
    W002 — Относительный путь с длинной цепочкой ../
    W003 — Похожий якорь существует (опечатка?)

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

        # Пропускаем внешние ссылки
        if href.startswith(("http://", "https://", "mailto:")):
            continue

        links.append({
            "text": text,
            "href": href,
            "position": start,
        })
    return links


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
        result["errors"].append({
            "code": "E000",
            "message": f"Не удалось прочитать файл: {e}",
        })
        return result

    # Проверка frontmatter (Шаг 5)
    frontmatter = extract_frontmatter(content)
    for field in ["standard", "index"]:
        if field in frontmatter:
            value = frontmatter[field]

            # E005: Квадратные скобки
            if "[" in value or "]" in value:
                result["errors"].append({
                    "code": "E005",
                    "message": f"Квадратные скобки в frontmatter-ссылке: {field}: {value}",
                })

            # E006: Ведущий /
            if value.startswith("/"):
                result["errors"].append({
                    "code": "E006",
                    "message": f"Ведущий / в frontmatter-ссылке: {field}: {value}",
                })

            # E007: Файл не существует
            resolved = repo_root / value
            if not resolved.exists():
                result["errors"].append({
                    "code": "E007",
                    "message": f"Файл из frontmatter не существует: {field}: {value}",
                })

    # Проверка ссылок в SSOT (Шаг 6)
    is_ssot = file_path == repo_root / ".structure" / "README.md"
    if is_ssot:
        for match in re.finditer(r"^###\s*🔗\s*\[([^\]]+)\]\(([^)]+)\)", content, re.MULTILINE):
            link_text = match.group(1)
            link_href = match.group(2)

            # E008: Название без trailing slash
            if not link_text.endswith("/"):
                result["errors"].append({
                    "code": "E008",
                    "message": f"Неверный формат ссылки в SSOT: [{link_text}] должен заканчиваться на /",
                })

            # E009: Путь не на README.md
            if not link_href.endswith("README.md"):
                result["errors"].append({
                    "code": "E009",
                    "message": f"Ссылка в SSOT не на README.md: {link_href}",
                })

    # Проверка всех ссылок
    links = extract_links(content)

    for link in links:
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
                    result["errors"].append({
                        "code": "E004",
                        "message": f"Ссылка на папку без trailing slash: {href}",
                    })
            elif not resolved.exists():
                # Проверяем, это папка или файл
                if path_part.endswith("/"):
                    result["errors"].append({
                        "code": "E002",
                        "message": f"Папка не существует: {href}",
                    })
                else:
                    result["errors"].append({
                        "code": "E001",
                        "message": f"Файл не существует: {href}",
                    })
                continue  # Не проверяем якорь, если файл не существует

        # Шаг 3: Якорные ссылки
        if anchor:
            target_file = resolve_path(file_path, href, repo_root)
            if target_file.exists() and target_file.is_file():
                try:
                    target_content = target_file.read_text(encoding="utf-8")
                    headings = extract_headings(target_content)

                    if anchor not in headings:
                        # E003: Якорь не найден
                        result["errors"].append({
                            "code": "E003",
                            "message": f"Якорь не найден: {href}",
                        })

                        # W003: Похожий якорь
                        similar = similar_anchor(anchor, headings)
                        if similar:
                            result["warnings"].append({
                                "code": "W003",
                                "message": f"Похожий якорь существует: #{similar} (вместо #{anchor})",
                            })
                except Exception:
                    pass

        # Шаг 2: Формат пути
        if path_part:
            # W001: Абсолютный путь для файла в той же папке
            if path_part.startswith("/"):
                resolved = repo_root / path_part.lstrip("/")
                if resolved.parent == file_path.parent:
                    result["warnings"].append({
                        "code": "W001",
                        "message": f"Абсолютный путь для файла в той же папке: {href}",
                    })

            # W002: Длинная цепочка ../
            parent_count = path_part.count("../")
            if parent_count >= 3:
                result["warnings"].append({
                    "code": "W002",
                    "message": f"Длинная цепочка ../: {href}",
                })

    return result


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
                "errors": [{"code": "E000", "message": "Путь не существует"}],
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

    return result


def main():
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
