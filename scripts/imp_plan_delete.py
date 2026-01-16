#!/usr/bin/env python3
"""
Скрипт удаления плана реализации по ID.

Использование:
    python scripts/imp_plan_delete.py 001
    python scripts/imp_plan_delete.py 001 --force  # без подтверждения
"""

import re
import json
import argparse
from pathlib import Path


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent
PLANS_DIR = PROJECT_ROOT / 'general_docs' / '06_imp_plans'
INDEX_FILE = PLANS_DIR / '000_imp_plans.md'
COUNTER_FILE = PROJECT_ROOT / 'general_docs' / '.doc_counter'


def load_counters():
    """Load document counters."""
    if not COUNTER_FILE.exists():
        return {"imp_plans": 0}
    with open(COUNTER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_counters(counters):
    """Save document counters."""
    with open(COUNTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(counters, f, indent=2, ensure_ascii=False)


def decrement_counter_if_last(plan_id):
    """Decrement counter if deleting the last created plan."""
    try:
        id_num = int(plan_id)
    except ValueError:
        return False

    counters = load_counters()
    current = counters.get("imp_plans", 0)

    # Only decrement if this was the last created plan
    if id_num == current:
        counters["imp_plans"] = max(0, current - 1)
        save_counters(counters)
        return True
    return False


def find_plan_file(plan_id):
    """Найти файл плана по ID."""
    # Нормализуем ID
    plan_id = plan_id.zfill(3)

    pattern = f"{plan_id}_plan_*.md"
    files = list(PLANS_DIR.glob(pattern))
    if files:
        return files[0]

    # Попробуем без _plan_
    pattern_alt = f"{plan_id}_*.md"
    files = list(PLANS_DIR.glob(pattern_alt))
    if files:
        return files[0]

    return None


def update_index_on_delete(plan_id):
    """Обновить индекс после удаления плана."""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Удалить строку из таблицы индекса
    # Паттерн для строки с ID
    row_pattern = rf'\| {plan_id} \| \[[^\]]+\]\([^)]+\) \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \|\n?'
    content = re.sub(row_pattern, '', content)

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


def delete_plan(plan_id, force=False):
    """Удалить план по ID."""
    # Нормализуем ID
    plan_id_norm = plan_id.zfill(3)

    filepath = find_plan_file(plan_id)

    if not filepath:
        print(f"[ERROR] Plan {plan_id} ne nayden")
        return False

    filename = filepath.name

    if not force:
        confirm = input(f"Udalit' {filename}? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Otmeneno")
            return False

    # Удаляем файл
    filepath.unlink()

    # Обновляем индекс
    update_index_on_delete(plan_id_norm)

    # Уменьшаем счётчик если это был последний план
    counter_decremented = decrement_counter_if_last(plan_id_norm)

    print(f"[OK] Plan udalen: {plan_id}")
    print(f"  Fayl: {filename}")
    if counter_decremented:
        print(f"  Counter decremented")

    return True


def main():
    parser = argparse.ArgumentParser(description='Udalit\' plan po ID')
    parser.add_argument('plan_id', help='ID plana (naprimer: 001)')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Udalit\' bez podtverzhdeniya')

    args = parser.parse_args()

    delete_plan(args.plan_id, args.force)


if __name__ == '__main__':
    main()
