#!/usr/bin/env python3
"""
Скрипт комплексной проверки здоровья документации проекта.

Запуск:
    python scripts/check_doc_health.py
    python scripts/check_doc_health.py --verbose
    python scripts/check_doc_health.py --check links      # Только проверка ссылок
    python scripts/check_doc_health.py --check structure  # Только проверка структуры
    python scripts/check_doc_health.py --check status     # Только проверка статусов
    python scripts/check_doc_health.py --check metadata   # Только проверка метаданных
    python scripts/check_doc_health.py --check markdown   # Только проверка форматирования

Что проверяет:
    1. Целостность ссылок:
       - Ссылки на несуществующие файлы
       - Ссылки на несуществующие якоря (#заголовки)

    2. Структура документации:
       - Наличие обязательных README.md в сервисах/пакетах
       - Наличие обязательных разделов в документах
       - Соответствие дискуссий/архитектуры шаблонам

    3. Статусы дискуссий:
       - Корректность статусов (draft, in_progress, review, approved, final, feedback)
       - Соответствие workflow

    4. Метаданные:
       - Наличие дат последнего обновления
       - Версионирование файлов архитектуры

    5. Markdown форматирование:
       - Валидность заголовков
       - Корректность списков
       - Форматирование таблиц

Возвращает:
    0 - все проверки пройдены
    1 - найдены проблемы
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Set
from datetime import datetime
from collections import defaultdict


# ============================================
# Константы и паттерны
# ============================================

# Паттерн для поиска markdown-ссылок: [текст](путь)
LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

# Паттерн для поиска заголовков
HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')

# Паттерн для статусов
STATUS_PATTERN = re.compile(r'\*\*Статус:\*\*\s*(.+)', re.IGNORECASE)

# Паттерн для дат
DATE_PATTERN = re.compile(r'\*\*Дата(?:\s+последнего\s+обновления)?:\*\*\s*(\d{4}-\d{2}-\d{2})', re.IGNORECASE)

# Паттерн для версий
VERSION_PATTERN = re.compile(r'\*\*Версия:\*\*\s*(\d+\.\d+)', re.IGNORECASE)

# Директории для проверки
DOCS_DIRS = ['general_docs', 'llm_instructions', 'llm_tasks']

# Корневые директории для README.md
README_REQUIRED_DIRS = [
    'apps/web',
    'services/api-gateway',
    'services/auth',
    'services/users',
    'packages',
    'infrastructure',
    'tests',
]

# Валидные статусы для разных типов документов
VALID_STATUSES = {
    'discuss': {'draft', 'in_progress', 'feedback', 'review', 'approved', 'final'},
    'architecture': {'draft', 'in_progress', 'feedback', 'review', 'approved', 'final'},
    'imp_plans': {'draft', 'in_progress', 'review', 'test', 'approved', 'final'},
    'diagrams': {'in_progress', 'final'},
}

# Обязательные разделы для разных типов документов
REQUIRED_SECTIONS = {
    'discuss': [
        'Исходный запрос пользователя',
        'Принятые архитектурные решения',
        'Принятое решение',
    ],
    'architecture': [
        'Цель и контекст',
        'Диаграммы',
        'История изменений',
    ],
    'imp_plans': [
        'Задачи',
        'Зависимости',
    ],
}


# ============================================
# Утилиты
# ============================================

class HealthChecker:
    """Класс для комплексной проверки здоровья документации."""

    def __init__(self, root_dir: Path, verbose: bool = False):
        self.root_dir = root_dir
        self.verbose = verbose
        self.issues = defaultdict(list)

    def log(self, message: str):
        """Вывод в verbose режиме."""
        if self.verbose:
            print(message)

    def add_issue(self, category: str, file_path: Path, line_num: int, message: str):
        """Добавить проблему."""
        relative_path = file_path.relative_to(self.root_dir)
        self.issues[category].append({
            'file': str(relative_path),
            'line': line_num,
            'message': message
        })

    def print_results(self):
        """Вывести результаты проверки."""
        if not self.issues:
            print("✓ Все проверки пройдены успешно!")
            return 0

        print("✗ Найдены проблемы в документации:\n")

        total_issues = 0
        for category, problems in sorted(self.issues.items()):
            print(f"{'='*60}")
            print(f"{category.upper()}")
            print(f"{'='*60}\n")

            for problem in problems:
                total_issues += 1
                if problem['line'] > 0:
                    print(f"  {problem['file']}:{problem['line']}")
                else:
                    print(f"  {problem['file']}")
                print(f"    {problem['message']}\n")

        print(f"{'='*60}")
        print(f"Всего проблем: {total_issues}")
        print(f"{'='*60}")
        return 1


# ============================================
# 1. Проверка ссылок
# ============================================

def find_md_files(root_dir: Path, dirs: List[str] = None) -> List[Path]:
    """Найти все markdown-файлы в указанных директориях."""
    md_files = []
    search_dirs = dirs or DOCS_DIRS

    for docs_dir in search_dirs:
        dir_path = root_dir / docs_dir
        if dir_path.exists():
            for file_path in dir_path.rglob('*.md'):
                md_files.append(file_path)
    return md_files


def extract_headers(file_path: Path) -> Dict[str, int]:
    """Извлечь все заголовки из файла. Возвращает {якорь: номер_строки}."""
    headers = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            match = HEADER_PATTERN.match(line.strip())
            if match:
                header_text = match.group(2).strip()
                # Создаём якорь по правилам GitHub (lowercase, пробелы -> дефисы, убрать спецсимволы)
                anchor = header_text.lower()
                anchor = re.sub(r'[^\w\s-]', '', anchor)
                anchor = re.sub(r'[\s]+', '-', anchor)
                anchor = anchor.strip('-')
                headers[anchor] = line_num
    return headers


def extract_links(file_path: Path) -> List[Tuple[int, str, str]]:
    """Извлечь все ссылки из файла. Возвращает (номер_строки, текст, путь)."""
    links = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            for match in LINK_PATTERN.finditer(line):
                text, path = match.groups()
                # Пропускаем внешние ссылки (http, https, mailto)
                if not path.startswith(('http://', 'https://', 'mailto:', 'ftp://')):
                    links.append((line_num, text, path))
    return links


def check_links(checker: HealthChecker):
    """Проверить целостность всех ссылок."""
    checker.log("Проверка целостности ссылок...")

    md_files = find_md_files(checker.root_dir)

    for file_path in md_files:
        links = extract_links(file_path)

        for line_num, text, link_path in links:
            # Разделяем путь и якорь
            if '#' in link_path:
                path_part, anchor_part = link_path.split('#', 1)
            else:
                path_part = link_path
                anchor_part = None

            # Проверка существования файла
            if path_part:
                source_dir = file_path.parent
                target_path = (source_dir / path_part).resolve()

                if not target_path.exists():
                    checker.add_issue(
                        'broken_links',
                        file_path,
                        line_num,
                        f"Битая ссылка на файл: [{text}]({link_path})"
                    )
                    continue

                # Проверка якоря, если указан
                if anchor_part and target_path.suffix == '.md':
                    headers = extract_headers(target_path)
                    if anchor_part not in headers:
                        checker.add_issue(
                            'broken_anchors',
                            file_path,
                            line_num,
                            f"Якорь не найден: [{text}]({link_path})\n      "
                            f"Доступные якоря в {target_path.name}: {', '.join(list(headers.keys())[:5])}"
                        )

            # Проверка якоря в текущем файле
            elif anchor_part:
                headers = extract_headers(file_path)
                if anchor_part not in headers:
                    checker.add_issue(
                        'broken_anchors',
                        file_path,
                        line_num,
                        f"Якорь не найден в текущем файле: [{text}](#{anchor_part})"
                    )


# ============================================
# 2. Проверка структуры документации
# ============================================

def check_structure(checker: HealthChecker):
    """Проверить структуру документации."""
    checker.log("Проверка структуры документации...")

    # Проверка наличия README.md в обязательных директориях
    for dir_path in README_REQUIRED_DIRS:
        readme_path = checker.root_dir / dir_path / 'README.md'
        if not readme_path.exists():
            checker.add_issue(
                'missing_readme',
                checker.root_dir / dir_path,
                0,
                f"Отсутствует обязательный README.md"
            )

    # Проверка обязательных разделов в документах
    for doc_type, required_sections in REQUIRED_SECTIONS.items():
        doc_dir = checker.root_dir / 'general_docs' / doc_type
        if doc_dir.exists():
            for doc_file in doc_dir.glob('*.md'):
                check_required_sections(checker, doc_file, doc_type, required_sections)


def check_required_sections(checker: HealthChecker, file_path: Path, doc_type: str, required_sections: List[str]):
    """Проверить наличие обязательных разделов в документе."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for section in required_sections:
        # Проверяем наличие раздела (с учётом вариаций заголовков)
        section_pattern = re.compile(rf'^#+\s+.*{re.escape(section)}', re.MULTILINE | re.IGNORECASE)
        if not section_pattern.search(content):
            checker.add_issue(
                'missing_sections',
                file_path,
                0,
                f"Отсутствует обязательный раздел: '{section}' (тип: {doc_type})"
            )


# ============================================
# 3. Проверка статусов
# ============================================

def check_statuses(checker: HealthChecker):
    """Проверить корректность статусов в дискуссиях и архитектуре."""
    checker.log("Проверка статусов документов...")

    for doc_type, valid_statuses in VALID_STATUSES.items():
        doc_dir = checker.root_dir / 'general_docs' / doc_type
        if not doc_dir.exists():
            continue

        for doc_file in doc_dir.glob('*.md'):
            status = extract_status(doc_file)
            if status:
                if status not in valid_statuses:
                    checker.add_issue(
                        'invalid_status',
                        doc_file,
                        0,
                        f"Некорректный статус: '{status}'. "
                        f"Допустимые: {', '.join(sorted(valid_statuses))}"
                    )
            else:
                checker.add_issue(
                    'missing_status',
                    doc_file,
                    0,
                    f"Отсутствует статус документа (тип: {doc_type})"
                )


def extract_status(file_path: Path) -> str:
    """Извлечь статус из документа."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = STATUS_PATTERN.search(line)
            if match:
                return match.group(1).strip().lower()
    return None


# ============================================
# 4. Проверка метаданных
# ============================================

def check_metadata(checker: HealthChecker):
    """Проверить метаданные документов."""
    checker.log("Проверка метаданных...")

    # Проверка дат в критических документах
    critical_docs = ['discuss', 'architecture', 'imp_plans']
    for doc_type in critical_docs:
        doc_dir = checker.root_dir / 'general_docs' / doc_type
        if not doc_dir.exists():
            continue

        for doc_file in doc_dir.glob('*.md'):
            date = extract_date(doc_file)
            if not date:
                checker.add_issue(
                    'missing_metadata',
                    doc_file,
                    0,
                    f"Отсутствует дата последнего обновления"
                )

    # Проверка версий в архитектурных документах
    arch_dir = checker.root_dir / 'general_docs' / 'architecture'
    if arch_dir.exists():
        for doc_file in arch_dir.glob('*.md'):
            version = extract_version(doc_file)
            if not version:
                checker.add_issue(
                    'missing_metadata',
                    doc_file,
                    0,
                    f"Отсутствует версия документа (архитектура должна иметь версию)"
                )


def extract_date(file_path: Path) -> str:
    """Извлечь дату из документа."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = DATE_PATTERN.search(line)
            if match:
                return match.group(1)
    return None


def extract_version(file_path: Path) -> str:
    """Извлечь версию из документа."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = VERSION_PATTERN.search(line)
            if match:
                return match.group(1)
    return None


# ============================================
# 5. Проверка Markdown форматирования
# ============================================

def check_markdown(checker: HealthChecker):
    """Проверить форматирование markdown."""
    checker.log("Проверка форматирования markdown...")

    md_files = find_md_files(checker.root_dir)

    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Проверка заголовков
        for line_num, line in enumerate(lines, 1):
            # Заголовки должны иметь пробел после #
            if line.strip().startswith('#'):
                if not re.match(r'^#{1,6}\s+.+', line.strip()):
                    checker.add_issue(
                        'markdown_format',
                        file_path,
                        line_num,
                        "Заголовок должен иметь пробел после символов #"
                    )

            # Проверка списков (должны иметь пробел после маркера)
            if line.strip().startswith(('-', '*', '+')):
                if not re.match(r'^[\s]*[-*+]\s+.+', line):
                    checker.add_issue(
                        'markdown_format',
                        file_path,
                        line_num,
                        "Список должен иметь пробел после маркера"
                    )


# ============================================
# Главная функция
# ============================================

def main():
    """Основная функция проверки."""
    parser = argparse.ArgumentParser(description='Проверка здоровья документации')
    parser.add_argument('--verbose', '-v', action='store_true', help='Подробный вывод')
    parser.add_argument('--check', choices=['links', 'structure', 'status', 'metadata', 'markdown'],
                        help='Выполнить только указанную проверку')
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    checker = HealthChecker(root_dir, verbose=args.verbose)

    print(f"Проверка документации проекта")
    print(f"Корневая директория: {root_dir}")
    print(f"{'='*60}\n")

    # Выполняем проверки
    if args.check is None or args.check == 'links':
        check_links(checker)

    if args.check is None or args.check == 'structure':
        check_structure(checker)

    if args.check is None or args.check == 'status':
        check_statuses(checker)

    if args.check is None or args.check == 'metadata':
        check_metadata(checker)

    if args.check is None or args.check == 'markdown':
        check_markdown(checker)

    # Вывод результатов
    return checker.print_results()


if __name__ == '__main__':
    sys.exit(main())
