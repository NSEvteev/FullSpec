#!/usr/bin/env python3
"""
Скрипт удаления дискуссии по ID.

Использование:
    python scripts/discuss_delete.py 001
    python scripts/discuss_delete.py 001 --force  # без подтверждения
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent
DISCUSS_DIR = PROJECT_ROOT / 'general_docs' / '01_discuss'
INDEX_FILE = DISCUSS_DIR / '000_discuss.md'
COUNTER_FILE = PROJECT_ROOT / 'general_docs' / '.doc_counter'


def load_counters():
    """Load document counters."""
    if not COUNTER_FILE.exists():
        return {"discuss": 0}
    with open(COUNTER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_counters(counters):
    """Save document counters."""
    with open(COUNTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(counters, f, indent=2, ensure_ascii=False)


def decrement_counter_if_last(discuss_id):
    """Decrement counter if deleting the last created discussion."""
    try:
        id_num = int(discuss_id)
    except ValueError:
        return False

    counters = load_counters()
    current = counters.get("discuss", 0)

    # Only decrement if this was the last created discussion
    if id_num == current:
        counters["discuss"] = max(0, current - 1)
        save_counters(counters)
        return True
    return False


def find_discussion_file(discuss_id):
    """Найти файл дискуссии по ID."""
    pattern = f"{discuss_id}_*.md"
    files = list(DISCUSS_DIR.glob(pattern))
    if files:
        return files[0]
    return None


def update_index_on_delete(discuss_id, filename):
    """Обновить индекс после удаления дискуссии."""
    today = datetime.now().strftime('%Y-%m-%d')

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Удалить строку из таблицы индекса
    # Паттерн для строки с ID
    row_pattern = rf'\| {discuss_id} \| \[[^\]]+\]\([^)]+\) \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \|\n?'
    content = re.sub(row_pattern, '', content)

    # 2. Обновить статистику draft (уменьшить на 1)
    content = re.sub(
        r'\| draft \| (\d+) \|',
        lambda m: f'| draft | {max(0, int(m.group(1)) - 1)} |',
        content
    )

    # 3. Обновить всего (уменьшить на 1)
    content = re.sub(
        r'\| \*\*Всего\*\* \| \*\*(\d+)\*\* \|',
        lambda m: f'| **Всего** | **{max(0, int(m.group(1)) - 1)}** |',
        content
    )

    # 4. Обновить дату
    content = re.sub(
        r'\*\*Последнее обновление:\*\* \d{4}-\d{2}-\d{2}',
        f'**Последнее обновление:** {today}',
        content
    )

    # 5. Обновить быстрый поиск по статусу draft
    # Убрать ссылку на удалённую дискуссию
    slug = filename.replace('.md', '')
    content = re.sub(
        rf'- \*\*draft\*\* \((\d+)\) — новые идеи и предложения: \[{slug}\]\({filename}\)',
        lambda m: f'- **draft** ({max(0, int(m.group(1)) - 1)}) — новые идеи и предложения',
        content
    )

    # 6. Обновить "По дате" если там была эта дискуссия
    content = re.sub(
        rf'- \*\*Последние обновления:\*\* \[{slug}\]\({filename}\)',
        '- **Последние обновления:** —',
        content
    )
    content = re.sub(
        rf'- \*\*Недавно созданные:\*\* \[{slug}\]\({filename}\)',
        '- **Недавно созданные:** —',
        content
    )

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


def delete_discussion(discuss_id, force=False):
    """Удалить дискуссию по ID."""
    filepath = find_discussion_file(discuss_id)

    if not filepath:
        print(f"[ERROR] Diskussiya {discuss_id} ne naydena")
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
    update_index_on_delete(discuss_id, filename)

    # Уменьшаем счётчик если это была последняя дискуссия
    counter_decremented = decrement_counter_if_last(discuss_id)

    print(f"[OK] Diskussiya udalena: {discuss_id}")
    print(f"  Fayl: {filename}")
    if counter_decremented:
        print(f"  Counter decremented")

    return True


def main():
    parser = argparse.ArgumentParser(description='Udalit\' diskussiyu po ID')
    parser.add_argument('discuss_id', help='ID diskussii (naprimer: 001)')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Udalit\' bez podtverzhdeniya')

    args = parser.parse_args()

    delete_discussion(args.discuss_id, args.force)


if __name__ == '__main__':
    main()
