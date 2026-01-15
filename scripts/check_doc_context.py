#!/usr/bin/env python3
"""
Скрипт агрегации документации в единый контекст для LLM анализа.

Быстро собирает все данные из .md файлов и формирует структурированный JSON
для глубокого смыслового анализа через Amy Santiago.

Использование:
    python scripts/check_doc_context.py
    python scripts/check_doc_context.py --output custom_path.json
    python scripts/check_doc_context.py --verbose

Результат:
    JSON файл в llm_tasks/temp/doc_context.json
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
from collections import defaultdict


# Паттерны для извлечения данных
LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')
STATUS_PATTERN = re.compile(r'\*\*Статус:\*\*\s*(.+)', re.IGNORECASE)
DATE_PATTERN = re.compile(r'\*\*Дата(?:\s+последнего\s+обновления)?:\*\*\s*(\d{4}-\d{2}-\d{2})', re.IGNORECASE)
VERSION_PATTERN = re.compile(r'\*\*Версия:\*\*\s*(\d+\.\d+)', re.IGNORECASE)
FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

# Директории для проверки
DOCS_DIRS = [
    'general_docs',        # Общая документация проекта
    'llm_instructions',    # Инструкции для LLM
    'llm_tasks',           # Задачи (current, future, completed)
    '.claude/agents',      # Описания агентов
    '.claude/skills'       # Скиллы Claude Code
]

# Корневые файлы для проверки
ROOT_DOCS = [
    'README.md',
    'CLAUDE.md',
    'CONTRIBUTING.md'
]


class DocumentationAggregator:
    """Класс для агрегации документации проекта."""

    def __init__(self, root_dir: Path, verbose: bool = False):
        self.root_dir = root_dir
        self.verbose = verbose

    def log(self, message: str):
        """Вывод в verbose режиме."""
        if self.verbose:
            print(message)

    def aggregate(self) -> Dict:
        """Собрать всю документацию в единый контекст."""
        self.log("📦 Начало агрегации документации...")

        context = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "root_dir": str(self.root_dir),
                "total_files": 0,
                "total_size_kb": 0
            },
            "documents": [],
            "glossary": {
                "terms": [],
                "categories": {},
                "total_count": 0
            },
            "dependency_graph": {
                "nodes": [],
                "edges": [],
                "chains": []
            },
            "links": {
                "internal": [],
                "external": [],
                "broken": []
            },
            "statistics": {
                "by_type": defaultdict(int),
                "by_status": defaultdict(int),
                "by_folder": defaultdict(int),
                "total_words": 0,
                "total_lines": 0
            }
        }

        # 1. Собрать все документы
        self.log("📄 Сбор документов...")
        md_files = self._find_md_files()
        context["metadata"]["total_files"] = len(md_files)

        for file_path in md_files:
            doc = self._extract_document_info(file_path)
            context["documents"].append(doc)

            # Обновить статистику
            self._update_statistics(context["statistics"], doc)

        self.log(f"   Найдено файлов: {len(md_files)}")

        # 2. Извлечь глоссарий
        self.log("📖 Извлечение глоссария...")
        glossary_file = self.root_dir / 'general_docs' / 'glossary.md'
        if glossary_file.exists():
            context["glossary"] = self._extract_glossary(glossary_file)
            self.log(f"   Терминов в глоссарии: {context['glossary']['total_count']}")

        # 3. Построить граф зависимостей
        self.log("🔗 Построение графа зависимостей...")
        context["dependency_graph"] = self._build_dependency_graph(context["documents"])
        self.log(f"   Узлов: {len(context['dependency_graph']['nodes'])}")
        self.log(f"   Связей: {len(context['dependency_graph']['edges'])}")
        self.log(f"   Цепочек: {len(context['dependency_graph']['chains'])}")

        # 4. Собрать все ссылки
        self.log("🔗 Анализ ссылок...")
        context["links"] = self._extract_all_links(context["documents"])
        self.log(f"   Внутренних ссылок: {len(context['links']['internal'])}")
        self.log(f"   Битых ссылок: {len(context['links']['broken'])}")

        # 5. Подсчитать размер
        total_size = sum(f.stat().st_size for f in md_files)
        context["metadata"]["total_size_kb"] = round(total_size / 1024, 2)

        # Конвертировать defaultdict в dict для JSON
        context["statistics"]["by_type"] = dict(context["statistics"]["by_type"])
        context["statistics"]["by_status"] = dict(context["statistics"]["by_status"])
        context["statistics"]["by_folder"] = dict(context["statistics"]["by_folder"])

        self.log("✅ Агрегация завершена")
        return context

    def _find_md_files(self) -> List[Path]:
        """Найти все markdown-файлы."""
        md_files = []

        # 1. Собрать файлы из директорий
        for docs_dir in DOCS_DIRS:
            dir_path = self.root_dir / docs_dir
            if dir_path.exists():
                for file_path in dir_path.rglob('*.md'):
                    md_files.append(file_path)

        # 2. Добавить корневые файлы
        for root_file in ROOT_DOCS:
            file_path = self.root_dir / root_file
            if file_path.exists():
                md_files.append(file_path)

        return md_files

    def _extract_document_info(self, file_path: Path) -> Dict:
        """Извлечь информацию из документа."""
        relative_path = file_path.relative_to(self.root_dir)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        return {
            "path": str(relative_path).replace('\\', '/'),
            "type": self._detect_document_type(relative_path),
            "title": self._extract_title(lines),
            "status": self._extract_status(content),
            "date": self._extract_date(content),
            "version": self._extract_version(content),
            "headers": self._extract_headers_list(lines),
            "links": self._extract_document_links(content, file_path),
            "word_count": len(content.split()),
            "line_count": len(lines),
            "has_frontmatter": bool(FRONTMATTER_PATTERN.search(content))
        }

    def _detect_document_type(self, path: Path) -> str:
        """Определить тип документа по пути."""
        path_str = str(path).replace('\\', '/')

        # Корневые файлы (приоритет выше, чем README.md в подпапках)
        if path.name == 'README.md' and path.parent == self.root_dir:
            return 'root_readme'
        elif path.name == 'CLAUDE.md':
            return 'root_claude'
        elif path.name == 'CONTRIBUTING.md':
            return 'root_contributing'

        # Агенты и скиллы
        elif '.claude/agents' in path_str:
            return 'agent'
        elif '.claude/skills' in path_str:
            return 'skill'

        # Общая документация (general_docs)
        elif '01_discuss' in path_str:
            return 'discuss'
        elif '02_architecture' in path_str:
            return 'architecture'
        elif '03_diagrams' in path_str:
            return 'diagram'
        elif '04_decisions' in path_str:
            return 'decision'
        elif '05_resources' in path_str:
            return 'resource'
        elif '06_imp_plans' in path_str:
            return 'imp_plan'
        elif 'glossary.md' in path_str:
            return 'glossary'

        # Инструкции и задачи
        elif 'llm_instructions' in path_str:
            return 'instruction'
        elif 'llm_tasks' in path_str:
            return 'task'

        # README в подпапках
        elif path.name == 'README.md':
            return 'readme'
        else:
            return 'other'

    def _extract_title(self, lines: List[str]) -> str:
        """Извлечь заголовок документа (первый # заголовок)."""
        for line in lines[:20]:  # Смотрим только первые 20 строк
            match = HEADER_PATTERN.match(line.strip())
            if match and match.group(1) == '#':
                return match.group(2).strip()
        return "Без заголовка"

    def _extract_status(self, content: str) -> Optional[str]:
        """Извлечь статус из документа."""
        match = STATUS_PATTERN.search(content)
        if match:
            return match.group(1).strip().lower()
        return None

    def _extract_date(self, content: str) -> Optional[str]:
        """Извлечь дату из документа."""
        match = DATE_PATTERN.search(content)
        if match:
            return match.group(1)
        return None

    def _extract_version(self, content: str) -> Optional[str]:
        """Извлечь версию из документа."""
        match = VERSION_PATTERN.search(content)
        if match:
            return match.group(1)
        return None

    def _extract_headers_list(self, lines: List[str]) -> List[Dict]:
        """Извлечь список всех заголовков."""
        headers = []
        for line_num, line in enumerate(lines, 1):
            match = HEADER_PATTERN.match(line.strip())
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headers.append({
                    "level": level,
                    "text": text,
                    "line": line_num
                })
        return headers

    def _extract_document_links(self, content: str, file_path: Path) -> List[Dict]:
        """Извлечь все ссылки из документа."""
        links = []
        for match in LINK_PATTERN.finditer(content):
            text, path = match.groups()

            # Определяем тип ссылки
            is_external = path.startswith(('http://', 'https://', 'mailto:', 'ftp://'))

            link_info = {
                "text": text,
                "target": path,
                "is_external": is_external
            }

            # Проверяем существование внутренних ссылок
            if not is_external:
                link_info["exists"] = self._check_link_exists(path, file_path)

            links.append(link_info)

        return links

    def _check_link_exists(self, link_path: str, source_file: Path) -> bool:
        """Проверить существование ссылки."""
        # Разделяем путь и якорь
        if '#' in link_path:
            path_part = link_path.split('#')[0]
        else:
            path_part = link_path

        if not path_part:  # Якорь в текущем файле
            return True

        # Проверяем существование файла
        source_dir = source_file.parent
        target_path = (source_dir / path_part).resolve()

        return target_path.exists()

    def _update_statistics(self, stats: Dict, doc: Dict):
        """Обновить статистику."""
        stats["by_type"][doc["type"]] += 1

        if doc["status"]:
            stats["by_status"][doc["status"]] += 1

        # Статистика по папкам
        folder = str(Path(doc["path"]).parts[0]) if Path(doc["path"]).parts else "root"
        stats["by_folder"][folder] += 1

        stats["total_words"] += doc["word_count"]
        stats["total_lines"] += doc["line_count"]

    def _extract_glossary(self, glossary_file: Path) -> Dict:
        """Извлечь термины из глоссария."""
        glossary = {
            "terms": [],
            "categories": {},
            "total_count": 0
        }

        with open(glossary_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        current_category = None
        current_term = None

        for line in lines:
            # Определяем категорию (## Категория)
            if line.startswith('## ') and not line.startswith('## '):
                category_name = line[3:].strip()
                if category_name not in ['Свойства Глоссария', 'Требования к глоссарию',
                                        'Пример описания термина', 'Содержание', 'Кандидаты', 'Примеры']:
                    current_category = category_name
                    glossary["categories"][current_category] = []

            # Определяем термин (### Термин)
            elif line.startswith('### '):
                term_name = line[4:].strip()
                current_term = {
                    "name": term_name,
                    "category": current_category or "Без категории"
                }
                glossary["terms"].append(current_term)

                if current_category:
                    glossary["categories"][current_category].append(term_name)

        glossary["total_count"] = len(glossary["terms"])
        return glossary

    def _build_dependency_graph(self, documents: List[Dict]) -> Dict:
        """Построить граф зависимостей между документами."""
        graph = {
            "nodes": [],
            "edges": [],
            "chains": []
        }

        # Создаём индекс документов по пути
        doc_index = {doc["path"]: doc for doc in documents}

        # Узлы = документы определённых типов
        important_types = ["discuss", "architecture", "decision", "resource", "imp_plan"]
        for doc in documents:
            if doc["type"] in important_types:
                graph["nodes"].append({
                    "id": doc["path"],
                    "type": doc["type"],
                    "title": doc["title"],
                    "status": doc["status"]
                })

        # Рёбра = ссылки между документами
        for doc in documents:
            for link in doc["links"]:
                if not link["is_external"] and link.get("exists"):
                    # Нормализуем путь ссылки
                    target_path = self._normalize_link_path(link["target"], doc["path"])

                    if target_path in doc_index:
                        graph["edges"].append({
                            "from": doc["path"],
                            "to": target_path,
                            "type": "reference"
                        })

        # Определить цепочки зависимостей
        graph["chains"] = self._detect_dependency_chains(graph, doc_index)

        return graph

    def _normalize_link_path(self, link: str, source_path: str) -> str:
        """Нормализовать путь ссылки относительно корня проекта."""
        # Убираем якорь
        if '#' in link:
            link = link.split('#')[0]

        if not link:
            return source_path

        # Строим абсолютный путь
        source_dir = Path(source_path).parent
        target = (source_dir / link).as_posix()

        # Нормализуем
        parts = []
        for part in target.split('/'):
            if part == '..':
                if parts:
                    parts.pop()
            elif part and part != '.':
                parts.append(part)

        return '/'.join(parts)

    def _detect_dependency_chains(self, graph: Dict, doc_index: Dict) -> List[Dict]:
        """Обнаружить цепочки зависимостей."""
        chains = []

        # Ищем цепочки начиная с discuss
        discuss_nodes = [n for n in graph["nodes"] if n["type"] == "discuss"]

        for discuss in discuss_nodes:
            chain = self._build_chain_from_node(discuss["id"], graph, doc_index)
            if len(chain["path"]) > 1:
                chains.append(chain)

        return chains

    def _build_chain_from_node(self, start_node: str, graph: Dict, doc_index: Dict) -> Dict:
        """Построить цепочку от узла."""
        chain = {
            "start": start_node,
            "path": [start_node],
            "complete": False,
            "missing_links": []
        }

        current = start_node
        visited = {current}
        expected_sequence = ["discuss", "architecture", "decision", "resource", "imp_plan"]

        while current:
            # Найти следующий узел в цепочке
            next_node = None
            current_type = doc_index.get(current, {}).get("type")

            if current_type in expected_sequence:
                current_idx = expected_sequence.index(current_type)
                if current_idx + 1 < len(expected_sequence):
                    next_type = expected_sequence[current_idx + 1]

                    # Ищем исходящее ребро к документу нужного типа
                    for edge in graph["edges"]:
                        if edge["from"] == current and edge["to"] not in visited:
                            target_type = doc_index.get(edge["to"], {}).get("type")
                            if target_type == next_type:
                                next_node = edge["to"]
                                break

                    if not next_node:
                        chain["missing_links"].append({
                            "after": current,
                            "expected_type": next_type
                        })

            if next_node:
                chain["path"].append(next_node)
                visited.add(next_node)
                current = next_node
            else:
                break

        # Проверяем полноту цепочки
        if len(chain["path"]) == len(expected_sequence):
            chain["complete"] = True

        return chain

    def _extract_all_links(self, documents: List[Dict]) -> Dict:
        """Собрать все ссылки."""
        links = {
            "internal": [],
            "external": [],
            "broken": []
        }

        for doc in documents:
            for link in doc["links"]:
                link_info = {
                    "source": doc["path"],
                    "text": link["text"],
                    "target": link["target"]
                }

                if link["is_external"]:
                    links["external"].append(link_info)
                else:
                    links["internal"].append(link_info)

                    if not link.get("exists"):
                        links["broken"].append(link_info)

        return links


def save_context(context: Dict, output_path: Path, verbose: bool = False):
    """Сохранить контекст в файл."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)

    if verbose:
        print(f"\n💾 Контекст сохранён: {output_path}")


def print_summary(context: Dict):
    """Вывести сводку по собранному контексту."""
    print(f"\n📊 Сводка по документации:")
    print(f"   Всего файлов: {context['metadata']['total_files']}")
    print(f"   Общий размер: {context['metadata']['total_size_kb']} KB")
    print(f"   Всего слов: {context['statistics']['total_words']:,}")
    print(f"   Всего строк: {context['statistics']['total_lines']:,}")

    print(f"\n📁 По типам документов:")
    for doc_type, count in sorted(context['statistics']['by_type'].items()):
        print(f"   {doc_type}: {count}")

    print(f"\n📖 Глоссарий:")
    print(f"   Всего терминов: {context['glossary']['total_count']}")
    for category, terms in context['glossary']['categories'].items():
        print(f"   {category}: {len(terms)}")

    print(f"\n🔗 Граф зависимостей:")
    print(f"   Узлов: {len(context['dependency_graph']['nodes'])}")
    print(f"   Связей: {len(context['dependency_graph']['edges'])}")
    print(f"   Цепочек: {len(context['dependency_graph']['chains'])}")

    complete_chains = sum(1 for c in context['dependency_graph']['chains'] if c['complete'])
    if context['dependency_graph']['chains']:
        print(f"   Полных цепочек: {complete_chains}/{len(context['dependency_graph']['chains'])}")

    print(f"\n🔗 Ссылки:")
    print(f"   Внутренних: {len(context['links']['internal'])}")
    print(f"   Внешних: {len(context['links']['external'])}")
    print(f"   Битых: {len(context['links']['broken'])}")


def main():
    """Главная функция."""
    # Установка UTF-8 для вывода в консоль (для Windows)
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        if sys.stderr:
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    parser = argparse.ArgumentParser(description='Агрегация документации в единый контекст')
    parser.add_argument('--output', '-o', help='Путь для сохранения контекста')
    parser.add_argument('--verbose', '-v', action='store_true', help='Подробный вывод')
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent

    # Создаём агрегатор
    aggregator = DocumentationAggregator(root_dir, verbose=args.verbose)

    # Собираем контекст
    context = aggregator.aggregate()

    # Определяем путь для сохранения
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = root_dir / 'llm_tasks' / 'temp' / 'doc_context.json'

    # Сохраняем
    save_context(context, output_path, verbose=args.verbose)

    # Выводим сводку
    print_summary(context)

    print(f"\n✅ Готово! Контекст сохранён в: {output_path.relative_to(root_dir)}")
    print(f"\nСледующий шаг: запустить глубокий аудит через Amy")
    print(f"Команда: make docs-check-deep")


if __name__ == '__main__':
    main()
