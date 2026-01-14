#!/usr/bin/env python3
"""
Скрипт проверки целостности ссылок в markdown-документации.

Запуск:
    python scripts/check_doc_links.py

Что проверяет:
    - Относительные ссылки на файлы [текст](путь/к/файлу.md)
    - Якорные ссылки [текст](файл.md#раздел)
    - Ссылки на изображения и диаграммы

Возвращает:
    0 - все ссылки валидны
    1 - найдены битые ссылки
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


# Паттерн для поиска markdown-ссылок: [текст](путь)
LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

# Директории для проверки
DOCS_DIRS = ['general_docs', 'llm_instructions']

# Расширения файлов для проверки
MD_EXTENSIONS = {'.md'}


def find_md_files(root_dir: Path) -> List[Path]:
    """Найти все markdown-файлы в директории."""
    md_files = []
    for docs_dir in DOCS_DIRS:
        dir_path = root_dir / docs_dir
        if dir_path.exists():
            for file_path in dir_path.rglob('*.md'):
                md_files.append(file_path)
    return md_files


def extract_links(file_path: Path) -> List[Tuple[int, str, str]]:
    """Извлечь все ссылки из файла. Возвращает (номер_строки, текст, путь)."""
    links = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            for match in LINK_PATTERN.finditer(line):
                text, path = match.groups()
                # Пропускаем внешние ссылки (http, https, mailto)
                if not path.startswith(('http://', 'https://', 'mailto:')):
                    links.append((line_num, text, path))
    return links


def check_link(source_file: Path, link_path: str, root_dir: Path) -> bool:
    """Проверить, существует ли файл по ссылке."""
    # Убираем якорь (#section) если есть
    path_without_anchor = link_path.split('#')[0]

    if not path_without_anchor:
        # Ссылка только на якорь в текущем файле
        return True

    # Разрешаем относительный путь от файла-источника
    source_dir = source_file.parent
    target_path = (source_dir / path_without_anchor).resolve()

    return target_path.exists()


def main():
    """Основная функция проверки."""
    root_dir = Path(__file__).parent.parent

    print(f"Проверка ссылок в документации...")
    print(f"Корневая директория: {root_dir}")
    print()

    md_files = find_md_files(root_dir)
    print(f"Найдено markdown-файлов: {len(md_files)}")
    print()

    broken_links = []

    for file_path in md_files:
        links = extract_links(file_path)
        for line_num, text, link_path in links:
            if not check_link(file_path, link_path, root_dir):
                relative_file = file_path.relative_to(root_dir)
                broken_links.append((relative_file, line_num, text, link_path))

    if broken_links:
        print("ОШИБКА: Найдены битые ссылки:")
        print()
        for file_path, line_num, text, link_path in broken_links:
            print(f"  {file_path}:{line_num}")
            print(f"    [{text}]({link_path})")
            print()
        print(f"Всего битых ссылок: {len(broken_links)}")
        return 1
    else:
        print("OK: Все ссылки валидны.")
        return 0


if __name__ == '__main__':
    sys.exit(main())
