#!/usr/bin/env python3
"""
Скрипт удаления ресурса по ID.

Использование:
    python scripts/resource_delete.py 001
    python scripts/resource_delete.py 001 --force  # без подтверждения
    python scripts/resource_delete.py 001 -t backend  # указать тип для ускорения поиска
"""

import re
import json
import argparse
from pathlib import Path


# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent
RESOURCES_DIR = PROJECT_ROOT / 'general_docs' / '05_resources'
COUNTER_FILE = PROJECT_ROOT / 'general_docs' / '.doc_counter'

# Допустимые типы ресурсов
VALID_TYPES = ['database', 'backend', 'frontend', 'infra']


def load_counters():
    """Load document counters."""
    if not COUNTER_FILE.exists():
        return {"resources": 0}
    with open(COUNTER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_counters(counters):
    """Save document counters."""
    with open(COUNTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(counters, f, indent=2, ensure_ascii=False)


def decrement_counter_if_last(res_id):
    """Decrement counter if deleting the last created resource."""
    try:
        id_num = int(res_id)
    except ValueError:
        return False

    counters = load_counters()
    current = counters.get("resources", 0)

    # Only decrement if this was the last created resource
    if id_num == current:
        counters["resources"] = max(0, current - 1)
        save_counters(counters)
        return True
    return False


def find_resource_file(res_id, res_type=None):
    """Найти файл ресурса по ID."""
    # Нормализуем ID
    res_id = res_id.zfill(3)

    # Если указан тип, ищем только в этой папке
    if res_type:
        type_dir = RESOURCES_DIR / res_type
        if type_dir.exists():
            pattern = f"{res_id}_*.md"
            files = list(type_dir.glob(pattern))
            if files:
                return files[0], res_type

    # Ищем во всех подпапках
    for t in VALID_TYPES:
        type_dir = RESOURCES_DIR / t
        if type_dir.exists():
            pattern = f"{res_id}_*.md"
            files = list(type_dir.glob(pattern))
            if files:
                return files[0], t

    return None, None


def update_index_on_delete(res_id, res_type, filename):
    """Обновить индекс после удаления ресурса."""
    index_file = RESOURCES_DIR / res_type / f'000_{res_type}.md'

    if not index_file.exists():
        return

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Удалить строку из таблицы индекса
    # Паттерн для строки с файлом
    row_pattern = rf'\| \[[^\]]+\]\({re.escape(filename)}\) \| [^|]+ \| [^|]+ \| [^|]+ \|\n?'
    content = re.sub(row_pattern, '', content)

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)


def delete_resource(res_id, res_type=None, force=False):
    """Удалить ресурс по ID."""
    # Нормализуем ID
    res_id_norm = res_id.zfill(3)

    filepath, found_type = find_resource_file(res_id, res_type)

    if not filepath:
        print(f"[ERROR] Resurs {res_id} ne nayden")
        if not res_type:
            print("Podskazka: ukazhite tip resursa s -t (database/backend/frontend/infra)")
        return False

    filename = filepath.name

    if not force:
        confirm = input(f"Udalit' {found_type}/{filename}? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Otmeneno")
            return False

    # Удаляем файл
    filepath.unlink()

    # Обновляем индекс
    update_index_on_delete(res_id_norm, found_type, filename)

    # Уменьшаем счётчик если это был последний ресурс
    counter_decremented = decrement_counter_if_last(res_id_norm)

    print(f"[OK] Resurs udalen: {res_id}")
    print(f"  Fayl: {found_type}/{filename}")
    if counter_decremented:
        print(f"  Counter decremented")

    return True


def main():
    parser = argparse.ArgumentParser(description='Udalit\' resurs po ID')
    parser.add_argument('res_id', help='ID resursa (naprimer: 001)')
    parser.add_argument('-t', '--type', choices=VALID_TYPES,
                        help='Tip resursa (dlya uskoreniya poiska)')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Udalit\' bez podtverzhdeniya')

    args = parser.parse_args()

    delete_resource(args.res_id, args.type, args.force)


if __name__ == '__main__':
    main()
