#!/usr/bin/env python3
"""
Скрипт удаления архитектурного решения (ADR) по ID.

Использование:
    python scripts/decision_delete.py DEC-001
    python scripts/decision_delete.py DEC-001 --force  # без подтверждения
"""

import re
import json
import argparse
from pathlib import Path


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent
DECISIONS_DIR = PROJECT_ROOT / 'general_docs' / '04_decisions'
INDEX_FILE = DECISIONS_DIR / '000_decisions.md'
COUNTER_FILE = PROJECT_ROOT / 'general_docs' / '.doc_counter'


def load_counters():
    """Load document counters."""
    if not COUNTER_FILE.exists():
        return {"decisions": 0}
    with open(COUNTER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_counters(counters):
    """Save document counters."""
    with open(COUNTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(counters, f, indent=2, ensure_ascii=False)


def decrement_counter_if_last(dec_id):
    """Decrement counter if deleting the last created ADR."""
    # Извлекаем номер из DEC-XXX
    match = re.match(r'DEC-(\d+)', dec_id, re.IGNORECASE)
    if not match:
        return False

    try:
        id_num = int(match.group(1))
    except ValueError:
        return False

    counters = load_counters()
    current = counters.get("decisions", 0)

    # Only decrement if this was the last created ADR
    if id_num == current:
        counters["decisions"] = max(0, current - 1)
        save_counters(counters)
        return True
    return False


def find_decision_file(dec_id):
    """Найти файл ADR по ID."""
    # Поддерживаем оба формата: DEC-001 и просто 001
    if not dec_id.upper().startswith('DEC-'):
        dec_id = f"DEC-{dec_id.zfill(3)}"

    pattern = f"{dec_id}*.md"
    files = list(DECISIONS_DIR.glob(pattern))
    if files:
        return files[0]

    # Попробуем без учёта регистра
    pattern_lower = f"{dec_id.lower()}*.md"
    files = list(DECISIONS_DIR.glob(pattern_lower))
    if files:
        return files[0]

    return None


def update_index_on_delete(dec_id):
    """Обновить индекс после удаления ADR."""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Удалить строку из таблицы индекса
    # Паттерн для строки с ID (поддерживаем DEC-XXX формат)
    row_pattern = rf'\| {re.escape(dec_id)} \| \[[^\]]+\]\([^)]+\) \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \|\n?'
    content = re.sub(row_pattern, '', content, flags=re.IGNORECASE)

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


def delete_decision(dec_id, force=False):
    """Удалить ADR по ID."""
    # Нормализуем ID
    if not dec_id.upper().startswith('DEC-'):
        dec_id = f"DEC-{dec_id.zfill(3)}"
    dec_id = dec_id.upper()

    filepath = find_decision_file(dec_id)

    if not filepath:
        print(f"[ERROR] ADR {dec_id} ne nayden")
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
    update_index_on_delete(dec_id)

    # Уменьшаем счётчик если это был последний ADR
    counter_decremented = decrement_counter_if_last(dec_id)

    print(f"[OK] ADR udalen: {dec_id}")
    print(f"  Fayl: {filename}")
    if counter_decremented:
        print(f"  Counter decremented")

    return True


def main():
    parser = argparse.ArgumentParser(description='Udalit\' ADR po ID')
    parser.add_argument('dec_id', help='ID ADR (naprimer: DEC-001 ili 001)')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Udalit\' bez podtverzhdeniya')

    args = parser.parse_args()

    delete_decision(args.dec_id, args.force)


if __name__ == '__main__':
    main()
