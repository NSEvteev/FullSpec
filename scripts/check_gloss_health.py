#!/usr/bin/env python3
"""
Скрипт проверки здоровья глоссария проекта.

Запуск:
    python scripts/check_gloss_health.py
    python scripts/check_gloss_health.py --verbose
    python scripts/check_gloss_health.py --warn-unused  # Предупреждать о неиспользуемых терминах

Что проверяет:
    1. Ссылки на глоссарий:
       - Все ли термины с иконкой 📖 существуют в glossary.md
       - Все ли ссылки на глоссарий корректны (файл и якорь)

    2. Битые ссылки на глоссарий:
       - Несуществующие термины
       - Некорректные якоря

    3. Неиспользуемые термины (опционально):
       - Термины в глоссарии, на которые нет ссылок в проекте

    4. Структура глоссария:
       - Наличие обязательных полей в определениях терминов
       - Корректность форматирования определений

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
from collections import defaultdict


# ============================================
# Константы и паттерны
# ============================================

# Паттерн для поиска ссылок на глоссарий: [📖 термин](путь/glossary.md#термин)
GLOSSARY_LINK_PATTERN = re.compile(r'\[📖\s+([^\]]+)\]\(([^)]+glossary\.md#([^)]+))\)')

# Паттерн для поиска определений терминов в глоссарии
# Формат: ## Термин или ### Термин
TERM_DEFINITION_PATTERN = re.compile(r'^#{2,3}\s+(.+)$')

# Путь к файлу глоссария
GLOSSARY_PATH = Path('general_docs/glossary.md')

# Директории для проверки ссылок на глоссарий
DOCS_DIRS = ['general_docs', 'llm_instructions', 'llm_tasks', 'apps', 'services', 'packages']

# Обязательные поля в определении термина
REQUIRED_TERM_FIELDS = [
    'Определение',
]


# ============================================
# Утилиты
# ============================================

class GlossaryHealthChecker:
    """Класс для проверки здоровья глоссария."""

    def __init__(self, root_dir: Path, verbose: bool = False, warn_unused: bool = False):
        self.root_dir = root_dir
        self.verbose = verbose
        self.warn_unused = warn_unused
        self.issues = defaultdict(list)
        self.glossary_terms = {}  # {якорь: (название_термина, номер_строки)}
        self.term_references = defaultdict(set)  # {якорь: set(файлы, где используется)}

    def log(self, message: str):
        """Вывод в verbose режиме."""
        if self.verbose:
            print(message)

    def add_issue(self, category: str, file_path: Path, line_num: int, message: str):
        """Добавить проблему."""
        if file_path:
            relative_path = file_path.relative_to(self.root_dir)
            self.issues[category].append({
                'file': str(relative_path),
                'line': line_num,
                'message': message
            })
        else:
            self.issues[category].append({
                'file': None,
                'line': line_num,
                'message': message
            })

    def print_results(self):
        """Вывести результаты проверки."""
        if not self.issues:
            print("✓ Глоссарий в порядке!")
            return 0

        print("✗ Найдены проблемы в глоссарии:\n")

        total_issues = 0
        for category, problems in sorted(self.issues.items()):
            print(f"{'='*60}")
            print(f"{category.upper()}")
            print(f"{'='*60}\n")

            for problem in problems:
                total_issues += 1
                if problem['file']:
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
# 1. Загрузка глоссария
# ============================================

def load_glossary(checker: GlossaryHealthChecker) -> Dict[str, Tuple[str, int]]:
    """Загрузить все термины из glossary.md. Возвращает {якорь: (название, номер_строки)}."""
    checker.log("Загрузка терминов из glossary.md...")

    glossary_path = checker.root_dir / GLOSSARY_PATH
    if not glossary_path.exists():
        checker.add_issue(
            'missing_glossary',
            None,
            0,
            f"Файл глоссария не найден: {GLOSSARY_PATH}"
        )
        return {}

    terms = {}
    with open(glossary_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            match = TERM_DEFINITION_PATTERN.match(line.strip())
            if match:
                term_name = match.group(1).strip()
                # Создаём якорь по правилам GitHub
                anchor = term_name.lower()
                anchor = re.sub(r'[^\w\s-]', '', anchor)
                anchor = re.sub(r'[\s]+', '-', anchor)
                anchor = anchor.strip('-')
                terms[anchor] = (term_name, line_num)

    checker.log(f"Найдено терминов в глоссарии: {len(terms)}")
    return terms


# ============================================
# 2. Проверка ссылок на глоссарий
# ============================================

def find_md_files(root_dir: Path, dirs: List[str]) -> List[Path]:
    """Найти все markdown-файлы в указанных директориях."""
    md_files = []
    for docs_dir in dirs:
        dir_path = root_dir / docs_dir
        if dir_path.exists():
            for file_path in dir_path.rglob('*.md'):
                # Пропускаем сам glossary.md
                if file_path.name != 'glossary.md':
                    md_files.append(file_path)
    return md_files


def extract_glossary_links(file_path: Path) -> List[Tuple[int, str, str, str]]:
    """Извлечь все ссылки на глоссарий из файла.
    Возвращает (номер_строки, название_термина, полный_путь, якорь)."""
    links = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            for match in GLOSSARY_LINK_PATTERN.finditer(line):
                term_name, full_path, anchor = match.groups()
                links.append((line_num, term_name.strip(), full_path, anchor))
    return links


def check_glossary_links(checker: GlossaryHealthChecker):
    """Проверить все ссылки на глоссарий."""
    checker.log("Проверка ссылок на глоссарий...")

    md_files = find_md_files(checker.root_dir, DOCS_DIRS)

    for file_path in md_files:
        links = extract_glossary_links(file_path)

        for line_num, term_name, full_path, anchor in links:
            # Проверяем, существует ли термин в глоссарии
            if anchor not in checker.glossary_terms:
                checker.add_issue(
                    'undefined_term',
                    file_path,
                    line_num,
                    f"Термин не найден в глоссарии: [📖 {term_name}](#{anchor})\n      "
                    f"Возможно, имелся в виду один из: {', '.join(list(checker.glossary_terms.keys())[:5])}"
                )
            else:
                # Добавляем в список использованных терминов
                checker.term_references[anchor].add(str(file_path.relative_to(checker.root_dir)))

            # Проверяем корректность пути к glossary.md
            source_dir = file_path.parent
            glossary_path = (source_dir / full_path.split('#')[0]).resolve()

            if not glossary_path.exists():
                checker.add_issue(
                    'broken_glossary_path',
                    file_path,
                    line_num,
                    f"Неверный путь к glossary.md: {full_path}"
                )


# ============================================
# 3. Проверка неиспользуемых терминов
# ============================================

def check_unused_terms(checker: GlossaryHealthChecker):
    """Проверить неиспользуемые термины в глоссарии."""
    if not checker.warn_unused:
        return

    checker.log("Проверка неиспользуемых терминов...")

    glossary_path = checker.root_dir / GLOSSARY_PATH

    for anchor, (term_name, line_num) in checker.glossary_terms.items():
        if anchor not in checker.term_references:
            checker.add_issue(
                'unused_term',
                glossary_path,
                line_num,
                f"Термин '{term_name}' не используется в проекте (якорь: #{anchor})"
            )


# ============================================
# 4. Проверка структуры определений
# ============================================

def check_term_definitions(checker: GlossaryHealthChecker):
    """Проверить структуру определений терминов."""
    checker.log("Проверка структуры определений...")

    glossary_path = checker.root_dir / GLOSSARY_PATH
    if not glossary_path.exists():
        return

    with open(glossary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Разбиваем на секции терминов
    term_sections = re.split(r'^#{2,3}\s+', content, flags=re.MULTILINE)[1:]  # Пропускаем преамбулу

    for i, section in enumerate(term_sections):
        lines = section.split('\n')
        term_name = lines[0].strip()

        # Проверяем наличие обязательных полей
        for required_field in REQUIRED_TERM_FIELDS:
            field_pattern = re.compile(rf'\*\*{re.escape(required_field)}:\*\*', re.IGNORECASE)
            if not field_pattern.search(section):
                # Находим номер строки термина
                term_line_num = None
                for anchor, (name, line_num) in checker.glossary_terms.items():
                    if name == term_name:
                        term_line_num = line_num
                        break

                checker.add_issue(
                    'incomplete_definition',
                    glossary_path,
                    term_line_num or 0,
                    f"Определение термина '{term_name}' не содержит обязательное поле '{required_field}'"
                )


# ============================================
# 5. Мониторинг размера глоссария
# ============================================

def check_glossary_size(checker: GlossaryHealthChecker):
    """Проверить размер глоссария и предупредить, если он становится слишком большим."""
    checker.log("Проверка размера глоссария...")

    glossary_path = checker.root_dir / GLOSSARY_PATH
    if not glossary_path.exists():
        return

    # Подсчитываем строки
    with open(glossary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        line_count = len(lines)

    # Подсчитываем термины
    term_count = len(checker.glossary_terms)

    # Пороги для предупреждения
    LINE_THRESHOLD = 1000
    TERM_THRESHOLD = 150

    # Проверяем пороги
    if line_count > LINE_THRESHOLD or term_count > TERM_THRESHOLD:
        message = (
            f"⚠️ Глоссарий становится большим:\n"
            f"      - Терминов: {term_count} (порог: {TERM_THRESHOLD})\n"
            f"      - Строк: {line_count} (порог: {LINE_THRESHOLD})\n"
            f"      \n"
            f"      Рекомендации:\n"
            f"      1. Создать дискуссию 'general_docs/discuss/XXX_glossary_split.md'\n"
            f"      2. Спроектировать структуру категорий\n"
            f"      3. Создать план миграции (обновление ссылок, скриптов, скиллов)\n"
            f"      \n"
            f"      См. instructions_general_docs.md для деталей."
        )
        checker.add_issue(
            'glossary_size_warning',
            glossary_path,
            0,
            message
        )
    else:
        checker.log(f"Размер глоссария в норме: {term_count} терминов, {line_count} строк")


# ============================================
# Главная функция
# ============================================

def main():
    """Основная функция проверки."""
    parser = argparse.ArgumentParser(description='Проверка здоровья глоссария')
    parser.add_argument('--verbose', '-v', action='store_true', help='Подробный вывод')
    parser.add_argument('--warn-unused', '-u', action='store_true',
                        help='Предупреждать о неиспользуемых терминах')
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    checker = GlossaryHealthChecker(root_dir, verbose=args.verbose, warn_unused=args.warn_unused)

    print(f"Проверка глоссария проекта")
    print(f"Корневая директория: {root_dir}")
    print(f"{'='*60}\n")

    # Загружаем глоссарий
    checker.glossary_terms = load_glossary(checker)

    if not checker.glossary_terms:
        print("✗ Глоссарий не найден или пуст!")
        return 1

    # Выполняем проверки
    check_glossary_links(checker)
    check_unused_terms(checker)
    check_term_definitions(checker)
    check_glossary_size(checker)

    # Вывод результатов
    return checker.print_results()


if __name__ == '__main__':
    sys.exit(main())
