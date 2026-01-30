#!/usr/bin/env python3
"""
list-rules.py — Список всех rules с описаниями.

Сканирует /.claude/rules/ и выводит информацию о каждом rule.

Использование:
    python list-rules.py [--json] [--repo <dir>]

Примеры:
    python list-rules.py
    python list-rules.py --json
    python list-rules.py --repo /path/to/repo

Возвращает:
    0 — успех
    1 — ошибка
"""

import argparse
import json
import re
import sys
from pathlib import Path


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
    current_value = []

    for line in match.group(1).split('\n'):
        # Проверка на новый ключ
        if ':' in line and not line.startswith(' ') and not line.startswith('-'):
            # Сохранить предыдущий ключ
            if current_key:
                result[current_key] = '\n'.join(current_value).strip()

            key, value = line.split(':', 1)
            current_key = key.strip()
            current_value = [value.strip()] if value.strip() else []
        elif current_key:
            # Продолжение значения (массив или многострочное)
            current_value.append(line.strip())

    # Сохранить последний ключ
    if current_key:
        result[current_key] = '\n'.join(current_value).strip()

    return result


def parse_paths_array(value: str) -> list[str] | None:
    """Распарсить массив paths из frontmatter."""
    if not value:
        return None

    # Убрать пробелы и переносы
    value = value.replace('\n', ' ')

    # Паттерн для массива YAML
    # Формат: - "pattern" или - pattern
    patterns = re.findall(r'-\s*["\']?([^"\'\n]+)["\']?', value)

    if patterns:
        return [p.strip() for p in patterns]

    return None


def check_paths_overlap(paths1: list[str] | None, paths2: list[str] | None) -> bool:
    """Проверить пересечение paths (упрощённая проверка)."""
    if not paths1 or not paths2:
        return False

    # Упрощённая проверка: точное совпадение паттернов
    return bool(set(paths1) & set(paths2))


# =============================================================================
# Основная логика
# =============================================================================

def list_rules(repo_root: Path, json_output: bool = False) -> bool:
    """Список всех rules."""
    rules_dir = repo_root / ".claude" / "rules"

    if not rules_dir.exists():
        if json_output:
            print(json.dumps({"error": "Директория /.claude/rules/ не найдена"}))
        else:
            print("ℹ️  Директория /.claude/rules/ не найдена")
        return True

    rule_files = sorted(rules_dir.glob("*.md"))

    if not rule_files:
        if json_output:
            print(json.dumps({"rules": []}))
        else:
            print("ℹ️  Rules не найдены в /.claude/rules/")
        return True

    rules_data = []

    for rule_file in rule_files:
        try:
            content = rule_file.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)

            description = fm.get("description", "")
            paths_value = fm.get("paths", "")
            paths = parse_paths_array(paths_value)

            rule_type = "conditional" if paths else "global"

            rules_data.append({
                "file": rule_file.stem,
                "description": description,
                "type": rule_type,
                "paths": paths or [],
            })

        except Exception as e:
            if json_output:
                rules_data.append({
                    "file": rule_file.stem,
                    "error": str(e),
                })
            else:
                print(f"⚠️  Ошибка чтения {rule_file.name}: {e}")

    if json_output:
        print(json.dumps({"rules": rules_data}, ensure_ascii=False, indent=2))
    else:
        # Вывод таблицы
        print(f"Найдено rules: {len(rules_data)}\n")
        print("| Rule | Type | Paths | Description |")
        print("|------|------|-------|-------------|")

        for rule in rules_data:
            if "error" in rule:
                print(f"| {rule['file']} | ERROR | — | {rule['error']} |")
            else:
                paths_str = ", ".join(rule['paths']) if rule['paths'] else "—"
                print(f"| {rule['file']}.md | {rule['type']} | {paths_str} | {rule['description']} |")

        # Проверка пересечений paths
        print()
        overlaps_found = False

        for i, rule1 in enumerate(rules_data):
            if "error" in rule1:
                continue

            for rule2 in rules_data[i + 1:]:
                if "error" in rule2:
                    continue

                if check_paths_overlap(rule1.get('paths'), rule2.get('paths')):
                    if not overlaps_found:
                        print("⚠️  WARNING: Обнаружены пересечения paths:")
                        overlaps_found = True

                    paths1_str = ", ".join(rule1['paths'])
                    paths2_str = ", ".join(rule2['paths'])
                    print(f"   - {rule1['file']}.md ({paths1_str}) ↔ {rule2['file']}.md ({paths2_str})")

        if not overlaps_found:
            print("✅ Пересечений paths не обнаружено")

    return True


def main():
    """Точка входа."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Список всех rules с описаниями"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Корень репозитория (по умолчанию: текущая папка)"
    )

    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    success = list_rules(repo_root, args.json)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
