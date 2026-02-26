#!/usr/bin/env python3
"""
extract-svc-context.py — Извлечение контекста сервисов из design.md для review.md.

Парсит блоки SVC-N из design.md: для каждого сервиса определяет затронутые секции
(§§ 1-9), criticality level и технологии. Выводит структуру для заполнения
секции "Контекст ревью" в review.md при /review-create.

Использование:
    python extract-svc-context.py <design-path> [--json] [--repo <dir>]

Аргументы:
    design-path     Путь к design.md (specs/analysis/NNNN-{topic}/design.md)

Примеры:
    python extract-svc-context.py specs/analysis/0001-oauth2-authorization/design.md
    python extract-svc-context.py specs/analysis/0001-oauth2/design.md --json

Возвращает:
    0 — успех
    1 — ошибка (файл не найден, неверный формат)
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Константы
# =============================================================================

# Заголовок SVC-N блока: ## SVC-1: ServiceName или ## SVC-1: ServiceName (critical-high)
SVC_HEADING_REGEX = re.compile(
    r'^## (SVC-\d+):\s+(\S+)(?:\s+\(critical-(\w+)\))?',
    re.MULTILINE
)

# Заголовок подсекции § N внутри SVC блока: ### § 1 или ### 1.
SECTION_HEADING_REGEX = re.compile(
    r'^### (?:§\s*)?(\d+)[.\s]',
    re.MULTILINE
)

# Упоминание технологий в тексте (из § 5 Code Map)
TECH_PATTERN = re.compile(
    r'\b(Python|TypeScript|JavaScript|Go|Rust|Java|Kotlin|PostgreSQL|MySQL|Redis|'
    r'MongoDB|Elasticsearch|Kafka|RabbitMQ|gRPC|REST|GraphQL|FastAPI|Django|'
    r'Flask|Spring|Express|NestJS|React|Vue|Angular|Docker|Kubernetes|Nginx)\b',
    re.IGNORECASE
)

# Секции с именами для вывода
SECTION_NAMES = {
    "1": "Назначение и критичность",
    "2": "API контракты",
    "3": "Data Model",
    "4": "Потоки данных",
    "5": "Code Map",
    "6": "Зависимости",
    "7": "Доменная модель",
    "8": "Границы автономии LLM",
    "9": "Planned Changes",
}

# Секции, важные для ревью (всегда включать если есть)
REVIEW_KEY_SECTIONS = {"2", "3", "8", "9"}


# =============================================================================
# Функции
# =============================================================================

def find_repo_root(start_path: Path) -> Path:
    """Найти корень репозитория (папка с .git)."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def get_svc_blocks(content: str) -> list[dict]:
    """Извлечь блоки SVC-N из design.md."""
    body = re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)

    # Найти все заголовки SVC-N
    svc_matches = list(SVC_HEADING_REGEX.finditer(body))
    if not svc_matches:
        return []

    blocks = []
    for i, match in enumerate(svc_matches):
        svc_id = match.group(1)       # SVC-1
        svc_name = match.group(2)     # ServiceName
        criticality = match.group(3)  # high, medium, low (или None)

        # Границы блока
        start = match.end()
        end = svc_matches[i + 1].start() if i + 1 < len(svc_matches) else len(body)
        block_text = body[start:end]

        # Найти подсекции §§
        sections = SECTION_HEADING_REGEX.findall(block_text)

        # Найти технологии
        techs = set(TECH_PATTERN.findall(block_text))
        # Нормализовать регистр
        techs = {t.lower() for t in techs}

        blocks.append({
            "id": svc_id,
            "name": svc_name,
            "criticality": criticality or "medium",
            "sections": sorted(set(sections)),
            "technologies": sorted(techs),
        })

    return blocks


def get_global_technologies(content: str) -> list[str]:
    """Найти технологии, упомянутые глобально (вне SVC блоков)."""
    body = re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)

    # Убрать SVC блоки
    body_no_svc = SVC_HEADING_REGEX.sub('', body)
    techs = TECH_PATTERN.findall(body_no_svc)
    return sorted({t.lower() for t in techs})


def format_text_output(blocks: list[dict], global_techs: list[str], branch: str) -> str:
    """Форматировать вывод в текстовом виде для вставки в review.md."""
    lines = []

    for block in blocks:
        svc = block["name"]
        criticality = block["criticality"]
        sections = block["sections"]

        lines.append(f"### {svc} (critical-{criticality})")
        lines.append("")
        lines.append("| Секция | Путь | Что проверяем |")
        lines.append("|--------|------|----------------|")

        for section_num in sections:
            section_name = SECTION_NAMES.get(section_num, f"§ {section_num}")
            anchor = section_name.lower().replace(" ", "-").replace("/", "")
            # Для ключевых секций — добавить маркер
            marker = " (**эталон P1**)" if section_num == "9" else ""
            lines.append(
                f"| § {section_num} {section_name} "
                f"| `specs/docs/{svc}.md#{anchor}` "
                f"| Planned Changes{marker if section_num == '9' else ''} |"
            )

        lines.append("")
        lines.append("*Незатронутые секции не включаются.*")
        lines.append("")

    # Технологии
    all_techs = set()
    for block in blocks:
        all_techs.update(block["technologies"])
    all_techs.update(global_techs)

    if all_techs:
        lines.append("### Tech-стандарты")
        lines.append("")
        lines.append("| Технология | Стандарт |")
        lines.append("|------------|----------|")
        for tech in sorted(all_techs):
            lines.append(f"| {tech} | `specs/docs/.technologies/standard-{tech}.md` |")
        lines.append("")

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
        description="Извлечение контекста сервисов из design.md для review.md"
    )
    parser.add_argument("design_path", help="Путь к design.md")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    design_path = Path(args.design_path)
    if not design_path.is_absolute():
        design_path = repo_root / design_path

    if not design_path.exists():
        print(f"❌ design.md не найден: {design_path}", file=sys.stderr)
        sys.exit(1)

    if design_path.name != "design.md":
        print(f"❌ Ожидается файл design.md, получен: {design_path.name}", file=sys.stderr)
        sys.exit(1)

    try:
        content = design_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}", file=sys.stderr)
        sys.exit(1)

    blocks = get_svc_blocks(content)
    global_techs = get_global_technologies(content)
    branch = design_path.parent.name

    if not blocks:
        print("⚠️  SVC-N блоки не найдены в design.md", file=sys.stderr)
        sys.exit(1)

    if args.json:
        result = {
            "branch": branch,
            "services": blocks,
            "global_technologies": global_techs,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"# Контекст ревью для ветки {branch}")
        print(f"# Сервисов: {len(blocks)}")
        print()
        print(format_text_output(blocks, global_techs, branch))

    sys.exit(0)


if __name__ == "__main__":
    main()
