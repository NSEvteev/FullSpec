#!/usr/bin/env python3
"""
validate-skill.py — Валидация скиллов по стандарту standard-skill.md.

Использование:
    python validate-skill.py <skill-name-or-path>
    python validate-skill.py --all
    python validate-skill.py --json <skill-name-or-path>

Примеры:
    python validate-skill.py structure-create
    python validate-skill.py .claude/skills/skill-create/SKILL.md
    python validate-skill.py --all
    python validate-skill.py --json skill-create

Возвращает:
    0 — валидация пройдена
    1 — есть ошибки
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


# =============================================================================
# Константы
# =============================================================================

SKILLS_DIR = Path(__file__).parent.parent.parent.parent / "skills"
MAX_LINES = 80

ERROR_CODES = {
    "K001": "Отсутствует `name`",
    "K002": "Неверный формат `name` (не kebab-case)",
    "K003": "Отсутствует `description`",
    "K004": "Отсутствует `allowed-tools`",
    "K005": "Description превышает 1024 символа",
    "K006": "Description слишком короткое (< 100 символов)",
    "K010": "Отсутствует заголовок H1",
    "K011": "Несколько заголовков H1",
    "K012": "Отсутствует SSOT-ссылка",
    "K013": "Отсутствует 'Формат вызова'",
    "K014": "Отсутствует 'Воркфлоу'",
    "K015": "Отсутствует 'Чек-лист'",
    "K016": "Отсутствует 'Примеры'",
    "K020": "SSOT-файл не существует",
    "K021": "Битая ссылка в чек-листе",
    "K030": "Дублирование шагов из инструкции",
    "K031": "Скилл превышает лимит строк",
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


def is_kebab_case(s: str) -> bool:
    """Проверить, что строка в kebab-case."""
    return bool(re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', s))


def parse_frontmatter(content: str) -> dict:
    """Извлечь frontmatter из markdown."""
    if not content.startswith('---'):
        return {}

    end_idx = content.find('---', 3)
    if end_idx == -1:
        return {}

    yaml_content = content[3:end_idx].strip()
    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return {}


# =============================================================================
# Проверки
# =============================================================================

def check_frontmatter(frontmatter: dict) -> list[tuple[str, str]]:
    """Проверить frontmatter скилла."""
    errors = []

    # K001, K002: name
    if not frontmatter.get('name'):
        errors.append(("K001", ERROR_CODES["K001"]))
    elif not is_kebab_case(frontmatter['name']):
        errors.append(("K002", ERROR_CODES["K002"]))

    # K003, K005, K006: description
    desc = frontmatter.get('description', '')
    if not desc:
        errors.append(("K003", ERROR_CODES["K003"]))
    else:
        desc_str = str(desc)
        if len(desc_str) > 1024:
            errors.append(("K005", f"{ERROR_CODES['K005']} ({len(desc_str)} символов)"))
        elif len(desc_str) < 100:
            errors.append(("K006", f"{ERROR_CODES['K006']} ({len(desc_str)} символов)"))

    # K004: allowed-tools
    if not frontmatter.get('allowed-tools'):
        errors.append(("K004", ERROR_CODES["K004"]))

    return errors


def check_structure(content: str) -> list[tuple[str, str]]:
    """Проверить структуру скилла."""
    errors = []

    # Получить body после frontmatter
    body = content
    if content.startswith('---'):
        end_idx = content.find('---', 3)
        if end_idx != -1:
            body = content[end_idx + 3:]

    # K010, K011: H1 заголовок
    h1_count = len(re.findall(r'^# [^#]', body, re.MULTILINE))
    if h1_count == 0:
        errors.append(("K010", ERROR_CODES["K010"]))
    elif h1_count > 1:
        errors.append(("K011", ERROR_CODES["K011"]))

    # K012: SSOT-ссылка
    if '**SSOT:**' not in body:
        errors.append(("K012", ERROR_CODES["K012"]))

    # K013-K016: обязательные секции
    if '## Формат вызова' not in body:
        errors.append(("K013", ERROR_CODES["K013"]))
    if '## Воркфлоу' not in body:
        errors.append(("K014", ERROR_CODES["K014"]))
    if '## Чек-лист' not in body:
        errors.append(("K015", ERROR_CODES["K015"]))
    if '## Примеры' not in body:
        errors.append(("K016", ERROR_CODES["K016"]))

    return errors


def check_links(content: str, skill_path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Проверить ссылки в скилле."""
    errors = []

    # Найти SSOT-ссылку
    ssot_match = re.search(r'\*\*SSOT:\*\*\s*\[.*?\]\((.*?)\)', content)
    if ssot_match:
        ssot_path = ssot_match.group(1)
        if ssot_path.startswith('/'):
            ssot_full_path = repo_root / ssot_path.lstrip('/')
        else:
            ssot_full_path = skill_path.parent / ssot_path

        if not ssot_full_path.exists():
            errors.append(("K020", f"{ERROR_CODES['K020']}: {ssot_path}"))

    return errors


def check_size(content: str) -> list[tuple[str, str]]:
    """Проверить размер скилла."""
    errors = []
    line_count = len(content.split('\n'))

    if line_count > MAX_LINES:
        errors.append(("K031", f"Скилл {line_count} строк (макс {MAX_LINES})"))

    return errors


# =============================================================================
# Основные функции
# =============================================================================

def validate_skill(skill_path: Path, repo_root: Path) -> list[tuple[str, str]]:
    """Валидировать один скилл."""
    errors = []

    if not skill_path.exists():
        return [("K000", f"Файл не найден: {skill_path}")]

    try:
        content = skill_path.read_text(encoding='utf-8')
    except Exception as e:
        return [("K000", f"Ошибка чтения файла: {e}")]

    # Парсинг frontmatter
    frontmatter = parse_frontmatter(content)

    # Все проверки
    errors.extend(check_frontmatter(frontmatter))
    errors.extend(check_structure(content))
    errors.extend(check_links(content, skill_path, repo_root))
    errors.extend(check_size(content))

    return errors


def find_all_skills(skills_dir: Path) -> list[Path]:
    """Найти все скиллы."""
    skills = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.endswith('_old'):
            skill_file = skill_dir / 'SKILL.md'
            if skill_file.exists():
                skills.append(skill_file)
    return sorted(skills)


def format_output(name: str, errors: list[tuple[str, str]], line_count: int, as_json: bool) -> str:
    """Форматировать вывод."""
    if as_json:
        return json.dumps({
            "skill": name,
            "valid": len(errors) == 0,
            "lines": line_count,
            "errors": [{"code": code, "message": msg} for code, msg in errors]
        }, ensure_ascii=False, indent=2)

    if not errors:
        return f"✅ {name} — валидация пройдена ({line_count} строк)"

    lines = [f"❌ {name} — {len(errors)} ошибок:"]
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
        description="Валидация скиллов по стандарту"
    )
    parser.add_argument("skill", nargs="*", help="Имя скилла или путь к SKILL.md (можно несколько)")
    parser.add_argument("--all", action="store_true", help="Проверить все скиллы")
    parser.add_argument("--json", action="store_true", help="JSON вывод")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__))

    if args.all:
        skills = find_all_skills(SKILLS_DIR)
        if not skills:
            print("Скиллы не найдены")
            sys.exit(1)
    elif args.skill:
        skills = []
        for skill_arg in args.skill:
            # Определить: путь или имя
            if '/' in skill_arg or '\\' in skill_arg or skill_arg.endswith('.md'):
                # Это путь к файлу
                skill_path = Path(skill_arg)
                if not skill_path.is_absolute():
                    skill_path = repo_root / skill_path
                skills.append(skill_path)
            else:
                # Это имя скилла
                skills.append(SKILLS_DIR / skill_arg / 'SKILL.md')
    else:
        parser.print_help()
        sys.exit(2)

    all_valid = True
    results = []

    for skill_path in skills:
        skill_name = skill_path.parent.name
        errors = validate_skill(skill_path, repo_root)

        if errors:
            all_valid = False

        # Подсчёт строк
        try:
            line_count = len(skill_path.read_text(encoding='utf-8').split('\n'))
        except Exception:
            line_count = 0

        output = format_output(skill_name, errors, line_count, args.json)
        results.append(output)

    if args.json:
        print("[" + ",\n".join(results) + "]")
    else:
        print("\n".join(results))

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
