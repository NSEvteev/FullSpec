#!/usr/bin/env python3
"""
Хук SubagentStart: записывает статус агента при запуске.

Входные данные (stdin JSON):
- agent_id: уникальный ID субагента
- agent_type: тип агента (Explore, Bash, кастомный)
- agent_transcript_path: путь к транскрипту (опционально)

SSOT: /.claude/.instructions/state/standard-state.md
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    # Читаем JSON из stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    agent_id = input_data.get("agent_id")
    agent_type = input_data.get("agent_type", "unknown")

    if not agent_id:
        print("Error: agent_id is required", file=sys.stderr)
        sys.exit(1)

    # Путь к agents-status.json
    script_dir = Path(__file__).parent
    state_file = script_dir.parent / "state" / "agents-status.json"

    if not state_file.exists():
        print(f"Error: {state_file} not found", file=sys.stderr)
        sys.exit(1)

    # Читаем текущий state
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {state_file}: {e}", file=sys.stderr)
        sys.exit(1)

    # Добавляем запись об агенте
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    state.setdefault("agents", {})[agent_id] = {
        "status": "running",
        "agent_type": agent_type,
        "started_at": now,
        "finished_at": None,
        "task": "",  # Агент обновит позже
        "working_on": [],  # Агент обновит позже
    }

    # Записываем обратно
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Agent {agent_id} ({agent_type}) registered as running")


if __name__ == "__main__":
    main()
