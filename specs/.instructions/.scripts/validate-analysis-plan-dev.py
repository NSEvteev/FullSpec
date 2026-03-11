#!/usr/bin/env python3
"""
validate-analysis-plan-dev.py — Валидация документов плана разработки SDD.

Проверяет соответствие документа плана разработки стандарту standard-plan-dev.md.

Использование:
    python validate-analysis-plan-dev.py <path> [--json] [--all] [--repo <dir>]

Примеры:
    python validate-analysis-plan-dev.py specs/analysis/0001-oauth2-authorization/plan-dev.md
    python validate-analysis-plan-dev.py --all
    python validate-analysis-plan-dev.py --json specs/analysis/0001-oauth2-authorization/plan-dev.md

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

FOLDER_REGEX = re.compile(r'^(\d{4})-.+$')
HEADING_SUFFIX_REGEX = re.compile(r'—\s*Plan Dev\s*$')

VALID_STATUSES = {
    "DRAFT", "WAITING", "RUNNING", "REVIEW", "DONE",
    "CONFLICT", "ROLLING_BACK", "REJECTED",
}

REQUIRED_STANDARD = "specs/.instructions/analysis/plan-dev/standard-plan-dev.md"
REQUIRED_INDEX = "specs/analysis/README.md"
STANDARD_VERSION_REGEX = re.compile(r'^v\d+\.\d+$')

TASK_HEADING_PATTERN = re.compile(r'^####\s+TASK-(\d+):\s+(.+)$', re.MULTILINE)
COMPLEXITY_PATTERN = re.compile(r'\*\*Сложность:\*\*\s*(\d+)/10')
PRIORITY_PATTERN = re.compile(r'\*\*Приоритет:\*\*\s*(high|medium|low)', re.IGNORECASE)
DEPS_PATTERN = re.compile(r'\*\*Зависимости:\*\*\s*(.+)')
TC_FIELD_PATTERN = re.compile(r'\*\*TC:\*\*\s*(.+)')
SOURCE_PATTERN = re.compile(r'\*\*Источник:\*\*\s*(.+)')
TYPE_PATTERN = re.compile(r'\*\*Type:\*\*\s*(.+)')

SUBTASK_PATTERN = re.compile(r'^- \[[ x]\]\s+(\d+)\.(\d+)\.\s+(.+)$', re.MULTILINE)
SUBTASK_DEPS_PATTERN = re.compile(r'\(deps:\s*([^)]+)\)')

VALID_PRIORITIES = {"high", "medium", "low"}
VALID_TYPES = {"feature", "task", "infra", "test"}

ERROR_CODES = {
    "PD001": "Неверное расположение файла",
    "PD002": "Отсутствует description",
    "PD003": "Неверный standard",
    "PD004": "Невалидный status",
    "PD005": "Отсутствует parent",
    "PD006": "Parent Plan Tests не существует",
    "PD007": "Milestone не совпадает с parent",
    "PD008": "Запрещённое поле children",
    "PD009": "Отсутствует Резюме",
    "PD010": "Нет per-service раздела",
    "PD011": "Нет Задачи в per-service",
    "PD012": "Нет TASK-N в per-service",
    "PD013": "Невалидная Сложность",
    "PD014": "Невалидный Приоритет",
    "PD015": "Отсутствует поле TASK-N",
    "PD016": "Нет TC-N",
    "PD017": "Невалидный Источник",
    "PD018": "Дублирование TASK-N",
    "PD019": "1 подзадача в блоке",
    "PD020": "Неверная нотация подзадачи",
    "PD021": "Кросс-задачная зависимость в подзадаче",
    "PD022": "Нет Кросс-сервисные зависимости",
    "PD023": "Нет Маппинг GitHub Issues",
    "PD024": "NNNN не совпадает",
    "PD025": "Description слишком длинное",
    "PD026": "Циклическая зависимость",
    "PD027": "Задача перед зависимостью",
    "PD028": "INFRA превышает 20%",
    "PD029": "Маркер при статусе > DRAFT",
    "PD030": "Кросс-зависимость не в таблице",
    "PD031": "Нет Блоки выполнения",
    "PD032": "TASK-N без BLOCK-N",
    "PD033": "Циклическая зависимость BLOCK-N",
    "PD034": "File overlap в волне",
    "PD035": "INFRA-блок не в первой волне",
    "PD036": "BLOCK-N не совпадает с plan-test",
    "PD037": "Нет Предложения",
    "PD038": "Нет Отвергнутые предложения",
    "PD039": "Невалидный Type",
    "PD040": "Тестовые TC объединены без причины",
}


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


def parse_frontmatter(content: str) -> dict:
    """Извлечь frontmatter из markdown."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    result = {}
    current_key = None
    list_values = []

    for line in match.group(1).split('\n'):
        if line.strip().startswith('- ') and current_key:
            list_values.append(line.strip()[2:])
            result[current_key] = list_values
            continue

        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if value == '[]':
                result[key] = []
                current_key = key
                list_values = []
            elif value == '' or value is None:
                current_key = key
                list_values = []
                result[key] = value
            else:
                result[key] = value
                current_key = key
                list_values = []

    return result


def remove_code_blocks(content: str) -> str:
    """Убрать блоки кода из содержимого."""
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', '', content)
    return content


def get_body(content: str) -> str:
    """Получить тело документа без frontmatter."""
    return re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)


def split_sections(body: str) -> list[tuple[str, str]]:
    """Разбить body на секции h2. Возвращает [(heading, content), ...]."""
    parts = re.split(r'^(## .+)$', body, flags=re.MULTILINE)
    sections = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((heading, content))
    return sections


# =============================================================================
# Проверки
# =============================================================================

def check_location(path: Path) -> list[tuple[str, str]]:
    """PD001: Проверить расположение файла."""
    errors = []

    if path.name != "plan-dev.md":
        errors.append(("PD001", f"Имя файла '{path.name}', ожидается 'plan-dev.md'"))
        return errors

    parent_name = path.parent.name
    if not FOLDER_REGEX.match(parent_name):
        errors.append(("PD001", f"Папка '{parent_name}' не соответствует формату NNNN-{{topic}}"))

    return errors


def check_frontmatter(content: str, path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """PD002-PD008, PD025: Проверить frontmatter."""
    errors = []

    if not content.startswith("---\n"):
        errors.append(("PD002", "Отсутствует frontmatter"))
        return errors

    fm = parse_frontmatter(content)

    # PD002: description
    desc = fm.get("description", "")
    if not desc:
        errors.append(("PD002", "Отсутствует поле description"))
    elif len(desc) > 1024:
        errors.append(("PD025", f"Description {len(desc)} символов (макс. 1024)"))

    # PD003: standard
    standard = fm.get("standard", "")
    if standard != REQUIRED_STANDARD:
        errors.append(("PD003", f"standard = '{standard}', ожидается '{REQUIRED_STANDARD}'"))

    # standard-version
    sv = fm.get("standard-version", "")
    if not sv:
        errors.append(("PD003", "Отсутствует поле standard-version"))
    elif not STANDARD_VERSION_REGEX.match(sv):
        errors.append(("PD003", f"standard-version = '{sv}', ожидается формат vX.Y"))

    # PD004: status
    status = fm.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(("PD004", f"status = '{status}', допустимые: {', '.join(sorted(VALID_STATUSES))}"))

    # index
    index = fm.get("index", "")
    if index != REQUIRED_INDEX:
        errors.append(("PD003", f"index = '{index}', ожидается '{REQUIRED_INDEX}'"))

    # PD005: parent
    parent = fm.get("parent", "")
    if not parent:
        errors.append(("PD005", "Отсутствует поле parent (Plan Tests обязателен)"))
    else:
        # PD006: parent exists
        parent_path = path.parent / parent
        if not parent_path.exists():
            errors.append(("PD006", f"Parent Plan Tests не найден: {parent}"))

    # PD008: children запрещён
    if "children" in fm:
        errors.append(("PD008", "Поле children запрещено (Plan Dev — терминальный объект)"))

    # milestone
    milestone = fm.get("milestone", "")
    if not milestone:
        errors.append(("PD007", "Отсутствует поле milestone"))

    return errors


def check_heading(content: str, path: Path) -> list[tuple[str, str]]:
    """PD024: Проверить совпадение NNNN и суффикс — Plan Dev."""
    errors = []

    folder_match = FOLDER_REGEX.match(path.parent.name)
    if not folder_match:
        return errors

    folder_nnnn = folder_match.group(1)
    body = get_body(content)

    # Ищем заголовок h1
    h1_match = re.search(r'^# (.+)$', body, re.MULTILINE)
    if not h1_match:
        errors.append(("PD024", "Заголовок '# NNNN: Тема — Plan Dev' не найден"))
        return errors

    h1_text = h1_match.group(1).strip()

    # Проверяем суффикс
    if not HEADING_SUFFIX_REGEX.search(h1_text):
        errors.append(("PD024", "Заголовок не заканчивается на '— Plan Dev'"))

    # Проверяем NNNN
    nnnn_match = re.match(r'^(\d{4}):', h1_text)
    if nnnn_match:
        heading_nnnn = nnnn_match.group(1)
        if folder_nnnn != heading_nnnn:
            errors.append(("PD024", f"NNNN в папке ({folder_nnnn}) ≠ NNNN в заголовке ({heading_nnnn})"))
    else:
        errors.append(("PD024", "NNNN не найден в заголовке"))

    return errors


def check_required_sections(content: str) -> list[tuple[str, str]]:
    """PD009, PD010, PD022, PD023: Проверить обязательные разделы."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)
    sections = split_sections(body_no_code)
    headings = [h for h, _ in sections]

    # PD009: Резюме
    if not any("Резюме" in h for h in headings):
        errors.append(("PD009", "Отсутствует раздел '## Резюме'"))

    # PD022: Кросс-сервисные зависимости
    if not any("Кросс-сервисные зависимости" in h for h in headings):
        errors.append(("PD022", "Отсутствует раздел '## Кросс-сервисные зависимости'"))

    # PD023: Маппинг GitHub Issues
    if not any("Маппинг GitHub Issues" in h for h in headings):
        errors.append(("PD023", "Отсутствует раздел '## Маппинг GitHub Issues'"))

    # PD031: Блоки выполнения
    if not any("Блоки выполнения" in h for h in headings):
        errors.append(("PD031", "Отсутствует раздел '## Блоки выполнения'"))

    # PD037: Предложения
    if not any(h == "## Предложения" for h in headings):
        errors.append(("PD037", "Отсутствует раздел '## Предложения'"))

    # PD038: Отвергнутые предложения
    if not any("Отвергнутые предложения" in h for h in headings):
        errors.append(("PD038", "Отсутствует раздел '## Отвергнутые предложения'"))

    # PD010: per-service разделы
    special = {"Резюме", "Кросс-сервисные зависимости", "Маппинг GitHub Issues", "Блоки выполнения", "Предложения", "Отвергнутые предложения"}
    per_service = [h for h in headings if not any(s in h for s in special)]
    if not per_service:
        errors.append(("PD010", "Нет ни одного per-service раздела"))

    return errors


def check_per_service_sections(content: str) -> list[tuple[str, str]]:
    """PD011, PD012: Проверить подсекции per-service разделов."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)
    sections = split_sections(body_no_code)

    special = {"Резюме", "Кросс-сервисные зависимости", "Маппинг GitHub Issues", "Блоки выполнения", "Предложения", "Отвергнутые предложения"}

    for heading, section_content in sections:
        if any(s in heading for s in special):
            continue

        svc_match = re.match(r'## (SVC-\d+:\s*.+)', heading)
        if svc_match:
            service_name = svc_match.group(1).strip()
        else:
            service_name = heading.replace("## ", "").strip()

        # PD011: Задачи
        if "### Задачи" not in section_content:
            errors.append(("PD011", f"Сервис '{service_name}': нет подсекции 'Задачи'"))

        # PD012: хотя бы одна TASK-N
        tasks = TASK_HEADING_PATTERN.findall(section_content)
        if not tasks:
            errors.append(("PD012", f"Сервис '{service_name}': нет ни одной TASK-N"))

    return errors


def extract_tasks(content: str) -> list[dict]:
    """Извлечь все TASK-N из документа с позициями."""
    body = get_body(content)
    body_no_code = remove_code_blocks(body)

    tasks = []
    task_positions = list(TASK_HEADING_PATTERN.finditer(body_no_code))

    for i, match in enumerate(task_positions):
        task_num = int(match.group(1))
        task_name = match.group(2).strip()
        start = match.end()
        end = task_positions[i + 1].start() if i + 1 < len(task_positions) else len(body_no_code)
        block = body_no_code[start:end]

        # Извлечь поля
        complexity_match = COMPLEXITY_PATTERN.search(block)
        priority_match = PRIORITY_PATTERN.search(block)
        deps_match = DEPS_PATTERN.search(block)
        tc_match = TC_FIELD_PATTERN.search(block)
        source_match = SOURCE_PATTERN.search(block)
        type_match = TYPE_PATTERN.search(block)

        tasks.append({
            "num": task_num,
            "name": task_name,
            "block": block,
            "position": match.start(),
            "complexity": complexity_match.group(1) if complexity_match else None,
            "priority": priority_match.group(1).lower() if priority_match else None,
            "deps": deps_match.group(1).strip() if deps_match else None,
            "tc": tc_match.group(1).strip() if tc_match else None,
            "source": source_match.group(1).strip() if source_match else None,
            "type": type_match.group(1).strip() if type_match else None,
        })

    return tasks


def check_task_fields(tasks: list[dict]) -> list[tuple[str, str]]:
    """PD013-PD018: Проверить формат полей TASK-N."""
    errors = []
    seen_nums = set()

    for task in tasks:
        num = task["num"]
        prefix = f"TASK-{num}"

        # PD018: дублирование
        if num in seen_nums:
            errors.append(("PD018", f"Дубликат {prefix}"))
        seen_nums.add(num)

        # PD013: Сложность
        if task["complexity"] is None:
            errors.append(("PD015", f"{prefix}: отсутствует поле Сложность"))
        else:
            try:
                val = int(task["complexity"])
                if val < 1 or val > 10:
                    errors.append(("PD013", f"{prefix}: Сложность {val}/10 вне диапазона 1-10"))
            except ValueError:
                errors.append(("PD013", f"{prefix}: Сложность '{task['complexity']}' не является числом"))

        # PD014: Приоритет
        if task["priority"] is None:
            errors.append(("PD015", f"{prefix}: отсутствует поле Приоритет"))
        elif task["priority"] not in VALID_PRIORITIES:
            errors.append(("PD014", f"{prefix}: Приоритет '{task['priority']}', допустимые: {', '.join(sorted(VALID_PRIORITIES))}"))

        # PD015: Зависимости
        if task["deps"] is None:
            errors.append(("PD015", f"{prefix}: отсутствует поле Зависимости"))

        # PD016: TC
        if task["tc"] is None:
            errors.append(("PD015", f"{prefix}: отсутствует поле TC"))
        else:
            tc_value = task["tc"].strip()
            has_tc = bool(re.search(r'TC-\d+', tc_value))
            is_infra = tc_value.upper() == "INFRA"
            if not has_tc and not is_infra:
                errors.append(("PD016", f"{prefix}: нет TC-N или INFRA в поле TC"))

        # PD017: Источник
        if task["source"] is None:
            errors.append(("PD015", f"{prefix}: отсутствует поле Источник"))
        else:
            if not re.search(r'SVC-\d+\s*§\s*\d+', task["source"]):
                errors.append(("PD017", f"{prefix}: Источник '{task['source']}' не соответствует формату SVC-N § K"))

        # PD039: Type (опционально)
        if task["type"] is not None:
            type_val = task["type"].lower().rstrip('—').strip()
            if type_val and type_val != "—" and type_val not in VALID_TYPES:
                errors.append(("PD039", f"{prefix}: Type '{task['type']}', допустимые: {', '.join(sorted(VALID_TYPES))}"))

    return errors


def check_subtasks(tasks: list[dict]) -> list[tuple[str, str]]:
    """PD019-PD021: Проверить подзадачи."""
    errors = []

    for task in tasks:
        num = task["num"]
        prefix = f"TASK-{num}"
        block = task["block"]

        # Найти блок "Подзадачи:"
        if "Подзадачи:" not in block:
            continue

        subtask_matches = list(SUBTASK_PATTERN.finditer(block))

        # PD019: минимум 2
        if len(subtask_matches) == 1:
            errors.append(("PD019", f"{prefix}: 1 подзадача в блоке (минимум 2)"))

        for st_match in subtask_matches:
            task_part = int(st_match.group(1))
            sub_part = int(st_match.group(2))
            description = st_match.group(3)

            # PD020: нотация N.M
            if task_part != num:
                errors.append(("PD020", f"{prefix}: подзадача {task_part}.{sub_part} — номер задачи {task_part} ≠ {num}"))

            # PD021: кросс-задачные deps
            deps_in_subtask = SUBTASK_DEPS_PATTERN.search(description)
            if deps_in_subtask:
                deps_str = deps_in_subtask.group(1)
                for dep_ref in re.findall(r'(\d+)\.(\d+)', deps_str):
                    dep_task_num = int(dep_ref[0])
                    if dep_task_num != num:
                        errors.append(("PD021", f"{prefix}: подзадача {task_part}.{sub_part} ссылается на задачу {dep_task_num} (кросс-задачная зависимость)"))

    return errors


def check_infra_limit(tasks: list[dict]) -> list[tuple[str, str]]:
    """PD028: Проверить лимит INFRA задач (≤ 20%)."""
    errors = []

    if not tasks:
        return errors

    infra_count = sum(1 for t in tasks if t["tc"] and t["tc"].strip().upper() == "INFRA")
    total = len(tasks)
    limit = total * 0.2

    if infra_count > limit:
        errors.append(("PD028", f"INFRA задач: {infra_count}/{total} ({infra_count/total*100:.0f}%), макс. 20%"))

    return errors


def check_dependencies(tasks: list[dict]) -> list[tuple[str, str]]:
    """PD026, PD027: Проверить циклические зависимости и порядок."""
    errors = []

    task_map = {t["num"]: t for t in tasks}
    task_order = {t["num"]: i for i, t in enumerate(tasks)}

    # Построить граф зависимостей
    dep_graph: dict[int, list[int]] = {}
    for task in tasks:
        deps_str = task["deps"]
        if not deps_str or deps_str.strip() == "—":
            dep_graph[task["num"]] = []
            continue

        dep_nums = [int(m) for m in re.findall(r'TASK-(\d+)', deps_str)]
        dep_graph[task["num"]] = dep_nums

    # PD026: циклические зависимости (DFS)
    def has_cycle(node: int, visited: set, rec_stack: set) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for dep in dep_graph.get(node, []):
            if dep not in visited:
                if has_cycle(dep, visited, rec_stack):
                    return True
            elif dep in rec_stack:
                return True
        rec_stack.discard(node)
        return False

    visited: set[int] = set()
    for task_num in dep_graph:
        if task_num not in visited:
            if has_cycle(task_num, visited, set()):
                errors.append(("PD026", f"Циклическая зависимость обнаружена (включает TASK-{task_num})"))
                break

    # PD027: порядок (задача с deps после deps)
    for task in tasks:
        for dep in dep_graph.get(task["num"], []):
            if dep in task_order and task["num"] in task_order:
                if task_order[dep] > task_order[task["num"]]:
                    errors.append(("PD027", f"TASK-{task['num']} зависит от TASK-{dep}, но расположена раньше"))

    return errors


BLOCK_ROW_PATTERN = re.compile(
    r'\|\s*BLOCK-(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|'
)


def check_blocks(content: str, tasks: list[dict]) -> list[tuple[str, str]]:
    """PD031-PD035: Проверить секцию Блоки выполнения."""
    errors = []

    body = get_body(content)
    body_no_code = remove_code_blocks(body)
    sections = split_sections(body_no_code)

    block_section = None
    for heading, sec_content in sections:
        if "Блоки выполнения" in heading:
            block_section = sec_content
            break

    if block_section is None:
        return errors  # PD031 уже проверено в check_required_sections

    # Если заглушка — пропустить
    if "заглушка" in block_section.lower() or "нет блоков" in block_section.lower():
        return errors

    # Извлечь строки таблицы
    block_rows = list(BLOCK_ROW_PATTERN.finditer(block_section))
    if not block_rows:
        return errors

    all_task_nums = {t["num"] for t in tasks}
    tasks_in_blocks: set[int] = set()
    block_deps: dict[int, list[int]] = {}
    block_waves: dict[int, int] = {}

    for match in block_rows:
        block_num = int(match.group(1))
        tasks_str = match.group(2).strip()
        deps_str = match.group(4).strip()
        wave = int(match.group(5))

        block_waves[block_num] = wave

        # Извлечь TASK-N из блока
        task_nums_in_block = [int(m) for m in re.findall(r'TASK-(\d+)', tasks_str)]
        tasks_in_blocks.update(task_nums_in_block)

        # Зависимости между блоками
        if deps_str == "—" or deps_str == "-":
            block_deps[block_num] = []
        else:
            dep_blocks = [int(m) for m in re.findall(r'BLOCK-(\d+)', deps_str)]
            block_deps[block_num] = dep_blocks

    # PD032: каждый TASK-N принадлежит блоку
    for task_num in all_task_nums:
        if task_num not in tasks_in_blocks:
            errors.append(("PD032", f"TASK-{task_num} не принадлежит ни одному BLOCK-N"))

    # PD033: циклические зависимости между блоками
    def has_block_cycle(node: int, visited: set, rec_stack: set) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for dep in block_deps.get(node, []):
            if dep not in visited:
                if has_block_cycle(dep, visited, rec_stack):
                    return True
            elif dep in rec_stack:
                return True
        rec_stack.discard(node)
        return False

    visited_blocks: set[int] = set()
    for bn in block_deps:
        if bn not in visited_blocks:
            if has_block_cycle(bn, visited_blocks, set()):
                errors.append(("PD033", f"Циклическая зависимость между BLOCK-N (включает BLOCK-{bn})"))
                break

    # PD035: INFRA-блоки в wave 0 или 1
    infra_task_nums = {t["num"] for t in tasks if t["tc"] and t["tc"].strip().upper() == "INFRA"}
    for match in block_rows:
        block_num = int(match.group(1))
        tasks_str = match.group(2).strip()
        wave = int(match.group(5))
        task_nums_in_block = {int(m) for m in re.findall(r'TASK-(\d+)', tasks_str)}

        if task_nums_in_block & infra_task_nums and wave > 1:
            errors.append(("PD035", f"BLOCK-{block_num} содержит INFRA задачи, но wave={wave} (ожидается 0 или 1)"))

    return errors


def check_markers_and_status(content: str) -> list[tuple[str, str]]:
    """PD029: Проверить маркеры при статусе > DRAFT."""
    errors = []

    fm = parse_frontmatter(content)
    status = fm.get("status", "DRAFT")

    if status in ("DRAFT", ""):
        return errors

    body = get_body(content)

    # PD029: маркеры
    markers = re.findall(r'\[ТРЕБУЕТ УТОЧНЕНИЯ[^\]]*\]', body)
    if markers:
        errors.append(("PD029", f"Найдено {len(markers)} маркеров при статусе {status}"))

    return errors


def check_readme_registration(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Проверить регистрацию в README."""
    errors = []

    readme_path = repo_root / "specs" / "analysis" / "README.md"
    if not readme_path.exists():
        return errors

    try:
        readme_content = readme_path.read_text(encoding='utf-8')
    except Exception:
        return errors

    folder_match = FOLDER_REGEX.match(path.parent.name)
    if not folder_match:
        return errors

    folder_nnnn = folder_match.group(1)
    folder_name = path.parent.name

    if folder_nnnn not in readme_content and folder_name not in readme_content:
        errors.append(("PD024", f"Запись для '{folder_name}' не найдена в README"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_plan_dev(path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать один документ плана разработки."""
    errors = []

    if not path.exists():
        return [("PD001", f"Файл не найден: {path}")]

    # PD001: расположение
    errors.extend(check_location(path))

    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [("PD001", f"Ошибка чтения файла: {e}")]

    # PD002-PD008, PD025: frontmatter
    errors.extend(check_frontmatter(content, path, repo_root))

    # PD024: заголовок
    errors.extend(check_heading(content, path))

    # PD009, PD010, PD022, PD023: обязательные разделы
    errors.extend(check_required_sections(content))

    # PD011, PD012: per-service подсекции
    errors.extend(check_per_service_sections(content))

    # Извлечь задачи для проверки полей
    tasks = extract_tasks(content)

    # PD013-PD018: формат полей TASK-N
    errors.extend(check_task_fields(tasks))

    # PD019-PD021: подзадачи
    errors.extend(check_subtasks(tasks))

    # PD028: INFRA лимит
    errors.extend(check_infra_limit(tasks))

    # PD026-PD027: зависимости
    errors.extend(check_dependencies(tasks))

    # PD031-PD035: блоки выполнения
    errors.extend(check_blocks(content, tasks))

    # PD029: маркеры и статус
    errors.extend(check_markers_and_status(content))

    # README
    errors.extend(check_readme_registration(path, repo_root))

    return errors


def find_all_plan_devs(repo_root: Path) -> list[Path]:
    """Найти все документы плана разработки."""
    analysis_dir = repo_root / "specs" / "analysis"
    if not analysis_dir.exists():
        return []

    results = []
    for folder in sorted(analysis_dir.iterdir()):
        if folder.is_dir() and FOLDER_REGEX.match(folder.name):
            pd_file = folder / "plan-dev.md"
            if pd_file.exists():
                results.append(pd_file)
    return results


def format_output(path: Path, errors: list[tuple[str, str]], as_json: bool) -> str:
    """Форматировать вывод."""
    if as_json:
        return json.dumps({
            "file": str(path),
            "valid": len(errors) == 0,
            "errors": [{"code": code, "message": msg} for code, msg in errors]
        }, ensure_ascii=False, indent=2)

    display_name = f"{path.parent.name}/{path.name}"
    if not errors:
        return f"✅ {display_name} — валидация пройдена"

    lines = [f"❌ {display_name} — {len(errors)} ошибок:"]
    for code, msg in errors:
        lines.append(f"   {code}: {msg}")
    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация документов плана разработки SDD"
    )
    parser.add_argument("path", nargs="*", help="Путь к документу плана разработки")
    parser.add_argument("--all", action="store_true", help="Проверить все планы разработки")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))

    if args.all:
        plan_devs = find_all_plan_devs(repo_root)
        if not plan_devs:
            print("Планы разработки не найдены")
            sys.exit(0)
    elif args.path:
        plan_devs = [Path(p) for p in args.path]
    else:
        parser.print_help()
        sys.exit(2)

    all_valid = True
    results = []

    for path in plan_devs:
        errors = validate_plan_dev(path, repo_root)
        if errors:
            all_valid = False

        output = format_output(path, errors, args.json)
        results.append(output)

    if args.json:
        print("[" + ",\n".join(results) + "]")
    else:
        print("\n".join(results))

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
