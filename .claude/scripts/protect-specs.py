#!/usr/bin/env python3
"""
Hook для блокировки прямого редактирования файлов в /specs/.
Все изменения в /specs/ должны идти через скиллы: /spec-create, /spec-update, /spec-status.

Exit codes:
  0 - разрешить операцию
  2 - заблокировать операцию
"""
import json
import sys

# Читаем данные из stdin
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)  # Если не можем распарсить — пропускаем

# Получаем путь к файлу
file_path = data.get('tool_input', {}).get('file_path', '')

# Запрещённые папки (разные форматы путей)
forbidden_paths = ['/specs/', '\\specs\\', '/specs\\', '\\specs/']

# Проверяем наличие запрещённых путей
if any(forbidden in file_path for forbidden in forbidden_paths):
    print("❌ Прямое редактирование файлов в /specs/ запрещено", file=sys.stderr)
    print(f"   Файл: {file_path}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Используй скиллы:", file=sys.stderr)
    print("  /spec-create — создание документов", file=sys.stderr)
    print("  /spec-update — редактирование", file=sys.stderr)
    print("  /spec-status — изменение статуса", file=sys.stderr)
    sys.exit(2)  # Блокировать операцию

sys.exit(0)  # Разрешить операцию
